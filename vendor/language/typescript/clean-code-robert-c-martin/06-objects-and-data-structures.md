# @Domain

These rules MUST be triggered whenever the AI is tasked with:
- Designing or creating new classes, types, or data models.
- Defining interfaces or boundaries between system modules.
- Refactoring existing object hierarchies, procedural code, or data models.
- Implementing database mappers, object-relational mapping (ORM) entities, or data parsing logic.
- Adding new behaviors or new data types to an existing architecture.
- Writing or refactoring chained method calls.

# @Vocabulary

- **Object**: A construct that hides its data behind abstractions and exposes functions (behavior) that operate on that data.
- **Data Structure**: A construct that exposes its data fully and contains no meaningful functions or business logic.
- **Data/Object Anti-Symmetry**: The diametrically opposed nature of Objects and Data Structures. Procedural code (Data Structures) makes it easy to add new functions but hard to add new data types. Object-Oriented code makes it easy to add new classes but hard to add new functions.
- **Law of Demeter (LoD)**: A heuristic stating that a module should not know about the innards of the objects it manipulates ("talk to friends, not to strangers").
- **Train Wreck**: A chain of consecutive method calls (e.g., `a.getB().getC().doSomething()`) that violates the Law of Demeter when dealing with Objects. 
- **Hybrid**: An anti-pattern construct that is half Object and half Data Structure, possessing both significant business logic and exposed internal data (or public accessors/mutators).
- **Data Transfer Object (DTO)**: The quintessential Data Structure, consisting of a class with public variables and no functions, often used for parsing sockets or communicating with databases.
- **Bean**: A DTO variant with private variables manipulated by getters and setters, providing quasi-encapsulation but acting purely as a Data Structure.
- **Active Record**: A special form of DTO that directly translates to database tables and includes navigational methods like `save` or `find`, but MUST NOT contain business rules.

# @Objectives

- The AI MUST establish a rigid, absolute boundary between Objects and Data Structures.
- The AI MUST protect the internal implementation details of Objects through pure behavioral abstraction, never merely blanketing private variables with getters and setters.
- The AI MUST prevent cascading dependencies and tight coupling by rigorously enforcing the Law of Demeter and the "Tell, Don't Ask" principle.
- The AI MUST determine the vector of change for a given system component (adding new types vs. adding new behaviors) and choose either OO or Procedural design accordingly.
- The AI MUST eradicate Hybrid structures from the codebase.

# @Guidelines

### Data Abstraction
- **Do Not Blithely Add Accessors**: The AI MUST NOT automatically generate getters and setters for all private variables. Hiding implementation is about providing abstract interfaces, not just a layer of functions between the variable and the caller.
- **Express Data Abstractly**: The AI MUST design interfaces that allow users to manipulate the *essence* of the data without ever knowing its internal implementation (e.g., using percentages instead of raw units).

### Data/Object Anti-Symmetry
- **Choose the Right Paradigm**: The AI MUST recognize that "everything is an object" is a myth. 
- **When to Use Objects**: The AI MUST use Objects when the system requires the flexibility to add new *data types* without changing existing functions.
- **When to Use Data Structures**: The AI MUST use Data Structures and procedural code when the system requires the flexibility to add new *functions* without changing existing data structures.

### The Law of Demeter
- **Restrict Method Invocations**: When implementing a method `f` in class `C`, the AI MUST ONLY call methods on:
  1. `C` itself.
  2. Objects created locally within `f`.
  3. Objects passed as arguments to `f`.
  4. Objects held in instance variables of `C`.
- **Do Not Talk to Strangers**: The AI MUST NOT invoke methods on objects that are returned by any of the allowed functions above.

### Train Wrecks and Hiding Structure
- **Analyze the Chain**: When encountering chained calls (`a.getB().getC()`), the AI MUST determine if the elements are Objects or Data Structures. If they are Data Structures, the chain is acceptable (as data is naturally exposed). If they are Objects, it is a Train Wreck and MUST be refactored.
- **Tell, Don't Ask**: If the AI needs to navigate an Object's internal structure to perform an action, the AI MUST relocate that action into the Object itself. Tell the Object what to do; do not ask it for its internal state.

### Hybrids
- **Never Mix Paradigms**: The AI MUST NEVER create Hybrid structures. A class must either unambiguously hide its data and expose behavior, or unambiguously expose its data and have no behavior. Hybrids make it hard to add both new functions and new data structures.

