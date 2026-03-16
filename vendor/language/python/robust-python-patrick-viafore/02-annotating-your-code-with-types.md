## @Domain
These rules MUST trigger whenever the AI is tasked with writing, modifying, refactoring, or reviewing Python code. This specifically applies to defining functions, classes, variables, public APIs, and cross-module interfaces, or when setting up static analysis tooling and typecheckers for a Python codebase.

## @Vocabulary
*   **Type Annotation / Type Hint:** Additional syntax (`: <type>` and `-> <type>`) attached to variables, parameters, and return signatures that notifies readers and tools of the expected type.
*   **Dynamic Typing:** The default Python behavior where type information is embedded in the value itself, allowing variables to change types at runtime.
*   **Typechecker:** A static analysis tool (such as `mypy`) that scans source code to flag mismatched type annotations without executing the code.
*   **Cognitive Overhead:** The mental burden placed on a developer when they must read deep into implementation details, read testing suites, or trace external callers just to determine what data types a function expects or returns.
*   **Static Analysis:** Examining the source code prior to runtime to catch bugs, enforce intentions, and provide a safety net.
*   **Table Stakes:** Baseline requirements for any meaningful project; in this context, clean and annotated code is table stakes for robust Python.

## @Objectives
*   **Enforce Discipline in Large Codebases:** Transition from unstructured dynamic typing to disciplined, strongly-communicated contracts to support system scalability and maintainability.
*   **Eliminate Cognitive Overhead:** Express exact developer intent directly in the function signature so future maintainers never have to read the implementation to understand how to use the code.
*   **Provide Verified Documentation:** Treat type annotations as a living, executable form of documentation that never goes out of date.
*   **Shift Errors Left:** Catch type incompatibilities, missing attributes, and `None` fall-through bugs immediately via static analysis before code reaches runtime.
*   **Reduce Friction:** Create code that is intuitive to consume and modify, building future maintainers' confidence.

## @Guidelines
*   **Mandatory API Annotation:** The AI MUST annotate all parameters and return types for functions that serve as public APIs, library entry points, or are expected to be called by other modules.
*   **Strict Return Type Adherence:** The AI MUST ensure that all code paths within a function strictly return the type annotated in the signature. Do not allow conditional fall-throughs to return `None` if a specific type (e.g., `str`) is expected.
*   **No Runtime Reliance:** The AI MUST NOT rely on type annotations to enforce runtime checks. Annotations are for static analysis and human readability only; the Python interpreter ignores them at runtime.
*   **Avoid Variable Clutter:** The AI MUST NOT annotate variables when the type is blatantly obvious from the assignment (e.g., `text: str = "useless"` or `number: int = 0`). 
*   **Explicit Empty Collections:** The AI MUST explicitly type-annotate variables when assigning an empty collection (e.g., `numbers: list[int] = []`) to prevent the typechecker from defaulting to `Any`.
*   **Highlight Complex Types:** The AI MUST use type annotations to clarify complex, nested, or unintuitive data structures (e.g., dictionaries of strings mapped to lists of objects).
*   **Modern Syntax Preference:** The AI MUST use Python 3.5+ syntax for annotations. Avoid legacy Python 2.7 comment-based type hints (`# type: float`) unless explicitly constrained to legacy systems.
*   **Collection Method Accuracy:** The AI MUST map methods strictly to the specific collection type annotated (e.g., do not call `.update()` on a `list`; use `.extend()` instead).
*   **Byte/String Disambiguation:** The AI MUST strictly differentiate between `bytes` and `str` types in annotations and implementation, especially when reading files or using `.encode()`/`.decode()`.

## @Workflow
1.  **Analyze the Interface:** When defining or modifying a function, determine the exact semantic intent of every parameter and the final return value.
2.  **Define the Signature:** Apply type annotations to all parameters using the `name: type` syntax.
3.  **Define the Return:** Apply the return type annotation using the `-> type` syntax. If the function returns nothing, explicitly annotate it as `-> None`.
4.  **Implement Body:** Write the function body, ensuring that operations performed on the parameters strictly adhere to the mechanical limitations of the annotated types.
5.  **Verify Code Paths:** Trace every possible branching path (every `if`, `elif`, `else`, `try`, `except`) to guarantee that the returned value matches the annotated return type. Ensure there is no implicit `None` returned at the end of the function.
6.  **Annotate Internal Variables:** Review internal variables. Add annotations *only* to empty collections being initialized or highly complex data structures. Leave obvious primitive assignments unannotated.
7.  **Simulate Static Analysis:** Mentally run the code through a strict typechecker (like `mypy`). Flag and resolve any incompatible types, missing attributes, or signature mismatches.

## @Examples (Do's and Don'ts)

### Function Signatures and Cognitive Overhead
[DO] 
```python
import datetime
import random

def schedule_restaurant_open(open_time: datetime.datetime, workers_needed: int) -> None:
    workers = find_workers_available_for_time(open_time)
    for worker in random.sample(workers, workers_needed):
        worker.schedule(open_time)
```
[DON'T]
```python
import random

# Missing annotations force the reader to guess if open_time is a string, int, or datetime
# and if workers_needed is a count or a list of Worker objects.
def schedule_restaurant_open(open_time, workers_needed):
    workers = find_workers_available_for_time(open_time)
    for worker in random.sample(workers, workers_needed):
        worker.schedule(open_time)
```

### Variable Annotations and Clutter
[DO]
```python
# Annotate empty collections to assist the typechecker
workers: list[str] = find_workers_available_for_time(open_time)
numbers: list[int] = []
ratio: float = get_ratio(5, 3)
```
[DON'T]
```python
# Do not clutter code with blatantly obvious types
number: int = 0
text: str = "useless"
values: list[float] = [1.2, 3.4, 6.0]
worker: Worker = Worker()
```

### Return Type Consistency
[DO]
```python
# All code paths, including fall-throughs, must satisfy the return type annotation
def get_restaurant_name(city: str) -> str:
    if city in ITALY_CITIES:
        return "Trattoria Viafore"
    if city in GERMANY_CITIES:
        return "Pat's Kantine"
    
    return "Unknown Restaurant"
```
[DON'T]
```python
def get_restaurant_name(city: str) -> str:
    if city in ITALY_CITIES:
        return "Trattoria Viafore"
    if city in GERMANY_CITIES:
        return "Pat's Kantine"
    
    # Anti-pattern: Returning None when a strict 'str' is expected
    return None 
```

### Collection Method Accuracy
[DO]
```python
def add_doubled_values(my_list: list[int]) -> None:
    # Using the correct method for the annotated 'list' type
    my_list.extend([x * 2 for x in my_list])
```
[DON'T]
```python
def add_doubled_values(my_list: list[int]) -> None:
    # Anti-pattern: Calling 'update' on a list. Mypy will flag: "list[int]" has no attribute "update"
    my_list.update([x * 2 for x in my_list])
```

### Bytes vs String Disambiguation
[DO]
```python
def read_file_and_reverse_it(filename: str) -> str:
    with open(filename) as f:
        # Returning a string as annotated
        return f.read()[::-1]
```
[DON'T]
```python
def read_file_and_reverse_it(filename: str) -> str:
    with open(filename) as f:
        # Anti-pattern: Returning bytes when a string is expected
        return f.read().encode("utf-8")[::-1]
```