@Domain
Python development tasks involving data pipelines, sequence processing, loops, large dataset handling, memory optimization, and mathematical or infinite series generation. Trigger these rules when refactoring list comprehensions, writing data ingest functions, mitigating `MemoryError` issues, or optimizing CPU/Memory tradeoffs in loops.

@Vocabulary
- **Iterator**: An object that implements the iterator protocol (`__iter__` and `__next__`), allowing traversal through a sequence until a `StopIteration` exception is raised.
- **Generator**: A specific type of iterator defined by a function that uses the `yield` keyword to return data one element at a time, pausing execution state between calls.
- **Lazy Evaluation**: The computing strategy of delaying the evaluation of an expression until its value is needed, thereby avoiding memory overhead of precomputing entire sequences.
- **Generator Comprehension**: A syntax utilizing `(expression for item in sequence if condition)` that lazily yields values, as opposed to list comprehensions `[...]` which eagerly load all values into memory.
- **Single Pass / Online Algorithm**: An algorithm that processes its input piece-by-piece in a serial fashion, requiring only the current value (and explicitly managed bounded state) without needing to reference the entire dataset.
- **Itertools**: Python's standard library module providing memory-efficient tools for manipulating iterators (e.g., `islice`, `chain`, `takewhile`, `cycle`, `groupby`, `filterfalse`).
- **CPU/Memory Trade-off**: The architectural decision between precomputing and storing data (uses more memory, saves CPU on repeated access) versus using generators (uses less memory, consumes CPU to recompute on repeated access).

@Objectives
- Drastically reduce memory footprints by converting eager evaluations (lists/arrays) into lazy evaluations (generators) wherever data is processed sequentially.
- Enforce the separation of concerns by isolating data generation logic from data transformation/filtering logic.
- Maximize the use of built-in Python generator tools (`range`, `map`, `zip`, `filter`, `enumerate`, and the `itertools` module) to process sequences.
- Prevent memory exhaustion caused by creating intermediate list objects solely for the purpose of counting, filtering, or throwing away data.
- Design data algorithms to be "single-pass" so they can handle datasets larger than the available system RAM and be seamlessly adapted for distributed computing.

@Guidelines

**Data Generation vs. Transformation**
- The AI MUST separate data generation from data transformation. Generators are responsible for yielding data; normal functions/loops are responsible for acting on or transforming that generated data.
- When generating sequences (finite or infinite), the AI MUST use `yield` instead of `append`ing to a local list and returning it.
- Infinite series MUST be encapsulated in generator functions using a `while True: yield` pattern. The termination logic MUST be handled by the consumer (e.g., using `itertools.takewhile` or explicit `break` statements).

**Comprehensions and Aggregations**
- The AI MUST NOT use list comprehensions to filter or process a sequence if the resulting list is only used to calculate a length or sum. 
- To count elements matching a condition, the AI MUST use the `sum()` function with a generator comprehension (e.g., `sum(1 for x in seq if condition)`), thereby preventing the allocation of massive intermediate lists.

**Leveraging Standard Library Tools**
- The AI MUST utilize Python's built-in lazy functions: `range`, `map`, `zip`, `filter`, `reversed`, and `enumerate`.
- The AI MUST use the `itertools` module for complex iterator manipulation:
  - Use `itertools.islice` to slice infinite or large generators.
  - Use `itertools.chain` to link multiple generators together seamlessly.
  - Use `itertools.takewhile` to apply an end condition to an infinite generator.
  - Use `itertools.cycle` to make a finite generator infinite.
  - Use `itertools.filterfalse` to efficiently invert filter logic.
  - Use `itertools.groupby` to group sequential data. The AI MUST ensure the input data is sorted or sequential by the key before applying `groupby`.

