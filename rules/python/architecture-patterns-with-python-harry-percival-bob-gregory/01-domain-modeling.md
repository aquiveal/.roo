# @Domain
Activation conditions: Trigger these rules when generating, refactoring, or testing core business logic, domain models, domain objects (Entities or Value Objects), or business processes. This applies whenever the user requests modeling a business problem, establishing foundational data structures independent of infrastructure (such as ORMs, APIs, or databases), or writing unit tests that enforce business rules and invariants.

# @Vocabulary
- **Domain**: The specific business problem or area of activity the software is attempting to solve or automate (e.g., purchasing, procurement, logistics).
- **Domain Model**: The mental map or conceptual model of the business process, translated into pure code. It is the part of the code closest to the business and the most likely to change.
- **Ubiquitous Language (Business Jargon)**: The specific terminology used by business stakeholders. This vocabulary must be explicitly mirrored in class names, variables, methods, and tests.
- **Value Object**: A domain object uniquely identified by the data it holds rather than a long-lived identity. Two value objects with the exact same data are considered completely equal. They must be immutable.
- **Entity**: A domain object that possesses a persistent, long-lived identity. Its attributes may change over time, but it remains recognizably the same object. It requires identity equality.
- **Domain Service**: A standalone function (a "verb") that models a business process or action that does not naturally belong inside a single Entity or Value Object.
- **Domain Exception**: Custom exception classes named using the Ubiquitous Language to explicitly express domain concepts and business rule violations (e.g., `OutOfStock`).

# @Objectives
- Build a rich, pure, object-oriented domain model that accurately captures business rules and constraints without any reliance on infrastructure (persistence ignorance).
- Guarantee that the Domain Model operates completely independently of databases, ORMs, web frameworks, or external APIs.
- Express the business's Ubiquitous Language directly in the code so non-technical stakeholders could theoretically read the unit tests and understand the system's behavior.
- Use explicit types, dataclasses, and Python magic methods to create expressive, idiomatic, and highly testable business logic.

# @Guidelines
- **Infrastructure Independence**: The AI MUST NOT import or depend on ORMs (e.g., SQLAlchemy, Django `models`), web frameworks (e.g., Flask), or external I/O libraries within the domain model. The model must consist of plain Python objects (`dataclasses`, `NamedTuple`, standard types).
- **Ubiquitous Language Enforcement**: The AI MUST name classes, methods, and variables using the exact business jargon provided in the prompt or requirements. 
- **Value Object Implementation**: 
  - The AI MUST implement Value Objects for concepts that have data but no identity.
  - Value Objects MUST be immutable. Use `@dataclass(frozen=True)` or `NamedTuple`.
  - Value Objects MUST rely on value equality (provided out-of-the-box by frozen dataclasses).
  - The AI SHOULD implement mathematical or logical magic methods (e.g., `__add__`, `__sub__`) on Value Objects if operations on their values are required by the domain.
- **Entity Implementation**:
  - The AI MUST implement Entities for domain concepts that have a long-lived identity.
  - Entities MUST implement custom identity equality via the `__eq__` magic method, comparing ONLY the unique identifier/reference field (e.g., `self.reference == other.reference`).
  - The AI MUST protect `__eq__` by first checking `if not isinstance(other, ClassName): return False`.
  - Entities SHOULD explicitly set `__hash__ = None` to make them unhashable by default. If hashing is strictly required (e.g., for `set` operations), the AI MUST implement `__hash__` based strictly on the unique, read-only identity attribute (e.g., `return hash(self.reference)`).
  - The AI MUST NEVER modify `__hash__` without also modifying `__eq__`.
- **Domain Service Functions (Verbs)**:
  - The AI MUST model cross-object business processes as pure Python functions rather than forcing them into objects.
  - The AI MUST NOT create artificial manager classes (e.g., `FooManager`, `BarBuilder`, `BazFactory`). Instead, use expressive functions (e.g., `manage_foo()`, `build_bar()`).
- **Domain Exceptions**:
  - The AI MUST define custom Exception classes for business rule violations.
  - Do NOT use generic exceptions (like `ValueError` or `Exception`) to express domain concepts.
- **Idiomatic Magic Methods**:
  - The AI SHOULD implement standard Python magic methods (like `__gt__` for sorting) on domain models so they can be interacted with using idiomatic Python (e.g., `sorted(list_of_entities)`).
- **Type Hints**:
  - The AI MUST use Python type hints (`typing.Optional`, `typing.List`, `typing.Set`) in domain models to clarify expected arguments and document the domain API.
- **Unit Testing**:
  - Tests MUST be written *first* (TDD) or alongside the domain model.
  - Test names MUST describe the business behavior clearly (e.g., `test_allocating_to_a_batch_reduces_the_available_quantity`).
  - Tests MUST NOT require dependencies, database connections, or complex setup (no fixtures for DB sessions).

# @Workflow
1. **Analyze the Domain Language**: Extract nouns (potential Entities/Value Objects), verbs (potential Domain Services), and rules/invariants (potential Domain Exceptions) from the user's requirements.
2. **Draft Domain Tests**: Write fast, dependency-free unit tests utilizing the exact business language. Instantiate models and test their behaviors and assertions.
3. **Define Value Objects**: Create `@dataclass(frozen=True)` classes for items identified solely by their data.
4. **Define Entities**: Create standard classes or mutable `@dataclass` classes for items with a persistent identity. Implement `__eq__` and `__hash__` targeting the unique identifier.
5. **Implement Magic Methods**: Add methods like `__gt__`, `__add__`, etc., to support idiomatic Python operations dictated by the tests.
6. **Define Domain Exceptions**: Create empty classes inheriting from `Exception` that represent business failures.
7. **Draft Domain Services**: Implement standalone functions that coordinate behaviors between multiple Domain Objects and raise Domain Exceptions when business rules are violated.

# @Examples (Do's and Don'ts)

**Value Objects**
- [DO]:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int
```
- [DON'T] (Do not use mutable classes for concepts without a unique identity):
```python
class OrderLine:
    def __init__(self, orderid, sku, qty):
        self.orderid = orderid
        self.sku = sku
        self.qty = qty
```

**Entities and Identity Equality**
- [DO]:
```python
class Batch:
    def __init__(self, ref: str, sku: str, qty: int):
        self.reference = ref
        self.sku = sku
        self.available_quantity = qty

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)
```
- [DON'T] (Do not inherit from ORMs in the domain layer, and do not rely on default instance equality for Entities):
```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Batch(Base): # ORM dependency in Domain Model is strictly forbidden!
    __tablename__ = 'batches'
    reference = Column(String, primary_key=True)
```

**Domain Services**
- [DO]:
```python
def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
```
- [DON'T] (Do not use Manager classes for what should be simple functions):
```python
class AllocationManager:
    def allocate_line_to_batches(self, line, batches):
        # Unnecessary class wrapper
        pass
```

**Domain Exceptions**
- [DO]:
```python
class OutOfStock(Exception):
    pass
# Raised when a business rule constraint is hit
```
- [DON'T]:
```python
# Do not raise generic exceptions for business rules
raise ValueError("Out of stock")
```

**Unit Testing**
- [DO]:
```python
def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False
```
- [DON'T] (Do not include infrastructure in domain tests):
```python
def test_cannot_allocate_if_available_smaller_than_required(db_session):
    # Domain tests must not require a database session
    pass
```