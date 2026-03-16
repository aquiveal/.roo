# @Domain

This rule file triggers when the AI is tasked with creating, refactoring, or evaluating custom Python classes, implementing custom collections, defining mathematical or numeric objects, handling object string representations, or working with Python's special methods (magic methods/dunder methods) to ensure classes are "Pythonic" and properly integrate with the Python Data Model.

# @Vocabulary

- **Python Data Model**: The API of the Python language itself that formalizes the interfaces of building blocks like sequences, functions, iterators, and classes.
- **Special Method**: A method invoked by the Python interpreter to perform basic object operations, often triggered by special syntax (e.g., `__getitem__` for `obj[key]`).
- **Magic Method**: Slang for special method.
- **Dunder Method**: A shortcut for "double underscore before and after." This is the correct way to pronounce and refer to special methods (e.g., `__getitem__` is pronounced "dunder-getitem").
- **PyVarObject / ob_size**: A C struct field underlying Python's variable-sized built-in collections (like `list`, `str`). `len()` reads this field directly for built-ins, making it drastically faster than a method call.
- **Infix Operator**: An operator placed between two operands (e.g., `+`, `*`). In Python, they are supported by specific dunder methods (e.g., `__add__`, `__mul__`).
- **Collection ABCs**: Abstract Base Classes (`Iterable`, `Sized`, `Container`) unified under the `Collection` ABC that define the essential interfaces every collection should implement.

# @Objectives

- Leverage the Python Data Model to make user-defined objects behave naturally and consistently like built-in types.
- Favor standard Python built-in functions (like `len()`, `iter()`, `str()`) and syntax over arbitrary custom method names (like `.size()`, `.length()`).
- Enable seamless integration with the Python standard library (e.g., `random.choice`, `sorted`, `reversed`) strictly by implementing the necessary dunder methods.
- Ensure proper object representations for both debugging and end-user display.
- Enforce the correct architectural patterns for mathematical and infix operators (immutability of operands).

# @Guidelines

- **General Special Method Usage**:
  - The AI MUST NOT invoke special methods directly in user code (e.g., do not write `my_obj.__len__()`). The AI MUST use the related built-in function (e.g., `len(my_obj)`).
  - The only common exception for direct special method invocation is calling `super().__init__()` inside a subclass's `__init__` method.
  - The AI MUST NOT invent new dunder names (e.g., `__foo__`). Any use of `__*__` names must strictly follow explicitly documented Python Data Model uses.

- **Emulating Collections**:
  - To make an object behave like a sequence, the AI MUST implement `__len__` and `__getitem__`.
  - The AI MUST rely on `__getitem__` to implicitly provide iteration (`for i in x`), the `in` operator (fallback sequential scan if `__contains__` is missing), and slicing.
  - The AI SHOULD delegate the work of `__len__` and `__getitem__` to standard built-in objects by using composition (e.g., delegating to a `list` stored as an instance attribute).
  - The AI MUST NOT create custom methods like `.pick_random()` if standard library functions like `random.choice(obj)` can be unlocked simply by implementing `__len__` and `__getitem__`.

- **String Representation (`__repr__` and `__str__`)**:
  - The AI MUST implement `__repr__` to return an unambiguous string that, if possible, matches the source code necessary to re-create the represented object.
  - When formatting attributes inside `__repr__`, the AI MUST use the `!r` conversion flag in f-strings (e.g., `f'Class({self.attr!r})'`) to ensure standard representation (e.g., distinguishing between strings and integers).
  - The AI MUST implement `__str__` to return a string suitable for display to end users.
  - If the AI can only implement one of these two methods, it MUST choose `__repr__`, because the fallback behavior of `__str__` is to call `__repr__`.

