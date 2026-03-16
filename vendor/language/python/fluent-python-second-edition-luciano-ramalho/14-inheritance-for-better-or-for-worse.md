# @Domain
These rules MUST be triggered whenever the AI is tasked with creating, modifying, reviewing, or refactoring Python object-oriented code, specifically involving class hierarchies, subclassing, multiple inheritance, mixin classes, overriding methods, or creating custom collection types (e.g., custom dictionaries, lists, or strings).

# @Vocabulary
- **MRO (Method Resolution Order)**: The tuple stored in the `__mro__` attribute of a class, defining the search path Python uses to resolve method calls across the inheritance graph, computed via the C3 algorithm.
- **Cooperative Method**: A method in a multiple inheritance hierarchy that explicitly calls `super()` to yield control to the next class in the MRO, preventing execution sequence failures.
- **Mixin Class**: A class designed to be subclassed together with at least one other class to provide specific, reusable method implementations, without implying an "is-a" relationship or holding internal instance state.
- **Aggregate Class**: An empty or near-empty class constructed primarily by inheriting from mixins and abstract base classes to bundle them together into a convenient, user-facing entity.
- **Interface Inheritance**: Subclassing primarily to define a subtype that fulfills a specific API contract, best implemented using Abstract Base Classes (ABCs) or `typing.Protocol`.
- **Implementation Inheritance**: Subclassing primarily to avoid code duplication by reusing logic from a superclass.
- **Late Binding**: The principle where the exact method to be called is determined at runtime based on the class of the receiver (`self`).

# @Objectives
- Prevent subtle, hard-to-diagnose bugs caused by the C-level implementation of Python's built-in types ignoring method overrides.
- Ensure that multiple inheritance graphs resolve cleanly and predictably by enforcing cooperative methods and strict MRO positioning.
- Reduce tight coupling and system brittleness by favoring object composition over inheritance.
- Clarify the intent of inheritance (interface vs. implementation) by strictly separating Abstract Base Classes from Mixin classes.

# @Guidelines
- **Favor Composition Over Inheritance**: The AI MUST initially evaluate if the desired functionality can be achieved by an object holding a reference to a component and delegating to it, rather than inheriting from it.
- **Never Subclass Built-ins Directly**: The AI MUST NOT subclass `dict`, `list`, or `str` directly when creating custom collections. Built-in methods written in C bypass user-defined overrides. The AI MUST subclass `collections.UserDict`, `collections.UserList`, or `collections.UserString` instead.
- **Always Use `super()`**: When overriding a method, the AI MUST use `super().method_name()` to call the superclass method. The AI MUST NOT hardcode the base class name (e.g., `BaseClass.method_name(self)`), as this breaks the MRO in multiple inheritance.
- **Omit Arguments in `super()`**: The AI MUST use the zero-argument form of `super()` (available in Python 3) unless specifically required to skip part of the MRO for debugging or specialized workarounds.
- **Write Cooperative Methods**: In any non-root class participating in multiple inheritance, every overridden method MUST call `super().method_name()` to ensure the next class in the MRO receives the method call.
- **Mixin Naming Convention**: The AI MUST append the suffix `Mixin` to the name of any class designed to provide reusable implementation methods without acting as a primary base class.
- **Stateless Mixins**: The AI MUST NOT define instance attributes or internal state (e.g., no `__init__` assigning `self.x`) within a Mixin class.
- **Mixin MRO Placement**: When declaring a class that uses a Mixin, the AI MUST place the Mixin class first in the tuple of base classes (e.g., `class MyClass(MyMixin, BaseClass):`) so its methods are encountered first in the MRO.
- **Avoid Subclassing Concrete Classes**: The AI MUST ensure that classes intended to act as superclasses are abstract (ABCs) or Mixins. "All non-leaf classes should be abstract."
- **Use `@final` for Protection**: The AI MUST use the `@final` decorator (from `typing`) on classes or methods that are not designed to be safely subclassed or overridden.

# @Workflow
1. **Analyze Inheritance Intent**: Determine if the requested subclassing is for Interface (requires ABC/Protocol), Implementation (requires Mixins), or both.
2. **Composition Check**: Before writing a subclass, explicitly evaluate and prefer object composition and delegation if it satisfies the requirement.
3. **Select Base Classes Safely**: If subclassing a standard collection, import `collections` and select the appropriate `User*` wrapper class instead of the native C built-in.
4. **Define Mixins**: If extracting reusable logic, isolate it into a stateless class named `*Mixin`.
5. **Construct the Subclass**: 
   - Order the base classes strictly: Mixins first, followed by the primary base class or Aggregate class.
   - Override necessary methods.
6. **Implement Cooperative Delegation**: Inject `super().<method_name>()` into overridden methods to ensure MRO propagation.

# @Examples (Do's and Don'ts)

### Subclassing Collections
- **[DO]**
  ```python
  import collections

  class DoppelDict(collections.UserDict):
      def __setitem__(self, key, value):
          super().__setitem__(key, [value] * 2)
  ```
- **[DON'T]**
  ```python
  class DoppelDict(dict):  # Anti-pattern: built-in dict will ignore __setitem__ in update()
      def __setitem__(self, key, value):
          super().__setitem__(key, [value] * 2)
  ```

### Calling Superclass Methods
- **[DO]**
  ```python
  class LastUpdatedOrderedDict(OrderedDict):
      def __setitem__(self, key, value):
          super().__setitem__(key, value)
          self.move_to_end(key)
  ```
- **[DON'T]**
  ```python
  class LastUpdatedOrderedDict(OrderedDict):
      def __setitem__(self, key, value):
          OrderedDict.__setitem__(self, key, value) # Anti-pattern: hardcodes base class, breaks MRO
          self.move_to_end(key)
  ```

### Using Mixin Classes
- **[DO]**
  ```python
  class UpperCaseMixin:  # No __init__, no state
      def __setitem__(self, key, item):
          super().__setitem__(key.upper(), item)

  class UpperDict(UpperCaseMixin, collections.UserDict): # Mixin placed first
      pass
  ```
- **[DON'T]**
  ```python
  class UpperCase:
      def __init__(self):
          self.is_upper = True  # Anti-pattern: Mixin holds state

      def __setitem__(self, key, item):
          collections.UserDict.__setitem__(self, key.upper(), item)

  class UpperDict(collections.UserDict, UpperCase): # Anti-pattern: Mixin placed after base class
      pass
  ```

### Object Composition over Inheritance
- **[DO]**
  ```python
  class CustomWidget:
      def __init__(self):
          self.geometry_manager = GridManager() # Delegation
      
      def arrange(self):
          self.geometry_manager.apply(self)
  ```
- **[DON'T]**
  ```python
  class CustomWidget(BaseWidget, GridManager, PackManager): # Anti-pattern: Inheriting implementation instead of delegating
      def arrange(self):
          self.apply_grid()
  ```