# @Domain
Python codebase modifications involving concurrency, parallelism, asynchronous programming (asyncio), thread management, subprocess execution, or performance optimizations for I/O-bound and CPU-bound workloads. Triggered when requested to parallelize tasks, refactor synchronous code to asynchronous, coordinate threads, or improve execution speed.

# @Vocabulary
- **Concurrency**: Executing multiple paths of execution seemingly simultaneously (interleaved progress), typically used for I/O-bound tasks.
- **Parallelism**: Executing multiple paths of execution genuinely at the same time across multiple CPU cores, used for CPU-bound tasks.
- **GIL (Global Interpreter Lock)**: A CPython mutex that prevents multiple threads from executing Python bytecode in parallel.
- **Fan-out**: Spawning multiple concurrent execution paths for a discrete workload.
- **Fan-in**: Waiting for and aggregating the results of multiple concurrent execution paths.
- **Data Race**: State corruption caused by uncoordinated preemptive multithreading where the GIL pauses a thread mid-operation (e.g., during `+=`).
- **Coroutine**: A function defined with `async def` that pauses and yields control back to an event loop via the `await` keyword.
- **Event Loop**: The asyncio mechanism that rapidly interleaves execution between coroutines.
- **Top-down Migration**: Transitioning a synchronous codebase to asyncio by starting at the main entry points and pushing synchronous calls down to executors.
- **Bottom-up Migration**: Transitioning to asyncio by starting at leaf functions and wrapping them in `run_until_complete` for synchronous callers.

# @Objectives
- Correctly distinguish between I/O-bound and CPU-bound workloads and apply the corresponding optimal Python concurrency or parallelism model.
- Prevent data races and ensure thread safety using explicit locking and coordination structures.
- Maximize system resource efficiency by avoiding unbounded thread creation, memory explosions, and context-switching overhead.
- Ensure the asyncio event loop remains highly responsive by keeping blocking operations strictly off the main thread.
- Provide graceful degradation and avoid deadlocks through explicit timeouts and proper exception propagation.

# @Guidelines

- **Subprocess Management (Item 52)**
  - The AI MUST use the `subprocess` module to manage child processes. Use `subprocess.run` for simple execution and `subprocess.Popen` for advanced I/O pipelines.
  - The AI MUST pass the `timeout` parameter to the `communicate()` method to prevent deadlocks from misbehaving child processes.

- **Thread Usage and Limitations (Item 53, 54)**
  - The AI MUST use `threading` exclusively for blocking I/O tasks. 
  - The AI MUST NOT use threads for CPU-bound parallel computation due to the GIL.
  - The AI MUST use `threading.Lock` within a `with` statement to protect shared state mutations across threads. The AI MUST NOT assume the GIL protects against data races.

- **Thread Coordination and Fan-Out (Item 55, 56, 57)**
  - The AI MUST use `queue.Queue` to coordinate work between threads and build concurrent pipelines. 
  - The AI MUST NOT use `list` with `append` and `pop(0)` for thread queues.
  - The AI MUST NOT create new `Thread` instances dynamically inside a loop for on-demand fan-out.

- **Executors (Item 58, 59, 64)**
  - The AI MUST prefer `concurrent.futures.ThreadPoolExecutor` over manually constructing thread pools with `Queue` for simple fan-out/fan-in I/O scenarios.
  - The AI MUST use `concurrent.futures.ProcessPoolExecutor` to achieve true parallelism for CPU-bound tasks.
  - The AI MUST restrict `ProcessPoolExecutor` workloads to isolated, high-leverage functions to minimize serialization (Pickle) overhead across process boundaries.

- **Coroutines and Asyncio (Item 60, 61, 63)**
  - The AI MUST use `asyncio` and coroutines (`async`/`await`) to achieve highly concurrent I/O operations (e.g., thousands of simultaneous connections).
  - The AI MUST NOT execute blocking system calls (e.g., file I/O, `time.sleep`, synchronous socket calls) directly within the asyncio event loop.
  - The AI MUST enable `debug=True` via `asyncio.run(..., debug=True)` during development to identify coroutines that block the event loop.

