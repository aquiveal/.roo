# @Domain
These rules trigger when the user requests assistance with writing tests, setting up continuous integration, debugging logic errors, tracing memory leaks, refactoring code for testability, or writing test harnesses in Python.

# @Vocabulary
*   **`repr` / `__repr__`**: The printable, type-explicit string representation of a Python object, often evaluating to valid Python code to recreate the object.
*   **`TestCase`**: The base class from the `unittest` module used to group related tests.
*   **`subTest`**: A context manager within `TestCase` that allows multiple independent assertions to run within a single test method.
*   **`setUp` / `tearDown`**: Methods executed before and after every individual test method to ensure isolated test environments.
*   **`setUpModule` / `tearDownModule`**: Functions executed once per test module to manage expensive, module-level test harnesses (e.g., database connections) used across integration tests.
*   **Mock**: An object from `unittest.mock` that records how it is used and returns configured expectations; distinct from a "fake" which provides an alternative, simplified implementation.
*   **`spec`**: A parameter in `Mock` that strictly binds the mock's interface to match a real class or function.
*   **Seam / Encapsulation**: A refactoring technique where complex dependencies are grouped into helper functions or wrapper classes to facilitate dependency injection during testing.
*   **`pdb` / `breakpoint()`**: Python's built-in interactive debugger and the function used to invoke it at runtime.
*   **Post-mortem debugging**: Invoking the debugger after an uncaught exception has crashed the program (e.g., `python -m pdb -c continue script.py`).
*   **`tracemalloc`**: A built-in Python module used to track memory allocations back to their source code lines, vastly superior to the `gc` module for finding memory leaks.

# @Objectives
*   Guarantee type-explicit visibility when outputting variables during debugging sessions.
*   Produce robust, highly isolated unit and integration tests using the `unittest` framework.
*   Prevent masked bugs in tests by enforcing strict mock interfaces and precise parameter verification.
*   Refactor tightly coupled code into modular seams to enable deterministic testing.
*   Pinpoint runtime errors and memory leaks using Python's most advanced built-in tracing tools.

# @Guidelines
*   When generating debug output or formatting variables for inspection, the AI MUST use `repr()` or the `!r` f-string suffix (e.g., `print(f"{value!r}")`) instead of standard string conversions, to ensure type and boundary information is preserved.
*   When defining custom classes, the AI MUST implement a `__repr__` special method that evaluates to a string containing the Python expression necessary to recreate the object state.
*   When writing tests, the AI MUST inherit from `unittest.TestCase` and group related behaviors into specific subclass methods prefixed with `test_`.
*   When validating assertions in tests, the AI MUST use `TestCase` helper methods (e.g., `self.assertEqual`, `self.assertRaises`) instead of the built-in `assert` statement, to guarantee verbose error tracking.
*   When writing data-driven tests over multiple inputs or parameters, the AI MUST use the `self.subTest(value=value)` context manager to ensure all sub-tests execute even if an earlier one fails.
*   When initializing test environments, the AI MUST isolate tests by utilizing `setUp` and `tearDown` for test-specific resources, and `setUpModule` and `tearDownModule` for expensive, module-scoped integration dependencies.
*   When testing code with complex external dependencies, the AI MUST use `unittest.mock.Mock` or the `patch` family of functions to simulate the behavior.
*   When instantiating a Mock, the AI MUST pass the target class or function to the `spec` parameter to ensure the mock rejects calls to non-existent attributes and prevents masked testing bugs.
*   When verifying mock interactions, the AI MUST use `assert_called_once_with`, `assert_has_calls`, and `unittest.mock.ANY` to rigidly validate expected parameters.
*   When encountering hard-to-mock dependencies (e.g., deeply nested or hardcoded database calls), the AI MUST refactor the code to encapsulate dependencies within wrapper classes or explicit helper functions (seams) prior to writing the test.
*   When diagnosing complex runtime logic or crashes, the AI MUST suggest injecting `breakpoint()` for interactive `pdb` debugging or utilize post-mortem debugging, but MUST ensure `breakpoint()` calls are never included in final or committed code.
*   When diagnosing memory leaks, the AI MUST use the `tracemalloc` built-in module (via `take_snapshot` and `compare_to('lineno')`) rather than the `gc` module, to pinpoint the exact source code line allocating the leaked memory.

# @Workflow
1.  **Analyze the Request**: Determine if the task involves debugging, testing, refactoring for testability, or memory profiling.
2.  **Debug Formatting**: If logging or printing state, wrap all outputs in `repr()` formatting.
3.  **Refactoring for Seams**: If writing tests for coupled code, first extract dependencies (APIs, DBs) into wrapper classes or keyword arguments.
4.  **Test Structuring**: Create `unittest.TestCase` classes. Define `setUp` and `tearDown` for isolated state.
5.  **Mock Injection**: Apply `unittest.mock.patch` to inject dependencies. ALWAYS pass `spec=True` or `spec=TargetClass` to the mock.
6.  **Assertion Definition**: Write test logic using `self.assert*` methods. Use `self.subTest()` if iterating through multiple test parameters.
7.  **Memory Tracing**: If tracking memory, write a script utilizing `tracemalloc.start()`, execute the offending code, capture `tracemalloc.take_snapshot()`, and print the top offenders using `.compare_to()`.

# @Examples (Do's and Don'ts)

**Concept: Debugging Output**
*   [DO] `print(f"Current state: {my_var!r}")`
*   [DON'T] `print(f"Current state: {my_var}")`

**Concept: Custom Class Representations**
*   [DO]
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f'Point({self.x!r}, {self.y!r})'
```
*   [DON'T]
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    # Missing __repr__, prints <__main__.Point object at 0x...>
```

**Concept: Test Assertions**
*   [DO]
```python
class MyTest(TestCase):
    def test_logic(self):
        self.assertEqual(compute(5), 10)
```
*   [DON'T]
```python
class MyTest(TestCase):
    def test_logic(self):
        assert compute(5) == 10  # Lacks verbose context on failure
```

**Concept: Data-Driven Tests**
*   [DO]
```python
def test_multiple(self):
    cases = [(1, 2), (3, 6), (4, 8)]
    for input_val, expected in cases:
        with self.subTest(input_val=input_val):
            self.assertEqual(double(input_val), expected)
```
*   [DON'T]
```python
def test_multiple(self):
    cases = [(1, 2), (3, 6), (4, 8)]
    for input_val, expected in cases:
        self.assertEqual(double(input_val), expected)  # Fails fast, stops testing remaining cases
```

**Concept: Mock Specification**
*   [DO]
```python
from unittest.mock import Mock
database_mock = Mock(spec=DatabaseConnection)
database_mock.fetch_data.return_value = []
```
*   [DON'T]
```python
from unittest.mock import Mock
database_mock = Mock()
# Dangerous: database_mock.fetc_data() won't throw an error if misspelled
database_mock.fetch_data.return_value = []
```

**Concept: Memory Profiling**
*   [DO]
```python
import tracemalloc
tracemalloc.start(10)
time1 = tracemalloc.take_snapshot()
# ... run leaky code ...
time2 = tracemalloc.take_snapshot()
stats = time2.compare_to(time1, 'lineno')
for stat in stats[:3]:
    print(stat)
```
*   [DON'T]
```python
import gc
# Provides object counts, but zero context on where they were allocated
print(len(gc.get_objects()))
```