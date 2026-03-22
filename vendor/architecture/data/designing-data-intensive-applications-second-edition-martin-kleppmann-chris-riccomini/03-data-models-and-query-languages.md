# @Domain
These rules are triggered whenever the AI is tasked with database architecture, data modeling, schema design, database migrations, query optimization, API data payload design, or evaluating the trade-offs between different database paradigms (e.g., Relational, NoSQL/Document, Graph, Event Sourcing, Dataframes).

# @Vocabulary
*   **Declarative Query Language**: A language (e.g., SQL, Cypher, SPARQL) where the user specifies the pattern/conditions of the desired data, allowing the database query optimizer to determine the execution algorithm.
*   **Impedance Mismatch**: The disconnect between in-memory object-oriented data structures and relational database tables, often requiring translation layers.
*   **ORM (Object-Relational Mapping)**: Frameworks that reduce boilerplate translation between objects and relations but can introduce inefficiencies (e.g., N+1 queries).
*   **Shredding**: The relational database technique of splitting a document-like, tree-structured entity into multiple separate tables with foreign key relationships.
*   **Schema-on-read**: An approach where the data structure is implicit and only interpreted by the application code when read (often incorrectly called "schemaless").
*   **Schema-on-write**: The traditional relational approach where the database explicitly enforces a schema when data is written.
*   **Data Locality**: The performance advantage gained when all relevant data (e.g., a full JSON document) is stored in one contiguous string, requiring fewer disk seeks compared to multi-table joins.
*   **Normalization**: Storing human-meaningful information in exactly one place and referencing it via IDs to ensure fast, consistent writes.
*   **Denormalization**: Duplicating data across records to speed up reads and avoid joins, at the cost of write complexity and potential inconsistency.
*   **Hydrating**: The process of looking up human-readable information by ID (essentially an application-level join) when reading denormalized or cached structures.
*   **Fact Table**: In analytics, a central table containing individual events or transactions, often extremely large.
*   **Dimension Table**: In analytics, tables containing the "who, what, where, when, how" metadata referenced by the fact table.
*   **Star Schema**: A data warehouse schema where a central fact table connects directly to surrounding dimension tables.
*   **Snowflake Schema**: A more normalized variation of a star schema where dimension tables are further broken down into sub-dimensions.
*   **One Big Table (OBT)**: An analytics schema pattern that heavily denormalizes by folding dimension data directly into the fact table.
*   **Property Graph**: A data model consisting of vertices (entities) and edges (relationships), both capable of holding key-value properties.
*   **Triple-Store**: A data model (often using RDF/Turtle) storing data as (subject, predicate, object) statements.
*   **Datalog**: A logic programming language based on Prolog used for recursive relational/graph queries via virtual derived tables.
*   **Event Sourcing**: Modeling state by storing an immutable, append-only log of fact-based events representing past actions.
*   **CQRS (Command Query Responsibility Segregation)**: Maintaining separate read-optimized representations (materialized views) derived from a write-optimized representation (event log).
*   **Dataframe**: An analytical data model representing data as tabular, in-memory structures supporting bulk operations, often transformed into matrices for machine learning.
*   **One-Hot Encoding**: A technique for transforming categorical data into numerical matrices by creating a binary column for each possible category.

# @Objectives
*   Select the correct data model based strictly on the complexity of relationships in the application (e.g., Document for 1-to-many trees, Relational for N-to-1 or N-to-M, Graph for highly interconnected N-to-M).
*   Optimize read and write performance by strategically balancing normalization (for write-heavy consistency) and denormalization (for read-heavy performance).
*   Utilize declarative query languages to delegate execution optimization to the database engine.
*   Ensure backward and forward compatibility in schema evolution, applying explicit fallback logic for schema-on-read implementations.
*   Implement event sourcing and CQRS architectures with strict determinism and immutability.
*   Transform relational data into appropriate mathematical representations (Dataframes/Matrices) when interfacing with machine learning or analytical subsystems.

# @Guidelines

