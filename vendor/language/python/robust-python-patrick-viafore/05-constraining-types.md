# @Domain
Trigger these rules when working on Python codebases, specifically during tasks involving type hinting, data modeling, API design, refactoring legacy code, implementing error handling, defining state/configuration objects, or resolving typechecker (e.g., `mypy`) violations.

# @Vocabulary
- **Representable State Space**: The set of all possible combinations of values an object or data structure can take.
- **Product Type**: A type (like a standard class or dataclass) where the number of representable states is the mathematical product of the possible values of its fields. Often leads to a massive state space containing illegal combinations.
- **Sum Type**: A type (like a `Union`) where the number of representable states is the sum of its constituents. Used to strictly limit state space and eliminate illegal combinations.
- **Illegal State**: A combination of variables or data that logically contradicts the business rules or physical reality of the system (e.g., an error object that also holds a success payload).
- **Defensive Programming**: Attempting to foresee and account for every possible error case manually (e.g., ubiquitous `if x is None:` checks) instead of leveraging the type system.
- **Blessed Function**: The singular, explicitly sanctioned factory method used to create a `NewType`, verifying its constraints before instantiation.
- **Type Alias**: An alternative name for a type that is perfectly interchangeable with the original type (unlike `NewType`, which enforces strict one-way boundaries).

# @Objectives
- Make illegal states fundamentally unrepresentable using Python's advanced typing system.
- Eradicate the "billion-dollar mistake" of unhandled `None` references.
- Drastically reduce the representable state space of data models by favoring Sum Types over Product Types.
- Shift error detection from runtime defensive programming to static typechecking time.
- Encode business context and developer intent directly into type signatures to facilitate asynchronous communication with future maintainers.

# @Guidelines
- **Optional/None Constraints**:
  - The AI MUST NOT use `None` as a valid return type or parameter value without explicitly annotating the type as `Optional[T]` (or `Union[T, None]`).
  - The AI MUST enforce explicit `is None` checks in the code before dereferencing or invoking methods on any variable annotated as `Optional`.
  - The AI MUST treat empty collections (e.g., `[]`) and `None` as distinct semantic concepts. `None` indicates an error or missing state; an empty collection indicates valid data with zero elements.
- **Union & State Space Constraints**:
  - The AI MUST NOT create flat "Product Type" data models that mix conflicting states (e.g., putting an `error_code` field and a `success_data` field in the same dataclass).
  - The AI MUST extract mutually exclusive states into separate classes and group them using a `Union` (a "Sum Type") to make illegal states impossible to instantiate.
- **Literal Constraints**:
  - The AI MUST NOT use generic types like `str` or `int` when a variable is only allowed to hold a small, highly restricted set of specific values.
  - The AI MUST use `Literal[value1, value2, ...]` to explicitly constrain exact acceptable values.
- **Annotated Constraints**:
  - For constraints too complex for `Literal` (e.g., regex matching, min/max lengths, specific ranges), the AI MUST use `Annotated[T, Metadata]` to statically communicate these constraints to future developers.
- **NewType Constraints**:
  - The AI MUST use `NewType` to separate raw data types from validated/context-specific data types (e.g., separating a raw `str` from a `SanitizedString`, or an unservable `HotDog` from a `ReadyToServeHotDog`).
  - The AI MUST NEVER manually instantiate a `NewType` outside of a designated "blessed" factory function. The blessed function must validate the preconditions and return the `NewType`.
  - The AI MUST NOT confuse `NewType` with Type Aliases. Use Type Aliases (e.g., `IdOrName = Union[str, int]`) solely to improve readability of complex nested types, recognizing that aliases remain interchangeable with their underlying types.
- **Final Constraints**:
  - The AI MUST annotate global constants, module-level configuration names, or immutable class variables with `Final` to signal that they must never be rebound.
  - The AI MUST document that `Final` prevents reassignment of the variable name, but does NOT prevent mutation of the underlying object (e.g., lists or dictionaries).

