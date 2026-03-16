# @Domain
Triggered when the user requests the creation, refactoring, or testing of API endpoints (e.g., Flask), Service Layer orchestrations, or application folder structures in Python projects utilizing Domain-Driven Design (DDD) and layered architectures.

# @Vocabulary
- **Service Layer (Orchestration / Use-Case Layer)**: An abstraction layer between the entrypoints (e.g., Flask API) and the Domain Model. It orchestrates the workflow of a use case (fetching data, calling the domain, saving state) without containing core business rules.
- **Application Service**: A function within the Service Layer whose job is to handle requests from the outside world and orchestrate an operation. 
- **Domain Service**: A piece of core business logic that belongs in the domain model but doesn't sit naturally inside a stateful entity or value object. Distinct from an Application Service.
- **Entrypoint**: The outward-facing adapter (e.g., a Flask API endpoint) that drives the application by routing inputs to the Service Layer.
- **FakeRepository**: An in-memory implementation of the `AbstractRepository` used strictly for fast unit testing of the Service Layer.
- **FakeSession**: A temporary test double representing a database session, providing a `commit()` method used to verify that the Service Layer persists changes.
- **End-to-End (E2E) Test**: A test that exercises a "real" API endpoint using HTTP and interacts with a real database.
- **Inverted Test Pyramid (Ice-Cream Cone Model)**: An anti-pattern where a system relies on a massive amount of slow E2E tests rather than fast unit tests.
- **Anemic Domain**: An anti-pattern where the Domain Model contains little or no business logic because that logic has incorrectly leaked into the Service Layer.

# @Objectives
- Decouple the web framework (e.g., Flask) and infrastructure concerns from the Domain Model.
- Ensure API endpoints act strictly as thin adapters.
- Encapsulate the application's primary use cases within a dedicated Service Layer.
- Enable a healthy test pyramid by testing workflows at the Service Layer using Fakes, minimizing the need for slow E2E tests.
- Maintain the Single Responsibility Principle by keeping orchestration logic out of the Domain Model and web controllers.

# @Guidelines

### Architectural Constraints & Layering
- The AI MUST strictly separate "stuff that talks HTTP" from "stuff that talks domain operations".
- The AI MUST NEVER place database queries, orchestration logic, or domain rules inside an API endpoint (e.g., `@app.route` functions). 
- The AI MUST NEVER place orchestration logic (like fetching from a database, committing, or sending emails) inside the Domain Model.
- The AI MUST consolidate all use cases of the application into Application Services within the Service Layer.
- The AI MUST avoid the Anemic Domain anti-pattern: the Service Layer must orchestrate, but the Domain Model must perform the actual business logic and state mutations.

### Service Layer Implementation Rules
- When generating a Service Layer function, the AI MUST adhere to the following 4-step execution sequence:
  1. Fetch necessary objects from the repository.
  2. Perform checks/assertions about the request against the current state of the world (e.g., validating that an entity exists).
  3. Call a Domain Service or Domain Model method to execute the business logic.
  4. Save/update the modified state and commit the session.
- The AI MUST declare explicit dependencies in the Service Layer using abstractions via type hints (e.g., `repo: AbstractRepository`). This complies with the Dependency Inversion Principle (DIP).
- The AI MUST handle error conditions that require database checks (e.g., verifying if a SKU exists) in the Service Layer, NOT in the Domain Model. 

### Web/API Implementation Rules
- When building a web endpoint (e.g., Flask), the AI MUST limit its responsibilities to standard web concerns: 
  - Parsing JSON or POST parameters.
  - Instantiating dependencies (e.g., Database Session, Repository).
  - Calling the appropriate Service Layer Application Service.
  - Catching expected Domain/Service exceptions (e.g., `OutOfStock`, `InvalidSku`) and translating them into appropriate HTTP status codes (e.g., 400 Bad Request) and JSON messages.
  - Returning success HTTP status codes (e.g., 201 Created) and JSON responses.

### Testing Rules
- The AI MUST prioritize writing fast unit tests against the Service Layer using `FakeRepository` and `FakeSession`.
- The AI MUST restrict E2E tests to testing the "happy path" and primary "unhappy path" of the HTTP/API layer to prevent an Inverted Test Pyramid.
- When generating E2E tests, the AI MUST use fixtures and helpers (e.g., `random_sku()`, `random_batchref()`, `add_stock()`) to isolate randomized test data and prevent test interference.

