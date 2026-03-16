# @Domain
This rule set activates when the AI is tasked with adding, modifying, or refactoring application dependencies, creating adapters for external systems, configuring application startup/initialization, implementing message buses, writing service-layer handlers, or writing unit/integration tests that interact with external state (I/O, database, notifications) in a Python-based Event-Driven Architecture.

# @Vocabulary
- **Dependency Injection (DI):** The practice of providing a component with its required dependencies from the outside, rather than having the component import or instantiate them directly.
- **Implicit Dependency:** A dependency acquired directly within the code via an `import` statement or direct instantiation.
- **Explicit Dependency:** A dependency declared clearly in a function signature or class constructor, fulfilling the Dependency Inversion Principle.
- **Composition Root / Bootstrapper:** A centralized script or module (e.g., `bootstrap.py`) responsible for initializing dependencies, performing one-time setup (like starting ORM mappers), wiring dependencies into handlers, and returning the configured entrypoint object (e.g., `MessageBus`).
- **Manual DI:** Dependency injection performed without a third-party framework, using language features like closures, partials, or standard classes.
- **Closure / Partial Function:** Functional programming techniques used to bind dependencies to a function ahead of execution, leaving a callable that only requires the runtime arguments (e.g., the command/event).
- **Late Binding:** A behavior in Python closures (lambdas) where variables are looked up at execution time. This can cause bugs if mutable dependencies are used in loops during manual DI.
- **MessageBus (Class):** A stateful object initialized with already-injected handlers, replacing the static/module-level message bus to allow isolated dependency contexts.
- **Adapter:** A concrete implementation of a defined interface (Port) that interacts with external I/O (e.g., Email Server, Redis, SQL Database).

# @Objectives
- **Eliminate Implicit Dependencies:** The AI MUST remove direct imports of infrastructural I/O inside domain or service-layer code.
- **Enforce Explicit Dependencies:** All external interactions (UoW, email, pub/sub) MUST be passed into handlers as arguments.
- **Centralize Wiring:** The AI MUST use a Composition Root (`bootstrap.py`) to wire dependencies, keeping entrypoints (API, CLI, consumers) completely free of initialization logic.
- **Eradicate Mocks in Favor of Fakes:** The AI MUST completely avoid the use of `mock.patch` for application dependencies in testing, utilizing injected Fake objects instead.
- **Standardize Adapter Creation:** The AI MUST follow a strict, multi-step process for defining, faking, and integration-testing any new external dependency.

# @Guidelines
- **Explicit over Implicit:** Handlers MUST explicitly declare dependencies in their signatures (e.g., `def allocate(cmd: commands.Allocate, uow: unit_of_work.AbstractUnitOfWork):`). 
- **No Monkeypatching:** The AI MUST NOT use `unittest.mock.patch` to stub out side effects in tests. Tests MUST configure the system by injecting Fake implementations through the bootstrapper.
- **Bootstrap Initialization:** The `bootstrap.py` module MUST contain default production dependencies but allow EVERY dependency to be overridden via keyword arguments. It MUST handle one-time setup tasks, such as `orm.start_mappers()`.
- **Injection Methods (Functional):** When using functional handlers, the AI MUST use `functools.partial`, `lambda` closures, or an `inspect.signature`-based dynamic injector to bind dependencies to handlers in the bootstrapper.
- **Injection Methods (Class-Based):** If handlers are implemented as classes, the AI MUST inject dependencies via the `__init__` method and implement the handler logic inside the `__call__` method.
- **Message Bus Instantiation:** The `MessageBus` MUST be implemented as a class that accepts `event_handlers` and `command_handlers` dictionaries in its `__init__` method. The AI MUST NOT use a static/global module dictionary for handlers.
- **Thread Safety Warning:** When implementing the `MessageBus` class, the AI MUST be aware that utilizing `self.queue` on a globally shared bus instance is NOT thread-safe.
- **Entrypoint Simplicity:** Entrypoints (e.g., Flask routes, Redis consumers) MUST ONLY instantiate the bootstrapper (`bus = bootstrap.bootstrap()`), parse the incoming request into a Command/Event, and pass it to the bus (`bus.handle(cmd)`). They MUST NOT instantiate Units of Work or repositories directly.
- **Adapter Complexity:** Use simple `Callable` signatures for basic dependencies (e.g., `send_mail: Callable`). Use Abstract Base Classes (ABCs) for complex dependencies with multiple methods (e.g., `notifications: AbstractNotifications`).

# @Workflow
When tasked with adding a new external dependency, creating a new use case, or refactoring existing code to use DI, the AI MUST follow this exact sequence:

1.  **Define the Port (Interface):**
    - For simple actions, define a `Callable` type hint.
    - For complex interactions, define an Abstract Base Class (ABC) in the `adapters` module with explicit `@abc.abstractmethod` signatures.
2.  **Implement the Real Adapter:**
    - Create a concrete class or function that implements the interface and performs the actual I/O (e.g., `EmailNotifications` using `smtplib`).
3.  **Implement the Fake Adapter:**
    - Create an in-memory Fake version of the adapter for unit tests (e.g., `FakeNotifications` using a `defaultdict` list).
4.  **Update Handlers:**
    - Modify the target service-layer handler signature to accept the new dependency explicitly. Do NOT import the adapter directly into the handler module.
5.  **Update the Bootstrapper (`bootstrap.py`):**
    - Add the new dependency to the `bootstrap()` function signature with the real adapter as the default value.
    - Map the dependency to the handlers using manual lambdas, partials, or `inspect.signature` injection.
6.  **Update Unit Tests:**
    - Modify the test setup to call `bootstrap.bootstrap()` and pass the Fake adapter as an argument. Assert against the state of the Fake object.
7.  **Write Integration Tests:**
    - Create an integration test that uses the bootstrapper with the *real* adapter, utilizing a local test environment (e.g., Docker container, MailHog) to verify actual I/O execution.

# @Examples (Do's and Don'ts)

## Dependency Declaration inside Handlers
- **[DO]**
  ```python
  def send_out_of_stock_notification(
      event: events.OutOfStock, 
      send_mail: Callable,
  ):
      send_mail('stock@example.com', f'Out of stock for {event.sku}')
  ```
- **[DON'T]**
  ```python
  from allocation.adapters import email # IMPLICIT DEPENDENCY

  def send_out_of_stock_notification(event: events.OutOfStock):
      email.send_mail('stock@example.com', f'Out of stock for {event.sku}')
  ```

## Handler DI using Classes
- **[DO]**
  ```python
  class AllocateHandler:
      def __init__(self, uow: unit_of_work.AbstractUnitOfWork):
          self.uow = uow

      def __call__(self, cmd: commands.Allocate):
          with self.uow:
              # handler logic
  ```
- **[DON'T]**
  ```python
  class AllocateHandler:
      def __call__(self, cmd: commands.Allocate):
          self.uow = unit_of_work.SqlAlchemyUnitOfWork() # HARDCODED INITIALIZATION
          with self.uow:
              # handler logic
  ```

## Bootstrapper Implementation
- **[DO]**
  ```python
  def bootstrap(
      start_orm: bool = True,
      uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
      send_mail: Callable = email.send,
  ) -> messagebus.MessageBus:
      if start_orm:
          orm.start_mappers()
      
      dependencies = {'uow': uow, 'send_mail': send_mail}
      
      injected_event_handlers = {
          events.OutOfStock: [lambda e: handlers.send_out_of_stock_notification(e, send_mail)]
      }
      
      return messagebus.MessageBus(
          uow=uow,
          event_handlers=injected_event_handlers,
          command_handlers={}
      )
  ```
- **[DON'T]**
  Avoid scattering setup logic across entrypoints, and do not statically bind handlers to the message bus at the module level without allowing runtime injection.

## Testing External Dependencies
- **[DO]**
  ```python
  def test_sends_email_on_out_of_stock_error():
      fake_notifs = FakeNotifications()
      bus = bootstrap.bootstrap(
          start_orm=False,
          uow=FakeUnitOfWork(),
          notifications=fake_notifs,
          publish=lambda *args: None,
      )
      bus.handle(commands.Allocate("o1", "POPULAR-CURTAINS", 10))
      assert fake_notifs.sent['stock@example.com'] == ["Out of stock for POPULAR-CURTAINS"]
  ```
- **[DON'T]**
  ```python
  def test_sends_email_on_out_of_stock_error():
      with mock.patch("allocation.adapters.email.send") as mock_send_mail:
          # Test logic triggering the handler
          mock_send_mail.assert_called_once_with(...)
  ```

## Entrypoint Execution
- **[DO]**
  ```python
  bus = bootstrap.bootstrap()

  @app.route("/allocate", methods=['POST'])
  def allocate_endpoint():
      cmd = commands.Allocate(request.json['orderid'], request.json['sku'], request.json['qty'])
      bus.handle(cmd)
      return 'OK', 202
  ```
- **[DON'T]**
  ```python
  @app.route("/allocate", methods=['POST'])
  def allocate_endpoint():
      uow = unit_of_work.SqlAlchemyUnitOfWork() # DO NOT INSTANTIATE DEPENDENCIES IN ROUTE
      cmd = commands.Allocate(request.json['orderid'], request.json['sku'], request.json['qty'])
      messagebus.handle(cmd, uow)
      return 'OK', 202
  ```