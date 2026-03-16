# @Domain
Trigger these rules when architecting or implementing event-driven systems in Python, decoupling components into producers and consumers, working with publish/subscribe (pub/sub) message brokers, implementing the Observer pattern, or building reactive data pipelines/streams.

# @Vocabulary
*   **Event-Driven Architecture**: An architectural style revolving around reactions to stimuli, where producers send notifications (events) and consumers act upon them without direct knowledge of one another.
*   **Producer**: A component that acts as a stimulus, emitting an event or data when a specific condition is met or action completes.
*   **Consumer**: A component that reacts to a stimulus, receiving events from producers to execute subsequent logic.
*   **Transport Mechanism**: The intermediary layer (e.g., a message broker or list of callbacks) that passes data back and forth between decoupled producers and consumers.
*   **Message Broker**: A specific piece of code or infrastructure that routes messages from producers to consumers using a publish/subscribe model based on topics.
*   **Pub/Sub**: Publisher/Subscriber. A messaging pattern where producers publish messages to specific topics, and consumers subscribe to those topics to receive the messages.
*   **Topic**: A unique identifier (usually a string namespace) used by a message broker to distinguish one message channel from another.
*   **Observer Pattern**: A design pattern where a producer maintains a generic list of observers (consumers) and notifies them directly.
*   **Reactive Programming**: An architectural style revolving around continuous streams of events (observables), manipulated via chained operators.
*   **Observable**: A data source representing a continuous stream of events in reactive programming.
*   **Pipable Operators**: Functions in reactive programming (like map, filter, average) chained together to transform and process an observable data stream.

# @Objectives
*   Decouple system components to maximize extensibility, allowing new producers and consumers to be added without modifying existing code.
*   Select the appropriate event abstraction (Message Broker, Observer Pattern, or Reactive Programming) based on the event frequency and system boundaries.
*   Mitigate the inherent risks of event-driven architectures, specifically logical dependency breakages, typechecker blindspots, and cascading errors.
*   Prioritize lightweight, Pythonic event implementations (e.g., using `Callable`) over heavy, traditional object-oriented boilerplates (e.g., abstract Publisher/Subscriber base classes).

# @Guidelines
*   **Architectural Decoupling**: Isolate producers and consumers. Producers must not know which components are consuming their events, and consumers must not know which components produced the events. Both must depend only on the transport mechanism.
*   **Drawback Mitigation - Logical Dependencies**: Recognize that decoupled event systems rely on shared message formats. Because typecheckers cannot validate data passing through a dynamic message broker, you MUST explicitly document and validate message payloads at the consumer level.
*   **Drawback Mitigation - Error Handling**: Establish a clear strategy for consumer exceptions. Wrap consumer/subscriber logic in `try...except` blocks if a failure in one consumer should not crash the producer or block other consumers.
*   **Drawback Mitigation - Debugging**: When debugging message brokers or reactive streams, do not step into the library internals. Place breakpoints inside the specific callback functions or operator lambda functions.
*   **Message Brokers (`pypubsub`)**: Use `pypubsub` for single-process pub/sub architectures. Use external systems (Kafka, Redis, RabbitMQ) when events must cross process or machine boundaries.
*   **Message Broker Constraint**: `pypubsub` subscribers operate in the exact same thread as the publisher. You MUST NOT perform blocking I/O (e.g., waiting on a socket, synchronous HTTP requests) inside a subscriber, as it will block the publisher and all other subscribers.
*   **Observer Pattern**: Use the Observer pattern when typechecking and simple debugging are prioritized over complete physical decoupling. 
*   **Observer Pattern Constraint**: Implement observers as generic lists of `Callable` objects. DO NOT use boilerplate-heavy Object-Oriented base classes (`Publisher` and `Subscriber` interfaces) unless strictly necessary for complex state management.
*   **Observer Pattern Call-Stack Pollution**: Avoid the Observer pattern if you must pass the list of observers down through many unrelated layers of the call stack to reach the producer. Use a message broker instead.
*   **Reactive Programming (`RxPY`)**: Use reactive programming for systems dominated by continuous streams of data, data pipelines, ETL systems, or continuous I/O reactions.
*   **Reactive Pipelines**: Construct reactive workflows using `observable.pipe()` to chain pure, immutable functions and `rx.operators`.

