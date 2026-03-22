@Domain
These rules are triggered during system architecture design, data infrastructure setup, database selection, data pipeline creation (ETL/ELT), cloud infrastructure provisioning, microservice boundary definition, performance/cost optimization, and privacy/compliance planning.

@Vocabulary
- **Data-Intensive Application**: An application where data management (volume, complexity, rate of change) is the primary challenge, as opposed to compute-intensive tasks.
- **Frontend**: Client-side code (web browsers, mobile apps) handling single-user data.
- **Backend**: Server-side code (reachable via HTTP/WebSocket) managing state across all users using databases, caches, and message queues.
- **OLTP (Online Transaction Processing)**: Operational systems with interactive, low-latency, point queries fetching/updating individual records by key. Represents current state.
- **OLAP (Online Analytic Processing)**: Analytical systems with queries aggregating over huge numbers of records for business intelligence. Represents history of events.
- **Data Warehouse**: A separate, read-only analytical database containing data extracted from multiple OLTP systems, optimized for complex SQL queries.
- **ETL/ELT (Extract-Transform-Load / Extract-Load-Transform)**: The process of moving data from operational sources to analytical systems.
- **HTAP (Hybrid Transactional/Analytic Processing)**: Systems attempting to support both OLTP and OLAP workloads without requiring ETL.
- **Data Lake**: A centralized repository storing raw, untransformed files (Avro, Parquet, text, images) supporting machine learning and data science.
- **Sushi Principle**: The philosophy that "raw data is better," advocating for storing untransformed data in Data Lakes for flexible downstream use.
- **Data Lakehouse**: An architecture running SQL/data warehousing workloads directly on Data Lake files (e.g., Hive, Spark SQL, Trino).
- **Reverse ETL**: Moving processed data/insights from analytical systems back into operational systems (e.g., ML recommendations).
- **System of Record (Source of Truth)**: The authoritative database where new data is first written, typically in a normalized representation.
- **Derived Data System**: Redundant but necessary systems (caches, search indexes, materialized views, Data Warehouses) created by transforming data from the System of Record to optimize reads.
- **Cloud-Native**: Architectures built on high-level cloud abstractions (e.g., object storage) characterized by the separation of compute and storage, multitenancy, and elasticity.
- **Disaggregated Storage and Compute**: The architectural separation of processing power (CPU/RAM) from persistent storage (Object Stores) in cloud-native systems.
- **Observability**: Tooling (tracing, OpenTelemetry, Zipkin, Jaeger) used to diagnose slow requests and failures in distributed systems.
- **Service-Oriented Architecture (SOA) / Microservices**: Decomposing applications into independent services, each with one purpose, managed by one team, communicating via network APIs.
- **Serverless (FaaS)**: Cloud deployment model scaling automatically by request, billing by execution time, rather than provisioning instances.
- **HPC (High-Performance Computing) / Supercomputing**: Systems built for intensive batch jobs using checkpointing and RDMA, contrasting with cloud computing's high-availability, TCP/IP-based online services.
- **Data Minimization (Datensparsamkeit)**: The legal and ethical principle of collecting only necessary data, retaining it only as long as needed, and deleting it to reduce liability and protect user privacy (GDPR/CCPA).

@Objectives
- Determine the optimal database and architecture choice by distinguishing between operational (OLTP) and analytical (OLAP/ML) workloads.
- Map the flow of data cleanly by explicitly designating Systems of Record and Derived Data systems.
- Decouple microservices by enforcing strict boundaries, including database separation and API versioning.
- Prevent operational impact on transactional systems by isolating expensive analytical queries.
- Leverage cloud-native paradigms, specifically the separation of storage and compute, when deploying in cloud environments.
- Default to single-node simplicity unless inherent distributed requirements (fault tolerance, scale, geography) are explicitly met.
- Ensure system designs account for legal compliance, data residency, and the right to be forgotten (Data Minimization).

