# @Domain
Tasks involving frontend UI styling, layout implementation (e.g., Bootstrap, CSS), handling Django static files, and writing tests (Functional and Unit) for aesthetics, layout, and HTML structure.

# @Vocabulary
- **Smoke Test for Aesthetics**: A minimal functional test that verifies whether static files (CSS) have loaded by checking the approximate position or visibility of a key element, rather than testing pixel-perfect designs, fonts, or colors.
- **Template Inheritance**: A Django feature used to eliminate HTML boilerplate by defining a parent `base.html` template with `{% block %}` tags, which child templates `{% extends %}`.
- **StaticLiveServerTestCase**: A Django test class (`django.contrib.staticfiles.testing`) that automatically serves static files during functional tests, unlike the standard `LiveServerTestCase`.
- **collectstatic**: A Django management command that gathers static files from various apps into a single directory (`STATIC_ROOT`) for production web servers.
- **lxml / cssselect**: Python libraries used to parse HTML into a DOM object, allowing unit tests to assert against HTML structure and attributes using CSS selectors rather than brittle string matching.
- **Tuple Unpacking Assertion**: Using Python's assignment unpacking (e.g., `[element] = parsed.cssselect(...)`) to implicitly assert that a selector returns exactly one match.
- **Spiking (in FTs)**: Writing a temporary, quick-and-dirty hack (like an inline `style="..."` attribute) strictly to verify that a new Functional Test works, before reverting the hack to implement the proper framework solution.

# @Objectives
- The AI MUST NOT write brittle tests that verify constants, exact pixel measurements, exact HTML strings, fonts, or colors.
- The AI MUST test layout and styling behavior by writing functional smoke tests that verify CSS is loading (e.g., checking if an element is roughly centered).
- The AI MUST keep HTML templates DRY by aggressively using Django template inheritance.
- The AI MUST ensure static files load properly in test environments by using `StaticLiveServerTestCase`.
- The AI MUST use DOM parsing (`lxml`) for unit testing HTML structure instead of testing raw strings, making tests resilient to semantic whitespace changes or UI framework CSS class additions.

# @Guidelines
- **Testing Aesthetics**: When asked to test layout or styling, the AI MUST NOT test exact pixels. It MUST test the *behavior* of the styling (e.g., "does the CSS load?") by asserting on approximate sizing and coordinates.
- **Window Sizing**: When writing functional tests for layout, the AI MUST set an explicit browser window size using `self.browser.set_window_size(width, height)` before making location assertions.
- **Delta Assertions**: When asserting element coordinates or dimensions in Selenium, the AI MUST use `self.assertAlmostEqual(actual, expected, delta=X)` to account for fractional pixels, scrollbars, and rounding errors.
- **Spike and Revert**: When adding a new layout Functional Test, the AI MUST first use a basic HTML cheat (like `<div style="text-align: center">`) to get the test to pass (verifying the test logic), and then immediately revert it to implement the proper CSS framework solution.
- **Static Files in Tests**: Whenever the AI introduces CSS or static files, it MUST change the functional test base class from `LiveServerTestCase` to `StaticLiveServerTestCase`.
- **Template DRYness**: The AI MUST extract shared HTML boilerplate (like `<head>`, `<nav>`, CSS links) into a `base.html` file using `{% block %}` tags. 
- **Unit Testing HTML**: The AI MUST NOT use `assertContains` with large strings of raw HTML, as it breaks when CSS classes (like Bootstrap's `form-control`) or whitespace are added.
- **HTML Parsing**: The AI MUST use `lxml.html.fromstring()` and `.cssselect()` to query the DOM in unit tests.
- **Tuple Unpacking**: To assert that an HTML element exists and is unique, the AI MUST use tuple unpacking: `[element] = parsed.cssselect('selector')`. If zero or multiple elements are found, this will safely raise a `ValueError`.
- **Static Root**: When configuring Django for production-ready static files, the AI MUST define `STATIC_ROOT = BASE_DIR / "static"` in `settings.py`.
- **Unnecessary Static Files**: If the AI runs `collectstatic` and Django admin is not being used, the AI SHOULD recommend commenting out `django.contrib.admin` in `INSTALLED_APPS` to avoid pulling in unnecessary CSS/JS files.

# @Workflow
1. **Define the Layout FT**: Write a Functional Test using Selenium to find an element, calculate its center using `.location` and `.size`, and assert it is roughly where it should be using `assertAlmostEqual` with a delta.
2. **Cheat to Pass**: Implement an inline HTML/CSS hack in the template just to make the FT pass. (This proves the FT is valid).
3. **Revert the Hack**: Remove the inline style (using `git reset --hard` conceptually).
4. **Refactor Templates**: Create `base.html` with basic structure, and have existing templates extend it.
5. **Integrate CSS Framework**: Download or link the CSS framework (e.g., Bootstrap) in `base.html` under the `/static/` URL path.
6. **Apply CSS Classes**: Update the template HTML with the framework's grid and styling classes (e.g., `container`, `row`, `justify-content-center`).
7. **Fix Test Environment**: Change the FT runner to inherit from `StaticLiveServerTestCase` so the CSS files are actually served during the test.
8. **Fix Brittle Unit Tests**: If applying CSS classes breaks unit tests relying on exact HTML string matching, refactor those unit tests to use `lxml` and `cssselect` to target specific tags and attributes independently of their formatting or styling classes.

# @Examples (Do's and Don'ts)

### Functional Testing Layout
**[DO]** Set explicit window size and use `assertAlmostEqual` with a delta.
```python
def test_layout_and_styling(self):
    self.browser.set_window_size(1024, 768)
    inputbox = self.browser.find_element(By.ID, "id_new_item")
    self.assertAlmostEqual(
        inputbox.location["x"] + inputbox.size["width"] / 2,
        512,
        delta=10,
    )
```

**[DON'T]** Assert exact pixel locations without setting window size, or test aesthetic constants like colors.
```python
def test_layout_and_styling(self):
    inputbox = self.browser.find_element(By.ID, "id_new_item")
    # Brittle: Fails on different screens or minor rendering differences
    self.assertEqual(inputbox.location["x"], 300) 
    self.assertEqual(inputbox.value_of_css_property("color"), "rgba(255, 0, 0, 1)")
```

### Serving Static Files in Functional Tests
**[DO]** Use `StaticLiveServerTestCase`.
```python
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):
    # Tests will now serve CSS/JS files correctly
```

**[DON'T]** Rely on standard `LiveServerTestCase` when testing CSS/JS behavior.
```python
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):
    # CSS files will return 404s, failing layout tests
```

### Unit Testing HTML Attributes
**[DO]** Parse the HTML and use CSS selectors and list unpacking to verify structure.
```python
import lxml.html

def test_renders_input_form(self):
    response = self.client.get("/")
    parsed = lxml.html.fromstring(response.content)
    
    # Implicitly asserts exactly ONE form exists with method POST
    [form] = parsed.cssselect("form[method=POST]")
    self.assertEqual(form.get("action"), "/lists/new")
    
    # Asserting an input with a specific name exists in the form, ignoring CSS classes
    inputs = form.cssselect("input")
    self.assertIn("item_text", [input.get("name") for input in inputs])
```

**[DON'T]** Use `assertContains` with large strings of raw HTML that include presentation logic.
```python
def test_renders_input_form(self):
    response = self.client.get("/")
    # Brittle: Fails if someone adds 'class="form-control"' to the input tag
    self.assertContains(
        response, 
        '<input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />',
        html=True
    )
```