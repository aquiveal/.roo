@Domain
These rules activate whenever the AI is implementing new features, designing system architecture, refactoring templates, or writing tests (Functional Tests and Unit Tests), specifically within a Django or MVC web framework context using Test-Driven Development (TDD).

@Vocabulary
- **Outside-In TDD:** A development methodology that drives design starting from the outermost user-facing layers (Presentation/GUI) and moves inward through the Controller/View layers down to the innermost Model/Database layers.
- **Inside-Out TDD:** An anti-pattern (in this context) where development starts at the innermost database/model layer based on speculation, moving outward to the UI.
- **Programming by Wishful Thinking:** Writing code at a higher level of abstraction by pretending the lower-level details, APIs, or data structures already exist and work exactly as desired.
- **Presentation Layer:** The outermost layer, representing the UI (HTML templates in Django).
- **Controller Layer:** The middle routing and logic layer (URLs and Views in Django).
- **Model Layer:** The innermost data and business logic layer (Django Models).
- **Template Composition:** Using template includes (`{% include %}`) to build pages from reusable fragments, as opposed to relying strictly on Template Inheritance (`{% extends %}`).
- **Early Return:** Placing a `return` statement in the middle of a Functional Test (FT) to temporarily halt its execution, ensuring the test suite is "green" (passing) so that refactoring can be done safely.
- **YAGNI (You Ain't Gonna Need It):** The principle of avoiding the implementation of features or APIs until they are strictly required by a higher-level layer.

@Objectives
- Drive all system design and API contracts from the perspective of the user (from the outside in), rather than speculating on database requirements (from the inside out).
- Ensure lower-level components are built *only* to satisfy the exact, proven requirements of the higher-level components that consume them.
- Maintain a "working state to working state" workflow by refactoring only against a passing (green) test suite.
- Create flexible, readable template architectures by preferring composition over deep, awkward inheritance hierarchies.
- Use tests as explicit documentation for system constraints and edge cases (e.g., explicitly testing that optional fields are truly optional).

@Guidelines
- **Enforce Outside-In Development:** The AI MUST NOT start feature implementation by adding attributes to database models. The AI MUST begin at the Functional Test layer, move to the Template layer, then the View/URL layer, and finally the Model layer.
- **Apply Wishful Thinking:** When writing upper-layer code (like a template or view), the AI MUST invent the most convenient API possible for that specific context, even if the underlying model or method does not exist yet.
- **Refactor Only on Green:** If a refactor is required mid-feature, the AI MUST temporarily disable failing assertions (e.g., using an Early Return in an FT) to get the test suite back to green before executing the refactor.
- **Prefer Composition Over Inheritance in Templates:** When templates share disparate parts (e.g., some share a form, some share a table), the AI MUST extract those parts into reusable includes (`{% include %}`) rather than forcing awkward subclassing/inheritance structures (`{% extends %}`).
- **Accept Temporary Failing Tests Across Layers:** When moving down a layer (e.g., from View to Model) to satisfy a requirement, the AI MAY leave the upper-layer test failing temporarily rather than over-complicating the test suite with mocks, unless strict test isolation (London-school TDD) is explicitly requested.
- **Use `@property` for Duck Typing:** The AI MUST use the `@property` decorator to encapsulate logic behind an attribute-like interface on models. This decouples the interface from the implementation, allowing smooth API usage in templates.
- **Explicitly Test Negative/Optional Constraints:** The AI MUST write specific tests to document when fields are optional (e.g., saving a model with no owner and asserting it does not raise an error).
- **Manually Supplement Security Tests:** Because Outside-In TDD focuses heavily on user-visible features, the AI MUST proactively prompt for or implement tests for non-user-visible critical features, particularly security and authorization constraints.

@Workflow
1. **Functional Test (FT):** Write the FT describing the user's interaction with the new feature. Run it to get an expected failure.
2. **Presentation Layer (Template):** Write the HTML to satisfy the FT. Use "Wishful Thinking" to call variables or methods (e.g., `list.name`) that represent the ideal API.
3. **Controller Layer (URL/View):** Map the URL and create the view. Write a unit test for the view. Update the view to pass the exact context variables demanded by the Template.
4. **Model Layer (Database):** When the view requires a database change (e.g., saving a list owner), write a unit test for the Model layer. Implement the model fields or `@property` methods to satisfy the View's requirements.
5. **Mid-Feature Refactoring (If Needed):** 
   - Insert an Early Return (`return`) in the FT just before the failing step.
   - Run tests to ensure green status.
   - Execute the refactor (e.g., splitting a base template into includes).
   - Remove the Early Return and resume TDD.

@Examples (Do's and Don'ts)

**Template Architecture**
- [DO] Use composition (`include`) for flexible shared components:
  ```html
  {% block extra_header %}
    {% include "includes/form.html" with form=form form_action=form_action %}
  {% endblock %}
  {% block scripts %}
    {% include "includes/scripts.html" %}
  {% endblock %}
  ```
- [DON'T] Use awkward inheritance to remove features from a base template:
  ```html
  {% extends 'base.html' %}
  <!-- Attempting to "switch off" the table block inherited from base -->
  {% block table %}{% endblock %}
  ```

**Refactoring During TDD**
- [DO] Use an Early Return in an FT to refactor against a green state:
  ```python
  self.wait_for(lambda: self.assertIn("edith@example.com", self.browser.find_element(By.CSS_SELECTOR, "h1").text))
  return # TODO: resume here after templates refactor
  # ... rest of the failing test
  ```
- [DON'T] Refactor application code while the test suite is failing.

**Model API Design (Programming by Wishful Thinking)**
- [DO] Define the ideal API in the template, then implement it cleanly in the model using `@property`:
  ```html
  <!-- Template (Wishful Thinking) -->
  <a href="{{ list.get_absolute_url }}">{{ list.name }}</a>
  ```
  ```python
  # Model (Implementation)
  @property
  def name(self):
      return self.item_set.first().text
  ```
- [DON'T] Start by adding speculative fields to the database before the UI demands them:
  ```python
  # Anti-pattern: Inside-Out TDD
  class List(models.Model):
      name = models.CharField(max_length=255) # Added just in case we need it later
      owner = models.ForeignKey(User) # Added before we even have a login system
  ```

**Testing Optional Constraints (Tests as Documentation)**
- [DO] Write an explicit test to prove a field is optional:
  ```python
  def test_list_owner_is_optional(self):
      List.objects.create()  # should not raise an error
  ```
- [DON'T] Rely on implicit framework defaults without documenting the intended behavior via a test.