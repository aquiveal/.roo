@Domain
Trigger these rules when performing code refactoring, cleaning up legacy classes, writing or analyzing unit test frameworks (like JUnit), performing string manipulation and comparisons, or resolving code smells related to naming, structure, and conditionals.

@Vocabulary
- **Boy Scout Rule**: The practice of leaving a module cleaner than you found it, regardless of its initial state.
- **Scope Encoding**: The practice of prefixing variable names with characters that denote their scope or type (e.g., `f` for fields, `m_` for members).
- **Unencapsulated Conditional**: A complex boolean expression (e.g., `A == null || B == null || A.equals(B)`) exposed directly in an `if` or `while` statement rather than being wrapped in an explanatory method.
- **Variable Shadowing**: When a local variable shares the same name as a class member, requiring the `this.` prefix to disambiguate.
- **Temporal Coupling**: A hidden dependency where two or more methods must be called in a specific, strict order, but the method signatures do not enforce or document this requirement.
- **Topological Sorting**: Organizing methods in a file such that a calling function appears immediately before the functions it calls, resulting in a top-down narrative flow.
- **Analysis Functions**: Methods responsible for computing metrics, indices, or states (e.g., finding a common prefix length).
- **Synthesis Functions**: Methods responsible for assembling or building the final output (e.g., compacting a string using computed lengths).

@Objectives
- Continuously apply the Boy Scout Rule to incrementally improve code structure and readability during every modification.
- Eliminate outdated conventions such as scope encodings.
- Reveal the true intent of the code by encapsulating complex logic into clearly named methods.
- Make hidden temporal couplings explicit through method parameters or structural orchestration.
- Eliminate arbitrary math clutter (e.g., swarms of `+ 1` and `- 1`) by accurately defining the base and semantics of variables (e.g., length vs. index).
- Topologically separate distinct algorithmic phases, such as data analysis and data synthesis.
- Embrace refactoring as an iterative trial-and-error process; be willing to undo or inline previous extractions if a cleaner overall architecture emerges.

@Guidelines
- **Remove Scope Encodings**: The AI MUST NOT use prefixes like `f`, `m_`, or `_` for instance variables. Modern IDEs handle scope highlighting.
- **Encapsulate Conditionals**: The AI MUST extract multi-part conditional expressions into private helper methods with intention-revealing names.
- **Prefer Positive Conditionals**: The AI MUST use positive conditionals (e.g., `if (canBeCompacted())`) over negative conditionals (e.g., `if (!shouldNotBeCompacted())`) whenever logically possible, as negatives require more cognitive overhead to parse.
- **Avoid Variable Shadowing**: The AI MUST assign unique, descriptive names to local variables to prevent shadowing class members. Avoid relying on the `this.` keyword simply to differentiate between a local and member variable.
- **Name for Side-Effects and Returns**: The AI MUST ensure method names fully describe their behavior. If a method formats a string rather than just compacting it, it MUST be named `formatCompactedComparison`, not simply `compact`.
- **Enforce Single Responsibility in Methods**: If a method calculates data and also formats output, the AI MUST split it into two methods: one for calculation, one for formatting.
- **Ensure Consistent Method Conventions**: The AI MUST NOT mix state-mutation with return-value assignment in parallel functions. If `findCommonPrefix` returns a value, `findCommonSuffix` MUST also return a value, rather than mutating state directly while the other does not.
- **Expose Temporal Couplings**: If `methodB` relies on variables calculated by `methodA`, the AI MUST make this explicit. Either pass the result of `methodA` as an argument to `methodB`, or create a parent method (e.g., `findCommonPrefixAndSuffix()`) that explicitly calls them in the required order.
- **Fix Boundary Math at the Source**: The AI MUST resolve swarms of `+ 1` and `- 1` calculations by redefining the underlying variables correctly (e.g., changing a 1-based `suffixIndex` to a 0-based `suffixLength`).
- **Eliminate Masked Dead Code**: When off-by-one math is corrected, the AI MUST review surrounding `if` statements. If a condition was only necessary due to previous bad math (e.g., checking if `suffixLength > 0` when it could never be 0), the AI MUST delete the redundant conditional.
- **Topological Sorting and Grouping**: The AI MUST place caller methods above callee methods. Furthermore, the AI MUST group Analysis functions (finding prefixes/suffixes) together, and Synthesis functions (building the final string) together.

