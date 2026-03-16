# @Domain
Python application development involving scalability, concurrency, parallelism, network communication, asynchronous I/O, and architectural design for high-performance systems.

# @Vocabulary
- **GIL (Global Interpreter Lock):** A lock in CPython that allows only one thread to execute Python bytecode at a time, inherently limiting multithreading for CPU-bound tasks.
- **Multithreading:** Running multiple threads concurrently within a single Python process. Best suited for I/O-oriented tasks or background GUI operations.
- **Multiprocessing:** Using the `multiprocessing` package to fork new processes (via `os.fork()`), bypassing the GIL to achieve true parallelism for CPU-bound workloads.
- **Event-Driven Architecture:** A programming paradigm that dictates program flow using an event loop, reacting to events (e.g., data ready to read/write) rather than relying on sequential blocking operations.
- **C10K Problem:** The challenge of optimizing network sockets to handle ten thousand (or more) concurrent connections simultaneously.
- **asyncio:** The modern Python standard (PEP 3156) for asynchronous I/O, utilizing `async`, `await`, and event loops instead of callback-based frameworks.
- **Coroutine:** A function defined with `async def` that can yield control to the event loop using `await`, allowing other operations to run concurrently.
- **Service-Oriented Architecture (SOA):** A software design style where decoupled components provide services via communication protocols (HTTP REST, RPC, AMQP).
- **RPC (Remote Procedure Call):** A mechanism for interprocess communication where a program causes a procedure to execute in another address space.
- **ZeroMQ (zmq):** A high-performance asynchronous messaging library used for building scalable interprocess communication (IPC) and distributed networks.
- **AMQP (Advanced Message Queuing Protocol):** A messaging protocol used for remote procedure calls and message brokering (e.g., via Kombu, RabbitMQ).

# @Objectives
- Maximize CPU utilization by correctly identifying CPU-bound workloads and distributing them across multiple processes.
- Handle high-concurrency I/O operations efficiently without incurring the memory and context-switching overhead of operating system threads.
- Decouple application components to facilitate horizontal scaling across multiple nodes and processes.
- Eliminate race conditions and locking complexity by preferring event-driven architectures and message-passing over shared-state multithreading.

# @Guidelines
- **Workload Profiling:** The AI MUST explicitly categorize the user's workload as either CPU-intensive (algorithmic computations, data processing) or I/O-intensive (network requests, database queries, file reading) before writing concurrency code.
- **Handling CPU-bound Tasks:** The AI MUST NOT use the `threading` module for CPU-intensive operations. The AI MUST use the `multiprocessing` module (e.g., `multiprocessing.Pool`) to bypass the GIL and utilize multiple CPU cores.
- **Handling I/O-bound Tasks:** The AI MUST restrict the use of `threading` strictly to high-latency I/O operations or background tasks (like GUI event waiting). For modern network/I/O concurrency, the AI MUST prefer `asyncio` and event loops over multithreading.
- **Event-Driven Implementation:** When building highly concurrent network applications (solving the C10K problem), the AI MUST use `asyncio` with `async` and `await` syntax. If operating at a lower level, the AI MUST use the `select` module (`select.select()`) and set sockets to non-blocking mode (`setblocking(0)`).
- **Avoiding Thread-per-Connection:** The AI MUST NOT implement a architecture that spawns a new OS thread or process for every incoming network connection.
- **Interprocess Communication (IPC):** When designing distributed systems or worker pools, the AI MUST use a messaging bus or socket library like `ZeroMQ` (using PUSH/PULL or REQ/REP patterns) or an AMQP library (like `Kombu`) to decouple the architecture.
- **Stateless Services:** When exposing APIs to the outside world, the AI MUST favor stateless REST-style HTTP architectures to ensure easy replication and scaling.
- **Alternative Runtimes:** The AI MUST assume CPython as the target runtime. Do NOT recommend switching to Jython solely to bypass the GIL, as alternative runtimes lag behind CPython features.