## Data Model Selection
*   The AI MUST choose a **Document Model** (e.g., JSON/NoSQL) when the primary data structure is a self-contained tree of one-to-many relationships, provided the entire tree is typically loaded at once.
*   The AI MUST NOT use the Document Model if the application requires frequent updates to deeply nested items or contains genuinely large unbounded arrays (e.g., thousands of comments on a post). In such cases, the AI MUST use a relational approach.
*   The AI MUST choose a **Relational Model** when the data features many-to-one or many-to-many relationships that require frequent joins, or when referential integrity is paramount.
*   The AI MUST choose a **Graph Model** (Property Graph or Triple-Store) when the data is heterogeneous and many-to-many relationships are dominant, especially if queries require variable-length path traversals (e.g., "find all things within X degrees of separation").

## Queries and ORMs
*   When generating relational database queries via an ORM, the AI MUST proactively identify and resolve the **N+1 query problem** by explicitly enforcing eager loading or join fetches.
*   The AI MUST prefer generating **Declarative Queries** (SQL, Cypher, SPARQL) over imperative application-level filtering, allowing the database's query optimizer to handle execution plans.
*   When querying variable-length graph traversals in a relational database, the AI MUST use `WITH RECURSIVE` (recursive common table expressions), but SHOULD advise the user that dedicated graph languages (like Cypher) are vastly more concise and efficient for this task.

## Normalization vs. Denormalization
*   The AI MUST normalize data (using IDs) in OLTP systems where write performance, consistent spelling, localization, and ease of updating are the primary concerns.
*   The AI MAY denormalize data (duplicating strings/structures) in read-heavy systems or analytics environments, provided it includes a distinct, reliable mechanism to handle updates to the duplicated data (e.g., fan-out update processes).
*   When dealing with highly volatile related data (e.g., "like" counts on a social media post), the AI MUST NOT denormalize the volatile fields into cached views; instead, it MUST store only the ID and "hydrate" the volatile data via an application-level join at read time.

## Schema Evolution and Flexibility
*   When writing code for a **Schema-on-read** (Document) database, the AI MUST include application-level fallback logic to handle heterogeneous or legacy data structures (e.g., checking if an old field exists and mapping it to a new format on the fly).
*   When performing schema migrations in a **Schema-on-write** (Relational) database, the AI MUST utilize fast operations (like adding a column with a default `NULL`) and avoid long-running `UPDATE` statements that require copying the entire table, minimizing operational downtime.

## Analytics and Data Warehousing
*   When designing for analytical workloads (OLAP), the AI MUST decouple the architecture from the operational (OLTP) systems, utilizing a Data Warehouse or Data Lake.
*   The AI MUST design analytics schemas using a **Star Schema** (preferred for analyst simplicity) or **Snowflake Schema**, strictly separating Fact tables (events) from Dimension tables (metadata).
*   The AI MUST NOT use "SELECT *" in analytical queries; it MUST explicitly name only the 4 or 5 required columns to leverage the performance benefits of underlying columnar storage engines.

