# @Domain
Trigger these rules when processing Python files, analyzing algorithms, or refactoring code that involves sequence manipulation (lists, tuples, strings), iteration over data structures, sorting algorithms, and dictionary state management (including mapping operations and missing key handling).

# @Vocabulary
- **Sequence Slicing**: Extracting subsets of data using the `somelist[start:end]` syntax.
- **Stride**: The third parameter in a slicing operation `somelist[start:end:stride]` that dictates the step size.
- **Catch-All Unpacking**: Using a starred expression (`*variable`) within an assignment to capture all remaining unassigned elements of a sequence.
- **Stable Sorting**: Python's native `sort` behavior that preserves the relative order of elements that evaluate as equal.
- **Insertion Ordering**: The behavior standardized in Python 3.7+ where iterating over a standard `dict` yields keys in the exact order they were inserted.
- **Duck Typing**: Python's dynamic typing paradigm where an object's suitability is determined by the presence of certain methods (e.g., `MutableMapping`), rather than its actual class type.
- **Default Value Hook**: A callable passed to `collections.defaultdict` or logic implemented in a custom `__missing__` method to automatically generate values for missing dictionary keys.
- **Unicode Sandwich**: The architectural pattern of handling text encoding/decoding strictly at the program's boundaries, keeping internal operations as pure Unicode `str`.

# @Objectives
- Produce highly readable, visually clean Pythonic sequence manipulation code.
- Prevent subtle off-by-one errors and out-of-bounds index exceptions using Python's native syntax.
- Ensure safe memory utilization when unpacking iterators.
- Construct robust sorting logic using keys, lambda expressions, and Python's stable sort guarantees.
- Eliminate redundant dictionary access operations, side-effects, and superfluous object allocations when handling missing keys.
- Ensure algorithmic safety when dealing with dictionary-like duck-typed objects that may not guarantee insertion ordering.

# @Guidelines

## Sequence Slicing
- The AI MUST omit the `0` index when slicing from the beginning of a list (use `a[:5]`, not `a[0:5]`).
- The AI MUST omit the final index when slicing to the end of a list (use `a[5:]`, not `a[5:len(a)]`).
- The AI MUST use negative numbers for relative offsets from the end of a list.
- The AI MUST recognize that indexing a list by a negated variable (`somelist[-n:]`) creates a copy of the original list when `n` is `0`.
- The AI MUST NEVER combine `start`, `end`, and `stride` in a single slicing expression due to extreme visual noise and confusing behavior (especially with negative strides).
- If striding is required, the AI MUST use a positive stride and omit `start` and `end` indexes.
- If `start`, `end`, and `stride` are all required, the AI MUST either perform two separate assignments (one to stride, one to slice) or use `itertools.islice`.

## Catch-All Unpacking
- The AI MUST prefer catch-all unpacking with starred expressions (`*others`) over manual slicing and indexing when dividing a list into non-overlapping pieces.
- The AI MUST include at least one required part in an unpacking assignment (e.g., `*others = somelist` is a `SyntaxError`).
- The AI MUST NEVER use multiple catch-all expressions in a single-level unpacking pattern.
- The AI MUST explicitly account for the fact that a starred expression always evaluates to a `list` instance, even if it catches zero elements (an empty list).
- The AI MUST NOT use catch-all unpacking on arbitrary iterators unless there is absolute certainty that the resulting data will fit entirely in memory.

## Sorting by Complex Criteria
- The AI MUST use the `key` parameter (usually with a `lambda` function) for sorting objects, rather than defining natural orderings (`__lt__`) unless the object inherently requires natural ordering.
- For sorting by multiple criteria, the AI MUST return a tuple from the `key` function.
- The AI MUST use the unary minus operator (`-`) inside the tuple to mix ascending and descending sort directions for numerical values.
- For types that do not support unary negation (like strings), the AI MUST combine sorting criteria by calling the `sort()` method multiple times. These calls MUST be executed in the reverse order of priority (lowest rank criteria sorted first, highest rank criteria sorted last) to leverage Python's stable sorting.

## Dictionary Insertion Ordering
- The AI MUST assume standard `dict` instances (Python 3.7+) preserve insertion ordering for standard iterations, `**kwargs`, and class `__dict__` attributes.
- The AI MUST NOT assume insertion ordering is preserved if the dictionary is passed from an external source and could be a custom container type (e.g., `collections.abc.MutableMapping`).
- When order is strictly required for an algorithm, the AI MUST either write order-agnostic code, explicitly check `isinstance(ranks, dict)`, or enforce the type using type annotations and static analysis.