@Guidelines
- **Operational vs. Analytical Separation**: When designing a system that requires both transaction processing and business reporting, the AI MUST create a separate Data Warehouse or Data Lake for the analytics. The AI MUST NOT run heavy `GROUP BY` or analytical scans on the OLTP database.
- **Data Lake vs. Data Warehouse**: When the user requires machine learning, feature engineering, NLP, or unstructured data processing, the AI MUST recommend a Data Lake (object storage with raw files) rather than a relational Data Warehouse.
- **Derived Data Updates**: When configuring Derived Data (caches, search indexes, materialized views), the AI MUST define a clear, automated integration mechanism (e.g., Change Data Capture or Event Streams) to keep it updated from the System of Record.
- **Cloud-Native Storage**: When designing cloud-hosted data systems, the AI MUST favor disaggregated storage and compute. Treat local instance disks as ephemeral caches and rely on Object Storage (e.g., S3) for durable, long-term state.
- **Distributed vs. Single-Node**: The AI MUST evaluate if a workload can fit on a single node (using DuckDB, SQLite, KùzuDB, etc.) before proposing a complex distributed system. If a distributed system is chosen, the AI MUST explicitly state the justifying factor (fault tolerance, latency, elasticity).
- **Microservice Database Isolation**: When generating microservices architectures, the AI MUST assign each service its own independent database. The AI MUST explicitly forbid database sharing between microservices to prevent coupling. API contracts (OpenAPI, gRPC) MUST be used for inter-service communication.
- **Observability in Distributed Systems**: When generating distributed or microservice code, the AI MUST include distributed tracing (e.g., OpenTelemetry) to track API calls and network latency.
- **Handling API Evolution**: When defining APIs for microservices, the AI MUST plan for independent evolvability using description standards (OpenAPI, gRPC) so developers do not break upstream/downstream clients.
- **Data Minimization and Compliance**: When designing schemas or data retention policies, the AI MUST implement data minimization. The AI MUST define mechanisms for deleting user data (GDPR right to be forgotten), especially considering the complexity of removing data from append-only logs or derived ML training sets.
- **Handling Supercomputing vs. Cloud assumptions**: The AI MUST NOT apply HPC design patterns (like stopping the entire cluster to repair a node and loading from a checkpoint) to highly-available cloud/web services. Cloud services MUST be designed to tolerate individual node failures continuously.

@Workflow
1. **Analyze the Workload Requirements**:
   - Classify the request as Operational (OLTP), Analytical (OLAP), or Machine Learning (Data Science).
   - Determine dataset size, latency constraints, and query patterns (point-queries vs. large aggregations).
2. **Determine Data Flow and Sovereignty**:
   - Identify the System of Record.
   - Map out the ETL/ELT data pipelines or event streams.
   - Define all Derived Data systems (caches, indexes, materialized views, ML models).
3. **Select the Deployment Architecture**:
   - Evaluate Single-Node vs. Distributed. Default to Single-Node if scale permits.
   - Evaluate Self-hosted vs. Cloud-native. If Cloud-native, design for Disaggregated Storage and Compute.
4. **Enforce Service Boundaries**:
   - If utilizing microservices, isolate databases per service.
   - Define OpenAPI or gRPC interfaces for communication.
   - Inject observability (tracing/metrics) into the network boundaries.
5. **Apply Privacy and Compliance Filters**:
   - Review the architecture for Data Minimization.
   - Ensure a mechanism exists to hard-delete Personally Identifiable Information (PII) across both the System of Record and all Derived Data systems.

@Examples (Do's and Don'ts)

- **Analytical vs Operational Separation**
  - [DO]: Design an architecture where a Node.js/PostgreSQL backend handles user traffic (OLTP), and an asynchronous ETL job synchronizes data to Snowflake (OLAP) for the BI team.
  - [DON'T]: Provide an architecture where a business analyst runs a `SELECT SUM(revenue) FROM orders GROUP BY month` directly on the primary production PostgreSQL database, impacting user latency.

- **Microservice Database Isolation**
  - [DO]: Create a `User Service` with its own `users_db` and an `Order Service` with its own `orders_db`. Have the `Order Service` query the `User Service` via REST/gRPC API to fetch user details.
  - [DON'T]: Allow the `Order Service` to execute SQL queries directly against the `users_db` owned by the `User Service`.

- **Cloud-Native Storage**
  - [DO]: Design a scalable analytics system that writes raw event data as Parquet files to Amazon S3 (Object Storage) and spins up ephemeral compute nodes (e.g., Spark/Presto) only when queries are running.
  - [DON'T]: Design a cloud analytics system that permanently stores petabytes of data on Amazon EBS (virtual block devices) attached to continuously running EC2 instances.

- **Data Minimization and Right to be Forgotten**
  - [DO]: Implement a data retention policy that automatically drops IP address logs after 30 days, and build an event-driven "User Deletion" workflow that scrubs user PII from the primary DB, the search index, and the data lake.
  - [DON'T]: Store sensitive location data indefinitely "just in case it becomes useful later" without an explicit business purpose or deletion mechanism.

- **Derived Data Clarity**
  - [DO]: Clearly document that Redis is a Derived Data system holding a cached view of the MySQL System of Record, and write application logic that treats Redis data as ephemeral and reconstructable.
  - [DON'T]: Treat a cache or a search index as a System of Record, risking permanent data loss if the index is corrupted.