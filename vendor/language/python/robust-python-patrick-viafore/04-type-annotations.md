@Domain
Python code development, specifically focusing on defining function signatures, applying type hinting, refactoring legacy code for static analysis, and ensuring typechecker (e.g., mypy) compliance to maintain clean and robust codebases.

@Vocabulary
- **Type Annotation / Hint:** An optional syntax (`: <type>` for parameters/variables and `-> <type>` for return values) used to notify developers and tools of the expected type.
- **Typechecker:** A static analysis tool (such as `mypy`) that scans source code to flag type incompatibilities without executing the code.
- **Dynamic Typing:** Python's default type system where types are bound to values rather than variables, meaning variables can change types at runtime (type annotations do not change this runtime behavior).
- **Static Analysis:** Code inspection performed prior to runtime.
- **Cognitive Overload/Overhead:** The mental burden placed on future maintainers when they are forced to read through function implementations or trace calling code to deduce variable types.
- **Stub / Legacy Type Hint:** Comment-based type annotations (`# type: <type>`) used in Python versions older than 3.5.

@Objectives
- Eliminate cognitive overhead for future maintainers by explicitly declaring what types are expected to be passed into and returned from functions.
- Enable intelligent IDE features (e.g., autocompletion) and static analysis safety nets (e.g., mypy) by strictly adhering to typing standards.
- Prevent subtle, hard-to-detect runtime bugs (such as `NoneType` errors, `bytes` vs. `str` mix-ups, or invalid collection methods) by catching them at development time via rigid type adherence.
- Maintain Python's readability by avoiding verbose or unnecessary type annotations on blindingly obvious local variables.

@Guidelines
- **Core Syntax Enforcement:** The AI MUST annotate function parameters using `: type` and return values using `-> type`.
- **Return Type Mandate:** The AI MUST ALWAYS annotate return types for functions. Maintainers must never be forced to dig through implementation details (e.g., database calls or fallback logic) to determine what a function returns.
- **Variable Annotation Restraint:** The AI MUST NOT annotate variables where the type is "blindingly obvious" (e.g., `text: str = "useless"` or `worker: Worker = Worker()`). This prevents unnecessary code clutter.
- **Empty Collection Annotations:** The AI MUST annotate variables when assigning them to an empty collection, as typecheckers cannot infer the type (e.g., `numbers: list[int] = []`).
- **Python Version Specifics for Collections:**
  - For Python 3.9 and newer, the AI MUST use built-in collection bracket syntax (e.g., `list[str]`, `dict[str, int]`).
  - For Python 3.8 and older, the AI MUST import and use types from the `typing` module (e.g., `from typing import List, Dict`).
- **Target Areas for Annotation:** The AI MUST prioritize type annotations for:
  1. Public APIs, library entry points, and functions expected to be called by other modules.
  2. Complex or unintuitive types (e.g., nested dictionaries mapping strings to lists of objects).
  3. Areas where a typechecker explicitly complains about missing inference.
- **Strict Return Compliance:** The AI MUST ensure that the implementation's return statements strictly match the annotated return type.
  - Do not return `bytes` when `str` is expected (e.g., failing to `.decode("utf-8")`).
  - Do not implicitly or explicitly return `None` if the return annotation does not explicitly permit it.
- **Collection Method Accuracy:** The AI MUST ensure that methods called on a collection are valid for that specific collection type (e.g., do not call `.update()` on a `list`; use `.extend()`).
- **Legacy Python Support:** If constrained to Python 2.7 or versions < 3.5, the AI MUST implement type hints using comment syntax (e.g., `# type: (datetime.datetime) -> List[str]`).
- **Honoring the Hint:** The AI MUST NEVER pass a type that contradicts a function's type hint. If an extreme edge case requires ignoring a type hint (e.g., using a duck-typed class with identical functionality), the AI MUST include a prominent comment explaining the rationale.

