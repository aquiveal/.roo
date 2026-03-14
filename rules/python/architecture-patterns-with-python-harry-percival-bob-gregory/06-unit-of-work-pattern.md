# @Domain
These rules MUST be activated when the AI is tasked with implementing database transactions, designing service layer architectures, handling data persistence, managing database sessions (e.g., SQLAlchemy), writing integration/unit tests for data access, or refactoring code where the API or Service Layer directly interacts with database connection objects.

# @Vocabulary
- **Unit of Work (UoW)**: An abstraction over the concept of atomic operations. It manages the database session, provides a single entrypoint to persistent storage, and keeps track of what objects were loaded.
- **Atomic Operation**: A set of operations that succeed or fail as a single block. Managed by the UoW to enforce data integrity.
- **Context Manager**: A Python construct (`with` block) utilizing `__enter__` and `__exit__` magic methods, used idiomatically by the UoW to define the scope of a database transaction.
- **AbstractUnitOfWork**: The Abstract Base Class (ABC) defining the interface for the UoW (context manager methods, `commit`, `rollback`, and access to repositories).
- **SqlAlchemyUnitOfWork**: The concrete implementation of the UoW that wraps a real SQLAlchemy database session and instantiates real repositories.
- **FakeUnitOfWork**: A test double implementation of the UoW that uses `FakeRepository` and tracks committed states without requiring a real database.
- **Session Factory**: A callable (e.g., SQLAlchemy `sessionmaker`) injected into the concrete UoW to generate database sessions on demand.
- **Explicit Commit**: The design choice to require the user to manually call `uow.commit()` to persist changes, ensuring the system is safe by default.

# @Objectives
- **Decouple Service Layer from Data Layer**: Completely remove database session management and direct repository instantiation from the API and Service Layer.
- **Provide Atomic Operations**: Ensure that all state modifications within a single use case succeed or fail together as a single unit.
- **Ensure Safe-by-Default Execution**: Utilize context managers to automatically roll back any uncommitted work upon exiting the scope or encountering an exception.
- **Simplify Persistence APIs**: Expose a narrow, restricted interface for data access to prevent arbitrary database queries from leaking into the domain or service logic.
- **Enable High-Gear Testing**: Facilitate the creation of fast, database-free unit tests by making the UoW easy to mock via `FakeUnitOfWork`.

# @Guidelines
- **Never Interact Directly with DB Sessions in the API or Service Layer**: The API must only initialize the UoW and invoke a service. The Service Layer must only interact with the injected `AbstractUnitOfWork`.
- **Use Context Managers for Scope**: The AI MUST wrap all repository interactions and domain logic modifications inside a `with uow:` block.
- **Require Explicit Commits**: The AI MUST NOT implement implicit commits in the UoW's `__exit__` method. The happy path MUST explicitly call `uow.commit()`.
- **Rollback by Default**: The `__exit__` method of the UoW MUST call `self.rollback()`. This ensures that if an exception is raised, or if `commit()` is forgotten, no partial state is saved. (Note: `rollback()` has no effect if `commit()` was already called).
- **The UoW Owns the Repositories**: The UoW MUST provide access to the necessary repositories as attributes (e.g., `self.batches = repository.SqlAlchemyRepository(self.session)`). Client code retrieves the repository via `uow.batches`.
- **Don't Mock What You Don't Own**: The AI MUST NOT mock the SQLAlchemy `Session` object in tests. Instead, fake the `AbstractUnitOfWork`. The Session interface is too complex and mocking it leads to data access code bleeding into the codebase. 
- **Narrow the ORM Interface**: Even though ORMs like SQLAlchemy already implement the UoW pattern via their `Session` objects, the AI MUST wrap it in a custom UoW to restrict the API to its essential core (`start`, `commit`, `rollback`) and to dispense repository objects.
- **Group Multiple Operations Atomically**: When a use case requires multiple distinct domain changes (e.g., deallocating an order line and then reallocating it), the AI MUST group them within a single `with uow:` block so they succeed or fail together.

# @Workflow
When implementing or refactoring an application to use the Unit of Work pattern, the AI MUST adhere to the following strict algorithmic sequence:

1. **Define the AbstractUnitOfWork**:
   - Create an ABC inheriting from `abc.ABC`.
   - Define type hints for the required repositories (e.g., `batches: repository.AbstractRepository`).
   - Implement `__enter__` to return `self`.
   - Implement `__exit__` to capture exceptions and call `self.rollback()`.
   - Define `@abc.abstractmethod` for `commit(self)` and `rollback(self)`.

