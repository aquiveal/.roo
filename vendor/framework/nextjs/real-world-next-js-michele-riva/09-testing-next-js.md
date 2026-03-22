# @Domain
This rule file is triggered when the user requests assistance with testing a Next.js application, configuring test environments, writing test suites (Unit, Integration, or End-to-End), or utilizing testing libraries such as Jest, Cypress, and `react-testing-library` within a Next.js context.

# @Vocabulary
- **Unit Testing**: Tests aimed at ensuring individual functions or components in the codebase work correctly against valid and invalid inputs.
- **End-to-End (E2E) Testing**: Tests that reproduce a typical user interaction with the application on a browser, validating user interface rendering, form submissions, and page navigation.
- **Integration Testing**: Tests ensuring that separate parts of the application (functions and modules) work cohesively together to produce correct outputs.
- **Test Runner**: A tool responsible for executing every test found in the codebase, collecting coverage, and displaying results. Exits with a non-zero code if tests fail.
- **Jest**: The primary test runner and testing framework used for Unit and Integration testing in this architecture.
- **React Testing Library (RTL)**: The library used alongside Jest to mount, render, and test the output of React components.
- **JSDOM**: A library that emulates browser features in Node.js, required for running RTL within Jest.
- **Cypress**: A testing tool that runs in Chromium-based browsers or Firefox, used exclusively for E2E and API testing in this architecture.
- **`start-server-and-test`**: A utility library used to build the server, wait for it to boot on a specific port, and automatically trigger Cypress tests.

# @Objectives
- Correctly configure the Next.js testing environment for both Jest and Cypress without interfering with Next.js built-in routing mechanisms.
- Implement robust unit and integration tests using Jest and `react-testing-library` while properly mocking external data sources.
- Execute frontend component tests within a simulated browser environment using JSDOM.
- Implement comprehensive E2E tests using Cypress that validate API responses, handle expected HTTP errors gracefully, and assert UI navigation.
- Ensure automated testing scripts safely build and boot the Next.js production server prior to running E2E test suites.

# @Guidelines

### General Testing Setup
- The AI MUST categorize tests into Unit, Integration, or End-to-End (E2E).
- The AI MUST use Jest for Unit and Integration tests.
- The AI MUST use Cypress for End-to-End (E2E) tests.

### Jest and Next.js Configuration
- The AI MUST configure Jest to use the default Next.js Babel preset to transpile modern ESNext modules. Create a `.babelrc` file in the project root containing `{"presets": ["next/babel"]}`.
- **CRITICAL**: The AI MUST NEVER place test files (files ending in `.test.js` or `.spec.js`) inside the Next.js `pages/` directory. Next.js will attempt to render them as application pages, breaking the build.
- The AI MUST place test files either next to their source files (outside of `pages/`) or grouped inside dedicated `tests/` or `cypress/integration/` directories.

### React Testing Library (RTL) Constraints
- The AI MUST add the JSDOM pragma `/** @jest-environment jsdom */` at the very top of any Jest test file that imports `@testing-library/react`. Node.js does not possess the `document` global variable required by RTL.
- The AI MUST mock external API data when testing components. The AI MUST NOT execute real network requests inside unit/integration tests. Create a separate `mock.js` file adjacent to the test file to store mock payload objects.

### Cypress (E2E) Constraints
- The AI MUST place Cypress E2E tests inside a `cypress/integration/` directory at the root level of the repository.
- The AI MUST configure Cypress by creating a `cypress.json` file in the project root containing `{"baseUrl": "http://localhost:3000"}`.
- When testing API endpoints using Cypress, the AI MUST use `cy.request`.
- When testing API endpoints that are *expected* to return a 400+ status code (e.g., testing 404 Not Found), the AI MUST pass `{ failOnStatusCode: false }` in the `cy.request` configuration object, because Cypress throws an error by default on 400+ status codes.
- When iterating over an array of responses in Cypress using the `.each()` method, the AI MUST use the `done` callback in the test definition and invoke `done()` after the assertions to handle asynchronous resolution correctly.
- The AI MUST use Chai assertions (e.g., `.to.have.keys(...)`) to validate the structure of JSON API responses in Cypress.

