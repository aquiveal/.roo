# @Domain
Trigger these rules when creating, refactoring, or reviewing code that represents core business logic, domain models, business processes, or domain-layer unit tests. This includes defining data structures for business concepts, writing business rules, or implementing calculations that do not require external I/O (e.g., no databases, APIs, or web frameworks).

# @Vocabulary
- **Domain**: The specific problem you are trying to solve or the set of activities that business processes support.
- **Model**: A map of a process or phenomenon that captures a useful property; the mental map business owners have of their business.
- **Ubiquitous Language**: The terminology and business jargon used by business stakeholders. This vocabulary must be used directly in the code to represent a distilled understanding of the domain model.
- **Value Object**: Any domain object that is uniquely identified strictly by the data it holds. It has no long-lived identity and is usually implemented as an immutable data structure.
- **Entity**: A domain object that has a long-lived, persistent identity. It remains recognizably the same thing even if its data/attributes change over time.
- **Domain Service**: An operation or business process that does not have a natural home in an Entity or Value Object. Modeled as a standalone function.
- **Domain Exception**: An exception used to express a specific business concept, edge case, or rule violation, named using the Ubiquitous Language.

# @Objectives
- Build a business layer consisting of a Domain Model that is completely free of external dependencies, infrastructure concerns, or web frameworks.
- Encode the hard-won experience of business experts into the software by strictly mirroring the business's Ubiquitous Language in class names, variable names, and method names.
- Ensure the Domain Model is highly compatible with Test-Driven Development (TDD) by making it easy to instantiate and test in memory without any external state setup.
- Distinguish strictly between objects defined by their identity (Entities) and objects defined by their attributes (Value Objects).
- Leverage Python's multi-paradigm nature and idiomatic features (magic methods, dataclasses, standalone functions) to make the domain model expressive and pythonic.

# @Guidelines
- **No External Dependencies**: The domain model must have zero dependencies on external infrastructure. Do not import ORMs, web frameworks, filesystem libraries, or network libraries into domain model files.
- **Ubiquitous Language in Code**: Classes, variables, and methods MUST be named using the exact jargon used by business domain experts.
- **Entities vs. Value Objects**: You MUST explicitly choose whether a domain concept is an Entity or a Value Object.
- **Value Object Implementation**: 
  - Use `@dataclass(frozen=True)` or `namedtuple` to implement Value Objects.
  - They MUST be immutable. 
  - They MUST be evaluated for equality based on all their values (value equality). 
  - You MAY implement complex behavior or mathematical operators (e.g., `__add__`, `__sub__`) on Value Objects.
- **Entity Implementation**:
  - Entities MUST have a unique, persistent identifier (e.g., a reference, ID, or SKU).
  - You MUST implement the `__eq__` magic method so that Entity equality is based *only* on their unique identifier.
  - You MUST implement the `__hash__` magic method based *only* on the unique identifier. Do not modify `__hash__` without also modifying `__eq__`.
- **Domain Services**: 
  - If a business action or "verb" does not naturally belong to a specific Entity or Value Object, you MUST implement it as a standalone function. 
  - DO NOT create unnecessary objects like `FooManager`, `BarBuilder`, or `BazFactory`.
- **Pythonic Magic Methods**: You MUST use Python's magic methods (e.g., `__gt__`, `__eq__`, `__hash__`) to express domain semantics, allowing the domain models to be used with standard Python idioms like `sorted()`.
- **Domain Exceptions**: You MUST create custom Exception classes to express business rule violations or domain concepts (e.g., `OutOfStock`). DO NOT rely solely on generic Python exceptions (like `ValueError`) for core business logic.
- **Unit Testing**: 
  - Write domain model unit tests using the business jargon.
  - Test names must describe the exact business behavior or rule being verified.
  - Test edge cases and business constraints directly against the domain model objects in memory.
- **Type Hints**: You MAY use type hints to clarify expected arguments in the domain model, but weigh them against readability.

# @Workflow
1. **Explore the Domain**: Analyze the business requirements to identify the Ubiquitous Language, including the nouns (objects) and verbs (actions/rules).
2. **Write Domain Tests**: Write unit tests first. Name the tests and variables using the exact business jargon. Set up the test state in-memory.
3. **Define Value Objects**: Identify concepts defined only by their data. Implement them using `@dataclass(frozen=True)`.
4. **Define Entities**: Identify concepts with a persistent identity. Implement them as standard classes, strictly defining their `__eq__` and `__hash__` methods based on their unique identifier.
5. **Implement Domain Rules**: Add business logic methods to the Entities or Value Objects to satisfy the unit tests.
6. **Extract Domain Services**: If an operation involves multiple aggregates or doesn't fit into a single object, implement it as a standalone function.
7. **Apply Magic Methods**: Refactor the model to use Python magic methods where they clarify the domain semantics (e.g., sorting, comparing).
8. **Define Domain Exceptions**: Identify failure states in the business rules and define custom exception classes for them.

# @Examples (Do's and Don'ts)

## Value Objects
**[DO]** Use frozen dataclasses for concepts without long-lived identity:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int
```

**[DON'T]** Use mutable classes for Value Objects, or implement custom equality based on IDs when the concept is purely data:
```python
class OrderLine:
    def __init__(self, orderid, sku, qty):
        self.orderid = orderid
        self.sku = sku
        self.qty = qty
        self.id = generate_id() # Anti-pattern: Value objects don't have unique IDs
```

## Entities
**[DO]** Define identity equality and hashes based strictly on the unique reference:
```python
class Batch:
    def __init__(self, ref: str, sku: str, qty: int):
        self.reference = ref
        self.sku = sku
        self._purchased_quantity = qty

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)
```

**[DON'T]** Allow default object equality (memory address) or value equality for Entities:
```python
@dataclass
class Batch:
    reference: str
    sku: str
    qty: int
    # Anti-pattern: Dataclass default __eq__ will compare 'qty', 
    # meaning the Batch "changes identity" if the quantity changes.
```

## Domain Services
**[DO]** Use standalone functions for operations that don't belong to a specific object:
```python
def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
```

**[DON'T]** Create Manager classes for verbs:
```python
class AllocationManager:
    def allocate_line_to_batches(self, line, batches):
        # Anti-pattern: Unnecessary class wrapper for a function
        pass
```

## Domain Exceptions
**[DO]** Express domain concepts as custom exceptions:
```python
class OutOfStock(Exception):
    pass

# Usage inside a domain service/model
raise OutOfStock(f'Out of stock for sku {line.sku}')
```

**[DON'T]** Use generic exceptions for business logic:
```python
# Anti-pattern: Hides the domain concept
raise ValueError(f'Cannot allocate. Out of stock for sku {line.sku}')
```

## Pythonic Magic Methods
**[DO]** Implement standard magic methods to express domain sorting or comparison:
```python
class Batch:
    # ...
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta
```