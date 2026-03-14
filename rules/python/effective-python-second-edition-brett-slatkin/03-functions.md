# @Domain
These rules MUST be triggered whenever the AI is tasked with generating, refactoring, or reviewing Python code that involves function definitions, function calls, return values, argument parsing, closures, decorators, or API interface design.

# @Vocabulary
- **Unpacking**: The Python syntax for assigning multiple values from an iterable in a single statement.
- **Closure**: A function that refers to variables from the scope in which it was defined.
- **Scoping Bug**: A common Python error where assigning to a variable inside a closure creates a new local variable instead of modifying the variable in the enclosing scope.
- **Varargs / Star Args**: A variable number of positional arguments, typically denoted as `*args`.
- **Keyword-Only Arguments**: Arguments that can only be supplied by keyword and never by position. Defined after a single `*` in the argument list.
- **Positional-Only Arguments**: Arguments that can only be supplied by position and never by keyword. Defined before a single `/` in the argument list.
- **Decorator**: Special syntax (`@`) allowing one function to wrap and modify another function at runtime.
- **Checked Exceptions**: A concept from other languages (like Java) not present in Python. Python relies on docstrings to indicate exceptional behavior.

# @Objectives
- Maximize the clarity, readability, and explicit intent of Python function interfaces.
- Eliminate subtle runtime bugs caused by mutable defaults, closure scope issues, and tuple unpacking reordering.
- Ensure robust error handling by avoiding ambiguous return types (e.g., `None`).
- Create forward-compatible function signatures that can be safely extended without breaking existing downstream callers.

# @Guidelines

### 1. Multiple Return Values and Unpacking
- When a function returns multiple values, the AI MUST NOT allow unpacking into more than three variables. 
- If four or more return values are required, the AI MUST define a lightweight class or `collections.namedtuple` and return an instance of that instead.

### 2. Error Handling over `None`
- The AI MUST NOT return `None` to indicate a special meaning, failure, or undefined state (e.g., division by zero), because `None` and other values (like `0` or `""`) evaluate to `False` in conditionals, leading to bugs.
- Instead, the AI MUST raise an explicit `Exception` (e.g., `ValueError`) and expect the caller to handle it.
- The AI MUST use type annotations to indicate that the function never returns `None` for these cases, and MUST document the exception-raising behavior in the docstring.

### 3. Closures and Variable Scope
- When a closure needs to modify a variable in its enclosing scope, the AI MUST use the `nonlocal` statement.
- The AI MUST NOT use `nonlocal` for complex functions or when the variable and the `nonlocal` declaration are far apart.
- If state management within a closure becomes complex, the AI MUST replace the closure with a helper class that encapsulates the state and implements the `__call__` special method.

### 4. Variable Positional Arguments (`*args`)
- The AI MUST use `*args` to reduce visual noise for functions that accept a variable, but reasonably small, number of inputs.
- The AI MUST NOT use the `*` operator to pass generators directly into `*args` functions unless it is guaranteed the generator is small, as this will exhaust the generator, convert it to a tuple, and potentially crash the program out of memory.
- When extending an existing function that accepts `*args`, the AI MUST add new parameters as keyword-only arguments to avoid breaking existing callers.

### 5. Optional Behavior and Keyword Arguments
- The AI MUST use keyword arguments to provide optional behavior and default values.
- When calling functions, the AI MUST pass optional keyword arguments by keyword, not by position, to clarify intent.

### 6. Dynamic Default Arguments
- The AI MUST NEVER use mutable or dynamic values (e.g., `{}`, `[]`, or `datetime.now()`) as default argument values in a function signature, because they are evaluated only once at module load time.
- The AI MUST use `None` as the default value for dynamic/mutable keyword arguments.
- The AI MUST implement the dynamic assignment inside the function body (`if arg is None: arg = []`) and MUST document the actual default behavior in the docstring.

### 7. Keyword-Only and Positional-Only Arguments
- The AI MUST use keyword-only arguments (placing a `*` in the parameter list) to force callers to explicitly name parameters. This is strictly required for boolean flags or complex functions where positional confusion could cause bugs.
- The AI MUST use positional-only arguments (placing a `/` in the parameter list) to ensure callers cannot couple to parameter names that have no semantic meaning or might change in the future.

