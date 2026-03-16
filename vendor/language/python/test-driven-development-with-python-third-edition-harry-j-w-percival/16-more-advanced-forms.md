# @Domain

These rules MUST activate when the AI is tasked with creating, modifying, or refactoring Django forms, implementing database-layer or form-layer validation (specifically uniqueness or duplicate prevention constraints), writing view or model unit tests, managing Django CSS/UI presentation logic within forms, or troubleshooting `IntegrityError` and `ValidationError` exceptions.

# @Vocabulary

- **IntegrityError**: A database-level exception raised upon calling `.save()` when a database constraint (like `UNIQUE`) is violated.
- **ValidationError**: A Django-level exception raised upon calling `.full_clean()` on a model or `.is_valid()` on a form when a Django-level validation rule is violated.
- **unique_together**: A Django model `Meta` attribute used to enforce composite uniqueness constraints across multiple fields.
- **clean_<fieldname>**: A Django form method hook used to implement custom, field-specific validation logic.
- **is-invalid**: A Bootstrap CSS class applied to HTML form `<input>` elements to trigger the red error styling.
- **invalid-feedback**: A Bootstrap CSS class applied to the `<div>` containing the actual error message text.
- **Developer Silliness**: The concept of deciding what to test. You MUST write tests to protect against *accidental* silliness (e.g., skipping a uniqueness check), but you MUST NOT write tests to protect against *deliberately perverse* implementations.
- **Framework Sweet Spot**: The boundary where a framework feature (like `ModelForm`) saves time. Exceeding the sweet spot means the feature requires too much hackery (mixing presentation, validation, and ORM logic), dictating a fallback to simpler base classes (like `forms.Form`).

# @Objectives

- Push data integrity constraints as deep into the application as possible (database/model layer) to guarantee absolute data consistency.
- Maintain a strict separation of concerns between layers: Forms handle validation, Models handle database interactions, and Templates handle presentation (CSS/HTML).
- Avoid "framework hackery"; if a `ModelForm` requires overriding core methods to inject CSS classes, downgrade it to a basic `Form` and move the UI logic to the template.
- Write hyper-focused, granular unit tests. Avoid long, verbose tests that verify multiple behaviors simultaneously.
- Ensure test outputs are human-readable by defining string representations for models and properly formatting queryset assertions.

# @Guidelines

## Model and Database Constraints
- You MUST enforce uniqueness and composite uniqueness constraints at the database layer using the `class Meta` declaration (e.g., `unique_together = ("field1", "field2")`).
- You MUST explicitly define default sorting in models using `class Meta: ordering = ("id",)` to prevent unpredictable queryset ordering.
- You MUST define a `__str__` method on all models. Without this, test failure messages involving querysets will be unreadable (e.g., `<Item object (3)>`).

## Writing Unit Tests
- **Model Tests**: You MUST refactor verbose, all-encompassing model tests into tiny, specific tests. Create exactly one test for default text values, one test for model relationships, and one test for string representations.
- **Queryset Assertions**: When asserting that a QuerySet matches a specific sequence of items, you MUST cast the QuerySet to a standard Python list first (`list(queryset)`) to avoid Django's obscure QuerySet-to-list comparison evaluation errors.
- **Negative Testing**: You MUST write tests that explicitly check that valid edge cases do *not* raise errors (e.g., saving the same item text to *different* lists should pass). Use a comment `# should not raise` to document the intent.
- **Testing Exceptions**: You MUST use the `with self.assertRaises(ExceptionType):` context manager when verifying that code throws an error. Remember that `item.save()` throws `IntegrityError`, whereas `item.full_clean()` throws `ValidationError`.

## Form Architecture and Validation
- **Contextual Forms**: If a form requires contextual state to validate data (e.g., it needs to know *which* list an item is being added to), you MUST override the form's `__init__` method to accept and store that context (e.g., `def __init__(self, for_list, *args, **kwargs):`).
- **Custom Validation**: You MUST implement custom validation rules by defining `def clean_<fieldname>(self):` on the form. Extract the data using `self.cleaned_data["fieldname"]`, run your conditional logic, and `raise forms.ValidationError(ERROR_MESSAGE)` if it fails.
- **Custom Save Methods**: You MUST override the form's `save()` method if you need to inject the parent object before persisting to the database.

