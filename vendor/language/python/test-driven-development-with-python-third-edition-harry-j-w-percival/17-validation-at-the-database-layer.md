@Domain
These rules MUST activate when the AI is tasked with adding data validation to Django applications, writing tests for expected exceptions, handling POST request errors in views, surfacing validation errors to the frontend, or refactoring Django URL resolutions (removing hardcoded URLs).

@Vocabulary
- **Model-Layer Validation**: The practice of pushing data integrity constraints down to the Django Model/Database layer rather than relying exclusively on client-side or form-level validation.
- **full_clean()**: A Django model method that explicitly runs all model-level validation (e.g., checking `blank=False`). Unlike forms, Django models do not run full validation automatically on `.save()`.
- **ValidationError**: The exception raised by Django when a validation-related constraint (like `blank=False`) is violated during `full_clean()`.
- **IntegrityError**: The exception raised directly by the database (e.g., SQLite, PostgreSQL) when a database-level constraint (like `NOT NULL` or `UNIQUE`) is violated.
- **self.assertRaises Context Manager**: A Python `unittest` construct used to elegantly assert that a specific block of code raises a specific exception.
- **Orphaned Parent Object**: A database record created in a view just before a related child object fails validation, requiring manual deletion in the `except` block to prevent database clutter.
- **Early Return (in FTs)**: A TDD methodology where a `return` statement is temporarily placed in a Functional Test (FT) right before the failing assertion, allowing the developer to achieve a "green" state to safely perform application-level refactoring.
- **get_absolute_url**: A Django model method used to define the canonical URL for a specific model instance, strictly utilized to adhere to the DRY (Don't Repeat Yourself) principle.

@Objectives
- Push validation constraints to the lowest possible level (Model/Database) to guarantee absolute data integrity.
- Use explicit context managers for testing exception handling.
- Ensure Django model validation is explicitly triggered in both tests and views.
- Prevent invalid database states and orphaned parent records when child object validation fails.
- Consolidate POST processing and GET rendering into single views to seamlessly pass validation errors back to templates.
- Eradicate hardcoded URLs from the entire codebase (views, templates, tests) using Django's reverse URL resolution mechanisms.

@Guidelines
- **Exception Testing Structure**: The AI MUST use the `with self.assertRaises(ExceptionType):` context manager when writing unit tests that expect an exception. The AI MUST NOT use a `try/except` block with a manual `self.fail()` call for this purpose.
- **Triggering Model Validation**: When testing model constraints (e.g., `blank=False`), the AI MUST call `model_instance.full_clean()` before calling `model_instance.save()`. The AI MUST recognize that Django's `save()` method does not trigger `ValidationError` on its own.
- **Handling View Validation**: When a view processes a POST request and manually creates model instances, the AI MUST wrap the `full_clean()` and `save()` calls in a `try/except ValidationError:` block.
- **Preventing Orphaned Data**: If a view creates a parent object (e.g., a List) prior to validating and saving a child object (e.g., an Item), the AI MUST explicitly delete the parent object within the `except ValidationError:` block to prevent saving blank/invalid states to the database.
- **Consolidated View Pattern**: The AI MUST process `POST` requests in the exact same view that renders the form. Upon catching a `ValidationError`, the AI MUST drop through to the `render()` function at the end of the view, passing the error message as context to the template.
- **HTML Escaping in Asserts**: When testing that a specific error message appears in a response using `assertContains`, and that message contains apostrophes or special characters (e.g., "You can't have an empty list item"), the AI MUST wrap the expected string in `django.utils.html.escape()`.
- **DRY URLs (Models)**: The AI MUST define a `get_absolute_url(self)` method on models using `django.urls.reverse` whenever the model has a canonical detail page.
- **DRY URLs (Views)**: The AI MUST pass model instances directly to the `redirect()` shortcut in views (e.g., `return redirect(model_instance)`), relying on the model's `get_absolute_url` under the hood. The AI MUST NOT hardcode URLs in `redirect()` calls.
- **DRY URLs (Templates)**: The AI MUST use the `{% url 'view_name' args %}` template tag instead of hardcoding `action="/path/"` or `href="/path/"` attributes.
- **Safe Refactoring**: If the AI determines a codebase refactor is necessary while a Functional Test is currently failing, the AI MUST insert an early `return` statement in the FT to bypass the failure, perform the refactor against a "green" state, and subsequently remove the early `return`.

@Workflow
1. **Model Validation Test Generation**: Write a unit test asserting that an invalid model instantiation raises a `ValidationError` when `full_clean()` is called. Use `with self.assertRaises(ValidationError):`.
2. **Model Constraint Implementation**: Add the required constraints to the Django model (e.g., `default=""`).
3. **View Validation Test Generation**: Write unit tests for the view handling the POST request. Include asserts that:
   - The database count remains 0 for both parent and child objects on invalid input.
   - The response status code is 200 (not a 302 redirect).
   - The correct template is used.
   - The expected error message is present in the response (using `html.escape` if needed).
4. **View Validation Implementation**: 
   - Instantiate the parent object.
   - Instantiate the child object with POST data.
   - Enter a `try:` block. Call `child.full_clean()` then `child.save()`.
   - Enter an `except ValidationError:` block. Call `parent.delete()` to clean up. Define the `error` message variable.
   - Drop out of the conditional logic and return a `render()` call passing the `error` variable to the template context.
5. **URL Refactoring**: 
   - Define `get_absolute_url` on the parent model.
   - Update the view's success path to use `return redirect(parent_instance)`.
   - Update all HTML templates to use the `{% url %}` tag for forms and links.

@Examples (Do's and Don'ts)

[DO] Use the context manager to assert exceptions in tests.
```python
def test_cannot_save_empty_list_items(self):
    mylist = List.objects.create()
    item = Item(list=mylist, text="")
    with self.assertRaises(ValidationError):
        item.full_clean()
        item.save()
```

[DON'T] Use try/except/fail for exception testing.
```python
def test_cannot_save_empty_list_items(self):
    mylist = List.objects.create()
    item = Item(list=mylist, text="")
    try:
        item.full_clean()
        item.save()
        self.fail("The save should have raised an exception")
    except ValidationError:
        pass
```

[DO] Clean up orphaned parent objects when child validation fails.
```python
def new_list(request):
    nulist = List.objects.create()
    item = Item(text=request.POST["item_text"], list=nulist)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        nulist.delete() # Cleans up the orphaned parent
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})
    return redirect(nulist)
```

[DON'T] Leave orphaned parent objects in the database.
```python
def new_list(request):
    nulist = List.objects.create()
    item = Item(text=request.POST["item_text"], list=nulist)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error}) # Bad: nulist remains in DB
    return redirect(f"/lists/{nulist.id}/")
```

[DO] Escape HTML characters in test assertions.
```python
from django.utils import html

def test_validation_errors_are_sent_back_to_template(self):
    response = self.client.post("/lists/new", data={"item_text": ""})
    expected_error = html.escape("You can't have an empty list item")
    self.assertContains(response, expected_error)
```

[DON'T] Hardcode URLs in redirects if a model has a canonical URL.
```python
# Bad
return redirect(f"/lists/{nulist.id}/")
```

[DO] Use `get_absolute_url` for redirects.
```python
# Good
class List(models.Model):
    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])

# In view:
return redirect(nulist)
```