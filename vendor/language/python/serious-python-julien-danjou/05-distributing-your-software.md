@Domain
Python project distribution, library packaging, PyPI publication, dynamic feature discovery, application extensibility (plugins/drivers), and executable console script creation. Trigger these rules when generating `setup.py`, `setup.cfg`, publishing packages, or implementing plugin architectures.

@Vocabulary
*   **distutils**: The legacy standard library packaging tool. Deprecated for complex tasks; do not use for modern packaging.
*   **setuptools**: The de facto standard library for advanced package installations, dependency handling, and distribution.
*   **distribute**: A deprecated fork of setuptools that has been merged back into setuptools.
*   **distutils2 / packaging**: Abandoned projects intended to replace distutils.
*   **setup.py**: The standard Python installation script, which should be kept minimal.
*   **setup.cfg**: A plaintext declarative file that stores package metadata, configuration, and entry points, making it easier for external tools to read.
*   **pbr (Python Build Reasonableness)**: An extension for setuptools that automates documentation, changelogs, file lists, and version management via git tags.
*   **Wheel (.whl)**: The PEP 427 standard Python distribution package format. A zip file with a specific extension that does not require execution during installation.
*   **manylinux1**: A platform tag (PEP 513) guaranteeing binary wheels work across various Linux distributions.
*   **PyPI (Python Package Index)**: The central repository for Python packages.
*   **testpypi**: The PyPI staging server used exclusively for safely testing the publishing process.
*   **~/.pypirc**: The configuration file storing credentials and index servers for PyPI uploads.
*   **Entry Points**: A mechanism in setuptools allowing packages to advertise dynamic features, executable scripts, or plugins for other programs to discover.
*   **console_scripts**: A specific entry point group used to automatically generate cross-platform executable scripts for Python functions.
*   **pkg_resources**: A Python library used to parse, discover, and load entry points at runtime.
*   **stevedore**: A library that abstracts and simplifies the discovery and loading of dynamic plugins using entry points.
*   **epi (entry-point-inspector)**: A CLI tool to visualize and inspect entry points installed on a system.

@Objectives
*   Transition packaging configuration from procedural code (`setup.py`) to declarative metadata (`setup.cfg`).
*   Automate build steps (versioning, manifests) using `pbr` where applicable.
*   Distribute software strictly via the Wheel format, utilizing universal wheels for multi-version support.
*   Guarantee safe release practices by mandating the use of a testing sandbox (`testpypi`) before production publication.
*   Eliminate manual, error-prone shell scripts in favor of automatically generated cross-platform `console_scripts`.
*   Establish decoupled, extensible software architectures by utilizing Entry Points and the `stevedore` package for plugin and driver management.

@Guidelines
*   **Packaging Tool Selection:** The AI MUST use `setuptools`. The AI MUST NEVER use `distutils`, `distribute`, or `distutils2` for managing package installations.
*   **Declarative Metadata:** The AI MUST place all packaging metadata (name, version, author, description, classifiers) inside `setup.cfg`. The `setup.py` file MUST be restricted to a bare minimum stub (e.g., `import setuptools; setuptools.setup()`).
*   **Build Reasonableness (pbr):** When setting up a new package, the AI SHOULD suggest and configure `pbr` (`setup_requires=['pbr'], pbr=True` in `setup.py` and `[pbr]` section in `setup.cfg`) to automate versioning and changelog generation from git history.
*   **Wheel Format Constraint:** The AI MUST generate distributions using the Wheel format (`python setup.py bdist_wheel`). If the code is compatible with both Python 2 and 3, the AI MUST configure the wheel as universal (via the `--universal` CLI flag or `universal=1` inside the `[wheel]` section of `setup.cfg`).
*   **Publishing Sandbox Constraint:** When providing instructions or scripts for publishing packages, the AI MUST explicitly use the PyPI staging server (`testpypi`) first. The AI MUST instruct the user to configure `~/.pypirc` with a `[testpypi]` block.
*   **Executable Scripts Constraint:** The AI MUST NOT create manual executable wrapper scripts (e.g., in a `bin/` directory) for launching applications. Instead, the AI MUST use the `console_scripts` entry point to map shell commands directly to Python functions.
*   **Plugin Architecture Constraint:** When asked to create an extensible application, a hook system, or a driver-based architecture, the AI MUST use setuptools Entry Points.
*   **Plugin Management Library:** To load and manage entry points dynamically, the AI MUST use the `stevedore` library (e.g., `ExtensionManager` or `DriverManager`) rather than manually iterating with `pkg_resources`.

