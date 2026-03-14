# @Domain
These rules MUST trigger whenever the AI is tasked with generating, refactoring, or analyzing Python code involving object-oriented design, class definitions, attribute access control, data validation upon assignment, dynamic properties, subclass hierarchies, class registration, or the implementation of descriptors and metaclasses.

# @Vocabulary
- **Plain Attribute**: A standard, public instance variable (e.g., `self.x = 1`) accessed directly without explicit getter/setter methods.
- **@property**: A built-in decorator used to intercept attribute access, allowing an instance attribute to execute a method dynamically while maintaining a plain attribute interface.
- **Descriptor**: A class that implements Python's descriptor protocol (`__get__`, `__set__`, and/or `__delete__`) to define and reuse reusable attribute access logic across multiple fields or classes.
- **__getattr__**: A special method called *only* as a fallback when an attribute cannot be found in the instance's dictionary or its class tree.
- **__getattribute__**: A special method called on *every* attribute access, intercepting the standard attribute lookup completely.
- **__setattr__**: A special method called on *every* attribute assignment.
- **__init_subclass__**: A class method introduced in Python 3.6 that acts as a hook to initialize and validate subclasses at the time they are defined.
- **__set_name__**: A descriptor method introduced in Python 3.6 that automatically receives the name of the attribute it was assigned to in the owning class.
- **Class Decorator**: A function applied to a class definition using the `@` syntax that modifies or wraps the class prior to returning it.
- **Metaclass**: A class inheriting from `type` that defines the behavior of class objects. In modern Python, these should generally be avoided in favor of `__init_subclass__` and Class Decorators.

# @Objectives
- Enforce the Pythonic paradigm of using plain public attributes by default, actively avoiding Java-style explicit getter and setter methods.
- Safely evolve class data models over time using `@property` and Descriptors without breaking backwards compatibility.
- Maximize code reuse and limit boilerplate by abstracting redundant `@property` validation logic into Descriptors.
- Prevent infinite recursion loops when overriding dynamic attribute access (`__getattr__`, `__getattribute__`, `__setattr__`).
- Avoid the complexity, unapproachability, and conflict risks of Metaclasses by utilizing Python 3.6+ features (`__init_subclass__`, `__set_name__`) and Class Decorators for subclass validation, registration, and extension.

# @Guidelines
- **Attribute Access**: The AI MUST default to plain attributes for all new class interfaces. The AI MUST NOT generate explicit `get_attribute()` or `set_attribute()` methods.
- **Evolving Attributes**: When an existing plain attribute requires new behavior (like validation, bounds checking, or on-the-fly calculation), the AI MUST convert it into a `@property` with a corresponding `@property_name.setter`.
- **@property Constraints**: The AI MUST NOT include slow operations, complex computations, I/O, or surprising side effects within `@property` methods. The AI MUST NOT mutate the state of *other* unrelated object attributes inside a getter method.
- **Descriptor Extraction**: When encountering identical `@property` validation or computation logic repeated across multiple attributes or classes, the AI MUST extract this logic into a separate Descriptor class.
- **Descriptor State Management**: When implementing a Descriptor, the AI MUST prevent memory leaks. The AI MUST NOT store instance-specific data on the descriptor object itself unless using `weakref.WeakKeyDictionary`. Alternatively, and preferably, the AI MUST use the `__set_name__` hook to learn the attribute's name and store the data directly on the owning instance's `__dict__`.
- **Lazy Attributes**: When tasked with deferring the loading or computation of an attribute until it is first accessed, the AI MUST implement `__getattr__`.
- **Strict Attribute Interception**: When tasked with intercepting *all* attribute accesses (e.g., to check transaction state on every read), the AI MUST implement `__getattribute__`.
- **Recursion Prevention**: When implementing `__getattribute__` or `__setattr__`, the AI MUST access the instance's dictionary using `super().__getattribute__(name)` or `super().__setattr__(name, value)`. The AI MUST NOT access `self.__dict__` or `self.attribute` directly within these methods to prevent `RecursionError`.
- **Subclass Validation**: When tasked with verifying that a subclass is defined correctly (e.g., enforcing class attributes or method overrides), the AI MUST implement the `__init_subclass__` method in the parent class. The AI MUST NOT use a custom Metaclass (`__new__`) for this purpose.
- **Subclass Registration**: When tasked with maintaining a registry of subclasses (e.g., for factory patterns, serialization/deserialization mapping), the AI MUST automate the registration using `__init_subclass__` to prevent developers from forgetting to register classes.
- **Multiple Inheritance Support**: When overriding `__init_subclass__`, the AI MUST call `super().__init_subclass__()` to ensure compatibility with multiple inheritance and diamond hierarchies.
- **Descriptor Naming**: When a Descriptor needs to know the name of the attribute it is assigned to, the AI MUST implement the `__set_name__(self, owner, name)` method on the Descriptor instead of requiring the name to be passed manually into the Descriptor's `__init__`.
- **Class Extension**: When tasked with modifying all methods or attributes of a class (e.g., wrapping all methods with a logging/tracing decorator), the AI MUST use a Class Decorator. The AI MUST NOT use a Metaclass, as Metaclasses cannot be easily composed and trigger "metaclass conflict" TypeErrors when a class inherits from multiple bases with different metaclasses.

