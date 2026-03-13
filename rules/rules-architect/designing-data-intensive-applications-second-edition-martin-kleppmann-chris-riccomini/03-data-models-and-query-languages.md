# @Domain
These rules MUST be activated when the AI is tasked with designing database schemas, selecting data storage technologies, writing database queries (SQL, NoSQL, Graph, or GraphQL), building data pipelines, architecting event-driven systems, configuring Object-Relational Mappers (ORMs), or preparing data for analytics and machine learning.

# @Vocabulary
- **Data Model**: The abstraction layer representing how data is structured, stored, and queried.
- **Impedance Mismatch**: The disconnect between object-oriented application code and relational database models.
- **ORM (Object-Relational Mapping)**: Frameworks that translate between objects in application code and relational database tables.
- **N+1 Query Problem**: An ORM anti-pattern where resolving references requires one initial query followed by N subsequent queries.
- **Document Model**: A data model (e.g., JSON) organizing data as self-contained, tree-structured documents, optimizing for one-to-many relationships and data locality.
- **Normalization**: Storing human-meaningful information in exactly one place and referencing it via unique IDs to prevent inconsistencies and reduce write costs.
- **Denormalization**: Duplicating data across multiple records to optimize read performance by avoiding joins.
- **Shredding**: The relational technique of splitting a document-like structure into multiple tables.
- **Schema-on-Write**: An explicit schema enforced by the database upon data insertion (traditional relational databases).
- **Schema-on-Read**: An implicit schema where data structure is interpreted by application code only when read (often incorrectly called "schemaless").
- **Star Schema**: An analytics data model featuring a central **Fact Table** (events/transactions) surrounded by **Dimension Tables** (attributes/metadata).
- **Snowflake Schema**: A variation of the Star Schema where dimension tables are further normalized into subdimensions.
- **Property Graph**: A graph model consisting of vertices (nodes) and edges (relationships), where both can contain arbitrary key-value properties.
- **Triple-Store**: A graph model storing data as `(subject, predicate, object)` statements (e.g., RDF, Turtle).
- **Declarative Query Language**: Languages (like SQL, Cypher, SPARQL) that specify the pattern of data desired without defining the execution algorithm.
- **Event Sourcing**: Modeling state as an append-only log of immutable events (facts) that occurred in the past.
- **CQRS (Command Query Responsibility Segregation)**: Separating write-optimized models (event logs) from read-optimized models (materialized views/projections).
- **Dataframe**: A tabular data structure used in analytics and data science for bulk manipulations and transitioning relational data into matrices.
- **One-Hot Encoding**: Transforming categorical data into numerical matrices by creating a binary column for each possible value.

# @Objectives
- Eliminate Impedance Mismatch by selecting the data model that most naturally fits the application's data structure and access patterns.
- Balance read and write performance by strategically applying Normalization and Denormalization.
- Ensure evolvability of data structures by managing schema changes safely, whether using Schema-on-Read or Schema-on-Write paradigms.
- Optimize analytical workloads by applying specialized schemas (Star/Snowflake) and separating them from operational (OLTP) models.
- Model highly interconnected data seamlessly using Graph data models rather than forcing them into relational structures.
- Preserve absolute historical truth and enable reproducible states using Event Sourcing and CQRS.

# @Guidelines

## Relational vs. Document Models
- The AI MUST use a Document Model (JSON/BSON) when data structures are self-contained, tree-like (one-to-many), and typically loaded in their entirety (data locality).
- The AI MUST NOT use a Document Model if the application requires referencing deeply nested items directly or accessing data involving complex many-to-many relationships.
- The AI MUST use a Relational Model when the data contains many-to-many relationships or many-to-one relationships requiring frequent joins.
- When using ORMs, the AI MUST explicitly avoid the N+1 query problem by configuring eager fetching or join queries.

## Normalization vs. Denormalization
- The AI MUST use IDs (Normalization) for any data value that has human meaning and might change in the future (e.g., names, geographic regions) to avoid update anomalies.
- The AI MAY use plain text (Denormalization) ONLY if the field is a free-text entry or if read performance strictness dictates avoiding joins, provided a mechanism is established to keep redundant data updated.
- If using Denormalization, the AI MUST document it as "Derived Data" and implement a process (e.g., stream processing or asynchronous fan-out) to update all copies when the source changes.

## Schema Evolution
- For Document Databases (Schema-on-Read), the AI MUST implement application-level code to handle historical data formats (e.g., checking if an old field exists and mapping it to a new field at runtime).
- For Relational Databases (Schema-on-Write), the AI MUST write non-blocking schema migrations (e.g., adding a column with a `NULL` default) and avoid operations that require rewriting the entire table (like `UPDATE` on a massive table) in real-time.

