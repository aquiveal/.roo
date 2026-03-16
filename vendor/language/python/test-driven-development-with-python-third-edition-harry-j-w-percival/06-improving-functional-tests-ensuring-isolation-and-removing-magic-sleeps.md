@Domain
Functional Testing in Python and Django using Selenium, specifically triggered when the AI is tasked with creating, refactoring, or debugging functional/end-to-end tests, managing test isolation, or implementing mechanisms to wait for browser/UI state changes.

@Vocabulary
- **Functional Test (FT)**: A high-level, black-box test that drives a real web browser to simulate user interactions from end to end.
- **Test Isolation**: The practice of ensuring that the execution of one test does not alter the global state (e.g., the database) in a way that affects subsequent tests.
- **LiveServerTestCase**: A Django test class that automatically spins up a background development server and creates an isolated, ephemeral test database for functional testing.
- **Magic Sleeps**: Anti-pattern. The use of arbitrary, fixed-duration pauses (e.g., `time.sleep(1)`) to wait for asynchronous UI changes, leading to brittle, slow, and flaky tests.
- **Explicit Wait**: An algorithmic pattern that continuously polls the application state, proceeding immediately when a condition is met, or failing safely after a maximum timeout threshold is breached.
- **Implicit Wait**: A built-in Selenium feature (`implicitly_wait`) that attempts to automatically wait for elements. It is considered unreliable and an anti-pattern.
- **WebDriverException**: A Selenium exception frequently raised when attempting to interact with or locate a DOM element before the page has finished loading.

@Objectives
- Guarantee total test isolation so that database records and state modifications from one functional test do not bleed into or contaminate subsequent tests.
- Eliminate arbitrary fixed timeouts ("magic sleeps") to optimize test execution speed and eradicate false positives (flaky tests).
- Structure functional tests as a native Django app to seamlessly integrate with the default Django test runner.
- Enforce deterministic DOM interaction through robust explicit polling and retry loops.

@Guidelines
- The AI MUST structure functional tests within a dedicated Python package (e.g., a folder named `functional_tests/` containing an `__init__.py` file and test files like `tests.py`).
- The AI MUST NOT place functional tests in a standalone script in the project root.
- The AI MUST ensure functional test classes inherit from `django.test.LiveServerTestCase` (or `django.contrib.staticfiles.testing.StaticLiveServerTestCase` for static files) rather than standard `unittest.TestCase`.
- The AI MUST use `self.live_server_url` for browser navigation instead of hardcoding localhost addresses (e.g., `http://localhost:8000`).
- The AI MUST NEVER use arbitrary `time.sleep(N)` commands to wait for page loads or DOM updates.
- The AI MUST NOT use Selenium's `implicitly_wait` feature.
- When verifying asynchronous UI changes, the AI MUST implement custom explicit wait helper methods (e.g., `wait_for...`).
- The AI MUST implement explicit wait loops using a `while True` construct combined with a `try/except` block.
- The AI MUST catch BOTH `AssertionError` and `selenium.common.exceptions.WebDriverException` inside the explicit wait `try/except` block.
- The AI MUST define and enforce a maximum timeout threshold (e.g., `MAX_WAIT = 5`) within polling loops to prevent infinite hangs.
- If the `MAX_WAIT` threshold is exceeded during a polling loop, the AI MUST explicitly re-raise the caught exception.

@Workflow
1. **Audit Test Structure**: Check if functional tests reside in a standalone file. If so, create a `functional_tests` directory, add an `__init__.py` file, and move the test files inside.
2. **Upgrade Test Class Inheritance**: Modify the functional test class to inherit from `LiveServerTestCase` (requires `from django.test import LiveServerTestCase`).
3. **Abstract Navigation URLs**: Scan for `self.browser.get("http://localhost:...")` and replace the hardcoded string with `self.live_server_url`. Remove any `if __name__ == '__main__':` blocks, as the Django test runner will handle execution.
4. **Audit for Magic Sleeps**: Search the functional test codebase for `time.sleep()` statements used for pacing browser interactions.
5. **Implement Polling Helper**: Create a helper method (e.g., `wait_for_row_in_list_table(self, row_text)`) to encapsulate the condition being tested.
6. **Construct the Retry Loop**: Inside the helper method:
    - Record the start time: `start_time = time.time()`.
    - Start an infinite loop: `while True:`.
    - Open a `try` block and execute the DOM fetch and assertion (e.g., `find_element` and `assertIn`). If successful, `return` to exit the loop.
    - Open an `except` block targeting `(AssertionError, WebDriverException) as e:`.
    - Check the elapsed time: `if time.time() - start_time > MAX_WAIT: raise e`.
    - If the timeout has not been reached, pause briefly before retrying: `time.sleep(0.5)`.
7. **Refactor Tests**: Replace all instances of magic sleeps + raw assertions with invocations of the newly created explicit wait helper method.

@Examples (Do's and Don'ts)

**Test Class Inheritance and Navigation**
- [DON'T]
```python
import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def test_can_start_a_todo_list(self):
        self.browser.get("http://localhost:8000")
```

- [DO]
```python
from django.test import LiveServerTestCase
from selenium import webdriver

class NewVisitorTest(LiveServerTestCase):
    def test_can_start_a_todo_list(self):
        self.browser.get(self.live_server_url)
```

**Waiting for UI Updates (Explicit Waits vs Magic Sleeps)**
- [DON'T]
```python
import time

def test_can_start_a_todo_list(self):
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)  # Magic sleep - ANTI-PATTERN
    
    table = self.browser.find_element(By.ID, "id_list_table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    self.assertIn("1: Buy peacock feathers", [row.text for row in rows])
```

- [DO]
```python
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 5

def wait_for_row_in_list_table(self, row_text):
    start_time = time.time()
    while True:
        try:
            table = self.browser.find_element(By.ID, "id_list_table")
            rows = table.find_elements(By.TAG_NAME, "tr")
            self.assertIn(row_text, [row.text for row in rows])
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)

def test_can_start_a_todo_list(self):
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table("1: Buy peacock feathers")
```