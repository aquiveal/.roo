# @Domain
This rule file activates when the AI is instructed to write, refactor, or review test suites, specifically when applying Test-Driven Development (TDD) principles. It also triggers when the AI is tasked with creating or modifying Service Layer functions, defining APIs, or structuring test data setup and End-to-End (E2E) tests.

# @Vocabulary
- **Test Pyramid**: A ratio and structure of testing where unit tests (Service Layer and Domain) drastically outnumber Integration and End-to-End (E2E) tests.
- **High Gear**: Writing tests against the Service Layer using fakes. This approach provides lower coupling and higher coverage, allowing the underlying Domain Model to be refactored freely.
- **Low Gear**: Writing tests directly against the Domain Model. Used for rapid feedback when exploring new, complex, or "gnarly" business rules, acting as a sketch or living documentation.
- **Edge-to-Edge Testing**: Testing the system by invoking the Service Layer API and utilizing fakes for I/O and repositories, covering the entire workflow of a use case without hitting the database or web framework.
- **Primitives**: Basic data types (e.g., strings, ints, bools) used exclusively in Service Layer function signatures to decouple external clients (and tests) from Domain Model objects.
- **Fixture Functions**: Helper functions, factories, or `@pytest.fixture` definitions used to encapsulate and hide any necessary Domain Model object instantiation away from the main test bodies.

# @Objectives
- Build a healthy test pyramid heavily weighted toward fast, Edge-to-Edge Service Layer tests.
- Decouple the test suite from the Domain Model to enable fearless, large-scale refactoring without breaking hundreds of tests.
- Design the Service Layer as a stable, primitive-based API that serves as the primary boundary for both the web framework and the test suite.
- Ensure test setups interact with the system strictly through official use cases (Service Layer functions) rather than hacking database state or instantiating Domain objects directly.

# @Guidelines
- **Test Level Selection (High vs. Low Gear)**:
  - The AI MUST default to "High Gear" (testing against the Service Layer) when adding standard features, fixing bugs, or implementing CRUD-like workflows.
  - The AI MUST drop to "Low Gear" (testing against the Domain Model) ONLY when solving a highly complex business rule or starting a brand new, poorly understood domain concept.
- **Domain Test Pruning**: The AI MUST actively delete or replace Domain-level tests once their functionality is adequately covered by higher-level Service Layer tests. Domain tests are temporary sketches, not permanent fixtures, unless they cover highly specific edge-case algorithms.
- **Service Layer Signatures**: The AI MUST define all Service Layer function parameters using Primitive types. The AI MUST NOT pass Domain objects (Entities, Value Objects, Aggregates) directly into Service Layer functions.
- **Test Data Setup**: The AI MUST setup test state by calling other Service Layer functions (e.g., calling `add_batch()` to prepare data for `allocate()`). The AI MUST NOT instantiate Domain objects or use raw SQL/ORM inserts in the test body to set up state.
- **Mitigating Domain Dependencies**: If Domain objects must be constructed in tests, the AI MUST encapsulate them completely within Fixture Functions or factory methods (e.g., `FakeRepository.for_batch()`).
- **End-to-End (E2E) Testing Constraints**:
  - The AI MUST write exactly ONE happy-path E2E test per feature to demonstrate the moving parts are glued together correctly.
  - The AI MUST group all unhappy paths into a single, separate E2E test (or a minimal set).
  - The AI MUST delegate exhaustive edge-case and error-handling coverage strictly to Service Layer unit tests, NOT E2E tests.
- **Missing Services**: If the AI finds itself needing to hack state in a test because a specific Service Layer function does not exist, the AI MUST create that missing Service Layer function (e.g., introducing an `add_batch` service to facilitate `allocate` tests).

# @Workflow
1. **Determine the Gear**: Evaluate the complexity of the task. If it is a complex domain problem, start in Low Gear. If it is a standard feature or workflow, start in High Gear.
2. **Low Gear (If Applicable)**: Write a unit test directly against the Domain Model using domain terminology. Implement the Domain Model logic to pass the test.
3. **Shift to High Gear**: Define the Service Layer API for the new feature. Ensure the function signature accepts ONLY primitives.
4. **Write Service Layer Tests**: Write Edge-to-Edge tests using a Fake Repository and a Fake Unit of Work. 
5. **Setup State via Services**: Within the Service Layer test, prepare all necessary prior state by invoking other primitive-based Service Layer functions. 
6. **Implement Service Layer**: Write the Service Layer implementation, fetching objects from the repository, calling the domain model, and committing the Unit of Work.
7. **Clean Up Domain Tests**: Review existing Domain tests. Delete any tests that are now fully exercised by the new Service Layer tests to reduce coupling.
8. **Write E2E Tests**: Create exactly one happy-path E2E test hitting the web/API layer. Create one general unhappy-path E2E test. Delegate all other edge cases to the Service Layer tests.

# @Examples (Do's and Don'ts)

### Service Layer Signatures & Decoupling

[DO] Express Service Layer inputs using primitives.
```python
def allocate(
    orderid: str, sku: str, qty: int, repo: AbstractRepository, session: AbstractSession
) -> str:
    line = OrderLine(orderid, sku, qty)
    # ...
```

[DON'T] Pass Domain objects directly into the Service Layer, coupling clients to the domain.
```python
def allocate(
    line: OrderLine, repo: AbstractRepository, session: AbstractSession
) -> str:
    # ...
```

### Test Setup

[DO] Setup test state using official Service Layer functions and primitives.
```python
def test_allocate_returns_allocation():
    repo, session = FakeRepository([]), FakeSession()
    # Setup state using a service
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, repo, session)
    
    # Execute behavior using a service
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, session)
    assert result == "batch1"
```

[DON'T] Setup test state by instantiating Domain objects directly inside a Service Layer test.
```python
def test_returns_allocation():
    # Coupled tightly to the Domain Model implementation!
    batch = model.Batch("batch1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])
    
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, FakeSession())
    assert result == "batch1"
```

### Hiding Unavoidable Domain Dependencies

[DO] Hide domain object construction inside Fixture Functions or Factories if they absolutely must be used.
```python
class FakeRepository(set):
    @staticmethod
    def for_batch(ref, sku, qty, eta=None):
        return FakeRepository([
            model.Batch(ref, sku, qty, eta),
        ])

def test_returns_allocation():
    repo = FakeRepository.for_batch("batch1", "COMPLICATED-LAMP", 100, eta=None)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, FakeSession())
    assert result == "batch1"
```

[DON'T] Leak Domain Model imports and instantiations into every Service Layer test file.

### E2E Testing Strategy

[DO] Use E2E tests sparingly, focusing on HTTP endpoints and utilizing API calls to set up state.
```python
def test_happy_path_returns_201_and_allocated_batch():
    # State setup via API (External Service)
    post_to_add_batch("batch1", "SKU1", 100, "2011-01-01")
    
    # Action via API
    data = {'orderid': 'order1', 'sku': 'SKU1', 'qty': 3}
    r = requests.post(f'{url}/allocate', json=data)
    
    assert r.status_code == 201
    assert r.json()['batchref'] == "batch1"
```

[DON'T] Hack database state directly in E2E tests using raw SQL or ORM fixtures, as it breaks encapsulation and creates brittle tests.
```python
def test_happy_path_returns_201_and_allocated_batch(add_stock):
    # Hacking database state directly!
    add_stock([
        ("batch1", "SKU1", 100, "2011-01-01"),
    ])
    # ...
```