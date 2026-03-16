# @Domain
Python asynchronous programming utilizing `asyncio`, native coroutines (`async`/`await`), asynchronous iterables and iterators, asynchronous context managers, and high-performance network/I/O operations. These rules apply whenever the user requests asynchronous architectures, concurrent network clients/servers, or event-loop-based concurrency in Python.

# @Vocabulary
- **Native Coroutine**: A coroutine function defined with `async def`. Can delegate to other native coroutines using the `await` keyword.
- **Classic Coroutine**: A legacy generator function that consumes data via `.send()`. *Deprecated and no longer supported by `asyncio`.*
- **Generator-based Coroutine**: A legacy coroutine decorated with `@types.coroutine`.
- **Asynchronous Generator**: A function defined with `async def` that uses `yield` in its body. Returns an asynchronous generator object providing `__anext__`.
- **Awaitable**: An object that can be used in an `await` expression. Common awaitables include native coroutine objects, `asyncio.Task`, and objects with an `__await__` method returning an iterator.
- **Event Loop**: The core execution mechanism in `asyncio` that manages a queue of pending coroutines, drives them, monitors I/O events, and multiplexes execution in a single thread.
- **Task**: An `asyncio.Task` object that wraps a coroutine, scheduling it to run on the event loop and providing methods to query its state or cancel it.
- **Semaphore**: A synchronization primitive (e.g., `asyncio.Semaphore`) used to throttle concurrent operations (like limiting active network requests).
- **Asynchronous Context Manager**: An object implementing `__aenter__` and `__aexit__` as coroutines, used with the `async with` statement.
- **Asynchronous Iterable/Iterator**: An object implementing `__aiter__` (returning an async iterator) and `__anext__` (returning an awaitable), driven by `async for`.
- **Structured Concurrency**: A pattern where a group of asynchronous tasks is constrained to a single entry and exit point (e.g., Curio's `TaskGroup` or Trio's nurseries), ensuring all tasks complete or cancel cleanly before exiting the block.
- **ASGI (Asynchronous Server Gateway Interface)**: The successor to WSGI, designed for asynchronous Python web frameworks like FastAPI.

# @Objectives
- Ensure peak concurrency performance by strictly eliminating blocking I/O and CPU-bound operations from the event loop thread.
- Write modern, idiomatic Python using native coroutines (`async def` / `await`), completely avoiding legacy generator-based coroutine syntax.
- Manage concurrent resources and tasks safely using asynchronous context managers, semaphores, and proper task gathering/yielding.
- Accurately type-hint asynchronous objects, distinguishing between the return types of coroutine functions, `Coroutine` objects, and `AsyncGenerator` objects.

# @Guidelines

### Core Asynchronous Paradigms
- **Use Native Coroutines:** The AI MUST define all new coroutine functions using `async def` and drive them using `await`.
- **Legacy Coroutine Ban:** The AI MUST NOT use `@asyncio.coroutine` or `yield from` to manage coroutines. These are deprecated/removed.
- **Entry Point:** The AI MUST use `asyncio.run(main())` to initialize the event loop and drive the top-level coroutine, rather than manually instantiating or closing the event loop.
- **Never Block the Event Loop:** The AI MUST NOT use blocking functions (e.g., `time.sleep()`, `requests.get()`) inside an `async def` block. Use asynchronous equivalents (e.g., `await asyncio.sleep()`, `httpx.AsyncClient`).
- **File I/O Delegation:** File I/O is blocking. The AI MUST delegate file reading/writing to a separate thread. For Python 3.9+, the AI MUST use `await asyncio.to_thread(func, *args)`. For earlier versions, use `loop.run_in_executor(None, func, *args)`.
- **CPU-bound Delegation:** Any CPU-bound computation (e.g., heavy math, parsing massive JSONs) MUST be delegated to a `ProcessPoolExecutor` or an external task queue to prevent freezing the event loop.

### Concurrency Orchestration
- **Task Creation:** To schedule a coroutine to run concurrently without immediately waiting for its result, the AI MUST use `asyncio.create_task(coro())`.
- **Waiting for Multiple Tasks:** 
  - Use `await asyncio.gather(*coros)` when all results are needed simultaneously.
  - Use `asyncio.as_completed(coros)` in a `for` loop when processing results individually as soon as they finish.
- **Throttling/Rate Limiting:** Network clients MUST be throttled to prevent DoS-like behavior or resource exhaustion. The AI MUST instantiate an `asyncio.Semaphore(limit)` in the supervisor and use `async with semaphore:` around the specific I/O execution in the worker coroutine.

### Asynchronous Context Managers and Iterators
- **Async Context Managers:** The AI MUST use `async with` when managing asynchronous resources (database connections, HTTP clients like `httpx.AsyncClient`, semaphores).
- **Async Generators:** When building an asynchronous generator (`async def` containing a `yield`), the AI MUST drive it using `async for` or async comprehensions.
- **Custom Async Context Managers:** To create a custom async context manager without writing a full class, the AI MUST use the `@contextlib.asynccontextmanager` decorator on an asynchronous generator function containing a single `yield`.

### Asynchronous Comprehensions
- The AI MAY use async comprehensions (e.g., `[await func(x) for x in items]`) to concurrently evaluate awaitables inside a native coroutine.
- The AI MAY use async generator expressions (e.g., `(x async for x in async_iterable)`) anywhere in a module, but MUST only consume them inside an `async def` block.

