@Domain
These rules are triggered when the AI is writing, refactoring, or optimizing Python code that involves data transformations, iterations, list/dictionary/set creation, filtering, mapping, or any scenario where imperative loops and state mutations can be replaced with functional programming paradigms.

@Vocabulary
*   **Pure Function**: A function with no side effects that takes an input and produces an output without keeping state or modifying anything not reflected in the return value (e.g., returning a modified copy rather than mutating the original object).
*   **Idempotent**: The property of a pure function where calling the exact same function repeatedly with the exact same arguments always returns the same result.
*   **Generator**: An object that behaves like an iterator by generating values on the fly using the `yield` statement, saving the stack reference, and resuming on the `next()` call to save memory.
*   **Coroutine (Generator)**: A generator that receives values passed into it via the `.send()` method, allowing dynamic input during iteration.
*   **Generator Expression**: An inline, memory-efficient generator defined using syntax similar to list comprehensions but enclosed in parentheses `()`.
*   **List Comprehension (listcomp)**: A concise syntax `[expression for item in iterable if condition]` used to construct lists inline without imperative `for` loops or state modification.
*   **Predicate**: A function that evaluates an item and returns a Boolean value, used heavily in filtering operations.

@Objectives
*   Transition Python code from stateful, imperative, and object-mutating patterns into stateless, purely functional patterns.
*   Maximize memory efficiency when handling large datasets by utilizing generators and iterables instead of pre-computing full collections in memory.
*   Enhance code readability and brevity by utilizing list/dict/set comprehensions and built-in functional primitives (`map`, `filter`, `any`, `all`, `zip`, `enumerate`).
*   Eliminate limitations of inline `lambda` expressions by leveraging `functools.partial` and the `operator` module.

@Guidelines
*   **Enforce Pure Functions**: The AI MUST NOT modify arguments in place (e.g., using `list.pop()`). The AI MUST write purely functional functions that return modified copies of the data (e.g., using slicing `list[:-1]`) to ensure thread-safety, modularity, and testability.
*   **Implement Generators for Large Data**: When iterating over or generating large datasets, the AI MUST use generators (`yield`) or generator expressions `()` instead of building entire lists in memory to prevent `MemoryError`.
*   **Use Coroutine Patterns**: The AI MUST use `yield` as an assignment (`var = yield result`) and `.send(value)` when values need to be dynamically passed into a generator during execution.
*   **Replace Loops with Comprehensions**: The AI MUST replace imperative `for` loops that iteratively `.append()` to lists with List Comprehensions `[]`. The AI MUST also use Dict `{k: v}` and Set `{v}` comprehensions where applicable. The AI MUST NOT modify variables or states inside a comprehension.
*   **Use Functional Built-ins**: The AI MUST utilize Python's functional built-ins instead of custom loops:
    *   Use `map(function, iterable)` to apply transformations.
    *   Use `filter(predicate, iterable)` to filter items.
    *   Use `enumerate(iterable)` instead of manual index counters (`i += 1`).
    *   Use `sorted(iterable, key=...)` for sorting.
    *   Use `any(iterable)` and `all(iterable)` for boolean evaluations instead of iterative flag-setting.
    *   Use `zip(iter1, iter2)` to combine multiple sequences.
*   **Optimize "First Match" Lookups**: The AI MUST use `next((x for x in iterable if condition), default)` or the external `first` package to find the first item satisfying a condition, bypassing the need to evaluate the entire list or write multi-line loops.
*   **Avoid Complex Lambdas**: Because `lambda` is restricted to a single line, the AI MUST NOT write overly complex or nested lambdas. Instead, the AI MUST use `functools.partial` combined with functions from the `operator` module (e.g., `operator.le`, `operator.itemgetter`) to create reusable, pre-configured functions.
*   **Leverage Itertools**: The AI MUST utilize the `itertools` module (`accumulate`, `chain`, `combinations`, `groupby`, etc.) for complex iterator manipulations rather than writing custom generator logic from scratch.
*   **Generator Debugging**: When debugging generators, the AI MUST utilize `inspect.isgeneratorfunction()` and `inspect.getgeneratorstate()` (to check for `GEN_CREATED`, `GEN_SUSPENDED`, `GEN_CLOSED`).
*   **Python 3 Iterable Awareness**: The AI MUST acknowledge that `map()`, `filter()`, and `zip()` return iterables (not lists) in Python 3, making them inherently memory efficient.

