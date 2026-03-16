# @Domain
This rule file is triggered whenever the AI is requested to write, refactor, or review Python code involving function definitions, API design, class method signatures, or static type checking using PEP 484 annotations.

# @Vocabulary
- **Gradual Typing**: A type system where type hints are optional. Untyped code defaults to `Any`. It does not catch type errors at runtime or enhance performance.
- **Duck Typing**: Typing based on the object's structure and supported operations at runtime, regardless of its declared class.
- **Nominal Typing**: Typing enforced statically by checking the explicit names of classes and their inheritance trees.
- **Consistent-with**: A relationship where a type can safely substitute another in a gradual type system. A subtype is consistent-with a supertype. `Any` is consistent-with every type, and every type is consistent-with `Any`.
- **Subtype-of**: A strict object-oriented relationship where a child class inherits from a parent class.
- **Any**: The dynamic wildcard type. It sits at both the top and bottom of the type hierarchy, bypassing all static type checks.
- **Optional**: A type hint (e.g., `Optional[T]`) indicating a value can be of type `T` or `None`. Conceptually identical to `Union[T, None]` or `T | None`.
- **TypeVar**: A type variable used to create parameterized generics, maintaining type relationships between function arguments and return values.
- **Static Protocol (`typing.Protocol`)**: A class used to define an interface based on supported operations (static duck typing) rather than explicit inheritance.
- **Callable**: A type hint representing a function or callable object, defining its argument types and return type.
- **NoReturn**: A special type hint for functions that never return execution to the caller (e.g., functions that unconditionally raise exceptions).

# @Objectives
- Enhance code maintainability, static analysis, and developer tooling (IDE autocomplete, linters) using PEP 484 type hints.
- Preserve Python’s dynamic flexibility and expressive power by applying gradual typing pragmatically, avoiding over-engineering.
- Adhere to Postel’s Law (the Robustness Principle) in function signatures: be liberal in what you accept (use abstract types for parameters) and conservative in what you send (use concrete types for return values).
- Prevent the illusion of runtime type safety; type hints must not replace necessary runtime data validation (e.g., when parsing JSON).

# @Guidelines

## General Gradual Typing Rules
- The AI MUST treat type hints as optional. Do not force 100% type hint coverage if it results in overly convoluted, unreadable APIs.
- The AI MUST NOT rely on type hints for runtime validation. For dynamic data (like JSON or API payloads), the AI MUST implement explicit runtime checks or use validation libraries (like `pydantic`).
- The AI MUST avoid abusing `Any`, as it neutralizes static type checking.
- The AI MUST prefer `object` over `Any` when a function accepts any type but does not invoke arbitrary methods on the object.

## Type Hierarchies and Numeric Types
- The AI MUST remember that `int` is consistent-with `float`, and `float` is consistent-with `complex`. To accept both integers and floats, the AI MUST use `float` in the type hint.

## Optional and Union Types
- When annotating a parameter that can be `None`, the AI MUST explicitly provide the default value `= None` in the signature. `Optional[T]` or `T | None` does not automatically make the parameter optional in the function call.
- For Python >= 3.10, the AI MUST prefer the union operator `X | Y` over `Union[X, Y]`, and `X | None` over `Optional[X]`.

## Collections and Generics
- For Python >= 3.9, the AI MUST use built-in types for generics (e.g., `list[str]`, `dict[str, int]`, `set[float]`). The AI MUST NOT use `typing.List`, `typing.Dict`, or `typing.Set` unless explicitly maintaining legacy code (<= 3.8).
- For generic mappings, the AI MUST specify both key and value types (e.g., `dict[str, set[str]]`).

## Tuple Annotations
- When a tuple is used as a record (fixed size, potentially mixed types), the AI MUST explicitly declare each positional type: `tuple[str, float, str]`.
- When a tuple is used as an immutable sequence (variable length, single type), the AI MUST use the ellipsis: `tuple[int, ...]`.

## Postel's Law: Abstract Arguments, Concrete Returns
- The AI MUST use abstract base classes from `collections.abc` (e.g., `Mapping`, `Sequence`, `Iterable`, `MutableSequence`) for function parameters to maximize caller flexibility.
- The AI MUST use concrete classes (e.g., `list`, `dict`, `set`) for function return types to provide clear guarantees to the caller.
- The AI MUST explicitly differentiate between `abc.Iterable` (for functions that iterate over an object once) and `abc.Sequence` (for functions that require `len()` or indexing `[i]`).

