@Domain
These rules trigger when the AI is writing, refactoring, or reviewing Python code involving object assignment, variable scoping, equality versus identity checking, collection copying, function parameter definitions (especially default values), class initialization with mutable arguments, and memory management/garbage collection.

@Vocabulary
- **Variable as Label**: In Python, variables are not boxes that contain data; they are labels (or sticky notes) bound to objects. 
- **Binding**: The process of attaching a variable name (label) to an object. Objects are created before variables are bound to them.
- **Alias**: Two or more variables bound to the exact same object in memory.
- **Identity**: The unique, unchanging integer label of an object, conceptually its memory address (retrieved via `id()`, compared via `is`).
- **Equality**: The evaluation of the data/value an object holds (compared via `==`, evaluated via the `__eq__` method).
- **Relative Immutability**: The characteristic of tuples where their physical contents (the references they hold) are strictly immutable, but the values of the objects they reference can change if those objects are mutable.
- **Shallow Copy**: A duplicate of an outermost container, filled with references to the exact same items held by the original container. Created via type constructors (e.g., `list()`), slicing (`[:]`), or `copy.copy()`.
- **Deep Copy**: A duplicate of an object and all of its nested objects, gracefully handling cyclic references. Created via `copy.deepcopy()`.
- **Call by Sharing**: Python's parameter passing mode where formal parameters inside a function become aliases of the actual arguments provided by the caller.
- **Garbage Collection**: The process of discarding objects when they become unreachable (primarily via reference counting in CPython, supplemented by generational garbage collection for cyclic references).
- **Interning**: An undocumented Python optimization technique where certain immutable objects (like short strings, small integers, or empty tuples) are shared across variables to save memory.

@Objectives
- Prevent subtle state-corruption bugs caused by unintended aliasing of mutable objects.
- Ensure the safe design of function signatures by strictly avoiding mutable default arguments.
- Protect class boundaries by enforcing defensive programming when accepting mutable arguments.
- Guarantee correct comparison semantics by strictly separating identity checks (`is`) from value checks (`==`).
- Ensure safe resource management by avoiding manual destruction (`__del__`) and relying on context managers instead.

@Guidelines
- **Variables and Assignment**: The AI MUST treat assignment (`=`) as binding a label to an object, not copying data. The AI MUST recognize that assigning an existing variable to a new variable creates an alias.
- **Identity vs. Equality**: 
  - The AI MUST use `==` to compare object values.
  - The AI MUST use `is` ONLY to check object identity, specifically when comparing to singletons like `None` (`x is None`, `x is not None`) or custom sentinel objects (e.g., `END_OF_DATA = object()`).
  - The AI MUST NOT use `is` to compare strings, integers, or tuples, as relying on Python's interning optimization is dangerous and unpredictable.
- **Tuple Immutability**: The AI MUST account for relative immutability. If a tuple contains mutable objects (e.g., a list), the AI MUST recognize that the tuple's overall value can change, making it unhashable and unsuitable for dictionary keys or set elements.
- **Copying Collections**: 
  - The AI MUST use shallow copies (`list(x)`, `x[:]`, `copy.copy(x)`) ONLY when the collection contains exclusively immutable items or when sharing nested mutable items is explicitly desired.
  - The AI MUST use `copy.deepcopy(x)` when duplicating collections of mutable objects where complete independence between the copy and the original is required.
- **Function Parameter Defaults**: The AI MUST NEVER use mutable objects (like `list`, `dict`, `set`, or user-defined instances) as default values in function or method signatures. The AI MUST use `None` as the default and instantiate the mutable object inside the function body.
- **Defensive Parameter Passing (Constructors & Methods)**: When a function or class initializer receives a mutable parameter (like a list) and stores it as an attribute or modifies it, the AI MUST create a local copy of the parameter (e.g., `self.items = list(passed_items)`) to prevent unintended mutation of the caller's object. Do not simply assign `self.items = passed_items` unless the explicit goal is to share state with the caller.
- **Object Destruction**: The AI MUST recognize that `del x` deletes the reference label `x`, not the object itself. 
  - The AI MUST NOT implement the `__del__` special method for releasing resources. 
  - The AI MUST use context managers (`with` statements) for deterministic cleanup of external resources (like files or network connections).
