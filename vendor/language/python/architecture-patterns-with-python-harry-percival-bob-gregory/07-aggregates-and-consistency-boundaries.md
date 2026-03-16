# @Domain
Triggered when the user request involves designing or modifying domain models, establishing consistency boundaries, building Repositories, structuring object graphs, implementing database concurrency controls (locking/versioning), or writing tests for data integrity and concurrent transactions.

# @Vocabulary
- **Constraint**: A business rule that restricts the possible states a model can get into (e.g., "cannot allocate more stock than is available").
- **Invariant**: A condition that must *always* be true whenever an operation finishes. Invariants can be temporarily bent in memory during an operation, but the final consistent state must strictly uphold them.
- **Aggregate**: A design pattern representing a cluster of associated objects that are treated as a single unit for the purpose of data changes. It acts as a consistency boundary.
- **Aggregate Root**: The specific entity within an Aggregate that serves as the single entrypoint for modifying any objects inside the boundary.
- **Consistency Boundary**: The logical boundary drawn around a small number of objects that must be consistent with one another. Updates within this boundary occur in a single database transaction.
- **Bounded Context**: The specific domain context in which an Aggregate operates. A model should only include the data required for calculations within its specific context (e.g., an Allocation `Product` only needs a SKU and batches, not a price or description).
- **Optimistic Concurrency Control (OCC)**: A concurrency strategy that assumes conflicts are unlikely. It uses version numbers to allow concurrent reads but rejects concurrent writes if the version number has changed.
- **Pessimistic Concurrency Control (PCC)**: A concurrency strategy that assumes conflicts are highly likely. It explicitly locks database rows/tables (e.g., using `SELECT FOR UPDATE`) to prevent concurrent access.
- **Read-Modify-Write Cycle**: A transaction failure mode where two concurrent processes read state, modify it in memory, and attempt to write it back, potentially overwriting each other if unprotected.

# @Objectives
- Protect business invariants by establishing explicit consistency boundaries using the Aggregate pattern.
- Ensure high system performance and scalability by keeping Aggregates as small as possible and minimizing the scope of database locks.
- Enforce strict encapsulation: treat Aggregates as the "public" API of the domain model, and all subsidiary entities/value objects as "private".
- Guarantee transactional integrity during concurrent updates by implementing Optimistic Concurrency Control via explicit version numbers.
- Strictly enforce the architectural rule that Repositories must only interact with Aggregate Roots.

# @Guidelines

## Domain Modeling & Consistency Boundaries
- The AI MUST encapsulate associated objects into an Aggregate to resolve the tension between protecting invariants and allowing highly concurrent system usage.
- The AI MUST define a single Aggregate Root for each consistency boundary.
- The AI MUST NOT allow external code (including Service Layers) to directly modify child entities or value objects. All state mutations MUST be routed through methods on the Aggregate Root.
- The AI MUST raise domain exceptions if an operation cannot be completed without violating a system invariant.
- The AI MUST NOT modify multiple Aggregates in a single transaction. If a business process touches multiple Aggregates, they must be made *eventually consistent* (e.g., via domain events).
- The AI MUST restrict the attributes of an Aggregate to only the data strictly necessary for its specific Bounded Context. Do not pollute the Aggregate with generic data (e.g., image URLs) if the context only calculates logistics or allocations.

## Repositories & Aggregates
- The AI MUST enforce the rule: "One Aggregate = One Repository".
- The AI MUST NOT create Repositories for child entities. (e.g., If `Product` is the Aggregate Root containing `Batch` entities, the AI MUST build a `ProductRepository`, NOT a `BatchRepository`).
- The AI MUST design the data model so that reading an Aggregate requires only a single database query, and persisting changes requires only a single update.
- The AI MAY implement lazy-loading for an Aggregate's internal collections only if the collection is expected to grow to thousands of items and cause performance degradation.

## Concurrency & Data Integrity
- The AI MUST NOT use whole-table locks.
- The AI MUST implement Optimistic Concurrency Control by default to handle concurrent state modifications.
- The AI MUST add a `version_number` attribute (typically an integer initialized to 0) to the Aggregate Root.
- The AI MUST explicitly increment the `version_number` from *inside* the Aggregate Root's mutation methods within the domain model.
- The AI MUST NOT implement `version_number` increments in the Service Layer, nor rely on Unit of Work (UoW) or Repository "magic" to automatically increment versions, as this mixes responsibilities.
- The AI MUST explicitly handle concurrency failures (e.g., version mismatch) in the application layer. The standard mitigation is to retry the failed operation from the beginning.
- If Pessimistic Concurrency Control is mandated by the user, the AI MUST explicitly lock the specific rows using the ORM's specific locking syntax (e.g., SQLAlchemy's `.with_for_update()`).
- The AI MUST configure the database session/engine with the appropriate transaction isolation level (e.g., `isolation_level="REPEATABLE READ"` in Postgres) to enforce Optimistic Concurrency Control.

