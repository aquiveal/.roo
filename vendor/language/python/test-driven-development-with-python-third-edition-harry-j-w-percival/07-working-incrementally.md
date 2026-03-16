# @Domain
Trigger these rules when the user requests architectural refactoring, data model alterations, URL routing restructuring, or the implementation of new features requiring changes to existing, tested Python/Django codebases. These rules govern the process of adapting existing code using an incremental, step-by-step methodology (Test-Driven Development) to move safely from one working state to another.

# @Vocabulary
- **YAGNI ("You ain't gonna need it")**: The Agile principle dictating that developers should resist the urge to build features or write code based on anticipated future needs.
- **Big Design Up Front (BDUF)**: An anti-pattern in Agile/TDD where a lengthy design stage attempts to anticipate all system requirements before coding begins.
- **Working State to Working State**: The philosophy of breaking large refactors into microscopic steps so that the application and its test suite are never broken for long.
- **Testing Goat**: The personification of rigorous, step-by-step TDD discipline.
- **Refactoring Cat**: The anti-pattern of diving in, making massive systemic changes all at once, and ending up with dozens of broken tests and an un-runnable application.
- **REST-ish**: A pragmatic approach to URL routing that maps URLs to data structures (e.g., `/lists/<id>/`) without strictly adhering to pure REST protocols if HTML forms restrict HTTP methods (e.g., using POST instead of PUT).
- **Regression Test**: An existing Functional Test (FT) that is kept active while building new features to guarantee that existing functionality is not accidentally broken.
- **Meta-comments (`##`)**: Comments in test code used to explain *how* or *why* the test mechanics work (e.g., `## We delete cookies to simulate a new user`), distinguishing them from standard single-hash `#` comments that describe the User Story.
- **Programming by Wishful Thinking**: A design technique where the developer writes tests or templates using variables, APIs, or URLs that do not exist yet, letting those "wishes" drive the implementation of the underlying backend code.

# @Objectives
- The AI MUST safely transition an application from an old design to a new design without breaking existing functionality.
- The AI MUST fight the urge to rewrite everything at once; all architectural changes MUST be broken down into the smallest possible self-contained steps.
- The AI MUST use existing tests to verify that intermediate refactoring steps do not cause regressions.
- The AI MUST avoid writing code for anticipated future requirements (YAGNI).

# @Guidelines

### 1. Incremental Architecture & Design
- When planning a new feature, the AI MUST NOT engage in "Big Design Up Front". Instead, define the Minimum Viable Product (MVP) and let the design evolve gradually.
- When encountering ideas for future enhancements, the AI MUST strictly apply YAGNI and refuse to write code that is not strictly required by the current failing test.
- When refactoring, the AI MUST adhere to "Working State to Working State" by making one localized change at a time (e.g., hardcoding a temporary URL for a single list before building dynamic routing for multiple lists).
- If tests fail unexpectedly during a refactor, the AI MUST find the quickest, simplest path to get back to a green (passing) state before continuing the refactor.

### 2. URL Routing and REST-ish Standards
- The AI MUST format "View" URLs (GET requests to view data) WITH a trailing slash (e.g., `/lists/<list_id>/`).
- The AI MUST format "Action" URLs (POST requests that modify data) WITHOUT a trailing slash (e.g., `/lists/new` or `/lists/<list_id>/add_item`).
- The AI MUST be aware that Django will issue a 301 redirect if a view URL is requested without a trailing slash (if `APPEND_SLASH` is true), which can cause 404s or unexpected test failures.
- When configuring top-level `urls.py`, the AI MUST use `include()` to delegate routing to app-specific `urls.py` files.
- When importing views from multiple apps in a top-level `urls.py`, the AI MUST use the alias syntax: `from app_name import views as app_name_views`.

### 3. Functional Testing (FT) Practices
- When writing FTs, the AI MUST use `##` for meta-comments regarding test mechanics to separate them from `#` User Story comments.
- When verifying that URLs conform to new REST-ish designs, the AI MUST use `self.assertRegex(url, r"pattern")`.
- **CRITICAL - Race Condition Prevention:** When testing UI transitions in Selenium (e.g., submitting a form that reloads a page with new and old items), the AI MUST assert the presence of the *newest* element FIRST. If it asserts the old element first, Selenium might read the old page state right before it reloads, causing intermittent flaky test failures.
- The AI MUST use existing FTs as regression tests to ensure new feature work does not break previous working states.

