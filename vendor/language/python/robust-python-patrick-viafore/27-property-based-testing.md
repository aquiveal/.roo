# @Domain
Trigger these rules when tasked with writing, refactoring, or reviewing Python tests, specifically when traditional parameterized tests are brittle, when testing complex algorithms, when evaluating stateful objects over a sequence of operations, or when manual boundary value analysis is insufficient to capture all edge cases.

# @Vocabulary
- **Property-Based Testing (Generative Testing)**: A testing methodology where tools automatically generate diverse test cases to verify properties rather than testing specific hardcoded input/output combinations.
- **Properties / Invariants**: Immutable truths or guarantees about a system that must always hold true regardless of the input provided.
- **Boundary Value Analysis**: A traditional testing technique that involves analyzing code to find equivalence classes and testing the exact boundaries between them.
- **Equivalence Classes**: Sets of input values that share the same property or trigger the same execution path.
- **Hypothesis**: The standard Python library for property-based testing.
- **Shrinking**: The process Hypothesis performs after finding a failing test case to incrementally reduce the input to the absolute minimal failing value.
- **Strategy**: A Hypothesis construct that defines exactly how test cases are generated and how the data gets shrunk upon failure.
- **Composite Strategy**: A custom, user-defined Hypothesis strategy built by composing existing strategies using the `@composite` decorator and the `draw` function.
- **Stateful Testing**: A generative testing approach used to test combinations of operations and algorithmic steps via a state machine.
- **Example Database**: A database (local file system, Redis, or Multiplexed) where Hypothesis records previously failing examples to test them explicitly in future runs.

# @Objectives
- Supplement traditional deterministic testing with property-based generative testing to build a more comprehensive safety net.
- Shift focus from hardcoding specific inputs/outputs to defining and verifying universal system invariants.
- Utilize Hypothesis strategies to automatically generate edge cases and bypass the limitations of manual boundary value analysis.
- Embrace nondeterminism in test generation to uncover hidden bugs and reduce test fragility.
- Leverage stateful testing to verify complex algorithms and state mutations over an arbitrary sequence of events.

# @Guidelines
- **Test Generation Strategy**
  - The AI MUST NOT rely solely on hardcoded input/output combinations if the input domain is vast or complex.
  - The AI MUST use `hypothesis` (`from hypothesis import given`) to generate test inputs dynamically.
  - The AI MUST test properties (e.g., "the sum of all dish calories is less than the target") rather than specific results (e.g., `assert meals == [Meal("A"), Meal("B")]`).
- **Using Hypothesis Strategies**
  - The AI MUST use appropriate strategies from `hypothesis.strategies` (e.g., `integers()`, `floats()`, `text()`, `times()`, `dictionaries()`, `lists()`).
  - The AI MUST apply constraints directly to strategies whenever possible using strategy arguments (e.g., `integers(min_value=900, max_value=2000)`).
- **Custom and Composite Strategies**
  - The AI MUST use the `@composite` decorator and the `draw()` function to build complex or domain-specific strategies.
  - The AI MAY use `.map()` and `.filter()` on strategies for further customization.
- **Filtering and Explicit Examples**
  - The AI MUST use `hypothesis.assume(condition)` to skip invalid generated test cases that cannot be constrained directly via strategy arguments.
  - The AI MUST use the `@example(value)` decorator to guarantee that known, specific edge cases or previous failures are always explicitly tested on every run.
- **Stateful Testing**
  - When testing algorithms or objects that require a combination of steps/operations, the AI MUST use `hypothesis.stateful.RuleBasedStateMachine`.
  - The AI MUST define actions using the `@rule` decorator and pass strategies to the rule parameters.
  - The AI MUST verify state after rules are applied using the `@invariant` decorator.
  - The AI MUST assign the state machine's `TestCase` to a variable prefixed with `Test` so standard test runners (like pytest) can discover it (e.g., `TestMyAlgorithm = MyChecker.TestCase`).
- **Database Configuration**
  - The AI SHOULD recommend or configure an Example Database when setting up Hypothesis for a team or CI/CD environment.
  - The AI MUST suggest `hypothesis.database.MultiplexedDatabase` to combine shared CI failure databases (e.g., Redis) with a developer's local `.hypothesis/examples` database.