## GraphQL Implementations
*   The AI MUST use GraphQL solely for client-device data fetching to prevent over-fetching/under-fetching.
*   The AI MUST NOT attempt to use GraphQL for recursive graph traversals or arbitrary search conditions unless explicitly defining dedicated endpoint resolvers, as GraphQL is inherently restricted to prevent denial-of-service attacks.
*   The AI MUST duplicate context data within GraphQL nested structures (e.g., returning the sender's profile picture inside a `replyTo` field) to simplify client-side UI rendering, accepting the trade-off of larger response sizes.

## Event Sourcing and CQRS
*   When defining Event Sourcing events, the AI MUST name events as immutable facts in the past tense (e.g., `BookingCancelled`, not `CancelBooking`).
*   The AI MUST ensure that the process generating Materialized Views (Read Models) from the Event Log is strictly deterministic.
*   The AI MUST NOT execute external, volatile side-effects (e.g., fetching current exchange rates, sending emails) during the replay of an event log. Volatile data MUST be captured and baked into the event payload at the time of creation.
*   If personal data (GDPR/CCPA) is stored, the AI MUST architect a mechanism for data deletion within the immutable log, such as cryptographic erasure (encrypting the payload and deleting the key) or storing PII outside the log.

## Dataframes and Machine Learning
*   When preparing relational data for machine learning algorithms, the AI MUST utilize Dataframes to transform row-based data into multi-dimensional Arrays/Matrices.
*   The AI MUST apply **One-Hot Encoding** to transform categorical string columns into numerical binary columns suitable for linear algebra operations.

# @Workflow
1.  **Analyze Relationship Complexity**: Assess the user's data structures. Determine the ratio of 1-to-N, N-to-1, and N-to-M relationships.
2.  **Select Paradigm**: Map the relationship complexity to Document (1-to-N tree), Relational (mixed), or Graph (heavy N-to-M). If analytical, select Data Warehouse (Star Schema) or Dataframes. If auditability is key, select Event Sourcing.
3.  **Define Schema Strategy**: Determine if the system requires Schema-on-write (strict, relational) or Schema-on-read (heterogeneous, document). Write migration or runtime-fallback code accordingly.
4.  **Balance Normalization**: Identify write-heavy components (normalize using IDs) and read-heavy components (denormalize or materialize views). Design hydration logic for fast-changing sub-entities.
5.  **Draft Queries**: Write declarative queries prioritizing explicit column selection. In ORMs, explicitly define eager loading to bypass N+1 issues.
6.  **Enforce Determinism (If Event Sourced)**: Review event structures to ensure all external state is captured at generation time and named in the past tense.

# @Examples (Do's and Don'ts)

## Handling Schema-on-Read Evolution
*   **[DO]** Handle missing legacy fields gracefully in application code when using Document databases.
```javascript
function formatUser(userDoc) {
    // Schema-on-read: Handle older documents written before 'first_name' was introduced
    if (userDoc.name && !userDoc.first_name) {
        userDoc.first_name = userDoc.name.split(" ")[0];
    }
    return userDoc;
}
```
*   **[DON'T]** Assume all documents in a schema-on-read database conform to the latest implicit schema, which will cause crashes on historical data.
```javascript
function formatUser(userDoc) {
    // ANTI-PATTERN: Will crash or return undefined on old documents
    return userDoc.first_name.toUpperCase();
}
```

## ORM Querying (N+1 Problem)
*   **[DO]** Eager load relationships to utilize declarative database joins.
```python
# Django ORM example
# Executes a single query with a SQL JOIN
comments = Comment.objects.select_related('author').filter(post_id=1)
for comment in comments:
    print(comment.author.name)
```
*   **[DON'T]** Iterate over relations, causing a new query per row.
```python
# ANTI-PATTERN: N+1 queries
comments = Comment.objects.filter(post_id=1) # 1 query
for comment in comments:
    print(comment.author.name) # N queries executed inside the loop
```

## Graph Querying
*   **[DO]** Use native graph declarative languages (like Cypher) for variable-length relationships.
```cypher
MATCH (person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (:Location {name:'Europe'})
RETURN person.name
```
*   **[DON'T]** Force relational SQL recursive CTEs for complex graph traversals unless constrained by the technology stack, as it creates brittle, unreadable queries.
```sql
-- ANTI-PATTERN: Over-complicating graph traversal in SQL
WITH RECURSIVE in_europe(vertex_id) AS (
    SELECT vertex_id FROM vertices WHERE properties->>'name' = 'Europe'
    UNION
    SELECT edges.tail_vertex FROM edges JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
) ...
```

## Event Sourcing
*   **[DO]** Name events as historical facts and embed volatile external state.
```json
{
    "eventType": "CartCheckedOut",
    "timestamp": "2023-10-14T10:00:00Z",
    "payload": {
        "cartId": "123",
        "totalAmount": 100.00,
        "exchangeRateAtCheckout": 1.15 
    }
}
```
*   **[DON'T]** Name events as commands or require materialized view builders to fetch live external state.
```json
{
    "eventType": "CheckoutCart", // ANTI-PATTERN: Imperative command
    "payload": {
        "cartId": "123",
        "totalAmount": 100.00
        // ANTI-PATTERN: Missing exchange rate, forcing replay logic to fetch live API
    }
}
```

## Analytics / Columnar Queries
*   **[DO]** Select only required columns in OLAP systems to leverage columnar storage.
```sql
SELECT dim_date.weekday, SUM(fact_sales.quantity) 
FROM fact_sales JOIN dim_date ON fact_sales.date_key = dim_date.date_key;
```
*   **[DON'T]** Use `SELECT *` in analytic queries, forcing the engine to load massive amounts of unneeded columnar blocks from disk.
```sql
-- ANTI-PATTERN: Forces loading 100+ columns into memory
SELECT * FROM fact_sales JOIN dim_date ON fact_sales.date_key = dim_date.date_key;
```