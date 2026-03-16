# @Domain
This rule file is triggered whenever the AI is tasked with writing, refactoring, reviewing, or documenting Python code that involves function or class decorators, method definitions (instance, static, class, or abstract), class inheritance, or object-oriented interface design.

# @Vocabulary
- **Decorator**: A callable (function or class) that takes another function as an argument, extends or alters its behavior, and returns a new modified function.
- **Wrapper**: The inner function defined within a decorator that actually replaces the original function and accepts `*args, **kwargs`.
- **Class Decorator**: A decorator that acts on classes instead of functions, often used to dynamically set attributes or wrap classes in state-tracking objects.
- **Bound Method**: A method tied to an object instance; Python automatically passes the instance to the method's `self` parameter.
- **Unbound Method**: A method conceptually attached to the class but not an instance (in Python 3, essentially a standard function until bound).
- **Static Method**: A method decorated with `@staticmethod` that does not depend on the object's or class's state (does not take `self` or `cls`).
- **Class Method**: A method decorated with `@classmethod` that is bound to the class rather than the instance, receiving the class object (`cls`) as its first argument.
- **Abstract Method**: A method decorated with `@abc.abstractmethod` inside an Abstract Base Class (ABC). It enforces implementation in subclasses but can also contain default base implementations.
- **MRO (Method Resolution Order)**: The ordered list of parent classes that Python browses to resolve attribute and method lookups in multiple inheritance.
- **Super Object**: A proxy object instantiated by the `super()` constructor that delegates method calls to parent or sibling classes according to the MRO.
- **Descriptor Protocol**: The internal Python mechanism (via `__get__`) that allows objects like unbound `super` objects to resolve attributes dynamically when accessed.

# @Objectives
- Eradicate repetitive boilerplate code by aggressively factoring cross-cutting logic (e.g., access control, state management) into decorators.
- Ensure all decorated functions perfectly preserve their original metadata (names, docstrings) to maintain documentation generation and introspection.
- Accurately categorize and decorate class methods to maximize memory efficiency and clearly signal intent (static vs. class vs. instance).
- Establish rock-solid inheritance patterns by relying exclusively on dynamic MRO traversal rather than hardcoded parent class names.

# @Guidelines

## Decorator Implementation
- The AI MUST use decorators to factor out common code that runs before, after, or around multiple functions.
- The AI MUST define the inner wrapper function to accept `*args, **kwargs` to ensure signature compatibility.
- The AI MUST ALWAYS apply `@functools.wraps(f)` to the inner wrapper function to copy the `__name__` and `__doc__` attributes from the original function.
- When extracting specific arguments inside a decorator, the AI MUST use the `inspect` module (e.g., `inspect.getcallargs(f, *args, **kwargs)`) to reliably resolve arguments regardless of whether they were passed as positional or keyword arguments.
- When applying multiple decorators (stacking), the AI MUST account for the fact that decorators are applied bottom-up (closest to `def` applied first) but the wrappers execute top-down.
- The AI MAY use class decorators to factorize code that manipulates classes (e.g., automatically setting ID attributes) or to wrap functions to store complex persistent state (using `__init__` and `__call__`).

## Method Categorization and Decoration
- The AI MUST use `@staticmethod` for any method that does not access or modify `self` or `cls`. This prevents Python from needlessly instantiating bound methods, thereby saving memory and CPU cycles.
- The AI MUST use `@classmethod` when writing factory methods so that subclasses inheriting the factory correctly instantiate their own types, not the hardcoded parent type.
- The AI MUST define interfaces using the `abc` module (setting the metaclass to `abc.ABCMeta` and using `@abc.abstractmethod`).
- The AI MUST be aware that `@abc.abstractmethod` does not restrict subclasses from expanding the method signature (adding new arguments).
- When combining method decorators, the AI MUST place `@classmethod` or `@staticmethod` directly above `@abc.abstractmethod`.
- The AI MAY provide concrete default implementations inside an `@abc.abstractmethod`. Subclasses overriding the method can invoke this base logic using `super()`.

