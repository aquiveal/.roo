@Domain
These rules MUST trigger when the AI is tasked with designing, implementing, refactoring, or reviewing session management, state persistence, distributed system communication, Web application data flow, or handling the transition between pending uncommitted data and permanent record data.

@Vocabulary
*   **Session State**: Data that is relevant only to a particular active session and separated from other sessions and their business transactions.
*   **Record Data**: Long-term persistent data held in the database, visible to all sessions and verified by system integrity rules.
*   **Client Session State**: A pattern where session data is stored on the client (via URL parameters, hidden fields, cookies, or rich client objects) and sent to the server with each request.
*   **Server Session State**: A pattern where session state is kept on a server system (in memory or serialized to a shared data source) identified by a session ID.
*   **Database Session State**: A pattern where session data is stored as committed data in the database, requiring isolation from record data.
*   **Data Transfer Object (DTO)**: An object that carries data between processes to reduce the number of method calls, heavily utilized to serialize Client Session State over the wire.
*   **Memento**: A pattern used to serialize Server Session State into a persistent storage format to free up memory resources.
*   **Serialized LOB (Large OBject)**: A database field storing an entire serialized object graph (BLOB for binary, CLOB for text/XML), often used to persist session state in a database without tabularizing it.
*   **Server Affinity (Sticky Sessions)**: A clustering configuration that forces one server to handle all requests for a particular session, which hinders failover resiliency.
*   **Session Migration**: The ability for a session to move from server to server, enabling load balancing and failover.
*   **Session Stealing**: A security breach where a malicious user alters their session ID to hijack another user's session.
*   **Pending Tables**: Exact clones of real database tables used to store isolated session data before it is committed as Record Data.
*   **Pending Field**: A field (Boolean or Session ID) added to standard database tables to differentiate uncommitted session data from Record Data.

@Objectives
*   Achieve stateless server objects wherever possible to maximize clustering, load balancing, and failover resiliency.
*   Secure all session state transferred across the network against inspection, alteration, and session stealing.
*   Strictly isolate uncommitted session data from permanent Record Data to prevent dirty reads and application-wide data corruption.
*   Balance network bandwidth, server memory, and database I/O when choosing the location to store session state.
*   Implement robust cleanup mechanisms for abandoned or canceled sessions to prevent resource exhaustion and database contention.

@Guidelines

**1. Client Session State Rules**
*   When implementing Client Session State, the AI MUST use a Data Transfer Object (DTO) to serialize and transfer the data over the wire.
*   The AI MUST NOT store session state in the visual fields/widgets of a rich-client interface; it MUST use nonvisual objects (DTOs or Domain Models).
*   For HTML interfaces, the AI MUST choose the storage mechanism based on data size and context:
    *   **URL Parameters**: Use ONLY for minimal data (e.g., Session ID). The AI MUST NOT use this for consumer-facing sites where users bookmark pages, as the session state will be incorrectly bookmarked.
    *   **Hidden Fields**: Use `<INPUT type="hidden">` with XML or text encoding. The AI MUST prevent data loss scenarios where a user navigates to a static HTML page that lacks the hidden field routing.
    *   **Cookies**: The AI MUST account for size limits and users disabling cookies. The AI MUST implement URL rewriting as a fallback if cookies are disabled.
*   **Security constraints**: The AI MUST assume all client-side data is vulnerable to prying and alteration. The AI MUST encrypt any sensitive session data sent to the client. The AI MUST strictly revalidate all data sent back from the client before processing it on the server.
*   **Session ID constraints**: The AI MUST use random session IDs or cryptographic hashes to prevent Session Stealing.

**2. Server Session State Rules**
*   The AI MUST initially attempt to store Server Session State in an in-memory map keyed by session ID.
*   When memory resources are a concern, or when clustering/failover is required, the AI MUST serialize the session state into a Memento for persistent storage.
*   **Serialization Format constraints**: 
    *   Use Binary serialization for speed and minimal disk space. The AI MUST account for versioning fragility (changes to class structure breaking deserialization).
    *   Use Text/XML serialization for human-readability and robustness against class version changes, accepting the penalty of larger size and slower parsing.
*   **Storage Location constraints**:
    *   For single-server setups, the AI MAY store the memento on the local file system or a local database.
    *   For clustered environments (Session Migration), the AI MUST store the memento on a shared server or database to avoid Server Affinity.
*   **Cleanup constraints**: If storing Server Session State in a shared database, the AI MUST implement a cleanup mechanism for abandoned sessions. To avoid database contention, the AI SHOULD consider partitioning the session table into time-based segments (e.g., 12 segments rotated every 2 hours, deleting the oldest segment).

