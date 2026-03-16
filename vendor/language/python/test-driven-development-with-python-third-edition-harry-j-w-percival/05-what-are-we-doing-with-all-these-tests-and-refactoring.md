# @Domain
Trigger these rules when the user requests tasks related to Test-Driven Development (TDD), Python web development, Django view/template creation, Selenium functional testing, test refactoring, or resolving HTML/UI validation in a testing context.

# @Vocabulary
- **Testing Goat**: The strict, uncompromising discipline of TDD that forces small steps and rigorous test-first methodologies.
- **TDD Ratchet**: The concept of using tests to save progress, ensuring the codebase never slips backward into a broken state, preventing cognitive overload.
- **Boiled Frog Problem**: The danger of complexity sneaking up gradually on un-tested trivial functions, eventually turning them into unmaintainable spaghetti code.
- **Testing Constants**: The anti-pattern of asserting exact raw strings (like HTML tags) in unit tests instead of testing logic or configuration.
- **Smoke Test**: A minimal test (e.g., checking for a specific keyword in rendered output) that quickly verifies if core behaviour is intact, guarding against implementation-specific brittle tests (like empty templates).
- **Refactoring**: Improving code structure or readability without changing its functionality.
- **Refactoring Cat**: The anti-pattern/danger of getting carried away, skipping steps, changing tests and code simultaneously, and ending up with a completely broken application.
- **Double-Loop TDD**: The nested TDD workflow. The "Outer Loop" uses Functional Tests (FTs) to drive high-level features. The "Inner Loop" uses Unit Tests to drive low-level implementation details.
- **Expected Failure**: A test failure that occurs exactly for the reason predicted, proving the test is correctly evaluating the missing or incomplete code.

# @Objectives
- The AI MUST enforce the discipline of TDD, ensuring every single code change is justified by a failing test.
- The AI MUST prevent the "Boiled Frog Problem" by establishing test placeholders even for trivial, one-line functions.
- The AI MUST maintain test reliability by decoupling unit tests from exact HTML strings, utilizing Django templates and high-level behavioral smoke tests.
- The AI MUST execute refactoring safely by strictly isolating code changes from test changes.
- The AI MUST drive all feature development using Double-Loop TDD (Functional tests for the user story, Unit tests for the implementation).

# @Guidelines

### 1. The Rule of Trivial Tests
- When encountering a trivial function or constant return, the AI MUST write a unit test for it.
- The AI MUST NOT use subjective judgments about whether code is "complicated enough" to warrant a test.
- **Action:** Treat the trivial test as a placeholder to lower the psychological barrier for future additions (e.g., `if` statements or `for` loops). 

### 2. "Don't Test Constants" Rule
- When generating unit tests for HTML output, the AI MUST NOT test exact, raw HTML strings (e.g., `self.assertTrue(html.startswith('<html>'))`).
- **Action:** Refactor the codebase to use Django templates (`render()`) and update the test to use `self.assertTemplateUsed()`.

### 3. Test Behaviour, Not Implementation
- When testing templates, the AI MUST acknowledge that testing *only* the template name is testing an implementation detail (which makes the test brittle to empty files or renamed templates).
- **Action:** The AI MUST pair `assertTemplateUsed()` with a minimal Smoke Test using `assertContains()` to verify that a core piece of user-visible behaviour (e.g., a specific word or title) is actually rendered.

### 4. The Golden Rule of Refactoring
- When instructed to refactor, the AI MUST work on EITHER the application code OR the test code, but NEVER both simultaneously.
- **Action:** Before refactoring, the AI MUST ensure the test suite is entirely green. During refactoring, the tests act as the guarantee that behaviour is preserved.

