# @Domain
Python codebase maintenance, static analysis configuration, continuous integration (CI/CD) setup, code complexity reduction, security scanning, and the development of custom abstract syntax tree (AST) linters. Triggers when users request code review, security audits, linting setup, or enforcement of domain-specific coding standards.

# @Vocabulary
- **Static Analysis**: Tools that inspect the codebase without executing it, looking for potential errors, stylistic inconsistencies, and security flaws.
- **Linter**: A class of static analysis tools that search for common programming mistakes and style violations (e.g., Pylint).
- **Shift Errors Left**: A DevOps tenet focusing on finding and fixing errors as early in the development cycle as possible, reducing the cost of remediation.
- **Astroid**: A library used by Pylint to parse Python files into an Abstract Syntax Tree (AST), providing a structured way to interact with Python source code programmatically.
- **Swiss Cheese Model**: The concept of stacking multiple defensive tools (typecheckers, linters, security scanners), where the "holes" (blind spots) of one tool are covered by the strengths of another.
- **Cyclomatic Complexity**: A heuristic measuring the number of independent execution paths in a control flow graph of a codebase (measured via tools like `mccabe`).
- **Whitespace Heuristic**: A simpler complexity heuristic that evaluates the average or total levels of indentation in a Python file to identify overly nested, complex code.
- **Bandit**: A Python static analysis tool dedicated to finding common security vulnerabilities.
- **Dodgy**: A static analysis tool specifically designed to look for leaked secrets and hardcoded credentials.

# @Objectives
- Build an overlapping "Swiss Cheese" safety net consisting of linters, complexity checkers, and security scanners to catch errors before they reach production.
- Shift errors left by integrating static analysis tools into CI pipelines, pre-commit hooks, and server-side hooks.
- Enforce strict coding standards by eliminating dangerous defaults, dead code, and inconsistent return statements.
- Extend static analysis to domain-specific business rules by writing custom Pylint plugins that parse the AST.
- Reduce cognitive load and bug density by proactively identifying and refactoring code with high cyclomatic or whitespace complexity.
- Harden codebase security by systematically scanning for hardcoded secrets, injection vulnerabilities, and misconfigurations.

# @Guidelines

## Linting & Pylint
- The AI MUST utilize or recommend `pylint` to check for PEP 8 style violations, dead/unreachable code, access constraint violations (private/protected members), unused variables/functions, lack of class cohesion, and missing docstrings.
- The AI MUST flag dangerous mutable default arguments (e.g., `[]` or `{}`) and refactor them to use `None` with internal instantiation.
- The AI MUST prevent inconsistent return statements. If a function can return a value, all execution paths MUST explicitly return a value. 
- The AI MUST NOT rely exclusively on `assert` statements to prevent falling through to implicit `return None` paths, as `assert` statements are stripped when Python runs with the `-O` optimization flag.

## Custom Domain Linters (Pylint & Astroid)
- When requested to enforce business logic invariants or domain-specific constraints statically, the AI MUST write custom Pylint plugins.
- Custom checkers MUST inherit from `pylint.checkers.BaseChecker` and implement `pylint.interfaces.IAstroidChecker`.
- The AI MUST define plugin metadata including `name`, `priority`, and `msgs` (mapping error codes like `W0001` to a tuple of message, identifier, and description).
- The AI MUST traverse the AST using `astroid` hook methods such as `visit_functiondef`, `leave_functiondef`, and `visit_call`.
- The AI MUST track state during AST traversal (e.g., recording when execution enters a specific function via `visit_functiondef` and clearing that state in `leave_functiondef`) to enforce context-specific rules.
- The AI MUST use `self.add_message('message-identifier', node=node)` to flag detected violations.
- The AI MUST provide a `register(linter: PyLinter)` function at the module level to load the custom checker.

## Complexity Checking
- The AI MUST treat high complexity as a primary heuristic for identifying bug hotspots.
- The AI MUST utilize or recommend the `mccabe` tool to check for cyclomatic complexity (e.g., flagging functions with a complexity score `>= 5` using `--min 5`).
- The AI MUST employ the Whitespace Heuristic to assess complexity by tracking indentation levels (replacing tabs with 4 spaces and calculating `len(text) - len(text.lstrip())`). Deeply nested code MUST be flagged for refactoring.

## Security Scanning
- The AI MUST actively scan for and flag any hardcoded secrets (e.g., AWS keys, API tokens). The AI MUST recommend tools like `dodgy` or exact text searches to prevent secrets from entering version control.
- The AI MUST utilize or recommend `bandit` (`bandit -r path/to/code`) to catch severe security flaws.
- The AI MUST specifically check for flaws caught by Bandit, including:
  - Flask running in debug mode (Remote Code Execution risk).
  - HTTPS requests with certificate validation disabled.
  - Raw SQL statements susceptible to SQL injection.
  - Weak cryptographic key creation.
  - Unsafe YAML loading (`yaml.load` instead of `yaml.safe_load`).
