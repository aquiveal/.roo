@Domain
These rules trigger whenever the AI is tasked with refactoring code, writing new code, reviewing pull requests, conducting code quality audits, or writing and updating unit tests. They activate unconditionally when the user requests "clean code" enforcement, "code smell" detection, or architectural restructuring.

@Vocabulary
- **Code Smell**: Surface indications that usually correspond to a deeper problem in the system's design or code.
- **DRY (Don't Repeat Yourself)**: A principle stating that every piece of knowledge must have a single, unambiguous, authoritative representation within a system.
- **Feature Envy**: A code smell where a method accesses the data of another object more than its own data.
- **Selector Argument**: A boolean, enum, or integer passed into a function to control its execution path, violating the single responsibility principle.
- **Temporal Coupling**: An implicit dependency where methods must be called in a specific, unenforced order.
- **Bucket Brigade**: A technique to expose temporal coupling by making each function return a result that the next function in the sequence requires as an argument.
- **Transitive Navigation (Law of Demeter)**: A code smell where a module navigates through multiple collaborators (e.g., `a.getB().getC()`). Code should be "shy" and only talk to immediate friends.
- **Magic Number**: Any raw number or string token in code whose meaning is not self-describing; must be replaced by a named constant.
- **Obsolete Comment**: A comment that has become irrelevant, incorrect, or floating away from the code it originally described.
- **Mumbling**: A comment that forces the reader to look at other parts of the system to understand what the comment means.
- **Boundary Condition**: A corner case or edge calculation (e.g., array length + 1) that is prone to errors and should be encapsulated.

@Objectives
- **Eliminate Duplication**: Ruthlessly abstract repeated code, switch statements, and similar algorithms using methods, polymorphism, and design patterns.
- **Enforce Single Responsibility**: Ensure functions do exactly one thing, and classes manage exactly one concept.
- **Achieve Total Transparency**: Code intent must be instantly visible through descriptive naming, encapsulated conditionals, and explanatory intermediate variables.
- **Minimize Dependencies**: Restrict module knowledge to immediate collaborators to prevent rigid architectures.
- **Ensure Rigorous Verification**: All behaviors, especially boundary conditions and bug-adjacent logic, must be exhaustively and automatically tested.

@Guidelines

**Comments**
- **C1: Ban Meta-Data**: Do not include historical text, author attributions, or change histories in comments. Leave this to source control.
- **C2: Delete Obsolete Comments**: Immediately update or delete comments that no longer accurately describe the code.
- **C3: Ban Redundancy**: Do not write comments that state what the code adequately says for itself (e.g., Javadocs that just repeat the method signature).
- **C4: Enforce Professional Writing**: If a comment is necessary, write it with correct grammar, punctuation, and brevity.
- **C5: Annihilate Commented-Out Code**: Delete commented-out code immediately. Source control will remember it.

**Environment**
- **E1: Single-Step Build**: The system must build with a single trivial command (e.g., `ant all` or equivalent).
- **E2: Single-Step Test**: All unit tests must be executable via a single, obvious command or button click.

**Functions**
- **F1: Limit Arguments**: Functions must have zero to two arguments. Three is highly questionable. More than three is strictly forbidden.
- **F2: Ban Output Arguments**: Arguments must be inputs. If state must change, change the state of the object the method is called on.
- **F3: Ban Flag Arguments**: Never pass booleans into a function. Split the function into two separate functions instead.
- **F4: Delete Dead Functions**: Remove methods that are never called.

**General Design & Architecture**
- **G1: One Language per File**: Minimize or eliminate the mixing of multiple languages (e.g., Java, HTML, XML, JavaScript) in a single source file.
- **G2: Implement Obvious Behavior**: Functions and classes must fulfill the reasonable expectations of the programmer reading the name (Principle of Least Surprise).
- **G3: Test Boundaries Exhaustively**: Never rely on intuition. Write specific tests for every corner case and boundary condition.
- **G4: Do Not Override Safeties**: Never ignore compiler warnings, bypass manual serialization controls, or turn off failing tests.
- **G5: DRY (Don't Repeat Yourself)**: Eliminate identical code clones via methods, repetitive `if/switch` chains via polymorphism, and similar algorithms via the Template Method or Strategy patterns.
- **G6: Strict Abstraction Levels**: Place general concepts in base classes and detailed implementation in derivatives. Do not mix levels of abstraction in the same container.
- **G7: Blind Base Classes**: Base classes must know absolutely nothing about their derivatives.
- **G8: Minimal Interfaces**: Hide data, utility functions, constants, and temporaries. Classes should have minimal methods and instance variables.
- **G9: Purge Dead Code**: Delete unexecuted `if` blocks, impossible `catch` blocks, and unused switch cases.
- **G10: Vertical Separation**: Declare local variables immediately above their first use. Define private functions immediately below their first use.
- **G11: Strict Consistency**: Use identical naming and structural conventions for similar operations throughout the codebase.
- **G12: Eradicate Clutter**: Delete empty default constructors, unused variables, and meaningless comments.
- **G13: Ban Artificial Coupling**: Do not declare enums, constants, or static functions within specific classes if they are used generally. Put them in appropriate, independent locations.
- **G14: Cure Feature Envy**: A method must be interested only in the variables of its own class. Do not use accessors to manipulate the data of another object from the outside.
- **G15: Ban Selector Arguments**: Never pass booleans, enums, or ints to select a behavior path. Extract into multiple independent functions.
- **G16: Reveal Intent**: Do not use run-on expressions or magic numbers. Make the algorithm's intent visually transparent.
- **G17: Appropriate Placement**: Place code where a reader naturally expects it to live based on function/class names.
- **G18: Restrict Static Methods**: Prefer non-static methods. Only make a method static if it does not operate on instance state AND will never need to behave polymorphically.
- **G19: Use Explanatory Variables**: Break complex calculations into intermediate variables with descriptive names.
- **G20: Honest Function Names**: The name must describe EVERYTHING the function does, including side effects.
- **G21: Understand the Algorithm**: Do not rely on trial-and-error passing of tests. You must intellectually understand why the algorithm is correct.
- **G22: Physicalize Dependencies**: If Module A depends on Module B, it must explicitly ask Module B for data. Do not rely on logical assumptions (e.g., hardcoded page sizes).
- **G23: The "One Switch" Rule**: Prefer polymorphism. A given type of selection can have ONLY ONE switch statement in the system, used exclusively to create polymorphic objects.
- **G24: Enforce Conventions**: Follow a strict, team-wide coding standard for formatting, naming, and structure.
- **G25: Replace Magic Numbers**: Hide raw numbers and string tokens behind well-named constants.
- **G26: Be Precise**: Handle nulls explicitly, use appropriate locking for concurrency, use integer math for currency, and handle all exceptions.
- **G27: Structure Over Convention**: Enforce design rules using architectural structures (e.g., abstract methods) rather than naming conventions.
- **G28: Encapsulate Conditionals**: Extract boolean logic inside `if` or `while` statements into well-named functions.
- **G29: Positive Conditionals**: Always prefer positive conditionals over negative conditionals.
- **G30: Functions Do One Thing**: Split functions that perform multiple operations into a sequence of smaller, single-purpose functions.
- **G31: Expose Temporal Coupling**: Enforce required method execution order by passing the output of the first method as an argument to the second method (Bucket Brigade).
- **G32: Meaningful Structure**: Do not arbitrarily scope classes or variables. The structure must communicate its necessity.
- **G33: Encapsulate Boundary Conditions**: Extract `+1` or `-1` index offsets into clearly named variables (e.g., `int nextLevel = level + 1;`).
- **G34: Descend One Level of Abstraction**: Statements within a function must be EXACTLY one level of abstraction below the function's name.
- **G35: Elevate Configurable Data**: Pass default/configuration values from high-level components down to low-level functions. Do not bury defaults in the low level.
- **G36: Avoid Transitive Navigation**: Enforce the Law of Demeter. Modules must only call methods on their immediate collaborators.

**Java-Specific Rules**
- **J1: Wildcard Imports**: Use `import package.*;` when importing two or more classes from a package to reduce clutter and hard dependencies.
- **J2: Ban Inherited Constants**: NEVER implement an interface just to gain access to its constants. Use `import static` instead.
- **J3: Prefer Enums**: Always use Java `enum` instead of `public static final int` to leverage named types, fields, and methods.

**Naming Rules**
- **N1: Descriptive Names**: Names must dictate the structure and expectations of the code. Reevaluate them continuously.
- **N2: Abstraction-Level Naming**: Names must reflect the abstraction level of the class/interface, not the implementation details (e.g., `connectionLocator` instead of `phoneNumber`).
- **N3: Standard Nomenclature**: Use pattern names (e.g., `Decorator`) and ubiquitous domain language terms.
- **N4: Unambiguous Names**: Do not use vague verbs. Names must clearly differentiate functions from one another.
- **N5: Length Matches Scope**: Use short names (`i`, `j`) ONLY for tiny scopes. Use long, precise names for large or global scopes.
- **N6: Ban Encodings**: Never use type prefixes, scope prefixes (`m_`), or Hungarian notation.
- **N7: Reveal Side-Effects**: Names must explicitly state if a function creates, initializes, or mutates state (e.g., `createOrReturnOos` instead of `getOos`).

**Testing Rules**
- **T1: Test Everything**: Tests are insufficient until every condition and calculation is validated.
- **T2: Coverage Tools**: Use coverage tools to visually identify untested `if` or `catch` blocks.
- **T3: Do Not Skip Trivial Tests**: Write them for documentary value.
- **T4: Document Ambiguity**: Use `@Ignore` or commented-out tests to explicitly mark requirement ambiguities.
- **T5: Focus on Boundaries**: Algorithms fail at the boundaries. Exhaustively test limits and corner cases.
- **T6: Exhaustive Near-Bug Testing**: When a bug is found, write exhaustive tests for that entire function; bugs congregate.
- **T7: Analyze Failure Patterns**: Look for commonalities in failing tests (e.g., all negative inputs fail) to diagnose issues.
- **T8: Analyze Coverage Patterns**: Use passing tests' coverage to deduce why failing tests fail.
- **T9: Keep Tests Fast**: Optimize test execution time. Slow tests get skipped.

@Workflow
1. **Initial Assessment**: Run all tests (E2) and ensure the build succeeds (E1). Execute a coverage tool (T2) to identify blind spots.
2. **De-cluttering Phase**: Scan the target file. Delete all commented-out code (C5), dead functions (F4), unused variables (G9, G12), and obsolete/redundant comments (C2, C3).
3. **Naming & Abstraction Alignment**: Rename classes, variables, and methods to correctly reflect their abstraction level (N2) and exact behavior (N7). Remove all Hungarian notation and `m_` prefixes (N6).
4. **Function Extraction & Simplification**: 
   - Identify functions with >2 arguments and extract Argument Objects (F1).
   - Identify flag arguments and split the function into two paths (F3, G15).
   - Extract boolean logic inside `if/while` into descriptive methods (G28).
   - Identify functions doing more than one thing and extract methods until each does one thing, descending exactly one level of abstraction (G30, G34).
5. **Coupling & Dependency Resolution**:
   - Search for `a.getB().getC()` and refactor to immediate collaborators (G36).
   - Search for methods requiring a specific order and refactor them to take the output of the previous method (G31).
   - Move methods suffering from Feature Envy to the class containing the data they manipulate (G14).
6. **Polymorphism & Abstraction**: Find repetitive `switch` or `if/else` chains. Extract them into polymorphic classes using the Abstract Factory or Strategy patterns (G23).
7. **Refinement & Testing**: Replace all magic numbers with constants (G25). Add targeted unit tests for boundary conditions (T5) and ensure tests execute fast (T9).

@Examples

**[DO] Encapsulate Conditionals**
```java
if (timer.shouldBeDeleted()) {
    delete(timer);
}
```

**[DON'T] Encapsulate Conditionals**
```java
if (timer.hasExpired() && !timer.isRecurrent()) {
    delete(timer);
}
```

**[DO] Avoid Transitive Navigation (Law of Demeter)**
```java
// Tell the immediate collaborator to perform the action
myCollaborator.doSomething();
```

**[DON'T] Avoid Transitive Navigation (Law of Demeter)**
```java
// Navigating through the object graph
myCollaborator.getPart().getSubPart().doSomething();
```

**[DO] Expose Temporal Coupling**
```java
public void dive(String reason) {
    Gradient gradient = saturateGradient();
    List<Spline> splines = reticulateSplines(gradient);
    diveForMoog(splines, reason);
}
```

**[DON'T] Expose Temporal Coupling**
```java
public void dive(String reason) {
    saturateGradient();
    reticulateSplines(); // Relies on hidden state set by saturateGradient
    diveForMoog(reason);
}
```

**[DO] Avoid Flag Arguments**
```java
public int straightPay() {
    return getTenthsWorked() * getTenthRate();
}

public int overTimePay() {
    int overTimeTenths = Math.max(0, getTenthsWorked() - 400);
    int overTimePay = overTimeBonus(overTimeTenths);
    return straightPay() + overTimePay;
}
```

**[DON'T] Avoid Flag Arguments**
```java
public int calculateWeeklyPay(boolean overtime) {
    int tenthRate = getTenthRate();
    int tenthsWorked = getTenthsWorked();
    int straightTime = Math.min(400, tenthsWorked);
    int overTime = Math.max(0, tenthsWorked - straightTime);
    int straightPay = straightTime * tenthRate;
    double overtimeRate = overtime ? 1.5 : 1.0 * tenthRate;
    int overtimePay = (int)Math.round(overTime*overtimeRate);
    return straightPay + overtimePay;
}
```

**[DO] Use Explanatory Variables**
```java
Matcher match = headerPattern.matcher(line);
if(match.find()) {
    String key = match.group(1);
    String value = match.group(2);
    headers.put(key.toLowerCase(), value);
}
```

**[DON'T] Use Explanatory Variables**
```java
Matcher match = headerPattern.matcher(line);
if(match.find()) {
    headers.put(match.group(1).toLowerCase(), match.group(2));
}
```

**[DO] Constants vs Enums**
```java
public enum HourlyPayGrade {
    APPRENTICE {
        public double rate() { return 1.0; }
    },
    JOURNEYMAN {
        public double rate() { return 1.5; }
    };
    public abstract double rate();
}
```

**[DON'T] Constants vs Enums**
```java
public interface PayrollConstants {
    public static final int APPRENTICE = 1;
    public static final int JOURNEYMAN = 2;
}
```