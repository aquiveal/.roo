# @Domain
Trigger these rules when refactoring Python applications to use Dependency Injection (DI), when replacing `mock.patch` in test suites with explicit fakes, when implementing a Composition Root (bootstrap script) for application initialization, or when decoupling service-layer command/event handlers from infrastructure details.

# @Vocabulary
- **Dependency Injection (DI)**: The practice of passing dependencies (e.g., database sessions, email clients) into a function or class rather than importing and instantiating them internally.
- **Implicit Dependency**: A dependency hardcoded into a module via an `import` statement and used directly within the code.
- **Explicit Dependency**: A dependency declared strictly as a function argument or class initialization parameter.
- **Composition Root / Bootstrap Script**: A centralized location (`bootstrap.py`) where the application's components and their dependencies are wired together before runtime.
- **Monkeypatching / mock.patch**: The dynamic replacement of attributes/functions at runtime, typically used in tests for implicit dependencies. Strongly discouraged.
- **Closure**: A dynamically defined function (e.g., `lambda` or nested `def`) that captures variables from its enclosing scope. Used for manual DI.
- **Late Binding**: Python's behavior in closures where captured variables are evaluated at call time, which can cause bugs if the captured dependencies are mutable.
- **Partial Function**: A function created via `functools.partial` that has some of its arguments pre-filled (bound). Used as a safe alternative to closures for manual DI.
- **Adapter**: A concrete or fake implementation of an infrastructural dependency.
- **Abstract Base Class (ABC) / Port**: The abstract interface defining the contract for a complex dependency.

# @Objectives
- Eradicate the use of `mock.patch` and monkeypatching in test suites by converting implicit dependencies into explicit dependencies.
- Completely decouple the service layer and command/event handlers from infrastructure details.
- Centralize all application initialization, ORM mapping, and dependency wiring into a single `bootstrap.py` script.
- Transform the application from relying on statically defined, globally imported states (like a global message bus) to instantiating configured objects at runtime.
- Standardize the creation of infrastructural adapters by defining abstract interfaces, concrete implementations, and fake implementations for testing.

# @Guidelines

## Dependency Management & Anti-Patterns
- The AI MUST NOT use `mock.patch` or monkeypatching for testing service-layer logic. 
- The AI MUST NOT use implicit dependencies (e.g., importing a module and calling its functions directly inside a handler).
- The AI MUST declare all infrastructural requirements (e.g., `uow`, `send_mail`, `publish`) explicitly as arguments in handler functions or inside the `__init__` method of handler classes.
- The AI MUST treat explicit dependency injection as a realization of the Dependency Inversion Principle.

## Manual Dependency Injection Strategies
- The AI MUST implement "manual" DI using one of three approved strategies:
  1. **Closures**: Using `lambda cmd: handler(cmd, dep)`. The AI MUST be cautious of late-binding issues if dependencies are mutable.
  2. **Partials**: Using `functools.partial(handler, dep=dep)`.
  3. **Classes**: Rewriting handlers as classes taking dependencies in `__init__` and executing logic in `__call__`.
- The AI MUST perform this dependency injection entirely within the `bootstrap.py` script, NOT in the entrypoints (e.g., Flask APIs) or the Message Bus.

## The Bootstrap Script (Composition Root)
- The AI MUST create a `bootstrap.py` module responsible for:
  1. Performing one-time initialization (e.g., `orm.start_mappers()`, logging setup).
  2. Declaring default dependencies for the production environment.
  3. Allowing all dependencies to be overridden via function arguments for testing.
  4. Injecting dependencies into all command and event handlers.
  5. Instantiating and returning a configured `MessageBus` object.
- When defining default dependencies in the `bootstrap()` function signature, the AI MUST use `None` as the default value if the dependency instantiation causes unwanted side effects at import time.
- To inject dependencies, the AI MAY use Python's `inspect.signature(handler).parameters` to dynamically match and inject dependencies by name, OR write out explicit manual mappings.

## Message Bus Instantiation
- The AI MUST refactor the `MessageBus` from a static module with globally defined `HANDLERS` into a stateful class.
- The `MessageBus` class MUST be instantiated with its dependencies (`uow`, `event_handlers`, `command_handlers`) passed into `__init__`.
- The AI MUST explicitly recognize that using `self.queue` within a `MessageBus` instance is NOT thread-safe. If the application is multithreaded and the bus is shared across threads, the AI MUST implement thread-safe queues or ensure the bus is instantiated per-thread/per-request.

