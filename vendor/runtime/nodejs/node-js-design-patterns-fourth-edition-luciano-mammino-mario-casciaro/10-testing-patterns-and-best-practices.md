@Domain
Triggered when the user requests the creation, modification, or review of test files (e.g., `*.test.js`, `*.test.ts`, `*-test.js`), test configurations, Playwright end-to-end (E2E) scripts, integration tests, or tasks involving test runners, mocking, and code coverage in a Node.js environment.

@Vocabulary
- **System Under Test (SUT)**: The specific component, module, function, or application being evaluated in a test case.
- **AAA (Arrange, Act, Assert)**: A structured pattern for writing tests. Arrange (set up preconditions), Act (execute the SUT), Assert (verify the results).
- **Code Coverage**: A metric indicating the percentage of code executed during tests (line, branch, statement, class, function). High coverage does not guarantee high test quality.
- **Test Doubles**: Stand-in components used to isolate the SUT from its dependencies. Includes Stubs, Spies, and Mocks.
- **Stub**: A test double providing predetermined, static responses to method calls, ignoring context.
- **Spy**: A test double that retains stub-like behavior but records interactions (call count, arguments, execution order) for later inspection.
- **Mock**: A strict test double that combines stub-like responses with predefined expectations, failing the test if the exact interaction rules are not met.
- **Test-Driven Development (TDD)**: A development methodology based on a Red (failing test), Green (passing test), Refactor cycle.
- **Behavior-Driven Development (BDD)**: Executable specifications written in human-readable format (e.g., Gherkin with Given/When/Then) to bridge technical and business contexts.
- **Continuous Integration (CI)**: The practice of merging code frequently, triggering automated builds and tests.
- **Continuous Delivery / Deployment (CD)**: Automating the release process to staging/production. Deployment is fully automated; Delivery requires a manual approval step.
- **Testing Pyramid**: A strategy advocating for a large base of fast Unit Tests, a middle layer of Integration Tests, and a small top layer of E2E Tests.
- **Testing Trophy**: An alternative testing strategy emphasizing a heavier reliance on integration tests for the highest return on investment.
- **Black-box Testing**: Testing the application as an opaque system without knowledge of its internals.
- **White-box Testing**: Testing leveraging knowledge of implementation details.
- **Fuzz Testing**: Bombarding the system with chaotic or malformed inputs to uncover crashes.
- **Property Testing**: Defining invariants and generating diverse inputs to verify them.
- **Mutation Testing**: Introducing small bugs ("mutants") into code to evaluate the effectiveness of the test suite.
- **TestContext (`t`)**: The object automatically passed by the Node.js test runner into the function under test (FUT), providing methods like `t.test`, `t.skip`, `t.mock`.
- **Web-first Assertions**: Playwright assertions (e.g., `toBeVisible()`) that automatically poll and wait for a condition to become true up to a timeout.

@Objectives
- Structure all tests strictly using the Arrange-Act-Assert (AAA) pattern.
- Utilize the native Node.js test runner (`node:test`) and strict assertions (`node:assert/strict`) over third-party alternatives where possible.
- Favor Dependency Injection (DI) to isolate dependencies over global module mocking.
- Isolate test boundaries effectively by utilizing appropriate test doubles (Stubs, Spies, Mocks) and explicitly resetting global states between tests.
- Write E2E tests from the user's perspective (Black-box) utilizing Playwright's automatic waiting and web-first assertions, avoiding arbitrary manual timeouts.

@Guidelines

### 1. Test Architecture & Strategy
- The AI MUST balance test types according to the Testing Pyramid: write many granular Unit Tests, fewer but robust Integration Tests, and a selective handful of E2E Tests focusing on high-stakes user workflows.
- For Unit Tests: Isolate the SUT completely from external dependencies (databases, APIs, filesystem).
- For Integration Tests: Verify synergy between components. Use realistic environments (e.g., in-memory SQLite databases) but restore the system to a clean state before each test.
- For E2E Tests: Focus on user-facing behavior. Do not couple to code internals. Use production-like environments or mock network responses at the browser level.

### 2. Node.js Native Test Runner (`node:test`)
- The AI MUST use `node:test` for test declarations: `import { test, suite, describe, it, before, after, beforeEach, afterEach, mock } from 'node:test'`.
- Tests MUST be written using the `*.test.js`, `*.test.ts`, or `test-*.js` naming conventions.
- Test implementations (Function Under Test - FUT) MUST signal completion through one of three ways:
  1. Synchronous completion (throws on failure).
  2. Returning a Promise / using `async/await` (rejects on failure).
  3. Using a `done` callback (passing an error triggers failure).
