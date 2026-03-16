# @Domain
Python metaprogramming, specifically the design, implementation, and application of attribute descriptors (`__get__`, `__set__`, `__delete__`, and `__set_name__`). The AI MUST trigger these rules when working on Python code involving custom properties, attribute validation, lazy evaluation/caching of attributes, ORM-like field definitions, or any refactoring of repetitive getter/setter logic into independent classes.

# @Vocabulary
* **Descriptor**: A class implementing a dynamic protocol consisting of the `__get__`, `__set__`, or `__delete__` methods.
* **Descriptor class**: The class implementing the descriptor protocol.
* **Managed class**: The class where descriptor instances are declared as class attributes.
* **Descriptor instance**: Each instance of a descriptor class, declared as a class attribute of the managed class.
* **Managed instance**: One instance of the managed class.
* **Storage attribute**: An attribute of the managed instance that holds the value of a managed attribute for that particular instance.
* **Managed attribute**: A public attribute in the managed class that is handled by a descriptor instance, with values stored in storage attributes.
* **Overriding descriptor (Data descriptor / Enforced descriptor)**: A descriptor that implements the `__set__` method. It intercepts and overrules attempts to assign to instance attributes.
* **Nonoverriding descriptor (Nondata descriptor / Shadowable descriptor)**: A descriptor that does not implement `__set__`. Setting an instance attribute with the same name will shadow the descriptor.
* **Bound method**: A callable that wraps a function and binds the managed instance to the first argument (`self`), created dynamically via the `__get__` method of a function.

# @Objectives
* Abstract and reuse attribute access, validation, and computation logic across multiple attributes and classes using descriptors.
* Ensure thread-safe and instance-safe state management by strictly separating descriptor instance state (shared class level) from managed instance state (per-object storage).
* Choose the exact type of descriptor (overriding vs. nonoverriding) based on the required behavioral semantics (e.g., read-only protection, validation, or caching).
* Eliminate boilerplate attribute naming by universally leveraging the modern `__set_name__` special method.

# @Guidelines
* **State Management Constraint**: The AI MUST NEVER store managed instance data in the descriptor instance itself (e.g., `self.value = value` in `__set__` is strictly forbidden). Values MUST be stored in the managed instance (e.g., `instance.__dict__[self.storage_name] = value` or `setattr(instance, self.storage_name, value)`).
* **Automatic Naming**: The AI MUST implement `__set_name__(self, owner, name)` in all new descriptor classes to automatically capture the attribute name and derive the `storage_name`.
* **Class-Level Access Handling**: The AI MUST handle class-level access in the `__get__` method. When a managed attribute is accessed via the class, `instance` will be `None`. The AI MUST `return self` in this scenario to support introspection.
* **Read-Only Attributes**: To create a strictly read-only descriptor, the AI MUST implement both `__get__` and `__set__`. The `__set__` method MUST raise an `AttributeError` with a suitable message. Omitting `__set__` creates a nonoverriding descriptor, allowing the user to overwrite the attribute.
* **Validation Descriptors**: When writing a descriptor solely for data validation, the AI MAY implement only the `__set__` method. If `__get__` is omitted, the descriptor behaves as an overriding descriptor without a `__get__`, meaning read access will retrieve the underlying instance attribute directly (provided the storage name matches the managed attribute name).
* **Caching/Lazy Evaluation Descriptors**: To implement a caching descriptor, the AI MUST implement ONLY `__get__` (creating a nonoverriding descriptor). The `__get__` method should compute the value and set it directly on the instance. Subsequent accesses will find the instance attribute, shadowing the descriptor and bypassing the `__get__` overhead.
* **Infinite Recursion Prevention**: When writing to the storage attribute in `__set__` or reading in `__get__`, the AI MUST avoid `getattr`/`setattr` calls that use the managed attribute's public name, as this triggers infinite recursion. Use `instance.__dict__[self.storage_name]` or ensure `storage_name` is distinct from the managed attribute name (e.g., prefixed with `_`).
* **Properties vs. Descriptors**: The AI MUST prefer the built-in `@property` decorator for simple, one-off attribute protection. The AI MUST refactor to descriptor classes when identical getter/setter logic is duplicated across multiple attributes.
* **Template Method Pattern in Descriptors**: When building a family of validating descriptors, the AI SHOULD implement an abstract base class with a `__set__` method that acts as a template method, delegating specific validation logic to an abstract `validate` method implemented by concrete subclasses.

# @Workflow
1. **Analyze Attribute Requirements**: Determine if the attribute requires validation, read-only protection, or lazy computation. Evaluate if this logic is repeated across multiple attributes.
2. **Define Descriptor Class**: Create a class representing the descriptor. Do not subclass any specific base class unless building a hierarchy of descriptors.
3. **Implement `__set_name__`**: Add `def __set_name__(self, owner, name):` to capture the `name` and set `self.storage_name`. If using `setattr`/`getattr` later, ensure `self.storage_name` is distinct (e.g., `'_' + name`).
4. **Implement `__get__` (if required)**:
   * Define `def __get__(self, instance, owner=None):`.
   * Add guard: `if instance is None: return self`.
   * Return the value using `getattr(instance, self.storage_name)` or `instance.__dict__[self.storage_name]`.
5. **Implement `__set__` (if required)**:
   * Define `def __set__(self, instance, value):`.
   * Perform validation, transformation, or caching checks on `value`.
   * Store the result using `setattr(instance, self.storage_name, value)` or `instance.__dict__[self.storage_name] = value`.
6. **Deploy Descriptor**: Instantiate the descriptor as a class attribute in the managed class (e.g., `price = Quantity()`).

# @Examples (Do's and Don'ts)

### [DO] Use `__set_name__` and store state in the managed instance
```python
class Quantity:
    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        if value > 0:
            # Store in the managed instance's __dict__ to avoid infinite recursion
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError(f'{self.storage_name} must be > 0')

class LineItem:
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
```

### [DON'T] Store state on the descriptor instance (causes shared state corruption)
```python
class Quantity:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            # WRONG: This overwrites the value for ALL instances of the managed class
            self.value = value 
        else:
            raise ValueError('must be > 0')

    def __get__(self, instance, owner):
        return self.value # WRONG: Returns shared state
```

### [DO] Implement `__get__` correctly to handle class-level access
```python
class Field:
    def __set_name__(self, owner, name):
        self.storage_name = '_' + name

    def __get__(self, instance, owner=None):
        if instance is None:
            # DO: Return the descriptor instance when accessed via the class
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)
```

### [DON'T] Attempt to create a read-only descriptor without `__set__`
```python
class ReadOnly:
    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None: return self
        return instance.__dict__.get(self.storage_name, 'default')
    
    # WRONG: Omitting __set__ makes this a nonoverriding descriptor.
    # A user can easily overwrite it: `obj.my_attr = 'new_value'`, 
    # which permanently shadows the descriptor for that instance.
```

### [DO] Create an overriding descriptor to strictly enforce read-only behavior
```python
class ReadOnly:
    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None: return self
        return instance.__dict__.get(self.storage_name, 'default')
    
    def __set__(self, instance, value):
        # DO: Block assignment explicitly
        raise AttributeError(f"readonly attribute {self.storage_name!r}")
```