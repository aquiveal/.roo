# @Domain
Python development tasks involving cross-version compatibility (Python 2 and Python 3), method dispatching, resource management refactoring, and class definition simplification. These rules trigger whenever the AI is tasked with porting code, abstracting class methods, writing setup/teardown resource blocks, or defining data-heavy classes with initialization boilerplate.

# @Vocabulary
- **six**: A Python 2 and 3 compatibility library that provides utility functions and variables to bridge syntax and behavioral differences between versions.
- **modernize**: A code translation tool (superior to `2to3`) that relies on the `six` module to port Python 2 code to Python 3 while retaining Python 2 compatibility.
- **CLOS (Common Lisp Object System)**: A Lisp object system paradigm that inspires generic method dispatching outside of strict class boundaries.
- **singledispatch**: A decorator (from `functools`) that implements a simplified version of CLOS in Python, allowing generic function overloading based strictly on the type of the first argument.
- **Context Management Protocol**: The protocol governing the `with` statement, requiring objects to implement `__enter__` and `__exit__` methods to handle setup and teardown actions securely.
- **contextlib.contextmanager**: A standard library decorator that transforms a generator function into a context manager, eliminating the need to manually write `__enter__` and `__exit__` methods.
- **attr**: A third-party library used to remove class initialization boilerplate by automatically generating `__init__`, `__repr__`, and other magic methods based on declared attributes.
- **@attr.s**: The class decorator used by the `attr` library to signify a boilerplate-free class.
- **attr.ib**: The function used to declare an attribute within a class decorated by `@attr.s`.
- **frozen=True**: An argument passed to `@attr.s` to make class instances immutable and hashable (usable in sets or as dictionary keys).

# @Objectives
- Achieve seamless backward and forward compatibility between Python 2 and Python 3 without degrading code readability.
- Decouple method implementations from specific classes to create generic, reusable dispatchers.
- Enforce rigid, leak-proof resource handling using generator-based context managers.
- Drastically reduce class boilerplate code (manual assignments, basic validation, and string representations) to maximize code conciseness and maintainability.

# @Guidelines
- **Cross-Version Compatibility (six)**:
  - The AI MUST NOT use naive version checking. Minimize the scatter of `if six.PY3` conditionals to maintain code readability.
  - The AI MUST use `six.iteritems(dictionary)` instead of `.iteritems()` or `.items()` when iterating over dictionary key-value pairs in code targeting both Py2 and Py3.
  - The AI MUST use `six.reraise()` to handle exception raising when maintaining cross-version support, avoiding syntax errors caused by Py2's multi-argument `raise` and Py3's single-argument `raise`.
  - The AI MUST use `six.u`, `six.string_types`, and `six.integer_types` for type checking and declarations of strings and integers.
  - The AI MUST use `six.moves` to import standard library modules that were renamed or moved between Py2 and Py3 (e.g., `six.moves.configparser`). Use `six.add_move` for custom internal moves if required.
  - The AI SHOULD encapsulate `six` logic inside a custom internal compatibility module if usage is extensive, allowing it to be easily removed when Py2 support is eventually dropped.
  - The AI MUST prefer `modernize` over `2to3` for automated code porting.
- **Generic Method Dispatching (singledispatch)**:
  - The AI MUST use `@functools.singledispatch` to create generic methods instead of writing long `if/elif isinstance()` chains.
  - The AI MUST define a base function decorated with `@singledispatch` that raises a `NotImplementedError` to handle unregistered types.
  - The AI MUST register type-specific implementations using `@<base_function_name>.register(<Type>)`.
  - The AI MUST account for the limitation that `singledispatch` only routes based on the *first* argument. 
  - The AI MUST NOT use `super()` inside singledispatch implementations, as generic functions lack class inheritance hierarchy.
- **Context Managers (contextlib)**:
  - The AI MUST implement custom context managers using `@contextlib.contextmanager` on a generator function yielding a value, rather than manually authoring classes with `__enter__` and `__exit__` methods.
  - The AI MUST wrap the `yield` statement inside a `try...finally` block if exceptions raised within the `with` block could interrupt the necessary teardown/cleanup phase.
  - The AI MUST combine multiple context managers into a single `with` statement (e.g., `with open(x) as a, open(y) as b:`) rather than nesting multiple `with` blocks.
