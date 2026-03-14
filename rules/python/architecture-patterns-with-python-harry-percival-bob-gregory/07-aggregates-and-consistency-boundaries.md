# @Domain
This rule file MUST be activated when the AI is performing any of the following tasks:
- Designing, refactoring, or modifying Domain Models.
- Designing or modifying Repositories or Data Access Layers.
- Implementing business logic that involves state changes, data integrity, or business rules.
- Handling race conditions, concurrency, or database locking mechanisms.
- Designing systems that require a high degree of concurrent writes.
- Writing integration tests for database transactions or concurrent operations.
- Structuring entities within a Bounded Context or Microservice.

# @Vocabulary
- **Constraint**: A business rule that restricts the possible states a model can get into (e.g., "Cannot allocate more stock than is available").
- **Invariant**: A condition or rule that must always be true whenever a business operation finishes.
- **Consistency Boundary**: A boundary within which all invariants are guaranteed to be maintained.
- **Aggregate**: A design pattern representing a cluster of associated domain objects treated as a single unit for the purpose of data changes.
- **Aggregate Root**: The single entrypoint entity within an Aggregate. Outside code can only hold references to this root.
- **Bounded Context**: A specific boundary within a system where a domain model is defined. A concept (like "Product") will have different definitions and attributes depending on its Bounded Context.
- **Optimistic Concurrency Control**: A concurrency strategy that assumes conflicts are rare, proceeding with operations and relying on a mechanism (like a version number) to detect and reject conflicting concurrent updates upon commit.
- **Pessimistic Concurrency Control**: A concurrency strategy that assumes conflicts will happen and uses database locks (e.g., `SELECT FOR UPDATE`) to prevent concurrent access to rows.
- **Version Number**: An integer attribute on an Aggregate used to implement optimistic concurrency control by incrementing on every state mutation.

# @Objectives
- The AI MUST enforce data integrity and business invariants by funneling all state changes through explicit consistency boundaries (Aggregates).
- The AI MUST optimize system performance and concurrency by preventing the locking of entire database tables, utilizing Aggregate-level optimistic locking instead.
- The AI MUST decouple domain models from infrastructure while ensuring the database correctly serializes concurrent modifications to the same Aggregate.
- The AI MUST design domain objects that strictly reflect the needs of their specific Bounded Context, stripping away any attributes not required for immediate business logic calculations.

# @Guidelines

## Aggregate Design and Consistency Boundaries
- The AI MUST identify the invariants of the system before designing the domain model.
- The AI MUST group entities and value objects that share invariants into a single Aggregate.
- The AI MUST designate one entity as the Aggregate Root.
- The AI MUST keep Aggregates as small as possible to optimize performance and concurrency. If an Aggregate grows too large (e.g., thousands of child entities), the AI MUST implement lazy-loading or redesign the aggregate boundaries.
- The AI MUST enforce that the ONLY way to modify objects inside an Aggregate is to load the entire Aggregate and call methods on the Aggregate Root.

## Bounded Contexts
- The AI MUST NOT create "kitchen-sink" domain models. When modeling an entity (e.g., `Product`), the AI MUST include ONLY the attributes necessary for the current context's calculations (e.g., `sku` and `batches`). Ignore attributes like `price` or `description` if they belong to a different context (like ecommerce/catalog).

## Repository Constraints
- The AI MUST apply the rule: "One Aggregate = One Repository".
- The AI MUST NOT create Repositories for subsidiary entities or value objects. If `Product` is the Aggregate containing `Batch` objects, there MUST be a `ProductRepository`, and there MUST NOT be a `BatchRepository`.

## Concurrency Control
- To handle concurrent writes without locking entire tables, the AI MUST implement Optimistic Concurrency Control by default.
- The AI MUST add a `version_number` attribute (defaulting to 0) to the Aggregate Root.
- The AI MUST explicitly increment `self.version_number += 1` inside the Aggregate Root's method whenever a state-mutating action is successfully performed.
- The AI MUST NOT implement the version number increment in the Service Layer or Unit of Work. It is a Domain concern.
- When an operation fails due to a concurrent update (optimistic lock failure), the AI MUST assume the standard recovery strategy is to retry the operation from the beginning (fetching the new state and attempting the mutation again).
- If performance profiling requires it, the AI MAY use Pessimistic Concurrency Control using SQLAlchemy's `.with_for_update()`, but it MUST be aware of the "read-modify-write" failure mode and the increased risk of deadlocks.

