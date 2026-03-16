@Domain
When the AI is requested to design, refactor, or implement Python classes involving dynamic attribute access, object attribute caching, JSON-to-object facades, attribute validation, and metaprogramming related to properties and attribute handling.

@Vocabulary
- Uniform Access Principle: The design principle stating that all services offered by a module should be available through a uniform notation (e.g., `obj.attr`), which does not betray whether they are implemented through storage or through computation.
- Dynamic Attribute: An attribute that presents the same interface as a data attribute but is computed on demand, typically using `@property` or the `__getattr__` special method.
- Virtual Attribute: An attribute that is not explicitly declared in the source code or present in the instance `__dict__`, but is retrieved or computed on the fly via `__getattr__`.
- Bypassing the Property: The technique of accessing `self.__dict__['attr_name']` directly within a property's methods to avoid infinite recursion.
- Bunch Idiom: Updating an instance's `__dict__` directly with keyword arguments (`self.__dict__.update(kwargs)`) for rapid data-driven attribute creation.
- __getattr__: Special method invoked by the interpreter *only* when the usual process fails to retrieve an attribute (i.e., it acts as a fallback).
- __getattribute__: Special method *always* called when an attempt is made to retrieve an attribute directly.
- __setattr__: Special method *always* called when an attempt is made to set an attribute.
- __new__: Special class method invoked by Python to construct an instance before `__init__` is called to initialize it.
- @cached_property: A decorator from the `functools` module that caches the result of a method in an instance attribute of the same name. (It is technically a nonoverriding descriptor).

@Objectives
- Enforce the Uniform Access Principle by avoiding Java-style getter and setter methods in favor of plain attributes or Pythonic properties.
- Safely implement dynamic and virtual attributes without causing infinite recursion loops.
- Prevent syntax errors and data loss when dynamically generating attributes from external data (e.g., JSON) by sanitizing reserved keywords and invalid identifiers.
- Optimize application memory and CPU usage by applying the correct property caching strategies depending on class design (e.g., presence of `__slots__` or namesake instance attributes).
- Appropriately use `__new__` for flexible object creation scenarios where `__init__` is insufficient.

@Guidelines

- The AI MUST adhere to the Uniform Access Principle. Start with simple public data attributes. Only implement `@property` if validation, access control, or computation is strictly required. Do NOT generate `get_foo()` and `set_foo()` methods.
- When implementing a read-only facade for dynamic data (like JSON), the AI MUST use `__getattr__`. 
- Within `__getattr__`, if the requested attribute is missing from the underlying data source, the AI MUST raise `AttributeError`, not `KeyError`.
- When dynamically building attributes from external mapping keys, the AI MUST sanitize keys. If a key is a Python reserved keyword, use `keyword.iskeyword(key)` to detect it and append an underscore (e.g., `class_`) to the attribute name.
- If a property needs to retrieve or modify data stored in an instance attribute with the exact same name as the property itself, the AI MUST access the data via `self.__dict__['attr_name']` to bypass the property logic and avoid `RecursionError`.
- When property caching is required, the AI MUST evaluate the context to choose the correct caching strategy:
  1. Use `@functools.cached_property` for standard caching of expensive read-only properties.
  2. The AI MUST NOT use `@cached_property` if the class defines `__slots__`.
  3. The AI MUST NOT use `@cached_property` if the property method relies on an existing instance attribute with the exact same name.
  4. If `@cached_property` is unsuitable, the AI MUST stack `@property` strictly on top of `@functools.cache`.
- The AI MUST NOT use `@cached_property` if the code must maintain the PEP 412 (Key-Sharing Dictionary) optimization, as `@cached_property` creates instance attributes after `__init__` is complete, which defeats this optimization.
- For attribute validation, the AI MUST use a `@property` getter and an `@attr.setter` method. The setter MUST validate the input and raise `ValueError` or `TypeError` for invalid data before storing the value.
- If handling attribute deletion is required, the AI MUST implement a method decorated with `@attr.deleter`.
- When overriding `__getattribute__` or `__setattr__`, the AI MUST delegate to the superclass implementation using `super().__getattribute__(name)` or `super().__setattr__(name, value)` to prevent catastrophic infinite recursion. Avoid implementing these two methods unless absolutely necessary, favoring `__getattr__` or properties instead.
- The AI MUST use `__new__` instead of `__init__` when the class needs to act as a factory that might return instances of different classes, pre-existing instances, or when inheriting from immutable built-in types. Remember that `__new__` receives the class (`cls`) as its first argument, not `self`.
- The AI MAY use the "Bunch Idiom" (`self.__dict__.update(kwargs)`) in `__init__` for quick initialization of arbitrary attributes, provided the keys have been validated as safe.

