@Domain
These rules MUST be triggered whenever the AI is tasked with creating, modifying, or refactoring Python data structures, user-defined types, object-oriented designs, or classes. They specifically apply when deciding how to model data and behaviors, enforcing state constraints, defining class APIs, or organizing methods versus module-level functions.

@Vocabulary
- **Invariant**: A property or truth about an entity that must remain unchanged and valid throughout the entire lifetime of that entity.
- **Encapsulation**: The mechanism of hiding internal properties and the actions that operate upon those properties to prevent callers from breaking invariants.
- **Accessor**: A method responsible for retrieving information from an object without altering its state or invariants.
- **Mutator**: A method responsible for altering the state of an object while strictly preserving all class invariants.
- **Free Function**: A function that lives at the module-level scope, outside of any class, used instead of static methods for logic that does not operate on class members.
- **Name Mangling**: Python's behavior of obfuscating attributes prefixed with two underscores (`__`) to prevent accidental external access.
- **Cohesion**: The degree to which the elements inside a class belong together; high cohesion means the class has exactly one reason to change (Single Responsibility Principle).
- **Factory Method**: A module-level function used to construct an object, often used when exceptions are not desired for invalid construction (returns an `Optional` type).

@Objectives
- The AI MUST make illegal states unrepresentable by strictly enforcing invariants at the point of object construction.
- The AI MUST deliberately select the correct data abstraction (Dictionary, Enum, Dataclass, or Class) based strictly on the presence of invariants and data relationships.
- The AI MUST design class APIs that hide internal state to prevent external developers from breaking invariants.
- The AI MUST favor module-level free functions over `@staticmethod` or `@classmethod`.

@Guidelines
- **Selecting the Appropriate Abstraction:**
  - If mapping dynamic keys to values that change at runtime, the AI MUST use a Dictionary.
  - If representing a single value from a static collection of discrete scalar values, the AI MUST use an Enumeration (`Enum`).
  - If bundling independent data fields with no interdependent constraints or invariants, the AI MUST use a `dataclass`.
  - If the data fields are interdependent and have constraints (invariants) that must be preserved, the AI MUST use a `Class`.
- **Enforcing Invariants in Constructors:**
  - The AI MUST check all invariants inside the `__init__` method.
  - If a caller attempts to construct a class with invalid data, the AI MUST either raise an exception, or massage the data to conform to the invariant.
  - The AI MUST use `assert` to catch developer mistakes (expected to always be true unless a developer breaks the contract).
  - The AI MUST use explicit exceptions (e.g., `ValueError`, custom exceptions) for user errors or external malicious input, since `assert` statements can be disabled in Python (via the `-O` flag).
  - If exceptions are undesirable, the AI MUST prefix the class with an underscore (`_Class`) and provide a module-level factory function that validates inputs and returns `Optional[_Class]`.
- **Encapsulation and Data Protection:**
  - The AI MUST use a single underscore (`_`) to denote protected attributes meant only for subclasses.
  - The AI MUST use double underscores (`__`) to denote private attributes, utilizing Python's name mangling to explicitly forbid external access and protect invariants.
  - The AI MUST NOT mindlessly generate getters and setters for every private member. If a class consists solely of getters and setters, it lacks invariants and the AI MUST convert it to a `dataclass`.
  - When returning mutable private attributes (like lists or dictionaries) from an accessor, the AI MUST return a deep copy (e.g., `copy.deepcopy()`) to prevent callers from modifying internal state.
- **Defining Operations (Methods):**
  - The AI MUST ensure every mutator method explicitly maintains the class invariants before it completes execution.
  - If a method does not interact with the class's state or invariants, the AI MUST NOT place it inside the class. It MUST be extracted as a module-level free function.
  - The AI MUST avoid using `@staticmethod` and MUST heavily scrutinize the use of `@classmethod`. Module-level free functions MUST be used instead of static methods to decouple dependencies and improve composability.
- **Communicating Invariants:**
  - The AI MUST clearly document all invariants, including those not programmatically enforceable, in the class-level docstring.
  - For unit tests concerning classes with invariants, the AI SHOULD write `@contextlib.contextmanager` functions that automatically assert invariants are preserved after operations complete.

