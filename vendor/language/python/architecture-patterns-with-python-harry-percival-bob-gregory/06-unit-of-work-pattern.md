# @Domain
These rules MUST be activated when the AI is performing tasks related to database transactions, atomic operations, data integrity, persistent storage abstraction, integration testing for database states, or when refactoring a Service Layer, API endpoint, or Repository to remove direct ORM/database session dependencies.

# @Vocabulary
- **Unit of Work (UoW)**: An abstraction over the concept of atomic operations and data integrity. It acts as a single entrypoint to persistent storage and tracks loaded objects and state.
- **Atomic Operations**: A sequence of operations that succeed or fail as a single block. If any operation fails, none of the changes are persisted.
- **Context Manager**: A Python construct (`with` statement) used by the UoW to define the scope of a transaction, automatically handling setup (`__enter__`) and teardown (`__exit__`).
- **Explicit Commit**: The practice of actively calling `uow.commit()` to persist changes, enforcing that the software is safe by default.
- **Rollback by Default**: The practice of automatically discarding uncommitted changes when exiting the UoW context manager, preventing partial or inconsistent states.
- **FakeUnitOfWork**: A test double (fake) implementation of the UoW that uses in-memory collections (like `FakeRepository`) and simple boolean flags (e.g., `self.committed`) instead of a real database session.
- **Don't Mock What You Don't Own**: A principle directing the AI to use custom abstractions (like `FakeUnitOfWork`) rather than mocking complex third-party libraries (like SQLAlchemy's `Session`).

# @Objectives
- Abstract away atomic operations and transaction management from the Service Layer and API/entrypoint handlers.
- Fully decouple the Service Layer from the data layer/ORM by providing repositories exclusively through the UoW.
- Guarantee data integrity by ensuring operations execute as a single atomic unit that is safe by default (requires explicit commit, rolls back on exception or early exit).
- Narrow the interface between the ORM and application code to prevent data access code from leaking across the codebase.
- Simplify unit testing by allowing the Service Layer to be tested entirely with in-memory fakes instead of mocked database sessions.

# @Guidelines
- **UoW as a Context Manager**: The AI MUST implement the UoW as a Python context manager. The `__enter__` method MUST initialize the database session and the repository instances. The `__exit__` method MUST close the session and trigger a rollback.
- **Explicit Commits Only**: The AI MUST NOT implement implicit commits on successful exits of the context manager. The Service Layer MUST explicitly call `uow.commit()` to persist changes.
- **Rollback by Default**: The AI MUST implement `self.rollback()` inside the `__exit__` method. If an error is raised, or if `commit()` is not called, the UoW MUST safely discard all state changes.
- **Repositories Belong to the UoW**: The AI MUST expose Repositories as attributes of the UoW (e.g., `uow.batches`). The Service Layer MUST NOT instantiate Repositories directly.
- **Narrow ORM Interfaces**: Even if the underlying ORM (like SQLAlchemy) implements its own UoW (e.g., `Session`), the AI MUST wrap it in a custom UoW class. The AI MUST NOT expose the ORM's complex API to the Service Layer.
- **Group Multiple Operations**: When a use case requires multiple state modifications (e.g., deallocating an order line and then reallocating it), the AI MUST execute all of them within a single `with uow:` block to guarantee atomicity.
- **Testing with Fakes**: The AI MUST implement a `FakeUnitOfWork` for unit tests. The AI MUST NOT use `mock.patch` to mock ORM sessions (adhering to "Don't mock what you don't own").
- **API/Entrypoint Constraints**: API endpoints (like Flask routes) MUST NOT instantiate database sessions or repositories directly. They MUST only instantiate a UoW, pass it to the Service Layer, and handle routing/JSON formatting.

# @Workflow
1. **Define the Abstract UoW**: Create an `AbstractUnitOfWork` base class using `abc.ABC`.
   - Define abstract properties or attributes for required repositories (e.g., `batches: repository.AbstractRepository`).
   - Implement `__exit__` to explicitly call `self.rollback()`.
   - Define abstract methods for `commit()` and `rollback()`.
2. **Implement the Concrete UoW**: Create a real UoW (e.g., `SqlAlchemyUnitOfWork`).
   - In `__init__`, accept a session factory.
   - In `__enter__`, instantiate the database session and the concrete repositories, then return `self`.
   - In `__exit__`, call `super().__exit__()` and close the database session.
   - Implement `commit()` and `rollback()` using the ORM's underlying session methods.
3. **Implement the Fake UoW**: Create a `FakeUnitOfWork` for tests.
   - Instantiate fake repositories in `__init__`.
   - Implement a `commit()` method that sets a `self.committed = True` flag.
   - Implement an empty `rollback()` method.
4. **Refactor the Service Layer**: Update use-case functions to accept `uow: AbstractUnitOfWork` instead of separate `session` and `repo` arguments.
5. **Enforce Atomicity in Use Cases**: Wrap the entire service logic inside a `with uow:` block. Retrieve objects via `uow.<repo_name>`, mutate them, and call `uow.commit()` only at the very end of the success path.
6. **Write UoW Integration Tests**: Write tests against the concrete UoW using a real (or SQLite) database to verify that:
   - Uncommitted work is rolled back by default.
   - Exceptions raised within the context manager trigger a rollback.
   - Explicit commits successfully persist data.

# @Examples (Do's and Don'ts)

### UoW Implementation and Explicit Commits
**[DO]** Require an explicit commit and roll back by default.
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

**[DON'T]** Implement implicit commits on success, which makes the system harder to reason about and unsafe by default.
```python
class AbstractUnitOfWork(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        # ANTI-PATTERN: Implicit commit
        if exn_type is None:
            self.commit()
        else:
            self.rollback()
```

### Service Layer Signature and Usage
**[DO]** Pass the abstract UoW to the service layer and group database reads/writes inside the context manager.
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

**[DON'T]** Pass raw database sessions or disconnected repositories into the service layer, leaking infrastructure details.
```python
# ANTI-PATTERN: Service layer handling infrastructure/sessions directly
def allocate(orderid: str, sku: str, qty: int, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref
```

### API Endpoint Initialization
**[DO]** Initialize the UoW in the entrypoint and pass it to the service.
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    try:
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        batchref = services.allocate(
            request.json['orderid'],
            request.json['sku'],
            request.json['qty'],
            uow
        )
    except InvalidSku as e:
        return jsonify({'message': str(e)}), 400
    return jsonify({'batchref': batchref}), 201
```

**[DON'T]** Initialize sessions and repositories in the web framework router.
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    # ANTI-PATTERN: API talks directly to three layers
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    batchref = services.allocate(line, repo, session)
    return jsonify({'batchref': batchref}), 201
```

### Testing Dependencies
**[DO]** Use a `FakeUnitOfWork` that implements the `AbstractUnitOfWork` interface to test service layer logic.
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
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"
    assert uow.committed
```

**[DON'T]** Use `mock.patch` to stub out ORM sessions (violates "Don't mock what you don't own").
```python
# ANTI-PATTERN: Mocking third-party ORM APIs
@mock.patch("sqlalchemy.orm.Session")
def test_allocate_returns_allocation(mock_session):
    repo = FakeRepository([])
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, mock_session)
    mock_session.commit.assert_called_once()
```