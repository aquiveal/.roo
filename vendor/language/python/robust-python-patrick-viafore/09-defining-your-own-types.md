# @Domain

These rules apply when the AI is tasked with defining data structures, modeling domain concepts, creating classes, structuring configuration data, refactoring primitive collections (like dictionaries or tuples) into robust types, or establishing data validation boundaries in Python.

# @Vocabulary

- **User-Defined Type**: A custom type created by the developer to represent specific domain concepts and behaviors, enhancing readability over basic types like dictionaries or tuples.
- **Enumeration (Enum)**: A construct representing a restricted, static set of choices or values.
- **Base Enum Class**: An enumeration meant to be subtyped, typically not including any values directly, but often defining methods like `_generate_next_value_`.
- **Flag**: A specialized enumeration that supports bitwise operations (e.g., OR `|`, AND `&`) for combining non-overlapping values.
- **IntEnum / IntFlag**: Enumerations that allow implicit degradation/conversion to raw integers.
- **Data Class**: A user-defined type used for grouping related, heterogeneous data fields together without explicitly requiring a constructor.
- **Composite Type**: A type made up of multiple values that represent a logical grouping or relationship.
- **Invariant**: A property or rule of an entity that must remain unchanged and true throughout the entire lifetime of that entity.
- **Factory Method**: A function used to evaluate invariants and instantiate a class, often returning an `Optional` type rather than throwing exceptions upon failure.
- **Encapsulation**: The practice of hiding properties and actions of an entity, controlling how external code accesses or changes data.
- **Public / Protected / Private**: Access control levels. In Python, protected is denoted by a single underscore prefix (`_`), and private by a double underscore prefix (`__`), which triggers name mangling.
- **Accessor**: A method used for retrieving information (often related to invariants).
- **Mutator**: A method that alters the state of an object while preserving invariants.
- **Free Function**: A function that lives at the module scope outside of a class.

# @Objectives

- Replace primitive data structures (tuples, untyped dictionaries) with domain-specific user-defined types to reduce cognitive burden and clarify intent.
- Ensure illegal states are unrepresentable by strictly enforcing data restrictions through the type system.
- Choose the correct level of abstraction (Enum, Data Class, Class, or Dictionary) based on the presence of invariants and the nature of the data.
- Protect the internal state of objects to guarantee invariants remain true for the lifetime of an instance.

# @Guidelines

## Choosing the Right Abstraction
- Use **Dictionaries** only for dynamic key-value mappings that change at runtime or as intermediate data (e.g., parsing JSON). For heterogeneous data, prefer `TypedDict` if no behaviors are attached, but default to a Data Class.
- Use **Enumerations (Enums)** to represent a single value chosen from a static collection of values.
- Use **Data Classes** for bundles of heterogeneous data that are mostly independent, where users are free to get and set individual attributes. Avoid `namedtuple` unless strictly requiring Python 3.6 compatibility.
- Use **Classes** when fields are interdependent, or there are strict invariants to preserve.

## Enumerations (Enums)
- **DO NOT** use Enums when the options are determined or changed at runtime.
- Use `auto()` when the specific underlying value of the enumeration is irrelevant and should not be relied upon by developers.
- Implement `_generate_next_value_` in a Base Enum Class if you need to control the sequence/format of `auto()` values (e.g., capitalizing names).
- Use `Flag` when you need a grouping of unique values that support bitwise operations. Ensure underlying values do not overlap (e.g., powers of 2).
- **CRITICAL**: Avoid `IntEnum` and `IntFlag` unless absolutely necessary for legacy systems or hardware interoperability. They allow implicit integer conversion which breaks type safety and hides intent.
- Apply the `@unique` decorator from the `enum` module when you must guarantee that no two Enum members share the same underlying value (preventing accidental aliases).

## Data Classes
- Embed specific behaviors (methods) directly inside the data class to improve reusability if the operation is directly tied to the data.
- Set `eq=True` in the `@dataclass` decorator if you need to perform equality checks between instances.
- Set `order=True` (and `eq=True`) to enable relational comparisons (`<`, `>`, `<=`, `>=`).
- **CRITICAL**: If you manually override comparison functions (`__lt__`, `__le__`, `__gt__`, `__ge__`), you MUST NOT set `order=True`, or Python will raise a `ValueError`.
- Use `frozen=True` to indicate and enforce that the data class should not be changed after instantiation (making it hashable and safe for use as dictionary keys or in sets).
- **WARNING**: Remember that `frozen=True` only prevents reassignment of the class fields. If a field contains a mutable type (like a `list` or `set`), it can still be mutated. Use immutable members (e.g., `tuple`, `frozenset`) inside frozen data classes to guarantee deep immutability.

## Classes and Invariants
- Enforce all invariants inside the constructor (`__init__`). Never construct a class if the invariants would be broken.
- If an invariant is violated during construction, either:
  1. Throw an exception (`ValueError`, `AssertionError`) to prevent instantiation.
  2. Massage the data to conform to the invariant (e.g., re-ordering items silently).
- If exceptions during initialization are undesirable, use a Factory Method. Prefix the class name with `_` to hide it, and provide a public factory function that checks invariants and returns an `Optional[Type]`.
- Define one class per set of related invariants (Single Responsibility Principle).

