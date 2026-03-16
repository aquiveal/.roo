# @Domain
These rules MUST trigger when the AI is tasked with creating extensible Python architectures, refactoring tightly coupled systems, designing algorithms with customizable steps, injecting entire algorithms dynamically, or building/managing plug-in architectures (specifically using the `stevedore` library or `setuptools` entry points).

# @Vocabulary
- **Pluggable Code**: Software designed with extension points that allow future developers to attach new functionality (like attachments on a stand mixer) without modifying the core codebase.
- **Extension Points**: Specific parts of a system expressly designed to allow other developers to extend functionality.
- **Template Method Pattern**: A design pattern for filling in the blanks of an algorithm by defining a series of steps but forcing the caller to supply specific operations for some of those steps.
- **Strategy Pattern**: A design pattern for plugging entire algorithms into a context, allowing callers to swap out the entire behavior.
- **Plug-in**: A piece of code that can be dynamically loaded at runtime, allowing it to be developed, tested, and deployed in isolation from the core codebase.
- **Contract**: The unambiguous programmatic definition (using `typing.Protocol`) of what services the core platform expects from a plug-in.
- **stevedore**: A Python library used for managing dynamically loaded plug-ins across discrete Python packages using namespaces.
- **Entry Points**: A feature of Python packaging (`setuptools`) that allows Python to discover components and plug-ins at runtime.
- **ExtensionManager**: A `stevedore` class used to find, load, and iterate over all plug-ins registered to a specific namespace.
- **DriverManager**: A `stevedore` class used to load a specific, explicitly named plug-in for a given namespace.

# @Objectives
- Build flexible systems that allow functionality to be added without modifying existing legacy code.
- Prefer Pythonic, function-based composition (e.g., passing `Callable` types) over verbose, class-heavy Object-Oriented implementations for common design patterns.
- Decouple core systems from their extensions using formal contracts and runtime-loaded modules.
- Ensure all dynamic plug-in architectures are protected against type mismatching by validating interfaces at runtime.

# @Guidelines

## Template Method Pattern
- When implementing the Template Method Pattern, the AI MUST encapsulate the customizable steps as `typing.Callable` fields within a `@dataclass`.
- The AI MUST pass this `dataclass` into the core algorithm function, allowing the algorithm to invoke the callables at the appropriate steps.
- The AI MUST NOT implement the Template Method Pattern using the canonical Gang of Four (GoF) Object-Oriented approach (i.e., the AI MUST NOT create a base class with methods that raise `NotImplementedError` intended for subclassing).

## Strategy Pattern
- When implementing the Strategy Pattern, the AI MUST define the strategy as a single function (`typing.Callable`) passed directly into the context execution function.
- The AI MUST ensure the context function gathers necessary dependencies and delegates the core work to the passed strategy `Callable`.
- The AI MUST NOT use single-method classes and subclasses to represent strategies.

## Plug-in Architectures (`stevedore` and `setuptools`)
- When designing a system that requires independent deployment of extensions or third-party modules, the AI MUST utilize a Plug-in Architecture.
- The AI MUST define a clear Contract between the core and the plug-ins using `typing.Protocol` combined with the `@runtime_checkable` decorator.
- The AI MUST use the `@abstractmethod` decorator for methods defined within the `Protocol` to ensure clear expectations.
- The AI MUST register plug-ins using `setuptools` and `setup.py` by adding them to the `entry_points` dictionary, mapped to a designated namespace.
- When the system requires loading *all* available plug-ins for a given context, the AI MUST use `stevedore.extension.ExtensionManager(namespace=..., invoke_on_load=True)`.
- When iterating over all loaded plug-ins, the AI MUST use the `map()` method of the `ExtensionManager`.
- When the system requires loading a *specific* plug-in by name, the AI MUST use `stevedore.driver.DriverManager(namespace=..., name=..., invoke_on_load=True)`.
- **CRITICAL WARNING:** Because typecheckers cannot validate classes loaded dynamically via `stevedore`, the AI MUST perform `isinstance(plugin_instance, ExpectedProtocol)` checks at runtime to catch interface mismatches before invoking plug-in methods.

# @Workflow
When tasked with making a Python system extensible, the AI MUST follow this evaluation and implementation sequence:

1. **Identify the Scope of Extensibility**:
   - If swapping out *specific steps* within a larger algorithm, use the Template Method Pattern.
   - If swapping out an *entire* algorithm/behavior, use the Strategy Pattern.
   - If injecting entire classes, modules, or subsystems that may live in separate Python packages, use a Plug-in Architecture (`stevedore`).

2. **Implement Template Method (If Applicable)**:
   - Define a `@dataclass` holding `Callable` types for the overridable steps.
   - Write the main algorithm function to accept this dataclass and invoke its callables.

3. **Implement Strategy (If Applicable)**:
   - Define the context function to accept a single `Callable` representing the strategy.
   - Write distinct functions matching the `Callable` signature for each unique strategy.

