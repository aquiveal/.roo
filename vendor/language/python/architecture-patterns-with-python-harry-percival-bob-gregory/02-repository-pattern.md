# @Domain
This rule file activates when the AI is engaged in Python backend development tasks involving database access, Object-Relational Mapping (ORM) setup (particularly SQLAlchemy), unit and integration testing, and architectural refactoring aimed at implementing Domain-Driven Design (DDD), Hexagonal Architecture, Onion Architecture, or Ports and Adapters.

# @Vocabulary
- **Repository Pattern**: A simplifying abstraction over persistent storage that hides the boring details of data access by pretending that all of our data is in an in-memory collection.
- **Dependency Inversion Principle (DIP)**: High-level modules (domain) must not depend on low-level modules (infrastructure/ORM); both must depend on abstractions.
- **Persistence Ignorance**: The concept that the domain model must not know anything about how data is loaded or persisted.
- **Classical Mapping**: An explicit mapping configuration (e.g., using SQLAlchemy's `mapper` or `map_imperatively`) that binds an independently defined database schema to an independently defined pure Python domain model.
- **Port**: The interface between the application and whatever is being abstracted away (e.g., an `AbstractRepository` defined using Python's `abc` module or duck typing).
- **Adapter**: The concrete implementation behind the interface (e.g., `SqlAlchemyRepository` or `FakeRepository`).
- **Fake Repository**: A test double (adapter) that implements the Repository interface using native, in-memory Python collections (like `set`) to enable fast, database-free unit testing.

# @Objectives
- The AI MUST decouple the core domain model from all infrastructure concerns, specifically the database and ORM.
- The AI MUST ensure that the ORM imports and depends on the domain model, not the other way around.
- The AI MUST facilitate rapid unit testing by creating simple, easily fakeable abstractions over data storage.
- The AI MUST enforce the rule that business logic and service layers interact with persistent storage ONLY through the Repository abstraction.

# @Guidelines
- **Model Purity**: The AI MUST NOT allow domain model classes to inherit from ORM base classes (e.g., `declarative_base()` or `models.Model`). Domain models must be pure Python objects (e.g., `dataclasses`).
- **Inverted ORM Dependency**: The AI MUST define database tables explicitly (e.g., using SQLAlchemy `Table` and `MetaData`) and bind them to the domain model using classical mapping functions.
- **Repository Abstraction**: The AI MUST define an `AbstractRepository` (the Port) using the `abc` module. 
- **Restricted Interface**: The Repository interface MUST be kept radically simple. It MUST strictly expose collection-like methods: `add()` and `get()` (and optionally `list()`). 
- **No Commits in Repository**: The AI MUST NOT include `.commit()` or `.save()` calls inside the Repository methods. Committing data is the responsibility of the caller (or the Unit of Work), ensuring the Repository merely mimics an in-memory collection.
- **Fake Abstractions for Testing**: The AI MUST implement a `FakeRepository` for unit tests. This fake MUST use simple Python collections (like a `set`) and one-liner methods to replicate the `AbstractRepository` interface.
- **Duck Typing over ABCs**: If ABCs become unmaintained or misleading, the AI MAY rely on Python's duck typing to define the "Port" (a repository is any object with `add(thing)` and `get(id)` methods) or use PEP 544 `typing.Protocol`.
- **Integration Tests for Concrete Repos**: The AI MUST write integration tests for the real ORM-backed repository (e.g., `SqlAlchemyRepository`) using raw SQL to verify that the repository correctly translates domain objects to and from the database schema.

# @Workflow
1. **Define the Domain Model**: Create the domain model using pure Python objects (`@dataclass` or standard classes) with absolutely no ORM imports.
2. **Define the Schema**: In a separate module (e.g., `orm.py`), define the database tables using SQLAlchemy's `Table` objects.
3. **Map Schema to Model**: Create a function (e.g., `start_mappers()`) that explicitly maps the tables to the pure domain model classes using SQLAlchemy's classical mapping.
4. **Create the Port (Abstract Repository)**: Define an `AbstractRepository` class inheriting from `abc.ABC`, defining `@abc.abstractmethod` for `add(self, item)` and `get(self, reference)`.
5. **Create the Concrete Adapter**: Implement a `SqlAlchemyRepository` that inherits from `AbstractRepository`. Inject the database `session` into its `__init__`. Implement `add` using `self.session.add()` and `get` using `self.session.query()`.
6. **Create the Fake Adapter**: Implement a `FakeRepository` for tests. Initialize it with a Python `set`. Implement `add` via `self._collection.add()` and `get` via a generator/list comprehension over the `set`.
7. **Refactor Business Logic**: Replace all direct `session.query()` calls in the service layer or API handlers with calls to the injected `AbstractRepository`'s `add()` and `get()` methods.

# @Examples (Do's and Don'ts)

### [DON'T] Make the domain model depend on the ORM
```python
# ANTI-PATTERN: Model depends on ORM
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrderLine(Base):
    __tablename__ = 'order_lines'
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    qty = Column(Integer)
```

### [DO] Separate the schema and use classical mapping (ORM depends on Model)
```python
# PERFECT: Pure domain model
@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

# Explicit ORM definition in a separate infrastructure file
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper

metadata = MetaData()

order_lines = Table(
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('orderid', String(255)),
)

def start_mappers():
    mapper(OrderLine, order_lines)
```

### [DON'T] Mix data access directly in business logic/API endpoints
```python
# ANTI-PATTERN: Hardcoded DB session queries in the endpoint
@flask.route.gubbins
def allocate_endpoint():
    session = start_session()
    batches = session.query(Batch).all() # Direct ORM coupling
    allocate(line, batches)
    session.commit()
    return 201
```

### [DO] Use the Repository Pattern to abstract storage
```python
# PERFECT: Abstract Base Class (The Port)
import abc

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError

# Concrete SQLAlchemy Implementation (The Adapter)
class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(Batch).filter_by(reference=reference).one()

# Fake Implementation for Testing (The Adapter)
class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)
```