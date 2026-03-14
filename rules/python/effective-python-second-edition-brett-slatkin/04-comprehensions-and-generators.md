# @Domain
These rules MUST be triggered whenever the AI is writing, refactoring, or reviewing Python code that involves processing sequences, filtering data, mapping transformations, creating iterables/iterators, building collections (lists, dictionaries, sets), managing memory for large datasets, or using generator functions.

# @Vocabulary
- **Comprehension:** Compact Python syntax for deriving a new list, dictionary, or set from another sequence or iterable.
- **Generator:** A function that uses `yield` expressions to incrementally produce a sequence of values, minimizing memory footprint by yielding one item at a time.
- **Generator Expression:** A memory-efficient generalization of list comprehensions enclosed in `()`, which evaluates to an iterator instead of materializing the entire sequence in memory.
- **Assignment Expression (Walrus Operator `:=`):** Syntax introduced in Python 3.8 used to both assign and evaluate a variable in a single expression.
- **Iterator Protocol:** The mechanism by which Python `for` loops traverse containers, utilizing `iter()` (which calls `__iter__`) and `next()` (which calls `__next__` until `StopIteration` is raised).
- **Stateful Iterator:** An iterator that can only be consumed once. Iterating over it again produces no results and raises `StopIteration`.
- **Iterable Container:** A custom Python class that implements the `__iter__` special method as a generator, ensuring a fresh iterator is returned each time `iter()` is called.
- **itertools:** A Python built-in module containing highly optimized functions for linking iterators, filtering items, and producing combinations of items.

# @Objectives
- Maximize readability by replacing verbose iteration logic and obfuscated functional programming paradigms with concise comprehensions.
- Enforce strict limits on the cognitive complexity of comprehensions.
- Prevent memory explosion and out-of-memory crashes by strictly preferring generators and generator expressions over materialized lists for large data.
- Ensure functional purity and prevent silent bugs caused by exhausted iterators.
- Optimize performance by eliminating redundant computations within iterations using assignment expressions.

# @Guidelines
- **Prefer Comprehensions over Functional Built-ins:** The AI MUST use list, dict, and set comprehensions instead of combining the `map` and `filter` built-in functions with `lambda` expressions.
- **Limit Comprehension Complexity:** The AI MUST NOT use more than two control subexpressions in a comprehension (e.g., two `for` loops, two `if` conditions, or one `for` loop and one `if` condition). If a comprehension requires three or more control subexpressions, the AI MUST rewrite it using normal `for` loops and `if` statements (often inside a helper function).
- **Prevent Redundant Computation:** When the same computation is used in both the condition and the value expression of a comprehension or generator expression, the AI MUST use an assignment expression (`:=`) in the condition to compute and assign the value, and then reference that variable in the value expression.
- **Prevent Loop Variable Leakage:** The AI MUST NOT use an assignment expression (`:=`) in the value expression of a comprehension without an `if` condition, as this leaks the loop variable into the containing scope.
- **Prefer Generators for Sequences:** When writing a function that produces a sequence of results, the AI MUST use a generator (`yield`) instead of appending to a list and returning the list, especially if the size of the output is unbounded or unknown.
- **Defensive Iteration:** When writing a function that iterates over an input argument multiple times, the AI MUST check if the input is an iterator and raise a `TypeError` if so. The AI MUST use `if iter(numbers) is numbers:` or `if isinstance(numbers, collections.abc.Iterator):` to detect iterators.
- **Provide Iterable Containers for Repeated Iteration:** If a sequence needs to be iterated multiple times without copying it entirely into memory, the AI MUST implement a custom container class with an `__iter__` method defined as a generator.
- **Use Generator Expressions for Large Data:** The AI MUST use generator expressions `(x for x in ...)` instead of list comprehensions `[x for x in ...]` when dealing with large or infinite input streams to avoid memory exhaustion.
- **Compose Generators Safely:** The AI MUST use the `yield from` expression to compose multiple nested generators into a single generator. The AI MUST NOT use manual `for` loops with `yield` to iterate over nested generators.
- **Avoid `send` in Generators:** The AI MUST NOT use the `send` method to inject data into generators. It causes confusing state, especially when combined with `yield from` (which yields unexpected `None` values). Instead, the AI MUST pass an iterator into the generator function to cascade inputs.
- **Avoid `throw` in Generators:** The AI MUST NOT use the `throw` method to trigger state transitions or inject exceptions into generators. Instead, the AI MUST use an iterable container class with methods that manage exceptional state transitions.
- **Utilize `itertools`:** The AI MUST use functions from the `itertools` built-in module for complex iterations:
  - *Linking:* `chain`, `repeat`, `cycle`, `tee`, `zip_longest`
  - *Filtering:* `islice`, `takewhile`, `dropwhile`, `filterfalse`
  - *Combinations:* `accumulate`, `product`, `permutations`, `combinations`, `combinations_with_replacement`