### Directory Structure Rules
- The AI MUST organize the project into the following specific folder hierarchy to visually indicate where components belong:
  - `domain/`: Contains `model.py` and domain services.
  - `service_layer/`: Contains `services.py`.
  - `adapters/`: Contains `orm.py` and `repository.py`.
  - `entrypoints/`: Contains `flask_app.py`.
  - `tests/`: Divided into `unit/`, `integration/`, and `e2e/`.

### Known Awkwardness & Future Refactoring
- The AI MUST recognize that passing Domain Objects (like `OrderLine`) directly into the Service Layer couples the Service Layer to the Domain Model. While permissible in the initial implementation phase, the AI SHOULD be prepared to decouple the clients by migrating Service Layer parameters to primitive data types (e.g., strings and ints) in subsequent refactoring.
- The AI MUST recognize that passing raw session objects directly to the Service Layer tightens coupling. This is accepted temporarily but will be mitigated later using the Unit of Work pattern.

# @Workflow
1. **Analyze the Use Case**: Identify the external trigger (e.g., API request), the required data, and the underlying Domain Model operation.
2. **Define the E2E Test (High-level)**: Write a basic happy-path end-to-end test targeting the API endpoint, asserting the expected HTTP status and JSON response.
3. **Build Fakes for Unit Testing**: Create or update `FakeRepository` (wrapping a `set` or `list`) and `FakeSession` (exposing a `commit()` method and tracking `committed = True/False`).
4. **Test-Drive the Service Layer**: Write fast unit tests for the Application Service using the fakes. Test error conditions (e.g., `InvalidSku` exceptions).
5. **Implement the Service Layer**: Write the orchestration function in `services.py` following the 4-step sequence (fetch, assert against state, call domain, commit).
6. **Implement the API Endpoint**: Write the thin Flask endpoint in `flask_app.py` to parse input, instantiate the real SQL repository and session, call the service, catch exceptions, and return JSON.
7. **Refactor and Organize**: Ensure all code is placed in the strict `domain`, `service_layer`, `adapters`, `entrypoints`, and `tests` directory structure.

# @Examples (Do's and Don'ts)

### Service Layer Orchestration
**[DO]** Implement a Service Layer function that depends on abstractions and orchestrates the 4-step sequence:
```python
class InvalidSku(Exception):
    pass

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    # 1. Fetch
    batches = repo.list()
    # 2. Check current state
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    # 3. Call Domain
    batchref = model.allocate(line, batches)
    # 4. Save/Commit
    session.commit()
    return batchref
```

**[DON'T]** Put database queries, checks, or orchestration directly inside the Domain Model:
```python
# Anti-pattern: Domain model performing DB lookups and orchestrating commits
def allocate(self, line: OrderLine, session) -> str:
    batches = session.query(Batch).all() # DON'T DO THIS
    if line.sku not in [b.sku for b in batches]:
        raise Exception("Invalid SKU")
    # ... allocation logic ...
    session.commit() # DON'T DO THIS
```

### Thin API Endpoints (Flask)
**[DO]** Keep endpoints thin. Delegate to the Service Layer and handle HTTP translations:
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
    )
    
    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({'message': str(e)}), 400
        
    return jsonify({'batchref': batchref}), 201
```

**[DON'T]** Mix domain logic, orchestration, and DB lookups directly into the Flask endpoint:
```python
# Anti-pattern: Thick controller / Distributed Ball of Mud
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    line = model.OrderLine(request.json['orderid'], request.json['sku'], request.json['qty'])
    
    # DON'T check database state in the endpoint
    if line.sku not in {b.sku for b in batches}:
        return jsonify({'message': 'Invalid sku'}), 400
        
    try:
        # DON'T call domain logic directly from the endpoint
        batchref = model.allocate(line, batches) 
    except model.OutOfStock as e:
        return jsonify({'message': str(e)}), 400
        
    session.commit() # DON'T perform commits in the endpoint
    return jsonify({'batchref': batchref}), 201
```

### Testing the Service Layer using Fakes
**[DO]** Use `FakeRepository` and `FakeSession` to write fast unit tests for use cases:
```python
def test_returns_allocation():
    line = model.OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = model.Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()
    
    result = services.allocate(line, repo, session)
    
    assert result == "b1"
    assert session.committed is True

def test_error_for_invalid_sku():
    line = model.OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = model.Batch("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()
    
    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate(line, repo, session)
```

**[DON'T]** Rely solely on E2E HTTP tests to verify orchestration logic, error conditions, and DB constraints. Doing so creates a slow, brittle, inverted test pyramid.