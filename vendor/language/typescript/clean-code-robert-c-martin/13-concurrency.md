@Domain
This rule file MUST trigger whenever the AI is tasked with writing, refactoring, debugging, or analyzing concurrent code, multithreaded applications, asynchronous processes, thread synchronization mechanisms, task scheduling, or system throughput optimizations.

@Vocabulary
- **Concurrency**: A decoupling strategy that separates *what* gets done from *when* it gets done, allowing multiple execution paths.
- **Thread**: An abstraction of a schedule representing a single execution path.
- **Critical Section**: Any section of code that must be protected from simultaneous use for the program to be correct.
- **Intrinsic Lock**: The built-in locking mechanism of a language (e.g., Java's `synchronized` keyword).
- **Producer-Consumer**: An execution model where producer threads create work and place it in a bound resource (queue), and consumer threads acquire and complete the work.
- **Readers-Writers**: An execution model dealing with a shared resource heavily read but occasionally updated, requiring a balance between throughput and preventing starvation.
- **Dining Philosophers**: An execution model representing enterprise processes competing for limited resources, requiring careful design to avoid deadlock and livelock.
- **Client-Based Locking**: A locking strategy where the client locks the server before calling the first method and unlocks after the last method.
- **Server-Based Locking**: A locking strategy where the server encapsulates the locking mechanism, calling the required methods and then unlocking, exposing a single thread-safe method to the client.
- **Adapted Server**: A locking strategy creating an intermediary adapter to perform locking when the original server code cannot be modified.
- **Spurious Failure**: A failure in concurrent code that is not easily repeatable, often incorrectly dismissed as a cosmic ray, hardware glitch, or "one-off".
- **Code Instrumentation**: The act of adding methods like `wait()`, `sleep()`, `yield()`, or `priority()` to code to force threads to run in different orderings and expose hidden flaws.
- **Pluggable Code**: Threaded code written so that it can be run in various configurations (e.g., single thread, multiple threads, varying test doubles).
- **Tunable Code**: Threaded code designed so that the number of threads and execution parameters can be easily adjusted, even dynamically.

@Objectives
- Decouple the *what* (application logic) from the *when* (execution schedule) to improve throughput and system structure.
- Prevent catastrophic concurrency failures such as deadlocks, livelocks, race conditions, and starvation.
- Isolate concurrency management completely from business logic to adhere to the Single Responsibility Principle (SRP).
- Minimize the scope of shared data and the size of critical sections to reduce lock contention and complexity.
- Ensure concurrent systems can shut down gracefully without leaving orphan threads or deadlocking.
- Maximize testability of concurrent code by writing it in a pluggable, tunable, and instrumentable manner.

@Guidelines

**1. Separation of Concerns (SRP for Concurrency)**
- The AI MUST separate concurrency-related code (thread management, scheduling, locking) from other production code (business logic).
- The AI MUST NOT embed concurrency implementation details directly into standard application POJOs.

**2. Data Encapsulation and Scope Limitation**
- The AI MUST severely limit the access of any data that may be shared across threads.
- The AI MUST deeply encapsulate shared data to minimize the number of critical sections.
- The AI MUST evaluate if shared data can be avoided entirely by using copies of data instead. If read-only copies can be used and merged later, the AI MUST prefer this over synchronization.

**3. Thread Independence**
- The AI MUST attempt to partition data into independent subsets that can be operated on by independent threads.
- The AI MUST design threads to operate as independently as possible, ideally relying entirely on unshared local variables.

**4. Concurrency Libraries and Safe Collections**
- The AI MUST use thread-safe collections provided by the language/library (e.g., `java.util.concurrent.ConcurrentHashMap`) instead of retrofitting non-thread-safe collections.
- The AI MUST use modern execution frameworks (e.g., Executor framework) rather than manually instantiating and managing bare threads.
- The AI MUST utilize nonblocking solutions (e.g., Atomic variables using Compare-And-Swap) where applicable to reduce the overhead of intrinsic locks.

**5. Execution Models and Algorithms**
- The AI MUST recognize which fundamental execution model applies to the current task (Producer-Consumer, Readers-Writers, Dining Philosophers) and implement the established pattern for that model.

**6. Dependencies Between Synchronized Methods**
- The AI MUST AVOID using more than one synchronized method on a shared object.
- IF multiple methods on a shared object must be invoked atomically, the AI MUST use Server-Based Locking (preferred) or an Adapted Server. Client-Based Locking MUST ONLY be used as a last resort.

**7. Critical Sections**
- The AI MUST keep synchronized sections as small as absolutely possible.
- The AI MUST NOT extend synchronization beyond the minimal critical section to avoid degrading performance and increasing contention.

**8. Graceful Shutdown**
- The AI MUST plan for and implement graceful shutdown code early in the development lifecycle.
- The AI MUST explicitly design against shutdown deadlocks (e.g., a parent thread waiting for a child thread that is infinitely blocked waiting for a terminated producer).

**9. Testing Threaded Code**
- The AI MUST NOT ignore system failures as "one-offs". All spurious failures MUST be treated as candidate threading issues.
- The AI MUST get nonthreaded code working and fully tested first before introducing thread awareness.
- The AI MUST make threaded code pluggable and tunable to allow testing under various configurations and loads.
- The AI MUST run tests with more threads than processors to encourage context switching and expose race conditions.
- The AI MUST instrument code (using `yield`, `sleep`, etc., manually or via automation tools) to jiggle execution order and force rare failures during testing.

@Workflow
When tasked with implementing or refactoring concurrent logic, the AI MUST strictly follow this algorithm:
1. **Extract Business Logic**: Write or refactor the core logic as thread-ignorant POJOs. Prove this code works using standard, single-threaded unit tests.
2. **Isolate Thread Management**: Create distinct classes responsible solely for the threading policy (e.g., Schedulers, Executors, Thread Factories).
3. **Minimize Shared State**: Review the architecture to eliminate shared data. Pass copies of data to threads whenever feasible. If data must be shared, encapsulate it entirely within a thread-safe server class.
4. **Implement Locking Strategy**: If shared state exists, implement the narrowest possible `synchronized` blocks or locks. Apply Server-Based Locking if multiple methods are involved.
5. **Implement Shutdown**: Write explicit, timeout-bound shutdown sequences for all threads and validate them immediately.
6. **Create Tunable Tests**: Write concurrent tests where the number of threads, iterations, and loads are variables that can be easily modified.
7. **Instrument for Edge Cases**: Introduce instrumentation (e.g., `Thread.yield()`) in test configurations to force varied execution interleaving. Execute tests assuming that intermittent failures are legitimate concurrency bugs.

@Examples (Do's and Don'ts)

**Principle: Single Responsibility in Concurrency**
- [DON'T] Mix thread instantiation and network/business logic in the same method.
```java
public void process(final Socket socket) {
    Runnable clientHandler = new Runnable() {
        public void run() {
            String message = MessageUtils.getMessage(socket);
            // Business logic mixed with raw thread creation
        }
    };
    Thread clientConnection = new Thread(clientHandler);
    clientConnection.start();
}
```
- [DO] Delegate thread management to a dedicated scheduler/executor class.
```java
public void run() {
    while (keepProcessing) {
        ClientConnection clientConnection = connectionManager.awaitClient();
        ClientRequestProcessor requestProcessor = new ClientRequestProcessor(clientConnection);
        clientScheduler.schedule(requestProcessor); // Threading policy isolated here
    }
}
```

**Principle: Server-Based Locking vs. Client-Based Locking**
- [DON'T] Force the client to manage the lock for multiple operations on a shared resource (Client-Based Locking).
```java
// Client code
synchronized (iterator) {
    if (iterator.hasNext()) {
        nextValue = iterator.next();
    }
}
```
- [DO] Encapsulate the locking logic within the server class so the client does not need to worry about synchronization (Server-Based Locking).
```java
// Server code
public synchronized Integer getNextOrNull() {
    if (nextValue < limit)
        return nextValue++;
    else
        return null;
}

// Client code
Integer nextValue = iterator.getNextOrNull();
```

**Principle: Keep Synchronized Sections Small**
- [DON'T] Synchronize an entire heavy method containing I/O and processing.
```java
public synchronized String getNextPageOrNull() {
    if (urls.hasNext()) {
        return reader.getPageFor(urls.next()); // I/O operation locks the object!
    }
    return null;
}
```
- [DO] Synchronize only the critical section manipulating the shared state.
```java
public String getNextPageOrNull() {
    String url;
    synchronized(this) {
        if (!urls.hasNext()) return null;
        url = urls.next(); // Only the state mutation is locked
    }
    return reader.getPageFor(url); // I/O happens outside the lock
}
```

**Principle: Code Instrumentation for Testing**
- [DON'T] Assume code is thread-safe just because standard unit tests pass sequentially.
- [DO] Inject yield/sleep points during testing to force varied execution pathways.
```java
public synchronized String nextUrlOrNull() {
    if(hasNext()) {
        ThreadJigglePoint.jiggle(); // Automatically configured to yield/sleep in tests
        String url = urlGenerator.next();
        ThreadJigglePoint.jiggle();
        updateHasNext();
        return url;
    }
    return null;
}
```