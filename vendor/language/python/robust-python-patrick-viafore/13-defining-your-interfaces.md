# @Domain
Trigger these rules when tasked with designing, refactoring, or extending Python interfaces, APIs, public-facing classes, modules, or any boundaries where different parts of a codebase (or different developers) interact.

# @Vocabulary
- **API (Application Programming Interface)**: The set of types, related functions, and external functions a developer interacts with to use a piece of code.
- **Paradox of Code Interfaces**: The principle that you have one chance to get an interface right, but you won't know it is right until it is used, at which point it becomes too difficult to change due to dependent code.
- **Curse of Knowledge**: A cognitive bias where the creator of an interface is so intimately familiar with its inner workings that they are blinded to how confusing it might be to a new user.
- **TDD (Test-Driven Development)**: A design methodology (not just a testing methodology) used to evaluate the friction of calling code before the implementation is written.
- **RDD (README-Driven Development)**: A design methodology where top-level ideas and code interactions are distilled into a single README document *before* coding begins.
- **Usability Testing**: The process of observing prospective users interacting with an interface to identify pain points and confusing mappings.
- **Natural Mapping**: Designing controls and their behaviors to take advantage of physical analogies and cultural standards, leading to immediate understanding (per Donald Norman).
- **Magic Methods (Dunder Methods)**: Built-in Python methods prefixed and suffixed with double underscores (e.g., `__add__`) that define custom behavior for built-in operations.
- **Errors of Omission**: Bugs caused by a developer forgetting to do a required action (like cleaning up a resource).
- **Context Manager**: A Python construct utilized via the `with` block (often created using `@contextmanager`) that ensures required setup and teardown operations execute automatically, preventing errors of omission.

# @Objectives
- **Mitigate the Paradox of Code Interfaces**: Exert extreme deliberate care when designing public APIs, recognizing that they are virtually immutable once adopted.
- **Emulate the User's Mindspace**: Design interfaces from the perspective of the caller, explicitly fighting the Curse of Knowledge.
- **Make Interfaces Easy to Use Correctly**: Create intuitive, domain-aligned natural mappings utilizing Python's Magic Methods.
- **Make Interfaces Hard to Use Incorrectly**: Eliminate errors of omission and unenforced invariants using Context Managers and strict encapsulation.
- **Ensure Frictionless Usage**: Prevent broken mental models, duplicated functionality, and reduced testing caused by overly complex interfaces.

# @Guidelines

### Interface Design Methodologies
- The AI MUST design the interface *before* implementing the logic.
- When generating a new class or module, the AI MUST explicitly use TDD or RDD. Write a usage snippet, a hypothetical test, or a README block demonstrating how a user will interact with the code to verify it feels natural and frictionless.
- The AI MUST treat the following as severe red flags indicating an interface is too complicated:
  - Confusing or overly verbose function calls.
  - Long chains of dependencies required for setup.
  - Tests that must be written in a fixed, rigid order.

### Natural Mappings and Domain Alignment
- The AI MUST map interfaces directly to domain concepts (e.g., use `Order` and `GroceryList` classes rather than generic `dict` or `list` structures).
- The AI MUST define APIs that non-technical domain experts could understand when described aloud.

### Making Code Easy to Use Correctly (Magic Methods)
- The AI MUST evaluate if built-in Python operators logically map to the domain object. If they do, the AI MUST implement the corresponding Magic Methods instead of creating arbitrary method names.
- Permitted Natural Mappings via Magic Methods include:
  - Arithmetic: `__add__`, `__sub__`, `__mul__`, `__div__` (e.g., adding two `Ingredient` amounts together).
  - Implicit Booleans: `__bool__`.
  - Logical Operations: `__and__`, `__or__`.
  - Attribute Access: `__getattr__`, `__setattr__`, `__delattr__`.
  - Comparisons: `__le__`, `__lt__`, `__eq__`, `__ne__`, `__gt__`, `__ge__`.
  - String Representations: `__str__`, `__repr__`.

