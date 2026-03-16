# @Domain
These rules apply whenever the AI is tasked with architectural design, refactoring, dependency management, package resolution, module import structuring, system design, or writing code that interacts with internal or external libraries in a Python codebase.

# @Vocabulary
- **Dependency**: A relationship where one piece of code requires another piece of code to behave in a specific way.
- **Spaghetti Code**: A tangled, unmanageable mess of dependencies where everything is highly coupled.
- **Coupling**: The degree to which different parts of the codebase are tied together.
- **Pinning**: Freezing dependencies at a specific version or commit to prevent unexpected breakages.
- **Physical Dependency**: A static relationship observed directly in code (e.g., function calls, type compositions, imports, inheritance).
- **Dependency Inversion**: Reversing the direction of a dependency so that the core/stable system dictates the contract, rather than depending on the external/volatile system.
- **Logical Dependency**: A relationship with no direct physical linkage in code, occurring via abstraction, indirection, or runtime evaluation (e.g., HTTP communication, duck typing).
- **Substitutability**: The ability to replace a component easily because nothing physically depends on its concrete implementation, only its logical contract.
- **Temporal Dependency**: A relationship linked by time, where execution must occur in a strict, specific order.
- **Fan-in**: The amount of code/modules that depend on a specific entity. High fan-in entities sit at the bottom of the dependency graph.
- **Fan-out**: The number of external entities a specific piece of code depends upon. High fan-out entities sit at the top of the dependency graph.
- **DRY (Don't Repeat Yourself) Limit**: The principle that code should only be deduplicated if it shares the exact same *reason to change*, not just because it looks structurally similar.

# @Objectives
- Actively manage and minimize dependencies to prevent spaghetti code and tight coupling.
- Ensure high fan-in components are highly stable and have low fan-out.
- Mitigate the risks of temporal dependencies by enforcing execution order through the type system or strict precondition checks.
- Prevent accidental complexity caused by over-applying the DRY principle to unrelated business rules.
- Transform implicit logical dependencies into explicit contracts.
- Utilize automated dependency visualization tools when diagnosing complex architectures.

# @Guidelines
- **Dependency Pinning & Updates**: The AI MUST pin external package dependencies to ensure reproducibility. When managing dependencies, the AI MUST NOT allow unpinned dependencies to depend on pinned ones. The AI MUST recommend using continuous integration and dependency managers (like `poetry`) to continually update, test, and check in new pins.
- **Physical Dependency Directionality**: The AI MUST evaluate the direction of physical dependencies. If a volatile system (e.g., payment processing) dictates the state of a stable core system (e.g., order fulfillment), the AI MUST use Dependency Inversion so the stable system defines the contract and the volatile system queries it.
- **Avoiding Circular Dependencies**: The AI MUST actively prevent circular physical dependencies (A imports B, B imports A) by extracting shared interfaces or moving the shared logic to a lower-level module.
- **The DRY Principle Limit**: The AI MUST NOT deduplicate code solely because it is structurally identical. Before refactoring duplicate code into a shared function, the AI MUST verify that both calling sites have the *exact same reason to change*. If they belong to different business domains, the code MUST remain duplicated.
- **Managing Logical Dependencies**: When writing code that relies on logical dependencies (e.g., HTTP calls, duck typing, implicit list ordering), the AI MUST make the implicit contract explicit. If code relies on a specific collection order, the AI MUST write an explicit mapping function or add explicit documentation/types rather than relying on hidden runtime assumptions.
- **Enforcing Temporal Dependencies**: The AI MUST NOT rely on developers remembering to call functions in a specific order (e.g., `configure()` before `execute()`). The AI MUST enforce temporal dependencies by:
  1.  **Using the Type System**: Creating a specific type (e.g., `ConfiguredSystem`) that is only returned by step A, and requiring that type as a parameter for step B.
  2.  **Embedding Preconditions**: Moving the initialization/check directly inside the execution function, throwing explicit exceptions if conditions are not met.
- **Fan-in and Fan-out Organization**: The AI MUST design architectures where code with high fan-in (many dependents) has low fan-out (depends on very little). High fan-in code MUST be exceptionally stable. Business logic MUST have high fan-out and low fan-in.
- **Visualizing Dependencies**: When the AI is tasked with analyzing or untangling complex dependencies, it MUST suggest or utilize the following visualization tools:
  - `pipdeptree` and `GraphViz` for package dependencies.
  - `pydeps` for module-level import graphs.
  - `pyan3` for static function call graphs.
  - `cProfile` and `gprof2dot` for dynamic, runtime call graphs.

# @Workflow
When adding a new feature, importing a module, or refactoring existing architecture, the AI MUST strictly follow this algorithm:
1.  **Dependency Categorization**: Identify all new relationships required by the task. Categorize each as Physical, Logical, or Temporal.
2.  **Physical Dependency Check**:
    - Calculate the conceptual Fan-in and Fan-out of the modified module.
    - If the module has high Fan-in, verify that the new dependency does not introduce volatility.
    - If a circular dependency is detected, immediately halt and apply Dependency Inversion.
3.  **Logical Dependency Check**:
    - If relying on an external service, dynamic configuration, or implicit data structure order, define an explicit type or mapping function to handle it. Do not pass raw, undocumented data structures.
4.  **Temporal Dependency Check**:
    - If Step B requires Step A to happen first, modify the function signature of Step B to require a strict type that can ONLY be instantiated by the successful completion of Step A.
5.  **DRY Evaluation**:
    - If refactoring duplicated code, evaluate the *business reason* for the code. If the reasons differ, abandon the deduplication effort to prevent tight coupling of unrelated domains.
6.  **Implementation & Pinning**:
    - Write the code. If introducing a new external library, pin the version explicitly.

# @Examples (Do's and Don'ts)

### Temporal Dependencies
**[DO]** Enforce execution order using the type system.
```python
from typing import NewType

ConfiguredMachine = NewType("ConfiguredMachine", Machine)

def configure_machine(machine: Machine) -> ConfiguredMachine:
    machine.setup()
    return ConfiguredMachine(machine)

# The type system statically enforces that the machine MUST be configured first
def mass_produce(machine: ConfiguredMachine, amount: int):
    machine.execute(amount)
```

**[DON'T]** Rely on the caller to remember the correct order of operations.
```python
def configure_machine(machine: Machine):
    machine.setup()

def mass_produce(machine: Machine, amount: int):
    # DANGER: Temporal dependency. If caller forgets configure_machine(), this fails or corrupts data.
    machine.execute(amount)
```

### The DRY Principle Limit
**[DO]** Allow structural duplication if the business reasons to change are entirely unrelated.
```python
# Domain A: Employee Onboarding
def generate_employee_id(first_name: str, last_name: str) -> str:
    return f"{first_name[:3].lower()}_{last_name[:3].lower()}"

# Domain B: Product SKU Generation
# This looks identical to employee ID generation, but products and employees 
# change for completely different business reasons. They MUST remain separate.
def generate_product_sku(category: str, item_name: str) -> str:
    return f"{category[:3].lower()}_{item_name[:3].lower()}"
```

**[DON'T]** Create a physical dependency between unrelated domains just because the code looks the same.
```python
# DANGER: Coupling Employee logic and Product logic together.
# If HR wants to change employee IDs to 4 letters, product SKUs will break.
def generate_three_letter_prefix_id(part_one: str, part_two: str) -> str:
    return f"{part_one[:3].lower()}_{part_two[:3].lower()}"
```

### Dependency Inversion (Physical Dependencies)
**[DO]** Have the volatile system query the stable core system.
```python
# STABLE CORE
class PizzaMaker:
    def get_available_menu(self) -> list[str]:
        return ["Cheese", "Pepperoni"]

# VOLATILE EXTERNAL SYSTEM
class PaymentSystem:
    def __init__(self, pizza_maker: PizzaMaker):
        self.pizza_maker = pizza_maker

    def display_options(self):
        # Payment system reacts to the core system's state
        for item in self.pizza_maker.get_available_menu():
            print(f"Buy {item}")
```

**[DON'T]** Hardcode the state of the stable system inside the volatile system (High Coupling).
```python
# DANGER: If the pizza maker runs out of pepperoni, the payment system 
# must be independently updated, leading to shotgun surgery and logical desync.
class PaymentSystem:
    def display_options(self):
        print("Buy Cheese")
        print("Buy Pepperoni")
        print("Buy Stromboli")
```