2. **Implement the Concrete Database UoW (e.g., SqlAlchemyUnitOfWork)**:
   - Accept a `session_factory` in `__init__`.
   - In `__enter__`, invoke the `session_factory` to create a `self.session`.
   - In `__enter__`, instantiate concrete repositories passing `self.session` (e.g., `self.batches = repository.SqlAlchemyRepository(self.session)`).
   - In `__exit__`, call `super().__exit__(*args)` and then `self.session.close()`.
   - Implement `commit` to call `self.session.commit()`.
   - Implement `rollback` to call `self.session.rollback()`.

3. **Implement the FakeUnitOfWork for Testing**:
   - In `__init__`, instantiate fake repositories (e.g., `self.batches = FakeRepository([])`) and set `self.committed = False`.
   - Implement `commit` to set `self.committed = True`.
   - Implement `rollback` as a `pass` (or track rolled-back state if required by specific tests).

4. **Refactor the Service Layer**:
   - Change service function signatures to accept `uow: unit_of_work.AbstractUnitOfWork` instead of passing `session` or individual `repository` objects.
   - Wrap the core logic of the service function in a `with uow:` block.
   - Fetch resources using `uow.<repository_name>.get(...)`.
   - Modify the domain objects.
   - Call `uow.commit()` as the final step inside the `with` block.

5. **Refactor the Entrypoints (API/CLI)**:
   - Instantiate the concrete UoW (`SqlAlchemyUnitOfWork()`).
   - Pass the UoW directly into the service layer function.
   - Remove all database session creation, repository instantiation, and `session.commit()` calls from the API endpoint.

6. **Write UoW Integration Tests**:
   - Write tests against the concrete UoW to verify it can retrieve and save data.
   - Write explicit tests proving that uncommitted work rolls back by default.
   - Write explicit tests proving that an exception inside the `with uow:` block triggers a rollback.

# @Examples (Do's and Don'ts)

**[DO] Use an explicit Unit of Work with a context manager in the Service Layer:**
```python
def allocate(orderid: str, sku: str, qty: int, uow: unit_of_work.AbstractUnitOfWork) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = model.allocate(line, batches)
        uow.commit()
    return batchref
```

**[DON'T] Manage database sessions or repositories directly in the Service Layer:**
```python
# ANTI-PATTERN: Depending directly on a database session and passing it to a repository
def allocate(orderid: str, sku: str, qty: int, session) -> str:
    repo = repository.SqlAlchemyRepository(session)
    batches = repo.list()
    line = OrderLine(orderid, sku, qty)
    batchref = model.allocate(line, batches)
    session.commit() # Dangerous: No rollback mechanism if an error occurs earlier
    return batchref
```

**[DO] Implement the UoW with explicit commits and safe-by-default rollbacks:**
```python
class AbstractUnitOfWork(abc.ABC):
    batches: repository.AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
```

**[DON'T] Implement implicit commits in the Unit of Work:**
```python
# ANTI-PATTERN: Implicit commits make the system harder to reason about and less safe.
class AbstractUnitOfWork(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit() # DANGEROUS: Automatically commits without explicit instruction
        else:
            self.rollback()
```

**[DO] Use the Unit of Work to group multiple distinct operations atomically:**
```python
def change_batch_quantity(batchref: str, new_qty: int, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        batch = uow.batches.get(reference=batchref)
        batch.change_purchased_quantity(new_qty)
        while batch.available_quantity < 0:
            line = batch.deallocate_one()
        uow.commit() # Both the quantity change and the deallocations commit together
```

**[DON'T] Mock the SQLAlchemy Session in tests (Don't mock what you don't own):**
```python
# ANTI-PATTERN: Mocking complex third-party infrastructure
@mock.patch("sqlalchemy.orm.Session")
def test_allocate(mock_session):
    mock_session.query.return_value.filter_by.return_value.one.return_value = Batch(...)
    # This couples the test tightly to SQLAlchemy's internal API
```

**[DO] Use a Fake Unit of Work to mock out the persistence layer cleanly:**
```python
class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    uow.batches.add(model.Batch("batch1", "COMPLICATED-LAMP", 100, eta=None))
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"
    assert uow.committed
```