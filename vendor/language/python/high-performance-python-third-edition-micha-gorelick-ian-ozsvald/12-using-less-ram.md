# @Domain
These rules MUST be triggered when the AI is tasked with optimizing Python code for memory usage, reducing RAM footprints, handling large datasets, performing memory profiling, selecting data structures for high-volume text or numerics, managing large sparse matrices, or implementing approximate/probabilistic counting and membership algorithms.

# @Vocabulary
- **Contiguous Memory**: Memory allocated in a single unbroken block (e.g., `array.array`, `numpy.array`), drastically reducing overhead compared to Python lists which store scattered object references.
- **Lazy Allocation**: An OS-level behavior where memory is not truly consumed until it is written to. (e.g., `np.zeros` is lazily allocated, `np.ones` is strictly allocated).
- **Temporary Arrays**: Invisible intermediate arrays created during complex vectorized operations in NumPy or Pandas, causing massive hidden RAM spikes.
- **NumExpr**: A library that breaks vectorized calculations into cache-friendly chunks, avoiding the creation of large temporary arrays and accelerating computation.
- **Trie (Prefix Tree) / DAWG (Directed Acyclic Word Graph)**: Tree-like data structures that compress text by sharing common prefixes (and suffixes in DAWGs) to massively reduce RAM usage for string collections.
- **Marisa Trie**: A highly RAM-efficient, static (read-only after creation) trie data structure using Cython bindings.
- **Hashing Trick / FeatureHasher**: A method of converting text tokens into a fixed-width sparse matrix via a hash function (like MurmurHash3) without storing a memory-expensive vocabulary.
- **Sparse Matrix (COO, CSR, CSC)**: A matrix representation that only stores non-zero elements. COO is used for construction; CSR/CSC are used for computation.
- **Probabilistic Data Structures**: Data structures that trade exact accuracy for massive memory reductions (lossy compression of state).
- **Morris Counter**: A probabilistic counter that tracks an exponent to estimate magnitude (counts up to ~5e76 using only 1 byte).
- **K-Minimum Values (KMV)**: A structure that estimates the cardinality (number of unique items) by tracking the spacing of the $k$ smallest unique hash values. Error rate is $O(1/\sqrt{k})$. Idempotent.
- **Bloom Filter**: A bit-array structure using multiple hash functions to test set membership. Guarantees no false negatives, but allows a controllable rate of false positives.
- **Scalable / Timing Bloom Filters**: Variants of the Bloom filter that either dynamically chain new filters when capacity is reached or expire old elements to handle infinite data streams.
- **LogLog / HyperLogLog (HLL / HLL++)**: Cardinality estimators that track the maximum number of trailing or leading zeros in binary hashes. HLL++ uses spherical averaging for highly accurate estimates ($O(1.04/\sqrt{m})$ error) using mere kilobytes of RAM.

# @Objectives
- Ruthlessly minimize the RAM footprint of Python applications.
- Prevent Out of Memory (OOM) errors caused by hidden temporary arrays in mathematical operations.
- Avoid the overhead of Python objects (28+ bytes for an integer) when storing millions of primitive items.
- Select the most memory-efficient string storage and NLP feature extraction mechanisms.
- Aggressively trade exactness for memory using probabilistic data structures when precise counts or set memberships are not strictly required by the business logic.

# @Guidelines

## Profiling Memory
- The AI MUST NOT rely exclusively on `sys.getsizeof()` for measuring container RAM usage, as it only reports the shallow size of the container, ignoring the sizes of referenced contents.
- The AI MUST NOT rely exclusively on `pympler.asizeof()`, as it is extremely slow and relies on guessing/inference which often misses C-library level allocations.
- The AI MUST use OS-level process measuring tools like `memory_profiler` (`%memit`) or `ipython_memory_usage` to verify true RAM consumption.
- The AI MUST restart the Python shell/process between `%memit` profiling runs to ensure cached memory does not skew results.

## Storing Primitives and Numbers
- The AI MUST NEVER use Python `list` objects to store millions of numeric types (ints, floats). Lists store pointers to heavy Python objects, wasting massive amounts of RAM.
- The AI MUST use the standard library `array.array(typecode)` for 1D storage of uniform basic primitives to ensure contiguous memory without adding external dependencies.
- The AI MUST select the smallest possible precision typecode (e.g., 2-byte floats vs 8-byte floats) necessary for the task when using `array.array` or `numpy.array`.
- The AI MUST use `numpy` arrays for multi-dimensional data, complex numbers, or when fast numeric algorithms are required.
- The AI MUST be aware of lazy allocation when profiling `numpy`. `np.zeros` may report 0 RAM increment initially until modified, whereas `np.ones` allocates immediately.

## Math and Vector Operations
- The AI MUST prevent intermediate memory spikes in complex NumPy or Pandas operations.
- The AI MUST use `numexpr.evaluate("expression")` instead of direct NumPy chained math (e.g., `A * B + C`) for large arrays.
- The AI MUST use `df.eval("expression")` in Pandas, ensuring `numexpr` is installed, to calculate columns without creating large temporary Series objects.

