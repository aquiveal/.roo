# @Domain
Python programming involving object-oriented design, class architectures, interface definitions, inheritance structures, data encapsulation, and custom container type implementations. This rule file activates whenever the AI is refactoring data structures into classes, defining class hierarchies, implementing API hooks, utilizing multiple inheritance, or building custom sequence/mapping types.

# @Vocabulary
- **Built-in Nesting:** The anti-pattern of using dictionaries that contain other dictionaries, long tuples, or complex nestings of built-in types to maintain internal state.
- **Hook:** A function or callable passed as an argument to an API to customize its behavior during execution (e.g., the `key` argument in `list.sort`).
- **Stateful Closure:** A nested function that maintains state using the `nonlocal` keyword. (An anti-pattern when used for hooks).
- **Callable:** An object that can be executed like a function, enabled in custom classes via the `__call__` special method.
- **Class Method Polymorphism:** Using the `@classmethod` decorator to define alternative, generic constructors for a class hierarchy.
- **Diamond Inheritance:** A multiple inheritance scenario where a subclass inherits from two separate classes that share the same superclass.
- **MRO (Method Resolution Order):** The algorithm (C3 linearization) Python uses to determine the order in which superclasses are initialized, ensuring common superclasses in diamond hierarchies are run only once.
- **Mix-in:** A class designed to compose functionality into subclasses. It defines a small set of methods, does not define its own instance attributes, and does not require its `__init__` constructor to be called.
- **Name Mangling:** The compiler transformation applied to private attributes (double leading underscore, `__attribute`), converting them to `_ClassName__attribute`.
- **Protected Attribute:** An attribute prefixed with a single underscore (`_attribute`), signaling an internal API by convention.
- **Private Attribute:** An attribute prefixed with a double underscore (`__attribute`), used strictly to prevent naming conflicts with out-of-control subclasses.
- **collections.abc:** A built-in module providing abstract base classes for standard Python interfaces (e.g., `Sequence`, `MutableMapping`).

# @Objectives
- Prevent brittle and unreadable state management by decomposing deeply nested built-in types into lightweight data structures or class hierarchies.
- Ensure API hooks and callbacks are implemented using stateless functions or stateful `__call__` classes, avoiding complex stateful closures.
- Standardize object construction and multiple inheritance using `@classmethod` factories and `super()` initialization to avoid diamond inheritance bugs.
- Maximize code reuse and composability using stateless Mix-in classes instead of deep, stateful multiple inheritance.
- Enforce the Pythonic philosophy of "consenting adults" by defaulting to protected attributes over private attributes to allow safe subclassing.
- Guarantee custom container types implement full Python protocols by inheriting from `collections.abc` rather than duck-typing partial implementations.

# @Guidelines

## Data Structures & Composition (Item 37)
- The AI MUST NOT use dictionaries whose values are dictionaries, long tuples, or complex nestings of other built-in types.
- When an internal state dictionary requires more than one level of nesting, the AI MUST break the bookkeeping out into multiple classes.
- The AI MUST use `collections.namedtuple` for lightweight, immutable data containers instead of standard tuples when positional data implies distinct fields.
- The AI MUST transition from `namedtuple` to the built-in `dataclasses` module if the data container requires more than a handful of attributes, optional properties, or default argument values.

## Hooks & Interfaces (Item 38)
- The AI MUST pass simple functions instead of instantiating classes for simple API interfaces and callbacks.
- When a function hook requires maintaining internal state, the AI MUST NOT use a stateful closure with the `nonlocal` statement.
- When state is required in a hook, the AI MUST define a class encapsulating that state and implement the `__call__` special method so the class instance acts as a callable.

## Generic Object Construction (Item 39)
- The AI MUST NOT require every subclass in a hierarchy to share a compatible `__init__` constructor.
- When alternative or generic ways to build objects are needed, the AI MUST use the `@classmethod` decorator to implement class method polymorphism.

## Parent Class Initialization (Item 40)
- The AI MUST NOT directly call a parent class's `__init__` method (e.g., `ParentClass.__init__(self)`).
- The AI MUST use the `super()` built-in function to initialize parent classes (e.g., `super().__init__(value)`).
- The AI MUST call `super()` with zero arguments within a class definition, unless explicitly accessing a specific superclass implementation from a child class to wrap or reuse functionality.

## Mix-in Classes (Item 41)
- The AI MUST avoid multiple inheritance of classes that possess instance attributes or require `__init__` calls.
- When sharing generic functionality across multiple unrelated classes, the AI MUST use Mix-in classes.
- When defining a Mix-in class, the AI MUST NOT define an `__init__` method and MUST NOT define instance attributes natively within the Mix-in.
- The AI MUST use `super()` within Mix-in methods to defer to default implementations, allowing subclasses to provide pluggable overrides (e.g., to prevent infinite recursion/cycles).

