# @Domain
Trigger this rule file when the user requests the creation, refactoring, or review of software tests, specifically when tasked with writing integration tests, acceptance tests, BDD-style tests, or implementing Test-Driven Development (TDD) for use cases, pages, or domain features.

# @Vocabulary
*   **Advanced TDD:** A testing methodology where integration and acceptance tests serve as the primary focus over isolated unit tests, testing functional requirements in the language of the domain.
*   **Integration Test:** The primary sort of test to write in this architecture. They cover maximum ground by testing the functional requirements, the page, the state required for that page, and any components needed to realize the features simultaneously.
*   **BDD-Style Test:** Behavior-Driven Development tests mapped directly from functional requirements. They utilize the "Given-When-Then" syntax to document scenarios and business logic.
*   **Acceptance Test:** Fast-running tests at the outer boundary of the code, written declaratively using the language of the domain to prove that customer-driven features work as intended.
*   **Given-When-Then:** A domain-specific language structure (Gherkin) for defining test specifications without implementation specifics (Given = Preconditions, When = Command/Action, Then = Postconditions).
*   **Mock Object:** An in-memory, fake implementation of an infrastructure dependency (e.g., `MockUserRepo`) used strictly to keep tests fast and isolated from I/O (like databases or web servers).

# @Objectives
*   Establish tests as the primary and most effective form of documentation for the codebase.
*   Prioritize Integration Tests that test vertical slices (Pages, State, and Components together) over granular, isolated unit tests.
*   Translate business logic, use cases, and functional requirements into failing BDD-style test cases before writing implementation code.
*   Ensure the test suite runs extremely fast by leveraging Dependency Inversion to mock slow infrastructure layer dependencies.
*   Drive Emergent Design by using tests as a tight feedback loop to safely refactor and simplify abstractions.

# @Guidelines
*   **Integration Tests are Paramount:** You MUST prioritize integration tests over granular unit tests. For frontend applications, integration tests MUST validate the container/page component, the underlying state hooks/services, and the presentational components simultaneously.
*   **Tests as Documentation:** You MUST write test descriptions that act as readable documentation. Any new developer should be able to read the test suite and understand the domain, the use cases, and the business rules. Do NOT write separate API documentation if tests can demonstrate the functionality.
*   **Enforce BDD Structure:** You MUST use the `Given-When-Then` format for test specifications. Map `describe` and `it`/`test` blocks to the Preconditions (Given), the Action (When), and the Postconditions (Then).
*   **Use the Ubiquitous Language:** You MUST name test variables, methods, and descriptions using domain-specific terms discovered from use-case design, not technical jargon. 
*   **Mock Infrastructure, Never Domain:** You MUST inject in-memory mock repositories (e.g., classes implementing interface adapters like `IUserRepo`) into Application Services/Controllers during testing. You MUST NOT mock Domain Entities, Value Objects, or Domain Services; instantiate them directly.
*   **Test-Driven Refactoring (Simple Design):** You MUST write the failing test first, make it pass with minimal code, and ONLY THEN refactor for duplication, clarity, and structural constraints. Do not over-engineer the implementation before the test passes.
*   **Test CQS (Command Query Separation):** When testing Commands, assert the state changes or emitted Domain Events. When testing Queries, assert the returned Read Model data. Never test both in the same Use Case.

# @Workflow
1.  **Analyze Functional Requirements:** Identify the Use Case, the Actor, and the specific Command or Query being implemented.
2.  **Define the Scenarios (Gherkin):** Write out the exact scenarios in plain English using `Given` (Preconditions), `When` (Action), and `Then` (Postconditions).
3.  **Construct BDD Test Skeletons:** Create nested `describe` blocks that correspond exactly to the Given and When statements, and `it`/`test` blocks that correspond to the Then statements.
4.  **Setup Mock Infrastructure (Arrange):** In the `beforeEach` or `beforeAll` block, instantiate in-memory mock repositories or mock providers. Inject these into the Application Service or UI Page being tested.
5.  **Execute the Action (Act):** Invoke the Use Case or simulate the UI interaction (e.g., filling out a form and clicking submit).
6.  **Assert Postconditions (Assert):** Write expectations against the returned values, the mocked infrastructure state, or the emitted Domain Events.
7.  **Run Failing Test:** Ensure the test fails (Red).
8.  **Implement Code:** Write the minimal imperative code required to pass the test (Green).
9.  **Refactor:** Clean the code, apply SOLID principles, push complexity downwards, and ensure no duplication remains (Refactor).

# @Examples (Do's and Don'ts)

### 1. Structuring BDD-Style Integration Tests
[DO] Structure tests using nested blocks that read like a business requirement.
```typescript
describe('Scenario: Successful login', () => {
  describe('Given I have an account', () => {
    describe('When I try to login', () => {
      test('Then I should be redirected to the dashboard', async () => {
        // Arrange
        const mockRepo = new MockUserRepo();
        const authService = new AuthService(mockRepo);
        
        // Act
        const result = await authService.login('khalil@example.com', 'tacos');
        
        // Assert
        expect(result.isSuccess).toBe(true);
      });
    });
  });
});
```

[DON'T] Use vague, uninformative test names that fail to document the business rule.
```typescript
describe('AuthService', () => {
  test('login works', async () => {
    const authService = new AuthService(new MockUserRepo());
    const result = await authService.login('khalil@example.com', 'tacos');
    expect(result.isSuccess).toBe(true);
  });
});
```

### 2. Frontend Integration Testing
[DO] Test the Page, the state, and the components together as a vertical slice.
```typescript
test('Then I should be redirected to the dashboard', async () => {
  // Arrange
  const mocks = [ { request: { query: LOGIN, variables: { /*...*/ } }, result: { data: { /*...*/ } } } ];
  const component = RouterTextUtils.renderWithRouter(
    <MockedProvider mocks={mocks} addTypename={true}>
      <LoginPage/>
    </MockedProvider>
  );

  // Act
  const emailInput = await component.getByPlaceholderText(/email/);
  fireEvent.change(emailInput, { target: { value: 'khalil@example.com'}});
  const button = await component.findByRole('button');
  button.click();
  
  await act(async() => { await waitForResponse() });

  // Assert
  expect(historySpy).toHaveBeenCalledWith('/dashboard');
});
```

[DON'T] Isolate UI components so much that the actual feature/use case is not validated.
```typescript
test('LoginPage renders', () => {
  // Only tests that the component mounts, failing to test the integration of the feature.
  const { getByText } = render(<LoginPage />);
  expect(getByText('Submit')).toBeInTheDocument();
});
```

### 3. Mocking Infrastructure
[DO] Use Dependency Inversion to pass fast, in-memory mocks of external systems.
```typescript
class MockUserRepo implements IUserRepo {
  private users: User[] = [];
  async getUsers(): Promise<User[]> {
    return this.users;
  }
}

// In test setup:
userController = new UserController(new MockUserRepo()); // Speedy!
```

[DON'T] Use real infrastructure connections in test suites, causing slow test execution and fragile feedback loops.
```typescript
// DON'T do this in a test suite
userController = new UserController(new SequelizeUserRepo(models)); // Slows down tests, requires running DB
```