### Making Code Hard to Use Incorrectly (Defensive Interfaces)
- The AI MUST prevent users from invalidating state. If an object is locked/finalized, subsequent mutation attempts MUST raise a custom, descriptive exception (e.g., `OrderAlreadyFinalizedError` inheriting from `RuntimeError`).
- The AI MUST utilize defensive copying (e.g., `copy.deepcopy`) when returning internal collections from an API to prevent callers from inadvertently mutating private internal data.
- The AI MUST NOT rely on the caller to remember to clean up state, close resources, or revert flags. 

### Context Managers for Errors of Omission
- For any operation requiring a paired teardown action (e.g., locking/unlocking, reserving/unreserving, opening/closing), the AI MUST use a Context Manager.
- The AI MUST implement Context Managers using the `@contextmanager` decorator from the `contextlib` module.
- The Context Manager MUST yield the required object inside a `try` block and perform the cleanup inside a `finally` block to guarantee execution regardless of exceptions.

# @Workflow
When tasked with creating a new system, class, or API, the AI MUST follow this rigid sequence:
1. **Domain Description**: Write a plain-text explanation of the desired interactions using domain terminology (no code concepts).
2. **Draft Usage (RDD/TDD)**: Write a hypothetical code snippet or unit test showing exactly how the caller will instantiate and use the interface. Refine this until it looks perfectly natural.
3. **Type and Invariant Definition**: Define the structural classes. Hide internal state and write custom exception types for illegal state transitions.
4. **Magic Method Injection**: Review the operations. If the user needs to combine, compare, or represent objects, implement the respective dunder methods (`__add__`, `__eq__`, etc.) to provide natural mapping.
5. **Context Manager Wrapping**: Identify any multi-step processes or resource allocations that could result in an error of omission if interrupted. Wrap the initialization of these processes in a `@contextmanager` generator with a `try...yield...finally` block.

# @Examples (Do's and Don'ts)

### Interface Design (RDD/TDD)
- **[DO]** Write the ideal usage code before implementing the class logic to ensure the interface is clean:
  ```python
  # Ideal Usage drafted first:
  order = Order(recipes)
  with create_grocery_list(order, inventory) as grocery_list:
      grocery_list.reserve_items_from_stores()
      grocery_list.order_and_unreserve_items()
  ```
- **[DON'T]** Build internal methods first and force the user to figure out how to chain them together, leading to leaked state and high friction.

### Defensive Data Returns
- **[DO]** Return a deep copy of internal data to prevent accidental mutation by the caller:
  ```python
  def get_ingredients(self) -> list[Ingredient]:
      return sorted(deepcopy(self.__ingredients), key=lambda ing: ing.name)
  ```
- **[DON'T]** Return a direct reference to a private mutable collection:
  ```python
  def get_ingredients(self) -> list[Ingredient]:
      return self.__ingredients # Caller can append to this and break invariants!
  ```

### Magic Methods
- **[DO]** Implement Magic Methods to map behaviors to natural Python operators:
  ```python
  def __add__(self, rhs: "Ingredient") -> "Ingredient":
      assert (self.name, self.brand) == (rhs.name, rhs.brand)
      # Perform unit conversion and return new Ingredient
      return Ingredient(self.name, self.brand, new_amount, self.units)
  
  # Usage: target_ingredient += new_ingredient
  ```
- **[DON'T]** Force the user to call arbitrary, unnatural methods for standard operations:
  ```python
  def combine_with_other_ingredient(self, rhs: "Ingredient") -> "Ingredient":
      pass 
  
  # Usage: target_ingredient = target_ingredient.combine_with_other_ingredient(new_ingredient)
  ```

### Context Managers for Resource/State Cleanup
- **[DO]** Use `@contextmanager` and `try...finally` to ensure cleanup happens automatically, eliminating errors of omission:
  ```python
  from contextlib import contextmanager
  
  @contextmanager
  def create_grocery_list(order: Order, inventory: Inventory):
      grocery_list = _GroceryList(order, inventory)
      try:
          yield grocery_list
      finally:
          if grocery_list.has_reserved_items():
              grocery_list.unreserve_items()
  ```
- **[DON'T]** Expect the caller to remember to manually clean up or handle exceptions:
  ```python
  # Fragile: If an exception occurs, unreserve_items() is never called.
  grocery_list = GroceryList(order, inventory)
  grocery_list.reserve_items()
  # ... user logic ...
  grocery_list.unreserve_items() 
  ```