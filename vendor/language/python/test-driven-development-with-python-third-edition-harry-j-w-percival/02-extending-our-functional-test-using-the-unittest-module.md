# @Domain

These rules trigger when the user requests the AI to create, extend, refactor, or debug a Functional Test (FT) in Python, specifically involving web browser automation (Selenium) or transitioning raw test scripts into the standard library `unittest` framework.

# @Vocabulary

- **Functional Test (FT)**: A test that drives a real web browser to examine how the application functions from the user's point of view.
- **End-to-End Test / Acceptance Test / System Test / Black Box Test / Closed Box Test**: Synonymous terms for Functional Tests. These tests interact with the application strictly from the outside, with no knowledge of internal code structures.
- **User Story**: A human-readable narrative describing how an application will work from the point of view of the user. Used to structure and document Functional Tests.
- **Minimum Viable App**: The simplest implementation of an application that can be built and still be useful. Used to scope the initial Functional Test.
- **Expected Failure**: A state where a test fails for the exact reason predicted by the developer (e.g., an assertion fails because the feature isn't built yet). This confirms the test is written correctly.
- **`setUp`**: A special `unittest` method executed *before* each individual test method.
- **`tearDown`**: A special `unittest` method executed *after* each individual test method, regardless of whether the test passed or failed.

# @Objectives

- Transform raw, script-based browser automation into robust, object-oriented test suites using Python's `unittest` module.
- Ensure all tests accurately reflect a User Story from the perspective of the end-user.
- Guarantee clean browser lifecycle management to prevent leftover/zombie browser windows.
- Provide highly descriptive, specific error messages upon test failure by using framework-native assertion methods.
- Enforce a strict "test first, then commit" workflow.

# @Guidelines

- **Test Class Structure**: The AI MUST group all tests into classes that inherit from `unittest.TestCase`.
- **Test Method Naming**: The AI MUST name every test method with the prefix `test_` so that the `unittest` test runner can automatically discover and execute them. Test names MUST be descriptive (e.g., `test_can_start_a_todo_list`).
- **Browser Lifecycle Management**: The AI MUST NOT use global variables for the browser instance. The AI MUST initialize the browser in the `setUp(self)` method (`self.browser = webdriver.Firefox()`) and safely destroy it in the `tearDown(self)` method (`self.browser.quit()`).
- **Instance Attributes**: The browser instance MUST be stored as an instance attribute (`self.browser`) so it can be passed safely between `setUp`, `tearDown`, and the test methods.
- **User Story Comments**: The AI MUST write explicit, human-readable comments detailing the User Story inside the test method. These comments act as the specification for the application.
- **Anti-Pattern (Lying Comments)**: The AI MUST NOT write comments that merely repeat what the code is doing (e.g., `# increment by 1`). Comments MUST capture the narrative context/intent of the User Story.
- **Framework Assertions**: The AI MUST NOT use raw Python `assert` statements. The AI MUST use `unittest` helper methods (e.g., `self.assertIn()`, `self.assertEqual()`, `self.assertTrue()`) to ensure detailed, formatted failure messages.
- **Incomplete Test Placeholders**: If a functional test is mapped out but not yet fully implemented, the AI MUST use `self.fail("Finish the test!")` to force an explicit failure and act as a reminder.
- **Command Line Execution**: The AI MUST include the `if __name__ == "__main__": unittest.main()` block at the bottom of the test file to allow direct execution from the terminal.
- **Version Control Preparedness**: The AI MUST encourage atomic commits after establishing an Expected Failure, specifically advocating for `git status`, `git diff -w` (to ignore whitespace changes), and `git commit -a`.

# @Workflow

1. **Define the User Story**: Begin the test method by writing out the sequence of user actions as continuous, narrative comments.
2. **Scaffold the TestCase**: Wrap the planned test in a class inheriting from `unittest.TestCase`.
3. **Implement Lifecycle Hooks**: Add `setUp(self)` to instantiate `self.browser` and `tearDown(self)` to call `self.browser.quit()`.
4. **Translate Narrative to Code**: Interleave Selenium WebDriver commands immediately below their corresponding User Story comments.
5. **Implement Assertions**: Apply `self.assert*` methods to verify the state of the application after user actions.
6. **Add Execution Block**: Append `unittest.main()` execution logic to the bottom of the file.
7. **Verify Expected Failure**: Instruct the user to run the test and verify it produces an Expected Failure with a helpful assertion error message.
8. **Commit**: Instruct the user to review changes using `git diff -w` and commit the test specification before writing application code.

# @Examples (Do's and Don'ts)

### Browser Lifecycle and Test Structure
**[DO]** Use `unittest.TestCase`, `setUp`, and `tearDown`.
```python
import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("To-Do", self.browser.title)

if __name__ == "__main__":
    unittest.main()
```

**[DON'T]** Use global variables and raw scripts that leave browsers hanging.
```python
from selenium import webdriver

browser = webdriver.Firefox()
browser.get("http://localhost:8000")
assert "To-Do" in browser.title
# Anti-pattern: Browser is never explicitly quit if the assertion fails.
```

### Assertions
**[DO]** Use `unittest` helper methods for clear failure output.
```python
self.assertIn("To-Do", self.browser.title)
```

**[DON'T]** Use raw assert keywords that result in unhelpful `AssertionError` tracebacks.
```python
assert "To-Do" in browser.title
```

### Comments and User Stories
**[DO]** Write comments that tell the human-readable story from the user's perspective.
```python
# Edith has heard about a cool new online to-do app.
# She goes to check out its homepage
self.browser.get("http://localhost:8000")

# She notices the page title and header mention to-do lists
self.assertIn("To-Do", self.browser.title)

# She is invited to enter a to-do item straight away
self.fail("Finish the test!")
```

**[DON'T]** Write redundant comments that explain standard code mechanics.
```python
# Call the get method on the browser object
self.browser.get("http://localhost:8000")

# Use assertIn to check if To-Do is in the title
self.assertIn("To-Do", self.browser.title)
```