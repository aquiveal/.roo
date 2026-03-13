@Domain
This rule file is triggered when the AI is tasked with database architecture design, storage engine selection, schema design, query optimization, indexing strategy, data warehouse configuration, or performance tuning for data-intensive applications. It applies whenever evaluating the trade-offs between different data storage formats, read/write ratios, disk I/O optimizations, and analytical versus operational query patterns.

@Vocabulary
- **Log-Structured Merge-Tree (LSM-Tree)**: A storage engine architecture that buffers writes in memory and flushes them to disk as immutable sorted segment files.
- **SSTable (Sorted String Table)**: An on-disk file format used by LSM-trees where key-value pairs are stored in sorted order.
- **Memtable**: An in-memory data structure (e.g., red-black tree, skip list) used to buffer incoming writes before flushing to an SSTable.
- **Compaction**: The background process of merging multiple SSTables, discarding deleted or overwritten values, and generating new merged segment files.
- **Bloom Filter**: A memory-efficient, probabilistic data structure used to test whether a key is present in an SSTable, preventing unnecessary disk reads (may yield false positives, but no false negatives).
- **B-Tree**: The standard update-in-place index structure that breaks the database down into fixed-size blocks/pages (e.g., 4 KiB) and builds a balanced tree of page references.
- **Write-Ahead Log (WAL) / Journal**: An append-only log used in B-trees to record every modification before it is applied to the tree pages, ensuring crash recovery.
- **Write Amplification**: The ratio of the total number of bytes written to the physical disk compared to the number of bytes written by the application to the database.
- **Clustered Index**: An index where the actual row/document data is stored directly within the index structure.
- **Heap File**: An unordered storage file for database records, typically referenced by pointers from secondary indexes.
- **Covering Index**: A secondary index that stores copies of some table columns alongside the index key, allowing queries to be satisfied without fetching the full record from the heap.
- **Column-Oriented Storage**: A storage layout where all values from a single column are stored contiguously, optimized for analytical queries.
- **Bitmap Encoding**: A compression technique for columnar storage where columns with low cardinality are represented as bitmaps (one bit per row).
- **Run-Length Encoding (RLE)**: A compression technique that counts the number of consecutive identical values (or zeros/ones in a bitmap) to save space.
- **Vectorized Processing**: A query execution optimization where operators process tight batches of column values in inner loops to utilize CPU cache and SIMD instructions.
- **Data Cube / OLAP Cube**: A materialized view representing a grid of precomputed aggregates grouped by different dimensions.
- **Inverted Index**: A search index mapping terms (words) to postings lists (the list of document IDs containing that term).
- **Vector Embedding**: A representation of document semantics as a multi-dimensional array of floating-point numbers.
- **HNSW (Hierarchical Navigable Small World)**: An approximate nearest neighbor index for fast vector search using multi-layered graphs.
- **IVF (Inverted File Index)**: A vector index that clusters the vector space into partitions (centroids) to reduce the number of vectors compared during a query.

@Objectives
- The AI MUST select the appropriate storage engine (LSM-Tree vs. B-Tree) based strictly on the application's read/write ratio and throughput constraints.
- The AI MUST minimize write amplification and optimize disk lifecycle by aligning data structures with underlying hardware characteristics (e.g., SSD garbage collection).
- The AI MUST strictly separate OLTP (row-oriented) and OLAP (column-oriented) architectural designs, preventing the conflation of transactional storage with analytical querying.
- The AI MUST design indexing strategies that reduce disk seeks, utilizing covering indexes, clustered indexes, and bloom filters where appropriate.
- The AI MUST leverage the appropriate multi-dimensional, text, or vector index for domain-specific queries (e.g., semantic search, geospatial mapping).

@Guidelines

# Storage Engine Selection (OLTP)
- When a workload is write-heavy, the AI MUST recommend an LSM-Tree storage engine (e.g., RocksDB, Cassandra, ScyllaDB) to leverage sequential writes and lower write amplification.
- When a workload is read-heavy and requires highly predictable low-latency reads, the AI MUST recommend a B-Tree storage engine (e.g., PostgreSQL, MySQL InnoDB).
- When configuring LSM-Trees, the AI MUST explicitly define the compaction strategy:
  - Use **Size-tiered compaction** for extremely high write throughput (accepting higher disk space overhead).
  - Use **Leveled compaction** for read-heavy workloads or when keeping disk space overhead low is critical.
- The AI MUST NOT recommend updating data in place for LSM-Trees. Deletions MUST be implemented using tombstones.

# Hardware Optimizations
- The AI MUST account for SSD characteristics: sequential writes (LSM-trees) are preferable to random writes (B-trees) because they cause less wear on the SSD and interact better with the SSD's internal garbage collection.
- When designing in-memory databases (e.g., Redis, VoltDB), the AI MUST clarify that the performance gains come from avoiding the CPU overhead of encoding/decoding disk formats, not merely from avoiding disk I/O (as OS page caches handle disk I/O buffering).