# @Workflow
1. **Analyze Invariants**: Identify the core properties and invariants of the function or class under test. What must ALWAYS be true?
2. **Select Strategies**: Map the input parameters of the target function to standard `hypothesis.strategies`.
3. **Build Composite Data (If Needed)**: If the target requires complex objects, write a `@composite` function utilizing `draw()` to pull from primitive strategies to instantiate the domain objects.
4. **Write the Test**: Decorate the test function with `@given` and inject the selected strategies.
5. **Apply Constraints**: Constrain the input domain using `min_value`/`max_value` arguments, or apply `assume()` inside the test body for complex conditional filtering.
6. **Add Explicit Examples**: Decorate the test with `@example(...)` for any known critical boundaries or historical regressions.
7. **Implement Stateful Tests (For Algorithms)**: If testing an algorithm or state machine:
   a. Subclass `RuleBasedStateMachine`.
   b. Initialize the target object and tracking variables in `__init__`.
   c. Create mutation steps using `@rule(...)`.
   d. Create assertion steps using `@invariant()`.
   e. Expose the test case to the test runner via `<TestName> = <StateMachineClass>.TestCase`.

# @Examples (Do's and Don'ts)

### Testing Invariants with Hypothesis
**[DO]**
```python
from hypothesis import given, assume, example
from hypothesis.strategies import integers

@given(integers(min_value=1))
@example(5001)  # Explicitly test a known historical edge case
def test_meal_recommendation_under_specific_calories(calories):
    # Skip difficult to constrain logic natively inside the strategy
    assume(calories != 1234)
    
    meals = get_recommended_meal(Recommendation.BY_CALORIES, calories)
    
    # Assert invariants/properties rather than specific outputs
    assert len(meals) == 3
    assert is_appetizer(meals[0])
    assert is_salad(meals[1])
    assert is_main_dish(meals[2])
    assert sum(meal.calories for meal in meals) < calories
```

**[DON'T]**
```python
# Anti-pattern: Brittle, hardcoded test that relies on manual boundary value analysis and specific outputs
def test_meal_recommendation_under_specific_calories():
    calories = 900
    meals = get_recommended_meal(Recommendation.BY_CALORIES, calories)
    # Fragile: Breaks immediately if the menu or recommendation algorithm changes
    assert meals == [Meal("Spring Roll", 120), Meal("Green Papaya Salad", 230), Meal("Larb Chicken", 500)]
```

### Creating Composite Strategies
**[DO]**
```python
from hypothesis import given
from hypothesis.strategies import composite, integers
from my_domain import Dish

ThreeCourseMeal = tuple[Dish, Dish, Dish]

@composite
def three_course_meals(draw) -> ThreeCourseMeal:
    appetizer_calories = integers(min_value=100, max_value=900)
    main_dish_calories = integers(min_value=550, max_value=1800)
    dessert_calories = integers(min_value=500, max_value=1000)
    
    return (
        Dish("Appetizer", draw(appetizer_calories)),
        Dish("Main Dish", draw(main_dish_calories)),
        Dish("Dessert", draw(dessert_calories))
    )

@given(three_course_meals())
def test_three_course_meal_substitutions(three_course_meal: ThreeCourseMeal):
    assert sum(dish.calories for dish in three_course_meal) >= 1150
```

**[DON'T]**
```python
# Anti-pattern: Manually building randomized data in the test, defeating Hypothesis's shrinking mechanics
import random

def test_three_course_meal_substitutions():
    # Shrinking cannot apply to `random.randint`
    meal = (
        Dish("Appetizer", random.randint(100, 900)),
        Dish("Main Dish", random.randint(550, 1800)),
        Dish("Dessert", random.randint(500, 1000))
    )
    assert sum(dish.calories for dish in meal) >= 1150
```

### Stateful Testing for Algorithms
**[DO]**
```python
from functools import reduce
from hypothesis.strategies import integers
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule

class RecommendationChecker(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.recommender = MealRecommendationEngine()
        self.filters = []

    @rule(price_limit=integers(min_value=6, max_value=200))
    def filter_by_price(self, price_limit):
        self.recommender.apply_price_filter(price_limit)
        self.filters = [f for f in self.filters if f[0] != "price"]
        self.filters.append(("price", lambda m: m.price))

    @invariant()
    def recommender_provides_three_unique_meals(self):
        assert len(self.recommender.get_meals()) == 3
        assert len(set(self.recommender.get_meals())) == 3

# Expose the TestCase so pytest can discover and run it
TestRecommender = RecommendationChecker.TestCase
```

**[DON'T]**
```python
# Anti-pattern: Manually executing a specific hardcoded sequence of operations to test algorithmic state
def test_recommendation_algorithm_state():
    recommender = MealRecommendationEngine()
    recommender.apply_price_filter(6)
    recommender.apply_distance_filter(0)
    recommender.apply_price_filter(16)
    
    # Fails to test the thousands of other combinations Hypothesis would find automatically
    assert len(recommender.get_meals()) == 3
```