### DTOs and Active Records
- **Keep DTOs Dumb**: The AI MUST implement DTOs as simple structures with public variables (or Bean-style getters/setters if framework conventions demand it) and ZERO business logic.
- **Segregate Active Records**: The AI MUST treat Active Records purely as Data Structures. The AI MUST NOT embed business rules into Active Records. Instead, the AI MUST extract business rules into separate Object classes that encapsulate the Active Record or its data.

# @Workflow

When designing, analyzing, or refactoring types, the AI MUST follow this algorithmic process:

1. **Classification**: Before writing the class, determine its core purpose. Is its purpose to hold raw data, or is its purpose to expose behaviors? Explicitly classify it as an `[OBJECT]` or a `[DATA_STRUCTURE]`.
2. **Implementation based on Classification**:
   - *If [OBJECT]*: Make all variables private. DO NOT auto-generate getters/setters. Expose only abstract, intention-revealing methods.
   - *If [DATA_STRUCTURE]*: Expose data variables directly (or via simple Bean accessors). DO NOT add business logic methods.
3. **Demeter Check**: Scan all implemented methods. Identify any chained method calls (`obj.getThing().getOtherThing()`).
   - If the chain traverses `[OBJECT]`s, the AI MUST refactor the code to ask the primary object to perform the ultimate behavior directly.
4. **Active Record Segregation**: If an object maps to a database table (has `save()`/`find()`), scan it for business logic (e.g., `calculatePay()`, `isValid()`). If business logic exists, extract it into a separate, pure `[OBJECT]` and leave the Active Record as a pure `[DATA_STRUCTURE]`.
5. **Hybrid Eradication**: Review the final output. If a class has meaningful business logic methods AND exposes its internal variables, split it into two distinct constructs: a Data Structure and an Object that acts upon it.

# @Examples (Do's and Don'ts)

### Data Abstraction
- **[DO]**:
  ```java
  public interface Vehicle {
      double getPercentFuelRemaining();
  }
  ```
- **[DON'T]**: Exposing the exact internal variables.
  ```java
  public interface Vehicle {
      double getFuelTankCapacityInGallons();
      double getGallonsOfGasoline();
  }
  ```

### Data/Object Anti-Symmetry (Procedural Data Structures vs OO)
- **[DO]**: Use simple data structures if you plan to add many new operations (like `area()`, `perimeter()`) without changing the types.
  ```java
  public class Square {
      public Point topLeft;
      public double side;
  }
  public class Rectangle {
      public Point topLeft;
      public double height;
      public double width;
  }
  public class Geometry {
      public double area(Object shape) {
          if (shape instanceof Square) {
              Square s = (Square)shape;
              return s.side * s.side;
          }
          // ...
      }
  }
  ```
- **[DON'T]**: Create Hybrids that try to do both, resulting in data exposure AND localized logic.

### Law of Demeter & Train Wrecks
- **[DO]**: Tell the object to do the work, hiding its internal structure.
  ```java
  // ctxt is an Object
  BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
  ```
- **[DON'T]**: Violate the Law of Demeter by navigating through the object's internals.
  ```java
  // ctxt is an Object
  final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();
  String outFile = outputDir + "/" + className.replace('.', '/') + ".class";
  FileOutputStream fout = new FileOutputStream(outFile);
  BufferedOutputStream bos = new BufferedOutputStream(fout);
  ```

### Active Records
- **[DO]**: Separate the Active Record (data) from the Business Rules (behavior).
  ```java
  // Data Structure
  public class EmployeeRecord {
      public String name;
      public double hourlyRate;
      public void save() { ... }
  }

  // Object
  public class PayrollCalculator {
      private EmployeeRecord record;
      public PayrollCalculator(EmployeeRecord record) { this.record = record; }
      public double calculatePay(int hours) {
          return record.hourlyRate * hours;
      }
  }
  ```
- **[DON'T]**: Mix business rules into the Active Record.
  ```java
  public class EmployeeRecord {
      public String name;
      public double hourlyRate;
      public void save() { ... }
      
      // Anti-pattern: Business logic in an Active Record
      public double calculatePay(int hours) {
          return this.hourlyRate * hours;
      }
  }
  ```