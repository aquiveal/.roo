# @Domain
These rules MUST be activated when the AI is tasked with implementing data validation in a Django application, specifically working with Django models, views handling POST requests, form rendering in templates, URL routing refactoring, and writing unit or functional tests for these components.

# @Vocabulary
- **Database-related constraints**: Constraints enforced directly by the database engine (e.g., `null=False` mapping to `NOT NULL`). Violations raise an `IntegrityError`.
- **Validation-related constraints**: Constraints enforced at the application/Django layer (e.g., `blank=False` preventing empty strings). SQLite does not enforce empty string constraints at the DB level. Violations raise a `ValidationError`.
- **full_clean()**: A Django model method that manually triggers model-level validation.
- **self.assertRaises**: A Python `unittest` context manager used to assert that a specific block of code raises a specific exception.
- **Early Return**: The practice of temporarily placing a `return` statement in a Functional Test (FT) to pause feature development, allowing the developer to refactor application code against a passing (green) test state.
- **get_absolute_url**: A special Django model method that defines the canonical URL for an object, allowing instances to be passed directly to `redirect()`.
- **html.escape()**: A Django utility function (`django.utils.html.escape`) used to escape HTML characters in strings (e.g., apostrophes) when asserting against rendered template content.

# @Objectives
- Push validation logic as low down the stack as possible (to the database/model layer) to provide the ultimate guarantee of data integrity.
- Prevent invalid data from ever being saved to the database.
- Gracefully surface model validation errors in the user interface.
- Consolidate view logic by processing POST requests in the same view that renders the associated form.
- Eliminate hardcoded URLs across the codebase (in views, templates, and tests) to adhere to the DRY (Don't Repeat Yourself) principle.
- Maintain highly specific, focused unit tests by extracting repeated setup logic into helper methods.

# @Guidelines

### Model and Database Validation
- The AI MUST distinguish between database-level constraints (`IntegrityError`) and model-level constraints (`ValidationError`).
- The AI MUST NOT rely on Django's `.save()` method to run model-level validation (like `blank=False`). Due to a Django quirk, `.save()` does not run full validation.
- To enforce model-level validation, the AI MUST explicitly call `.full_clean()` on the model instance before calling `.save()`.

### Testing Exceptions
- When testing that an exception is raised, the AI MUST use the `with self.assertRaises(ExceptionType):` context manager rather than `try/except` blocks with `self.fail()`.

### View Architecture for Forms
- The AI MUST use a unified view pattern for forms: process POST requests in the very same view that renders the form.
- If validation fails (catches a `ValidationError`), the view MUST NOT save the object. It MUST re-render the template, passing the error message in the context.
- If validation succeeds, the view MUST save the object and return an HTTP 302 redirect.

### Unit Testing Views
- The AI MUST NOT write monolithic test blocks with multiple, unrelated assertions.
- The AI MUST separate view testing concerns into distinct tests (e.g., one test to ensure invalid input isn't saved, one for the response status/template, one for the error message rendering).
- The AI MUST extract repeated request logic (like dispatching an invalid POST request) into a helper method on the test class (e.g., `def post_invalid_input(self):`).
- When asserting the presence of error messages in responses, the AI MUST wrap the expected string in `html.escape()` to account for Django's automatic template escaping (e.g., escaping apostrophes).

### Template Validation Rendering
- The AI MUST use Bootstrap validation classes to surface errors in templates.
- Add the `.is-invalid` class conditionally to the `<input>` element if an error exists.
- Display the actual error text inside a `<div class="invalid-feedback">` element.

### URL Refactoring (DRY)
- The AI MUST NOT use hardcoded URL strings in templates. It MUST use the `{% url 'view_name' args %}` template tag.
- The AI MUST define a `get_absolute_url(self)` method using Django's `reverse()` on models that have a canonical view.
- In views, the AI MUST pass the model instance directly to `redirect(model_instance)` instead of hardcoding or concatenating URL strings.

### Refactoring Workflow
- When a required refactor is discovered halfway through writing a new feature's Functional Test, the AI MUST insert an early `return` in the FT. This ensures the refactor occurs against a "green" (passing) test state before resuming feature development.

# @Workflow
1. **Model Test**: Write a unit test for the model verifying that invalid input raises a `ValidationError` when `.full_clean()` is called. Use `self.assertRaises`.
2. **Model Implementation**: Ensure the model fields have the correct constraints (e.g., `default=""`).
3. **View Tests (Invalid Path)**: Write unit tests for the view handling a POST request with invalid data. Create a helper method for the POST request. Write three distinct tests:
   - Check that the database count does not increase.
   - Check that the response status is 200 and the correct template is used.
   - Check that the response contains the escaped error message.
4. **View Implementation**: Update the view to instantiate the model, call `.full_clean()`, and call `.save()`. Wrap this in a `try...except ValidationError:` block. On exception, render the template with the error message.
5. **Template Implementation**: Update the template to conditionally render the `.is-invalid` CSS class on the input and display the error message inside an `.invalid-feedback` div.
6. **Refactoring URLs**:
   - Write a model test asserting that `get_absolute_url` returns the correct path.
   - Implement `get_absolute_url` on the model using `reverse()`.
   - Update the view's successful POST path to `return redirect(model_instance)`.
   - Update templates to replace hardcoded `action="/path/"` strings with `action="{% url 'view_name' %}"`.

# @Examples (Do's and Don'ts)

### Exception Testing
**[DO]** Use the context manager for testing exceptions.
```python
def test_cannot_save_empty_list_items(self):
    mylist = List.objects.create()
    item = Item(list=mylist, text="")
    with self.assertRaises(ValidationError):
        item.full_clean()
```
**[DON'T]** Use try/except with manual failure.
```python
def test_cannot_save_empty_list_items(self):
    mylist = List.objects.create()
    item = Item(list=mylist, text="")
    try:
        item.full_clean()
        self.fail("Should have raised ValidationError")
    except ValidationError:
        pass
```

### Model Validation in Views
**[DO]** Explicitly call `full_clean()` and catch the exception to prevent saving invalid data.
```python
def new_list(request):
    nulist = List.objects.create()
    item = Item(text=request.POST["item_text"], list=nulist)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        nulist.delete()
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})
    return redirect(nulist)
```
**[DON'T]** Assume `.save()` will catch model-level validation errors like `blank=False`.
```python
def new_list(request):
    nulist = List.objects.create()
    try:
        # This will save an empty string because SQLite doesn't enforce it!
        Item.objects.create(text=request.POST["item_text"], list=nulist)
    except ValidationError:
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})
    return redirect(f"/lists/{nulist.id}/")
```

### Splitting View Tests and Using HTML Escape
**[DO]** Split assertions, use a helper method, and escape HTML.
```python
def post_invalid_input(self):
    return self.client.post("/lists/new", data={"item_text": ""})

def test_for_invalid_input_nothing_saved_to_db(self):
    self.post_invalid_input()
    self.assertEqual(Item.objects.count(), 0)

def test_for_invalid_input_renders_list_template(self):
    response = self.post_invalid_input()
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "home.html")

def test_for_invalid_input_shows_error_on_page(self):
    response = self.post_invalid_input()
    expected_error = html.escape("You can't have an empty list item")
    self.assertContains(response, expected_error)
```
**[DON'T]** Write monolithic tests with unescaped strings.
```python
def test_validation_errors(self):
    response = self.client.post("/lists/new", data={"item_text": ""})
    self.assertEqual(Item.objects.count(), 0)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "home.html")
    # Will fail if Django escapes the apostrophe to &#x27;
    self.assertContains(response, "You can't have an empty list item") 
```

### DRY URLs
**[DO]** Implement `get_absolute_url` and pass instances to `redirect()`.
```python
# models.py
class List(models.Model):
    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])

# views.py
return redirect(our_list)

# template.html
<form method="POST" action="{% url 'view_list' list.id %}">
```
**[DON'T]** Hardcode URL strings.
```python
# views.py
return redirect(f"/lists/{our_list.id}/")

# template.html
<form method="POST" action="/lists/{{ list.id }}/">
```