- The AI MUST NOT treat static security analyzers as the only line of defense; it MUST explicitly recommend supplemental practices like penetration testing and audits.

# @Workflow
1. **Tool Stack Assembly**: When establishing a safety net, configure a multi-layered static analysis stack including a typechecker (mypy), a linter (pylint), a complexity checker (mccabe), and a security scanner (bandit).
2. **Standard Linting Pass**: Run codebase through Pylint. Resolve mutable defaults, inconsistent returns, and unreachable code.
3. **Complexity Audit**: Run `mccabe` and evaluate whitespace nesting. Refactor any function exceeding a cyclomatic complexity of 5 or displaying excessive indentation.
4. **Security Audit**: Scan for raw secrets using `dodgy` or `grep`. Run `bandit` across the codebase to identify injection risks and unsafe configurations. Resolve all high-severity security warnings.
5. **Custom Invariant Enforcement**: Identify business rules that rely on developer discipline (e.g., "Only construct X via factory Y"). Write a custom Pylint AST plugin to enforce this rule statically.
6. **Shift Left Integration**: Provide configurations to execute this entire suite within the project's CI/CD pipeline and local pre-commit hooks.

# @Examples (Do's and Don'ts)

## Linting: Mutable Defaults and Return Statements
- **[DON'T]** Use mutable defaults and implicit returns masked by asserts.
  ```python
  def add_authors_cookbooks(author_name: str, cookbooks: list[str] = []) -> bool:
      author = find_author(author_name)
      if author is None:
          assert False, "Author does not exist" # Fails if -O flag is passed
      else:
          for cookbook in author.get_cookbooks():
              cookbooks.append(cookbook)
          return True
  ```
- **[DO]** Use `None` for mutable defaults and ensure consistent explicit returns.
  ```python
  def add_authors_cookbooks(author_name: str, cookbooks: Optional[list[str]] = None) -> bool:
      if cookbooks is None:
          cookbooks = []
      author = find_author(author_name)
      if author is None:
          raise ValueError("Author does not exist")
      for cookbook in author.get_cookbooks():
          cookbooks.append(cookbook)
      return True
  ```

## Custom Pylint Checkers
- **[DON'T]** Rely solely on code comments to enforce strict structural business logic.
  ```python
  # NOTE: Only create ReadyToServeHotDog using prepare_for_serving method.
  ReadyToServeHotDog = NewType("ReadyToServeHotDog", HotDog)
  ```
- **[DO]** Write an `astroid` based Pylint plugin to structurally enforce the invariant.
  ```python
  import astroid
  from pylint.checkers import BaseChecker
  from pylint.interfaces import IAstroidChecker
  from pylint.lint.pylinter import PyLinter

  class ServableHotDogChecker(BaseChecker):
      __implements__ = IAstroidChecker
      name = 'unverified-ready-to-serve-hotdog'
      priority = -1
      msgs = {
          'W0001': (
              'ReadyToServeHotDog created outside of prepare_for_serving.',
              'unverified-ready-to-serve-hotdog',
              'Only create a ReadyToServeHotDog through prepare_for_serving.'
          ),
      }

      def __init__(self, linter=None):
          super().__init__(linter)
          self._is_in_prepare_for_serving = False

      def visit_functiondef(self, node: astroid.scoped_nodes.FunctionDef):
          if node.name == "prepare_for_serving":
              self._is_in_prepare_for_serving = True

      def leave_functiondef(self, node: astroid.scoped_nodes.FunctionDef):
          if node.name == "prepare_for_serving":
              self._is_in_prepare_for_serving = False

      def visit_call(self, node: astroid.node_classes.Call):
          if getattr(node.func, "name", "") != 'ReadyToServeHotDog':
              return
          if self._is_in_prepare_for_serving:
              return
          self.add_message('unverified-ready-to-serve-hotdog', node=node)

  def register(linter: PyLinter):
      linter.register_checker(ServableHotDogChecker(linter))
  ```

## Security Scanning
- **[DON'T]** Write unsafe, vulnerable parsing or execution code.
  ```python
  import yaml
  # Bandit will flag this as unsafe YAML loading
  data = yaml.load(user_input) 
  
  # Bandit will flag this as potential SQL injection
  cursor.execute(f"SELECT * FROM users WHERE name = '{user_name}'")
  ```
- **[DO]** Use safe methods and parameterized queries to pass security static analysis.
  ```python
  import yaml
  data = yaml.safe_load(user_input)
  
  cursor.execute("SELECT * FROM users WHERE name = ?", (user_name,))
  ```