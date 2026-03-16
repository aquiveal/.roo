# @Domain
Trigger these rules when tasked with refactoring legacy code, cleaning up existing object-oriented classes, improving test coverage, resolving code smells, isolating abstractions from implementations, or restructuring class hierarchies.

# @Vocabulary
- **Boy Scout Rule**: The practice of checking in code slightly cleaner than when it was checked out.
- **Explaining Temporary Variable**: A well-named local variable used exclusively to break down a complex algorithm or calculation into transparent, understandable steps.
- **Feature Envy**: A code smell where a method is more interested in the fields or methods of another class than the class it resides in.
- **Logical Dependency**: An implicit assumption one module makes about another's implementation that is not physically enforced by the code architecture.
- **Abstract Factory Pattern**: A creational pattern used to shield a base class from knowing about or instantiating its own derivatives.
- **Ordinal**: A relative offset or sequence number (e.g., days since a specific epoch), preferred over implementation-specific terms like "Serial Number" for abstract concepts.

# @Objectives
- **Make it Work First**: The AI must ensure a comprehensive safety net of tests is in place, achieving >90% coverage and fixing boundary condition bugs *before* structural refactoring begins.
- **Separate Abstraction from Implementation**: The AI must meticulously prevent abstract base classes from knowing about, instantiating, or housing data specific to their concrete derivatives.
- **Maximize Expressiveness**: The AI must eliminate noise (redundant comments, dead code, cluttered keywords) and use precise naming and explanatory variables to reveal algorithmic intent.
- **Promote Type Safety**: The AI must ruthlessly eradicate primitive constants (`int`, `String`) and flag arguments, replacing them with strongly typed `enum` structures and polymorphic behaviors.

# @Guidelines

### Testing & Preparation
- The AI MUST analyze existing unit tests for missing coverage and write independent unit tests to cover unexecuted executable statements before altering code structure.
- The AI MUST fix boundary condition bugs (e.g., `>` vs `>=`) and algorithmic errors exposed by tests before starting the "cleanup" phase.
- The AI MUST ensure all tests pass after *every single incremental change*.

### Comments & Clutter
- The AI MUST delete historical change logs or bylines from comments. Source code control handles history.
- The AI MUST delete redundant comments that simply restate the method, variable name, or obvious behavior.
- The AI MUST NOT use multiple languages (e.g., HTML tags like `<ul>`, `<li>`) inside Javadocs or source comments. Use `<pre>` or standard markdown to preserve formatting.
- The AI MUST delete dead code, including unused variables, unused private methods, and empty default constructors.
- The AI MUST remove `final` keywords from method arguments and local variables if they add no real value and only contribute to visual clutter.

### Naming & Abstraction
- The AI MUST NOT use implementation-specific terms in the names of abstract classes (e.g., rename `SerialDate` to `DayDate`).
- The AI MUST name methods according to their side effects. If a method returns a new instance rather than mutating the current object, the AI MUST use prefixes like `plus` instead of `add` (e.g., `plusDays` instead of `addDays`).
- The AI MUST NOT use abbreviations or arbitrary numbering in variable names; use descriptive terminology.

### Architecture & Object-Oriented Design
- The AI MUST NOT use inheritance to gain access to constants.
- The AI MUST convert groups of related primitive constants (e.g., `public static final int JANUARY = 1`) into `enum` types.
- The AI MUST push down variables, constants, and methods that are specific to a single implementation from the abstract base class to the concrete derivative class.
- The AI MUST pull up methods from derivative classes to the base class if the implementation does not depend on any derivative-specific state.
- The AI MUST NOT allow a base class to instantiate its own derivatives. The AI MUST extract instantiation logic into an Abstract Factory.
- The AI MUST resolve Feature Envy by moving methods into the class or `enum` containing the data the method operates on.
- The AI MUST eliminate flag arguments used to format output (e.g., a boolean passed to `toString`). Create separate, well-named methods instead.

### Algorithmic Clarity
- The AI MUST combine duplicate `if` statements or identical conditional blocks into a single expression using logical operators like `||`.
- The AI MUST use Explaining Temporary Variables to clarify complex mathematics, date calculations, or index manipulations.
- The AI MUST replace `switch` statements with polymorphic methods on `enum` types or derivative classes.
- The AI MUST convert logical dependencies into physical dependencies. If an algorithm depends on an implementation detail, the AI MUST create an abstract method to explicitly query that detail.
- The AI MUST convert static methods to instance methods if they operate primarily on the variables/state of the class they belong to.