@Workflow
When tasked with configuring a Python project for distribution, follow this algorithmic process:

1.  **Initialize Declarative Config:**
    *   Create a `setup.cfg` file.
    *   Populate the `[metadata]` section with project details (name, author, license, url, classifiers).
2.  **Generate setup.py Stub:**
    *   Create `setup.py`.
    *   Include only `import setuptools` and `setuptools.setup()`.
    *   If `pbr` is requested, modify `setup()` to include `setup_requires=['pbr'], pbr=True`.
3.  **Define Entry Points (if applicable):**
    *   If the application requires an executable CLI, add an `[entry_points]` section to `setup.cfg`.
    *   Add `console_scripts =` followed by `command_name = module.path:function_name`.
    *   If the application exposes a plugin architecture, define a custom entry point group (e.g., `myapp.plugins =`).
4.  **Configure Wheel:**
    *   If the code is purely Python and Python 2/3 compatible, add a `[wheel]` section to `setup.cfg` with `universal=1`.
5.  **Build Phase:**
    *   Instruct the execution of `python setup.py sdist` (for source) and `python setup.py bdist_wheel` (for built format).
6.  **Staging Release Phase:**
    *   Instruct the user to define `testpypi` in `~/.pypirc`.
    *   Instruct the execution of the upload to the test server: `python setup.py register -r testpypi` followed by `python setup.py bdist_wheel upload -r testpypi`.
    *   Instruct the user to verify the installation via `pip install -i https://testpypi.python.org/pypi <package>`.

@Examples (Do's and Don'ts)

**Principle: Project Metadata Configuration**
*   [DO] Use `setup.cfg` for metadata and leave `setup.py` as a minimal stub.
    ```python
    # setup.py
    import setuptools
    setuptools.setup()
    ```
    ```ini
    # setup.cfg
    [metadata]
    name = my_package
    author = John Doe
    description = file: README.rst
    ```
*   [DON'T] Stuff all metadata into a monolithic, procedural `setup.py` using legacy distutils.
    ```python
    # setup.py
    from distutils.core import setup
    setup(name="my_package", author="John Doe") # ANTI-PATTERN
    ```

**Principle: Creating Executable Scripts**
*   [DO] Use `console_scripts` in `setup.cfg` to generate cross-platform executables automatically.
    ```ini
    # setup.cfg
    [entry_points]
    console_scripts =
        my_cli = my_package.cli:main
    ```
*   [DON'T] Create a custom bash or python script in a `bin/` folder that manually manipulates `sys.path`.
    ```python
    #!/usr/bin/python
    # bin/my_cli  (ANTI-PATTERN)
    import sys
    import my_package
    my_package.cli.main(sys.argv)
    ```

**Principle: Building Plugin Architectures**
*   [DO] Use `stevedore` to cleanly load registered entry points without boilerplate.
    ```python
    from stevedore.extension import ExtensionManager

    def load_plugins():
        extensions = ExtensionManager('my_package.plugins', invoke_on_load=True)
        for ext in extensions:
            ext.obj.do_work()
    ```
*   [DON'T] Write manual, error-prone loops using `pkg_resources` to handle plugin loading unless strictly necessary.
    ```python
    import pkg_resources

    def load_plugins():
        for ep in pkg_resources.iter_entry_points('my_package.plugins'):
            try:
                plugin = ep.load()
                plugin().do_work()
            except Exception:
                pass # ANTI-PATTERN: Manual error handling and loading
    ```

**Principle: Publishing Workflow**
*   [DO] Upload to the PyPI staging server to verify metadata and packaging before a public release.
    ```bash
    python setup.py bdist_wheel upload -r testpypi
    ```
*   [DON'T] Blindly upload the first draft of a package straight to the production PyPI server.
    ```bash
    python setup.py sdist upload # ANTI-PATTERN: Direct production upload
    ```