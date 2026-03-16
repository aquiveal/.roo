# @Domain
These rules activate when the AI is tasked with optimizing data lookups, deduplicating data, managing unordered collections, implementing custom classes intended for use as keys or unique items, or analyzing the performance and memory footprint of Python dictionaries (`dict`) and sets (`set`).

# @Vocabulary
- **Hash Table**: The underlying data structure powering Python dictionaries and sets, providing O(1) lookups and insertions by turning an arbitrary key into an array index.
- **Key**: A unique reference object used to index data within a hash table. It must be of a hashable type.
- **Hashable Type**: A type that implements both the `__hash__` magic method and either `__eq__` or `__cmp__`.
- **Masking**: The bitwise operation (using a mask like `0b111` for an 8-bucket table) applied to a hash value to truncate it so that it fits within the allocated number of buckets in system memory. 
- **Hash Collision**: When two different keys produce the same masked hash index, requiring the hash table to find a new location for the data.
- **Probing**: The linear function mechanism Python uses to resolve hash collisions by generating a new index. Python's specific probing mechanism incorporates higher-order bits of the original hash to avoid identical probing sequences.
- **Load Factor**: A measure of how well distributed the data is throughout the hash table. 
- **Entropy (of a Hash Function)**: A measure of how well a hash function distributes its values. Maximized when every hash value has an equal probability of being chosen, thereby minimizing collisions.
- **Sentinel Value**: A special internal value written to a memory bucket when an item is deleted from a dictionary or set, indicating the bucket is empty but that the probing sequence must continue.
- **Amortized O(1)**: The average time complexity for dictionary/set insertions, accounting for the fact that most insertions are instantaneous, but occasional insertions trigger an expensive O(n) table resize.

# @Objectives
- Achieve O(1) computational complexity for data lookups and deduplication by correctly utilizing dictionaries and sets in place of lists.
- Prevent O(n) performance degradation in hash tables by writing high-entropy custom hash functions that minimize hash collisions.
- Control memory overhead and manage resize operations effectively, understanding the exact thresholds that trigger Python's internal memory reallocation.
- Ensure custom objects behave correctly in sets and dictionaries by explicitly defining value-based hashing rather than relying on default memory-address hashing.

# @Guidelines
- **Data Structure Selection**: The AI MUST use a `set` to extract unique items from a collection or test membership. The AI MUST NEVER use a `list` for membership testing (`if item in list:`) if the collection is large, as this incurs an O(n) linear search penalty.
- **Dictionary Lookups**: The AI MUST use a `dict` for mapping relationships (like a phonebook) to achieve O(1) lookups, strictly avoiding iterating over lists of tuples.
- **Custom Object Hashing**: When defining user-defined classes that will be placed in a `set` or used as `dict` keys, the AI MUST implement a custom `__hash__` and `__eq__` method based on the object's properties (content-based hashing).
- **Avoiding Default Hashes**: The AI MUST NOT rely on Python's default `__hash__` for custom objects if instances with identical data need to be treated as the same dictionary key or set element. (The default uses the `id()` memory placement, which treats identical instances as distinct).
- **Maximizing Hash Entropy**: When writing custom hash functions, the AI MUST ensure the returned integer evenly distributes across the expected mask. The AI MUST NEVER return a constant integer or highly clustered values, as this forces O(n) performance degradation due to massive collision resolution.
- **Accounting for Resizing**: The AI MUST account for the memory overhead of hash tables. Dictionaries resize when they are 2/3 full, and sets resize when they are 3/5 full. The new size is always a power of two.
- **Memory Optimization via Deletion**: When optimizing memory after deleting many items (`dict.pop()`), the AI MUST recognize that sentinel values are left behind. To force the hash table to shrink and release memory, the AI MUST insert a new element (which triggers the resize evaluation).
- **Insertion Order**: The AI MUST recognize that modern Python dictionaries append key/value data into a standard dense array and store only the indices in the sparse hash table, thereby preserving insertion order and reducing memory footprints.
- **Type Uniformity in Math**: For numeric optimization, if the problem requires math over unordered elements, the AI MUST note that generic `dict` and `set` structures carry memory overhead and cannot be natively vectorized like `numpy` arrays. 

# @Workflow
1. **Analyze the Data Access Pattern**:
   - Determine if the application requires searching for specific values, checking uniqueness, or mapping keys to values.
   - If yes, initialize a `dict` or `set`. If the data simply needs to be iterated sequentially, consider if a `list` or `tuple` is more memory-efficient.
2. **Evaluate the Key Type**:
   - If the key is a primitive type (string, integer, tuple), proceed directly to insertion, as Python's native `hash()` (using SipHash for strings) provides near-ideal entropy.
   - If the key is a custom class, implement `__eq__(self, other)` to compare the relevant underlying data properties.
   - Implement `__hash__(self)` to return an integer derived from the exact same properties used in `__eq__` (e.g., `return hash((self.prop1, self.prop2))`).
3. **Analyze Memory and Resizing Triggers**:
   - Calculate the expected number of elements `N`.
   - Calculate the minimum buckets needed: `N * (3/2)` for dicts, or `N * (5/3)` for sets.
   - Find the next power of 2 greater than this number to determine the true memory footprint. 
   - If memory is heavily constrained, evaluate if a different data structure is required.
4. **Implement and Profile**:
   - Implement the `set` deduplication or `dict` mapping.
   - If a large volume of items was removed and memory must be reclaimed, insert a single dummy item to trigger the kernel's resizing algorithm and clear sentinel values.

# @Examples (Do's and Don'ts)

### [DO] Use Sets for O(1) Deduplication and Membership Testing
```python
# O(1) deduplication leveraging the hash table properties of sets
def set_unique_first_names(phonebook):
    unique_first_names = set()
    for name, phonenumber in phonebook:
        first_name, last_name = name.split(" ", 1)
        unique_first_names.add(first_name)
    return len(unique_first_names)
```

### [DON'T] Use Lists for Uniqueness or Membership Testing
```python
# ANTI-PATTERN: O(n^2) or O(n log n) performance due to linear search
def list_unique_first_names(phonebook):
    unique_first_names = []
    for name, phonenumber in phonebook:
        first_name, last_name = name.split(" ", 1)
        for unique in unique_first_names: # LINEAR SEARCH
            if unique == first_name:
                break
        else:
            unique_first_names.append(first_name)
    return len(unique_first_names)
```

### [DO] Implement Content-Based Hashing for Custom Objects
```python
# Custom objects properly deduplicate in sets/dicts
class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __hash__(self):
        # Uses internal tuple hashing to guarantee entropy
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

p1 = Point(1, 1)
p2 = Point(1, 1)
unique_points = set([p1, p2])
# len(unique_points) == 1
```

### [DON'T] Rely on Default Hashing for Value-Equivalent Custom Objects
```python
# ANTI-PATTERN: Default hash uses memory address, breaking deduplication
class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

p1 = Point(1, 1)
p2 = Point(1, 1)
unique_points = set([p1, p2])
# len(unique_points) == 2 (Memory addresses differ, so both are added)
```

### [DON'T] Write Low-Entropy Custom Hash Functions
```python
# ANTI-PATTERN: Intentional hash collisions destroy performance (O(n) lookups)
class BadHash(str):
    def __hash__(self):
        # Creates massive collisions, forcing continuous probing
        return 42
```