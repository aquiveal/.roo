@Domain
This rule file is triggered when the AI performs Python type hinting, designs interfaces, resolves typechecker errors related to duck typing or dynamic behavior, refactors inheritance hierarchies, or decouples dependencies between producers and consumers using structural subtyping.

@Vocabulary
- **Duck Typing**: A programming concept where the type or class of an object is less important than the methods and properties it defines.
- **Structural Subtyping**: Subtyping based on the actual structure (methods and attributes) of the object, rather than its explicit declarations. Used by Python at runtime and supported in typechecking via Protocols.
- **Nominal Subtyping**: Subtyping based on the explicit names and declared relationships of types (e.g., explicit inheritance).
- **Protocol**: A class inheriting from `typing.Protocol` that defines a set of required methods and attributes. It informs the static typechecker to use structural subtyping.
- **Composite Protocol**: A Protocol that inherits from multiple other Protocols to group a set of required behaviors into a single type hint.
- **Runtime Checkable Protocol**: A Protocol decorated with `@runtime_checkable`, allowing it to be used in `isinstance()` checks at runtime.
- **Non-data Protocol**: A Protocol that defines only methods and no variables (attributes). This is a requirement if the Protocol is to be used safely with `issubclass()`.

@Objectives
- Reconcile Python's dynamic runtime duck typing with static typecheckers (like mypy) using Protocols.
- Prevent the creation of artificial, fragile, or highly coupled class hierarchies (via deep inheritance trees or heavy mixin usage) solely for the purpose of passing type checks.
- Prevent the degradation of type safety caused by falling back to `Any` or hardcoding `Union`s when dealing with generic behaviors.
- Ensure Protocol definitions are completely decoupled from the concrete implementations that satisfy them.
- Differentiate between structural contracts (which require Protocols) and behavioral/stateful contracts (which require inheritance).

