# @Domain
These rules MUST trigger when the AI is asked to design system architecture, add new features to existing codebases, refactor highly coupled code, implement notification/event systems, design plug-in frameworks, or resolve issues related to "spaghetti code", complex dependency chains, or repeated code modifications across multiple files.

# @Vocabulary
- **Extensibility**: The property of systems that allows new functionality to be added without modifying existing parts of the system.
- **Shotgun Surgery (Anti-pattern)**: A situation where a single conceptual change requires modifications spread across multiple files or modules.
- **Necessary Complexity**: Complexity intrinsic to the problem domain.
- **Accidental Complexity**: Complexity introduced by poor implementation or architecture.
- **Open-Closed Principle (OCP)**: Code should be open for extension but closed for modification.
- **Physical Dependency**: A static, direct relationship in code, such as imports, class inheritance, or direct function calls.
- **Logical Dependency**: A relationship without direct linkage in code, resolved at runtime (e.g., HTTP requests, message brokers, duck typing).
- **Temporal Dependency**: A dependency linked by time or order of operations (e.g., an object must be configured before it can be used).
- **Fan-in**: The number of external entities depending on a specific module. High fan-in modules should be stable leaf nodes.
- **Fan-out**: The number of external entities a specific module depends upon. High fan-out modules usually contain business logic and can change more frequently.
- **Composability**: Building small components with minimal inter-dependencies and separated business logic that can be mixed and matched.
- **Policy**: Business logic; the "what" the code is trying to achieve.
- **Mechanism**: The implementation details; the "how" the code enacts the policy (e.g., iteration, logging, retrying).
- **Pure Function**: A function whose output is solely derived from inputs, with no side effects.
- **Event-Driven Architecture (EDA)**: Architecture decoupled into Producers and Consumers communicating via transport mechanisms (stimulus and reaction).
- **Message Broker**: A piece of code acting as a transport for data (Pub/Sub) separating publishers and subscribers via topics (e.g., `PyPubSub`).
- **Observer Pattern**: A producer maintains a list of observer callbacks to invoke on events, creating a generic logical dependency instead of a physical one.
- **Reactive Programming**: An architectural style centered on continuous streams of events (observables) and pipable operators (e.g., `RxPY`).
- **Plug-in**: A piece of code loaded dynamically at runtime via extension points.
- **Template Method Pattern**: An algorithm defined as a series of steps where callers supply specific step implementations.
- **Strategy Pattern**: Plugging entire interchangeable algorithms into a predefined context.

# @Objectives
- Empower future maintainers by maximizing code extensibility and composability.
- Decouple producers and consumers using event-driven or plug-in architectures.
- Separate policies (business logic) from mechanisms (implementation details).
- Prevent "shotgun surgery" by designing systems that accept new features via configuration, dependency injection, or new discrete types rather than modifying existing function signatures.
- Make incorrect code usage impossible by enforcing temporal dependencies via the type system.
- Replace heavy Object-Oriented (OO) boilerplate (e.g., canonical Gang of Four patterns) with Pythonic equivalents leveraging `Callable`, data classes, and protocols.

# @Guidelines
- **Extensibility & OCP Enforcement**:
  - When adding parameters to a function causes a ripple effect across the codebase, the AI MUST redesign the system using `Union` types, `Protocol`s, or dictionary-based routing to decouple the caller from the new requirements.
  - The AI MUST consolidate varying requirements (e.g., notification types, notification methods) into discrete data classes rather than expanding function parameter lists.
- **Dependency Management**:
  - **Inverting Dependencies**: The AI MUST invert physical dependencies to protect core domain logic. (e.g., The core system defines what is available; peripheral systems query the core, rather than the core updating peripheral systems).
  - **Temporal Dependencies**: The AI MUST mitigate temporal dependencies (required order of operations) using the type system (e.g., returning a uniquely typed `ConfiguredObject` from the configuration step that is required for the action step), embedding preconditions deeper, or leaving explicit breadcrumb comments.
  - **Over-DRYing**: The AI MUST NOT deduplicate code solely because it looks physically similar if the code blocks have *different reasons to change*. Excessive DRYing creates unwanted physical coupling.
  - **Fan-in/Fan-out**: The AI MUST place code with high fan-in (many dependents) at the bottom of the dependency graph and ensure it rarely changes. High fan-out code (depends on many things) MUST be restricted to business logic/policies.
- **Composability (Policy vs. Mechanism)**:
  - The AI MUST separate mechanism (how) from policy (what). 
  - Mechanisms MUST be extracted into decorators (e.g., retry logic via `backoff`, caching) or higher-order functions (e.g., using `itertools` for sorting/filtering algorithms).
  - Policies MUST be implemented declaratively, utilizing composed mechanisms.
- **Event-Driven Architectures**:
  - For simple, single-process decoupling, the AI MUST implement the Observer Pattern using lists of `Callable` objects rather than defining heavy base classes (`Publisher`/`Subscriber`).
  - To completely sever physical dependencies in single-process systems, the AI MUST use a message broker like `PyPubSub` (`pub.subscribe`, `pub.publish`).
  - For continuous streams of data, the AI MUST implement Reactive Programming using `RxPY` (`rx.pipe`, observables, and chained operations).
  - The AI MUST handle exceptions explicitly in event producers, as typecheckers cannot validate cross-broker boundaries, and failing consumers can crash the producer loop.
