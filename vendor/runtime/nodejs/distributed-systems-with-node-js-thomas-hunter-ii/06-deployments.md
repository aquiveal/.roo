# @Domain
These rules MUST trigger when the user requests assistance with configuring Continuous Integration (CI) pipelines (e.g., Travis CI), writing application deployment scripts (e.g., Heroku container deployments), implementing automated test suites (Unit, Integration, and Code Coverage), calculating or enforcing Semantic Versioning (SemVer), resolving Node.js module loading issues, or configuring/publishing npm packages (including private registries).

# @Vocabulary
- **Build Pipeline**: A formal collection of stages required to deploy an application, including checking out code, installing dependencies, testing, compiling, and deploying.
- **Continuous Integration (CI)**: A software development practice where self-contained changes are constantly tested, merged into a mainline branch, and deployed via a CI server.
- **Build**: The process where a snapshot of a codebase (e.g., a Git commit) is converted into an executable form.
- **Release**: A specific combination of a build paired with targeted environment configuration settings.
- **Artifact**: A byproduct file or directory produced during the build pipeline (e.g., a code coverage HTML report or a Docker image).
- **Rollback**: The act of reverting a newly deployed, faulty release back to a previous, known-good release.
- **Unit Test**: Tests focused on individual units of code (logical branches, success/failure conditions) that MUST NOT touch the network or perform I/O.
- **Integration Test**: Higher-level tests that check how parts of an application work together, strictly requiring real servers and real HTTP requests over the network.
- **Code Coverage**: A metric defining how much of an application's code (statements, branches, functions, lines) is executed during a test suite run.
- **Module Resolution Algorithm**: The complex internal logic Node.js uses to locate files when `require()` is called, checking core modules, explicit paths, and recursive `node_modules` directories.
- **Require Cache**: An object (`require.cache`) where Node.js stores cached `Module` objects for previously loaded files to prevent multiple executions of the same file.
- **SemVer (Semantic Versioning)**: A strict versioning philosophy formatted as Major.Minor.Patch (e.g., 1.2.3) dictating how version numbers increment based on breaking changes, new features, and bug fixes.
- **Scope**: A namespace prefix for npm packages (e.g., `@org/package`) to avoid naming collisions in public and private registries.
- **Deduplication / Hoisting**: The npm CLI algorithm that moves sub-dependencies higher up in the `node_modules/` directory tree to avoid deeply nested, cyclical, or redundant package installations.

# @Objectives
- Construct deterministic, secure, and automated CI/CD build pipelines.
- Implement highly realistic integration tests by spawning real processes rather than relying on mocked request objects.
- Strictly enforce 100% code coverage, explicitly handling intentional fallbacks.
- Ensure strict adherence to Semantic Versioning (SemVer) rules when modifying package APIs.
- Scaffold clean, secure npm packages that omit unnecessary application-specific files from published tarballs.
- Prevent Node.js module resolution bugs by enforcing explicit file extensions and avoiding global state.

# @Guidelines

### Build Pipelines & Deployments
- The AI MUST configure continuous integration to test code BOTH on pull requests and after merging to the mainline branch prior to deployment.
- The AI MUST NOT commit raw, plaintext secrets (e.g., API keys, Heroku tokens) into version control. The AI MUST instruct the use of CLI encryption tools (like `travis encrypt`) and inject them via environment variables.
- When configuring container-based deployments for PaaS (like Heroku), the AI MUST define a pipeline script that logs into the container registry, pushes the image, and releases the container.

### Automated Testing
- **Unit Tests**: The AI MUST isolate unit tests from any network interactions. "If it touches the network, it’s not a unit test."
- **Integration Tests**: The AI MUST write integration tests that start the actual server (e.g., using `child_process.spawn`) on a random port (`PORT=0`), extract the bound port from `stdout`, and send REAL HTTP requests (e.g., via `node-fetch`).
- The AI MUST NEVER mock request/response objects (e.g., passing `{ foo: { bar: 1 } }` directly to a route handler). Real HTTP requests pass data as strings; mocking hides string-coercion and query-parsing bugs.
- When tests finish, the AI MUST explicitly kill the spawned server process to prevent hanging test suites.

### Code Coverage
- The AI MUST enforce a 100% threshold for all coverage metrics (`branches`, `lines`, `functions`, `statements`) using tools like `nyc` and a `.nycrc` file.
- For intentional, safe, but uncovered logic branches (e.g., a default port fallback `process.env.PORT || 8000` used only for local development), the AI MUST explicitly prepend the line with the `/* istanbul ignore next */` comment rather than lowering the 100% threshold.

