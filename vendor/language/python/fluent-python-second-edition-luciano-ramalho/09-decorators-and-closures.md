# @Domain
Python development tasks involving metaprogramming, functional enhancements, state preservation across function invocations, caching/memoization, dynamic function dispatching, and custom function routing or registration. These rules trigger whenever the AI creates, modifies, or reviews function decorators, closures, scope-specific variable assignments, or utilizes the `functools` library (specifically `wraps`, `cache`, `lru_cache`, and `singledispatch`).

# @Vocabulary
- **Decorator**: A callable that takes another function as an argument, performs some processing, and returns it or replaces it with another callable object. Conceptually, `@decorate def target(): pass` is identical to `target = decorate(target)`.
- **Import Time vs. Runtime**: Decorators are executed at *import time* (as soon as the module is loaded), whereas the decorated functions themselves run at *runtime* (when explicitly invoked).
- **Registration Decorator**: A decorator that adds a function to a central registry but returns the decorated function unchanged.
- **Closure**: A function with an extended scope that encompasses non-global variables referenced in its body that are defined in an encompassing outer function.
- **Free Variable**: A variable referenced within a function that is neither a global variable nor a local variable defined within that function. Its binding is kept in the `__closure__` attribute.
- **Local Variable Shadowing**: Python's design choice where assigning to a variable within a function body automatically makes it local, potentially shadowing a global or free variable unless explicitly declared.
- **`nonlocal`**: A keyword introduced in Python 3 that allows a nested function to rebind (assign a new value to) a free variable from a surrounding scope.
- **`functools.wraps`**: A standard library decorator used inside decorators to copy relevant metadata attributes (`__name__`, `__doc__`, etc.) from the original function to the new wrapped function.
- **Memoization**: An optimization technique implemented by `@functools.cache` and `@functools.lru_cache` that saves the results of previous function invocations to avoid repeating expensive computations.
- **Single Dispatch**: A generic function mechanism (via `@functools.singledispatch`) that executes different logic based on the type of the *first* argument, replacing long `if/elif/elif` type-checking chains.
- **Decorator Factory (Parameterized Decorator)**: A function or class that accepts arguments and returns the actual decorator, which is then applied to the target function.
- **Stacked Decorators**: Multiple decorators applied to a single function. Evaluated from bottom to top (e.g., `@alpha \n @beta \n def fn():` evaluates as `fn = alpha(beta(fn))`).

# @Objectives
- Ensure all custom decorators are "well-behaved" by preserving the original function's identity and metadata.
- Prevent scope-related bugs (`UnboundLocalError`) by enforcing explicit variable scope declarations when modifying outer-scope variables.
- Optimize application performance safely using appropriate caching mechanisms, avoiding memory leaks in long-running processes.
- Achieve clean, extensible polymorphism using generic dispatching instead of monolithic `isinstance` conditional chains.
- Architect complex parameterized decorators using object-oriented principles (classes) when functional nesting becomes deeply unreadable.

# @Guidelines
- **Decorator Application**: When analyzing or writing decorators, the AI MUST conceptually treat `@decorator` as `func = decorator(func)`. 
- **Import-time Execution**: The AI MUST place setup, registration, or routing logic directly inside the decorator's outer body if it needs to execute exactly once when the module loads.
- **Metadata Preservation**: The AI MUST apply `@functools.wraps(func)` to the inner wrapper function whenever writing a decorator that replaces the target function.
- **Closure State Mutation**: If an inner function assigns a new value to a free variable of an immutable type (int, str, tuple), the AI MUST declare that variable using the `nonlocal` keyword to prevent accidental local shadowing and `UnboundLocalError`.
- **Mutable Defaults in Closures**: The AI MAY omit `nonlocal` if the free variable is a mutable collection (e.g., `list`, `dict`) and the inner function only mutates the collection's contents (e.g., `my_list.append()`) without rebinding the variable name.
- **Caching Strategy - Short-lived Scripts**: The AI MAY use `@functools.cache` for short-lived command-line scripts where unbounded memory consumption is not a risk.
- **Caching Strategy - Long-running Applications**: The AI MUST prefer `@functools.lru_cache` over `@cache` for long-running processes (like web servers) to bound memory usage. The `maxsize` parameter SHOULD be set to a power of 2 for optimal performance.
- **Caching Constraints**: The AI MUST ensure that all arguments passed to a function decorated with memoization (`@cache` or `@lru_cache`) are hashable.
- **Polymorphism over Type Checking**: The AI MUST NOT write functions with long `if/elif` chains using `isinstance()` checks. Instead, the AI MUST use `@functools.singledispatch` to create a generic base function and register specialized implementations.
- **Goose Typing in Dispatch**: When registering types with `@singledispatch`, the AI MUST favor Abstract Base Classes (ABCs) from `collections.abc` or `numbers` (e.g., `abc.MutableSequence`, `numbers.Integral`) over concrete classes (e.g., `list`, `int`) to support a broader variety of compatible types.
- **Stacked Decorators Logic**: When writing stacked decorators, the AI MUST sequence them based on the mathematical composition `f(g(x))`. 
- **Parameterized Decorators (Functional)**: When implementing a parameterized decorator functionally, the AI MUST nest three levels deep: the decorator factory, the decorator itself, and the inner wrapper function.
- **Parameterized Decorators (Class-based)**: For complex parameterized decorators, the AI SHOULD implement them as a class where `__init__` accepts the parameters and `__call__` accepts the function and defines the wrapper.