- **Pluggable Python (Patterns)**:
  - **Template Method**: Instead of writing base classes that `raise NotImplementedError`, the AI MUST define a `@dataclass` containing `Callable` fields for the steps to be overridden, and pass this configuration to the template function.
  - **Strategy Pattern**: The AI MUST pass a single `Callable` representing the strategy algorithm to the context function.
  - **System-level Plugins**: To build dynamically loaded systems spanning multiple packages, the AI MUST use `stevedore`. Define a `Protocol` for the contract, register plugins via `setup.py` `entry_points`, and load them using `ExtensionManager` or `DriverManager`.

# @Workflow
1. **Analyze Change Scope**: When asked to add a feature, evaluate if the change requires modifying multiple unrelated files (Shotgun Surgery).
2. **Decouple via Types**: If tightly coupled, extract the varying data or logic into discrete types (`@dataclass` or `Protocol`) and create a registry (dictionary or list) mapping types to handlers.
3. **Separate Policy/Mechanism**: Identify if the request mixes business rules with execution logic (e.g., a function that calculates data AND manages `while/try/except` retries). Extract the mechanism into a decorator or a separate iterator function.
4. **Select Architecture**:
   - If adding reactions to a state change: Use the Observer Pattern (list of `Callables`) or `PyPubSub`.
   - If processing continuous data feeds: Set up an `RxPY` pipeline.
   - If creating a framework for future arbitrary algorithms: Implement the Template Method or Strategy pattern using `Callable` parameters.
   - If building a highly decoupled package ecosystem: Use `stevedore` and `Protocol`.
5. **Enforce Safety**: Map out temporal dependencies and enforce them by returning specific types from initialization functions. Add necessary exception handling for logical dependencies.

# @Examples (Do's and Don'ts)

## Extensibility and OCP
- **[DON'T]** Force shotgun surgery by expanding function signatures for unrelated concerns.
```python
# Anti-pattern: Accidental complexity and tight coupling
def declare_special(dish: Dish, start_date: datetime, end_date: datetime, emails: list[str], texts: list[str], send_to_customer: bool):
    # logic ...
```
- **[DO]** Use types and routing dictionaries to keep code open for extension and closed for modification.
```python
# Pattern: Extensible design
@dataclass
class NewSpecial:
    dish: Dish
    start_date: datetime
    end_date: datetime

Notification = Union[NewSpecial, OutOfStock, NewMenuItem]
NotificationMethod = Union[Email, Text, SupplierAPI]

# Registry mapping policies to mechanisms
users_to_notify: dict[type, list[NotificationMethod]] = {
    NewSpecial: [Email("boss@company.org"), Text("555-1234")],
}

def send_notification(notification: Notification):
    users = users_to_notify.get(type(notification), [])
    for method in users:
        notify(method, notification) # Route to specific handlers
```

## Temporal Dependencies
- **[DON'T]** Rely on human memory to enforce order of operations.
```python
# Anti-pattern: Hidden temporal dependency
pizza_maker = PizzaMaker()
pizza_maker.configure_for_mass_production() # Easy to forget
pizza_maker.mass_produce(50)
```
- **[DO]** Use the type system to enforce preconditions.
```python
# Pattern: Type-enforced temporal dependency
pizza_maker = PizzaMaker()
# mass_produce only exists on the object returned by configure
mass_producer: MassProductionPizzaMaker = pizza_maker.configure_for_mass_production()
mass_producer.mass_produce(50) 
```

## Composability (Decorators & Mechanisms)
- **[DON'T]** Mix business policy with retry/execution mechanisms.
```python
# Anti-pattern: Mechanism tangled with Policy
def save_inventory(inventory):
    time_to_sleep = 1
    while True:
        try:
            # Policy
            db.save(inventory)
            break
        except HTTPError:
            # Mechanism
            time.sleep(time_to_sleep)
            time_to_sleep *= 2
```
- **[DO]** Compose pure business logic with mechanism decorators (e.g., `backoff`).
```python
# Pattern: Composable Mechanisms
import backoff

@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_time=60)
def save_inventory(inventory):
    db.save(inventory) # Pure policy
```

## Observer Pattern
- **[DON'T]** Use heavy OOP base classes for simple observer patterns.
```python
# Anti-pattern: Heavy Java-style OOP in Python
class Subscriber:
    def notify(self, data): raise NotImplementedError()

class Publisher:
    def add_subscriber(self, sub: Subscriber): ...
```
- **[DO]** Use lists of `Callable` objects.
```python
# Pattern: Pythonic Observer
def complete_order(order: Order, observers: list[Callable[[Order], None]]):
    package_order(order)
    for observer in observers:
        observer(order)
```

## Template Method Pattern
- **[DON'T]** Rely on subclassing and `NotImplementedError` for algorithms.
```python
# Anti-pattern: Inheritance for Template Method
class PizzaCreator:
    def prepare_ingredients(self): raise NotImplementedError()
    def create(self):
        self.prepare_ingredients()
        self.bake()
```
- **[DO]** Use a data class of `Callable`s to plug steps into an algorithm.
```python
# Pattern: Pluggable Template Method
@dataclass
class PizzaCreationFunctions:
    prepare_ingredients: Callable[[], None]
    add_toppings: Callable[[], None]

def create_pizza(funcs: PizzaCreationFunctions):
    funcs.prepare_ingredients()
    roll_out_dough()
    funcs.add_toppings()
    bake()
```