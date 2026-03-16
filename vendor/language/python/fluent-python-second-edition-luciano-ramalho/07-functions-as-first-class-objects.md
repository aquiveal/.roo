# @Domain
These rules MUST be triggered when the AI is writing, refactoring, or reviewing Python code that involves functions, callbacks, higher-order functions, sorting/filtering iterables, parameter signature definitions (positional-only, keyword-only), callables, stateful functions, or functional programming paradigms utilizing the `operator` or `functools` modules.

# @Vocabulary
- **First-class object**: A program entity that can be created at runtime, assigned to a variable or data structure element, passed as an argument to a function, and returned as the result of a function. In Python, all functions are first-class objects.
- **Higher-order function**: A function that takes a function as an argument or returns a function as a result (e.g., `map`, `filter`, `reduce`, `sorted`).
- **Callable**: Any object that can be invoked using the call operator `()`. Python has nine flavors of callables, ranging from user-defined functions and built-in methods to classes and instances implementing `__call__`.
- **Anonymous function**: A function created with the `lambda` keyword. It is restricted to a single pure expression and cannot contain Python statements (like `while`, `try`, or `=`).
- **Positional-only parameters**: Function parameters defined before a `/` symbol in the signature, restricting them from being passed via keyword arguments (available in Python 3.8+).
- **Keyword-only parameters**: Function parameters defined after a `*` or `*args` in the signature, forcing them to be passed exclusively by keyword.
- **Call by sharing**: Python's parameter-passing model where formal parameters get a copy of the reference to the actual arguments, meaning mutable objects can be changed within a function but object identity cannot be replaced.
- **Reducing function**: A function that applies an operation to successive items in a series, accumulating previous results to reduce the series to a single value (e.g., `sum`, `all`, `any`, `functools.reduce`).
- **Closure**: A function with an extended scope that encompasses non-global variables defined outside of its body, used to maintain internal state.

# @Objectives
- Treat functions strictly as first-class objects (data) to create highly readable, functional-style Python code.
- Modernize functional code by replacing legacy functions (`map`, `filter`, `reduce`) with list comprehensions, generator expressions, and specialized built-ins.
- Utilize standard library functional packages (`operator`, `functools`) to eliminate trivial, boilerplate functions and lambdas.
- Ensure strict and explicit function signatures using Python's advanced parameter handling (positional-only and keyword-only markers).
- Create stateful callables properly by implementing the `__call__` method on classes when simple functions or closures become insufficient.

# @Guidelines
- **Modernizing Higher-Order Functions**:
  - Do NOT use `map()` and `filter()`. You MUST replace them with list comprehensions or generator expressions for better readability and performance.
  - Do NOT use `functools.reduce()` for simple summation or boolean reductions. You MUST use the built-in `sum()`, `all()`, or `any()` functions.
- **Lambda Functions**:
  - Limit the use of `lambda` to simple, single-expression arguments for higher-order functions.
  - NEVER use the assignment operator (`=`) or other statements inside a `lambda`. (The walrus operator `:=` is syntactically allowed but strictly forbidden here if it harms readability).
  - If a `lambda` is difficult to read, you MUST apply Fredrik Lundh's refactoring recipe:
    1. Write a comment explaining what the lambda does.
    2. Think of a name that captures the essence of the comment.
    3. Convert the lambda to a `def` statement using that name.
    4. Remove the comment.
- **Callable Objects**:
  - Do not assume `function` is the only callable type. Use the built-in `callable(obj)` to safely determine if an object is callable.
  - When an object needs to behave like a function while retaining internal state across invocations (e.g., memoization caches or complex decorators), MUST implement the `__call__` instance method on a class.
- **Function Parameter Architecture**:
  - Use the `/` marker in function signatures to denote positional-only arguments when parameter names are arbitrary or have no meaningful external context (requires Python 3.8+).
  - Use the `*` marker (or `*args`) to strictly enforce keyword-only parameters for configuration options, flags, or attributes that require explicit naming for readability.
