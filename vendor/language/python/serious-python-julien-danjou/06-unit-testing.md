# @Domain

These rules trigger when the AI is tasked with writing, refactoring, or reviewing Python unit tests, configuring continuous integration/continuous deployment (CI/CD) pipelines, setting up virtual test environments, or architecting mock objects and test fixtures for Python codebases.

# @Vocabulary

- **pytest**: The primary testing framework for loading and executing Python test files and functions.
- **Fixture**: A repeatable component or state (e.g., a database connection) set up before a test runs and cleaned up afterward, defined using `@pytest.fixture`.
- **Parameterized Fixture**: A fixture configured with multiple parameters to run the same test suite against different scenarios (e.g., different database drivers).
- **Mocking**: The process of creating simulated objects (`unittest.mock.Mock`) that mimic the behavior of real application objects in controlled ways to isolate the focus object.
- **Side Effect**: A behavior triggered by a mock object (via `side_effect`) that executes a function or raises an exception instead of just returning a static value.
- **coverage**: A tool/metric used to identify which lines of code were executed during a test suite and which parts remain untested (dead code).
- **Virtual Environment**: An isolated library directory (`virtualenv` or `venv`) containing an application's specific dependencies to prevent systemic conflicts.
- **tox**: A management tool that automates and standardizes test execution across multiple isolated virtual environments and Python versions.
- **detox**: A tool to run tox environments in parallel.
- **Test Double**: A generic term for a simulated object (like a mock) used to provoke corner case behavior without requiring complex layered states.

# @Objectives

- Ensure 100% of committed code is accompanied by corresponding unit tests (Zero-tolerance policy for untested code).
- Architect test suites that mimic the source code hierarchy and reside within the main package to allow distribution.
- Minimize repetitive test setup/teardown by utilizing scoped and parameterized pytest fixtures.
- Isolate test environments from system-level dependencies using virtual environments and tox.
- Achieve reliable and fast test execution through parallelization (`pytest-xdist`, `detox`) and proper mocking of high-latency or unpredictable I/O operations (HTTP, Database).
- Write pure, functionally oriented code to naturally increase testability and ease the implementation of test doubles.

# @Guidelines

## Test Organization and Structure
- The AI MUST store tests inside a `tests` submodule of the application or library they apply to (e.g., `$ROOT/$PACKAGE/tests`).
- The AI MUST mirror the structure of the rest of the source tree within the `tests` directory (e.g., code in `mylib/foobar.py` MUST be tested in `mylib/tests/test_foobar.py`).
- The AI MUST NOT allow the rest of the source tree to import from the `tests` tree. 

## Writing Tests with pytest
- The AI MUST prefix all test files with `test_` and all test functions with `test_`.
- The AI MUST use simple Python `assert` statements rather than specialized assertion methods, relying on pytest's introspection for detailed diffs.
- The AI MUST use `@pytest.mark.skip("reason")` or `@pytest.mark.skipif(condition, reason="...")` to explicitly skip tests that cannot run (e.g., missing dependencies), rather than letting them fail or commenting them out.
- The AI MUST use dynamic marking (`@pytest.mark.<keyword>`) to group tests logically, allowing subset execution via `pytest -m <keyword>`.

## Fixtures and Resource Management
- The AI MUST extract common setup and teardown logic into fixtures using the `@pytest.fixture` decorator.
- The AI MUST use the `yield` keyword within fixtures to execute teardown code after the test completes.
- The AI MUST specify `scope="module"` or `scope="class"` for expensive fixtures (like database connections) to prevent unnecessary initialization per test function.
- The AI MUST use `autouse=True` on fixtures only when the setup/teardown applies universally to every test in the scope without needing to be explicitly passed as an argument.
- The AI MUST utilize parameterized fixtures (`@pytest.fixture(params=[...])`) when the exact same test logic must be verified against multiple scenarios (e.g., different backend drivers).

## Mocking
- The AI MUST isolate the focus object by mocking external dependencies, especially HTTP clients or database interactions, using `unittest.mock`.
- The AI MUST assign functions or exceptions to a mock's `side_effect` attribute to test complex scenarios (e.g., network latency, 404 errors, or I/O errors).
- The AI MUST verify mock interactions using the `assert_called()` family of methods (e.g., `assert_called_once_with()`).
- The AI MUST use `mock.ANY` when asserting mock calls where a specific argument's exact value is unknown or irrelevant.
- The AI MUST use `mock.patch()` as a context manager or decorator to inject fake functions/objects into external modules.

## Coverage and Parallelism
- The AI MUST track code execution using `pytest-cov` (`--cov=<package>`) to reveal untested paths.
- The AI MUST NOT treat 100% line coverage as proof of perfection; the AI must also ensure all *conditions* and corner cases are explicitly tested.
- The AI MUST configure test parallelization using `pytest-xdist` (`pytest -n auto`) for large suites to balance load across CPU cores.

