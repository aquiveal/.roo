# @Domain
Triggered when the user requests database architecture design, storage engine selection, data modeling for performance, index optimization, query tuning, data warehouse design, or the implementation of advanced search systems (full-text, spatial, or semantic vector search). 

# @Vocabulary
- **Log**: An append-only sequence of records on disk, used for fast writes.
- **Hash Index**: An in-memory hash map mapping keys to byte offsets in a log file.
- **SSTable (Sorted String Table)**: A log-structured file format where key-value pairs are sorted by key, allowing for sparse in-memory indexes and block compression.
- **Memtable**: An in-memory tree data structure (like a red-black tree or skip list) used to buffer writes and keep them sorted before flushing to an SSTable on disk.
- **LSM-Tree (Log-Structured Merge-Tree)**: A storage engine architecture that buffers writes in a Memtable and flushes them to immutable SSTable segment files, which are periodically merged and compacted.
- **Compaction**: The background process of merging SSTable segments and discarding overwritten or deleted values.
- **Tombstone**: A special deletion record appended to an LSM-tree log to indicate that previous values for a key should be discarded during compaction.
- **Bloom Filter**: A memory-efficient, probabilistic data structure included in SSTables to quickly test whether a key is *not* present in the file, preventing unnecessary disk reads.
- **Size-Tiered Compaction**: A compaction strategy where newer/smaller SSTables are merged into older/larger ones; optimizes for write throughput.
- **Leveled Compaction**: A compaction strategy where key ranges are split into smaller SSTables and organized by "levels"; optimizes for read performance and disk space.
- **B-Tree**: A ubiquitous update-in-place indexing structure that breaks the database down into fixed-size blocks (pages), maintaining keys in sorted order within a balanced tree.
- **Write-Ahead Log (WAL) / Redo Log**: An append-only file to which every database modification is written *before* it is applied to the main data structure (like a B-Tree), ensuring crash recovery.
- **Write Amplification**: A metric representing the total number of bytes written to the underlying disk divided by the number of bytes written by the application.
- **Garbage Collection (GC) (SSD context)**: The process within an SSD controller of moving valid pages to new blocks before erasing old blocks; heavily impacted by random vs. sequential writes.
- **Clustered Index**: A secondary index where the actual row/document data is stored directly within the index structure.
- **Heap File**: An unordered storage file for actual data, referenced by secondary indexes.
- **Covering Index (Index with Included Columns)**: An index that stores some of a table's columns alongside the index key, allowing specific queries to be answered without accessing the heap file.
- **Column-Oriented (Columnar) Storage**: A storage layout where all values from one column are stored contiguously, optimizing analytical queries that scan few columns over many rows.
- **Bitmap Encoding**: A column compression technique where columns with low cardinality are converted into bit arrays (one per distinct value) indicating the presence of that value per row.
- **Run-Length Encoding (RLE)**: A compression technique that counts consecutive zeros or ones in a sparse bitmap, drastically reducing storage size.
- **Query Compilation**: An analytical query execution technique where the query engine generates and compiles machine code specific to the query to avoid interpreter overhead.
- **Vectorized Processing**: An analytical query execution technique where tightly written loops process batches of column values (vectors) utilizing CPU cache and SIMD instructions.
- **Data Cube (OLAP Cube)**: A grid of precomputed aggregates grouped by different dimensions, serving as a specialized materialized view for extremely fast analytical queries.
- **R-Tree / Bkd-Tree**: Specialized multidimensional indexes that group nearby data points into subtrees, used heavily for spatial/geospatial queries.
- **Inverted Index**: A search index structure mapping terms (words) to postings lists (lists of document IDs containing the term).
- **Levenshtein Automaton**: A finite state automaton used in inverted indexes to efficiently search for words within a specific edit distance (typo tolerance).
- **Vector Embedding**: A list of floating-point numbers representing a document's semantic meaning as a point in a multidimensional space.
- **HNSW (Hierarchical Navigable Small World)**: An approximate nearest neighbor index for vector embeddings that maintains multiple graph layers to quickly route queries to proximal vectors.
- **IVF (Inverted File) Index**: An approximate nearest neighbor index that clusters the vector space into partitions (centroids) to limit the search space to a few nearby clusters (probes).

