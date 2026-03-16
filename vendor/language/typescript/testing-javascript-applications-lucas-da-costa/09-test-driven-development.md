# @Domain
These rules trigger when implementing new features, fixing bugs, refactoring existing code, writing automated tests (unit, integration, or acceptance), designing architectures, or processing requests that explicitly mention "Test-driven development", "TDD", or "BDD" (Behavior-driven development). 

# @Vocabulary
- **TDD (Test-driven development)**: An iterative software development technique consisting of taking small incremental steps toward a solution using tests to guide the process.
- **Red, Green, Refactor**: The three-step TDD cycle. Red: write a failing test. Green: write the bare minimum code to make it pass. Refactor: improve the code design while keeping tests green.
- **Bottom-up Testing**: A testing strategy that validates the most granular, individual functions first, and then moves up toward coarser, higher-level pieces of software.
- **Top-down Testing**: A testing strategy that validates the topmost function in a dependency hierarchy first, indirectly attesting to the quality of its underlying dependencies.
- **Transitive Guarantee**: Creating a thorough test for a heavily used dependency in isolation, so that other tests depending on it only need to check if the dependency is called correctly, rather than exhaustively re-testing its behavior.
- **BDD (Behavior-driven development)**: An agile approach related to TDD that facilitates communication among stakeholders by expressing requirements in a shared, structured language.
- **Given, When, Then**: The BDD framework formula for defining specifications. *Given* describes the initial context, *When* describes the action, and *Then* describes the expected output.

# @Objectives
- Tighten the feedback loop to catch and fix mistakes as early and cheaply as possible.
- Reduce development fear and anxiety by building confidence through rigorous, step-by-step validation.
- Drive software design from a consumer-centric perspective, encouraging developers to program to an interface rather than an implementation.
- Guarantee that tests are thorough and capable of catching bugs by explicitly ensuring they fail before any application code is written.
- Balance delivery speed, maintenance costs, and test brittleness by dynamically adjusting iteration step sizes and testing strategies (Top-down vs. Bottom-up).
- Ensure continuous integration by never permitting failing tests in the codebase.
- Bridge technical and nontechnical specifications by translating business requirements into automated behavioral tests.

# @Guidelines

## The Core TDD Cycle
- The AI MUST adhere strictly to the exact order of the TDD cycle: Write a failing test -> Write application code -> Refactor.
- The AI MUST NEVER write application code without first writing a failing test that dictates the need for that code.
- The AI MUST write ONLY the bare minimum amount of code necessary to make the current failing test pass (e.g., returning a hardcoded value if that satisfies the current test). 
- The AI MUST refactor only AFTER the tests are green. During refactoring, the AI MUST NOT alter the observable behavior dictated by the tests.

## Adjusting Iteration Size
- The AI MUST dynamically adjust the size of its TDD steps based on confidence and complexity.
- **Low Confidence / High Complexity**: The AI MUST take tiny steps. Write extremely narrow tests, write minimal code to pass, and iterate frequently.
- **High Confidence / Low Complexity**: The AI MAY take larger steps. Write full-blown, comprehensive tests immediately, and write the final implementation of the function at once to increase iteration speed.

## Top-Down vs. Bottom-Up Testing Strategies
- **Choose Bottom-Up** when confidence is low, or when the unit under test is a shared dependency used by many other functions. This provides granular feedback and solid foundations but increases test overlap and maintenance cost.
- **Choose Top-Down** when confidence is high. This reduces test overlap, lowers maintenance costs, and allows for faster iteration, though it provides coarser feedback.
- The AI MUST adapt the strategy during the software lifecycle: Use Bottom-Up during implementation if needed for granular feedback, but transition to Top-Down during the maintenance phase by deleting redundant granular tests if they overlap with higher-level guarantees.

## Test-Driven Maintenance
- The AI MUST keep tests green. If a test breaks due to a codebase change, the AI MUST fix the test or roll back the code.
- The AI MUST refactor tests to ensure they serve as clear, readable documentation and usage examples for future developers.
- The AI MUST aggressively delete redundant or overlapping tests during maintenance phases. If a top-level function's test completely covers the behavior of a lower-level function, the lower-level test SHOULD be deleted if it breaks due to structural refactoring.

