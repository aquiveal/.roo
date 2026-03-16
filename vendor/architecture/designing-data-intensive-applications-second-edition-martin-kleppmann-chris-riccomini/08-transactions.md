# @Domain
These rules MUST be activated whenever the AI is tasked with writing database access code, designing database schemas, implementing Object-Relational Mapping (ORM) logic, writing concurrent data manipulation logic, configuring database isolation levels, or handling error/retry logic for data persistence operations.

# @Vocabulary
- **Transaction**: A way to group several database reads and writes into a single logical unit that either entirely succeeds (commit) or entirely fails (abort/rollback).
- **ACID**: The safety guarantees provided by transactions: Atomicity, Consistency, Isolation, and Durability.
- **Atomicity**: The ability to abort a transaction on error and discard/undo all writes made up to that point, saving the application from partial failure states.
- **Consistency**: An application-specific notion of the database being in a "good state" preserving data invariants. 
- **Isolation**: The guarantee that concurrently executing transactions do not step on each other's toes (e.g., serializability).
- **Durability**: The promise that once a transaction commits, data is not lost despite hardware faults or crashes.
- **Dirty Read**: A transaction reading data written by another transaction that has not yet committed.
- **Dirty Write**: A transaction overwriting data written by another transaction that has not yet committed.
- **Read Skew (Nonrepeatable Read)**: A client observing the database in an inconsistent state across multiple queries due to concurrent commits.
- **Snapshot Isolation**: An isolation level where each transaction reads from a consistent snapshot of the database from the moment the transaction started. Readers do not block writers, and writers do not block readers.
- **MVCC (Multi-Version Concurrency Control)**: The mechanism used to implement Snapshot Isolation by keeping multiple committed versions of a row side-by-side.
- **Lost Update**: Two clients concurrently perform a read-modify-write cycle, and one clobbers the other's write.
- **Write Skew**: A concurrency anomaly where a transaction reads data, makes a decision based on that premise, and writes the decision, but the premise becomes false before the commit.
- **Phantom Read**: A write in one transaction changes the result of a search query in another concurrent transaction.
- **Serializability**: The strongest isolation level, ensuring concurrent transactions have the same effect as if they executed serially (one at a time).
- **Two-Phase Locking (2PL)**: A pessimistic concurrency control mechanism where writers block readers and readers block writers using shared and exclusive locks.
- **Predicate Lock / Index-Range Lock**: Locks applied to a search condition (or index range) rather than a specific object, used to prevent phantoms.
- **Serializable Snapshot Isolation (SSI)**: An optimistic concurrency control algorithm that detects stale reads and writes affecting prior reads, aborting transactions only if execution was not serializable.

# @Objectives
- Systematically prevent concurrency bugs (dirty reads, lost updates, write skew, and phantoms) by selecting the appropriate transaction isolation level and concurrency control mechanisms.
- Guarantee data integrity by encapsulating multi-object operations within atomic transactions.
- Implement robust error handling that safely retries aborted transactions while handling external side-effects and system overload appropriately.
- Avoid the impedance mismatch of ORM-generated read-modify-write cycles by favoring atomic database operations or explicit locking when dealing with concurrent state mutations.

# @Guidelines
- **Define Transaction Boundaries**: The AI MUST group all database writes that must remain in sync (e.g., foreign key references, denormalized data, counter updates) into a single explicit transaction.
- **Do Not Confuse Single-Object Operations with Transactions**: The AI MUST NOT treat single-object atomic operations (e.g., CAS, increment) as a substitute for multi-object transactions when multiple distinct objects must be updated atomically.
- **Handle Aborts and Retries Safely**: 
  - The AI MUST implement retry loops for database operations that fail due to transient errors (deadlocks, isolation violations, network timeouts).
  - The AI MUST use exponential backoff to prevent retry storms during system overload.
  - The AI MUST NOT place external side-effects (e.g., sending an email, calling a third-party API) directly inside a retriable transaction block, as the side-effect will trigger multiple times if the transaction aborts and retries.
- **Prevent Lost Updates**: 
  - The AI MUST avoid naive read-modify-write cycles in application code.
  - The AI MUST use database-native atomic write operations (e.g., `UPDATE ... SET x = x + 1`) whenever possible.
  - If atomic operations are not possible, the AI MUST use explicit locking (e.g., `SELECT ... FOR UPDATE`) or conditional writes (compare-and-swap) to prevent concurrent overwrites.
- **Prevent Write Skew and Phantoms**: 
  - When writing logic that follows the "Read -> Decide -> Write" pattern based on a search condition (e.g., checking if a username is taken, or a room is available), the AI MUST recognize the risk of write skew.
  - To solve write skew, the AI MUST use Serializable isolation, explicit Index-Range Locks (`SELECT FOR UPDATE`), or define database-level unique constraints.
- **Understand Isolation Level Limitations**: 
  - The AI MUST recognize that "Read Committed" does not prevent read skew or lost updates.
  - The AI MUST recognize that "Snapshot Isolation" (often confusingly named "Repeatable Read" in PostgreSQL/MySQL) prevents read skew but DOES NOT prevent write skew or phantoms.
  - The AI MUST assume that ORM frameworks default to weak isolation levels and generate code vulnerable to lost updates and write skew unless explicitly configured otherwise.