# @Objectives
- Evaluate and select the optimal storage engine architecture (Log-Structured vs. Update-In-Place) based on the application's precise read/write ratio and latency requirements.
- Engineer data access paths using primary, secondary, clustered, and covering indexes to strictly eliminate $O(n)$ full-table scans for operational workloads.
- Design analytical (OLAP) systems using column-oriented storage, ensuring high compression via sort keys, bitmap encoding, and run-length encoding.
- Mitigate hardware-level storage degradation (e.g., SSD write wear) by minimizing write amplification through sequential write patterns and appropriate compaction strategies.
- Ensure strict durability and consistent crash recovery by mandating Write-Ahead Logs (WAL) for B-Trees and append-only recovery logs for Memtables.
- Implement advanced search architectures mapping specific query needs to their mathematical index structures (R-trees for spatial, Inverted Indexes for text, HNSW/IVF for semantic vectors).

# @Guidelines
- **Storage Engine Selection:**
  - The AI MUST select **LSM-Trees (Log-Structured Merge-Trees)** for workloads requiring extremely high write throughput, as they convert random writes into sequential writes, which are significantly faster on magnetic disks and cause less wear on SSDs.
  - The AI MUST select **B-Trees** for workloads requiring predictable, consistent read latencies, as they avoid the background compaction spikes inherent in LSM-Trees and require checking only one tree path.
- **LSM-Tree Implementation Rules:**
  - MUST buffer incoming writes in an in-memory `Memtable` while simultaneously appending to an un-sorted disk log strictly for crash recovery.
  - MUST flush the `Memtable` to an immutable `SSTable` on disk once a size threshold is reached.
  - MUST implement a `Tombstone` marker for deletions; NEVER delete data in-place.
  - MUST attach a `Bloom Filter` to each SSTable to prevent unnecessary disk reads for keys that do not exist.
  - MUST configure `Size-tiered compaction` for write-heavy workloads (merges small SSTables into larger ones).
  - MUST configure `Leveled compaction` for read-heavy workloads (splits ranges into levels to minimize read amplification).
- **B-Tree Implementation Rules:**
  - MUST organize data into fixed-size pages (e.g., 4 KiB to 16 KiB) with references acting as on-disk pointers.
  - MUST write every modification to a `Write-Ahead Log (WAL)` before updating the B-Tree page to ensure resilience against crashes during page splits.
  - MUST handle updates in-place, meaning a page is overwritten directly on the disk.
  - When preventing fragmentation over time, MUST implement or recommend a vacuum/de-fragmentation background process.
- **Secondary Indexing Constraints:**
  - When designing a schema, the AI MUST explicitly define the secondary index resolution path:
    1. **Clustered**: Store the entire row inside the index.
    2. **Heap File**: Store only a reference to an unordered data file.
    3. **Covering**: Store the exact columns required by frequent queries directly in the index to prevent heap lookups.
  - NEVER implement an on-disk hash map for massive datasets due to poor random I/O performance and expensive resizing.
- **Analytical (OLAP) Storage Rules:**
  - NEVER use row-oriented OLTP storage for analytical queries that aggregate a few columns over millions of rows.
  - MUST use **Column-Oriented Storage** (e.g., Parquet, ORC) to minimize disk I/O by parsing only the required columns.
  - MUST design a sort order for columnar tables. Use the most frequently filtered dimension (e.g., `date_key`) as the primary sort key to maximize run-length encoding (RLE) compression efficiency.
  - MUST apply `Bitmap Encoding` and `Run-Length Encoding` to columns with low cardinality (e.g., product categories, store IDs).
  - MUST utilize `Vectorized Processing` or `Query Compilation` for executing analytical queries to maximize CPU cache utilization and minimize branch mispredictions.
  - MUST use `Materialized Views` or `Data Cubes` to precompute and store heavily repeated multidimensional aggregations.
