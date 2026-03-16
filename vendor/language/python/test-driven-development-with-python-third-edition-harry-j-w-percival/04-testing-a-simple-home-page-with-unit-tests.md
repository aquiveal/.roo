@Domain
These rules MUST trigger when the AI is tasked with creating a new Django app, writing unit tests for Django views, configuring URL routing (`urls.py`), handling HTTP requests and responses, decoding HTML responses in tests, or engaging in the Python/Django Test-Driven Development (TDD) red/green/refactor cycle.

@Vocabulary
- **Functional Test (FT) / Acceptance Test / End-to-End Test**: A test that drives a real web browser (e.g., using Selenium) to test the application from the outside, from the user's point of view. It provides confidence that everything is wired together correctly.
- **Unit Test**: A test that tests the application from the inside, from the programmer's point of view. It exhaustively checks lower-level details, permutations, individual functions, and edge cases.
- **Expected Failure**: A test failure that occurs precisely for the reason predicted by the developer. It is a necessary milestone in the TDD cycle.
- **MVC (Model-View-Controller)**: The architectural pattern Django broadly follows. In Django, Views act as controllers, and Templates act as the view.
- **URL Resolution**: The process Django uses to decide which view function should deal with an incoming HTTP request, based on rules defined in `urls.py`.
- **HttpRequest**: The input object created by Django when a user's browser asks for a page.
- **HttpResponse**: The object output by a Django view function, containing the raw bytes (`.content`) sent down the wire to the browser.
- **Django Test Client**: A testing tool provided by Django (`self.client`) that simulates a browser making HTTP requests to test URL resolution and view rendering simultaneously.
- **Unit-Test/Code Cycle**: The iterative process of running unit tests to see how they fail, making a minimal code change, and repeating until tests pass.

@Objectives
- Execute a strict, microscopic Test-Driven Development (TDD) workflow where NO application code is written without a corresponding failing unit test.
- Use Unit Tests to drive the low-level design of Django view functions and HTTP response generation.
- Use Functional Tests to drive the high-level application specification and guarantee end-to-end wiring.
- Strictly adhere to making the smallest, most minimal code changes possible to change the test's failure message or pass the test.
- Master traceback analysis to accurately diagnose and resolve test failures one step at a time.
- Correctly map URL routing in Django to ensure view functions are accessible to the test client and the user.

@Guidelines

### TDD Constraints and Minimal Changes
- The AI MUST NEVER write application code before writing a unit test that fails.
- When a unit test fails, the AI MUST make the smallest, most minimal code change required to address precisely the current test failure. Do NOT skip ahead or write the "final" solution immediately.
- If a test fails due to an `ImportError`, the AI MUST only create the file or function/variable placeholder to fix the import, returning `None` or using `pass` if necessary.
- If a test fails due to a `TypeError` (e.g., takes 0 positional arguments but 1 was given), the AI MUST only add the required argument signature to the function.

### Unit Testing Django Views (Manual Method)
- When initially testing a view function directly (without the test client), the AI MUST import and instantiate `HttpRequest`.
- The AI MUST pass the request object to the view function and capture the returned `HttpResponse`.
- The AI MUST decode the response content using `.content.decode("utf8")` to examine the raw HTML string.
- The AI MUST use `self.assertIn()`, `self.assertTrue(html.startswith(...))`, and `self.assertTrue(html.endswith(...))` to verify HTML structure and content.

### Unit Testing with the Django Test Client
- When testing URL resolution and view integration, the AI MUST use `self.client.get("url_path")`.
- The AI MUST use the `self.assertContains(response, "expected_content")` helper method, which automatically handles decoding and assertion.
- Once the Django Test Client is implemented, the AI MUST refactor and consolidate lower-level manual `HttpRequest` tests into the test client test to reduce duplication.

### Traceback Analysis Rules
When encountering a test failure or exception, the AI MUST systematically analyze the traceback using the following exact steps:
1. Examine the actual error/exception message at the very bottom.
2. Double-check the test name to ensure the failure is occurring in the expected test.
3. Trace the stack upwards to find the specific line of test code that kicked off the failure.
4. Utilize Python 3 caret markers (`^^^^`) if present to identify the exact expression causing the error.
5. Look further down the traceback (if applicable) for the specific line of application code involved in the failure.

### URL Routing (`urls.py`)
- The AI MUST remember that Django strips the leading slash from URLs. The base/root URL MUST be represented as the empty string `""` in `path()`.
- The AI MUST configure URL paths in the `urlpatterns` list using `path("url_pattern", views.view_function, name="view_name")`.

### Version Control (Git) Hygiene
- The AI MUST review staged changes (e.g., using `git diff --staged` or `git diff`) before executing a commit.
- The AI MUST make frequent, atomic commits after every successful Green test or major refactor using `git commit -am "Descriptive message"`.

@Workflow
1. **Initialize App**: Run `python manage.py startapp <app_name>`.
2. **Verify Test Runner**: Write a deliberately silly failing test (e.g., `self.assertEqual(1 + 1, 3)`) in `tests.py` and run `python manage.py test` to ensure the Django test machinery is working.
3. **Write Unit Test**: Write a unit test invoking the view manually with an `HttpRequest`.
4. **Run Tests**: Execute `python manage.py test` and perform a strict 5-step traceback analysis on the failure.
5. **Minimal Code Change**: Write exactly one line or the smallest logical block of code required to advance the error message.
6. **Iterate**: Repeat steps 4 and 5 until the view returns the correct HTML content.
7. **Write Test Client Unit Test**: Add a test using `self.client.get()` to test URL routing.
8. **Configure URL**: Map the URL in `urls.py` to fix the 404 error thrown by the test client.
9. **Refactor**: Remove the manual `HttpRequest` test and rely entirely on the `self.client.get()` and `assertContains` test.
10. **Run FTs**: Run `python functional_tests.py` to verify the outer loop user story now passes.
11. **Commit**: Review diffs and commit changes to version control.

@Examples (Do's and Don'ts)

### Defining View Functions Incrementally
- **[DO]**: Make the minimal change to satisfy an `ImportError` or `Callable` error.
```python
# When test says: ImportError: cannot import name 'home_page'
home_page = None

# When test says: TypeError: 'NoneType' object is not callable
def home_page():
    pass

# When test says: TypeError: home_page() takes 0 positional arguments but 1 was given
def home_page(request):
    pass
```
- **[DON'T]**: Write the entire view function preemptively before the test demands it.
```python
# Anti-pattern: writing the final code immediately
def home_page(request):
    return HttpResponse("<html><title>To-Do lists</title></html>")
```

### Manual View Unit Testing
- **[DO]**: Test the raw view function by constructing an HttpRequest.
```python
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.startswith("<html>"))
        self.assertTrue(html.endswith("</html>"))
```
- **[DON'T]**: Forget to decode the `.content` byte string before running string assertions.

### Refactored Django Test Client Testing
- **[DO]**: Consolidate manual request tests into a clean Test Client implementation.
```python
from django.test import TestCase

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertContains(response, "<title>To-Do lists</title>")
        self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")
```
- **[DON'T]**: Keep redundant manual `HttpRequest` tests once the `self.client` tests are verifying the exact same rendering behavior.

### URL Configuration
- **[DO]**: Omit the leading slash in `path()`.
```python
from django.urls import path
from lists.views import home_page

urlpatterns = [
    path("", home_page, name="home"),
]
```
- **[DON'T]**: Include a leading slash in the route definition.
```python
# Anti-pattern
urlpatterns = [
    path("/", home_page, name="home"),
]
```