# @Workflow
1.  **Analyze Event Frequency & Boundaries**: Determine if the system requires "Simple Events" (discrete, infrequent occurrences) or "Streaming Events" (continuous flows of data).
2.  **Select the Transport Mechanism**:
    *   If handling Streaming Events, adopt Reactive Programming (`RxPY`).
    *   If handling Simple Events within a single process, and type-safety/debugging is paramount, use the Observer Pattern.
    *   If handling Simple Events, but the Observer Pattern would cause deep call-stack pollution, use a Message Broker (`pypubsub`).
    *   If handling Simple Events across multiple processes or machines, use a distributed Message Broker (Redis, Kafka).
3.  **Implement the Observer Pattern** (If selected):
    *   Define the producer function signature to accept a parameter `observers: list[Callable[[PayloadType], None]]`.
    *   Perform the primary business logic.
    *   Iterate over the `observers` list and invoke each `Callable` with the event payload.
4.  **Implement a Message Broker** (If selected, e.g., `pypubsub`):
    *   Define string-based topics.
    *   In the consumer module, import `pub` and register the callback: `pub.subscribe(consumer_function, "topic_name")`.
    *   In the producer module, import `pub` and emit the event: `pub.publish("topic_name", payload=data)`.
5.  **Implement Reactive Streams** (If selected, e.g., `RxPY`):
    *   Define the data source using `rx.of(...)` or other observable creators.
    *   Build a pipeline using the `.pipe()` method on the observable.
    *   Chain `rx.operators` (e.g., `filter`, `map`, `max`) inside the pipe, passing small, pure lambda functions or modular functions to each operator.
    *   Attach the final consumer using `.subscribe(consumer_function)`.

# @Examples (Do's and Don'ts)

**Principle: Implementing the Observer Pattern**
*   **[DO]** Use lightweight Pythonic type hints (`Callable`) to inject observers dynamically.
```python
from typing import Callable

def complete_order(order: Order, observers: list[Callable[[Order], None]]):
    package_order(order)
    for observer_func in observers:
        try:
            observer_func(order)
        except Exception as e:
            log_error(f"Observer failed: {e}")
```
*   **[DON'T]** Use heavy, traditional OOP base classes just to implement the observer pattern, as it introduces unnecessary boilerplate and tight coupling.
```python
# Anti-pattern: Unnecessary Java-style OOP interfaces in Python
class Subscriber:
    def notify(self, data: Any):
        raise NotImplementedError()

class Publisher:
    def __init__(self):
        self.subscribers = []
    def add_subscriber(self, sub: Subscriber):
        self.subscribers.append(sub)
```

**Principle: Message Broker (`pypubsub`) Execution**
*   **[DO]** Keep subscriber logic fast and non-blocking when using single-process message brokers.
```python
from pubsub import pub

def schedule_pick_up_for_meal(order: Order):
    # Fast, non-blocking state update or async task scheduling
    delivery_queue.put_nowait(order)

pub.subscribe(schedule_pick_up_for_meal, "meal-done")
```
*   **[DON'T]** Execute blocking I/O directly inside the subscriber, freezing the publisher thread.
```python
from pubsub import pub
import requests

def notify_external_service(order: Order):
    # Anti-pattern: Blocking I/O inside a pypubsub subscriber
    # This blocks the producer and all other subscribers!
    requests.post("https://slow-external-api.com/notify", json=order.to_dict())

pub.subscribe(notify_external_service, "meal-done")
```

**Principle: Reactive Programming (`RxPY`)**
*   **[DO]** Use `observable.pipe()` to compose clean, modular transformation steps.
```python
import rx
import rx.operators as ops

get_max_altitude = observable.pipe(
    ops.skip_while(is_close_to_restaurant),
    ops.filter(lambda data: isinstance(data, LocationData)),
    ops.map(lambda loc: loc.z),
    ops.max()
)

get_max_altitude.subscribe(save_max_altitude)
```
*   **[DON'T]** Write manual `while` or `for` loops with deep nested conditional logic to process continuous streams of varying event types.
```python
# Anti-pattern: Manual stream processing instead of reactive pipelines
max_altitude = 0
for data in continuous_data_stream:
    if not is_close_to_restaurant(data):
        if isinstance(data, LocationData):
            if data.z > max_altitude:
                max_altitude = data.z
save_max_altitude(max_altitude)
```