## Handling Missing Dictionary Keys
- The AI MUST NOT use `in` checks or catch `KeyError` to handle missing dictionary keys when simple defaults are required. Use the `get()` method instead.
- For complex types (e.g., lists or dictionaries) where the default value has an allocation cost or may raise exceptions, the AI MUST use `get()` combined with the assignment expression (walrus operator `:=`).
- The AI MUST NOT use `dict.setdefault()` unless the default value is cheap to construct, mutable, and exception-free. (Note: `setdefault` evaluates its default argument immediately, which causes performance degradation and memory overhead if instantiating objects).
- When managing the internal state of a class with arbitrary keys, the AI MUST use `collections.defaultdict` instead of `setdefault`.
- If the default value construction requires knowledge of the specific key being accessed, `defaultdict` cannot be used (its factory function takes no arguments). In this scenario, the AI MUST subclass `dict` and implement the `__missing__(self, key)` special method.

# @Workflow
When generating, refactoring, or reviewing Python code dealing with sequences and dictionaries, follow this strict evaluation path:

1. **Slice Extraction Analysis**: 
   - Scan for explicit `0` starts or `len()` ends. Remove them.
   - Scan for 3-parameter slices `[a:b:c]`. Split them into a striding step and a slicing step, or import `itertools.islice`.
2. **Unpacking Analysis**:
   - Scan for manual sequence indexing (`first = a[0]`, `rest = a[1:]`).
   - Refactor into starred expressions (`first, *rest = a`).
3. **Sorting Evaluation**:
   - Scan for custom classes implementing sorting. Ensure they use `list.sort(key=...)`.
   - If sorting requires multiple directions (e.g., weight descending, name ascending), check if the secondary criteria supports negation. If yes, use a tuple: `key=lambda x: (-x.weight, x.name)`. If no, implement sequential stable sorts.
4. **Dictionary Missing Key Evaluation**:
   - Assess the source of the dictionary: Is it external or internal state?
   - Assess the default value: Is it a primitive scalar, a complex object, or does it require the key string to compute?
   - Apply the corresponding pattern:
     - External + Primitive = `dict.get(key, default)`
     - External + Complex = `if (val := d.get(key)) is None: d[key] = val = Complex()`
     - Internal + Key-independent = `collections.defaultdict(Complex)`
     - Internal + Key-dependent = Subclass `dict` and implement `__missing__(self, key)`.

# @Examples (Do's and Don'ts)

## Sequence Slicing
- **[DO]** Use boundary-forgiving shorthand slicing:
  ```python
  first_twenty = a[:20]
  last_twenty = a[-20:]
  ```
- **[DON'T]** Include redundant slice indexes or combine stride with start/end:
  ```python
  first_twenty = a[0:20] # Redundant 0
  last_twenty = a[-20:len(a)] # Redundant len(a)
  evens_subset = a[2:10:2] # Anti-pattern: stride + start/end
  ```

## Catch-All Unpacking
- **[DO]** Use starred expressions for cleanly dividing sequences:
  ```python
  oldest, second_oldest, *others = car_ages_descending
  ```
- **[DON'T]** Use hardcoded indexes and manual slicing to unpack:
  ```python
  oldest = car_ages_descending[0]
  second_oldest = car_ages_descending[1]
  others = car_ages_descending[2:]
  ```

## Complex Sorting
- **[DO]** Use unary minus in tuples for mixed-direction sorting of numbers:
  ```python
  power_tools.sort(key=lambda x: (-x.weight, x.name))
  ```
- **[DO]** Use multiple stable sorts for un-negatable types (like strings):
  ```python
  # Sort by name ascending, then weight descending
  power_tools.sort(key=lambda x: x.name)
  power_tools.sort(key=lambda x: x.weight, reverse=True)
  ```
- **[DON'T]** Attempt to use unary minus on strings:
  ```python
  power_tools.sort(key=lambda x: (x.weight, -x.name), reverse=True) # Raises TypeError
  ```

## Dictionary Missing Keys: Complex Values
- **[DO]** Use `get` with the walrus operator for complex default allocations:
  ```python
  if (names := votes.get(key)) is None:
      votes[key] = names = []
  names.append(who)
  ```
- **[DON'T]** Use `setdefault` for complex values (allocates an unused list on every access):
  ```python
  names = votes.setdefault(key, [])
  names.append(who)
  ```

## Dictionary Missing Keys: Internal State
- **[DO]** Use `defaultdict` for internal class state:
  ```python
  from collections import defaultdict
  class Visits:
      def __init__(self):
          self.data = defaultdict(set)
      def add(self, country, city):
          self.data[country].add(city)
  ```
- **[DON'T]** Use `setdefault` manually for internal class state:
  ```python
  class Visits:
      def __init__(self):
          self.data = {}
      def add(self, country, city):
          city_set = self.data.setdefault(country, set())
          city_set.add(city)
  ```

## Dictionary Missing Keys: Key-Dependent Values
- **[DO]** Subclass `dict` and implement `__missing__` when the default value relies on the key:
  ```python
  class Pictures(dict):
      def __missing__(self, key):
          value = open_picture(key)
          self[key] = value
          return value
  ```
- **[DON'T]** Use `setdefault` with a function that executes immediately and blindly:
  ```python
  # Anti-pattern: opens the file even if path already exists in dict
  handle = pictures.setdefault(path, open(path, 'a+b'))
  ```