- **Asyncio Migration (Item 62)**
  - The AI MUST use `loop.run_in_executor` to execute legacy blocking synchronous functions from within an asynchronous coroutine.
  - The AI MUST use `asyncio.run_coroutine_threadsafe` or `loop.run_until_complete` to execute asynchronous coroutines from legacy synchronous threads.

# @Workflow
1. **Workload Analysis**: Determine if the requested task is I/O-bound (network, filesystem, subprocess) or CPU-bound (heavy computation, mathematical processing).
2. **Subprocess Routing**: If the task involves running external command-line tools, implement using `subprocess.run` or `subprocess.Popen` with timeouts.
3. **CPU-Bound Routing**: If the task is CPU-bound, implement using `concurrent.futures.ProcessPoolExecutor`. Ensure data passed to workers is minimal and picklable.
4. **Massive I/O Routing**: If the task requires massive I/O concurrency, implement using `asyncio` coroutines. Use `asyncio.gather` for fan-in.
5. **Limited I/O Routing**: If the task is I/O bound but must integrate with legacy synchronous libraries, implement using `concurrent.futures.ThreadPoolExecutor`.
6. **Thread Safety Verification**: If raw threads are manipulated, scan all shared objects for state mutations. Wrap all state mutations in `with lock:` blocks. Replace list-based queues with `queue.Queue`.
7. **Async Event Loop Audit**: If generating `asyncio` code, audit all code paths within `async def` blocks. Identify any standard library blocking calls (e.g., `open()`, `read()`, `time.sleep()`). Wrap these calls in `loop.run_in_executor`.

# @Examples (Do's and Don'ts)

**Subprocesses**
- [DO]:
  ```python
  import subprocess
  proc = subprocess.Popen(['sleep', '10'])
  try:
      proc.communicate(timeout=0.1)
  except subprocess.TimeoutExpired:
      proc.terminate()
      proc.wait()
  ```
- [DON'T]: Call `.communicate()` without a timeout, which can cause the Python parent process to hang indefinitely.

**Thread Data Races**
- [DO]:
  ```python
  from threading import Lock
  
  class LockingCounter:
      def __init__(self):
          self.lock = Lock()
          self.count = 0
          
      def increment(self, offset):
          with self.lock:
              self.count += offset
  ```
- [DON'T]: Use `self.count += offset` in a threaded context without a lock, as the GIL will not prevent context switching mid-addition.

**On-Demand Fan-Out**
- [DO]:
  ```python
  from concurrent.futures import ThreadPoolExecutor
  
  def process_items(items):
      with ThreadPoolExecutor(max_workers=10) as pool:
          futures = [pool.submit(my_io_task, item) for item in items]
          results = [f.result() for f in futures]
      return results
  ```
- [DON'T]: Loop over items and instantiate raw `Thread` objects dynamically (e.g., `thread = Thread(...); thread.start()`), which triggers memory exhaustion and massive context-switch overhead.

**Blocking the Event Loop**
- [DO]:
  ```python
  import asyncio
  
  async def write_data(data):
      loop = asyncio.get_running_loop()
      # Offload blocking file I/O to a thread pool
      await loop.run_in_executor(None, blocking_file_write, data)
  ```
- [DON'T]:
  ```python
  import asyncio
  
  async def write_data(data):
      # This blocks the entire asyncio event loop!
      with open('file.txt', 'wb') as f:
          f.write(data)
  ```

**CPU-Bound Parallelism**
- [DO]:
  ```python
  from concurrent.futures import ProcessPoolExecutor
  
  def main():
      with ProcessPoolExecutor(max_workers=4) as pool:
          results = list(pool.map(heavy_computation, large_dataset))
  ```
- [DON'T]: Use `ThreadPoolExecutor` or raw `threading.Thread` for `heavy_computation`, as the GIL will force the threads to run serially on a single core.