## Attribute Visibility (Item 42)
- The AI MUST default to using public attributes for class data.
- For internal APIs and state, the AI MUST use protected attributes (prefixed with a single underscore, `_field`) and document their expected usage for subclasses.
- The AI MUST NOT use private attributes (prefixed with a double underscore, `__field`) to simulate strict access control.
- The AI MAY ONLY use private attributes when explicitly preventing naming conflicts with subclasses that are out of the programmer's control (e.g., in a public API base class).

## Custom Container Types (Item 43)
- When implementing a simple sequence or mapping, the AI SHOULD subclass Python's built-in `list` or `dict` directly.
- When implementing custom container types that do not inherit from built-ins, the AI MUST inherit from the interfaces defined in the `collections.abc` module (e.g., `Sequence`, `MutableMapping`, `Set`).
- The AI MUST NOT attempt to duct-tape custom sequences merely by implementing `__getitem__` and `__len__`; the AI MUST use `collections.abc` to inherit the full suite of expected methods (`index`, `count`, etc.).

# @Workflow
1. **State Assessment:** When refactoring state management, check for nested dictionaries or long tuples. Flatten tuples into `namedtuple` or `dataclass`. Break nested dictionaries into a hierarchy of explicitly defined classes.
2. **Interface Refactoring:** When defining API callbacks, default to passing a function. If the callback tracks state, upgrade it to a class implementing `__call__`.
3. **Constructor Design:** If a class requires multiple ways to be instantiated from different data sources, implement `@classmethod` factories.
4. **Inheritance Check:** Scan class `__init__` methods. Replace all explicit `Parent.__init__(self)` calls with `super().__init__()`.
5. **Composition Review:** If a class inherits from multiple stateful base classes, extract the shared utility logic into stateless Mix-in classes and layer them.
6. **Visibility Pass:** Scan for `__private` attributes. Downgrade them to `_protected` attributes and add documentation, unless they are specifically designed to prevent naming collisions in external subclasses.
7. **Container Protocol Check:** If a class implements `__getitem__`, make it inherit from `collections.abc.Sequence` or `collections.abc.Mapping` to ensure protocol completeness.

# @Examples (Do's and Don'ts)

## Item 37: Avoid Deep Nesting
- **[DON'T]** Use deeply nested built-in types for state.
```python
class WeightedGradebook:
    def __init__(self):
        # Maps student_name -> subject -> list of (score, weight) tuples
        self._grades = defaultdict(lambda: defaultdict(list))
    
    def report_grade(self, name, subject, score, weight):
        self._grades[name][subject].append((score, weight))
```
- **[DO]** Break nested types into a hierarchy of classes and use `namedtuple`.
```python
from collections import namedtuple, defaultdict

Grade = namedtuple('Grade', ('score', 'weight'))

class Subject:
    def __init__(self):
        self._grades = []
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)

class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)
```

## Item 38: Use `__call__` for Stateful Hooks
- **[DON'T]** Use stateful closures for callbacks.
```python
def increment_with_report(current, increments):
    added_count = 0
    def missing():
        nonlocal added_count
        added_count += 1
        return 0
    result = defaultdict(missing, current)
    # ...
```
- **[DO]** Define a class with `__call__`.
```python
class CountMissing:
    def __init__(self):
        self.added = 0
    def __call__(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter, current)
```

## Item 39: Use `@classmethod` for Generic Construction
- **[DON'T]** Rely on external helper functions to initialize hierarchies.
```python
def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers
```
- **[DO]** Use class method polymorphism.
```python
class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers
```

## Item 40: Initialize with `super()`
- **[DON'T]** Call parent `__init__` directly.
```python
class MyChildClass(MyBaseClass, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
```
- **[DO]** Use `super()`.
```python
class MyChildClass(MyBaseClass, TimesTwo):
    def __init__(self, value):
        super().__init__(value)
```

## Item 41: Compose with Mix-ins
- **[DON'T]** Use multiple inheritance with stateful `__init__` for simple utilities.
- **[DO]** Define a stateless Mix-in class.
```python
class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)
    
    def _traverse_dict(self, instance_dict):
        # Implementation...
        pass

class BinaryTree(ToDictMixin):
    def __init__(self, value):
        self.value = value
```

## Item 42: Prefer Protected Attributes
- **[DON'T]** Use private (double underscore) attributes to enforce access control.
```python
class MyStringClass:
    def __init__(self, value):
        self.__value = value  # Brittle for subclasses
```
- **[DO]** Use protected (single underscore) attributes and document them.
```python
class MyStringClass:
    def __init__(self, value):
        # _value stores the user-supplied string. Subclasses may read this.
        self._value = value
```

## Item 43: Inherit from `collections.abc`
- **[DON'T]** Implement partial container protocols manually.
```python
class BinaryNode:
    # Only implements __getitem__ and __len__, lacks count(), index(), etc.
    def __getitem__(self, index): ...
    def __len__(self): ...
```
- **[DO]** Inherit from `collections.abc` to guarantee complete protocols.
```python
from collections.abc import Sequence

class BinaryNode(Sequence):
    # Implements __getitem__ and __len__; Sequence provides count() and index()
    def __getitem__(self, index): ...
    def __len__(self): ...
```