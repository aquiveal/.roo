# @Domain
This rule file activates during Python class design, refactoring of complex data structures, implementation of inheritance architectures, development of class interfaces and APIs, constructor design, and the creation of custom container types.

# @Vocabulary
- **Mix-in**: A class that defines a small set of additional methods for its child classes without defining its own instance attributes or requiring its `__init__` constructor to be called.
- **Diamond Inheritance**: A scenario where a subclass inherits from two separate classes that share the same superclass somewhere in the hierarchy.
- **MRO (Method Resolution Order)**: The C3 linearization algorithm Python uses to determine the strict order in which superclasses are initialized.
- **Name Mangling**: Python's compiler transformation of private attributes (e.g., `__field` to `_Class__field`) to prevent accidental access by subclasses.
- **Pluggable Behavior**: Instance-level overrides in subclasses that modify or safely constrain the generic behavior of a Mix-in (e.g., preventing infinite loops in graph traversals).
- **Callable**: Any object that implements the `__call__` special method, allowing instances of the class to be executed exactly like a function.

# @Objectives
- Prevent brittle, deeply nested built-in types by systematically migrating to lightweight data containers or well-defined class hierarchies.
- Maximize code reuse and API flexibility through stateless functions, callables, and mix-in classes.
- Ensure robust and predictable class hierarchies by strictly adhering to Python's MRO via `super()`.
- Avoid the restrictive use of private attributes, favoring an open architecture guided by protected conventions and documentation, unless preventing explicit name collisions in public APIs.
- Guarantee complete and correct custom container implementations by inheriting from `collections.abc`.

# @Guidelines
- **Complex State Management**: When internal state dictionaries become deeper than one level of nesting (e.g., dictionaries mapping to dictionaries, or containing long, position-dependent tuples), the AI MUST extract the bookkeeping into multiple classes.
- **Lightweight Containers**: The AI MUST use `collections.namedtuple` for lightweight, immutable data containers before escalating to a full class.
- **Namedtuple Limitations**: The AI MUST NOT use `namedtuple` if the data structure requires default argument values or exceeds a handful of attributes. In these cases, the AI MUST use the `dataclasses` module instead.
- **Interface Hooks**: For simple interfaces between components (e.g., the `key` argument in sorting or the default value hook in `defaultdict`), the AI MUST accept simple functions instead of defining and instantiating new classes.
- **Stateful Hooks**: If a function passed as a hook requires maintaining state, the AI MUST define a class implementing the `__call__` special method instead of using a stateful closure.
- **Alternative Constructors**: The AI MUST use the `@classmethod` decorator to define alternative constructors or generic factory methods (polymorphism for classes). The AI MUST NOT require every subclass to have a compatible `__init__` method for generic object construction.
- **Parent Initialization**: The AI MUST initialize parent classes using `super().__init__()` with zero arguments.
- **Direct Initialization Anti-Pattern**: The AI MUST NOT directly call a parent class's `__init__` method (e.g., `Parent.__init__(self)`), as this ignores MRO and causes severe bugs in multiple and diamond inheritance.
- **Mix-in Constraints**: The AI MUST prefer Mix-in classes over multiple inheritance with instance attributes and `__init__` methods. Mix-ins MUST ONLY provide instance or class methods.
- **Attribute Visibility**: The AI MUST prefer public attributes and conventionally protected attributes (prefixed with a single underscore `_`) over private attributes (prefixed with a double underscore `__`).
- **Protected Attribute Documentation**: The AI MUST thoroughly document protected fields to guide subclass usage rather than attempting to force access control with private attributes.
- **Private Attributes Exception**: The AI MUST ONLY use private attributes to explicitly avoid naming conflicts with subclasses that are entirely out of the control of the API author (e.g., in a widely consumed public API).
- **Custom Containers**: When creating custom sequence, mapping, or set types that go beyond simple direct inheritance of `list` or `dict`, the AI MUST inherit from the abstract base classes in the `collections.abc` module to ensure all required methods (e.g., `__len__`, `count`, `index`) are properly implemented and missing method errors are caught at instantiation.

# @Workflow
1. **Data Structure Evaluation**: Analyze the depth of nested built-in types. If dicts contain dicts or complex tuples, extract the inner levels into `namedtuple`s, `dataclasses`, or custom classes.
2. **Interface Design**: When an API requires a callback or hook, accept a plain function. If the implementation of that hook requires tracking state over time, implement a class with a `__call__` method.
3. **Hierarchy Construction**: Map out inheritance trees. If generic instantiation of subclasses is required, define a generic `@classmethod` factory. Verify all parent initializations strictly use `super().__init__()`.
4. **Mix-in Composition**: If multiple inheritance is proposed, strip state and `__init__` from the secondary parent classes, distilling shared behavior into stateless Mix-in classes.
5. **Attribute Scoping**: Default all class fields to public. Prefix internal-only attributes with a single underscore `_` and add docstrings explaining subclass handling. Only apply `__` prefixes if the class is a public API subject to unpredictable namespace collisions.
6. **Container Verification**: If the class represents a container structure (e.g., a tree behaving like a list), verify it inherits from the appropriate `collections.abc` interface (e.g., `collections.abc.Sequence`). Implement all required abstract methods indicated by the base class.

# @Examples (Do's and Don'ts)

## Complex State Management
- [DO] Use `namedtuple` or helper classes for multi-level bookkeeping:
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
```
- [DON'T] Nest dictionaries within dictionaries:
```python
class WeightedGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        # Anti-pattern: Deeply nested built-in types
        self._grades[name][subject].append((score, weight))
```

## Stateful Hooks
- [DO] Use a class with `__call__` when state must be maintained:
```python
class CountMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter, current_dict)
```
- [DON'T] Use stateful closures to track state in hooks:
```python
def increment_with_report(current, increments):
    added_count = 0
    
    def missing():
        nonlocal added_count  # Anti-pattern: hard to read and test
        added_count += 1
        return 0
        
    result = defaultdict(missing, current)
```

## Generic Object Construction
- [DO] Use `@classmethod` polymorphism for generic construction:
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
- [DON'T] Hardcode constructor shapes across subclasses or use external builder functions:
```python
def create_workers(input_list):
    workers = []
    for input_data in input_list:
        # Anti-pattern: hardcoded class construction prevents generic polymorphism
        workers.append(LineCountWorker(input_data))
    return workers
```

## Parent Class Initialization
- [DO] Use `super().__init__()` to strictly follow MRO:
```python
class TimesSevenCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7
```
- [DON'T] Directly call parent `__init__` methods:
```python
class TimesSeven(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)  # Anti-pattern: Breaks under diamond inheritance
        self.value *= 7
```

## Attribute Visibility
- [DO] Use protected attributes and rely on documentation:
```python
class MyStringClass:
    def __init__(self, value):
        # This stores the user-supplied value.
        # It should be coercible to a string. 
        # Treat as immutable by subclasses.
        self._value = value
```
- [DON'T] Use private attributes to falsely enforce access control:
```python
class MyStringClass:
    def __init__(self, value):
        self.__value = value  # Anti-pattern: Subclasses will break if hierarchy changes
```

## Custom Containers
- [DO] Inherit from `collections.abc` to enforce complete container interfaces:
```python
from collections.abc import Sequence

class SequenceNode(Sequence):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __getitem__(self, index):
        # Implementation...
        pass

    def __len__(self):
        # Implementation...
        pass
```
- [DON'T] Implement custom containers without ABCs, missing expected default methods:
```python
class IndexableNode:
    # Anti-pattern: Missing __len__, count, index, etc. expected of sequences
    def __getitem__(self, index):
        pass
```