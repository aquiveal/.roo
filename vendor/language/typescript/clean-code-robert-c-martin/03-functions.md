# @Domain
These rules MUST trigger when the AI is tasked with creating, modifying, refactoring, or reviewing functions, methods, or subroutines within any programming language. They apply to all architectural levels and modules where behavioral logic is defined.

# @Vocabulary
- **Niladic Function**: A function taking zero arguments. (Highly preferred).
- **Monadic Function**: A function taking exactly one argument.
- **Dyadic Function**: A function taking exactly two arguments.
- **Triadic Function**: A function taking exactly three arguments. (Avoid).
- **Polyadic Function**: A function taking more than three arguments. (Strictly prohibited).
- **Flag Argument**: A boolean value passed into a function, immediately indicating that the function does more than one thing (one thing if true, another if false).
- **Output Argument**: An argument used as an output container rather than an input. 
- **Command Query Separation**: The principle stating that a function should either change the state of an object (Command) OR return information about that object (Query), but never both.
- **The Stepdown Rule**: Code should read like a top-down narrative, where every function is immediately followed by the functions at the next level of abstraction down.
- **Abstract Factory**: A design pattern used to encapsulate switch statements so that they occur only once to create polymorphic objects.
- **Temporal Coupling**: An implicit order-of-operations dependency where one function must be called before another.

# @Objectives
- Ensure functions are microscopically small, typically fewer than 20 lines.
- Guarantee that every function performs exactly ONE conceptual action.
- Eliminate mixed levels of abstraction within a single function.
- Minimize function arity (argument count), pushing aggressively toward zero-argument (niladic) functions.
- Eliminate side effects, output arguments, and flag arguments.
- Isolate error handling from business logic.

# @Guidelines
- **Size & Indentation Constraints**:
  - Functions MUST rarely exceed 20 lines.
  - Blocks within `if`, `else`, `while`, and similar control structures MUST be exactly one line long. That line MUST be a function call.
  - The indentation level of a function MUST NOT exceed one or two levels.
- **Do One Thing**:
  - A function is doing one thing if you cannot meaningfully extract another function from it with a name that is not merely a restatement of its implementation.
  - Functions MUST NOT be divided into sections (e.g., "declarations", "initializations", "processing").
- **Abstraction Levels**:
  - Every statement inside a function MUST be at the exact same level of abstraction.
  - That level of abstraction MUST be exactly one level below the stated name of the function.
- **The Stepdown Rule**:
  - When writing multiple functions in a file, order them so that the caller is placed strictly above the callee, creating a top-down narrative reading flow.
- **Switch Statements**:
  - Switch statements (and large `if/else` chains) MUST be avoided where possible.
  - If a switch statement is unavoidable, it MUST be buried in the basement of an Abstract Factory, it MUST be used solely to create polymorphic objects, and it MUST NOT be repeated elsewhere in the system.
- **Naming**:
  - Do not fear long names. A long descriptive name is superior to a short enigmatic name and superior to a long descriptive comment.
  - Use a consistent lexicon. Use the same verbs and nouns for similar concepts across the codebase.
- **Arguments**:
  - Maximum allowed arguments: 2 (Dyadic). 3 (Triadic) is strongly discouraged and requires explicit architectural justification. 4+ is forbidden.
  - **Flag Arguments**: NEVER pass a boolean into a function. Split the function into two separate functions instead.
  - **Output Arguments**: NEVER use arguments to output state. State changes MUST happen on the owning object (`this.changeState()` rather than `changeState(outputArg)`).
  - **Argument Objects**: If a function requires more than two arguments, conceptually related arguments MUST be grouped into an object/class.
  - **Keyword Form**: Encode argument names into the function name to avoid ordering confusion (e.g., `assertExpectedEqualsActual(expected, actual)`).
- **Side Effects**:
  - Functions MUST NOT do anything hidden. Do not initialize sessions, open connections, or modify globals if the function name implies a simple check or query.
- **Command Query Separation**:
  - A function MUST either do something (Command) or answer something (Query). Do not mix the two. (e.g., Do not return a boolean success flag from a state-mutating function; throw an exception instead).