## Testing Concurrency and Integrity
- When testing data integrity rules against concurrent operations, the AI MUST write integration tests that simulate overlapping transactions.
- The AI MUST use `time.sleep()` within the test execution flow to force a context switch, or use explicit synchronization primitives (like semaphores) between threads.
- The AI MUST assert that concurrent updates raise the appropriate database serialization exceptions (e.g., `could not serialize access due to concurrent update`).
- The AI MUST assert that only the first transaction succeeds and the version number increments exactly once.

# @Workflow
When tasked with modeling a business process that modifies state, the AI MUST follow this exact algorithmic process:

1. **Identify Invariants**: Determine the strict business rules that must be true after the operation completes.
2. **Define the Aggregate**: Choose the smallest possible cluster of objects required to evaluate and enforce those invariants.
3. **Select the Root**: Pick the primary entity to act as the Aggregate Root.
4. **Encapsulate State**: Remove any public setters on child entities. Create methods on the Aggregate Root to handle all modifications.
5. **Implement Versioning**: Add `version_number: int = 0` to the Aggregate Root. Increment this number inside every modifying method.
6. **Restrict Repositories**: Delete any existing Repositories for child entities. Create a single Repository interface for the Aggregate Root.
7. **Configure Isolation**: Ensure the database session or Unit of Work is configured with the correct transaction isolation level (e.g., `isolation_level="REPEATABLE READ"`) to enforce the version number check.
8. **Write Concurrency Tests**: Create an integration test spanning two threads. Thread 1 loads the aggregate. Thread 2 loads the aggregate. Thread 1 modifies and commits. Thread 2 modifies and attempts to commit. Assert Thread 2 throws a concurrency exception.

# @Examples (Do's and Don'ts)

## Aggregate Design and State Modification
- **[DO]** Route all modifications through the Aggregate Root, allowing it to enforce invariants.
```python
class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number

    def allocate(self, line: OrderLine) -> str:
        # Aggregate enforces business rules across its children
        batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
        batch.allocate(line)
        self.version_number += 1
        return batch.reference
```
- **[DON'T]** Modify child entities directly from the Service Layer, bypassing the Aggregate Root's consistency boundary.
```python
# Anti-pattern: Modifying a child entity directly without an Aggregate
def allocate(line: OrderLine, repo: BatchRepository, session):
    batches = repo.list(sku=line.sku)
    batch = next(b for b in batches if b.can_allocate(line))
    batch.allocate(line) # Invariants are not protected against concurrent cross-batch rules!
    session.commit()
```

## Repository Pattern Usage
- **[DO]** Create Repositories strictly for Aggregate Roots.
```python
class AbstractProductRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: Product):
        pass

    @abc.abstractmethod
    def get(self, sku: str) -> Product:
        pass
```
- **[DON'T]** Create Repositories for subsidiary objects or collections that belong inside an Aggregate.
```python
# Anti-pattern: Repository for a subsidiary entity
class BatchRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, reference: str) -> Batch:
        pass
```

## Bounded Contexts
- **[DO]** Define models strictly with the attributes needed for the immediate domain calculation.
```python
class Product:
    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku
        self.batches = batches
```
- **[DON'T]** Bloat the model with attributes belonging to a different operational context.
```python
# Anti-pattern: Kitchen-sink model mixing multiple contexts
class Product:
    def __init__(self, sku: str, batches: List[Batch], price: float, description: str, image_url: str, dimensions: dict):
        self.sku = sku
        self.batches = batches
        self.price = price
        self.description = description
```

## Version Numbers and Optimistic Locking
- **[DO]** Increment the version number inside the domain model's modifying method.
```python
class Product:
    def change_batch_quantity(self, ref: str, qty: int):
        batch = next(b for b in self.batches if b.reference == ref)
        batch.change_purchased_quantity(qty)
        self.version_number += 1 # Domain object controls its version
```
- **[DON'T]** Increment the version number in the Service Layer or ORM logic.
```python
# Anti-pattern: Leaking version control into the Service Layer
def change_batch_quantity(ref: str, qty: int, uow: UnitOfWork):
    with uow:
        product = uow.products.get_by_batchref(ref)
        product.change_batch_quantity(ref, qty)
        product.version_number += 1 # WRONG: Service layer should not mutate version
        uow.commit()
```