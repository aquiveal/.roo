@Domain
Code generation, refactoring, code review, or optimization requests involving Python robustness, performance optimization, resource management, exception handling, timezone calculations, mathematical precision, object serialization, queuing, list searching, and high-throughput memory operations.

@Vocabulary
- **Context Manager**: A function or class implementing `__enter__` and `__exit__` (or utilizing `@contextlib.contextmanager`) that defines a special scope for a block of code, automatically handling setup and teardown via the `with` statement.
- **UTC (Coordinated Universal Time)**: The standard, time-zone-independent representation of time, usually represented as seconds since the UNIX epoch.
- **Serialization/Deserialization**: The process of converting live Python objects to a stream of bytes (e.g., using `pickle`), and vice versa.
- **FIFO Queue**: A First-In, First-Out queue (Producer-Consumer queue) where the first items added are the first to be removed.
- **Priority Queue**: A queue that processes items in order of relative importance or natural sort order, rather than the order they were inserted.
- **Zero-Copy**: Operations that process large amounts of memory (like slicing binary data) without allocating new memory or duplicating the underlying data, avoiding CPU overhead.
- **Buffer Protocol**: A low-level C API in CPython that allows objects like `bytes` and `bytearray` to expose their underlying memory buffers.
- **Gradual Typing/Type Annotations**: (Contextual) The practice of applying types to ensure code correctness, often avoiding the need for extensive runtime checks.

@Objectives
- Maximize reliability by guaranteeing proper resource cleanup and distinct error-handling paths.
- Ensure cross-platform and globally accurate time calculations.
- Maintain data integrity and backwards compatibility during object serialization.
- Guarantee exact mathematical precision, especially for monetary or scientific calculations.
- Maximize I/O and CPU throughput by applying the correct high-performance data structures (deques, heaps, binary trees) and zero-copy memory views.
- Base all performance optimizations on empirical profiling data rather than intuition.

@Guidelines
- **Exception Handling & Resource Cleanup**
  - The AI MUST use the `try/finally` construct or `with` statements to ensure cleanup code (like closing file handles) always runs, regardless of exceptions.
  - The AI MUST use `try/except/else` blocks to minimize the amount of code inside the `try` block. The `else` block MUST be used for code that should only execute if the `try` block succeeds, visually distinguishing the success path and ensuring exceptions raised there propagate up normally.
  - The AI MUST combine `try/except/else/finally` when reading, processing, and updating resources to isolate specific error handling from cleanup logic.
  - The AI MUST prefer `with` statements and the `contextlib.contextmanager` decorator over raw `try/finally` blocks for repetitive context management tasks (e.g., locks, temporary logging level changes).
  - The AI MUST yield values from `@contextmanager` functions if the block needs to interact directly with the context object (via the `with ... as target` syntax).

- **Time and Dates**
  - The AI MUST NOT use the `time` built-in module for converting between different local time zones, as it is platform-dependent and highly error-prone.
  - The AI MUST use the `datetime` built-in module combined with the `pytz` package for timezone conversions.
  - The AI MUST always represent time in UTC internally, perform all necessary date/time math on the UTC values, and ONLY convert to local time as the final step before presentation to the user.

- **Serialization**
  - The AI MUST NOT use the `pickle` module for untrusted data (use `json` instead).
  - When using `pickle` for trusted data, the AI MUST use the `copyreg` built-in module to register serialization/deserialization functions. This prevents breakage when classes are renamed, attributes are added, or attributes are removed over time.
  - The AI MUST define constructors with default arguments for new class attributes to ensure older serialized objects deserialize successfully.
  - The AI MUST add a `version` parameter to the `copyreg` serialization dictionary to handle backwards-incompatible class changes (like removing fields).

- **Numerical Precision**
  - The AI MUST use the `Decimal` class from the `decimal` module (or `Fraction` from `fractions`) when exact precision and specific rounding behaviors are paramount (e.g., currency calculations).
  - The AI MUST initialize `Decimal` instances using `str` values or `int` values. The AI MUST NEVER initialize `Decimal` using `float` instances, as doing so immediately introduces IEEE 754 floating-point inaccuracies.
  - The AI MUST use `Decimal.quantize()` to round values strictly to the required decimal place.

- **Profiling and Optimization**
  - The AI MUST NOT optimize Python code based on intuition.
  - The AI MUST use the `cProfile` module instead of the pure-Python `profile` module to accurately measure performance with minimal overhead.
  - The AI MUST use `Profile.runcall()` to profile code and the `pstats.Stats` object to analyze the results (e.g., using `.sort_stats('cumulative')` and `.print_callers()`).

- **Queues and Searching**
  - The AI MUST NOT use a standard `list` for Producer-Consumer (FIFO) queues. Using `list.pop(0)` degrades performance superlinearly (O(N^2)) as the queue grows.
  - The AI MUST use `collections.deque` for FIFO queues, utilizing `.append()` to add items and `.popleft()` to consume items in constant O(1) time.
  - The AI MUST NOT use linear scans (e.g., `list.index()` or `for` loops) to search for items in large, sorted sequences.
  - The AI MUST use the `bisect` module (e.g., `bisect_left`) to perform logarithmic time (O(log N)) binary searches on sorted sequences.
  - The AI MUST NOT use standard list insertions and `list.sort()` to implement priority queues.
  - The AI MUST use the `heapq` built-in module (`heappush`, `heappop`, `heapify`) to build priority queues.
  - When using `heapq` with custom objects, the AI MUST use `@functools.total_ordering` and define at least the `__lt__` special method to provide a natural sort order.

