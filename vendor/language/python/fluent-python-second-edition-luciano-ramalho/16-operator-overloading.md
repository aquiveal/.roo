@Domain
Python object-oriented programming, specifically when defining custom classes that require operator overloading, emulating numeric/collection types, or implementing mathematical/algebraic behaviors.

@Vocabulary
- **Unary Operator**: An operator with a single operand, e.g., `-` (`__neg__`), `+` (`__pos__`), `~` (`__invert__`), and `abs()` (`__abs__`).
- **Infix Operator**: An operator placed between two operands, e.g., `+`, `-`, `*`, `/`, `@`.
- **Forward Method**: The special method called on the left-hand operand of an infix operator, e.g., `a.__add__(b)` for `a + b`.
- **Reverse (Reflected) Method**: The special method called on the right-hand operand when the left-hand operand does not support the operation, e.g., `b.__radd__(a)`.
- **In-place (Augmented Assignment) Operator**: Operators that combine an infix operation with assignment, e.g., `+=` (`__iadd__`), `*=` (`__imul__`).
- **Rich Comparison Operators**: Operators used for comparing objects: `==` (`__eq__`), `!=` (`__ne__`), `>` (`__gt__`), `<` (`__lt__`), `>=` (`__ge__`), `<=` (`__le__`).
- **NotImplemented**: A special Python singleton value returned by operator methods to signal to the interpreter that the method does not know how to handle the given operand type, triggering the interpreter's fallback/dispatch mechanisms.
- **Goose Typing**: A type-checking approach leveraging `isinstance` checks against abstract base classes (ABCs) from `collections.abc` or `numbers` rather than concrete classes.

@Objectives
- Ensure that operator overloading strictly adheres to Python's data model rules regarding object mutability, identity, and return types.
- Leverage Python's built-in dispatch algorithm by appropriately using `NotImplemented`.
- Prevent accidental mutation of operands during standard unary and infix operations.
- Ensure proper fallback logic for heterogeneous operand types using reverse methods.
- Provide idiomatic augmented assignment operations that differentiate between mutable and immutable classes.

@Guidelines
- **General Operator Limitations**: The AI MUST NOT attempt to redefine operators for built-in C-level types. The AI MUST NOT attempt to create entirely new operators. The AI MUST NOT attempt to overload `is`, `and`, `or`, and `not`.
- **Unary Operators**: The AI MUST implement unary operators (`__neg__`, `__pos__`, `__invert__`) such that they NEVER modify `self`. They MUST always create and return a new instance of a suitable type.
- **Infix Operators (Forward & Reverse)**:
  - Infix operators (e.g., `__add__`, `__mul__`, `__matmul__`) MUST NEVER modify `self` or `other`. They MUST return a new object.
  - The AI MUST implement reverse methods (e.g., `__radd__`, `__rmul__`) to support mixed-type operations. For commutative operations, the reverse method CAN simply delegate to the forward method (e.g., `return self + other`).
  - If a reverse method is implemented, and the forward method is designed to work *only* with operands of the same type as `self`, the reverse method is useless and MUST NOT be implemented.
- **Handling Type Incompatibilities**:
  - The AI MUST NOT raise a `TypeError` directly within an infix operator method when encountering an unsupported operand type.
  - Instead, the AI MUST return the `NotImplemented` singleton. If internal operations (like `zip_longest` or type conversions) raise a `TypeError`, the AI MUST catch the `TypeError` and return `NotImplemented`. This allows Python to attempt the reverse method on the other operand.
  - The AI MUST NOT confuse `NotImplemented` (a value to be returned) with `NotImplementedError` (an exception to be raised).
