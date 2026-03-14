# @Domain
Trigger these rules when refactoring, architecting, or testing Python code that interacts with external state, I/O (e.g., filesystems, network, databases), or when the user requests improvements to code testability, decoupling, or test creation.

# @Vocabulary
- **Coupling (Global)**: The degree to which distinct system components depend on one another. High global coupling (the "Ball of Mud" anti-pattern) is heavily restricted.
- **Coupling (Local) / Cohesion**: The degree to which elements within a single component support one another. High local cohesion is desired.
- **Abstraction**: A simplified interface that hides complex or messy details (like I/O) to protect the core system from change.
- **Functional Core, Imperative Shell (FCIS)**: An architectural pattern where the "core" of the application consists of pure functions with no side-effects (business logic), surrounded by a "shell" that handles stateful operations and I/O.
- **Dependency Injection (DI)**: The practice of passing explicit stateful dependencies (like file readers or filesystems) into functions or classes rather than importing and instantiating them internally.
- **Fake**: A working implementation of a dependency designed exclusively for tests (e.g., an in-memory collection). Fakes are used to make assertions about the end state of a system.
- **Mock**: A test double used to verify how something gets used (e.g., checking if a method was called with specific arguments). Explicitly discouraged in this paradigm.
- **Spy**: A type of test double (often implemented simply as a `list` in Python) that records the actions performed on it so they can be inspected later.
- **Edge-to-Edge Testing**: Testing a whole system or use-case together by invoking the exact production code but faking the I/O at the absolute edges.
- **Classic-style TDD**: Test-driven development that builds tests around state (both in setup and assertions) rather than verifying interactions.
- **London-school TDD**: Test-driven development heavily reliant on mocks and interaction testing. Rejected by this architecture.
- **Duck Typing**: Python's dynamic typing system where the presence of methods and properties determines valid use, rather than explicit inheritance (meaning explicit Abstract Base Classes/ABCs are optional for DI).

# @Objectives
- The AI MUST minimize global coupling by introducing simplifying abstractions between business logic and I/O.
- The AI MUST make systems easier to test by separating "what to do" (logic) from "how to do it" (execution).
- The AI MUST prioritize Classic-style TDD and state-based assertions over interaction testing.
- The AI MUST aggressively avoid mocking frameworks (e.g., `unittest.mock.patch`).
- The AI MUST design for testability, understanding that designing for testability is inherently designing for extensibility.

# @Guidelines

## Choosing Abstractions
- The AI MUST abstract state using familiar Python data structures (e.g., representing a filesystem as a dictionary of hashes to paths).
- The AI MUST carve out explicit "seams" to insert abstractions between logic and external dependencies.
- The AI MUST make implicit concepts explicit by capturing operations as simple data structures (e.g., yielding tuples of `("COPY", src, dest)` instead of directly executing `shutil.copy`).

## Functional Core, Imperative Shell (FCIS)
- The AI MUST separate code into three distinct phases when dealing with I/O:
  1. **Imperative Shell (Gather Inputs)**: Interrogate the external state and convert it to a simple data structure.
  2. **Functional Core (Decide)**: Pass the data structure to pure business logic functions that return an output data structure representing planned actions.
  3. **Imperative Shell (Apply Outputs)**: Read the planned actions and execute the messy I/O.

## Testing and Test Doubles
- **CRITICAL**: The AI MUST NOT use `mock.patch` or monkeypatching. Mocking couples tests to implementation details, hides design flaws, and makes tests brittle.
- The AI MUST use **Fakes** or **Spies** instead of Mocks.
- The AI MUST build simple test doubles. A highly recommended pattern is having a Fake inherit from `list` and append tuple representations of actions (e.g., `self.append(('MOVE', src, dest))`), allowing natural Python assertions like `assert action in fake_filesystem`.
- The AI MUST write Edge-to-Edge tests that invoke the top-level system functions using explicit dependency injection for the Fakes.
- The AI MUST assert against the state of the Fakes rather than making behavioral assertions (e.g., avoid `assert_called_once_with`).

