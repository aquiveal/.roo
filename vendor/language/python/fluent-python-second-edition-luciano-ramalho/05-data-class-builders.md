@Domain
Python codebases involving the creation of data-centric classes, record types, DTOs (Data Transfer Objects), and structural pattern matching of class instances. Activation triggers include user requests to create data containers, usage of `collections.namedtuple`, `typing.NamedTuple`, `@dataclasses.dataclass`, class pattern matching (`match/case`), and refactoring "anemic" classes (classes with data but no behavior).

@Vocabulary
- **Data Class**: A class that is essentially a collection of fields with little or no extra functionality.
- **Class Builder**: A standard library tool or decorator (`namedtuple`, `NamedTuple`, `@dataclass`) that automatically generates boilerplate methods like `__init__`, `__repr__`, and `__eq__`.
- **Type Hint / Annotation**: A declaration of the expected type of a variable, function parameter, or return value. Python ignores these at runtime; they exist for static type checkers (e.g., Mypy) and IDEs.
- **Mutable Default Value**: A default value for a parameter that can be modified in place (e.g., `list`, `dict`, `set`). A common source of bugs if shared across instances.
- **`default_factory`**: A parameter in `dataclasses.field` that accepts a zero-argument callable to generate a fresh default value for each new instance.
- **`__post_init__`**: A special method called automatically by the generated `__init__` in a `@dataclass` to perform validation or compute field values based on other fields.
- **`ClassVar`**: A `typing` pseudotype used to declare a class attribute, signaling to `@dataclass` that it should not be processed as an instance field.
- **`InitVar`**: A `dataclasses` pseudotype used to declare arguments passed to `__init__` (and subsequently `__post_init__`) that do not become instance fields.
- **Data Class Code Smell**: An anti-pattern described by Martin Fowler where classes consist only of data and accessors with no behavior, violating the core OOP principle of grouping data and behavior.
- **Scaffolding**: An initial, simplistic implementation of a class used to jump-start a project, where a data class is temporarily acceptable.
- **Intermediate Representation**: A valid use case for a data class where records are built for export/import across system boundaries (e.g., JSON serialization).
- **Destructuring**: An advanced form of unpacking used in pattern matching to extract values from objects.
- **`__match_args__`**: A special class attribute listing instance attributes in the order they should be used for positional pattern matching.

@Objectives
- Automate boilerplate method generation by selecting the most appropriate data class builder based on mutability and syntax requirements.
- Ensure strict type safety and memory safety regarding mutable defaults in data class definitions.
- Apply `__post_init__`, `ClassVar`, and `InitVar` accurately to handle complex initialization and class-level state in `@dataclass` architectures.
- Prevent the proliferation of the "Data Class Code Smell" by advocating for the inclusion of behavior alongside data, restricting pure data classes to scaffolding or intermediate representations.
- Implement robust structural pattern matching on class instances using keyword and positional patterns.

@Guidelines
- **Selecting a Class Builder**:
  - The AI MUST use `collections.namedtuple` for simple, backward-compatible, immutable records without type hints.
  - The AI MUST use `typing.NamedTuple` for immutable records that require type hints and class statement syntax (allowing custom methods and docstrings).
  - The AI MUST use `@dataclasses.dataclass` for mutable records, or when deep customization of generated methods (`__repr__`, `__eq__`, `__hash__`) is required. Use `@dataclass(frozen=True)` if instances must be immutable.
- **Type Hints**:
  - The AI MUST NOT assume type hints enforce types at runtime. Type hints must be treated strictly as static analysis tools.
  - The AI MUST read annotations dynamically using `inspect.get_annotations(MyClass)` (Python 3.10+) or `typing.get_type_hints(MyClass)` (Python 3.5+), and MUST NOT read from `__annotations__` directly, to ensure forward references are resolved correctly.
- **Dataclass Fields and Initialization**:
  - The AI MUST explicitly use `dataclasses.field(default_factory=...)` for any instance field requiring a mutable default value (e.g., `list`, `set`, `dict`).
  - The AI MUST implement `__post_init__` when validation or computed initialization logic is required after the standard `__init__`.
- **Special Dataclass Variables**:
  - The AI MUST annotate class attributes inside a `@dataclass` using `typing.ClassVar[Type]` so the decorator does not convert them into instance fields.
  - The AI MUST annotate arguments meant only for initialization (passed to `__init__` and `__post_init__` but not saved as fields) using `dataclasses.InitVar[Type]`.
