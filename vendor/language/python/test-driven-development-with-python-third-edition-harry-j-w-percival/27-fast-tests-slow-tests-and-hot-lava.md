# @Domain

These rules MUST trigger whenever the AI is tasked with writing tests, refactoring test suites, optimizing test execution speed, separating business logic from framework/database dependencies, designing application architecture, or troubleshooting overly complex, slow, or mock-heavy test suites.

# @Vocabulary

- **Test Desiderata**: A checklist of 12 desirable characteristics for effective tests: Isolated, Composable, Deterministic, Fast, Writable, Readable, Behavioural, Structure-agnostic, Automated, Specific, Predictive, and Inspiring.
- **The Holy Flow State**: A state of deep, uninterrupted programmer concentration. This state is fragile and is instantly destroyed by slow-running test suites.
- **Hot Lava**: A metaphor for the database. In the context of fast unit testing, touching the database ("hot lava") incurs massive performance penalties that scale geometrically over time.
- **Test Pyramid**: The optimal distribution of test types: a massive base of fast, isolated Unit Tests; a middle layer of Integration Tests; and a tiny top layer of slow, brittle Functional/End-to-End (E2E) Tests.
- **Acceptance Test**: A test that validates a piece of behavior important to the user (acceptance criteria). These are NOT inherently E2E tests; they can and should be pushed down to the unit/integration level whenever possible.
- **Mock Hell**: An anti-pattern resulting from the overuse of mocks, leading to tests that are unreadable, tightly coupled to implementation details, hostile to refactoring, and ultimately testing mocks against other mocks rather than verifying real behavior.
- **Ports and Adapters (Hexagonal / Clean / Onion Architecture)**: Architectural patterns that identify system boundaries, create interfaces for those boundaries, and decouple the core business logic from external dependencies (like databases or web frameworks).
- **Functional Core, Imperative Shell**: An architectural pattern where the application "shell" handles state, side-effects, and framework integration (imperative, tested via integration tests), while the "core" handles business rules using pure functions without side-effects (functional, tested via pure unit tests).
- **Test-Induced Design Damage**: A criticism of highly decoupled architectures, acknowledging that introducing abstraction and indirection adds complexity. This must be weighed against the benefits of testability and modularity.
- **Boiled Frog Problem**: The phenomenon where a test suite gradually becomes unacceptably slow over time without the developer noticing until it is too late.
- **Odysseus Pact**: A pre-commitment strategy to combat the Boiled Frog Problem. Setting a strict "red line" (e.g., "If the test suite takes more than 10 seconds, we stop and rethink the architecture").
- **Testing in Production**: Relying on robust monitoring and observability to verify system health in the live environment, acting as an ultimate fallback that makes certain brittle tests unnecessary.

# @Objectives

- **Preserve the Flow State**: Ensure test execution remains fast enough (typically sub-second to a few seconds) to maintain continuous developer focus.
- **Drive Architectural Decoupling**: Use testing friction as feedback to push business logic out of framework-bound layers (Django models/views) and into pure Python modules.
- **Enforce the Test Pyramid**: Actively push test coverage down to the lowest, fastest layer possible.
- **Eradicate Mock Hell**: Replace extensive monkeypatching with well-defined interfaces and fakes, or by restructuring code to isolate I/O from logic.
- **Design for Testability**: Accept the trade-off that testable code requires abstraction and indirection, valuing modularity and maintainability over short-term simplicity.

# @Guidelines

- **Evaluate Test Desiderata**: When writing or reviewing a test, the AI MUST cross-reference it against the 12 Desiderata. If a test is slow, brittle, or tests implementation (structure) rather than behavior, it MUST be refactored.
- **Treat the Database as Hot Lava**: The AI MUST aggressively identify tests that hit the database unnecessarily. Core business logic MUST NOT require a database connection to be tested.
- **Map Acceptance Criteria Downward**: The AI MUST NOT assume an acceptance test must be a Selenium/Functional test. The AI MUST attempt to satisfy user acceptance criteria using isolated unit tests combined with minimal integration tests.
- **Listen to Test Friction**: If a class or function requires excessive setup or complex mocking to test, the AI MUST interpret this as a design flaw. The AI MUST suggest separating the I/O (boundary) from the logic (core).
- **Implement Functional Core, Imperative Shell**: 
  - The AI MUST isolate business rules into pure functions that take data structures as input and return data structures as output.
  - The AI MUST restrict Django views and models to acting as the "Imperative Shell", solely responsible for passing data to the pure functions and persisting the results.
- **Avoid Mock Hell**: The AI MUST NOT generate tests with deep, nested `@mock.patch` decorators. If a dependency needs to be mocked heavily, the AI MUST suggest refactoring to a "Ports and Adapters" architecture using explicit dependency injection or interfaces.
- **Enforce the Odysseus Pact**: If the AI detects or is informed that local test execution exceeds an acceptable threshold (e.g., 10 seconds), the AI MUST alert the user to the "Boiled Frog Problem" and propose architectural decoupling.
- **Acknowledge Production Observability**: Before writing highly complex, brittle end-to-end tests for obscure edge cases, the AI MUST ask the user if this behavior is better monitored via production observability tools.

