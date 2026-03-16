# @Domain
When the AI is designing, refactoring, or implementing web application architecture, handling user sessions across multiple requests, managing state in stateless environments (like HTTP), or configuring server, client, and database interactions for business transactions.

# @Vocabulary
- **Stateless Server**: A server object that does not retain state between requests. Its fields are undefined between invocations, allowing the object to be pooled to service multiple users, thus improving resource efficiency.
- **Stateful Server**: A server object that retains state between requests for a specific user session, requiring one server object per active user, which limits scalability.
- **Session State**: Data relevant only to a particular active session and business transaction. It represents uncommitted, intermediate data.
- **Record Data**: Long-term, persistent data held in the database that is visible to all sessions and represents the official committed state of the system.
- **Client Session State**: A pattern where session state is stored on the client (via URL parameters, hidden fields, or cookies) and transferred to the server with each request.
- **Server Session State**: A pattern where session state is held in memory on the application server or serialized to a durable server-side store between requests.
- **Database Session State**: A pattern where session state is broken into tables and fields and stored in a database, similar to lasting record data.
- **Session Migration**: The ability for a session to move from one application server to another within a cluster across different requests.
- **Server Affinity**: Forcing a specific client to interact with only one specific server for the duration of a session (often problematic with proxies like AOL).
- **Pending Tables**: Exact structural clones of real database tables used exclusively to store uncommitted Database Session State data.
- **Session Stealing**: A security breach where a malicious user modifies their session ID to hijack another user's session.

# @Objectives
- Maximize the use of Stateless Servers to pool resources and improve scalability while accurately maintaining inherently stateful business transactions.
- Strictly isolate Session State from Record Data to prevent inconsistent reads and corrupted database states.
- Secure Client Session State against tampering, spoofing, and unauthorized access.
- Ensure clustering and failover resiliency through appropriate state serialization and distribution.
- Prevent memory leaks and database contention by rigorously implementing cleanup mechanisms for abandoned sessions.

# @Guidelines

## General Session Management
- The AI MUST NOT treat performance-enhancing data caches as Session State. Session State is strictly data required between requests for correct behavior.
- The AI MUST ALWAYS use Client Session State to store the session identifier (Session ID), regardless of which pattern is used for the rest of the state.
- The AI MUST generate randomized or cryptographically hashed Session IDs to prevent Session Stealing.

## Client Session State
- The AI MUST NOT use Client Session State for large amounts of data (e.g., > a few kilobytes) to avoid excessive bandwidth consumption and latency on every request.
- The AI MUST assume all data sent to the client is vulnerable to inspection and tampering.
- The AI MUST encrypt all sensitive Session State data stored on the client.
- The AI MUST revalidate all Client Session State data upon its return to the server; it must never be blindly trusted.
- When using URL parameters, the AI MUST NOT use them for consumer sites where users might bookmark the URL with stale or inappropriate session data.
- When using hidden fields, the AI MUST serialize the data into a format (like XML or a compressed text encoding) and parse it on the server.
- The AI MUST account for users disabling cookies. If cookies are used, the system should fall back to URL rewriting if cookies are disabled.

## Server Session State
- If the application requires clustering or failover (Session Migration), the AI MUST NOT store Server Session State exclusively in local application server memory.
- For clustered environments, the AI MUST serialize the Server Session State to a memento (binary or textual/XML) and store it in a shared data source (e.g., a shared database table with a Serialized LOB).
- The AI MUST implement an automatic timeout and cleanup mechanism to handle abandoned sessions.
- If storing Server Session State in a database, the AI MUST mitigate contention on the session table. (e.g., implement a time-segmented partitioning strategy, such as rotating segments every two hours and dropping the oldest).

## Database Session State
- The AI MUST strictly isolate pending Session State from committed Record Data.
- The AI MUST use one of two methods for Database Session State isolation: 
  1. **Pending Fields**: Adding a `sessionID` field to record tables. All queries for Record Data MUST filter out rows where `sessionID is not NULL`.
  2. **Pending Tables** (Preferred): Creating exact clones of the record tables appended with a `sessionID` field.