## Analytical Data Modeling
- When architecting analytical data warehouses, the AI MUST use a Star Schema or Snowflake Schema.
- The AI MUST create a central Fact Table representing atomic, historical events (e.g., individual sales, clicks) that are append-only.
- The AI MUST create Dimension Tables representing the "who, what, where, when, how, and why" attributes referenced by foreign keys in the Fact Table.
- The AI MAY use One Big Table (OBT) denormalization strategies for analytics specifically to improve read performance, as analytics data does not suffer from operational write consistency issues.

## Graph Data Models
- The AI MUST use a Graph Data Model (Property Graph or Triple-Store) when relationships between data points are complex, many-to-many, and queries require traversing variable-length paths.
- If forced to query graph data within a Relational Database, the AI MUST use Recursive Common Table Expressions (`WITH RECURSIVE`).
- The AI MUST utilize specialized graph query languages (Cypher, SPARQL, Datalog) when interacting with native graph databases, exploiting their pattern-matching syntax.

## GraphQL
- The AI MUST use GraphQL ONLY for client-driven data fetching (e.g., UIs requesting specific UI-rendering fields) and MUST limit query complexity to prevent denial-of-service attacks.
- The AI MUST NOT use GraphQL for recursive queries or complex arbitrary analytical searches, as the language intentionally restricts these capabilities.

## Event Sourcing and CQRS
- The AI MUST define Event Sourcing events as immutable facts. Events MUST NEVER be updated or deleted.
- The AI MUST name all events in the past tense (e.g., `SeatBooked`, `OrderPlaced`).
- The AI MUST implement CQRS when using Event Sourcing by writing deterministic code that reads the event log and builds read-optimized Materialized Views.
- The AI MUST ensure event processing logic is entirely deterministic (e.g., injecting external state like exchange rates directly into the event payload rather than fetching it at view-generation time).

## Machine Learning and Analytics Data
- When preparing data for ML models, the AI MUST use Dataframes (e.g., Pandas, Spark) to transform relational structures into Multidimensional Arrays or Matrices.
- The AI MUST apply One-Hot Encoding when converting categorical string data into numerical matrices for linear algebra operations.

# @Workflow
When generating data architectures, schemas, or database queries, the AI MUST execute the following steps:

1. **Workload Analysis**: Identify whether the primary workload is Operational (OLTP), Analytical (OLAP), Machine Learning, or UI-driven data fetching.
2. **Relationship Mapping**: Map the entity relationships. If mostly isolated trees (1:N), choose Document. If interconnected (M:1, M:N), choose Relational. If highly interconnected with path traversals, choose Graph.
3. **Normalization Strategy**: Determine which fields require Normalization (human-readable concepts liable to change) and which can be Denormalized for read performance.
4. **Schema Management**: Define how schemas will be enforced. If Schema-on-Read, write the necessary fallback logic in application code. If Schema-on-Write, write the `ALTER TABLE` migrations.
5. **Event / Fact Definition**: If using Analytics or Event Sourcing, isolate immutable events into Fact tables or Event Logs, and name them in the past tense. Define the corresponding Materialized Views or Dimension tables.
6. **Query Construction**: Write the query using the declarative language best suited for the model (SQL, Cypher, SPARQL, Datalog, MongoDB Aggregation Pipeline).

# @Examples (Do's and Don'ts)

## Object-Relational Mismatch and N+1 Queries
- **[DO]** Write queries that fetch related data in a single database round-trip (e.g., `JOIN` in SQL, `$lookup` in MongoDB).
- **[DON'T]** Loop over a list of returned objects in application code and issue a separate query for each object's related data.

## Schema-on-Read Evolution
- **[DO]** Write application code that accounts for older document structures:
  ```javascript
  if (user && user.name && !user.first_name) {
      // Handle documents written before schema change
      user.first_name = user.name.split(" ")[0];
  }
  ```
- **[DON'T]** Assume every document in a schema-on-read database perfectly matches the newest application model expectations.

## Graph Querying
- **[DO]** Use Cypher for concise variable-length path traversal:
  ```cypher
  MATCH (person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (:Location {name:'United States'}),
        (person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (:Location {name:'Europe'})
  RETURN person.name
  ```
- **[DON'T]** Use SQL for variable-length graph traversals unless absolutely necessary, as it requires highly verbose `WITH RECURSIVE` queries that are difficult to maintain.

## Event Sourcing
- **[DO]** Model state changes as explicit, immutable past-tense events:
  ```json
  { "eventType": "UserRegistered", "userId": 123, "timestamp": "2023-10-01T12:00:00Z" }
  { "eventType": "EmailUpdated", "userId": 123, "newEmail": "test@test.com", "timestamp": "2023-10-02T14:00:00Z" }
  ```
- **[DON'T]** Treat the event log as a mutable database table (e.g., never run an `UPDATE` on the event log to change the email address).

## Normalization vs Denormalization
- **[DO]** Reference human-readable entities by ID in transaction tables: `{"user_id": 251, "region_id": 513}`.
- **[DON'T]** Embed data that might change globally across millions of documents: `{"user_id": 251, "region_name": "Washington, DC, United States", "company_logo_url": "http://img.com/old_logo.png"}` unless a strict update pipeline is architected.