# @Domain
These rules apply whenever the AI is interacting with, creating, or modifying Functional Tests (FTs), particularly when using Selenium Webdriver in a Python/Django environment. This domain is activated when the user requests to optimize test speed, skip repetitive UI workflows (such as authentication/login), set up test data (fixtures), or refactor explicit wait/polling mechanisms.

# @Vocabulary
*   **Test Fixture**: The initial state, environment, or data preconditions required to run a test successfully (e.g., pre-populating a database or creating a browser cookie).
*   **SessionStore**: A Django backend interface (`django.contrib.sessions.backends.db.SessionStore`) used to programmatically create and manipulate server-side user sessions.
*   **JSON Fixtures**: A mechanism in Django for saving and restoring database states using JSON files (`dumpdata`/`loaddata`). Considered an anti-pattern in this methodology.
*   **Decorator**: A Python function used to wrap and modify the behavior of another function (e.g., abstracting a `while True` polling loop into a `@wait` prefix).
*   **Variadic Arguments**: The use of `*args` and `**kwargs` in Python to allow a wrapper function to accept any number of positional and keyword arguments, ensuring decorator flexibility.
*   **Explicit Wait**: A testing pattern where the code repeatedly polls the browser for a specific condition (catching expected exceptions) until a maximum timeout is reached.
*   **Separation of Concerns (in FTs)**: The principle that a specific functional test should focus on a single feature flow, bypassing unrelated, time-consuming UI sequences if they are already tested elsewhere.

# @Objectives
*   **Accelerate Feedback Loops**: Optimize Functional Test execution time by programmatically skipping redundant, slow UI interactions (like email-based or form-based logins).
*   **Enhance Code Readability**: Abstract repetitive `try/except` and `while True` timeout loops from test helper methods into a clean, reusable Python decorator.
*   **Ensure Test Data Maintainability**: Reject the use of brittle, hardcoded JSON data files in favor of utilizing the Django Object-Relational Mapper (ORM) for dynamic test fixture generation.
*   **Maintain Test Isolation**: Ensure that test fixtures and session bypass techniques do not cause tests to bleed state into one another.

# @Guidelines
*   **Bypassing Repetitive UI Flows**: When a Functional Test requires an authenticated user (but is not specifically testing the login mechanism), the AI MUST programmatically pre-create an authenticated session rather than driving the browser through the login UI.
*   **Programmatic Session Creation**: To pre-authenticate a user in Django, the AI MUST manually create a `SessionStore` object, assign the user's primary key to `SESSION_KEY`, assign the appropriate authentication backend to `BACKEND_SESSION_KEY`, and save the session.
*   **Injecting Cookies into Selenium**: Because HTTP is stateless and Selenium requires the browser to be on the target domain before setting a cookie, the AI MUST instruct the browser to visit a fast-loading page on the target domain (e.g., a deliberately non-existent 404 page) *before* calling `browser.add_cookie()`.
*   **Anti-Pattern: JSON Fixtures**: The AI MUST NOT use Django's `loaddata` or JSON fixtures to populate test databases. They are difficult to maintain during schema changes and obscure the specific data requirements of the test.
*   **ORM for Fixtures**: The AI MUST use the Django ORM (e.g., `User.objects.create()`) or dedicated factory methods with descriptive names to generate all test data.
*   **Refactoring Explicit Waits**: The AI MUST NOT duplicate timeout loops (`start_time = time.time()`, `while True`, `try/except`) across multiple Selenium helper methods.
*   **Wait Decorator Implementation**: The AI MUST encapsulate explicit wait logic inside a custom `@wait` decorator. 
*   **Decorator Signature Support**: The inner wrapper function of the `@wait` decorator MUST utilize variadic arguments (`*args, **kwargs`) and pass them to the target function to ensure the decorator can be applied to methods with varying signatures.
*   **Targeted Exception Handling in Waits**: The wait decorator MUST specifically catch `AssertionError` and `selenium.common.exceptions.WebDriverException`. It MUST calculate elapsed time against a predefined `MAX_WAIT` constant, and reraise the exact exception if the timeout is exceeded.
*   **FT De-duplication Caution**: While the AI MUST reduce duplication, it MUST NOT over-abstract FTs to the point where unexpected interactions between different parts of the application are masked.

