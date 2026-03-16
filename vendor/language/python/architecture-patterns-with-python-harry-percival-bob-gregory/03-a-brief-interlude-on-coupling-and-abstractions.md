# @Domain
These rules MUST be activated when the AI is tasked with refactoring existing Python code, designing new system architectures, writing unit or integration tests, handling I/O operations (filesystem, network, databases), or addressing issues related to tight coupling and untestable code.

# @Vocabulary
- **Coupling**: The degree to which components depend on each other. High local coupling (cohesion) is desirable; high global coupling (the "Ball of Mud") prevents safe changes.
- **Cohesion**: The principle that components working closely together should support each other locally.
- **Abstraction**: A simplified interface that hides complex low-level details (especially messy I/O), protecting the system from change and reducing the degree of global coupling.
- **FCIS (Functional Core, Imperative Shell)**: An architectural pattern (coined by Gary Bernhardt) where the "core" of the code handles pure business logic without side-effects, and the "shell" handles gathering inputs and applying outputs (I/O).
- **Edge-to-Edge Testing**: Testing a whole system or large chunk of a system together by faking out the I/O at the absolute edges, rather than testing individual internal functions in isolation.
- **Dependency Injection (DI)**: Passing stateful components or I/O handlers into a function explicitly as arguments, rather than hardcoding imports or instantiating them internally.
- **Fake**: A working implementation of a dependency that acts as a test double (e.g., an in-memory repository or filesystem) designed exclusively for use in tests. 
- **Spy**: A test double (often a simple list or set) that records how it was used (e.g., appending method calls and arguments to a list) so state-based assertions can be made later.
- **Classic-style TDD**: Test-driven development that relies on setting up state, running code, and asserting on the final state (using Fakes/Spies), rather than asserting on the interactions between intermediaries.
- **London-school TDD**: Test-driven development heavily reliant on Mocks and interaction testing (e.g., `assert_called_once_with`). This approach is explicitly DISCOURAGED by these rules.

# @Objectives
- Reduce global coupling by inserting simple abstractions between business logic and infrastructure/I/O.
- Maximize testability by designing code that does not require real filesystems, networks, or databases to run core logic.
- Design for extensibility (e.g., allowing for `--dry-run` flags or different storage backends without rewriting core logic).
- Enforce Classic-style TDD over London-school TDD: use explicit state-based assertions via Fakes instead of testing behavior via Mocks.
- Separate *what* the system wants to do from *how* it does it.

# @Guidelines

## Architecture and Coupling Constraints
- The AI MUST separate business logic from I/O details. Never interleave I/O operations (e.g., `os.walk`, `shutil.copy`, `requests.get`) with domain decision-making.
- The AI MUST apply the Functional Core, Imperative Shell (FCIS) pattern:
  1. Gather inputs via I/O.
  2. Pass inputs as simple Python data structures (dicts, sets, lists) to a pure function (the core).
  3. The core MUST yield or return a representation of the actions to be taken (e.g., a list of tuples like `('COPY', src, dest)`).
  4. Apply the outputs via I/O.
- The AI MUST utilize Dependency Injection (DI) to pass I/O dependencies to top-level functions.
- The AI MUST NOT mandate Abstract Base Classes (ABCs) or explicit interfaces for DI unless absolutely necessary; Python's dynamic nature allows reliance on duck typing for abstractions.

## Testing and Mocking Anti-Patterns
- The AI MUST AVOID using `unittest.mock.patch` or any mocking/monkeypatching frameworks. Mocking is considered a code smell because it couples tests to implementation details and fails to improve the system's design.
- The AI MUST NOT write tests that verify interactions (e.g., checking if `shutil.copy` was called with specific arguments). 
- The AI MUST write tests that assert on state.
- The AI MUST use Fakes and Spies (e.g., a `FakeFileSystem` class inheriting from `list` that appends actions to itself) to test I/O-dependent code edge-to-edge.
- The AI MUST ensure that the test suite acts as a record of design choices and explains the system. Tests overwhelmed with mock setup code MUST be refactored.

