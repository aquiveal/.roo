@Domain
This rule file applies when the AI is tasked with implementing, refactoring, or reviewing object-oriented design patterns in Python, specifically targeting codebases that use classic object-oriented hierarchies (such as Strategy, Command, Template Method, or Visitor patterns), single-method interfaces, or when the user requests to make OOP code more "Pythonic" by leveraging first-class functions.

@Vocabulary
- **First-Class Object**: A program entity that can be created at runtime, assigned to variables, passed as arguments, and returned as results. In Python, functions are first-class objects.
- **Strategy Pattern**: A design pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable.
- **Context**: In the Strategy pattern, the component that delegates computation to interchangeable strategy components.
- **Concrete Strategy**: A specific implementation of an algorithm defined by the Strategy interface.
- **Flyweight**: A shared object that can be used in multiple contexts simultaneously to save memory. In Python, plain functions inherently act as flyweights.
- **Registration Decorator**: A decorator function whose sole purpose is to add the decorated function to a central registry (e.g., a list or dictionary) at import time.
- **Command Pattern**: A design pattern that decouples an object that invokes an operation (Invoker) from the provider object that implements it (Receiver).
- **MacroCommand**: A command pattern variant that stores a sequence of commands and executes them in order.
- **Single-Method Interface**: A class or abstract base class (ABC) that dictates exactly one method (e.g., `execute`, `run`, `discount`).

@Objectives
- Replace verbose, rigid class hierarchies from classic object-oriented design patterns with concise, readable function-oriented code.
- Treat functions as first-class objects to eliminate stateless, single-method classes.
- Decouple components efficiently by passing plain callables (callbacks) rather than instantiating dedicated command or strategy objects.
- Ensure extensibility of functional patterns by utilizing dynamic aggregation techniques like registration decorators or module introspection.

@Guidelines
- **Refactoring Stateless Single-Method Classes**: When the AI encounters a class that implements a single method and holds no internal state (common in Concrete Strategies and Commands), the AI MUST refactor the class into a plain function.
- **Context Type Hinting**: When a class accepts a function-oriented strategy or command, the AI MUST type-hint the parameter using `collections.abc.Callable` or `typing.Callable` with the appropriate signature, rather than using a custom abstract base class type.
- **Invoking Callable Attributes**: When a context class holds a strategy as an instance attribute (e.g., `self.promotion`), the AI MUST invoke it directly via `self.promotion(self)` rather than attempting to call a named method on it (e.g., `self.promotion.discount(self)`).
- **Eliminating Flyweights**: The AI MUST NOT implement the Flyweight pattern to share stateless strategy objects. Instead, the AI MUST use plain functions, which inherently serve as shared objects across multiple contexts.
- **Dynamic Strategy Discovery (Module Introspection)**: To avoid hardcoded lists of strategies, the AI MAY use `globals().items()` to collect functions matching a specific naming convention (e.g., `name.endswith('_promo')`). Alternatively, if strategies are segregated into their own module, the AI MUST use `inspect.getmembers(module, inspect.isfunction)` to aggregate them dynamically.
- **Dynamic Strategy Discovery (Registration Decorator)**: The AI MUST strongly prefer using a registration decorator to aggregate strategies. The AI MUST create an empty list (e.g., `promos = []`), define a decorator that appends the function to the list and returns the function unchanged, and apply this decorator to all relevant strategy functions.
- **Refactoring the Command Pattern**: The AI MUST decouple Invokers from Receivers by passing plain functions (callbacks) instead of Command instances. The AI MUST NOT create an Abstract `Command` class with an `execute` method unless specifically required by an external framework.
- **Implementing MacroCommands**: When a sequence of commands must be executed, the AI MUST implement `MacroCommand` as a class equipped with an `__init__` method that accepts an iterable of callables, and a `__call__` method that iterates over and invokes each callable.
- **Stateful Commands**: If a command requires internal state (e.g., to support an "undo" operation), the AI MUST use a callable class (implementing `__call__`) or a closure, rather than building a classic Command inheritance hierarchy.

