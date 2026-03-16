# @Domain
These rules MUST be activated when the user requests tasks involving the Service Layer, API endpoints, the Message Bus, domain events, workflow orchestration, or when refactoring existing service functions into an event-driven architecture.

# @Vocabulary
- **Situated Software**: Software that runs for extended periods, managing real-world physical processes where unexpected changes (e.g., damaged stock, shipping delays) occur constantly.
- **Message Bus**: The central routing mechanism and main entrypoint to the service layer, acting as a publish-subscribe system that maps `Events` to their respective `Handlers` and manages the event execution queue.
- **Event Handler (formerly Service Function)**: A function responsible for executing business use cases. In this architecture, ALL service functions must be expressed purely as event handlers that accept an `Event` and a `Unit of Work` (UoW).
- **Preparatory Refactoring**: The practice of "making the change easy; then making the easy change." Restructuring the architecture (e.g., converting services to handlers) before implementing new behavioral requirements.
- **Primitive Obsession (Mitigation)**: The anti-pattern of passing multiple primitive types (strings, ints) to service layers. Mitigated here by using `Event` dataclasses as the explicit input interface for the application.
- **Edge-to-Edge Testing**: Testing the entire flow of a system by pushing an event into the message bus and observing the output events or system state changes, without mocking internal handler logic.
- **Fake Message Bus**: A testing construct that overrides the event collection mechanism to intercept and record published events rather than executing them, allowing isolated unit testing of complex event chains.

# @Objectives
- The AI MUST transform the application into a pure message-processing machine where every input and internal state change is handled as an `Event`.
- The AI MUST eliminate the conceptual distinction between internal events (raised by the domain model) and external events (triggered by API calls).
- The AI MUST decouple API endpoints from service-layer implementations by enforcing the Message Bus as the sole entrypoint.
- The AI MUST utilize `Event` classes to cleanly encapsulate use-case inputs, avoiding primitive obsession in function signatures.

# @Guidelines

## Preparatory Refactoring
- When introducing a new workflow that fundamentally alters how events are processed, the AI MUST first refactor existing structural code (e.g., converting all services to handlers) BEFORE adding the new feature logic.

## Event as the Universal Interface
- The AI MUST define all inputs to the system as `Event` dataclasses.
- The AI MUST NOT pass raw primitives (e.g., `sku: str`, `qty: int`) from the API to the service layer.
- The AI MUST instantiate an `Event` within the API routing method and pass ONLY that event to the Message Bus.

## Handler Signatures and Logic
- The AI MUST write every use case as an event handler function.
- Every event handler MUST accept exactly two arguments: `event: events.<SpecificEvent>` and `uow: unit_of_work.AbstractUnitOfWork`.
- Handlers MUST extract parameters directly from the `event` object (e.g., `line = OrderLine(event.orderid, event.sku, event.qty)`).
- If a handler requires specific data retrieval, the AI MUST add targeted query methods to the repository (e.g., `get_by_batchref`) rather than performing complex loops or filtering inside the handler.

## Message Bus Implementation
- The Message Bus `handle` function MUST accept `(event: events.Event, uow: unit_of_work.AbstractUnitOfWork)`.
- The Message Bus MUST maintain an internal `queue` of events initialized with the incoming event.
- The Message Bus MUST process events by popping them from the front of the queue, invoking all registered handlers for that event type, and passing the `uow` to the handler.
- After invoking handlers for an event, the Message Bus MUST dynamically extend the queue by calling `uow.collect_new_events()`.
- **Temporary Hack Exception**: Until CQRS is implemented, if the API requires a return value (e.g., an allocated batch reference), the AI MAY temporarily allow the Message Bus to collect and return results from handlers.

## Testing Strategy
- **Edge-to-Edge Testing**: The AI MUST write integration/E2E tests that inject an event into the Message Bus and assert the final state or resulting events, verifying the entire chain of handlers.
- **Event-Based Unit Testing**: Service layer unit tests MUST NOT call handler functions directly. They MUST call `messagebus.handle(event, uow)`.
- **Isolated Handler Testing**: If an event chain is highly complex, the AI MAY implement a `FakeUnitOfWorkWithFakeMessageBus` (or a `FakeMessageBus` class) that overrides `publish_events` to append events to a local list instead of routing them. This allows the AI to assert that a specific event was generated without triggering downstream handlers.

