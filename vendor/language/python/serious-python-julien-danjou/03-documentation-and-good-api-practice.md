# @Domain

These rules MUST trigger whenever the AI is tasked with creating, maintaining, or refactoring Python documentation, configuring documentation generators (Sphinx), designing Python APIs (Application Programming Interfaces), managing library versions, or deprecating existing Python functions/classes. 

# @Vocabulary

- **reST (reStructuredText)**: The lightweight, standard markup language for Python documentation.
- **Sphinx**: The de facto standard documentation generation tool for Python projects that consumes reST and outputs HTML/PDF.
- **autodoc (`sphinx.ext.autodoc`)**: A Sphinx extension that extracts reST-formatted docstrings directly from Python modules.
- **autosummary (`sphinx.ext.autosummary`)**: A Sphinx extension that automatically generates a table of contents and individual pages for specified modules.
- **doctest**: A Python standard module and Sphinx builder that searches documentation for interactive Python sessions (`>>>`) and tests them for accuracy.
- **DDD (Documentation-Driven Development)**: A methodology where the developer writes documentation and examples first, and then writes the code to match.
- **TDD (Test-Driven Development)**: Writing unit tests based on use cases before writing the API implementation, forcing design for usability.
- **Public API**: The interface exposed to end-users. 
- **Private API**: Internal code, universally denoted in Python by prefixing the symbol name with a single underscore (`_`).
- **DeprecationWarning / PendingDeprecationWarning**: Built-in warning classes used to alert developers that a function or feature is obsolete.
- **debtcollector**: A Python library that provides decorators to automate the emission of deprecation warnings and docstring updates.
- **Read the Docs**: An online tool that automatically builds and publishes Sphinx documentation.

# @Objectives

- Treat documentation as a first-class citizen, integrating it directly into the source code to prevent it from becoming out-of-date.
- Automate the documentation extraction, testing, and generation processes using Sphinx and its extensions.
- Maintain rigorous separation between Public and Private APIs using Pythonic naming conventions.
- Manage API evolution safely by implementing formal deprecation processes, explicit versioning, and rigorous changelog updates.
- Ensure all API designs prioritize simplicity, usability, explicitly documented "magic," and testability.

# @Guidelines

## Project Documentation Structure
- The AI MUST use `reStructuredText` (`.rst`) for all Python documentation files.
- The AI MUST ensure the root project directory contains a `README.rst` file detailing:
  1. The problem the project solves (1-2 sentences).
  2. The license under which the project is distributed.
  3. A small, working example of the code.
  4. Installation instructions.
  5. Links to community support (mailing list, IRC, forums).
  6. A link to the bug tracker system.
  7. A link to the source code.
- The AI MUST add the license information as a header in every single code file.
- The AI MUST create a `CONTRIBUTING.rst` file for source control (e.g., GitHub) providing a checklist for pull requests (e.g., PEP 8 compliance, unit test requirements).

## Sphinx Configuration and Automation
- The AI MUST locate or generate Sphinx configuration in the `doc/source` directory (specifically `conf.py` and `index.rst`).
- The AI MUST enable `sphinx.ext.autodoc` in `conf.py` to extract docstrings automatically.
- The AI MUST use the `.. automodule::` directive with appropriate flags (`:members:`, `:undoc-members:`, `:show-inheritance:`) to ensure complete module documentation.
- The AI MUST enable `sphinx.ext.autosummary` to automatically generate API tables of contents.
- The AI MUST embed interactive Python examples starting with `>>>` in docstrings to utilize the `doctest` module.
- When working with HTTP REST APIs or complex frameworks, the AI MUST utilize or write Sphinx extensions (like `sphinxcontrib-pecanwsme` or `sphinxcontrib.httpdomain`) to automatically extract API documentation from the code rather than writing it by hand.

## API Design and Visibility
- The AI MUST prefix all internal, non-public variables, functions, and classes with an underscore (`_`) to explicitly mark them as Private APIs.
- The AI MUST keep Public APIs simple and intuitive to prevent user error.
- The AI MUST "make the magic visible." If the API performs complex or unexpected operations under the hood, the AI MUST explicitly document these behaviors in the docstring.
- The AI MUST design APIs based on practical use cases, assuming the role of the end-user.

