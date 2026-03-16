# @Domain
These rules MUST activate when the AI is tasked with creating, modifying, or analyzing test files, test suites, testing architecture, or test environments. This includes unit tests, integration tests, functional tests, BDD/TDD processes, or any request involving the relationship, boundaries, and dependencies between production code and test code.

# @Vocabulary
*   **The Test Boundary**: The architectural separation between the system's test suite and the production system.
*   **System Component**: A recognized, integral part of the software architecture. Tests are first-class system components.
*   **Outermost Circle**: The absolute periphery of the Clean Architecture. Tests reside here, meaning nothing depends on them, and they depend on everything else.
*   **Fragile Tests Problem**: A catastrophic scenario where tests are strongly coupled to volatile system elements (like GUIs) or system structures, causing hundreds or thousands of tests to break upon trivial system changes.
*   **Structural Coupling**: The strongest and most insidious form of test coupling, where the test suite strictly mirrors the production code's structure (e.g., one test class per production class, one test method per production method).
*   **Testing API**: A specific, dedicated API created solely for the tests, allowing them to verify business rules without interacting with volatile components (like GUIs). It acts as a superset of the interactors and interface adapters.
*   **Testing Superpowers**: Mechanisms within the Testing API that allow tests to bypass security constraints, mock/bypass expensive resources (like databases), and forcefully put the system into specific testable states.
*   **Volatile Things**: System components that change frequently and for reasons unrelated to business logic (e.g., GUIs, page navigation structures).

# @Objectives
*   Treat all tests (TDD, BDD, unit, integration, acceptance) as architecturally equivalent system components.
*   Enforce strict dependency rules: tests depend on the system; the system NEVER depends on tests.
*   Eradicate the Fragile Tests Problem by decisively decoupling test structure from production structure.
*   Ensure business rules are completely verifiable without invoking or depending on the Graphical User Interface (GUI) or other volatile layers.
*   Facilitate the divergent evolution of code: allow tests to become increasingly concrete and specific while allowing production code to become increasingly abstract and general.
*   Protect production environments from "Testing Superpowers" by enforcing independent deployability of testing APIs.

# @Guidelines
*   **Constraint 1: Universal Test Equivalency**: The AI MUST treat all testing frameworks and methodologies as architecturally identical. Do not apply different dependency rules to unit tests versus integration tests. They all exist in the outermost circle.
*   **Constraint 2: Strictly Inward Dependencies**: The AI MUST NEVER introduce a dependency from production code to test code. Tests depend inward toward the code being tested. Production code remains entirely ignorant of the tests.
*   **Constraint 3: Avoid Volatile Dependencies (No GUI Testing for Business Rules)**: The AI MUST NOT write tests that verify business logic by interacting with or navigating through the GUI or presentation layers. Business rules MUST be tested directly via a Testing API to avoid fragility.
*   **Constraint 4: Prohibit Structural Coupling**: The AI MUST NOT create test suites that mirror the exact physical structure of the production code (e.g., avoiding a rigid 1:1 mapping of test classes to production classes or test methods to production methods). Tests must interact with behaviors and use cases, not internal structural layouts.
*   **Constraint 5: Implement a Testing API**: When asked to create a test suite for a system, the AI MUST route tests through a dedicated Testing API. This API must be a superset of the system's interactors and interface adapters, specifically designed to hide the structure of the application from the tests.
*   **Constraint 6: Utilize Testing Superpowers**: The AI MUST utilize the Testing API to bypass expensive databases, circumvent standard security constraints for the sake of state-setup, and explicitly force the system into required test states.
*   **Constraint 7: Secure the Testing API**: Because the Testing API possesses dangerous "superpowers," the AI MUST isolate the Testing API and its implementation into a separate, independently deployable component. It MUST NEVER be packaged or deployed into the live production environment.
*   **Constraint 8: Support Divergent Evolution**: The AI MUST write tests that supply concrete, highly specific inputs and assertions, while allowing the production code it tests to be freely refactored into abstract, general forms without breaking the tests.

# @Workflow
1.  **Analyze the Target Behavior**: Identify the exact business rules or use cases that require testing.
2.  **Locate or Define the Testing API**: 
    *   Check if a dedicated Testing API exists for the target domain.
    *   If absent, construct a Testing API interface that wraps the necessary interactors and interface adapters.
3.  **Implement Superpowers (Bypass Mechanisms)**: Ensure the Testing API has mechanisms to mock, bypass, or override volatile resources (e.g., routing directly to memory instead of a slow database, or bypassing an authentication wall to directly test a downstream business rule).
4.  **Write the Tests Against the API**: Construct the test logic ensuring it exclusively calls the Testing API. Ensure the test asserts concrete conditions without tying itself to the internal methods of the production classes.
5.  **Review Structural Coupling**: Audit the newly created tests. If the tests strictly mimic the private/internal layout of the production code, refactor the tests to target the broader use-case behaviors (Testing API) instead.
6.  **Verify Boundary Security**: Confirm that the Testing API and the tests themselves are placed in directories, modules, or packages that are strictly excluded from production deployment build artifacts.

# @Examples (Do's and Don'ts)

## GUI and Volatile Dependencies
*   **[DO]**: Test a loan approval business rule by passing concrete data directly into a `LoanApprovalInteractor` via a Testing API, bypassing the UI entirely.
*   **[DON'T]**: Test a loan approval business rule by simulating clicks on a login screen, navigating through a web menu, and filling out HTML form fields in the test suite. (This guarantees a fragile test).

## Structural Coupling
*   **[DO]**: Create a test file named `UserRegistrationBehaviorTest` that invokes a `TestRegistrationAPI`, which internally exercises various abstract factories and generalized user creation services without the test knowing those internal classes exist.
*   **[DON'T]**: Create `UserValidatorTest`, `UserDatabaseMapperTest`, and `UserPasswordHasherTest` that exactly mirror `UserValidator`, `UserDatabaseMapper`, and `UserPasswordHasher`, binding every private and public method to a specific test method.

## The Testing API and Superpowers
*   **[DO]**: Provide a method in the Testing API called `ForceSystemIntoOverdrawnState(accountId)` that uses backend bypasses to instantly set an account balance to a negative state for testing penalty calculations.
*   **[DON'T]**: Require the test suite to execute 50 legitimate withdrawal transactions through the standard user interface just to achieve an overdrawn state for testing.

## Deployment and Security
*   **[DO]**: Place the Testing API implementations in a `src/test-infrastructure` module that is exclusively linked during test execution and never packaged into the production binary.
*   **[DON'T]**: Leave `BypassSecurityForTesting()` methods inside the main `Authenticator` production class where they could be accidentally invoked in a live environment.