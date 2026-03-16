@Domain
The AI MUST activate these rules when engaged in Test-Driven Development (TDD), Python web development, Django framework configurations, Selenium functional testing, test refactoring, and general unit/integration testing tasks.

@Vocabulary
- **Testing Goat**: The absolute authority and mental model of TDD discipline. It demands that NO production code is written without a failing test.
- **TDD (Test-Driven Development)**: A strict discipline consisting of writing a test, seeing it fail, writing the minimal code to pass, and then refactoring.
- **Double-Loop TDD**: The workflow consisting of an outer loop of Functional Tests (FTs) driving high-level user stories, and an inner loop of Unit Tests (UTs) driving granular implementation details.
- **FT (Functional Test) / End-to-End Test / Acceptance Test**: A test written from the user's perspective, running against a real or headless browser (e.g., Selenium) to test the fully integrated application.
- **Unit Test**: A fast, isolated test written from the programmer's perspective, targeting a specific function, view, or model.
- **Expected Failure**: A test failure that occurs exactly as predicted. This validates that the test is properly wired and testing the correct behavior.
- **Regression**: When a code change unexpectedly breaks previously working application behavior.
- **Red/Green/Refactor**: The atomic cycle of TDD. (Red = failing test, Green = passing test, Refactor = improving code without changing behavior).
- **Minimum Viable App**: The simplest possible implementation of a feature that delivers value and allows testing of the core functionality.
- **Triangulation**: Writing a specific test case that forces the developer to abstract a hardcoded "cheat" into general, proper logic.
- **Three Strikes and Refactor**: A rule of thumb dictating that duplication is tolerated twice, but upon the third occurrence, the code MUST be refactored to eliminate the duplication.
- **YAGNI (You Ain't Gonna Need It)**: The principle of resisting the urge to build anticipated features; write ONLY the code strictly required to pass the current test.
- **Explicit Wait**: A testing pattern utilizing a polling/retry loop with a timeout to wait for asynchronous UI updates, explicitly avoiding brittle, hardcoded `time.sleep()` calls.
- **Smoke Test**: A minimal, fast test to check if a fundamental component (e.g., routing, static file loading) is completely broken.

@Objectives
- The AI MUST strictly obey the "Testing Goat" discipline: Do absolutely nothing until there is a failing test.
- The AI MUST utilize Double-Loop TDD: Use FTs to define the user story and UI integration, and UTs to drive the specific Django models, views, and forms.
- The AI MUST ensure the application moves from working state to working state using minimal, atomic code changes.
- The AI MUST enforce separation of concerns between testing behavior (what the code does) and testing implementation (how the code does it).
- The AI MUST prioritize clean code and test isolation, ensuring that different test runs do not interfere with one another's database or browser states.

@Guidelines

# TDD Constraints and Discipline
- When asked to implement a feature, the AI MUST FIRST write a Functional Test describing the user story.
- When a Functional Test fails, the AI MUST write a Unit Test to define the programmer-level behavior before writing application code.
- When writing application code, the AI MUST write the absolute minimum amount of code required to change the test output or pass the test.
- When a test passes (Green), the AI MUST evaluate if the code requires refactoring. Refactoring MUST ONLY occur when tests are Green.
- When refactoring, the AI MUST work on either the application code OR the test code, but NEVER both simultaneously.
- When writing tests, the AI MUST structure them using the Arrange-Act-Assert (or Given-When-Then) pattern, separating setup, execution, and verification with whitespace.

# Functional Testing (Selenium) Rules
- When writing FTs, the AI MUST include human-readable comments detailing the user story step-by-step.
- When interacting with elements that cause a page load or asynchronous update (e.g., hitting ENTER, clicking submit), the AI MUST use an Explicit Wait.
- When implementing waits, the AI MUST NOT use `time.sleep()`. Instead, the AI MUST create a polling loop (e.g., `wait_for` or `wait_for_row_in_list_table`) that catches `AssertionError` and `WebDriverException` up to a `MAX_WAIT` timeout limit.
- When isolating FTs, the AI MUST use Django's `StaticLiveServerTestCase` to spin up isolated test databases and serve static files automatically.
- When querying elements, the AI MUST be aware of the difference between `find_element` (returns an element or raises an exception) and `find_elements` (returns a list, which may be empty).

# Unit Testing Rules
- When testing a Django view, the AI MUST ensure that each test tests ONE specific thing (e.g., one test for template used, one test for database side-effects).
- When asserting HTML content, the AI MUST NOT test exact constants or raw HTML strings (e.g., `assertContains(response, "<html>...</html>")`).
- When asserting templates, the AI MUST use `self.assertTemplateUsed(response, "template_name.html")`.
- When complex DOM assertions are needed in unit tests, the AI MUST use `lxml.html` to parse the response and query via CSS selectors rather than using brittle string matching.
- When testing that an exception should be raised, the AI MUST use the `with self.assertRaises(ExceptionType):` context manager.

# Django Architecture and Implementation Rules
- When processing user input, the AI MUST enforce the rule: Always Redirect After a POST. A successful POST request MUST return a 302 redirect (`redirect()`), NEVER a 200 rendered template.
- When mapping URLs, the AI MUST strictly handle trailing slashes: action URLs that modify state generally do not use trailing slashes (e.g., `/lists/new`), while viewing URLs do (e.g., `/lists/1/`).
- When defining URL routes, the AI MUST NOT hardcode URLs in views or templates. The AI MUST use Django's URL naming (`name="home"`) and reverse resolution (`{% url 'name' %}` or `redirect()`).
- When building HTML layouts, the AI MUST utilize Django Template Inheritance (`{% extends 'base.html' %}` and `{% block content %}`) to eliminate boilerplate HTML.
- When dealing with static files, the AI MUST properly configure `STATIC_URL` and use `StaticLiveServerTestCase` so FTs can validate CSS (e.g., Bootstrap integration) and JavaScript.

# Django Models and Database Rules
- When testing Model validations, the AI MUST explicitly call `.full_clean()` on the model instance in the test, because Django models do not run full validation natively on `.save()`.
- When modifying models, the AI MUST immediately generate the corresponding database migrations (`makemigrations`).
- When defining Model constraints, the AI MUST differentiate between database-level constraints (e.g., `default=""`) and validation-level constraints (e.g., catching `ValidationError`).

# Git and Version Control Rules
- When creating a project, the AI MUST populate `.gitignore` with `db.sqlite3`, `.venv`, `__pycache__`, and `*.pyc`.
- When tests are Green and a logical step is complete, the AI MUST perform an atomic Git commit with a descriptive message before moving to the next feature or refactoring.

@Workflow
1. **Define User Story**: Write a Functional Test using Selenium to simulate the user journey.
2. **Execute FT (Red)**: Run the FT to confirm it fails for the exact expected reason (Expected Failure).
3. **Drop to Unit Test**: Write a Unit Test for the specific view, template, or model required to advance the FT.
4. **Execute UT (Red)**: Run the Unit Test to confirm it fails expectedly.
5. **Implement Minimal Code**: Write the bare minimum Django code (e.g., adding a view, mapping a URL, or returning an `HttpResponse`) to pass the Unit Test.
6. **Execute UT (Green)**: Run the Unit test to confirm it passes.
7. **Refactor**: Review the code. If duplication exists (Rule of Three), extract templates, use `lxml` for DOM tests, or DRY up views. Ensure tests remain Green.
8. **Re-evaluate FT**: Run the FT. If it passes, the feature is complete. If it fails on the next step, repeat from Step 3.

@Examples (Do's and Don'ts)

# Explicit Waits vs Implicit Sleeps
[DO]
```python
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
```
[DON'T]
```python
def test_can_start_a_list(self):
    self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
    time.sleep(2) # Anti-pattern: Magic sleep, brittle and slows down test suites
    self.assertIn("Buy milk", self.browser.page_source)
```

# Redirecting after POST
[DO]
```python
def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/")
    return render(request, "home.html")
```
[DON'T]
```python
def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        # Anti-pattern: Rendering a template directly on a POST request
        return render(request, "home.html", {"new_item_text": request.POST["item_text"]})
    return render(request, "home.html")
```

# Testing HTML Structure (Avoid Testing Constants)
[DO]
```python
import lxml.html

def test_renders_input_form(self):
    response = self.client.get("/")
    parsed = lxml.html.fromstring(response.content)
    [form] = parsed.cssselect("form[method=POST]")
    self.assertEqual(form.get("action"), "/lists/new")
    
    inputs = form.cssselect("input")
    self.assertIn("item_text", [input.get("name") for input in inputs])
```
[DON'T]
```python
def test_renders_input_form(self):
    response = self.client.get("/")
    # Anti-pattern: Brittle string matching that breaks with minor whitespace or CSS class additions
    self.assertContains(
        response, 
        '<input class="form-control" name="item_text" id="id_new_item" placeholder="Enter a to-do item" />',
        html=True
    )
```

# Testing Model Validations
[DO]
```python
def test_cannot_save_empty_list_items(self):
    mylist = List.objects.create()
    item = Item(list=mylist, text="")
    with self.assertRaises(ValidationError):
        item.full_clean()
```
[DON'T]
```python
def test_cannot_save_empty_list_items(self):
    mylist = List.objects.create()
    item = Item(list=mylist, text="")
    with self.assertRaises(ValidationError):
        item.save() # Anti-pattern: Django models do not run full validation on save()
```