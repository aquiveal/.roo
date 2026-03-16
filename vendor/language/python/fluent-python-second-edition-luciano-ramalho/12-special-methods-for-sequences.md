@Domain
These rules trigger when the AI is tasked with creating, modifying, or refactoring custom Python sequence types, collections, or N-dimensional vector representations. It explicitly applies when implementing the Python sequence protocol (`__len__` and `__getitem__`), overloading slicing behavior, implementing dynamic attribute access (`__getattr__`), or implementing aggregation methods (`__hash__`, `__eq__`) for large or variable-length sequences.

@Vocabulary
- **Vector**: A user-defined sequence type representing multidimensional data (e.g., an N-dimensional Euclidean vector).
- **Sequence Protocol**: Python's informal interface (dynamic protocol) that requires a class to implement `__len__` and `__getitem__` to support iteration, indexing, slicing, and the `in` operator.
- **Protocol (Dynamic)**: An informal interface defined by convention, relying on duck typing (e.g., implementing `__getitem__` to act like a sequence).
- **Protocol (Static)**: A formalized interface defined by subclassing `typing.Protocol` to satisfy static type checkers.
- **Duck Typing**: Python's default typing behavior where an object is evaluated by the methods it implements (its behavior) rather than its inheritance lineage.
- **Goose Typing**: Explicit runtime type checking using Abstract Base Classes (ABCs), primarily utilizing `isinstance` against `collections.abc` classes.
- **Slice Object**: A built-in Python object `slice(start, stop, step)` that the interpreter passes to `__getitem__` when slice notation `seq[a:b:c]` is used.
- **Map-Reduce**: A computing pattern used in `__hash__` involving mapping a function to each item to generate a new series, then computing an aggregate result using a reducing function like `functools.reduce`.

@Objectives
- Seamlessly emulate standard Python immutable flat sequences using the sequence protocol.
- Guarantee memory-efficient and legible string representations for collections of arbitrary length.
- Ensure type-preserving slicing, meaning a slice of a custom sequence MUST return a new instance of that exact same custom sequence type.
- Safely expose dynamic attribute access without allowing users to silently shadow attributes and corrupt internal state.
- Optimize comparison and hashing operations to efficiently handle multi-dimensional or highly populated sequences without needlessly duplicating data in memory.

@Guidelines
- **Constructor Design**: Sequence constructors MUST take a single iterable argument to populate the sequence, mirroring built-in sequence types (like `list()` or `tuple()`), rather than accepting arbitrary positional arguments (`*args`).
- **Safe Representation (`__repr__`)**: When implementing `__repr__` for collections that can hold many items, the AI MUST use `reprlib.repr()` to abbreviate the string representation and prevent console flooding or log bloat.
- **Type-Preserving Slicing**: Inside `__getitem__`, the AI MUST check if the `key` argument is a `slice` object (`isinstance(key, slice)`). If it is, the method MUST return a new instance of the current class (`cls(self._components[key])`), preserving the object's type.
- **Index Validation**: When the `key` in `__getitem__` is not a slice, the AI MUST extract the index using `operator.index(key)` rather than an `isinstance(key, int)` check. This leverages duck typing and automatically raises a highly informative `TypeError` if the key is invalid.
- **Dynamic Attribute Read Access (`__getattr__`)**: If providing friendly shortcut names for sequence elements (e.g., `v.x`, `v.y`), implement `__getattr__`. The method MUST handle only the specific dynamic attributes intended, throwing an `AttributeError` for unknown names.
- **Dynamic Attribute Write Protection (`__setattr__`)**: Whenever `__getattr__` is implemented for dynamic attributes, the AI MUST also implement `__setattr__` to intercept assignments. This prevents users from writing `v.x = 10`, which would create an instance attribute that shadows the dynamic lookup and creates inconsistencies. Unhandled attributes MUST be delegated to `super().__setattr__(name, value)`.
- **Positional Pattern Matching**: If the class supports dynamic attributes representing specific positions (like `x` for index 0), the AI MUST define `__match_args__` as a class attribute tuple (e.g., `__match_args__ = ('x', 'y')`) to support Python 3.10+ positional pattern matching.
- **Efficient Hashing (`__hash__`)**: For multi-item collections, compute the hash by mapping `hash()` over the components and applying `functools.reduce` with `operator.xor`. Always provide `0` as the initializer (the third argument to `reduce`) to prevent exceptions on empty sequences.
- **Efficient Equality (`__eq__`)**: Do not convert entire sequences to tuples to compare them. The AI MUST first check if lengths match (`len(self) == len(other)`). If they do, use the `all()` built-in with `zip(self, other)` for memory-efficient, short-circuiting, item-by-item comparison.
- **Format Extensions (`__format__`)**: When extending the Format Specification Mini-Language, the AI MUST avoid reusing format codes already claimed by built-in types (e.g., avoid `e, E, f, F, g, G, n, %` for floats, or `s` for strings).

