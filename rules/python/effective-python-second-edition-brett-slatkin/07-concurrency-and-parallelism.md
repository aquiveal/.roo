# @Domain
Python programming tasks involving concurrent execution, parallel processing, asynchronous I/O, subprocess management, threading, thread pools, and multiprocessing architectures.

# @Vocabulary
- **Concurrency**: Doing many different things seemingly at the same time by interleaving execution. Provides no speedup for total work.
- **Parallelism**: Doing many different things actually at the same time using multiple CPU cores. Cuts total work time (provides speedup).
- **GIL (Global Interpreter Lock)**: A mutual-exclusion lock in CPython that prevents preemptive multithreading from corrupting interpreter state. Causes only one thread to make forward progress at a time.
- **Fan-out**: Spawning a concurrent line of execution for each unit of work.
- **Fan-in**: Waiting for all concurrent units of work to finish before moving on to the next phase.
- **Data Race**: Corruption of data structures caused by the interruption of a thread between bytecode instructions (e.g., during non-atomic `+=` operations).
- **Coroutine**: A function defined with `async def` that pauses at `await` expressions, allowing an event loop to rapidly interleave execution without thread overhead.
- **Top-down Migration**: Porting a codebase to `asyncio` by starting at the main entry points and using `run_in_executor` to execute legacy synchronous leaf functions.
- **Bottom-up Migration**: Porting a codebase to `asyncio` by starting at the leaf functions and using `run_until_complete` to execute them within legacy synchronous entry points.
- **High-leverage Task**: A computational task where a small amount of data transferred enables a massive amount of computation, suitable for process pools.

# @Objectives
- Choose the correct architectural paradigm (threads vs. coroutines vs. process pools) based strictly on the workload characteristics (I/O-bound vs. CPU-bound, low-scale vs. high-scale).
- Prevent silent data corruption by aggressively utilizing synchronization primitives.
- Eliminate thread-based memory explosion and scheduling overhead using executors and coroutines.
- Maximize responsiveness of asynchronous applications by strictly preventing blocking system calls within the event loop.
- Guarantee robust exception handling and propagation in all concurrent fan-out/fan-in models.

# @Guidelines
- **Managing Child Processes**
  - When gluing together command-line utilities, the AI MUST use the `subprocess` module.
  - The AI MUST use `subprocess.run` for simple process execution and `subprocess.Popen` for advanced usage (UNIX-style pipelines, asynchronous polling).
  - When waiting for a subprocess, the AI MUST use the `timeout` parameter in the `communicate(timeout=...)` method to avoid deadlocks and hanging processes.

- **Using Threads**
  - When encountering CPU-bound tasks, the AI MUST NOT use threads for parallelism due to the GIL.
  - When encountering blocking I/O operations (network, file reading) in legacy or synchronous code, the AI MAY use threads to maintain program responsiveness.

- **Preventing Data Races**
  - When multiple threads modify the same object, the AI MUST NOT rely on the GIL for safety.
  - The AI MUST use `threading.Lock` within a `with` statement to protect shared state and enforce data structure invariants.

- **Threaded Pipelines and Queues**
  - When constructing concurrent pipelines, the AI MUST NOT use standard Python `list` types.
  - The AI MUST use `queue.Queue` to coordinate work between threads.
  - The AI MUST specify a buffer size (e.g., `Queue(maxsize=1)`) to prevent memory explosion from pipeline backups.
  - The AI MUST utilize `get()`, `put()`, `task_done()`, and `join()` for blocking operations and tracking progress.
  - The AI MUST implement special sentinel values (e.g., `object()`) to gracefully signal worker threads to terminate.

- **Fan-out / Fan-in Architecture**
  - When executing on-demand fan-out, the AI MUST NOT spawn a new `Thread` instance per unit of work (to prevent memory exhaustion and swallowed exceptions).
  - When threaded I/O concurrency is necessary without a full `asyncio` refactor, the AI MUST use `concurrent.futures.ThreadPoolExecutor`.
  - The AI MUST call `.result()` on the `Future` returned by `pool.submit()` during the fan-in phase to guarantee exception propagation.

- **Asynchronous Coroutines (`asyncio`)**
  - When achieving highly concurrent I/O (e.g., thousands of simultaneous network requests), the AI MUST use `async def`, `await`, and the `asyncio` module.
  - The AI MUST use `asyncio.gather(*tasks)` to execute and fan-in concurrent coroutines.
  - When transitioning code to `asyncio`, the AI MUST substitute blocking logic with asynchronous built-in equivalents (e.g., `asynccontextmanager`, `async for`).

- **Mixing Threads and Coroutines**
  - When performing a top-down `asyncio` migration, the AI MUST use `loop.run_in_executor()` to run blocking synchronous functions in a thread pool.
  - When performing a bottom-up `asyncio` migration, the AI MUST use `loop.run_until_complete()` to run async leaf functions in synchronous contexts.
  - When a synchronous worker thread needs to trigger a coroutine in the main event loop, the AI MUST use `asyncio.run_coroutine_threadsafe`.

