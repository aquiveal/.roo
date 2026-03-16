# @Domain
These rules trigger when the AI is writing, refactoring, or reviewing Python code involving resource management (I/O, locks, transactions), complex conditional logic (tree traversal, AST parsing, structural matching), looping constructs with completion checks, or exception handling for control flow.

# @Vocabulary
- **Context Manager**: An object that controls a `with` statement, implementing the `__enter__` and `__exit__` protocols to guarantee safe setup and teardown.
- **EAFP (Easier to ask for forgiveness than permission)**: A common Python coding style that assumes the existence of valid keys/attributes and catches exceptions if the assumption proves false. Contrast with LBYL.
- **LBYL (Look before you leap)**: A coding style that explicitly tests for pre-conditions before making calls or lookups. Prone to race conditions.
- **Destructuring**: A form of unpacking used in `match/case` statements to extract elements from a matched sequence or mapping structure.
- **Guard**: An `if` clause appended to a `case` pattern that must evaluate to `True` for the pattern to match.
- **OR-pattern**: A sequence of patterns separated by the `|` operator in a `case` statement. Succeeds if any subpattern matches.
- **`__enter__`**: Protocol method called at the top of a `with` block. Its return value is bound to the `as` target variable.
- **`__exit__`**: Protocol method called when a `with` block completes or terminates. Takes `exc_type`, `exc_value`, and `traceback`.

# @Objectives
- Replace boilerplate `try/finally` setup and teardown code with `with` blocks and Context Managers.
- Build efficient, localized resource management APIs using `@contextmanager` instead of full classes where appropriate.
- Simplify complex conditional and structural parsing logic (e.g., DSLs, interpreters, data validation) using `match/case` pattern matching.
- Express code intent clearly and prevent race conditions by utilizing the EAFP principle with `try/except/else` blocks.
- Eliminate boolean flag variables used for loop completion tracking by utilizing `for/else` and `while/else` constructs.

# @Guidelines

## Context Managers and the `with` Statement
- The AI MUST use the `with` statement for operations requiring guaranteed teardown or state restoration (e.g., file handling, DB transactions, threading locks, temporary patching).
- When writing a Context Manager class, the AI MUST implement `__enter__` (to return the target object) and `__exit__` (to handle teardown).
- If `__exit__` successfully handles an exception, the AI MUST return `True`. If the exception should propagate, the AI MUST return `None` (or any falsy value).
- The AI MUST NOT assume that the object returned by `__enter__` is the context manager instance itself (e.g., it may return a different proxy or data object).
- For Python 3.10+ environments, the AI MUST group multiple context managers using the parenthesized syntax `with (Ctx1() as c1, Ctx2() as c2):` instead of nesting multiple `with` statements.

## Using `contextlib` Utilities
- The AI MUST prefer the `@contextmanager` decorator over creating full classes for simple context managers.
- When writing a `@contextmanager` generator, the AI MUST yield exactly once.
- **CRITICAL**: The AI MUST wrap the `yield` statement of a `@contextmanager` inside a `try/finally` block to ensure the teardown code executes even if an exception is raised inside the caller's `with` block.
- If the context manager needs to suppress or handle specific exceptions, the AI MUST use `try/except/finally` around the `yield` inside the `@contextmanager` generator.
- The AI MUST utilize `contextlib.suppress` to temporarily ignore specific exceptions instead of writing empty `try/except/pass` blocks.
- The AI MUST use `contextlib.nullcontext` when conditional logic dictates that a context manager might not be needed, but the structural flow demands a `with` block.
- The AI MUST use `contextlib.ExitStack` when the number of context managers to enter is dynamic or not known beforehand (e.g., opening an arbitrary list of files).

## Pattern Matching (`match/case`)
- The AI MUST use `match/case` for structural parsing (such as AST evaluators, command processors, or message routers) instead of long `if/elif` chains with manual index extraction.
- When destructuring sequences, the AI MUST use `[*rest]` or `*_` to capture varying lengths of arguments.
- The AI MUST use pattern guards (`case [x, y] if x == y:`) to enforce value constraints that cannot be expressed purely through structural layout.
- When using OR-patterns (`|`), the AI MUST ensure that all subpatterns bind the exact same variable names.
- The AI MUST always include a fallback wildcard `case _:` if the patterns are not strictly exhaustive, and should raise a descriptive exception (e.g., `SyntaxError`, `ValueError`) if an unmatched pattern represents an invalid state.

