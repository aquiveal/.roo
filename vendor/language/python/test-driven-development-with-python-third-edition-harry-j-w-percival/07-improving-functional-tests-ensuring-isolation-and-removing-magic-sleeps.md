# @Domain
Django application development, specifically writing, structuring, and refactoring Functional Tests (FTs) using Selenium WebDriver, managing browser wait times, ensuring database isolation, and executing tests via the Django test runner. Trigger these rules whenever modifying end-to-end tests, UI tests, or Selenium browser automation within a Django project.

# @Vocabulary
- **Functional Test (FT)**: An end-to-end test that drives a real web browser to test the application from the user's perspective.
- **Test Isolation**: The practice of ensuring that different test runs do not interfere with one another (e.g., by leaving stale data in the database).
- **LiveServerTestCase**: A Django testing class that automatically spins up a background development server and creates a clean test database for FTs.
- **Magic Sleep**: An anti-pattern using hardcoded `time.sleep(N)` to wait for page loads, which causes either spurious test failures (if too short) or unnecessarily slow test suites (if too long).
- **Implicit Wait**: A Selenium feature (`implicitly_wait`) that attempts to automatically wait for elements, which is unreliable and disabled by default in modern Selenium.
- **Explicit Wait**: A robust testing pattern utilizing a custom polling/retry loop to repeatedly attempt to locate an element or assert a condition until a timeout is reached.
- **Spurious Failure / False Positive**: A test that fails not because the application is broken, but because the test infrastructure (like a rigid timeout) failed to account for environmental slowness.
- **WebDriverException**: An exception raised by Selenium when it cannot interact with the browser or find an element because the page has not fully loaded.
- **AssertionError**: An exception raised when a test assertion fails, which in the context of FTs often means the page has loaded but the expected state has not yet rendered.

# @Objectives
- Ensure absolute test isolation by utilizing Django's built-in testing classes rather than running tests against the local development database.
- Integrate Functional Tests natively into the Django project structure so they are discovered and executed by Django's test runner.
- Eradicate all "magic sleeps" (`time.sleep(N)`) and unreliable implicit waits from the test suite.
- Implement robust, deterministic explicit wait mechanisms (polling loops) to drastically reduce spurious test failures while minimizing total test execution time.

# @Guidelines
- **Directory Structure Requirements**: The AI MUST NOT place Functional Tests in a standalone script in the project root (e.g., `functional_tests.py`). The AI MUST structure FTs as a valid Python package (e.g., `functional_tests/tests.py` accompanied by an `__init__.py` file).
- **Test Class Inheritance**: The AI MUST inherit Functional Test classes from `django.test.LiveServerTestCase` (or `StaticLiveServerTestCase`), NEVER from standard `unittest.TestCase`. 
- **Dynamic URL Resolution**: The AI MUST NEVER hardcode `localhost` or specific ports (e.g., `http://localhost:8000`) within FTs. The AI MUST use `self.live_server_url` provided by `LiveServerTestCase`.
- **Prohibition of Magic Sleeps**: The AI MUST NEVER use arbitrary `time.sleep(N)` to wait for UI updates, page refreshes, or element rendering.
- **Prohibition of Implicit Waits**: The AI MUST NOT configure or rely upon Selenium's `implicitly_wait`.
- **Explicit Wait Implementation**: When waiting for a UI state change, the AI MUST implement a custom retry/polling loop.
- **Polling Loop Constraints**:
  - The loop MUST be governed by a `MAX_WAIT` constant (e.g., 5 seconds).
  - The loop MUST use a `while True:` block.
  - The loop MUST wrap the Selenium interactions and test assertions inside a `try/except` block.
  - The `except` block MUST explicitly catch both `AssertionError` and `WebDriverException`.
  - Inside the `except` block, the AI MUST calculate elapsed time. If elapsed time exceeds `MAX_WAIT`, the AI MUST re-raise the exception.
  - If elapsed time is within limits, the AI MUST execute a microscopic sleep (e.g., `time.sleep(0.5)`) before allowing the loop to continue.
