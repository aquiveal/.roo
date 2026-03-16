# @Domain
This rule file is triggered when the AI performs tasks related to Python class metaprogramming. This includes dynamic class generation at runtime, modifying class definitions programmatically, defining or troubleshooting class decorators, utilizing the `__init_subclass__` hook, authoring custom metaclasses, dynamically generating `__slots__`, or resolving method resolution order (`__mro__`) and metaclass conflicts.

# @Vocabulary
- **Class Metaprogramming**: The art of creating or customizing classes at runtime.
- **Metaclass**: A class factory. A class whose instances are classes. In Python, the default metaclass is `type`.
- **Class Factory**: A function that constructs and returns a class dynamically (typically invoking `type(name, bases, dict)`).
- **Class Decorator**: A callable taking a class as an argument and returning a class (often the same class, mutated), executed immediately after the class is built by `type.__new__`.
- **`__init_subclass__`**: A special method called upon the superclass when a subclass of the current class is defined.
- **`__prepare__`**: A special class method on metaclasses invoked before the class body is evaluated, returning a mapping to hold the class namespace.
- **`cls_dict`**: The namespace mapping of the class under construction, passed to the metaclass `__new__` method.
- **Import Time**: The phase when the interpreter parses source code, compiles bytecode, and executes the top-level code (including class statements, decorators, and metaclass execution).

# @Objectives
- Employ the Principle of Least Astonishment and favor the simplest metaprogramming mechanisms available (i.e., prefer `__init_subclass__` or class decorators over custom metaclasses).
- Enforce strict adherence to Python's class construction evaluation order.
- Safely manage dynamic class attributes, taking special care with structural constraints like `__slots__`.
- Prevent and resolve metaclass conflicts in complex inheritance hierarchies.

# @Guidelines
- **Simplicity First**: For general application code, the AI MUST strongly discourage metaclasses and suggest modern alternatives like `@dataclass`, `typing.NamedTuple`, `__init_subclass__`, or class decorators. Metaclasses MUST be reserved for framework-level infrastructure.
- **Dynamic Class Creation**: When generating classes dynamically within a function (Class Factory), the AI MUST use the built-in `type(cls_name, bases, cls_attrs)` constructor.
- **Implementing `__init_subclass__`**:
  - The AI MUST name the first argument `subclass` (not `cls`, because the argument is the newly defined subclass, not the class where the method is implemented).
  - The AI MUST call `super().__init_subclass__()` to ensure cooperative multiple inheritance does not break.
- **Configuring `__slots__` Dynamically**:
  - The AI MUST NOT attempt to dynamically configure `__slots__` using `__init_subclass__` or a class decorator, as these execute *after* the class has been built by `type.__new__` (rendering `__slots__` assignments ineffective).
  - To dynamically configure `__slots__`, the AI MUST modify the class namespace (`cls_dict`) inside a metaclass `__new__` method, or construct the class via a class factory function passing `__slots__` into `type()`.
- **Implementing Metaclasses**:
  - A custom metaclass MUST inherit from `type`.
  - When implementing the metaclass `__new__` method, the AI MUST name the first argument `meta_cls` (or `mcs`), followed by `cls_name`, `bases`, and `cls_dict`.
  - The AI MUST return `super().__new__(meta_cls, cls_name, bases, cls_dict)` to construct the class.
  - When implementing `__prepare__`, the AI MUST decorate it with `@classmethod` and MUST return a mapping object (e.g., `dict`, `UserDict`, or a custom mapping).
- **Evaluation Order Awareness**: The AI MUST design metaprogramming logic assuming the exact following sequence during class statement execution:
  1. `__prepare__` (on the metaclass)
  2. The class body is evaluated.
  3. `__new__` (on the metaclass)
  4. `__set_name__` (on any descriptors present in the class namespace)
  5. `__init_subclass__` (on the superclasses)
  6. Class decorators are applied.
- **Resolving Metaclass Conflicts**: If a `TypeError: metaclass conflict` is encountered, the AI MUST resolve it either by decoupling the class hierarchy to avoid multiple metaclasses, or by creating a new metaclass that explicitly inherits from all conflicting metaclasses.
- **Private Names in Class Decorators**: When a class decorator injects module-level functions into a decorated class as methods, the AI MUST prefix those module-level function names with an underscore (e.g., `_fields`) to minimize namespace pollution and naming conflicts.