- **Object-Oriented Design (Code Smells)**:
  - When encountering a heavily used data class with no significant behavior, the AI MUST recommend refactoring to move the functions that manipulate this data into the class itself.
  - Pure data classes MUST ONLY be preserved if they represent temporary scaffolding or an intermediate representation for data interchange (e.g., pre-JSON serialization).
- **Pattern Matching**:
  - The AI MUST use Simple Class Patterns (e.g., `case float(x):`) ONLY for the nine blessed built-in types (`bytes`, `dict`, `float`, `frozenset`, `int`, `list`, `set`, `str`, `tuple`).
  - For custom classes, the AI MUST use Keyword Class Patterns (e.g., `case City(continent='Asia', country=cc):`) for explicit readability.
  - To support Positional Class Patterns (e.g., `case City('Asia', _, country):`), the AI MUST ensure the target class defines the `__match_args__` tuple. (Note: `NamedTuple` and `@dataclass` generate this automatically).

@Workflow
1. **Analyze Requirements**: Determine if the requested object needs to be mutable or immutable, and if it requires type hints.
2. **Select Builder**: Choose between `collections.namedtuple`, `typing.NamedTuple`, or `@dataclass`.
3. **Define Attributes & Types**: Write the class definition using PEP 526 variable annotation syntax.
4. **Isolate Class vs. Instance Scope**: Check for class attributes and wrap their types in `typing.ClassVar[]`. Check for initialization-only arguments and wrap them in `dataclasses.InitVar[]`.
5. **Secure Defaults**: Scan for mutable default values (`[]`, `{}`, etc.). Replace them immediately with `field(default_factory=...)`.
6. **Inject Behavior**: If custom validation or computed attributes are needed, implement `def __post_init__(self):`.
7. **Evaluate OOP Health**: Review the class. If it is purely a dumb data holder and is heavily manipulated by external functions, refactor to encapsulate those functions as methods within the class.
8. **Enable Pattern Matching**: If the class was built manually (without a class builder) and requires positional pattern matching, define `__match_args__ = ('field1', 'field2')`.

@Examples (Do's and Don'ts)

**1. Handling Mutable Defaults in `@dataclass`**
- [DO]:
```python
from dataclasses import dataclass, field

@dataclass
class ClubMember:
    name: str
    guests: list[str] = field(default_factory=list)
```
- [DON'T] (Raises ValueError):
```python
from dataclasses import dataclass

@dataclass
class ClubMember:
    name: str
    guests: list = []  # Anti-pattern: mutable default
```

**2. Declaring Class Attributes in `@dataclass`**
- [DO]:
```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class HackerClubMember:
    name: str
    all_handles: ClassVar[set[str]] = set()
```
- [DON'T] (Treats `all_handles` as an instance field):
```python
from dataclasses import dataclass

@dataclass
class HackerClubMember:
    name: str
    all_handles: set[str] = set()
```

**3. Using Initialization-Only Variables**
- [DO]:
```python
from dataclasses import dataclass, InitVar

@dataclass
class C:
    i: int
    j: int = None
    database: InitVar[DatabaseType] = None

    def __post_init__(self, database):
        if self.j is None and database is not None:
            self.j = database.lookup('j')
```
- [DON'T] (Treats `database` as a standard stored instance field):
```python
from dataclasses import dataclass

@dataclass
class C:
    i: int
    j: int = None
    database: DatabaseType = None
```

**4. Reading Type Annotations at Runtime**
- [DO]:
```python
import inspect

class Coordinate:
    lat: float
    lon: float

# Python 3.10+
annotations = inspect.get_annotations(Coordinate)
# Or Python 3.5+
# import typing
# annotations = typing.get_type_hints(Coordinate)
```
- [DON'T] (Fails to resolve forward references properly):
```python
class Coordinate:
    lat: float
    lon: float

annotations = Coordinate.__annotations__
```

**5. Positional Pattern Matching for Custom Classes**
- [DO]:
```python
class Vector2d:
    __match_args__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

def match_vector(v):
    match v:
        case Vector2d(0, 0):
            print("Origin")
```
- [DON'T] (Raises TypeError: accepts 0 positional sub-patterns):
```python
class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def match_vector(v):
    match v:
        case Vector2d(0, 0):
            print("Origin")
```