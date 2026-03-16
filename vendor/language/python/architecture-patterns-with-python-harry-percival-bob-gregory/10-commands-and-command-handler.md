# @Domain
These rules MUST be activated when the AI is analyzing, refactoring, generating, or documenting code related to message buses, event-driven architecture, command handlers, message dispatching, or error recovery in distributed systems/messaging loops.

# @Vocabulary
- **Message**: A dumb data structure (represented as a Python `@dataclass`) sent by one part of the system to another. The union type of `Command` and `Event`.
- **Command**: A message sent by one actor to another specific actor instructing the system to do something. Captures intent.
- **Event**: A message broadcast by an actor to all interested listeners recording a fact about something that has already happened.
- **Message Bus**: A publish-subscribe mechanism that routes Messages to their appropriate Handlers.
- **Command Handler**: A function dedicated to executing a specific Command. A Command has exactly ONE handler.
- **Event Handler**: A function that reacts to a specific Event. An Event can have ZERO to MANY handlers.
- **Transient Failure**: Temporary execution failures (e.g., network hiccups, table deadlocks) that can be recovered elegantly by retrying the operation.
- **Tenacity**: A Python library used to implement retry patterns with exponential back-off.

# @Objectives
- Enforce a strict semantic and structural segregation between Commands and Events.
- Implement distinct, purpose-built routing rules for Commands (1:1 routing) vs. Events (1:N routing).
- Ensure Commands fail noisily and bubble up errors to the sender.
- Ensure Events fail independently without interrupting the broader processing flow.
- Ensure system resilience by implementing synchronous error recovery (retry loops) for transient failures.

# @Guidelines
- **Message Data Structures**: The AI MUST define all Commands and Events as pure data structures using Python's `@dataclass`. 
- **Command Naming Convention**: The AI MUST name Commands using the imperative mood (verb phrases). E.g., `Allocate`, `CreateBatch`, `ChangeBatchQuantity`.
- **Event Naming Convention**: The AI MUST name Events using past-tense verb phrases. E.g., `Allocated`, `BatchCreated`, `BatchQuantityChanged`.
- **Message Bus Routing**: The AI MUST explicitly separate the routing dictionaries for Commands and Events:
  - `COMMAND_HANDLERS`: MUST map a `Command` type to a **single** `Callable`.
  - `EVENT_HANDLERS`: MUST map an `Event` type to a **List** of `Callable`s.
- **Command Error Handling**: When generating the `handle_command` dispatch logic, the AI MUST log any exceptions and **re-raise** them immediately. Commands MUST fail fast and fail noisily.
- **Event Error Handling**: When generating the `handle_event` dispatch logic, the AI MUST catch exceptions, log them, and **continue** execution. The failure of one event handler MUST NOT prevent the execution of subsequent event handlers or crash the message bus.
- **State Consistency**: The AI MUST structure Commands to modify a single aggregate and either succeed or fail in totality. Any subsequent bookkeeping, cleanup, or notification MUST be triggered via Events.
- **Pre-execution Logging**: The AI MUST inject a debug log line immediately before invoking a handler (e.g., `logger.debug('handling event %s with handler %s', event, handler)`). Because messages are dataclasses, this ensures a neatly printed summary is available for manual replay if needed.
- **Synchronous Error Recovery**: The AI MUST wrap event handler invocations in a retry loop using the `tenacity` library. The AI MUST configure the retry loop with bounded limits (e.g., `stop_after_attempt`) and exponential back-off (e.g., `wait_exponential`).

# @Workflow
When tasked with implementing a new system action or modifying the message bus, the AI MUST adhere to the following strict algorithmic process:
1. **Determine Message Category**: Evaluate whether the requirement represents an intent to change state (Command) or a reaction to a completed state change (Event).
2. **Define the Dataclass**: Create a `@dataclass` for the message, strictly applying the imperative naming rule for Commands or the past-tense naming rule for Events.
3. **Register the Handler**:
   - If a Command: Add it to `COMMAND_HANDLERS` mapping to exactly one handler function.
   - If an Event: Add it to `EVENT_HANDLERS` mapping to a list of handler functions.
4. **Implement Bus Dispatch Logic** (if modifying the bus):
   - Identify the message type using `isinstance(message, events.Event)` or `isinstance(message, commands.Command)`.
   - Route to `handle_event` or `handle_command` respectively.
5. **Implement Command Dispatch**: In `handle_command`, wrap the execution in a `try/except` block. In the `except` block, log the exception and `raise`.
6. **Implement Event Dispatch & Retry**: In `handle_event`, iterate over all registered handlers. Wrap the execution in a `try/except Exception` block. 
   - Inside the `try`, implement a `for attempt in Retrying(...):` loop using `tenacity`.
   - In the `except` block, log the failure and use `continue` to proceed to the next handler.

# @Examples (Do's and Don'ts)

## Message Naming and Definition
[DO]
```python
from dataclasses import dataclass

class Command:
    pass

class Event:
    pass

@dataclass
class Allocate(Command): # Imperative mood
    orderid: str
    sku: str
    qty: int

@dataclass
class BatchQuantityChanged(Event): # Past-tense
    ref: str
    qty: int
```

[DON'T]
```python
@dataclass
class AllocationRequired(Event): # Anti-pattern: Sounds like a command/intent
    orderid: str
    sku: str

@dataclass
class BatchCreated(Command): # Anti-pattern: Past tense used for a Command
    ref: str
```

## Handler Registration
[DO]
```python
EVENT_HANDLERS = {
    events.OutOfStock: [handlers.send_out_of_stock_notification],
} # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.Allocate: handlers.allocate,
} # type: Dict[Type[commands.Command], Callable]
```

[DON'T]
```python
# Anti-pattern: Mixing commands and events in the same dict, allowing multiple handlers for a command
HANDLERS = {
    commands.Allocate: [handlers.allocate, handlers.do_other_thing],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}
```

## Command Dispatch Error Handling
[DO]
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
        raise # MUST re-raise for commands
```

[DON'T]
```python
def handle_command(command, queue, uow):
    try:
        handler = COMMAND_HANDLERS[type(command)]
        handler(command, uow=uow)
    except Exception:
        pass # Anti-pattern: Swallowing exceptions on a command
```

## Event Dispatch and Synchronous Retry
[DO]
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
            continue # MUST continue to the next handler
```

[DON'T]
```python
def handle_event(event, queue, uow):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            handler(event, uow=uow)
        except Exception:
            raise # Anti-pattern: Re-raising interrupts the loop and crashes the bus
```