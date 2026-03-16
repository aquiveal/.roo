# @Domain
These rules activate whenever the AI is engaged in:
- Test-Driven Development (TDD) workflows in Python (specifically using Django and `unittest`).
- Writing or modifying functional tests (end-to-end tests) using Selenium WebDriver.
- Writing or modifying unit tests for web views and templates.
- Performing code refactoring.
- Debugging test failures or configuring HTML/CSS templates.

# @Vocabulary
- **Testing Goat**: The personification of rigorous TDD discipline. Represents the mindset of being uncompromising and bloody-minded about writing tests before writing code, taking small steps, and never skipping trivial tests.
- **Refactoring Cat**: An anti-pattern persona representing the dangerous temptation to change multiple things at once, skip ahead, or mix functionality additions with refactoring, resulting in broken code.
- **TDD Ratchet**: A metaphor (by Kent Beck) comparing TDD to lifting a heavy bucket out of a well. Tests act as a ratchet that saves progress, ensuring you never slip backward, so you don't have to be "smart all the time."
- **Double-Loop TDD**: The nested cycle of testing. The outer loop is driven by Functional Tests (testing high-level requirements from the user's perspective). The inner loop is driven by Unit Tests (testing low-level details from the programmer's perspective).
- **Smoke Test**: A minimal test designed to quickly verify that core functionality or content exists without exhaustively testing every detail (e.g., verifying a core string exists in a template).
- **Expected Failure**: A test failure that occurs exactly as predicted because the required application code has not been written yet. It acts as permission to write new code.
- **Refactoring**: Improving the structure or design of existing code without changing its external functionality.

# @Objectives
- **Enforce the TDD Ratchet**: Guarantee that progress is systematically locked in by writing tests before implementation, reducing cognitive load and preventing regression.
- **Decouple Tests from Implementation**: Transition tests from brittle, constant-checking assertions to behavior-focused abstractions.
- **Maintain Strict Separation of Concerns**: Keep Python code focused on logic and flow control, and move raw HTML/UI formatting strictly into template files.
- **Ensure Safe Refactoring**: Prevent the mixing of behavior changes with structural code improvements.

# @Guidelines

### Test Generation & Granularity
- The AI MUST write tests for even the most trivial functions or constants. These serve as placeholders that prevent the "boiled frog" problem of complexity sneaking up on untested code.
- The AI MUST NOT skip writing a test based on subjective, hand-wavy rules about a function being "too simple."
- The AI MUST provide custom, descriptive error messages as the second parameter to boolean assertions (e.g., `assertTrue`, `assertFalse`) if the default failure message lacks context.

### Selenium and Functional Testing
- When expecting a single mandatory UI element, the AI MUST use `find_element(...)`. (This raises an exception if the element is missing).
- When expecting a list of elements that might legitimately be empty, the AI MUST use `find_elements(...)`.
- The AI MUST implement an explicit wait (e.g., `time.sleep()`) immediately after triggering an action that causes a page refresh (such as `Keys.ENTER` or a form submit) before executing the next assertion.

### Unit Testing and Templates
- **The "Don't Test Constants" Rule**: The AI MUST NOT write unit tests that assert against long, raw HTML strings or exact sequences of characters.
- The AI MUST extract HTML out of Python views and place it into dedicated `.html` template files to allow for syntax highlighting and separation of concerns.
- The AI MUST use higher-level abstraction testing (e.g., Django's `assertTemplateUsed`) to verify that a view renders the correct template.
- The AI MUST supplement template-used assertions with a minimal "Smoke Test" (e.g., checking for a core word like "To-Do") to protect against the template file accidentally being emptied or deleted.

### Refactoring Rules
- The AI MUST strictly separate refactoring from adding new features. 
- The AI MUST verify that all tests are passing (Green) before initiating any refactoring.
- The AI MUST work on either the code OR the tests during a refactor, but NEVER both simultaneously.

# @Workflow
The AI MUST adhere to the following rigid algorithmic process for Double-Loop TDD:

1. **Outer Loop (Functional Test - Red)**
   - Write a Functional Test describing a user story.
   - Run the FT and observe an Expected Failure.

2. **Inner Loop (Unit Test - Red)**
   - Determine the minimal implementation needed to progress the FT.
   - Write a Unit Test for that specific implementation detail.
   - Run the Unit Test and observe an Expected Failure.

3. **Inner Loop (Code - Green)**
   - Write the absolute minimum application code required to pass the current Unit Test.
   - Run the Unit Tests. If they fail, modify the code until they pass.

4. **Inner Loop (Refactor)**
   - With Unit Tests passing, look for opportunities to refactor the code (e.g., moving raw HTML into a template).
   - Ensure Unit Tests remain Green after the refactor.
   - Refactor the tests themselves to test behavior rather than implementation (e.g., replacing raw string matching with `assertTemplateUsed`).

5. **Outer Loop (Functional Test - Check)**
   - Rerun the Functional Test. 
   - If the FT fails, return to Step 2.
   - If the FT passes, proceed to Step 6.

6. **Outer Loop (Refactor)**
   - With both Unit and Functional Tests passing, perform any high-level refactoring.
   - Commit the working state to version control.

# @Examples (Do's and Don'ts)

### 1. Refactoring Discipline
- **[DO]** Run the test suite, confirm a Green state, change the implementation of a view to use a `render()` shortcut instead of a manual `HttpResponse()`, run the test suite again to confirm Green, and commit.
- **[DON'T]** Change a view to use a template AND add a new input field to the UI in the same step. (Avoid the Refactoring Cat anti-pattern).

### 2. Testing Templates
- **[DO]** Test behavior and include a minimal smoke test:
  ```python
  def test_uses_home_template(self):
      response = self.client.get("/")
      self.assertTemplateUsed(response, "home.html")

  def test_renders_homepage_content(self):
      response = self.client.get("/")
      self.assertContains(response, "To-Do")
  ```
- **[DON'T]** Test raw HTML constants:
  ```python
  def test_home_page_returns_correct_html(self):
      response = self.client.get("/")
      html = response.content.decode("utf8")
      self.assertTrue(html.startswith("<html>"))
      self.assertIn("<title>To-Do lists</title>", html)
      self.assertTrue(html.endswith("</html>"))
  ```

### 3. Assertion Clarity
- **[DO]** Provide explicit error messages for obscure boolean checks:
  ```python
  self.assertTrue(
      any(row.text == "1: Buy peacock feathers" for row in rows),
      f"New to-do item did not appear in table. Contents were:\n{table.text}"
  )
  ```
- **[DON'T]** Rely on default, cryptic error messages:
  ```python
  self.assertTrue(any(row.text == "1: Buy peacock feathers" for row in rows))
  # Leads to: AssertionError: False is not true
  ```