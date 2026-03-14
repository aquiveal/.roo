# @Domain
These rules MUST activate whenever the user requests the creation, modification, or refactoring of API endpoints, web controllers, application entrypoints, use cases, orchestration logic, or tests related to system workflows.

# @Vocabulary
- **Service Layer (Application Service / Orchestration Layer / Use-Case Layer)**: A layer of abstraction that handles requests from the outside world and orchestrates operations (fetching data, checking preconditions, calling the domain model, and persisting changes). It defines the entrypoints and use cases of the system.
- **Domain Service**: A piece of logic that belongs in the domain model representing a business concept or process that does not sit naturally inside a stateful entity or value object. (Distinct from a Service Layer service).
- **Entrypoint**: The interfacing code that connects the application to the real world (e.g., a Flask API, a CLI). Its sole responsibility is parsing I/O, such as JSON routing and HTTP status codes.
- **FakeRepository / FakeSession**: In-memory abstractions used exclusively in unit tests to simulate database interactions without requiring a real database connection.
- **End-to-End (E2E) Test**: A test that exercises a "real" API endpoint (e.g., using HTTP) and talks to a real database. 
- **Orchestration**: The boring, repetitive work that must happen for every operation in the system: getting data from the database, validating state, updating the domain model, and persisting changes.

# @Objectives
- The AI MUST cleanly separate "stuff that talks HTTP" (Entrypoints) from "stuff that talks business operations" (Service Layer).
- The AI MUST ensure the web framework/API layer contains absolutely no orchestration or domain logic.
- The AI MUST capture all use cases of the application in a single, dedicated Service Layer.
- The AI MUST enable fast, high-gear unit testing of workflows by testing against the Service Layer using in-memory Fakes (`FakeRepository`, `FakeSession`), strictly minimizing the need for slow E2E tests.

# @Guidelines

### API / Entrypoint Constraints
- The AI MUST restrict the responsibilities of API endpoints exclusively to standard web operations: per-request session management, parsing information out of requests (e.g., POST parameters, JSON), invoking the Service Layer, handling raised exceptions, and returning appropriate HTTP response status codes and JSON.
- The AI MUST NOT perform database queries, validation of business rules, or orchestration logic directly inside an API endpoint.

### Service Layer Constraints
- The AI MUST define a clear API for the domain by encapsulating every use case in a dedicated Service Layer function.
- The AI MUST enforce the Dependency Inversion Principle (DIP) by ensuring Service Layer functions depend on abstractions (e.g., `AbstractRepository`), never on concrete database implementations.
- The AI MUST implement sanity checks and error conditions that require database checks (e.g., checking if a SKU exists in the database) in the Service Layer before invoking the Domain Model.
- The AI MUST catch domain exceptions (e.g., `OutOfStock`) and service-level exceptions (e.g., `InvalidSku`) in the API layer to return explicit HTTP error codes (e.g., `400 Bad Request`).

### Testing Constraints
- The AI MUST divide tests into two distinct categories: 
  1. E2E tests for web-specific functionality (happy path and unhappy path HTTP responses).
  2. Unit tests for orchestration and business logic, tested directly against the Service Layer using a `FakeRepository` and `FakeSession`.
- The AI MUST NOT write E2E tests for every possible business rule edge case; those MUST be handled by Service Layer unit tests.

### Directory and Architectural Structure
- The AI MUST organize project files to reflect architectural responsibilities. If generating a project structure, use the following layout:
  - `domain/`: Contains `model.py` (Entities, Value Objects, Domain Exceptions).
  - `service_layer/`: Contains `services.py` (Orchestration functions).
  - `adapters/`: Contains `orm.py` and `repository.py` (Infrastructure and data access).
  - `entrypoints/`: Contains `flask_app.py` (or similar web framework files).
  - `tests/`: Contains `unit/`, `integration/`, and `e2e/` directories.

# @Workflow
When instructed to implement a new use case or API endpoint, the AI MUST rigidly follow this algorithmic process:

1. **Write the Service Layer Unit Test**:
   - Instantiate a `FakeRepository` populated with required test data.
   - Instantiate a `FakeSession`.
   - Call the target Service Layer function, passing the fakes.
   - Assert the expected outcome (e.g., the return value or the state of `session.committed`).

2. **Implement the Service Layer Function**:
   - Define the function in `services.py` accepting the necessary parameters, an `AbstractRepository`, and a `session`.
   - **Step A**: Fetch necessary objects from the repository using the provided `repo`.
   - **Step B**: Make checks or assertions about the request against the current state of the world (e.g., `is_valid_sku`). Raise a Service Layer exception if preconditions fail.
   - **Step C**: Call the Domain Service or Domain Model method to perform the business logic.
   - **Step D**: If all is well, call `session.commit()` to save/update the state.
   - **Step E**: Return the required result.

3. **Write the API E2E Test**:
   - Write a happy-path test that posts JSON to the endpoint and asserts a `201` (or `200`) status code and expected JSON response.
   - Write an unhappy-path test that posts invalid data and asserts a `400` status code and error message.

4. **Implement the API Endpoint**:
   - Define the endpoint in the web framework.
   - Extract parameters from the request payload.
   - Instantiate the concrete database session and concrete repository (`SqlAlchemyRepository`).
   - Wrap the Service Layer call in a `try/except` block.
   - Call the Service Layer function.
   - Catch known Domain and Service Layer exceptions and return them as `400` HTTP responses with JSON error messages.
   - Return the successful result as a JSON response with the correct HTTP status code.

# @Examples (Do's and Don'ts)

### API Endpoints

**[DON'T]** Mix orchestration, data access, and domain logic in the web controller:
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
    )
    if not is_valid_sku(line.sku, batches):
        return jsonify({'message': f'Invalid sku {line.sku}'}), 400

    try:
        batchref = model.allocate(line, batches)
    except model.OutOfStock as e:
        return jsonify({'message': str(e)}), 400

    session.commit()
    return jsonify({'batchref': batchref}), 201
```

**[DO]** Delegate all orchestration to the Service Layer, keeping the endpoint thin:
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

### Service Layer Implementation

**[DON'T]** Tie the Service Layer to concrete database implementations:
```python
def allocate(line: OrderLine):
    session = get_session()
    repo = SqlAlchemyRepository(session)
    batches = repo.list()
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref
```

**[DO]** Depend on abstractions and strictly follow the 4-step orchestration process:
```python
class InvalidSku(Exception):
    pass

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(line: OrderLine, repo: repository.AbstractRepository, session) -> str:
    # 1. Fetch objects
    batches = repo.list()
    
    # 2. Check preconditions against current state
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
        
    # 3. Call domain logic
    batchref = model.allocate(line, batches)
    
    # 4. Save/Commit
    session.commit()
    
    return batchref
```

### Testing Workflows

**[DON'T]** Write an exhaustive suite of E2E tests for every business rule edge case, interacting directly with the database in every test.

**[DO]** Use `FakeRepository` and `FakeSession` to write blazing fast unit tests against the Service Layer:
```python
class FakeRepository(repository.AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)

class FakeSession():
    committed = False
    def commit(self):
        self.committed = True

def test_returns_allocation():
    line = model.OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = model.Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])
    
    result = services.allocate(line, repo, FakeSession())
    
    assert result == "b1"

def test_error_for_invalid_sku():
    line = model.OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = model.Batch("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([batch])
    
    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate(line, repo, FakeSession())
```