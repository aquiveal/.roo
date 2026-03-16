# @Domain
These rules activate when implementing user input features, handling HTTP POST requests, creating or modifying Django models, writing database migrations, or constructing unit and functional tests related to database persistence and form submissions in Python/Django applications.

# @Vocabulary
- **Triangulation:** A testing technique where you write an additional test case with a new specific example to force yourself to write generic, generalized code rather than "cheating" by returning hardcoded constants.
- **Three Strikes and Refactor:** A rule of thumb for DRY (Don't Repeat Yourself). Copy and paste code once, but when you find yourself writing the exact same code for a third time, you MUST refactor it into a reusable helper method or abstraction.
- **Scratchpad To-Do List:** A method of writing down non-critical bugs, edge cases, or future refactoring ideas that occur to you while coding, allowing you to stay focused on the current test failure without forgetting the tasks.
- **Regression:** When a new code change unexpectedly breaks some aspect of the application that previously worked.
- **Expected Failure:** When a test fails exactly for the reason you predicted, validating that the test is written correctly.
- **Unexpected Failure:** When a test fails in an unpredicted way, indicating either a flawed test, an unhandled edge case, or a regression.
- **Arrange-Act-Assert (Given-When-Then):** A structural convention for unit tests where the setup of data, the execution of the code under test, and the verification of the results are visually separated by whitespace.
- **Contract Testing (Frontend/Backend):** Testing the specific HTML attributes (`method="POST"`, `name="..."`) that dictate how the frontend sends data to the backend, rather than testing cosmetic HTML text.

# @Objectives
- Drive development in tiny, incremental steps based STRICTLY on current test failures, actively resisting the urge to implement "correct" but complex designs (e.g., multiple database tables) before the tests demand them.
- Safely process user input via HTTP POST requests, adhering strictly to web security and architectural best practices (CSRF tokens, Redirect-After-POST).
- Ensure unit tests remain highly focused, testing exactly one behavior per test.
- Integrate the database using Django's ORM and migrations while preventing invalid data (like empty strings) from persisting.

# @Guidelines

## Development Methodology & TDD Enforcement
- **Work Incrementally:** You MUST code "short-sightedly". Do only what is required to move the current failing test one step forward. Do not implement complex architectures until a test specifically forces you to.
- **Triangulate:** If a test allows you to write "cheating" code (e.g., returning a hardcoded magic constant), you MUST write a second test that forces the application to implement the actual generic logic.
- **Use the Scratchpad:** When you spot glaring issues (e.g., saving blank items, missing multi-user support) while fixing a specific test, DO NOT fix them immediately. Add them to a conceptual "scratchpad" and return to them in a separate test-code cycle.
- **Three Strikes Rule:** Do not refactor duplication on the second occurrence. Wait for the third occurrence ("third strike") to refactor into helper methods. 

## Testing Standards
- **Test the Contract, Not Constants:** When testing HTML forms, you MUST assert the presence of critical routing and processing attributes (e.g., `<form method="POST">`, `<input name="item_text">`) rather than cosmetic text or layout tags.
- **One Concept Per Test:** Unit tests MUST test only one thing. If a test asserts database persistence, HTTP response codes, and HTML content simultaneously, you MUST split it into multiple, smaller tests (e.g., `test_can_save_a_POST_request` and `test_redirects_after_POST`).
- **Arrange-Act-Assert:** You MUST visually separate the setup, invocation, and assertion phases of your unit tests using blank lines.
- **Improve Error Messages:** You MUST provide custom, descriptive error messages in assertions (or refactor complex logic like `any()` into `assertIn()`) so that test output clearly explains what failed without requiring manual inspection.

## Web Development & Django Patterns
- **CSRF Protection:** Every HTML form using POST MUST include the `{% csrf_token %}` template tag.
- **Redirect After POST:** A view handling a POST request MUST NEVER return a standard HTML render response. It MUST ALWAYS return an HTTP 302 redirect (`return redirect(...)`).
- **ORM Shorthands:** Utilize Django ORM shorthands like `Model.objects.count()`, `Model.objects.first()`, and `Model.objects.create(field=value)` for concise test and view logic.
- **Migrations:** When adding new non-nullable fields to a model, you MUST provide a `default=""` (or appropriate default value) so the database can populate existing rows during the migration process.
- **Template Variable Rendering:** Use Django template syntax `{{ variable_name }}` to inject Python variables from the view context into the HTML. Avoid hardcoding outputs that should be dynamic.

## Functional Test Debugging
- **Manual Pauses:** If an FT fails unpredictably or you need to inspect browser state, inject `time.sleep(10)` right before the failure point to visually debug the browser.
- **Check State Leaks:** If FTs fail because of lingering data from previous runs, ensure the test environment resets the database, or manually clear it if running against a local live database during development.

# @Workflow
1. **Define the User Story:** Write an FT describing the expected user interaction (e.g., submitting a form).
2. **Identify the Frontend/Backend Contract:** Write unit tests checking that the form renders with `method="POST"` and specific `name` attributes on inputs.
3. **Add CSRF and Template Tags:** Implement the HTML form, ensuring `{% csrf_token %}` is present to avoid 403 Forbidden errors.
4. **Handle POST in View:** Write a unit test for the POST request. In the view, extract `request.POST["field_name"]`.
5. **Enforce Redirect:** Write a separate unit test verifying the view returns a 302 redirect after a POST. Implement `redirect("/")` in the view.
6. **Define the Model:** Write a unit test for database saving/retrieving. Create the Django model subclassing `models.Model`.
7. **Migrate:** Run `makemigrations` and `migrate`. Ensure defaults are provided for new fields.
8. **Wire View to Model:** Update the view to save the POSTed data to the model using `.objects.create()`.
9. **Refactor and Review:** Check tests for the "Three Strikes" rule. Extract duplicated assertions into helper methods. Ensure tests follow Arrange-Act-Assert spacing.

# @Examples (Do's and Don'ts)

## Test Formatting (Arrange-Act-Assert)
[DO]
```python
def test_displays_all_list_items(self):
    Item.objects.create(text="itemey 1")
    Item.objects.create(text="itemey 2")

    response = self.client.get("/")

    self.assertContains(response, "itemey 1")
    self.assertContains(response, "itemey 2")
```
[DON'T]
```python
def test_displays_all_list_items(self):
    Item.objects.create(text="itemey 1")
    Item.objects.create(text="itemey 2")
    response = self.client.get("/")
    self.assertContains(response, "itemey 1")
    self.assertContains(response, "itemey 2")
```

## POST Request Handling
[DO]
```python
def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/")
    
    items = Item.objects.all()
    return render(request, "home.html", {"items": items})
```
[DON'T]
```python
def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        # Anti-pattern: Rendering a template directly in response to a POST
        return render(request, "home.html", {"new_item_text": request.POST["item_text"]})
    return render(request, "home.html")
```

## Testing Form Contracts
[DO]
```python
def test_renders_input_form(self):
    response = self.client.get("/")
    self.assertContains(response, '<form method="POST">')
    self.assertContains(response, '<input name="item_text"')
```
[DON'T]
```python
def test_renders_input_form(self):
    response = self.client.get("/")
    # Anti-pattern: Testing cosmetic constants instead of behavioral contracts
    self.assertContains(response, 'To-Do')
    self.assertContains(response, 'Enter a to-do item')
```

## Test Scope
[DO]
```python
def test_can_save_a_POST_request(self):
    self.client.post("/", data={"item_text": "A new list item"})
    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, "A new list item")

def test_redirects_after_POST(self):
    response = self.client.post("/", data={"item_text": "A new list item"})
    self.assertRedirects(response, "/")
```
[DON'T]
```python
def test_can_save_and_redirects_after_post(self):
    # Anti-pattern: Testing too many concepts in a single test
    response = self.client.post("/", data={"item_text": "A new list item"})
    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, "A new list item")
    self.assertRedirects(response, "/")
```