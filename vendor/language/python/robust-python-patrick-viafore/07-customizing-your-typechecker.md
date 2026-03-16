# @Domain
Python development tasks involving type hinting, static analysis configuration, typechecker optimization, security flaw detection (taint analysis), and codebase diagnostic setups using tools like `mypy`, `Pyre`, and `Pyright`.

# @Vocabulary
- **Typechecker**: A static analysis tool that verifies that the codebase's behavior matches the documentation provided by type annotations.
- **Inline Configuration**: Typechecker configuration specified directly at the top of a Python file using comments (e.g., `# mypy: disallow-any-generics`).
- **mypy.ini**: The standard configuration file for `mypy`, supporting both global (`[mypy]`) and per-module (`[mypy-module.*]`) options.
- **Daemon Mode (dmypy)**: A mode of running `mypy` where the process stays alive in memory, enabling near-instantaneous subsequent typechecks.
- **Pyre**: A typechecker developed by Facebook that supports codebase querying and built-in security analysis.
- **Codebase Querying**: Using `pyre query` to introspect attributes, callees, and dependencies of functions/classes directly from the CLI.
- **Pysa (Python Static Analyzer)**: A security-focused static analyzer built into Pyre.
- **Taint Analysis**: The tracking of potentially tainted (untrusted) data from its source to ensure it cannot propagate to a system vulnerability.
- **Taint Source**: The origin of untrusted data (e.g., user input).
- **Taint Sink**: The execution point where untrusted data could cause harm (e.g., `os.system`).
- **Sanitizer Function**: A function (denoted in Pysa via `@sanitize`) that inspects or modifies untrusted data so it can be trusted.
- **Pyright**: A highly configurable typechecker developed by Microsoft.
- **Pylance**: A VS Code extension built upon Pyright that provides real-time workspace diagnostics and autocompletion.

# @Objectives
- Enforce strict, verifiable documentation through rigorous typechecker configuration.
- Eliminate dynamic, untyped behavior (`Any`) and implicit `None` assumptions from the codebase.
- Accelerate the development feedback loop by utilizing typechecker daemon modes and real-time IDE diagnostics.
- Prevent security vulnerabilities like Remote Code Execution (RCE) and SQL injection by modeling and tracking data flow via taint analysis.
- Provide clear, actionable metrics regarding type coverage and dynamic expression usage via generated reports.

# @Guidelines
- The AI MUST configure `mypy` using a `mypy.ini` file, explicitly separating global options (`[mypy]`) from per-module exceptions.
- The AI MUST disable dynamic type inference by enforcing the `--disallow-any-expr` and `--disallow-any-generics` flags unless working with a strictly heterogeneous data structure (like a general-purpose cache).
- The AI MUST strictly require comprehensive function definitions by enabling `--disallow-untyped-defs`, `--disallow-incomplete-defs`, and `--disallow-untyped-calls`.
- The AI MUST prevent the "billion-dollar mistake" (null reference errors) by ensuring `--strict-optional` is enabled.
- The AI MUST NOT use implicit optional typing. It MUST explicitly declare `Optional[Type]` and enable `--no-implicit-optional`.
- When tasked with running `mypy` iteratively, the AI MUST utilize daemon mode (`dmypy run -- mypy-flags <files>`) to drastically reduce execution time.
- When metrics or coverage audits are requested, the AI MUST generate targeted reports using `--html-report`, `--linecount-report`, `--any-exprs-report`, or `--junit-xml`.
- When dealing with user-supplied input or sensitive execution contexts, the AI MUST configure Pyre/Pysa by creating `taint.config` and `.pysa` stub files to define `TaintSource` and `TaintSink`.
- The AI MUST write sanitizer functions mapped via `@sanitize` to break the chain between a `TaintSource` and a `TaintSink` in Pysa models.
- When querying architecture (e.g., finding all callers of a function or attributes of a class), the AI MUST use `pyre query` (e.g., `pyre query "callees(module.function)"`).
- If working in a VS Code context, the AI MUST format and structure types specifically to take advantage of Pylance's real-time diagnostic checking.

# @Workflow
1. **Initialize Configuration**: Create a `mypy.ini` (or equivalent `.pyre_configuration`) at the root of the project. Define the global strictness baseline.
2. **Apply Strict Typing Rules**: Configure the typechecker to reject `Any` expressions, incomplete definitions, and implicit optionals.
3. **Run Diagnostics Iteratively**: Start the typechecker in daemon mode (e.g., `dmypy start` followed by `dmypy run`) to get sub-second feedback on type changes.
4. **Refine Submodules**: If integrating third-party legacy libraries, apply targeted per-module exceptions (e.g., `ignore_missing_imports = True`) rather than weakening the global configuration.
5. **Generate Quality Reports**: Run `--any-exprs-report` to identify and refactor remaining untyped dynamic expressions.
6. **Implement Security Analysis (if applicable)**:
   - Initialize Pyre (`pyre init`).
   - Define a `taint.config` establishing application-specific sources and sinks.
   - Write `.pysa` stub files mapping application functions to `TaintSource` and `TaintSink`.
   - Run `pyre analyze` to locate data flow vulnerabilities.

# @Examples (Do's and Don'ts)

**Concept: Handling Optionals/None**
- [DO] Use explicit optional typing:
  ```python
  def foo(x: Optional[int] = None) -> None:
      if x is not None:
          print(x + 5)
  ```
- [DON'T] Rely on implicit optionals or operate on them without checking:
  ```python
  def foo(x: int = None) -> None:
      print(x + 5)
  ```

**Concept: Inline Configuration**
- [DO] Apply file-specific typechecker instructions cleanly at the top of the file:
  ```python
  # mypy: disallow-any-generics
  ```
- [DON'T] Ignore type errors silently without fixing the underlying configuration.

**Concept: Untyped Definitions**
- [DO] Provide complete type annotations for all parameters and return types:
  ```python
  def plus_four(x: int) -> int:
      return x + 4
  ```
- [DON'T] Leave parameters untyped, falling back to dynamic `Any` behavior:
  ```python
  def plus_four(x):
      return x + 4
  ```

**Concept: Pysa Taint Modeling**
- [DO] Define precise stub files (`.pysa`) to track untrusted data:
  ```python
  # stubs/taint/general.pysa
  def input(__prompt = ...) -> TaintSource[UserControlled]: ...
  def os.system(command: TaintSink[RemoteCodeExecution]): ...
  ```
- [DON'T] Pass user input directly into executable sinks without Pysa tracking and a `@sanitize` step.