**Handling CPU/Memory Trade-offs**
- The AI MUST evaluate the access pattern of the data. If the sequence will be iterated over exactly once, a generator MUST be used.
- If the sequence must be referenced multiple times, the AI MUST explicitly weigh the cost of recomputation (generator) vs memory exhaustion (list). If RAM is abundant and CPU time is the bottleneck, materializing the generator into a `list` or `tuple` is permitted but MUST be justified.
- The AI MUST package algorithm state explicitly when using iterators. By defining exact states, the AI prepares the code for multi-CPU or distributed cluster execution where state packaging is strictly required.

**Rolling Windows and State Management**
- When implementing a rolling window over an iterator, the AI MUST store only the window's worth of data in memory.
- If using a `tuple` for a window, slide the window by slicing and concatenating: `window = window[1:] + (item,)`.
- If using `collections.deque` for O(1) performance on window appends/pops, the AI MUST yield a copy of the deque (or cast it to a tuple) to prevent mutating the reference held by the consuming function.

@Workflow
When requested to write, refactor, or optimize data processing loops, the AI MUST follow this algorithmic process:
1. **Analyze Access Patterns**: Determine if the data sequence is consumed once (single-pass) or multiple times.
2. **Identify Eager Structures**: Scan the code for list accumulations (`[]` with `.append()`), list comprehensions used strictly for aggregation (`len([x for x...])`), and eager file/data reads (`.readlines()`).
3. **Convert to Generators**: Refactor eager structures into generator functions (`yield`) or generator comprehensions `(x for x...)`.
4. **Apply Itertools**: Identify complex logic (breaking loops, nested grouping, slicing subsets) and replace with appropriate `itertools` methods (`takewhile`, `groupby`, `islice`).
5. **Decouple Logic**: Ensure the function generating the data has no dependency on the function transforming or analyzing the data.
6. **Verify Trade-offs**: Confirm that the conversion to lazy evaluation does not inadvertently cause massive CPU spikes due to unintended multi-pass recomputation. If multi-pass is required, cache the data safely.

@Examples (Do's and Don'ts)

**Principle: Generating Sequences**
- [DO]
```python
def fibonacci_gen(num_items):
    a, b = 0, 1
    while num_items:
        yield a
        a, b = b, a + b
        num_items -= 1
```
- [DON'T]
```python
def fibonacci_list(num_items):
    numbers = []
    a, b = 0, 1
    while len(numbers) < num_items:
        numbers.append(a)
        a, b = b, a + b
    return numbers # Allocates massive memory for large num_items
```

**Principle: Counting with Comprehensions**
- [DO]
```python
# Uses O(1) memory
divisible_by_three = sum(1 for n in fibonacci_gen(100_000) if n % 3 == 0)
```
- [DON'T]
```python
# Creates an unnecessary list in memory just to count elements
divisible_by_three = len([n for n in fibonacci_gen(100_000) if n % 3 == 0])
```

**Principle: Infinite Series and Takewhile**
- [DO]
```python
from itertools import takewhile

def fibonacci():
    i, j = 0, 1
    while True:
        yield i
        i, j = j, i + j

# Decouples generation from bounding logic
first_5000 = takewhile(lambda x: x < 5000, fibonacci())
count = sum(1 for x in first_5000 if x % 2)
```
- [DON'T]
```python
def fibonacci_naive():
    i, j = 0, 1
    count = 0
    # Generation and bounding logic are tightly coupled
    while i <= 5000:
        if i % 2:
            count += 1
        i, j = j, i + j
    return count
```

**Principle: Rolling Windows on Generators**
- [DO]
```python
from itertools import islice

def groupby_window(data_iterator, window_size=3600):
    window = tuple(islice(data_iterator, window_size))
    for item in data_iterator:
        yield window
        window = window[1:] + (item,)
```
- [DON'T]
```python
from collections import deque

def groupby_window_broken(data_iterator, window_size=3600):
    window = deque(maxlen=window_size)
    for _ in range(window_size):
        window.append(next(data_iterator))
    for item in data_iterator:
        yield window # DANGER: Yielding a mutable reference. Consumer will see changing data!
        window.append(item)
```