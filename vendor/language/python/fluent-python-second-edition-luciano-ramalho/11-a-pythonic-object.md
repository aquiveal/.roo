# @Domain
Python class design, object-oriented programming, data model implementation, custom type formatting, object hashability, and memory optimization. These rules trigger when the AI is tasked with creating, refactoring, or optimizing user-defined Python classes, implementing dunder (special) methods, making objects behave like built-in types ("Pythonic" behavior), or addressing memory footprint issues with Python objects.

# @Vocabulary
- **Pythonic**: Designing user-defined types to behave as naturally as built-in types by implementing the appropriate special methods (dunder methods) of the Python Data Model.
- **Alternative Constructor**: A method designed to instantiate a class from different types of arguments than the primary `__init__` method, traditionally implemented using the `@classmethod` decorator.
- **Format Specification Mini-Language**: The extensible notation used in formatting specifiers (the part after the colon in f-strings or `format()` calls) that classes can parse via the `__format__` special method.
- **Name Mangling**: A safety mechanism in Python where attributes prefixed with two leading underscores (e.g., `__x`) are internally renamed to `_ClassName__x` to prevent accidental overwriting by subclasses.
- **Protected Attribute**: An attribute prefixed with a single underscore (e.g., `_x`), establishing a strong convention that it should not be accessed from outside the class, though not enforced by the compiler.
- **__slots__**: A class attribute containing a tuple of strings that optimizes memory by telling the interpreter to store instance attributes in a hidden array of references rather than a per-instance `__dict__`.
- **Virtual Attributes**: Attributes not explicitly declared in the source code or instance dictionary but computed on the fly via the `__getattr__` special method.

# @Objectives
- Ensure user-defined classes leverage the Python Data Model to behave seamlessly like built-in types.
- Provide comprehensive and standard-compliant object representations (`__repr__`, `__str__`, `__bytes__`, `__format__`).
- Accurately manage object mutability, hashability, and rich comparisons.
- Safely optimize memory usage for classes with millions of instances without breaking expected behaviors like weak references or dynamic attribute assignment.
- Enforce strict adherence to Pythonic conventions regarding class methods, static methods, and attribute access controls.

# @Guidelines
- **Object Representation**
  - The AI MUST implement `__repr__` to return a string that, whenever possible, matches the source code necessary to re-create the represented object (e.g., `return f'{type(self).__name__}({self.x!r}, {self.y!r})'`).
  - The AI MUST use the `!r` conversion flag in f-strings inside `__repr__` to ensure the standard representation of attribute values is displayed.
  - The AI MUST implement `__str__` to return a user-friendly string representation. If `__str__` is omitted, the AI MUST rely on the fallback to `__repr__`.
  - The AI MUST implement `__bytes__` if the object needs to be exported as a binary sequence.

- **Formatted Displays**
  - The AI MUST implement `__format__(self, fmt_spec='')` to support f-strings, the `format()` built-in, and `str.format()`.
  - If parsing a custom `fmt_spec`, the AI MUST avoid reusing format codes already supported by built-in types (e.g., avoid `e, E, f, F, g, G, n, %, b, c, d, o, x, X, s`).
  - If delegating formatting to built-in components, the AI MUST pass the `fmt_spec` down to those components using the `format()` built-in.

- **Constructors and Methods**
  - The AI MUST NOT use `@staticmethod` for alternative constructors.
  - The AI MUST use `@classmethod` for alternative constructors so the method receives the class (`cls`) as the first argument, allowing it to work correctly with subclasses.
  - The AI MUST restrict the use of `@staticmethod` to plain functions that merely happen to live in a class body; if the function does not need the class or instance, strongly consider moving it to the module level.

- **Hashability and Immutability**
  - If an object is intended to be hashable (usable in sets or as dict keys), the AI MUST make the object's fields read-only using the `@property` decorator.
  - The AI MUST implement `__hash__` to return an integer, typically by computing the hash of a tuple of the instance's attributes (e.g., `return hash((self.x, self.y))`) or using `functools.reduce` with `operator.xor` for multi-component objects.
  - The AI MUST implement `__eq__` alongside `__hash__`. Objects that compare equal MUST have the same hash code.

- **Dynamic Attributes and Protection**
  - If implementing `__getattr__` to provide virtual attributes, the AI MUST usually also implement `__setattr__` to prevent inconsistent behavior (e.g., preventing a user from assigning a value to a virtual attribute, which would inadvertently create an instance attribute that shadows `__getattr__`).
  - The AI MUST use a single leading underscore (e.g., `self._x`) to denote protected attributes by convention.
  - The AI MUST use double leading underscores (e.g., `self.__x`) ONLY to prevent accidental naming collisions in inheritance hierarchies (Name Mangling), recognizing it is a safety device, not a security mechanism.

