# @Domain

These rules MUST be activated when the AI is asked to implement new requirements that involve side-effects, secondary workflows, notifications (e.g., sending emails or SMS), or cross-aggregate communications within a Python application using Domain-Driven Design (DDD), the Repository pattern, the Unit of Work (UoW) pattern, or the Service Layer pattern. They also apply when the user requests an Event-Driven Architecture or Message Bus implementation.

# @Vocabulary

When discussing or generating code in this domain, the AI MUST strictly adhere to the following definitions to maintain the exact mental model of the author:
- **Event (Domain Event):** A pure data structure (value object) representing a fact about something that has happened in the system. It contains data but no behavior.
- **Message Bus:** A piece of infrastructure, usually implemented as a dictionary mapping, that routes Events to their subscribed Handlers. It acts as a publish-subscribe system.
- **Handler:** A function subscribed to an Event via the Message Bus. It receives the Event and performs the necessary orchestration, side-effect, or infrastructure interaction.
- **Single Responsibility Principle (SRP):** The principle that a class or function should have only one reason to change. In this context, it means separating core domain use cases from side-effects (e.g., allocating stock is separate from sending an email).
- **Seen Aggregates:** A collection (`set`) maintained by a Repository to track which Aggregates have been loaded or added during a transaction, allowing the UoW to inspect them for new events.
- **Workflow Orchestration:** A set of steps the system must follow to achieve a goal (e.g., "try to allocate, and if it fails, send an email").

# @Objectives

When applying this chapter's knowledge, the AI MUST achieve the following overarching goals:
- Keep the Domain Model entirely free of infrastructure concerns (e.g., no email sending logic, no external API calls).
- Keep Web Controllers (API endpoints) extremely thin and free of orchestration logic.
- Prevent the Service Layer from becoming a tangled mess of primary logic and secondary side-effects.
- Separate temporal or causal requirements (e.g., "When X happens, then do Y") using Domain Events.
- Treat events as first-class citizens in the model to improve testability, observability, and isolation of concerns.

# @Guidelines

The AI MUST abide by the following granular constraints, formatting requirements, and architectural rules:

- **Web Controller Constraints:**
  - The AI MUST NOT place side-effect logic, error-catching for the purpose of side-effects, or workflow orchestration inside web controllers/API endpoints.
- **Domain Model Constraints:**
  - The AI MUST NOT import or invoke infrastructure code (e.g., `email.send_mail()`) inside the Domain Model.
  - The AI MUST define Events as simple `@dataclass` objects.
  - The AI MUST name Events using the ubiquitous language of the domain, strictly formatted as past-tense verb phrases (e.g., `OutOfStock`, `BatchCreated`).
  - The AI MUST initialize an empty list `self.events = []` (type-hinted as `List[Event]`) inside the `__init__` method of the Aggregate root.
  - The AI MUST record facts by appending instantiated Event objects to the `self.events` list of the Aggregate.
  - **Exception Replacement Rule:** The AI MUST NOT use exceptions for control flow to trigger side effects. If implementing Domain Events, the AI MUST replace exceptions describing a domain concept with a published Event (e.g., replace `raise OutOfStock()` with `self.events.append(OutOfStock())`).
- **Service Layer Constraints:**
  - The AI MUST NOT write Service Layer functions that manually handle side-effects using `try/except` blocks (e.g., catching an error just to send an email).
- **Message Bus Implementation Constraints:**
  - The AI MUST implement the Message Bus to map Event types to lists of Handler functions.
  - The AI MUST execute Handlers synchronously within the Message Bus (avoiding asynchronous parallel threads for this pattern, to keep units of work small and conceptually simple).
- **Event Publishing constraints (The "Option 3" Approach):**
  - The AI MUST implement the preferred "UoW Publishes Events" pattern.
  - To support this, the AI MUST implement a `self.seen = set()` attribute on the base/abstract Repository.
  - The AI MUST ensure the Repository adds any retrieved or added Aggregate to the `self.seen` set.
  - The AI MUST override the UoW's `commit` method (using a private `_commit()` for the database transaction) to loop through all `seen` aggregates, pop their events, and pass them to the Message Bus.
- **Message Bus Trade-off Warnings:**
  - The AI MUST be aware of and warn the user (if discussing architecture) of the trade-offs: hidden event-handling code executes synchronously, potentially delaying web endpoint responses; overall flows become implicit; and there is a risk of infinite loops/circular dependencies.

# @Workflow

When instructed to implement a new secondary requirement or side-effect (e.g., "send a notification when X fails"), the AI MUST follow this rigid, step-by-step algorithmic process:

1. **Define the Event:**
   - Create a new `@dataclass` in the events module (e.g., `events.py`) inheriting from a base `Event` class.
   - Name it using a past-tense verb. Define only the data payload needed.