- **Advanced Indexing and Search:**
  - For spatial/geospatial queries (e.g., bounding boxes), MUST recommend multidimensional indexes like `R-Trees` or `Bkd-Trees`. NEVER use simple concatenated indexes for 2D bounding boxes.
  - For full-text search, MUST recommend `Inverted Indexes` mapping terms to postings lists (bitmaps/arrays of document IDs).
  - For typo tolerance, MUST recommend `Levenshtein Automatons` or n-gram (trigram) indexes.
  - For semantic search and vector embeddings, MUST NOT use exact nearest neighbor (Flat) indexes for large datasets due to $O(n)$ latency. MUST use approximate nearest neighbor (ANN) indexes like `HNSW` (for layered graph routing) or `IVF` (for partition/centroid routing).

# @Workflow
1. **Workload Profiling:**
   - Determine if the workload is OLTP (interactive, point queries, frequent updates) or OLAP (batch, large scans, aggregations).
   - Calculate the read-to-write ratio and identify if writes are highly random or sequential.
2. **Core Storage Engine Design:**
   - If OLTP + Write-Heavy -> Design LSM-Tree architecture (define Memtable, SSTable, Bloom filters, Compaction strategy).
   - If OLTP + Read-Heavy -> Design B-Tree architecture (define page size, branching factor, WAL mechanism).
   - If OLAP -> Design Columnar architecture (define column layout, block partitioning, file format).
3. **Data Layout and Compression Optimization:**
   - For Columnar OLAP, define the primary and secondary sort keys.
   - Map low-cardinality columns to Bitmap encodings and apply Run-Length Encoding.
4. **Index Strategy Formulation:**
   - Define the Primary Key index.
   - Map out Secondary Indexes. Assign them as Clustered, Heap-referencing, or Covering based on specific query payload requirements.
   - Identify specialized index needs (R-Trees for location, Inverted Indexes for text, HNSW/IVF for semantic vectors) and map them to the corresponding data fields.
5. **Durability and Crash Recovery Verification:**
   - Explicitly define the crash recovery mechanism (WAL for B-Trees, separate append-only log for Memtables).
   - Verify that updates do not corrupt data if the system loses power mid-write.

# @Examples (Do's and Don'ts)

- **Storage Engine Selection**
  - [DO]: Recommend an LSM-Tree (like RocksDB or Cassandra) for an IoT application ingesting millions of sensor readings per minute, because the append-only nature eliminates random write penalties.
  - [DON'T]: Recommend a B-Tree for a massive write-heavy workload without warning about write amplification and SSD wear from constant page overwrites and splits.

- **Index Design**
  - [DO]: Use a Covering Index for a query `SELECT name FROM users WHERE age > 30` by creating an index on `age` that includes `name`, entirely skipping the heap file lookup.
  - [DON'T]: Create a concatenated index on `(latitude, longitude)` for a map bounding-box query, because B-Trees cannot efficiently query ranges on both dimensions simultaneously. Use an R-tree instead.

- **Analytical Queries**
  - [DO]: Store data in a columnar format (like Parquet) sorted by `date` to allow a query summing `sales` over a specific month to read only the compressed `date` and `sales` files from disk.
  - [DON'T]: Run a `SUM(sales)` query over 500 million rows in a row-oriented PostgreSQL database without expecting massive I/O bottlenecks, as the engine must load the entire row from disk just to extract the `sales` integer.

- **Vector Search**
  - [DO]: Use an HNSW index for a semantic text search engine to quickly traverse a multi-layered graph to find the nearest vector embeddings in logarithmic time.
  - [DON'T]: Use a Flat index for 10 million vector embeddings in production, as calculating the cosine similarity for every single vector per query will cripple system latency.

- **Crash Recovery**
  - [DO]: Append writes to an unstructured Write-Ahead Log on disk *before* updating a B-Tree page in memory.
  - [DON'T]: Keep writes exclusively in a Memtable without a backing disk log, as a power failure will result in total data loss of the un-flushed writes.