## Adapter Construction Process
- For simple dependencies (e.g., an email sender, a redis publisher), the AI MAY define the dependency as a `Callable`.
- For complex dependencies (e.g., S3 clients, Key/Value stores), the AI MUST follow the complete adapter lifecycle:
  1. Define the API using an `abc.ABC` interface.
  2. Implement the "real" concrete adapter.
  3. Build a "fake" adapter for unit, handler, and service-layer tests.
  4. Build an integration test to verify the "real" adapter against a local dockerized version of the external service.

# @Workflow
When tasked with refactoring a codebase to use Dependency Injection:
1. **Analyze and Extract**: Scan all command and event handlers for implicit `import` dependencies used to trigger side effects. Remove the imports and add the dependencies as arguments to the handler signatures.
2. **Update the Message Bus**: Refactor the Message Bus into a class that accepts its handlers via `__init__` and accesses them via `self`. Remove static handler dictionaries.
3. **Build the Bootstrapper**: Create `bootstrap.py`. Define a `bootstrap()` function that accepts overrides for all dependencies. Inside, map the dependencies to the handlers (via `inspect` or manual closures), instantiate the `MessageBus` with these injected handlers, and return the bus.
4. **Refactor Entrypoints**: Update API handlers (e.g., Flask views) and CLI scripts to remove manual UoW/infrastructure instantiation. Instead, call `bus = bootstrap.bootstrap()` and route commands through `bus.handle(cmd)`.
5. **Refactor Tests**: Remove all instances of `mock.patch`. Update test setup to invoke `bootstrap.bootstrap()` passing fake implementations (e.g., `FakeUnitOfWork()`, `send_mail=lambda *args: None`) as arguments.
6. **Formalize Complex Adapters**: If a dependency has multiple methods, define an ABC, implement a Concrete class, implement a Fake class, and update `bootstrap.py` to use the Concrete class as the default.

# @Examples (Do's and Don'ts)

## Dependency Injection in Handlers
[DON'T] Use implicit imports and hardcoded infrastructure calls:
```python
from allocation.adapters import email

def send_out_of_stock_notification(event: events.OutOfStock):
    # Implicit dependency tying the domain to infrastructural details
    email.send('stock@made.com', f'Out of stock for {event.sku}')
```

[DO] Use explicit dependency injection:
```python
from typing import Callable

def send_out_of_stock_notification(
    event: events.OutOfStock, 
    send_mail: Callable,
):
    # Explicit dependency, easily swappable in tests
    send_mail('stock@made.com', f'Out of stock for {event.sku}')
```

## Testing Interactions
[DON'T] Use `mock.patch` to intercept implicit dependencies:
```python
from unittest import mock

def test_sends_email_on_out_of_stock_error():
    with mock.patch("allocation.adapters.email.send") as mock_send_mail:
        # Run test logic...
        mock_send_mail.assert_called_with(...)
```

[DO] Use fakes injected via the bootstrap script:
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
    assert fake_notifs.sent['stock@made.com'] == ["Out of stock for POPULAR-CURTAINS"]
```

## The Message Bus
[DON'T] Define the Message Bus as a static module:
```python
# messagebus.py
EVENT_HANDLERS = {
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}

def handle(message):
    # Relies on global state and manual UoW injection inside the handler
    ...
```

[DO] Define the Message Bus as a class injected with prepared handlers:
```python
# messagebus.py
class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        self.queue = [message] # Note: Not thread-safe for shared bus instances
        while self.queue:
            message = self.queue.pop(0)
            # handle logic...
```

## Bootstrapper Configuration
[DON'T] Perform DI and configuration directly in the API endpoints:
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    cmd = commands.Allocate(...)
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    # Missing explicit injection for emails/publishers
    messagebus.handle(cmd, uow)
```

[DO] Use a composition root to bootstrap the bus and route the command:
```python
# bootstrap.py
def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = None,
    notifications: AbstractNotifications = None,
) -> messagebus.MessageBus:
    if start_orm:
        orm.start_mappers()
    
    # Safe defaults to avoid import-time side effects
    if uow is None:
        uow = unit_of_work.SqlAlchemyUnitOfWork()
    if notifications is None:
        notifications = EmailNotifications()

    dependencies = {'uow': uow, 'notifications': notifications}
    
    # Injection logic (e.g., manual lambdas, functools.partial, or inspect)
    injected_event_handlers = {
        events.OutOfStock: [lambda e: handlers.send_out_of_stock_notification(e, notifications)]
    }
    
    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers={}
    )

# flask_app.py
bus = bootstrap.bootstrap()

@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    cmd = commands.Allocate(...)
    bus.handle(cmd)
```