@Workflow
1. **Analyze Data Constraints:** Evaluate the requested data structure. Identify if there are interdependent fields or rules that must remain true for the object's lifetime (invariants).
2. **Select Abstraction:** Choose `Class` only if invariants exist. Otherwise, fallback to `dataclass`, `Enum`, or `Dict`.
3. **Draft the Class Interface:** Define the `__init__` method. Write explicit validation logic (assertions for dev errors, exceptions for runtime input errors) to reject invalid states.
4. **Encapsulate State:** Assign validated data to private attributes using the `__` prefix.
5. **Implement Operations:** Write accessors that return copies of mutable state. Write mutators that perform state changes and validate invariants before returning.
6. **Extract Independent Logic:** Review all methods. If any method does not reference `self`, move it outside the class as a module-level free function.
7. **Document:** Write a comprehensive docstring at the class level detailing the exact invariants and business rules enforced by the class.

@Examples (Do's and Don'ts)

- **[DO] Use a class to enforce invariants and encapsulate state:**
```python
from copy import deepcopy

class PizzaSpecification:
    """
    Represents a Pizza Specification.
    Invariants:
    - Dough must be a whole number between 6 and 12 inches (inclusive).
    - Toppings may have at most one sauce.
    - Sauce will always be the first topping in the list, regardless of input order.
    """
    def __init__(self, dough_radius_in_inches: int, toppings: list[str]):
        if not (6 <= dough_radius_in_inches <= 12):
            raise ValueError("Dough must be between 6 and 12 inches")
            
        sauces = [t for t in toppings if self._is_sauce(t)]
        if len(sauces) > 1:
            raise ValueError("Can have at most one sauce")
            
        self.__dough_radius_in_inches = dough_radius_in_inches
        sauce = sauces[:1]
        self.__toppings = sauce + [t for t in toppings if not self._is_sauce(t)]

    def add_topping(self, topping: str) -> None:
        """Mutator that preserves the single-sauce and sauce-first invariants."""
        if self._is_sauce(topping) and any(self._is_sauce(t) for t in self.__toppings):
            raise ValueError("Pizza may only have one sauce")
            
        if self._is_sauce(topping):
            self.__toppings.insert(0, topping)
        else:
            self.__toppings.append(topping)

    def get_toppings(self) -> list[str]:
        """Accessor returning a copy of mutable state to prevent external invariant breaking."""
        return deepcopy(self.__toppings)

    def _is_sauce(self, topping: str) -> bool:
        return "sauce" in topping.lower()
```

- **[DON'T] Leave invariant data public or rely on callers to construct it correctly (using dicts or dataclasses for constrained data):**
```python
# DON'T do this: Callers can easily break invariants by modifying lists or passing bad data
from dataclasses import dataclass

@dataclass
class PizzaSpecification:
    dough_radius_in_inches: int
    toppings: list[str]

# Caller can do:
# pizza = PizzaSpecification(100, ["Tomato Sauce", "Pesto Sauce"]) # Invalid size and double sauce!
# pizza.toppings.append("Alfredo Sauce") # Broke invariant again!
```

- **[DO] Use free functions instead of static methods:**
```python
def format_pizza_receipt(pizza_spec: PizzaSpecification) -> str:
    """Free function at the module level. Does not belong in the class because it doesn't mutate state."""
    toppings_str = ", ".join(pizza_spec.get_toppings())
    return f"Pizza with {toppings_str}"

class PizzaSpecification:
    # class implementation...
```

- **[DON'T] Use `@staticmethod` as a dumping ground for logic inside a class:**
```python
class PizzaSpecification:
    # class implementation...

    @staticmethod
    def format_pizza_receipt(pizza_spec: 'PizzaSpecification') -> str:
        # DON'T do this. It creates rigid dependencies and reduces composability.
        pass
```

- **[DO] Use a factory method returning `Optional` if you want to avoid exceptions on construction:**
```python
from typing import Optional

class _PizzaSpecification:
    def __init__(self, dough_radius: int):
        self.__dough_radius = dough_radius

def create_pizza_spec(dough_radius: int) -> Optional[_PizzaSpecification]:
    """Factory method to avoid exceptions."""
    if not (6 <= dough_radius <= 12):
        return None
    return _PizzaSpecification(dough_radius)
```