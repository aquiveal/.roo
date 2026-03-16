@Domain
Trigger these rules when tasked with Django web application development involving data validation, form creation, form/view refactoring, model constraints, template rendering, and Test-Driven Development (TDD) involving form submissions and database integrity.

@Vocabulary
- **Model-Level Validation**: Validation enforced by Django's Python logic (e.g., `blank=False`), triggered explicitly via `.full_clean()`, raising a `ValidationError`.
- **Database-Level Validation**: Constraints enforced by the underlying database engine (e.g., `NOT NULL`, `UNIQUE`), triggering an `IntegrityError` upon `.save()`.
- **unique_together**: A Django `Meta` class attribute used to enforce uniqueness across a combination of multiple model fields.
- **ModelForm Sweet Spot**: The boundary up to which `ModelForm` is useful before it becomes an anti-pattern. Exceeding this boundary involves mixing presentation logic, validation logic, and ORM/storage logic within a single Python form class.
- **Form Context Injection**: The practice of passing external context (like a parent model instance) into a form by overriding the `__init__` method.
- **clean_<fieldname>**: A Django form method used to apply custom validation logic to a specific field.
- **Developer Silliness**: The concept of writing tests for deliberately perverse implementations. The AI must guard against accidental logic errors but assume the developer is not intentionally writing malicious/perverse code.

@Objectives
- Push data integrity constraints to the lowest possible layer (the database/model layer).
- Ensure that form logic strictly handles validation and data conversion, without leaking presentation logic (HTML/CSS) into Python code.
- Write robust, specific unit tests that cleanly differentiate between database errors (`IntegrityError`) and application validation errors (`ValidationError`).
- Recognize when the abstractions of a framework (like `ModelForm`) leak or become burdensome, and willingly downgrade to simpler structures (like `forms.Form`) to maintain clean separation of concerns.

@Guidelines