## Heuristics for Choosing Abstractions
- When encountering messy I/O, the AI MUST ask: "Can I choose a familiar Python data structure to represent the state of this messy system and then try to imagine a single function that can return that state?"
- The AI MUST look for seams to draw a line between systems and insert an abstraction.
- The AI MUST explicitly divide components based on responsibilities: one component interrogates state, one makes decisions, and one applies changes.

# @Workflow
When tasked with refactoring heavily coupled code or writing tests for I/O-heavy logic, the AI MUST follow this exact algorithmic process:

1. **Identify Responsibilities**: Analyze the target function and break it down into three categories: gathering state (I/O), business logic/decisions (Core), and applying state changes (I/O).
2. **Define the Data Abstraction**: Create simple Python data structures (like dictionaries mapping hashes to paths, or sets of identifiers) that can fully represent the external state required by the logic.
3. **Extract the Functional Core**: Write a pure function that accepts the data abstraction as input and returns/yields a list of explicit commands or actions to perform (e.g., `('MOVE', old_path, new_path)`).
4. **Build the Imperative Shell**: Refactor the original top-level function to orchestrate the process: call the gathering function, pass the result to the core function, and iterate over the core's output to execute the actual I/O.
5. **Implement Dependency Injection (Optional but recommended for edge-to-edge)**: If testing the imperative shell directly, parameterize the I/O functions (e.g., `reader`, `filesystem`) so they can be injected.
6. **Create Fakes/Spies**: Write test doubles (e.g., a `FakeFileSystem`) that implement the duck-typed interface of the I/O dependencies but simply record the actions applied to them in memory (using sets or lists).
7. **Write State-Based Tests**: Write unit tests that instantiate the Fakes, inject them into the target function, and assert against the state of the Fakes using standard Python comparison operators (e.g., `assert filesystem == [("COPY", "/src", "/dest")]`).

# @Examples (Do's and Don'ts)

## Principle: Functional Core, Imperative Shell (Separating Logic from I/O)

**[DON'T]** Interleave I/O and business logic in a single function.
```python
def sync(source, dest):
    # Coupling I/O and logic makes this untestable without a real filesystem
    for folder, _, files in os.walk(source):
        for fn in files:
            source_path = Path(folder) / fn
            dest_path = Path(dest) / fn
            if not dest_path.exists():
                shutil.copy(source_path, dest_path)
```

**[DO]** Split into Imperative Shell and Functional Core.
```python
def sync(source, dest):
    # Imperative shell: Step 1, gather inputs
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)
    
    # Step 2: Call functional core (NO I/O)
    actions = determine_actions(source_hashes, dest_hashes, source, dest)
    
    # Imperative shell: Step 3, apply outputs
    for action, *paths in actions:
        if action == 'copy':
            shutil.copyfile(*paths)
        elif action == 'move':
            shutil.move(*paths)

def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
    # Pure business logic returning data structures
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            yield 'copy', Path(src_folder) / filename, Path(dst_folder) / filename
```

## Principle: Dependency Injection and Edge-to-Edge Testing

**[DON'T]** Hardcode imports and use `mock.patch` to verify behavior.
```python
from my_app import sync
from unittest import mock

@mock.patch('my_app.shutil.copy')
@mock.patch('my_app.os.walk')
def test_sync(mock_walk, mock_copy):
    mock_walk.return_value = [('/src', [], ['file1.txt'])]
    sync('/src', '/dest')
    mock_copy.assert_called_once_with('/src/file1.txt', '/dest/file1.txt')
```

**[DO]** Use Dependency Injection and a Fake/Spy object for state-based testing.
```python
# Application Code
def sync(reader, filesystem, source_root, dest_root):
    source_hashes = reader(source_root)
    dest_hashes = reader(dest_root)
    # ... logic ...
    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            filesystem.copy(source_root / filename, dest_root / filename)

# Test Code
class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(('COPY', src, dest))
        
def test_sync_copies_missing_file():
    source = {"sha1": "my-file"}
    dest = {}
    filesystem = FakeFileSystem() # Spy
    reader = {"/source": source, "/dest": dest}
    
    sync(reader.pop, filesystem, "/source", "/dest")
    
    # State-based assertion
    assert filesystem == [("COPY", "/source/my-file", "/dest/my-file")]
```