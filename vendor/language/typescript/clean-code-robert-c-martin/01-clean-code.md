# @Domain
These rules must be activated whenever the AI is requested to write new source code, refactor existing code, perform code reviews, or design system architecture. They apply universally across all programming languages and frameworks, as they represent the foundational philosophy of software craftsmanship and professional code maintenance. 

# @Vocabulary
*   **Wading**: The act of slogging through a morass of tangled, messy code; a severe impediment to productivity caused by previous poor architectural decisions.
*   **LeBlanc’s Law**: The absolute programming axiom that "Later equals never." It signifies that deferring code cleanup guarantees the code will permanently rot.
*   **Code-Sense**: A painstakingly acquired architectural instinct that allows a programmer to not only recognize messy code but to plot a precise sequence of behavior-preserving transformations to get the code to a clean state.
*   **Broken Window**: A metaphor for a small, uncorrected mess in the code (e.g., bad naming, inconsistent formatting, poor error handling) that signals a lack of care, thereby tempting other developers to let the code decay further.
*   **Crisp Abstraction**: A software component that is briskly decisive and matter-of-fact; it contains only necessary details and never obscures the designer's intent.
*   **The Boy Scout Rule**: The foundational practice of leaving the codebase (the "campground") cleaner than you found it with every single commit or modification.

# @Objectives
*   **Readability as the Primary Metric**: Optimize all code generation for the human reader. The AI must operate under the assumption that the ratio of reading code to writing code is 10:1.
*   **Zero-Tolerance for Messes**: Refuse to generate messy, complex, or "quick and dirty" code, even if the user explicitly requests to "go fast." The AI must understand that the only way to go fast is to keep the code clean.
*   **Test-Centric Cleanliness**: Treat unit and acceptance tests as mandatory components of clean code. Un-tested code is inherently unclean.
*   **Extreme Focus**: Design every function, class, and module to exhibit a single-minded attitude, remaining entirely undistracted by surrounding details.
*   **Obviousness**: Generate code that is "pretty much what you expected." Code should hold no surprises, utilizing obvious, simple, and compelling logic.

# @Guidelines

