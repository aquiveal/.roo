# @Domain
Functional Testing in Python with Selenium, Test Suite Refactoring, UI Interaction Testing, Multi-User Simulation, and Django Feature Implementation (specifically social/sharing features). Trigger these rules when the user requests refactoring of functional tests, handling multiple browser instances, abstracting UI elements, or implementing features using Outside-In Test-Driven Development (TDD).

# @Vocabulary
- **Page Object Pattern (Page Pattern)**: A testing design pattern where all the logic, information, CSS selectors, and helper methods for dealing with a specific page of a website are encapsulated in a single, dedicated class.
- **`addCleanup`**: A `unittest` method used to register cleanup functions that execute after `tearDown()`. Ideal for resources allocated halfway through a test.
- **Method Chaining**: A programming convenience where action methods return `self`, allowing consecutive method calls to be strung together on a single line (e.g., `ListPage(self).add_list_item("item")`).
- **Outside-In TDD**: A development methodology driven by functional tests that starts at the outer layers (presentation/templates), moves to the controller layer (URLs/views), and finally descends into the innermost layers (database models).

# @Objectives
- Eliminate duplication of HTML IDs, CSS selectors, and UI interaction logic across Functional Tests (FTs) by abstracting them into Page Objects.
- Safely and cleanly manage test resource teardown (like multiple browser instances) using `addCleanup` rather than complex conditional logic in `tearDown`.
- Facilitate complex multi-user FTs to simulate collaborative/social features (e.g., sharing lists between users).
- Follow a strict Outside-In TDD workflow when implementing new database-backed user-facing features.

# @Guidelines
- **Test Resource Management**:
  - The AI MUST use `self.addCleanup()` for any resources (like secondary web browsers) created mid-test.
  - The AI MUST NOT place conditional logic inside `tearDown()` to clean up resources that may or may not have been instantiated.
  - When cleaning up web browsers via `addCleanup`, the AI MUST wrap `browser.quit()` in a `try/except` block to gracefully handle browsers that may have already crashed or closed.
- **Page Object Implementation**:
  - The AI MUST extract page-specific actions, queries, and selectors into a dedicated class (e.g., `ListPage`, `MyListsPage`).
  - The AI MUST initialize Page Objects with the test context (`def __init__(self, test): self.test = test`) so the Page Object can access `self.test.browser` and `self.test.wait_for`.
  - The AI MUST return `self` from action methods inside Page Objects to enable method chaining.
  - The AI MUST define element locators as methods within the Page Object (e.g., `def get_share_box(self): return self.test.browser.find_element(...)`).
- **Multi-User Testing**:
  - The AI MUST use discrete browser instance variables (e.g., `edith_browser`, `oni_browser`) when simulating multiple users in a single FT.
  - The AI MUST explicitly reassign `self.browser` to the target user's browser before performing actions on their behalf.
- **Django Implementation (Outside-In)**:
  - When implementing shared/social data relationships, the AI MUST use a `ManyToManyField`.
  - The AI MUST explicitly handle clashing `related_name` attributes when adding a `ManyToManyField` to a Django model that relates to a User model.

# @Workflow
When tasked with refactoring FTs using the Page Pattern or implementing collaborative features, the AI MUST adhere to the following algorithmic process:

1. **Setup Multi-User FTs**:
   - Instantiate the primary user's browser.
   - Register the primary browser for cleanup using `self.addCleanup()`.
   - Instantiate the secondary user's browser.
   - Register the secondary browser for cleanup using `self.addCleanup()`.
   - Toggle `self.browser` between the primary and secondary browser variables to simulate distinct user actions.

2. **Implement Page Objects**:
   - Create a new file for the Page Object (e.g., `list_page.py`).
   - Define a class initialized with `test`.
   - Move `self.browser.find_element` and `self.browser.find_elements` calls from the FT into descriptive getter methods on the Page Object.
   - Move interaction sequences (e.g., typing text and pressing ENTER) into action methods on the Page Object.
   - End all action methods with `return self`.
   - Update the FT to instantiate the Page Object and call its methods.

3. **Drive Feature Implementation (Outside-In TDD)**:
   - **Step 1 (Template)**: Add the required UI elements (e.g., a share form input) to the HTML template to satisfy the first FT failure.
   - **Step 2 (URL & View Placeholder)**: Define the target URL in the template, wire it in `urls.py`, and create a minimal placeholder view.
   - **Step 3 (View Unit Test)**: Write a unit test asserting the view responds to POST requests and redirects appropriately.
   - **Step 4 (Model Unit Test & Model)**: Write a unit test for the required database relationship (e.g., adding a user to a list's `shared_with` collection). Update the model with a `ManyToManyField`, resolve `related_name` clashes, and generate migrations.
   - **Step 5 (View Logic)**: Update the view unit test to verify database state changes, then implement the view logic to perform the action.
   - **Step 6 (Template Display)**: Update templates to display the new data (e.g., rendering lists shared with the user).

# @Examples (Do's and Don'ts)

**[DO] Manage mid-test browser instances with `addCleanup` and a safe quit helper:**
```python
def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass

class SharingTest(FunctionalTest):
    def test_can_share_a_list_with_another_user(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(self.browser))
        
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
```

**[DON'T] Use conditional logic in tearDown for mid-test resources:**
```python
class SharingTest(FunctionalTest):
    def tearDown(self):
        if hasattr(self, 'oni_browser') and self.oni_browser:
            self.oni_browser.quit()
        self.browser.quit()
```

**[DO] Implement Page Objects that take `test` context and return `self` for chaining:**
```python
class ListPage:
    def __init__(self, test):
        self.test = test

    def get_share_box(self):
        return self.test.browser.find_element(By.CSS_SELECTOR, 'input[name="sharee"]')

    def share_list_with(self, email):
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
            email, [item.text for item in self.get_shared_with_list()]
        ))
        return self
```

**[DON'T] Scatter raw CSS selectors across multiple FT methods:**
```python
# Anti-pattern: Duplicating locators in the FT directly
share_box = self.browser.find_element(By.CSS_SELECTOR, 'input[name="sharee"]')
share_box.send_keys("friend@example.com")
share_box.send_keys(Keys.ENTER)
```

**[DO] Toggle `self.browser` explicitly when testing multiple users:**
```python
# Edith starts a list
self.browser = edith_browser
self.browser.get(self.live_server_url)

# Onesiphorus visits the page
self.browser = oni_browser
self.browser.get(self.live_server_url)
```