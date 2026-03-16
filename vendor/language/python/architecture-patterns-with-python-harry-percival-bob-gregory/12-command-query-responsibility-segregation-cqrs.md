# @Domain
These rules apply when the AI is tasked with designing, implementing, or refactoring data access patterns, APIs, or architectural structures involving read and write operations. They specifically trigger when working on Command-Query Responsibility Segregation (CQRS), Command-Query Separation (CQS), database views, read/write models, event handlers updating state, or performance optimizations for data retrieval (e.g., resolving ORM SELECT N+1 issues).

# @Vocabulary
- **CQRS (Command-Query Responsibility Segregation)**: The architectural pattern of separating the data models and access patterns used for reading data (Queries) from those used for writing data (Commands).
- **CQS (Command-Query Separation)**: The principle that a function should either modify state (a command) or answer a question (a query), but never both.
- **Write Model**: The domain model and repositories optimized for enforcing business rules, constraints, and invariants during state changes. Requires transactional consistency.
- **Read Model / View Model**: A specialized, often denormalized data store or raw SQL query optimized exclusively for fast data retrieval. Can be eventually consistent.
- **Eventual Consistency**: The acceptable state in distributed systems where read models may temporarily reflect stale data before being fully synchronized with the write model.
- **SELECT N+1 Problem**: An ORM performance anti-pattern where an initial query retrieves a list of objects, and subsequent individual queries are executed to retrieve associated attributes/foreign keys.
- **Post/Redirect/Get**: A web development pattern that embodies CQS by separating the write phase (POST) from the read phase (GET via Redirect).
- **Denormalized Data Store**: A flat database table or NoSQL store (e.g., Redis) with no foreign keys, designed purely for fast `SELECT * FROM table WHERE key = value` queries.

# @Objectives
- The AI MUST strictly separate read operations from write operations across the entire application architecture.
- The AI MUST protect the Domain Model from read-specific bloat, keeping it exclusively focused on enforcing write-time invariants and business rules.
- The AI MUST optimize read operations for maximum performance and horizontal scalability by bypassing complex ORM joins in favor of raw SQL or denormalized read models.
- The AI MUST embrace eventual consistency for read operations, understanding that stale data is unavoidable and acceptable in distributed web systems.
- The AI MUST utilize the Event-Driven Architecture (Message Bus and Event Handlers) to synchronize the Write Model with the Read Model.

# @Guidelines

## Command-Query Separation (CQS)
- The AI MUST ensure that any function, endpoint, or method either alters state (Command) or retrieves state (Query). A single function MUST NOT do both.
- When implementing APIs, the AI MUST return simple acknowledgments (e.g., `201 Created` or `202 Accepted`) from write endpoints rather than returning the newly created or modified complex domain state.

## Protecting the Write Model
- The AI MUST NOT add read-specific helper methods (e.g., `.for_order()`) to Repositories. Repositories are strictly for retrieving and saving Aggregates during write operations.
- The AI MUST NOT add read-specific properties or methods to Domain Model entities to satisfy UI or API query requirements.

## Implementing the Read Model (Views)
- The AI MUST place read-only operations in a dedicated `views.py` (or equivalent) module.
- The AI MUST default to using raw SQL queries with standard database drivers (or SQLAlchemy `session.execute`) for read models, directly mapping database rows to simple data structures (e.g., dictionaries) rather than Domain Objects.
- The AI MUST avoid using the ORM for complex read queries to prevent the SELECT N+1 problem and high CPU usage from relational joins.
- For high-scale read requirements, the AI MUST design completely separate, denormalized read tables (no foreign keys, just primitives) or use a separate storage engine altogether (e.g., Redis).

## Updating the Read Model
- The AI MUST update denormalized Read Models asynchronously or as a secondary step using Event Handlers.
- When a write operation successfully completes and raises a Domain Event (e.g., `Allocated`), the AI MUST create a dedicated handler (e.g., `add_allocation_to_read_model`) to update the View/Read table.
- The AI MUST design the system so that the Read Model can be completely rebuilt from scratch using historical Write Model data or events.

## Testing CQRS
- The AI MUST test CQRS views using integration tests.
- When writing integration tests for views, the AI MUST use the public entrypoint (the Message Bus) to set up the test state (via Commands/Events) rather than manually inserting data into the database or using Repositories.

# @Workflow
When tasked with implementing a new feature that involves both modifying and retrieving data, the AI MUST follow this exact sequence:
1. **Segregate the Request**: Identify the write component (Command) and the read component (Query) of the feature.
2. **Implement the Write Flow**: Use the standard Domain Model, Repository, and Unit of Work to enforce business rules and mutate state. Ensure this flow emits a Domain Event representing the state change.
3. **Implement the View (Query) Flow**: Create a separate function in a `views` module. Implement the data retrieval using raw SQL or a direct query to a denormalized read store. Return plain data structures (e.g., dicts), NOT Domain Objects.
4. **Synchronize via Events**: If using a denormalized read store, create an Event Handler that listens to the Domain Event emitted in Step 2 and executes a simple `INSERT`/`UPDATE`/`DELETE` on the read store.
5. **Register Handlers**: Map the Domain Event to both its primary side-effect handlers and the Read Model update handler in the Message Bus.
6. **Test**: Write an integration test for the View. Trigger the system's write operations using the Message Bus, then query the View to assert the expected output.