# Indexing Rules
- The AI MUST warn against indexing every column. It MUST evaluate and state the write penalty associated with maintaining secondary indexes.
- When designing secondary indexes, the AI MUST define whether to use a Clustered Index, a Heap File pointer, or a Covering Index based on read frequency and record size.
- To optimize LSM-Tree read performance, the AI MUST ensure Bloom filters are enabled to prevent unnecessary disk seeks for non-existent keys.

# Analytical Storage (OLAP)
- For data warehouse/analytics workloads spanning millions of rows but requiring few columns per query, the AI MUST use Column-Oriented Storage. The AI MUST NOT recommend row-oriented databases for heavy aggregations.
- The AI MUST apply Bitmap Encoding and Run-Length Encoding (RLE) to low-cardinality columns in column-store designs.
- When defining sort keys for a column store, the AI MUST sort the entire row simultaneously (not independent columns). The primary sort key MUST be chosen based on the most common range queries (e.g., date ranges) to maximize the effectiveness of RLE.
- The AI MUST buffer OLAP writes in memory and flush them in bulk (log-structured style). It MUST NOT recommend single-row inserts for columnar storage.

# Advanced Indexing (Text, Spatial, Semantic)
- For geospatial or 2D/3D range queries, the AI MUST use multi-dimensional indexes like R-trees, Bkd-trees, or space-filling curves rather than standard B-Trees.
- For full-text search, the AI MUST implement an Inverted Index using terms and postings lists, potentially leveraging n-grams for typo tolerance or Levenshtein automata.
- For semantic search and unstructured concepts, the AI MUST utilize Vector Embeddings and specify an approximate nearest neighbor index (HNSW or IVF). The AI MUST NOT use B-trees for multi-dimensional vector comparisons.

@Workflow
1. **Workload Characterization**: Determine if the task involves OLTP (point queries, transactional updates) or OLAP (bulk scans, aggregations, data mining). Evaluate the read-to-write ratio.
2. **Storage Architecture Selection**:
   - For OLTP write-heavy: Select Log-Structured Merge-Trees (LSM).
   - For OLTP read-heavy/predictable latency: Select B-Trees with a Write-Ahead Log (WAL).
   - For OLAP: Select Columnar Storage separated from compute (Cloud Data Warehouse patterns).
3. **Index Strategy Formulation**:
   - Define the Primary Key strategy.
   - Define Secondary Indexes, specifying if they should be Clustered, Covering, or use a Heap File.
   - If utilizing LSM-Trees, mandate the inclusion of Bloom Filters.
4. **OLAP Optimization (If applicable)**:
   - Define the primary and secondary sort keys to group data and maximize Run-Length Encoding (RLE).
   - Specify whether query execution should utilize JIT Query Compilation or Vectorized Processing.
   - Design Materialized Views or Data Cubes for frequently executed aggregate queries.
5. **Advanced Capabilities Integration**:
   - If the request involves text, spatial, or semantic retrieval, attach the appropriate specialized index (Inverted Index, R-Tree, HNSW/IVF).

@Examples (Do's and Don'ts)

# Storage Engine Selection
- [DO]: Recommend LSM-trees (e.g., RocksDB) for logging application events where the write throughput is massive and updates are rare.
- [DON'T]: Recommend a B-tree for high-throughput, unstructured event logging, as the random write pattern will cause severe page fragmentation and wear out the SSD prematurely due to write amplification.

# Indexing
- [DO]: Use a covering index (`INCLUDE` columns in SQL) for a highly trafficked read query so the database can return the result entirely from the index without performing a heap file lookup.
- [DON'T]: Create a secondary index for every column in a table "just in case," as every index multiplies the write amplification and slows down insert/update performance.

# LSM-Tree Reads
- [DO]: Configure a Bloom filter on SSTables to immediately return "not found" for missing keys, saving expensive disk seeks.
- [DON'T]: Rely purely on the sparse index to look up keys that frequently do not exist in the dataset, as this forces the engine to decode blocks unnecessarily.

# Columnar Storage for Analytics
- [DO]: Sort a columnar fact table first by `date_key` and then by `product_id` so that Run-Length Encoding can highly compress consecutive rows with identical dates and products.
- [DON'T]: Sort columns independently of one another in a columnar database, as this destroys the ability to reconstruct a single row across multiple columns.

# Vector & Semantic Search
- [DO]: Use an HNSW or IVF index for a recommendation system comparing 1000-dimensional vector embeddings via cosine similarity.
- [DON'T]: Attempt to store and query high-dimensional vectors in a traditional relational B-tree using concatenated indexes.