- **CRITICAL**: The AI MUST NEVER use both a `done` callback and return a Promise in the same test function.
- The AI MUST use `t.test()` to define subtests for grouping related assertions or creating parameterized tests using loops.

### 3. Assertions
- The AI MUST import assertions from the strict module: `import { equal, deepEqual } from 'node:assert/strict'`. NEVER use the non-strict `node:assert`.
- Use `equal` for primitives and strict object identity checks.
- Use `deepEqual` strictly for comparing object structural equivalence.
- Provide descriptive custom error messages as the third parameter to assertion functions where it aids debugging.

### 4. Concurrency and Test Isolation
- Subtests MUST be executed concurrently by passing `{ concurrency: true }` to the `test` or `suite` options, EXCEPT when testing constraints prevent it.
- **CRITICAL**: The AI MUST explicitly disable concurrency (`{ concurrency: false }`) for the entire suite when utilizing `t.mock.module()`, as module mocks mutate the global environment and will cross-contaminate concurrent tests.

### 5. Mocking Dependencies
- **Spies**: The AI MUST use `mock.fn()` to wrap tasks or create spy functions to track execution (e.g., `mock.callCount()`), rather than manually managing boolean flags or resolver promises.
- **HTTP Mocking (Built-in)**: Use `t.mock.method(global, 'fetch', ...)` to mock global fetches scoped safely to a specific test.
- **HTTP Mocking (Undici)**: When using Undici, instantiate a `MockAgent`, call `agent.disableNetConnect()`, and use `setGlobalDispatcher(agent)`. The AI MUST extract the agent setup to `beforeEach` and restore the original dispatcher in `afterEach`.
- **Module Mocking (`t.mock.module`)**: When mocking built-in or third-party modules:
  - You MUST set `{ cache: false }`.
  - You MUST import the SUT *dynamically* (`await import('./module.js')`) **AFTER** applying the mock. Standard top-level imports execute before the mock is registered and will fail to use the mocked module.
- **Dependency Injection (Preferred)**: The AI MUST prefer refactoring the SUT to accept dependencies as arguments (Dependency Injection) instead of mocking global imports. DI eliminates the need for dynamic imports, avoids global state mutation, and allows test concurrency.

### 6. Integration Testing
- For database integration, prefer lightweight, in-memory databases (e.g., SQLite with `:memory:`) to ensure speed, isolation, and idempotent schema initialization via `CREATE TABLE IF NOT EXISTS`.
- When testing Fastify (or similar frameworks), use the framework's injection mechanisms (e.g., `app.inject()`) to simulate HTTP requests without binding to a local port.

### 7. End-to-End (E2E) Testing with Playwright
- The AI MUST use Playwright (`@playwright/test`) for E2E testing.
- Rely on Playwright’s automatic actionability checks. The AI MUST NOT use manual `waitForTimeout` or arbitrary sleep mechanisms.
- **Locators**: Use resilient, user-centric locators such as `page.getByRole()`, `page.getByLabel()`, `page.getByText()`, and `page.getByTestId()`.
- **Web-First Assertions**: The AI MUST use asynchronous assertions (e.g., `await expect(locator).toBeVisible()`) that automatically poll until the condition is met or the timeout is reached.
- **State collision**: Seed unique data for form inputs (e.g., using `Date.now()`) to avoid unique constraint violations across test runs.
- **Security via Text**: When verifying or manipulating DOM content directly, prefer `textContent` over `innerHTML` to mitigate XSS vulnerabilities.

### 8. Code Coverage and Filtering
- Utilize the `--experimental-test-coverage` (or `--test-coverage`) flag for coverage.
- To intentionally ignore coverage on specific code blocks (e.g., unreachable edge cases), the AI MUST wrap the block using `/* node:coverage disable */` and `/* node:coverage enable */` rather than single-line ignores, as auto-formatters can shift code across multiple lines.
- Filter tests programmatically during debugging by utilizing the `skip: true`, `only: true`, or `todo: true` options within the test configuration, or by calling `t.skip()`, `t.todo()`.

