@Domain
JavaScript and Node.js Automated Testing. Triggered when the user requests to create, refactor, debug, or evaluate test suites, specifically using the Jest testing framework, or when setting up test doubles, analyzing code coverage, or asserting application state.

@Vocabulary
- **Test Double:** An overarching term for objects used to modify and replace parts of an application to ease or enable testing (includes Mocks, Stubs, and Spies).
- **Spy:** A test double that records data related to the usage of a function (arguments, call count) without interfering in its original implementation (e.g., `jest.spyOn`).
- **Stub:** A test double that replaces the original implementation of a function, returning canned responses or alternative implementations (e.g., `jest.fn()`, `.mockImplementation()`).
- **Mock:** A test double that replaces a function's behavior with preprogrammed expectations. In Jest parlance, usually refers to module replacements via `jest.mock()`.
- **Manual Mock:** A mock defined in a `__mocks__` directory adjacent to the mocked module to automatically resolve imports to the test double.
- **Atomicity:** The principle that a test must be capable of running independently, producing the exact same results whether run in isolation or among a thousand other tests.
- **Flaky Test:** A test that yields different results (pass/fail) across multiple runs despite the unit under test remaining unchanged.
- **Assertion:** A verification step checking if the actual output matches the expected output.
- **Tight Assertion:** An assertion that allows only a single exact result to pass (e.g., `toBe(2)`).
- **Loose Assertion:** An assertion that allows a broad range of values to pass (e.g., `typeof number`, `toBeGreaterThan(1)`).
- **Asymmetric Matcher:** A matcher that allows tight validation on most of an object while permitting loose validation on specific, unpredictable fields (e.g., `expect.any(Date)`).
- **Circular Assertion:** An anti-pattern where the expected result is generated using the exact same application code/function being tested.
- **Branch Coverage:** A code coverage metric indicating how many execution paths (branches) tests have evaluated compared to total possible paths.

@Objectives
- Generate tests that break ONLY when the application misbehaves, while being sensitive enough to catch genuine bugs.
- Architect test suites that provide pinpoint, decipherable feedback indicating precisely what failed and why.
- Balance testing costs by minimizing redundancy, avoiding over-mocking, and prioritizing Integration Tests over overly complex isolated Unit Tests.
- Ensure 100% test atomicity and determinism across concurrent and sequential test runs.

@Guidelines

**Test Suite Organization & Atomicity**
- The AI MUST group related tests and their specific helper functions inside `describe` blocks. Do not pollute the global file scope with helpers or variables used by only a subset of tests.
- The AI MUST scope lifecycle hooks (`beforeEach`, `beforeAll`, `afterEach`, `afterAll`) to the most specific `describe` block possible. 
- The AI MUST guarantee test atomicity. Tests must not depend on the execution of prior tests. Use `beforeEach` or inline state resets to guarantee a pristine initial state.
- The AI MUST break down tests so they assert a single aspect of the unit under test per `it`/`test` block, preventing multi-assertion failures from masking subsequent errors.
- If configuring global setups (e.g., database spin-ups), the AI MUST use `globalSetup` and `globalTeardown` in `jest.config.js` rather than repeating heavy setups in individual test files.
- If tests share a mutable resource (like a database or file) and parallel execution causes flakiness, the AI MUST recommend running tests sequentially (using `--runInBand`) or dynamically allocating isolated resources per worker thread.

**Writing Good Assertions**
- The AI MUST write "Tight Assertions" (e.g., `toBe()`, `toEqual()`). AVOID "Loose Assertions" (e.g., checking `typeof`, `toBeGreaterThan`, or negated assertions like `not.toBe()`) unless verifying true randomness.
- The AI MUST use "Asymmetric Matchers" (e.g., `expect.any(Date)`) specifically for unpredictable fields within an otherwise predictable object.
- The AI MUST absolutely AVOID "Circular Assertions". Never use the function under test to calculate the expected assertion value. Always hardcode the expected literal or use a completely isolated utility.
- When asserting that a function throws an error, the AI MUST use `expect(() => fn()).toThrow()` rather than manually wrapping the call in a `try/catch` block.
- If a manual `try/catch` block is entirely unavoidable in a test, the AI MUST explicitly declare `expect.hasAssertions()` or `expect.assertions(n)` at the top of the test to prevent the test from falsely passing if the error is never thrown.
- The AI MUST utilize custom matchers (like `jest-extended`) to produce readable failure diffs (e.g., use `expect(date).toBeBefore(otherDate)` instead of `expect(date < otherDate).toBe(true)`).

**Mocks, Stubs, and Spies**
- The AI MUST use a Spy (`jest.spyOn`) when it needs to verify a function's execution (arguments, call count) but wants the original application logic to execute.
- The AI MUST use a Stub (`mockImplementation`, `mockReturnValue`) to prevent a function from executing (e.g., to silence console logs or bypass external side effects).
- The AI MUST clear test double state between tests to prevent call counts/arguments from leaking. Use `mockClear()` (to erase records but keep the double), `mockReset()` (to erase records and canned behavior), or `mockRestore()` (to destroy the double entirely). Alternatively, recommend `clearMocks: true` in `jest.config.js`.
- When spying on directly imported module methods (where reassignments break), the AI MUST use `jest.mock("module_name")` to replace the module.
- If mocking a module but requiring some of its original implementations, the AI MUST use `jest.requireActual("module_name")` and merge it with the mocked methods.

