@Domain
These rules MUST be activated when the AI is interacting with Python/Django test suites, specifically when:
1. Refactoring or reorganizing test files (splitting crowded monolithic test files into modular packages).
2. Implementing or modifying Selenium Functional Tests (FTs) that require browser interaction and asynchronous waits.
3. Executing a Red/Green/Refactor (R/G/R) TDD cycle where structural changes must be isolated from behavioral changes.
4. Managing Django Unit Tests (UTs) to mirror application source code structure.

@Vocabulary
- **FT (Functional Test)**: High-level tests mapping to user stories or features, driving a real web browser via Selenium.
- **UT (Unit Test)**: Low-level tests isolated to specific application logic (e.g., views, models, forms).
- **R/G/R (Red/Green/Refactor)**: The core TDD cycle. Write a failing test (Red), make it pass (Green), then clean up the design (Refactor).
- **Dunderinit (`__init__.py`)**: A special Python file required inside directories to make the Django test runner recognize them as regular packages rather than namespace packages.
- **Namespace Package**: A Python directory lacking an `__init__.py`. The Django test runner will silently fail to discover tests inside namespace packages.
- **`@skip`**: A decorator from `unittest` used to temporarily ignore a failing test.
- **Early Return**: Placing a `return` statement in the middle of a test method to stop execution before a failing assertion.
- **`wait_for`**: A generic explicit wait helper method that polls a wrapped assertion until it passes or times out.
- **Lambda Function**: A one-line, anonymous function (`lambda: <expression>`) used to defer the execution of an assertion so it can be continuously retried by the `wait_for` helper.
- **Explicit Wait**: Waiting for a specific condition to be true or an element to exist, as opposed to an arbitrary `time.sleep()`.

@Objectives
- Transform monolithic, crowded test files into scalable, maintainable directory structures.
- Ensure 100% test discovery by the Django test runner by meticulously managing package initializers.
- Eliminate arbitrary or static time delays (`time.sleep`) in Functional Tests in favor of robust, generic polling mechanisms (`wait_for`).
- Strictly enforce the separation of refactoring and behavior modification: the AI MUST NEVER refactor code while tests are failing (Red).
- Provide clean, centralized inheritance hierarchies for test setups (e.g., extracting shared logic to `base.py`).

@Guidelines

# 1. Test Organization and File Structure
- **Unit Test Structure**: The AI MUST create a dedicated `tests/` directory for application unit tests.
- **UT File Mapping**: Inside the `tests/` directory, the AI MUST create a separate test file for each source code file being tested (e.g., `test_models.py`, `test_views.py`, `test_forms.py`).
- **FT Structure**: The AI MUST organize Functional Tests by high-level feature or user story into distinct files (e.g., `test_simple_list_creation.py`, `test_list_item_validation.py`).
- **Base Test Classes**: The AI MUST extract shared setup, teardown, and helper methods into a base class located in a `base.py` file. All specific test classes MUST inherit from this base class.
- **Dunderinit Requirement**: The AI MUST place an `__init__.py` file in EVERY test directory. Failure to do so will result in tests not being executed.
- **Placeholder Tests**: The AI MUST ensure there is at least a placeholder test for every function and class in the codebase.
- **Relative Imports**: The AI MAY use relative imports (e.g., `from .base import FunctionalTest`) within test packages, provided the relative position of the files is guaranteed to be stable.

# 2. The Refactoring Constraint (Refactoring Against Green)
- **Zero-Failing-Tests Rule**: The AI MUST NOT mix refactoring with behavior changes. Refactoring MUST ONLY occur when the test suite is fully passing (Green).
- **Masking Failures for Refactoring**: If the AI needs to refactor code while working on an incomplete feature (where a test is currently failing), the AI MUST temporarily disable the failing test to achieve a Green state.
- **Disabling Methods**: The AI MUST use the `@skip` decorator from `unittest` OR place an early `return` statement in the test right before the failing step.
- **Mandatory Cleanup**: The AI MUST remove all `@skip` decorators and early `return` statements immediately after the refactoring step is complete, before committing code or finalizing the feature.

