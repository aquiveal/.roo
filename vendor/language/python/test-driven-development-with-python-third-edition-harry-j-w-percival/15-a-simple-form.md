@Domain
Trigger these rules when the user requests tasks involving Django forms, input validation, moving logic out of Django views, rendering HTML forms via Django templates, or writing tests for form validation and saving.

@Vocabulary
- **ModelForm**: A Django class (`forms.models.ModelForm`) that autogenerates a form based on a specific database model.
- **class Meta**: An inner class used within a `ModelForm` to define the target `model`, `fields`, `widgets`, and `error_messages`.
- **Widget**: A Django form component that dictates how a form field is rendered in HTML (e.g., `forms.widgets.TextInput`).
- **is_valid()**: A Django form method that triggers validation and populates the `errors` dictionary. Returns a boolean.
- **form.errors**: A dictionary-like object populated after `is_valid()` is called, mapping field names to lists of validation error strings.
- **form.instance**: The database model instance that the `ModelForm` is currently creating or modifying.
- **HTML5 Validation**: Client-side validation automatically enforced by the browser based on HTML attributes like `required`.
- **Development-Driven Tests**: A temporary exploratory coding technique where a unit test is written to intentionally fail (e.g., `self.fail(form.as_p())`) to inspect the output of an unfamiliar API.

