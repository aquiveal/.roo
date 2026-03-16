# @Domain
These rules MUST be triggered whenever the AI is tasked with writing automated JavaScript tests, designing testing strategies, implementing bug fixes that require test coverage, setting up test environments (particularly databases), or evaluating whether to write tests for a specific project based on its lifespan. 

# @Vocabulary
- **Automated Test**: A program that automates the task of testing software by interfacing with an application to perform actions and compare the actual result with a previously defined expected output.
- **Test Database**: A fully separated, isolated database instance strictly used for testing to prevent data loss, prevent inconsistent states, and ensure customers' actions do not interfere with test results.
- **Predictability**: The resulting state of a development process when the distance (in time and code surface) between writing code and receiving feedback is minimized, effectively preventing unexpected behavior.
- **Reproducibility**: The capability of automated tests to execute the exact same series of steps without human error, specifically designed to capture repetitive edge cases (e.g., `-1`, `NaN`).
- **Testing Dividends**: The concept that automated tests have an up-front cost but drop the ongoing execution effort to near zero, yielding positive ROI primarily for long-term projects.

# @Objectives
- Replace manual verification and human drudgery with precise, machine-executable code.
- Prove that specific bugs are no longer present by explicitly reproducing the exact steps that caused them.
- Provide the fastest, most precise feedback possible to make the development workflow predictable.
- Guarantee that tests serve as the ultimate, up-to-date documentation for how the codebase operates and how developers should collaborate.

# @Guidelines
- **Failing Tests First:** When fixing a bug, the AI MUST write a test that reproduces the bug and verify that it fails before implementing the fix. The only useful test is one that fails when the application doesn't work.
- **Target Specific Bugs:** When writing tests, the AI MUST NOT attempt to "prove the software works" absolutely. Instead, the AI MUST target specific inputs, edge cases (e.g., `NaN`, `-1`), and known failure modes to prove that specific bugs are absent.
- **Database Isolation:** When a test interacts with data, the AI MUST configure and utilize a completely separate test database. The AI MUST NEVER pollute production or standard development databases with testing data.
- **Direct Function Invocation:** When testing a specific feature (e.g., tracking an order), the AI MUST isolate the test by calling the target function directly rather than routing the test through unrelated application layers (e.g., UI or checkout flows) to ensure precise, localized feedback.
- **Tests as Documentation:** When generating test suites, the AI MUST structure and name the tests clearly so they act as up-to-date API documentation and integration contracts for other developers.
- **ROI Assessment:** When the user specifies a short-term project (e.g., a hackathon prototype), the AI MUST advise against heavy automated testing, as the project will not live long enough to reap the testing dividends. Conversely, for long-term projects, the AI MUST heavily enforce automated testing.

# @Workflow
When tasked with writing automated tests or fixing a bug with test coverage, the AI MUST follow this algorithmic process:
1. **Action Flow Identification:** Analyze how a human user would trigger the feature or bug, and map this exact action flow to programmatic steps.
2. **Environment Isolation:** Ensure the test environment is fully controlled (e.g., route connections to a dedicated test database, separate from production).
3. **Scenario Setup:** Write the code to instantiate the exact initial state required to reproduce the scenario or bug.
4. **Failing Assertion Creation:** Write the execution and verification steps (the assertion). If this is a bug fix, explicitly note that this test MUST fail against the current broken code.
5. **Code Implementation:** Implement the application logic or bug fix to correct the behavior.
6. **Verification:** Confirm that the previously failing test now passes, proving the specific bug is eradicated and the system is predictable.

# @Examples (Do's and Don'ts)

### Test Database Isolation
**[DO]**
```javascript
// Ensure tests run against an isolated test database
const db = require('database-client');
db.connect('mongodb://localhost/testing_database_isolated');

// Set up clean state
await db.clear('inventory');
await db.insert('inventory', { item: 'macaroon', quantity: 0 });
```

**[DON'T]**
```javascript
// Anti-pattern: Using the main production/dev database for tests
const db = require('database-client');
db.connect(process.env.PROD_DB_URL); 

// Anti-pattern: Risking production data loss or test interference from live users
await db.clear('inventory'); 
```

### Writing the Test Before the Bug Fix
**[DO]**
```javascript
// 1. Write the test that reproduces the bug (e.g., adding out-of-stock items)
test('Prevents adding out-of-stock macaroons to cart', () => {
    const cart = new Cart();
    inventory.set('macaroon', 0);
    cart.addToCart('macaroon', 10000); // This should currently fail/throw
    expect(cart.contents).not.toContain('macaroon');
});
// 2. ONLY THEN implement the inventory check inside `addToCart`.
```

**[DON'T]**
```javascript
// Anti-pattern: Fixing the bug in the application code first
function addToCart(item, qty) {
    if (inventory.get(item) < qty) throw new Error('Out of stock');
    // ...
}
// And then writing a test that always passes, never proving the test could catch the initial failure.
```

### Direct Function Invocation for Predictability
**[DO]**
```javascript
// Isolate the exact function being tested for precise feedback
const trackOrder = require('./trackOrder');

test('Tracking returns the correct status for a dispatched order', () => {
    const status = trackOrder('order_123');
    expect(status).toBe('dispatched');
});
```

**[DON'T]**
```javascript
// Anti-pattern: Writing a convoluted test that touches the whole app to test one function
test('Tracking an order works', () => {
    // Too much setup, bugs could hide anywhere in here
    server.start();
    browser.open();
    browser.click('Add to Cart');
    browser.click('Checkout');
    browser.fillCreditCard();
    // By the time we test tracking, 1000 lines of code have executed
    browser.click('Track Order');
    expect(browser.getText()).toBe('dispatched');
});
```

### Reproducibility via Edge Cases
**[DO]**
```javascript
// Test extreme, machine-specific edge cases humans forget
test('Handles invalid macaroon quantities reliably', () => {
    const cart = new Cart();
    cart.addToCart('macaroon', -1);
    cart.addToCart('macaroon', NaN);
    expect(cart.total).toBe(0);
});
```

**[DON'T]**
```javascript
// Anti-pattern: Only testing the "happy path" a human would check manually
test('Adds macaroon', () => {
    const cart = new Cart();
    cart.addToCart('macaroon', 1);
    expect(cart.total).toBe(1);
});
```