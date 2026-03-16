# @Domain
Trigger these rules when implementing new functionality, modifying existing business logic, fixing bugs, or refactoring code. These rules apply to all code creation tasks where the goal is to build testable, flexible, and maintainable software using iterative feedback loops.

# @Vocabulary
- **TDD (Test-Driven Development)**: A technical practice from Extreme Programming where new functionality is added by first writing a failing test, making it pass, then contemplating the design.
- **Emergent Design**: An approach to design promoted by TDD where design decisions gradually emerge through frequent feedback loops, rather than upfront planning (Big Design Up Front).
- **Simple Design**: A prioritization framework where code is clean if it: 1) Runs all tests, 2) Contains no duplication, 3) Maximizes clarity, 4) Has fewer elements.
- **Acceptance Tests**: Declarative tests written using the language of the domain that document functionality, measure completion, and act as a mounting point for developers to understand the domain.
- **Unit Tests**: Tests that run very fast on the inside layers of the code to verify specific functionality in isolation.
- **BDD-Style Tests (Behavior-Driven Development)**: Tests structured using "Given-When-Then" preconditions and postconditions to express domain logic and feature requirements.
- **Refactoring**: Changing the internal structure of code to improve its design without altering its external behavior, safely guarded by passing tests.

# @Objectives
- Develop the simplest possible thing that works by continuously driving implementation through tests.
- Create code that proves business correctness, prevents regressions, and gives confidence to safely refactor.
- Utilize tests as the primary form of documentation for the codebase, pushing complexity downwards.
- Catch bad designs early before they solidify into hard-to-maintain legacy code.
- Decrease the time required to test the system and reduce overall bugs to save development hours.

# @Guidelines
- **Write the Test First**: Never add new functionality without first writing a failing test that defines the expected behavior.
- **Minimum Code Required**: Write only the bare minimum amount of code necessary to make the failing test pass. Do not over-engineer or add premature optimizations (YAGNI).
- **Refactor Safely**: Refactoring must only occur when tests are passing. Look for code smells (especially duplication) and refactor to create simpler, more generic abstractions.
- **Bug Fixing Protocol**: When encountering a bug, immediately write a test that proves the bug's existence. Only after the test fails should you write the code to fix the bug, ensuring the test then passes.
- **No Tests, No Refactoring**: Do not attempt to refactor legacy, scary, or messy code without first safeguarding it with tests. Changing code without tests introduces regressions.
- **Tests as Documentation**: Write tests in a declarative, BDD-style format that clearly explains what the code does. Use the language of the domain (Ubiquitous Language) in test scenarios.
- **Simple Design Priority**: Follow the four elements of simple design strictly in order: 1. Ensure all tests run and pass. 2. Remove duplication. 3. Maximize clarity (rename for intention). 4. Minimize the number of elements.
- **Curb Complexity**: Use the feedback loops inherent in TDD to watch the design emerge and correct bad abstractions before they become unmaintainable.

# @Workflow
1. **Identify the Requirement**: Determine the specific feature, business rule, or bug fix required (often expressed as a Given-When-Then scenario).
2. **Write a Failing Test (Red)**: Create a unit or acceptance test that exercises the desired functionality. Run the test suite to explicitly confirm that the test fails (proving the logic does not yet exist or the bug is active).
3. **Make it Pass (Green)**: Write the absolute minimum imperative code required to satisfy the test. Ignore elegance or architecture temporarily if necessary—focus strictly on making the test pass.
4. **Contemplate and Refactor (Refactor)**: With the safety net of a passing test, review the design. Remove duplication, extract logic into appropriate abstractions (e.g., Domain Models, Value Objects), improve naming for clarity, and ensure the code adheres to Simple Design.
5. **Verify**: Run the test suite again to ensure the refactoring did not break the expected behavior.
6. **Iterate**: Move on to the next functional requirement, repeating the cycle.

# @Examples (Do's and Don'ts)

- **[DO]** Write a failing test first to define the functional requirements before implementing the domain logic.
```typescript
describe("A post the member hasn't upvoted", () => {
  it("When upvoted, it should upvote the post's score by one", () => {
    let initialScore: number;
    post = Post.create(...);
    initialScore = post.score;
    member = Member.create(...);

    // Act
    postService.upvotePost(existingPostVotes, member, post);

    // Assert - This test will fail initially because the logic isn't written yet
    expect(post.score).toEqual(initialScore + 1);
  });
});
```

- **[DON'T]** Change or refactor messy code without first writing tests to cover its current behavior.
```typescript
// Anti-pattern: Refactoring "blind" without test coverage
function calculatePayment(user, hours) {
  // Trying to clean up this messy logic without a test harness guarantees regressions.
  if (user.isContractor) { /* complex logic */ }
}
```

- **[DO]** Use BDD-style given/when/then terminology to make tests act as clear domain documentation.
```typescript
describe('Scenario: Successful login', () => {
  describe('Given I have an account', () => {
    describe('When I try to login', () => {
      test('Then I should be redirected to the dashboard', async () => {
        // ... Arrange, Act, Assert
      })
    })
  })
})
```

- **[DON'T]** Write the implementation first and then backfill the tests just to achieve code coverage. This violates the TDD cycle and destroys the emergent design feedback loop.