# @Workflow

1. **Assess the Goal**: Determine if the user is asking to add a feature, write a test, or refactor a slow/complex test suite.
2. **Determine the Layer (The Test Pyramid)**:
   - Does this logic require external integration (DB, Network, HTML)? -> *Integration/Functional Layer*.
   - Is this purely business rules/calculations? -> *Unit Layer*.
3. **Decouple and Extract (Functional Core)**: 
   - If the business logic is trapped inside a Django View or Model, the AI MUST extract it into a pure Python function completely independent of Django imports.
4. **Write the Core Tests**: 
   - Write lightning-fast, 100% isolated unit tests for the extracted pure functions. Do NOT use Django's `TestCase` (which spins up a DB) for these; use standard Python `unittest.TestCase` or `pytest`.
5. **Write the Shell Tests (Imperative Shell)**: 
   - Write integration tests for the Django View/Model that call the pure function. These tests check the *boundary* (did the data save? did the template render?) but do NOT exhaustively test the business permutations.
6. **Review for Mock Hell**: 
   - Scan the generated tests. If there are multiple `mock.patch` calls, refactor the application code to accept dependencies as arguments (Ports and Adapters), allowing the test to pass in simple fake objects instead of using the `mock` library.
7. **Verify the Desiderata**: 
   - Ensure the final test suite is Fast, Isolated, Behavioural, and Structure-agnostic.

# @Examples (Do's and Don'ts)

### Architecture & Database Isolation (The Database is Hot Lava)

**[DON'T]** Mix complex business logic with database operations, forcing slow integration tests.
```python
# app/views.py
from django.shortcuts import render
from .models import Order

def process_discount(request, order_id):
    order = Order.objects.get(id=order_id)
    # Business logic trapped in the shell! Requires DB to test.
    if order.customer.is_vip and order.total > 100:
        order.discount = 0.20
    elif order.total > 500:
        order.discount = 0.10
    else:
        order.discount = 0.0
    order.save()
    return render(request, "success.html")

# app/tests.py (Slow, requires DB setup)
class DiscountTests(TestCase):
    def test_vip_discount(self):
        user = User.objects.create(is_vip=True)
        order = Order.objects.create(customer=user, total=150)
        response = self.client.post(f"/discount/{order.id}/")
        order.refresh_from_db()
        self.assertEqual(order.discount, 0.20) # Hot lava!
```

**[DO]** Extract a Functional Core and test it entirely in memory, leaving only a thin Imperative Shell.
```python
# app/core.py (Functional Core - Pure Python)
def calculate_discount(is_vip: bool, total: float) -> float:
    if is_vip and total > 100:
        return 0.20
    if total > 500:
        return 0.10
    return 0.0

# app/views.py (Imperative Shell)
from .core import calculate_discount

def process_discount(request, order_id):
    order = Order.objects.get(id=order_id)
    order.discount = calculate_discount(order.customer.is_vip, order.total)
    order.save()
    return render(request, "success.html")

# app/tests.py (Fast, isolated unit test)
import unittest
from app.core import calculate_discount

class PureDiscountTests(unittest.TestCase):
    def test_vip_discount(self):
        # Sub-millisecond execution. No database. No hot lava.
        self.assertEqual(calculate_discount(is_vip=True, total=150.0), 0.20)
```

### Avoiding Mock Hell & Implementing Ports and Adapters

**[DON'T]** Rely on deep monkeypatching to isolate dependencies, coupling the test to implementation details.
```python
# app/tests.py
from unittest.mock import patch
import unittest

class CheckoutTests(unittest.TestCase):
    @patch('app.services.requests.post')
    @patch('app.services.EmailSender.send')
    @patch('app.services.Inventory.decrement')
    def test_checkout_process(self, mock_decrement, mock_send, mock_post):
        # MOCK HELL. Tightly coupled to implementation structure.
        # If the code structure changes, this test breaks (Structure-agnostic failure).
        mock_post.return_value.status_code = 200
        process_checkout(cart_id=123)
        self.assertTrue(mock_post.called)
        self.assertTrue(mock_send.called)
```

**[DO]** Introduce interfaces (Ports) and pass in Fakes (Adapters) to decouple tests cleanly.
```python
# app/services.py
class PaymentGateway: # The Port (Interface)
    def charge(self, amount: float) -> bool: pass

# app/tests.py
import unittest

class FakePaymentGateway(PaymentGateway): # The Fake Adapter
    def __init__(self):
        self.charged_amount = 0
    def charge(self, amount: float) -> bool:
        self.charged_amount = amount
        return True

class CheckoutTests(unittest.TestCase):
    def test_checkout_process_with_fake(self):
        fake_gateway = FakePaymentGateway()
        # Dependency Injection
        result = process_checkout(cart_id=123, payment_gateway=fake_gateway)
        
        self.assertTrue(result.success)
        self.assertEqual(fake_gateway.charged_amount, 100.0)
```