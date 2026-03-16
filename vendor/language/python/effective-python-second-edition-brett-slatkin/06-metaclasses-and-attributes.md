# @Domain
Triggered when the user requests the creation, modification, or refactoring of Python classes, specifically involving attribute access control, properties, descriptors, dynamic attributes (`__getattr__`, `__getattribute__`, `__setattr__`), class validation, class registration, or class behavior extensions.

# @Vocabulary
- **`@property`**: A built-in decorator used to define getter, setter, and deleter methods for a class attribute, enabling special behavior during attribute access without changing the public API.
- **Descriptor Protocol**: A set of special methods (`__get__`, `__set__`, `__delete__`, `__set_name__`) that define how attribute access is intercepted and interpreted at the class level.
- **`WeakKeyDictionary`**: A dictionary from the `weakref` module that removes objects when no other references to them exist. Historically used in descriptors to prevent memory leaks.
- **`__getattr__`**: An object hook called *only* when an attribute cannot be found in an object's instance dictionary. Used for lazy loading.
- **`__getattribute__`**: An object hook called *every time* an attribute is accessed on an object, even if it already exists.
- **`__setattr__`**: An object hook called *every time* an attribute is assigned on an instance.
- **`__init_subclass__`**: A special class method (Python 3.6+) called when a class is subclassed. Used for class validation or registration without metaclasses.
- **`__set_name__`**: A special descriptor method (Python 3.6+) called on every descriptor instance when its containing class is defined, receiving the class and the assigned attribute name.
- **Class Decorator**: A function applied with the `@` prefix before a class declaration that receives the class instance and returns a modified or new class.
- **Metaclass**: A class inheriting from `type` that intercepts the `class` statement to modify class creation. Largely superseded by `__init_subclass__` and class decorators.

# @Objectives
- Ensure classes expose simple public attributes by default rather than using explicit getter/setter methods.
- Abstract reusable, memory-safe attribute validation and logic across unrelated classes using descriptors and `__set_name__`.
- Implement lazy or dynamic attribute resolution safely, strictly avoiding infinite recursion.
- Validate and register subclasses implicitly and reliably at definition time using `__init_subclass__` instead of complex metaclasses.
- Extend and modify class behaviors composably using class decorators to prevent metaclass conflicts.

# @Guidelines
- **Attributes vs Methods**: Start implementations with simple public attributes. NEVER implement explicit setter or getter methods (e.g., `get_value()` or `set_value()`).
- **Property Transitions**: Use `@property` to transition simple numerical or data attributes into on-the-fly calculations if special behavior is required, ensuring existing calling code does not break.
- **Property Setters**: Use `@property.setter` methods to perform type checking, validation, or to enforce immutability on parent class attributes (by raising `AttributeError`).
- **Property Anti-patterns**: NEVER set other attributes or modify unrelated object state inside a getter `@property` method. Modify related object state ONLY in `@property.setter` methods.
- **Property Performance**: Ensure `@property` methods execute extremely fast. NEVER execute I/O, database queries, slow helper functions, or complex side effects inside them. Use normal methods for slow operations.
- **Refactoring Properties**: Do NOT overuse `@property`. If you find yourself repeatedly extending `@property` methods or adding complex logic, refactor the class to use normal methods or a better data model instead.
- **Descriptors for Reuse**: Use descriptor classes (implementing `__get__` and `__set__`) to reuse `@property` logic and validation across multiple attributes or unrelated classes.
- **Descriptor State (`__set_name__`)**: ALWAYS define `__set_name__` on descriptor classes to capture the assigned attribute name. Store the descriptor's manipulated data directly within the class's instance dictionary using `getattr(instance, self.internal_name)` and `setattr(instance, self.internal_name, value)`. This prevents memory leaks natively.
- **Descriptor State (Legacy)**: Only if supporting legacy Python (pre-3.6) without `__set_name__`, use `WeakKeyDictionary` to store per-instance state inside the descriptor to prevent memory leaks. NEVER use a standard dictionary for per-instance state in a descriptor.
- **Lazy Attributes**: Use `__getattr__` to lazily load attributes (e.g., from a schemaless database record). It is invoked only when an attribute is missing.
- **Dynamic Attributes**: Use `__getattribute__` only if you must execute logic on *every* attribute access (e.g., checking global transaction state). Be extremely cautious of the severe performance overhead this incurs.
- **Avoiding Recursion**: Inside `__getattr__`, `__getattribute__`, and `__setattr__`, ALWAYS use `super().__getattr__(name)`, `super().__getattribute__(name)`, and `super().__setattr__(name, value)` to access or modify the instance dictionary. NEVER use `self.attribute` or `self.__dict__` directly, as it will trigger an infinite recursion loop and crash the program.
- **Missing Attributes**: Raise `AttributeError` inside `__getattr__` and `__getattribute__` when a dynamically accessed property is missing or invalid.
- **Subclass Validation**: ALWAYS use `__init_subclass__` to validate subclasses at the time they are defined. Avoid using a metaclass `__new__` method for validation.
- **Subclass Registration**: ALWAYS use `__init_subclass__` to automatically register subclasses (e.g., for serialization, ORMs, plugins) to ensure registration is never accidentally omitted.
- **Super in `__init_subclass__`**: ALWAYS call `super().__init_subclass__()` inside your `__init_subclass__` definition to support multiple layers of validation and diamond inheritance.
- **Class Extensions**: Prefer class decorators over metaclasses for modifying every method or attribute of a class (e.g., adding tracing or logging). Class decorators are composable, whereas multiple metaclasses throw `TypeError` conflicts.

