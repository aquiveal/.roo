# @Domain
Trigger these rules when performing code refactoring, writing unit tests, analyzing software architecture, or optimizing system design. This applies specifically when the user requests code cleanup, duplication elimination, improved readability, or the application of the four rules of Simple Design.

# @Vocabulary
* **Emergent Design:** A design approach where robust, clean architecture naturally evolves and improves by continually applying a small set of simple rules during the coding process.
* **Simple Design:** Kent Beck's four fundamental rules for producing well-designed software, prioritized as: 1) Runs all the tests, 2) Contains no duplication, 3) Expresses intent, 4) Minimizes classes and methods.
* **Duplication:** The primary enemy of a well-designed system, which manifests as identical lines of code, similar implementation logic, or overlapping state tracking.
* **Template Method Pattern:** A specific design pattern utilized to remove higher-level duplication by placing the skeleton of an algorithm in a base class and delegating the divergent details to subclasses.
* **Expressiveness:** The degree to which code clearly and effortlessly communicates the original programmer's intent to future readers and maintainers.
* **Dogmatism:** Rigid, unpragmatic adherence to arbitrary coding rules (e.g., "create an interface for every class") that artificially inflates the number of classes and methods.

# @Objectives
* Ensure the system is fully testable and continuously passes all tests, as testability drives high cohesion and low coupling.
* Relentlessly seek out and eliminate all forms of duplication, from micro-level line repetitions to macro-level algorithmic similarities.
* Maximize the expressiveness of the code so that future maintainers spend zero mental effort deciphering intent.
* Balance the application of Single Responsibility Principle (SRP) and duplication elimination by keeping the total number of classes and methods as small as pragmatically possible.
* Facilitate a continuous, incremental refactoring process where the system's design improves step-by-step without fear of breaking functionality.

# @Guidelines
* **Test-Driven Foundation:** The AI MUST ensure that any code design is verifiable. If code cannot be tested, its design is inherently flawed. Writing tests MUST be the first priority to enable safe refactoring.
* **Continuous Incremental Refactoring:** The AI MUST pause after generating or modifying a few lines of code to reflect on the design. If the design degraded, the AI MUST clean it up immediately while ensuring tests still pass.
* **Micro-Duplication Elimination:** The AI MUST extract commonality at the smallest level. If two methods track related states or perform highly similar calculations, the AI MUST consolidate the logic (e.g., tying an `isEmpty` check directly to a `size` check rather than maintaining two separate variables).
* **Macro-Duplication Elimination:** When algorithms are largely similar but differ in specific steps, the AI MUST utilize the TEMPLATE METHOD pattern or similar abstractions to pull common code into a base class.
* **Expressive Naming:** The AI MUST choose names that act as clear descriptions of class and function responsibilities. If a name is difficult to choose, the class or function is likely too large.
* **Standard Nomenclature:** The AI MUST use standard design pattern names (e.g., COMMAND, VISITOR) in class names to succinctly communicate the architectural design to other developers.
* **Tests as Documentation:** The AI MUST construct unit tests that are expressive enough to act as documentation by example, allowing a reader to quickly understand what a class is all about.
* **Pragmatic Minimization:** The AI MUST NOT create unnecessary abstractions purely out of dogma. It MUST resist separating data and behavior or creating interfaces for every class if doing so adds zero value and merely increases the class/method count.

# @Workflow
1. **Verification Phase:** Ensure that a comprehensive suite of tests exists for the target code. If tests do not exist, draft them to establish a safety net. Code must run and pass all tests.
2. **Refactoring Pause:** Stop feature development to evaluate the current code block against the rules of Simple Design.
3. **Duplication Hunt:** 
   * Scan for exact duplicate lines of code and extract them into shared functions.
   * Scan for similar lines of code and parameterize them.
   * Scan for duplicate implementations/state tracking and consolidate them.
   * Apply the TEMPLATE METHOD pattern for duplicated high-level algorithms.
4. **Expressiveness Check:** Review the refactored code. Rename variables, methods, and classes to vividly express their intent. Integrate standard design pattern terminology into class names where applicable.
5. **Minimization Pass:** Review the resulting architecture. If classes or methods were created strictly due to arbitrary rules or dogmatic standards (and add no real value), consolidate them to minimize the system's overall footprint.
6. **Validation:** Rerun all tests to ensure the incremental refactoring step preserved all system behavior.

# @Examples (Do's and Don'ts)

**Principle: Removing Implementation Duplication (Micro-Level)**
* **[DO]:** Reuse existing state calculations to determine secondary states.
  ```java
  int size() { return count; }
  boolean isEmpty() { return 0 == size(); }
  ```
* **[DON'T]:** Maintain separate variables for related states, creating duplication of implementation.
  ```java
  int size() { return count; }
  boolean isEmpty() { return emptyTracker; } // Must be updated alongside count
  ```

**Principle: Removing Algorithmic Duplication (Macro-Level via Template Method)**
* **[DO]:** Abstract the common algorithm into a base class and delegate specific steps to subclasses.
  ```java
  abstract public class VacationPolicy {
      public void accrueVacation() {
          calculateBaseVacationHours();
          alterForLegalMinimums();
          applyToPayroll();
      }
      private void calculateBaseVacationHours() { /* ... */ };
      abstract protected void alterForLegalMinimums();
      private void applyToPayroll() { /* ... */ };
  }
  
  public class USVacationPolicy extends VacationPolicy {
      @Override protected void alterForLegalMinimums() { /* US specific logic */ }
  }
  ```
* **[DON'T]:** Write nearly identical methods that duplicate the algorithm structure.
  ```java
  public class VacationPolicy {
      public void accrueUSDivisionVacation() {
          // calculate base hours
          // US specific minimums
          // apply to payroll
      }
      public void accrueEUDivisionVacation() {
          // calculate base hours
          // EU specific minimums
          // apply to payroll
      }
  }
  ```

**Principle: Expressiveness and Standard Nomenclature**
* **[DO]:** Name classes to reveal the standard design pattern they implement.
  ```java
  public class DocumentVisitor { ... }
  public class ExecutePrintCommand { ... }
  ```
* **[DON'T]:** Use generic, unexpressive terms when a standard pattern is in play.
  ```java
  public class DocumentProcessor { ... }
  public class PrintDoer { ... }
  ```

**Principle: Minimizing Classes and Methods (Avoiding Dogma)**
* **[DO]:** Create a standard concrete class when it does a single job perfectly well without the need for polymorphic swapping.
  ```java
  public class User { ... }
  ```
* **[DON'T]:** Blindly follow a team rule that every class must have an interface and a separate data container, bloating the system.
  ```java
  public interface IUser { ... }
  public class UserImpl implements IUser { ... }
  public class UserData { ... }
  ```