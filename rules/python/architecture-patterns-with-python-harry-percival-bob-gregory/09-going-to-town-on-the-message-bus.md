# @Domain
Trigger these rules when tasked with refactoring an application toward an event-driven architecture, implementing or modifying a Message Bus, converting service-layer functions into event handlers, or designing "situated software" that must respond to complex, asynchronous real-world events and chained workflows. 

# @Vocabulary
- **Situated Software**: Software that runs for extended periods of time, managing real-world physical processes where unexpected events (e.g., damaged stock, delays) occur continuously.
- **Message Processor / Event Processor**: An architectural state where the message bus acts as the sole entrypoint to the service layer, and all inputs (internal and external) are modeled as events.
- **Preparatory Refactoring**: The workflow principle of "Make the change easy; then make the easy change." Refactoring existing code to accept a new architectural pattern before implementing new business logic on top of it.
- **Event Interface (Replacing Primitive Obsession)**: The practice of coupling the external world (API/tests) to domain Event classes instead of a loose scattering of primitives (strings/ints), providing a unified and consistent contract.
- **Split Transaction Integrity Risk**: The inherent risk introduced when a single logical workflow is split across multiple chained events and handled in separate Units of Work (database transactions). If the first succeeds and the second fails, the system may reach an inconsistent state.
- **Fake Message Bus**: A test double used to isolate the testing of event handlers. It captures published events in memory rather than passing them to downstream handlers, avoiding the need to test complex, edge-to-edge chained side-effects.

# @Objectives
- Transform the application into a pure message-processing machine where the Message Bus is the primary and only entrypoint to the service layer.
- Ensure all service-layer functions are strictly refactored into event handlers.
- Invert the dependency between the Unit of Work (UoW) and the Message Bus so the UoW passively yields events and the Message Bus actively collects and queues them.
- Standardize all system inputs and tests to utilize Event dataclasses rather than primitive data types.

# @Guidelines
- **Preparatory Refactoring Mandate**: When implementing a new chained event requirement, the AI MUST first refactor existing service functions into event handlers, ensure tests pass, and ONLY THEN implement the new requirement.
- **Handler Signature Rule**: The AI MUST construct all service-layer event handlers to accept exactly two arguments: the specific `event` object and the `uow`. 
- **Message Bus Queueing**: The AI MUST implement the `handle()` method of the Message Bus using a dynamic `queue` (e.g., a Python `list`). As handlers process events, the AI MUST extend this queue with newly generated events collected from the UoW.
- **Passive Unit of Work**: The AI MUST NOT allow the UoW to actively push events to the Message Bus. The UoW MUST provide a `collect_new_events()` generator method that pops events off loaded aggregates.
- **Temporary Result Hack**: Until Command-Query Responsibility Segregation (CQRS) is fully implemented, the AI MUST allow the Message Bus to collect and return results (e.g., generated IDs or references) from handlers to satisfy synchronous API requirements.
- **API Endpoint Constraint**: API controllers/endpoints MUST be exceptionally thin. The AI MUST restrict endpoints to: parsing JSON, instantiating an Event dataclass, passing the event to `messagebus.handle()`, and returning the result. 
- **Split Transaction Awareness**: When designing workflows that emit events to trigger subsequent handlers, the AI MUST explicitly account for the fact that these run in separate database transactions.
- **Isolated Handler Testing**: For deeply chained events, the AI MUST implement a `FakeMessageBus` (or `FakeUnitOfWorkWithFakeMessageBus`) to test handlers in isolation by asserting on the events emitted, rather than testing downstream side-effects.
- **Class-Based Message Bus**: The AI SHOULD consider implementing the Message Bus as an instantiable class (e.g., `AbstractMessageBus` and `MessageBus`) rather than a module-level singleton, to facilitate easier faking during isolated testing.

# @Workflow
To successfully implement the "Whole App is a Message Bus" architecture, the AI MUST follow this exact algorithmic step-by-step process:

1. **Define Input Events**: Analyze the required inputs (API or internal) and define them as Event dataclasses in `events.py`.
2. **Refactor Service Functions**: Modify existing functions in `services.py` (now `handlers.py`) to accept `(event: events.SpecificEvent, uow: unit_of_work.AbstractUnitOfWork)`. Extract required data exclusively from the `event` object.
3. **Refactor the Message Bus**:
    - Initialize a `queue` with the incoming event.
    - Loop `while queue:`.
    - Pop the event, find its registered handler(s), and invoke `handler(event, uow=uow)`.
    - Collect resulting output (temporary hack) and append to a `results` list.
    - Extend the `queue` by calling `queue.extend(uow.collect_new_events())`.
    - Return `results`.
4. **Refactor the UoW**: Remove `messagebus` imports from the UoW. Replace `publish_events()` with a `collect_new_events()` generator that yields and pops events from `product.events`.
5. **Update Test Suites**: Rewrite all unit tests to instantiate Event objects and pass them to `messagebus.handle()`. Remove all direct calls to service/handler functions in the tests.
6. **Update the API / Entrypoints**: Refactor Flask controllers (or equivalent) to instantiate Event objects from the request payload and pass them to `messagebus.handle()`.
7. **Implement New Requirements**: With the architecture prepped, implement the new business logic:
    - Add new domain logic that modifies state and appends subsequent events to the aggregate's `.events` list.
    - Write a new handler for the new event.
    - Map the new event to the new handler in the Message Bus `HANDLERS` dictionary.

# @Examples (Do's and Don'ts)

### Service Layer Signatures (Primitive Obsession vs Event Interface)
[DO]
```python
def allocate(
    event: events.AllocationRequired, 
    uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(event.orderid, event.sku, event.qty)
    with uow:
        product = uow.products.get(sku=event.sku)
        # ...
```
[DON'T]
```python
# Anti-pattern: Primitive obsession and missing the Event interface
def allocate(
    orderid: str, 
    sku: str, 
    qty: int, 
    uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    # ...
```

### Message Bus Queue Management
[DO]
```python
def handle(event: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            results.append(handler(event, uow=uow))
        queue.extend(uow.collect_new_events())
    return results
```
[DON'T]
```python
# Anti-pattern: No internal queue. Cannot process chained events emitted during the transaction.
def handle(event: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    for handler in HANDLERS[type(event)]:
        handler(event, uow=uow)
```

### Unit of Work Event Collection
[DO]
```python
class AbstractUnitOfWork(abc.ABC):
    def collect_new_events(self):
        for product in self.products.seen:
            while product.events:
                yield product.events.pop(0)
```
[DON'T]
```python
# Anti-pattern: Circular dependency. UoW actively pushes to message bus.
from . import messagebus

class AbstractUnitOfWork(abc.ABC):
    def publish_events(self):
        for product in self.products.seen:
            while product.events:
                event = product.events.pop(0)
                messagebus.handle(event)
```

### API Endpoint Usage
[DO]
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    try:
        event = events.AllocationRequired(
            request.json['orderid'], 
            request.json['sku'], 
            request.json['qty'],
        )
        results = messagebus.handle(event, unit_of_work.SqlAlchemyUnitOfWork())
        batchref = results.pop(0)
    # ... return response
```
[DON'T]
```python
# Anti-pattern: API calls service functions directly, bypassing the message processor architecture.
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    batchref = services.allocate(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
        unit_of_work.SqlAlchemyUnitOfWork(),
    )
    # ... return response
```