@Workflow
1.  **Analyze State and Side Effects**: Review the target function. If it modifies an input array, dictionary, or global variable, rewrite it to return a fresh, modified copy (pure function).
2.  **Evaluate Memory Constraints**: If the function processes large volumes of data, replace list instantiations with `yield` statements to create a generator, or use generator expressions `(...)`.
3.  **Refactor Iteration to Comprehensions**: Identify `for` loops used solely for building collections. Replace them with list `[...]`, set `{...}`, or dict `{k: v ...}` comprehensions.
4.  **Substitute Built-ins**: Identify loops used for transforming, filtering, or evaluating data. Replace them with `map()`, `filter()`, `any()`, `all()`, or `zip()`. Apply `enumerate()` if an index is required.
5.  **Optimize Search Operations**: If a loop is used to find the first element matching a predicate, rewrite it using the `next((generator), default)` idiom.
6.  **Refactor Callables**: Review `lambda` functions used as `key` or predicate arguments. If they rely on hardcoded arguments or basic operators, replace them using `functools.partial` and `operator` methods.

@Examples (Do's and Don'ts)

**Principle: Pure Functions (No Side Effects)**
[DON'T]
```python
def remove_last_item(mylist):
    mylist.pop(-1) # Modifies state
```
[DO]
```python
def butlast(mylist):
    return mylist[:-1] # Returns a copy
```

**Principle: Memory-Efficient Generation**
[DON'T]
```python
a = list(range(10000000)) # Triggers MemoryError for large datasets
for value in a:
    if value == 50000:
        print("Found it")
        break
```
[DO]
```python
# Generates dynamically, preventing MemoryError
for value in range(10000000): 
    if value == 50000:
        print("Found it")
        break
```

**Principle: List Comprehensions**
[DON'T]
```python
x = []
for i in (1, 2, 3):
    x.append(i)
```
[DO]
```python
x = [i for i in (1, 2, 3)]
```

**Principle: Using Enumerate**
[DON'T]
```python
i = 0
while i < len(mylist):
    print("Item %d: %s" % (i, mylist[i]))
    i += 1
```
[DO]
```python
for i, item in enumerate(mylist):
    print("Item %d: %s" % (i, item))
```

**Principle: Finding the First Item**
[DON'T]
```python
def first_positive_number(numbers):
    for n in numbers:
        if n > 0:
            return n
```
[DO]
```python
# Using a generator expression with next() and a default value
next((x for x in numbers if x > 0), None)
```

**Principle: Replacing Lambdas with Partial and Operator**
[DON'T]
```python
def greater_than_zero(number):
    return number > 0

first([-1, 0, 1, 2], key=lambda x: greater_than_zero(x))
```
[DO]
```python
import operator
from functools import partial
from first import first

# Replaces lambda by utilizing partial and built-in operator
first([-1, 0, 1, 2], key=partial(operator.le, 0))
```

**Principle: Coroutines (Passing Values to Generators)**
[DON'T] (Relying on external state modification for generator logic)
```python
# Modifying global/external state to change generator output
```
[DO]
```python
def shorten(string_list):
    length = len(string_list[0])
    for s in string_list:
        # yield returns a value AND receives value sent via .send()
        length = yield s[:length] 

gen = shorten(['loremipsum', 'dolorsit'])
s = next(gen)
s = gen.send(4) # dynamically adjust the next iteration
```