### Test Orchestration
- The AI MUST NOT run Cypress against the Next.js development server (`next dev`). 
- The AI MUST configure `start-server-and-test` in the `package.json` scripts to build and start the production server before running Cypress. The exact script format MUST be: `"e2e": "start-server-and-test 'yarn build && yarn start' http://localhost:3000 cypress"`.

# @Workflow
1. **Determine Test Type**: Identify if the user needs Unit/Integration testing (Jest/RTL) or E2E testing (Cypress).
2. **Configure Environment (Jest)**:
    - If Jest is required, ensure `.babelrc` contains the `"next/babel"` preset.
    - If UI components are being tested, ensure `@testing-library/react` is installed and the `/** @jest-environment jsdom */` pragma is added to the test files.
    - Verify test files are positioned securely outside of the `pages/` directory.
3. **Draft Unit/Integration Tests**:
    - Import functions or components.
    - If testing components, import mock data from a dedicated mock file.
    - Use `describe` to group tests, `test` to define the scenario, and `expect` with RTL queries (e.g., `render`, `screen.getByText`) to assert outcomes.
4. **Configure Environment (Cypress)**:
    - If E2E is required, ensure `cypress.json` is configured with the `baseUrl`.
    - Ensure `start-server-and-test` is integrated into `package.json` scripts.
5. **Draft E2E Tests**:
    - Place files in `cypress/integration/`.
    - To test APIs, use `cy.request()` and validate HTTP headers, status codes, and body keys.
    - To test navigation, use `cy.visit()`, `cy.get()`, click elements, and assert URL changes using `cy.url().should('be.equal', ...)`.

# @Examples (Do's and Don'ts)

### Test File Placement
- **[DO]** Place component tests alongside the component outside the `pages/` directory: `components/ArticleCard/tests/index.test.js`.
- **[DON'T]** Place test files inside the `pages/` routing directory: `pages/about.test.js` (This will cause Next.js to route users to `/about.test`).

### Component Testing Environment (JSDOM)
- **[DO]** Add the JSDOM pragma when using RTL:
```javascript
/**
 * @jest-environment jsdom
 */
import { render, screen } from '@testing-library/react';
import ArticleCard from '../index';
import { article } from '../tests/mock';

describe('ArticleCard', () => {
  test('Renders correctly', () => {
    render(<ArticleCard {...article} />);
    expect(screen.getByText(article.title)).toBeDefined();
  });
});
```
- **[DON'T]** Import React Testing library without the JSDOM pragma, which will crash in the Node environment:
```javascript
import { render, screen } from '@testing-library/react'; // Missing JSDOM pragma
import ArticleCard from '../index';
```

### Cypress API Error Testing
- **[DO]** explicitly disable `failOnStatusCode` when testing expected 404 API responses in Cypress:
```javascript
test('should return 404 when an article is not found', () => {
  cy.request({
    url: 'http://localhost:3000/api/article?id=unexistingID',
    failOnStatusCode: false,
  })
  .its('status')
  .should('be.equal', 404);
});
```
- **[DON'T]** use standard `cy.request` for failing endpoints, as it will crash the test runner before the assertion:
```javascript
test('should return 404', () => {
  cy.request('http://localhost:3000/api/article?id=unexistingID') // Crashes here
  .its('status')
  .should('be.equal', 404);
});
```

### Cypress Asynchronous `.each()` Validation
- **[DO]** Use the `done` callback when validating arrays of objects in Cypress:
```javascript
test('should correctly return a list of articles', (done) => {
  cy.request('http://localhost:3000/api/articles')
    .its('body')
    .each((article) => {
      expect(article).to.have.keys('id', 'title', 'body', 'author', 'image');
      expect(article.author).to.have.keys('id', 'name');
      done();
    });
});
```
- **[DON'T]** Omit the `done` callback, which causes Cypress to lose track of the loop execution status.