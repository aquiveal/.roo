## @Domain
Activation conditions: The AI MUST activate these rules when handling tasks, files, or user requests involving large-scale offline data transformations, ETL (Extract, Transform, Load) pipelines, distributed joins, MapReduce algorithms, dataflow engine configurations (e.g., Apache Spark, Apache Flink in batch mode), and bulk data processing systems. 

## @Vocabulary
- **Batch Processing**: The processing of a bounded, known-size dataset where a job reads all input data, processes it, and produces an output.
- **MapReduce**: A low-level programming model and distributed execution framework for batch processing consisting of Map, Shuffle, and Reduce phases.
- **Mapper**: A function that reads an input record, parses it, and extracts a key and a value. It does not maintain state across records.
- **Reducer**: A function that takes a key and an iterator over all values associated with that key, and produces output records.
- **Shuffle**: The process of sorting the outputs of mappers by key, partitioning them, and transferring them across the network to the appropriate reducers.
- **Materialization**: The act of writing the intermediate state or output of a processing stage to durable storage (like a distributed filesystem) before the next stage begins.
- **Dataflow Engine**: Advanced batch processing systems (like Spark) that model a job as a Directed Acyclic Graph (DAG) of operators, avoiding unnecessary materialization of intermediate state to disk.
- **Sort-Merge Join**: A distributed join strategy where both datasets are partitioned by the join key, sorted, and then merged sequentially.
- **Broadcast Hash Join**: A distributed join strategy used when one dataset is small enough to fit in memory. The small dataset is broadcast to all machines processing the large dataset and loaded into an in-memory hash table.
- **Partitioned Hash Join (Grace Hash Join)**: A join where both datasets are partitioned by the hash of the join key, and each partition is joined independently in memory.
- **Skew / Hot Key**: A phenomenon where a small number of keys have a disproportionately large amount of data, causing specific partitions (and the nodes processing them) to become bottlenecks.
- **Deterministic / Pure Function**: A function that always produces the same output for the same input and has no external side effects (e.g., modifying external databases).

## @Objectives
- Architect batch processing pipelines that maximize overall throughput rather than minimizing individual request latency.
- Ensure absolute fault tolerance by designing all processing steps to be safely retryable upon node failure.
- Optimize distributed join performance by dynamically selecting the correct join algorithm based on dataset sizes.
- Eliminate straggler tasks by actively mitigating data skew and hot keys.
- Minimize disk I/O and network overhead by leveraging memory-optimized dataflow engines instead of strict materialization.

## @Guidelines
- **Immutability of Inputs**: The AI MUST treat all batch job inputs as strictly immutable. Output MUST be written to a new location or a new version of the dataset.
- **Determinism Constraint**: The AI MUST design all map, reduce, and transformation functions to be purely deterministic. They MUST NOT depend on real-time clocks, random number generators (without fixed seeds), or external mutable state.
- **Zero Side-Effects Rule**: The AI MUST NEVER include cross-system side effects (e.g., making network requests to external APIs or performing `UPDATE` queries on operational databases) inside a map or reduce function.
- **Join Strategy Selection**:
  - The AI MUST select a **Broadcast Hash Join** if one of the datasets can comfortably fit in the RAM of a single node.
  - The AI MUST select a **Sort-Merge Join** or **Partitioned Hash Join** if both datasets are too large to fit in memory.
- **Skew Mitigation**: When joining or grouping data, the AI MUST explicitly check for or anticipate skewed keys. If hot keys exist, the AI MUST implement a skew-handling strategy, such as adding random salts to the skewed keys to distribute the load across multiple reducers (a two-stage aggregation).
- **Engine Selection**: The AI MUST prefer configuring pipelines as DAGs in a Dataflow Engine (like Spark) over traditional MapReduce to enable pipelining and minimize the costly materialization of intermediate files to disk.
- **Atomic Commits**: Output operations MUST be atomic. The AI MUST ensure that a batch job writes to a temporary directory and renames it to the final destination only upon successful completion, preventing downstream systems from reading partial outputs.

## @Workflow
1. **Input Analysis**: Identify the bounded datasets to be processed. Determine their sizes, data formats, and partition schemas.
2. **Algorithm Design**: Map the business logic into a series of pure transformation functions (e.g., map, filter, group, reduce).
3. **Join Optimization**: Evaluate the relative sizes of datasets requiring joins. Assign the appropriate distributed join strategy (Broadcast vs. Sort-Merge).
4. **Skew Assessment**: Analyze the grouping/join keys for potential skew. If a few keys dominate, inject a two-stage aggregation algorithm (salting) into the pipeline.
5. **DAG Construction**: Chain the operations into a Directed Acyclic Graph. Avoid forcing data to disk between stages unless explicitly required for a fault-tolerance checkpoint.
6. **Output and Commit**: Design the final write stage to output immutable files to a hidden/temporary path, followed by a deterministic, atomic filesystem rename operation to expose the data.

## @Examples (Do's and Don'ts)

### Determinism and Side Effects
- **[DO]**: Pass external configuration or reference data into the job at initialization time (e.g., via a broadcast variable) and use it as an immutable lookup table within the mapper.
- **[DON'T]**: Write code inside a mapper that makes an HTTP POST request to an external service to update a record. If the map task fails and is retried by the framework, the external service will be hit multiple times, corrupting external state.

### Join Strategy Selection
- **[DO]**: Use a Broadcast Hash Join when joining a 10-Terabyte fact table of user events with a 50-Megabyte dimension table of user demographic data.
- **[DON'T]**: Force a Sort-Merge Join with a shuffle phase on both datasets when one dataset is tiny, as this incurs massive unnecessary network I/O and sorting overhead.

### Handling Data Skew
- **[DO]**: When counting events by user ID, and a few "celebrity" users have millions of events while others have ten, append a random integer (salt) between 1 and 100 to the celebrity user IDs. Perform a pre-aggregation on the salted keys, then remove the salt and perform a final aggregation.
- **[DON'T]**: Use a standard `GROUP BY` on a highly skewed dataset. This will cause all records for the celebrity user to be sent to a single reducer, creating a straggler task that causes 99% of the cluster to sit idle while one node chokes.

### Atomic Outputs
- **[DO]**: Write the batch job output to `s3://bucket/output_tmp_jobID/`, and upon successful job completion, atomically rename or move it to `s3://bucket/output_final/`.
- **[DON'T]**: Write records directly to `s3://bucket/output_final/` during the map/reduce execution. If the job crashes halfway through, downstream consumers will read partial, corrupted data.