# @Workflow
1. **Attribute Definition**: Define object state using plain public attributes in `__init__`.
2. **Behavior Addition**: If validation, logging, or calculation is needed upon attribute access later, convert the plain attribute to a `@property` and `@property.setter`, keeping the exact same public name.
3. **Logic Abstraction**: If the `@property` logic is repeated across multiple attributes or classes, abstract it into a generic Descriptor class.
4. **Descriptor Implementation**: Implement `__get__`, `__set__`, and `__set_name__` on the Descriptor. In `__set_name__`, prefix the attribute name (e.g., `'_' + name`) and store values in `__set__` using `setattr(instance, self.internal_name, value)`.
5. **Dynamic/Lazy Loading**: If attributes must be loaded dynamically (e.g., database rows), implement `__getattr__`. Route internal state lookups through `super().__getattr__` to avoid recursion.
6. **Hierarchy Validation/Registration**: If creating a base class where all subclasses must be validated or registered, implement `__init_subclass__(cls)` on the base class. Call `super().__init_subclass__()` as the first line of the method, then apply the logic.
7. **Class Modification**: If altering or wrapping all methods of a class, write a class decorator function and apply it with `@decorator_name` above the `class` definition instead of using a metaclass.

# @Examples (Do's and Don'ts)

**Properties vs Explicit Getter/Setter Methods**
- [DON'T] Use Java-style getter and setter methods:
  ```python
  class Resistor:
      def __init__(self, ohms):
          self._ohms = ohms
      def get_ohms(self):
          return self._ohms
      def set_ohms(self, ohms):
          if ohms <= 0:
              raise ValueError('ohms must be > 0')
          self._ohms = ohms
  ```
- [DO] Use simple attributes, upgrading to `@property` when validation is needed:
  ```python
  class Resistor:
      def __init__(self, ohms):
          self.ohms = ohms  # Triggers setter
      
      @property
      def ohms(self):
          return self._ohms
          
      @ohms.setter
      def ohms(self, ohms):
          if ohms <= 0:
              raise ValueError('ohms must be > 0')
          self._ohms = ohms
  ```

**Property Side Effects**
- [DON'T] Modify unrelated object state inside a getter property:
  ```python
  @property
  def ohms(self):
      self.voltage = self._ohms * self.current # Bizarre side effect!
      return self._ohms
  ```
- [DO] Modify related state only inside the setter:
  ```python
  @voltage.setter
  def voltage(self, voltage):
      self._voltage = voltage
      self.current = self._voltage / self.ohms # Expected side effect
  ```

**Descriptors and Memory Leaks**
- [DON'T] Store per-instance state in a descriptor's standard dictionary (causes memory leaks):
  ```python
  class Grade:
      def __init__(self):
          self._values = {} # Leaks memory!
      def __set__(self, instance, value):
          self._values[instance] = value
  ```
- [DO] Use `__set_name__` and store the state directly on the instance:
  ```python
  class Grade:
      def __set_name__(self, owner, name):
          self.internal_name = '_' + name
          
      def __get__(self, instance, instance_type):
          if instance is None:
              return self
          return getattr(instance, self.internal_name, 0)
          
      def __set__(self, instance, value):
          if not (0 <= value <= 100):
              raise ValueError('Grade must be between 0 and 100')
          setattr(instance, self.internal_name, value)
  ```

**Dynamic Attribute Recursion**
- [DON'T] Access instance attributes directly inside `__getattribute__`:
  ```python
  class BrokenDictionaryRecord:
      def __init__(self, data):
          self._data = data
      def __getattribute__(self, name):
          # Infinite recursion! Accesses self._data, triggering __getattribute__ again
          return self._data[name] 
  ```
- [DO] Use `super().__getattribute__` to safely bypass the hook:
  ```python
  class DictionaryRecord:
      def __init__(self, data):
          self._data = data
      def __getattribute__(self, name):
          data_dict = super().__getattribute__('_data')
          return data_dict[name]
  ```

**Subclass Validation and Registration**
- [DON'T] Use a metaclass (`__new__`) to validate or register subclasses:
  ```python
  class ValidatePolygon(type):
      def __new__(meta, name, bases, class_dict):
          if bases and class_dict.get('sides', 0) < 3:
              raise ValueError('Polygons need 3+ sides')
          return type.__new__(meta, name, bases, class_dict)
          
  class Polygon(metaclass=ValidatePolygon):
      sides = None
  ```
- [DO] Use `__init_subclass__` for clear, composable validation/registration:
  ```python
  class Polygon:
      sides = None
      
      def __init_subclass__(cls):
          super().__init_subclass__()
          if cls.sides < 3:
              raise ValueError('Polygons need 3+ sides')
  ```

**Class Extensions**
- [DON'T] Use a metaclass to modify all methods in a class, which breaks if the class needs multiple metaclasses:
  ```python
  class TraceMeta(type):
      def __new__(meta, name, bases, class_dict): ... # Wrap methods
      
  class TraceDict(dict, metaclass=TraceMeta):
      pass
  ```
- [DO] Use a class decorator to composably modify the class:
  ```python
  def trace(klass):
      for key in dir(klass):
          # Wrap methods...
          pass
      return klass

  @trace
  class TraceDict(dict):
      pass
  ```