## Dependency Injection
- The AI MUST make dependencies explicit by passing them as arguments to top-level functions (e.g., passing a `reader` function and a `filesystem` object).
- The AI MUST NOT rely on abstract base classes (ABCs) or explicit interfaces unless specifically requested; Python's duck typing is sufficient for adapters/fakes.

# @Workflow
When tasked with refactoring heavily coupled code or making I/O-bound code testable, the AI MUST strictly follow this algorithmic sequence:
1. **Analyze Responsibilities**: Identify exactly what the code needs from the external system (e.g., reading paths, hashing files, moving files).
2. **Define the Abstraction**: Choose basic Python data structures (dicts, sets, tuples) to represent the external state and the desired output actions.
3. **Extract the Functional Core**: Write a pure function that takes the abstracted input state, processes the business logic, and yields or returns the abstracted output actions.
4. **Extract the Imperative Shell**: Write a top-level function that gathers the inputs, calls the functional core, and executes the output actions.
5. **Inject Dependencies**: Modify the top-level function to accept the I/O mechanisms (e.g., reader functions, writer objects) as explicit arguments.
6. **Create Fakes**: Create simple in-memory test doubles (e.g., list-based spies, dictionary-based readers) that conform to the duck-type signature of the injected dependencies.
7. **Write State-Based Tests**: Write edge-to-edge tests that inject the Fakes, execute the top-level function, and assert against the final state of the Fakes.

# @Examples (Do's and Don'ts)

## Principle: Functional Core, Imperative Shell
**[DON'T]** Mix I/O directly with business logic in a way that requires real filesystems to test.
```python
def sync(source, dest):
    for folder, _, files in os.walk(source):
        for fn in files:
            source_path = Path(folder) / fn
            dest_path = Path(dest) / fn
            if not dest_path.exists():
                shutil.copy(source_path, dest_path)
```

**[DO]** Separate state-gathering, logic, and state-applying.
```python
def sync(source, dest):
    # Imperative Shell 1: Gather Inputs
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)
    
    # Functional Core: Call business logic
    actions = determine_actions(source_hashes, dest_hashes, source, dest)
    
    # Imperative Shell 2: Apply Outputs
    for action, *paths in actions:
        if action == 'copy':
            shutil.copyfile(*paths)
        if action == 'move':
            shutil.move(*paths)
        if action == 'delete':
            os.remove(paths[0])

def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
    # Pure logic returning data structures
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            yield 'copy', Path(src_folder) / filename, Path(dst_folder) / filename
```

## Principle: Dependency Injection and Edge-to-Edge Testing
**[DON'T]** Use `mock.patch` to verify interactions.
```python
@mock.patch('shutil.copyfile')
@mock.patch('os.walk')
def test_sync(mock_walk, mock_copy):
    mock_walk.return_value = [('/src', [], ['file1.txt'])]
    sync('/src', '/dst')
    mock_copy.assert_called_once_with('/src/file1.txt', '/dst/file1.txt')
```

**[DO]** Inject explicit dependencies and use Fakes/Spies for state-based assertions.
```python
# Production Code
def sync(reader, filesystem, source_root, dest_root):
    source_hashes = reader(source_root)
    dest_hashes = reader(dest_root)
    
    actions = determine_actions(source_hashes, dest_hashes, source_root, dest_root)
    
    for action, *paths in actions:
        if action == 'copy':
            filesystem.copy(*paths)
        # ... handling other actions ...

# Test Code
class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(('COPY', src, dest))

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source = {"sha1": "my-file"}
    dest = {}
    filesystem = FakeFileSystem()
    reader = {"/source": source, "/dest": dest}
    
    sync(reader.pop, filesystem, "/source", "/dest")
    
    assert [("COPY", "/source/my-file", "/dest/my-file")] == filesystem
```