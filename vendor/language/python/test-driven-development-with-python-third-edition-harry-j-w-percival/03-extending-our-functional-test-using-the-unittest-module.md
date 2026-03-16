# @Domain
Trigger these rules when the user requests the creation, refactoring, execution, or structuring of Functional Tests (also known as End-to-End tests, Acceptance tests, or System tests), particularly those using Python, Selenium WebDriver, and the `unittest` standard library. 

# @Vocabulary
- **Functional Test (FT)**: A test that drives a real web browser to examine how the application functions from the outside, from the user's point of view.
- **End-to-End Test / System Test / Acceptance Test / Black Box Test / Closed Box Test**: Alternative names and classifications for Functional Tests. They test the application without knowing anything about its internal structures.
- **User Story**: A human-readable, narrative description of how the application will work from the point of view of the user. Used to structure and document a Functional Test.
- **Minimum Viable App**: The simplest thing that can be built that is still useful. Used to scope the initial Functional Test.
- **Expected Failure**: A state where a test fails for the exact reason it was anticipated to fail (e.g., checking for a title that hasn't been implemented yet), proving the test is written correctly.
- **Lie (Comment)**: A comment that merely repeats what the code is doing, or an outdated comment that no longer matches the implementation.

# @Objectives
- Translate user requirements into formal User Stories documented as comments within Functional Tests.
- Structure all Functional Tests using the Python standard library `unittest` module to ensure reliable setup, teardown, and error reporting.
- Prevent resource leakage (e.g., orphaned browser windows) by strictly managing WebDriver lifecycles.
- Produce highly readable test outputs and tracebacks using specific `unittest` assertion methods rather than raw Python `assert` statements.
- Maintain a clean version control workflow that aligns with the Test-Driven Development (TDD) cycle.

# @Guidelines
- **Test Framework Selection**: When generating or updating tests, the AI MUST use the Python standard library `unittest` module. The AI MUST NOT use `pytest` for these specific tests, as the surrounding Django/TDD methodology relies on `unittest` tooling.
- **Class Structure**: When structuring a Functional Test, the AI MUST organize tests into classes that inherit from `unittest.TestCase`.
- **Method Naming**: When defining a test method inside the class, the AI MUST prefix the method name with `test_` and use a highly descriptive name (e.g., `test_can_start_a_todo_list`).
- **Resource Management (setUp/tearDown)**: 
  - The AI MUST use the `def setUp(self):` method to initialize the browser instance (`self.browser = webdriver.Firefox()`).
  - The AI MUST use the `def tearDown(self):` method to safely close the browser (`self.browser.quit()`), ensuring the browser window is cleaned up even if the test fails.
- **State Management**: The AI MUST NOT use global variables for the browser instance. The browser MUST be assigned to the class instance (`self.browser`).
- **Assertions**: 
  - When making test assertions, the AI MUST NOT use the raw Python `assert` keyword. 
  - The AI MUST use `unittest` helper methods (e.g., `self.assertIn`, `self.assertEqual`, `self.assertTrue`, `self.assertFalse`) to ensure detailed, helpful error messages in the traceback.
- **Incomplete Tests**: When a Functional Test is intentionally left incomplete, the AI MUST use `self.fail("Finish the test!")` to force a failure and provide a reminder to finish it later.
- **Command-Line Execution**: When creating the test file, the AI MUST include the standard execution block at the bottom of the file: `if __name__ == "__main__": unittest.main()`.
- **Commenting Rules**:
  - The AI MUST use comments within the test method to explicitly write out the "User Story" step-by-step.
  - The AI MUST NOT write comments that simply repeat what the code does (e.g., `# increment wibble by 1`). Code must be readable enough via variable and function names to not require mechanical explanations.
- **Version Control Integrations**:
  - When asked to commit changes after a test refactor, the AI MUST recommend or use `git status` and `git diff -w` (ignore whitespace) to review changes.
  - When committing routine test refactors, the AI MUST use `git commit -a` to automatically add changes to tracked files, followed by a descriptive commit message.

# @Workflow
1. **Scope the Minimum Viable App**: Determine the absolute simplest functionality required to be useful.
2. **Draft the User Story**: Write the steps of the User Story purely as Python comments inside a new `test_` method.
3. **Structure the `unittest` Class**: Wrap the method in a `class MyTestName(unittest.TestCase):` definition.
4. **Implement Lifecycle Methods**: Add `setUp` to instantiate `self.browser` and `tearDown` to call `self.browser.quit()`.
5. **Translate Comments to Code**: Underneath each User Story comment, write the corresponding Selenium WebDriver commands.
6. **Apply `unittest` Assertions**: Use `self.assertIn`, `self.assertEqual`, etc., to validate the UI state against the User Story.
7. **Add Execution Hook**: Append `if __name__ == "__main__": unittest.main()` to the script.
8. **Run and Verify Expected Failure**: Execute the test and verify it fails exactly where the unimplemented feature is checked.
9. **Version Control**: Review the changes using `git diff -w` and commit them using `git commit -a` with a descriptive message detailing the User Story.

# @Examples (Do's and Don'ts)

## Test Structure and Browser Lifecycle
- **[DO]** Organize the test using `unittest` and manage the browser in `setUp` and `tearDown`.
```python
import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app.
        self.browser.get("http://localhost:8000")
        self.assertIn("To-Do", self.browser.title)

if __name__ == "__main__":
    unittest.main()
```
- **[DON'T]** Use global variables and raw scripts without teardown guarantees.
```python
from selenium import webdriver

browser = webdriver.Firefox()
browser.get("http://localhost:8000")
assert "To-Do" in browser.title
browser.quit() # If the assert fails, this never runs!
```

## Assertions
- **[DO]** Use `unittest` assertion methods for clear error reporting.
```python
self.assertIn("To-Do", self.browser.title)
self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")
self.fail("Finish the test!")
```
- **[DON'T]** Use raw `assert` statements which yield unhelpful `AssertionError` tracebacks.
```python
assert "To-Do" in browser.title
```

## Commenting Practices
- **[DO]** Use comments to tell a human-readable User Story.
```python
# She is invited to enter a to-do item straight away
# She types "Buy peacock feathers" into a text box
# (Edith's hobby is tying fly-fishing lures)
```
- **[DON'T]** Use comments that lie or redundantly explain basic syntax.
```python
# find the element by tag name h1
header_text = self.browser.find_element(By.TAG_NAME, "h1").text
# assert that To-Do is in the header text
self.assertIn("To-Do", header_text)
```