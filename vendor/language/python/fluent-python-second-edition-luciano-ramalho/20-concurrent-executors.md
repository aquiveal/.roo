# @Domain
Python programming tasks involving concurrent execution, parallel processing, I/O-bound network operations (e.g., HTTP clients), CPU-bound mathematical/data operations, and explicit usage of the `concurrent.futures` package.

# @Vocabulary
- **Executor**: An interface encapsulating the asynchronous execution of callables, managing thread/process pools and work/result queues automatically (`ThreadPoolExecutor` and `ProcessPoolExecutor`).
- **Future**: An object representing a deferred computation that may or may not have completed. It encapsulates a pending operation so its state can be checked and its result (or exception) retrieved.
- **I/O-Bound Task**: A computation that spends most of its time waiting for input/output operations (e.g., network requests, disk reads). Unaffected by the GIL because Python releases the GIL during I/O.
- **CPU-Bound Task**: A computation that spends most of its time performing intensive processor calculations. Highly restricted by the GIL in multi-threading.
- **GIL (Global Interpreter Lock)**: A mechanism in CPython that prevents multiple native threads from executing Python bytecodes at once.
- **as_completed**: A function from `concurrent.futures` that takes an iterable of futures and returns an iterator that yields those futures as they finish (out of order).
- **Poison Pill**: A sentinel value (often `None`, `0`, or `...`) used in low-level queue management to signal a worker to shut down, though `concurrent.futures` hides this low-level detail.

# @Objectives
- Simplify concurrency by treating threads, processes, and queues as infrastructure managed by high-level `Executor` classes, rather than manual constructs.
- Maximize throughput by matching the workload type (I/O vs. CPU) to the appropriate executor pool (Thread vs. Process).
- Ensure safe execution and cleanup by strictly utilizing executors as context managers.
- Manage asynchronous results and exceptions robustly without blocking the main execution thread prematurely.

# @Guidelines
- **Executor Selection**:
  - The AI MUST use `ThreadPoolExecutor` for I/O-bound tasks (e.g., downloading files, making HTTP requests).
  - The AI MUST use `ProcessPoolExecutor` for CPU-bound tasks (e.g., parsing large datasets, heavy mathematical computations) to bypass the GIL.
- **Context Management**: The AI MUST instantiate `Executor` classes using the `with` statement (context manager) to guarantee that `executor.shutdown(wait=True)` is called automatically, blocking until all workers finish cleanly.
- **Task Submission and Result Retrieval**:
  - If the AI needs to apply the same callable to an iterable of arguments and requires the results in the *exact same order* as the input, the AI MUST use `executor.map()`.
  - If the AI needs to process results *as soon as they are ready* (regardless of submission order), or needs to submit varying callables/arguments, the AI MUST use `executor.submit()` combined with `concurrent.futures.as_completed()`.
- **The `as_completed` Idiom**: When using `as_completed`, the AI MUST build a dictionary mapping each `Future` instance to its corresponding input data (e.g., `future_to_url = {executor.submit(func, url): url}`). This is critical because `as_completed` yields futures out of order, and the AI must retain the context of what each future represents.
- **Future Instantiation**: The AI MUST NOT instantiate `concurrent.futures.Future` objects directly. Futures MUST only be created by the framework as a return value of `Executor.submit()`.
- **Exception Handling**: The AI MUST wrap `future.result()` calls in a `try/except` block. Exceptions raised inside the worker thread/process are captured by the framework and re-raised only when `.result()` is invoked (or when the iterator from `.map()` yields the result).
- **Worker Limits**: When configuring `ThreadPoolExecutor`, the AI SHOULD omit the `max_workers` argument to allow Python to compute a sensible default (which scales based on CPU count but caps at 32 to avoid resource exhaustion), UNLESS a specific constraint (e.g., rate-limiting an API) requires a hard cap.
- **Avoiding Stateful Failures**: The AI MUST NOT mutate the arguments passed to the worker functions in ways that cause race conditions. Workers MUST return new objects or scalar values as results.

