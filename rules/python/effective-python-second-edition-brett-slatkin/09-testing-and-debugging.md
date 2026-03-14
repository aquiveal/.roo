@Domain
Python Testing, Mocking, Profiling, and Interactive Debugging tasks. This rule file activates when the user requests to write unit tests, integration tests, mock dependencies, debug exceptions, or profile memory leaks in a Python codebase.

@Vocabulary
- **repr**: The printable representation of an object, returning a string that is often a valid Python expression (evaluable via `eval()`).
- **TestCase**: The canonical base class from the `unittest` built-in module used to organize tests.
- **subTest**: A `TestCase` helper method used to define multiple independent sub-tests within a single test method, typically for data-driven testing.
- **Test Harness**: The setup and cleanup environment required to run tests, managed via `setUp`, `tearDown`, `setUpModule`, and `tearDownModule`.
- **Mock**: An object from `unittest.mock` that provides expected responses for dependent functions/classes given a set of expected calls. Distinct from a *Fake*, which contains actual simplified logic.
- **spec**: An argument passed to `Mock` ensuring the mock strictly adheres to the target object's interface, preventing misspelled method bugs.
- **patch**: A family of functions/decorators/context managers in `unittest.mock` used to temporarily reassign an attribute of a module or class for dependency injection.
- **Seam**: A helper function or architectural boundary specifically designed to allow dependency injection during testing.
- **Post-mortem Debugging**: Invoking the Python interactive debugger (`pdb`) after a program has already raised an exception and crashed.
- **tracemalloc**: A built-in Python module used to take snapshots of memory usage and trace object allocations back to the specific source code lines that created them.

@Objectives
- Guarantee that all testing code strictly utilizes `unittest.TestCase` assertion helpers rather than standard Python `assert` statements.
- Ensure test isolation by structurally managing test state through harness methods.
- Enforce the use of strictly-specified mocks over manual fakes to verify interaction with complex dependencies.
- Maximize debugging visibility by leveraging explicit `repr` formatting, `breakpoint()`, and `tracemalloc`.

@Guidelines
- **Debugging Output**: When adding print statements or logging for debugging, the AI MUST use `repr` representations. The AI MUST use the `%r` format string, the `!r` suffix in f-strings, or explicitly call `repr()`.
- **Class Representations**: When creating custom classes, the AI MUST define the `__repr__` special method to return a string containing the Python expression that recreates the object. If modification of the class is not possible, the AI MUST print the object's `__dict__` attribute.
- **Assertion Standards**: When writing tests, the AI MUST NEVER use the built-in `assert` statement. The AI MUST strictly use `TestCase` helper methods (e.g., `assertEqual`, `assertTrue`, `assertRaises`).
- **Exception Testing**: When testing that an exception is raised, the AI MUST use `assertRaises` as a context manager (with statement) to clarify exactly where the exception originates.
- **Custom Test Helpers**: When defining custom helper methods within a `TestCase`, the AI MUST NOT prefix the method name with `test_`. The AI MUST use `self.fail()` within these helpers to clarify unmet invariants.
- **Data-Driven Tests**: When testing multiple inputs for the same logic, the AI MUST use the `self.subTest()` context manager inside a loop to prevent a single failure from halting the execution of subsequent test cases.
- **Test Isolation**: The AI MUST isolate tests. For per-test state, use `setUp` and `tearDown` methods. For computationally expensive setups (like database initialization), the AI MUST use module-level `setUpModule` and `tearDownModule` functions.
- **Mocking Strategy**: When isolating code from complex dependencies, the AI MUST use `unittest.mock.Mock`.
- **Mock Specifications**: The AI MUST ALWAYS pass the `spec=TargetClassOrFunction` argument when instantiating a `Mock` to prevent the code from calling non-existent methods without failing.
- **Mock Assertions**: The AI MUST verify mock interactions using methods like `assert_called_once_with`, `assert_called_with`, or `assert_has_calls`.
- **Irrelevant Mock Parameters**: When verifying mock calls where certain arguments do not matter, the AI MUST use the `unittest.mock.ANY` constant.
- **Mock Injection**: The AI MUST inject mocks using keyword-only arguments in the function signature, or by using the `unittest.mock.patch` family of functions.
- **Patching C-Extensions**: When attempting to patch C-extension modules (like `datetime.datetime.utcnow`), the AI MUST either wrap the target in a Python helper function (a seam) or inject the mock via keyword-only arguments, as C-extensions cannot be patched directly.
- **Dependency Encapsulation**: To reduce boilerplate when mocking multiple functions, the AI MUST encapsulate dependencies into classes and pass the class instances to the code under test.
- **Interactive Debugging**: When instructing the user to debug interactively, the AI MUST insert the `breakpoint()` built-in function just before the problematic state, rather than explaining line-number-based breakpoints.
- **Memory Profiling**: When investigating memory leaks, the AI MUST NEVER use `gc.get_objects()`. The AI MUST use `tracemalloc` to take before/after snapshots and compare them using `time2.compare_to(time1, 'lineno')` or `'traceback'`.