## Abstracting the Message Bus (Class-Based)
- When refactoring for improved testability, the AI SHOULD implement the Message Bus as a configurable class (`AbstractMessageBus` / `MessageBus`) containing a `HANDLERS` dictionary mapping, rather than relying on a module-level singleton.

# @Workflow
When tasked with implementing a new requirement that alters domain state and cascades into further actions, the AI MUST follow this exact sequence:

1. **Define the Events**: Create the necessary `Event` dataclasses (e.g., `BatchQuantityChanged`, `AllocationRequired`) in `events.py`.
2. **Refactor Existing Services (if applicable)**: Rename `services.py` to `handlers.py`. Update all existing service functions to accept an `Event` object instead of primitive arguments.
3. **Update the Message Bus**: Ensure the Message Bus manages an event queue and collects new events from the UoW after each handler executes. Register the refactored handlers in the `HANDLERS` dictionary.
4. **Refactor the API Entrypoints**: Update Flask/web controllers to instantiate the new `Event` objects from JSON payloads and pass them strictly to `messagebus.handle(event, uow)`.
5. **Write Edge-to-Edge Tests**: Write tests in terms of Events. Pass an initial Event into the bus and assert the expected downstream state modifications or final Event outputs.
6. **Implement Domain Logic**: Add the necessary methods to the Domain Model (e.g., `Product.change_batch_quantity`) ensuring it mutates state AND appends the subsequent required `Event` (e.g., `AllocationRequired`) to `self.events`.
7. **Write the New Handler**: Implement the new handler function in `handlers.py`, retrieve the aggregate via the `uow`, invoke the domain method, and call `uow.commit()`.

# @Examples (Do's and Don'ts)

## API Entrypoints
**[DO]** Instantiate an event and pass it to the message bus:
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    try:
        event = events.AllocationRequired(
            request.json['orderid'], 
            request.json['sku'], 
            request.json['qty']
        )
        results = messagebus.handle(event, unit_of_work.SqlAlchemyUnitOfWork())
        batchref = results.pop(0)
    except InvalidSku as e:
        return jsonify({'message': str(e)}), 400
    return jsonify({'batchref': batchref}), 201
```

**[DON'T]** Pass primitives directly to a service layer from the API:
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    # ANTI-PATTERN: Primitives passed to a service function
    batchref = services.allocate(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
        unit_of_work.SqlAlchemyUnitOfWork()
    )
    return jsonify({'batchref': batchref}), 201
```

## Handler Signatures
**[DO]** Accept an Event and a Unit of Work:
```python
def allocate(
    event: events.AllocationRequired, 
    uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(event.orderid, event.sku, event.qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {event.sku}')
        batchref = product.allocate(line)
        uow.commit()
        return batchref
```

**[DON'T]** Accept primitive arguments representing command intent:
```python
# ANTI-PATTERN: Primitive Obsession in the service layer
def allocate(
    orderid: str, 
    sku: str, 
    qty: int, 
    uow: unit_of_work.AbstractUnitOfWork
) -> str:
```

## Message Bus Queue Management
**[DO]** Dynamically process an event queue to handle side-effect events:
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

**[DON'T]** Execute a single event without checking for newly raised domain events:
```python
# ANTI-PATTERN: Fails to process cascaded events generated by the domain
def handle(event: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    for handler in HANDLERS[type(event)]:
        handler(event, uow=uow)
```

## Service Layer Testing
**[DO]** Test by pushing events into the message bus:
```python
def test_returns_allocation():
    uow = FakeUnitOfWork()
    messagebus.handle(
        events.BatchCreated("batch1", "COMPLICATED-LAMP", 100, None), uow
    )
    result = messagebus.handle(
        events.AllocationRequired("o1", "COMPLICATED-LAMP", 10), uow
    )
    assert result == ["batch1"]
```

**[DON'T]** Call service functions directly in unit tests:
```python
def test_returns_allocation():
    uow = FakeUnitOfWork()
    # ANTI-PATTERN: Directly invoking service methods bypasses the message bus architecture
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"
```