- **Reducing Boilerplate (attr)**:
  - The AI MUST use the `attr` library (`@attr.s` and `attr.ib()`) instead of manually defining `__init__`, `self.x = x` assignments, and `__repr__` methods for data-heavy objects.
  - The AI MUST use the `converter` argument in `attr.ib()` (e.g., `converter=str`) or the `@<attribute_name>.validator` decorator for input validation and coercion, instead of writing custom validation logic in an `__init__` method.
  - The AI MUST use `@attr.s(frozen=True)` when an object must be hashable (e.g., used as a dictionary key or in a set) to enforce immutability.

# @Workflow
1. **Analyze Compatibility Requirements**: Check if the code requires Python 2 and Python 3 support. If yes, immediately import `six`. 
2. **Abstract Iteration & Exceptions**: Scan for `.iteritems()`, multi-argument `raise` statements, and moved standard library imports. Replace them with their `six` equivalents (`six.iteritems`, `six.reraise`, `six.moves`).
3. **Refactor Conditional Type Checking**: Look for methods cluttered with `if isinstance(arg, Type):`. Extract the method to a standalone generic function using `@functools.singledispatch`, writing a `@<func>.register` block for each type.
4. **Enforce Safe Resource Handling**: Identify paired setup/teardown operations (e.g., open/close, lock/release). Wrap them in a generator function decorated with `@contextlib.contextmanager`, placing the teardown logic in a `finally` block.
5. **Optimize Class Definitions**: Scan for classes dominated by `__init__` assignments and standard dunder methods (`__repr__`, `__hash__`). Replace the class declaration with `@attr.s` and replace the `__init__` variables with `attr.ib()`. Apply `frozen=True` if hashing is required.

# @Examples (Do's and Don'ts)

### Cross-Version Compatibility
**[DON'T]** Use Py2 specific methods or basic version-check scattering for dictionary iteration:
```python
if sys.version_info[0] < 3:
    for k, v in mydict.iteritems():
        print(k, v)
else:
    for k, v in mydict.items():
        print(k, v)
```

**[DO]** Use the `six` module for a clean, universally compatible approach:
```python
import six

for k, v in six.iteritems(mydict):
    print(k, v)
```

### Module Imports
**[DON'T]** Use try/except blocks to handle moved standard libraries:
```python
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
```

**[DO]** Use `six.moves` to handle standard library renames transparently:
```python
from six.moves.configparser import ConfigParser
conf = ConfigParser()
```

### Generic Method Dispatching
**[DON'T]** Write monolithic methods with deep type-checking chains:
```python
def play(instrument):
    if isinstance(instrument, SnareDrum):
        return "POC!"
    elif isinstance(instrument, Cymbal):
        return "FRCCCHHT!"
    else:
        raise NotImplementedError("Cannot play these")
```

**[DO]** Use `@singledispatch` to decouple logic into clean, type-specific generic functions:
```python
import functools

@functools.singledispatch
def play(instrument):
    raise NotImplementedError("Cannot play these")

@play.register(SnareDrum)
def _(instrument):
    return "POC!"

@play.register(Cymbal)
def _(instrument):
    return "FRCCCHHT!"
```

### Context Managers
**[DON'T]** Nest `with` statements or write custom `__enter__`/`__exit__` classes for simple resource wrapping. Don't leave `yield` unprotected from internal block exceptions:
```python
with open("file1", "r") as source:
    with open("file2", "w") as destination:
        destination.write(source.read())

# Unprotected custom context manager
@contextlib.contextmanager
def MyContext():
    setup_resource()
    yield
    cleanup_resource() # Will not run if an exception occurs in the with-block
```

**[DO]** Combine `with` statements and use protected `contextlib` generators:
```python
import contextlib

with open("file1", "r") as source, open("file2", "w") as destination:
    destination.write(source.read())

@contextlib.contextmanager
def MyContext():
    setup_resource()
    try:
        yield 42
    finally:
        cleanup_resource() # Guaranteed to run
```

### Reducing Class Boilerplate
**[DON'T]** Manually write `__init__`, `__repr__`, and basic validations for data-holding classes:
```python
class Car(object):
    def __init__(self, color, speed=0):
        self.color = str(color)
        if speed < 0:
            raise ValueError("Value cannot be negative")
        self.speed = speed

    def __repr__(self):
        return "Car(color=%r, speed=%r)" % (self.color, self.speed)
```

**[DO]** Use `attr` to auto-generate boilerplate, conversions, and validations:
```python
import attr

@attr.s
class Car(object):
    color = attr.ib(converter=str)
    speed = attr.ib(default=0)

    @speed.validator
    def speed_validator(self, attribute, value):
        if value < 0:
            raise ValueError("Value cannot be negative")
```