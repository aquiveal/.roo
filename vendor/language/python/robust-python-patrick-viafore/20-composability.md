# @Domain
Trigger these rules when writing, refactoring, or reviewing Python code, specifically when tasked with designing system architecture, creating reusable libraries, abstracting logic, or when requested to make code "composable", "extensible", or "reusable". 

# @Vocabulary
- **Composability**: The design principle of building small, discrete components with minimal inter-dependencies and little embedded business logic, allowing them to be freely mixed and matched to build new applications.
- **Policy**: The business logic of the system; the "what" that needs to be done (e.g., what to log, what data to save, the specific criteria for filtering recommendations).
- **Mechanism**: The implementation details of the system; the "how" an action is enacted (e.g., how to write to a log file, how to execute a database retry, the iteration algorithm for sorting).
- **Declarative Style**: A programming style where code expresses the logic of a computation (the policy) without describing its control flow (the mechanism), often appearing as a linear set of clear instructions.
- **Functional Programming (FP)**: A programming paradigm focusing on pure functions as first-class citizens.
- **Pure Function**: A function whose output is solely derived from its input arguments, completely free of side effects and independent of global state or environments.
- **Side Effect**: Any observable action a function performs outside of returning a value (e.g., mutating external variables, I/O operations, network calls).
- **Higher-Order Function**: A function that takes one or more functions as arguments, or returns a function as its result.
- **Decorator**: A higher-order function that wraps another function to modify or augment its behavior without altering the original function body.

# @Objectives
- Build small, discrete units of software that can be reused independently across different contexts.
- Strictly separate Policies (business logic) from Mechanisms (execution details) to prevent tangling unrelated concepts.
- Enable a declarative programming style where domain workflows are defined linearly without being bogged down by implementation details.
- Maximize the use of pure functions to reduce hidden physical dependencies.
- Compose algorithms by separating iteration/processing mechanisms from sorting/filtering criteria policies.

# @Guidelines
- **Component Size and Scope**: Keep components small and focused. Do not embed business logic into generic mechanisms. A generic component (like a data parser or retry handler) should never depend on a specific business policy (like a `BLTMaker`).
- **Policy vs. Mechanism Separation**: When designing a system, explicitly identify the mechanisms and extract them from the policy. The mechanism should be generic enough to serve multiple different policies.
- **Declarative Policies**: Write policy code such that it reads as a linear set of high-level instructions. Hide the complex mechanism calls behind simple, composable interfaces.
- **Avoid Linking Unrelated Policies**: Never make one policy depend on another policy simply to reuse a mechanism buried inside it. Extract the mechanism to a shared location instead.
- **Favor Pure Functions**: Strip side effects from your functions wherever possible. If a function only depends on its inputs to create its outputs, it is inherently composable and lacks external physical dependencies.
- **Use Decorators for Execution Mechanisms**: Abstract mechanisms related to execution flow (such as retries, caching, timing, or logging) into decorators. Do not pollute the body of a business logic function with `try/except` retry loops or `time.sleep()` calls.
- **Compose Multiple Decorators**: Stack multiple decorators on a single function to mix and match behaviors (e.g., one decorator for a specific exception retry, another for a timeout).
- **Abstract Algorithmic Mechanisms**: Do not write complex, nested `for` loops to sort, filter, and group data based on hardcoded business rules. Use Python's built-in iteration mechanisms (e.g., `sorted()`, `filter()`, `map()`) and `itertools` (e.g., `itertools.groupby`, `itertools.takewhile`).
- **Inject Algorithmic Policies**: Pass sorting keys, filtering conditions, and grouping criteria into your algorithmic mechanisms as injected policies (e.g., via a dataclass containing `Callable` properties or `lambda` functions).