# @Workflow
1. **Analyze Metaprogramming Requirements**: Determine the specific customization needed (e.g., injecting methods, verifying type hints, generating attributes, dynamically configuring `__slots__`).
2. **Tool Selection**:
   - If generating identical boilerplate classes on the fly -> Use a Class Factory function with `type()`.
   - If enforcing rules/injecting attributes onto subclasses -> Use `__init_subclass__`.
   - If mutating a class post-creation without affecting its inheritance tree -> Use a class decorator.
   - If (and only if) altering the class creation process itself (e.g., injecting `__slots__` before memory allocation) -> Use a metaclass.
3. **Implementing a Class Factory**:
   - Define closure functions for methods like `__init__`, `__repr__`.
   - Assemble a `cls_attrs` dictionary.
   - Return `type(cls_name, (object,), cls_attrs)`.
4. **Implementing `__init_subclass__`**:
   - Define `def __init_subclass__(subclass, **kwargs):`
   - Immediately call `super().__init_subclass__(**kwargs)`.
   - Apply mutations directly to the `subclass` object.
5. **Implementing a Metaclass**:
   - Define `class CustomMeta(type):`
   - To intercept namespace creation, implement `@classmethod def __prepare__(meta_cls, cls_name, bases): return {}`.
   - To modify class creation, implement `def __new__(meta_cls, cls_name, bases, cls_dict):`.
   - Mutate `cls_dict` as required (e.g., `cls_dict['__slots__'] = [...]`).
   - Conclude with `return super().__new__(meta_cls, cls_name, bases, cls_dict)`.

# @Examples (Do's and Don'ts)

## 1. Using `__init_subclass__`
- **[DO]** Use the `subclass` argument name and call `super()`.
```python
class Checked:
    def __init_subclass__(subclass, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        for name, constructor in get_type_hints(subclass).items():
            setattr(subclass, name, Field(name, constructor))
```
- **[DON'T]** Use `cls` as the first argument (it confuses the context since it acts on the subclass) or forget the `super()` call.
```python
class Checked:
    @classmethod
    def __init_subclass__(cls) -> None:  # Anti-pattern: @classmethod not needed, wrong argument name, no super()
        for name in cls._fields():
            ...
```

## 2. Dynamic `__slots__` Configuration
- **[DO]** Use a metaclass to inject `__slots__` into `cls_dict` before the class is built.
```python
class CheckedMeta(type):
    def __new__(meta_cls, cls_name, bases, cls_dict):
        if '__slots__' not in cls_dict:
            slots = []
            for name in cls_dict.get('__annotations__', {}):
                slots.append(f'_{name}')
            cls_dict['__slots__'] = slots
        return super().__new__(meta_cls, cls_name, bases, cls_dict)

class Checked(metaclass=CheckedMeta):
    __slots__ = ()
```
- **[DON'T]** Attempt to set `__slots__` in a class decorator or `__init_subclass__`.
```python
def add_slots(cls):
    cls.__slots__ = ['_title', '_year'] # Anti-pattern: Too late! The class __dict__ is already created.
    return cls
```

## 3. Metaclass Signature
- **[DO]** Use `meta_cls` in `__new__` to clearly designate the metaclass parameter.
```python
class MetaBunch(type):
    def __new__(meta_cls, cls_name, bases, cls_dict):
        # Configuration logic here
        return super().__new__(meta_cls, cls_name, bases, cls_dict)
```
- **[DON'T]** Use `self` or `cls` as the first argument in a metaclass `__new__` method, which obfuscates that the instance being created is a class and the first argument is the metaclass.

## 4. Class Factory
- **[DO]** Construct the class definition dict and use `type()`.
```python
def record_factory(cls_name: str, field_names: list[str]) -> type[tuple]:
    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)
            
    cls_attrs = {
        '__slots__': tuple(field_names),
        '__init__': __init__,
    }
    return type(cls_name, (object,), cls_attrs)
```
- **[DON'T]** Use `exec()` or `eval()` to parse string-based class definitions dynamically unless strictly necessary for compilation-level feature injection (like `namedtuple` used to do before it was refactored).