## Storing and Querying Text
- The AI MUST avoid storing millions of strings in a simple `list`. If a list is mandatory, the AI MUST explicitly use `.sort()` and query via the `bisect` module to achieve $O(\log n)$ lookups, avoiding $O(n)$ linear searches.
- The AI MUST use a `set` for $O(1)$ string lookups only if RAM is plentiful.
- The AI MUST recommend `marisa_trie.Trie()` when building static, read-only dictionaries of strings with overlapping prefixes to compress memory footprint drastically.

## Machine Learning & NLP Constraints
- The AI MUST use `sklearn.feature_extraction.FeatureHasher` instead of `DictVectorizer` when memory is strictly constrained. `FeatureHasher` uses the hashing trick, bypassing the creation and storage of a massive `vocabulary_` dictionary.
- The AI MUST accept that `FeatureHasher` is a one-way lossy transformation (collisions occur and `inverse_transform` is impossible).
- The AI MUST use SciPy sparse matrices (e.g., `scipy.sparse`) instead of dense NumPy matrices when the dataset consists of >=66% zeros.
- The AI MUST use COO format to construct sparse matrices, and convert to CSR or CSC format to perform mathematical operations.

## Probabilistic Data Structures
- When asked to count total events in heavily restricted RAM (e.g., embedded hardware), the AI MUST use a **Morris Counter** to approximate magnitude using a single byte (tracking an exponent updated by random probability).
- When asked to count *unique* items (cardinality) over massive datasets, the AI MUST use **HyperLogLog** (or HLL++) or **K-Minimum Values (KMV)** instead of Python `set`s.
- When asked to test if an item has been seen before (set membership) in massive datasets, the AI MUST use a **Bloom Filter** instead of a `set`.
- If the dataset size is unknown or an infinite stream, the AI MUST implement a **Scalable Bloom Filter** (dynamically allocating new filters) or a **Timing Bloom Filter** (expiring old entries) because a standard Bloom Filter degrades to 100% false positives when its capacity is exceeded.
- The AI MUST explicitly communicate the standard deviation error rate (e.g., $O(1.04/\sqrt{m})$ for HLL) when implementing probabilistic structures.

# @Workflow
1. **Analyze Constraints**: Determine if the problem is bound by RAM capacity. Confirm if precise answers are strictly required, or if probabilistic estimates are acceptable.
2. **Profile First**: Implement `memory_profiler` to identify which structures/lines are causing memory bloat.
3. **Optimize Primitives**: Convert any homogeneous numeric `list`s to `array.array` or `numpy.array` with the minimal required byte-width `dtype`.
4. **Eliminate Temporaries**: Scan all vectorized NumPy/Pandas math operations. Wrap chained operations in `numexpr.evaluate()` or `pd.eval()`.
5. **Compress Strings**: If storing large vocabularies/text corpuses, swap `set`/`dict` for `marisa_trie` or use `bisect` on a sorted list.
6. **Apply Probabilistic Structures**: If memory is still exceeded and accuracy requirements permit:
   - Swap `len(set)` with `HyperLogLog`.
   - Swap `item in set` with `BloomFilter`.
   - Swap simple total increments with `MorrisCounter`.

# @Examples (Do's and Don'ts)

## Measuring Object Memory
- **[DON'T]** Rely solely on `sys.getsizeof` for collections:
  ```python
  import sys
  # Falsely reports only the size of the list container (e.g., ~800MB), ignoring string contents.
  sys.getsizeof([str(i) for i in range(100_000_000)]) 
  ```
- **[DO]** Use `memory_profiler` for true process footprint:
  ```python
  %load_ext memory_profiler
  # Accurately measures OS-level RAM spikes
  %memit data = [str(i) for i in range(100_000_000)]
  ```

## Storing Homogeneous Numbers
- **[DON'T]** Use lists for large numeric collections:
  ```python
  # Wastes ~2.3GB of RAM overhead for Python Int objects
  my_data = [i for i in range(100_000_000)]
  ```
- **[DO]** Use `array.array` or `numpy` arrays:
  ```python
  import array
  # Uses exactly ~800MB (contiguous C-type integers)
  my_data = array.array('l', range(100_000_000))
  ```

## Vectorized Math Operations
- **[DON'T]** Chain NumPy operations directly if memory is tight:
  ```python
  import numpy as np
  # Creates massive hidden temporary arrays for (1-yt), log(yp), etc.
  answer = -(yt * np.log(yp) + ((1-yt) * (np.log(1-yp))))
  ```
- **[DO]** Use `numexpr` to chunk calculations and optimize cache, keeping RAM flat:
  ```python
  import numexpr
  # Processes in chunks; peak memory usage is drastically reduced
  answer = numexpr.evaluate("-(yt * log(yp) + ((1-yt) * (log(1-yp))))")
  ```

## Large NLP Feature Extraction
- **[DON'T]** Default to `DictVectorizer` if you have limited RAM and don't need feature inspection:
  ```python
  from sklearn.feature_extraction import DictVectorizer
  # Builds a massive, RAM-heavy dictionary vocabulary
  dv = DictVectorizer()
  X = dv.fit_transform(token_dicts)
  ```
- **[DO]** Use `FeatureHasher` to bind features to a fixed-width sparse matrix without storing vocabulary:
  ```python
  from sklearn.feature_extraction import FeatureHasher
  # Uses MurmurHash3 to map tokens to columns directly. Extremely low RAM.
  fh = FeatureHasher(n_features=1048576, alternate_sign=False)
  X = fh.transform(token_dicts)
  ```