# @Workflow
1. **Model Definition**: Define classes using simple public attributes.
2. **Behavior Injection**: If validation or computation is required upon attribute access, wrap the attribute in a `@property`.
3. **Logic Deduplication**: If the `@property` logic is repeated, refactor it into a Descriptor class.
4. **Descriptor Implementation**: Implement `__get__`, `__set__`, and `__set_name__` on the Descriptor. Have the Descriptor store its state directly in the target instance using `setattr(instance, self.internal_name, value)`.
5. **Dynamic Resolution**: If attributes are schemaless or loaded dynamically from a database, implement `__getattr__` to populate them on first access.
6. **Class Hierarchy Rules**: If the base class requires subclasses to conform to a specific schema or register themselves, implement `__init_subclass__` on the base class to validate or map the subclass. Call `super().__init_subclass__()` within it.
7. **Cross-Cutting Concerns**: If cross-cutting modifications must be made to an entire class (like debugging wrappers), write a Class Decorator and apply it with `@decorator_name` above the class definition.

# @Examples (Do's and Don'ts)

### Plain Attributes vs Getter/Setters
- **[DO]** Use plain attributes and `@property`.
```python
class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms

class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f'ohms must be > 0; got {ohms}')
        self._ohms = ohms
```
- **[DON'T]** Write explicit getter/setter methods.
```python
class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f'ohms must be > 0; got {ohms}')
        self._ohms = ohms
```

### Descriptors and __set_name__
- **[DO]** Use `__set_name__` to automatically capture the attribute name and store state safely on the instance.
```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class Customer:
    first_name = Field()
    last_name = Field()
```
- **[DON'T]** Manually pass the attribute name to the descriptor or leak memory by storing instance state locally without a `WeakKeyDictionary`.
```python
class LeakyField:
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + name
        self.values = {} # ANTI-PATTERN: Leaks memory!

    def __set__(self, instance, value):
        self.values[instance] = value # Keeps instance alive forever

class Customer:
    # ANTI-PATTERN: Redundant name declaration
    first_name = LeakyField('first_name') 
```

### Recursion in Dynamic Attributes
- **[DO]** Use `super().__getattribute__` to safely bypass dynamic interception.
```python
class DictionaryRecord:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        data_dict = super().__getattribute__('_data')
        if name in data_dict:
            return data_dict[name]
        return super().__getattribute__(name)
```
- **[DON'T]** Access `self.attribute` inside `__getattribute__`, triggering a recursive stack overflow.
```python
class BrokenDictionaryRecord:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        # ANTI-PATTERN: Accessing self._data triggers __getattribute__ again!
        return self._data[name] 
```

### Subclass Validation and Registration
- **[DO]** Use `__init_subclass__` to validate and register classes safely.
```python
registry = {}

class BetterPolygon:
    sides = None

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.sides is not None and cls.sides < 3:
            raise ValueError('Polygons need 3+ sides')
        registry[cls.__name__] = cls

class Hexagon(BetterPolygon):
    sides = 6 # Automatically validated and registered
```
- **[DON'T]** Use a complex Metaclass (`__new__`) for simple subclass validation.
```python
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        if bases:
            if class_dict.get('sides', 0) < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    sides = None
```

### Class Modification
- **[DO]** Use a Class Decorator to modify all methods of a class.
```python
def trace(klass):
    for key in dir(klass):
        value = getattr(klass, key)
        if callable(value):
            setattr(klass, key, trace_func(value))
    return klass

@trace
class TraceDict(dict):
    pass
```
- **[DON'T]** Use a Metaclass to modify class methods, as it prevents composability and breaks multiple inheritance via metaclass conflicts.
```python
class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        # ANTI-PATTERN: Brittle and causes conflicts if inheriting from another class with a metaclass
        klass = super().__new__(meta, name, bases, class_dict)
        return klass

class TraceDict(dict, metaclass=TraceMeta):
    pass
```