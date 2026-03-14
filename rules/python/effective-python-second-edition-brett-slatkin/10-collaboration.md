@Domain
Python API Design, Collaboration, Codebase Organization, Dependency Management, Documentation, and Static Analysis. These rules trigger whenever the AI is tasked with creating or modifying Python APIs, documenting code, resolving circular imports, deprecating old code, managing environment dependencies, structuring Python packages, or applying type annotations.

@Vocabulary
- **PyPI (Python Package Index):** The central repository for community-built Python modules.
- **pip:** The standard command-line tool for installing packages.
- **venv:** The built-in module for creating isolated, reproducible Python environments.
- **Dependency Hell:** System breakage caused by conflicting transitive dependencies of globally installed packages.
- **Docstring:** A string literal (`"""`) that occurs as the first statement in a module, function, class, or method definition.
- **Package:** A directory containing an `__init__.py` file, used to group related modules and provide namespaces.
- **__all__:** A special module-level list attribute that defines the strict, stable public API of a package or module.
- **Wildcard Import:** The anti-pattern of using `from module import *`.
- **Deployment Environment:** A specific configuration under which a program runs (e.g., production, development, testing).
- **Root Exception:** A base exception class specifically defined for a single module or API, from which all other exceptions in that module inherit.
- **Intermediate Root Exception:** A base exception class for a specific functional area within a module, sitting between the root exception and specific exceptions.
- **Circular Dependency:** An error occurring when two modules must call into each other at import time, resulting in an `AttributeError`.
- **Dynamic Import:** An `import` statement placed inside a function or method rather than at the top level of a module, used to delay module initialization.
- **Gradual Typing:** The practice of incrementally adding type annotations to a Python codebase using the `typing` module.
- **Forward Reference:** A type annotation that refers to a class that has not yet been fully defined.

@Objectives
- Ensure code is modular, strictly isolated, and reproducible across different developers' machines.
- Maintain comprehensive, self-documenting codebases where intentions and interfaces are explicitly clear.
- Provide robust, backward-compatible, and well-insulated APIs to downstream consumers.
- Gracefully deprecate outdated usage without immediately breaking downstream code.
- Prevent runtime bugs proactively through architectural organization and static type checking.

@Guidelines

**1. Dependency Management (Items 82 & 83)**
- The AI MUST NEVER suggest or execute global package installations.
- The AI MUST always use `venv` to create isolated environments (`python3 -m venv <name>`).
- The AI MUST execute package installations using the explicit module invocation: `python3 -m pip install <package>`.
- The AI MUST reproduce environments using `python3 -m pip freeze > requirements.txt` and `python3 -m pip install -r requirements.txt`.
- The AI MUST NEVER attempt to move a virtual environment directory; it must instruct the user to recreate it.

**2. Documentation (Item 84)**
- The AI MUST write docstrings for every module, class, public function, and public method.
- **Module Docstrings:** The first line MUST be a single-sentence description. Subsequent paragraphs must detail the module's purpose, important classes/functions, and command-line usage.
- **Class Docstrings:** The first line MUST be a single-sentence description. Subsequent paragraphs must detail operation, public attributes, and guidance for subclasses regarding protected attributes.
- **Function/Method Docstrings:** The first line MUST be a single sentence. Must describe specific behaviors, arguments (`*args`, `**kwargs`), return values (omit if `None`), raised exceptions (and under what conditions), default values, and generator/coroutine behaviors.
- **Type Hint Integration:** If a function or method uses static type annotations, the AI MUST NOT duplicate the type information within the docstring.

**3. Packages and APIs (Item 85)**
- The AI MUST organize growing codebases into packages using `__init__.py`.
- To avoid namespace conflicts, the AI MUST use `import module as alias` or access names via their highest unique absolute module path.
- The AI MUST NEVER use wildcard imports (`from module import *`).
- For external-facing APIs, the AI MUST define an `__all__` list in the module or `__init__.py` to explicitly declare the public API. Internal functions must be hidden (e.g., prefix with `_` and omit from `__all__`).

**4. Deployment Environments (Item 86)**
- The AI MUST handle varying deployment environments by using module-scoped `if` statements (e.g., `if sys.platform.startswith('win32'):` or `if __main__.TESTING:`) to define names differently at startup.
- The AI MUST NOT hardcode heavy external assumptions (like database connections) if they can be bypassed for local testing using module-level conditional logic.

