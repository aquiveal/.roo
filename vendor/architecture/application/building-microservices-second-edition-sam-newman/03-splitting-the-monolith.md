# @Domain
These rules MUST be triggered whenever the AI is tasked with architectural design, code refactoring, or infrastructure planning involving the decomposition of a monolithic application into microservices. This includes tasks related to splitting databases, separating application layers, managing legacy system migrations, implementing routing proxies for migration (e.g., Strangler Fig), or handling data synchronization and reporting in a newly distributed architecture. 

# @Vocabulary
- **Monolith / Monolithic Architecture**: An application where all code is deployed as a single process, or all data is tightly coupled in a single database, acting as a single unit of deployment.
- **Incremental Migration**: The practice of extracting functionality from a monolith one piece at a time, rather than attempting a total rewrite.
- **Big-Bang Rewrite**: An anti-pattern involving rewriting an entire system from scratch in a single massive deployment.
- **Premature Decomposition**: Splitting a system into microservices before the business domain is fully understood, leading to unstable service boundaries and high coordination costs.
- **Code First Decomposition**: Extracting the application code into a microservice while temporarily leaving its data in the monolithic database.
- **Data First Decomposition**: Extracting the tables associated with a domain into a separate database before separating the application code.
- **Strangler Fig Pattern**: Intercepting calls to an existing monolithic system and redirecting them to a new microservice incrementally as features are built, wrapping the old system.
- **Parallel Run**: Running both the monolithic implementation and the new microservice implementation side-by-side, serving the same requests, and comparing the results to ensure parity.
- **Feature Toggle / Feature Flag**: A mechanism to switch between the monolithic implementation and the microservice implementation dynamically.
- **Application-Level Join**: Replicating the behavior of a database `JOIN` by making a network call from one microservice to another to fetch related data.
- **Reporting Database Pattern**: Creating a dedicated database explicitly for read-only external access and reporting, which the microservice populates, thereby hiding its internal, authoritative state management.

# @Objectives
- The AI MUST treat microservices as a means to an end, not the end goal itself. It must always prioritize understanding the specific business or technical goal (e.g., scaling, independent deployability) before suggesting decomposition.
- The AI MUST advocate for incremental, step-by-step migrations and actively reject "big-bang" rewrites.
- The AI MUST safely guide the decoupling of data, acknowledging and actively mitigating the loss of database-level foreign keys, ACID transactions, and native `JOIN` operations.
- The AI MUST protect the internal state of microservices by explicitly forbidding the sharing of databases for integration or reporting purposes.

# @Guidelines

## Strategic Migration Rules
- **Validate the Goal:** Before initiating any split, the AI MUST ask or establish what the end goal is. If the goal can be achieved by simpler means (e.g., spinning up more monolith instances behind a load balancer), the AI MUST suggest the simpler alternative first.
- **Avoid Premature Decomposition:** If the domain model is highly volatile or poorly understood (e.g., a startup finding product-market fit), the AI MUST advise against splitting the monolith.
- **Prioritize Low-Hanging Fruit:** When deciding what to split first, the AI MUST balance the ease of extraction against the benefit. It MUST recommend starting with small, non-critical, easily detangled components to build momentum and establish operational readiness.
- **Preserve the Monolith:** The AI MUST NOT treat the monolith as an enemy that must be completely destroyed. It is acceptable for a monolith to coexist with microservices indefinitely if the remaining functionality does not warrant the cost of extraction.

## Layered Decomposition Rules
- **Code First Extraction:** When extracting a service, the AI MAY suggest extracting the backend code first while maintaining the connection to the monolithic database. However, it MUST state that the extraction is incomplete until the data is also decoupled.
- **Data First Extraction:** If data separation risk is high, the AI MAY suggest extracting the database tables first to validate data integrity boundaries before touching the application code.

## Integration & Routing Patterns
- **Use the Strangler Fig Pattern:** When replacing monolith routes, the AI MUST implement a proxy or gateway that intercepts calls and routes migrated features to the new microservice while routing legacy features to the monolith.
- **Use Feature Toggles:** The AI MUST incorporate feature toggles to switch between the monolith and microservice implementations safely without requiring lockstep deployments.
- **Validate via Parallel Runs:** For critical functionality, the AI MUST implement logic to route traffic to both the old monolith code and the new microservice code, discarding the microservice response but comparing it to the monolith's output to verify correctness.