## Inheritance and Super()
- The AI MUST ALWAYS use `super()` to call parent class methods. The AI MUST NEVER hardcode a parent class name when overriding methods.
- In Python 3 code, the AI MUST use the zero-argument form of `super()` (i.e., `super().method()`), allowing Python to automatically inspect the stack frame to resolve the class and instance.

# @Workflow
1. **Analysis:** When writing a class method, analyze its internal logic.
2. **Classification:** 
   - If it uses `self`, leave it as an instance method.
   - If it only needs the class context (e.g., alternative constructors), apply `@classmethod` and use `cls`.
   - If it uses neither `self` nor `cls`, immediately apply `@staticmethod`.
   - If it defines a contract for subclasses, apply `@abc.abstractmethod`.
3. **Refactoring Repetition:** Identify repeated validation or setup/teardown logic across methods. Extract this logic into a decorator.
4. **Decorator Construction:** Build the decorator with an inner `wrapper(*args, **kwargs)`, decorate the wrapper with `@functools.wraps(original_func)`, and safely inspect arguments using the `inspect` module if specific parameter values are required.
5. **Inheritance Resolution:** When overriding a parent method, route the fallback or base behavior through `super().method_name()` to ensure cooperative multiple inheritance and MRO compliance.

# @Examples (Do's and Don'ts)

## Decorator Metadata
- **[DO]** Use `functools.wraps` to preserve function metadata:
  ```python
  import functools

  def check_access(f):
      @functools.wraps(f)
      def wrapper(*args, **kwargs):
          # Access check logic here
          return f(*args, **kwargs)
      return wrapper
  ```
- **[DON'T]** Return a wrapper without preserving metadata, which destroys docstrings:
  ```python
  def check_access(f):
      def wrapper(*args, **kwargs):
          return f(*args, **kwargs)
      return wrapper # BAD: Original name and docstring are lost
  ```

## Factory Methods
- **[DO]** Use `@classmethod` for factory methods to support inheritance:
  ```python
  class Pizza(object):
      def __init__(self, ingredients):
          self.ingredients = ingredients

      @classmethod
      def from_fridge(cls, fridge):
          return cls(fridge.get_cheese() + fridge.get_vegetables())
  ```
- **[DON'T]** Hardcode the class name in a static method factory, breaking subclassing:
  ```python
  class Pizza(object):
      @staticmethod
      def from_fridge(fridge):
          # BAD: Subclasses calling this will get a Pizza, not the subclass type
          return Pizza(fridge.get_cheese() + fridge.get_vegetables())
  ```

## Static Methods
- **[DO]** Apply `@staticmethod` if `self` is unused:
  ```python
  class MathUtils:
      @staticmethod
      def add(a, b):
          return a + b
  ```
- **[DON'T]** Leave it as an instance method if state isn't accessed (wastes memory instantiating bound methods):
  ```python
  class MathUtils:
      def add(self, a, b):
          return a + b # BAD: self is never used
  ```

## Implementations in Abstract Methods
- **[DO]** Provide base implementations in abstract methods and use `super()`:
  ```python
  import abc

  class BasePizza(metaclass=abc.ABCMeta):
      default_ingredients = ['cheese']

      @abc.abstractmethod
      def get_ingredients(self):
          return self.default_ingredients

      @classmethod
      def __subclasshook__(cls, C):
          return NotImplemented

  class DietPizza(BasePizza):
      def get_ingredients(self):
          # Extends the abstract method's base implementation
          return ['egg'] + super().get_ingredients()
  ```
- **[DON'T]** Assume abstract methods cannot contain code, or hardcode parent calls:
  ```python
  class DietPizza(BasePizza):
      def get_ingredients(self):
          return ['egg'] + BasePizza.get_ingredients(self) # BAD: Hardcoded parent
  ```