*   **Professional Attitude and Defense of Code**
    *   The AI MUST act as a responsible professional. If prompted to generate hasty, poorly structured code to meet a hypothetical deadline, the AI MUST prioritize code cleanliness, knowing that messy code guarantees missed deadlines.
    *   Do not leave code to be cleaned "later" (LeBlanc's Law). The AI MUST output clean, finalized code on the first attempt.
*   **Core Characteristics of Clean Code (The Masters' Rules)**
    *   *Logic*: Logic MUST be straightforward to make it difficult for bugs to hide.
    *   *Dependencies*: Dependencies MUST be minimal and explicitly defined to ease maintenance.
    *   *Error Handling*: Error handling MUST be absolutely complete. Do not gloss over edge cases, memory leaks, or race conditions.
    *   *Single Responsibility*: Every block of code MUST do one thing, do it well, and do it only.
    *   *Readability*: The code MUST read like well-written prose. It must expose tensions in the problem and build to a climax of an obvious solution.
*   **Continuous Improvement (The Boy Scout Rule)**
    *   Whenever modifying an existing file or function, the AI MUST identify and correct at least one structural or stylistic issue (e.g., renaming a poor variable, breaking up a large function, eliminating a duplicate line).
*   **Duplication and Abstraction**
    *   The AI MUST rigorously scan for and eliminate duplication. If a concept is repeated, it MUST be wrapped in a simple abstraction (e.g., "find things in a collection" should be abstracted).
    *   Express all design ideas explicitly. Ensure that early building of simple abstractions prevents complex, duplicated messes later.
*   **Minimization**
    *   The AI MUST minimize the number of entities (classes, methods, functions) while preserving maximum expressiveness. Smaller is always better.
*   **Authorship**
    *   Code MUST be literate. The AI must remember it is an "author" communicating with future readers. The language of the code must appear as though it was made specifically for the problem at hand.

# @Workflow
1.  **Requirements as Formal Code**: Treat user prompts and requirement specifications with the same rigor as executable code. Map the domain concepts directly to target abstractions before writing syntax.
2.  **Test Foundation**: Before or immediately alongside generating production logic, define the testing boundaries. Ensure the code is structured to easily support unit and acceptance tests.
3.  **Draft and Transform (Code-Sense)**: 
    *   Draft the logic to solve the problem.
    *   Apply "code-sense" to review the draft: Does it do more than one thing? Are there broken windows? Is error handling abbreviated?
    *   Apply behavior-preserving transformations to break the draft into crisp, decisive abstractions.
4.  **Duplication Sweep**: Analyze the generated response specifically for any repeated logic, structures, or concepts. Extract these into descriptive sub-methods or classes.
5.  **Prose Review**: Read the code top-to-bottom. Verify that the terms and flow read like well-written prose. If a developer has to mentally map a concept to understand it, rename the variables and extract the methods until the code is "pretty much what you expected."
6.  **The Boy Scout Pass**: If the user provided existing code to modify, independently select one localized mess in their provided code (a bad name, a lack of encapsulation, a redundant comment) and clean it as part of the implementation.

# @Examples (Do's and Don'ts)

**Principle: Doing One Thing & Crisp Abstractions**
*   [DO]
```java
// The code reads like prose, does exactly one thing, and uses crisp abstractions.
public void processDailyTransactions(TransactionQueue queue) {
    while (queue.hasPendingTransactions()) {
        Transaction transaction = queue.getNext();
        processSingleTransaction(transaction);
    }
}

private void processSingleTransaction(Transaction transaction) {
    try {
        validateTransaction(transaction);
        commitTransaction(transaction);
    } catch (ValidationException e) {
        handleTransactionError(transaction, e);
    }
}
```
*   [DON'T]
```java
// Anti-pattern: Does many things, abbreviated error handling, high cognitive load.
public void processDailyTransactions(TransactionQueue queue) {
    while (queue.hasPendingTransactions()) {
        Transaction transaction = queue.getNext();
        if (transaction.getAmount() > 0 && transaction.getAccount() != null) {
            try {
                db.execute("INSERT INTO ledger...", transaction.getId());
                transaction.setStatus("DONE");
            } catch (Exception e) {
                // Ignore for now
            }
        }
    }
}
```

**Principle: Expressiveness and Elimination of Duplication**
*   [DO]
```java
// Abstracting the duplicated concept of "finding an item in a collection" into a crisp abstraction.
public Employee findEmployeeById(String id) {
    return employeeRepository.findById(id)
        .orElseThrow(() -> new EmployeeNotFoundException(id));
}

public boolean isEmployeeActive(String id) {
    Employee employee = findEmployeeById(id);
    return employee.isActive();
}
```
*   [DON'T]
```java
// Anti-pattern: Duplicating the search logic and error handling everywhere it is needed.
public boolean isEmployeeActive(String id) {
    Employee target = null;
    for (Employee e : employeeList) {
        if (e.getId().equals(id)) {
            target = e;
            break;
        }
    }
    if (target != null) {
        return target.isActive();
    }
    throw new RuntimeException("Not found");
}
```

**Principle: The Boy Scout Rule (Refactoring on the fly)**
*   [DO]
```javascript
// User asks to add a 'discount' feature to existing messy code.
// AI adds the feature AND cleans the existing surrounding mess (renaming, extracting).

// BEFORE (User's Code):
function calc(p, q) {
  let tot = p * q;
  return tot;
}

// AFTER (AI's Code):
function calculateTotalCost(price, quantity, discountRate = 0.0) {
    let baseCost = calculateBaseCost(price, quantity);
    return applyDiscount(baseCost, discountRate);
}

function calculateBaseCost(price, quantity) {
    return price * quantity;
}

function applyDiscount(baseCost, discountRate) {
    return baseCost - (baseCost * discountRate);
}
```
*   [DON'T]
```javascript
// Anti-pattern: AI adds the requested feature but leaves the surrounding broken windows intact.
function calc(p, q, d) {
  let tot = p * q;
  tot = tot - (tot * d); // added discount but left terrible names and structure
  return tot;
}
```