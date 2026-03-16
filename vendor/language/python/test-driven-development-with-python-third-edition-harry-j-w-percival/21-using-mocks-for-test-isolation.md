@Domain
These rules trigger when the AI is tasked with writing or refactoring unit tests in Python (specifically using the `unittest` and `unittest.mock` libraries, often within a Django context), isolating system components, handling external dependencies, or addressing excessive test execution times/combinatorial explosion of test cases.

@Vocabulary
- **London-school TDD (Mockist TDD)**: A test-driven development style that heavily emphasizes using mocks to isolate the unit under test from its dependencies, leading to tests that specify interactions between objects.
- **Classical / Detroit-style TDD**: A TDD style that minimizes mocking, preferring to use real objects and integrated layers unless an external boundary (like a network or database) forces otherwise.
- **Combinatorial Explosion**: The exponential growth in the number of required tests when testing integrated components (e.g., if Component A has 3 states and Component B has 3 states, an integrated test suite requires 9 tests, whereas isolated tests require only 3 + 3 = 6 tests).
- **Mocking / Monkeypatching**: Replacing an object, function, or module in a namespace at runtime with a fake version (`unittest.mock.Mock`) to prevent side effects and allow introspection of calls.
- **DONTifying**: The practice of temporarily disabling a test during a major refactor by renaming its definition from `test_something` to `DONT_test_something`.
- **`call_args`**: A property of a `Mock` object that records the exact positional and keyword arguments the mock was last called with, stored as a special `call` tuple.
- **`mock.call()`**: A helper object from `unittest.mock` used to cleanly construct expected call arguments for comparison against `call_args`.
- **`.return_value`**: An attribute of a `Mock` object used either to dictate what the mock should output (in the Arrange phase) or to reference its output dynamically (in the Assert phase).