**Choosing What to Test**
- The AI MUST NOT write tests targeting third-party software behavior (e.g., testing if an ORM actually inserted data into a DB instance). Testing third-party software is the library author's job.
- When deciding whether to mock a dependency: If creating the test double is overly complex, error-prone, or requires replicating extensive library logic, the AI MUST skip the mock and write an Integration Test using the real dependency (e.g., a real test database).
- When in doubt about test scope, the AI MUST default to Integration Tests. They offer the best balance of reliable quality guarantees, speed, and cost, avoiding the fragility of over-mocked unit tests and the slowness of end-to-end GUI tests.

**Code Coverage**
- The AI MUST prioritize Branch Coverage. Covering every statement is insufficient if all logical branches (e.g., `if`/`else` defaults, short-circuit evaluations) are not explicitly evaluated.
- The AI MUST NOT assume 100% coverage equals bug-free code. The AI MUST proactively generate test cases for edge-case inputs (e.g., `NaN`, `null`, boundary numbers) even if coverage is already fully reported.

@Workflow
1. **Determine Test Scope & Dependencies:** Evaluate if the unit under test uses complex third-party dependencies. If yes, default to an integration approach (no mocking). If it relies on unpredictable/uncontrollable factors (e.g., random numbers, time), prepare to use Stubs/Fake Timers.
2. **Setup Isolation:** Encapsulate the target within a `describe` block. Implement `beforeEach` hooks to clear database tables, reset state maps, and execute `mockClear()` on any shared test doubles to guarantee Atomicity.
3. **Implement the 3 A's Pattern:** 
   - **Arrange:** Set up the isolated initial state (seed data, initialize variables).
   - **Act:** Execute the single specific behavior of the unit under test.
   - **Assert:** Verify the outcome.
4. **Refine Assertions:** Ensure assertions are Tight. If comparing objects with timestamps or UUIDs, inject Asymmetric Matchers. If the code throws, apply `.toThrow()`. Remove any Circular Assertions.
5. **Break Down Granularity:** If the test contains multiple sequential acts and asserts targeting different features, split it into multiple, smaller `it()` blocks with shared `beforeEach` setups to ensure precise feedback on failure.

@Examples

**[DO] - Tight Assertions with Asymmetric Matchers**
```javascript
test("returns inventory contents with generated timestamp", () => {
  inventory.set("cheesecake", 1);
  const result = getInventory();
  expect(result).toEqual({
    cheesecake: 1,
    generatedAt: expect.any(Date) // [DO] Use asymmetric matcher for unpredictable fields
  });
});
```

**[DON'T] - Loose and Negated Assertions**
```javascript
test("returns inventory contents", () => {
  const result = getInventory();
  expect(typeof result.generatedAt).toBe("object"); // [DON'T] Too loose
  expect(result.cheesecake).not.toBe(2); // [DON'T] Negated assertions allow virtually any incorrect value to pass
});
```

**[DO] - Correct Error Handling Assertion**
```javascript
test("cancels operation for invalid quantities", () => {
  // [DO] Use toThrow for clean, concise error assertions
  expect(() => addToInventory("cheesecake", "not a number")).toThrow();
  expect(inventory.get("cheesecake")).toBe(0);
});
```

**[DON'T] - Unprotected Try/Catch Assertion**
```javascript
test("cancels operation for invalid quantities", () => {
  // [DON'T] If addToInventory doesn't throw, this test falsely passes
  try {
    addToInventory("cheesecake", "not a number");
  } catch (e) {
    expect(inventory.get("cheesecake")).toBe(0);
  }
});
```

**[DO] - Hardcoded Expected Results (Avoiding Circular Assertions)**
```javascript
test("fetching inventory", async () => {
  inventory.set("cheesecake", 1);
  const response = await sendGetInventoryRequest();
  
  // [DO] Hardcode the expected state.
  const expected = { cheesecake: 1, generatedAt: expect.any(String) };
  expect(await response.json()).toEqual(expected);
});
```

**[DON'T] - Circular Assertions**
```javascript
test("fetching inventory", async () => {
  inventory.set("cheesecake", 1);
  const response = await sendGetInventoryRequest();
  
  // [DON'T] Reusing the application code to generate the test expectation means bugs in getInventory() are invisible.
  const expected = { ...getInventory(), generatedAt: expect.any(String) };
  expect(await response.json()).toEqual(expected);
});
```

**[DO] - Partial Mocking of Modules**
```javascript
// [DO] Retain original functionality while replacing only what's necessary
jest.mock("./logger", () => {
  const originalLogger = jest.requireActual("./logger");
  return {
    ...originalLogger,
    logInfo: jest.fn() // Only stub the side-effect
  };
});
```