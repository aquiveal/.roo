# @Domain
These rules trigger whenever the AI is tasked with writing, refactoring, reviewing, or analyzing Python functions, function signatures, return values, decorators, and closures.

# @Vocabulary
* **Unpacking**: The Python syntax allowing multiple returned values from a function to be assigned to distinct variables in a single statement.
* **Closure**: A function defined within another function that can reference and interact with variables from its enclosing scopes.
* **Scoping Bug**: A common Python bug where assigning a value to a variable inside a closure creates a new local variable instead of modifying the target variable in the enclosing scope.
* **nonlocal**: A Python keyword used inside closures to explicitly declare that an assignment should modify a variable in the enclosing scope.
* **Variable Positional Arguments (*args)**: A parameter that collects a variable number of positional arguments into a tuple, reducing visual noise in function calls.
* **Keyword Arguments (**kwargs)**: Arguments passed by name, which clarify caller intent and enable extending functions with default behaviors backward-compatibly.
* **Dynamic Default Arguments**: Default values that need to be evaluated at runtime (e.g., `[]`, `{}`, or `datetime.now()`) rather than strictly at module load time.
* **Keyword-Only Arguments**: Parameters specified after a `*` in the function signature, requiring the caller to pass them strictly by name.
* **Positional-Only Arguments**: Parameters specified before a `/` (in Python 3.8+) in the function signature, prohibiting the caller from passing them by name.
* **Decorator**: A function that wraps another function to modify its behavior, arguments, or return values at runtime.
* **functools.wraps**: A standard library helper decorator that copies metadata (like `__name__` and `__doc__`) from a wrapped function to the wrapper function.

# @Objectives
* Maximize the readability, maintainability, and clarity of Python function signatures and calls.
* Prevent subtle, common Python bugs related to mutable default arguments, closure scoping, and returning `False`-equivalent values like `None`.
* Future-proof APIs by enforcing strict caller behaviors using keyword-only and positional-only arguments.
* Ensure that introspection, debugging, and serialization tools work seamlessly with decorated functions.

# @Guidelines
* **Return Value Unpacking**: The AI MUST NEVER unpack more than three variables from a function's return statement. If a function returns four or more values, the AI MUST package them into a lightweight class or `collections.namedtuple`.
* **Error Signaling**: The AI MUST NEVER return `None` to indicate a special case, failure, or error. `None` evaluates to `False` in conditionals and causes subtle bugs. The AI MUST raise a specific, documented Exception instead.
* **Closure State**: When a closure needs to modify state in an enclosing scope, the AI MUST use the `nonlocal` statement. 
* **Complex Closures**: If the state management within a closure becomes complex, the AI MUST NOT use `nonlocal`. Instead, the AI MUST refactor the closure into a helper class that implements the `__call__` special method.
* **Variable Positional Arguments (*args)**: The AI MUST use `*args` to accept a variable number of inputs to reduce visual noise. However, the AI MUST NOT pass generators to `*args` if the sequence could be large, as `*args` forces the generator into a memory-consuming tuple.
* **Extending *args**: The AI MUST NOT add new positional arguments to a function signature before an existing `*args` parameter, as it will subtly break existing callers.
* **Optional Behaviors**: The AI MUST use keyword arguments for optional behaviors. The AI MUST instruct callers to pass optional arguments by keyword, not by position.
* **Dynamic Default Arguments**: The AI MUST NEVER use mutable objects (e.g., `[]`, `{}`) or dynamic function calls (e.g., `datetime.now()`) as default argument values in a function signature. 
* **Dynamic Default Implementation**: To implement dynamic defaults, the AI MUST set the default argument to `None`, initialize the dynamic value inside the function body (`if arg is None: arg = []`), and document this behavior in the docstring.
* **Keyword-Only Arguments**: The AI MUST use keyword-only arguments (defined after a `*` in the signature) to force callers to explicitly name parameters. This MUST be applied to boolean flags and complex optional behaviors.
* **Positional-Only Arguments**: The AI MUST use positional-only arguments (defined before a `/` in the signature) when parameter names are arbitrary, not part of the public API, and subject to change, ensuring callers cannot rely on the parameter names.
* **Decorators**: The AI MUST ALWAYS apply `@functools.wraps(func)` to the internal wrapper function when defining a custom decorator.

