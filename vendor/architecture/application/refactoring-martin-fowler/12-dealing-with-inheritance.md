# @Domain
Trigger these rules when creating, modifying, or reviewing object-oriented class hierarchies, managing inheritance structures, dealing with type-code-based conditional logic, or resolving tight coupling between parent and child classes. 

# @Vocabulary
*   **Inheritance**: A mechanism to express that objects vary by category, placing common data/behavior in a superclass and variations in subclasses.
*   **Type Code**: A primitive value (enum, symbol, string, or number) used to classify different kinds of a similar thing (e.g., employee job type, order priority).
*   **Delegate**: An external object referenced by a host object, used to handle specific behaviors via composition rather than inheritance.
*   **Forwarding Function**: A method whose sole purpose is to call a corresponding method on a delegate object.
*   **Factory Function**: A function that encapsulates the instantiation of objects, often used to return different subclasses based on input parameters.
*   **Direct Inheritance**: Subclassing the primary entity directly (e.g., `Engineer` extends `Employee`).
*   **Indirect Inheritance**: Subclassing a property of the primary entity (e.g., `Engineer` extends `EmployeeType`) to allow the primary entity's type to mutate.
*   **Subclass Responsibility Error**: A placeholder error thrown in a superclass method to indicate that subclasses must implement the method (similar to an abstract method in dynamic languages).
*   **Type-Instance Homonym**: A modeling error where a class representing a category or type is wrongly used as a superclass for a physical instance (e.g., a car model used as a superclass for a specific physical car).

# @Objectives
*   Ensure class hierarchies cleanly separate common behavior (in superclasses) from variant behavior (in subclasses).
*   Eliminate duplicated code across sibling subclasses by meticulously pulling up methods and fields.
*   Prevent mis-inheritance by replacing inheritance with delegation when a subclass does not strictly fulfill the superclass contract.
*   Replace complex conditional logic based on type codes with robust polymorphic subclass hierarchies.
*   Maintain the flexibility to pivot between inheritance and delegation (composition) as the system's axes of variation evolve.

# @Guidelines

## Managing Class Hierarchies
*   **Pull Up Method**: When you encounter duplicate methods in subclasses that have identical bodies, you MUST extract them to the superclass.
    *   *Constraint*: Check that all method calls and field references inside the body can be called from the superclass.
    *   *Constraint*: If signatures differ, use `Change Function Declaration` first to unify them.
    *   *Constraint*: If a pulled-up method relies on a property defined only in subclasses, define a trap method (throwing a `Subclass Responsibility Error`) in the superclass.
*   **Pull Up Field**: When subclasses duplicate fields used in similar ways, you MUST move the field to the superclass to reduce data duplication and enable pulling up associated behavior.
*   **Pull Up Constructor Body**: When subclasses share common initialization logic, you MUST slide these statements to immediately follow the `super()` call and then pull them up into the superclass constructor. If code cannot move to the start, extract it to a method and pull up the method.
*   **Push Down Method/Field**: When a method or field is only relevant to one or a small subset of subclasses, you MUST push it down from the superclass to the specific subclasses.

## Managing Type Codes
*   **Replace Type Code with Subclasses**: When you encounter a type code that dictates conditional logic or determines the validity of specific fields, you MUST replace the type code with a subclass hierarchy.
    *   *Constraint*: If the type must mutate over the object's lifecycle, or if the class is already subclassed for another reason, you MUST use Indirect Inheritance (extract the type code to its own object and subclass that object).
    *   *Constraint*: Always use `Replace Constructor with Factory Function` to encapsulate the selection logic of which subclass to instantiate.
*   **Remove Subclass**: When a subclass does too little (e.g., it exists merely to return a specific type code or overrides a single minor method without adding distinct value), you MUST replace it with a field on the superclass and update the factory function to set this field.

## Refactoring Inheritance vs. Delegation
*   **Collapse Hierarchy**: When a class and its parent are no longer significantly different, you MUST merge them into a single class, choosing the name that best represents the future intent.
*   **Extract Superclass**: When two independent classes share similar data and behavior, you MUST create an empty superclass, inherit from it, and sequentially pull up fields and methods.
*   **Replace Subclass with Delegate**: When a class requires multiple axes of variation (which inheritance cannot support), or when inheritance introduces overly tight coupling between teams/modules, you MUST replace the subclass with a delegate object.
    *   *Implementation*: Create a delegate class, initialize it via the host's factory/constructor, move subclass methods to the delegate, and add dispatch logic to the host.
