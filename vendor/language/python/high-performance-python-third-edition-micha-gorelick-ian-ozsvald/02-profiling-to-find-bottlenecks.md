# @Domain
These rules MUST be triggered whenever the user requests performance optimization, execution speed measurement, memory footprint analysis, bottleneck identification, or profiling of Python code. They also apply when the user asks to "make the code faster", "reduce RAM usage", or compare the efficiency of two or more Python implementations.

# @Vocabulary
- **cProfile**: Python's built-in, C-based profiler used to measure execution time at the function level.
- **line_profiler / kernprof**: A third-party tool used to measure CPU execution time on a line-by-line basis for specific functions decorated with `@profile`.
- **memory_profiler / mprof**: A third-party tool used to measure RAM usage on a line-by-line basis, or to sample RAM usage over time (`mprof`).
- **Scalene**: A modern, low-overhead combined profiler that measures CPU, memory, and GPU usage, distinguishing between Python time, native C time, and system time.
- **PySpy**: A sampling profiler that introspects already-running Python processes without requiring code modifications.
- **VizTracer**: A profiling tool that generates an interactive, time-based visual call stack (flame chart) to observe execution timelines.
- **SnakeViz**: A browser-based visualizer for `cProfile` statistics files.
- **dis**: Python's built-in bytecode disassembler used to inspect the stack-based virtual machine instructions of a function.
- **Specialist**: A tool that uses color-coding to visualize CPython 3.11+ bytecode specialization (identifying "hot" code and adaptive instructions).
- **No-op Decorator**: A dummy `@profile` function injected into code during testing to prevent `NameError` exceptions when `line_profiler` or `memory_profiler` are not actively running.
- **Turbo Boost / SpeedStep**: Hardware CPU acceleration features that introduce random variation into execution times, skewing profiling results.

# @Objectives
- Base all optimization decisions on empirical profiling evidence, NEVER on gut instinct or intuition.
- Identify the exact bottleneck (CPU, RAM, or I/O) before modifying code logic.
- Do the least amount of work necessary to achieve the biggest practical performance gain.
- Ensure optimization does not break code correctness by heavily relying on unit tests and code coverage.
- Construct a stable benchmarking environment to prevent operating system or hardware noise from invalidating profiling results.

# @Guidelines
- **Hypothesis-Driven Profiling**: Before profiling, explicitly state a hypothesis about which part of the code is the bottleneck. Profile to prove or disprove the hypothesis.
- **Progressive Profiling**: Start with macro-profiling (`cProfile`, `/usr/bin/time -p`) to find the slowest functions. Only after identifying the slow functions, switch to micro-profiling (`line_profiler`, `memory_profiler`) to locate the exact slow lines.
- **Operator Short-Circuiting**: Order conditions in `if` and `while` statements so that the computationally cheapest checks evaluate first (e.g., check integer bounds before performing complex math), taking advantage of Python's left-to-right opportunistic evaluation.
- **Bytecode Awareness**: Use the `dis` module to compare implementations. Favor built-in functions (e.g., `sum()`) over manual Python `for` loops, as built-ins execute significantly fewer virtual machine bytecode instructions.
- **Test Integrity**: Never sacrifice code correctness for speed. Run `pytest` and `coverage.py` before and after optimization.
- **Decorator Safety**: When adding `@profile` decorators for `line_profiler` or `memory_profiler`, include a fallback "no-op" decorator block so that unit tests can run successfully without the profiling runner.
- **Tool Selection Strategy**:
  - Use `time.time()` decorators or `%timeit` (in Jupyter/IPython) for quick, coarse measurements of simple statements.
  - Use `cProfile` coupled with `SnakeViz` to get a high-level visual understanding of an unfamiliar codebase.
  - Use `Scalene` for an all-in-one view of CPU and memory, especially to identify if time is spent in native Python vs. C libraries.
  - Use `PySpy` to debug hanging, deadlocked, or long-running production processes where restarting or modifying code is impossible.
  - Use `memory_profiler` to track incremental memory allocations and memory leaks. Watch the `Mem usage` column, as allocations are relatively expensive operations.
