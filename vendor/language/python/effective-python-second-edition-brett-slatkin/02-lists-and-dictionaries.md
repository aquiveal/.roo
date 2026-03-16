# @Domain
These rules MUST be activated when the AI is writing, refactoring, or reviewing Python code that involves sequence manipulation (slicing, indexing, striding), unpacking iterables, sorting data structures, or managing state using dictionaries and associative arrays. These rules assume a Python 3.7+ environment.

# @Vocabulary
- **Slice**: A subset of a sequence defined by `start:end` bounds, where `start` is inclusive and `end` is exclusive.
- **Stride**: The step size parameter used when extracting items from a sequence, formatted as `start:end:stride`.
- **Catch-All Unpacking**: The use of a starred expression (`*variable`) in an assignment statement to capture all remaining, unassigned items of an iterable into a list.
- **Stable Sorting**: An algorithm property (inherent to Python's `list.sort()`) where the relative order of elements that compare as equal is preserved.
- **Duck Typing**: Relying on an object's implemented behaviors (like `MutableMapping`) instead of explicit class inheritance (like `dict`).
- **`defaultdict`**: A class from the `collections` module that automatically assigns a default value for missing keys using a zero-argument callable.
- **`__missing__`**: A class dunder method that can be implemented on a `dict` subclass to define dynamic, key-dependent fallback logic when a dictionary key is accessed but not found.

# @Objectives
- Maximize code readability by eliminating visual noise in sequence slicing and unpacking.
- Prevent subtle logic errors caused by combining slices and strides, off-by-one index bounds, or exhausted iterators.
- Optimize dictionary interactions by avoiding redundant key lookups, unnecessary memory allocations, and improper use of dict-like interfaces.
- Ensure robust sorting mechanisms by leveraging complex keys, tuple comparisons, and stable sorting properties instead of manual object comparator overrides.

# @Guidelines

## Sequence Slicing and Striding
- The AI MUST omit the `0` start index when slicing from the beginning of a sequence (e.g., use `a[:5]`, not `a[0:5]`).
- The AI MUST omit the final index when slicing to the end of a sequence (e.g., use `a[5:]`, not `a[5:len(a)]`).
- The AI MUST utilize negative numbers for offsets relative to the end of a list instead of calculating lengths manually.
- The AI MUST NOT use the expression `[-0:]` as it evaluates to `[:]` and returns a shallow copy of the entire list; use specific nonzero negative bounds instead.
- The AI MUST leverage the fact that slicing is forgiving of out-of-bounds start or end indexes to establish max lengths (e.g., `a[:20]` is safe even if `len(a) < 20`).
- The AI MUST assign to `[:]` when the goal is to replace the entire contents of an existing list object without allocating a new reference.
- The AI MUST NOT combine start, end, and stride parameters in a single slice expression (`a[start:end:stride]`).
- If a stride is required, the AI MUST use a positive stride without start or end indexes (e.g., `x[::2]`).
- If negative strides are used (e.g., `[::-1]`), the AI MUST avoid applying them to UTF-8 encoded byte strings representing Unicode characters, as it will corrupt multi-byte characters.
- If both slicing and striding are absolutely necessary, the AI MUST execute them as two separate assignments or utilize `itertools.islice`.

## Unpacking and Data Extraction
- The AI MUST prefer Catch-All Unpacking (`*rest`) over explicit indexing and slicing when dividing sequences into non-overlapping pieces.
- The AI MUST ensure that at least one required (non-starred) variable is present in an unpacking assignment that uses a starred expression.
- The AI MUST NOT use multiple catch-all expressions (`*`) in a single-level unpacking pattern.
- The AI MUST restrict the use of catch-all unpacking on arbitrary iterators (e.g., generators) to situations where it is absolutely certain that the remaining data will fit into memory, as the starred expression evaluates to an in-memory `list`.

## Sorting Lists
- The AI MUST NOT define dunder methods (like `__lt__`) on custom classes solely for the purpose of sorting, unless the class inherently possesses a natural mathematical or lexical ordering.
- The AI MUST use the `key` parameter with a helper function (or `lambda`) to extract the sorting criteria from objects.
- When sorting by multiple criteria, the AI MUST return a `tuple` from the `key` function.
- When sorting by multiple numeric criteria in different directions (ascending/descending), the AI MUST use unary negation (`-`) on the specific numeric values within the tuple returned by the `key` function.
- When sorting by multiple criteria where types cannot be negated (e.g., strings), the AI MUST call the `sort()` method multiple times. The AI MUST execute these calls in the reverse order of priority (lowest priority sort first, highest priority sort last) to leverage Python's stable sorting.

## Dictionaries and State Management
- The AI MUST rely on standard Python 3.7+ `dict` instances preserving insertion order (including `keys`, `values`, `items`, `popitem()`, `**kwargs`, and class `__dict__`).
- The AI MUST NOT assume insertion ordering is preserved when accepting arbitrary dictionary-like objects (e.g., custom classes implementing `MutableMapping`). 
- When an exact `dict` type is required for ordering, the AI MUST explicitly check the type at runtime (`isinstance(d, dict)`) OR use strict type annotations (`Dict[str, type]`) paired with static analysis.
- If handling high rates of key insertions and `popitem()` calls (e.g., an LRU cache), the AI MUST consider `collections.OrderedDict` for its specialized performance characteristics over standard `dict`.
- To count item frequencies, the AI MUST use `collections.Counter` instead of managing raw dictionary counts manually.
- The AI MUST prefer the `get` method for retrieving values with a default, avoiding `in` expressions and `KeyError` exceptions to reduce redundant key lookups.
- When checking for a missing key whose default value is computationally expensive to construct or could raise an exception, the AI MUST use `get` paired with an assignment expression (the walrus operator `:=`).
- The AI MUST NOT use the `setdefault` method unless the default value is exceptionally cheap to construct (like an empty list `[]`), mutable, and incapable of raising an exception.
- When controlling the creation of a dictionary that manages an arbitrary set of potential keys and needs standard default values, the AI MUST use `collections.defaultdict` instead of `setdefault`.
- If the default value for a missing dictionary key must be derived from the specific key itself, or requires arguments, the AI MUST subclass `dict` and implement the `__missing__(self, key)` dunder method.

# @Workflow
When tasked with writing or refactoring sequence or dictionary operations, the AI MUST follow this algorithmic process:

1. **Sequence Assessment:** Determine if a sequence is being accessed via raw numerical indexes. Replace index-based extractions with unpacking or catch-all unpacking where possible.
2. **Slice / Stride Audit:** Scan for brackets containing two colons (`[::]`). If start, end, and stride are all present, split the logic into two lines: one for the stride, one for the slice. Remove redundant `0` or `len()` boundaries.
3. **Sort Strategy Analysis:** If a custom object list requires sorting, implement a `lambda` for the `key` argument. For multi-criteria sorting, evaluate if the types are numeric. If yes, return a tuple with unary negation. If no, stack `.sort()` calls in reverse priority.
4. **Dictionary Lookup Evaluation:** Search for `if key in d:` or `try: d[key] except KeyError:`. Replace with `d.get(key, default)`. 
5. **State Initialization Refactoring:** If the code inserts missing nested structures into a dict (e.g., `d.setdefault(k, [])`), evaluate if the AI controls the dict creation. If yes, refactor to `collections.defaultdict`.
6. **Key-Dependent Default Verification:** If a dictionary needs defaults that are calculated dynamically based on the missing key string, immediately generate a `dict` subclass with `__missing__`.

# @Examples (Do's and Don'ts)

## Slicing and Striding
- [DO] Use clean bounds and positive strides:
  ```python
  evens = x[::2]
  subset = x[:20]
  last_few = x[-5:]
  ```
- [DON'T] Combine slice and stride or use redundant boundaries:
  ```python
  # Anti-pattern: confusing and visually noisy
  evens = x[0:20:2]
  last_few = x[-5:len(x)]
  ```

## Unpacking
- [DO] Use catch-all unpacking to extract subsets:
  ```python
  oldest, second_oldest, *others = car_ages_descending
  ```
- [DON'T] Use slicing and indexing to separate sequence items:
  ```python
  # Anti-pattern: error-prone and brittle boundaries
  oldest = car_ages_descending[0]
  second_oldest = car_ages_descending[1]
  others = car_ages_descending[2:]
  ```

## Sorting
- [DO] Use tuples with unary negation for mixed-direction numeric sorting:
  ```python
  power_tools.sort(key=lambda x: (-x.weight, x.name))
  ```
- [DON'T] Rely on unsupported negation or single calls for mixed string sorting:
  ```python
  # Anti-pattern: strings cannot be negated
  power_tools.sort(key=lambda x: (x.weight, -x.name), reverse=True)
  ```
- [DO] Leverage stable sorting by calling `.sort()` multiple times in reverse priority:
  ```python
  power_tools.sort(key=lambda x: x.name) # Lowest priority
  power_tools.sort(key=lambda x: x.weight, reverse=True) # Highest priority
  ```

## Handling Missing Dictionary Keys
- [DO] Use `get` with an assignment expression for complex lookups:
  ```python
  if (names := votes.get(key)) is None:
      votes[key] = names = []
  names.append(who)
  ```
- [DON'T] Use `in` checks which require redundant accesses:
  ```python
  # Anti-pattern: two accesses if key exists
  if key in votes:
      names = votes[key]
  else:
      votes[key] = names = []
  names.append(who)
  ```
- [DON'T] Use `setdefault` for expensive object allocations:
  ```python
  # Anti-pattern: the default open() is evaluated unconditionally
  handle = pictures.setdefault(path, open(path, 'a+b')) 
  ```

## Key-Dependent Defaults
- [DO] Use `__missing__` when the default value depends on the requested key:
  ```python
  class Pictures(dict):
      def __missing__(self, key):
          value = open_picture(key)
          self[key] = value
          return value
  ```
- [DON'T] Use `defaultdict` when the factory function requires arguments:
  ```python
  # Anti-pattern: defaultdict only accepts zero-argument callables
  pictures = defaultdict(open_picture) # open_picture requires a 'key'
  ```