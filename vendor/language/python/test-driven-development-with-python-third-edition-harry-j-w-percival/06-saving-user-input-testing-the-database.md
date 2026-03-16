# @Domain
These rules activate whenever the AI is tasked with implementing user input persistence, handling HTML forms, processing HTTP POST requests, creating or modifying Django models, writing database interactions (ORM), or writing unit and functional tests for any of these features in a Django application.

# @Vocabulary
- **FT (Functional Test)**: A high-level test driving a real web browser to test the application from the user's perspective.
- **Unit Test**: A low-level test checking the internal logic of functions or classes from the programmer's perspective.
- **Expected Failure**: A test failure that occurs exactly as predicted because the corresponding application code has not yet been written.
- **Unexpected Failure / Regression**: When a test fails in a way that was not anticipated, usually indicating a bug or that a recent change broke previously working functionality.
- **CSRF Token**: Cross-Site Request Forgery token. A security measure required by Django in all POST forms.
- **ORM (Object-Relational Mapper)**: Django's abstraction layer for querying and modifying the database using Python classes (Models).
- **QuerySet**: The list-like object returned by Django ORM queries (e.g., `Item.objects.all()`).
- **Migrations**: Django's version control system for the database schema, created via `makemigrations` and applied via `migrate`.
- **Triangulation**: A TDD technique where you write a specific test case to force the generalization of "cheating" or hardcoded implementation code.
- **Three Strikes and Refactor**: A rule of thumb for DRY (Don't Repeat Yourself). Copy and paste once (two instances) is acceptable, but upon the third instance of duplicated code, the AI MUST refactor it into a shared helper or common structure.
- **Arrange-Act-Assert (Given-When-Then)**: A testing structure convention where setup, execution, and verification are visually separated by whitespace.
- **Scratchpad To-Do List**: A temporary, written list of refactoring tasks, edge cases, or missing features that the AI discovers while coding, saved to be addressed later so as not to break the current red/green/refactor cycle.

# @Objectives
- Adopt an incremental, short-sighted, iterative TDD workflow (Working State to Working State). Do not jump ahead to the "perfect" design; only write code necessary to pass the current failing test.
- Ensure all HTML forms use POST requests securely and establish a clear testing contract between the frontend and backend.
- Strictly follow the "Always redirect after a POST" rule to prevent duplicate submissions.
- Map Python objects to database tables correctly using Django models and migrations.
- Maintain clean, highly readable tests by enforcing single-assertion tests, avoiding complex logic in assertions, and utilizing the Arrange-Act-Assert structure.

# @Guidelines

### 1. TDD and Incremental Iteration
- The AI MUST NOT implement complex logic, routing, or database models all at once.
- The AI MUST write the minimal code to get the current test past its current failure.
- If a glaring design flaw or missing feature is noticed (e.g., "we need support for multiple users" or "empty submissions are being saved"), the AI MUST add it to a "Scratchpad To-Do List" and finish the current test cycle before addressing it.

### 2. Frontend and Backend Contract Testing
- When testing forms, the AI MUST test the exact HTML attributes that matter for integration (e.g., `<form method="POST">` and `<input name="item_text">`) rather than checking cosmetic constants.
- The AI MUST ALWAYS include `{% csrf_token %}` inside any Django `<form method="POST">` template block.

### 3. Handling POST Requests
- View functions MUST separate GET and POST logic (e.g., `if request.method == "POST":`).
- The AI MUST ALWAYS return an HTTP 302 Redirect (`redirect()`) after processing a valid POST request. Never render a template directly as a success response to a POST request.

### 4. Database Models and ORM
- Database models MUST inherit from `models.Model`.
- When adding fields to models, the AI MUST provide defaults (e.g., `default=""`) to avoid migration prompts requesting one-off default values.
- The AI MUST use Django's ORM shortcuts like `Model.objects.create()` instead of manual instantiation and `.save()` when applicable for brevity.
- The AI MUST remember that Django unit tests use a blank, in-memory test database, while the dev server (`runserver`) uses the local `db.sqlite3`.

### 5. Debugging Functional Tests
- If an FT fails unexpectedly, the AI MUST employ debugging techniques:
  - Add explicit waits or `time.sleep()` to inspect the browser state.
  - Simplify assertion logic to get clearer error messages.
  - Provide a custom error message to `self.assertTrue()` or swap to `self.assertIn()` to auto-generate better failure outputs.

### 6. Test Structure and Cleanliness
- **One thing per test**: The AI MUST split long tests with multiple assertions (e.g., testing database saving AND testing HTTP redirects) into separate, single-purpose test methods.
- **Arrange-Act-Assert**: The AI MUST format unit tests using vertical whitespace (blank lines) to separate the setup of data, the calling of the code under test, and the assertions.
- **No clever logic in tests**: The AI MUST NOT use complex Python built-ins like list comprehensions inside `any()` for assertions. Prefer simple, readable assertions like `self.assertIn()`.
- **Three Strikes and Refactor**: The AI MUST refactor duplicated test logic (e.g., checking for rows in a table) into helper methods (e.g., `check_for_row_in_list_table(self, row_text)`) once it appears three times.

# @Workflow
1. **Functional Test Update**: Write or update the FT to submit user input (e.g., `inputbox.send_keys(Keys.ENTER)`). Run the FT to see it fail.
2. **Frontend Contract**: Write a unit test asserting the presence of `method="POST"` and the specific `name="..."` attribute on the input. Implement in the template. Include `{% csrf_token %}`.
3. **Handle POST in View**: Write a unit test for the POST request (using `self.client.post`). Implement a minimal POST check in the view (`if request.method == "POST"`).
4. **Model Creation**: Write a unit test checking that object count increases on POST. Create the Model class in `models.py`.
5. **Migrations**: Run `makemigrations` and `migrate` to update the database schema.
6. **Save and Redirect**: Update the view to save the POST data to the database using the ORM. Immediately return a `redirect()`.
7. **Template Rendering**: Write a unit test to ensure saved database items are passed to the template. Update the template with a `{% for item in items %}` loop to render them.
8. **Refactor**: Review tests for the "One thing per test" rule. Split tests if necessary. Format with Arrange-Act-Assert whitespace. Refactor duplicates using "Three strikes and refactor".

# @Examples (Do's and Don'ts)

### Testing the HTML Contract
**[DO]** Test specific attributes that drive behavior:
```python
def test_renders_input_form(self):
    response = self.client.get("/")
    self.assertContains(response, '<form method="POST">')
    self.assertContains(response, '<input name="item_text"')
```
**[DON'T]** Test cosmetic constants:
```python
def test_renders_input_form(self):
    response = self.client.get("/")
    # DON'T do this: it breaks if the placeholder text changes slightly
    self.assertContains(response, '<input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />')
```

### Writing Assertions
**[DO]** Use simple assertions that generate readable error messages automatically:
```python
self.assertIn("1: Buy peacock feathers", [row.text for row in rows])
```
**[DON'T]** Use clever/complex logic that obfuscates the failure:
```python
self.assertTrue(any(row.text == "1: Buy peacock feathers" for row in rows))
```

### Structuring Tests (Arrange-Act-Assert)
**[DO]** Separate test phases with whitespace:
```python
def test_displays_all_list_items(self):
    Item.objects.create(text="itemey 1")
    Item.objects.create(text="itemey 2")

    response = self.client.get("/")

    self.assertContains(response, "itemey 1")
    self.assertContains(response, "itemey 2")
```
**[DON'T]** Mash all phases together into an unreadable block:
```python
def test_displays_all_list_items(self):
    Item.objects.create(text="itemey 1")
    Item.objects.create(text="itemey 2")
    response = self.client.get("/")
    self.assertContains(response, "itemey 1")
    self.assertContains(response, "itemey 2")
```

### Unit Test Granularity
**[DO]** Split distinct behaviors into separate tests:
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
**[DON'T]** Cram multiple behavioral assertions into one test:
```python
def test_can_save_a_POST_request(self): # DON'T DO THIS
    response = self.client.post("/", data={"item_text": "A new list item"})
    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, "A new list item")
    self.assertRedirects(response, "/") # Obscured if the DB assert fails
```

### View POST Handling
**[DO]** Always redirect after a successful POST:
```python
def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/")
        
    items = Item.objects.all()
    return render(request, "home.html", {"items": items})
```
**[DON'T]** Render a template directly after a POST:
```python
def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        # DON'T DO THIS: A page refresh will cause duplicate submission
        return render(request, "home.html", {"new_item_text": request.POST["item_text"]})
```