# @Domain
This rule file is activated whenever the AI is tasked with designing, refactoring, or extending an Event-Driven Architecture (EDA) or Command-Query Responsibility Segregation (CQRS) system, specifically focusing on message buses, message dispatching, event handling, command handling, and systemic error recovery in Python applications.

# @Vocabulary
- **Message**: A unified base abstraction (e.g., `Union[Command, Event]`) representing data sent from one part of the system to another.
- **Command**: A message capturing user intent or a request for the system to perform an action. Represents a specific instruction sent by one actor to another specific actor.
- **Event**: A message broadcasted by an actor to all interested listeners capturing a fact about something that has already happened in the past.
- **Message Bus**: The central infrastructure component responsible for routing incoming Messages (Commands or Events) to their appropriate registered Handlers.
- **Handler**: A function or class method responsible for executing the business logic associated with a specific Command or Event. 
- **Transient Failure**: A temporary error (e.g., network hiccup, table deadlock) that can often be resolved by synchronously retrying the operation.
- **Tenacity**: A Python library used to implement automatic retry behavior with back-off strategies for transient failures.

# @Objectives
- The AI must strictly segregate the handling, naming, and error management of Commands versus Events.
- The AI must implement noisy, fast-failing error handling for Commands to ensure the sender receives feedback.
- The AI must implement independent, isolated error handling with exponential back-off retries for Events to ensure eventual consistency without breaking the primary application flow.
- The AI must ensure all Messages are implemented as simple data structures that produce easily reproducible string representations for logging and debugging.

# @Guidelines
- **Message Definition Rules**:
  - The AI MUST define all Commands and Events using Python `@dataclass`.
  - The AI MUST name Commands using imperative mood verb phrases (e.g., `Allocate`, `CreateBatch`, `ChangeBatchQuantity`).
  - The AI MUST name Events using past-tense verb phrases (e.g., `Allocated`, `BatchCreated`, `BatchQuantityChanged`, `OutOfStock`).
- **Handler Mapping Rules**:
  - The AI MUST map a Command to exactly ONE Handler (`Dict[Type[Command], Callable]`).
  - The AI MUST map an Event to a LIST of Handlers (`Dict[Type[Event], List[Callable]]`).
- **Command Dispatch Constraints**:
  - When dispatching a Command, the AI MUST execute its single registered handler.
  - If a Command handler raises an exception, the AI MUST log the exception and immediately re-raise it (`raise`). Commands MUST fail noisily.
  - The AI MUST allow Command handlers to return results (if temporarily required by the architecture), appending them to a results list.
- **Event Dispatch Constraints**:
  - When dispatching an Event, the AI MUST iterate over all registered handlers.
  - The AI MUST wrap the execution of each Event handler in a `try/except` block.
  - If an Event handler raises an exception, the AI MUST log the exception and use the `continue` statement to ensure subsequent handlers are still executed. Events MUST fail independently.
  - Event handlers MUST NOT return results.
- **Retry and Recovery Constraints**:
  - The AI MUST implement retry logic for Event handlers using a dedicated retry library (e.g., `tenacity`).
  - The AI MUST configure retries to use an exponentially increasing back-off period and a maximum attempt limit (e.g., 3 attempts).
  - Inside the retry loop, the AI MUST write a debug log line recording the event and the handler before execution to allow manual reproduction using the dataclass string representation.
- **Consistency Boundaries**:
  - A Command handler MUST modify only a single Aggregate per transaction. 
  - Subsequent bookkeeping, cleanup, or cross-aggregate updates MUST be triggered via Events, not within the original Command handler.

# @Workflow
When tasked with implementing or modifying a message, handler, or message bus, the AI must follow this algorithmic process:
1. **Identify Message Type**: Determine if the requested action is a request for action (Command) or a reaction to a past occurrence (Event).
2. **Define Data Structure**: Create a `@dataclass` for the message, adhering strictly to the imperative (Command) or past-tense (Event) naming convention.
3. **Register Handler**: 
   - If a Command, map it to a single function in `COMMAND_HANDLERS`.
   - If an Event, append its handler to the list in `EVENT_HANDLERS`.