@Workflow
When generating or modifying tests, the AI MUST follow this process:
1. **Analyze SUT**: Determine the scope of the test (Unit, Integration, or E2E). Identify all dependencies and side effects.
2. **Determine Isolation Strategy**: If the SUT has dependencies, refactor for Dependency Injection if permitted. If DI is not possible, plan local module mocks (`t.mock.module`) or HTTP mocks (`MockAgent`).
3. **Structure via AAA**: Write the test skeleton.
   - **Arrange**: Initialize inputs, set up mocks, initialize in-memory databases, define expected outcomes.
   - **Act**: Execute the SUT dynamically if modules are mocked, or normally if DI is used.
   - **Assert**: Verify return values, mock call counts, and side effects using strict assertions.
4. **Configure Test Options**: Apply `{ concurrency: true }` to suites/subtests by default, switching to `{ concurrency: false }` ONLY if global state (like `mock.module`) is manipulated.
5. **Cleanup**: Guarantee all global mocks, dispatchers, or open database connections are restored or closed in `after()` or `afterEach()` blocks.

@Examples

**[DO] Use Dependency Injection to test components concurrently and synchronously import them:**
```javascript
import assert from 'node:assert/strict'
import { suite, test } from 'node:test'
import { setImmediate } from 'node:timers/promises'
import { canPayWithVouchers } from './payments.js' // Safe top-level import

suite('canPayWithVouchers', { concurrency: true }, () => {
  test('Returns true if balance is enough', async t => {
    // Arrange
    const dbMock = {
      query: t.mock.fn(async () => {
        await setImmediate()
        return [{ balance: 10 }]
      }),
    }
    
    // Act
    const result = await canPayWithVouchers(dbMock, 'user1', 5)
    
    // Assert
    assert.equal(result, true, 'User should be able to pay')
    assert.equal(dbMock.query.mock.callCount(), 1)
  })
})
```

**[DON'T] Use static imports when mocking modules globally:**
```javascript
// DON'T DO THIS
import { saveConfig } from './saveConfig.js' // Imported BEFORE mock applies!
import { mock, test } from 'node:test'

test('Creates folder', async t => {
  t.mock.module('node:fs/promises', { /*...*/ })
  await saveConfig('./config.json', {}) // Will hit the REAL filesystem
})
```

**[DO] Use dynamic imports AFTER mocking a module and disable concurrency:**
```javascript
import assert from 'node:assert/strict'
import { mock, suite, test } from 'node:test'

suite('saveConfig', { concurrency: false }, () => { // Must be false!
  test('Creates folder', async t => {
    // Arrange
    const mockMkdir = mock.fn()
    t.mock.module('node:fs/promises', {
      cache: false,
      namedExports: { mkdir: mockMkdir, writeFile: mock.fn() }
    })
    
    // Act
    const { saveConfig } = await import('./saveConfig.js') // Imported AFTER mock
    await saveConfig('./path/to/configs/app.json', { port: 3000 })
    
    // Assert
    assert.equal(mockMkdir.mock.callCount(), 1)
  })
})
```

**[DO] Parameterize tests using loops and subtests:**
```javascript
import { equal } from 'node:assert/strict'
import { test } from 'node:test'
import { calculateTotal } from './calc.js'

test('Calculates total', { concurrency: true }, t => {
  const cases = [
    { name: 'Empty', input: [], expected: 0 },
    { name: 'Single', input: [2], expected: 2 },
  ]

  for (const { name, input, expected } of cases) {
    t.test(name, () => {
      const result = calculateTotal(input)
      equal(result, expected)
    })
  }
})
```

**[DO] Use Playwright web-first assertions and resilient locators:**
```javascript
import { test, expect } from '@playwright/test'

test('Booking flow', async ({ page }) => {
  // Act
  await page.goto('http://localhost:3000')
  await page.getByRole('link', { name: 'Sign up' }).click()
  
  const seed = Date.now().toString()
  await page.getByRole('textbox', { name: 'email' }).fill(`test${seed}@example.com`)
  await page.getByRole('button', { name: 'Create account' }).click()

  // Assert
  const badge = page.getByTestId('badge').first()
  await expect(badge).toHaveText('Active') // Web-first assertion, auto-waits
})
```

**[DON'T] Use manual timeouts in Playwright E2E tests:**
```javascript
// DON'T DO THIS
await page.getByRole('button', { name: 'Submit' }).click()
await page.waitForTimeout(2000) // Brittle and slow!
const success = await page.getByText('Success').isVisible()
```

**[DO] Disable coverage using block comments to survive auto-formatters:**
```javascript
/* node:coverage disable */
if (falsyCondition) {
  console.error('this should never happen')
}
/* node:coverage enable */
```