2. **Update the Domain Model to Raise the Event:**
   - Ensure the Aggregate root has a `self.events = []` attribute.
   - In the relevant domain method, append the newly defined Event to `self.events` when the trigger condition is met.
   - Remove any exceptions that were previously raised for this specific control-flow purpose.
3. **Update the Repository to Track Aggregates:**
   - In `AbstractRepository.__init__`, initialize `self.seen = set()`.
   - In the `add` method, call a private `_add` method and then `self.seen.add(aggregate)`.
   - In the `get` method, call a private `_get` method, and if an aggregate is found, add it to `self.seen`.
   - Update concrete repositories to implement `_add` and `_get` instead of `add` and `get`. Ensure fakes call `super().__init__()`.
4. **Update the Unit of Work to Publish Events:**
   - In `AbstractUnitOfWork.commit()`, execute the private `self._commit()` (to save to the DB), followed by a `self.publish_events()` method.
   - Implement `publish_events()`: Iterate over `self.repository.seen`. While `aggregate.events` has items, `pop(0)` the first event and pass it to `messagebus.handle(event)`.
5. **Implement the Message Bus and Handler:**
   - Write the Handler function (e.g., `send_notification(event: Event)`) encapsulating the infrastructure logic.
   - Update the Message Bus module: Map the Event type to a list containing the Handler function in a `HANDLERS` dictionary.
   - Implement the `messagebus.handle(event)` method to loop over `HANDLERS[type(event)]` and invoke each handler.

# @Examples (Do's and Don'ts)

### Defining an Event
- **[DO]**
  ```python
  from dataclasses import dataclass

  class Event:
      pass

  @dataclass
  class OutOfStock(Event):
      sku: str
  ```
- **[DON'T]** (Do not add behavior or infrastructure to events, do not use present tense)
  ```python
  class OutOfStockEvent:
      def __init__(self, sku):
          self.sku = sku
      def send_email(self):
          email.send("Out of stock!")
  ```

### Raising Events in the Domain Model
- **[DO]**
  ```python
  class Product:
      def __init__(self, sku: str, batches: List[Batch]):
          self.sku = sku
          self.batches = batches
          self.events = [] # type: List[events.Event]

      def allocate(self, line: OrderLine) -> str:
          try:
              batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
              batch.allocate(line)
              return batch.reference
          except StopIteration:
              self.events.append(events.OutOfStock(line.sku))
              return None
  ```
- **[DON'T]** (Do not raise exceptions for control flow, do not call infrastructure)
  ```python
  class Product:
      def allocate(self, line: OrderLine) -> str:
          try:
              # ... allocation logic ...
          except StopIteration:
              email.send_mail('stock@made.com', f'Out of stock for {line.sku}')
              raise OutOfStock(f'Out of stock for sku {line.sku}')
  ```

### Structuring the Web Controller
- **[DO]** (Keep it thin, strictly routing input to the Service Layer)
  ```python
  @app.route("/allocate", methods=['POST'])
  def allocate_endpoint():
      line = model.OrderLine(
          request.json['orderid'],
          request.json['sku'],
          request.json['qty'],
      )
      try:
          uow = unit_of_work.SqlAlchemyUnitOfWork()
          batchref = services.allocate(line, uow)
      except services.InvalidSku as e:
          return jsonify({'message': str(e)}), 400

      return jsonify({'batchref': batchref}), 201
  ```
- **[DON'T]** (Do not intercept exceptions to perform orchestration side-effects)
  ```python
  @app.route("/allocate", methods=['POST'])
  def allocate_endpoint():
      # ...
      try:
          batchref = services.allocate(line, uow)
      except model.OutOfStock as e:
          send_mail('out of stock', 'stock_admin@made.com', f'{line.sku}')
          return jsonify({'message': str(e)}), 400
  ```

### Collecting and Publishing Events in the UoW / Repository
- **[DO]**
  ```python
  # Repository tracks seen aggregates
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

  # UoW publishes events automatically
  class AbstractUnitOfWork(abc.ABC):
      def commit(self):
          self._commit()
          self.publish_events()

      def publish_events(self):
          for product in self.products.seen:
              while product.events:
                  event = product.events.pop(0)
                  messagebus.handle(event)
  ```
- **[DON'T]** (Do not force the Service Layer to manually grab events and pass them to the message bus)
  ```python
  # In services.py
  def allocate(orderid, sku, qty, uow):
      with uow:
          product = uow.products.get(sku)
          batchref = product.allocate(line)
          uow.commit()
          # Violates Option 3 (UoW pattern):
          messagebus.handle(product.events) 
          return batchref
  ```