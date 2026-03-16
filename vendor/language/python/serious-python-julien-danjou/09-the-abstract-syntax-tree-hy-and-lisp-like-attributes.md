@Domain
This rule file is activated for tasks involving Python Abstract Syntax Tree (AST) manipulation, dynamic code parsing/generation, the creation of custom `flake8` plugins/checks, and development using the Hy programming language (Python's Lisp dialect).

@Vocabulary
- **AST (Abstract Syntax Tree)**: A tree representation of the structure of the source code.
- **Node**: A single element in the AST representing an operation, statement, expression, or module.
- **`_ast.Module`**: The root element of a standard Python AST representing the contents of a file.
- **Statements (`ast.stmt`)**: AST nodes that influence control flow (e.g., `ast.Assign`, `ast.ClassDef`, `ast.FunctionDef`, `ast.if`).
- **Expressions (`ast.expr`)**: AST nodes that produce a value and have no impact on program flow (e.g., `ast.Call`, `ast.Name`, `ast.Str`).
- **`ast.parse`**: Function that parses a string of Python code and returns an AST (`_ast.Module`).
- **`ast.dump`**: Function that returns a string representation of the whole tree for visualization and debugging.
- **`compile`**: Built-in Python function that takes an AST, a source filename, and a mode to generate a native code object.
- **`ast.walk`**: Function for iterating non-destructively over all nodes in an AST.
- **`ast.NodeTransformer`**: Base class utilized to walk through an AST and modify particular nodes via `visit_<NodeType>` methods.
- **`ast.fix_missing_locations`**: Function used to automatically populate missing `lineno` and `col_offset` attributes on AST nodes.
- **`ast.literal_eval`**: A safer alternative to `eval` for evaluating strings that contain only simple data types.
- **Hy**: A Lisp dialect that parses a Lisp-like language and converts it to regular Python AST.
- **s-expressions**: Parentheses-based list structures used in Hy/Lisp to construct code.

@Objectives
- Safely parse, analyze, and manipulate Python source code programmatically using the `ast` module.
- Construct and evaluate executable Python code dynamically from manually built or transformed ASTs.
- Create custom, robust `flake8` linting rules that utilize AST walking.
- Ensure that AST modifications maintain proper metadata (line numbers, column offsets) to allow successful compilation.
- Utilize Hy for functional, Lisp-like programming while seamlessly interoperating with the Python ecosystem.

@Guidelines
- **AST Compilation Modes**: When using `compile()`, the mode must match the AST root:
  - Use `'exec'` when the root is an `_ast.Module`.
  - Use `'eval'` when the root is an `ast.Expression`.
  - Use `'single'` when the root is an `ast.Interactive` (single statement/expression).
- **Node Metadata Requirement**: Python refuses to compile an AST object that lacks `lineno` and `col_offset`. When dynamically creating or modifying AST nodes, you MUST manually set these attributes or call `ast.fix_missing_locations(tree)` before compilation.
- **Node Modification vs. Inspection**: 
  - If you only need to read/inspect nodes, use `ast.walk(tree)`.
  - If you need to alter/replace nodes dynamically, subclass `ast.NodeTransformer` and implement `visit_<NodeType>(self, node)` methods.
- **Safe Evaluation**: Use `ast.literal_eval` instead of `eval` when evaluating strings that should return simple data types to prevent malicious code execution.
- **Flake8 Plugin Architecture**:
  - The plugin MUST be a class.
  - The `__init__` method MUST accept `(self, tree, filename)`.
  - The `run(self)` method MUST yield tuples in the strict format: `(lineno, col_offset, error_string, code)`.
  - Plugins MUST be registered in `setup.cfg` under `[entry_points]` -> `flake8.extension`.
- **AST Version Compatibility**: Be aware that Python's AST is not a guaranteed public interface. It varies between Python 2 and 3, across minor Python 3 versions, and between CPython and PyPy. When writing AST parsers, implement version checks (e.g., `six.PY3`) if dealing with specific variable/node signatures (like `arg` vs `id` in function definitions).
- **Hy Programming Rules**:
  - Unquoted lists are evaluated: the first element is the function, the rest are arguments.
  - Use `(import module_name)` to directly interoperate with standard Python libraries.
  - Utilize Hy macros like `cond` for multiple branching paths instead of chaining verbose `if/elif/else` constructs.
  - Map Python OOP concepts using `defclass`.

@Workflow
1. **Analyze Code Structure**: Use `ast.dump(ast.parse("code string"))` to reverse-engineer and visualize the exact AST structure you need to target or build.
2. **Build or Parse the Tree**: Create the `_ast.Module` tree via `ast.parse()` or by instantiating AST objects (e.g., `ast.Call`, `ast.Name`).
3. **Traverse/Modify**: 
   - For linting/checking: Iterate via `ast.walk()`, using `isinstance(node, ast.<Type>)` to filter irrelevant code early.
   - For transforming: Instantiate your `ast.NodeTransformer` subclass and run `transformer.visit(tree)`.
4. **Fix Metadata**: Call `ast.fix_missing_locations(tree)` to ensure all nodes have valid line numbers and column offsets.
5. **Compile**: Convert the tree to bytecode using `code = compile(tree, '<input>', 'exec')`.
6. **Evaluate**: Run the compiled bytecode using `eval(code)`.

@Examples (Do's and Don'ts)

- **AST Compilation Metadata**
  - [DO]: Fix missing locations before compiling an artificially generated AST.
    ```python
    tree = ast.parse("x = 1/3")
    tree = ReplaceBinOp().visit(tree)
    ast.fix_missing_locations(tree)
    eval(compile(tree, '<input>', 'exec'))
    ```
  - [DON'T]: Attempt to compile a manually built node without `lineno` and `col_offset`.
    ```python
    hello_world = ast.Str(s='hello world!') # Missing lineno and col_offset
    # This will fail during compile()
    ```

- **Flake8 Plugin Implementation**
  - [DO]: Follow the exact class signature and yield structure.
    ```python
    class StaticmethodChecker(object):
        def __init__(self, tree, filename):
            self.tree = tree

        def run(self):
            for stmt in ast.walk(self.tree):
                if not isinstance(stmt, ast.ClassDef):
                    continue
                # ... checking logic ...
                yield (
                    body_item.lineno,
                    body_item.col_offset,
                    "H904: method should be declared static",
                    "H904",
                )
    ```
  - [DON'T]: Forget to register the plugin in `setup.cfg`.
    ```ini
    # DO THIS in setup.cfg:
    [entry_points]
    flake8.extension =
        H904 = ast_ext:StaticmethodChecker
    ```

- **Node Filtering During Walk**
  - [DO]: Skip irrelevant nodes immediately to optimize the walk.
    ```python
    for stmt in ast.walk(self.tree):
        if not isinstance(stmt, ast.ClassDef):
            continue
    ```
  - [DON'T]: Deeply nest logic without type-checking the AST node first, which leads to `AttributeError`s.

- **Safe String Evaluation**
  - [DO]: Use `ast.literal_eval` for evaluating data structures.
    ```python
    import ast
    safe_dict = ast.literal_eval("{'key': 'value'}")
    ```
  - [DON'T]: Use `eval()` on unsanitized strings that just contain data.
    ```python
    unsafe_dict = eval("{'key': 'value'}") # Anti-pattern
    ```

- **Hy Branching**
  - [DO]: Use `cond` for clean, Lisp-like multiple branching.
    ```clojure
    (cond
      [(> somevar 50) (print "Too big!")]
      [(< somevar 10) (print "Too small!")]
      [true (print "Jusssst right!")])
    ```
  - [DON'T]: Write deeply nested `if` statements in Hy.