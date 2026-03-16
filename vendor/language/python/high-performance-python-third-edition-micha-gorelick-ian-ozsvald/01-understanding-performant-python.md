@Domain
These rules are triggered when the user requests assistance with writing, optimizing, refactoring, profiling, or architecting Python code, particularly in the domains of scientific computing, data processing, machine learning, or general performance-critical applications. They also apply when the user requests help structuring a new Python project, converting Jupyter Notebooks to production code, or implementing testing and deployment pipelines for Python applications.

@Vocabulary
- **Computing Unit**: A component (CPU, GPU, TPU) responsible for transforming bits. Measured in Instructions Per Cycle (IPC) and clock speed.
- **Vectorization / SIMD (Single Instruction, Multiple Data)**: The ability of a CPU to perform the same operation on multiple pieces of data in a single clock cycle.
- **Hyperthreading**: Interleaving two threads of instructions into the execution units on a single CPU to maximize resource utilization.
- **Out-of-order Execution**: A compiler/hardware optimization where instructions are executed asynchronously based on resource availability rather than strict sequence, provided sequential dependencies are respected.
- **Amdahl's Law**: A principle stating that the maximum theoretical speedup of a parallelized program is strictly limited by the portion of the program that must run serially.
- **GIL (Global Interpreter Lock)**: A Python mechanism ensuring only one thread can modify a Python object at a time, severely limiting multithreading performance for CPU-bound tasks.
- **Memory Latency**: The time it takes a device to locate the data being requested.
- **Sequential Read vs. Random Access**: Reading contiguous chunks of memory (fast) versus reading scattered fragments (slow).
- **Bus Width & Frequency**: The amount of data moved in one transfer and the number of transfers per second.
- **Heavy Data**: The concept that moving data around hardware architecture requires significant time and effort, dictating that data should remain where it is needed whenever possible.
- **TDD (Test-Driven Development)**: A methodology of writing tests for expected input/output before writing the functional code.
- **JIT (Just-In-Time) Compiler**: A compiler that optimizes and compiles code down to machine code at runtime (e.g., PyPy, Numba, or the "copy and patch" JIT in Python 3.13+).
- **Copy and Patch**: A JIT methodology utilizing semi-compiled "stencils" of op-codes filled with variable memory addresses at runtime.

@Objectives
- Minimize computational overhead and optimize operations based on the underlying hardware architecture constraints (CPU caches, memory tiering, bus transfers).
- Prioritize team velocity, maintainability, and code readability over obscure or brittle block-level optimizations.
- Enforce the "Make it work, Make it right, Make it fast" lifecycle for all software development.
- Maximize sequential memory reads and minimize data movement (heavy data) by keeping data close to the CPU.
- Transition experimental code (e.g., Jupyter Notebooks) into robust, tested, and documented modular software.

@Guidelines

**Hardware and Architectural Awareness**
- The AI MUST consider CPU cache sizes (L1/L2) and bus transfer limitations when designing data structures.
- The AI MUST optimize memory access patterns to favor sequential reads over random data access, minimizing memory fragmentation caused by garbage collection.
- The AI MUST recognize Amdahl's Law and actively identify the serial bottlenecks in any parallelization strategy.
- The AI MUST avoid Python multithreading for CPU-bound tasks due to the GIL, instead utilizing `multiprocessing`, `Cython`, `Numba`, or distributed computing models.

**Project Structure and Tooling**
- The AI MUST enforce the use of isolated virtual environments (`Docker`, `Anaconda`, `pyenv`, `virtualenv`) to prevent OS-level dependency pollution.
- The AI MUST generate a `Dockerfile` at the top level to declare required OS-level libraries and guarantee reproducibility.
- The AI MUST generate a `README` file detailing the project's purpose, folder structure, data provenance, critical files, and run/test instructions.
- The AI MUST utilize a `NOTES` scratchpad file during active development for temporary commands, function defaults, and heuristics before migrating them to formal documentation.
- The AI MUST enforce PEP 8 coding standards automatically using `black` for formatting and `flake8` for linting.