## When NOT to use TDD
- The AI MUST NOT apply TDD when building disposable prototypes, quick proofs of concept, or when explicitly exploring/learning a new language or framework. 
- TDD MUST be applied to all code intended to live long-term in the codebase, including legacy code refactors.

## Behavior-Driven Development (BDD)
- When writing acceptance-focused tests or translating business requirements, the AI MUST use the "Given, When, Then" structure.
- The AI MUST format BDD tests using nested `describe` blocks for the "Given" and "When" contexts, and `it` blocks for the "Then" expectations.
- The AI MUST name BDD test files using the `.spec.js` or `.spec.ts` suffix (as opposed to `.test.js`) to denote them as automated specification validators.

# @Workflow
1. **Context Evaluation**: Determine if the task is a disposable prototype/exploration. If yes, skip TDD. If no, proceed to Step 2.
2. **Strategy Selection**: Evaluate the complexity of the target.
   - If highly complex or a core shared dependency: Select *Bottom-Up*.
   - If confident and straightforward: Select *Top-Down*.
3. **Red Phase (Write Test)**: Write a test for the next smallest piece of missing functionality. 
   - If fixing a bug, write a test that reproduces the bug.
   - Run the test to verify it fails. (This ensures the test is valid and capable of catching the missing implementation/bug).
4. **Green Phase (Write Code)**: Write the absolute minimum application code required to make the test pass. Do not implement future functionality yet.
5. **Verify**: Run the test suite. If it fails, adjust the application code until it passes.
6. **Refactor Phase**: Analyze the newly passing code and the test itself. Refactor for performance, readability, and design without changing the behavior. Verify tests remain green.
7. **Expand**: Expand the test scope by adding assertions for edge cases (e.g., `null`, `undefined`, `NaN`, invalid strings) one at a time, repeating the Red-Green-Refactor cycle.
8. **Maintenance Review**: Once the feature is complete, evaluate the test suite for overlap. Delete lower-level granular tests if upper-level tests implicitly guarantee their correctness, optimizing for long-term maintenance costs.

# @Examples (Do's and Don'ts)

## TDD Cycle: Bare Minimum Code
**[DON'T]** Write the final implementation before the test demands it.
```javascript
// Test
test("calculating total values", () => {
  expect(calculateCartPrice([1, 1, 2, 3])).toBe(7);
});

// Application Code (Too far ahead of the test)
const calculateCartPrice = prices => {
  return prices.reduce((sum, price) => sum + price, 0); 
};
```

**[DO]** Write the bare minimum to make the specific test pass, forcing you to write more tests to drive the real implementation.
```javascript
// Test
test("calculating total values", () => {
  expect(calculateCartPrice([1, 1, 2, 3])).toBe(7);
});

// Application Code (Bare minimum)
const calculateCartPrice = () => 7;
```

## BDD Specification Formatting
**[DON'T]** Write unstructured, technically-focused descriptions for business logic.
```javascript
describe("orderScheduler", () => {
  it("should sort the array by size if distance is equal", () => {
     // ...
  });
});
```

**[DO]** Use the Given/When/Then structure translated into `describe` and `it` blocks for `.spec.js` files.
```javascript
describe("given there's an order for location A 2 miles east", () => {
  describe("when a bigger order is placed for location B 2 miles west", () => {
    it("places the bigger order on the top of the list", () => {
      // ...
    });
    
    it("refuses the order if it's too big", () => {
      // ...
    });
  });
});
```

## Bug Fixing Workflow
**[DON'T]** Fix the code first, then write the test.
```javascript
// 1. Fix the bug in code
const calculateDiscount = (price, discount) => {
  if (isNaN(discount)) return price; // Bug fixed
  return price - discount;
};

// 2. Write the test (You don't know if the test would have caught the bug!)
test("handling NaN", () => {
  expect(calculateDiscount(10, NaN)).toBe(10);
});
```

**[DO]** Write the failing test first, see it fail, then fix the code.
```javascript
// 1. Write the test
test("handling NaN", () => {
  expect(calculateDiscount(10, NaN)).toBe(10); 
});

// 2. Run test -> Fails (Received NaN)

// 3. Fix the bug in code
const calculateDiscount = (price, discount) => {
  return typeof discount === "number" && !isNaN(discount) 
    ? price - discount 
    : price;
};
// 4. Run test -> Passes
```