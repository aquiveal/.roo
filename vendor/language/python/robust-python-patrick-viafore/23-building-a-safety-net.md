# @Domain
These rules MUST trigger whenever the AI performs tasks related to creating, modifying, evaluating, or refactoring Python tests, CI/CD pipelines, static analysis configurations, quality assurance workflows, or test automation scripts.

# @Vocabulary
- **Static Analysis**: Tools that inspect the codebase without executing it to find errors, style violations, and complexity issues.
- **Pylint**: A linter used to check for PEP 8 violations, dead code, cohesion, and common programming errors.
- **astroid**: A library used for parsing Python files into an Abstract Syntax Tree (AST), utilized to write custom Pylint checkers.
- **Cyclomatic Complexity**: A measure of the number of execution paths in a control flow graph (measured via `mccabe`).
- **Whitespace Heuristic**: A metric using indentation levels to gauge code complexity.
- **Bandit**: A security static analysis tool to find common security flaws (e.g., SQL injection, unsafe YAML).
- **dodgy**: A static analysis tool to detect leaked secrets/credentials in code.
- **AAA Test Pattern**: Arrange-Act-Assert. A structural methodology for writing readable tests.
- **Annihilate**: The cleanup stage of the AAA pattern, ensuring tests do not share resources.
- **Fixture**: A `pytest` construct for managing test initialization, dependency injection, and teardown (via `yield`).
- **Monkeypatching**: Dynamically replacing attributes at runtime. An anti-pattern if overused; mock objects via duck typing are preferred.
- **PyHamcrest**: A testing library using matchers for writing highly readable, natural-language-style assertions.
- **Behavior-Driven Development (BDD)**: A practice defining system behaviors using plain language to ensure the right product is built.
- **Gherkin**: A specification language using Given-When-Then (GWT) syntax to define testable requirements.
- **behave**: A Python framework that executes Gherkin specifications as automated acceptance tests.
- **Property-Based Testing**: A generative testing method where the framework generates input data to test defined system invariants (properties).
- **Hypothesis**: A Python library for property-based testing.
- **Shrinking**: The process where Hypothesis automatically searches for the minimal failing input value upon discovering a test failure.
- **Stateful Testing**: Using Hypothesis `RuleBasedStateMachine` to generate combinations of operations/algorithms to find errors.
- **Mutation Testing**: Making automated, discrete changes (mutants) to source code to verify if the test suite catches the bugs.
- **mutmut**: A Python mutation testing tool.
- **Line Coverage**: A metric indicating which lines of code are executed by tests. It is a predictor of the *absence* of robustness, not a guarantee of quality.

# @Objectives
- Shift errors left by catching bugs during the earliest possible phase using static analysis, linters, and security scanners.
- Validate that the software meets customer expectations using BDD, Gherkin, and acceptance testing.
- Write maintainable, readable, and highly isolated unit and integration tests using the strict AAA (Arrange, Act, Assert, Annihilate) pattern.
- Automate boundary value discovery and test invariant properties across vast input domains using generative property-based testing.
- Prove the actual efficacy of the test suite by ensuring tests fail when intentional bugs are introduced via mutation testing.

# @Guidelines

### Static Analysis & Linting
- The AI MUST enforce the use of `Pylint` to catch common errors such as dangerous mutable default arguments (e.g., `[]`) and inconsistent return statements.
- The AI MUST utilize the `astroid` library to build custom Pylint plugins (`BaseChecker`) to enforce domain-specific invariants (e.g., ensuring a specific type is only instantiated within a "blessed" function).
- The AI MUST monitor code complexity using `mccabe` (cyclomatic complexity) and the whitespace heuristic (indentation depth). Code exceeding defined complexity thresholds MUST be flagged for refactoring.
- The AI MUST invoke `dodgy` to scan for leaked secrets and `bandit` to identify security flaws (e.g., raw SQL, unsafe YAML).

### Test Structure & AAA Pattern
- All unit and integration tests MUST follow the Arrange-Act-Assert (-Annihilate) pattern.
- **Arrange**: The AI MUST extract large, repetitive setup boilerplate into helper functions or `pytest` fixtures.
- **Act**: The action being tested MUST be kept to 1-2 lines of code.
- **Act (Parameterization)**: For table-driven tests, the AI MUST use `@pytest.mark.parametrize` but MUST limit parameters to 3-4 variables to prevent tests from becoming overly generic and unreadable.
- **Assert**: The AI MUST group logical assertions targeting a single property. The AI MUST provide verbose assertion failure messages or use `PyHamcrest` matchers (e.g., `assert_that(result, is_(equal_to(expected)))`) for clarity.
- **Annihilate**: Tests MUST NOT share resources. The AI MUST implement cleanup code using `with` context managers or `yield` statements inside `pytest` fixtures to guarantee execution even if the assert fails.

### Mocking & Dependencies
- The AI MUST NOT litter tests with `monkeypatching`.
- The AI MUST prefer defining discrete Mock classes that fulfill structural subtyping (duck typing) expectations over dynamically patching existing complex objects.

### Acceptance Testing & BDD
- The AI MUST define customer-facing requirements using the Gherkin language in `.feature` files (Feature, Scenario, Given, When, Then).
- The AI MUST implement step definitions using the `behave` library (`@given`, `@when`, `@then`).
- The AI MUST use Scenario Outlines and Data Tables for similar Acceptance Test paths.
- The AI MUST parameterize step definitions in `behave` (e.g., `@given("an order containing {dish_name}")`) to build a reusable domain vocabulary.
- Setup and teardown for acceptance tests MUST be implemented in `environment.py` using `before_all`, `before_feature`, and `after_all` hooks.