## Encapsulation
- Mark attributes that should not be manipulated externally as protected (`_`) or private (`__`).
- **CRITICAL**: Do not write getters and setters for *every* private member. If a class consists solely of getters and setters, convert it to a Data Class.
- When returning private, mutable attributes from an accessor (getter), return a copy (e.g., `deepcopy(self.__data)`) rather than a reference, preventing callers from inadvertently breaking invariants.
- If a method does not concern itself with the class's invariants or members, it should not be a class method. Extract it as a Free Function at the module level.
- Avoid `@staticmethod` and `@classmethod`. Prefer module-level free functions instead, unless strictly necessary for metaprogramming or specific alternative constructors.

# @Workflow

When prompted to define or refactor types, follow this exact evaluation process:

1. **Analyze Data Constraints**: Identify if the data represents a restricted set of choices (Enum), independent grouped data (Data Class), or interdependent data requiring invariants (Class).
2. **Implement Enumerations**:
   - If a static set of choices, import `Enum`.
   - Assign values explicitly or use `auto()`.
   - If bitwise combinations are needed, use `Flag`.
3. **Implement Data Classes**:
   - Apply `@dataclass`.
   - Explicitly type-hint every field.
   - Determine if `frozen=True`, `eq=True`, or `order=True` is required.
   - If `frozen=True`, ensure all field types are deeply immutable (e.g., `tuple` instead of `list`).
4. **Implement Standard Classes**:
   - Define the `__init__` method.
   - Add invariant validation logic (assertions or exception raising) before assigning state.
   - Assign state to private (`__`) or protected (`_`) variables to encapsulate them.
5. **Implement Accessors/Mutators**:
   - Add mutator methods that explicitly re-verify invariants before modifying internal state.
   - Add accessor methods that return copies of mutable internal data.
6. **Extract Free Functions**: Review all class methods. If a method does not act on internal state or invariants, extract it to the module level.

# @Examples (Do's and Don'ts)

## Enumerations

**[DO]** Use standard `Enum` to enforce restricted choices.
```python
from enum import Enum, auto, unique

@unique
class MotherSauce(Enum):
    BECHAMEL = auto()
    VELOUTE = auto()
    ESPAGNOLE = auto()
    TOMATO = auto()
    HOLLANDAISE = auto()

def create_daughter_sauce(mother_sauce: MotherSauce, extra_ingredients: list[str]):
    pass
```

**[DON'T]** Use `IntEnum` for convenience or raw tuples for restricted sets, as it breaks type safety and hides intent.
```python
# ANTI-PATTERN: IntEnum allows arbitrary integer comparison, hiding bugs.
from enum import IntEnum

class Kitchenware(IntEnum):
    PLATE = 7
    CUP = 8

# A user can do `if Kitchenware.CUP == ImperialLiquidMeasure.CUP`, causing subtle bugs.

# ANTI-PATTERN: Static indexing of raw tuples hides intent.
MOTHER_SAUCES = ("Béchamel", "Velouté", "Espagnole", "Tomato", "Hollandaise")
create_daughter_sauce(MOTHER_SAUCES[2], ["Onions"])
```

## Data Classes

**[DO]** Use frozen data classes with immutable members to guarantee object stability.
```python
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Ingredient:
    name: str
    amount: float
    units: str

@dataclass(frozen=True)
class Recipe:
    name: str
    ingredients: Tuple[Ingredient, ...] # Tuple ensures deep immutability
```

**[DON'T]** Use `frozen=True` while leaving mutable fields, or use dictionaries/namedtuples when behaviors or constraints are needed.
```python
# ANTI-PATTERN: Frozen dataclass with a mutable list field.
@dataclass(frozen=True)
class Recipe:
    name: str
    ingredients: list[str] # A user can still do recipe.ingredients.append("Poison")

# ANTI-PATTERN: Using a dictionary for complex, domain-specific heterogeneous data.
food_lab = {"name": "The Food Lab", "page_count": 958}
```

## Classes and Invariants

**[DO]** Validate invariants in `__init__`, use private members, and return copies in accessors.
```python
from copy import deepcopy

class PizzaSpecification:
    """
    Pizza spec. Dough must be between 6 and 12 inches.
    Only one sauce is allowed, always placed first.
    """
    def __init__(self, dough_radius_in_inches: int, toppings: list[str]):
        if not (6 <= dough_radius_in_inches <= 12):
            raise ValueError("Dough must be between 6 and 12 inches")
        
        sauces = [t for t in toppings if self._is_sauce(t)]
        if len(sauces) > 1:
            raise ValueError("Can only have at most one sauce")
            
        self.__dough_radius = dough_radius_in_inches
        # Massage data: enforce invariant that sauce is first
        self.__toppings = sauces + [t for t in toppings if not self._is_sauce(t)]

    def get_toppings(self) -> list[str]:
        # Return a copy to prevent external mutation breaking invariants
        return deepcopy(self.__toppings)

    def _is_sauce(self, topping: str) -> bool:
        return "sauce" in topping.lower()
```

**[DON'T]** Leave invariant-dependent fields public or fail to validate upon construction.
```python
# ANTI-PATTERN: Public attributes allow external code to break invariants.
class PizzaSpecification:
    def __init__(self, dough_radius_in_inches: int, toppings: list[str]):
        self.dough_radius_in_inches = dough_radius_in_inches
        self.toppings = toppings

# External code can trivially break the business rules:
# pizza.dough_radius_in_inches = 1000 
# pizza.toppings.append("Another Sauce")
```