@Guidelines
- **Protocol Usage for Duck Typing**: When encountering functions that rely on an object having specific methods or attributes (duck typing), the AI MUST define a `typing.Protocol` instead of using `Any`, `Union`, or forcing inheritance.
- **Protocol Definition Format**: The AI MUST define Protocols by inheriting from `typing.Protocol`. Method bodies MUST be defined with an ellipsis (`...`) or a docstring and an ellipsis. Instance variables MUST be defined using standard type annotations without assigning default values.
- **Implicit Satisfaction**: The AI MUST NOT modify concrete classes to explicitly inherit from a Protocol. If a class structurally matches the Protocol, the typechecker will implicitly recognize it as a valid subtype.
- **Avoid Unions for Shared Behavior**: The AI MUST NOT use a `Union` of concrete classes in a type signature if the function is merely relying on a shared structural behavior. Doing so tightly couples the function to specific implementations and breaks the Open-Closed Principle.
- **Avoid Artificial Inheritance**: The AI MUST NOT create artificial base classes that raise `NotImplementedError` just to satisfy typecheckers when a structural relationship is all that is required.
- **Avoid Mixins for Pure Typechecking**: The AI MUST NOT force classes to inherit from mixins purely to satisfy a type signature if no code reuse is actually occurring.
- **Composite Protocols**: When a parameter must satisfy multiple protocols, the AI MUST define a new Composite Protocol. The new class MUST explicitly inherit from all constituent protocols AND `typing.Protocol`.
- **Runtime Checking**: If the code requires `isinstance()` checks against a protocol, the AI MUST import `runtime_checkable` from `typing` and decorate the Protocol class with `@runtime_checkable`.
- **The `issubclass()` Constraint**: The AI MUST NOT use `issubclass()` on a Protocol if that Protocol defines data attributes (variables). `issubclass()` is only safely supported for non-data protocols (protocols with only methods).
- **Protocol vs. Inheritance**: The AI MUST evaluate the required relationship. If the contract defines only structure (attributes/methods exist), the AI MUST use a Protocol. If the contract defines behaviors, state, or invariants that must be upheld and shared, the AI MUST use inheritance.
- **Modules as Protocols**: The AI MUST recognize that Python modules can satisfy Protocols. If a system requires passing a module that implements specific functions or variables, the AI MUST use a Protocol to type hint the expected module structure (noting that the `self` argument in the Protocol's method definitions will be safely ignored by the typechecker when a module is passed).

@Workflow
1. **Identify the Duck Type**: Analyze the function or consumer to determine exactly which attributes and methods it expects from an incoming object.
2. **Define the Protocol**: Create a new class inheriting from `typing.Protocol`.
3. **Declare Structure**: Add type hints for all expected attributes. Add function signatures with correct arguments and return types for all expected methods, using `...` for the body.
4. **Annotate the Consumer**: Replace generic hints (`Any`), fragile hints (`Union`), or base classes with the newly created Protocol.
5. **Clean Concrete Classes**: Remove any artificial inheritance (mixins, base classes) from concrete classes that was previously added solely to bypass the typechecker. Allow implicit structural subtyping to take over.
6. **Apply Advanced Features (If Needed)**:
    - If grouping multiple behaviors, create a Composite Protocol inheriting from the required Protocols and `typing.Protocol`.
    - If `isinstance` checks are present in the consumer, decorate the Protocol with `@runtime_checkable`.

@Examples (Do's and Don'ts)

[DO] Define and use a Protocol for structural subtyping without altering concrete classes.
```python
from typing import Protocol

class Splittable(Protocol):
    cost: float
    name: str

    def split_in_half(self) -> tuple['Splittable', 'Splittable']:
        ...

class BLTSandwich:
    def __init__(self):
        self.cost = 6.95
        self.name = 'BLT'
    
    def split_in_half(self) -> tuple['BLTSandwich', 'BLTSandwich']:
        # Implementation...
        return (BLTSandwich(), BLTSandwich())

def split_dish(dish: Splittable) -> tuple[Splittable, Splittable]:
    return dish.split_in_half()
```

[DON'T] Use `Any`, hardcoded `Union`s, or artificial Base Classes for shared behaviors.
```python
# Anti-pattern: Typechecker won't catch attribute errors
def split_dish(dish: Any) -> tuple[Any, Any]: ...

# Anti-pattern: Tightly coupled, breaks Open-Closed Principle
def split_dish(dish: Union[BLTSandwich, Chili]) -> tuple[Union[BLTSandwich, Chili], Union[BLTSandwich, Chili]]: ...

# Anti-pattern: Forces artificial inheritance purely for typing
class SplittableBase:
    def split_in_half(self):
        raise NotImplementedError

class BLTSandwich(SplittableBase): ...
```

[DO] Create Composite Protocols by explicitly inheriting from constituent protocols AND `typing.Protocol`.
```python
from typing import Protocol

class StandardLunchEntry(Splittable, Shareable, Substitutable, PickUppable, Protocol):
    pass
```

[DON'T] Forget to include `Protocol` when combining protocols.
```python
# Anti-pattern: StandardLunchEntry is NOT a protocol because it lacks the Protocol base class.
class StandardLunchEntry(Splittable, Shareable, Substitutable, PickUppable):
    pass
```

[DO] Use `@runtime_checkable` if you need to dynamically check structural subtyping at runtime.
```python
from typing import runtime_checkable, Protocol

@runtime_checkable
class Splittable(Protocol):
    cost: float
    name: str

    def split_in_half(self) -> tuple['Splittable', 'Splittable']:
        ...

def process_item(item: object):
    if isinstance(item, Splittable):
        return item.split_in_half()
```

[DON'T] Try to use `issubclass()` on a protocol that contains data variables.
```python
from typing import runtime_checkable, Protocol

@runtime_checkable
class DataProtocol(Protocol):
    my_var: int # Data variable present

# Anti-pattern: issubclass() will fail or act unpredictably with data protocols
issubclass(SomeClass, DataProtocol) 
```