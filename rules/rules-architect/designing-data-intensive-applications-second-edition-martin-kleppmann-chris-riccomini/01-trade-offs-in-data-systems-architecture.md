# @Domain
These rules MUST be activated when the AI is tasked with designing, reviewing, or refactoring data systems architecture, selecting database technologies, structuring backend services, creating data pipelines (ETL/ELT), or evaluating trade-offs between distributed, cloud-native, and single-node systems.

# @Vocabulary
- **Data-Intensive Application**: An application where the primary challenges are storing, processing, managing change, ensuring consistency, and maintaining availability of large data volumes, rather than CPU-bound computation.
- **OLTP (Online Transaction Processing)**: Operational systems with interactive access patterns, point queries (fetch by key), and low-latency reads/writes of individual records representing current state.
- **OLAP (Online Analytic Processing)**: Analytical systems used by business analysts and data scientists, characterized by queries that scan and aggregate huge numbers of historical records.
- **Data Warehouse**: A separate database containing a read-only, transformed copy of data extracted from multiple OLTP systems, optimized for analytics.
- **Data Lake**: A centralized repository holding raw, untransformed data as files (e.g., Avro, Parquet, text, images) without imposing a relational data model.
- **Data Lakehouse**: An architecture combining the file storage of a data lake with a query execution engine and schema metadata layer for SQL workloads.
- **System of Record (Source of Truth)**: The database holding the authoritative, canonical, and typically normalized version of data. New data is written here first.
- **Derived Data System**: A system containing data transformed or processed from another source (e.g., caches, search indexes, materialized views, ML models). If lost, it can be recreated from the source.
- **ETL/ELT (Extract-Transform-Load)**: The pipeline process of extracting data from operational systems, transforming it, and loading it into an analytical system.
- **HTAP (Hybrid Transactional/Analytic Processing)**: Systems attempting to support both OLTP and OLAP in a single database.
- **Cloud-Native**: Architectures designed specifically to leverage cloud services, notably utilizing object storage and the disaggregation of storage and compute.
- **Separation of Storage and Compute (Disaggregation)**: The architectural pattern of decoupling persistent data storage (e.g., S3) from the CPU/RAM used to process it.
- **Multitenancy**: Serving data and computation for several different customers on the same shared hardware/service while maintaining isolation.
- **Microservices**: An architecture decomposing applications into interacting services, where each service has one well-defined purpose, a single owning team, and its own isolated database.
- **Serverless (FaaS)**: Deployment model where infrastructure is outsourced, resources auto-scale per request, and billing is strictly metered by execution time.
- **Observability**: Tools and practices (e.g., distributed tracing) allowing high-level metrics and individual events across a distributed system to be analyzed.
- **Data Minimization (Datensparsamkeit)**: The legal and ethical principle of collecting only necessary data, using it only for explicitly specified purposes, and deleting it when no longer needed.

# @Objectives
- The AI MUST systematically separate operational (OLTP) and analytical (OLAP) workloads.
- The AI MUST clearly delineate Systems of Record from Derived Data Systems.
- The AI MUST evaluate the trade-offs of self-hosting vs. cloud-native services before recommending an infrastructure path.
- The AI MUST default to single-node simplicity unless the specific scale, availability, or geographic requirements mandate a distributed system.
- The AI MUST enforce strict service and data boundaries (e.g., independent databases for microservices).
- The AI MUST embed legal, ethical, and privacy constraints (GDPR, data minimization) directly into data system designs.

# @Guidelines

## Workload Separation
- The AI MUST separate OLTP and OLAP workloads into different data systems.
- The AI MUST NOT allow analytical applications (e.g., business intelligence dashboards, ML training) to directly query operational OLTP databases.
- The AI MUST route data from operational systems to analytical systems via ETL/ELT pipelines or event streams.

## Data Flow and Record Keeping
- The AI MUST explicitly label every database or storage component as either a "System of Record" or "Derived Data".
- When proposing a Derived Data system (e.g., a cache or search index), the AI MUST define the asynchronous or pipeline mechanism used to update it when the System of Record changes.
- The AI MUST treat derived data as redundant and design it such that it can be dropped and entirely rebuilt from the System of Record.

## Infrastructure and Cloud-Native Patterns
- When designing for the cloud, the AI MUST favor cloud-native patterns (e.g., building upon object storage like S3) over traditional Infrastructure-as-a-Service (IaaS) virtual disks, unless legacy compatibility is strictly required.
- The AI MUST design analytics and large-scale cloud data systems using the Separation of Storage and Compute.
- The AI MUST NOT apply High-Performance Computing (HPC) patterns (e.g., stop-the-world batch checkpointing, assuming completely trusted shared memory) to cloud-native online services, which require continuous high availability and strict security isolation.
- When recommending Serverless architectures, the AI MUST account for execution time limits, cold starts, and integration complexities.

