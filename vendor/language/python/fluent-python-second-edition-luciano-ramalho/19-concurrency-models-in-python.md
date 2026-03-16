# @Domain

These rules MUST be triggered when the user requests assistance with Python code involving concurrent execution, parallel processing, asynchronous programming (`asyncio`), multithreading (`threading`), multiprocessing (`multiprocessing`), optimizing performance bottlenecks (I/O-bound vs. CPU-bound tasks), or architecting web servers/background task queues. 

# @Vocabulary

The AI MUST adopt and strictly adhere to the following precise terminology to ensure alignment with the author's mental model:

- **Concurrency**: The ability to handle multiple pending tasks, making progress one at a time or in parallel, so that each eventually succeeds or fails (structuring a solution).
- **Parallelism**: The ability to execute multiple computations at the exact same time (requires multicore CPU, GPU, or clusters).
- **Execution Unit**: A general term for objects that execute code concurrently (Processes, Threads, and Coroutines).
- **Process**: An execution unit with isolated private memory space, communicating via pipes/sockets (requires serialization). Enables preemptive multitasking.
- **Thread**: An execution unit within a single process sharing the same memory space. Enables preemptive multitasking under the OS scheduler but is limited by the GIL in CPython.
- **Coroutine**: A function that can suspend itself and resume later, run by an event loop. Enables cooperative multitasking.
- **Queue**: A data structure (usually FIFO) used for exchanging application data and control messages between execution units safely.
- **Lock / Mutex**: An object used to synchronize actions and avoid corrupting shared data.
- **Contention**: Dispute over a limited asset, such as a lock, storage, or CPU time.
- **GIL (Global Interpreter Lock)**: A CPython lock preventing multiple Python threads from executing Python bytecodes at once.
- **Poison Pill / Sentinel**: A specific marker value (e.g., `None`, `0`, or `Ellipsis`) placed in a queue to signal a worker to terminate gracefully.

# @Objectives

- Accurately diagnose whether a requested workload is I/O-bound or CPU-bound to select the appropriate execution unit.
- Prevent catastrophic blocking in cooperative multitasking environments (e.g., `asyncio`).
- Ensure safe, predictable communication and termination of execution units using Queues, Events, and Sentinels.
- Guide architectural decisions away from "web-scale envy" and towards standard, proven multicore deployment strategies (WSGI/ASGI servers and distributed task queues).

# @Guidelines

### 1. Model Selection (I/O-Bound vs CPU-Bound)
- The AI MUST use `threading` or `asyncio` EXCLUSIVELY for I/O-bound tasks (network requests, disk reading/writing).
- The AI MUST use `multiprocessing` or C/Cython extensions for CPU-bound, compute-intensive tasks (e.g., mathematical computations, data transformations) to bypass the GIL.
- The AI MUST explicitly remind the user that Python threads are "great at doing nothing" (waiting for I/O) but suffer from severe performance degradation under CPU contention due to the GIL.

### 2. Asyncio Safety and Best Practices
- The AI MUST NEVER use blocking calls like `time.sleep()` inside an `async def` coroutine. It MUST use `await asyncio.sleep()` to yield control back to the event loop.
- If a CPU-bound function *must* temporarily reside within a coroutine, the AI MUST inject `await asyncio.sleep(0)` inside long-running loops (e.g., every 50,000 iterations) to "power nap" and allow the event loop to drive other pending coroutines.
- The AI MUST differentiate between starting a coroutine (`asyncio.create_task()`, which schedules it and returns a `Task`) and yielding to a coroutine (`await`, which pauses the current coroutine until the awaited one finishes).

### 3. Thread and Process Coordination
- The AI MUST use `threading.Event` or `multiprocessing.Event` to send boolean state signals (like shutdown commands) between execution units.
- For type-hinting `multiprocessing.Event`, the AI MUST import and use `multiprocessing.synchronize.Event`, because `multiprocessing.Event` is a factory function, not a class.
- The AI MUST use `queue` structures (e.g., `multiprocessing.SimpleQueue`) for passing data between workers.
- When terminating indefinite loops in worker processes/threads, the AI MUST implement the "Poison Pill" pattern by sending a designated sentinel value into the queue.
- For cross-process sentinels, the AI MUST NOT use `object()` because its identity is lost during serialization/pickling. The AI MUST recommend using `None`, an integer like `0`, or the `Ellipsis` (`...`) built-in object.

