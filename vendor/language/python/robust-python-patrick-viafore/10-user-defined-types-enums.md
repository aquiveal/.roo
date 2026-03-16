# @Domain

This rule file activates when the AI is tasked with data modeling, refactoring variables that accept a constrained set of values, defining state machines, handling configuration choices, replacing magic strings or numbers with named constants, or implementing bitwise flags/multi-select options in Python.

# @Vocabulary

- **User-Defined Type**: A custom data type created by a developer to represent a specific domain concept, replacing generic collections (like tuples or dictionaries) to improve codebase vocabulary and reasonability.
- **Enumeration (Enum)**: A Python construct (`from enum import Enum`) that represents a static, restricted set of named values. 
- **auto()**: A helper function from the `enum` module used to automatically generate values for Enum members when the exact underlying value is irrelevant.
- **_generate_next_value_**: A method that can be overridden in a base Enum class to customize how `auto()` generates values (e.g., capitalizing names).
- **Literal**: A type hint feature that restricts a variable to a specific set of raw values. Acts as a lightweight alternative to Enums for purely static type-checking.
- **Flag**: A specialized Enum base class (`from enum import Flag`) used when values represent unique attributes that can be combined using bitwise operations (`|`, `&`).
- **IntEnum / IntFlag**: Subclasses of Enum/Flag that allow degradation to raw integers for comparison. Considered an anti-pattern due to weakened type safety.
- **Aliasing**: The default Enum behavior where defining two members with the same value makes the second member an alias of the first.
- **@unique**: A decorator (`from enum import unique`) that prevents aliasing by enforcing that all members in an Enum have distinct underlying values.

# @Objectives

- Replace generic, primitive data types (strings, integers, tuples) with explicit, domain-specific types to communicate clear intent to future maintainers.
- Prevent the creation of invalid or unexpected states by restricting variable assignments to predefined Enum members.
- Enhance type safety and static analysis by utilizing Enums in function signatures and type hints.
- Eliminate "magic strings" and "magic numbers" that require external context or documentation to understand.
- Implement extensible and safe multi-select options using `Flag` and bitwise operations instead of collections of strings or integers.

# @Guidelines

## General Domain Modeling
- When encountering domain concepts represented by generic collections (e.g., a tuple representing a Restaurant), the AI MUST refactor the code to use a User-Defined Type.
- When a variable requires a selection from a static, pre-defined list of choices, the AI MUST use an `Enum` instead of a raw string, integer, or tuple index.

## Enum Implementation
- The AI MUST define enumerations by inheriting from `enum.Enum`.
- The AI MUST use UPPER_CASE naming conventions for Enum members to denote constant/immutable values.
- The AI MUST use the Enum class name as the type hint for any function parameters or return types that expect one of the Enum values.
- When iterating over options is required, the AI MUST iterate directly over the Enum class rather than maintaining a separate list of valid strings.

## Values and auto()
- When the underlying value of an Enum member is not strictly required by external systems, the AI MUST assign the value using `enum.auto()`.
- If custom logic is needed for `auto()` (e.g., generating string names instead of integers), the AI MUST implement the `_generate_next_value_` method in an abstract base Enum class, rather than directly in the populated Enum.

## Literal vs. Enum
- The AI MUST use `typing.Literal` when the only requirement is simple static type-checking restrictions.
- The AI MUST upgrade a `Literal` to an `Enum` if the code requires any of the following: iterating over the possible values, runtime validation, or mapping an explicit name to a different underlying value.

## Flag Enumerations
- When representing a grouping of unique, combinable values (e.g., multiple selections, bitmasks), the AI MUST inherit from `enum.Flag`.
- When using `Flag`, the AI MUST use `auto()` to ensure values are automatically assigned as non-overlapping powers of 2.
- The AI MAY define aliases within a `Flag` class to represent common combinations of flags (e.g., `ALL_OPTIONS = Option.A | Option.B`).

## Uniqueness and Aliasing
- If an Enum must strictly forbid duplicate values, the AI MUST apply the `@unique` decorator from the `enum` module to the class.
- The AI MUST rely on the default aliasing behavior (allowing duplicate values) only when explicitly attempting to support legacy naming or internationalization (e.g., `BECHAMEL = 1` and `BÉCHAMEL = 1`).

## Anti-Patterns and Constraints
- The AI MUST NOT use an `Enum` for options that are determined, generated, or modified at runtime. For dynamic mappings, the AI MUST use a `dict`.
- The AI MUST NOT use `IntEnum` or `IntFlag` unless there is a strict, documented requirement for legacy system interoperability or hardware APIs. Implicit conversion to integers hides intent and creates subtle, dangerous bugs if values change.

# @Workflow

When evaluating a variable, parameter, or return type that represents a set of choices, the AI MUST follow this algorithmic process:

1. **Evaluate Dynamism**: Determine if the set of choices can change during runtime.
   - If YES: Use a `dict` or database lookup. Do not use an Enum.
   - If NO: Proceed to step 2.