4. **Implement Plug-in Architecture (If Applicable)**:
   - Define the contract: Create a `@runtime_checkable` `Protocol` with `@abstractmethod` definitions.
   - Implement the plug-in: Create classes that structurally satisfy the protocol.
   - Register the plug-in: Configure `setup.py` with an `entry_points` dictionary assigning the plug-in class to a namespace.
   - Load the plug-in: Instantiate `ExtensionManager` (for multiple) or `DriverManager` (for single).
   - Validate the plug-in: Execute a runtime `isinstance` check against the `Protocol`.

# @Examples (Do's and Don'ts)

## Template Method Pattern
**[DO]** Use a dataclass of callables to fill in algorithm steps.
```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class PizzaCreationFunctions:
    prepare_ingredients: Callable[[], None]
    add_pre_bake_toppings: Callable[[], None]
    add_post_bake_toppings: Callable[[], None]

def create_pizza(pizza_creation_functions: PizzaCreationFunctions):
    pizza_creation_functions.prepare_ingredients()
    roll_out_pizza_base()
    pizza_creation_functions.add_pre_bake_toppings()
    bake_pizza()
    pizza_creation_functions.add_post_bake_toppings()
```

**[DON'T]** Use the canonical GoF Object-Oriented base class pattern with `NotImplementedError`.
```python
class PizzaCreator:
    def roll_out_dough(self): ...
    def bake(self): ...
    def prepare_ingredients(self):
        raise NotImplementedError()
    def add_pre_bake_toppings(self):
        raise NotImplementedError()
    def add_post_bake_toppings(self):
        raise NotImplementedError()
```

## Strategy Pattern
**[DO]** Pass a single function as the strategy.
```python
from typing import Callable

def prepare_tex_mex_dish(tex_mex_recipe_maker: Callable[[TexMexIngredients], Dish]):
    tex_mex_ingredients = get_available_ingredients("Tex-Mex")
    dish = tex_mex_recipe_maker(tex_mex_ingredients)
    serve(dish)

def make_soft_taco(ingredients: TexMexIngredients) -> Dish:
    # Implementation here
    return dish

prepare_tex_mex_dish(make_soft_taco)
```

**[DON'T]** Force the creation of single-method classes to act as strategies.
```python
class TexMexStrategy:
    def make_dish(self, ingredients: TexMexIngredients) -> Dish:
        raise NotImplementedError()

class SoftTacoStrategy(TexMexStrategy):
    def make_dish(self, ingredients: TexMexIngredients) -> Dish:
        return dish
```

## Defining a Plug-in Contract
**[DO]** Use a runtime-checkable Protocol for the contract.
```python
from abc import abstractmethod
from typing import runtime_checkable, Protocol

@runtime_checkable
class UltimateKitchenAssistantModule(Protocol):
    ingredients: list[Ingredient]

    @abstractmethod
    def get_recipes(self) -> list[Recipe]:
        raise NotImplementedError

    @abstractmethod
    def prepare_dish(self, inventory: dict[Ingredient, Amount], recipe: Recipe) -> Dish:
        raise NotImplementedError
```

**[DON'T]** Rely on implicit duck typing across package boundaries without a formal, checkable contract.
```python
# Missing Protocol and runtime_checkable definitions
class UltimateKitchenAssistantModule:
    pass
```

## Registering Plug-ins (`setup.py`)
**[DO]** Map the plug-in implementation to a namespace via `entry_points`.
```python
from setuptools import setup

setup(
    name='ultimate_kitchen_assistant',
    version='1.0',
    entry_points={
        'ultimate_kitchen_assistant.recipe_maker': [
            'pasta_maker = ultimate_kitchen_assistant.pasta_maker:PastaModule',
            'tex_mex = ultimate_kitchen_assistant.tex_mex:TexMexModule'
        ],
    },
)
```

## Loading Plug-ins Dynamically (`stevedore`)
**[DO]** Use `DriverManager` for single plug-ins or `ExtensionManager` for all plug-ins, and apply runtime type verification.
```python
import itertools
from stevedore import extension, driver

def get_all_recipes() -> list[Recipe]:
    mgr = extension.ExtensionManager(
        namespace='ultimate_kitchen_assistant.recipe_maker',
        invoke_on_load=True,
    )
    def get_recipes(ext):
        # Runtime verification
        if not isinstance(ext.obj, UltimateKitchenAssistantModule):
            raise TypeError("Invalid plug-in loaded.")
        return ext.obj.get_recipes()
    
    return list(itertools.chain.from_iterable(mgr.map(get_recipes)))

def make_dish(recipe: Recipe, module_name: str) -> Dish:
    mgr = driver.DriverManager(
        namespace='ultimate_kitchen_assistant.recipe_maker',
        name=module_name,
        invoke_on_load=True,
    )
    if not isinstance(mgr.driver, UltimateKitchenAssistantModule):
        raise TypeError("Invalid plug-in loaded.")
    return mgr.driver.prepare_dish(get_inventory(), recipe)
```

**[DON'T]** Trust dynamically loaded classes without verifying them against the Protocol, as static typecheckers cannot validate dynamic entry points.