# @Domain
These rules MUST trigger when the user requests assistance with parallelizing Python code, optimizing CPU-bound tasks, utilizing the `multiprocessing` or `joblib` modules, implementing Interprocess Communication (IPC), managing concurrent workers/pools, or sharing large data structures (like NumPy arrays) across multiple Python processes.

# @Vocabulary
- **Amdahl’s Law**: A principle stating that the maximum expected speedup from parallelization is strictly limited by the proportion of the code that must remain serial.
- **Embarrassingly Parallel**: A problem that requires little to no effort to separate into parallel tasks because there is no dependency or communication required between the processes.
- **GIL (Global Interpreter Lock)**: A mutex in CPython that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once.
- **Process**: A forked copy of the current Python interpreter running as an independent OS child process with its own private memory space and GIL.
- **Thread**: An OS-native thread bound by the Python GIL, suitable ONLY for I/O-bound tasks in Python, not CPU-bound calculations.
- **Pool**: A high-level `multiprocessing` component that wraps processes or threads to distribute chunks of work and aggregate results.
- **Queue**: A FIFO queue allowing multiple producers and consumers, utilizing Python's `pickle` for serialization.
- **Poison Pill (Sentinel)**: A specific flag or token (e.g., `b"WORK_FINISHED"`) inserted into a work queue to safely signal consumer processes to terminate.
- **IPC (Interprocess Communication)**: Mechanisms for processes to share state, including `Manager`, `Value`, `RawValue`, `mmap`, and external data stores like Redis.
- **Manager**: A `multiprocessing` component that provides proxy objects to safely share high-level Python objects (lists, dicts) across processes at the cost of high synchronization overhead.
- **RawValue / RawArray**: Wrappers around `ctypes` memory blocks that lack synchronization primitives, offering fast but unsafe shared memory.
- **mmap**: Memory-mapped file support, used with an anonymous block (`mmap(-1, size)`) for the absolute fastest, lock-free byte sharing between local processes.
- **Chunksize**: The number of work items submitted to a worker process in a single batch.
- **Joblib**: A third-party library built on `Loky` and `cloudpickle` providing lightweight pipelining, disk-based caching, and simple parallelization, highly optimized for NumPy.

# @Objectives
- The AI MUST maximize CPU utilization by distributing CPU-bound workloads across multiple independent processes, bypassing the GIL.
- The AI MUST protect system RAM by avoiding unnecessary data duplication across forked processes, utilizing shared memory protocols when working with massive datasets.
- The AI MUST strictly enforce thread/process safety, explicitly locking shared mutable states and avoiding non-atomic operations.
- The AI MUST ensure deterministic and mathematically sound randomness by explicitly re-seeding random number generators within child processes.
- The AI MUST minimize IPC synchronization overhead by applying serial pre-checks, unrolling loops, and selecting the lowest-overhead sharing mechanism suitable for the task.

# @Guidelines

## Process vs. Thread Selection
- When parallelizing a CPU-bound task, the AI MUST use `multiprocessing.Process`, `multiprocessing.Pool`, or `joblib.Parallel`.
- When parallelizing an I/O-bound task, the AI MUST use threads (e.g., `multiprocessing.dummy.Pool` or `concurrent.futures.ThreadPoolExecutor`).
- The AI MUST NOT use threads for CPU-bound Python loops, as the GIL will force serial execution, yielding zero speedup.

## Resource and RAM Management
- The AI MUST NOT hardcode the number of processes (e.g., `NUM_PROCESSES = 8`) unless explicitly requested for resource management. Default to the system's available cores.
- The AI MUST warn the user about hyperthreading limitations: hyperthreads share floating-point silicon. If the physical cores are completely saturated with floating-point math, adding processes for hyperthreads will yield zero speedup and waste RAM.
- The AI MUST calculate or estimate the RAM consumed per forked process (typically 10-20MB for standard libraries, up to hundreds of MBs with heavy data). If the system exceeds available RAM and resorts to disk swap, all parallelization benefits are instantly destroyed.