# 3. Handling Asynchronous UI Interactions (Explicit Waits)
- **Triggering Page Loads**: Whenever the AI simulates an action that causes a page reload or an asynchronous DOM update (e.g., hitting `Keys.ENTER` or clicking a submit button), the AI MUST use an explicit wait for the subsequent assertion.
- **The `wait_for` Helper**: The AI MUST implement a generic `wait_for` method in the base Functional Test class. This method MUST use a `while True` loop, a timeout mechanism, and a `try/except` block catching both `AssertionError` and `WebDriverException`.
- **Lambda Wrapping**: The AI MUST wrap assertions passed to `wait_for` inside a `lambda` function. (e.g., `self.wait_for(lambda: self.assertEqual(...))`).

@Workflow
When tasked with adding new validation or expanding tests, the AI MUST execute the following algorithm:

1. **File Evaluation**: Analyze the current test file. If it contains multiple distinct features or is overly long, trigger a structural refactoring.
2. **Directory Setup**: Create a `tests/` directory (or `functional_tests/`) and IMMEDIATELY create an empty `__init__.py` inside it.
3. **Base Class Extraction**: Create `base.py` in the new directory. Move the parent `TestCase` or `StaticLiveServerTestCase`, `setUp`, `tearDown`, and generic helper methods (like `wait_for`) into it.
4. **Class Distribution**: Move individual test classes into their own logically named files (e.g., `test_views.py`, `test_models.py`). Have them import the base class using relative imports.
5. **Run Suite**: Run the test suite targeting the specific module (`python manage.py test <app_name>.tests`) to ensure 100% discovery and passing status.
6. **Feature Addition**: Write the new FT or UT for the required feature. Run it and confirm it fails (Red).
7. **Interrupted Refactoring**: If the codebase requires a structural change to support the new feature, the AI MUST:
    a. Apply `@skip` or an early `return` to the failing test.
    b. Verify the test suite is Green.
    c. Perform the application-level refactoring.
    d. Verify the test suite is still Green.
    e. Remove the `@skip` or early `return`.
    f. Implement the feature code to make the newly un-skipped test pass.
8. **Wait Enforcement**: For any FT steps interacting with the UI, inject `self.wait_for(lambda: <assertion>)` rather than relying on procedural execution speed.

@Examples (Do's and Don'ts)

# Structuring Test Directories
[DO]
```python
# Directory structure:
# myapp/
# └── tests/
#     ├── __init__.py
#     ├── base.py
#     ├── test_models.py
#     └── test_views.py
```

[DON'T]
```python
# Directory structure:
# myapp/
# └── tests/
#     ├── test_models.py
#     └── test_views.py
# Anti-pattern: Missing __init__.py. Django will report "Ran 0 tests".
```

# Handling Explicit Waits in Functional Tests
[DO]
```python
def test_error_message_displays(self):
    self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
    
    # DO: Wrap the assertion in a lambda and pass to a generic wait_for helper
    self.wait_for(
        lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
            "You can't have an empty list item"
        )
    )
```

[DON'T]
```python
def test_error_message_displays(self):
    self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
    
    # Anti-pattern: Assuming the page reloads instantly. This will raise a NoSuchElementException.
    self.assertEqual(
        self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
        "You can't have an empty list item"
    )
```

# Refactoring While Writing a New Feature
[DO]
```python
from unittest import skip

class ItemValidationTest(FunctionalTest):
    
    @skip
    def test_cannot_add_empty_list_items(self):
        # Test logic goes here
        self.fail("Write me!")

# DO: Skip the test to get the suite back to Green, perform refactoring across the codebase, then remove the @skip.
```

[DON'T]
```python
class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # Test logic goes here
        self.fail("Write me!")

# Anti-pattern: Leaving the test failing (Red) while simultaneously modifying underlying view/template architecture. This destroys the regression safety net.
```

# Implementing the wait_for Helper
[DO]
```python
import time
from selenium.common.exceptions import WebDriverException

def wait_for(self, fn):
    start_time = time.time()
    while True:
        try:
            return fn()
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)
```

[DON'T]
```python
def wait_for(self, fn):
    # Anti-pattern: Using static time.sleep() instead of a polling loop catching assertions/webdriver exceptions.
    time.sleep(3)
    return fn()
```