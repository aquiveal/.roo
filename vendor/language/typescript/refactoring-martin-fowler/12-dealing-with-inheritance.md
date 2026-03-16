# @Domain
Trigger these rules when the user requests or the AI detects tasks involving class structures, inheritance hierarchies, object composition, interface design, deduplication of class methods/fields, conversion of type codes into polymorphic objects, or the restructuring of relationships between parent and child classes.

# @Vocabulary
*   **Inheritance**: A mechanism to reuse existing functionality by deriving a child class (subclass) from a parent class (superclass), allowing the addition or overriding of features.
*   **Subclass/Superclass**: The child (subclass) and parent (superclass) entities in an inheritance relationship.
*   **Delegation / Composition**: An alternative to inheritance where an object holds a reference to another object (the delegate) and forwards specific method calls to it, rather than inheriting from it.
*   **Polymorphism**: Overriding conditional logic (like `switch` statements) by providing different implementations of a method across multiple subclasses.
*   **Type Code**: A primitive value (enum, string, symbol, or number) used to differentiate between different kinds of a similar entity (e.g., job types, order priorities).
*   **Direct Inheritance**: Subclassing the entity class itself based on a type code.
*   **Indirect Inheritance**: Creating a separate class hierarchy for the type code property itself, useful when the primary class must change types dynamically or already has a subclass hierarchy.
*   **Subclass Responsibility Error**: An error thrown by a superclass method to explicitly indicate that subclasses must provide their own implementation (used in dynamic languages lacking abstract methods).
*   **Type-Instance Homonym**: A common modeling error where a class representing a generic type or model (e.g., a catalog item) is incorrectly used as a superclass for a specific physical instance (e.g., a physical scroll).
*   **Factory Function**: A function that encapsulates a constructor call, allowing the return of different subclasses or proxies depending on the input parameters or environment.

# @Objectives
*   Ensure that inheritance is used correctly and semantically: Every method on the superclass must make sense on the subclass, and every instance of the subclass must be a valid instance of the superclass.
*   Eliminate duplicate code and data across class hierarchies by moving features up or down the inheritance tree.
*   Replace complex conditional logic based on types with clean, polymorphic subclasses.
*   Favor a judicious mixture of composition and inheritance. Fall back to delegation when inheritance becomes a problem (e.g., single axis of variation limits, high coupling, or inappropriate reuse).
*   Execute hierarchy restructuring in safe, incremental, and easily testable steps.

# @Guidelines
*   **Pulling Up Methods & Fields**
    *   Methods must have identical bodies before being pulled up. If they are similar but not identical, parameterize them first.
    *   Before pulling up a method, check that all referenced fields and methods are accessible from the superclass. Pull up prerequisite fields first.
    *   If a pulled-up method relies on a property that varies by subclass, define a trap method (Subclass Responsibility Error) on the superclass to explicitly signal the contract.
*   **Pulling Up Constructor Bodies**
    *   Constructors have strict execution orders. Always define the superclass constructor and ensure subclasses call `super()` first.
    *   Use Slide Statements to move common subclass constructor logic immediately after the `super()` call before pulling it up.
    *   If common initialization logic depends on a field that must be assigned in the subclass, *do not* pull it up into the superclass constructor. Instead, extract a `finishConstruction()` method and pull that method up.
*   **Pushing Down Methods & Fields**
    *   Push features down if they are only relevant to one or a small subset of subclasses.
    *   Only push down a method if the calling code explicitly knows it is working with the specific subclass. If the caller does not know the specific subclass, use Replace Conditional with Polymorphism and leave a default/placebo behavior on the superclass.
*   **Replacing Type Codes with Subclasses**
    *   Use Direct Inheritance if the type code is immutable and the class isn't already subclassed for another reason.
    *   Use Indirect Inheritance if the type changes over the object's lifetime or if the class already has a subclass hierarchy. Encapsulate the type code into its own class and subclass that instead.
    *   Wrap the instantiation in a Factory Function so the caller is decoupled from the specific subclass constructors.
*   **Removing and Collapsing Subclasses**
    *   Remove a subclass if it does too little (e.g., just overrides a type code or single string).
    *   When collapsing a hierarchy, choose the class name that makes the most sense for the future unified class.
*   **Replacing Subclass with Delegate**
    *   Apply this when a class needs multiple axes of variation (since inheritance only supports one) or when a class's behavior category needs to change dynamically.
    *   Create a delegate class and initialize it inside the host class.
    *   Pass a back-reference (e.g., `this._host`) to the delegate constructor so it can access superclass data.
    *   When moving overridden methods that call `super`, either extract the base calculation in the host or pass the base calculation's result as an argument to the delegate's extension method to avoid infinite recursion.