### Node.js Modules
- The AI MUST use explicit file extensions in `require()` calls (e.g., `require('./foo.js')` instead of `require('./foo')`). Omitting extensions causes resolution race conditions (e.g., mistakenly loading a `.json` file if the `.js` file is deleted).
- The AI MUST NOT declare global variables using `global` or `globalThis` in modules. The AI MUST utilize the local scope provided by the Node.js module wrapper (`exports`, `require`, `module`, `__filename`, `__dirname`).
- The AI MUST warn against using singleton state instances within npm packages. Because npm deduplication/hoisting algorithms can shift package locations, applications might inadvertently instantiate multiple copies of a "singleton" if version ranges conflict.

### Semantic Versioning (SemVer)
- The AI MUST increment the **Patch** version solely for backwards-compatible bug fixes.
- The AI MUST increment the **Minor** version for backwards-compatible new features.
- The AI MUST increment the **Major** version for ANY backwards-breaking change. Deleting an exported method, even if completely unused by known consumers, constitutes a Major breaking change.
- If the major version is `0` (e.g., `0.1.2`), the AI MUST treat the first non-zero digit as the major version (e.g., a breaking change updates `0.1.2` to `0.2.0`).

### npm Package Configuration
- For application repositories (not published as packages), the AI MUST set `"private": true` in `package.json` to prevent accidental publication of proprietary code.
- For published packages, the AI MUST define an `.npmignore` file to exclude `package-lock.json`, test directories, and side-effect files (like raw binaries or coverage reports).
- The AI MUST ONLY commit `package-lock.json` in top-level application repositories, NEVER in the published tarball of a reusable npm package (as npm ignores lockfiles of dependencies).
- When creating internal packages for organizations, the AI MUST prefix the package name with an npm scope (e.g., `@corp/package`) to prevent naming collisions with public registry packages.

# @Workflow
When tasked with setting up a deployment, CI/CD pipeline, or package publication workflow, the AI MUST execute the following algorithm:
1. **Pipeline Scaffold**: Generate the CI configuration file (e.g., `.travis.yml`) defining the Node.js runtime environment, install scripts, test scripts, and deployment triggers for the master branch.
2. **Test Architecture**: Create separate directories/files for Unit Tests and Integration Tests. Write logic to spawn a real child process for the web server in the Integration tests.
3. **Coverage Enforcement**: Add `.nycrc` configured for 100% coverage. Scan the codebase for environmental fallbacks (like default ports) and apply `/* istanbul ignore next */` where appropriate.
4. **Secret Encryption**: Provide the exact commands the user must run locally to encrypt deployment credentials (e.g., `travis encrypt HEROKU_API_KEY=...`) and insert the resulting secure string block into the CI configuration.
5. **Deployment Scripting**: Write the shell script (e.g., `deploy-heroku.sh`) that builds the artifact (Docker image), authenticates with the target registry, pushes the artifact, and triggers the release.
6. **Package Verification** (If publishing a package): Create `.npmignore`, verify the `package.json` `name` uses a scope if private, ensure `package-lock.json` is ignored, and review the requested code changes to calculate the strict SemVer increment.

# @Examples (Do's and Don'ts)

### 1. Integration Testing Requests
- **[DO]** Spawn a real server and send actual HTTP requests to capture protocol and string-parsing realities:
```javascript
const { spawn } = require('child_process');
const fetch = require('node-fetch');
const test = require('tape');

test('GET /recipes/42', async (t) => {
  const server = spawn('node', ['server.js'], { env: { PORT: 0 } });
  // logic to wait for server output and extract URL...
  const result = await fetch(`${url}/recipes/42`);
  const body = await result.json();
  t.equal(body.id, 42);
  server.kill();
  t.end();
});
```
- **[DON'T]** Pass mocked JavaScript objects directly to router handlers, as this hides bugs caused by HTTP query strings:
```javascript
const router = require('foo-router.js');
test('#fooHandler()', async (t) => {
  // ANTI-PATTERN: Query parameters over HTTP are strings, passing a raw Number hides bugs.
  const result = await router.fooHandler({ query: { foo: { bar: 1 } } }); 
  t.equal(result, 2);
});
```

### 2. Module Loading
- **[DO]** Include explicit file extensions in `require` calls:
```javascript
const contacts = require('./contacts.js');
```
- **[DON'T]** Rely on implicit extension resolution which can load unintended files (like `contacts.json`) if `contacts.js` is removed:
```javascript
const contacts = require('./contacts');
```

### 3. SemVer Application
- **[DO]** Bump the MAJOR version when removing an unused method:
```javascript
// Previous version 1.1.0 exported `getName()` and `nameLength()`.
// New version removes `nameLength()`.
// Package MUST be bumped to 2.0.0.
```
- **[DON'T]** Bump the MINOR or PATCH version when removing a method, even if telemetry indicates zero users are calling it.

### 4. npm Package Configurations
- **[DO]** Exclude `package-lock.json` and tests via `.npmignore` for library packages:
```text
# .npmignore
temp.bin
test/
package-lock.json
```
- **[DON'T]** Publish an npm library that includes a `package-lock.json` or arbitrary testing binaries.