### Asyncio Streams API Traps
- **Writing to Streams:** `StreamWriter.write()` and `StreamWriter.writelines()` are plain functions, NOT coroutines. The AI MUST NOT `await` them.
- **Draining Streams:** After writing to a stream, the AI MUST flush the buffer by awaiting the coroutine `StreamWriter.drain()` (`await writer.drain()`).
- **Reading Streams:** `StreamReader.readline()` and `.read()` ARE coroutines. The AI MUST `await` them.

### Type Hinting Asynchronous Objects
- **Native Coroutine Return Types:** When type-hinting a native coroutine function (`async def`), the return type MUST be the type of the value returned upon `await`, NOT a `Coroutine` object. (e.g., `async def get_data() -> int:`).
- **Coroutine Object Parameters:** If a function takes a coroutine object as an argument, the AI MUST annotate it using `collections.abc.Coroutine[YieldType, SendType, ReturnType]`. (Use `typing.Coroutine` for Python < 3.9).
- **Async Generator Annotation:** An asynchronous generator (`async def` with `yield`) MUST be annotated with `collections.abc.AsyncIterator[YieldType]` or `collections.abc.AsyncGenerator[YieldType, SendType]`. AsyncGenerators do not have a `ReturnType`.

# @Workflow
When tasked with writing or refactoring asynchronous code, follow this algorithmic process:
1. **Identify I/O vs. CPU:** Analyze the required tasks. Categorize them as asynchronous Network I/O, blocking File I/O, or blocking CPU-bound computations.
2. **Define Base Coroutines:** Write `async def` functions for Network I/O. Ensure underlying libraries support async (e.g., use `httpx.AsyncClient` instead of `requests`).
3. **Wrap Blocking Code:** For any File I/O or CPU-bound tasks, wrap the synchronous function calls using `asyncio.to_thread` or `run_in_executor`.
4. **Implement Throttling:** If fanning out multiple network requests, initialize an `asyncio.Semaphore` and wrap the specific HTTP request lines in `async with sem:`.
5. **Orchestrate:** Write a `supervisor` coroutine. Use `asyncio.create_task` or list comprehensions to build task lists. Await them using `asyncio.gather` or `asyncio.as_completed`.
6. **Execute:** Define a standard (non-async) `main()` function that calls `asyncio.run(supervisor())`.
7. **Type Hint:** Apply precise type hints. Annotate `async def` return values directly as the resolved type.

# @Examples (Do's and Don'ts)

### 1. Sleeping and Pausing Execution
- **[DO]** Use `asyncio.sleep()` to yield control to the event loop.
```python
async def slow_operation() -> int:
    await asyncio.sleep(3)
    return 42
```
- **[DON'T]** Use `time.sleep()`, as it halts the entire event loop thread.
```python
async def slow_operation() -> int:
    time.sleep(3) # Anti-pattern: Blocks the entire thread!
    return 42
```

### 2. Delegating Blocking I/O
- **[DO]** Delegate blocking file operations to a thread.
```python
import asyncio
from pathlib import Path

def save_data(data: bytes, path: Path) -> None:
    path.write_bytes(data)

async def download_and_save(client, url, path) -> None:
    resp = await client.get(url)
    # Safely offloads blocking file I/O to a background thread
    await asyncio.to_thread(save_data, resp.content, path)
```
- **[DON'T]** Perform File I/O directly in the coroutine.
```python
async def download_and_save(client, url, path) -> None:
    resp = await client.get(url)
    # Anti-pattern: This blocks the event loop!
    path.write_bytes(resp.content) 
```

### 3. Throttling Concurrent Tasks
- **[DO]** Use a Semaphore to limit active concurrent tasks.
```python
import asyncio
import httpx

async def fetch(client: httpx.AsyncClient, url: str, sem: asyncio.Semaphore) -> str:
    async with sem:
        resp = await client.get(url)
        return resp.text

async def supervisor(urls: list[str]) -> list[str]:
    sem = asyncio.Semaphore(10) # Max 10 concurrent requests
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, url, sem) for url in urls]
        return await asyncio.gather(*tasks)
```
- **[DON'T]** Blast the server with unbounded concurrent requests.
```python
async def supervisor(urls: list[str]) -> list[str]:
    async with httpx.AsyncClient() as client:
        # Anti-pattern: May launch 10,000 concurrent requests, causing DoS or crashing the local app
        tasks = [client.get(url) for url in urls]
        return await asyncio.gather(*tasks)
```

### 4. Working with the Streams API
- **[DO]** Write to the stream buffer and explicitly `await` the drain.
```python
async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    writer.write(b"Hello\r\n") # Plain function
    await writer.drain()       # Coroutine, MUST be awaited
```
- **[DON'T]** Await `write()` or forget to `drain()`.
```python
async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    await writer.write(b"Hello\r\n") # TypeError: object NoneType can't be used in 'await' expression
```

### 5. Type Hinting Coroutines
- **[DO]** Annotate the `async def` function with its resolved return type.
```python
async def get_user_id(username: str) -> int:
    await asyncio.sleep(0.1)
    return 101
```
- **[DON'T]** Annotate the `async def` function as returning a `Coroutine` (unless it's a factory returning an un-awaited coroutine object).
```python
from collections.abc import Coroutine

# Anti-pattern: Mypy will complain because the async keyword already implies the Coroutine wrapper.
async def get_user_id(username: str) -> Coroutine[Any, Any, int]:
    await asyncio.sleep(0.1)
    return 101
```

### 6. Processing Results as they Complete
- **[DO]** Use `asyncio.as_completed()` when you need to act on results dynamically.
```python
async def supervisor(urls: list[str]) -> None:
    async with httpx.AsyncClient() as client:
        coros = [client.get(url) for url in urls]
        for coro in asyncio.as_completed(coros):
            response = await coro
            print(f"Finished downloading: {response.url}")
```