# @Workflow
When generating, refactoring, or reviewing Python data models or function signatures, the AI MUST strictly follow this algorithmic sequence:
1. **Audit for Nulls**: Scan the target function/model for any usage of `None`. If `None` is possible, rewrite the annotation to include `Optional[T]` and implement an early-return `is None` check.
2. **Audit for State Space Explosions**: Examine classes/dataclasses for fields that logically contradict each other (e.g., `is_deleted` and `active_session_id`). Split these into separate classes and combine them using a `Union`.
3. **Audit for Magic Strings/Numbers**: Identify `str` or `int` parameters that only accept specific enumerated constants. Convert these immediately to `Literal` types.
4. **Audit for Context-Dependent Safety**: If a basic type requires specific formatting, sanitization, or state preparation before it can be safely consumed by downstream functions, wrap it in a `NewType`. Create a "blessed" function to handle the conversion.
5. **Audit for Immutability Intent**: Locate any variables intended to be constant across the module/class lifespan and annotate them with `Final`.
6. **Audit for Readability**: Review the final type signatures. If a signature contains deeply nested generics or Unions, extract it into a descriptively named Type Alias. If a type has undocumented complex bounds, wrap it in an `Annotated` type.

# @Examples (Do's and Don'ts)

### Handling Null References (Optional)
- **[DO]**
  ```python
  from typing import Optional
  
  def dispense_bun() -> Optional[Bun]:
      if not buns_available():
          return None
      return Bun('Wheat')
  
  def build_hotdog():
      bun = dispense_bun()
      if bun is None:
          print_error("No buns available")
          return
      # Safe to use bun here
      bun.add_frank(frank)
  ```
- **[DON'T]**
  ```python
  # Anti-pattern: Returning None without Optional, and not checking before use
  def dispense_bun() -> Bun:
      if not buns_available():
          return None
      return Bun('Wheat')
  
  def build_hotdog():
      bun = dispense_bun()
      bun.add_frank(frank) # Typechecker error: bun might be None
  ```

### Limiting State Space (Union vs Product Types)
- **[DO]**
  ```python
  from dataclasses import dataclass
  from typing import Union
  
  @dataclass
  class ErrorState:
      error_code: int
      disposed_of: bool
  
  @dataclass
  class ValidSnack:
      name: str
      condiments: set[str]
  
  # The illegal state of having condiments AND an error code is unrepresentable
  SnackResponse = Union[ValidSnack, ErrorState]
  ```
- **[DON'T]**
  ```python
  from dataclasses import dataclass
  
  # Anti-pattern: Product Type allows illegal states (e.g. error_code=5 with condiments present)
  @dataclass
  class SnackResponse:
      name: str
      condiments: set[str]
      error_code: int
      disposed_of: bool
  ```

### Restricting Values (Literal)
- **[DO]**
  ```python
  from typing import Literal
  
  def order_snack(name: Literal["Pretzel", "Hot Dog", "Veggie Burger"]):
      pass
  ```
- **[DON'T]**
  ```python
  # Anti-pattern: Relying on generic strings and runtime checks
  def order_snack(name: str):
      if name not in ["Pretzel", "Hot Dog", "Veggie Burger"]:
          raise ValueError("Invalid snack")
  ```

### Enforcing Context Boundaries (NewType)
- **[DO]**
  ```python
  from typing import NewType
  
  HotDog = str
  ReadyToServeHotDog = NewType("ReadyToServeHotDog", HotDog)
  
  # Blessed function
  def prepare_for_serving(hot_dog: HotDog) -> ReadyToServeHotDog:
      assert_plated(hot_dog)
      return ReadyToServeHotDog(hot_dog)
  
  def serve_to_customer(hot_dog: ReadyToServeHotDog):
      pass
  ```
- **[DON'T]**
  ```python
  # Anti-pattern: Using Type Aliases where strict enforcement is needed, allowing raw types to slip through
  ReadyToServeHotDog = str # Just an alias, completely interchangeable
  
  def serve_to_customer(hot_dog: ReadyToServeHotDog):
      pass
  
  serve_to_customer("Raw, unplated hotdog") # Typechecker won't catch this!
  ```

### Documenting Complex Bounds (Annotated)
- **[DO]**
  ```python
  from typing import Annotated
  
  # Communicates intent that the string must match a specific regex format
  PhoneNumber = Annotated[str, "MatchesRegex('^[0-9]{3}-[0-9]{4}$')"]
  ```
- **[DON'T]**
  ```python
  # Anti-pattern: Leaving magic constraints hidden in implementation details
  PhoneNumber = str # Requires the developer to read the function body to know the required format
  ```

### Preventing Rebinding (Final)
- **[DO]**
  ```python
  from typing import Final
  
  VENDOR_NAME: Final = "Viafore's Auto-Dog"
  ```
- **[DON'T]**
  ```python
  # Anti-pattern: Leaving constants vulnerable to accidental rebinding
  VENDOR_NAME = "Viafore's Auto-Dog"
  VENDOR_NAME += " V2" # Accidental modification
  ```