# @Workflow
1. **Analyze Workload**: Determine if the target function is I/O-bound (e.g., `httpx.get`) or CPU-bound (e.g., calculating primes).
2. **Select Executor**: Choose `ThreadPoolExecutor` (I/O) or `ProcessPoolExecutor` (CPU).
3. **Determine Result Handling strategy**:
   - If order matters and the task is uniform: use `.map()`.
   - If order does not matter and immediate processing upon completion is preferred: use `.submit()` + `as_completed()`.
4. **Implement Context Manager**: Wrap the executor initialization in a `with` block.
5. **Submit Tasks**:
   - For `.submit()`, initialize an empty dictionary (e.g., `to_do_map = {}`).
   - Iterate over the input data, call `executor.submit()`, and assign `to_do_map[future] = input_data`.
6. **Iterate and Resolve**:
   - Pass the dictionary (or list of futures) to `concurrent.futures.as_completed()`.
   - Inside the loop, extract the result using `future.result()` enclosed in a `try/except` block targeting the specific exceptions the worker might raise.
   - If an exception occurs, retrieve the input context from the dictionary (`to_do_map[future]`) to log or handle the specific failure gracefully.

# @Examples (Do's and Don'ts)

**[DO] Use an executor as a context manager and map for ordered results:**
```python
from concurrent import futures

def download_many(url_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor:
        # .map returns results in the exact order of url_list
        results = executor.map(download_one, url_list)
        return len(list(results))
```

**[DON'T] Manually manage threads/processes or leave executors unclosed:**
```python
from concurrent.futures import ThreadPoolExecutor

def download_many(url_list: list[str]) -> int:
    # Anti-pattern: Missing 'with' block, requires manual shutdown
    executor = ThreadPoolExecutor(max_workers=10)
    results = executor.map(download_one, url_list)
    return len(list(results)) 
```

**[DO] Use the `as_completed` dictionary mapping idiom with robust exception handling:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import httpx

def download_many(cc_list: list[str], base_url: str) -> dict:
    status_counts = {'OK': 0, 'ERROR': 0}
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        # Dictionary mapping future to context
        to_do_map = {}
        for cc in cc_list:
            future = executor.submit(download_one, cc, base_url)
            to_do_map[future] = cc
            
        for future in as_completed(to_do_map):
            cc = to_do_map[future] # Retrieve context
            try:
                status = future.result()
            except httpx.HTTPStatusError as exc:
                print(f'{cc} error: HTTP {exc.response.status_code}')
                status_counts['ERROR'] += 1
            except Exception as exc:
                print(f'{cc} error: {exc}')
                status_counts['ERROR'] += 1
            else:
                status_counts['OK'] += 1
                
    return status_counts
```

**[DON'T] Call `future.result()` without a try/except block, or lose track of input context:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_many(cc_list: list[str], base_url: str) -> list:
    with ThreadPoolExecutor() as executor:
        futures_list = [executor.submit(download_one, cc, base_url) for cc in cc_list]
        
        results = []
        for future in as_completed(futures_list):
            # Anti-pattern 1: No try/except. A failed download crashes the entire aggregator.
            # Anti-pattern 2: We don't know which 'cc' failed if it does crash.
            res = future.result() 
            results.append(res)
            
    return results
```

**[DON'T] Instantiate `Future` objects manually:**
```python
from concurrent.futures import Future

# Anti-pattern: Client code should not instantiate Futures.
my_future = Future() 
my_future.set_result(42)
```

**[DO] Use `ProcessPoolExecutor` for CPU-bound mathematical operations:**
```python
from concurrent.futures import ProcessPoolExecutor
from primes import is_prime

def check_primes(numbers: list[int]) -> dict[int, bool]:
    # Bypasses the GIL to use multiple CPU cores
    with ProcessPoolExecutor() as executor:
        results = executor.map(is_prime, numbers)
    return dict(zip(numbers, results))
```