@Workflow
1. **Initialization**: Create `__init__` to accept a single `iterable` argument. Store the contents in an optimized internal flat sequence (e.g., `array.array`).
2. **Iteration**: Implement `__iter__` to yield elements from the internal structure.
3. **Representation**: Implement `__repr__` utilizing `reprlib.repr(self._components)` to safely format potentially massive arrays, extracting and formatting the abbreviated string appropriately.
4. **Sequence Protocol**: Implement `__len__` to return the size of the internal collection.
5. **Slicing**: Implement `__getitem__`. Route the logic: if `slice`, return a newly instantiated class wrapping the sliced internal array. Else, evaluate via `operator.index(key)` and return the discrete item.
6. **Dynamic Access (Optional)**: If element shortcuts are needed, implement `__getattr__` to map specific string names (e.g., 'x', 'y') to explicit indices.
7. **Consistency Enforcement**: Immediately implement `__setattr__` to catch and block assignments to the names defined in Step 6, raising an `AttributeError` to preserve immutability or mapping integrity.
8. **Hashing**: Implement `__hash__` using a generator expression inside `functools.reduce(operator.xor, hashes, 0)`.
9. **Equality**: Implement `__eq__` utilizing a type check or length check followed by `all(a == b for a, b in zip(self, other))`.

@Examples (Do's and Don'ts)

- **Initialization**
  - [DO]
    ```python
    def __init__(self, components):
        self._components = array(self.typecode, components)
    ```
  - [DON'T] Accept arbitrary positional arguments that break the standard sequence initialization pattern.
    ```python
    def __init__(self, *components): # Anti-pattern for sequences
        self._components = array(self.typecode, components)
    ```

- **Representation (`__repr__`)**
  - [DO] Use `reprlib` to prevent output explosion.
    ```python
    import reprlib
    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'Vector({components})'
    ```
  - [DON'T] Dump the raw structure directly.
    ```python
    def __repr__(self):
        return f'Vector({list(self._components)})' # Will freeze the console on large sequences
    ```

- **Slicing (`__getitem__`)**
  - [DO] Return a new instance of the class for slices, and use `operator.index`.
    ```python
    import operator
    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]
    ```
  - [DON'T] Return the internal storage object, or use `isinstance(key, int)` which breaks duck typing.
    ```python
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self._components[key] # Anti-pattern: Returns an array, not a Vector
        if isinstance(key, int):         # Anti-pattern: rejects valid index types
            return self._components[key]
    ```

- **Dynamic Attributes (`__getattr__` and `__setattr__`)**
  - [DO] Implement both to ensure read-only safety.
    ```python
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
  - [DON'T] Implement `__getattr__` without `__setattr__`, allowing users to shadow dynamic attributes.
    ```python
    def __getattr__(self, name):
        # Without __setattr__, `v.x = 10` succeeds and permanently breaks `v.x` lookups
        ...
    ```

- **Hashing and Equality**
  - [DO] Use `reduce` for hashing, and short-circuit evaluation for equality.
    ```python
    import functools
    import operator

    def __eq__(self, other):
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor, hashes, 0)
    ```
  - [DON'T] Duplicate the entire collection into memory just to compare or hash it.
    ```python
    def __eq__(self, other):
        return tuple(self) == tuple(other) # Horrible performance for N-dimensional vectors

    def __hash__(self):
        return hash(tuple(self)) # Excessive memory consumption
    ```