## API Evolution and Deprecation
- The AI MUST bump API version numbers based on user impact: Major changes = Major version bump (1 to 2); Minor additions = Minor version bump (2.2 to 2.3); Bug fixes = Patch version bump (2.2.0 to 2.2.1).
- The AI MUST NOT remove an old interface immediately upon changing an API. The old interface MUST be retained and marked as deprecated.
- The AI MUST document all deprecated elements using the Sphinx `.. deprecated:: <version>` directive, explicitly providing instructions on how to migrate to the new interface.
- The AI MUST raise runtime warnings for deprecated functions using the `warnings` module (`warnings.warn("msg", DeprecationWarning)`).
- When available in the project, the AI SHOULD use the `debtcollector` library (e.g., `@moves.moved_method`) to automate deprecation warnings and docstring generation.
- The AI MUST configure the test suite to run with the `-W error` flag (translating warnings to fatal errors) to catch calls to deprecated functions within the project's own code.

# @Workflow

## Workflow: Creating a New API Method
1. **Use Case & TDD**: Define the use case. Write unit tests (TDD) that simulate the user interacting with the new API.
2. **Drafting (DDD)**: Write the function signature and a complete `reST` docstring, including a step-by-step tutorial using `>>>` prompts for `doctest`.
3. **Implementation**: Write the implementation of the API, keeping the public surface simple. Prefix internal helper methods with `_`.
4. **Integration**: Add the module to the Sphinx `.rst` documentation files using `.. automodule:: <module_name>` and `.. autosummary::`.
5. **Testing**: Run `sphinx-build -b doctest doc/source doc/build` to ensure the documentation examples compile and pass.

## Workflow: Deprecating an Old API Method
1. **Create the New Interface**: Implement the new API following the workflow above.
2. **Modify the Old Interface's Docstring**: Add the `.. deprecated:: <version>` directive to the old method's docstring, clearly stating the new method users should call.
3. **Inject Runtime Warnings**: Import the `warnings` module and add a `warnings.warn()` call specifying `DeprecationWarning`, OR apply a `debtcollector` decorator like `@moves.moved_method`.
4. **Delegate Logic**: Refactor the old method's body to simply call the new method with the converted arguments, ensuring backward compatibility.
5. **Test Migration**: Run the project's test suite with `-W error` to identify and update any internal code that is still calling the newly deprecated method.
6. **Update Changelog**: Document the new elements, the deprecated elements, and migration instructions in the project's version changelog.

# @Examples (Do's and Don'ts)

## API Visibility
**[DO]** Explicitly separate public and private methods using the underscore prefix.
```python
class Car(object):
    def turn(self, direction):
        """Public API to turn the car."""
        self._calculate_wheel_angle(direction)
        
    def _calculate_wheel_angle(self, direction):
        """Private API for internal physics calculations."""
        pass
```

**[DON'T]** Leave private internal mechanics exposed as public APIs.
```python
class Car(object):
    def turn(self, direction):
        self.calculate_wheel_angle(direction)
        
    def calculate_wheel_angle(self, direction): # Missing underscore!
        pass
```

## Documenting and Emitting Deprecations
**[DO]** Use both Sphinx directives and runtime warnings to ensure the user is notified of deprecations.
```python
import warnings

class Car(object):
    def turn_left(self):
        """Turn the car left.

        .. deprecated:: 1.1
           Use :func:`turn` instead with the direction argument set to "left".
        """
        warnings.warn("turn_left is deprecated; use turn instead", DeprecationWarning)
        return self.turn(direction='left')

    def turn(self, direction):
        """Turn the car in some direction.

        :param direction: The direction to turn to.
        :type direction: str
        """
        pass
```

**[DON'T]** Delete the old method immediately, breaking backward compatibility without warning.
```python
class Car(object):
    # turn_left was completely deleted! User code will instantly crash with AttributeError.
    
    def turn(self, direction):
        """Turn the car in some direction."""
        pass
```

## Using `debtcollector` for Deprecation
**[DO]** Use automation libraries like `debtcollector` for clean, boilerplate-free deprecations.
```python
from debtcollector import moves

class Car(object):
    @moves.moved_method('turn', version='1.1')
    def turn_left(self):
        """Turn the car left."""
        return self.turn(direction='left')
```

## Interactive Doctests
**[DO]** Include executable examples in the docstrings so `doctest` can verify them.
```python
def add(a, b):
    """
    Add two numbers together.

    >>> add(2, 2)
    4
    >>> add(5, -1)
    4
    """
    return a + b
```