- **Error Handling**:
  - Prefer Exceptions to returning Error Codes. Returning error codes forces the caller to deal with errors immediately and clutters the happy path.
  - **Extract Try/Catch**: Try/Catch blocks mix error processing with normal processing. The body of the `try`, the `catch`, and the `finally` MUST be extracted into their own independent functions.
  - **Error Handling Is One Thing**: If a function handles errors, the `try` keyword MUST be the very first word in the function, and there MUST be nothing after the `catch`/`finally` blocks.
- **No Duplication (DRY)**:
  - Code MUST NOT be repeated. Duplicated algorithms or structures MUST be abstracted out into a single method, base class, or strategy.

# @Workflow
When tasked with writing or modifying a function, the AI MUST execute the following algorithm:
1. **Drafting**: Write the function to satisfy the immediate requirement, including all logic, loops, variables, and error handling.
2. **Testing**: Ensure unit tests cover the new logic (implicitly or explicitly).
3. **Extraction & Shrinking**:
   - Identify nested structures (`if`, `while`). Extract the bodies into well-named functions.
   - Look at the `try/catch` block. Extract the inner business logic into a separate function.
   - Check the length. If it exceeds 10-20 lines, identify the abstraction boundaries and split the function.
4. **Argument Reduction**:
   - Count the arguments.
   - If boolean flags are present, split the function into two explicitly named functions.
   - If arity is > 2, group related arguments into a data structure object.
5. **Naming Review**: Read the extracted function names. Ensure they form a verb-noun phrase that perfectly describes the action and does not hide side effects.
6. **Reordering**: Sort the newly extracted functions sequentially using the Stepdown Rule (caller above callee).

# @Examples (Do's and Don'ts)

### Try/Catch Extraction
**[DON'T]**
```java
public void delete(Page page) {
    try {
        deletePage(page);
        registry.deleteReference(page.name);
        configKeys.deleteKey(page.name.makeKey());
    } catch (Exception e) {
        logger.log(e.getMessage());
    }
}
```

**[DO]**
```java
public void delete(Page page) {
    try {
        deletePageAndAllReferences(page);
    } catch (Exception e) {
        logError(e);
    }
}

private void deletePageAndAllReferences(Page page) throws Exception {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
}

private void logError(Exception e) {
    logger.log(e.getMessage());
}
```

### Command Query Separation
**[DON'T]**
```java
// Sets the username and returns true if it worked.
if (set("username", "unclebob")) { ... }
```

**[DO]**
```java
if (attributeExists("username")) {
    setAttribute("username", "unclebob");
}
```

### Flag Arguments
**[DON'T]**
```java
public void render(boolean isSuite) {
    if (isSuite) {
        // render suite
    } else {
        // render single
    }
}
```

**[DO]**
```java
public void renderForSuite() {
    // render suite
}

public void renderForSingleTest() {
    // render single
}
```

### Switch Statements
**[DON'T]**
```java
public Money calculatePay(Employee e) throws InvalidEmployeeType {
    switch (e.type) {
        case COMMISSIONED:
            return calculateCommissionedPay(e);
        case HOURLY:
            return calculateHourlyPay(e);
        case SALARIED:
            return calculateSalariedPay(e);
        default:
            throw new InvalidEmployeeType(e.type);
    }
}
```

**[DO]**
```java
public abstract class Employee {
    public abstract boolean isPayday();
    public abstract Money calculatePay();
    public abstract void deliverPay(Money pay);
}

public interface EmployeeFactory {
    public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType;
}

public class EmployeeFactoryImpl implements EmployeeFactory {
    public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType {
        switch (r.type) {
            case COMMISSIONED:
                return new CommissionedEmployee(r);
            case HOURLY:
                return new HourlyEmployee(r);
            case SALARIED:
                return new SalariedEmployee(r);
            default:
                throw new InvalidEmployeeType(r.type);
        }
    }
}
```

### Grouping Arguments
**[DON'T]**
```java
Circle makeCircle(double x, double y, double radius);
```

**[DO]**
```java
Circle makeCircle(Point center, double radius);
```