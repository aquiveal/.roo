## @Domain
These rules activate when the AI is instructed to write tests, refactor existing code, debug reported issues, or design business logic modules. They apply to all unit testing and test-driven development (TDD) activities across any programming language.

## @Vocabulary
*   **Self-Testing Code:** A suite of fully automatic tests that execute and verify their own results (e.g., producing a green/red output) without requiring human inspection.
*   **Fixture:** The initial state, data, and objects required to run a specific test.
*   **Shared Fixture:** An anti-pattern where multiple tests mutate the same instance of a fixture defined in an outer scope, leading to non-deterministic, order-dependent test failures.
*   **Fresh Fixture:** A pristine, newly instantiated fixture created before every single test (e.g., inside a `beforeEach` block) to guarantee test isolation.
*   **Setup-Exercise-Verify:** The three mandatory phases of a well-structured test (also known as Given-When-Then or Arrange-Act-Assert).
*   **Teardown:** The implicit or explicit phase that cleans up the fixture after a test executes. Implicit teardown is achieved by using Fresh Fixtures.
*   **Boundary Conditions:** Edge cases where things are likely to go wrong, such as empty collections, zero, negative numbers, or empty strings.
*   **Failure:** A test outcome where a verification step (assertion) evaluates to false.
*   **Error:** A test outcome where an unexpected exception is thrown during the setup or exercise phase before the verification step can occur.
*   **Green/Red Bar:** The visual representation of a passing test suite (Green) or a suite with at least one failing test (Red). 

## @Objectives
*   Build a powerful, self-checking bug detector that decapitates the time it takes to find and fix defects.
*   Enable safe refactoring by ensuring code behavior remains completely observable and unchanged.
*   Drive the testing process by risk analysis rather than blind coverage metrics.
*   Guarantee test isolation by strictly avoiding state bleed between test cases.
*   Expose bugs via automated unit tests *before* writing the code to fix them.

## @Guidelines
*   **Automatic Result Checking:** Tests must evaluate their own results. The AI MUST NOT generate tests that require the user to manually inspect console output to determine success.
*   **Verify Failures First:** The AI MUST ensure a test is capable of failing. When writing a test for existing code, mentally or physically inject a temporary fault to verify the test fails (turns red), then revert it to see it pass (turns green).
*   **Risk-Driven Testing:** Do NOT blindly test every public method or simple data accessor. Focus testing effort entirely on areas of the code containing complex logic or where the risk of bugs is highest.
*   **Incomplete Over None:** It is better to write and run incomplete tests than to write no tests at all. Do not let the fear of missing a bug prevent the creation of tests for the most common bugs.
*   **Strictly Fresh Fixtures:** The AI MUST NEVER create a shared mutable fixture in an outer scope. Fixtures MUST be re-instantiated before every test using setup blocks (e.g., `beforeEach`).
*   **Single Verification Preference:** The AI MUST aim to write only a single verify statement (assertion) per test block (`it` clause). If a test fails on the first assertion, subsequent assertions are skipped, hiding valuable debugging information. Exceptions are allowed only if the properties being asserted are tightly coupled.
*   **Probe the Boundaries:** After writing the "happy path" tests, the AI MUST actively play the role of an enemy to the code. Write tests that feed empty arrays, zeroes, negative values, and empty strings to the functions.
*   **Bug Report Protocol:** When instructed to fix a reported bug, the AI MUST first write a unit test that clearly exposes the defect. Only after the test is written and fails should the AI implement the fix.
*   **Separate Business Logic:** When designing architecture, strictly separate business logic from user interface, persistence, and external service interactions to make the logic easily testable.
*   **Coverage is not Quality:** Use test coverage solely to identify untested areas of the code, not to assess the objective quality of the test suite. Quality is determined by the confidence that any introduced defect will trigger a test failure.

## @Workflow
1.  **Identify Target & Setup:** Determine the high-risk logic to be tested. Initialize a Fresh Fixture using a setup block (e.g., `beforeEach`) to ensure complete isolation.
2.  **Happy Path Execution:** Write the test by exercising the fixture and verifying the expected output (Setup-Exercise-Verify).
3.  **Failure Verification:** Inject a deliberate fault into the source code being tested. Run the test to confirm it fails and produces a clear error message. Revert the fault to make the test pass.
4.  **Boundary Probing:** Write additional tests specifically targeting the boundary conditions of the inputs (e.g., what happens if the demand is negative, or if the producers array is empty?).
5.  **Refactor:** Once the test suite is green, perform any required refactorings confidently. If the bar turns red, revert the last small step and try again.
6.  **Bug Handling:** If a bug is identified, write a test that fails due to the bug. Fix the implementation until the test passes.

## @Examples (Do's and Don'ts)

### Fixture Instantiation
**[DO]** Use a setup block to create a Fresh Fixture for every test execution.
```javascript
describe('province', function() {
  let asia;
  beforeEach(function() {
    asia = new Province(sampleProvinceData());
  });

  it('shortfall', function() {
    expect(asia.shortfall).equal(5);
  });

  it('profit', function() {
    expect(asia.profit).equal(230);
  });
});
```

**[DON'T]** Declare a shared fixture in the outer scope, which will cause test interaction and intermittent failures if mutated.
```javascript
describe('province', function() {
  const asia = new Province(sampleProvinceData()); // ANTI-PATTERN: Shared Fixture

  it('shortfall', function() {
    expect(asia.shortfall).equal(5);
  });
  
  it('change production', function() {
    asia.producers[0].production = 20; // This mutation bleeds into other tests
    expect(asia.shortfall).equal(-6);
  });
});
```

### Probing Boundaries
**[DO]** Actively seek out edge cases and write explicit tests for them to see how the system reacts.
```javascript
describe('province boundary conditions', function() {
  let asia;
  beforeEach(function() {
    asia = new Province(sampleProvinceData());
  });

  it('zero demand', function() {
    asia.demand = 0;
    expect(asia.shortfall).equal(-25);
    expect(asia.profit).equal(0);
  });

  it('negative demand', function() {
    asia.demand = -1;
    expect(asia.shortfall).equal(-26);
    expect(asia.profit).equal(-10);
  });

  it('empty string demand', function() {
    asia.demand = "";
    expect(asia.shortfall).NaN;
    expect(asia.profit).NaN;
  });
});
```

**[DON'T]** Only test the "happy path" where inputs are perfectly formatted and expected, ignoring how the system behaves when empty or zero values are injected.

### Assertion Strategy
**[DO]** Keep verification steps focused, ideally testing one behavior per block so that one failure does not mask another.
```javascript
it('calculates shortfall correctly when production changes', function() {
  asia.producers[0].production = 20;
  expect(asia.shortfall).equal(-6);
});

it('calculates profit correctly when production changes', function() {
  asia.producers[0].production = 20;
  expect(asia.profit).equal(292);
});
```

**[DON'T]** Chain dozens of unrelated assertions in a single test block, which turns the test into a brittle script where the first failure prevents the rest from being evaluated.