# @Workflow
When tasked with optimizing Functional Tests, adding preconditions, or refactoring Selenium waits, the AI MUST follow this algorithmic process:

1.  **Analyze the Target FT Requirement**:
    *   Determine if the test requires a logged-in user.
    *   Check if the login process is the actual subject of the test. If not, proceed to programmatic session creation.
2.  **Implement Programmatic Session Fixtures**:
    *   Create a user via the ORM.
    *   Instantiate `SessionStore()`.
    *   Assign `session[SESSION_KEY]` and `session[BACKEND_SESSION_KEY]`.
    *   Call `session.save()`.
3.  **Inject the Session via Cookie**:
    *   Command the webdriver to visit a fast 404 URL (e.g., `self.live_server_url + "/404_no_such_url/"`).
    *   Command the webdriver to add the cookie using the generated `session.session_key` and Django's `SESSION_COOKIE_NAME`.
4.  **Refactor Repetitive Polling**:
    *   Identify helper methods containing `while True:` and `time.sleep()` loops.
    *   Create a `def wait(fn):` decorator.
    *   Implement an inner `modified_fn(*args, **kwargs):` that houses the `time.time()` loop, catching `AssertionError` and `WebDriverException`.
    *   Ensure the timeout condition `if time.time() - start_time > MAX_WAIT:` explicitly re-raises the caught exception.
    *   Return `modified_fn`.
5.  **Apply the Decorator**:
    *   Strip the loop and error-handling boilerplate from the target helper methods.
    *   Prefix the helper methods with `@wait`.
6.  **Verify Test Isolation**: Ensure that custom fixtures are isolated and do not bleed between tests.

# @Examples (Do's and Don'ts)

## [DO] Use the ORM and SessionStore to bypass UI login
```python
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

User = get_user_model()

def create_pre_authenticated_session(self, email):
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    
    # Visit a fast 404 page to establish domain context before setting cookie
    self.browser.get(self.live_server_url + "/404_no_such_url/")
    self.browser.add_cookie(
        dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path="/",
        )
    )
```

## [DON'T] Drive the browser through the login UI for every single test
```python
# ANTI-PATTERN: Wasting time testing the login UI in a test meant for a completely different feature.
def test_user_can_view_dashboard(self):
    self.browser.get(self.live_server_url)
    self.browser.find_element(By.NAME, "email").send_keys("edith@example.com")
    self.browser.find_element(By.NAME, "password").send_keys("password123")
    self.browser.find_element(By.ID, "submit").click()
    self.wait_for_email_and_click_link() # Extremely slow!
    # Actual test starts here...
```

## [DO] Abstract explicit waits into a decorator supporting variadic arguments
```python
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 5

def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn

@wait
def wait_for_row_in_list_table(self, row_text):
    rows = self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr")
    self.assertIn(row_text, [row.text for row in rows])

@wait
def wait_to_be_logged_in(self, email):
    self.browser.find_element(By.CSS_SELECTOR, "#id_logout")
    navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
    self.assertIn(email, navbar.text)
```

## [DON'T] Duplicate while/try/except boilerplate across multiple helper methods
```python
# ANTI-PATTERN: Repeating explicit wait boilerplate in every helper method
def wait_for_row_in_list_table(self, row_text):
    start_time = time.time()
    while True:
        try:
            rows = self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr")
            self.assertIn(row_text, [row.text for row in rows])
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)

def wait_to_be_logged_in(self, email):
    start_time = time.time()
    while True:
        try:
            self.browser.find_element(By.CSS_SELECTOR, "#id_logout")
            navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
            self.assertIn(email, navbar.text)
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)
```

## [DON'T] Use JSON Fixtures for test data setup
```python
# ANTI-PATTERN: Using dumpdata/loaddata JSON fixtures. 
# They are brittle, hard to update during schema changes, and obscure test dependencies.
class MyListsTest(FunctionalTest):
    fixtures = ['initial_data.json']
```