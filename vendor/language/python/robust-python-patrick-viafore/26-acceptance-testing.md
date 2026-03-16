# @Domain
These rules apply whenever the AI is tasked with gathering product requirements, designing test strategies, configuring continuous integration test reports, generating behavioral specifications, or writing and maintaining acceptance tests. This includes any interaction with Behavior-Driven Development (BDD) paradigms, the Gherkin specification language, and the Python `behave` testing framework.

# @Vocabulary
- **Verification**: The process of ensuring code does what the developer intended (typically handled by unit and integration tests).
- **Validation**: The process of ensuring the code builds what the customer/end-user actually wants (handled by acceptance tests).
- **BDD (Behavior-Driven Development)**: A methodology focused on defining system behaviors in plain language with end-users prior to coding, clarifying communication.
- **Gherkin**: A formal specification language used in BDD, characterized by the `Given-When-Then` (GWT) format.
- **Executable Specifications**: A set of requirements translated directly into automated code, making the requirements themselves testable.
- **behave**: A Python framework that parses Gherkin requirements and links them to executable Python code.
- **Context (`ctx`)**: The state object passed through `behave` steps to share data and variables across a single scenario.
- **Parameterized Steps**: Reusable Python step definitions that accept variables parsed from the Gherkin text.
- **Scenario Outline**: A Gherkin construct that allows table-driven requirements to run the same scenario multiple times with different data rows (`Examples:`).
- **Step Matching**: The mechanism `behave` uses to map Gherkin text to Python functions. Can be customized using regular expressions.
- **Tags**: Arbitrary text prefixed with `@` (e.g., `@smoke`, `@wip`) used to categorize and selectively execute or exclude features and scenarios.
- **environment.py**: A specific file in the `behave` framework used to define global setup and teardown lifecycle hooks.

# @Objectives
- Validate customer intent by writing tests that confirm the system behaves as the end-user expects, not just verifying that functions execute without crashing.
- Maintain absolute traceability by making the project's requirements and the project's tests the exact same entity via Executable Specifications.
- Enforce a strict separation between human-readable requirements (`.feature` files) and the underlying test implementation logic (`.py` files).
- Eliminate duplicate test logic by aggressively utilizing parameterized steps, regex step matching, and Scenario Outlines.
- Ensure isolated and safe test execution by leveraging lifecycle hooks for global and scenario-level setup and teardown.

# @Guidelines
- **Test Strategy Classification**: Never use unit tests or integration tests to prove customer requirements. You MUST use acceptance tests for validation.
- **Directory Architecture**: You MUST place Gherkin files in a `features/` directory and Python step implementations in a `features/steps/` directory.
- **Gherkin Syntax Rigidity**: You MUST structure all scenarios strictly using `Given` (preconditions), `When` (actions), and `Then` (expected results).
- **State Management**: You MUST pass data between steps exclusively by attaching attributes to the `context` (`ctx`) object provided by `behave`. Never use global variables for step state.
- **Step Parameterization**: You MUST use `{variable}` parameters in `@given`/`@when`/`@then` decorators to capture dynamic data from Gherkin strings rather than duplicating step definitions.
- **Table-Driven Testing**: You MUST use `Scenario Outline` combined with an `Examples:` table when a scenario is repeated with varying input/output parameters.
- **Complex Step Matching**: You MUST call `use_step_matcher("re")` and use named regular expression groups (e.g., `(?P<variable_name>pattern)`) when Gherkin phrasing requires optional words or complex grammar.
- **Lifecycle Management**: You MUST centralize shared setup and teardown code (e.g., database initialization, cache clearing) in `features/environment.py` using `before_all`, `before_feature`, `before_scenario`, and their `after_*` counterparts.
- **Selective Execution**: You MUST use tags (e.g., `@smoke`, `@wip`) on features or scenarios to logically group them. Use `--tags=tagname` to include or `--tags=-tagname` to exclude tests during CLI execution.
- **Reporting**: You MUST output JUnit XML reports via `behave --junit` when test results need to be visualized or ingested by CI/CD tools (e.g., using `junit2html`).