### 5. Selenium and Functional Testing Constraints
- When a Selenium action causes a page refresh (e.g., `send_keys(Keys.ENTER)`), the AI MUST insert an explicit wait (e.g., `time.sleep(1)`) before the next assertion.
- When searching for elements, the AI MUST strictly distinguish between `find_element` (returns one element, raises exception if missing) and `find_elements` (returns a list, may be empty).
- When writing functional tests, the AI MUST utilize Pythonic built-ins like `any()` combined with generator expressions for concise assertions across collections of elements.
- **Action:** When `assertTrue` or `assertFalse` fails cryptically, the AI MUST add custom, human-readable error messages to the assertion (e.g., `self.assertTrue(condition, "Custom error message")`).

### 6. Test-Driven Guidance
- When the AI is unsure of what to do next, it MUST execute the test suite. 
- **Action:** The AI MUST read the traceback, find the expected failure, and use that exact failure to dictate the minimal next code change.

# @Workflow
When tasked with adding a new feature, fixing a bug, or refactoring, the AI MUST follow this rigid algorithm:

1. **Outer Loop (Functional Test):**
   - Write or update a Functional Test (FT) capturing the user story.
   - Run the FT and confirm it fails (Expected Failure).
2. **Inner Loop (Unit Test):**
   - Write a Unit Test defining the specific programmer-facing behaviour needed to satisfy the FT's current failure.
   - Run the Unit Test and confirm it fails.
3. **Minimal Code Change:**
   - Write the absolute minimal amount of application code required to pass the Unit Test.
4. **Verify Inner Loop:**
   - Rerun the Unit Test. If it fails, repeat Step 3. If it passes, proceed to Step 5.
5. **Verify Outer Loop:**
   - Rerun the Functional Test. If it fails with a *new* error, return to Step 2. If it passes, the feature is complete.
6. **Refactor:**
   - Look for duplication, hardcoded strings, or constants.
   - Run tests to ensure state is Green.
   - Modify the code OR the tests (never both).
   - Rerun tests to ensure state remains Green.

# @Examples (Do's and Don'ts)

### Testing HTML Responses
- **[DON'T]** Test raw HTML constants in a unit test:
  ```python
  def test_home_page_returns_correct_html(self):
      request = HttpRequest()
      response = home_page(request)
      html = response.content.decode('utf8')
      self.assertTrue(html.startswith('<html>'))
      self.assertIn('<title>To-Do lists</title>', html)
  ```
- **[DO]** Use templates, `assertTemplateUsed`, and a behavioural smoke test:
  ```python
  def test_uses_home_template(self):
      response = self.client.get('/')
      self.assertTemplateUsed(response, 'home.html')

  def test_renders_homepage_content(self):
      response = self.client.get('/')
      self.assertContains(response, 'To-Do')
  ```

### Writing Assertions in Functional Tests
- **[DON'T]** Use generic assertions that provide cryptic failure tracebacks for lists:
  ```python
  rows = table.find_elements(By.TAG_NAME, 'tr')
  self.assertTrue(any(row.text == '1: Buy peacock feathers' for row in rows))
  # Failure yields: AssertionError: False is not true
  ```
- **[DO]** Pass custom error messages to explain the failure context:
  ```python
  rows = table.find_elements(By.TAG_NAME, 'tr')
  self.assertTrue(
      any(row.text == '1: Buy peacock feathers' for row in rows),
      f"New to-do item did not appear in table. Contents were:\n{table.text}"
  )
  ```

### Handling Page Refreshes in Selenium
- **[DON'T]** Assert immediately after triggering a page load:
  ```python
  inputbox.send_keys(Keys.ENTER)
  table = self.browser.find_element(By.ID, 'id_list_table') # May raise StaleElement or NoSuchElement
  ```
- **[DO]** Use an explicit wait to allow the browser to update:
  ```python
  inputbox.send_keys(Keys.ENTER)
  time.sleep(1)
  table = self.browser.find_element(By.ID, 'id_list_table')
  ```

### Refactoring
- **[DON'T]** Change the application code to use a template AND change the test to use `assertTemplateUsed` in the same step.
- **[DO]** Refactor the application code to use `render()` while keeping the old constant-based tests. Verify the tests pass (behaviour is preserved). *Then* refactor the tests to use `assertTemplateUsed`.