- **Goose Typing for Operands**: The AI SHOULD use Goose Typing (`isinstance(other, abc.Iterable)`, `isinstance(other, abc.Sized)`) rather than checking for exact concrete types (like `list` or `tuple`) when evaluating operand compatibility in complex operators like `__matmul__` (`@`).
- **Rich Comparisons**:
  - When implementing `__eq__`, if the `other` type is unrecognized or incompatible, the AI MUST return `NotImplemented`. Python will handle falling back to reverse comparisons and eventually object identity (`id(a) == id(b)`).
  - The AI MUST NOT implement `__ne__` unless absolutely necessary, as Python's object base class provides a default `__ne__` that automatically negates the result of `__eq__`.
- **Augmented Assignments**:
  - For **immutable** types, the AI MUST NOT implement in-place operator methods (`__iadd__`, `__imul__`). Python will naturally fallback to `a = a + b`.
  - For **mutable** types, the AI MUST implement in-place operator methods. These methods MUST modify `self` in-place and MUST return `self`.
  - The AI MUST note that in-place operators (like `+=`) can be more liberal with accepted types than their infix counterparts (like `+`). For example, `+` may require two objects of the exact same type, while `+=` may accept any iterable (similar to `list.extend`).

@Workflow
1. **Analyze the Class**: Determine if the target class is mutable or immutable.
2. **Implement Unary Operators**: If requested, implement `__neg__`, `__pos__`, etc., ensuring they return new instances.
3. **Implement Forward Infix Operators**: Write `__add__`, `__mul__`, etc. 
   - Apply Duck Typing (try/except `TypeError`) or Goose Typing (`isinstance` with `collections.abc`).
   - If type validation fails, return `NotImplemented`.
4. **Implement Reverse Infix Operators**: Write `__radd__`, `__rmul__`, etc., to handle cases where the left-hand operand returns `NotImplemented`.
5. **Implement Rich Comparisons**: Write `__eq__` (and others if needed). Ensure type checking is conservative enough to avoid false positives (e.g., comparing a custom Vector to a generic tuple), returning `NotImplemented` on failure.
6. **Implement Augmented Assignment**: If the class is mutable, write `__iadd__`, `__imul__`, etc. Mutate `self` and return `self`. If immutable, skip this step.

@Examples (Do's and Don'ts)

- **Infix Operators & Error Handling**
  - [DO] Catch TypeErrors and return NotImplemented:
    ```python
    def __add__(self, other):
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented
    ```
  - [DON'T] Raise TypeError directly for unsupported operands (breaks reverse dispatch):
    ```python
    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("unsupported operand type") # INCORRECT
        return Vector(...)
    ```

- **Rich Comparisons**
  - [DO] Return NotImplemented for unknown types and omit `__ne__`:
    ```python
    def __eq__(self, other):
        if isinstance(other, Vector):
            return len(self) == len(other) and all(a == b for a, b in zip(self, other))
        else:
            return NotImplemented
    # __ne__ is intentionally omitted
    ```
  - [DON'T] Return False for unknown types or manually implement redundant `__ne__`:
    ```python
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False # INCORRECT: Prevents Python from trying other.__eq__(self)
        return ...
    
    def __ne__(self, other):
        return not self == other # INCORRECT: Redundant, Python does this automatically
    ```

- **Augmented Assignment (Mutable Types)**
  - [DO] Mutate `self` and return `self`:
    ```python
    def __iadd__(self, other):
        if isinstance(other, MyMutableContainer):
            other_iterable = other.items()
        else:
            try:
                other_iterable = iter(other)
            except TypeError:
                raise TypeError("right operand in += must be iterable")
        
        self.load(other_iterable) # Mutates self
        return self               # MUST return self
    ```
  - [DON'T] Return a new object in an `__i*__` method for a mutable class, or forget to return `self`:
    ```python
    def __iadd__(self, other):
        self.load(other)
        # INCORRECT: missing `return self`
    ```

- **Augmented Assignment (Immutable Types)**
  - [DO] Rely on standard infix operators:
    ```python
    class MyImmutableVector:
        def __add__(self, other):
            return MyImmutableVector(...)
        # __iadd__ is intentionally omitted. Python will do a = a + b.
    ```
  - [DON'T] Implement `__iadd__` for immutable types.