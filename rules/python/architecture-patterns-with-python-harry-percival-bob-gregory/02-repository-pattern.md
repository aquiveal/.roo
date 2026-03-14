# @Domain
Trigger these rules when tasked with implementing data persistence, configuring Object-Relational Mappers (ORMs), building data access layers, connecting domain models to databases, or writing tests that require database interactions.

# @Vocabulary
- **Repository Pattern**: A simplifying abstraction over persistent storage that hides data access details and provides the illusion that all data is in an in-memory collection.
- **Dependency Inversion Principle (DIP)**: The principle that high-level modules (domain models) should not depend on low-level modules (infrastructure/ORMs). Both should depend on abstractions.
- **Persistence Ignorance**: The concept that the domain model does not know anything about how its data is loaded or persisted.
- **Classical Mapping**: An explicit ORM mapping approach (specifically in SQLAlchemy) where database tables are defined separately from the domain model classes, and a mapper binds them together.
- **Port**: The interface between the application and the abstracted external dependency (e.g., `AbstractRepository`).
- **Adapter**: The concrete implementation behind the interface (e.g., `SqlAlchemyRepository`, `FakeRepository`).
- **FakeRepository**: A test double implementation of the repository that uses a simple in-memory data structure (like a `set`) to allow fast, I/O-free unit testing.

# @Objectives
- The AI MUST decouple the core domain model from infrastructural and database concerns.
- The AI MUST ensure the domain model remains "pure" and completely ignorant of the ORM or database technology.
- The AI MUST encapsulate all database access within Repository classes.
- The AI MUST provide a simple, in-memory illusion for data access to the rest of the application.
- The AI MUST facilitate fast unit testing by ensuring a fake, in-memory repository can be seamlessly swapped for the real database repository.

# @Guidelines
- **Decouple ORM and Domain**: The AI MUST NEVER inherit domain models from ORM base classes (e.g., SQLAlchemy's `declarative_base` or Django's `models.Model`).
- **Invert the Dependency**: The ORM configuration MUST import the domain model, NOT the other way around. 
- **Use Classical Mapping**: When using SQLAlchemy, the AI MUST define schema using explicit `Table` and `MetaData` objects, and bind them to the pure domain classes using `sqlalchemy.orm.mapper`.
- **Define an Abstract Port**: The AI MUST define an `AbstractRepository` using `abc.ABC` (or PEP 544 Protocols) to formalize the data access interface.
- **Use Collection-Like Methods**: The Repository interface MUST use simple collection-style methods: `add()` to put a new item in, and `get()` to retrieve an item. Do not use database-specific terminology like `insert`, `select`, or `update` in the abstract interface.
- **Keep Commit Outside the Repository**: The AI MUST NOT implement `.save()` or `.commit()` methods within the Repository itself. Database commits MUST be the responsibility of the caller (to be handled by the Unit of Work pattern).
- **Implement Fakes for Testing**: The AI MUST build a `FakeRepository` using standard Python collections (e.g., a `set()`) to be used in unit tests.
- **Write Integration Tests for Real Repositories**: The AI MUST test the concrete database repository using integration tests that execute raw SQL to verify the repository correctly saves and retrieves the complex object graph.
- **Avoid Over-Abstraction**: If a feature is a simple CRUD wrapper with no complex domain rules, the AI MUST explicitly evaluate if the Repository pattern is necessary, as it adds maintenance overhead and indirection.

# @Workflow
1. **Define the Domain Model**: Write the domain classes as pure Python objects (`@dataclass` or standard classes) with absolutely no ORM or database imports.
2. **Define the Database Schema**: In a separate infrastructure file (e.g., `orm.py`), define the database tables using your ORM's schema definition tools (e.g., SQLAlchemy `MetaData` and `Table`).
3. **Map the Schema to the Model**: Create a `start_mappers()` function that explicitly binds the database tables to the pure Python domain classes.
4. **Create the Abstract Repository**: Define an `AbstractRepository` base class with `@abc.abstractmethod` for `add(self, entity)` and `get(self, reference)`.
5. **Implement the Concrete Repository**: Create the real repository (e.g., `SqlAlchemyRepository`) that inherits from the abstract base and implements `add` and `get` using the ORM's session logic.
6. **Implement the Fake Repository**: Create a `FakeRepository` that inherits from the abstract base and implements `add` and `get` using a Python `set` for use in unit tests.
7. **Write Integration Tests**: Write tests for the concrete repository that insert data using raw SQL, use the repository to retrieve it, and assert the domain model is correctly populated. Conversely, use the repository to save a model, and use raw SQL to verify the database state.

# @Examples (Do's and Don'ts)

## ORM Dependency Management
**[DO]** Define the schema explicitly and map it to a pure Python domain model (Classical Mapping).
```python
# model.py
class OrderLine:
    def __init__(self, orderid, sku, qty):
        self.orderid = orderid
        self.sku = sku
        self.qty = qty

# orm.py
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import mapper
import model

metadata = MetaData()

order_lines = Table(
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('orderid', String(255)),
)

def start_mappers():
    mapper(model.OrderLine, order_lines)
```

**[DON'T]** Couple the domain model directly to the ORM (Declarative Mapping).
```python
# DON'T do this: Model depends on ORM
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrderLine(Base):
    __tablename__ = 'order_lines'
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    qty = Column(Integer)
    orderid = Column(String(250))
```

## Abstract Repository Definition
**[DO]** Define a simple, collection-like abstract base class without commit mechanisms.
```python
import abc
import model

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError
```

**[DON'T]** Include database-specific jargon or commit commands in the repository interface.
```python
# DON'T do this
class BadRepository:
    def insert_record(self, batch): # DB terminology
        self.session.add(batch)
        self.session.commit() # Commits belong outside the repository
```

## Fake Repository Implementation
**[DO]** Implement a fake repository using a simple Python `set` to simulate in-memory storage.
```python
class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
```

## Integration Testing the Real Repository
**[DO]** Use raw SQL to verify the repository correctly interacts with the database.
```python
def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit() # Caller handles commit

    rows = list(session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    ))
    assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]
```