@Workflow
1. **Clean Encodings and Names**: Scan the class for `f` or `m_` prefixes and remove them. Rename local variables that shadow member variables.
2. **Encapsulate and Invert Conditionals**: Locate raw boolean expressions in `if` statements. Extract them into methods like `shouldBeCompacted()`. Ensure the logic reads positively.
3. **Isolate Responsibilities**: Check primary public methods. If a method does error-checking, data analysis, and string construction, break it into dedicated private methods.
4. **Normalize Parallel Conventions**: Look at companion methods (e.g., `findPrefix` and `findSuffix`). Standardize them so they both either return values or both mutate member state.
5. **Resolve Temporal Couplings**: Identify methods that must execute sequentially. Wrap them in a structurally ordered parent method or chain them via parameters.
6. **Refine Math and Boundaries**: Check string manipulations and loop boundaries for `+ 1` or `- 1`. Rename and adjust the base metric of the associated variables (e.g., index to length) to eliminate the math clutter.
7. **Prune Dead Logic**: Re-evaluate `if` blocks surrounding newly cleaned math boundaries. Delete any checks rendered obsolete by the boundary fixes.
8. **Synthesize Cleanly**: Rebuild string concatenation using `StringBuilder` with clearly named helper methods for each fragment (e.g., `startingContext()`, `delta()`, `endingContext()`).
9. **Topological Sort**: Reorder the class methods. Public methods first, followed by high-level private methods, then analysis helpers, then synthesis helpers.

@Examples (Do's and Don'ts)

**Principle: Encapsulating and Positively Phrasing Conditionals**
[DO]
```java
public String formatCompactedComparison(String message) {
    if (canBeCompacted()) {
        compactExpectedAndActual();
        return Assert.format(message, compactExpected, compactActual);
    } else {
        return Assert.format(message, expected, actual);
    }
}

private boolean canBeCompacted() {
    return expected != null && actual != null && !expected.equals(actual);
}
```
[DON'T]
```java
public String compact(String message) {
    if (expected == null || actual == null || areStringsEqual())
        return Assert.format(message, expected, actual);
    // ... compaction logic
}
```

**Principle: Exposing Temporal Coupling**
[DO]
```java
private void findCommonPrefixAndSuffix() {
    findCommonPrefix();
    suffixLength = 0;
    for (; !suffixOverlapsPrefix(); suffixLength++) {
        if (charFromEnd(expected, suffixLength) != charFromEnd(actual, suffixLength))
            break;
    }
}
```
[DON'T]
```java
private void compactExpectedAndActual() {
    findCommonPrefix();
    findCommonSuffix(); // Hidden dependency: findCommonSuffix relies on fPrefix being set by findCommonPrefix!
}
```

**Principle: Avoiding Variable Shadowing and Scope Encoding**
[DO]
```java
private String expected;
private String actual;

private void compactExpectedAndActual() {
    String compactExpected = compactString(expected);
    String compactActual = compactString(actual);
}
```
[DON'T]
```java
private String fExpected;
private String fActual;

public String compact(String message) {
    String expected = compactString(this.fExpected);
    String actual = compactString(this.fActual);
}
```

**Principle: Clean Synthesis via Method Extraction (Removing Math Clutter)**
[DO]
```java
private String compact(String s) {
    return new StringBuilder()
        .append(startingEllipsis())
        .append(startingContext())
        .append(DELTA_START)
        .append(delta(s))
        .append(DELTA_END)
        .append(endingContext())
        .append(endingEllipsis())
        .toString();
}

private String delta(String s) {
    int deltaStart = prefixLength;
    int deltaEnd = s.length() - suffixLength;
    return s.substring(deltaStart, deltaEnd);
}
```
[DON'T]
```java
private String compactString(String source) {
    String result = DELTA_START + source.substring(fPrefix, source.length() - fSuffix + 1) + DELTA_END;
    if (fPrefix > 0)
        result = computeCommonPrefix() + result;
    if (fSuffix > 0)
        result = result + computeCommonSuffix();
    return result;
}
```