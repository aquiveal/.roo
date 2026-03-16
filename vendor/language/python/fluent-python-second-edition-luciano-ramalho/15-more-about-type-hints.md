# @Domain

This rule file activates when the AI is tasked with advanced Python type hinting, specifically involving overloaded function signatures, mapping type hints (e.g., `TypedDict`), type casting, runtime extraction of annotations, generic classes, type variance (invariance, covariance, contravariance), and generic static protocols. 

# @Vocabulary

- **Gradual Typing**: A type system where type hints are optional, do not catch errors at runtime, and do not enhance performance, but are utilized by static analyzers (like Mypy) to detect potential bugs.
- **Overload**: Defining multiple signatures for a single function using the `@typing.overload` decorator to reflect different combinations of parameter types and their corresponding return types.
- **TypedDict**: A typing construct that provides class-like syntax to annotate dictionaries with a fixed set of string keys and specific types for each value. It has no runtime effect and acts as a placebo during execution.
- **Type Casting**: Utilizing the `typing.cast()` function to silence spurious type checker warnings by signaling that a value has a specific type, without performing any actual runtime checks.
- **Generic Type**: A type declared with one or more type variables (e.g., `LottoBlower[T]`).
- **Formal Type Parameter**: The specific type variables that appear in a generic type declaration (e.g., the `T` in `Generic[T]`).
- **Parameterized Type**: A generic type declared with actual type parameters (e.g., `LottoBlower[int]`).
- **Actual Type Parameter**: The concrete types provided when a generic type is parameterized (e.g., the `int` in `LottoBlower[int]`).
- **Invariant Type**: A generic type parameter where there is no supertype or subtype relationship between parameterized types (e.g., `list[int]` is neither a supertype nor a subtype of `list[float]`).
- **Covariant Type**: A generic type parameter that preserves the subtype relationship of its actual type parameters. Indicated by `covariant=True` in `TypeVar`.
- **Contravariant Type**: A generic type parameter that reverses the subtype relationship of its actual type parameters. Indicated by `contravariant=True` in `TypeVar`.
- **Static Protocol**: A structural type (interface) defined by subclassing `typing.Protocol` that can be verified by static type checkers.

# @Objectives

- Provide precise, expressive type hints for functions where return types depend dynamically on the types of the arguments provided.
- Ensure correct and strictly bounded type variance based on data flow (whether data is entering or exiting an object).
- Prevent a false sense of security when dealing with dynamic data (like JSON API responses) by explicitly separating static type hints from runtime validation.
- Abstract and safeguard the extraction of runtime type annotations to prevent system breakage due to Python's evolving annotation evaluation rules (e.g., PEP 563, PEP 649).
- Guide static type checkers using explicit, non-contagious methods rather than blindly suppressing errors.

# @Guidelines

- **Overloaded Signatures**: 
  - When encountering functions where the return type varies based on the combination of parameter types (e.g., `max()` or `sum()`), the AI MUST use the `@typing.overload` decorator to declare each signature combination.
  - The AI MUST write the body of all `@overload` decorated signatures using only an ellipsis (`...`).
  - The AI MUST define the actual runtime implementation of the function immediately following the `@overload` signatures.
  - The AI MUST NOT include type hints on the implementation signature itself if the overloads comprehensively cover the typing definitions.

- **TypedDict and Dynamic Data**:
  - When encountering JSON parsing or dynamic dict-based record creation, the AI MUST NOT rely on `typing.TypedDict` as a mechanism for runtime data validation.
  - If the user requires safe runtime handling of dynamic structures that map to typed fields, the AI MUST recommend or implement a runtime validation tool (e.g., the `pydantic` package). `TypedDict` MUST only be used strictly for static analysis tooling.

- **Type Casting**:
  - When encountering an unavoidable type checker warning that is a false positive or stems from an outdated stub file, the AI MUST use `typing.cast(TargetType, value)` rather than applying `# type: ignore` or assigning the `Any` type.
  - The AI MUST restrict the use of `typing.cast()` to a last resort. Pervasive use of `cast()` is a code smell indicating a flawed type hierarchy.

- **Reading Annotations at Runtime**:
  - When encountering tasks that require inspecting type hints at runtime, the AI MUST NOT read the `__annotations__` attribute directly.
  - The AI MUST use `inspect.get_annotations()` (for Python 3.10+) or `typing.get_type_hints()` (for Python 3.5 to 3.9).
  - The AI MUST wrap the extraction logic inside a custom, localized helper method or function to protect the wider codebase from future changes in Python's annotation evaluation behavior.

- **Defining Generic Classes**:
  - When encountering a class that operates on items of arbitrary types, the AI MUST subclass `typing.Generic[T]` (where `T` is defined via `TypeVar`).

- **Applying Type Variance**:
  - *Covariant (Outputs)*: When encountering a formal type parameter that defines data that ONLY comes *out* of an object (e.g., return types, Iterators, read-only containers), the AI MUST define the `TypeVar` with `covariant=True` (e.g., `T_co = TypeVar('T_co', covariant=True)`).
  - *Contravariant (Inputs)*: When encountering a formal type parameter that defines data that ONLY goes *into* an object after initialization (e.g., arguments to `.send()`, write-only sinks), the AI MUST define the `TypeVar` with `contravariant=True` (e.g., `T_contra = TypeVar('T_contra', contravariant=True)`).
  - *Invariant (Inputs & Outputs)*: When encountering a formal type parameter that represents data that both goes *into* and comes *out* of an object (e.g., mutable collections like `list`), the AI MUST define the `TypeVar` as invariant (omitting kwargs). To err on the safe side, the AI MUST default to invariant.

