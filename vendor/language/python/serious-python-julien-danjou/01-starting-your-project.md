@Domain
This rule file is triggered when the AI is tasked with initializing, structuring, or scaffolding a new Python project, defining or updating Python package version numbers, configuring project layouts, generating boilerplate code, setting up testing hierarchies, or implementing code style/linting configurations (e.g., Flake8, PEP 8 compliance).

@Vocabulary
- **PEP 8**: The standard style guide for Python code formatting.
- **PEP 440**: The official specification for Python version numbering, establishing a universally accepted regex format.
- **Semantic Versioning (SemVer)**: A versioning scheme that overlaps with PEP 440 but contains incompatible prerelease syntaxes (e.g., `-alpha`). Not to be used strictly in Python.
- **Pyflakes**: A static analysis tool that checks Python source files for actual coding errors.
- **Pylint**: A linter that checks for both PEP 8 conformance and coding errors.
- **pep8**: The command-line tool used to check PEP 8 compliance.
- **flake8**: A combined tool that bundles Pyflakes, pep8, and complexity checks, extensible via plugins.
- **DVCS (Distributed Version Control System)**: Systems like Git or Mercurial, which should not be used to generate raw package version hashes (as they are not orderable).

@Objectives
- Ensure all newly scaffolded Python projects follow a logical, future-proof, and feature-based directory structure.
- Enforce strict adherence to PEP 440 for all package versions, rejecting non-compliant formats like pure Semantic Versioning or date-based versioning.
- Implement strict PEP 8 code formatting standards across all generated Python code.
- Prevent the AI from generating common architectural anti-patterns, such as type-based module naming (e.g., `functions.py`) or improperly placed test directories.
- Automate style and error checking requirements by defaulting to `flake8` for all project configurations.

@Guidelines

**Python Version Targeting:**
- The AI MUST target Python 3 (specifically Python 3.6 or later) for all code generation and project setups.
- The AI MUST NOT generate code for Python 2.x, 2.6, or 2.7 unless explicitly commanded by the user for legacy "archeology" purposes.

**Project Layout and Architecture:**
- When scaffolding a project, the AI MUST use a balanced hierarchy: neither too deep (a nightmare to navigate) nor too flat (bloated).
- The AI MUST place unit tests *inside* a subpackage of the main software package directory (e.g., `my_package/tests/`). The AI MUST NOT place unit tests in a top-level `tests/` directory outside the package, as setuptools might accidentally install it as a global `tests` module.
- The AI MUST create the following standard root files: `setup.py`, `setup.cfg`, and a `README.rst` (or `.md`/`.txt`).
- The AI MUST place documentation in a root `docs/` directory formatted for Sphinx (reStructuredText).
- The AI MUST place shell scripts in a `tools/` directory, binary installed scripts in a `bin/` directory, and sample configurations in an `etc/` directory if these assets are requested.

**Module Organization (Anti-Patterns to Avoid):**
- The AI MUST organize files and modules based on *features*, NOT on *types*.
- The AI MUST NOT create files named `functions.py`, `exceptions.py`, or `classes.py`. Functional areas must be confined to feature-specific files.
- The AI MUST NOT create a directory that contains only an `__init__.py` file (unnecessary nesting). If a directory is created, it must contain multiple related `.py` files. Otherwise, a single `.py` file must be used instead of a directory.
- The AI MUST leave `__init__.py` files empty by default to avoid unwanted execution side effects, unless explicitly instructed otherwise. The AI MUST NOT delete `__init__.py` entirely, as Python requires it to recognize submodules.

**Version Numbering Constraints (PEP 440):**
- When generating or updating package versions, the AI MUST strictly follow the PEP 440 regular expression format: `N[.N]+[{a|b|c|rc}N][.postN][.devN]`.
- The AI MUST treat versions like `1.2` as equivalent to `1.2.0`.
- The AI MUST NOT use date-based versioning schemes (e.g., `2013.06.22`). Versions starting with numbers `>= 1980` must be rejected as invalid.
- The AI MUST NOT use strictly Semantic Versioning prerelease tags that use hyphens or plus signs (e.g., `1.0.0-alpha+001`).
- The AI MUST NOT use Git or DVCS identifying hashes as package versions because they are not orderable.
- For Pre-releases, the AI MUST use `aN` for alpha, `bN` for beta, and `cN` or `rcN` for release candidates (noting that `rc` releases are considered newer than `c` releases if both are present).
- For Post-releases, the AI MUST use `.postN` only to address minor publication errors (e.g., release note fixes). The AI MUST NOT use `.postN` for bug-fix versions; bug fixes require incrementing the minor version number.
- The AI SHOULD avoid generating developmental `.devN` suffixes by default, as they are harder for humans to parse, unless specifically requested.

