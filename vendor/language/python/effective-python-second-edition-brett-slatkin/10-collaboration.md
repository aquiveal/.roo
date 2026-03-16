# @Domain
These rules MUST be triggered whenever the AI is assisting with Python programming tasks related to project setup, dependency management, API design, module organization, code documentation, exception hierarchy design, static type annotation, or codebase refactoring. It specifically applies when creating reusable libraries, collaborative codebases, or production-grade applications that require stability, strict interface boundaries, and forward compatibility.

# @Vocabulary
*   **PyPI (Python Package Index):** The central repository of community-built Python modules.
*   **pip:** The standard Python command-line tool for installing packages (`python3 -m pip`).
*   **venv:** The built-in module used to create isolated virtual environments, preventing dependency conflicts.
*   **Transitive Dependency / Dependency Hell:** The situation where different packages require conflicting versions of the same underlying package.
*   **Docstring:** A string literal (wrapped in `"""`) forming the first statement in a module, class, or function, accessible at runtime via the `__doc__` attribute.
*   **Package:** A directory containing an `__init__.py` file, used to group related modules and define namespaces.
*   **Wildcard Import:** An import statement of the form `from foo import *`, which obscures namespaces and overwrites overlapping names.
*   **__all__:** A special module-level attribute (list of strings) defining the exact explicit public API surface of a module or package.
*   **Deployment Environment:** The specific runtime configuration (e.g., development, testing, production) that dictates how a program should execute.
*   **Root Exception:** A custom base exception class (`class Error(Exception): pass`) defined per-module, from which all other module-specific exceptions inherit.
*   **Circular Dependency:** A mutual interdependence where two modules attempt to import each other at initialization, causing an `AttributeError`.
*   **Dynamic Import:** An import statement executed inside a function or method rather than at the top of the file, used to defer module loading and break circular dependencies.
*   **DeprecationWarning:** A built-in exception category used with the `warnings` module to signal that an API is changing or slated for removal.
*   **stacklevel:** An argument passed to `warnings.warn` that dictates how far up the call stack to attribute the warning (e.g., pointing to the caller's code instead of the utility function).
*   **Gradual Typing:** The practice of incrementally adding static type hints to a Python codebase using the `typing` module.
*   **Forward Reference:** Using a type hint for a class before it is fully defined in the file, requiring `from __future__ import annotations`.

# @Objectives
*   Establish reproducible, conflict-free development and production environments.
*   Produce robust, standardized, and immediately accessible documentation for all code components.
*   Architect strict, stable, and predictable API boundaries using packages and explicit namespace exports.
*   Insulate API consumers from internal implementation details and bugs using modular exception hierarchies.
*   Handle codebase evolution safely through programmatic warnings and deprecation notices.
*   Obviate runtime errors by employing rigorous static type analysis without sacrificing Python's dynamic flexibility.

# @Guidelines

## Dependency and Environment Management
*   The AI MUST recommend or utilize `python3 -m venv <name>` to isolate project environments.
*   The AI MUST instruct users to freeze dependencies using `python3 -m pip freeze > requirements.txt` and install them using `python3 -m pip install -r requirements.txt`.
*   The AI MUST search for and suggest utilizing community-built modules from PyPI (using `pip`) when solving complex, non-domain-specific tasks rather than reinventing the wheel.

## Documentation (Docstrings)
*   The AI MUST write docstrings for EVERY module, class, and public function/method.
*   **Modules:** The first line MUST be a single sentence describing the purpose. Subsequent paragraphs MUST detail operation, highlight important classes/functions, and (if applicable) provide command-line usage.
*   **Classes:** The first line MUST describe the purpose. Subsequent paragraphs MUST highlight public attributes, subclassing guidance, and protected attribute interactions.
*   **Functions/Methods:** The first line MUST describe the behavior. Subsequent paragraphs MUST document arguments (`*args`, `**kwargs`), default values, return values, and deliberately raised exceptions.
*   **Generator Functions:** The docstring MUST describe what the generator yields.
*   **Coroutines (async):** The docstring MUST explain when the execution stops/yields control.
*   **Type Hint Redundancy:** The AI MUST NOT duplicate type information in the docstring if it is already provided via `typing` annotations in the function signature.

## Packages and Module Organization
*   The AI MUST organize growing codebases into packages using `__init__.py`.
*   The AI MUST define explicit public APIs for packages by assigning a list of public names to the `__all__` attribute.
*   The AI MUST hide internal implementation details by omitting them from `__all__` and prefixing their names with a single underscore `_`.
*   The AI MUST expose stable package APIs by importing public names into the `__init__.py` file and extending `__all__` accordingly.
*   The AI MUST NOT use wildcard imports (`from module import *`). Imports MUST be explicit. If namespaces conflict, the AI MUST use the `as` clause (`import foo as bar`) or absolute module paths.

## Environment-Specific Configuration
*   The AI MUST utilize module-scoped `if` statements (e.g., `if __main__.TESTING:` or `if sys.platform == ...:`) to dynamically switch class or function definitions at import time based on the deployment environment.

## Exception Hierarchies
*   The AI MUST define a root exception (`class Error(Exception): pass`) for every module/API it designs.
*   All custom exceptions raised by the module MUST inherit from this root exception.
*   If the API is broad, the AI MUST define intermediate root exceptions (e.g., `class DatabaseError(Error): pass`) to group related error types.
*   The AI MUST use `logging.exception('msg')` inside `except` blocks to log the full stack trace of caught exceptions.

## Breaking Circular Dependencies
*   When a mutual interdependence causes an `AttributeError` at import, the AI MUST prioritize refactoring the shared state/dependency into a distinct, bottom-level module.
*   If refactoring is not feasible, the AI MUST break the cycle using a Dynamic Import (placing the `import` statement inside the calling function/method).
*   Alternatively, the AI MUST employ the Import/Configure/Run pattern, where modules only define structures at import time, and an explicit `configure()` function resolves cross-module references afterward.
*   The AI MUST NOT move imports to the bottom of the file to solve circular dependencies, as this violates PEP 8.

## API Deprecation and Warnings
*   When refactoring an API (e.g., changing argument requirements), the AI MUST use the `warnings.warn` function with `DeprecationWarning` to notify callers.
*   The AI MUST set the `stacklevel` parameter in `warnings.warn` (usually `stacklevel=2` or `3`) to ensure the warning points to the offending caller's code, not the internal helper function generating the warning.
*   In production code configurations, the AI MUST replicate warnings to the logging system using `logging.captureWarnings(True)`.
*   When writing tests for deprecations, the AI MUST use `warnings.catch_warnings(record=True)` as a context manager to verify that warnings are emitted correctly.

## Static Analysis and Typing
*   The AI MUST apply type hints (`typing` module) to variables, fields, functions, and methods, especially at API boundaries.
*   The AI MUST include `from __future__ import annotations` at the top of files to prevent `NameError` exceptions when utilizing forward references in type hints.
*   The AI MUST use `typing.Optional` when a variable can be `None`, forcing explicit null-checks in the logic.
*   The AI MUST NOT treat exceptions as part of the formal type signature; exception raising MUST be verified via unit tests, not static type analysis.

# @Workflow
1.  **Environment Setup:** Define the virtual environment and `requirements.txt` before writing application code.
2.  **API Abstraction:** Define the module layout. Create `__init__.py` files. Create a base `Error(Exception)` class for the package.
3.  **Implementation & Typing:** Write functions/classes using `typing` annotations and `from __future__ import annotations`. Avoid circular dependencies by refactoring shared state to the bottom of the dependency tree.
4.  **Documentation:** Write PEP 257 compliant docstrings. Ensure no redundancy exists between docstring text and type annotations.
5.  **API Finalization:** Populate `__all__` lists in submodules and aggregate them in the package's `__init__.py` to freeze the public interface. Prefix internal functions with `_`.
6.  **Migration/Deprecation:** If modifying an existing API, add `warnings.warn` with `stacklevel=3` to alert downstream consumers of deprecations before removing old functionality.
7.  **Validation:** Instruct the user to run `mypy --strict` to enforce type safety and run `python -W error` during testing to catch unresolved warnings.

# @Examples (Do's and Don'ts)

## Docstrings and Type Annotations
**[DO]** Use type annotations and omit redundant parameter type descriptions in the docstring.
```python
from typing import List

def find_anagrams(word: str, dictionary: List[str]) -> List[str]:
    """Find all anagrams for a given word.
    
    Args:
        word: Target word to match.
        dictionary: All known actual words to check against.
        
    Returns:
        Anagrams that were found.
    """
    pass
```

**[DON'T]** Duplicate type information in the docstring when using type annotations.
```python
from typing import List

def find_anagrams(word: str, dictionary: List[str]) -> List[str]:
    """Find all anagrams for a given word.
    
    Args:
        word: String of the target word.
        dictionary: List of strings representing all known actual words.
        
    Returns:
        List of strings representing anagrams that were found.
    """
    pass
```

## Package API Definitions
**[DO]** Expose a stable API using `__all__` in `__init__.py`.
```python
# mypackage/__init__.py
__all__ = []
from .models import *
__all__ += models.__all__

# mypackage/models.py
__all__ = ['Projectile']

class Projectile:
    pass

def _internal_helper():
    pass
```

**[DON'T]** Use wildcard imports in consumer code or fail to define `__all__`.
```python
# api_consumer.py
from mypackage.models import * # Bad: Obscures namespaces and imports everything
```

## Exception Hierarchies
**[DO]** Define a root exception to insulate callers.
```python
class Error(Exception):
    """Base-class for all exceptions raised by this module."""

class InvalidDensityError(Error):
    """A provided density value was invalid."""

def calculate(density):
    if density < 0:
        raise InvalidDensityError('Density must be positive')
```

**[DON'T]** Raise generic built-in exceptions for API-specific domain logic.
```python
def calculate(density):
    if density < 0:
        raise ValueError('Density must be positive') # Bad: Hard for callers to isolate from other ValueErrors
```

## Breaking Circular Dependencies
**[DO]** Use a dynamic import to break an unavoidable circular dependency.
```python
# dialog.py
class Dialog:
    pass

save_dialog = Dialog()

def show():
    import app # Dynamic import breaks the cycle
    save_dialog.save_dir = app.prefs.get('save_dir')
```

**[DON'T]** Reorder imports to the bottom of the file.
```python
# app.py
class Prefs:
    pass
prefs = Prefs()

import dialog # Bad: Violates PEP 8 and creates brittle file structures
dialog.show()
```

## Deprecation Warnings
**[DO]** Use `stacklevel` to point to the caller when issuing a warning.
```python
import warnings

def print_distance(speed, duration, *, speed_units=None):
    if speed_units is None:
        warnings.warn(
            'speed_units will be required soon, update your code',
            DeprecationWarning,
            stacklevel=2
        )
        speed_units = 'mph'
    pass
```

**[DON'T]** Call `warnings.warn` without a `stacklevel` (defaults to 1), which confusingly blames the API's internal source file instead of the caller.
```python
import warnings

def print_distance(speed, duration, *, speed_units=None):
    if speed_units is None:
        warnings.warn('speed_units required', DeprecationWarning) # Bad: Blames this line instead of the user's code
        speed_units = 'mph'
```

## Forward References in Type Hints
**[DO]** Use `from __future__ import annotations` to evaluate type hints lazily.
```python
from __future__ import annotations

class FirstClass:
    def __init__(self, value: SecondClass) -> None:
        self.value = value

class SecondClass:
    pass
```

**[DON'T]** Rely on string literals for forward references unless restricted to an older Python version.
```python
class FirstClass:
    def __init__(self, value: 'SecondClass') -> None: # Fragile and visually noisy
        self.value = value

class SecondClass:
    pass
```