- **Augmented Assignment (+vs +=)**: The AI MUST recognize that `+=` modifies mutable objects in place but creates entirely new objects for immutable types. The AI MUST NOT implement in-place operators (like `__iadd__`) for immutable types.

@Workflow
1. **Scope and Aliasing Analysis**: When analyzing or generating code that modifies a collection or object, trace the references. Determine if the object is aliased elsewhere and if in-place modification will cause unintended side effects.
2. **Comparison Audit**: Scan conditionals. Convert any `is` or `is not` operators to `==` or `!=` unless the right-hand operand is `None` or a known singleton/sentinel.
3. **Parameter Default Sanitization**: Check every function and method definition. If a default argument is `[]`, `{}`, or `set()`, immediately rewrite the signature to default to `None` and add an `if arg is None: arg = []` initialization block inside the body.
4. **Defensive Storage Check**: Whenever an object receives a collection from a caller and assigns it to an instance attribute (`self.collection = collection`), evaluate if the class mutates this collection later. If yes, rewrite the assignment to instantiate a copy (`self.collection = list(collection)`).
5. **Copy Depth Selection**: When copying objects, explicitly decide between shallow and deep copy based on the mutability of the nested elements. Import the `copy` module if nested isolation is required.
6. **Resource Cleanup Verification**: Ensure no `__del__` methods are generated for resource management. Replace any such logic with a class implementing `__enter__` and `__exit__`.

@Examples (Do's and Don'ts)

**Function Parameter Defaults**
- [DO] Use `None` as a default for mutable arguments.
  ```python
  class Bus:
      def __init__(self, passengers=None):
          if passengers is None:
              self.passengers = []
          else:
              self.passengers = list(passengers)
  ```
- [DON'T] Use mutable instances as defaults, which creates a shared state across all invocations.
  ```python
  class HauntedBus:
      def __init__(self, passengers=[]):  # ANTI-PATTERN
          self.passengers = passengers
  ```

**Defensive Parameter Assignment**
- [DO] Make a copy of the passed mutable argument if the class will modify it, protecting the caller's data.
  ```python
  class TwilightBus:
      def __init__(self, passengers=None):
          if passengers is None:
              self.passengers = []
          else:
              self.passengers = list(passengers)  # DO: Creates a local copy
              
      def drop(self, name):
          self.passengers.remove(name)
  ```
- [DON'T] Alias a passed mutable argument, causing internal class operations to inadvertently mutate the caller's original collection.
  ```python
  class TwilightBus:
      def __init__(self, passengers=None):
          if passengers is None:
              self.passengers = []
          else:
              self.passengers = passengers  # ANTI-PATTERN: Aliases the caller's list
  ```

**Identity vs. Equality**
- [DO] Use `is` for singletons and sentinels, and `==` for values.
  ```python
  END_OF_DATA = object()
  
  if node is END_OF_DATA:
      break
  if x is not None:
      process(x)
  if user_input == "yes":
      continue
  ```
- [DON'T] Use `is` to compare values, relying on CPython interning optimizations.
  ```python
  if user_input is "yes":  # ANTI-PATTERN
      continue
  ```

**Tuple Relative Immutability**
- [DO] Understand that appending to a mutable item inside a tuple alters the tuple's value, making it unhashable.
  ```python
  t = (1, 2, [30, 40])
  t[-1].append(99)
  # t is now (1, 2, [30, 40, 99])
  ```
- [DON'T] Perform augmented assignment on a mutable item within a tuple, as it results in a successful mutation followed by a confusing `TypeError`.
  ```python
  t = (1, 2, [30, 40])
  t[2] += [50, 60]  # ANTI-PATTERN: Mutates the list but raises TypeError
  ```

**Resource Management**
- [DO] Use context managers for deterministic teardown.
  ```python
  with open('test.txt', 'wt', encoding='utf-8') as fp:
      fp.write('1, 2, 3')
  ```
- [DON'T] Rely on `del` or `__del__` to close files or clean up connections.
  ```python
  fp = open('test.txt', 'wt', encoding='utf-8')
  fp.write('1, 2, 3')
  del fp  # ANTI-PATTERN: Does not guarantee immediate closure in all environments
  ```