### 4. Database Models and Migrations
- When adjusting models (e.g., adding `ForeignKey` relationships), the AI MUST create step-by-step test coverage for the new attributes.
- The AI MUST NOT test for "Developer Silliness." The AI should test that standard constraints work, but MUST NOT write exhaustive tests checking that a developer didn't intentionally write perverse or actively malicious implementation code.
- **CRITICAL - Migration Safety:** The AI MUST NEVER suggest modifying or deleting a Django database migration file that has already been committed to Git. If an error is made in a local, uncommitted migration, it is acceptable to delete it and recreate it; otherwise, a new migration MUST be generated.

### 5. Template Integration
- The AI MUST utilize "Programming by Wishful Thinking" by putting desired variables into templates first, then letting failing tests dictate what context variables the view needs to provide.
- The AI MUST be aware that Django templates silently ignore undefined variables by substituting empty strings, which can result in malformed URLs (e.g., `/lists//add_item` instead of `/lists/1/add_item`).

# @Workflow
When tasked with refactoring an application to support a new data dimension or architectural structure, the AI MUST adhere to this exact sequence:
1. **Analyze Requirements via FT**: Write or modify a Functional Test that describes the new requirement from the user's perspective, complete with URL regex checks and new interaction flows. Run it to get the expected failure.
2. **Define the Smallest Step**: Identify the smallest possible, temporary, isolated change that moves the codebase forward (e.g., changing a redirect to a hardcoded specific URL).
3. **Unit Test the Step**: Write a unit test specifically for that intermediate step.
4. **Implement the Step**: Write the minimal code to pass the unit test.
5. **Check Regressions**: Run the FTs to verify the old features still work and the new feature has progressed slightly.
6. **Separate Concerns**: If a view is doing too much (e.g., handling home page and list viewing), separate the logic into distinct views and templates *one at a time*.
7. **Address the Database**: Only after views and URLs are separated should the AI move down to the model layer to introduce new database fields or relationships, testing them explicitly.
8. **Re-integrate**: Connect the new model layer back up through the view and to the template.
9. **Refactor**: Once all tests are green, refactor for DRY principles (e.g., extracting duplicated URL paths into `urls.py` includes).

# @Examples (Do's and Don'ts)

### Handling Selenium Race Conditions
- **[DO]** Assert the new state before the old state to guarantee the page has refreshed.
```python
# The page updates again, and now shows both items on her list
self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")
self.wait_for_row_in_list_table("1: Buy peacock feathers")
```
- **[DON'T]** Assert the old state first; this will pass while the old page is still visible, and then fail randomly when the page reloads during the second assertion.
```python
# ANTI-PATTERN: Causes race condition failures
self.wait_for_row_in_list_table("1: Buy peacock feathers")
self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")
```

### URL Formatting
- **[DO]** Use trailing slashes for views, and omit them for actions.
```python
urlpatterns = [
    path("new", views.new_list, name="new_list"), # Action, no slash
    path("<int:list_id>/", views.view_list, name="view_list"), # View, trailing slash
]
```
- **[DON'T]** Omit trailing slashes on views, which causes Django 301/404 confusion.
```python
urlpatterns = [
    path("<int:list_id>", views.view_list, name="view_list"), # Missing trailing slash
]
```

### Test Comments
- **[DO]** Use `##` to explain test execution mechanics to future developers.
```python
# Now a new user, Francis, comes along to the site.
## We delete all the browser's cookies
## as a way of simulating a brand new user session
self.browser.delete_all_cookies()
```
- **[DON'T]** Muddle technical execution comments with the user story using standard single hashes.
```python
# Now a new user comes to the site
# we delete cookies here because otherwise the session persists
self.browser.delete_all_cookies()
```

### URL Imports in top-level `urls.py`
- **[DO]** Use aliases for view imports to prevent namespace collisions.
```python
from lists import views as list_views
from accounts import views as accounts_views
```
- **[DON'T]** Import views blindly, risking overwrites.
```python
from lists.views import *
from accounts.views import *
```