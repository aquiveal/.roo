# @Domain
Trigger these rules when writing Python code, defining function signatures, declaring variables, designing domain models, or selecting data types to represent specific behaviors and constraints.

# @Vocabulary
* **Type**: A communication method that conveys information and provides a representation that users and computers can reason about.
* **Mechanical Representation**: How types communicate behaviors and constraints to the Python language itself (e.g., binary memory interpretation, pointer linked lists, reference counts).
* **Semantic Representation**: How types communicate behaviors, constraints, boundaries, and freedoms to other developers asynchronously.
* **Strongly Typed**: A type system that restricts operations to compatible types, raising explicit errors (e.g., `TypeError`) when illegal operations are attempted (e.g., concatenating a list and a dict). Python is strongly typed.
* **Weakly Typed**: A type system that implicitly coerces types to make sense of an operation. 
* **Statically Typed**: A type system where type information is embedded at build time and variables cannot change types.
* **Dynamically Typed**: A type system where type information is embedded with the value itself, allowing variables to change types at runtime. Python is dynamically typed.
* **Duck Typing**: The ability to use objects and entities as long as they adhere to some interface or implement specific methods (e.g., `__iter__`), regardless of their explicit class hierarchy.

# @Objectives
* Treat types primarily as a semantic communication tool to broadcast developer intent to future maintainers.
* Restrict the potential behaviors of variables by choosing the most specific, constrained type possible.
* Prevent the inherent risks of a dynamically typed language by strictly avoiding runtime type rebinding.
* Leverage Python's strongly typed nature to intentionally fail fast on incompatible operations.
* Safely utilize Duck Typing to increase composability while mitigating broken assumptions by clearly annotating the expected interfaces.

# @Guidelines
* **Enforce Semantic Representation**: The AI MUST select the most specific type available for a given variable. It MUST NOT use primitive types (like `int` or `float`) if a more constrained domain type (like `datetime.datetime`) accurately represents the data's specific behaviors and limitations.
* **Expose Constraints via Types**: The AI MUST evaluate the operations supported by a chosen type (e.g., math, bitwise, string formatting) and select types that inherently forbid illogical operations for the given domain context.
* **Explicit Type Annotation**: The AI MUST append type annotations (e.g., `: datetime.datetime`) to function parameters and return types to make the semantic representation crystal clear without requiring developers to read the implementation body.
* **Prohibit Dynamic Rebinding**: Because Python allows dynamic typing, the AI MUST NOT rebind an existing variable name to a value of a completely different type. It MUST assign new types to new, well-named variables.
* **Rely on Strong Typing**: The AI MUST NOT write manual type coercion logic to work around mismatched types. It MUST allow Python's strongly typed runtime to throw a `TypeError` when incompatible types interact.
* **Safe Duck Typing**: When writing functions intended to accept multiple types via Duck Typing, the AI MUST use the `typing` module (e.g., `Iterable`) in the signature to communicate the specific structure or magic method (e.g., `__iter__`) the object must possess.
* **Prevent Duck Typing Overuse**: The AI MUST NOT rely on Duck Typing if the function requires deep, complex assumptions about the passed object. It MUST restrict the type explicitly to prevent callers from breaking the system with unexpected but superficially compatible objects.

# @Workflow
1. Analyze the domain concept being implemented and list the exact behaviors, supported operations, and constraints required.
2. Select the Python type that mechanically and semantically matches these exact constraints (favoring specific types over generic primitives).
3. Implement the function or variable declaration using explicit type annotations to establish the semantic contract.
4. Scan the surrounding scope to ensure the variable is never reassigned to a different type later in the code.
5. If the function is designed to be composable across disparate types, identify the shared interface (e.g., `__iter__`, `__add__`), import the corresponding abstraction from `typing`, and annotate the parameter to safely document the Duck Typing expectation.

# @Examples (Do's and Don'ts)

### Semantic Representation and Type Annotations
**[DO]**
```python
import datetime

def close_kitchen_if_past_cutoff_time(point_in_time: datetime.datetime):
    if point_in_time >= closing_time():
        close_kitchen()
        log_time_closed(point_in_time)
```

**[DON'T]**
```python
# Fails to communicate intent, leaving future developers guessing about constraints and supported operations.
def close_kitchen_if_past_cutoff_time(point_in_time):
    if point_in_time >= closing_time():
        close_kitchen()
        log_time_closed(point_in_time)
```

### Dynamic Typing Mitigation (Variable Rebinding)
**[DO]**
```python
# Create new variables when dealing with new types to preserve assumptions.
employee_id: int = 5
employee_name: str = "string"
```

**[DON'T]**
```python
# Do not leverage Python's dynamic typing to reuse variables for different types.
a: int = 5
a = "string"
```

### Safe Duck Typing
**[DO]**
```python
from typing import Iterable

# Explicitly states the required duck typing interface.
def print_items(items: Iterable):
    for item in items:
        print(item)

print_items([1, 2, 3])
print_items({"A": 1, "B": 2, "C": 3})
```

**[DON'T]**
```python
# Relies on blind duck typing without communicating the expected interface (__iter__) to the caller.
def print_items(items):
    for item in items:
        print(item)
```

### Relying on Strong Typing
**[DO]**
```python
# Allow the strongly typed runtime to reject illegal operations.
def combine_records(record_a: list, record_b: dict):
    # This will naturally throw a TypeError, failing fast and visibly.
    return record_a + record_b
```

**[DON'T]**
```python
# Do not implement manual, weak-type-style coercions.
def combine_records(record_a: list, record_b: dict):
    # Anti-pattern: hiding type incompatibilities.
    return str(record_a) + str(record_b)
```