## Testing
- The AI MUST write integration tests to verify data integrity rules under concurrent load.
- The AI MUST simulate "slow" transactions in tests using threading and `time.sleep()` to reliably trigger concurrent update failures.
- Concurrency tests MUST assert that the `version_number` is incremented exactly once and that the second transaction raises the expected concurrency exception (e.g., serialization failure).

# @Workflow
1. **Analyze Constraints**: Identify the business rules, invariants, and constraints that must be protected.
2. **Define the Aggregate**: Cluster the objects required to enforce these invariants. Select the most appropriate, narrowly-scoped concept to serve as the Aggregate Root (e.g., `Product` instead of `Warehouse`).
3. **Implement Bounded Context**: Strip the Aggregate down to only the properties needed for the current business process calculations.
4. **Implement Versioning**: Add `self.version_number = 0` to the Aggregate Root's constructor.
5. **Implement Mutations**: Write domain methods on the Aggregate Root that validate constraints, mutate inner state, and increment `self.version_number += 1`.
6. **Restrict Repositories**: Create/refactor the Repository interface so it exclusively takes and returns the Aggregate Root. Delete any Repositories managing child entities.
7. **Refactor Service Layer**: Update use cases to fetch the Aggregate Root from the Repository, call the domain mutation method, and commit the Unit of Work. Ensure the Service Layer handles potential concurrency exceptions (retries).
8. **Configure Isolation**: Ensure the underlying database session is configured with `REPEATABLE READ` (or equivalent) transaction isolation.
9. **Verify Concurrency**: Write a threaded integration test using `time.sleep()` to simulate a read-modify-write race condition, asserting that the version number prevents data corruption.

# @Examples (Do's and Don'ts)

## Aggregate Boundaries and Repositories

[DO] Create repositories only for Aggregate Roots and modify state exclusively through the root.
```python
# domain/model.py
class Product: # Aggregate Root
    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku
        self.batches = batches
        
    def allocate(self, line: OrderLine) -> str:
        # Constraint validation and mutation handled internally
        batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference

# adapters/repository.py
class AbstractProductRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, sku: str) -> Product:
        pass

# service_layer/services.py
def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork):
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku) # Fetch Aggregate
        batchref = product.allocate(line)        # Mutate via Aggregate Root
        uow.commit()
```

[DON'T] Create repositories for child entities or modify them directly in the service layer.
```python
# DON'T do this: Violates consistency boundaries and aggregate rules
class AbstractBatchRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, batch_id: str) -> Batch:
        pass

def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork):
    line = OrderLine(orderid, sku, qty)
    with uow:
        # Fetching a child entity directly bypasses Aggregate constraints
        batch = uow.batches.get_available_batch_for_sku(sku) 
        batch.allocate(line) 
        uow.commit()
```

## Optimistic Concurrency and Version Numbers

[DO] Place the version number in the domain model and increment it inside the Aggregate Root's domain logic.
```python
# domain/model.py
class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number # Explicit version number

    def allocate(self, line: OrderLine) -> str:
        batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
        batch.allocate(line)
        self.version_number += 1 # Increment explicitly in the domain
        return batch.reference
```

[DON'T] Increment version numbers in the Service Layer or rely on infrastructural magic to guess what changed.
```python
# DON'T do this: Leaks domain mutation responsibilities to the service layer
def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork):
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        product.allocate(line)
        product.version_number += 1 # Anti-pattern: Service layer mutating versions
        uow.commit()
```

## Testing Concurrency

[DO] Write threaded integration tests with synthetic delays to verify concurrency controls.
```python
# tests/integration/test_uow.py
import threading
import time

def try_to_allocate(orderid, sku, exceptions):
    line = model.OrderLine(orderid, sku, 10)
    try:
        with unit_of_work.SqlAlchemyUnitOfWork() as uow:
            product = uow.products.get(sku=sku)
            product.allocate(line)
            time.sleep(0.2) # Simulate slow transaction
            uow.commit()
    except Exception as e:
        exceptions.append(e)

def test_concurrent_updates_to_version_are_not_allowed(postgres_session_factory):
    sku, batch = random_sku(), random_batchref()
    session = postgres_session_factory()
    insert_batch(session, batch, sku, 100, eta=None, product_version=1)
    session.commit()

    exceptions = []
    thread1 = threading.Thread(target=lambda: try_to_allocate("order1", sku, exceptions))
    thread2 = threading.Thread(target=lambda: try_to_allocate("order2", sku, exceptions))
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # Assert version only incremented once
    [[version]] = session.execute(
        "SELECT version_number FROM products WHERE sku=:sku", dict(sku=sku)
    )
    assert version == 2
    
    # Assert second transaction failed cleanly
    assert len(exceptions) == 1
    assert 'could not serialize access due to concurrent update' in str(exceptions[0])
```

[DON'T] Test domain logic assuming single-threaded execution without establishing integration-level concurrency proofs when dealing with shared transactional state.