@Domain
When the AI is asked to write, refactor, optimize, or debug Python code involving I/O operations (such as network requests, database queries, API clients, web scrapers, or file reads/writes), or workloads that mix heavy CPU computation with intermittent I/O tasks.

@Vocabulary
*   **I/O Bound**: A program state where execution speed is limited by the efficiency of input/output operations (e.g., waiting for a network or disk) rather than the CPU.
*   **I/O Wait**: The time a program spends in a paused state waiting for the kernel or external devices to complete an I/O request.
*   **Concurrency**: A paradigm where multiple tasks interleave their execution on a single thread, hiding I/O wait times by running other operations while waiting for resources.
*   **Parallelism**: A paradigm where multiple tasks run simultaneously on individual, independent compute resources (e.g., multiple processes/CPUs).
*   **Event Loop**: A mechanism that maintains a list of runnable functions/tasks and manages what gets executed and when, allowing tasks to pause and resume.
*   **Nonblocking**: An operation that returns immediately without halting the program, guaranteeing completion at a later time.
*   **Callbacks**: An older concurrency paradigm where functions take a target "callback" function to execute upon completion, often leading to difficult-to-trace "callback hell."
*   **Futures**: An object holding the promise of a future result, returned by modern asynchronous functions.
*   **Coroutine**: An asynchronous function defined with `async def` that acts similarly to a generator, allowing its execution to be paused (using `await`) and resumed.
*   **Task**: An execution unit created from a coroutine that the event loop schedules and manages.
*   **Pipelining / Batching**: Grouping I/O requests into small, asynchronous bursts to limit overhead and database/server overload while maintaining simpler CPU logic.
*   **Context Switch**: The heavy operation performed by the kernel to save a program's state and switch to another, which concurrent asynchronous programming minimizes.

@Objectives
*   Maximize resource utilization by hiding I/O wait times through single-thread concurrency rather than multi-processing.
*   Modernize asynchronous code by utilizing Python's native `async`/`await` syntax and Futures instead of callback-based paradigms.
*   Prevent I/O starvation by safely interleaving CPU-heavy workloads with I/O workloads using explicit event loop deferment.
*   Prevent downstream server and local event loop overload by carefully controlling and tuning the number of concurrent I/O requests.

@Guidelines
*   **Identify the Bottleneck**: When encountering a performance issue, the AI MUST determine if the problem is I/O-bound or CPU-bound. If the task involves waiting on networks, databases, or disks, the AI MUST apply asynchronous I/O concurrency rather than process-based parallelism.
*   **Use Async/Await**: When implementing concurrent execution, the AI MUST use Python's `async def` and `await` keywords to handle Futures, completely avoiding the callback paradigm.
*   **Task Management**: When spawning multiple asynchronous tasks, the AI MUST use `asyncio.TaskGroup()` (available in Python 3.11+) as a context manager to ensure all tasks are completed or safely canceled. Alternatively, the AI MAY use `asyncio.gather()` if the tasks are strictly independent and the failure of one should not cancel the others.
*   **Event Loop Initialization**: When bridging synchronous code to asynchronous code, the AI MUST use `asyncio.run(coro())` to create and manage the temporary event loop.
*   **Session Pooling**: When performing concurrent HTTP requests or database calls, the AI MUST instantiate and reuse a single session object (e.g., `aiohttp.ClientSession()`) via an `async with` context manager rather than creating a new session for each request.
*   **CPU Deferment in Async Code**: When integrating CPU-bound computations within an asynchronous event loop, the AI MUST insert `await asyncio.sleep(0)` inside the computational loops. This forces the function to defer execution back to the event loop (ideally every 50-100 milliseconds), allowing pending I/O tasks to process and preventing the event loop from stalling.
*   **Concurrency Limits**: When generating large volumes of asynchronous requests, the AI MUST recognize diminishing returns (typically beyond 100-250 concurrent requests) and MUST implement connection limiting or batching to avoid context-switching overhead and overloading downstream services.
*   **Batched Asynchronous Execution**: When a full asynchronous refactor is too complex for a mixed CPU/I/O workload, the AI MUST implement an `AsyncBatcher` approach. The AI MUST queue CPU results in memory and flush them to the I/O service concurrently in batches, accepting a minor penalty for the ease of maintaining synchronous CPU logic.