## Distributed vs. Single-Node
- The AI MUST NOT prematurely distribute a system. The AI MUST evaluate if a single-node system (using modern, large CPU/RAM/Disk configurations) can satisfy the requirements before recommending a distributed architecture.
- When proposing a distributed system, the AI MUST explicitly state which requirement forces distribution (e.g., geographic latency, dataset size exceeding single-machine capacity, legal data residency, or high-availability fault tolerance).
- In distributed microservice architectures, the AI MUST assign a dedicated, isolated database to each service.
- The AI MUST NOT allow two microservices to integrate by reading/writing to the same shared database. All inter-service communication MUST occur via network APIs (HTTP/REST, gRPC, or Message Queues).
- The AI MUST incorporate observability (distributed tracing, metrics, logs) when defining distributed architectures.

## Ethics, Privacy, and Law
- The AI MUST apply the principle of Data Minimization. If data is not explicitly required for a specified business purpose, the AI MUST recommend against storing it.
- The AI MUST factor in "Right to be Forgotten" (GDPR/CCPA) mechanics. When using immutable constructs (e.g., append-only logs), the AI MUST define how user data can be successfully excised or anonymized.
- The AI MUST weigh the cost of storage not just in cloud billing, but in security liability, reputational risk, and regulatory fines.

# @Workflow
1. **Workload Analysis**: Determine if the user's request pertains to an operational system (OLTP, low latency, user-facing) or an analytical system (OLAP, bulk aggregations, BI/ML).
2. **Component Classification**: Categorize every required data store as either a System of Record or Derived Data.
3. **Distribution Evaluation**: Calculate the expected scale and availability requirements. Default to a single-node architecture. If thresholds are exceeded, explicitly justify the upgrade to a distributed architecture.
4. **Architectural Mapping**: 
   - If Cloud-Native: Apply Separation of Storage and Compute and utilize object storage.
   - If Microservices: Assign unique databases per service and define API contracts.
   - If Analytical: Design an ETL/ELT pipeline feeding a Data Warehouse or Data Lake.
5. **Compliance Review**: Audit the proposed architecture for data minimization, privacy compliance, and deletion capabilities. Modify immutable or infinitely-retained data structures to ensure compliance.
6. **Output Generation**: Present the architecture clearly outlining the trade-offs made between consistency, latency, cost, and operational complexity.

# @Examples (Do's and Don'ts)

## Operational vs Analytical Workloads
- **[DO]**: Set up a continuous change-data-capture stream from a PostgreSQL operational database to an S3 Data Lake, allowing data scientists to run heavy aggregate queries via Spark without affecting the user-facing website.
- **[DON'T]**: Write a cron job that runs a `GROUP BY` spanning millions of rows directly on the production operational database to generate a nightly business report.

## Microservice Data Boundaries
- **[DO]**: Design `OrderService` with its own database and `InventoryService` with its own database. `OrderService` communicates with `InventoryService` via an HTTP/gRPC API to verify stock.
- **[DON'T]**: Allow `OrderService` to establish a direct JDBC connection to the `InventoryService` database to run a `SELECT` query on the `inventory_items` table.

## Cloud-Native Storage
- **[DO]**: Design a cloud-native analytical database where raw data blocks are durably stored in Amazon S3, and stateless compute nodes pull those blocks over the network into local ephemeral memory to execute queries.
- **[DON'T]**: Design a cloud-scale data warehouse that strictly requires storing petabytes of data on Amazon EBS virtual block devices attached to specific compute instances.

## Single-Node vs Distributed
- **[DO]**: Recommend a single-node PostgreSQL or SQLite database for a new startup's backend where the total dataset is 50GB and peak load is 100 requests per second.
- **[DON'T]**: Recommend a heavily partitioned, multi-node distributed database cluster for a 50GB dataset simply because the application might grow in 5 years.

## System of Record vs Derived Data
- **[DO]**: Define a MySQL database as the System of Record for user profiles, and a Redis cache as a Derived Data system. Implement a pattern where updates to MySQL trigger an invalidation of the Redis cache.
- **[DON'T]**: Treat a Redis cache as a System of Record, relying on it for authoritative data without a mechanism to reconstruct it if the cache goes down.

## Data Minimization and Compliance
- **[DO]**: Store only the user's zip code instead of their exact GPS coordinates if the business requirement is solely to show localized weather forecasts.
- **[DON'T]**: Speculatively log and indefinitely store every user's exact IP address and GPS location "just in case Big Data analysis might find it useful later," ignoring deletion mechanisms and GDPR risks.