## `else` Blocks Beyond `if`
- **`try/except/else`**: The AI MUST place ONLY the code that is expected to throw the targeted exception inside the `try` block. Any code that should execute only upon the successful completion of the `try` block MUST be placed in the `else` block.
- **`for/else` and `while/else`**: The AI MUST use the `else` block to handle scenarios where a loop runs to natural exhaustion (i.e., not terminated by a `break`). The AI MUST NOT use temporary boolean flags (like `found = False`) to track if a loop was broken.

# @Workflow
When developing control flow or resource management structures, the AI MUST follow this evaluation sequence:
1. **Resource Scoping**: Determine if a resource requires cleanup, state restoration, or lock release. If yes, wrap it in a `with` statement.
2. **Context Manager Implementation**: If a custom context manager is needed, evaluate its complexity. If it strictly manages setup and teardown around a single action, use a generator decorated with `contextlib.@contextmanager` and wrap the `yield` in a `try/finally` block. If it requires extensive state management, implement a class with `__enter__` and `__exit__`.
3. **Dynamic Contexts**: If managing a variable number of resources, instantiate a `contextlib.ExitStack`.
4. **Structural Routing**: If processing inputs with varying shapes, types, or lengths (like an interpreter evaluating nodes), construct a `match/case` block. Prioritize specific structural patterns first, add `if` guards for value checks, and end with a `case _:` to handle syntax or routing errors.
5. **Exception-Driven Flow (EAFP)**: If validating keys, attributes, or access, execute the operation directly inside a `try` block. Catch the specific failure exception in an `except` block. Place the subsequent success-dependent logic strictly in an `else` block.
6. **Search Loops**: If iterating through a sequence to find an item, use `break` upon finding it. Place the "not found" logic inside the loop's `else` block.

# @Examples (Do's and Don'ts)

## Context Managers and `@contextmanager`

**[DO]** Wrap `@contextmanager` yields in `try/finally` for guaranteed teardown:
```python
import contextlib
import sys

@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write
    def reverse_write(text):
        original_write(text[::-1])
    sys.stdout.write = reverse_write
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        print('Please DO NOT divide by zero!')
    finally:
        sys.stdout.write = original_write
```

**[DON'T]** Leave `yield` exposed to unhandled exceptions preventing teardown:
```python
@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write
    sys.stdout.write = reverse_write
    
    yield 'JABBERWOCKY'  # If an exception occurs in the 'with' block, the next line never runs
    
    sys.stdout.write = original_write
```

## Pattern Matching (`match/case`)

**[DO]** Use destructuring, guards, and OR-patterns for clear routing:
```python
def evaluate(exp, env):
    match exp:
        case int(x) | float(x):
            return x
        case ['if', test, consequence, alternative]:
            if evaluate(test, env):
                return evaluate(consequence, env)
            else:
                return evaluate(alternative, env)
        case ['lambda', [*parms], *body] if body:
            return Procedure(parms, body, env)
        case [func_exp, *args] if func_exp not in KEYWORDS:
            proc = evaluate(func_exp, env)
            values = [evaluate(arg, env) for arg in args]
            return proc(*values)
        case _:
            raise SyntaxError(f"Invalid syntax: {exp}")
```

**[DON'T]** Use deep `if/elif` chains with manual index checking for structural data:
```python
def evaluate(exp, env):
    if isinstance(exp, (int, float)):
        return exp
    elif isinstance(exp, list) and len(exp) == 4 and exp[0] == 'if':
        if evaluate(exp[1], env):
            return evaluate(exp[2], env)
        else:
            return evaluate(exp[3], env)
    elif isinstance(exp, list) and len(exp) >= 3 and exp[0] == 'lambda':
        # Clunky and hard to read
        return Procedure(exp[1], exp[2:], env)
```

## EAFP and `try/except/else`

**[DO]** Isolate the exact failing operation in `try` and use `else` for success continuation:
```python
try:
    dangerous_call()
except OSError:
    log('OSError...')
else:
    after_call()
```

**[DON'T]** Place non-failing execution flow inside the `try` block, muddying error handling (LBYL / overly broad try):
```python
try:
    dangerous_call()
    after_call()  # If this raises OSError, it gets caught accidentally by the except block
except OSError:
    log('OSError...')
```

## Loop Completion (`for/else`)

**[DO]** Use `else` on a `for` loop to handle the "not found" state:
```python
for item in my_list:
    if item.flavor == 'banana':
        break
else:
    raise ValueError('No banana flavor found!')
```

**[DON'T]** Use flag variables to track loop exits:
```python
found = False
for item in my_list:
    if item.flavor == 'banana':
        found = True
        break

if not found:
    raise ValueError('No banana flavor found!')
```