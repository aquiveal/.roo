# @Domain
These rules apply to any Python codebase involving the creation, manipulation, extension, or structural matching of dictionaries, sets, and mapping types. Trigger these rules when a task requires data deduplication, key-value storage, data aggregation, processing of semi-structured data (like JSON), or the implementation of custom dictionary-like or set-like classes.

# @Vocabulary
- **Hashable**: An object is hashable if it has a hash code that never changes during its lifetime (implementing `__hash__()`) and can be compared to other objects (implementing `__eq__()`).
- **dictcomp / setcomp**: Dictionary comprehension and set comprehension; syntactic constructs for building mappings or sets expressively.
- **Destructuring**: A more advanced form of unpacking used in `match/case` statements to extract data from nested mappings and sequences.
- **MappingProxyType**: A wrapper class from the `types` module that provides a read-only, dynamic proxy for an underlying mapping.
- **UserDict**: A base class from `collections` designed specifically for subclassing to create custom mapping types, circumventing the limitations of subclassing the C-implemented `dict` directly.
- **Dictionary Views**: Read-only, dynamic projections of the internal data structures of a `dict` (`dict_keys`, `dict_values`, `dict_items`). `dict_keys` and `dict_items` act like sets.
- **ChainMap**: A mapping class from `collections` that holds a list of mappings that can be searched as one, useful for managing nested scopes or hierarchical configurations.
- **Counter**: A specialized mapping from `collections` that holds an integer count for each key, effectively functioning as a multiset.

# @Objectives
- Leverage Python's highly optimized, C-based `dict` and `set` data structures to ensure high-performance lookups and storage.
- Utilize modern Python syntax features such as the `|` operator, `**` unpacking, and `match/case` for concise, declarative mapping interactions.
- Avoid reinventing the wheel by utilizing specialized mapping types (`defaultdict`, `OrderedDict`, `Counter`, `ChainMap`) from the standard library.
- Safely extend mappings by subclassing `collections.UserDict` rather than the built-in `dict` to ensure reliable method overrides.
- Protect internal state by exposing immutable mapping facades where necessary.
- Reduce algorithmic complexity by replacing nested loops and conditionals with mathematically grounded set operations (`&`, `|`, `-`, `^`).

# @Guidelines
- **Modern Dict Syntax**: Use the `|` operator to create a new mapping by merging two dictionaries, and the `|=` operator to update an existing mapping in-place (requires Python 3.9+). 
- **Mapping Unpacking**: Use the `**` unpacking syntax inside dict literals to merge multiple mappings. Duplicate keys are allowed; later occurrences overwrite previous ones.
- **Handling Mutable Values**: When retrieving a mutable value from a mapping to update it, use `dict.setdefault(key, default)` to avoid redundant key lookups.
- **Automatic Missing Keys**: If default values must be generated dynamically for missing keys, use `collections.defaultdict(default_factory)`.
- **Custom Missing Key Logic**: To intercept and customize failed dictionary lookups, implement the `__missing__(self, key)` special method in a custom mapping class. Note: `__missing__` is not defined in the base `dict` class, but standard `__getitem__` is aware of it and will call it if present.
- **Pattern Matching with Mappings**: Use `match/case` (Python 3.10+) to destructure JSON-like semi-structured data. Remember that mapping patterns succeed on *partial* matches (extra keys in the subject do not cause the match to fail).
- **Capturing Extra Keys in Patterns**: Use `**extra` as the last element in a mapping pattern to capture unhandled key-value pairs as a dictionary. Do not use `**_` as it is forbidden and redundant.
- **Creating Custom Dictionaries**: ALWAYS subclass `collections.UserDict` (or `collections.abc.MutableMapping`) instead of the built-in `dict`. Built-in `dict` methods (written in C) bypass user-defined overrides, which breaks object-oriented late-binding expectations.
- **Read-Only Dictionaries**: To prevent users from inadvertently modifying a mapping, wrap it in `types.MappingProxyType`. This creates a dynamic, immutable view where changes to the underlying dictionary are visible, but direct modifications via the proxy raise a `TypeError`.
- **Set Initialization**: ALWAYS use literal syntax `{1, 2}` instead of `set([1, 2])` for performance. The literal syntax runs a specialized `BUILD_SET` bytecode. Use `set()` only for creating empty sets, as `{}` creates an empty dict.
- **Set Operations**: Prefer infix operators for sets (`&` for intersection, `|` for union, `-` for difference, `^` for symmetric difference) over explicit loops and conditional `in` checks.
- **Leverage Dictionary Views**: Remember that `dict.keys()` and `dict.items()` return views that behave like `frozenset`. You can perform set operations directly on them (e.g., `d1.keys() & d2.keys()`) provided all values in the dictionary are hashable for `dict_items`.
- **Type Checking**: NEVER type check against concrete `dict`. Check against `collections.abc.Mapping` or `collections.abc.MutableMapping` to support duck typing and specialized mapping types.
- **Hashability Warning**: Be aware that tuples containing mutable elements (like lists) are *not* hashable and will cause a `TypeError` if used as dict keys or set elements.