- **Targeted Test Execution**: The AI MUST use `python manage.py test <app_name>` to execute specific test suites (e.g., `python manage.py test functional_tests` for FTs, or `python manage.py test lists` for unit tests) instead of running the whole suite or standalone scripts.

# @Workflow
When tasked with creating or improving Functional Tests, the AI MUST strictly follow this sequence:
1. **App Initialization**: Ensure the functional tests exist within an app directory (e.g., `functional_tests/`) containing an `__init__.py` file. If they are in a root script, migrate them using `git mv`.
2. **Class Refactoring**: Update the test class to inherit from `LiveServerTestCase`. Remove any standard `unittest.main()` execution blocks.
3. **URL Refactoring**: Scan the test for hardcoded URLs (e.g., `http://localhost:8000`) and replace them with `self.live_server_url`.
4. **Wait Helper Generation**: Create a helper method (e.g., `wait_for_row_in_list_table`) that implements the strict explicit wait polling loop specified in the guidelines.
5. **Sleep Eradication**: Scan the test for any `time.sleep()` calls immediately following browser interactions (like `send_keys(Keys.ENTER)`). Remove the sleeps and replace the subsequent assertions with calls to the newly created wait helper.
6. **Execution**: Verify the changes by instructing the user to run the targeted test suite via the `manage.py test <app_name>` command.

# @Examples (Do's and Don'ts)

**FT Directory Structure**
- [DO]: Place tests in a package to allow discovery by Django's test runner.
  ```text
  project_root/
  ├── functional_tests/
  │   ├── __init__.py
  │   └── tests.py
  ```
- [DON'T]: Leave FTs as standalone root scripts.
  ```text
  project_root/
  ├── functional_tests.py
  ```

**Test Class and URL Setup**
- [DO]: Use `LiveServerTestCase` and its dynamic URL attribute.
  ```python
  from django.test import LiveServerTestCase
  from selenium import webdriver

  class NewVisitorTest(LiveServerTestCase):
      def setUp(self):
          self.browser = webdriver.Firefox()

      def test_can_start_a_todo_list(self):
          self.browser.get(self.live_server_url)
  ```
- [DON'T]: Use standard `unittest` and hardcoded localhost URLs for Django FTs.
  ```python
  import unittest
  from selenium import webdriver

  class NewVisitorTest(unittest.TestCase):
      def setUp(self):
          self.browser = webdriver.Firefox()

      def test_can_start_a_todo_list(self):
          self.browser.get("http://localhost:8000")
  ```

**Handling Page Loads and UI Changes (Waits)**
- [DO]: Implement a robust polling loop catching both state (`AssertionError`) and rendering (`WebDriverException`) failures.
  ```python
  import time
  from selenium.common.exceptions import WebDriverException

  MAX_WAIT = 5

  # Inside the test class:
  def wait_for_row_in_list_table(self, row_text):
      start_time = time.time()
      while True:
          try:
              table = self.browser.find_element(By.ID, "id_list_table")
              rows = table.find_elements(By.TAG_NAME, "tr")
              self.assertIn(row_text, [row.text for row in rows])
              return  # Exit loop if assertion passes
          except (AssertionError, WebDriverException) as e:
              if time.time() - start_time > MAX_WAIT:
                  raise e  # Timeout reached, bubble up the failure
              time.sleep(0.5)  # Wait before retrying
  ```
- [DON'T]: Use magic sleeps that cause race conditions, false positives, and slow tests.
  ```python
  # Anti-pattern: Magic sleep
  def test_can_start_a_todo_list(self):
      inputbox.send_keys(Keys.ENTER)
      time.sleep(1)  # DON'T DO THIS
      
      table = self.browser.find_element(By.ID, "id_list_table")
      rows = table.find_elements(By.TAG_NAME, "tr")
      self.assertIn("1: Buy peacock feathers", [row.text for row in rows])
  ```