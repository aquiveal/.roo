# @Domain
Trigger these rules when the user requests test creation, test refactoring, implementation of Test-Driven Development (TDD), service layer modifications, or end-to-end (E2E) / integration test setup. Activate specifically when resolving test coupling issues, managing test data setup, or defining service layer APIs.

# @Vocabulary
- **Test Pyramid**: A testing strategy prioritizing a massive base of fast unit/service tests, a smaller number of integration tests, and a minimal number of E2E tests (e.g., 15 unit tests, 8 integration tests, 2 E2E tests).
- **Blob of Glue**: The anti-pattern where tests are highly coupled to the domain model's internal implementation, cementing the system in a particular shape and making refactoring excessively difficult.
- **High Gear**: A testing methodology used for adding features or fixing bugs where tests are written against the service layer (edge-to-edge). It provides lower coupling, higher coverage, and faster refactoring.
- **Low Gear**: A testing methodology used when starting a new project or solving a highly complex domain problem. Tests are written directly against the domain model to gain rapid design feedback and create executable documentation.
- **Edge-to-Edge Testing**: Writing tests that invoke the whole system (via the service layer) using fakes for I/O, rather than directly interacting with domain objects.
- **Primitives**: Basic data types (strings, integers, floats, etc.) used to pass data into the service layer API, entirely decoupling the caller from domain object representations.

# @Objectives
- Build a highly decoupled, refactor-friendly test suite by interacting primarily with the service layer.
- Ensure the service layer API acts as an impenetrable boundary that only accepts primitive data types, hiding all domain objects from the outside world (including tests).
- Eradicate direct database manipulation (e.g., raw SQL inserts) in test setups, replacing them with official service layer or API calls.
- Maintain a healthy Test Pyramid by keeping E2E tests to an absolute minimum while maximizing service-layer test coverage.
- Treat tests as living documentation that guides design ("Low Gear") without permanently anchoring implementation details ("High Gear").

# @Guidelines
- **Gear Shifting (Test Level Selection)**:
  - The AI MUST operate in "Low Gear" (testing the domain model directly) ONLY when fleshing out a new, complex domain problem to get immediate design feedback.
  - The AI MUST operate in "High Gear" (testing against the service layer) for all standard feature additions, bug fixes, and general coverage to minimize coupling.
  - The AI MUST actively delete or rewrite domain-level tests if their functionality becomes fully covered by service-layer tests, preventing the "blob of glue" anti-pattern.
- **Service Layer API Design**:
  - The AI MUST define all service layer functions to accept primitive data types (e.g., `str`, `int`) instead of domain objects. 
  - The AI MUST NOT leak domain objects (e.g., `OrderLine`, `Batch`) into the arguments of service layer functions or API controllers.
- **Test Data Setup**:
  - The AI MUST NOT directly instantiate domain objects within service-layer tests. If domain dependencies are required, the AI MUST encapsulate them inside fixture functions or factory methods (e.g., `FakeRepository.for_batch()`).
  - The AI MUST NOT use hardcoded SQL or database fixture hacks to set up state for End-to-End (E2E) tests.
  - The AI MUST use actual API endpoints or service layer functions (e.g., `services.add_batch()`) to set up and tear down test environments.
  - If a required setup action does not exist as a service (e.g., adding stock to a database), the AI MUST create a dedicated service and API endpoint for it rather than hacking the test state.
- **E2E Test Constraints**:
  - The AI MUST write exactly ONE end-to-end test per feature to cover the happy path.
  - The AI MUST consolidate all unhappy paths for a feature into a single E2E test (or omit E2E error testing entirely if covered by the service layer). Error handling counts as a feature and should be exhaustively tested at the unit/service level.

# @Workflow
1. **Determine the Gear**: Assess if the task is a novel, complex domain problem (use Low Gear) or a routine feature/bug fix (use High Gear).
2. **Sketch Domain (If Low Gear)**: Write tests directly against domain objects to flesh out the design. Once the design is stable, proceed to step 3.
3. **Draft Service Layer Tests (High Gear)**: Write edge-to-edge tests against the service layer using primitive inputs. 
4. **Refactor Service Layer APIs**: Ensure the service layer signature accepts only primitives. Instantiate the required domain objects *inside* the service layer function.
5. **Establish Clean Test Setup**:
   - For Service/Unit tests: Use existing service functions (e.g., `services.add_batch`) to prepare the state. If unavailable, use a factory fixture.
   - For E2E tests: Use HTTP API clients to call endpoints for state preparation.
6. **Implement Missing Services**: If step 5 reveals missing operations (e.g., no way to add inventory without raw SQL), implement the missing service and expose it via the API.
7. **Optimize the Test Pyramid**: Write exhaustive edge cases at the service layer. Write exactly one happy-path E2E test and one unhappy-path E2E test.
8. **Prune Domain Tests**: Review existing domain-level tests and delete those whose logic is now entirely covered by the new service layer tests.

# @Examples (Do's and Don'ts)

### Service Layer API Design
[DON'T] Pass domain objects into the service layer or test setup.
```python
# DON'T
def allocate(line: OrderLine, repo: AbstractRepository, session):
    pass

def test_returns_allocation():
    batch = model.Batch("batch1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])
    result = services.allocate(model.OrderLine("o1", "COMPLICATED-LAMP", 10), repo, FakeSession())
```

[DO] Use primitives for the service API and use services for test setup.
```python
# DO
def allocate(orderid: str, sku: str, qty: int, repo: AbstractRepository, session) -> str:
    line = OrderLine(orderid, sku, qty)
    # ...

def test_allocate_returns_allocation():
    repo, session = FakeRepository([]), FakeSession()
    # Use a service to set up state instead of instantiating domain objects
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, repo, session)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, session)
    assert result == "batch1"
```

### End-to-End Test Setup
[DON'T] Use raw SQL or database fixtures to prepare state for E2E tests.
```python
# DON'T
@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_201(postgres_session):
    postgres_session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity) VALUES ("batch1", "LAMP", 100)'
    )
    data = {'orderid': 'order1', 'sku': 'LAMP', 'qty': 3}
    r = requests.post(f'{url}/allocate', json=data)
```

[DO] Use API endpoints to prepare state, ensuring complete decoupling from database schemas.
```python
# DO
@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_201_and_allocated_batch():
    # Setup using an API endpoint
    api_client.post_to_add_batch('batch1', 'LAMP', 100, None)
    
    data = {'orderid': 'order1', 'sku': 'LAMP', 'qty': 3}
    r = requests.post(f'{url}/allocate', json=data)
    
    assert r.status_code == 201
    assert r.json()['batchref'] == 'batch1'
```

### Domain Dependencies in Fixtures (When Services Are Unavailable)
[DON'T] Scatter domain instantiation throughout test files.
```python
# DON'T
def test_something():
    repo = FakeRepository([model.Batch("b1", "SKU", 100, eta=None)])
```

[DO] Encapsulate domain instantiation inside a factory or fixture.
```python
# DO
class FakeRepository(set):
    @staticmethod
    def for_batch(ref, sku, qty, eta=None):
        return FakeRepository([
            model.Batch(ref, sku, qty, eta),
        ])

def test_something():
    repo = FakeRepository.for_batch("b1", "SKU", 100, eta=None)
```