# @Domain
These rules activate when the user requests the implementation of secondary business workflows, side-effects (e.g., notifications, emails, logging), cross-consistency boundary updates, or event-driven architecture components (Events, Message Bus, Event Handlers) within a Python application.

# @Vocabulary
- **Event**: A purely data-bearing value object (usually a `@dataclass`) representing a fact about something that happened in the past within the domain.
- **Message Bus**: A publish-subscribe routing mechanism (often a `dict`) that maps Events to their subscribed Handler functions.
- **Handler**: A function designated to react to a specific Event dispatched by the Message Bus.
- **Single Responsibility Principle (SRP)**: The concept that a function or class should have only one reason to change. Specifically, core use cases (e.g., allocation) must be separated from secondary side-effects (e.g., sending emails).
- **Aggregate**: The domain model entrypoint which is now also responsible for recording Events that occur during its operations in an `.events` list.
- **Option 3 (UoW Event Publishing)**: The architectural pattern where the Unit of Work (UoW) is responsible for collecting Events from all Aggregates it has seen during a transaction and pushing them to the Message Bus.
- **.seen**: A `set` maintained by the Repository pattern to track which Aggregates have been loaded or added during the current Unit of Work lifespan.

# @Objectives
- Decouple primary domain use cases from secondary infrastructure side-effects (like email or logging) to adhere strictly to the Single Responsibility Principle.
- Prevent infrastructure concerns from polluting Web Controllers, Domain Models, and Service Layer functions.
- Transform the application into an event-driven system where the Domain Model records facts (Events) and the Message Bus dispatches those facts to independent Handlers.
- Centralize the collection and dispatching of Events within the Unit of Work to abstract event-handling logic away from the Service Layer.

# @Guidelines
- **Event Structure**: The AI MUST define Events as simple, behaviorless data structures. Use Python's `@dataclass` and inherit from a base `Event` class. 
- **Event Naming**: The AI MUST name Events using past-tense verbs in the ubiquitous language of the domain (e.g., `OutOfStock`, `Allocated`).
- **Domain Exception Replacement**: When a domain rule fails or a significant domain concept occurs, the AI MUST NOT use exceptions for control flow if an Event can represent the concept. The domain model MUST record the fact by appending the Event to a `self.events` list.
- **No Infrastructure in Models/Services**: The AI MUST NOT import infrastructure modules (like `email`, `requests`, etc.) into Web Controllers, Domain Models, or Service Layer orchestration functions.
- **Repository Tracking**: The AI MUST implement a `self.seen = set()` in the Abstract Repository constructor. The Abstract Repository MUST implement public `add()` and `get()` methods that add the aggregate to `self.seen` and then delegate to subclass-specific `_add()` and `_get()` methods.
- **UoW Event Publishing**: The AI MUST implement event publishing in the Unit of Work. The `commit()` method MUST first call `self._commit()` (implemented by subclasses) and then immediately call a `publish_events()` method that loops through all aggregates in `self.repository.seen`, popping events from `aggregate.events` and passing them to the Message Bus.
- **Message Bus Mapping**: The AI MUST implement the Message Bus as a mapping dictionary `HANDLERS = {EventType: [handler_function1, handler_function2]}`. 
- **Synchronous Execution**: The AI MUST implement event handlers to execute synchronously. Note the trade-off: service-layer functions will not complete until all event handlers finish.
- **Avoid Circular Dependencies**: The AI MUST carefully manage event handlers to prevent infinite loops of event generation and handling.

# @Workflow
1. **Define the Event**: Create a `@dataclass` representing the domain fact in past-tense (e.g., `OutOfStock(sku: str)`).
2. **Update the Aggregate**: Add a `self.events = []` attribute to the Aggregate's `__init__`. Modify the Aggregate's methods to append Event instances to `self.events` when specific domain triggers occur.
3. **Refactor the Repository**: 
   - Add `self.seen = set()` to the Abstract Repository's `__init__`.
   - Create public `add()` and `get()` methods that append to `self.seen` and call abstract `_add()` and `_get()` methods.
   - Update concrete Repositories to implement `_add()` and `_get()`.
4. **Refactor the Unit of Work**:
   - Rename the existing DB commit logic to an abstract `_commit()` method.
   - Create a `publish_events()` method that iterates over `self.repository.seen`, loops `while aggregate.events:`, pops the first event, and passes it to `messagebus.handle(event)`.
   - Update the public `commit()` method to call `self._commit()` followed by `self.publish_events()`.
5. **Create the Message Bus**: Define a `handle(event)` function that looks up the event's type in a `HANDLERS` dictionary and iterates through the subscribed functions, executing each.
6. **Implement the Handler**: Create an isolated Handler function in the Service Layer (or dedicated Handlers module) that accepts the Event and executes the infrastructure side-effect (e.g., sending an email).
7. **Register the Handler**: Add the Event and Handler function to the `HANDLERS` dictionary in the Message Bus.
8. **Clean the Service Layer**: Remove all explicit side-effect triggers, `try/except` blocks handling domain exceptions for side-effects, and infrastructure imports from the primary Service Layer orchestration function.

# @Examples (Do's and Don'ts)

**[DO]** Define Events as simple, past-tense dataclasses.
```python
from dataclasses import dataclass

class Event:
    pass

@dataclass
class OutOfStock(Event):
    sku: str
```

**[DON'T]** Mix infrastructure side-effects directly into Web Controllers, Service Layers, or Domain Models.
```python
# ANTI-PATTERN: Side-effects in the Service Layer violating SRP
def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork):
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        try:
            batchref = product.allocate(line)
            uow.commit()
            return batchref
        except model.OutOfStock:
            # DON'T do this!
            email.send_mail('stock@made.com', f'Out of stock for {line.sku}')
            raise
```

**[DO]** Record events in the Domain Model instead of using exceptions for control flow.
```python
class Product:
    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku
        self.batches = batches
        self.events = [] # DO: Initialize events list
    
    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            return batch.reference
        except StopIteration:
            # DO: Append to events rather than raising exception for control flow
            self.events.append(events.OutOfStock(line.sku))
            return None
```

**[DO]** Track seen aggregates in the Repository using the `_add` and `_get` pattern.
```python
class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, product: model.Product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.Product:
        raise NotImplementedError
```

**[DO]** Publish events from the Unit of Work after committing.
```python
class AbstractUnitOfWork(abc.ABC):
    def commit(self):
        self._commit()
        self.publish_events()

    def publish_events(self):
        for product in self.products.seen:
            while product.events:
                event = product.events.pop(0)
                messagebus.handle(event)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError
```

**[DON'T]** Manually trigger the message bus in every Service Layer function.
```python
# ANTI-PATTERN: Option 1/2 is less elegant than Option 3
def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork):
    # ...
    try:
        batchref = product.allocate(line)
        uow.commit()
        return batchref
    finally:
        # DON'T manually handle events in the service layer if the UoW can do it automatically
        messagebus.handle(product.events) 
```