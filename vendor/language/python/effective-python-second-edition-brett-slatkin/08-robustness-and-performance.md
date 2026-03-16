# @Domain
This rule file is activated for all Python programming tasks involving robustness (hardening code, managing exceptions, handling time zones, serialization, precision math) and performance optimization (profiling, queue management, searching, zero-copy buffer operations). It governs architectural decisions for I/O handling, data structure selection, and safe state management.

# @Vocabulary
- **`try/except/else/finally`**: A compound statement for robust error handling. `else` runs on success, `finally` runs unconditionally for cleanup.
- **`contextlib.contextmanager`**: A decorator that transforms a generator function into a `with` statement context manager.
- **UTC (Coordinated Universal Time)**: The standard, time-zone-independent representation of time.
- **`pytz`**: A community module containing the full database of time zone definitions.
- **`pickle` / `copyreg`**: Modules used for serializing/deserializing Python objects across trusted binary channels. `copyreg` enforces backward compatibility.
- **`Decimal`**: A class providing fixed-point math to avoid IEEE 754 floating-point precision loss.
- **`quantize`**: A method of `Decimal` used to explicitly round fixed-point numbers to a specific decimal place.
- **`cProfile` / `pstats`**: C-extension profiler and statistics analyzer used for accurate performance measurement without heavy overhead.
- **`collections.deque`**: A double-ended queue providing $O(1)$ constant time `append` and `popleft` operations.
- **`bisect`**: A built-in module for $O(\log N)$ logarithmic time binary searches on sorted sequences.
- **`heapq`**: A built-in module for managing priority queues, providing $O(\log N)$ insertions and extractions.
- **Buffer Protocol**: A low-level C API exposing underlying data buffers.
- **`memoryview` / `bytearray`**: Types used to slice and mutate byte streams without triggering expensive memory copies (zero-copy operations).

# @Objectives
- Ensure safe and predictable exception handling and resource cleanup.
- Standardize context manager usage for reusable setup/teardown logic.
- Guarantee reliable time zone conversions and arithmetic.
- Maintain backward compatibility of serialized Python objects over time.
- Eliminate floating-point inaccuracies in financially or mathematically sensitive operations.
- Mandate measurement-driven optimization over intuition-based micro-optimizations.
- Enforce the use of algorithmically optimal data structures for queues, sorting, and searching.
- Maximize I/O throughput by utilizing zero-copy memory operations for byte streams.

# @Guidelines

## Robust Exception Handling
- **Utilize All Exception Blocks**: Use `finally` strictly for cleanup code (e.g., closing file handles) regardless of exceptions. Use `else` to minimize the code inside the `try` block, visually distinguish the success path, and allow exceptions from the success path to propagate upward without being accidentally caught by the `except` block.

## Reusable Context Managers
- **Prefer `with` Statements**: Replace repetitive `try/finally` blocks with `with` statements to manage specialized contexts (e.g., Locks, file handles).
- **Use `@contextmanager`**: Build custom context managers using `contextlib.contextmanager` and the `yield` keyword instead of writing heavy classes with `__enter__` and `__exit__`.
- **Provide `as` Targets**: Yield values from the context manager to populate the `as` target, allowing the executing block to interact directly with the context state.

## Robust Time Management
- **Never Use the `time` Module for Time Zones**: The `time` module is platform-dependent and fails inconsistently for non-local time zones. Use it only to convert between UTC and the host computer's local time.
- **Use `datetime` and `pytz`**: Always use the `datetime` module coupled with the `pytz` library for timezone operations.
- **Normalize to UTC**: Always convert local times to UTC immediately. Perform all datetime operations (offsetting, arithmetic) on UTC values. Convert back to local time exclusively as the final step before human presentation.

## Reliable Serialization
- **Use `pickle` Only for Trusted Data**: `pickle` is unsafe by design. Use JSON for untrusted communication.
- **Control Pickling with `copyreg`**: Never rely on `pickle`'s default behavior for complex objects, as added or removed attributes will break backward compatibility. Register serialization/deserialization functions using `copyreg`.
- **Use Default Arguments**: In deserialization constructors, provide default values for arguments so older pickled objects seamlessly receive new attributes.
- **Version Classes**: Add a `version` key to the serialized kwargs dictionary. Use this version in your unpickling function to safely adapt or delete deprecated fields.
- **Provide Stable Import Paths**: Register a stable identifier (e.g., the unpickling function itself) with `copyreg` to prevent pickling breakage when classes are renamed or moved across modules.