@Workflow
1.  **Analyze Latency**: Evaluate the program to confirm time is lost to I/O wait (e.g., `requests.get` or database inserts blocking execution).
2.  **Select Libraries**: Choose `asyncio` alongside an asynchronous equivalent of the required library (e.g., replace `requests` with `aiohttp` or `httpx`; replace synchronous DB drivers with async variants).
3.  **Setup Entry Point**: Create an asynchronous main function (`async def run_experiment()`) and invoke it from the synchronous block using `asyncio.run(run_experiment())`.
4.  **Initialize Shared State**: Open connection pools or client sessions using `async with` at the highest necessary scope to ensure connection caching and reuse.
5.  **Orchestrate Tasks**: Open an `asyncio.TaskGroup()` context manager. Iterate over the workload, create coroutines, and submit them using `tg.create_task(coro)`.
6.  **Yield Control for CPU Work**: If the coroutine includes a heavy CPU-bound loop before or after the I/O call, insert `await asyncio.sleep(0)` within the loop to yield control to the event loop.
7.  **Process Results**: Gather results from the task objects after the `TaskGroup` context manager exits (or as they complete, if post-processing is intensive).

@Examples (Do's and Don'ts)

[DO] Use `asyncio.TaskGroup` and reuse `aiohttp.ClientSession` for concurrent I/O requests.
```python
import asyncio
import aiohttp

async def process(session, url):
    async with session.get(url) as response:
        return len(await response.text())

async def run_experiment(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            for url in urls:
                task = tg.create_task(process(session, url))
                tasks.append(task)
    
    # TaskGroup guarantees all tasks are done here
    return sum(task.result() for task in tasks)

if __name__ == "__main__":
    result = asyncio.run(run_experiment(["http://example.com"] * 100))
```

[DON'T] Use a synchronous library in a loop, compounding the I/O wait penalty for every request.
```python
import requests

def run_experiment(urls):
    response_size = 0
    with requests.Session() as session:
        for url in urls: # I/O wait blocks the entire program here
            response = session.get(url)
            response_size += len(response.text)
    return response_size
```

[DO] Defer execution to the event loop in a mixed CPU/I/O async function using `asyncio.sleep(0)`.
```python
async def calculate_task_aiohttp(num_iter, task_difficulty, session, url):
    async with asyncio.TaskGroup() as tg:
        for i in range(num_iter):
            # Heavy CPU task
            result = do_cpu_heavy_task(i, task_difficulty)
            
            # Queue the I/O task
            task = tg.create_task(save_result_aiohttp(session, url, result))
            
            # Defer back to the event loop to allow I/O to process
            await asyncio.sleep(0)
```

[DON'T] Run long synchronous CPU loops inside an async function without yielding, causing I/O starvation.
```python
async def calculate_task_aiohttp(num_iter, task_difficulty, session, url):
    async with asyncio.TaskGroup() as tg:
        for i in range(num_iter):
            # Heavy CPU task blocks the event loop completely
            result = do_cpu_heavy_task(i, task_difficulty)
            task = tg.create_task(save_result_aiohttp(session, url, result))
            # Missing await asyncio.sleep(0) means no I/O tasks will execute until the loop finishes!
```

[DO] Implement an AsyncBatcher if you need to integrate async I/O into a largely synchronous CPU-bound pipeline.
```python
class AsyncBatcher:
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.batch = []

    def save(self, result):
        self.batch.append(result)
        if len(self.batch) == self.batch_size:
            self.flush()

    def flush(self):
        asyncio.run(self.__aflush())

    async def __aflush(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(result, session) for result in self.batch]
            await asyncio.gather(*tasks)
        self.batch.clear()
```