@Workflow
1. Assess the data encapsulation requirement: Begin with public attributes.
2. If the prompt requires dynamic data traversal (e.g., exploring JSON), construct a read-only facade utilizing `__getattr__`.
3. In `__getattr__`, map the requested attribute to the underlying data dictionary. Catch `KeyError` on the dict and explicitly raise `AttributeError` for missing attributes.
4. When ingesting dynamic keys into attributes, iterate over the keys, run `keyword.iskeyword()`, and mutate the key (e.g., append `_`) before binding to the object.
5. If business rules dictate validation on assignment, write a `@property` for the getter and a corresponding `.setter` for validation.
6. When implementing properties that interact with storage attributes of the same name, use `self.__dict__['name']` for all reads and writes within the property methods.
7. If the prompt asks for property memoization/caching, check for `__slots__` or namesake underlying storage. If neither exists, use `@cached_property`. Otherwise, use `@property` above `@cache`.

@Examples (Do's and Don'ts)

[DO] Implement dynamic attribute access safely and handle missing attributes correctly
class FrozenJSON:
    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        try:
            return self.__data[name]
        except KeyError:
            raise AttributeError(f"'FrozenJSON' object has no attribute '{name}'")

[DON'T] Let dynamic attribute lookup raise a KeyError, which violates Python's standard attribute access contract
class FrozenJSON:
    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        # Anti-pattern: Will raise KeyError instead of AttributeError
        return self.__data[name]

[DO] Sanitize reserved keywords when dynamically setting attributes
import keyword

class Record:
    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

[DON'T] Blindly ingest dynamic keys as attributes without checking keywords
class Record:
    def __init__(self, mapping):
        # Anti-pattern: If mapping contains {'class': 1982}, student.class will raise a SyntaxError
        self.__dict__.update(mapping)

[DO] Bypass a property safely using `__dict__` to prevent recursion
class Event:
    def __init__(self):
        self.__dict__['speakers'] = [3471, 5199]

    @property
    def speakers(self):
        # Bypasses the property getter to avoid infinite recursion
        spkr_serials = self.__dict__['speakers']
        return [fetch_speaker(key) for key in spkr_serials]

[DON'T] Access the property's own name via `self` inside its getter
class Event:
    @property
    def speakers(self):
        # Anti-pattern: self.speakers triggers this property again, causing RecursionError
        spkr_serials = self.speakers
        return [fetch_speaker(key) for key in spkr_serials]

[DO] Stack `@property` over `@cache` when `@cached_property` is unsuitable
from functools import cache

class Event:
    @property
    @cache
    def speakers(self):
        spkr_serials = self.__dict__['speakers']
        return [fetch_speaker(key) for key in spkr_serials]

[DON'T] Stack decorators in the wrong order or use `@cached_property` when an attribute of the same name already exists in the instance
from functools import cache

class Event:
    @cache
    @property
    def speakers(self):
        # Anti-pattern: @cache must be under @property
        pass

[DO] Use `super()` when implementing `__getattribute__` or `__setattr__`
class MyClass:
    def __setattr__(self, name, value):
        if name == 'special':
            value = value.upper()
        super().__setattr__(name, value)

[DON'T] Use `self.__dict__ = ...` or `self.name = ...` inside `__setattr__` as it triggers infinite recursion
class MyClass:
    def __setattr__(self, name, value):
        # Anti-pattern: Triggers __setattr__ infinitely
        self.__dict__[name] = value

[DO] Use `__new__` for flexible object creation based on data types
class FrozenJSON:
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg