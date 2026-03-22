# @Domain
These rules MUST trigger whenever the AI is tasked with writing, modifying, or analyzing tests, setting up testing frameworks, refactoring code that requires test coverage, or fixing reported bugs in a codebase.

# @Vocabulary
*   **Self-Testing Code**: Code accompanied by a suite of fully automated tests that check their own results, serving as a powerful bug detector.
*   **Fixture**: The baseline state, data, and objects required to run a test.
*   **Shared Fixture**: An anti-pattern where the same instance of a fixture is mutated and shared across multiple tests, leading to interacting tests and nondeterminism.
*   **Fresh Fixture**: A fixture that is recreated from scratch for every single test (e.g., using `beforeEach`), ensuring complete test isolation.
*   **Setup-Exercise-Verify / Arrange-Act-Assert / Given-When-Then**: The standard three-phase structural pattern for writing a test.
*   **Teardown**: The implicit or explicit fourth phase of a test that removes the fixture between tests to prevent interactions.
*   **Boundary Conditions**: Edge cases (e.g., empty collections, zeroes, negative numbers, empty strings) where the code is most likely to fail.
*   **Error vs. Failure**: A *failure* is a verification step that evaluates to false (expected vs. actual mismatch). An *error* is an unhandled exception raised during the setup or exercise phases before verification occurs.
*   **Risk-Driven Testing**: The practice of focusing testing efforts only on areas of the code where bugs are most likely to occur, rather than aiming for arbitrary 100% metric coverage.

# @Objectives
*   Build reliable, fully automated, self-checking test suites that drastically reduce debugging time.
*   Ensure absolute test isolation and determinism by strictly avoiding shared mutable fixtures.
*   Structure tests logically to clearly communicate the setup, the action, and the expected outcome.
*   Adopt an "enemy mindset" to proactively target and break code using boundary conditions.
*   Prevent regression by ensuring any reported bug is captured by a failing test *before* the fix is applied.

# @Guidelines

### Test Design and Strategy
*   **Self-Checking Results**: The AI MUST write tests that programmatically verify their own results (using assertion libraries like Chai, JUnit, etc.). Tests MUST NEVER rely on printing output to the console for manual human inspection.
*   **Risk-Driven Focus**: The AI MUST focus testing on complex logic and areas most susceptible to bugs.
*   **Ignore Simple Accessors**: The AI MUST NOT write tests for simple accessors (getters/setters) that merely read or write a field without additional logic.
*   **Separation of Concerns**: The AI MUST separate business logic from UI, persistence, or external service interactions to make the logic easily testable.
*   **Coverage as a Tool, Not a Goal**: The AI MUST use test coverage metrics only to identify untested areas, NEVER as a subjective measure of test suite quality. The true measure of quality is confidence that a defect will trigger a failure.

### Fixture Management
*   **Mandatory Fresh Fixtures**: The AI MUST create a fresh fixture for every test run (e.g., instantiating objects inside a `beforeEach` block).
*   **No Shared Mutable Fixtures**: The AI MUST NOT declare fixture objects as constants or variables in an outer scope (e.g., at the `describe` level) if those objects will be mutated by individual tests.
*   **Implicit Teardown**: By utilizing fresh fixtures in `beforeEach` blocks, the AI relies on the testing framework to implicitly tear down state. Explicit teardown is only required for slow, shared, truly immutable external resources.

### Test Structure
*   **Three-Phase Structure**: The AI MUST structure every test clearly into Setup (instantiate fixture), Exercise (modify or execute target code), and Verify (assert the result).
*   **Single Verification Rule**: As a general rule, the AI SHOULD place only a single verification (assertion) statement in each test (`it`) block. If a test fails on the first verification, it masks subsequent verifications. Grouping is only permitted if the verifications are exceptionally closely related.

### Boundary and Error Testing
*   **Enemy Mindset**: The AI MUST actively attempt to break the code by probing boundary conditions.
*   **Required Boundaries**: The AI MUST test empty collections, the number `0`, negative numbers, empty strings, and `null`/`undefined` inputs where applicable.
*   **Error Handling**: If a test triggers an unhandled exception (an "error" rather than a "failure"), the AI MUST evaluate if the input came from a trusted internal source (leave as is or add an assertion) or an external untrusted source (add validation and test the validation).

### Bug Fixing Protocol
*   **Test-First Bug Fixing**: When presented with a bug report, the AI MUST FIRST write a unit test that explicitly exposes the bug (the test must fail). The AI MUST NOT fix the bug until the failing test is written and confirmed to fail.

# @Workflow
When adding tests to a new or existing codebase, the AI MUST follow this algorithmic process:

1.  **Isolate Logic**: Identify the pure business logic decoupled from UI or database connections.
2.  **Establish Fresh Fixture**: Create a `beforeEach` block (or language equivalent) to instantiate the default state/data required for the test suite.
3.  **Implement Setup-Exercise-Verify**:
    *   Write the test using the fresh fixture.
    *   Perform the action.
    *   *Placeholder Pattern*: If the expected result is complex/unknown, initially write a placeholder value in the assertion. Run the test, observe the actual output, verify the actual output by hand/logic, and replace the placeholder with the actual value.
4.  **Inject and Revert Fault**:
    *   Temporarily inject a deliberate fault into the production code being tested.
    *   Run the test and VERIFY that the test FAILS. (This proves the test is actually checking the right thing).
    *   Revert the injected fault and ensure the test passes (turns green) again.
5.  **Extract Duplication**: Scan the test code for duplication. If multiple tests require the same setup logic, move it into the `beforeEach` block.
6.  **Probe Boundaries**: Generate additional test blocks specifically targeting the boundary conditions of the newly tested code (empty inputs, zeroes, negatives).

# @Examples (Do's and Don'ts)

### Fixture Management
**[DO]** Use fresh fixtures for every test to guarantee isolation.
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

**[DON'T]** Use shared fixtures that can be mutated, causing test bleed and nondeterminism.
```javascript
describe('province', function() {
  // DON'T DO THIS: Shared fixture will cause tests to interact if mutated
  const asia = new Province(sampleProvinceData()); 

  it('shortfall', function() {
    expect(asia.shortfall).equal(5);
  });

  it('change production', function() {
    asia.producers[0].production = 20; // This mutates the shared fixture!
    expect(asia.shortfall).equal(-6);
  });
});
```

### Verification Density
**[DO]** Separate verifications into distinct tests to ensure one failure doesn't hide another.
```javascript
it('zero demand shortfall', function() {
  asia.demand = 0;
  expect(asia.shortfall).equal(-25);
});

it('zero demand profit', function() {
  asia.demand = 0;
  expect(asia.profit).equal(0);
});
```

**[DON'T]** Cram multiple unrelated assertions into a single test block.
```javascript
it('handles zero demand', function() {
  asia.demand = 0;
  expect(asia.shortfall).equal(-25); // If this fails, the next line is never executed
  expect(asia.profit).equal(0);
  expect(asia.producers.length).equal(3);
});
```

### Bug Fixing Process
**[DO]** Write a failing test that reproduces the bug *before* touching the production code.
```javascript
// 1. Write the test that proves the bug exists (e.g., negative demand causes NaN)
it('negative demand handles gracefully', function() {
  asia.demand = -1;
  expect(asia.profit).to.not.be.NaN; 
});
// 2. Run the test (it fails).
// 3. Fix the production code.
// 4. Run the test (it passes).
```

**[DON'T]** Immediately modify the production code to fix a reported bug without capturing the failure in a self-checking test first.

### Testing Targets
**[DO]** Focus tests on complex domain logic, derived values, and boundary edge-cases.
```javascript
it('empty string demand results in NaN', function() {
  asia.demand = "";
  expect(asia.shortfall).NaN;
});
```

**[DON'T]** Waste effort writing tests for dumb data holders or simple accessors.
```javascript
// DON'T DO THIS: Testing a simple getter/setter adds no value
it('sets and gets name', function() {
  const p = new Producer();
  p.name = "Byzantium";
  expect(p.name).equal("Byzantium");
});
```