- **Select Serializability Implementations Carefully**: 
  - If high throughput is required and the dataset fits in memory, the AI MAY suggest Single-Threaded Serial Execution via Stored Procedures.
  - If read-heavy workloads require serializability, the AI SHOULD favor Serializable Snapshot Isolation (SSI) over Two-Phase Locking (2PL) to prevent writers from blocking readers.
- **Do Not Use Read Locks for Dirty Reads**: The AI MUST NOT use read locks to prevent dirty reads if the target database supports MVCC (which most modern databases do).

# @Workflow
When generating or reviewing database access code, the AI MUST follow this algorithmic process:
1. **Identify the Scope**: Determine all data objects (rows, documents) involved in the operation. If multiple objects are involved, wrap them in a transaction boundary.
2. **Analyze Concurrency Risks**: 
   - Does the logic involve reading a value, modifying it in application memory, and writing it back? (Risk: Lost Update).
   - Does the logic check a precondition (e.g., `COUNT(*) > 0`) and execute a write based on that precondition? (Risk: Write Skew / Phantoms).
3. **Select Concurrency Control**:
   - For Lost Updates: Rewrite using a single atomic SQL statement. If impossible, add `FOR UPDATE` to the read query.
   - For Write Skew: Apply a unique constraint, use `SELECT FOR UPDATE` on the condition, or set the transaction isolation level to `SERIALIZABLE`.
4. **Implement Retry Logic**: Wrap the transaction in a retry block catching specific transient database errors (e.g., serialization failures, deadlocks) and implement exponential backoff.
5. **Decouple Side-Effects**: Verify that no non-idempotent external API calls or messaging publishing steps are tightly coupled inside the transaction retry block.

# @Examples (Do's and Don'ts)

### Preventing Lost Updates
[DON'T]
```python
# Anti-pattern: Naive read-modify-write cycle (vulnerable to lost updates)
def increment_counter(db, counter_id):
    # If two threads run this concurrently, one increment is lost.
    row = db.execute("SELECT value FROM counters WHERE id = ?", counter_id)
    new_value = row['value'] + 1
    db.execute("UPDATE counters SET value = ? WHERE id = ?", new_value, counter_id)
```

[DO]
```python
# Correct: Use an atomic database operation
def increment_counter(db, counter_id):
    db.execute("UPDATE counters SET value = value + 1 WHERE id = ?", counter_id)

# Alternative Correct: Use explicit locking if application logic is complex
def apply_complex_update(db, record_id):
    with db.transaction():
        row = db.execute("SELECT value FROM records WHERE id = ? FOR UPDATE", record_id)
        new_value = complex_business_logic(row['value'])
        db.execute("UPDATE records SET value = ? WHERE id = ?", new_value, record_id)
```

### Preventing Write Skew and Phantoms
[DON'T]
```sql
-- Anti-pattern: Write skew vulnerability under Snapshot Isolation / Read Committed
BEGIN TRANSACTION;
-- 1. Check premise (e.g., are there enough doctors on call?)
SELECT COUNT(*) FROM doctors WHERE on_call = true AND shift_id = 1234;
-- 2. Application sees count >= 2, decides it is safe to remove one.
-- Concurrently, another transaction does the exact same thing.
UPDATE doctors SET on_call = false WHERE name = 'Alice' AND shift_id = 1234;
COMMIT;
-- Result: Both doctors go off call, leaving 0 doctors. Rule violated.
```

[DO]
```sql
-- Correct: Lock the rows the transaction depends on (Materializing the conflict / Index-range locking)
BEGIN TRANSACTION;
-- Lock all rows matching the condition so concurrent transactions must wait
SELECT * FROM doctors WHERE on_call = true AND shift_id = 1234 FOR UPDATE;
-- Now it is safe to evaluate the count in the application and update
UPDATE doctors SET on_call = false WHERE name = 'Alice' AND shift_id = 1234;
COMMIT;
```

### Handling Aborts and External Side Effects
[DON'T]
```python
# Anti-pattern: Side effects inside a retriable transaction
def process_order(db, order_id):
    while True:
        try:
            with db.transaction():
                db.execute("UPDATE orders SET status = 'processed' WHERE id = ?", order_id)
                # DANGER: If the transaction aborts AFTER sending the email but BEFORE commit, 
                # the retry will send multiple emails to the customer.
                send_confirmation_email(order_id) 
            break
        except SerializationFailure:
            continue
```

[DO]
```python
# Correct: Separate database transactions from external side effects
def process_order(db, order_id):
    success = False
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with db.transaction():
                db.execute("UPDATE orders SET status = 'processed' WHERE id = ?", order_id)
            success = True
            break
        except SerializationFailure:
            sleep(backoff(attempt)) # Prevent retry storm
            
    if success:
        # Safe: Email only sends once the transaction is durably committed
        send_confirmation_email(order_id)
```