# @Domain
Trigger these rules when the user requests assistance with Continuous Integration (CI) configuration, pipeline creation, automated testing workflows, debugging remote CI failures, running headless browser tests, or configuring GitHub Actions/GitLab CI for Python (Django) and JavaScript (Jasmine) codebases.

# @Vocabulary
- **Continuous Integration (CI):** An automated server environment that runs the full test suite on every code push to prevent regressions and act as a deployment gate.
- **Pipeline:** A defined sequence of automated steps in CI (e.g., install dependencies, run unit tests, run functional tests).
- **Fast Feedback Loop:** The principle of structuring CI to fail as quickly as possible if there is an error, typically by running fast tests before slow tests and delaying heavy dependency installation.
- **Flaky Tests:** Tests that fail intermittently, often exposed by the slower or differently-resourced CI environment (the "noisy neighbour" problem).
- **Headless Browser:** A web browser running without a graphical user interface (GUI) or display monitor, required for running Selenium or Jasmine tests on a CI server.
- **Artifacts:** Output files (like screenshots and HTML dumps) saved by the CI server after a build, crucial for debugging remote test failures.
- **Local CI Reproduction:** The practice of using a local Dockerfile (e.g., `Dockerfile.ci`) to perfectly mimic the CI environment on a local machine for faster debugging.

# @Objectives
- Automate the execution of all tests (Unit and Functional) to prevent developers from bypassing slow test suites.
- Optimize CI pipelines for fast feedback by prioritizing unit tests and caching.
- Guarantee the reproducibility of CI environments locally using Docker.
- Equip functional tests (FTs) with automated artifact generation (screenshots and HTML dumps) to easily diagnose headless CI failures.
- Ensure all browser-based interactions in CI are explicitly configured to run in headless mode.
- Mitigate flaky tests by dynamically adjusting wait timeouts rather than disabling the tests.

# @Guidelines

## Pipeline Optimization and Structuring
- The AI MUST structure CI pipelines to run the fastest tests first (e.g., Unit Tests) before running slow tests (e.g., Functional Tests/Selenium).
- The AI MUST defer the installation of heavy, test-specific dependencies (like `selenium`) until *after* the fast tests have passed.
- The AI MUST separate distinct domains of testing (e.g., Python backend tests vs. JavaScript frontend tests) into separate CI jobs running on distinct, optimized base images (e.g., `python:slim` vs. `node:slim`).
- The AI MUST configure package caching (e.g., `PIP_CACHE_DIR` for Python, `npm` cache for Node) to speed up dependency installation across CI runs.

## Headless Browser Configuration
- The AI MUST set environment variables to force browsers into headless mode when running in CI (e.g., `MOZ_HEADLESS: "1"` for Firefox).
- When configuring JavaScript browser runners (like `jasmine-browser-runner`), the AI MUST explicitly set the browser name to the headless equivalent (e.g., `headlessFirefox`).

## Debugging and Artifacts
- The AI MUST configure CI scripts to save test artifacts (screenshots, HTML dumps) and MUST explicitly set the CI configuration to save these artifacts even when the build fails (e.g., `when: always` in GitLab CI).
- The AI MUST implement logic in the functional test framework's `tearDown` method to introspect the test result (e.g., using `self._outcome.result.failures` in Python's `unittest`) and automatically generate a screenshot and page source dump if the test failed.
- When generating artifact filenames, the AI MUST include the test class, test method name, and a timestamp to ensure uniqueness.
- When debugging a CI failure that cannot be immediately identified, the AI MUST construct a local `Dockerfile.ci` that perfectly mirrors the CI pipeline's steps to reproduce the error locally.

## Mitigating Flaky Tests
- When a functional test fails intermittently in CI due to timeout issues, the AI MUST increase explicit wait timeouts (e.g., `MAX_WAIT`) rather than disabling the test or reverting to implicit waits.

## JavaScript Testing in CI
- The AI MUST use a dedicated CLI test runner for JavaScript in CI (e.g., `jasmine-browser-runner runSpecs`) rather than relying on a static HTML SpecRunner page.
- If JavaScript tests rely on CSS frameworks (like Bootstrap) for visibility assertions, the AI MUST ensure the CSS files are explicitly loaded in the JS test runner's configuration file.

# @Workflow
When tasked with creating or modifying a CI pipeline, follow this rigid step-by-step process:

1. **Define the Pipeline Base:** Create the CI configuration file (e.g., `.gitlab-ci.yml`). Define global variables (like `PIP_CACHE_DIR` and `MOZ_HEADLESS: "1"`) and specify cache paths.
2. **Configure the Backend Job (Python):**
    - Set the image to a lightweight Python image (`python:slim`).
    - Define a `before_script` to set up the virtual environment.
    - In the `script` section:
        a. Install base requirements (`pip install -r requirements.txt`).
        b. Run Unit Tests immediately.
        c. *Only if unit tests pass*, install system dependencies for browsers (e.g., `apt install firefox-esr`).
        d. Install heavy testing dependencies (`pip install selenium`).
        e. Run the full test suite including Functional Tests.
3. **Configure Artifact Retention:** Add an `artifacts` block to the backend job, targeting the directory where screendumps are saved, and explicitly set `when: always`.
4. **Implement Artifact Generation in Code:**
    - Override the `tearDown` method in the base Functional Test class.
    - Check if the test failed using `self._outcome.result.failures` or `errors`.
    - If failed, call `browser.get_screenshot_as_file()` and dump `browser.page_source` to the designated artifact directory.
5. **Configure the Frontend Job (JavaScript):**
    - Create a separate job using a Node image (`node:slim`).
    - Install the browser (e.g., `firefox-esr`).
    - Run `npm install` based on `package-lock.json`.
    - Execute the headless JS test runner (e.g., `npx jasmine-browser-runner runSpecs`).
6. **Local CI Reproduction (If Debugging):**
    - If the user reports a CI-specific failure, immediately generate an `infra/Dockerfile.ci` that translates the YAML `script` steps into Docker `RUN` commands to allow local reproduction and debugging.

# @Examples (Do's and Don'ts)

## CI Pipeline Ordering & Feedback
- **[DO]** Run unit tests before installing heavy functional testing tools to get fast feedback.
  ```yaml
  test-python:
    script:
      - pip install -r requirements.txt
      - python manage.py test lists accounts  # Fast unit tests first
      - apt update -y && apt install -y firefox-esr
      - pip install selenium                  # Heavy install deferred
      - python manage.py test                 # Slow FTs last
  ```
- **[DON'T]** Install everything upfront and run all tests blindly.
  ```yaml
  test-python:
    script:
      - pip install -r requirements.txt selenium
      - apt update -y && apt install -y firefox-esr
      - python manage.py test  # Unit tests wait for selenium/firefox install
  ```

## CI Artifact Configuration
- **[DO]** Explicitly tell the CI server to save artifacts even on failure.
  ```yaml
  artifacts:
    when: always
    paths:
      - src/functional_tests/screendumps/
  ```
- **[DON'T]** Rely on default artifact behavior, which discards files if the CI script exits with a non-zero status (test failure).
  ```yaml
  artifacts:
    paths:
      - src/functional_tests/screendumps/  # Will be lost when tests fail!
  ```

## Programmatic Artifact Generation
- **[DO]** Introspect the test outcome in `tearDown` to take screenshots conditionally.
  ```python
  def tearDown(self):
      if self._test_has_failed():
          self.browser.get_screenshot_as_file(f"screendumps/{self.id()}.png")
          Path(f"screendumps/{self.id()}.html").write_text(self.browser.page_source)
      self.browser.quit()
      super().tearDown()

  def _test_has_failed(self):
      return self._outcome.result.failures or self._outcome.result.errors
  ```
- **[DON'T]** Take screenshots unconditionally, or fail to save the HTML DOM which contains vital debugging information.

## Headless Browser Execution
- **[DO]** Configure global environment variables for headless execution in the CI YAML.
  ```yaml
  variables:
    MOZ_HEADLESS: "1"
  ```
- **[DON'T]** Assume the CI server has a display variable set, which will cause `Process unexpectedly closed with status 1` or `no DISPLAY environment variable specified` errors.

## JavaScript CI Configuration
- **[DO]** Include required CSS frameworks in the headless test runner config if assertions depend on CSS visibility.
  ```javascript
  // jasmine-browser-runner.config.mjs
  export default {
    specDir: "tests",
    specFiles: ["**/*[sS]pec.js"],
    cssFiles: ["bootstrap/css/bootstrap.min.css"], // Required for visibility checks
    browser: { name: "headlessFirefox" }
  };
  ```
- **[DON'T]** Attempt to run an HTML `SpecRunner.html` file using standard Node without a dedicated browser runner, or forget to load the CSS, causing false positive test failures on `checkVisibility()` assertions.