### 8. Function Decorators
- When defining a function decorator, the AI MUST ALWAYS use the `@functools.wraps` decorator on the inner wrapper function.
- Failure to use `@wraps` hides the wrapped function's metadata (`__name__`, `__module__`, `__doc__`), which breaks introspection tools, debuggers, and object serializers (`pickle`).

# @Workflow
When tasked with writing or refactoring a Python function, the AI MUST follow this strict algorithm:
1. **Signature Design**: 
   - Determine required parameters. If the parameter name holds no external semantic value, make it positional-only (`/`).
   - Determine optional parameters. Add them as keyword-only (`*`) to prevent positional mix-ups.
   - If any default values are mutable or dynamic, set their default in the signature to `None`.
2. **Body Implementation**:
   - Handle `None` defaults by instantiating the dynamic/mutable value at the top of the function.
   - If the function delegates to closures, evaluate if `nonlocal` is sufficient or if a `__call__` helper class is required.
3. **Return and Error Handling**:
   - If the function can fail, raise an Exception. Do not return `None`.
   - If the function returns multiple values, count them. If `> 3`, define and return a `namedtuple` or custom class instead.
4. **Documentation and Types**:
   - Add type hints.
   - Write a docstring explaining arguments, return values, default behaviors for `None` inputs, and precisely which exceptions are raised.

# @Examples (Do's and Don'ts)

### 1. Unpacking Multiple Variables
- **[DON'T]** Unpack more than three variables from a function return.
```python
def get_stats(numbers):
    # ... logic ...
    return minimum, maximum, average, median, count

# Anti-pattern: High risk of reordering bugs (e.g., swapping average and median)
minimum, maximum, average, median, count = get_stats(lengths)
```
- **[DO]** Use a `namedtuple` for more than three return values.
```python
from collections import namedtuple

Stats = namedtuple('Stats', ('minimum', 'maximum', 'average', 'median', 'count'))

def get_stats(numbers):
    # ... logic ...
    return Stats(minimum, maximum, average, median, count)

stats = get_stats(lengths)
print(stats.average)
```

### 2. Exceptions vs. Returning None
- **[DON'T]** Return `None` to indicate an error or special state.
```python
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

result = careful_divide(x, y)
if not result: # Bug: Triggers on 0.0 as well as None!
    print('Invalid inputs')
```
- **[DO]** Raise an Exception and document it.
```python
def careful_divide(a: float, b: float) -> float:
    """Divides a by b.
    
    Raises:
        ValueError: When the inputs cannot be divided.
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e
```

### 3. Closures and Variable Scope
- **[DON'T]** Assign to an enclosing variable inside a closure without `nonlocal` (causes a scoping bug).
```python
def sort_priority(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True # Bug: creates a local variable 'found', does not modify the outer 'found'
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found
```
- **[DO]** Use `nonlocal` for simple state, or a `__call__` class for complex state.
```python
def sort_priority(numbers, group):
    found = False
    def helper(x):
        nonlocal found # Correctly references enclosing scope
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

# OR for complex state:
class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)
```

### 4. Dynamic Default Arguments
- **[DON'T]** Use mutable or dynamic values in the function signature.
```python
# Bug: datetime.now() is evaluated once at module load, not on every call
def log(message, when=datetime.now()): 
    print(f'{when}: {message}')

# Bug: The dictionary is shared across all function calls
def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default
```
- **[DO]** Use `None` and document the default behavior.
```python
def decode(data, default=None):
    """Load JSON data from a string.
    
    Args:
        data: JSON data to decode.
        default: Value to return if decoding fails.
                 Defaults to an empty dictionary.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default
```

### 5. Keyword-Only and Positional-Only Arguments
- **[DON'T]** Leave parameters ambiguous so callers can mix up positions.
```python
def safe_division(numerator, denominator, ignore_overflow, ignore_zero_division):
    pass

# Anti-pattern: Hard to remember what True/False correspond to
safe_division(1.0, 10**500, True, False)
```
- **[DO]** Use `/` and `*` to enforce clarity and decouple names.
```python
def safe_division(numerator, denominator, /, *, ignore_overflow=False, ignore_zero_division=False):
    pass

# Enforces positional for math inputs, and keyword for behavioral flags
safe_division(1.0, 0, ignore_zero_division=True)
```

### 6. Function Decorators
- **[DON'T]** Write a decorator without `functools.wraps`.
```python
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__} returned {result}')
        return result
    return wrapper # Bug: Hides original func's name and docstring
```
- **[DO]** Always use `@wraps`.
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