# @Workflow
1. **Analyze Data Requirements**: Determine if the task requires key-value mapping, uniqueness guarantees, or counting.
2. **Select the Data Structure**:
   - For standard lookups: Use `dict`.
   - For handling missing keys dynamically: Use `collections.defaultdict`.
   - For tallying/counting: Use `collections.Counter`.
   - For hierarchical fallback lookups (e.g., scoping, configuration layers): Use `collections.ChainMap`.
   - For uniqueness and mathematical intersections: Use `set`.
3. **Refactor Initialization**: Replace programmatic population of dicts/sets with `dictcomp` and `setcomp` constructs for clarity and speed.
4. **Refactor Lookups**: Identify patterns of `if key not in d: d[key] = []` and replace them immediately with `d.setdefault(key, [])`.
5. **Implement Custom Mappings**: If overriding `__getitem__`, `__setitem__`, or handling `__missing__` is required, create a class extending `collections.UserDict`. Add necessary logic inside the special methods.
6. **Apply Destructuring**: If parsing nested JSON-like configurations, replace nested `dict.get()` calls with `match/case` mapping patterns, utilizing type matching (e.g., `str(name)`) for validation.
7. **Expose Interfaces**: If returning an internal mapping to an outside consumer, wrap the return value in `types.MappingProxyType` to enforce read-only semantics.

# @Examples (Do's and Don'ts)

### Merging Mappings
- **[DO]** Use the `|` operator or `**` unpacking to merge dictionaries clearly.
  ```python
  # Python 3.9+
  merged_config = default_config | user_config

  # Python 3.5+
  merged_config = {**default_config, **user_config}
  ```
- **[DON'T]** Use manual iteration to merge dictionaries.
  ```python
  # Anti-pattern
  merged_config = default_config.copy()
  for k, v in user_config.items():
      merged_config[k] = v
  ```

### Inserting/Updating Mutable Values
- **[DO]** Use `setdefault` to retrieve and update a mutable value in a single lookup.
  ```python
  index.setdefault(word, []).append(location)
  ```
- **[DON'T]** Use `get` or `in` checks which require multiple lookups.
  ```python
  # Anti-pattern (performs up to 3 lookups)
  occurrences = index.get(word, [])
  occurrences.append(location)
  index[word] = occurrences
  ```

### Pattern Matching Semi-Structured Data
- **[DO]** Use `match/case` to concisely destructure and validate mapping structures.
  ```python
  match record:
      case {'type': 'book', 'api': 2, 'authors': [*names]}:
          return names
      case {'type': 'book', 'api': 1, 'author': name}:
          return [name]
      case {'type': 'book', **extra}:
          raise ValueError(f"Invalid book record. Extra fields: {extra}")
  ```
- **[DON'T]** Rely on deep, nested `if/elif` chains and `isinstance` checks for JSON unpacking.

### Creating Custom Mappings
- **[DO]** Subclass `UserDict` to guarantee that overridden methods are respected by the class.
  ```python
  import collections

  class StrKeyDict(collections.UserDict):
      def __missing__(self, key):
          if isinstance(key, str):
              raise KeyError(key)
          return self[str(key)]

      def __setitem__(self, key, item):
          self.data[str(key)] = item
  ```
- **[DON'T]** Subclass the built-in `dict` directly, as C-level optimizations will ignore your `__setitem__` and `__missing__` methods during operations like `__init__` and `update()`.
  ```python
  # Anti-pattern
  class StrKeyDict(dict):
      ...
  ```

### Returning Read-Only Dictionaries
- **[DO]** Protect internal mapping states using `MappingProxyType`.
  ```python
  from types import MappingProxyType

  class HardwareBoard:
      def __init__(self):
          self._pins = {1: 'A', 2: 'B'}
      
      @property
      def pins(self):
          return MappingProxyType(self._pins)
  ```
- **[DON'T]** Return the raw dictionary, which breaks encapsulation if the client mutates it.

### Finding Common Keys (Set Operations on Views)
- **[DO]** Use set operators on dictionary views.
  ```python
  common_keys = dict1.keys() & dict2.keys()
  ```
- **[DON'T]** Iterate through keys manually.
  ```python
  # Anti-pattern
  common_keys = set()
  for k in dict1:
      if k in dict2:
          common_keys.add(k)
  ```

### Set Initialization
- **[DO]** Use literal syntax for sets.
  ```python
  valid_status = {'OK', 'ERROR', 'NOT_FOUND'}
  ```
- **[DON'T]** Call the `set()` constructor with a list literal.
  ```python
  # Anti-pattern
  valid_status = set(['OK', 'ERROR', 'NOT_FOUND'])
  ```