- **Event Loop Responsiveness**
  - The AI MUST NOT execute blocking system calls (e.g., `open()`, `file.write()`, `time.sleep()`) directly within an `async def` function running on the main event loop.
  - The AI MUST encapsulate blocking I/O inside a dedicated `Thread` or a `ThreadPoolExecutor` when called from asynchronous code.
  - When debugging `asyncio` latency, the AI MUST utilize `asyncio.run(main(), debug=True)`.

- **CPU-bound True Parallelism**
  - When true parallelism for CPU-bound computation is required, the AI MUST use `concurrent.futures.ProcessPoolExecutor`.
  - The AI MUST ensure that tasks dispatched to `ProcessPoolExecutor` are isolated and high-leverage to justify the serialization (pickling) overhead.
  - The AI MUST NOT use the low-level `multiprocessing` module (shared memory, cross-process locks) unless `ProcessPoolExecutor` has been completely exhausted.

# @Workflow
When tasked with writing or refactoring concurrent/parallel code, the AI must follow this algorithmic decision process:
1. **Classify the Workload**: Determine if the task is CLI-glue, CPU-bound, or I/O-bound.
2. **Handle CLI Glue**: If managing external programs, implement `subprocess.run` or `subprocess.Popen` with timeouts.
3. **Handle CPU-bound**: If CPU-bound, wrap the isolated calculation in a standalone function and execute via `concurrent.futures.ProcessPoolExecutor`.
4. **Handle I/O-bound**:
    a. If building a new system or modifying a highly concurrent system, implement `asyncio` coroutines.
    b. If refactoring legacy synchronous code where `asyncio` is too disruptive, implement `concurrent.futures.ThreadPoolExecutor`.
5. **Enforce Synchronization**: Identify any shared mutable state across threads and immediately wrap modifications in a `with lock:` block using `threading.Lock()`.
6. **Audit Event Loops**: If using `asyncio`, scan all coroutines for hidden blocking system calls (e.g., standard file I/O). Move any discovered blocking calls into a `run_in_executor` wrapper.
7. **Ensure Exception Propagation**: Audit all fan-in points (`gather()`, `future.result()`, `task_done()`) to verify that exceptions occurring in children will correctly bubble up to the main thread.

# @Examples (Do's and Don'ts)

### Subprocesses
- **[DO]**
  ```python
  import subprocess
  proc = subprocess.Popen(['sleep', '10'])
  try:
      proc.communicate(timeout=0.1)
  except subprocess.TimeoutExpired:
      proc.terminate()
      proc.wait()
  ```
- **[DON'T]** Call communicate without a timeout, risking a permanent hang if the child process stalls.
  ```python
  import subprocess
  proc = subprocess.Popen(['sleep', '10'])
  proc.communicate() # Blocks indefinitely if process hangs
  ```

### Data Races and Locks
- **[DO]**
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
- **[DON'T]** Assume `+=` is atomic due to the GIL.
  ```python
  class Counter:
      def __init__(self):
          self.count = 0
      def increment(self, offset):
          self.count += offset # Data race waiting to happen!
  ```

### I/O Concurrency with Thread Pools
- **[DO]**
  ```python
  from concurrent.futures import ThreadPoolExecutor
  def simulate_pool(pool, grid):
      futures = []
      for y in range(grid.height):
          for x in range(grid.width):
              future = pool.submit(step_cell, y, x, grid.get)
              futures.append(future)
      for future in futures:
          future.result() # Propagates exceptions!
  ```
- **[DON'T]** Spawn raw threads dynamically in a loop without bounds.
  ```python
  from threading import Thread
  threads = []
  for y in range(grid.height): # Will blow up memory if grid is 10,000!
      thread = Thread(target=step_cell, args=(y, x, grid.get))
      thread.start()
      threads.append(thread)
  ```

### Avoid Blocking the Asyncio Event Loop
- **[DO]**
  ```python
  import asyncio
  async def tail_async(handle, interval, write_func):
      loop = asyncio.get_event_loop()
      while not handle.closed:
          # Run blocking file read in an executor
          line = await loop.run_in_executor(None, handle.readline)
          if line:
              await write_func(line)
  ```
- **[DON'T]** Perform standard blocking I/O inside a coroutine.
  ```python
  import asyncio
  async def tail_async(handle):
      while not handle.closed:
          line = handle.readline() # BLOCKS THE ENTIRE EVENT LOOP!
          if line:
              pass
  ```

### CPU-Bound Parallelism
- **[DO]**
  ```python
  from concurrent.futures import ProcessPoolExecutor
  def main():
      with ProcessPoolExecutor(max_workers=4) as pool:
          results = list(pool.map(heavy_computation, large_dataset))
  ```
- **[DON'T]** Use `ThreadPoolExecutor` for CPU-heavy tasks.
  ```python
  from concurrent.futures import ThreadPoolExecutor
  def main():
      # Yields NO speedup due to the GIL
      with ThreadPoolExecutor(max_workers=4) as pool:
          results = list(pool.map(heavy_computation, large_dataset))
  ```