@Workflow
1. **Identify the Task Context**: Determine if the request involves writing tests, mocking dependencies, debugging output, interactive debugging, or profiling memory.
2. **For Test Creation**: 
   - Subclass `unittest.TestCase`.
   - Name all test methods starting with `test_`.
   - Use `setUp`/`tearDown` for local state and `setUpModule`/`tearDownModule` for global state.
   - Replace any standard `assert` statements with `self.assert*` equivalents.
   - Wrap looping/parameterized tests in `with self.subTest(param):`.
3. **For Mocking**:
   - Identify the external dependency.
   - If the dependency involves multiple related functions, refactor to encapsulate them in a class.
   - Create the mock using `mock_obj = Mock(spec=TargetName)`.
   - Set expected returns using `mock_obj.return_value` or `mock_obj.side_effect` for exceptions.
   - Inject the mock via `patch` context managers, decorators, or keyword-only arguments.
   - Execute the test and verify interactions using `mock_obj.assert_called_once_with(...)`.
4. **For Debugging/Profiling Code Generation**:
   - If logging variables, format using `f"{var!r}"`.
   - If memory profiling is requested, import `tracemalloc`, start it, capture snapshots around the suspected leak, and output the `compare_to` statistics.

@Examples (Do's and Don'ts)

**Debugging Output**
- [DO]: `print(f'Value is {my_var!r}')`
- [DON'T]: `print(f'Value is {my_var}')`

**Class Representation**
- [DO]: 
  ```python
  class BetterClass:
      def __init__(self, x, y):
          self.x = x
          self.y = y
      def __repr__(self):
          return f'BetterClass({self.x!r}, {self.y!r})'
  ```
- [DON'T]: Leave classes without a `__repr__` method when debugging state is required.

**TestCase Assertions**
- [DO]: `self.assertEqual(expected, actual)`
- [DON'T]: `assert expected == actual`

**Exception Testing**
- [DO]:
  ```python
  with self.assertRaises(ValueError):
      function_under_test(bad_input)
  ```
- [DON'T]:
  ```python
  try:
      function_under_test(bad_input)
  except ValueError:
      pass
  ```

**Data-Driven Tests**
- [DO]:
  ```python
  for value, expected in test_cases:
      with self.subTest(value):
          self.assertEqual(expected, process(value))
  ```
- [DON'T]:
  ```python
  for value, expected in test_cases:
      self.assertEqual(expected, process(value)) # Fails immediately on first error
  ```

**Mock Instantiation**
- [DO]: `database_mock = Mock(spec=ZooDatabase)`
- [DON'T]: `database_mock = Mock()`

**Verifying Irrelevant Parameters in Mocks**
- [DO]: `mock_func.assert_called_with(ANY, 'Meerkat')`
- [DON'T]: `mock_func.assert_called_with(mock_db_instance, 'Meerkat')` (If the DB instance identity is irrelevant to the specific test).

**Memory Profiling**
- [DO]:
  ```python
  import tracemalloc
  tracemalloc.start(10)
  time1 = tracemalloc.take_snapshot()
  # ... code ...
  time2 = tracemalloc.take_snapshot()
  stats = time2.compare_to(time1, 'lineno')
  ```
- [DON'T]:
  ```python
  import gc
  objects = gc.get_objects()
  ```