- **Memory and I/O**
  - The AI MUST NOT slice `bytes` instances when parsing large amounts of data, as slicing creates copies and burns CPU time.
  - The AI MUST use the `memoryview` built-in type to wrap data supporting the buffer protocol (like `bytes`) to allow zero-copy slicing.
  - The AI MUST use the `bytearray` built-in type wrapped in a `memoryview` to perform zero-copy reads (e.g., `socket.recv_into()`) to splice new data directly into an arbitrary buffer location.

@Workflow
1. **Structural Analysis**: Review the requested Python code for external resource usage (files, sockets, locks). Apply `try/except/else/finally` or `contextlib.contextmanager` to ensure infallible cleanup and minimized `try` scopes.
2. **Time Check**: Scan for time manipulations. If timezone conversion is needed, explicitly import `datetime` and `pytz`, convert incoming local times to UTC, perform calculations in UTC, and convert back to local only at the boundary.
3. **Precision Check**: Identify monetary or high-precision math. Replace `float` with `Decimal(str(value))`.
4. **Data Structure Optimization**: 
   - Replace `list.pop(0)` implementations with `collections.deque`.
   - Replace `list.index` on sorted lists with `bisect.bisect_left`.
   - Replace repeatedly sorted lists with `heapq` implementations (ensuring `__lt__` is implemented on elements).
5. **Memory Optimization**: For large binary data operations or socket streaming, wrap byte streams in `memoryview` and `bytearray` to enforce zero-copy slicing and data ingestion.
6. **Serialization Hardening**: If `pickle` is used, implement `copyreg.pickle()` hooks to decouple the data format from the exact Python class definition, handling defaults and versions.

@Examples (Do's and Don'ts)

**[DO] Use try/except/else/finally correctly**
```python
def divide_json(path):
    handle = open(path, 'r+')
    try:
        data = handle.read()
        op = json.loads(data)
        value = op['numerator'] / op['denominator']
    except ZeroDivisionError:
        return None
    else:
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)
        return value
    finally:
        handle.close()
```

**[DON'T] Put unrelated or success-dependent code in the try block**
```python
def divide_json(path):
    handle = open(path, 'r+')
    try:
        data = handle.read()
        op = json.loads(data)
        value = op['numerator'] / op['denominator']
        # DON'T: File writing should be in the else block
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)
        return value
    except ZeroDivisionError:
        return None
    finally:
        handle.close()
```

**[DO] Use contextlib for reusable try/finally behavior**
```python
from contextlib import contextmanager
import logging

@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

with debug_logging(logging.DEBUG) as logger:
    logger.debug('Debug output!')
```

**[DO] Initialize Decimal with strings**
```python
from decimal import Decimal
# DO: Use string representation
rate = Decimal('1.45')
seconds = Decimal(222)
cost = rate * seconds / Decimal('60')
```

**[DON'T] Initialize Decimal with floats**
```python
from decimal import Decimal
# DON'T: Floating point inaccuracies are instantly captured by Decimal
rate = Decimal(1.45) 
```

**[DO] Use deque for Producer-Consumer Queues**
```python
import collections

def consume_queue(queue):
    while queue:
        # DO: O(1) removal from the left
        item = queue.popleft() 
        process(item)
```

**[DON'T] Use lists for FIFO queues**
```python
def consume_queue(queue):
    while queue:
        # DON'T: O(N) operation, scales quadratically
        item = queue.pop(0) 
        process(item)
```

**[DO] Use bisect for searching sorted sequences**
```python
from bisect import bisect_left

data = list(range(10**5))
# DO: Logarithmic time binary search
index = bisect_left(data, 91234)
```

**[DON'T] Use list.index for searching sorted sequences**
```python
data = list(range(10**5))
# DON'T: Linear time scan
index = data.index(91234)
```

**[DO] Use heapq for Priority Queues**
```python
from heapq import heappush, heappop
import functools

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
    def __lt__(self, other):
        return self.due_date < other.due_date

queue = []
heappush(queue, Book('Don Quixote', '2019-06-07'))
next_overdue = heappop(queue)
```

**[DO] Use memoryview and bytearray for zero-copy interactions**
```python
video_cache = b'some extremely large binary data...'
byte_offset = 1024
size = 1024 * 1024

# DO: Wrap with bytearray and memoryview for zero copy
video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset:byte_offset + size]
socket.recv_into(chunk)
```

**[DON'T] Slice bytes for high-throughput I/O**
```python
video_cache = b'some extremely large binary data...'
byte_offset = 1024
size = 1024 * 1024

# DON'T: This copies the data, burning CPU time
chunk = socket.recv(size)
before = video_cache[:byte_offset]
after = video_cache[byte_offset + size:]
new_cache = b''.join([before, chunk, after])
```