# @Domain
Python codebases possessing existing test suites where test effectiveness, robustness, and the quality of the testing safety net need to be evaluated, validated, or improved. Trigger these rules when asked to evaluate test quality, find gaps in test coverage, or perform mutation testing.

# @Vocabulary
- **Mutation Testing**: A form of meta-testing involving the deliberate modification of source code to introduce bugs, used to measure how effectively a test suite catches errors.
- **Mutant**: A single instance of a deliberate bug or modification introduced into the source code (e.g., changing `<=` to `<`, or `continue` to `break`).
- **Surviving Mutant**: A mutant that does not cause the test suite to fail. This indicates a gap in the test suite's coverage or assertions.
- **Eliminated/Killed Mutant**: A mutant that successfully causes the test suite to fail, proving the tests are robust enough to catch that specific deviation.
- **mutmut**: The primary Python library/tool used to automate the generation and testing of mutants.
- **Diff Notation**: The output format used by `mutmut` to display mutants, where `-` indicates the original line and `+` indicates the mutated line.
- **Line Coverage**: A metric indicating whether a line of code is executed by a test suite, which does not guarantee the line's behavior is actually verified.

# @Objectives
- Validate the actual effectiveness of existing test suites rather than relying solely on code execution metrics.
- Identify and patch holes in the testing safety net where code is executed but its behavior is not rigorously asserted.
- Elevate code coverage metrics from false proxies of quality to true predictors of robustness.
- Systematically eliminate surviving mutants by writing strict, precise tests that fail when code behavior changes.
- Apply mutation testing strategically to manage its high computational cost.

# @Guidelines
- **Avoid the Coverage Fallacy**: NEVER use high line or branch coverage percentages as the sole indicator of test quality. Tests that execute code without asserting specific outcomes will yield 100% coverage but 0% robustness.
- **Categorize Surviving Mutants**: When a mutant survives, the AI MUST classify the mutated line into one of three categories:
  1. The line is unneeded/dead code (Action: Delete the code).
  2. The line is needed but unimportant to test, such as debug logging (Action: Ignore the mutant).
  3. The line represents missing test coverage/assertions (Action: Write a new test or strengthen an existing one).
- **Target Mutation Testing Strategically**: Because mutation testing is computationally expensive, DO NOT run it blindly against an entire large codebase. Target specific areas such as:
  - Modules with historically high bug rates.
  - Files with high churn (frequent commits).
  - Mission-critical business logic that already possesses a mature test suite.
- **Leverage Test Coverage for Efficiency**: ALWAYS use line coverage data to restrict `mutmut`. Mutating code that has no test coverage is a waste of resources; only mutate code that the test suite actually executes.
- **Test for Specific Properties**: Ensure tests assert specific state changes, return values, or side effects. Tests that merely check `assert result is not None` or simply verify no exception is thrown are antipatterns that allow mutants to survive.
- **Understand `mutmut` Operations**: The AI MUST anticipate common mutations applied by `mutmut`, including:
  - Adding `1` to integer literals (catching off-by-one errors).
  - Exchanging `break` and `continue`.
  - Exchanging `True` and `False`.
  - Negating expressions (e.g., `x is None` to `x is not None`).
  - Changing operators (e.g., `/` to `//`, `<` to `<=`).

# @Workflow
When tasked with evaluating test suite quality or performing mutation testing, the AI MUST execute the following algorithmic process:

1. **Setup and Targeting**: 
   - Identify the specific high-value, high-churn, or highly buggy module to target.
   - Install required tools: `pip install mutmut coverage`.
2. **Generate Coverage Data**:
   - Run the test suite with coverage tracking to identify executed lines: `coverage run -m pytest <target_path>`.
3. **Execute Mutation Testing**:
   - Run `mutmut` restricted to covered lines: `mutmut run --paths-to-mutate <target_path> --use-coverage`.
   - *Note: If the run is interrupted, `mutmut` uses `.mutmut-cache` to resume progress automatically.*
4. **Analyze Results**:
   - View the summary of surviving and eliminated mutants: `mutmut results`.
   - For each surviving mutant ID, view the diff: `mutmut show <id>`.
5. **Eliminate Surviving Mutants (The Fix Loop)**:
   - Apply the specific mutant to the file on disk: `mutmut apply <id>`.
   - *Constraint*: Ensure the file is tracked in version control before applying.
   - Run the test suite. The tests will currently PASS (because the mutant survives).
   - Write a new test, or add assertions to an existing test, targeting the exact boundary or logic condition altered by the mutant.
   - Run the test suite again. The tests MUST now FAIL (the new test catches the mutant).
   - Revert the source code file to its original state (removing the mutant).
   - Run the test suite again. The tests MUST now PASS.
6. **Verification**:
   - Re-run `mutmut run` or generate a JUnit report (`mutmut junitxml > report.xml`) to confirm the mutant is officially eliminated.

# @Examples (Do's and Don'ts)

**[DON'T]**
Write tests that merely execute code to achieve line coverage without asserting behavior. This allows mutants to easily survive.
```python
# Code
def check_limit(val, limit):
    if val > limit:
        trigger_warning()

# Useless Test (Achieves 100% coverage but catches no mutants)
def test_check_limit():
    check_limit(10, 5)
    assert True # No exception thrown, coverage achieved!
```

**[DO]**
Write precise tests that assert specific boundary conditions and state changes, ensuring that operator mutations (like `>` to `>=`) will be caught.
```python
# Useful Test (Kills mutants)
def test_check_limit_boundary():
    # Arrange & Act
    check_limit(5, 5)
    # Assert (kills the val >= limit mutant)
    assert_no_warnings_triggered()
    
    # Arrange & Act
    check_limit(6, 5)
    # Assert
    assert_warnings_triggered()
```

**[DON'T]**
Run `mutmut` across an entire untested legacy codebase, which will generate massive amounts of unactionable noise.
```bash
# Inefficient and noisy
mutmut run --paths-to-mutate src/
```

**[DO]**
Generate test coverage first, then restrict mutation testing to only the lines of code that the test suite actually executes.
```bash
# Efficient and targeted
coverage run -m pytest src/billing/
mutmut run --paths-to-mutate src/billing/ --use-coverage
```

**[DON'T]**
Attempt to mentally guess why a mutant survived without physically testing the fix against the mutated code.

**[DO]**
Use the apply-test-revert workflow to definitively prove the new test eliminates the mutant.
```bash
mutmut apply 34
pytest tests/test_billing.py # Fails as expected after you write the new test
git checkout src/billing/core.py # Revert the mutant
pytest tests/test_billing.py # Passes, proving the safety net is patched
```