- **Pattern Matching Support**
  - The AI MUST define a `__match_args__` class attribute (a tuple of strings) to enable positional pattern matching for the object's attributes.

- **Memory Optimization with __slots__**
  - The AI MUST ONLY use `__slots__` when dealing with a very large number of instances (e.g., millions).
  - When using `__slots__`, the AI MUST define it as a tuple of strings (e.g., `__slots__ = ('_x', '_y')`).
  - The AI MUST NOT use `__slots__` simply to prevent users from adding new attributes.
  - The AI MUST redeclare `__slots__` in every subclass; otherwise, the subclass will instantiate a `__dict__`, defeating the memory optimization.
  - If the class instances need to be targets of weak references, the AI MUST include `'__weakref__'` in the `__slots__` tuple.
  - If the class requires `@cached_property` or dynamic attributes alongside slotted attributes, the AI MUST include `'__dict__'` in the `__slots__` tuple, weighing the memory trade-offs.

- **Overriding Class Attributes**
  - The AI MUST NOT override class attributes by mutating the class attribute through an instance (e.g., `self.__class__.attr = X`).
  - To customize a class attribute, the AI MUST either set an instance attribute that shadows the class attribute for that specific instance, or create a subclass that overwrites the class attribute.

# @Workflow
1. **Initialization**: Define the class and `__init__` method. Coerce arguments to the expected types early to catch errors (fail-fast).
2. **Positional Matching**: Define `__match_args__` as a tuple of attribute names to support `match/case` positional matching.
3. **Representation**: Implement `__repr__` utilizing `type(self).__name__` so it survives subclassing, and `__str__` for human-readable output. 
4. **Byte Conversion**: Implement `__bytes__` if binary serialization is required.
5. **Alternative Construction**: Implement `frombytes` or other alternative constructors using `@classmethod` passing `cls` to create the instance.
6. **Formatting**: Implement `__format__` to parse the format specification mini-language and format the object's internal data accordingly.
7. **Immutability & Hashing**: If the object must be hashable, prefix internal data with `_` or `__`, expose them via `@property` getters, and implement `__hash__` and `__eq__`.
8. **Dynamic Access**: If providing dynamic attribute access via `__getattr__`, implement `__setattr__` to explicitly reject assignments to virtual attributes and maintain state consistency.
9. **Memory Profiling**: If and only if the class will have millions of instances, add `__slots__` containing the exact storage attribute names.

# @Examples (Do's and Don'ts)

### Alternative Constructors
**[DO]** Use `@classmethod` for alternative constructors.
```python
class Vector2d:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
```

**[DON'T]** Use `@staticmethod` or hardcode the class name for constructors.
```python
class Vector2d:
    @staticmethod
    def frombytes(octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return Vector2d(*memv)  # Breaks if subclassed!
```

### Hashability and Read-Only Properties
**[DO]** Use properties to make attributes read-only when making an object hashable.
```python
class Vector2d:
    __match_args__ = ('x', 'y')

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return tuple(self) == tuple(other)
```

**[DON'T]** Implement `__hash__` while leaving the attributes publicly mutable.
```python
class Vector2d:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __hash__(self):
        # DANGER: Mutable objects should not be hashable!
        return hash((self.x, self.y))
```

### Memory Optimization with `__slots__`
**[DO]** Declare `__slots__` as a tuple of strings for massive instantiation, remembering to include `__weakref__` if needed.
```python
class Pixel:
    __slots__ = ('x', 'y', '__weakref__')

    def __init__(self, x, y):
        self.x = x
        self.y = y

class ColorPixel(Pixel):
    # Subclasses MUST redeclare slots to prevent __dict__ creation
    __slots__ = ('color',)
```

**[DON'T]** Forget to redeclare `__slots__` in subclasses, or use lists for slots.
```python
class Pixel:
    __slots__ = ['x', 'y']  # Don't use a list

class ColorPixel(Pixel):
    pass  # DANGER: ColorPixel instances will now have a __dict__!
```

### Safe Dynamic Attributes
**[DO]** Pair `__getattr__` with `__setattr__` to prevent overriding virtual attributes.
```python
class Vector:
    __match_args__ = ('x', 'y', 'z', 't')

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        raise AttributeError(f'{cls.__name__!r} object has no attribute {name!r}')

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)
```

**[DON'T]** Implement `__getattr__` without guarding against assignment, which breaks consistency.
```python
class Vector:
    __match_args__ = ('x', 'y', 'z', 't')

    def __getattr__(self, name):
        # ... logic to return component ...
        pass

    # Missing __setattr__!
    # User does `v.x = 10`
    # Now `v.x` is a real attribute and bypasses __getattr__, desynchronizing the object.
```