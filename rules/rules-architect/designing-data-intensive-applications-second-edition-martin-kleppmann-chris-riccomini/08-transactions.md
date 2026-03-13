# @Domain
Trigger these rules when writing database queries, configuring Object-Relational Mapping (ORM) frameworks, designing data models, implementing state-mutating application logic, debugging concurrency issues, or designing distributed data architectures.

# @Vocabulary
*   **Transaction**: A logical unit that groups several database reads and writes together to be executed as one operation, ending in either a commit or an abort (rollback).
*   **ACID**: The safety guarantees provided by transactions: Atomicity, Consistency, Isolation, and Durability.
*   **Atomicity**: An all-or-nothing guarantee. If a transaction fails halfway through, the database aborts and discards/undoes any writes made so far, preventing partial updates.
*   **Consistency**: An application-specific guarantee that data invariants (e.g., balanced accounts) remain true before and after a transaction.
*   **Isolation**: The guarantee that concurrently executing transactions do not step on each other's toes.
*   **Durability**: The promise that once a transaction commits, its writes will not be lost (via writing to disk/WAL or replication).
*   **Dirty Read**: Reading data from another transaction that has not yet been committed.
*   **Dirty Write**: Overwriting data that was written by another transaction that has not yet been committed.
*   **Read Skew (Nonrepeatable Read)**: A timing anomaly where a client sees different parts of the database at different points in time during a single transaction.
*   **Snapshot Isolation**: An isolation level where a transaction reads from a consistent snapshot of the database at the time it started. Writers do not block readers, and readers do not block writers.
*   **MVCC (Multi-Version Concurrency Control)**: The technique used to implement snapshot isolation by keeping several committed versions of a row side-by-side.
*   **Lost Update**: A concurrency anomaly where two transactions execute a read-modify-write cycle concurrently, and one clobbers the other's changes because it based its write on an outdated read.
*   **Write Skew**: A concurrency anomaly where a transaction reads a premise, makes a decision, and writes a result, but the premise is concurrently invalidated by another transaction before the commit.
*   **Phantom**: When a write in one transaction changes the result of a search query in another transaction, often causing write skew.
*   **Materializing Conflicts**: A workaround for phantoms that involves creating an artificial table of locks (e.g., all combinations of meeting rooms and time slots) so transactions have a concrete object to lock.
*   **Serializability**: The strongest isolation level, guaranteeing that concurrent transactions have the exact same effect as if they had run serially (one after the other).
*   **Two-Phase Locking (2PL)**: A pessimistic concurrency control mechanism where writers block both readers and writers, and readers block writers, using shared and exclusive locks.
*   **Index-Range Lock (Next-Key Lock)**: A lock applied to a range of values in an index to prevent phantom inserts within that range.
*   **Serializable Snapshot Isolation (SSI)**: An optimistic concurrency control algorithm that detects serialization conflicts (stale MVCC reads or writes affecting prior reads) at commit time and aborts conflicting transactions.

# @Objectives
*   Ensure data integrity by strictly grouping dependent multi-object operations into atomic transactions.
*   Systematically identify and prevent concurrency anomalies (dirty reads, dirty writes, read skew, lost updates, write skew, and phantoms).
*   Select and explicitly enforce the appropriate database isolation level or locking mechanism based on the specific read-modify-write or decision-making patterns in the code.
*   Implement robust, safe, and side-effect-free retry logic for aborted transactions.

# @Guidelines
*   **Multi-Object Updates**: The AI MUST group writes to multiple related objects (e.g., foreign key relationships, denormalized counters, secondary indexes) within a single transaction to guarantee Atomicity.
*   **Error Handling and Retries**: The AI MUST implement application-level retry logic for transaction aborts. 
    *   Limit the number of retries and use exponential backoff to prevent overload/feedback loops.
    *   Do NOT retry after permanent errors (e.g., constraint violations).
*   **External Side Effects**: The AI MUST NOT place external side effects (e.g., sending emails, charging credit cards) inside a database transaction block, because an aborted and retried transaction would cause the side effect to occur multiple times.
*   **Preventing Lost Updates**:
    *   Whenever possible, the AI MUST use atomic database operations (e.g., `UPDATE counters SET value = value + 1`) instead of pulling data into the application, modifying it, and writing it back.
    *   When atomic operations are impossible, the AI MUST use explicit locking (e.g., `SELECT FOR UPDATE`) to force sequential read-modify-write cycles.
    *   The AI MUST be highly suspicious of ORM-generated read-modify-write cycles and explicitly override them with atomic updates or locks when concurrent modifications are possible.
    *   Alternatively, the AI MAY use conditional writes (Compare-and-Swap / optimistic locking using version numbers), ensuring the code checks if the update succeeded and retries if it failed.
