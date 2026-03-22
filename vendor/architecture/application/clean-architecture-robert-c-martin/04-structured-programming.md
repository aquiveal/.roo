# @Domain
This rule set is activated when the AI is tasked with system architecture design, algorithm implementation, code refactoring, module/component definition, or writing and structuring automated tests. It applies whenever the AI must translate requirements into structural code elements, organize logic, or verify software behavior.

# @Vocabulary
- **Structured Programming**: A programming paradigm that imposes strict discipline on the direct transfer of control, restricting it entirely to sequence, selection, and iteration.
- **Sequence**: The linear execution of statements, mathematically provable through simple enumeration tracing inputs to outputs.
- **Selection**: Conditional branching structures (e.g., `if`/`then`/`else`), mathematically provable by enumerating and validating each distinct path.
- **Iteration**: Looping structures (e.g., `do`/`while`/`until`), mathematically provable using induction (proving for 1, assuming for N, proving for N+1, and validating start/end criteria).
- **Functional Decomposition**: The practice of taking a large-scale problem statement and recursively breaking it down into high-level functions, and then lower-level functions, ad infinitum, until tiny provable units are formed.
- **Falsifiability**: The core scientific principle applied to software stating that a program cannot be mathematically proven correct; it can only be proven incorrect. A program deemed "correct" is simply one that has withstood rigorous attempts to prove it false.
- **Provable Units**: Small, functionally decomposed blocks of code utilizing restricted control structures that can be subjected to falsification via testing.
- **Unrestrained Jumps**: Arbitrary transfers of control (e.g., `goto` statements) that prevent code from being recursively decomposed into divide-and-conquer provable units.

# @Objectives
- Eliminate all unrestrained and undisciplined transfers of control within the codebase.
- Enforce rigid Functional Decomposition to break large problems into the smallest possible provable units.
- Construct all programmatic logic strictly using the minimum set of control structures: sequence, selection, and iteration.
- Architect modules, components, and services at the macro-level to be highly testable and easily falsifiable.
- Treat software validation as a scientific process: write tests designed specifically to show the presence of bugs (falsify the code) rather than attempting to prove their absence.

# @Guidelines
- **Control Structure Restriction**: The AI MUST NEVER generate code that uses `goto` statements, unrestrained jumps, or unstructured breaks that emulate unrestrained jumps. 
- **Algorithmic Construction**: The AI MUST build all algorithms using ONLY sequence, selection, and iteration. No other control flow mechanisms are permitted for core logic.
- **Recursive Functional Decomposition**: When presented with a complex feature or requirement, the AI MUST recursively decompose the problem. It MUST NOT write monolithic functions. Every high-level function MUST be broken down into a hierarchy of tiny, lower-level functions.
- **Design for Falsifiability (Micro-level)**: Every generated function MUST be small enough and restricted enough in control flow that it can be treated as a "provable unit" subjected to falsification.
- **Design for Falsifiability (Macro-level)**: When designing software architecture, the AI MUST define boundaries for modules, components, and services specifically to make them easily falsifiable (testable). Testability is a primary driver of architectural structure.
- **Testing as Science**: The AI MUST design tests with the mindset of the scientific method. Tests MUST be written to aggressively attempt to prove the program incorrect. The AI MUST recognize that passing tests do not prove mathematical correctness; they only prove the code is "correct enough for our purposes" because it survived falsification.

# @Workflow
1. **Analyze Requirements**: Ingest the large-scale problem statement or system requirement.
2. **Perform Functional Decomposition**:
   - Define the highest-level function that represents the problem.
   - Recursively break this high-level function down into constituent lower-level functions.
   - Continue decomposition until the resulting functions perform a single, easily testable concept.
3. **Restrict Control Flow**: Implement the decomposed functions strictly utilizing:
   - *Sequence*: Linear, step-by-step logic.
   - *Selection*: `if/then/else` logic.
   - *Iteration*: `do/while/for` loops.
4. **Architect for Falsifiability**: Group the decomposed functions into modules and components. Expose APIs and interfaces that allow these components to be tested in isolation.
5. **Implement Falsification (Testing)**:
   - Generate automated tests for every tiny provable unit.
   - Design each test to actively attempt to break the function (prove it incorrect).
   - Once the function passes all aggressive falsification attempts, deem it correct enough for production.

# @Examples (Do's and Don'ts)

**[DO]** Use functional decomposition and strict control structures to create small, falsifiable units.
```python
# Do: Functional Decomposition with Sequence, Selection, and Iteration
def process_transactions(transactions):
    valid_transactions = filter_valid(transactions)
    apply_discounts(valid_transactions)
    return calculate_total(valid_transactions)

def filter_valid(transactions):
    valid = []
    for tx in transactions:          # Iteration
        if is_valid(tx):             # Selection
            valid.append(tx)         # Sequence
    return valid

def is_valid(tx):
    return tx.amount > 0 and tx.status == 'PENDING'

def apply_discounts(transactions):
    for tx in transactions:
        if tx.customer.is_vip():
            tx.amount *= 0.90

def calculate_total(transactions):
    total = 0
    for tx in transactions:
        total += tx.amount
    return total

# Falsification (Test)
def test_filter_valid_removes_invalid_transactions():
    # Attempting to prove the function false by feeding it edge cases
    txs = [Tx(-10, 'PENDING'), Tx(50, 'FAILED'), Tx(100, 'PENDING')]
    assert len(filter_valid(txs)) == 1
```

**[DON'T]** Write monolithic functions with complex, untestable control flows or unrestrained jumps.
```python
# Don't: Monolithic, unstructured code that is mathematically unprovable and hard to falsify
def process_transactions(transactions):
    total = 0
    i = 0
    # Anti-pattern: Simulating unrestrained jumps/lack of decomposition
    while True:
        if i >= len(transactions):
            break
        
        tx = transactions[i]
        
        if tx.amount <= 0:
            i += 1
            continue # Unstructured jump bypassing logic
            
        if tx.status != 'PENDING':
            i += 1
            continue
            
        if tx.customer.is_vip():
            tx.amount *= 0.90
            
        total += tx.amount
        i += 1
        
    return total
```