# @Workflow
1. **Signature Design**: Draft the function signature. Count the expected return values. If `> 3`, immediately define a `namedtuple` for the return type.
2. **Error Handling Check**: Identify all failure paths in the function. Remove any `return None` statements used for errors. Replace them with `raise ValueError(...)` or domain-specific exceptions.
3. **Default Arguments Scan**: Review the function parameters. If any default is a list, dict, set, or dynamic function, change the default in the signature to `None`. Add an `if param is None:` block at the top of the function to instantiate the default.
4. **Argument Categorization**: Structure the parameters. Place parameters that should be decoupled from their names before a `/`. Place a `*` before any parameters that control distinct behaviors or boolean flags to force keyword-only usage.
5. **State & Closures**: If defining a nested function (closure) that mutates external variables, inject the `nonlocal` keyword. If the closure spans many lines or manages multiple variables, abort the closure and generate a class with a `__call__` method.
6. **Decorator Construction**: If building a decorator, import `functools`. Immediately decorate the inner `wrapper` function with `@wraps(func)`.
7. **Documentation**: Write a PEP 257 compliant docstring. Document all parameters, raised exceptions, and explicitly state what a `None` argument resolves to if dynamic defaults are used.

# @Examples (Do's and Don'ts)

### Item 19: Return Value Unpacking
**[DON'T]** Unpack more than 3 values.
```python
def get_stats(numbers):
    # ...
    return minimum, maximum, average, median, count

# Anti-pattern: Too many variables, prone to ordering errors
minimum, maximum, average, median, count = get_stats(lengths)
```

**[DO]** Use a `namedtuple` for 4 or more return values.
```python
from collections import namedtuple

Stats = namedtuple('Stats', ['minimum', 'maximum', 'average', 'median', 'count'])

def get_stats(numbers):
    # ...
    return Stats(minimum, maximum, average, median, count)

stats = get_stats(lengths)
print(stats.average)
```

### Item 20: Raising Exceptions vs Returning None
**[DON'T]** Return `None` to indicate an error.
```python
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

result = careful_divide(x, y)
if not result:  # Anti-pattern: 0 also evaluates to False!
    print('Invalid inputs')
```

**[DO]** Raise exceptions.
```python
def careful_divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

try:
    result = careful_divide(x, y)
except ValueError:
    print('Invalid inputs')
```

### Item 21: Closures and Variable Scope
**[DON'T]** Rely on local scoping when modifying enclosing variables.
```python
def sort_priority(values, group):
    found = False
    def helper(x):
        if x in group:
            found = True  # Anti-pattern: Scoping bug. Modifies a local 'found', not the enclosing one.
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found
```

**[DO]** Use `nonlocal` for simple state, or a `__call__` class for complex state.
```python
# Simple State
def sort_priority(values, group):
    found = False
    def helper(x):
        nonlocal found  # Correct
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found

# Complex State
class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
values.sort(key=sorter)
```

### Item 24: Dynamic Default Arguments
**[DON'T]** Use mutable or dynamic default values in signatures.
```python
import datetime

# Anti-pattern: datetime.now() is evaluated exactly once at module load
def log(message, when=datetime.datetime.now()):
    print(f'{when}: {message}')

# Anti-pattern: The same dictionary is shared across all function calls
def decode(data, default={}):
    pass
```

**[DO]** Use `None` and evaluate inside the function.
```python
import datetime

def log(message, when=None):
    """
    Args:
        when: datetime of when the message occurred. Defaults to the present time.
    """
    if when is None:
        when = datetime.datetime.now()
    print(f'{when}: {message}')
```

### Item 25: Keyword-Only and Positional-Only Arguments
**[DON'T]** Leave ambiguous parameters as standard positional/keyword arguments.
```python
def safe_division(numerator, denominator, ignore_overflow, ignore_zero_division):
    pass

# Anti-pattern: Hard to read, easy to mix up the booleans
safe_division(1.0, 10**500, True, False)
```

**[DO]** Use `/` and `*` to strictly define the API boundaries.
```python
def safe_division(numerator, denominator, /, *, ignore_overflow=False, ignore_zero_division=False):
    pass

# Caller is forced to use keywords for the flags, and forced to use position for the math
safe_division(1.0, 0, ignore_zero_division=True)
```

### Item 26: Defining Function Decorators
**[DON'T]** Define a wrapper without transferring metadata.
```python
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__} returned {result}')
        return result
    return wrapper # Anti-pattern: Hides __name__ and __doc__ of 'func'
```

**[DO]** Use `@functools.wraps`.
```python
from functools import wraps

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__} returned {result}')
        return result
    return wrapper
```