2. **Evaluate Complexity**: Determine the required capabilities of the type.
   - If the code ONLY needs static type hints (no runtime iteration, no custom values): Use `typing.Literal`.
   - If the code requires iteration, runtime safety, or distinct identity: Proceed to step 3.
3. **Evaluate Combinability**: Determine if the choices are mutually exclusive or combinable.
   - If combinable (multiple choices allowed simultaneously): Inherit from `enum.Flag` and assign members using `auto()`. Combine using bitwise operators (`|`, `&`).
   - If mutually exclusive (only one choice allowed): Inherit from `enum.Enum`.
4. **Evaluate Value Importance**: Determine if the underlying assigned values matter.
   - If values don't matter: Use `auto()`.
   - If specific values are strictly required: Assign values explicitly.
5. **Evaluate Uniqueness**: Determine if duplicate values should trigger an error.
   - If duplicate values represent a configuration error: Apply the `@unique` decorator.
6. **Apply Type Hints**: Update all relevant function signatures, variable annotations, and data classes to use the newly created Enum/Flag class as the type hint.

# @Examples (Do's and Don'ts)

## Domain Modeling for Static Choices

[DON'T] Use raw strings or integers to define static choices, leaving the function signature vulnerable to typos or invalid states.
```python
def create_sauce(mother_sauce: str, extra_ingredients: list[str]):
    if mother_sauce == "Hollandaise":
        pass
    # Vulnerable to typos like "Holandaise" or "Veloute" (missing accent)
```

[DO] Define an `Enum` to build shared vocabulary and strictly type hint the function signature.
```python
from enum import Enum, auto

class MotherSauce(Enum):
    BÉCHAMEL = auto()
    VELOUTÉ = auto()
    ESPAGNOLE = auto()
    TOMATO = auto()
    HOLLANDAISE = auto()

def create_sauce(mother_sauce: MotherSauce, extra_ingredients: list[str]):
    # Type checker enforces valid inputs; runtime throws ValueError on invalid creation
    if mother_sauce is MotherSauce.HOLLANDAISE:
        pass
```

## Representing Combinable Attributes

[DON'T] Use generic collections (like lists or sets of strings) to manage multiple Boolean attributes, which lacks strict validation.
```python
allergens: set[str] = {"Fish", "Shellfish"}

if "Fish" in allergens:
    print("Contains fish")
```

[DO] Use `enum.Flag` with `auto()` to create a safe, bitwise-combinable type.
```python
from enum import Flag, auto

class Allergen(Flag):
    FISH = auto()
    SHELLFISH = auto()
    TREE_NUTS = auto()
    # Aliases for combinations are supported
    SEAFOOD = FISH | SHELLFISH

allergens: Allergen = Allergen.FISH | Allergen.SOY

if Allergen.FISH in allergens:
    print("Contains fish")
```

## IntEnum Anti-Pattern

[DON'T] Inherit from `IntEnum` just to avoid typing `.value`, as it allows unsafe integer comparison and cross-enum comparisons.
```python
from enum import IntEnum

class Kitchenware(IntEnum):
    PLATE = 7
    CUP = 8

class LiquidMeasure(IntEnum):
    CUP = 8
    PINT = 16

# DANGEROUS: This evaluates to True and introduces silent logic bugs!
if LiquidMeasure.CUP == Kitchenware.CUP:
    pass 
```

[DO] Use a standard `Enum` to enforce strict type identity, comparing exact enum members or explicitly accessing `.value` only when necessary.
```python
from enum import Enum

class Kitchenware(Enum):
    PLATE = 7
    CUP = 8

class LiquidMeasure(Enum):
    CUP = 8
    PINT = 16

# SAFE: This correctly evaluates to False. Type safety is maintained.
if LiquidMeasure.CUP is Kitchenware.CUP:
    pass 
```

## Enum vs. Literal

[DON'T] Use a heavyweight Enum if you only need a simple, static constraint and never iterate over or validate it at runtime.
```python
from enum import Enum

class Status(Enum):
    OPEN = "open"
    CLOSED = "closed"

# Overkill if we only ever pass strings statically
def set_status(status: Status): ...
```

[DO] Use `Literal` for simple, lightweight static constraints.
```python
from typing import Literal

def set_status(status: Literal["open", "closed"]): ...
```

[DO] Upgrade to `Enum` if runtime validation or iteration is required.
```python
from enum import Enum, auto

class Status(Enum):
    OPEN = auto()
    CLOSED = auto()

# Allows printing all options in a CLI/UI
for status in Status:
    print(f"Valid option: {status.name}")
```

## Forcing Uniqueness

[DON'T] Allow duplicate values if they represent a developer error in a configuration Enum.
```python
from enum import Enum

class WorkerRole(Enum):
    CHEF = 1
    SOUS_CHEF = 2
    SERVER = 1 # Silent bug: SERVER becomes an alias of CHEF
```

[DO] Use `@unique` to fail fast when accidental duplicates are introduced.
```python
from enum import Enum, unique

@unique
class WorkerRole(Enum):
    CHEF = 1
    SOUS_CHEF = 2
    SERVER = 1 # Throws ValueError at module load time
```