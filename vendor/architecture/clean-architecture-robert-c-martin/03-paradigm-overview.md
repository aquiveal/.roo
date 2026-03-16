# @Domain

These rules MUST activate whenever the AI is tasked with generating new code, refactoring existing software structures, establishing architectural boundaries, defining module algorithms, or managing data state and access. 

# @Vocabulary

*   **Structured Programming**: A programming paradigm that imposes discipline on the *direct* transfer of control. It replaces unrestrained jumps with sequence, selection, and iteration.
*   **Object-Oriented Programming (OOP)**: A programming paradigm that imposes discipline on the *indirect* transfer of control. It utilizes heap-allocated stack frames (instance variables and methods) and polymorphism.
*   **Functional Programming**: A programming paradigm that imposes discipline upon *assignment*. It is founded on $\lambda$-calculus and the concept of immutability.
*   **Immutability**: The foundational notion that the values of symbols do not change; the absence of variable assignment.
*   **Architectural Boundaries**: The points of separation between distinct software components, crossed using disciplined polymorphic interfaces.
*   **Negative Discipline**: The concept that architectural paradigms do not add new capabilities, but rather remove them (removing `goto` statements, function pointers, and assignment).

# @Objectives

*   Implement the algorithmic foundation of all modules exclusively through Structured Programming principles.
*   Achieve separation of components and cross architectural boundaries strictly through Object-Oriented Programming principles (Polymorphism).
*   Enforce rigorous data management, location, and access controls through Functional Programming principles (Immutability).
*   Treat all three programming paradigms as negative constraints that remove capabilities to enforce safe, disciplined code structures.

# @Guidelines

*   **Negative Constraints First**: The AI MUST recognize that paradigms tell us what *not* to do. The AI MUST proactively remove unrestrained jumps, undisciplined function pointers, and undisciplined assignments from the codebase.
*   **Algorithmic Foundations (Structured Programming)**:
    *   The AI MUST NOT use `goto` statements or any form of unrestrained, undisciplined direct transfer of control.
    *   The AI MUST construct all module algorithms using exclusively sequence, selection (`if`/`then`/`else`), and iteration (`do`/`while`/`until`).
*   **Boundary Management (Object-Oriented Programming)**:
    *   The AI MUST NOT use raw, undisciplined function pointers to manage indirect transfers of control.
    *   The AI MUST use polymorphism as the exclusive mechanism to cross architectural boundaries.
    *   When local variables need to exist long after a function returns, the AI MUST utilize constructors and classes to move the function call stack frame to the heap (i.e., local variables become instance variables, nested functions become methods).
*   **Data Management (Functional Programming)**:
    *   The AI MUST NOT use variable assignment arbitrarily.
    *   The AI MUST enforce immutability wherever possible by ensuring that the values of initialized symbols do not change.
    *   If a language requires mutability, the AI MUST apply very strict discipline to alter the value of a variable, segregating mutable state away from immutable business logic.
*   **Alignment with Architectural Concerns**:
    *   When addressing the architectural concern of *function*, the AI MUST apply Structured Programming.
    *   When addressing the architectural concern of *separation of components*, the AI MUST apply Object-Oriented Programming.
    *   When addressing the architectural concern of *data management*, the AI MUST apply Functional Programming.

# @Workflow

1.  **Analyze the Architectural Concern**: Identify whether the current task requires algorithmic implementation (function), component separation (boundaries), or data management (state).
2.  **Apply Negative Discipline**: Before generating code, explicitly restrict the use of `goto`, function pointers, and mutable assignment within the scope of the task.
3.  **Implement Algorithmic Logic**:
    *   Structure all control flow using standard `if/then/else` and `do/while` loops. 
    *   Recursively decompose functions into smaller units without breaking the sequential, selective, or iterative flow.
4.  **Implement Component Separation**:
    *   Identify boundaries between separate components.
    *   Introduce polymorphic interfaces to handle the indirect transfer of control across these boundaries.
    *   Encapsulate state within class instance variables rather than relying on global state or raw pointers.
5.  **Implement Data Management**:
    *   Define all data structures and variables as immutable by default.
    *   If an assignment or mutation is strictly required by the environment, isolate it behind strict disciplinary boundaries and prevent it from leaking into the broader system.
6.  **Verification Step**: Review the generated solution to ensure no banned constructs (`goto`, undisciplined function pointers, unrestricted variable assignments) have bypassed the paradigm rules.

# @Examples (Do's and Don'ts)

### Structured Programming: Direct Transfer of Control
*   **[DO]**: Use selection and iteration to control flow.
```python
def process_items(items):
    for item in items:
        if item.is_valid():
            process(item)
        else:
            log_error(item)
```
*   **[DON'T]**: Use `goto` or unrestrained jumps that break the discipline of control transfer.
```c
void process_items() {
    int i = 0;
start:
    if (i >= item_count) goto end;
    if (!is_valid(items[i])) goto error;
    process(items[i]);
    goto next;
error:
    log_error(items[i]);
next:
    i++;
    goto start;
end:
    return;
}
```

### Object-Oriented Programming: Crossing Architectural Boundaries
*   **[DO]**: Use polymorphism to safely dispatch behavior across boundaries.
```java
public interface DataStorage {
    void save(Data data);
}

public class CloudStorage implements DataStorage {
    @Override
    public void save(Data data) {
        // Implementation
    }
}

public class BusinessLogic {
    private final DataStorage storage;
    
    public BusinessLogic(DataStorage storage) {
        this.storage = storage; // Polymorphism handles indirect control transfer
    }
}
```
*   **[DON'T]**: Use raw function pointers or switch statements to manage indirect transfers across component boundaries.
```c
void (*save_function_ptr)(Data);

void execute_business_logic(Data data) {
    // Undisciplined indirect transfer of control
    save_function_ptr(data); 
}
```

### Functional Programming: Immutability and Assignment
*   **[DO]**: Enforce immutability and apply strict discipline to data management by preventing variable reassignment.
```typescript
function getSquares(numbers: readonly number[]): readonly number[] {
    return numbers.map(x => x * x);
}

const original = [1, 2, 3, 4, 5];
const squares = getSquares(original); // No internal state mutated
```
*   **[DON'T]**: Use undisciplined assignment or mutate symbols in place.
```typescript
let numbers = [1, 2, 3, 4, 5];

function getSquares() {
    // Undisciplined assignment mutating existing state
    for (let i = 0; i < numbers.length; i++) {
        numbers[i] = numbers[i] * numbers[i]; 
    }
}
```