- **Generic Static Protocols**:
  - When defining a formal interface for structural typing (static duck typing), the AI MUST subclass `typing.Protocol` (or `typing.Protocol[T]` if it is generic). 
  - The AI MUST properly assign variance to the generic parameter of the `Protocol` depending on how the protocol's methods utilize the parameter (e.g., covariant if the protocol only yields/returns the type).

# @Workflow

1. **Analyze Interface Flexibility**: Evaluate the target function or class to determine if it handles multiple types dynamically.
2. **Apply Overloads if Necessary**: If a function's return type is conditionally tied to specific input types, write stacked `@overload` signatures for each case. Ensure the final implementation `def` is untyped.
3. **Determine Validation Needs**: If dealing with structured dictionaries (e.g., JSON), define a `TypedDict` for static validation. Immediately establish whether runtime validation is required, and integrate an active validation library (like `pydantic`) if it is.
4. **Abstract Runtime Introspection**: If the code must inspect types at runtime, implement a wrapper function utilizing `inspect.get_annotations` or `get_type_hints`. Do not use `.__annotations__`.
5. **Establish Generic Constraints**: If building a generic class, define the data flow of the types. 
   - Is it strictly yielded/returned? Create a covariant `TypeVar`.
   - Is it strictly consumed/passed as arguments? Create a contravariant `TypeVar`.
   - Is it mutated/both? Create an invariant `TypeVar` (default).
6. **Resolve Static Errors Safely**: Run the static checker mental model over the code. If the static checker fails on valid runtime behavior, fix the type hierarchy. If unfixable (due to external stubs), apply `typing.cast()` targeting the precise variable, avoiding `Any`.

# @Examples (Do's and Don'ts)

### Overloaded Signatures
- **[DO]**
  ```python
  from typing import overload, Union, TypeVar
  from collections.abc import Iterable
  
  T = TypeVar('T')
  S = TypeVar('S')

  @overload
  def sum(it: Iterable[T]) -> Union[T, int]: ...

  @overload
  def sum(it: Iterable[T], /, start: S) -> Union[T, S]: ...

  def sum(it, /, start=0):
      # Implementation goes here without type hints
      pass
  ```
- **[DON'T]** Mix implementations with overloads or add type hints to the actual implementation after providing overloads.
  ```python
  @overload
  def sum(it: Iterable[T]) -> Union[T, int]:
      # DON'T put implementation here
      return 0

  # DON'T type hint the implementation if overloads exist
  def sum(it: Iterable[T], start: S = 0) -> Union[T, S]: 
      pass
  ```

### Variance
- **[DO]** Use covariant TypeVars for read-only outputs (e.g., an element being yielded).
  ```python
  from typing import TypeVar, Protocol

  T_co = TypeVar('T_co', covariant=True)

  class RandomPicker(Protocol[T_co]):
      def pick(self) -> T_co: ...
  ```
- **[DON'T]** Use a covariant TypeVar for a parameter that accepts input into the object.
  ```python
  T_co = TypeVar('T_co', covariant=True)

  class TrashCan(Generic[T_co]):
      # DON'T use covariant TypeVars for arguments
      def put(self, refuse: T_co) -> None: ...
  ```

### Reading Annotations at Runtime
- **[DO]** Use standard library inspection tools wrapped in a single access point.
  ```python
  from typing import get_type_hints

  class Checked:
      @classmethod
      def _fields(cls) -> dict[str, type]:
          return get_type_hints(cls)
  ```
- **[DON'T]** Access `__annotations__` directly as it breaks with forward references and string-evaluation changes.
  ```python
  class Checked:
      @classmethod
      def _fields(cls) -> dict[str, type]:
          # DON'T do this
          return cls.__annotations__ 
  ```

### Resolving Type Checker False Positives
- **[DO]** Use `typing.cast` to give explicit guidance for a specific variable.
  ```python
  from typing import cast
  
  def get_address(server) -> str:
      socket_list = cast(tuple[TransportSocket, ...], server.sockets)
      return socket_list[0].getsockname()
  ```
- **[DON'T]** Use `# type: ignore` or `Any` as a crutch, which destroys type checking context downstream.
  ```python
  def get_address(server) -> str:
      socket_list = server.sockets  # type: ignore
      # DON'T blind the type checker
      return socket_list[0].getsockname()
  ```

### TypedDict and Dynamic Data
- **[DO]** Use `TypedDict` for static hints, but perform manual or library-based (e.g., pydantic) checking for parsed JSON.
  ```python
  from typing import TypedDict
  import json
  
  class BookDict(TypedDict):
      title: str
      pagecount: int

  def from_json(data: str) -> BookDict:
      parsed = json.loads(data)
      # Perform runtime validation here before returning
      if not isinstance(parsed, dict) or 'title' not in parsed:
          raise ValueError("Invalid data")
      return parsed
  ```
- **[DON'T]** Assume `TypedDict` provides any runtime enforcement or casting.
  ```python
  def from_json(data: str) -> BookDict:
      # DON'T assume `parsed` is magically validated as a BookDict
      parsed: BookDict = json.loads(data) 
      return parsed
  ```