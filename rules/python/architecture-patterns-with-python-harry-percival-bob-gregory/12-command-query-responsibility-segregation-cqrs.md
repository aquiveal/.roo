# @Domain
This rule file activates when the AI is tasked with creating, modifying, or refactoring API endpoints, database queries, repositories, domain models, or data retrieval workflows where there is a distinction between modifying state (writes) and fetching data (reads).

# @Vocabulary
*   **CQRS (Command-Query Responsibility Segregation)**: The architectural pattern of treating read operations (queries) and write operations (commands) entirely differently, segregating their responsibilities and underlying models.
*   **CQS (Command-Query Separation)**: The principle that a function should either modify state (command) or answer questions (query), but never both.
*   **Write Model**: The domain model and its repositories, optimized strictly for enforcing constraints, invariants, and business rules during state changes. Uncacheable and strictly consistent.
*   **Read Model**: A denormalized data store, table, or cache optimized strictly for read operations and performance. Highly cacheable and eventually consistent.
*   **Eventual Consistency**: The acceptable state for read models where the returned data might be slightly stale compared to the write model, representing the reality of distributed systems.
*   **SELECT N+1**: A performance anti-pattern often caused by ORMs, where retrieving a list of objects triggers one initial query followed by N individual queries to fetch related attributes.
*   **Post/Redirect/Get**: A web pattern that sidesteps CQS violations by separating the write phase (POST) from the read phase (GET).

# @Objectives
*   Ensure the Domain Model is used exclusively for writing data and enforcing business rules, keeping it free of read-specific bloat.
*   Optimize read operations for performance and horizontal scalability by embracing eventual consistency and using denormalized data structures.
*   Prevent coupling between the read representation of data and the underlying relational or domain-driven write structures.

# @Guidelines
*   **Enforce Command-Query Separation (CQS)**: The AI MUST ensure that any function, endpoint, or method either modifies state OR returns data. It MUST NEVER do both.
*   **API Write Endpoints**: When building endpoints that modify state (e.g., POST, PUT, PATCH), the AI MUST NOT return the modified domain state in the response body. It MUST return a status code like `201 Created` or `202 Accepted` alongside an identifier or Location header, forcing the client to perform a separate GET request to read the result.
*   **Isolate Read Operations**: The AI MUST place all read-only query logic into a dedicated module (e.g., `views.py`), separate from the service layer, domain model, and repositories.
*   **Bypass the Domain Model for Reads**: When querying data for a view, the AI MUST NOT use the Domain Model or the primary Repository. The AI MUST prefer raw SQL, simple ORM queries, or direct NoSQL/cache lookups against a denormalized database table or read store.
*   **Avoid Read-Specific Domain Bloat**: The AI MUST NOT add helper methods (e.g., `repository.for_order()`) or properties (e.g., `batch.orderids`) to Domain Model classes or Repositories simply to satisfy UI or view requirements.
*   **Update Read Models via Events**: When the write model successfully modifies state, the AI MUST use Event Handlers listening to Domain Events (e.g., `Allocated`, `Deallocated`) to execute `INSERT`, `UPDATE`, or `DELETE` statements on the denormalized read model table/store.
*   **Embrace Denormalization**: When creating read models, the AI MUST use simple, flat data structures (e.g., tables with no foreign keys, just strings and integers) to avoid expensive database joins and ORM `SELECT N+1` performance penalties.
*   **Integration Testing Views**: When writing tests for CQRS views, the AI MUST NOT manually insert raw database rows for the setup phase. The AI MUST setup the test state by dispatching Commands to the message bus, and then assert against the output of the view function.

# @Workflow
1.  **Operation Classification**: When receiving a task, analyze whether it is a Command (modifies state, applies business rules) or a Query (fetches data for display).
2.  **Command Implementation (Write Path)**:
    *   Implement the operation using the Domain Model, Repository, and Unit of Work.
    *   Ensure the operation emits a Domain Event (e.g., `BatchQuantityChanged`) upon successful state mutation.
    *   Return only a success acknowledgment (e.g., `201`, `202`, or an ID).
3.  **Read Model Initialization**:
    *   Create a denormalized storage mechanism for the view (e.g., a simple SQL table like `allocations_view` or a Redis hash).
4.  **Read Model Synchronization (Event Handlers)**:
    *   Create an Event Handler within the service layer that listens to the Domain Event emitted in Step 2.
    *   Inject the Unit of Work (or Redis client) into the handler and update the denormalized read model to reflect the new state.
5.  **Query Implementation (Read Path)**:
    *   Create a function in a `views.py` module.
    *   Write a direct, highly optimized query (e.g., raw `SELECT * FROM read_model_table`) against the read model.
    *   Return the raw data structures (e.g., list of dictionaries) directly to the caller.
6.  **Test the View**:
    *   Write an integration test for the view. Use the message bus to push Commands to set up the data, then call the view function and assert the returned data structure matches expectations.

# @Examples (Do's and Don'ts)

**[DON'T]** Mix reads and writes in an API endpoint, returning the domain state directly after a mutation:
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    # Modifies state
    batchref = services.allocate(request.json['orderid'], request.json['sku'], request.json['qty'], uow)
    # CQS Violation: returning the result directly
    return jsonify({'batchref': batchref}), 201
```

**[DO]** Separate the write operation from the read operation using HTTP status codes and dedicated view endpoints:
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    # Modifies state
    services.allocate(request.json['orderid'], request.json['sku'], request.json['qty'], uow)
    # Returns 202 Accepted, client must query the view endpoint
    return 'OK', 202

@app.route("/allocations/<orderid>", methods=['GET'])
def allocations_view_endpoint(orderid):
    # Pure read operation using a dedicated view
    result = views.allocations(orderid, uow)
    if not result:
        return 'not found', 404
    return jsonify(result), 200
```

**[DON'T]** Clutter the domain model and repository with read-specific looping and filtering:
```python
# In repository.py
def for_order(self, orderid):
    # Added purely for a view requirement
    return [p for p in self.products if p.has_order(orderid)]

# In views.py
def allocations(orderid: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        # Pulling complex domain objects just to extract strings
        products = uow.products.for_order(orderid=orderid)
        batches = [b for p in products for b in p.batches]
        return [{'sku': b.sku, 'batchref': b.reference} for b in batches if orderid in b.orderids]
```

**[DO]** Use raw SQL and a denormalized read model table strictly for views, completely bypassing the Domain Model:
```python
# In views.py
def allocations(orderid: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        # Direct, highly performant query against a read-only table
        results = list(uow.session.execute(
            'SELECT sku, batchref FROM allocations_view WHERE orderid = :orderid',
            dict(orderid=orderid)
        ))
    return [{'sku': sku, 'batchref': batchref} for sku, batchref in results]
```

**[DO]** Update the denormalized read model using an event handler listening to Domain Events:
```python
# In handlers.py
def add_allocation_to_read_model(
    event: events.Allocated,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            'INSERT INTO allocations_view (orderid, sku, batchref)'
            ' VALUES (:orderid, :sku, :batchref)',
            dict(orderid=event.orderid, sku=event.sku, batchref=event.batchref)
        )
        uow.commit()
```