**Testing and Correctness**
- The AI MUST place all tests in a dedicated `tests/` directory.
- The AI MUST use `pytest` as the primary test runner and utilize the `coverage` tool to ensure complete line coverage.
- The AI MUST implement Integration Tests before modifying or inheriting legacy code to ensure overall flow and input/output expectations remain intact.
- The AI MUST write an immediate regression test whenever a bug is encountered ("no value to being bitten twice").
- The AI MUST strongly advocate for Test-Driven Development (TDD), defining tests before writing the underlying business logic.

**Code Quality and Readability**
- The AI MUST prioritize readability over "clever" but opaque code.
- The AI MUST refactor any function that grows longer than a single screen of text into shorter, testable components.
- The AI MUST provide descriptive docstrings for every function, class, and module, including short examples of expected outputs where possible.
- The AI MUST write early-termination clauses in loops and searches to skip unnecessary computations.
- The AI MUST NOT use `assert` statements for checking data state or validating inputs in idiomatic Python; instead, the AI MUST explicitly check conditions and raise appropriate exceptions (e.g., `ValueError`) or use validation frameworks like `Pandera`.

**Jupyter Notebook Practices**
- The AI MUST extract long functions out of Notebooks and into dedicated, testable Python modules.
- The AI MUST wrap logic in classes if encapsulation and data hiding are useful.
- The AI MUST insert sanity checks at the end of Notebooks (logic checks, `raise`, and `print` statements) to demonstrate the generated output is correct.
- The AI MUST recommend tools like `nbdime` for diffing Jupyter Notebooks in source control.

**Choosing the Right Standard and Third-Party Libraries**
- The AI MUST rely on Python's "batteries included" libraries where applicable (`io`, `array`, `math`, `sqlite3`, `collections`, `asyncio`).
- The AI MUST offload heavy numerical, matrix, and ML computations to optimized C/Fortran-backed libraries (e.g., `numpy`, `scipy`, `pandas`, `polars`, `scikit-learn`, `PyTorch`).

@Workflow
1. **Make It Work**: Build a "good-enough" prototype. Focus on measuring the problem, planning the architecture, and proving the concept is feasible without over-engineering.
2. **Make It Right**: Implement rigorous structure. Add a strong test suite (`pytest`), write clear documentation (`README`, docstrings), set up reproducibility (`Dockerfile`), and ensure code readability (`black`, `flake8`).
3. **Make It Fast**: Profile the working, tested code to identify true bottlenecks. Apply optimizations (compilation, parallelization, vectorization) strictly guided by profiling data. Use the test suite to verify that the optimized code still produces correct results.

@Examples (Do's and Don'ts)

**Data Validation**
- [DO]: Explicitly check data states and raise standard exceptions.
```python
def process_age(age: int):
    if age < 0:
        raise ValueError("Age cannot be negative.")
    # Process age
```
- [DON'T]: Use `assert` for runtime data validation, as it can be disabled globally and violates idiomatic Python practices.
```python
def process_age(age: int):
    assert age >= 0, "Age cannot be negative."
    # Process age
```

**Search Iteration**
- [DO]: Utilize early termination to avoid unnecessary compute cycles.
```python
def search_fast(haystack, needle):
    for item in haystack:
        if item == needle:
            return True
    return False
```
- [DON'T]: Iterate through the entire collection after a condition has already been met.
```python
def search_slow(haystack, needle):
    return_value = False
    for item in haystack:
        if item == needle:
            return_value = True
    return return_value
```

**Jupyter Notebook Code Management**
- [DO]: Keep Notebooks lightweight by importing complex logic from external, tested modules.
```python
# Inside Jupyter Notebook
from my_project.data_processor import clean_data
cleaned = clean_data(raw_data)
# Followed by final state sanity check
if cleaned is None or len(cleaned) == 0:
    raise RuntimeError("Data cleaning failed to produce output.")
```
- [DON'T]: Define 300-line operational functions directly inside a Jupyter cell, making it impossible to unit test or version control efficiently.