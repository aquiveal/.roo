@Domain
Trigger conditions for these rules include Python codebase modifications involving data collections, parsing heterogeneous data structures (like JSON, YAML, or CSVs), defining type annotations for lists/dicts/tuples/sets, extending or modifying collection behaviors, and designing generic data structures.

@Vocabulary
- **Collection Types**: Data structures that group arbitrary amounts of data, such as lists, dictionaries, sets, strings, and tuples.
- **Homogeneous Collection**: A collection where every value shares the exact same type or set of expected behaviors (e.g., a list of strings).
- **Heterogeneous Collection**: A collection where values have different types and meanings, forcing consumers to handle special cases.
- **Type Alias**: A descriptive, domain-specific name assigned to a complex type signature to communicate the specific context of a collection.
- **TypedDict**: A Python typing construct used to represent dictionaries with a fixed set of heterogeneous keys and values, highly appropriate for API responses and parsed data.
- **Generics / TypeVar**: Typing constructs used to indicate that a collection operates on an arbitrary type, but enforces consistency of that type throughout the collection's lifetime.
- **UserDict / UserList / UserString**: Wrapper classes located in the `collections` module explicitly designed to be safely subclassed by developers.
- **Abstract Base Classes (ABCs)**: Classes located in `collections.abc` used to implement custom collections by requiring the developer to override specific magic methods.

@Objectives
- Ensure all collection choices explicitly communicate their specific behavioral intent to future developers.
- Enforce the accurate annotation of inner types within all collections.
- Provide strong type-checking safety nets for heterogeneous data structures by utilizing structural typing tools.
- Prevent subtle runtime bugs caused by improperly subclassing Python's C-optimized built-in collections.
- Maximize code reusability and duck-typing compatibility through generic types and Abstract Base Classes.

@Guidelines
- **Always Annotate Inner Types**: Never use bare collection annotations (like `list` or `dict`). Always use bracket syntax to specify the inner types (e.g., `list[Cookbook]`, `dict[str, int]`).
- **Use Type Aliases for Readability**: When a collection's type signature becomes complex or lacks domain context, extract it into a descriptive type alias (e.g., `AuthorToCountMapping = dict[str, int]`).
- **Handle Heterogeneous Sequences Safely**: If a list MUST contain different types, explicitly annotate it with a `Union` (e.g., `list[Union[int, Ingredient]]`) so the typechecker forces users to verify the type before acting on it. Alternatively, use a `tuple` if the positions are fixed.
- **Use TypedDict for Heterogeneous Dictionaries**: Whenever storing heterogeneous data in a dictionary (e.g., reading JSON, YAML, or API responses), you MUST define and use a `TypedDict`. Do not use `dict[str, Any]` or `dict[str, Union[...]]`.
- **NEVER Subclass Built-in Collections Directly**: Do not subclass `dict`, `list`, or `str` to override methods. Built-in collections optimize performance by inlining calls, meaning your overridden methods (like `__getitem__`) will not be reliably called by internal methods (like `get()`).
- **MUST Use `collections.User*` for Modification**: When you need to tweak the behavior of a standard collection, inherit from `collections.UserDict`, `collections.UserList`, or `collections.UserString`. Access and manipulate the underlying storage using the `self.data` attribute.
- **MUST Use `collections.abc` for Custom Interfaces**: When creating a completely custom collection that merely emulates a standard interface, inherit from the appropriate ABC in `collections.abc` (e.g., `collections.abc.Set`) and implement the strictly required magic methods (e.g., `__contains__`, `__iter__`, `__len__`).
- **Use ABCs in Function Signatures**: To fully embrace duck typing while maintaining type safety, use `collections.abc` classes (like `Iterable`, `Mapping`, `Sequence`) for function parameters rather than concrete types (like `list` or `dict`).
- **Use Generics for Reusability**: When building custom collections that shouldn't care about the specific type they hold but must not mix incompatible types, use `typing.TypeVar` and `typing.Generic`.

@Workflow
1. **Analyze Collection Needs**: Determine the data being grouped. Assess if the data is homogeneous (same types/behaviors) or heterogeneous (different types).
2. **Select Standard Collections**: 
    - For homogeneous iterable data, use `list[Type]`.
    - For homogeneous unique data, use `set[Type]`.
    - For homogeneous key-value mapping, use `dict[KeyType, ValueType]`.
3. **Handle Heterogeneous Mappings**: If you are dealing with a dictionary containing varied types (like parsing a configuration file), define a `TypedDict` detailing the exact keys and value types.
4. **Abstract Complex Signatures**: Review the collection's type annotation. If it is unintuitive, declare a Type Alias at the module level.
5. **Architect Custom Collections**:
    - *Scenario A (Tweaking Behavior)*: Subclass `collections.UserDict`, `UserList`, or `UserString`. Override the necessary methods, ensuring you mutate/read `self.data`.
    - *Scenario B (Emulating Behavior)*: Subclass from `collections.abc` (e.g., `collections.abc.Set`). Implement the required underlying magic methods.
    - *Scenario C (Generic Data Structure)*: Define a `TypeVar` (e.g., `T = TypeVar("T")`) and subclass `Generic[T]`.
6. **Refine Function Signatures**: Update function parameters that accept collections to use `collections.abc.Iterable` or `collections.abc.Mapping` to decouple the function from concrete implementations.

@Examples (Do's and Don'ts)

**Principle: Annotating Inner Types and Using Aliases**
- [DO]
```python
AuthorToCountMapping = dict[str, int]

def create_author_count_mapping(cookbooks: list[Cookbook]) -> AuthorToCountMapping:
    # Implementation
```
- [DON'T]
```python
# Fails to communicate inner types or domain context
def create_author_count_mapping(cookbooks: list) -> dict:
    # Implementation
```

**Principle: Handling Heterogeneous Dictionaries**
- [DO]
```python
from typing import TypedDict

class NutritionInformation(TypedDict):
    calories: int
    fat_grams: float
    is_vegan: bool

def get_nutrition_info() -> NutritionInformation:
    # Implementation
```
- [DON'T]
```python
# Forces user to guess keys and handles types poorly
def get_nutrition_info() -> dict[str, Union[int, float, bool]]:
    # Implementation
```

**Principle: Extending Existing Collections**
- [DO]
```python
from collections import UserDict

class AliasedDictionary(UserDict):
    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            # Safely handle custom fallback behavior
            pass
```
- [DON'T]
```python
# Surprising behavior: dict.get() will NOT call this overridden __getitem__
class AliasedDictionary(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            pass
```

**Principle: Duck Typing via Abstract Base Classes**
- [DO]
```python
import collections.abc

def print_items(items: collections.abc.Iterable):
    for item in items:
        print(item)
```
- [DON'T]
```python
# Unnecessarily restricts the function to ONLY lists, rejecting sets or tuples
def print_items(items: list):
    for item in items:
        print(item)
```

**Principle: Generic Custom Collections**
- [DO]
```python
from typing import Generic, TypeVar

Node = TypeVar("Node")
Edge = TypeVar("Edge")

class Graph(Generic[Node, Edge]):
    def __init__(self):
        self.edges: dict[Node, list[Edge]] = {}
```
- [DON'T]
```python
# Forces use of 'Any', destroying type checker safety nets
class Graph:
    def __init__(self):
        self.edges: dict[Any, list[Any]] = {}
```