@Workflow
1. **Signature Analysis:** When writing or modifying a function, identify the logical input parameters and the exact expected output type.
2. **Apply Annotations:** Add type annotations to all parameters and add the `-> <type>` return annotation. 
3. **Internal Variable Review:** Scan the function body for local variables.
   - If a variable initializes an empty collection, apply a type annotation.
   - If a variable has a redundant/obvious type annotation, strip the annotation to keep the code clean.
4. **Mypy Simulation:** Mentally execute static analysis on the function body:
   - Check all `return` paths. Does every path return the exact type specified in the signature? (Watch out for fallback `if` statements that might implicitly return `None`).
   - Check collection manipulations. Are the methods invoked valid for the specific type (e.g., `list` vs `set`)?
   - Check data decoding. Are byte streams properly converted to strings if a string is expected?
5. **Final Format Check:** Ensure collection type syntax matches the target Python version (`list[]` vs `typing.List[]`).

@Examples (Do's and Don'ts)

**Principle: Function Signature and Return Annotations**
- [DO] Annotate parameters and return types clearly so the reader knows exactly what to expect.
```python
import datetime

def find_workers_available_for_time(open_time: datetime.datetime) -> list[str]:
    # Implementation hidden, but caller knows exactly what to pass and what is returned.
    pass
```
- [DON'T] Leave parameters and return types ambiguous, forcing the user to read the implementation to guess the types.
```python
def find_workers_available_for_time(open_time):
    workers = worker_database.get_all_workers()
    # User has to read all this logic to guess it returns a list of strings
    if available_workers:
        return available_workers
    return [OWNER]
```

**Principle: Variable Annotation Clutter**
- [DO] Annotate empty collections, but leave obvious instantiations unannotated.
```python
numbers: list[int] = []
text = "useless"
worker = Worker()
```
- [DON'T] Clutter the code by annotating variables whose types are blindingly obvious.
```python
numbers: list[int] = []
text: str = "useless"
worker: Worker = Worker()
```

**Principle: Strict Return Type Compliance (`None` handling)**
- [DO] Explicitly match the return type, handling conditional paths properly.
```python
def get_restaurant_name(city: str) -> str:
    if city in ITALY_CITIES:
        return "Trattoria Viafore"
    # If city is not found, we must raise an error or change the return signature to allow None
    raise ValueError("City not found")
```
- [DON'T] Implicitly or explicitly return `None` when a strict type is declared, which creates latent bugs in calling code.
```python
def get_restaurant_name(city: str) -> str:
    if city in ITALY_CITIES:
        return "Trattoria Viafore"
    # Anti-pattern: Returns None, violating the `str` return type
    return None 
```

**Principle: Strict Return Type Compliance (`bytes` vs `str`)**
- [DO] Convert types properly before returning to satisfy the type hint.
```python
def read_file_and_reverse_it(filename: str) -> str:
    with open(filename) as f:
        # Properly decode bytes to string before returning
        return f.read().encode("utf-8")[::-1].decode("utf-8")
```
- [DON'T] Return raw bytes when a string is explicitly requested.
```python
def read_file_and_reverse_it(filename: str) -> str:
    with open(filename) as f:
        # Anti-pattern: Returns bytes instead of str
        return f.read().encode("utf-8")[::-1] 
```

**Principle: Collection Method Accuracy**
- [DO] Use the correct method for the annotated collection type.
```python
def add_doubled_values(my_list: list[int]):
    my_list.extend([x*2 for x in my_list])
```
- [DON'T] Use methods that belong to other collection types (like `set`).
```python
def add_doubled_values(my_list: list[int]):
    # Anti-pattern: `list` has no attribute `update`
    my_list.update([x*2 for x in my_list])
```

**Principle: Legacy Python (< 3.5) Type Hinting**
- [DO] Use comment-based syntax for older Python versions.
```python
def get_workers(open):
    # type: (datetime.datetime) -> List[str]
    pass

ratio = get_ratio(5, 3) # type: float
```
- [DON'T] Use modern syntax (`:`, `->`) in legacy Python 2.7 environments, as it will cause syntax errors.