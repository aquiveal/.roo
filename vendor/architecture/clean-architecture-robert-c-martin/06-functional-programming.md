# @Domain
These rules MUST be activated whenever the AI is tasked with writing, refactoring, or reviewing code involving concurrency, multithreading, state management, algorithmic loops, functional programming paradigms (e.g., Lisp, Clojure, or functional features in Java/other languages), or data storage architectures. They are especially critical when the user explicitly requests event sourcing, race condition debugging, or the decoupling of stateful and stateless components.

# @Vocabulary
- **Functional Programming**: A programming paradigm that imposes strict discipline upon variable assignment, based on lambda-calculus.
- **Immutability**: The core principle that variables do not vary; their values are initialized once and never modified.
- **Mutable Variable**: A variable that changes state during the execution of a program. It is the sole root cause of all race conditions, deadlock conditions, and concurrent update problems.
- **Segregation of Mutability**: The architectural pattern of separating an application into immutable (purely functional) components and mutable components.
- **Transactional Memory**: A system that protects mutable variables from concurrent updates and race conditions by treating memory like a database, utilizing transaction- or retry-based schemes.
- **Atom**: A specific type of variable wrapper that allows its value to mutate only under strict, transactionally enforced disciplines.
- **Compare and Swap**: An algorithm used by transactional memory (e.g., `swap!`) where a value is read, passed to a pure function to compute a new value, locked, compared to the original read value, and written only if the original value remains unchanged. If changed, the operation unlocks and retries from the beginning.
- **Event Sourcing**: A data storage strategy where transactions are stored sequentially rather than storing the mutated state. Current state is derived by applying all transactions from the beginning of time.
- **CR (Create, Read) Application**: An application utilizing Event Sourcing where data is only appended (Created) and queried (Read). It explicitly lacks Update and Delete operations, completely avoiding concurrent update issues.

# @Objectives
- Eliminate race conditions, deadlocks, and concurrent update problems at the architectural level by aggressively minimizing and isolating mutable variables.
- Maximize the proportion of the codebase that resides in purely functional, immutable components.
- Ensure that any unavoidable state mutation is strictly segregated and safeguarded by robust transactional memory mechanisms.
- Transform traditional CRUD-based state management into append-only Event Sourcing architectures whenever storage constraints permit.

# @Guidelines
- **Impose Discipline on Assignment**: The AI MUST strictly limit the use of assignment statements. Variables MUST be treated as immutable by default.
- **Abolish Mutable Loops**: The AI MUST avoid standard iteration structures that rely on mutable loop control variables (e.g., traditional `for` or `while` loops). Instead, the AI MUST utilize infinite lists, maps, filters, reductions, and recursive functions.
- **Segregate Mutability**: The AI MUST explicitly divide the system into immutable components and mutable components. These two domains must not be arbitrarily mixed.
- **Push Logic to Immutable Components**: The AI MUST drive as much processing logic and code as possible *out* of the mutable components and push it into the purely functional, immutable components.
- **Protect Mutable Variables**: When variables MUST mutate, the AI MUST encapsulate them in transactional memory structures (e.g., Atoms) and update them using retry-based algorithms like Compare and Swap.
- **Use Event Sourcing for State**: Instead of updating a database record to reflect a new state, the AI MUST store the transaction that caused the state change.
- **Calculate State on Demand**: To retrieve state in an Event Sourcing system, the AI MUST compute it by aggregating all historical transactions. If performance dictates, the AI MAY cache state at fixed intervals (e.g., every midnight) and compute only the transactions occurring after the cached point.
- **Enforce CR over CRUD**: Data stores in functional architectures MUST be strictly Create and Read. The AI MUST NOT write `UPDATE` or `DELETE` statements for event-sourced entities.

# @Workflow
1. **State Requirements Analysis**: When designing a module or algorithm, explicitly identify all points where data changes over time.
2. **Functional Transformation**: Rewrite the algorithmic flow to eliminate mutable variables. Replace imperative loops with functional equivalents (e.g., mapping a pure function over a lazy sequence or range).
3. **Component Segregation**: If mutation is fundamentally required by the system, draw a strict architectural boundary. Place all pure business logic in an immutable component. Place the mutable state in a separate component.
4. **Transactional Implementation**: Within the mutable component, wrap all state variables in concurrency-safe transactional wrappers (e.g., atomic references). Implement state transitions exclusively via pure functions passed into Compare-and-Swap updaters.
5. **Data Layer Conversion**: Evaluate the database interaction. Convert CRUD-based tables into append-only Event Sourcing ledgers. Remove all SQL `UPDATE` and `DELETE` commands.
6. **State Hydration Logic**: Write functions that derive the current state by reading the append-only event ledger and applying a fold/reduce operation over the transaction history.

# @Examples (Do's and Don'ts)

## 1. Loop Control and Immutability
- **[DON'T]** Use mutable loop control variables that change state during execution.
  ```java
  // Anti-pattern: Mutable variable 'i' causes state changes
  public class Squint {
    public static void main(String args[]) {
      for (int i=0; i<25; i++)
        System.out.println(i*i);
    }
  }
  ```
- **[DO]** Use functional sequences and higher-order functions where variables are initialized but never modified.
  ```clojure
  ;; Correct: Purely functional approach using immutable sequences
  (println 
    (take 25 
      (map (fn [x] (* x x)) 
        (range))))
  ```

## 2. Managing Concurrency and State Mutation
- **[DON'T]** Directly reassign shared variables, exposing the system to race conditions and concurrent update problems.
  ```javascript
  // Anti-pattern: Direct mutation of shared state
  let counter = 0;
  function increment() {
      counter = counter + 1; // Vulnerable to race conditions
  }
  ```
- **[DO]** Segregate the mutable state and protect it using transactional memory concepts (e.g., Compare and Swap).
  ```clojure
  ;; Correct: Using an atom and a transactional swap! mechanism
  (def counter (atom 0))
  (swap! counter inc) ;; Safely increments using Compare and Swap
  ```

## 3. Database State Management
- **[DON'T]** Update existing records in place (CRUD), destroying historical context and risking concurrent update anomalies.
  ```sql
  -- Anti-pattern: Mutating state directly in the database
  UPDATE accounts SET balance = balance - 100 WHERE account_id = 123;
  ```
- **[DO]** Utilize Event Sourcing to strictly append transactions (CR), computing the state dynamically.
  ```sql
  -- Correct: Append-only Event Sourcing (Create/Read only)
  INSERT INTO account_transactions (account_id, amount, type, timestamp) 
  VALUES (123, -100, 'WITHDRAWAL', NOW());

  -- State is computed via read:
  SELECT SUM(amount) FROM account_transactions WHERE account_id = 123;
  ```