## Randomness in Parallel Processes
- When using `numpy.random` inside forked processes, the AI MUST explicitly call `np.random.seed()` at the start of the worker function. Without this, every child process will inherit the exact same random state from the parent and generate identical results.
- Note: Python's built-in `random` module is automatically re-seeded by `multiprocessing` upon fork, but `numpy.random` is NOT.

## Workload Distribution and Chunking
- If worker tasks have highly variable execution times, the AI MUST recommend randomizing the job sequence or sorting it so the slowest jobs are processed first, preventing a single long-running job from underutilizing CPUs at the end of the run.
- When configuring `chunksize` in a `Pool.map`, the AI MUST default to the `multiprocessing` default unless there is verified profiling evidence to change it.
- If adjusting `chunksize`, the AI MUST ensure the total number of chunks evenly aligns with the number of physical CPUs to prevent "trailing" chunks that leave CPUs idle.

## Joblib over Multiprocessing
- The AI SHOULD prefer `joblib` (`from joblib import Parallel, delayed`) over raw `multiprocessing` for scientific computing, pure Python loops, or NumPy array processing.
- When using `joblib.Memory` to cache function results, the AI MUST ensure that the function signature receives a unique identifier (like an index) if the function is called multiple times with the identical primary arguments but expects different probabilistic outcomes (e.g., Monte Carlo simulations). Otherwise, the cache will erroneously return the exact same result for every worker.
- The AI MUST NOT pass excessively large data structures via `joblib` or `multiprocessing` arguments, as the serialization (`pickle`/`cloudpickle`) overhead will negate parallelization gains. Use `shelve` or shared memory instead.

## Interprocess Communication (IPC) and State Sharing
- The AI MUST avoid sharing state between processes whenever possible. If state sharing is required, the AI MUST evaluate mechanisms in order of performance (fastest to slowest): `mmap` -> `RawValue` -> `Manager.Value` / `Redis` -> `Queue` -> Files.
- **Serial Pre-checks**: Before pushing work to an expensive parallel IPC architecture, the AI MUST implement a fast, serial pre-check for highly probable early-exit conditions (e.g., checking if a number is divisible by 2, 3, 5 before submitting to a pool).
- **Queues**: When using `multiprocessing.Queue`, the AI MUST implement "Poison Pills" (sentinel values) to safely terminate workers. The AI MUST push exactly one poison pill per worker process.
- **Redis**: The AI MAY recommend Redis for sharing state if cross-language compatibility, multi-machine distribution, or external visibility/debugging is required.
- **mmap**: For the absolute fastest binary flag sharing, the AI MUST use an anonymous memory map: `mmap.mmap(-1, 1)`.
- **Optimization of IPC Checks**: The AI MUST NOT check shared flags on every iteration of a tight inner loop. Use a counter (e.g., check every 1000 iterations). To further optimize, unroll the loop to eliminate decrementing the counter entirely (use `for outer in range(start, end, 1000):` and an inner loop bounded by the outer step).

## Atomic Operations and Locking
- When using `multiprocessing.Value`, the AI MUST explicitly use `multiprocessing.Lock()` (e.g., `with lock: value.value += 1`) if the value is being mutated. The built-in lock on `Value` prevents simultaneous read/writes but DOES NOT make `+=` operations atomic.
- When locking files, the AI MUST use a 3rd party tool like `fasteners` (`@fasteners.interprocess_locked('lockfile')`) and standard context managers (`with open(...)`) to prevent data corruption from concurrent writes.

