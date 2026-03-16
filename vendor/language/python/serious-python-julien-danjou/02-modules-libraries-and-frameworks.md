@Domain
Python module management, dependency installation, system imports, library and framework architecture, and API design. Triggered when writing or refactoring Python code, managing `sys.path`, adding external dependencies via `pip`, building custom file importers, or structuring large applications.

@Vocabulary
- **`__import__`**: The internal function wrapped by the `import` keyword, used to import a module whose name is unknown beforehand.
- **`sys.modules`**: A standard Python dictionary containing all currently loaded modules, keyed by module name.
- **`sys.builtin_module_names`**: A list of modules compiled directly into the Python interpreter.
- **`sys.path`**: A list of directory paths Python iterates over to find requested modules.
- **Import Hook Mechanism (PEP 302)**: The standard allowing developers to modify how Python imports modules using meta path finders and path entry finders.
- **Meta Path Finder**: An object used with `sys.meta_path` that exposes a `find_module(fullname, path=None)` method to return a loader object.
- **Loader Object**: An object returned by a meta path finder that implements a `load_module(fullname)` method responsible for compiling and returning a module object to the Python interpreter.
- **API Wrapper**: A custom abstraction layer encapsulating external library logic to keep third-party hooks out of the main source code.
- **`egg-link`**: A file placed in the distribution path by `pip install -e` that points to a local source directory, bypassing the need to copy files during development.
- **Framework vs. Library**: A library is an add-on called by the application, whereas a framework forms the chassis of the application (the application extends the framework).

@Objectives
- Safely and dynamically manage module imports without shadowing standard libraries.
- Extend the Python import system correctly using PEP 302 when non-standard file extensions (e.g., `.hy`) need to be imported as modules.
- Exhaustively leverage the Python Standard Library before considering custom implementations or external dependencies.
- Isolate external libraries using custom API wrappers to prevent vendor lock-in and minimize refactoring if the dependency becomes obsolete.
- Utilize `pip` developer modes for efficient local package testing and VCS repository integration.
- Design library APIs top-down using the Single Responsibility Principle, and write idiomatic, high-performance Python per core developer standards.

@Guidelines
- **Dynamic Imports**: When a module's name is only known at runtime, the AI MUST use the `__import__("MODULE_NAME".lower())` function.
- **Path Management**: The AI MUST NOT shadow Python built-in modules. Never create a local file with the same name as a standard library module (e.g., `random.py`), as the current directory is searched before the Standard Library directory.
- **Custom Importers**: When teaching Python to import custom file types, the AI MUST implement a custom Meta Path Finder containing `find_module` and a Meta Loader containing `load_module`, then append the finder to `sys.meta_path`.
- **Standard Library First**: Before writing basic utility functions or adding external dependencies, the AI MUST check the Standard Library. Required mappings:
  - For exit functions: `atexit`
  - For CLI parsing: `argparse`
  - For bisection/sorting: `bisect`
  - For deep/shallow copies: `copy`
  - For time/date: `datetime`, `calendar`
  - For pattern matching paths/files: `glob`, `fnmatch`
  - For memory streams: `io`
  - For basic operators (to avoid lambda): `operator`
  - For event scheduling: `sched`
  - For temporary files: `tempfile`
  - For unique IDs: `uuid`
  - For defining extension APIs: `abc`
  - For holding data without logic: `collections.namedtuple`
  - For stackable namespaces: `collections.ChainMap`
- **External Library Safety Checklist**: The AI MUST evaluate external dependencies against these criteria before implementation:
  1. Python 3 compatibility.
  2. Active development and maintenance (check response times to bugs).
  3. Packaged with major OS distributions.
  4. API compatibility commitment.
  5. License compatibility.
- **API Wrappers (Encapsulation)**: The AI MUST NOT allow external libraries to deeply hook into the core source code. The AI MUST create a proprietary API wrapper that encapsulates the external library. If the library must be replaced, only the wrapper should change.
- **Framework Selection**: The AI MUST weigh framework lock-in. Prefer lighter frameworks (e.g., Flask) that do less over heavier frameworks (e.g., Django) if you wish to avoid fighting framework-imposed design constraints in the future.
- **Pip Usage**: 
  - To avoid polluting OS directories, use `pip install --user`.
  - For local active development of a package, use `pip install -e .` to create an `egg-link`.
  - For depending on unreleased versions from VCS, use `pip install -e git+https://[url]#egg=[name]`.
- **Top-Down API Design**: When designing an API, the AI MUST apply the Single Responsibility Principle at each layer. Separate the implementation details from the public API code.
- **Idiomatic Coding (Code Review Rules)**:
  - Convert filtering loops (using `append()`) into generator expressions.
  - Use `itertools.chain()` to process combined lists rather than manually concatenating them.
  - Replace long `if/elif/else` blocks with a `dict()` lookup table.
  - Ensure functions ALWAYS return the same type of object (e.g., return an empty list `[]` instead of `None`).
  - Reduce function argument counts by combining related values into a `tuple` or a new class.
  - Use explicitly defined classes for public APIs instead of relying on dictionaries.

@Workflow
1. **Dependency Verification**: Check if the required functionality exists in the Python Standard Library. If yes, import and use it.
2. **External Evaluation**: If an external library is required, perform the Safety Checklist. 
3. **Encapsulation**: Create a standalone Python file/module to serve as an API wrapper for the external library.
4. **Implementation**: Build the feature using the API wrapper. Apply idiomatic rules: use generator expressions, dict lookups, and `itertools`.
5. **Development Installation**: Instruct the user to use `pip install -e .` if they are installing a local package for testing.

@Examples (Do's and Don'ts)

**Principle: Dynamic Imports**
- [DO] 
```python
module_name = "random"
dynamic_module = __import__(module_name)
```
- [DON'T] Use `exec` or `eval` to perform imports of dynamic strings.

**Principle: Shadowing Built-ins**
- [DO] Name a custom utility file `rand_utils.py` or `app_random.py`.
- [DON'T] Name a file `random.py` or `os.py` in the root directory, which overrides standard libraries.

**Principle: API Encapsulation**
- [DO] 
```python
# db_wrapper.py
import external_orm_library

class DatabaseAPI:
    def get_user(self, user_id):
        return external_orm_library.fetch(user_id)
```
- [DON'T] Import `external_orm_library` in every single business logic file across the codebase.

**Principle: Conditional Logic vs Lookup Tables**
- [DO]
```python
# Using a dict lookup table
operations = {
    'add': lambda x, y: x + y,
    'sub': lambda x, y: x - y,
    'mul': lambda x, y: x * y
}
result = operations.get(action, default_func)(a, b)
```
- [DON'T]
```python
# Long if/elif/else block
if action == 'add':
    result = a + b
elif action == 'sub':
    result = a - b
elif action == 'mul':
    result = a * b
```

**Principle: Filtering Iterables**
- [DO]
```python
# Using a generator expression
filtered_data = (item for item in raw_data if item.is_valid)
```
- [DON'T]
```python
# Anti-pattern: for-loop appending to a new list
filtered_data = []
for item in raw_data:
    if item.is_valid:
        filtered_data.append(item)
```

**Principle: Consistent Return Types**
- [DO]
```python
def find_matches(query):
    if not query:
        return [] # Returns empty list, consistent type
    return [match for match in data if query in match]
```
- [DON'T]
```python
def find_matches(query):
    if not query:
        return None # Inconsistent, caller must now check for None
    return [match for match in data if query in match]
```