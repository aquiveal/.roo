# @Domain
These rules MUST trigger whenever the AI is tasked with writing, modifying, or debugging Python unit tests that interact with external dependencies (e.g., email servers, payment gateways, third-party APIs), or when implementing/testing authentication backends and branching logic in web applications (specifically Django).

# @Vocabulary
- **Mocking**: The process of using a fake object (`unittest.mock.Mock`) to simulate the behavior of an external dependency to prevent unwanted external side effects during test execution.
- **Monkeypatching**: Dynamically replacing an object, function, or class in a namespace at runtime.
- **Test Isolation**: The principle that tests must not affect one another. Modifications to global state or namespaces must be reverted at the end of the test.
- **Tight Coupling (to implementation)**: An anti-pattern where tests assert *how* a framework achieves a result (e.g., mocking internal framework APIs) rather than *what* the result is, making the code resistant to refactoring.
- **Target Namespace**: The specific module where a dependency is *used* (looked up), which is where it must be patched, not the module where it is defined.
- **One If = One Test**: A heuristic dictating that every branching path in code (`if`, `else`, `try`, `except`) requires its own dedicated unit test.

# @Objectives
- The AI MUST strictly isolate unit tests from triggering real-world external side effects.
- The AI MUST guarantee test isolation by automatically reverting any monkeypatched objects after a test concludes.
- The AI MUST avoid creating tightly coupled tests by preferring behavioral and state assertions over mock assertions when dealing with internal framework utilities.
- The AI MUST ensure 100% branch coverage by writing a separate, distinctly named test for every logical branch in the code.

# @Guidelines

### 1. Mocking and Monkeypatching
- The AI MUST NOT use manual monkeypatching (e.g., `module.func = fake_func`). Manual monkeypatching persists across test boundaries and breaks test isolation.
- The AI MUST exclusively use the `@mock.patch` decorator from the `unittest.mock` library to mock external dependencies. This ensures the original object is automatically restored after the test.
- The AI MUST apply the `@mock.patch` decorator using the **Target Namespace** rule: Patch the object in the module where it is *imported and used*, not where it is defined (e.g., if `views.py` imports `send_mail` from `django.core.mail`, the patch target is `"app.views.send_mail"`).

### 2. Mock Argument Injection and Inspection
- When using `@mock.patch`, the AI MUST name the injected mock argument using the `mock_` prefix followed by the original function/object name (e.g., `mock_send_mail`).
- The AI MUST verify mock interactions using the `.called` property or by unpacking `.call_args`.
- When unpacking `.call_args`, the AI MUST handle both positional and keyword arguments accurately (e.g., `(arg1, arg2), kwargs = mock_func.call_args`).

### 3. Avoiding Tight Coupling to Implementation
- The AI MUST NOT mock internal framework utilities (such as Django's `messages` framework) just to verify they were called. Mocking framework internals creates tightly coupled tests that break when alternative, equally valid framework methods are used (e.g., `messages.success` vs `messages.add_message`).
- To test framework internals, the AI MUST assert against the resulting state or context (e.g., fetching `response.context["messages"]` and verifying the content and tags of the messages).
- Mocks MUST be strictly reserved for boundaries with systems outside the immediate application's control (e.g., network calls, email dispatches).

### 4. Branch Coverage ("One If = One Test")
- For every `if`, `elif`, `else`, `try`, and `except` block introduced into the application code, the AI MUST generate a corresponding, independent unit test.
- The AI MUST name these tests explicitly to describe the exact condition and the expected behavior (e.g., `test_returns_None_if_no_such_token`).

### 5. URL Generation
- When generating full URLs (including domain and protocol) for external dispatches (like email links), the AI MUST use Django's `request.build_absolute_uri()` combined with `reverse()`.

# @Workflow
When instructed to write tests for code that includes an external dependency or branching logic, the AI MUST follow this algorithmic process:

1. **Dependency Analysis**: Scan the code under test to identify any external side effects (e.g., sending an email).
2. **Namespace Resolution**: Determine the exact module path where the dependency is being utilized (the target namespace).
3. **Mock Setup**: Write the test method, decorating it with `@mock.patch("target.namespace.dependency")`.
4. **Mock Injection**: Add the `mock_dependency` argument to the test method signature.
5. **Test Execution**: Invoke the code under test (e.g., via the test client).
6. **Mock Verification**: Assert that the mock was called (`self.assertTrue(mock_dependency.called)`). Unpack `mock_dependency.call_args` to strictly assert the specific arguments passed to the external dependency.
7. **Coupling Audit**: Review the test. If a mock is being used to test an internal framework feature (like setting a flash message), delete the mock and rewrite the test to assert against the HTTP response context or database state.
8. **Branch Analysis**: Count the number of `if`, `else`, `try`, and `except` paths in the code under test.
9. **Branch Coverage Expansion**: Generate a separate test method for *each* identified path, utilizing descriptive names that explicitly state the condition and expected result.

# @Examples (Do's and Don'ts)

### Mocking External Dependencies
**[DO]** Use `@mock.patch` targeting the usage namespace and name the argument with `mock_`.
```python
from unittest import mock
from django.test import TestCase

class SendLoginEmailViewTest(TestCase):
    @mock.patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"})
        
        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link")
        self.assertEqual(to_list, ["edith@example.com"])
```

**[DON'T]** Manually monkeypatch functions, as this breaks test isolation for subsequent tests.
```python
class SendLoginEmailViewTest(TestCase):
    def test_sends_mail_to_address_from_post(self):
        # DON'T DO THIS: Persists across tests and ruins test isolation
        self.send_mail_called = False
        def fake_send_mail(*args, **kwargs):
            self.send_mail_called = True
        
        import accounts.views
        accounts.views.send_mail = fake_send_mail 
        
        self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"})
        self.assertTrue(self.send_mail_called)
```

### Testing Framework Internals (Avoiding Tight Coupling)
**[DO]** Test behavior/state by inspecting the response context.
```python
class SendLoginEmailViewTest(TestCase):
    def test_adds_success_message(self):
        response = self.client.post("/accounts/send_login_email", data={"email": "a@b.com"}, follow=True)
        message = list(response.context["messages"])[0]
        self.assertEqual(message.message, "Check your email")
        self.assertEqual(message.tags, "success")
```

**[DON'T]** Mock internal framework utilities like `django.contrib.messages`. This creates brittle tests that break if the framework implementation syntax changes.
```python
class SendLoginEmailViewTest(TestCase):
    @mock.patch("accounts.views.messages") # DON'T DO THIS
    def test_adds_success_message_with_mocks(self, mock_messages):
        response = self.client.post("/accounts/send_login_email", data={"email": "a@b.com"})
        mock_messages.success.assert_called_once()
```

### Branch Coverage ("One If = One Test")
**[DO]** Write explicitly named, separate tests for each logical branch.
```python
class AuthenticateTest(TestCase):
    def test_returns_None_if_no_such_token(self):
        # Tests the except Token.DoesNotExist branch
        pass

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        # Tests the except User.DoesNotExist branch
        pass

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        # Tests the happy path
        pass
```

**[DON'T]** Combine all branch tests into a single monolithic test block.
```python
class AuthenticateTest(TestCase):
    def test_authenticate_logic(self):
        # DON'T DO THIS: Tests should not test multiple paths in one method
        # ... test none ...
        # ... test new user ...
        # ... test existing user ...
```