### 4. Application Architecture & Scalability
- When advising on web application architecture, the AI MUST recommend deploying standard synchronous code (Django, Flask) via WSGI application servers (e.g., Gunicorn, uWSGI, mod_wsgi) that fork multiple processes to utilize multicore CPUs.
- For tasks that slow down HTTP responses (e.g., sending emails, generating PDFs), the AI MUST recommend decoupling via Distributed Task Queues (e.g., Celery, RQ) backed by message brokers (e.g., RabbitMQ, Redis).

# @Workflow

When presented with a concurrency problem or asked to parallelize a Python task, the AI MUST execute the following algorithmic process:

1. **Analyze Boundness**: Determine if the primary bottleneck is I/O (network/disk) or CPU (computation).
2. **Select the Execution Unit**:
   - If I/O-bound and the codebase is highly concurrent/modern: Propose `asyncio`.
   - If I/O-bound and integrating with legacy/synchronous code: Propose `threading`.
   - If CPU-bound: Propose `multiprocessing`.
3. **Structure Communication**: Define how inputs will reach the workers and how outputs will be collected. Default to `SimpleQueue` for processes or `asyncio.Queue` for coroutines.
4. **Define Lifecycle & Termination**: Explicitly implement a shutdown mechanism. Use `.cancel()` for `asyncio.Task`, `Event.set()` for threads, or a Poison Pill for queue-consuming processes.
5. **Review against GIL**: Verify that no CPU-bound code is accidentally trapped inside a thread or coroutine without a delegation mechanism (like `run_in_executor` or `ProcessPoolExecutor`).

# @Examples (Do's and Don'ts)

### Asyncio Sleeping and Blocking
- **[DON'T]** Block the event loop with synchronous sleeps or blocking I/O:
  ```python
  async def slow_operation():
      time.sleep(3) # WRONG: Blocks the entire event loop
      return 42
  ```
- **[DO]** Use asynchronous equivalents to yield control:
  ```python
  async def slow_operation():
      await asyncio.sleep(3) # CORRECT: Yields control to the event loop
      return 42
  ```

### Terminating Queue Workers safely
- **[DON'T]** Force-terminate processes or leave them hanging indefinitely:
  ```python
  def worker(jobs, results):
      while True:
          n = jobs.get()
          results.put(compute(n))
          # WRONG: No exit condition, hangs forever waiting for jobs
  ```
- **[DO]** Use a poison pill (sentinel) to exit the loop cleanly:
  ```python
  def worker(jobs, results):
      while True:
          n = jobs.get()
          if n is Ellipsis: # CORRECT: Sentinel detected, break loop
              results.put((Ellipsis, None)) # Acknowledge completion
              break
          results.put((n, compute(n)))
  ```

### Handling CPU-Bound Code in Asyncio
- **[DON'T]** Run heavy loops directly in an async function without yielding:
  ```python
  async def calculate_prime(n):
      for i in range(3, int(math.sqrt(n)) + 1, 2):
          if n % i == 0:
              return False
      return True # WRONG: CPU-bound loop starves other coroutines
  ```
- **[DO]** Delegate to an executor, or use "power napping" as a stopgap:
  ```python
  async def calculate_prime(n):
      for i in range(3, int(math.sqrt(n)) + 1, 2):
          if n % i == 0:
              return False
          if i % 100_000 == 1:
              await asyncio.sleep(0) # CORRECT (Stopgap): Power nap yields control
      return True
  ```

### Type Hinting Multiprocessing Events
- **[DON'T]** Type hint with the factory function:
  ```python
  from multiprocessing import Event
  def spin(msg: str, done: Event) -> None: # WRONG: Event is a function, not a type
      pass
  ```
- **[DO]** Type hint using the `synchronize` module:
  ```python
  from multiprocessing import synchronize
  def spin(msg: str, done: synchronize.Event) -> None: # CORRECT: Uses the actual class
      pass
  ```