## Presentation and Templates (The "Sweet Spot" Boundary)
- You MUST NOT inject CSS classes (like Bootstrap's `is-invalid`) via Python form widget attributes (e.g., `self.fields['text'].widget.attrs['class'] += ' is-invalid'`). This violates separation of concerns.
- When `ModelForm`s require too much customization of widgets and validation, you MUST revert to a standard `forms.Form` and write the HTML manually in the template.
- You MUST handle form error CSS classes directly in the Django template using conditional template tags (e.g., `<input class="form-control {% if form.errors %}is-invalid{% endif %}">`).
- You MUST extract single error messages safely in the template using the `.0` index (e.g., `{{ form.errors.text.0 }}`) to avoid rendering bulleted lists `<ul>` when only a single string is desired.

## View Testing Checklist
When writing tests for Django views, you MUST cover the following aspects:
1.  **Test Client**: Use `self.client` for all view interactions.
2.  **Templates Used**: Assert the correct template is rendered (`assertTemplateUsed`).
3.  **HTML Contracts**: Assert that critical integration points exist (e.g., the `<form>` `action` URL, the `<input>` `name` attribute).
4.  **Template Logic**: Perform basic smoke tests on `{% for %}` or `{% if %}` outputs.
5.  **Valid POSTs**: Verify database side-effects (e.g., object creation) and assert the correct HTTP 302 redirect (`assertRedirects`).
6.  **Invalid POSTs**: Verify that nothing is saved to the database, verify the response status is 200 (not a redirect), and verify the exact error message is present in the rendered HTML (escaping HTML characters as necessary).

# @Workflow

When implementing a new contextual validation rule (like preventing duplicate items), you MUST follow this exact outside-in sequence:

1.  **Functional Test**: Write an FT simulating the user triggering the validation error and seeing the UI feedback (e.g., `.invalid-feedback`).
2.  **Model Test (Negative)**: Write a unit test verifying that violating the constraint raises a `ValidationError` on `full_clean()`.
3.  **Model Test (Positive)**: Write a unit test verifying that valid similar data (e.g., duplicates across different parents) does *not* raise an error.
4.  **Model Implementation**: Add `class Meta` constraints to the model and implement `__str__` and `ordering`. Run `makemigrations`.
5.  **View Test (Invalid POST)**: Write a unit test for the view verifying that submitting the invalid data does not write to the DB, returns status 200, and contains the escaped error string.
6.  **Form Test**: Write a unit test instantiating the form with the parent context and invalid data, asserting `is_valid()` is `False` and `form.errors` contains the exact error string.
7.  **Form Implementation**: Override `__init__` to accept the context, implement `clean_<fieldname>`, and raise `ValidationError`.
8.  **View Implementation**: Update the view to instantiate the new form, passing the required context.
9.  **Template Implementation**: Manually render the form fields in the HTML, utilizing `{% if form.errors %}is-invalid{% endif %}` to trigger Bootstrap error states. 

# @Examples (Do's and Don'ts)

## Form Architecture and Presentation
**[DON'T]** Mix CSS presentation logic into form validation methods.
```python
# ANTI-PATTERN: Framework hackery exceeding the sweet spot
class ItemForm(forms.models.ModelForm):
    def is_valid(self):
        result = super().is_valid()
        if not result:
            # DO NOT DO THIS: Python forms should not know about Bootstrap CSS classes
            self.fields["text"].widget.attrs["class"] += " is-invalid"
        return result
```

**[DO]** Use basic forms for complex validation and handle CSS in the template.
```python
# Python Form
class ExistingListItemForm(forms.Form):
    text = forms.CharField(
        error_messages={"required": "You can't have an empty list item"}
    )
    
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._for_list = for_list

    def clean_text(self):
        text = self.cleaned_data["text"]
        if self._for_list.item_set.filter(text=text).exists():
            raise forms.ValidationError("You've already got this in your list")
        return text
```
```html
<!-- Django Template -->
<form method="POST" action="{% url 'view_list' list.id %}">
  {% csrf_token %}
  <input 
    name="text" 
    class="form-control {% if form.errors %}is-invalid{% endif %}"
    value="{{ form.text.value | default:'' }}"
  />
  {% if form.errors %}
    <div class="invalid-feedback">{{ form.errors.text.0 }}</div>
  {% endif %}
</form>
```

## Model Testing and Representation
**[DON'T]** Leave models without string representations, resulting in unreadable test failures, or compare raw QuerySets to lists.
```python
# ANTI-PATTERN
def test_list_items_order(self):
    # This will output <QuerySet [<Item object (1)>, ...]> on failure
    self.assertEqual(list1.item_set.all(), [item1, item2])
```

**[DO]** Define `__str__` on models, define ordering, and cast QuerySets to lists in tests.
```python
# models.py
class Item(models.Model):
    text = models.TextField(default="")
    
    class Meta:
        ordering = ("id",)
        unique_together = ("list", "text")

    def __str__(self):
        return self.text

# test_models.py
def test_list_items_order(self):
    list1 = List.objects.create()
    item1 = Item.objects.create(list=list1, text="i1")
    item2 = Item.objects.create(list=list1, text="item 2")
    
    # Cast queryset to list for accurate evaluation and readable failures
    self.assertEqual(list(list1.item_set.all()), [item1, item2])
```

## Testing Exceptions
**[DON'T]** Manually write try/except blocks to test for exceptions.
```python
# ANTI-PATTERN
try:
    item.full_clean()
    self.fail("Should have raised ValidationError")
except ValidationError:
    pass
```

**[DO]** Use the `assertRaises` context manager.
```python
# DO
def test_duplicate_items_are_invalid(self):
    mylist = List.objects.create()
    Item.objects.create(list=mylist, text="bla")
    with self.assertRaises(ValidationError):
        item = Item(list=mylist, text="bla")
        item.full_clean()
```