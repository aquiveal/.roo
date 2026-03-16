@Domain
This rule set activates whenever the AI is generating, refactoring, evaluating, or reviewing Python code that involves sequence processing, data transformation, iteration, list/dictionary/set construction, or streaming data structures. It applies to any task requiring loops, derivations of sequences, map/filter paradigms, or data generation.

@Vocabulary
- **Comprehension**: A compact Python syntax for deriving a new list, dictionary, or set from another sequence or iterable, supporting built-in filtering and transformation.
- **Generator**: A function that uses `yield` expressions to produce a sequence of results one at a time, lazily, rather than computing and storing them all in memory at once.
- **Generator Expression**: A generalization of list comprehensions enclosed in parentheses `()` that evaluates to an iterator yielding one item at a time, preventing memory exhaustion for large inputs.
- **Assignment Expression (Walrus Operator `:=`)**: Syntax introduced in Python 3.8 that assigns a value to a variable and evaluates to that value in a single expression.
- **Iterator**: A stateful object that produces results a single time and raises a `StopIteration` exception when exhausted.
- **Iterable Container**: A class that implements the iterator protocol by defining an `__iter__` method as a generator, allowing it to be iterated over multiple times.
- **Iterator Protocol**: The mechanism by which Python `for` loops and related expressions traverse containers (calling `iter()` which calls `__iter__`, then repeatedly calling `next()`).
- **`yield from`**: An expression that yields all values from a nested generator before returning control to the parent generator.
- **`.send()`**: A generator method that injects a value into the generator, becoming the result of the `yield` expression.
- **`.throw()`**: A generator method that re-raises an exception at the position of the most recently executed `yield` expression.

@Objectives
- Maximize code readability and compactness by prioritizing comprehensions over traditional loop-and-append or functional paradigms (`map`/`filter`).
- Prevent out-of-memory crashes by defaulting to generators and generator expressions for large or infinite data streams.
- Ensure correctness and prevent data-loss bugs when iterating over arguments multiple times.
- Eliminate redundant computation in loops and comprehensions using assignment expressions.
- Maintain transparent, maintainable generator architectures by avoiding complex internal state transitions (`send`/`throw`).

@Guidelines
- **Comprehension Priority**: The AI MUST use list, dictionary, or set comprehensions instead of the `map` and `filter` built-in functions. The AI MUST NOT use `map` with `lambda` expressions for sequence derivation.
- **Comprehension Complexity Limits**: The AI MUST avoid using more than two control subexpressions in a comprehension (e.g., two `for` loops, or one `for` loop and one `if` condition). If logic requires three or more control subexpressions, the AI MUST refactor the logic into normal `if` and `for` statements, ideally encapsulated in a helper generator function.
- **Eliminating Redundancy in Comprehensions**: The AI MUST use the walrus operator (`:=`) within the condition part of a comprehension to assign and evaluate a computation if that same computation is referenced in the value part of the comprehension.
- **Scope Leakage Prevention**: The AI MUST NOT use the walrus operator (`:=`) in the value expression of a comprehension if that comprehension lacks an `if` condition, as this leaks the loop variable into the containing scope.
- **Generator Return Preference**: The AI MUST consider using generators (functions yielding values) instead of functions that accumulate results in a local `list` and return that list. 
- **Defensive Iteration**: When writing a function that iterates over an input argument multiple times, the AI MUST check if the input is an iterator. The AI MUST raise a `TypeError` if `iter(numbers) is numbers` or `isinstance(numbers, Iterator)` evaluates to True.
- **Container Class Implementation**: To support multiple iterations over streaming data without copying the entire iterator to memory, the AI MUST create a custom container class that defines the `__iter__` method as a generator.
- **Generator Expressions for Large Data**: The AI MUST use generator expressions `(...)` instead of list comprehensions `[...]` when processing large data inputs (e.g., reading files line-by-line) to avoid memory exhaustion. The AI MUST chain generator expressions together for multi-step processing of large streams.
- **Generator Composition**: The AI MUST use the `yield from` expression to compose multiple nested generators into a single generator. The AI MUST NOT use manual `for x in nested_generator(): yield x` loops.
- **Avoid `.send()`**: The AI MUST NOT use the `.send()` method to inject data into generators, as it causes confusing behavior (especially with `None` values when transitioning between `yield from` generators). Instead, the AI MUST pass an iterator into the generator's arguments and call `next()` on it to pull data.
- **Avoid `.throw()`**: The AI MUST NOT use the `.throw()` method to cause state transitions or exceptional behavior within generators. Instead, the AI MUST define a stateful class implementing the `__iter__` method to manage exceptional state transitions.
- **Utilize itertools**: The AI MUST leverage the `itertools` built-in module for complex iterator manipulation:
  - Use `chain` to combine iterators sequentially.
  - Use `repeat` and `cycle` for repeating items.
  - Use `tee` to split a single iterator into multiple parallel iterators.
  - Use `zip_longest` to iterate over differently sized iterators without truncation.
  - Use `islice`, `takewhile`, `dropwhile`, and `filterfalse` for advanced filtering.
  - Use `accumulate`, `product`, `permutations`, `combinations`, and `combinations_with_replacement` for combinatorial logic.