# @Examples (Do's and Don'ts)

## CQS API Design
- **[DO]**
  ```python
  @app.route("/allocate", methods=['POST'])
  def allocate_endpoint():
      # Write operation returns simple acknowledgement
      bus.handle(commands.Allocate(request.json['orderid'], request.json['sku']))
      return 'OK', 202
  
  @app.route("/allocations/<orderid>", methods=['GET'])
  def allocations_view_endpoint(orderid):
      # Read operation delegates to a specialized view
      result = views.allocations(orderid, unit_of_work.SqlAlchemyUnitOfWork())
      return jsonify(result), 200
  ```
- **[DON'T]**
  ```python
  @app.route("/allocate", methods=['POST'])
  def allocate_endpoint():
      # Anti-pattern: Modifying state AND querying complex data in one call
      batchref = services.allocate(request.json['orderid'], request.json['sku'], uow)
      batch = uow.batches.get(batchref)
      return jsonify({'batchref': batchref, 'current_allocations': batch.allocations}), 201
  ```

## Implementing Views
- **[DO]**
  ```python
  # views.py
  def allocations(orderid: str, uow: SqlAlchemyUnitOfWork):
      with uow:
          # Raw SQL bypasses ORM overhead and returns flat dictionaries
          results = list(uow.session.execute(
              'SELECT sku, batchref FROM allocations_view WHERE orderid = :orderid',
              dict(orderid=orderid)
          ))
      return [{'sku': sku, 'batchref': batchref} for sku, batchref in results]
  ```
- **[DON'T]**
  ```python
  # views.py
  def allocations(orderid: str, uow: SqlAlchemyUnitOfWork):
      with uow:
          # Anti-pattern: Using complex ORM joins for reads (risks SELECT N+1)
          batches = uow.session.query(model.Batch).join(
              model.OrderLine, model.Batch._allocations
          ).filter(model.OrderLine.orderid == orderid)
          return [{'sku': b.sku, 'batchref': b.batchref} for b in batches]
  ```

## Repository and Domain Purity
- **[DO]**
  ```python
  class AbstractRepository(abc.ABC):
      @abc.abstractmethod
      def add(self, product: Product): ...
      
      @abc.abstractmethod
      def get(self, sku: str) -> Product: ...
      # Repository contains ONLY methods required for writing/updating Aggregates
  ```
- **[DON'T]**
  ```python
  class AbstractRepository(abc.ABC):
      # Anti-pattern: Cluttering the write repository with read-specific helper methods
      def for_order(self, orderid: str) -> List[Product]: ...
      def get_most_popular_products(self) -> List[Product]: ...
  ```

## Updating Read Models
- **[DO]**
  ```python
  # handlers.py
  def add_allocation_to_read_model(event: events.Allocated, uow: SqlAlchemyUnitOfWork):
      with uow:
          # Denormalized flat table updated purely via event handler
          uow.session.execute(
              'INSERT INTO allocations_view (orderid, sku, batchref) '
              'VALUES (:orderid, :sku, :batchref)',
              dict(orderid=event.orderid, sku=event.sku, batchref=event.batchref)
          )
          uow.commit()
  ```
- **[DON'T]**
  ```python
  # services.py
  def allocate(cmd: commands.Allocate, uow: SqlAlchemyUnitOfWork):
      with uow:
          product = uow.products.get(cmd.sku)
          batchref = product.allocate(line)
          # Anti-pattern: Tying read-model updates directly into core write-model logic
          uow.session.execute('INSERT INTO allocations_view ...')
          uow.commit()
  ```

## Testing CQRS Views
- **[DO]**
  ```python
  def test_allocations_view(sqlite_session_factory):
      uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
      # Setup uses the Message Bus (Commands) to reach the required state
      messagebus.handle(commands.CreateBatch('b1', 'sku1', 50, None), uow)
      messagebus.handle(commands.Allocate('o1', 'sku1', 20), uow)
      
      # Assertion queries the view directly
      assert views.allocations('o1', uow) == [{'sku': 'sku1', 'batchref': 'b1'}]
  ```
- **[DON'T]**
  ```python
  def test_allocations_view(sqlite_session_factory):
      uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
      # Anti-pattern: Manually hacking database state in a view test
      uow.session.execute("INSERT INTO batches ...")
      uow.session.execute("INSERT INTO order_lines ...")
      uow.commit()
      
      assert views.allocations('o1', uow) == [{'sku': 'sku1', 'batchref': 'b1'}]
  ```