@Objectives
- The AI MUST encapsulate user input validation and object creation logic within Django Form classes.
- The AI MUST keep Django views "thin" by delegating validation and saving responsibilities to Forms.
- The AI MUST implement robust, isolated unit tests for Form classes, specifically testing validation constraints and custom save behaviors.
- The AI MUST integrate Forms into templates utilizing Django's native field and error rendering.
- The AI MUST utilize constants for hardcoded error messages to ensure DRY (Don't Repeat Yourself) principles across tests and application code.

@Guidelines

**Architecture & View Refactoring**
- **Thin Views**: When encountering a complex view containing manual `request.POST` data extraction and validation, the AI MUST refactor this logic into a Form class. 
- **Merge Code Early**: When building a form, the AI MUST integrate it into the view and template as early as possible rather than over-engineering the form in isolation.

**Django Forms Implementation**
- **ModelForms**: The AI MUST prefer `forms.models.ModelForm` over standard `forms.Form` when the form directly maps to a database model.
- **Meta Configuration**: The AI MUST configure `ModelForms` using a `class Meta` that explicitly defines `model`, `fields`, `widgets`, and `error_messages`.
- **Constants for Errors**: The AI MUST extract string literals for validation errors into module-level constants (e.g., `EMPTY_ITEM_ERROR = "..."`) and import these constants in both the forms and the test files.
- **Custom Save Methods**: When a `ModelForm` requires additional data not provided by the user (e.g., a parent foreign key), the AI MUST override the form's `save()` method, assign the missing data to `self.instance`, and call `super().save()`.

**Template Integration**
- **Field Rendering**: The AI MUST use Django's template variables to render form inputs (e.g., `{{ form.text }}`).
- **Error Rendering**: The AI MUST conditionally render errors using `{% if form.errors %}`.
- **Single Error Extraction**: Since Django form errors are lists, the AI MUST access the first error string in the template using the `.0` index (e.g., `{{ form.errors.text.0 }}`).

**Testing Best Practices**
- **Exploratory Tests**: The AI MAY use `self.fail()` with a printout of an object (e.g., `form.as_p()`) when initially exploring a new API, but MUST replace this with rigorous assertions once the API behavior is understood.
- **Form Validation Tests**: The AI MUST write unit tests that instantiate the form with `data`, assert `form.is_valid()` is `False`, and assert that the correct error constant is present in `form.errors['fieldname']`.
- **One Assert Per Test**: The AI MUST break down large unit tests into smaller, highly specific tests. 
- **Test Helpers**: If multiple tests require the same setup (e.g., submitting an invalid POST request), the AI MUST extract this setup into a helper method (e.g., `def post_invalid_input(self):`).
- **HTML5 Validation in FTs**: The AI MUST adapt Functional Tests (FTs) to anticipate browser-level HTML5 validation. The AI MUST use CSS pseudo-selectors like `:invalid` and `:valid` (e.g., `#id_text:invalid`) to verify client-side validation rather than waiting for server-rendered error strings when a field is `required`.

**Refactoring Protocol**
- **Backing out**: If a refactoring step (like switching to a ModelForm) breaks multiple disparate tests (e.g., because input `name` attributes change), the AI MUST revert the breaking changes to return to a green state, establish a plan, and apply the refactor incrementally (one ID or attribute at a time).

@Workflow
When requested to implement a form or validation logic, the AI MUST follow this step-by-step process:

1. **Exploration & Unit Testing**: Create a new test file (e.g., `test_forms.py`). Write a test instantiating the Form and asserting its HTML output or validation logic.
2. **Form Definition**: Create the Form class inheriting from `ModelForm`. Define `class Meta` with `widgets` (for CSS classes/placeholders) and `error_messages` (using constants).
3. **Save Method Override**: If the form needs external context to save to the database, write a test passing that context to `form.save()`, then implement the custom `save(self, external_dependency)` method modifying `self.instance`.
4. **View Integration (GET)**: Update the target view to instantiate the empty form and pass it to the template context.
5. **Template Refactoring**: Replace handcrafted HTML inputs in the template with `{{ form.<fieldname> }}`. Update HTML error blocks to use `{{ form.errors.<fieldname>.0 }}`. Update frontend IDs/names to match Django's autogenerated values.
6. **View Integration (POST)**: Update the target view's POST handling to instantiate the form with `request.POST`. Use `if form.is_valid():` to dictate the control flow.
7. **Test Refactoring**: Update view tests to use helper methods for repetitive POST requests. Update Functional Tests to check for HTML5 `:invalid` states instead of server error messages for required fields.

@Examples (Do's and Don'ts)

**[DO] Use Constants for Form Error Messages**
```python
# forms.py
from django import forms
from .models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"

class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ("text",)
        widgets = {
            "text": forms.widgets.TextInput(
                attrs={"placeholder": "Enter a to-do item", "class": "form-control"}
            ),
        }
        error_messages = {"text": {"required": EMPTY_ITEM_ERROR}}
```

**[DON'T] Hardcode error messages directly in the Meta class**
```python
# Anti-pattern: Hardcoded string cannot be easily imported into test files
class ItemForm(forms.models.ModelForm):
    class Meta:
        error_messages = {"text": {"required": "You can't have an empty list item"}}
```

**[DO] Override the form's save method to inject foreign keys**
```python
# forms.py
class ItemForm(forms.models.ModelForm):
    # ... Meta config ...
    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
```

**[DON'T] Manually extract form data to save objects in the view**
```python
# Anti-pattern: Fat view handling manual database creation
def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        # DON'T do this:
        Item.objects.create(text=request.POST["text"], list=nulist)
        return redirect(nulist)
```

**[DO] Use helper methods in tests to maintain one assertion per test**
```python
# test_views.py
class NewListTest(TestCase):
    def post_invalid_input(self):
        return self.client.post("/lists/new", data={"text": ""})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
```

**[DON'T] Write monolithic tests with multiple assertions**
```python
# Anti-pattern: Multiple asserts mask subsequent failures
class NewListTest(TestCase):
    def test_invalid_input(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
```

**[DO] Use `.0` to extract the first form error in templates**
```html
<!-- base.html -->
{% if form.errors %}
  <div class="invalid-feedback">
    {{ form.errors.text.0 }}
  </div>
{% endif %}
```

**[DON'T] Print the raw error list in the template**
```html
<!-- Anti-pattern: Renders as a bulleted <ul> list instead of a clean string -->
{% if form.errors %}
  <div class="invalid-feedback">
    {{ form.errors.text }}
  </div>
{% endif %}
```