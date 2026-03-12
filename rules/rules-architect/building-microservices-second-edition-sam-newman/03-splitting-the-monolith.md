# @Domain
Trigger these rules when the user requests architectural changes related to breaking apart a monolithic application, migrating functionality to a microservice architecture, decomposing databases, extracting specific modules into independent services, or addressing data consistency and routing challenges during a system transition.

# @Vocabulary
- **Incremental Migration**: The process of chipping away at a monolith step-by-step rather than replacing it all at once.
- **Big-Bang Rewrite**: An anti-pattern involving the complete, simultaneous replacement of a legacy system with a new architecture.
- **Premature Decomposition**: Extracting microservices before the business domain boundaries are fully understood, leading to high costs of change.
- **Code-First Extraction**: Extracting the application code into a microservice while leaving the data temporarily in the monolithic database.
- **Data-First Extraction**: Extracting the data schema and tables into a separate database before moving the application code, derisking data integrity issues.
- **Strangler Fig Pattern**: A routing pattern that wraps the old system, intercepting calls and redirecting them to the new microservice if the functionality exists, or routing them to the monolith if it does not.
- **Parallel Run**: Executing both the monolithic implementation and the new microservice implementation side-by-side, serving the same requests, and comparing the results without impacting production state.
- **Feature Toggle**: A deployment mechanism that allows dynamic switching between the old monolithic implementation and the new microservice implementation.
- **Application-Level Join**: Retrieving data from multiple separate microservices and combining it in-memory within the application tier, replacing traditional database-level SQL joins.
- **Soft Delete**: Marking a record as deleted via a status column rather than physically removing it, used to cope with the loss of cross-database foreign key constraints.
- **Reporting Database**: A dedicated database optimized for external access and reporting, populated by a microservice to hide its internal state management.

# @Objectives
- Ensure all monolith-to-microservice migrations are incremental, objective-driven, and verifiable.
- Prevent big-bang rewrites and premature domain decomposition.
- Safely route traffic using established patterns (Strangler Fig, Feature Toggles).
- Mitigate the performance and consistency penalties of decomposed data (e.g., application-level joins, schema versioning).
- Maintain data integrity without relying on distributed database transactions.

# @Guidelines
- **Goal Verification**: The AI MUST explicitly ask the user for the overarching goal of the decomposition (e.g., independent scaling, faster time-to-market, technology retirement) before proposing any extraction strategy.
- **Simpler Alternatives First**: The AI MUST consider and suggest simpler scaling techniques (like running multiple copies of the monolith behind a load balancer) before recommending a complex microservice extraction.
- **Incremental Chipping**: The AI MUST enforce an incremental migration strategy. Never propose rebuilding the entire system from scratch simultaneously. 
- **Target Selection**: When identifying what to extract first, the AI MUST evaluate the balance between extraction ease and business benefit. The AI MUST recommend extracting "low-hanging fruit" (easy, low-risk, high-value) for the first few microservices to build momentum.
- **Domain Understanding**: The AI MUST warn against extracting services if the domain model is highly volatile.
- **Layered Decomposition Options**: 
  - The AI MUST outline whether a Code-First or Data-First extraction is appropriate. 
  - If Code-First is chosen, the AI MUST explicitly sketch out the future data extraction plan to prevent long-term data tangling.
  - If Data-First is chosen, the AI MUST address transactional and data integrity boundaries upfront.
- **Routing and Integration**: The AI MUST utilize the Strangler Fig Pattern by implementing an intercepting proxy/gateway to route traffic dynamically between the monolith and the new service.
- **Testing via Parallel Runs**: When migrating critical functionality, the AI MUST suggest a Parallel Run pattern to run both monolithic and microservice logic side-by-side to compare outputs safely.
- **Data Joins**: When databases are split, the AI MUST replace SQL `JOIN` statements with Application-Level Joins. The AI MUST instruct the user to implement bulk API lookups or local caching to mitigate the increased network latency.
- **Data Integrity**: The AI MUST NOT use cross-database foreign keys. The AI MUST implement coping patterns such as Soft Deletes to maintain relational context when referenced data is removed.
- **Transactions**: The AI MUST strictly forbid the use of distributed transactions (like Two-Phase Commits / 2PC). The AI MUST propose Sagas or eventual consistency mechanisms instead.
- **Database Tooling**: The AI MUST require the use of version-controlled delta scripts (e.g., Flyway, Liquibase) to manage database schema changes idempotently.
- **Reporting**: The AI MUST NOT allow external reporting tools to directly query a microservice's internal database. The AI MUST implement the Reporting Database pattern, where the microservice asynchronously pushes its state to a read-optimized reporting schema.