@Objectives
- Isolate system components using mocks to prevent combinatorial explosion in test suites.
- Verify exact implementation contracts when delegating to specific architectural boundaries (e.g., checking that Django's built-in auth framework is invoked correctly).
- Eliminate silent false-positives in mock assertions caused by Python's dynamic nature.
- Maintain test suite leanness by aggressively pruning duplicate coverage after introducing isolated mock tests.

@Guidelines

- **Handling Combinatorial Explosion**: When encountering nested or highly coupled system components, the AI MUST calculate the combination of required test states. If testing them together requires an exponentially growing number of tests, the AI MUST isolate the layers using mocks and test them independently.
- **Strict Mock Assertion Formatting**: The AI MUST NEVER use `Mock` magic methods like `.assert_called_with()`, `.assert_called_once_with()`, or `.assert_any_call()`. Because `Mock` dynamically accepts any method name (e.g., `asssert_called_with` will pass silently), the AI MUST explicitly use `self.assertEqual(mock_object.call_args, mock.call(...))`.
- **Mocking at the Module Level**: When a view or unit depends on a specific module (e.g., `django.contrib.auth`), the AI SHOULD mock the entire module via `@mock.patch('path.to.module')` rather than patching individual functions. This allows tracing interactions between multiple functions within that module.
- **Using `.return_value` in Setup (Arrange)**: To simulate unhappy paths or specific dependency outputs, the AI MUST assign a value to `mocked_function.return_value = ExpectedValue` before invoking the code under test.
- **Using `.return_value` in Assertions (Assert)**: To verify that the output of one mocked function was passed directly into another mocked function, the AI MUST reference `mocked_function_A.return_value` as the expected argument in `mocked_function_B`'s `call_args`.
- **Testing Implementation Details**: While the AI should generally "test behavior, not implementation", the AI MUST test implementation details using mocks IF the explicit architectural intent is to delegate to a specific interface (e.g., delegating authentication to a framework's built-in backend).
- **Test Pruning and Overlap**: After rewriting integrated tests as isolated mock tests, the AI MUST evaluate test overlap. The AI MUST delete mock tests that exactly duplicate the coverage of non-mocky behavioral tests, EXCEPT when the mock test uniquely verifies a required implementation contract.
- **DONTifying for Refactors**: When completely rewriting the implementation of a tested unit, the AI MUST rename existing tests from `test_...` to `DONT_test_...` to preserve them as references. The AI MUST NOT delete them or comment them out until the new mock-driven tests are written and passing, at which point the AI MUST "unDONTify" them and resolve coverage overlaps.
- **Django Built-in Views**: When implementing standard flows like Logout, the AI SHOULD utilize built-in framework abstractions (e.g., `auth_views.LogoutView.as_view(next_page="/")`) directly in the URL routing rather than writing custom views.
- **Local Environment Secrets**: The AI MUST NOT hardcode secrets in settings files. For local development, the AI MUST instruct the use of a `.env` file loaded into the shell (e.g., `set -a; source .env; set +a;`), ensuring `.env` is added to `.gitignore`.

@Workflow
When tasked with isolating a component or refactoring a highly coupled test suite, the AI MUST follow this exact sequence:
1. **Identify Coupling**: Analyze the code to see if the unit delegates complex logic to an underlying dependency (e.g., an auth backend, an email sender, a database model).
2. **DONTify Existing Tests**: Rename existing integrated tests to `DONT_test_...` to temporarily silence them and establish a clean slate.
3. **Patch the Boundary**: Apply `@mock.patch` to the required external module or class at the test method level.
4. **Assert the Happy Path**: Write a test verifying the mock is called correctly. Use `mock.call()` and `assertEqual` on the mock's `call_args`. If the mock returns a value that is passed to another function, assert this chain using `.return_value`.
5. **Assert the Unhappy Path**: Write a test where the dependency fails. Set `mock.return_value = None` (or raise an exception), invoke the code, and assert the correct failure behavior (e.g., error messages, redirects).
6. **Implement Logic**: Write the application code to satisfy the mock tests.
7. **UnDONTify and Prune**: Rename the `DONT_test_` functions back to `test_`. Run the suite. Analyze overlapping coverage. Delete mock tests that duplicate behavioral tests, retaining only those mock tests that enforce a strict implementation contract.

@Examples (Do's and Don'ts)

**Mock Assertions**
- [DO] 
```python
@mock.patch("accounts.views.auth")
def test_calls_authenticate_with_uid(self, mock_auth):
    self.client.get("/accounts/login?token=abcd123")
    self.assertEqual(
        mock_auth.authenticate.call_args,
        mock.call(uid="abcd123")
    )
```
- [DON'T] (Vulnerable to silent typos like `asssert_called_with`):
```python
@mock.patch("accounts.views.auth")
def test_calls_authenticate_with_uid(self, mock_auth):
    self.client.get("/accounts/login?token=abcd123")
    mock_auth.authenticate.assert_called_with(uid="abcd123")
```

**Testing Output Piping via Mocks**
- [DO] Use `.return_value` to prove wiring between two mocked functions:
```python
@mock.patch("accounts.views.auth")
def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
    response = self.client.get("/accounts/login?token=abcd123")
    self.assertEqual(
        mock_auth.login.call_args,
        mock.call(
            response.wsgi_request,
            mock_auth.authenticate.return_value, # dynamically references the mock's output
        ),
    )
```
- [DON'T] Manually construct fake return objects if you only need to prove the plumbing works:
```python
@mock.patch("accounts.views.auth")
def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
    fake_user = User(email="a@b.com")
    mock_auth.authenticate.return_value = fake_user
    response = self.client.get("/accounts/login?token=abcd123")
    self.assertEqual(mock_auth.login.call_args, mock.call(response.wsgi_request, fake_user))
```

**Temporarily Disabling Tests During Refactors**
- [DO] 
```python
def DONT_test_logs_in_if_given_valid_token(self):
    # Old integrated logic preserved here until refactor completes
```
- [DON'T] Delete the test immediately or use `#` to comment out large blocks of test code, which ruins syntax highlighting and readability.