## Data Decomposition Constraints
- **Application-Level Joins:** When data is split across databases, the AI MUST NOT use cross-database SQL joins. It MUST replace database joins with application-level network calls (e.g., querying the Ledger, then querying the Catalog via API using the retrieved IDs).
- **Mitigate Application Join Latency:** Because application-level joins introduce network latency, the AI MUST implement bulk lookups (fetching multiple IDs in one call) or localized caching to offset the performance hit.
- **Data Integrity:** The AI MUST acknowledge the loss of enforced foreign keys. It MUST implement application-level coping patterns, such as "soft deletes" (marking records as deleted rather than actually deleting them) to prevent orphaned data across services.
- **Distributed Transactions:** The AI MUST explicitly warn against relying on distributed transactions (like Two-Phase Commits) to manage state across newly split databases.
- **Schema Tooling:** The AI MUST recommend and configure schema migration tools (e.g., Flyway, Liquibase) to manage the stateful nature of separated databases idempotently.
- **Reporting & Analytics:** The AI MUST NOT allow reporting tools to query the microservice's internal database directly. Instead, it MUST implement the Reporting Database Pattern, pushing data from the microservice to a dedicated, decoupled read-only schema.

# @Workflow
When tasked with splitting a component out of a monolithic application, the AI MUST adhere to the following strict algorithmic process:

1. **Assess the Goal and Alternatives:**
   - Define the exact technical or business driver for the split (e.g., scale, team autonomy).
   - Evaluate if a simpler architecture (modular monolith, load-balanced single-process monolith) achieves the goal without distributed complexity.

2. **Select the Seam (Boundary):**
   - Identify a bounded context that is well-understood and relatively decoupled.
   - Choose a "low-hanging fruit" target for the first extraction to validate CI/CD and operational readiness.

3. **Determine the Layer Strategy:**
   - Decide between Code-First (extract logic, keep shared DB temporarily) or Data-First (extract tables, keep monolith logic temporarily) based on where the highest risk of coupling lies.

4. **Implement the Migration Pattern:**
   - Deploy the new microservice.
   - Configure a proxy/gateway implementing the Strangler Fig Pattern.
   - Wrap the new routing logic in a Feature Toggle.

5. **Address Data Decomposition:**
   - Remove foreign key constraints crossing the new boundary. Replace with soft-delete logic.
   - Refactor SQL `JOIN`s that cross the boundary into bulk API lookups in the application layer.
   - Set up Flyway/Liquibase for the new database.

6. **Validate and Cutover:**
   - Implement a Parallel Run for the extracted feature. Log discrepancies between the monolith and the microservice.
   - Once output parity is confirmed, toggle the feature flag to make the microservice the primary system of record.
   - Implement the Reporting Database pattern if data warehouse analytics are required.

# @Examples (Do's and Don'ts)

## Migration Strategy
- **[DO]** Chip away at the monolith using the Strangler Fig pattern, routing specific URI paths (e.g., `/api/wishlist`) to the new microservice while `/api/orders` still hits the monolith.
- **[DON'T]** Attempt to rewrite the entire application in a microservices architecture in a single parallel project and swap them overnight (Big-Bang).

## Handling Cross-Domain Data (Joins)
- **[DO]** Fetch a list of IDs from the `Ledger` database, then make a single HTTP request to the `Catalog` microservice passing an array of those IDs to get their textual descriptions (Application-level join with bulk lookup).
- **[DON'T]** Attempt to configure a database link or shared cluster to perform a `SELECT * FROM Ledger l JOIN Catalog c ON l.sku = c.sku` across the microservice boundary.

## Ensuring Data Integrity
- **[DO]** Add a `deleted_at` timestamp column (Soft Delete) to a `Catalog` table so that if an item is removed, the decoupled `Ledger` microservice does not crash when trying to look up historical sales data for that item.
- **[DON'T]** Rely on cascading deletes or cross-database foreign key constraints to manage data lifecycle across microservices.

## Enterprise Reporting
- **[DO]** Have the `Orders` microservice listen to its own state changes and publish a flattened, read-optimized projection of that data to a separate `Reporting Database` which data scientists can query via SQL.
- **[DON'T]** Give business analysts or Tableau/PowerBI read-replica access directly to the `Orders` microservice's internal relational database.