*   **Preventing Write Skew and Phantoms**:
    *   If the application makes a write based on the absence of a condition (e.g., checking if a username is available, or if a room is double-booked), the AI MUST recognize this as a phantom/write-skew risk.
    *   To prevent write skew, the AI MUST use Serializable isolation if the database supports it efficiently.
    *   If Serializable isolation is unavailable or performantly prohibitive, the AI MUST use explicit locks (`SELECT FOR UPDATE`) on the rows that the transaction depends on.
    *   If there are no rows to lock (a phantom insert scenario), the AI MUST use unique constraints where applicable.
    *   As an absolute last resort, the AI MAY materialize conflicts by creating a dedicated lock table for the specific conflict dimensions.
*   **Serial Execution Environments**: If working with a system that executes transactions serially on a single thread (e.g., Redis, VoltDB):
    *   The AI MUST NOT write interactive, multi-statement transactions that wait for application/network I/O.
    *   The AI MUST encapsulate the entire transaction logic into a stored procedure (e.g., Lua, Java) to execute atomically in memory.
*   **SSI (Serializable Snapshot Isolation)**: If the target database uses SSI (e.g., CockroachDB, PostgreSQL Serializable mode), the AI MUST ensure that read-write transactions are kept as short as possible to minimize the abort rate, while relying on the database to automatically abort transactions with outdated premises.

# @Workflow
1.  **Scope the Transaction**: Analyze the user's request to identify all database objects being read and written. Group dependent mutations into a single transactional boundary.
2.  **Analyze Concurrency Risk**: Evaluate the workflow for:
    *   *Read-Modify-Write*: Is data read into memory, modified, and written back? (Risk: Lost Update).
    *   *Premise-Based Writes*: Is a read query used to make a conditional decision to write? (Risk: Write Skew / Phantoms).
3.  **Apply Concurrency Controls**:
    *   If *Lost Update* risk: Refactor to atomic SQL update. If not possible, apply `SELECT FOR UPDATE` or optimistic version locking.
    *   If *Write Skew* risk: Enforce Serializable isolation level. If unfeasible, apply index-range locks or unique DB constraints.
4.  **Refactor Side Effects**: Scan the transaction block for non-database side effects (e.g., API calls, notifications). Move these *after* the transaction successfully commits.
5.  **Implement Retry Shell**: Wrap the transaction execution in a retry block that catches serialization/deadlock abort exceptions and retries with exponential backoff.

# @Examples (Do's and Don'ts)

## Preventing Lost Updates
**[DO]** Use database atomic operations or explicit locks.
```sql
-- Approach 1: Atomic update
UPDATE figures SET position = 'c4' WHERE id = 1234;

-- Approach 2: Explicit locking
BEGIN TRANSACTION;
SELECT * FROM figures WHERE name = 'robot' AND game_id = 222 FOR UPDATE;
UPDATE figures SET position = 'c4' WHERE id = 1234;
COMMIT;
```

**[DON'T]** Perform read-modify-write in application memory without locks, especially using standard ORM methods.
```javascript
// ANTI-PATTERN: Prone to Lost Updates
const figure = await db.figures.findOne({ id: 1234 });
figure.position = 'c4';
await db.figures.save(figure); 
```

## Preventing Write Skew and Phantoms
**[DO]** Rely on unique constraints or serializable isolation when making decisions based on the absence of records.
```sql
-- Safest approach for claiming a username or preventing double-booking:
-- 1. Rely on a UNIQUE constraint on the database level.
ALTER TABLE users ADD CONSTRAINT unique_username UNIQUE (username);

-- 2. Use Serializable Isolation
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN TRANSACTION;
SELECT count(*) FROM bookings WHERE room_id = 123 AND start_time < '13:00' AND end_time > '12:00';
-- If 0, insert
INSERT INTO bookings (room_id, start_time, end_time) VALUES (123, '12:00', '13:00');
COMMIT;
```

**[DON'T]** Rely on simple select checks in standard (Read Committed / Snapshot) isolation levels to prevent phantom inserts.
```sql
-- ANTI-PATTERN: Write skew vulnerability under Snapshot Isolation
BEGIN TRANSACTION;
SELECT count(*) FROM bookings WHERE room_id = 123 AND time = '12:00';
-- Concurrent transaction can insert here before this transaction commits!
INSERT INTO bookings (room_id, time) VALUES (123, '12:00'); 
COMMIT;
```

## Handling Side Effects in Transactions
**[DO]** Execute external side effects only after the transaction is durably committed.
```python
def process_order(order_id):
    while True:
        try:
            with db.transaction():
                # DB logic only
                db.execute("UPDATE inventory ...")
                db.execute("INSERT INTO orders ...")
            break # Commit successful
        except SerializationError:
            time.sleep(backoff())
            continue
            
    # Send email OUTSIDE the retryable transaction block
    send_confirmation_email(order_id)
```

**[DON'T]** Trigger emails or API calls inside the transaction, which causes duplicates upon aborts and retries.
```python
def process_order(order_id):
    with db.transaction():
        db.execute("UPDATE inventory ...")
        db.execute("INSERT INTO orders ...")
        # ANTI-PATTERN: If the transaction aborts after this line, the email is sent, 
        # and when retried, a second email will be sent!
        send_confirmation_email(order_id) 
```