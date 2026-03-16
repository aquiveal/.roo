# @Domain
Python programming tasks involving data structure selection, performance optimization of collections, memory footprint reduction, memory allocation optimization, and search/lookup algorithm implementation.

# @Vocabulary
*   **Array**: A flat list of data with intrinsic ordering stored in contiguous system memory.
*   **Bucket**: A block of system memory capable of holding an integer-sized pointer to the actual data.
*   **Reference (Pointer)**: How Python stores data in buckets; the memory bucket contains a pointer to the actual object rather than the object itself.
*   **Dynamic Array**: An array implementation (like Python's `list`) that allows mutability and dynamic resizing.
*   **Static Array**: An array implementation (like Python's `tuple`) whose contents and size are fixed and immutable upon creation.
*   **Overallocation (Headroom)**: The strategy used by dynamic arrays to allocate more memory than immediately required (`M > N`) to optimize future `append` operations, reducing the frequency of expensive memory copy operations.
*   **Linear Search**: An $O(n)$ search algorithm that iterates through every element to find a match (e.g., `list.index()`).
*   **Tim Sort**: Python's built-in hybrid sorting algorithm (insertion and merge sort), providing $O(n)$ best-case and $O(n \log n)$ worst-case performance.
*   **Binary Search**: An $O(\log n)$ search algorithm used on sorted arrays, implemented in Python via the `bisect` module.
*   **Freelist (Resource Caching)**: Python's garbage collection optimization that preserves memory allocations for destroyed tuples of sizes 1–20 (up to 2,000 of each size, 40,000 total) to enable ultra-fast future instantiations without OS-level memory reallocation.
*   **Heavy Data**: Data that invokes significant time and effort to move around system memory.

# @Objectives
*   Select the most optimal array-based data structure (list vs. tuple) based on data mutability, lifecycle, and memory constraints.
*   Eliminate $O(n)$ linear searches in arrays by leveraging intrinsic ordering, sorting, and binary searches.
*   Minimize memory bloat and allocation overhead caused by list overallocation, particularly in large datasets consisting of many small collections.
*   Maximize the utilization of Python's runtime optimizations (such as tuple freelists) to speed up object instantiation.

# @Guidelines
*   **Data Structure Selection Rules:**
    *   The AI MUST use `tuple` for collections of data that describe multiple static properties of a single unchanging entity (e.g., coordinates, phone number components).
    *   The AI MUST use `list` to store collections of data representing disparate, dynamic objects where the collection's size or contents will change.
    *   When storing millions of small collections, the AI MUST use `tuple` instead of `list` to prevent massive memory waste caused by list overallocation headroom and list state overhead.
*   **Search and Lookup Rules:**
    *   If the index of the required data is known, the AI MUST use direct index lookups, leveraging $O(1)$ performance.
    *   The AI MUST NOT use `list.index()` or manual `for` loops to search for items in large arrays unless the array is explicitly unsorted and cannot be sorted.
    *   If searching is required and data can be maintained in a sorted state (using `__eq__` and `__lt__`), the AI MUST use the `bisect` module to achieve $O(\log n)$ binary search performance.
    *   When finding the "closest" value to a target in a numerical array, the AI MUST use a sorted array and `bisect.bisect_left` to compare adjacent indices, rather than calculating the distance for all elements.
*   **Memory and Instantiation Constraints:**
    *   The AI MUST account for Python's list resize formula (`M = (N + (N >> 3) + 6) & ~3`). Be aware that calling `.append()` triggers this overallocation.
    *   To avoid overallocation when the exact data size is known and immutable, the AI MUST convert the data to a `tuple`.
    *   The AI MUST NOT use tuple concatenation (`t1 + t2`) to iteratively build a sequence in a loop. Because tuples lack overallocation headroom, concatenation operates in $O(n)$ time by fully allocating and copying memory on every operation. Use lists for dynamic building.
    *   For small, temporary, fixed-size data groupings (sizes 1 through 20), the AI MUST prefer tuples over lists to exploit Python's $O(1)$ memory freelist caching, skipping kernel-level OS memory allocation.
*   **Typing Constraints:**
    *   When extreme performance is required, the AI MUST minimize mixed-type (heterogeneous) lists/tuples, as they reduce the potential for underlying memory and computational optimizations (e.g., NumPy/array modules).

# @Workflow
1.  **Analyze Data Lifecycle:** Determine if the collection is static (immutable size and contents) or dynamic (will be appended to or modified). 
2.  **Determine Structure:** 
    *   If static, instantiate as a `tuple`.
    *   If dynamic, instantiate as a `list`.
3.  **Evaluate Search Requirements:**
    *   If data is accessed via a known position, use standard index lookup ($O(1)$).
    *   If data must be searched by value, determine if the data can be sorted.
    *   If sortable, apply `.sort()` (or `bisect.insort()`) and implement lookups using the `bisect` module ($O(\log n)$).
4.  **Audit Memory Overhead:**
    *   Check if the architecture involves creating thousands/millions of small lists (e.g., via list comprehensions).
    *   If yes, cast the output to `tuple` immediately to reclaim overallocation headroom and reduce the footprint.
5.  **Audit Instantiation Bottlenecks:**
    *   Ensure inner loops do not instantiate `list` objects if a `tuple` can be used (leveraging the 1-20 size freelist).
    *   Ensure inner loops do not concatenate tuples (which triggers $O(n)$ memory copies).

# @Examples (Do's and Don'ts)

## 1. Searching an Array
**[DON'T]** Use linear search (`.index()`) on an ordered dataset, yielding $O(n)$ complexity.
```python
def find_item_slow(needle, haystack):
    # Anti-pattern: Linear search O(n)
    try:
        return haystack.index(needle)
    except ValueError:
        return -1
```

**[DO]** Sort the array and use `bisect` for $O(\log n)$ performance.
```python
import bisect

def find_item_fast(needle, sorted_haystack):
    # Optimal: Binary search O(log n)
    i = bisect.bisect_left(sorted_haystack, needle)
    if i != len(sorted_haystack) and sorted_haystack[i] == needle:
        return i
    return -1
```

## 2. Finding the Closest Value
**[DON'T]** Iterate through all elements to find the minimum distance.
```python
def find_closest_slow(needle, haystack):
    # Anti-pattern: O(n) full scan
    return min(haystack, key=lambda x: abs(x - needle))
```

**[DO]** Maintain a sorted array and use `bisect` to compare only the immediate neighbors.
```python
import bisect

def find_closest_fast(needle, sorted_haystack):
    # Optimal: O(log n) via binary search
    i = bisect.bisect_left(sorted_haystack, needle)
    if i == len(sorted_haystack):
        return i - 1
    elif sorted_haystack[i] == needle:
        return i
    elif i > 0:
        j = i - 1
        if sorted_haystack[i] - needle > needle - sorted_haystack[j]:
            return j
    return i
```

## 3. Large Datasets of Small Collections
**[DON'T]** Use lists for millions of small static collections, wasting memory on overallocation headroom and list state tracking.
```python
import random

# Anti-pattern: Creates 1,000,000 lists with hidden overallocation overhead
data_list = [[random.randint(0, 100) for _ in range(9)] for _ in range(1_000_000)]
```

**[DO]** Use tuples to strictly bound memory usage and take advantage of internal caching.
```python
import random

# Optimal: Saves ~19% memory overhead by preventing dynamic array overallocation
data_tuple = [tuple(random.randint(0, 100) for _ in range(9)) for _ in range(1_000_000)]
```

## 4. Building Collections Dynamically
**[DON'T]** Use tuple concatenation in a loop. It lacks overallocation headroom, forcing an $O(n)$ full memory copy on every iteration.
```python
# Anti-pattern: O(n^2) overall time due to O(n) tuple copying
my_tuple = ()
for i in range(1000):
    my_tuple = my_tuple + (i,)
```

**[DO]** Use list append to utilize dynamic array overallocation, keeping amortized append time at $O(1)$.
```python
# Optimal: Amortized O(1) appends
my_list = []
for i in range(1000):
    my_list.append(i)
```

## 5. Small Collection Instantiation in Hot Loops
**[DON'T]** Instantiate lists for short, temporary sequences under 20 elements.
```python
# Anti-pattern: Bypasses the freelist, requesting new memory from the OS
def hot_loop_computation():
    for _ in range(10_000_000):
        temp_data = [1, 2, 3] # Slow OS memory allocation
        # compute...
```

**[DO]** Instantiate tuples for short sequences to hit Python's internal freelist.
```python
# Optimal: Hits the size 1-20 tuple freelist, ~7.6x faster instantiation
def hot_loop_computation():
    for _ in range(10_000_000):
        temp_data = (1, 2, 3) # Instant retrieval from cached resource
        # compute...
```