# @Domain
Triggered when the AI is tasked with architecting, implementing, or optimizing "Batch Processing" systems, ETL (Extract-Transform-Load) pipelines, bulk data imports, or large-scale offline analytics. *(Note: Because the target "Chapter 11: Batch Processing" is explicitly marked as unavailable in the provided source text, these rules are synthesized strictly and exhaustively from all batch-processing, ETL, and bulk-import principles scattered throughout the available chapters of the provided text).*

# @Vocabulary
- **Batch Processing**: The process of periodically crunching a large amount of accumulated data, as opposed to handling events or transactions interactively as they occur.
- **ETL (Extract-Transform-Load)**: A data pipeline process that extracts data from operational (OLTP) databases, transforms it into an analysis-friendly schema, cleans it up, and bulk-loads it into a data warehouse or data lake.
- **ELT**: A variant of ETL where the order of operations is swapped; data is extracted and loaded first, and the transformation is done subsequently within the data warehouse.
- **Bulk Import**: The primary write pattern for batch and analytical systems. It involves grouping many records together to write them in a single operation, which amortizes the cost of writing to disk (especially in compressed, column-oriented storage).
- **Data Warehouse**: A separate, read-optimized database dedicated to analytics and batch queries, preventing expensive batch operations from impacting the performance of interactive operational systems.
- **Data Lake**: A centralized repository storing batch-extracted data in its "raw" form (files), without imposing a strict relational schema upfront, adhering to the "sushi principle" (raw data is better).
- **Checkpointing**: A fault-tolerance mechanism used in large batch jobs (such as those on supercomputers) where the state of computation is periodically saved to disk.
- **Derived Data Systems**: Systems (like data warehouses or materialized views) whose data is the result of taking existing data from a system of record and transforming it via a batch process or pipeline.
- **Vectorized Processing**: An execution model for analytical/batch queries where operations are performed on batches (vectors) of column values rather than iterating over rows one by one.

# @Objectives
- Isolate batch processing and analytical workloads from operational (OLTP) workloads to ensure interactive application performance is not degraded.
- Handle large data volumes efficiently by utilizing bulk imports and vectorized processing rather than single-record read/write cycles.
- Ensure batch processing jobs are resilient to node failures by implementing state checkpointing and restart mechanisms.
- Maintain a strict architectural boundary between systems of record (source of truth) and derived data systems (outputs of batch pipelines).

# @Guidelines
- **MUST** route large-scale batch processing and analytical queries to a dedicated Data Warehouse, Data Lake, or Data Lakehouse, never to the primary OLTP database.
- **MUST** use ETL or ELT pipelines to decouple the extraction of operational data from the heavy transformation and batch processing required for analytics.
- **DO NOT** use single-row `INSERT` or `UPDATE` operations when writing the output of a batch job to a column-oriented storage engine.
- **MUST** utilize bulk imports to write data in large batches, amortizing the heavy cost of rewriting compressed columnar files.
- **MUST** design long-running batch jobs to periodically checkpoint their computational state to disk.
- **MUST** handle node failures during batch jobs by stopping the affected cluster workload, repairing the faulty node, and restarting the computation from the last successfully written checkpoint.
- **MUST** utilize vectorized processing (processing values in batches) for complex calculations over large datasets to keep CPU pipelines busy and minimize cache misses.
- **DO NOT** implement interactive, human-in-the-loop wait states within a batch processing pipeline; the process must run autonomously over accumulated data.
- **MUST** treat all data produced by batch processing pipelines as derived data, ensuring it can be deterministically recreated from the original system of record if lost.
- **MUST** use immutable, schema-driven binary file formats (e.g., Parquet, Avro) when dumping batch data to object storage to ensure forward and backward compatibility.

# @Workflow
1. **Workload Classification**: Evaluate the incoming request to determine if it requires periodic crunching of accumulated data (Batch/OLAP) or low-latency, interactive point queries (OLTP).
2. **Environment Isolation**: If classified as a batch workload, ensure the architecture targets a separate derived data system (Data Warehouse/Lake) to prevent impacting operational databases.
3. **Data Ingestion Pipeline (ETL)**:
    - *Extract*: Pull data from the operational systems or SaaS APIs (using tools or periodic data dumps).
    - *Transform*: Clean and map the data into an analysis-friendly schema (e.g., star/snowflake schema) or keep it raw for a data lake.
    - *Load*: Write the data into the analytical storage engine exclusively using bulk import techniques.
4. **Batch Execution**:
    - Structure the batch query or computation using vectorized processing to operate on chunks of columnar data in memory.
    - Implement periodic checkpointing to disk throughout the execution lifecycle.
5. **Fault Recovery**:
    - Monitor for node or network failures during the batch run.
    - If a failure occurs, halt the specific cluster workload, repair the node, and resume from the most recent checkpoint rather than starting from the beginning.
6. **Output Management**: Store the final aggregated results as derived datasets, ensuring they are reproducible from the raw data sources.

# @Examples (Do's and Don'ts)

- **[DO]**: Build an ETL pipeline that dumps transactional data nightly into an object store, transforms it, and bulk-loads it into a columnar data warehouse for business analysts to run complex batch queries.
- **[DON'T]**: Write an application feature that runs a `SELECT SUM(revenue) FROM sales` query across 50 million rows directly on the customer-facing OLTP database during peak traffic hours.

- **[DO]**: When writing output from a batch job into a column-oriented storage engine, accumulate the results in memory and flush them to disk as a single, large, compressed bulk write.
- **[DON'T]**: Iterate through the results of a batch job and execute individual `INSERT` statements for each row into a columnar database, which will cause massive write amplification and terrible performance.

- **[DO]**: Design a 10-hour data crunching batch job to write its state to disk every 30 minutes, so a server crash at hour 9 only requires re-running the last 30 minutes.
- **[DON'T]**: Execute a massive batch transformation entirely in memory without checkpointing, requiring the entire process to start over from hour zero if a transient fault occurs.

- **[DO]**: Use explicit schema-backed formats like Avro or Parquet when exporting raw batch data to a data lake, ensuring that newer reader code can safely parse data dumped by older writer code.
- **[DON'T]**: Dump large batch datasets into unstructured CSV files without a schema, risking silent data corruption if a column is added or removed in the upstream database.