# @Workflow
1. **Analyze the Request**: Break down the feature into "What needs to be done" (Policy) and "How it will be executed" (Mechanism).
2. **Extract Mechanisms**: Create generic functions, classes, or decorators to handle the "how" (e.g., database retry logic, standard sorting algorithms, a generic preparation tool). Ensure these mechanisms import ZERO business-specific code.
3. **Define the Policy**: Create dataclasses, higher-order functions, or scripts that define the specific business rules (e.g., a `RecommendationPolicy` containing lambda functions for specific filter limits).
4. **Isolate Side Effects**: Identify any I/O, state mutation, or network calls. Push these side effects to the boundaries of the system, keeping the core data transformation functions pure.
5. **Compose**: Construct the final feature by passing the defined Policy into the generic Mechanism, or by wrapping pure policy functions with mechanism decorators. Review the final policy code to ensure it reads declaratively.

# @Examples (Do's and Don'ts)

## Separating Policy from Mechanism (Execution Logic)
**[DO]** Use decorators to abstract the mechanism (retry logic, backoff) away from the policy (saving to the database).
```python
import backoff
import requests
from database import OperationException

@backoff.on_exception(backoff.expo, OperationException, max_tries=5)
@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_time=60)
def save_inventory_counts(inventory):
    for ingredient in inventory:
        inventory_db[ingredient.name] = ingredient.count
```

**[DON'T]** Mix mechanism (retry loops, sleeping) directly into the policy (saving data).
```python
import time
import requests
from database import OperationException

def save_inventory_counts(inventory):
    retry = True
    retry_counter = 0
    time_to_sleep = 1
    while retry:
        try:
            for ingredient in inventory:
                inventory_db[ingredient.name] = ingredient.count
            retry = False
        except OperationException:
            retry_counter += 1
            if retry_counter == 5:
                retry = False
        except requests.exceptions.HTTPError:
            time.sleep(time_to_sleep)
            time_to_sleep *= 2
            if time_to_sleep > 60:
                retry = False
```

## Composing Algorithms
**[DO]** Separate the iteration mechanism (`itertools`, `sorted`) from the policy (the `RecommendationPolicy` dataclass containing the criteria).
```python
import itertools
from dataclasses import dataclass
from typing import Callable

@dataclass
class RecommendationPolicy:
    meals: list[Meal]
    initial_sorting_criteria: Callable
    grouping_criteria: Callable
    secondary_sorting_criteria: Callable
    selection_criteria: Callable
    desired_number_of_recommendations: int

def recommend_meal(policy: RecommendationPolicy) -> list[Meal]:
    sorted_meals = sorted(policy.meals, key=policy.initial_sorting_criteria, reverse=True)
    grouped_meals = itertools.groupby(sorted_meals, key=policy.grouping_criteria)
    _, top_grouped = next(grouped_meals)
    
    secondary_sorted = sorted(top_grouped, key=policy.secondary_sorting_criteria, reverse=True)
    candidates = itertools.takewhile(policy.selection_criteria, secondary_sorted)
    
    return list(candidates)[:policy.desired_number_of_recommendations]

# Usage is fully declarative:
recommend_meal(RecommendationPolicy(
    meals=get_specials(),
    initial_sorting_criteria=get_proximity_to_surplus_ingredients,
    grouping_criteria=get_proximity_to_surplus_ingredients,
    secondary_sorting_criteria=get_proximity_to_last_meal,
    selection_criteria=proximity_greater_than_75_percent,
    desired_number_of_recommendations=3
))
```

**[DON'T]** Hardcode business policies into raw, nested algorithm mechanisms (`for` loops and `if` statements).
```python
def recommend_meal(last_meal: Meal, specials: list[Meal], surplus: list[Ingredient]) -> list[Meal]:
    highest_proximity = 0
    for special in specials:
        if (proximity := get_proximity(special, surplus)) > highest_proximity:
            highest_proximity = proximity
            
    grouped_by_surplus_matching = []
    for special in specials:
        if get_proximity(special, surplus) == highest_proximity:
            grouped_by_surplus_matching.append(special)
            
    filtered_meals = []
    for meal in grouped_by_surplus_matching:
        if get_proximity(meal, last_meal) > .75:
            filtered_meals.append(meal)
            
    sorted_meals = sorted(filtered_meals, key=lambda meal: get_proximity(meal, last_meal), reverse=True)
    return sorted_meals[:3]
```