- The AI MUST NOT apply strict record-data integrity and validation rules to pending Database Session State data, as intermediate states are often legally invalid until the final commit.
- The AI MUST implement a daemon or cron job to periodically sweep and delete Database Session State rows linked to abandoned `sessionID`s, based on a "last interaction" timestamp.
- The AI MUST implement server-side caching of the Database Session State to mitigate the performance cost of pulling data in and out of the database on every request.
- When updating existing Record Data within a session, the AI MUST copy the existing data to the pending state, modify it there, and commit it back to the record tables only at the end of the session.

# @Workflow
1. **Analyze State Requirements**: Separate the application's data into Record Data (lasting, shared), Cache Data (performance, safely discardable), and Session State (uncommitted business transaction data).
2. **Determine Statelessness**: Design server objects to be stateless by default. Only implement Session State patterns when the business interaction (e.g., a shopping cart) inherently requires it.
3. **Evaluate Trade-offs for Pattern Selection**:
   - *Choose Client Session State* if the data is extremely small (e.g., just an ID), server memory is limited, and the data is non-sensitive or can be cheaply encrypted.
   - *Choose Server Session State* if rapid performance is required, data is complex/large, and development effort must be minimized. Serialize to a shared store if Session Migration/clustering is required.
   - *Choose Database Session State* if you have large amounts of idle users, require robust failover, and the data easily maps to tabular formats.
4. **Implement Isolation and Security**: If using Client state, implement encryption and validation. If using Database state, implement Pending Tables.
5. **Establish Lifecycle and Cleanup**: Implement timeout mechanisms. Write daemons or scheduled tasks to purge abandoned session data from databases or shared server stores.
6. **Commit Phase**: Write the logic to transform the Session State into Record Data (enforcing all business and integrity validations) upon the user confirming the business transaction.

# @Examples (Do's and Don'ts)

## Client Session State
- **[DO]** Store only a randomized, hashed session identifier in a secure HTTP-only cookie, keeping the heavy data on the server.
```java
Cookie sessionCookie = new Cookie("SESSION_ID", secureRandomHash());
sessionCookie.setHttpOnly(true);
sessionCookie.setSecure(true);
response.addCookie(sessionCookie);
```
- **[DON'T]** Serialize a massive, unencrypted object graph into a hidden HTML field or cookie.
```html
<!-- ANTI-PATTERN: Exposing vulnerable, unencrypted, bloated session state -->
<input type="hidden" name="sessionData" value="{ 'user_id': 123, 'cart_total': 500, 'discount_applied': true, 'items': [...] }">
```

## Server Session State
- **[DO]** Serialize Server Session State to a shared repository if operating in a clustered environment, ensuring Session Migration is possible if a node dies.
```java
// Serializing session state to a shared data store for clustered environments
public void saveSessionState(String sessionId, SessionData data) {
    byte[] serializedData = serializeToMemento(data);
    sharedDatabase.storeSessionBlob(sessionId, serializedData, System.currentTimeMillis());
}
```
- **[DON'T]** Rely strictly on local RAM for Server Session State if the architecture requires robust failover, as a server crash will destroy the ongoing business transaction.
```java
// ANTI-PATTERN: Using local memory in a clustered environment without Server Affinity guarantees
private static Map<String, SessionData> localMemorySessionStore = new ConcurrentHashMap<>();
```

## Database Session State
- **[DO]** Use isolated "Pending Tables" to store Database Session State, preventing dirty reads by other system components querying Record Data.
```sql
-- Record Table
CREATE TABLE orders (id INT PRIMARY KEY, customer_id INT, total DECIMAL);

-- Pending Table for Database Session State
CREATE TABLE pending_orders (session_id VARCHAR, id INT, customer_id INT, total DECIMAL, last_interaction TIMESTAMP);
```
- **[DON'T]** Mingle session data with record data without a foolproof filtering mechanism, allowing incomplete, unvalidated session data to appear in global application reports.
```sql
-- ANTI-PATTERN: Mixing pending session data into record tables without strict filtering
INSERT INTO orders (id, customer_id, status) VALUES (999, 123, 'PENDING_IN_CART');
-- A financial report query might accidentally sum this uncommitted order.
```

## Handling Abandonment
- **[DO]** Implement a scheduled job that deletes orphaned session data based on a timestamp to prevent database/memory exhaustion.
```java
public void cleanupAbandonedSessions() {
    long timeoutThreshold = System.currentTimeMillis() - (30 * 60 * 1000); // 30 mins
    database.execute("DELETE FROM pending_orders WHERE last_interaction < ?", timeoutThreshold);
}
```