@Workflow
1. **Analyze Sequence Processing**: Identify any logic that derives new lists, dicts, or sets, or processes streams of data.
2. **Refactor Functional Paradigms**: Replace `map` and `filter` occurrences with equivalent comprehensions.
3. **Evaluate Comprehension Complexity**: Count the control subexpressions in comprehensions. If > 2, extract the logic into a standalone generator function.
4. **Optimize Comprehensions**: Identify repeated function calls or calculations inside comprehensions. Move the calculation into an assignment expression (`:=`) in the `if` clause.
5. **Memory Profiling Check**: Assess the expected size of sequence outputs. If potentially large, convert list accumulations (`append`) to `yield` generators, and list comprehensions to generator expressions.
6. **Defend Iterators**: Scan function arguments that are iterated over `>1` times. Add an `iter(x) is x` check that raises `TypeError` for plain iterators.
7. **Compose Generators**: Scan for `for` loops that merely `yield` items from another generator. Replace them immediately with `yield from`.
8. **Audit Generator State Manipulation**: Remove usages of `.send()` (replace with passed iterators) and `.throw()` (replace with iterable classes).
9. **Apply Itertools**: Review manual nested loops for combinatorial outputs or specialized filtering, and replace them with the appropriate `itertools` function.

@Examples (Do's and Don'ts)

**Principle: Use Comprehensions Instead of map and filter**
- [DO]
  ```python
  even_squares = [x**2 for x in a if x % 2 == 0]
  even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
  ```
- [DON'T]
  ```python
  even_squares = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
  even_squares_dict = dict(map(lambda x: (x, x**2), filter(lambda x: x % 2 == 0, a)))
  ```

**Principle: Avoid More Than Two Control Subexpressions in Comprehensions**
- [DO]
  ```python
  flat = [x for row in matrix for x in row]
  squared = [[x**2 for x in row] for row in matrix]
  ```
- [DON'T]
  ```python
  # Too many subexpressions, extremely difficult to read
  filtered = [[x for x in row if x % 3 == 0] for row in matrix if sum(row) >= 10]
  flat = [x for sublist1 in my_lists for sublist2 in sublist1 for x in sublist2]
  ```

**Principle: Avoid Repeated Work in Comprehensions by Using Assignment Expressions**
- [DO]
  ```python
  found = {name: batches for name in order
           if (batches := get_batches(stock.get(name, 0), 8))}
  ```
- [DON'T]
  ```python
  # Redundant calls to stock.get and get_batches
  found = {name: get_batches(stock.get(name, 0), 8) for name in order
           if get_batches(stock.get(name, 0), 8)}

  # Leaks loop variable into the containing scope
  half = [(last := count // 2) for count in stock.values()]
  ```

**Principle: Consider Generators Instead of Returning Lists**
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

**Principle: Be Defensive When Iterating Over Arguments**
- [DO]
  ```python
  def normalize_defensive(numbers):
      if iter(numbers) is numbers:
          raise TypeError('Must supply a container')
      total = sum(numbers)
      result = []
      for value in numbers:
          percent = 100 * value / total
          result.append(percent)
      return result
      
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
  # Iterating multiple times without checking if `numbers` is a stateful iterator
  def normalize(numbers):
      total = sum(numbers)
      result = []
      for value in numbers:
          percent = 100 * value / total
          result.append(percent)
      return result
  ```

**Principle: Consider Generator Expressions for Large List Comprehensions**
- [DO]
  ```python
  it = (len(x) for x in open('my_file.txt'))
  roots = ((x, x**0.5) for x in it)
  ```
- [DON'T]
  ```python
  # Materializes entire output in memory, leading to crashes for large files
  value = [len(x) for x in open('my_file.txt')]
  ```

**Principle: Compose Multiple Generators with yield from**
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

**Principle: Avoid Injecting Data into Generators with send**
- [DO]
  ```python
  # Pass an iterator explicitly to the generator to pull inputs
  def wave_cascading(amplitude_it, steps):
      step_size = 2 * math.pi / steps
      for step in range(steps):
          radians = step * step_size
          fraction = math.sin(radians)
          amplitude = next(amplitude_it)
          yield amplitude * fraction
  ```
- [DON'T]
  ```python
  # Using yield on the right side of assignment and requiring .send()
  def wave_modulating(steps):
      step_size = 2 * math.pi / steps
      amplitude = yield
      for step in range(steps):
          radians = step * step_size
          fraction = math.sin(radians)
          amplitude = yield amplitude * fraction
  ```

**Principle: Avoid Causing State Transitions in Generators with throw**
- [DO]
  ```python
  class Timer:
      def __init__(self, period):
          self.current = period
          self.period = period
      def reset(self):
          self.current = self.period
      def __iter__(self):
          while self.current:
              self.current -= 1
              yield self.current
  ```
- [DON'T]
  ```python
  def timer(period):
      current = period
      while current:
          current -= 1
          try:
              yield current
          except Reset:
              current = period
  # Later calling it.throw(Reset())
  ```