### Property-Based Testing
- The AI MUST use `Hypothesis` (`@given`, `@example`) to test invariants rather than relying exclusively on hardcoded input values.
- The AI MUST use `hypothesis.strategies` to generate input data (`integers()`, `text()`, `dictionaries()`).
- The AI MUST use `@composite` decorators to build complex, domain-specific data generation strategies.
- For complex, heavily interdependent algorithms, the AI MUST implement stateful testing using `RuleBasedStateMachine`, `@rule`, and `@invariant` to test varying sequences of operations.

### Mutation Testing & Coverage
- The AI MUST NOT treat 100% line coverage as a guarantee of test quality.
- The AI MUST utilize `mutmut` to measure test efficacy.
- The AI MUST restrict mutation testing to code with existing test coverage by using the `--use-coverage` flag to reduce noise.
- When fixing survived mutants, the AI MUST apply the mutant to disk (`mutmut apply <id>`), write a failing test that catches the mutation, and then revert the mutation.

# @Workflow
When instructed to build or refactor a testing safety net for a module, the AI MUST execute the following steps in order:
1. **Static Analysis**: Run Pylint, mccabe, and bandit on the target code. Fix mutable defaults, inconsistent returns, and complexity spikes before writing tests.
2. **Behavior Definition (Acceptance)**: If the feature is customer-facing, write a Gherkin `.feature` file. Implement the `behave` steps to create an executable specification.
3. **Unit/Integration Testing (AAA)**: Write isolated unit tests using `pytest`. Implement fixtures with `yield` for annihilate/cleanup. Parameterize repetitive tests. Use Hamcrest matchers for assertions.
4. **Generative Edge-Case Discovery**: Identify the invariants and boundaries. Write a `Hypothesis` test using `@given` and strategies to automate input generation and verify properties.
5. **Efficacy Validation**: Run `mutmut` with `--use-coverage`. Identify any surviving mutants. Write targeted assertions to eliminate surviving mutants.

# @Examples (Do's and Don'ts)

### Static Analysis
- **[DON'T]** Use mutable defaults or allow inconsistent returns:
  ```python
  def add_authors_cookbooks(author_name: str, cookbooks: list[str] = []) -> bool:
      author = find_author(author_name)
      if author is None:
          assert False, "Author does not exist"
      else:
          for cookbook in author.get_cookbooks():
              cookbooks.append(cookbook)
          return True # Pylint error: inconsistent return statements (returns None if assert is disabled)
  ```
- **[DO]** Use immutable defaults and ensure strict return paths:
  ```python
  def add_authors_cookbooks(author_name: str, cookbooks: Optional[list[str]] = None) -> bool:
      if cookbooks is None:
          cookbooks = []
      author = find_author(author_name)
      if author is None:
          raise ValueError("Author does not exist")
      for cookbook in author.get_cookbooks():
          cookbooks.append(cookbook)
      return True
  ```

### Test Annihilate (Cleanup)
- **[DON'T]** Leave cleanup to the end of the function where an assertion failure will bypass it:
  ```python
  def test_calorie_calculation():
      add_ingredient_to_database("Bacon")
      calories = get_calories("Bacon")
      assert calories == 1000 # If this fails, cleanup never runs
      cleanup_database()
  ```
- **[DO]** Use pytest fixtures with `yield` to guarantee execution:
  ```python
  @pytest.fixture
  def test_database():
      db = setup_local_database()
      try:
          yield db
      finally:
          db.cleanup()

  def test_calorie_calculation(test_database):
      test_database.add_ingredient("Bacon")
      assert get_calories("Bacon") == 1000
  ```

### Acceptance Testing (BDD)
- **[DON'T]** Write untraceable unit tests for business requirements:
  ```python
  def test_vegan_substitution():
      assert is_vegan(substitute(Cheeseburger())) == True
  ```
- **[DO]** Use Gherkin and `behave` for executable specifications:
  ```gherkin
  Feature: Vegan-friendly menu
    Scenario Outline: Vegan Substitutions
      Given an order containing <dish_name>
      When I ask for vegan substitutions
      Then <result>

      Examples: Vegan Substitutable
        | dish_name                 | result                                      |
        | a Cheeseburger with Fries | I receive the meal with no animal products  |
  ```
  ```python
  @given("an order containing {dish_name}")
  def setup_order(ctx, dish_name):
      ctx.dish = create_dish(dish_name)
  ```

### Property-Based Testing
- **[DON'T]** Hardcode limited boundary values:
  ```python
  def test_meal_recommendation():
      meals = get_recommended_meal(900)
      assert sum(m.calories for m in meals) < 900
  ```
- **[DO]** Use Hypothesis to explore the domain:
  ```python
  from hypothesis import given
  from hypothesis.strategies import integers

  @given(integers(min_value=900))
  def test_meal_recommendation(calories):
      meals = get_recommended_meal(Recommendation.BY_CALORIES, calories)
      assert len(meals) == 3
      assert sum(meal.calories for meal in meals) < calories
  ```

### Mutation Testing
- **[DON'T]** Rely on tests that just check for execution (100% coverage, 0% robustness):
  ```python
  def test_foo_can_do_something():
      foo = Thingamajiggy()
      foo.doSomething()
      assert foo is not None # Mutmut will expose this test as useless
  ```
- **[DO]** Write tests that fail if logic is mutated (e.g., if `continue` is swapped for `break` or `<` to `<=`):
  ```python
  def test_meal_is_marked_as_over_calories():
      meals = [Meal("Fish", 1000), Meal("Salad", 100)]
      check_meals_for_calorie_overage(meals, 900)
      assert_meal_has_warning("Fish")
      # This specific assertion prevents a 'continue' -> 'break' mutation from surviving
      assert_no_warnings_displayed_on_meal("Salad") 
  ```