4. **Implement Message Bus Routing**: Create a `handle` method that pops messages from a queue, checks `isinstance`, and routes to `handle_event` or `handle_command`.
5. **Implement Command Dispatcher**: Create `handle_command` that executes the handler, catches exceptions, logs them with `logger.exception`, and explicitly calls `raise`.
6. **Implement Event Dispatcher**: Create `handle_event` that iterates over handlers. 
7. **Implement Resiliency**: Wrap the inner loop of `handle_event` with a retry mechanism (e.g., `for attempt in Retrying(...):`). Log the execution attempt. Catch `RetryError`, log the failure, and explicitly call `continue`.

# @Examples (Do's and Don'ts)

### Defining Messages
**[DO]**
```python
from dataclasses import dataclass

class Command:
    pass

class Event:
    pass

@dataclass
class Allocate(Command):
    orderid: str
    sku: str
    qty: int

@dataclass
class Allocated(Event):
    orderid: str
    sku: str
    qty: int
    batchref: str
```

**[DON'T]**
```python
# Anti-pattern: Using past-tense for commands, imperative for events, and missing dataclasses
class AllocatedStock(Command): # Should be imperative (AllocateStock)
    def __init__(self, orderid, sku):
        self.orderid = orderid
        self.sku = sku

class ChangeQuantity(Event): # Should be past-tense (QuantityChanged)
    def __init__(self, ref, qty):
        self.ref = ref
        self.qty = qty
```

### Routing and Handler Dictionaries
**[DO]**
```python
EVENT_HANDLERS = {
    events.OutOfStock: [handlers.send_out_of_stock_notification],
    events.Allocated: [handlers.publish_allocated_event, handlers.add_allocation_to_read_model]
} # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.Allocate: handlers.allocate,
} # type: Dict[Type[commands.Command], Callable]
```

**[DON'T]**
```python
# Anti-pattern: Mapping commands to lists of handlers, treating events and commands identically
MESSAGE_HANDLERS = {
    commands.Allocate: [handlers.allocate, handlers.send_email], # Commands must have exactly ONE handler
    events.OutOfStock: handlers.send_out_of_stock_notification # Events must map to a LIST of handlers
}
```

### Handling Commands
**[DO]**
```python
def handle_command(
    command: commands.Command, queue: List[Message], uow: unit_of_work.AbstractUnitOfWork
):
    logger.debug('handling command %s', command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logger.exception('Exception handling command %s', command)
        raise # Fail noisily
```

**[DON'T]**
```python
# Anti-pattern: Swallowing exceptions in commands
def handle_command(command, queue, uow):
    try:
        handler = COMMAND_HANDLERS[type(command)]
        handler(command, uow=uow)
    except Exception:
        # Sender will never know the command failed!
        logger.error('Failed')
        pass 
```

### Handling Events with Retries
**[DO]**
```python
from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential

def handle_event(
    event: events.Event, queue: List[Message], uow: unit_of_work.AbstractUnitOfWork
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            for attempt in Retrying(
                stop=stop_after_attempt(3),
                wait=wait_exponential()
            ):
                with attempt:
                    logger.debug('handling event %s with handler %s', event, handler)
                    handler(event, uow=uow)
                    queue.extend(uow.collect_new_events())
        except RetryError as retry_failure:
            logger.error(
                'Failed to handle event %s times, giving up!', 
                retry_failure.last_attempt.attempt_number
            )
            continue # Fail independently, do not interrupt other handlers
```

**[DON'T]**
```python
# Anti-pattern: Bubbling up event exceptions and lacking retry logic
def handle_event(event, queue, uow):
    for handler in EVENT_HANDLERS[type(event)]:
        # No retry mechanism
        logger.debug('handling event %s', event)
        handler(event, uow=uow)
        # If this handler fails, subsequent handlers for this event are skipped, 
        # and the entire message bus crashes!
```