# @Workflow
1. **Sequence Generation Analysis:** When tasked with generating a new sequence, evaluate if the data transformation is simple enough to fit into a comprehension (<= 2 control subexpressions). If not, implement a helper function using standard loops.
2. **Built-in Replacement Check:** Scan the code for instances of `map()` and `filter()`. Replace them with equivalent comprehensions unless the `map` operation uses a single-argument built-in function without a lambda.
3. **Memory Bounding Check:** Evaluate the potential size of the input/output sequence. If the sequence could exceed available memory or involves file/network I/O, immediately convert the list comprehension to a generator expression, or the list-returning function into a generator function.
4. **Redundancy Elimination:** Scan comprehensions for identical function calls or math operations in both the `if` and output clauses. Consolidate these using the walrus operator (`:=`) placed strictly in the `if` clause.
5. **Defensive Parameter Check:** If a function iterates over a parameter more than once, inject a type-check at the top of the function to reject bare iterators. If the user provides an iterator, instruct them to wrap their generator in an iterable container class via the `__iter__` protocol.
6. **Generator Composition Optimization:** If multiple generators are executed sequentially or nested, refactor them into a unified generator using `yield from`.
7. **Stateful Generator Purge:** Audit generator usage for `.send()` or `.throw()`. Refactor `.send()` out by passing iterators as arguments. Refactor `.throw()` out by defining stateful iterable classes.

# @Examples (Do's and Don'ts)

**Concept: Comprehensions vs. Map/Filter**
- [DO]
  ```python
  even_squares = [x**2 for x in a if x % 2 == 0]
  ```
- [DON'T]
  ```python
  even_squares = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
  ```

**Concept: Comprehension Complexity**
- [DO]
  ```python
  flat = []
  for sublist1 in my_lists:
      for sublist2 in sublist1:
          flat.extend(sublist2)
  ```
- [DON'T]
  ```python
  # Hard to read: 3 control subexpressions
  flat = [x for sublist1 in my_lists for sublist2 in sublist1 for x in sublist2]
  ```

**Concept: Assignment Expressions in Comprehensions**
- [DO]
  ```python
  found = {name: batches for name in order
           if (batches := get_batches(stock.get(name, 0), 8))}
  ```
- [DON'T]
  ```python
  # Repeated get_batches computation
  found = {name: get_batches(stock.get(name, 0), 8) for name in order
           if get_batches(stock.get(name, 0), 8)}
  ```

**Concept: Generators Instead of Returning Lists**
- [DO]
  ```python
  def index_words_iter(text):
      if text:
          yield 0
      for index, letter in enumerate(text):
          if letter == ' ':
              yield index + 1
  ```
- [DON'T]
  ```python
  def index_words(text):
      result = []
      if text:
          result.append(0)
      for index, letter in enumerate(text):
          if letter == ' ':
              result.append(index + 1)
      return result
  ```

**Concept: Defensive Iteration Arguments**
- [DO]
  ```python
  def normalize_defensive(numbers):
      if iter(numbers) is numbers:  # Reject single-use iterators
          raise TypeError('Must supply a container')
      total = sum(numbers)
      return [100 * value / total for value in numbers]

  class ReadVisits:
      def __init__(self, data_path):
          self.data_path = data_path
      def __iter__(self):
          with open(self.data_path) as f:
              for line in f:
                  yield int(line)
  ```
- [DON'T]
  ```python
  def normalize(numbers):
      total = sum(numbers)
      # If numbers is a generator, this loop will silently execute zero times!
      return [100 * value / total for value in numbers]
  ```

**Concept: Composing Generators with `yield from`**
- [DO]
  ```python
  def animate_composed():
      yield from move(4, 5.0)
      yield from pause(3)
      yield from move(2, 3.0)
  ```
- [DON'T]
  ```python
  def animate():
      for delta in move(4, 5.0):
          yield delta
      for delta in pause(3):
          yield delta
      for delta in move(2, 3.0):
          yield delta
  ```

**Concept: Injecting Data into Generators**
- [DO]
  ```python
  def wave_cascading(amplitude_it, steps):
      step_size = 2 * math.pi / steps
      for step in range(steps):
          radians = step * step_size
          fraction = math.sin(radians)
          amplitude = next(amplitude_it)  # Pull input safely
          yield amplitude * fraction
  ```
- [DON'T]
  ```python
  def wave_modulating(steps):
      step_size = 2 * math.pi / steps
      amplitude = yield  # Initial receive
      for step in range(steps):
          radians = step * step_size
          fraction = math.sin(radians)
          amplitude = yield amplitude * fraction  # Fragile send() target
  ```