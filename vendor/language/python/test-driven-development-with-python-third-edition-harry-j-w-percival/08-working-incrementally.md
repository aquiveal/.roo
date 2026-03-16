# @Domain
Trigger these rules when the user requests architectural changes, feature additions that require restructuring existing code, database model migrations involving relationships (like Foreign Keys), or specifically asks to refactor existing code to support new behaviors. These rules strictly govern the AI's behavior during Test-Driven Development (TDD) cycles involving both Functional Tests (FTs) and Unit Tests (UTs), focusing on incremental, step-by-step evolution of the codebase.

# @Vocabulary
- **Working State to Working State**: The core methodology of making microscopic, self-contained code changes to ensure the test suite is always green before taking the next step.
- **YAGNI (You Ain't Gonna Need It)**: The principle of resisting the urge to write code, fields, or features just because they "might be useful" in the future.
- **Regression Test**: An existing Functional Test that must be kept passing while implementing a new design, ensuring previous capabilities are not broken.
- **Refactoring Cat**: An anti-pattern describing a developer (or AI) who dives in and changes multiple files (models, views, templates) simultaneously, breaking the system entirely and losing track of the working state.
- **Double-Loop TDD**: The workflow where an outer loop (Functional Tests) drives high-level requirements and an inner loop (Unit Tests) drives specific implementation details.
- **REST-ish Design**: Designing URL structures that map cleanly to data structures and resources (e.g., `/lists/<identifier>/` for viewing, `/lists/new` for creation).
- **Programming by Wishful Thinking**: Writing tests or templates using variables, URLs, or relationships before they actually exist in the backend, allowing the resulting errors to dictate the next development step.
- **Capture Group**: A URL routing syntax (e.g., `<int:list_id>`) used to extract parameters from a URL and pass them to a view.

# @Objectives
- To implement major design changes and new features without ever leaving a "working state" for longer than a single test cycle.
- To use existing Functional Tests as a safety net (regression tests) while modifying underlying implementation details.
- To rigorously enforce the YAGNI principle by writing *only* the code mandated by the current failing test.
- To cleanly separate concerns by splitting monolithic views, URLs, and templates into distinct, resource-oriented components step-by-step.
- To isolate failures effectively by addressing one error at a time, avoiding the temptation to fix multiple disconnected errors in a single prompt.

# @Guidelines
- **Avoid Big Bang Refactoring (No Refactoring Cat)**: The AI MUST NOT implement a new design across models, views, and templates simultaneously. Changes MUST be executed one file or one logical step at a time.
- **YAGNI Enforcement**: When modifying models or databases, the AI MUST NOT add extraneous fields (e.g., user names, passwords, timestamps) unless explicitly requested by the user or the test.
- **Respect the Regression Test**: When adding new Functional Tests, the AI MUST ensure that older FTs remain passing. If an older FT fails, a regression has occurred, and the AI MUST immediately halt feature development to fix the regression.
- **Embrace "Cheating" for Green Tests**: If a refactoring step breaks the code, the AI MAY use temporary hardcoded values (cheats) to return the test to a green state quickly, provided it immediately follows up with a proper refactoring step to remove the hardcoded value.
- **Template-Driven API Design**: The AI MUST use templates to define the ideal data API (e.g., `{{ list.id }}`) and let the resulting `TemplateDoesNotExist` or missing context errors drive the creation of the backend views and models.
- **Verify Frontend/Backend Contracts**: When Unit Tests pass but Functional Tests fail, the AI MUST investigate the HTML integration points (e.g., checking if `<form>` tags have the correct `action="..."` URL and `method="POST"`).
- **URL Parameter Extraction**: The AI MUST utilize URL capture groups (e.g., `<int:list_id>`) to pass identifiers to views, and update view signatures to accept these parameters.
- **URL Delegation**: Once an app contains multiple specific URLs, the AI MUST refactor the top-level `urls.py` to use `include()` to delegate routing to the app's specific `urls.py`.
- **Remove Redundancy**: After a successful refactor where responsibilities have been successfully separated (e.g., splitting a single view into two), the AI MUST delete the now-redundant code and obsolete tests.

# @Workflow
1. **Define the Goal (FT Level)**: Write or extend a Functional Test to define the new requirement. Use Regex if necessary to define URL patterns (e.g., `assertRegex(url, '/lists/.+')`). Run the FT to confirm it fails exactly as expected.
2. **Identify the Smallest Step**: Break the feature into the absolute smallest technical increment (e.g., just change the URL redirect of an existing view).
3. **Write the Unit Test**: Modify or write a Unit Test for that specific increment. Run the UT and observe the failure.
4. **Implement Minimal Code**: Write the bare minimum code to pass the UT. If this requires pointing a new URL to an old view temporarily, do it.
5. **Verify State**: Run the UTs. If green, run the FTs. Check if the regression tests pass and if the new FT progresses further.
6. **Iterate Towards Design**: 
   - *Split the Views*: Create a placeholder view for the new endpoint. Update the UTs to expect this new view.
   - *Split the Templates*: Create a placeholder template. Make the view render it.
   - *Update the Model*: When the view requires saving relationships (like a Foreign Key), update the model, generate migrations, and adjust the view to handle the relationship.
7. **Fix Integration Breakages**: As the design shifts, if FTs fail due to missing context or broken form actions, fix the HTML templates to point to the newly created URLs.
8. **Refactor and Clean Up**: Once FTs and UTs are fully green, review the code. Delete old views, remove redundant logic, strip obsolete tests, and extract shared URLs into an `include()` block.

# @Examples (Do's and Don'ts)

### Working State / Routing

**[DO]** Point a new URL to an existing view temporarily to ensure the routing works before building out the complex new logic.
```python
# First step: Point new URL to existing home_page view to keep tests green
urlpatterns = [
    path("", views.home_page, name="home"),
    path("lists/the-only-list-in-the-world/", views.home_page, name="view_list"),
]
```

**[DON'T]** Delete the old URL, write three new views, and change the template all in one massive, untestable leap.
```python
# ANTI-PATTERN: Refactoring Cat
urlpatterns = [
    path("new", views.new_list, name="new_list"),
    path("<int:list_id>/", views.view_list, name="view_list"),
    path("<int:list_id>/add_item", views.add_item, name="add_item"),
]
# Doing this before the views or templates exist will completely break the app.
```

### YAGNI (Database Models)

**[DO]** Add only the exact fields required by the current test failure.
```python
class List(models.Model):
    pass # Start with an empty model if that's all the test requires to map the Foreign Key

class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
```

**[DON'T]** Anticipate future requirements by adding unrequested fields.
```python
# ANTI-PATTERN: YAGNI Violation
class List(models.Model):
    name = models.CharField(max_length=255) # Unrequested
    created_at = models.DateTimeField(auto_now_add=True) # Unrequested
    owner = models.ForeignKey(User) # Unrequested at this stage
```

### URL Parameter Capture

**[DO]** Use URL capture groups and pass them into the view signature.
```python
# urls.py
path("lists/<int:list_id>/", views.view_list, name="view_list")

# views.py
def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    # ...
```

**[DON'T]** Rely on global states or hardcoded IDs once the test demands unique URLs.
```python
# ANTI-PATTERN
def view_list(request):
    our_list = List.objects.first() # Fails when multiple lists exist
```

### Regression / Integration Points

**[DO]** Verify form actions in unit tests when splitting views to ensure the frontend talks to the correct backend endpoint.
```python
def test_renders_input_form(self):
    response = self.client.get(f"/lists/{mylist.id}/")
    self.assertContains(response, f'<form method="POST" action="/lists/{mylist.id}/add_item">')
```

**[DON'T]** Assume that because a view unit test passes, the feature works. The HTML form might still be POSTing to the old URL.
```html
<!-- ANTI-PATTERN: Leaving old hardcoded URLs after refactoring views -->
<form method="POST" action="/">
```