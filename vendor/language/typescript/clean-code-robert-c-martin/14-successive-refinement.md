# @Domain
Trigger these rules when tasked with code refactoring, structural code improvements, cleaning up legacy code, implementing new features in existing large classes, or when explicitly asked to apply "Successive Refinement" or clean up a "working but messy" module.

# @Vocabulary
- **Successive Refinement**: The architectural practice of writing a working "rough draft" of code and subsequently transforming it into clean code through a series of continuous, tiny, behavior-preserving transformations.
- **Rough Draft**: The initial version of a module that successfully works and passes tests but is structurally messy, highly coupled, or bloated.
- **Festering Pile**: A code module that has been allowed to rot and become unmaintainable because programmers added features to a working draft without refactoring it.
- **Incrementalism**: The discipline of making a large number of very tiny, isolated changes rather than massive structural overhauls, ensuring the system remains executable and tests pass after every single change.
- **Type-Case**: An anti-pattern utilizing `if/else` or `switch` chains to check the type or flag of a variable to determine behavior.
- **ArgumentMarshaler**: The archetypal pattern introduced in this chapter representing the extraction of type-specific parsing and formatting logic into polymorphic derivative classes.
- **TDD (Test-Driven Development)**: The practice of relying on a suite of automated unit tests to verify that the precise behavior of the system remains unchanged during successive refinement.

# @Objectives
- The AI MUST prioritize the long-term maintainability and structure of the code over merely getting it to "work." Working code is only the first step.
- The AI MUST eliminate `if/else` or `switch` chains used for type-checking by extracting them into polymorphic interfaces and derivative classes.
- The AI MUST separate concerns by moving distinct responsibilities (like exception definitions and error message formatting) out of the core logic classes and into dedicated modules.
- The AI MUST protect the system from breaking during refactoring by strictly adhering to incrementalism—planning and executing refactoring in micro-steps.

# @Guidelines
- **Draft Then Refine**: The AI MUST recognize that clean code is not written in one pass. When generating new complex logic, the AI may write a functional rough draft, but MUST immediately follow up with successive refinement to clean the structure.
- **Micro-Refactoring (Incrementalism)**: When refactoring, the AI MUST NOT make massive, sweeping structural changes in a single bound. The AI MUST apply changes one variable, one method, or one class at a time.
- **Test-Backed Safety**: The AI MUST assume that automated tests exist and MUST NOT break them. If instructed to refactor, the AI should mentally or literally verify that the behavior remains identical.
- **Temporary Scaffolding**: The AI MUST be willing to "put things in so you can take them out again." (e.g., temporarily passing an unused argument to a method so that its signature matches other methods, enabling them to be abstracted into a common interface).
- **Eradicate Type-Cases**: When encountering code that branches logic based on a type identifier (e.g., `isBoolean`, `isString`, `isInt`), the AI MUST refactor this into an abstract base class or interface with polymorphic derivatives.
- **Isolate Exceptions**: The AI MUST completely separate exception handling, error codes, and error formatting from the main domain logic. Create dedicated Exception classes to handle their own error message formatting.
- **Variable Consolidation**: If a class contains multiple collections or variables handling different types of the same logical entity (e.g., `booleanArgs`, `stringArgs`, `intArgs`), the AI MUST consolidate them into a single collection of a unified polymorphic type (e.g., `Map<Character, ArgumentMarshaler>`).
- **Never Settle for "Working"**: The AI MUST NEVER leave a function in a bloated state just because it passes tests. The AI MUST proactively suggest or execute cleanups for nested `try/catch` blocks, large instance variable lists, and mixed levels of abstraction.

# @Workflow
When tasked with refining a messy module, the AI MUST adhere to the following rigid algorithmic process:

1. **Analysis & Test Verification**:
   - Analyze the module to identify the core responsibilities.
   - Identify Type-Cases, bloated variable lists, and misplaced error handling.
   - Acknowledge the requirement to preserve existing behavior.

2. **Establish the Interface (Skeleton)**:
   - Create the target abstract base class or interface (e.g., `ArgumentMarshaler`) at the bottom of the file or in a new file.
   - Define the shared abstract methods required by the type-cases (e.g., `set()`, `get()`).

3. **Incremental Migration**:
   - Create the first derivative class (e.g., `BooleanArgumentMarshaler`).
   - Change the first specific collection/variable to use the new polymorphic type.
   - Update the `set` and `get` methods for *only* that specific type to delegate to the new derivative class.
   - Leave the remaining types untouched.

4. **Iterative Deployment**:
   - Repeat Step 3 for the next type (e.g., `StringArgumentMarshaler`), then the next (e.g., `IntegerArgumentMarshaler`), ensuring the system remains conceptually compilable/testable at every step.

5. **Consolidate Collections**:
   - Once all types have derivative classes, replace the individual type-specific collections with a single collection utilizing the shared interface.

6. **Eliminate the Type-Case**:
   - Remove the `if/else` or `switch` block that checked the types, replacing it with a single polymorphic method call (e.g., `m.set(currentArgument)`).

7. **Extract Misplaced Responsibilities**:
   - Extract internal exception classes, error enums, and error formatting strings into a dedicated Exception class file.
   - Extract the interface and derivative classes into their own dedicated files.

# @Examples (Do's and Don'ts)

### Polymorphic Abstraction over Type-Cases
[DO]
```java
// Clean: Unified collection and polymorphic delegation
private Map<Character, ArgumentMarshaler> marshalers = new HashMap<Character, ArgumentMarshaler>();

private boolean setArgument(char argChar) throws ArgsException {
    ArgumentMarshaler m = marshalers.get(argChar);
    if (m == null)
        return false;
    try {
        m.set(currentArgument);
        return true;
    } catch (ArgsException e) {
        e.setErrorArgumentId(argChar);
        throw e;
    }
}
```

[DON'T]
```java
// Messy: Multiple collections and Type-Case if/else chains
private Map<Character, Boolean> booleanArgs = new HashMap<Character, Boolean>();
private Map<Character, String> stringArgs = new HashMap<Character, String>();

private boolean setArgument(char argChar) throws ArgsException {
    if (isBooleanArg(argChar))
        setBooleanArg(argChar, true);
    else if (isStringArg(argChar))
        setStringArg(argChar);
    else
        return false;
    return true;
}
```

### Separation of Error Formatting
[DO]
```java
// Clean: Error formatting is the responsibility of the Exception class
public class ArgsException extends Exception {
    private ErrorCode errorCode;
    private char errorArgumentId;

    public String errorMessage() {
        switch (errorCode) {
            case MISSING_STRING:
                return String.format("Could not find string parameter for -%c.", errorArgumentId);
            // ...
        }
    }
}
```

[DON'T]
```java
// Messy: Main logic class is polluted with UI/Error formatting
public class Args {
    private ErrorCode errorCode;
    private char errorArgument;

    public String errorMessage() throws Exception {
        switch (errorCode) {
            case MISSING_STRING:
                return String.format("Could not find string parameter for -%c.", errorArgument);
            // ...
        }
    }
}
```

### Step-by-Step Method Standardization (Scaffolding)
[DO]
```java
// Step 1: Add iterator argument to boolean even if it doesn't need it, so it matches String/Int requirements
public void set(Iterator<String> currentArgument) throws ArgsException {
    booleanValue = true; // Iterator is safely ignored, but signature matches interface
}
```

[DON'T]
```java
// Attempting to keep divergent signatures breaks polymorphism
public void setBoolean() { booleanValue = true; }
public void setString(Iterator<String> args) { stringValue = args.next(); }
// The AI must not leave signatures fragmented if they need to belong to a unified interface.
```