**5. Root Exceptions (Item 87)**
- The AI MUST define a custom root exception (e.g., `class Error(Exception): pass`) for every API module.
- All specific exceptions raised by the module MUST inherit from this root exception.
- The AI MUST utilize intermediate root exceptions to group related errors (e.g., `class WeightError(Error): pass`) to future-proof the API.
- The AI MUST NOT raise generic built-in exceptions (like `ValueError`) for domain-specific API errors.

**6. Circular Dependencies (Item 88)**
- The AI MUST resolve circular dependencies primarily by refactoring the mutual dependency into a new, separate module at the bottom of the dependency tree.
- If refactoring is not feasible, the AI MUST use a dynamic import (placing the `import` statement inside the function or method).
- The AI MUST NEVER move an `import` statement to the bottom of a file to fix a circular dependency (violates PEP 8).

**7. Deprecation and Warnings (Item 89)**
- When refactoring APIs (e.g., making optional arguments required), the AI MUST use the `warnings` module (`warnings.warn`) to notify callers programmatically.
- The AI MUST use the `stacklevel` parameter in `warnings.warn` so the warning points to the caller's code, not the API's internal code.
- The AI MUST configure tests to raise warnings as exceptions using `warnings.simplefilter('error')` or `-W error`.

**8. Static Analysis and Typing (Item 90)**
- The AI MUST apply type annotations (from the `typing` module) to variables, fields, functions, and methods, especially at API boundaries.
- The AI MUST use `Optional[Type]` when a value can be `None`.
- The AI MUST resolve forward references in type hints by adding `from __future__ import annotations` at the top of the file, rather than wrapping types in strings.
- The AI MUST recognize that exceptions are not part of Python's type hints and must be documented and tested separately.

@Workflow
1. **Dependency Check:** Whenever initiating a new project or script, ensure execution happens within a `venv` and dependencies are managed via `requirements.txt`.
2. **Interface Design:** Define the public surface area. Create an `__all__` list. Define a module-specific root exception.
3. **Implementation:** Write the logic. If varying environments are detected, use module-scoped `if` statements to handle configuration.
4. **Typing & Documentation:** Add strict type hints to function signatures. Write comprehensive `"""` docstrings omitting redundant type data.
5. **Refactoring/Dependency Resolution:** If a circular import occurs, extract the shared state into a base module. If impossible, use a dynamic import inside the consuming function.
6. **Deprecation:** If altering an existing API's signature, implement `warnings.warn` with the appropriate `stacklevel` for deprecated usage.

@Examples (Do's and Don'ts)

**[DO] Combine Type Hints and Docstrings Efficiently**
```python
from typing import List, Container

def find_anagrams(word: str, dictionary: Container[str]) -> List[str]:
    """Find all anagrams for a word.
    
    This function evaluates membership in the provided dictionary.
    
    Args:
        word: The target word to check.
        dictionary: All known actual words.
        
    Returns:
        Anagrams that were found.
    """
    pass
```

**[DON'T] Duplicate Type Info in Docstrings**
```python
def find_anagrams(word: str, dictionary: Container[str]) -> List[str]:
    """
    Args:
        word (str): The target word.
        dictionary (Container[str]): All known actual words.
        
    Returns:
        List[str]: Anagrams that were found.
    """
    pass
```

**[DO] Use Root and Intermediate Exceptions**
```python
class MyModuleError(Exception):
    """Root exception for this module."""

class CalculationError(MyModuleError):
    """Intermediate exception for math errors."""

class InvalidDensityError(CalculationError):
    """Raised when density is negative."""
```

**[DON'T] Raise Generic Exceptions for API Errors**
```python
def calculate_density(volume, mass):
    if volume <= 0:
        raise ValueError("Volume must be positive") # Hard for callers to isolate
```

**[DO] Handle Circular Imports with Dynamic Imports**
```python
class Dialog:
    def show(self):
        import app  # Dynamic import avoids circular dependency at startup
        self.save_dir = app.prefs.get('save_dir')
```

**[DON'T] Handle Circular Imports by Moving Imports to the Bottom**
```python
class Dialog:
    pass

import app  # Violates PEP 8 and creates brittle initialization
```

**[DO] Use `__future__` for Forward References**
```python
from __future__ import annotations

class Node:
    def __init__(self, parent: Node) -> None:
        self.parent = parent
```

**[DON'T] Use Strings for Forward References (Unless strictly required by older Python versions)**
```python
class Node:
    def __init__(self, parent: 'Node') -> None:
        self.parent = parent
```

**[DO] Issue Context-Aware Warnings**
```python
import warnings

def calculate(speed, distance, units=None):
    if units is None:
        warnings.warn('units will be required soon', DeprecationWarning, stacklevel=2)
        units = 'metric'
    return speed * distance
```