# @Workflow
1. **Requirement Elicitation**: Write requirements in a `.feature` file in plain language using the Given-When-Then format. Group related scenarios under a `Feature:` heading.
2. **Data Deduplication**: Identify repetitive scenarios and consolidate them into `Scenario Outline` structures with an `Examples:` table.
3. **Tagging**: Apply appropriate tags (e.g., `@smoke`) to the Feature or Scenario to enable execution filtering.
4. **Step Stubbing**: Run the `behave` command to identify undefined steps. Create a new Python file in `features/steps/`.
5. **Step Implementation**: Write Python functions decorated with `@given`, `@when`, and `@then`.
6. **State Passing**: Instantiate and mutate objects on the `ctx` (context) argument within the `Given` and `When` steps.
7. **Assertion**: Assert expected outcomes against the `ctx` object within the `Then` steps.
8. **Refactoring for Reuse**: Refine step decorators using string parameters (`{var}`) or Regex matchers to combine similar steps.
9. **Environment Hook Generation**: If the test suite requires global state setup/teardown (e.g., a database context), implement `features/environment.py` and assign resources to `ctx` inside the appropriate hook (e.g., `before_scenario`).
10. **Execution & Reporting**: Run the test suite using `behave features/ --junit` and generate HTML visual reports if requested.

# @Examples (Do's and Don'ts)

### Gherkin Scenario Duplication
- **[DO]** Use Scenario Outlines for table-driven requirements:
  ```gherkin
  Feature: Vegan-friendly menu
    Scenario Outline: Vegan Substitutions
      Given an order containing <dish_name>
      When I ask for vegan substitutions
      Then <result>
  
      Examples: Vegan Substitutable
        | dish_name                 | result                                     |
        | a Cheeseburger with Fries | I receive the meal with no animal products |
        | Cobb Salad                | I receive the meal with no animal products |
  ```
- **[DON'T]** Copy and paste the exact same scenario to test different variables:
  ```gherkin
  Feature: Vegan-friendly menu
    Scenario: Can substitute cheeseburger
      Given an order containing a Cheeseburger with Fries
      When I ask for vegan substitutions
      Then I receive the meal with no animal products
      
    Scenario: Can substitute cobb salad
      Given an order containing a Cobb Salad
      When I ask for vegan substitutions
      Then I receive the meal with no animal products
  ```

### Step Implementation and Reusability
- **[DO]** Parameterize steps to build a shared, reusable vocabulary:
  ```python
  from behave import given
  
  @given("an order containing {dish_name}")
  def setup_order(ctx, dish_name):
      if dish_name == "a Cheeseburger with Fries":
          ctx.dish = CheeseburgerWithFries()
      elif dish_name == "Meatloaf":
          ctx.dish = Meatloaf()
  ```
- **[DON'T]** Write explicit, rigid step definitions for every single variation:
  ```python
  from behave import given
  
  @given("an order containing a Cheeseburger with Fries")
  def setup_cheeseburger_order(ctx):
      ctx.dish = CheeseburgerWithFries()
      
  @given("an order containing Meatloaf")
  def setup_meatloaf_order(ctx):
      ctx.dish = Meatloaf()
  ```

### Step Matching for Complex Grammar
- **[DO]** Use regex matchers for optional phrasing/grammar:
  ```python
  from behave import use_step_matcher, given
  use_step_matcher("re")
  
  @given("an order containing [a |an ]?(?P<dish_name>.*)")
  def setup_order(ctx, dish_name):
      ctx.dish = create_dish(dish_name)
  ```
- **[DON'T]** Stack decorators just to handle optional grammar words:
  ```python
  from behave import given
  
  @given("an order containing a {dish_name}")
  @given("an order containing an {dish_name}")
  @given("an order containing {dish_name}")
  def setup_order(ctx, dish_name):
      ctx.dish = create_dish(dish_name)
  ```

### Test Lifecycle Management
- **[DO]** Use `environment.py` hooks for setup and teardown:
  ```python
  # features/environment.py
  def before_all(ctx):
      ctx.database = setup_database()
      
  def after_all(ctx):
      ctx.database.cleanup()
  ```
- **[DON'T]** Put global setup and teardown logic directly into `@given` and `@then` steps, as failed assertions will skip the teardown code:
  ```python
  @then("the database is updated")
  def check_db(ctx):
      assert ctx.database.is_updated()
      ctx.database.cleanup() # Anti-pattern: If assert fails, this never runs.
  ```