## Type Variables and Constraints
- The AI MUST use `typing.TypeVar` for generic functions where the return type depends on the argument type.
- The AI MUST use the `bound=...` argument in a `TypeVar` to restrict the generic to types that implement a specific protocol or base class (e.g., `TypeVar('T', bound=Hashable)`).
- The AI MUST use restricted TypeVars when a function strictly accepts a finite set of types (e.g., `TypeVar('NumberT', float, Decimal, Fraction)`).

## Static Protocols (Static Duck Typing)
- If a function requires an argument to support specific operations (e.g., `.quack()`, or `<`), the AI MUST define a `typing.Protocol` defining those specific methods rather than using `Any` or forcing nominal inheritance.

## Callables and NoReturn
- The AI MUST annotate callback parameters using `Callable[[Param1Type, Param2Type], ReturnType]`.
- If the signature of the callable is completely dynamic, the AI MUST use the ellipsis: `Callable[..., ReturnType]`.
- The AI MUST use `NoReturn` for the return type of functions that unconditionally raise exceptions or call `sys.exit()`.

## Variadic Parameters (`*args` and `**kwargs`)
- The AI MUST annotate `*args` and `**kwargs` with the type of the *individual* items they contain, not the collection type. If `def foo(*args: str)` is used, `args` will statically resolve as `tuple[str, ...]`.
- For positional-only parameters in Python >= 3.8, the AI MUST use the `/` marker in the signature.

# @Workflow
1. **Analyze Signature Intent**: Determine the purpose of the function. What does it consume? What does it produce?
2. **Select Parameter Types**: Convert concrete parameter expectations into the broadest possible Abstract Base Classes (`Iterable` instead of `list`, `Mapping` instead of `dict`).
3. **Select Return Types**: Identify the exact concrete data structure returned by the function and annotate it accordingly.
4. **Link Generics**: If the return type directly mirrors or wraps the input type, define a `TypeVar` to preserve the type relationship.
5. **Enforce Behaviors**: If an input relies on specific "duck typed" methods, create a `typing.Protocol` and bind it to the parameter.
6. **Apply Defaults**: Ensure any type hinted as `Optional` or `T | None` is assigned `= None` in the signature.
7. **Format Syntax**: Apply Python version-appropriate syntax (e.g., standard collection generics `list[T]` for 3.9+, union operator `A | B` for 3.10+).

# @Examples (Do's and Don'ts)

## Abstract Parameters and Concrete Returns
- **[DO]**
  ```python
  from collections.abc import Iterable

  def tokenize(text: str) -> list[str]:
      return text.upper().split()

  def process_items(items: Iterable[str]) -> list[str]:
      return [tokenize(item) for item in items]
  ```
- **[DON'T]**
  ```python
  # Fails Postel's Law: Demands a concrete list, returns an abstract Iterable
  def process_items(items: list[str]) -> Iterable[str]:
      return [tokenize(item) for item in items]
  ```

## Optional Parameters
- **[DO]**
  ```python
  def show_count(count: int, singular: str, plural: str | None = None) -> str:
      if not plural:
          plural = singular + 's'
      return f"{count} {plural}"
  ```
- **[DON'T]**
  ```python
  # Missing the default assignment (= None) makes the parameter mandatory
  def show_count(count: int, singular: str, plural: str | None) -> str:
      ...
  ```

## Variadic Parameters
- **[DO]**
  ```python
  def tag(name: str, /, *content: str, **attrs: str) -> str:
      # *content expects individual strings. Inside the function, it evaluates to tuple[str, ...]
      pass
  ```
- **[DON'T]**
  ```python
  def tag(name: str, /, *content: tuple[str, ...], **attrs: dict[str, str]) -> str:
      # Incorrectly annotating the wrapper container instead of the items
      pass
  ```

## Tuple Annotations
- **[DO]**
  ```python
  # Record (fixed length, specific types)
  def get_coordinate() -> tuple[float, float, str]:
      return (45.5, -122.6, "Portland")

  # Immutable sequence (variable length, uniform type)
  def get_hashes() -> tuple[int, ...]:
      return (12345, 67890, 54321)
  ```
- **[DON'T]**
  ```python
  # Missing the ellipsis for a variable-length tuple
  def get_hashes() -> tuple[int]:
      return (12345, 67890, 54321) # Type checker will expect exactly ONE integer
  ```

## Static Protocols (Static Duck Typing)
- **[DO]**
  ```python
  from typing import Protocol, TypeVar

  class SupportsMultiply(Protocol):
      def __mul__(self, repeat_count: int) -> 'SupportsMultiply': ...

  T = TypeVar('T', bound=SupportsMultiply)

  def double(x: T) -> T:
      return x * 2
  ```
- **[DON'T]**
  ```python
  # Forcing nominal inheritance or falling back to Any loses type safety
  def double(x: Any) -> Any:
      return x * 2
  ```