## Sharing Large NumPy Arrays (Zero-Copy)
- To share a massive NumPy array across processes without RAM duplication, the AI MUST:
  1. Allocate a flat 1D shared memory block: `shared_base = multiprocessing.Array(ctypes.c_double, SIZE, lock=False)`.
  2. Wrap it with NumPy: `main_nparray = np.frombuffer(shared_base, dtype=ctypes.c_double)`.
  3. Reshape it locally: `main_nparray = main_nparray.reshape(ROWS, COLS)`.
  4. Ensure workers access this global/shared reference via indices, rather than passing the array through function arguments.

# @Workflow
When tasked with parallelizing Python code, the AI MUST execute the following sequence:
1. **Analyze CPU vs I/O**: Determine if the bottleneck is CPU-bound (math, loops) or I/O-bound (network, disk). Select Processes/Joblib for CPU, Threads/Async for I/O.
2. **Minimize State**: Refactor the algorithm to be as "embarrassingly parallel" as possible, stripping away shared variables or moving them to a post-processing reduction phase.
3. **Serial Pre-Check Integration**: Insert lightweight serial checks in the parent process to handle trivial cases before invoking the overhead of process forking.
4. **Randomness Isolation**: If using NumPy, insert `np.random.seed()` at the very beginning of the target worker function.
5. **Memory Strategy**: If large datasets are involved, design a zero-copy shared memory architecture (`frombuffer` with `multiprocessing.Array`).
6. **Worker Orchestration**: Implement the Pool or Queue. If using Queues, implement asynchronous job feeders and inject poison pills.
7. **Locking & IPC**: If mutation of shared state is strictly required, inject explicit `multiprocessing.Lock` context managers.

# @Examples (Do's and Don'ts)

## Random Seeding in NumPy
- **[DON'T]** Rely on the parent process seed for NumPy in a process pool:
```python
import numpy as np
from multiprocessing import Pool

def worker(task):
    # DANGER: All workers will generate the exact same random sequence!
    return np.random.uniform(0, 1)
```
- **[DO]** Re-seed NumPy explicitly inside the worker:
```python
import numpy as np
from multiprocessing import Pool

def worker(task):
    # Safe: Generates unique entropy per forked process
    np.random.seed()
    return np.random.uniform(0, 1)
```

## Atomic Updates to Shared Values
- **[DON'T]** Assume `multiprocessing.Value` provides atomic increments:
```python
import multiprocessing

def worker(shared_val):
    for _ in range(1000):
        # DANGER: Not atomic, race conditions will lead to lost counts!
        shared_val.value += 1 
```
- **[DO]** Use an explicit `multiprocessing.Lock`:
```python
import multiprocessing

def worker(shared_val, lock):
    for _ in range(1000):
        with lock:
            shared_val.value += 1
```

## Worker Termination via Queues
- **[DON'T]** Leave consumers hanging indefinitely:
```python
def worker(q):
    while True:
        item = q.get()
        process(item) # Will hang forever when queue is empty
```
- **[DO]** Use a Poison Pill / Sentinel value:
```python
FLAG_ALL_DONE = b"WORK_FINISHED"

def worker(in_q, out_q):
    while True:
        item = in_q.get()
        if item == FLAG_ALL_DONE:
            break # Safely exit
        out_q.put(process(item))
```

## Sharing Large NumPy Arrays
- **[DON'T]** Pass large arrays through `Pool.map` arguments:
```python
# DANGER: This will pickle and duplicate the 30GB array for every worker, exhausting RAM instantly.
pool.map(worker, [(large_array, idx) for idx in ranges])
```
- **[DO]** Use a lock-free `multiprocessing.Array` and `numpy.frombuffer` in the global scope:
```python
import ctypes
import multiprocessing
import numpy as np

# Create shared memory block
shared_base = multiprocessing.Array(ctypes.c_double, 1000 * 1000, lock=False)
# Wrap with NumPy and reshape
shared_array = np.frombuffer(shared_base, dtype=ctypes.c_double).reshape(1000, 1000)

def worker(row_idx):
    # Access the global shared_array by index
    shared_array[row_idx, :] = np.random.random(1000)
```