- **The `operator` and `functools` Modules**:
  - Do NOT write trivial functions or lambdas for basic operations (e.g., `lambda a, b: a * b`). You MUST use functions from the `operator` module (e.g., `operator.mul`, `operator.add`).
  - Do NOT write lambdas to extract items or attributes (e.g., `lambda x: x[1]` or `lambda x: x.name`). You MUST use `operator.itemgetter` and `operator.attrgetter`. Use multiple arguments in these getters if extracting a tuple of values.
  - Use `operator.methodcaller` to create functions that invoke a method by name on the object given as an argument, additionally freezing any arguments required by that method.
  - Use `functools.partial` (or `partialmethod`) to freeze specific arguments of a callable, adapting a complex function to an API that requires a callback with fewer arguments.

# @Workflow
1. **Analyze Callable Requirements**: Determine if the task needs a plain function (`def`), a one-off pure expression (`lambda`), or a stateful callable object (Class with `__call__`).
2. **Define the Signature**:
   - Place positional-only arguments first, followed by `/`.
   - Place standard arguments next.
   - Place `*` or `*args` to consume arbitrary positional data.
   - Place keyword-only arguments after the `*`.
   - Place `**kwargs` last.
3. **Evaluate Iteration & Reduction**:
   - If transforming an iterable, write a list comprehension or generator expression instead of `map()`/`filter()`.
   - If aggregating an iterable, use `sum()`, `all()`, `any()`, or specialized math functions before resorting to `functools.reduce()`.
4. **Refactor Lambdas & Helpers**:
   - Check all `lambda` functions. If they merely call a method, access an attribute, or perform basic math, replace them with `operator.methodcaller`, `operator.attrgetter`, `operator.itemgetter`, or standard `operator` math functions.
   - If adapting a function for a callback, wrap it in `functools.partial` instead of writing a new lambda/def.
5. **Enforce Readability**: Apply Fredrik Lundh's recipe to any remaining lambdas that are complex or difficult to read.

# @Examples (Do's and Don'ts)

**[DO] Use list comprehensions or generator expressions instead of map/filter**
```python
# List comprehension
fact_list = [factorial(n) for n in range(6) if n % 2]

# Generator expression
fact_gen = (factorial(n) for n in range(6) if n % 2)
```

**[DON'T] Use map and filter**
```python
# Hard to read and obsolete
fact_list = list(map(factorial, filter(lambda n: n % 2, range(6))))
```

**[DO] Use `operator.itemgetter` and `operator.attrgetter` for sorting/extraction**
```python
from operator import itemgetter, attrgetter

metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
]

# Sort by country code (index 1)
sorted_cities = sorted(metro_data, key=itemgetter(1))

# Extract multiple attributes
name_lat = attrgetter('name', 'coord.lat')
```

**[DON'T] Write trivial lambdas for extraction**
```python
sorted_cities = sorted(metro_data, key=lambda x: x[1])
```

**[DO] Implement `__call__` for stateful function-like objects**
```python
import random

class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()

bingo = BingoCage(range(3))
result = bingo() # Acts like a function
```

**[DON'T] Rely on global variables or hacky dynamic scopes for simple stateful callables**
```python
_items = []
def pick_item():
    global _items
    return _items.pop()
```

**[DO] Strictly separate positional-only and keyword-only parameters**
```python
# `name` is positional only. `class_` is keyword only.
def tag(name, /, *content, class_=None, **attrs):
    pass

tag('p', 'hello', class_='sidebar')
```

**[DON'T] Mix parameters ambiguously if they represent different API contracts**
```python
# `name` can be passed as a keyword accidentally, tying the variable name to the API.
def tag(name, *content, class_=None, **attrs):
    pass
```

**[DO] Use `functools.partial` to adapt function signatures**
```python
import unicodedata
from functools import partial

# Freeze the first argument of normalize
nfc = partial(unicodedata.normalize, 'NFC')
s1 = nfc('cafe\u0301')
```

**[DON'T] Write verbose wrapper functions for simple adaptations**
```python
import unicodedata

def nfc(text):
    return unicodedata.normalize('NFC', text)
s1 = nfc('cafe\u0301')
```