*   **Replace Superclass with Delegate**: When a subclass does not need all the methods of its superclass, or violates the type-instance homonym rule, you MUST remove the inheritance link.
    *   *Implementation*: Create a field in the subclass referencing the former superclass, initialize it, create explicit forwarding functions for only the methods that are actually needed, and break the `extends` relationship.

# @Workflow
1.  **Analyze the Hierarchy / Conditionals**: Identify the target of the refactoring (duplicate code in subclasses, type-code switch statements, or inappropriate inheritance).
2.  **Encapsulate**: If dealing with instantiation or type codes, self-encapsulate variables and wrap constructors in Factory Functions to isolate the creation logic.
3.  **Iterative Movement**: 
    *   When moving *up* (Pull Up): Move fields first, unify signatures, then move methods. Handle constructors last, ensuring `super()` rules are respected.
    *   When moving *down* (Push Down): Copy the feature to all target subclasses, then remove it from the parent.
4.  **Transition to Delegation (If required)**:
    *   Create the delegate class.
    *   Add a back-reference to the host if necessary.
    *   Move functions one by one from the subclass/superclass to the delegate, leaving behind forwarding methods.
    *   Sever the `extends` keyword inheritance link.
5.  **Clean Up**: Apply `Remove Dead Code` to empty subclasses or obsolete type code accessors. Check for `Subclass Responsibility Errors` to ensure strict contracts.

# @Examples (Do's and Don'ts)

## Replace Type Code with Subclasses
**[DO]** Use a factory function and polymorphism to handle variations.
```javascript
class Employee {
  constructor(name) {
    this._name = name;
  }
}
class Engineer extends Employee {
  get type() { return "engineer"; }
}
class Manager extends Employee {
  get type() { return "manager"; }
}
function createEmployee(name, type) {
  switch (type) {
    case "engineer": return new Engineer(name);
    case "manager": return new Manager(name);
    default: return new Employee(name);
  }
}
```
**[DON'T]** Use hard-coded switch statements based on a raw type code property.
```javascript
class Employee {
  constructor(name, type) {
    this._name = name;
    this._type = type;
  }
  // Anti-pattern: Conditional logic bound to a type code string
  calculateBonus() {
    switch(this._type) {
      case "engineer": return 500;
      case "manager": return 1000;
      default: return 0;
    }
  }
}
```

## Replace Superclass with Delegate
**[DO]** Use composition when an object only needs a subset of another object's features or isn't a true structural subtype.
```javascript
class Scroll {
  constructor(id, title, tags, dateLastCleaned) {
    this._id = id;
    // Delegate to CatalogItem instead of inheriting from it
    this._catalogItem = new CatalogItem(id, title, tags);
    this._lastCleaned = dateLastCleaned;
  }
  get id() { return this._id; }
  get title() { return this._catalogItem.title; }
  hasTag(aString) { return this._catalogItem.hasTag(aString); }
}
```
**[DON'T]** Inherit from a class just to reuse its fields or a single method, exposing irrelevant methods to the subclass's public API.
```javascript
// Anti-pattern: A physical instance (Scroll) incorrectly extending a conceptual category (CatalogItem)
class Scroll extends CatalogItem {
  constructor(id, title, tags, dateLastCleaned) {
    super(id, title, tags);
    this._lastCleaned = dateLastCleaned;
  }
}
```

## Pull Up Constructor Body
**[DO]** Slide common assignments after `super()` and pull them into the parent.
```javascript
class Party {
  constructor(name) {
    this._name = name;
  }
}
class Employee extends Party {
  constructor(name, id, monthlyCost) {
    super(name);
    this._id = id;
    this._monthlyCost = monthlyCost;
  }
}
```
**[DON'T]** Duplicate identical initialization logic across multiple subclass constructors.
```javascript
class Party {}
class Employee extends Party {
  constructor(name, id, monthlyCost) {
    super();
    this._name = name; // Anti-pattern: Duplicated across all siblings
    this._id = id;
    this._monthlyCost = monthlyCost;
  }
}
class Department extends Party {
  constructor(name, staff) {
    super();
    this._name = name; // Anti-pattern: Duplicated across all siblings
    this._staff = staff;
  }
}
```