# @Workflow
1. **Goal and Candidate Identification**: 
   - Ask the user what business or technical constraint is driving the decomposition.
   - Analyze the monolith to identify a small, low-risk candidate for extraction (low-hanging fruit).
2. **Layer Strategy Selection**:
   - Determine if the extraction should be Code-First (move logic, map to old DB) or Data-First (move tables, map monolith to new DB).
3. **Data Dependency Resolution**:
   - Identify broken SQL joins and rewrite them as bulk API calls to the new service.
   - Identify broken foreign keys and implement soft deletes or eventual consistency syncs.
   - Set up Flyway/Liquibase for the new database schema.
4. **Routing Implementation**:
   - Design an HTTP proxy or routing layer applying the Strangler Fig Pattern.
   - Implement Feature Toggles to dynamically switch traffic.
5. **Validation Strategy**:
   - Set up a Parallel Run to compare the monolith's output with the new microservice's output.
6. **Reporting Strategy (If applicable)**:
   - If the extracted data is used in massive monolithic queries, design a Reporting Database and an event-driven data pump to populate it.

# @Examples (Do's and Don'ts)

### Strangler Fig Routing
[DO]
```nginx
# NGINX implementation of Strangler Fig Pattern
server {
    listen 80;

    # New Microservice takes over the /wishlist route
    location /wishlist {
        proxy_pass http://wishlist_microservice:8080;
    }

    # All other traffic falls back to the legacy monolith
    location / {
        proxy_pass http://legacy_monolith:80;
    }
}
```

[DON'T]
```nginx
# Hardcoding direct client links to different servers, bypassing a centralized routing proxy, forcing clients to know the architecture.
# Client App Code
const monolithUrl = "http://legacy:80";
const microserviceUrl = "http://wishlist:8080";
```

### Handling Decomposed Data Joins
[DO]
```javascript
// Application-Level Join with Bulk Lookup
async function getTopSellingAlbums() {
    // 1. Get ledger data from Sales service
    const topSkus = await salesService.getTopSellers(10); 
    const skuIds = topSkus.map(s => s.skuId);

    // 2. Bulk lookup album info from Catalog service to mitigate latency
    const albumDetails = await catalogService.getAlbumsByIds(skuIds);

    // 3. Join in memory
    return topSkus.map(sku => ({
        ...sku,
        details: albumDetails.find(a => a.id === sku.skuId)
    }));
}
```

[DON'T]
```sql
/* Querying across service boundaries using cross-database links */
SELECT l.skuId, l.sales_count, a.album_name 
FROM MonolithDB.Ledger l
JOIN CatalogDB.Albums a ON l.skuId = a.id;
```

### Data Integrity and Deletions
[DO]
```sql
-- Using a Soft Delete to preserve data integrity when foreign keys are lost
UPDATE Albums 
SET status = 'DELETED', deleted_at = NOW() 
WHERE id = 12345;
```

[DON'T]
```sql
-- Hard deleting a record that might be referenced by an external microservice (e.g., Sales Ledger)
DELETE FROM Albums WHERE id = 12345;
```

### External Reporting
[DO]
```javascript
// Microservice pushing data to a dedicated Reporting Database
async function processOrder(order) {
    await internalDb.save(order);
    // Push stripped-down or denormalized data to reporting DB/Queue
    await reportingQueue.publish('OrderCompleted', extractReportingMetrics(order));
}
```

[DON'T]
```python
# External BI tool directly querying the microservice's internal transactional database
db_connection = connect_to("microservice_internal_production_db")
results = db_connection.execute("SELECT * FROM internal_orders_table")
```