- **Environmental Stability**: When executing profiles, instruct the user to disable Turbo Boost/SpeedStep in the BIOS, plug in AC power, and disable background sync tools (like Dropbox/backups) to reduce execution time variance.

# @Workflow
1. **Make it Work & Make it Right**: Ensure the target code is functional. Write unit tests to guarantee expected behavior. Run `coverage.py` to ensure the target code is actively tested.
2. **Formulate Hypothesis**: State what part of the system is suspected to be the bottleneck and why.
3. **Establish Baseline**: Run a coarse timing test (e.g., `/usr/bin/time` or a simple decorator) to record the baseline wall-clock and CPU time.
4. **Macro-Profile**: Execute `cProfile` and sort by cumulative time (`-s cumulative`). Identify the specific function consuming the most time.
5. **Micro-Profile**: Decorate the identified function with `@profile`. Execute `kernprof -l -v` (for CPU) or `python -m memory_profiler` (for RAM).
6. **Analyze Output**: Identify the exact line with the highest `% Time` or highest RAM `Increment`.
7. **Optimize**: Rewrite the specific line/block. Consider algorithmic changes, swapping operator order, or utilizing built-in functions.
8. **Verify Correctness**: Run the unit tests to ensure the optimization did not alter the program's output.
9. **Verify Performance**: Rerun the micro and macro profiles. Compare the new metrics against the baseline to definitively prove the bottleneck was resolved.

# @Examples (Do's and Don'ts)

## Timing Code Execution
**[DO]** Use a structured decorator to wrap functions for clean, reusable, and coarse timing without cluttering business logic:
```python
import time
from functools import wraps

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {fn.__name__} took {(t2 - t1):0.2f} seconds")
        return result
    return measure_time

@timefn
def expensive_calculation():
    pass
```

**[DON'T]** Clutter algorithms with raw `print` statements mixed into the business logic.
```python
def expensive_calculation():
    t1 = time.time()
    # do work
    t2 = time.time()
    print("Work done in", t2-t1)
```

## Preserving Unit Tests While Profiling
**[DO]** Inject a no-op `@profile` decorator into the namespace so `pytest` can execute the file without raising a `NameError`:
```python
# Check for line_profiler or memory_profiler in the local scope.
# If absent, inject a dummy @profile decorator.
if 'line_profiler' not in dir() and 'profile' not in dir():
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner

@profile
def function_to_test_and_profile():
    return sum(range(100000))
```

**[DON'T]** Leave `@profile` bare without a fallback, which strictly binds the code to `kernprof` and breaks standard test runners.
```python
@profile # Will raise NameError if run with standard python or pytest
def function_to_test_and_profile():
    return sum(range(100000))
```

## Leveraging Bytecode Efficiency
**[DO]** Use standard built-in functions and list comprehensions which map to heavily optimized C-backend bytecode instructions:
```python
def fn_terse(upper=1_000_000):
    return sum(range(upper)) # Executes ~7 bytecode instructions
```

**[DON'T]** Write manual loops for standard accumulations, which forces the Python virtual machine to perform expensive dynamic type lookups on every single iteration:
```python
def fn_expressive(upper=1_000_000):
    total = 0
    for n in range(upper):
        total += n # Executes ~17 bytecode instructions and type checks per loop
    return total
```

## Logical Operator Short-Circuiting
**[DO]** Place the cheapest computational checks on the left side of an `and` statement so Python can short-circuit before executing expensive functions.
```python
# n < maxiter evaluates in ~20ns. abs(z) evaluates in ~66ns.
while n < maxiter and abs(z) < 2:
    z = z * z + c
    n += 1
```

**[DON'T]** Place expensive dynamic function calls on the left side of a logical evaluation.
```python
# Forces the expensive abs() to be evaluated even if n >= maxiter
while abs(z) < 2 and n < maxiter: 
    z = z * z + c
    n += 1
```