# @Workflow
1. **Determine the Bottleneck:** Analyze if the target operation is limited by the CPU (processing data) or by I/O (waiting for network/disk).
2. **Select the Concurrency Model:**
   - If CPU-bound: Import `multiprocessing`.
   - If I/O-bound and making network requests: Import `asyncio` (and related libraries like `aiohttp`).
   - If requiring low-level socket control: Import `select` and configure non-blocking sockets.
3. **Implement the Execution Block:**
   - For `multiprocessing`: Instantiate a `Pool(processes=X)` and use `pool.map()` to distribute the workload.
   - For `asyncio`: Define `async def` coroutines, use `await` for blocking calls, and orchestrate them using `asyncio.get_event_loop().run_until_complete(asyncio.gather(*coroutines))`.
4. **Architect for Horizontal Scaling:** If the system must scale beyond a single machine, introduce `zmq` sockets to create a message bus (e.g., a PUSH socket for task distribution and a PULL socket for result collection), wrapping the worker logic in decoupled processes.

# @Examples (Do's and Don'ts)

### 1. Scaling CPU-Intensive Workloads
- **[DO]** Use `multiprocessing` to bypass the GIL and achieve true parallel execution.
```python
import multiprocessing
import random

def compute(n):
    return sum([random.randint(1, 100) for i in range(1000000)])

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=8)
    results = pool.map(compute, range(8))
    print(f"Results: {results}")
```
- **[DON'T]** Use multithreading for CPU-heavy tasks, as the GIL will limit the program to ~1 CPU core of utilization.
```python
import threading
import random

results = []
def compute():
    results.append(sum([random.randint(1, 100) for i in range(1000000)]))

# This will struggle to exceed >100% CPU usage on a multi-core machine due to the GIL.
workers = [threading.Thread(target=compute) for x in range(8)]
for worker in workers:
    worker.start()
```

### 2. High-Concurrency Network Requests
- **[DO]** Use `asyncio` and `aiohttp` to perform concurrent I/O operations without the overhead of threads.
```python
import aiohttp
import asyncio

async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response

loop = asyncio.get_event_loop()
coroutines = [get("http://example.com") for _ in range(8)]
results = loop.run_until_complete(asyncio.gather(*coroutines))
print(f"Results: {results}")
```
- **[DON'T]** Create a new thread for every outgoing network request, which is memory-heavy and scales poorly.

### 3. Decoupling Processes with ZeroMQ (Service-Oriented Architecture)
- **[DO]** Use ZeroMQ sockets (PUSH/PULL) to distribute work to independent worker processes.
```python
import multiprocessing
import zmq

def worker():
    context = zmq.Context()
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://127.0.0.1:5555")
    
    result_sender = context.socket(zmq.PUSH)
    result_sender.connect("tcp://127.0.0.1:5556")
    
    while True:
        task = work_receiver.recv_pyobj()
        # Execute task...
        result_sender.send_pyobj(task())

if __name__ == '__main__':
    context = zmq.Context()
    work_sender = context.socket(zmq.PUSH)
    work_sender.bind("tcp://127.0.0.1:5555")
    
    # Start workers
    for _ in range(8):
        multiprocessing.Process(target=worker).start()
```
- **[DON'T]** Rely strictly on tightly coupled, monolithic architectures with complex threading locks and shared memory variables to pass data between components.

### 4. Low-Level Event-Driven Socket Handling
- **[DO]** Use `select.select()` and non-blocking sockets for custom event loops.
```python
import select
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0) # Never block on read/write
server.bind(('localhost', 10000))
server.listen(8)

while True:
    inputs, outputs, excepts = select.select([server], [], [server])
    if server in inputs:
        connection, client_address = server.accept()
        connection.send(b"hello!\n")
```
- **[DON'T]** Leave sockets in blocking mode (`setblocking(1)`) while iterating over them, as one slow client will freeze the entire server.