*   **Replacing Superclass with Delegate**
    *   Apply this when the subclass does not need all the methods of the superclass, or to fix a Type-Instance Homonym.
    *   Never inherit from a class just to reuse its internal data or utility methods if the public interface doesn't semantically match.
    *   Create a delegate reference to the former superclass, implement forwarding methods for the features you *actually* want to expose, and remove the `extends` keyword.
    *   If multiple instances were copying the superclass data, consider using Change Value to Reference to link them to a single shared delegate object.

# @Workflow
1.  **Assess the Hierarchy Problem**: Determine the goal (e.g., deduplication = Pull Up; narrowing scope = Push Down; resolving bad inheritance = Replace with Delegate; enabling polymorphism = Type Code to Subclass).
2.  **Encapsulate Access**: Self-encapsulate any type codes, fields, or constructor calls (using Factory Functions) that will be affected by the structural change.
3.  **Prepare the Target Structure**: Create the necessary empty superclasses, subclasses, or delegate classes. 
4.  **Migrate Data (Fields)**: Move fields to the target structure first. Test.
5.  **Migrate Behavior (Methods)**: Move methods one by one to the target structure. If moving to a delegate, ensure back-references (`this._host`) are established. If moving to a superclass, ensure abstract/trap methods are defined. Test after each move.
6.  **Migrate Constructors**: Slide common statements, extract initialization methods if necessary, or modify factory functions to instantiate the new structures.
7.  **Reroute & Clean Up**: Update clients to call the new factory functions or delegate forwarding methods. Delete empty subclasses, remove obsolete `extends` declarations, and apply Remove Dead Code.
8.  **Validate**: Run static checks and tests after every atomic change.

# @Examples (Do's and Don'ts)

### Pull Up Method & Subclass Responsibility
**[DON'T]** Leave implicit dependencies when pulling up a method to a superclass in dynamic languages without defining the requirement.
```javascript
class Party {}
class Employee extends Party {
  get annualCost() { return this.monthlyCost * 12; }
}
class Department extends Party {
  get annualCost() { return this.monthlyCost * 12; }
}
```

**[DO]** Pull up the common method and define a Subclass Responsibility Error for the varying property to explicitly signal the contract.
```javascript
class Party {
  get annualCost() { return this.monthlyCost * 12; }
  get monthlyCost() { throw new Error("SubclassResponsibilityError"); }
}
class Employee extends Party {
  // implements monthlyCost
}
class Department extends Party {
  // implements monthlyCost
}
```

### Pull Up Constructor Body
**[DON'T]** Duplicate standard assignments across subclass constructors.
```javascript
class Employee extends Party {
  constructor(name, id, monthlyCost) {
    super();
    this._name = name;
    this._id = id;
    this._monthlyCost = monthlyCost;
  }
}
class Department extends Party {
  constructor(name, staff) {
    super();
    this._name = name;
    this._staff = staff;
  }
}
```

**[DO]** Move the common assignment to the superclass constructor and pass it via `super()`.
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
class Department extends Party {
  constructor(name, staff) {
    super(name);
    this._staff = staff;
  }
}
```

### Replace Type Code with Subclasses & Factory
**[DON'T]** Rely on type codes and switch statements for instantiation logic spread across the code.
```javascript
class Employee {
  constructor(name, type) {
    this._name = name;
    this._type = type;
  }
  get type() { return this._type; }
}
const emp = new Employee("John", "engineer");
```

**[DO]** Wrap instantiation in a Factory Function and use subclass overrides.
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
const emp = createEmployee("John", "engineer");
```

### Replace Superclass with Delegate
**[DON'T]** Inherit from a class just to reuse its data if the subclass isn't semantically a true instance of the superclass (Type-Instance Homonym).
```javascript
class CatalogItem {
  constructor(id, title) {
    this._id = id;
    this._title = title;
  }
  get title() { return this._title; }
}
// Modeling error: A physical scroll is NOT a catalog item.
class Scroll extends CatalogItem {
  constructor(id, title, dateLastCleaned) {
    super(id, title);
    this._lastCleaned = dateLastCleaned;
  }
}
```

**[DO]** Remove inheritance, construct a delegate, and explicitly forward only the valid methods.
```javascript
class CatalogItem {
  constructor(id, title) {
    this._id = id;
    this._title = title;
  }
  get title() { return this._title; }
}
// Scroll uses composition to reference the CatalogItem
class Scroll {
  constructor(id, title, dateLastCleaned) {
    this._id = id;
    this._catalogItem = new CatalogItem(id, title);
    this._lastCleaned = dateLastCleaned;
  }
  get id() { return this._id; }
  get title() { return this._catalogItem.title; } // Forwarded
}
```