**Coding Style (PEP 8):**
- The AI MUST use exactly four (4) spaces per indentation level.
- The AI MUST limit all lines to a maximum of 79 characters.
- The AI MUST separate top-level function and class definitions with exactly two (2) blank lines.
- The AI MUST encode all files using ASCII or UTF-8.
- The AI MUST use one module import per `import` statement and per line.
- The AI MUST place all import statements at the top of the file (after comments and docstrings).
- The AI MUST group imports in the following strict order: 1) Standard library, 2) Third-party, 3) Local library.
- The AI MUST NOT use extraneous whitespaces inside parentheses, square brackets, or braces, or before commas.
- The AI MUST name classes using `CamelCase`.
- The AI MUST suffix exception classes with `Error` (if applicable).
- The AI MUST name functions and methods using lowercase with words separated by underscores (`separated_by_underscores`).
- The AI MUST use a leading underscore for private attributes or methods (e.g., `_private`).

**Linting and Automated Checks:**
- When scaffolding CI/CD or project configs, the AI MUST include configuration for `flake8` as the primary static analysis and style-checking tool.
- The AI SHOULD include the `flake8-import-order` plugin configuration to enforce alphabetical sorting of imports.
- The AI MUST only use `# noqa` to ignore checks on a specific line when absolutely necessary and justifiable.

@Workflow
When tasked with starting a new Python project or refactoring an existing layout, the AI must execute the following algorithmic steps:

1. **Verify Environment:** Confirm the target Python version is 3.6+ and establish PEP 8 as the default formatting rule.
2. **Scaffold the Root Directory:** Generate standard files including `setup.py`, `setup.cfg`, and a `README.rst`.
3. **Establish Top-Level Folders:** Create `docs/` for documentation, and conditionally create `etc/`, `tools/`, or `bin/` based on project requirements.
4. **Create the Package Structure:** Create the main source package directory using feature-based nomenclature. Ensure `__init__.py` files are present but empty.
5. **Implement the Testing Hierarchy:** Create a `tests/` directory *inside* the main package directory. DO NOT place it at the root of the project.
6. **Set Version Numbers:** Ensure the version string in `setup.cfg` or `__init__.py` strictly validates against PEP 440 (e.g., `1.0.0`).
7. **Configure Linting:** Generate a `tox.ini` or `.flake8` file enforcing 79-character line limits and other PEP 8 standards.

@Examples (Do's and Don'ts)

**Project Structure and Layout:**
- [DO]
  ```text
  my_project/
  ├── setup.py
  ├── setup.cfg
  ├── README.rst
  ├── docs/
  └── my_package/
      ├── __init__.py
      ├── authentication.py
      ├── database.py
      └── tests/
          ├── __init__.py
          ├── test_authentication.py
          └── test_database.py
  ```
- [DON'T] (Placing tests at the root, and using type-based module names)
  ```text
  my_project/
  ├── setup.py
  ├── tests/                  <-- WRONG: External tests directory
  │   └── test_all.py
  └── my_package/
      ├── __init__.py
      ├── exceptions.py       <-- WRONG: Type-based module
      ├── functions.py        <-- WRONG: Type-based module
      └── classes.py          <-- WRONG: Type-based module
  ```

**Version Numbering:**
- [DO] Use PEP 440 compliant strings.
  - `1.2.0` (Final release)
  - `2.3.1b2` (Beta 2 of version 2.3.1)
  - `0.4rc1` (Release candidate 1)
  - `1.4.post2` (Post-release addressing a publication error)
- [DON'T] Use non-compliant strings.
  - `1.0.0-alpha+001` (WRONG: Strict SemVer format not allowed)
  - `2019.12.01` (WRONG: Date-based format)
  - `1.2-bugfix` (WRONG: Invalid suffix string)
  - `e8a7b4c` (WRONG: Git hash is not orderable)

**Module Organization:**
- [DO] Create a single file `hooks.py` if the functional area requires only a few classes and functions.
- [DON'T] Create a directory `hooks/` containing solely an `__init__.py` file.

**Imports and Formatting:**
- [DO]
  ```python
  import os
  import sys

  import requests

  import my_local_module
  ```
- [DON'T] (Multiple imports on one line, unordered, bad whitespace)
  ```python
  import sys, os, my_local_module, requests

  def my_func( arg1 , arg2 ):   # WRONG: Extraneous spaces
      pass
  ```