**3. Database Session State Rules**
*   The AI MUST explicitly separate local session data (pending) from committed Record Data.
*   **Isolation strategies**:
    *   *Pending Field (Invasive)*: The AI MAY add a `sessionID` field (or Boolean `isPending`) to existing tables. If chosen, the AI MUST modify ALL application queries that target Record Data to explicitly filter out session data (e.g., `WHERE sessionID IS NULL`).
    *   *Pending Tables (Recommended)*: The AI SHOULD create exact schema clones of the real tables, appending a `sessionID` field. The AI MUST use these pending tables to store intermediate session data.
*   **Integrity and Validation**: When using Pending Tables, the AI MUST relax database integrity and validation rules, as intermediate session state is often logically incomplete or invalid until the final commit.
*   **Rollback and Cancel**: 
    *   The AI MUST provide a mechanism to cleanly delete session data if the user cancels.
    *   If using Pending Tables, the AI MUST implement commit logic that copies data from the pending tables to the record tables upon session completion, then purges the pending data.
*   **Cleanup constraints**: The AI MUST implement a timeout daemon tracking the last interaction time to purge abandoned Database Session State.
*   *Boundary crossover*: If pending tables are ONLY ever read by the objects handling the session, the AI MUST consider using a Serialized LOB instead of tabular columns, effectively shifting the pattern to Server Session State.

@Workflow
1.  **Analyze Data Volume and Security**: Evaluate the exact size of the session data and its sensitivity. If it is a single ID or tiny non-sensitive dataset, default to Client Session State.
2.  **Evaluate Infrastructure Constraints**: Determine if the deployment environment uses a single server or a cluster. If clustered, eliminate local-memory Server Session State unless Server Affinity (sticky sessions) is strictly guaranteed and acceptable.
3.  **Select the Pattern**:
    *   Choose **Client Session State** for stateless servers, small data footprints, and high failover requirements.
    *   Choose **Server Session State** for large data footprints where database I/O must be minimized, utilizing shared storage/Serialzed LOBs for clustering.
    *   Choose **Database Session State** when the session data heavily interacts with tabular record data and high availability/failover is paramount, accepting the write-performance penalty.
4.  **Implement Security and Serialization**: For Client state, apply encryption and DTO serialization. For Server state, generate Binary or XML serialization routines.
5.  **Implement State Isolation**: For Database state, provision Pending Tables, clone the schema, and configure the mapping layer to route intermediate saves to the pending tables.
6.  **Implement Garbage Collection**: Construct timed daemons or table-rotation scripts to purge abandoned session data based on the last interaction timestamp.

@Examples (Do's and Don'ts)

*   **[DO]** Use DTOs to encapsulate session state before sending it to the client.
    ```java
    // DTO encapsulates session state for client transfer
    public class SessionStateDTO implements Serializable {
        private String sessionToken;
        private String currentStep;
        // getters and setters
    }
    ```

*   **[DON'T]** Store session state directly in UI widgets or visual interface fields.
    ```csharp
    // ANTI-PATTERN: Storing domain session state in UI fields
    public void SaveSessionState() {
        hiddenSessionData.Text = serialize(domainObject); // Do not do this!
    }
    ```

*   **[DO]** Revalidate all session data returning from the client to prevent tampering.
    ```java
    public void processClientState(SessionStateDTO state) {
        if (!SignatureValidator.isValid(state)) {
            throw new SecurityException("Client state tampering detected.");
        }
        // process state
    }
    ```

*   **[DON'T]** Use the "Pending Field" approach in Database Session State without rigorously updating all application queries.
    ```sql
    -- ANTI-PATTERN: Querying record data without filtering out pending session data
    SELECT * FROM orders WHERE customer_id = 123; 
    -- This will accidentally return uncommitted session data if a Pending Field is used!
    ```

*   **[DO]** Clone tables for Database Session State to isolate uncommitted data and relax constraints.
    ```sql
    -- Standard Record Table
    CREATE TABLE orders (id INT PRIMARY KEY, amount DECIMAL NOT NULL);

    -- Pending Table for Database Session State (Constraints relaxed)
    CREATE TABLE pending_orders (
        session_id VARCHAR(255),
        id INT, 
        amount DECIMAL, -- NOT NULL removed for intermediate state
        last_interaction TIMESTAMP
    );
    ```

*   **[DO]** Rotate table segments to efficiently clean up Server/Database Session State without locking contention.
    ```sql
    -- Drop the oldest segment table completely instead of running massive DELETE queries
    DROP TABLE session_state_segment_1;
    CREATE TABLE session_state_segment_1 (...);
    ```

*   **[DON'T]** Use Binary serialization for Server Session State if the class schema is volatile and sessions must survive application upgrades. XML/Text serialization MUST be used in volatile environments.