## Precision Math
- **Use `Decimal` for Exact Math**: Replace `float` with `decimal.Decimal` when exact precision is required (e.g., monetary calculations).
- **Initialize with Strings**: Always pass string instances (`str`) to the `Decimal` constructor instead of `float` instances to prevent initial IEEE 754 precision loss.
- **Control Rounding**: Use `Decimal.quantize` (e.g., with `ROUND_UP`) to enforce explicit rounding behavior.

## Performance Profiling
- **Profile Before Optimizing**: Ignore intuition. Measure program performance first to identify the actual bottlenecks (Amdahl's law).
- **Avoid `profile`**: Use the `cProfile` module exclusively. The pure-Python `profile` module imposes high overhead that skews results.
- **Trace Callers**: Use `pstats.Stats` and `print_callers()` to determine which upstream functions are responsible for the cumulative execution time of heavily utilized utility functions.
- **Isolate I/O**: Ensure the profiler is measuring code performance, not the latency of underlying disk or network systems. Warm up caches before starting the profiler.

## High-Performance Data Structures
- **Use `deque` for FIFO Queues**: Never use `list.pop(0)` for consumer queues. It triggers an $O(N)$ shift of all elements, degrading superlinearly. Use `collections.deque` and `popleft()` for $O(1)$ performance.
- **Use `bisect` for Searching Sorted Lists**: Never use `list.index()` or `for` loops to search sorted arrays ($O(N)$). Use `bisect.bisect_left` for logarithmic $O(\log N)$ search performance.
- **Use `heapq` for Priority Queues**: Never use a `list` with a subsequent `sort()` call to manage priority tasks ($O(N \log N)$). Use `heapq.heappush` and `heapq.heappop` for $O(\log N)$ scaling.
- **Make Heap Items Comparable**: Ensure objects placed into a `heapq` implement the `__lt__` special method (via `@functools.total_ordering`).
- **Lazy Deletion in Heaps**: Do not actively `remove()` items from a priority queue (which requires an $O(N)$ scan). Flag them as invalid (e.g., `returned = True`) and silently skip/pop them when they reach the top of the heap.

## Zero-Copy I/O
- **Avoid Slicing `bytes`**: Slicing `bytes` creates expensive in-memory copies, crippling throughput.
- **Use `memoryview`**: Wrap byte data in a `memoryview` to expose the buffer protocol. Slicing a `memoryview` returns a new view, completely avoiding data copying.
- **Use `bytearray`**: For mutable byte streams, use `bytearray`. Splicing incoming chunks can be done by taking a `memoryview` of the `bytearray` and calling methods like `socket.recv_into(chunk)`.

# @Workflow
1. **Exception Review**: Analyze all `try` blocks. Move non-error-throwing, post-success logic into an `else` block. Move cleanup logic into a `finally` block or a `@contextmanager`.
2. **Time Handling Verification**: Locate all `time` module usages. Replace time zone mathematics with `datetime` and `pytz`. Ensure all intermediate data representations are strictly UTC.
3. **Serialization Audit**: If `pickle` is used, implement a `copyreg` registration function. Introduce a `version` parameter and ensure all class modifications handle missing/legacy kwargs gracefully.
4. **Floating-Point Audit**: Replace `float` with `Decimal` initialized via strings for any exact-precision math. Add `.quantize()` for precise rounding.
5. **Performance Measurement**: Run `cProfile` and `pstats` before making algorithmic changes. Identify the specific bottleneck.
6. **Data Structure Replacement**: 
   - Replace `list` queues with `collections.deque`.
   - Replace linear searches on sorted data with `bisect_left`.
   - Replace sorted lists with `heapq`.
7. **Memory Buffer Optimization**: Refactor high-throughput `bytes` slicing into `memoryview` and `bytearray` logic with `recv_into()`.

# @Examples (Do's and Don'ts)

## Exception Handling Blocks
- **[DON'T]** Mix success execution and cleanup logic blindly in a `try` block.
```python
def divide_json(path):
    handle = open(path, 'r+')
    try:
        data = handle.read()
        op = json.loads(data)
        value = op['numerator'] / op['denominator']
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)
        return value
    except ZeroDivisionError:
        return UNDEFINED
    finally:
        handle.close()
```
- **[DO]** Isolate the vulnerable code in `try`, catch specific exceptions, use `else` for subsequent execution, and `finally` for teardown.
```python
def divide_json(path):
    handle = open(path, 'r+')
    try:
        data = handle.read()
        op = json.loads(data)
        value = op['numerator'] / op['denominator']
    except ZeroDivisionError:
        return UNDEFINED
    else:
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)
        return value
    finally:
        handle.close()
```

## Context Managers
- **[DON'T]** Repeat `try/finally` state manipulation globally.
```python
logger = logging.getLogger()
old_level = logger.getEffectiveLevel()
logger.setLevel(logging.DEBUG)
try:
    my_function()
finally:
    logger.setLevel(old_level)
```
- **[DO]** Use `@contextmanager` to yield control and handle cleanup cleanly.
```python
from contextlib import contextmanager

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
    logger.debug("Inside context")
```

## Local Clocks and Time Zones
- **[DON'T]** Use the `time` module to parse or convert remote time zones.
```python
# Fails depending on platform OS
arrival_nyc = '2019-03-16 23:33:24 EDT'
time_tuple = time.strptime(arrival_nyc, '%Y-%m-%d %H:%M:%S %Z')
```
- **[DO]** Use `datetime` and `pytz` to convert to UTC first, then localize to the target time zone.
```python
import pytz
from datetime import datetime

arrival_nyc = '2019-03-16 23:33:24'
time_format = '%Y-%m-%d %H:%M:%S'
nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)

eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))

pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
```

## Decimal Precision
- **[DON'T]** Use `float` or initialize `Decimal` with a `float` instance for exact arithmetic.
```python
rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(round(cost, 2)) # May round incorrectly due to IEEE 754 limits

# Also bad:
bad_decimal = Decimal(1.45) # Loses precision immediately
```
- **[DO]** Initialize `Decimal` with `str` and use `.quantize()` for controlled rounding.
```python
from decimal import Decimal, ROUND_UP

rate = Decimal('1.45')
seconds = Decimal(3*60 + 42)
cost = rate * seconds / Decimal(60)
rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
```

## Producer-Consumer Queues
- **[DON'T]** Use a `list` for a FIFO queue.
```python
queue = []
queue.append(email) # Producer
email = queue.pop(0) # Consumer: O(N) operation, degrades superlinearly
```
- **[DO]** Use `collections.deque`.
```python
import collections

queue = collections.deque()
queue.append(email) # Producer
email = queue.popleft() # Consumer: O(1) operation
```

## Searching Sorted Sequences
- **[DON'T]** Use `list.index()` or iterative scanning.
```python
index = data.index(91234) # O(N) scan
```
- **[DO]** Use `bisect_left`.
```python
from bisect import bisect_left
index = bisect_left(data, 91234) # O(log N) binary search
```

## Priority Queues
- **[DON'T]** Append to a list and continuously sort it.
```python
queue.append(book)
queue.sort(key=lambda x: x.due_date, reverse=True) # Superlinear degradation
```
- **[DO]** Use `heapq` and `@functools.total_ordering`.
```python
import functools
from heapq import heappush, heappop

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.returned = False
    
    def __lt__(self, other):
        return self.due_date < other.due_date

queue = []
heappush(queue, book)

# Lazy removal of cancelled/returned items
while queue:
    top_book = queue[0]
    if top_book.returned:
        heappop(queue)
        continue
    # Process top_book...
```

## Zero-Copy I/O
- **[DON'T]** Slice `bytes` instances to send or splice data.
```python
# Creates an expensive copy in memory
chunk = video_data[byte_offset:byte_offset + size] 
new_cache = b''.join([before, chunk, after])
```
- **[DO]** Use `memoryview` and `bytearray` to access and mutate buffers without copying.
```python
# Zero-copy slicing for sending
video_view = memoryview(video_data)
chunk = video_view[byte_offset:byte_offset + size]

# Zero-copy receiving into a pre-allocated buffer
video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset:byte_offset + size]
socket.recv_into(chunk)
```