## Environment Isolation and CI/CD
- The AI MUST NEVER run tests directly against the global operating system Python environment.
- The AI MUST define a `tox.ini` file at the root of the project to automate the creation of virtual environments (`[testenv]`), installation of dependencies (`deps`), and execution of tests (`commands`).
- The AI MUST configure `tox` to test against multiple Python versions natively (e.g., `envlist=py27,py36,pypy`).
- The AI MUST integrate code style checks (like `flake8`) as distinct environments within `tox.ini`.
- The AI MUST configure CI services (e.g., Travis CI via `.travis.yml`) to use `tox` (or `tox-travis`) for execution.

## Architectural Best Practices for Testability
- The AI MUST separate concerns in the source code: do not perform state changes (writing to a DB) and complex calculations in the same method. Make calculation logic purely functional so it can be tested without mocks.
- The AI MUST evolve layered stacks to ensure the contract between layers is predictable, simple, and replaceable.

# @Workflow

1. **Hierarchy Setup**: Create the `tests` subpackage inside the main module directory. Mirror the source files with `test_<name>.py` files.
2. **Environment Configuration**: Generate a `tox.ini` file defining target Python versions (`envlist`), dependencies (`deps=pytest`, `pytest-cov`), and the test command (`commands=pytest --cov=mypackage`).
3. **Write Functional Logic**: Ensure the application code separates pure calculations from state-mutating I/O operations.
4. **Implement Fixtures**: Identify shared resources (e.g., configurations, databases). Create `@pytest.fixture` functions in a shared test file or within the specific test module, utilizing `yield` for clean teardown.
5. **Implement Mocks**: For any I/O operation (HTTP requests, file system access), use `@mock.patch` to inject `mock.Mock()` objects. Configure `return_value` or `side_effect` to simulate success and failure states.
6. **Write Assertions**: Write test functions using standard `assert` statements. Verify mock interactions using `assert_called_once_with`.
7. **Execute and Measure**: Run `tox` (or `detox` for parallel environment execution). Analyze the coverage report to identify missed branches or conditions, and iteratively add test scenarios to cover them.
8. **CI Integration**: Create the CI configuration file (e.g., `.travis.yml`) to automate the `tox` run on every commit.

# @Examples (Do's and Don'ts)

## Project Structure
- **[DO]**
  ```text
  my_package/
  ├── __init__.py
  ├── core.py
  └── tests/
      ├── __init__.py
      └── test_core.py
  ```
- **[DON'T]**
  ```text
  my_package/
  ├── __init__.py
  └── core.py
  tests/
  ├── __init__.py
  └── test_core.py
  ```

## Writing Fixtures
- **[DO]**
  ```python
  import pytest

  @pytest.fixture(scope="module")
  def database():
      db = connect_to_database()
      yield db
      db.close()

  def test_insert(database):
      database.insert(123)
      assert database.count == 1
  ```
- **[DON'T]**
  ```python
  def test_insert():
      # Anti-pattern: manual setup and teardown in the test itself
      db = connect_to_database()
      db.insert(123)
      assert db.count == 1
      db.close()
  ```

## Mocking External I/O
- **[DO]**
  ```python
  from unittest import mock
  import pytest
  from myapp import fetch_data, NetworkError

  @mock.patch('myapp.requests.get')
  def test_fetch_data_network_failure(mock_get):
      mock_get.side_effect = IOError("Network unreachable")
      
      with pytest.raises(NetworkError):
          fetch_data("http://example.com")
          
      mock_get.assert_called_once_with("http://example.com", timeout=mock.ANY)
  ```
- **[DON'T]**
  ```python
  from myapp import fetch_data

  def test_fetch_data_network_failure():
      # Anti-pattern: Relies on actual network state and unreachable URLs
      with pytest.raises(Exception):
          fetch_data("http://this-does-not-exist.com")
  ```

## Parameterized Fixtures
- **[DO]**
  ```python
  import pytest
  import myapp

  @pytest.fixture(params=["mysql", "postgresql"])
  def driver(request):
      d = myapp.get_driver(request.param)
      d.start()
      yield d
      d.stop()

  def test_driver_initialization(driver):
      assert driver.is_ready() is True
  ```

## Tox Configuration
- **[DO]**
  ```ini
  [tox]
  envlist = py27, py36, pep8

  [testenv]
  deps =
      pytest
      pytest-cov
  commands = pytest --cov=myapp

  [testenv:pep8]
  deps = flake8
  commands = flake8 myapp
  ```
- **[DON'T]**
  ```ini
  # Anti-pattern: Hardcoding paths or lacking isolated environment definitions
  [testenv]
  commands = python /usr/local/bin/pytest myapp/tests/
  ```