# @Workflow
1. **Analyze and Test**: Evaluate the target class and existing tests. Generate exhaustive unit tests for any uncovered logic. Run tests and fix any failing boundary conditions.
2. **De-clutter**: Remove file headers containing change history, delete redundant Javadoc comments, strip HTML from comments, and remove useless `final` keywords on local variables/arguments.
3. **Rename for Abstraction**: Rename the class and its core methods to reflect the abstract concept rather than the underlying implementation (e.g., removing "Serial" or "Ordinal" from abstract API names).
4. **Enum Conversion**: Locate all `public static final int` constant groups. Convert them into rich `enum` classes. Update all method signatures that previously accepted `int` to accept the new `enum`.
5. **Class Relocation**: Move enums and unrelated utility classes out of the base class and into their own separate files.
6. **Push Down / Pull Up**: Identify fields in the base class used only by specific derivatives and push them down. Identify abstract methods implemented identically across derivatives without relying on concrete state and pull them up.
7. **Decouple via Factory**: Locate any place the base class instantiates a concrete derivative. Replace this with an Abstract Factory pattern.
8. **Resolve Feature Envy**: Move methods that heavily query external classes/enums directly into those classes/enums.
9. **Clarify Algorithms**: Break apart complex formulas using Explaining Temporary Variables. Convert static state-manipulating methods into instance methods.
10. **Polymorphism over Switch**: Convert any remaining `switch` statements over types/enums into abstract polymorphic methods implemented by the enum values or subclasses.
11. **Verify**: Ensure the test suite runs and passes perfectly.

# @Examples (Do's and Don'ts)

### 1. Inheriting Constants
- **[DON'T]** Implement an interface just to avoid typing the class name for constants.
```java
public abstract class DayDate implements MonthConstants {
    public void setMonth(int month) {
        if (month == JANUARY) { ... }
    }
}
```
- **[DO]** Use a strongly typed `enum` to represent the group of constants.
```java
public enum Month {
    JANUARY(1), FEBRUARY(2);
    public final int index;
    Month(int index) { this.index = index; }
}

public abstract class DayDate {
    public void setMonth(Month month) {
        if (month == Month.JANUARY) { ... }
    }
}
```

### 2. Base Class Knowing Derivatives
- **[DON'T]** Allow an abstract base class to instantiate its own concrete subclass.
```java
public abstract class DayDate {
    public DayDate addDays(int days) {
        // Base class directly coupling to SpreadsheetDate
        return new SpreadsheetDate(this.ordinal + days); 
    }
}
```
- **[DO]** Use an Abstract Factory to decouple the base class from implementation details.
```java
public abstract class DayDate {
    public DayDate plusDays(int days) {
        return DayDateFactory.makeDate(this.getOrdinalDay() + days);
    }
}
```

### 3. Naming Immutability
- **[DON'T]** Use verbs that imply state mutation when returning a new instance.
```java
DayDate date = oldDate.addDays(5); // Misleading: looks like oldDate is mutated
```
- **[DO]** Use names that imply a new value is being created and returned.
```java
DayDate date = oldDate.plusDays(5); // Clear: returns a new DayDate instance
```

### 4. Explaining Temporary Variables
- **[DON'T]** Write dense, impenetrable math algorithms in a single line.
```java
public DayDate getNearestDayOfWeek(final Day targetDay) {
    if (((targetDay.index - getDayOfWeek().index + 7) % 7) > 3)
        return plusDays(((targetDay.index - getDayOfWeek().index + 7) % 7) - 7);
    else
        return plusDays((targetDay.index - getDayOfWeek().index + 7) % 7);
}
```
- **[DO]** Break the algorithm down with explanatory variables.
```java
public DayDate getNearestDayOfWeek(final Day targetDay) {
    int offsetToThisWeeksTarget = targetDay.index - getDayOfWeek().index;
    int offsetToFutureTarget = (offsetToThisWeeksTarget + 7) % 7;
    int offsetToPreviousTarget = offsetToFutureTarget - 7;

    if (offsetToFutureTarget > 3)
        return plusDays(offsetToPreviousTarget);
    else
        return plusDays(offsetToFutureTarget);
}
```

### 5. Polymorphism over Switch
- **[DON'T]** Use a switch statement to determine behavior based on an enum or type code.
```java
public boolean isInRange(DayDate d, DateInterval interval) {
    switch(interval) {
        case OPEN: return d > left && d < right;
        case CLOSED: return d >= left && d <= right;
    }
}
```
- **[DO]** Push the behavior into the enum itself.
```java
public enum DateInterval {
    OPEN {
        public boolean isIn(int d, int left, int right) { return d > left && d < right; }
    },
    CLOSED {
        public boolean isIn(int d, int left, int right) { return d >= left && d <= right; }
    };
    public abstract boolean isIn(int d, int left, int right);
}

// Usage:
return interval.isIn(d, left, right);
```