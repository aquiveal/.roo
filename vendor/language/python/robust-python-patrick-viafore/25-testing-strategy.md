# @Domain
Trigger these rules when tasked with creating, modifying, planning, or refactoring Python tests, specifically utilizing the `pytest` framework, or when defining an overall testing strategy for a Python codebase.

# @Vocabulary
- **Test Strategy**: A deliberate plan outlining the time and effort spent testing software to mitigate risk, framed as a list of questions the tests must answer (e.g., functional, security, usability).
- **Testing Pyramid**: A heuristic for prioritizing tests based on their value-to-cost ratio, favoring fast, isolated tests at the base and slower, costly tests at the top.
- **AAA Pattern**: A structural convention for writing tests composed of Arrange, Act, and Assert steps.
- **Annihilate**: A fourth "A" representing the cleanup or teardown phase, ensuring resources are isolated and properly released.
- **Arrange**: The phase of a test where preconditions, dependencies, and test data are set up.
- **Act**: The phase of a test where the core operation being verified is executed.
- **Assert**: The phase of a test where post-conditions are verified against expectations.
- **Fixture**: A `pytest` construct used to encapsulate boilerplate setup (Arrange) and teardown (Annihilate) code.
- **Mocking**: Substituting a complex dependency with a simplified, fake object (often relying on Python's duck typing) to isolate the code under test.
- **Monkeypatching**: Dynamically swapping out methods at runtime to inject mocks. Considered an anti-pattern when overused, as it indicates a system is too tightly coupled physically.
- **Parameterization**: Executing the same test logic over a table of different input and output parameters (table-driven tests) using `@pytest.mark.parametrize`.
- **Hamcrest Matchers**: An assertion library (`PyHamcrest`) that reads like natural language, allowing for highly readable and custom assertion definitions.

# @Objectives
- Treat test code as a first-class citizen of the codebase, demanding the same level of readability, robustness, and maintainability as production code.
- Prioritize the value-to-cost ratio; maximize test value while minimizing the cost of writing, running, and maintaining tests.
- Enforce the AAA (Arrange, Act, Assert) + Annihilate pattern rigorously in every test function to reduce cognitive load for future maintainers.
- Guarantee total test isolation; no test should ever depend on or affect the state of another test.
- Drive the test design based on the specific questions the software must answer (e.g., unit, integration, acceptance, load).

# @Guidelines
### Strategic Testing Rules
- You MUST identify the "why" and "what" of a test before writing it. Explicitly state the question the test answers (e.g., "Does the boundary case act as expected?").
- You MUST prioritize tests with a high value-to-cost ratio. If a test is extremely costly to write or maintain but offers low impact, propose alternative architectural solutions or modularization.
- You MUST NOT overuse `monkeypatching`. If you find yourself heavily monkeypatching, you MUST suggest refactoring the code to reduce physical dependencies and enable cleaner duck-typed mocking.

### AAA Formatting Rules
- You MUST visually segment every test function into `Arrange`, `Act`, and `Assert` sections (using comments if helpful).
- **Arrange**: 
  - You MUST abstract massive or repetitive setup blocks into helper functions or `@pytest.fixture` definitions. Keep the Arrange step in the actual test function brief.
- **Annihilate (Teardown)**: 
  - You MUST NOT share resources (global variables, class variables, database states) between tests.
  - You MUST NOT place manual cleanup code directly at the bottom of a test function, as it will be skipped if an assertion fails.
  - You MUST use context managers (`with` blocks) or `pytest` fixtures utilizing the `yield` keyword to guarantee teardown execution.
- **Act**: 
  - You MUST restrict the Act phase to 1 or 2 lines of code. Less is more.
  - You MUST use `@pytest.mark.parametrize` to convert repetitive tests into table-driven tests.
  - You MUST NOT exceed 3 or 4 parameters in a parameterized test to maintain readability.
- **Assert**:
  - You MUST restrict tests to a single logical assertion concept near the end of the test. Do not jam multiple unrelated assertions into one test.
  - You MUST provide verbose, informative string messages in assertions when using the built-in `assert` (e.g., `assert val == expected, "Informative error message"`).
  - You SHOULD consider using `PyHamcrest` (`assert_that`, `is_`, `equal_to`) for complex assertions to build a natural, readable testing vocabulary.

# @Workflow
1. **Define the Question**: Determine exactly what business/system question the test is answering.
2. **Setup Isolation (Annihilate/Arrange)**: Identify required resources. Abstract their initialization into a `@pytest.fixture` that `yield`s the resource and cleans it up immediately after.
3. **Write the Act Phase**: Write the 1-2 lines of code that perform the core action.
4. **Write the Assert Phase**: Write a single logical assertion verifying the post-condition. Include a verbose failure message.
5. **Refactor for Reusability**: If writing similar tests, extract the common setup into helper functions or convert the test into a table-driven test using `@pytest.mark.parametrize`.
6. **Review for Anti-Patterns**: Check for excessive `monkeypatching` or missing teardowns. Refactor to use simple mock classes (duck typing) if dependencies are too rigid.

# @Examples (Do's and Don'ts)

### Annihilate / Teardown
- **[DO]** Use `yield` fixtures to guarantee cleanup regardless of assertion failures:
  ```python
  import pytest

  @pytest.fixture
  def test_database(db_creation):
      # Arrange
      database = db_creation()
      database.populate_base_ingredients()
      try:
          yield database
      finally:
          # Annihilate
          database.cleanup()

  def test_calorie_calculation(test_database):
      # Act
      calories = get_calories("Bacon Cheeseburger")
      # Assert
      assert calories == 1200
  ```
- **[DON'T]** Put manual cleanup at the bottom of the test function:
  ```python
  def test_calorie_calculation():
      db = setup_db()
      calories = get_calories("Bacon Cheeseburger")
      assert calories == 1200 # If this fails, cleanup_database() never runs!
      cleanup_database(db) 
  ```

### Act / Parameterization
- **[DO]** Use `@pytest.mark.parametrize` for repeating identical act/assert logic across data boundaries:
  ```python
  @pytest.mark.parametrize(
      "extra_ingredients, dish_name, expected_calories",
      [
          (["Bacon", 2400], "Bacon Cheeseburger", 900),
          ([], "Cobb Salad", 1000),
          ([], "Mashed Potatoes", 400)
      ]
  )
  def test_calorie_calculation(extra_ingredients, dish_name, expected_calories, test_database):
      for ingredient in extra_ingredients:
          test_database.add_ingredient(ingredient)
      setup_dish_ingredients(dish_name)
      
      calories = get_calories(dish_name)
      
      assert calories == expected_calories, f"Incorrect calories for {dish_name}"
  ```
- **[DON'T]** Write massive inline loops or copy-paste identical tests 10 times for different inputs.

### Arrange / Boilerplate
- **[DO]** Extract heavy Arrange steps into helper functions to make the test's unique parameters obvious at a glance:
  ```python
  def test_calorie_calculation_with_substitution():
      # Arrange
      add_base_ingredients_to_database()
      setup_bacon_cheeseburger(bacon="Turkey Bacon")
      
      # Act
      calories = get_calories("Bacon Cheeseburger")
      
      # Assert
      assert calories == 1100, "Turkey bacon substitution did not reduce calories as expected"
  ```
- **[DON'T]** Inline 20 lines of database population directly inside the test function, obscuring the actual purpose of the test.

### Assert / Verbosity
- **[DO]** Use custom Hamcrest matchers or verbose assert strings for clear failure outputs:
  ```python
  from hamcrest import assert_that, is_, empty

  def test_no_restaurant_found_in_non_matching_areas():
      restaurants = find_owned_restaurants_in("Huntsville, AL")
      assert_that(restaurants, is_(empty()))
  ```
- **[DON'T]** Chain dozens of unrelated asserts in a single test, or use naked asserts without context (`assert x == y`).