- **Truthiness and Boolean Value**:
  - To determine truthiness, the AI SHOULD implement `__bool__`, which MUST return a boolean explicitly.
  - If a custom conversion is complex, the AI MUST wrap the final return value in `bool()` to ensure the strict return type requirement is met (e.g., `return bool(abs(self))`).
  - If `__bool__` is not implemented, the AI MUST rely on the fallback behavior where Python tries to invoke `__len__` (0 evaluates to `False`, >0 to `True`).

- **Emulating Numeric Types and Operators**:
  - When implementing infix operators (e.g., `+` via `__add__`, `*` via `__mul__`), the AI MUST NOT modify the operands (`self` or `other`). 
  - Infix operator methods MUST create and return a brand new instance of the class containing the computed result.

# @Workflow

1. **Analyze the Object's Role**: Determine if the class acts as a collection/container, a mathematical/numeric type, or a standard data record.
2. **Implement Initialization & Representation**:
   - Write `__init__`.
   - Write `__repr__` using f-strings and the `!r` flag for all constructor-relevant attributes to output a string resembling the object's constructor call.
3. **Apply Collection Protocols** (If applicable):
   - Add `__len__` to return the size.
   - Add `__getitem__` to delegate item access to an internal collection.
   - Verify that this unlocks iteration, slicing, and standard library support (like `random.choice`). Do not write redundant custom methods for these.
4. **Apply Numeric Protocols** (If applicable):
   - Add `__abs__` for magnitude.
   - Add `__bool__` for truthiness (relying on `__abs__` or `__len__` if appropriate, ensuring explicit `bool()` casting).
   - Add mathematical dunder methods (`__add__`, `__mul__`). Ensure these methods instantiate and return new objects.
5. **Code Review against Data Model**: 
   - Scan code to ensure no dunder methods are explicitly called where built-ins should be used.
   - Scan for invented dunder names. Remove any undocumented `__*__` attributes.

# @Examples (Do's and Don'ts)

### Special Method Invocation
- **[DO]**
  ```python
  length = len(my_deck)
  first_item = my_deck[0]
  for item in my_deck:
      print(item)
  ```
- **[DON'T]**
  ```python
  length = my_deck.__len__()
  first_item = my_deck.__getitem__(0)
  iterator = my_deck.__iter__()
  ```

### String Representation (`__repr__`)
- **[DO]**
  ```python
  class Vector:
      def __init__(self, x, y):
          self.x = x
          self.y = y

      def __repr__(self):
          return f'Vector({self.x!r}, {self.y!r})'
  ```
- **[DON'T]**
  ```python
  class Vector:
      def __init__(self, x, y):
          self.x = x
          self.y = y
      
      # Fails to use !r, risking ambiguity between string '1' and int 1
      # Implements __str__ but neglects the more important __repr__
      def __str__(self):
          return f'Vector({self.x}, {self.y})'
  ```

### Emulating Collections
- **[DO]**
  ```python
  from random import choice

  class Deck:
      def __init__(self):
          self._cards = ['A', 'K', 'Q', 'J']

      def __len__(self):
          return len(self._cards)

      def __getitem__(self, position):
          return self._cards[position]

  # Let standard library handle it natively
  my_deck = Deck()
  random_card = choice(my_deck)
  ```
- **[DON'T]**
  ```python
  import random

  class Deck:
      def __init__(self):
          self._cards = ['A', 'K', 'Q', 'J']

      def get_size(self):
          return len(self._cards)

      def pick_random(self):
          return random.choice(self._cards)
  ```

### Infix Operators (`__add__`)
- **[DO]**
  ```python
  class Vector:
      def __init__(self, x, y):
          self.x = x
          self.y = y

      def __add__(self, other):
          # Returns a brand new instance
          return Vector(self.x + other.x, self.y + other.y)
  ```
- **[DON'T]**
  ```python
  class Vector:
      def __init__(self, x, y):
          self.x = x
          self.y = y

      def __add__(self, other):
          # Anti-pattern: Mutates operands instead of returning new object
          self.x += other.x
          self.y += other.y
          return self
  ```