# @Workflow
When tasked with creating or modifying a decorator, closure, or dispatched function, the AI MUST follow this exact sequence:
1. **Determine the Paradigm**: Decide if the requirement needs a Registration Decorator (no wrapper), a Behavioral Decorator (needs wrapper), or a Parameterized Decorator (needs factory).
2. **Scope Analysis**: Identify all variables accessed inside the inner function. If any variable from the outer scope is reassigned (using `=`, `+=`, etc.), explicitly add a `nonlocal` declaration for it.
3. **Wrapper Implementation**: Define the inner function (e.g., `def clocked(*args, **kwargs):`), ensuring it accepts generic arguments unless strictly typed.
4. **Metadata Preservation**: Immediately decorate the inner function with `@functools.wraps(func)`.
5. **Return Flow**: Ensure the inner function returns the result of the original function, the decorator returns the inner function, and the factory (if used) returns the decorator.
6. **Dispatch Refactoring**: If tasked with refactoring type-checking logic, define a base function throwing `NotImplementedError` or providing fallback logic, decorate it with `@singledispatch`, and create `_<type>` or `_` named functions decorated with `@<base_func>.register(<ABC_Type>)`.

# @Examples (Do's and Don'ts)

## Metadata Preservation
**[DO]**
```python
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # timing logic here
        return func(*args, **kwargs)
    return wrapper
```

**[DON'T]**
```python
def timer(func):
    def wrapper(*args, **kwargs):
        # timing logic here
        return func(*args, **kwargs)
    return wrapper # Loses __name__, __doc__, and original signature
```

## Modifying Closure State
**[DO]**
```python
def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager
```

**[DON'T]**
```python
def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        count += 1 # Raises UnboundLocalError: local variable referenced before assignment
        total += new_value
        return total / count
    return averager
```

## Function Dispatching
**[DO]**
```python
from functools import singledispatch
from collections import abc
import numbers

@singledispatch
def format_data(obj: object) -> str:
    return str(obj)

@format_data.register
def _(text: str) -> str:
    return text.upper()

@format_data.register
def _(seq: abc.Sequence) -> str:
    return " -> ".join(format_data(item) for item in seq)

@format_data.register
def _(n: numbers.Integral) -> str:
    return hex(n)
```

**[DON'T]**
```python
def format_data(obj):
    if isinstance(obj, str):
        return obj.upper()
    elif isinstance(obj, list) or isinstance(obj, tuple): # Highly coupled to concrete types
        return " -> ".join(format_data(item) for item in obj)
    elif isinstance(obj, int):
        return hex(obj)
    else:
        return str(obj)
```

## Parameterized Decorators
**[DO]**
```python
# Class-based approach for parameterized decorators is highly readable
import functools

class clock:
    def __init__(self, fmt='[{elapsed:0.8f}s] {name}'):
        self.fmt = fmt
        
    def __call__(self, func):
        @functools.wraps(func)
        def clocked(*args, **kwargs):
            # execution and formatting logic here using self.fmt
            return func(*args, **kwargs)
        return clocked

@clock(fmt="time taken: {elapsed}s")
def compute():
    pass
```

**[DON'T]**
```python
# Deeply nested functions without wraps that are hard to debug
def clock(fmt='[{elapsed:0.8f}s] {name}'):
    def decorate(func):
        def clocked(*args, **kwargs):
            # logic here
            return func(*args, **kwargs)
        return clocked
    return decorate
```

## Caching Application Data
**[DO]**
```python
from functools import lru_cache

# Bounded memory, safe for long-running processes. Power of 2 maxsize.
@lru_cache(maxsize=512)
def fetch_user_profile(user_id):
    pass
```

**[DON'T]**
```python
from functools import cache

# Unbounded memory, will eventually cause Out Of Memory (OOM) in long-running services
@cache
def fetch_user_profile(user_id):
    pass
```