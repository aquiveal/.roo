@Domain
Trigger this rule file when the user requests architectural refactoring at the class level, asks to implement a generic solution to a common software problem, needs to enforce object creation constraints (especially for Domain Entities or Value Objects), or explicitly mentions applying Creational, Structural, or Behavioral "Design Patterns" (such as Factory, Observer, Adapter, etc.).

@Vocabulary
- **Design Pattern**: A generic, reusable solution to a commonly occurring problem in software development, applied at the class or function level.
- **Creational Patterns**: Patterns that control how objects are created (e.g., Singleton, Abstract Factory, Prototype, Factory, Builder).
- **Structural Patterns**: Patterns that simplify how relationships between components are defined (e.g., Adapter, Bridge, Decorator).
- **Behavioral Patterns**: Patterns that facilitate elegant communication between objects (e.g., Template, Mediator, Observer).
- **Singleton**: A creational pattern ensuring only a single instance of a class can exist.
- **Abstract Factory**: A creational pattern for creating an instance of several families of classes.
- **Prototype**: A creational pattern for starting out with an instance that is cloned from an existing one.
- **Factory Pattern**: A creational pattern acting as the sole place to create an object, heavily utilized to enforce validation and business rules prior to instantiation.
- **Adapter**: A structural pattern creating an interface to enable classes that generally can't work together to work together.
- **Bridge**: A structural pattern splitting a class into a hierarchy, enabling implementations to be developed independently.
- **Decorator**: A structural pattern for adding responsibilities to objects dynamically.
- **Template**: A behavioral pattern deferring the exact steps of an algorithm to a subclass.
- **Mediator**: A behavioral pattern defining the exact communication channels allowed between classes.
- **Observer**: A behavioral pattern enabling classes to subscribe to something of interest and be notified when a change occurs.
- **YAGNI**: "You Aren't Gonna Need It." A core principle dictating that design patterns should not be introduced unless absolutely necessary to avoid accidental complexity.
- **Intentional Signifier**: A visual clue in code (such as the pattern name in the class name, e.g., `StudentController`, `DuckFactory`) that communicates to other developers what can and cannot be done with that code.

@Objectives
- Apply standardized class-level patterns to solve recurring structural, creational, and behavioral software problems.
- Enforce strict object creation policies and prevent illegal states by utilizing the Factory Pattern.
- Decouple object instantiation from object behavior and simplify component relationships.
- Communicate conceptual models and design intent explicitly to other developers through intentional pattern naming (Signifiers).
- Prevent Overengineering by strictly applying YAGNI; only introduce design patterns when the inherent complexity of the problem demands it.

@Guidelines
- **Pattern Selection & Categorization**:
  - Analyze the problem to determine if it requires a Creational (object instantiation), Structural (component relationships), or Behavioral (object communication) solution.
- **Creational Constraints & Factory Pattern Implementation**:
  - MUST enforce constraints on object creation using the Factory Pattern when modeling complex domains (Entities, Value Objects).
  - MUST use a `private` constructor to prevent the use of the `new` keyword from outside the class, circumventing creation rules.
  - MUST expose a `public static create()` method that runs validation logic and returns either a valid instance or an explicit error.
  - MUST avoid partial object creation; ensure an object is fully created with all required dependencies and valid state, or not created at all.
  - MUST resolve "multiple variants" anti-patterns (e.g., deep inheritance trees like `DuckThatCanFlyAndCook`) by refactoring to the Factory or Builder patterns.
- **Signifiers & Naming**:
  - MUST include the pattern name in the class name (e.g., `AudioDeviceFactory`) or match the structural signature of the pattern to act as an intentional signifier for future maintainers.
- **Complexity Management (YAGNI)**:
  - NEVER introduce a design pattern prematurely. Design patterns add accidental complexity.
  - ALWAYS attempt to keep designs as simple as possible first.
  - MUST justify the use of a design pattern; only implement it when you are absolutely sure you need it to solve coupling, cohesion, or duplication issues.

@Workflow
1. **Analyze the Problem Statement**: Identify if the task involves object creation rules, managing relationships between incompatible classes, or defining communication flows between objects.
2. **YAGNI Assessment**: Evaluate the simplest possible design that runs the tests, contains no duplication, and maximizes clarity. If a simple function or class suffices, abort pattern implementation. 
3. **Select the Appropriate Pattern**: If a pattern is justified, choose from Creational (Singleton, Abstract Factory, Prototype, Factory, Builder), Structural (Adapter, Bridge, Decorator), or Behavioral (Template, Mediator, Observer).
4. **Draft the Interface/Contract**: Define the abstraction before the implementation to enforce the Dependency Inversion Principle.
5. **Implement the Factory (If Creational)**:
   - Make the class constructor `private`.
   - Create a `public static create(props)` method.
   - Insert guard clauses and business rule validations inside the `create` method.
   - Return the fully instantiated object (or a Result/Error monad).
6. **Apply Intentional Signifiers**: Rename variables, methods, and classes to reflect the chosen pattern (e.g., appending `Factory`, `Adapter`, `Observer`) so the conceptual model is immediately obvious to human readers.
7. **Review against Accidental Complexity**: Ensure the implementation does not introduce "Interface Bloat" or unnecessary layers of abstraction that degrade developer experience (DX).

@Examples (Do's and Don'ts)

**Creational Patterns (Factory) & Object Constraints**
- [DO]: Use a private constructor and a static factory method to enforce business rules and prevent illegal states.
  ```typescript
  export class User {
    private constructor(private props: UserProps) {}

    public static create(props: UserProps): Result<User> {
      if (!props.email || !props.username) {
        return Result.fail<User>("Missing required properties");
      }
      // additional validation logic here
      return Result.ok<User>(new User(props));
    }
  }
  ```
- [DON'T]: Expose a public constructor that allows developers to instantiate objects in an invalid state, requiring them to remember to call validation methods manually.
  ```typescript
  export class User {
    public email: string;
    public username: string;
    
    // Allows invalid partial creation
    constructor() {} 
  }
  ```

**Resolving Multiple Variants Anti-Pattern**
- [DO]: Use a Factory or Builder pattern to compose behaviors dynamically.
  ```typescript
  const duckThatCanCook = DuckFactory.create({ capabilities: ['cook'] });
  const duckThatCanFlyAndCook = DuckFactory.create({ capabilities: ['cook', 'fly'] });
  ```
- [DON'T]: Create overly specific, brittle inheritance chains (over-specification).
  ```typescript
  class Duck {}
  class DuckThatCanFly extends Duck {}
  class DuckThatCanFlyAndCook extends Duck {}
  ```

**Intentional Signifiers (Pattern Naming)**
- [DO]: Explicitly name abstractions to communicate the design pattern conceptually.
  ```typescript
  abstract class AudioDevice { ... }
  class AudioDeviceFactory {
    public static create(deviceType: string): AudioDevice { ... }
  }
  ```
- [DON'T]: Hide the pattern's intent behind generic or tech-y sounding names (e.g., `AudioDeviceManager`, `AudioDeviceHelper`, `AudioDeviceProcessor`).