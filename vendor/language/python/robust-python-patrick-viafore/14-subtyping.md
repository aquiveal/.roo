# @Domain
These rules MUST trigger whenever the AI is tasked with generating, reviewing, or refactoring Python code involving object-oriented design, class hierarchies, inheritance, mixins, interface implementation, composition, or duck typing. They specifically activate when defining relationships between types, overriding methods, or establishing base/derived classes.

# @Vocabulary
- **Subtyping**: Creating types based on other types, allowing for extension without modifying the original types. Can be achieved via inheritance, protocols, or duck typing.
- **Inheritance**: A mechanism for creating a new type (child/derived class) from another type (parent/base class) that copies all behaviors into the new type.
- **Is-A Relationship**: A strict relationship modeled by inheritance where any object of a derived class is also universally an instance of the base class.
- **Has-A Relationship**: A relationship modeled by composition where a type contains member variables of another type.
- **Substitutability**: The core requirement of subtyping; a derived class must be completely usable in every instance that requires the base class, without the calling code knowing the difference.
- **Liskov Substitution Principle (LSP)**: A behavioral notion of subtyping stating that if a subtype `S` is derived from type `T`, it must adhere to all the same properties and behaviors as `T`.
- **Invariant**: A property of an entity that remains unchanged throughout the lifetime of that entity.
- **Precondition**: A condition that must be true before interacting with a type's property or calling a function.
- **Postcondition**: A condition that must be true after interacting with a type's property or calling a function.
- **Method Resolution Ordering (MRO)**: Python's complex set of rules governing the order in which base classes are searched during multiple inheritance.
- **Mixin**: A class intended to be inherited from to provide generic functionality, containing no invariants, no data/state, and methods that are not intended to be overridden.
- **Coupling**: The degree of dependency between entities. High coupling means changes in one entity directly affect another.

# @Objectives
- Extend existing functionality seamlessly without modifying existing, tested code.
- Prevent subtle, catastrophic bugs caused by invalid assumptions in type hierarchies.
- Enforce strict substitutability (Liskov Substitution Principle) across all subtype relationships.
- Minimize coupling by favoring composition over inheritance for pure code reuse.
- Design base and derived classes with explicit, unbroken contracts regarding invariants, preconditions, and postconditions.

# @Guidelines

## General Subtyping and Inheritance
- The AI MUST restrict inheritance exclusively to true "Is-A" relationships.
- The AI MUST NOT use inheritance solely for the purpose of code reuse. If the subtype cannot be fully substituted for the supertype, the AI MUST use Composition ("Has-A" relationship) instead.
- The AI MUST treat duck typing as a formal subtype/supertype relationship and apply all substitutability rules to duck-typed objects.

## Enforcing the Liskov Substitution Principle (LSP)
- **Invariants**: The AI MUST ensure that derived classes preserve all invariants of the base class. A subtype MUST NOT alter the fundamental truths guaranteed by the supertype (e.g., a `Square` subclassing a `Rectangle` violates the invariant that height and width can be set independently).
- **Preconditions**: The AI MUST NOT define preconditions in a derived class method that are more restrictive than the base class method. (Red flag: Adding `if` statements at the beginning of an overridden method to restrict allowed arguments).
- **Postconditions**: The AI MUST NOT weaken postconditions in a derived class. (Red flag: Using early `return` statements in an overridden method that skip postcondition guarantees made by the base class).
- **Exceptions**: The AI MUST NOT throw exceptions in a derived class method that are fundamentally different from those thrown by the base class. The AI MUST NEVER throw a `NotImplementedError` (or similar) in an overridden method to indicate unsupported inherited behavior.

## Overriding Methods
- The AI MUST call `super()` in every overridden method to ensure the base class behavior is preserved and executed, UNLESS the base method is intentionally empty (e.g., an abstract method).
- If a derived class cannot safely execute the base class method via `super()`, the AI MUST dismantle the inheritance relationship and use Composition instead.

## Multiple Inheritance and Mixins
- The AI MUST NOT use multiple inheritance for stateful classes due to the cognitive burden of tracking multiple sets of invariants and complex Method Resolution Ordering (MRO).
- The AI MAY use multiple inheritance ONLY when implementing Mixins. 
- When generating Mixins, the AI MUST ensure the Mixin contains no invariants, no private/protected data state, and only independent methods.

## Base Class Design
- The AI MUST strictly document all invariants of a base class (e.g., in docstrings) so future implementers of derived classes are aware of the contract.
- The AI MUST NOT change existing invariants when modifying a base class, as it will break all downstream derived classes.
- The AI MUST NOT tie invariants to protected fields (`_field`), as derived classes are inherently meant to interact with them, risking invariant violations. The AI MUST tie invariants to private data (`__field`) and force derived classes to interact with them via protected/public methods.