@Workflow
1. **Analyze Interface Structures**: Identify any Abstract Base Classes or interfaces that define a single method (e.g., `discount`, `execute`, `do_it`).
2. **Statefulness Check**: Inspect the concrete implementations of these single-method interfaces. If they do not utilize `__init__` to store internal state, flag them for functional refactoring.
3. **Class-to-Function Conversion**: Extract the logic inside the single method of the concrete class and convert it into a standalone module-level function. 
4. **Context Adaptation**: Update the Context or Invoker class to accept a `Callable` instead of an object instance. Remove any abstract base class formerly used to type-hint the strategy/command.
5. **Call-Site Update**: Modify the execution call inside the Context to invoke the callable directly (e.g., `self.strategy()` instead of `self.strategy.execute()`).
6. **Strategy Aggregation**: If the program iterates over multiple strategies to find a best fit (a "metastrategy"), avoid hardcoding the list of functions. Implement a registration decorator (e.g., `@promotion`) to dynamically append functions to a registry list at import time.
7. **Execution**: Ensure that any instances previously creating strategy objects (e.g., `Order(Customer, Cart, FidelityPromo())`) are updated to pass the function directly (`Order(Customer, Cart, fidelity_promo)`).

@Examples (Do's and Don'ts)

**Strategy Pattern Refactoring**

[DON'T] Use single-method classes to define algorithms.
```python
from abc import ABC, abstractmethod
from decimal import Decimal

class Promotion(ABC):
    @abstractmethod
    def discount(self, order) -> Decimal: ...

class FidelityPromo(Promotion):
    def discount(self, order) -> Decimal:
        return order.total() * Decimal('0.05') if order.customer.fidelity >= 1000 else Decimal(0)

# Instantiation
order = Order(joe, cart, FidelityPromo())
```

[DO] Use plain functions for stateless strategies.
```python
from decimal import Decimal
from typing import Callable

def fidelity_promo(order) -> Decimal:
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * Decimal('0.05') if order.customer.fidelity >= 1000 else Decimal(0)

class Order:
    def __init__(self, customer, cart, promotion: Callable[['Order'], Decimal] = None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        
    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self) # Invoked directly as a callable
        return self.total() - discount

# Instantiation
order = Order(joe, cart, fidelity_promo)
```

**Strategy Aggregation (Metastrategy)**

[DON'T] Hardcode a list of functions that must be manually updated.
```python
promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order) -> Decimal:
    return max(promo(order) for promo in promos)
```

[DO] Use a registration decorator to dynamically collect strategies.
```python
Promotion = Callable[['Order'], Decimal]
promos: list[Promotion] = []

def promotion(promo: Promotion) -> Promotion:
    promos.append(promo)
    return promo

@promotion
def fidelity_promo(order: Order) -> Decimal:
    return order.total() * Decimal('0.05') if order.customer.fidelity >= 1000 else Decimal(0)

@promotion
def bulk_item_promo(order: Order) -> Decimal:
    # logic here...

def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)
```

**Command Pattern Refactoring**

[DON'T] Create Command interfaces and single-method concrete classes.
```python
class Command(ABC):
    @abstractmethod
    def execute(self): ...

class PasteCommand(Command):
    def __init__(self, document):
        self.document = document
    def execute(self):
        self.document.paste()
```

[DO] Pass the receiver's method directly as a callable callback.
```python
# Instead of instantiating PasteCommand(my_doc), simply pass the bound method:
invoker.set_command(my_doc.paste)
```

**MacroCommand Implementation**

[DON'T] Build an explicit `execute` method that iterates through a hardcoded list of command objects.
```python
class MacroCommand:
    def __init__(self, commands):
        self.commands = commands
    def execute(self):
        for command in self.commands:
            command.execute()
```

[DO] Use `__call__` so the MacroCommand object acts exactly like a regular function.
```python
class MacroCommand:
    """A command that executes a list of callables"""
    def __init__(self, commands):
        self.commands = list(commands)
        
    def __call__(self):
        for command in self.commands:
            command()
```