**Testing Principles & Constraints**
- The AI MUST NOT write tests for deliberately perverse or malicious implementations (e.g., writing tests to ensure a function doesn't arbitrarily return `666`). The AI MUST write tests to protect against accidental omissions or structural mistakes.
- The AI MUST explicitly add tests to verify that valid edge cases do *not* raise errors (e.g., testing that the same item *can* be saved to two different parent lists). Use comments like `# should not raise` to document the intent.
- When asserting the ordering or contents of a Django `QuerySet` against a standard Python list, the AI MUST wrap the QuerySet in `list()` to prevent confusing evaluation mismatches (e.g., `self.assertEqual(list(queryset), [item1, item2])`).
- The AI MUST test string representations of models by explicitly calling `str()` on the model instance and asserting the output.
- When shifting presentation logic from the form to the template, the AI MUST delete the lower-level presentation tests from the form test file and replace them with higher-level view tests (using tools like `lxml` to parse the HTML and check for CSS classes like `is-invalid`).

**Model & Database Validation**
- The AI MUST know that Django's `.save()` method DOES NOT run full model validation. To test model-level validation (e.g., `blank=False` or `unique_together`), the AI MUST explicitly call `.full_clean()` before `.save()`.
- The AI MUST capture `ValidationError` (from `django.core.exceptions`) when testing `.full_clean()`, and `IntegrityError` (from `django.db.utils`) when testing `.save()` constraints.
- When adding uniqueness constraints across multiple columns, the AI MUST use the `Meta` class `unique_together` attribute and MUST generate a corresponding database migration.

**Form Design & Refactoring**
- When a form requires knowledge of a parent object (e.g., knowing which `List` an `Item` belongs to for uniqueness validation), the AI MUST override the form's `__init__` method to accept the parent object, pop it from kwargs/args, assign it to an instance variable, and call `super().__init__`.
- The AI MUST implement custom field validation by defining a `clean_<fieldname>(self)` method that raises `forms.ValidationError` if the custom logic fails.
- The AI MUST override the form's `save()` method if it needs to automatically attach the parent object to the child object before committing to the database.
- **CRITICAL SEPARATION OF CONCERNS**: The AI MUST NOT inject CSS classes (like Bootstrap's `is-invalid`) or HTML attributes via Python form widget modifications (e.g., `self.fields["text"].widget.attrs["class"] += " is-invalid"`). The AI MUST push presentation logic to the HTML template using template conditionals (e.g., `{% if form.errors %}is-invalid{% endif %}`).
- If a `ModelForm` requires extensive overriding of `__init__`, `clean`, `save`, and widget attributes, the AI MUST recognize this as an anti-pattern and refactor the class to inherit from a standard `forms.Form`, handling the ORM creation explicitly in the `save()` method.

@Workflow
When implementing advanced validation and forms, follow this exact sequence:

1. **Functional Test**: Write an FT that triggers the validation error in the browser and expects a specific UI response (e.g., a Bootstrap `.invalid-feedback` element).
2. **Model Validation Test**: Write a unit test invoking `.full_clean()` and wrapping it in `with self.assertRaises(ValidationError):`.
3. **Model Implementation**: Add the constraint to the model (e.g., `class Meta: unique_together = ("parent", "child")`) and run `makemigrations`.
4. **Form Initialization**: Write a unit test for a custom form that passes the required context (e.g., `form = MyForm(parent_obj, data=...)`).
5. **Form Validation Logic**: Write a unit test ensuring `form.is_valid()` returns `False` and `form.errors` contains the correct message. Implement `clean_<fieldname>()` in the form.
6. **Form Save Logic**: Write a unit test for `form.save()` ensuring it correctly associates the child with the parent. Implement the overridden `save()` method.
7. **View Refactoring**: Update the view to instantiate the form with `request.POST` and the parent object. Use `if form.is_valid(): form.save()` to simplify the view.
8. **Template Presentation**: Ensure the HTML template manually handles the rendering of error classes (e.g., `is-invalid` and `invalid-feedback`) using the `form.errors` context, rather than relying on Python-side widget attribute hacks. Delete any Python tests checking for CSS classes on form widgets, replacing them with View tests that parse the rendered HTML.

@Examples (Do's and Don'ts)

**QuerySet Testing**
- [DO]:
```python
def test_list_items_order(self):
    list1 = List.objects.create()
    item1 = Item.objects.create(list=list1, text="i1")
    item2 = Item.objects.create(list=list1, text="item 2")
    self.assertEqual(
        list(list1.item_set.all()),
        [item1, item2]
    )
```
- [DON'T]:
```python
def test_list_items_order(self):
    # This will fail with a confusing error message comparing a QuerySet string representation to a list
    self.assertEqual(
        list1.item_set.all(),
        [item1, item2]
    )
```

**Testing Model Validation**
- [DO]:
```python
def test_duplicate_items_are_invalid(self):
    mylist = List.objects.create()
    Item.objects.create(list=mylist, text="bla")
    with self.assertRaises(ValidationError):
        item = Item(list=mylist, text="bla")
        item.full_clean()
```
- [DON'T]:
```python
def test_duplicate_items_are_invalid(self):
    mylist = List.objects.create()
    Item.objects.create(list=mylist, text="bla")
    with self.assertRaises(ValidationError):
        item = Item(list=mylist, text="bla")
        item.save() # DON'T: This will raise an IntegrityError from the DB, not a Django ValidationError
```

**Form Context Injection**
- [DO]:
```python
class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._for_list = for_list

    def clean_text(self):
        text = self.cleaned_data["text"]
        if self._for_list.item_set.filter(text=text).exists():
            raise forms.ValidationError("Duplicate item")
        return text
```
- [DON'T]:
```python
# DON'T rely on the view to manually attach the parent list before saving, bypassing form validation capabilities.
def view_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.list = parent_list
        # If it's a duplicate, it crashes with IntegrityError here instead of showing a nice form error
        item.save() 
```

**Separation of Presentation and Form Logic**
- [DO]: Handle CSS classes in the HTML template.
```html
<input name="text" class="form-control {% if form.errors %}is-invalid{% endif %}" />
{% if form.errors %}
    <div class="invalid-feedback">{{ form.errors.text.0 }}</div>
{% endif %}
```
- [DON'T]: Hack CSS classes into the Python form object.
```python
class ItemForm(forms.models.ModelForm):
    def is_valid(self):
        result = super().is_valid()
        if not result:
            # DON'T: This mixes presentation logic into Python
            self.fields["text"].widget.attrs["class"] += " is-invalid"
        return result
```