# @Workflow
When tasked with creating, modifying, or evaluating a relationship between two Python types, the AI MUST execute the following algorithm:

1. **Relationship Assessment**:
   - Determine if Type B is a strict categorization of Type A ("Is-A").
   - If Type B merely needs to utilize the logic of Type A but operates differently, default to Composition. Instantiate Type A as a member variable inside Type B.
2. **Substitutability Verification (LSP Check)**:
   - If utilizing inheritance, evaluate Type B against Type A's contract.
   - Will Type B restrict input arguments more than Type A? If Yes -> FAIL. Use Composition.
   - Will Type B skip output guarantees made by Type A? If Yes -> FAIL. Use Composition.
   - Will Type B raise unexpected exception types? If Yes -> FAIL. Modify to match Type A.
3. **Implementation Generation**:
   - Define the base class. Document invariants explicitly in the class docstring. Secure invariant-related state using private attributes.
   - Define the derived class. Override methods as necessary.
   - Inject `super().method_name()` into every overridden method.
4. **Multiple Inheritance Check**:
   - If inheriting from more than one class, verify all but one are Mixins.
   - Strip all state/`__init__` methods from the Mixin classes.
5. **Review Red Flags**:
   - Scan derived methods for: conditional argument checks, early returns bypassing logic, missing `super()` calls, and `NotImplementedError` raises. Fix any found.

# @Examples (Do's and Don'ts)

## [DO] Favor Composition Over Inheritance for Code Reuse
```python
# The AI uses composition because a RestrictedMenuRestaurant cannot fully 
# substitute a Restaurant without violating postconditions/preconditions.

class Restaurant:
    def change_menu(self, menu: Menu):
        self.__menu = menu

class RestrictedMenuRestaurant:
    def __init__(self, base_restaurant: Restaurant, restricted_items: list[Ingredient]):
        # Composition: Has-A relationship
        self._restaurant = base_restaurant
        self._restricted_items = restricted_items

    def change_menu(self, menu: Menu):
        if any(not menu.contains(ingredient) for ingredient in self._restricted_items):
            raise MenuError("Missing mandatory restricted items.")
        self._restaurant.change_menu(menu)
```

## [DON'T] Violate LSP by Adding Restrictive Preconditions
```python
# ANTI-PATTERN: The subclass adds a more restrictive precondition, 
# breaking substitutability. Calling code expecting a Restaurant will break.

class RestrictedMenuRestaurant(Restaurant):
    def change_menu(self, menu: Menu):
        # RED FLAG: Conditionally checking arguments and returning early/raising exceptions
        if any(not menu.contains(ingredient) for ingredient in self.__restricted_items):
            return  # RED FLAG: Postcondition (menu is changed) is weakened/skipped!
        super().change_menu(menu)
```

## [DO] Proper Method Overriding with `super()`
```python
class FoodTruck(Restaurant):
    def __init__(self, name: str, location: Coordinates, finances: Finances):
        # The AI safely delegates to the base class constructor
        super().__init__(name, location, finances)
        self.__gps = initialize_gps()

    def move_location(self, new_location: Coordinates):
        # Add new behavior
        schedule_auto_driving_task(new_location)
        # The AI MUST call super() to preserve base class behavior
        super().move_location(new_location)
```

## [DON'T] Use Multiple Inheritance for Stateful Classes
```python
# ANTI-PATTERN: Inheriting from two complex, stateful base classes creates MRO 
# nightmares and conflicting invariants.

class FoodTruck(Restaurant, Vehicle):
    def __init__(self, name, engine_type):
        Restaurant.__init__(self, name) # RED FLAG: Manual initialization
        Vehicle.__init__(self, engine_type) # RED FLAG: Conflicting state
```

## [DO] Use Multiple Inheritance Exclusively for Mixins
```python
class ThreadingMixIn:
    # No __init__, no state, no invariants. Just independent methods.
    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)

# Safe multiple inheritance
class Server(TCPServer, ThreadingMixIn):
    pass
```

## [DON'T] Throw `NotImplementedError` to Disable Inherited Behavior
```python
# ANTI-PATTERN: If a derived class must disable a method, it is not a true subtype.

class BaconCheeseburger(SplittableDish):
    def split_in_half(self):
        # RED FLAG: Throwing an exception not present in the base class.
        # This breaks callers who expect all SplittableDish objects to split.
        raise NotImplementedError("Cannot split a bacon cheeseburger")
```