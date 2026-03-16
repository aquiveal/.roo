# @Domain
These rules MUST be activated when the user requests assistance with tabular data processing, dataframe manipulation, time-series data analysis, or performance optimization for data science pipelines using Python. Specific triggers include the use of `pandas`, `dask`, `polars`, `swifter`, dataframe transformations, row-wise function applications, and out-of-core/larger-than-RAM data processing.

# @Vocabulary
- **DataFrame / Series**: 2D and 1D tabular data structures holding heterogeneous datatypes.
- **BlockManager**: The internal Pandas machinery that groups columns of the same dtype together into contiguous memory blocks to accelerate operations.
- **Extension Types**: Pandas-specific datatypes (e.g., nullable `Int64`, `boolean`) that handle missing data (NaN) without implicitly casting integers or booleans to floats.
- **PyArrow Backend**: An alternative memory backend for Pandas utilizing Apache Arrow, highly optimized for string data and compressed representations.
- **raw=True**: An argument for Pandas `.apply()` that passes the underlying NumPy array to the applied function, avoiding the overhead of creating intermediate Pandas Series objects.
- **Numba Engine**: A JIT compiler backend that can be invoked within Pandas (e.g., `engine="numba"`) to compile mathematical operations to machine code dynamically.
- **Distributed DataFrame (Dask)**: A virtual dataframe representing multiple Pandas DataFrames partitioned along an index, allowing parallel and larger-than-RAM processing.
- **Task Graph**: A delayed, acyclic graph of discrete execution steps used by Dask to lazily evaluate data pipelines.
- **dask-expr**: Dask's query optimization framework that automatically reorders and compresses steps (like predicate pushdown and column projection) to reduce data I/O.
- **Swifter**: A library that heuristically determines whether to vectorize or use Dask to parallelize Pandas `.apply()` operations.
- **Polars**: A highly performant, Arrow-backed dataframe library with a built-in query optimizer and a strict, consistent API.

# @Objectives
- Maximize execution speed of row-wise and column-wise dataframe operations by bypassing virtual machine and intermediate object overhead.
- Minimize RAM consumption by preventing unnecessary memory copies, utilizing optimal datatypes, and avoiding intermediate object creation.
- Ensure data schema integrity and maintainable, debuggable code.
- Seamlessly scale compute from single-threaded Pandas to multi-core (Dask/Swifter) or optimized multi-engine (Polars) paradigms based on data size and compute complexity.

# @Guidelines

## Pandas Internal Architecture & Memory Management
- The AI MUST select the PyArrow backend (`dtype="string[pyarrow]"`) for string data to save RAM and improve execution speed over standard Python strings.
- The AI MUST use NumPy backends for numeric data ONLY IF planning to use Numba compilation (Numba does not currently support Arrow arrays).
- The AI MUST use Pandas nullable extension types (e.g., `Int64`, `boolean`) when dealing with integer or boolean data that contains `NaN` values, preventing unwanted coercion to `float64` (which increases memory footprint and loses precision).
- The AI MUST downcast large numeric types (e.g., `float64` to `float16`, `int64` to `int8`) when the data range safely permits it, to reduce RAM pressure.
- The AI MUST cast low-cardinality string columns to `Category` dtype (`.astype('category')`) to accelerate operations like `groupby` and drastically reduce RAM usage.
- The AI MUST use the `del` keyword to explicitly free memory of large DataFrames when they are no longer needed.
- The AI MUST AVOID the `inplace=True` argument, as it is scheduled for deprecation and often does not prevent memory copies internally.

## Row-Wise Operations and Function Application
- The AI NEVER MUST use `for` loops with `.iloc[]` to iterate over DataFrame rows. This is the absolute slowest approach due to fresh Series creation and dereferencing overhead.
- The AI MUST AVOID `.iterrows()` and `.itertuples()` for mathematical or heavy computations.
- The AI MUST PREFER `.apply(..., axis=1)` for idiomatic row-wise function execution.
- The AI MUST USE `.apply(..., axis=1, raw=True)` whenever the applied function does not require Pandas Series methods. Passing `raw=True` feeds a pure NumPy array to the function, stripping away Series creation overhead.

## Computation and Validation Overhead
- The AI MUST evaluate the necessity of safety checks in libraries like `scikit-learn` (which run expensive `_validate_data` and `_preprocess_data` checks). If data is guaranteed to be clean, the AI MUST PREFER direct linear algebra implementations (e.g., `np.linalg.lstsq` instead of `LinearRegression().fit()`) to eliminate up to 85% of execution overhead.
- The AI MUST utilize Numba for complex numeric row operations. Use `df.apply(func, engine="numba", raw=True)` or decorate the target function with `@numba.jit(nopython=True)`.
- To parallelize Numba operations, the AI MUST pass `engine_kwargs={'parallel': True}`.

## Building DataFrames and Iteration
- The AI NEVER MUST iteratively call `pd.concat()` or `df.append()` inside a loop. This leads to quadratic execution time due to repeated memory reallocation.
- To build a DataFrame dynamically, the AI MUST accumulate partial results in a standard Python list (or dictionary) and execute a single `pd.DataFrame(list_of_results)` or `pd.concat()` call at the very end.

## String Processing in Pandas
- When parsing strings, the AI MUST evaluate whether chaining multiple Pandas `.str` accessors (e.g., `df['col'].str.split().str[1].str.find()`) creates excessive intermediate Series objects.
- If intermediate Series creation causes memory or speed bottlenecks, the AI MUST replace `.str` chains with a single `.apply()` mapping a custom Python string-processing function line-by-line.

## General Best Practices for Data Pipelines
- The AI MUST verify that optional dependencies `numexpr` and `bottleneck` are installed to automatically accelerate Pandas `.eval()` and background routines.
- The AI MUST filter data/rows BEFORE applying heavy calculations, not after. Push filtering down to the SQL query level if importing from a database.
- The AI MUST validate schemas programmatically at runtime using a tool like `pandera` to prevent downstream pipeline errors.
- The AI MUST keep pipelines readable. AVOID excessively long method chains that obscure tracebacks.
- The AI MUST persist heavy intermediate prepared DataFrames to disk using `df.to_pickle()` or Parquet format to prevent redundant processing during iterative development.

## Scaling with Dask and Swifter
- When datasets exceed RAM or require multi-core execution without manual multiprocessing, the AI MUST switch to Dask DataFrames.
- The AI MUST set Dask `npartitions` to roughly match or exceed the number of physical CPU cores.
- For Pandas/GIL-bound workloads in Dask, the AI MUST execute with `compute(scheduler='processes')` rather than the default thread scheduler.
- The AI MUST leverage `dask-expr` to automatically compress operations, avoiding manual column projection and predicate filtering.
- For a single-line parallelization upgrade to Pandas, the AI MUST suggest `swifter` (`df.swifter.apply(...)`).

## Scaling with Polars
- For new projects or pipelines requiring optimal single-machine performance, the AI MUST PREFER Polars over Pandas.
- The AI MUST leverage Polars' lazy execution (`.lazy()`, `.collect()`) to allow the built-in query optimizer to automatically parallelize execution and prune unnecessary data loads.
- For larger-than-RAM datasets in Polars, the AI MUST enable experimental streaming mode via `.collect(streaming=True)`.

# @Workflow
1. **Analyze Data Constraints:** Evaluate if the dataset fits in RAM (use Pandas/Polars) or exceeds RAM (use Dask/Polars Streaming).
2. **Optimize Datatypes:** Convert strings to PyArrow or Categories. Downcast floats/integers. Use Pandas nullable extension types for data with NaNs.
3. **Filter First:** Apply predicate masks and drop unused columns before any compute tasks.
4. **Refactor Iteration:** Replace any `iloc` or `iterrows` loops with `.apply()`. If the logic is purely numerical, add `raw=True`.
5. **Compile & Vectorize:** If numerical logic is complex, wrap the target function in Numba or use the `engine="numba"` parameter.
6. **Eliminate Intermediate Copies:** Remove iterative `pd.concat()` calls. Replace chained `.str` methods with unified `.apply()` functions if string parsing is slow.
7. **Scale Up:** If CPU-bound, apply `Swifter`. If system-bound, convert to Dask DataFrame or rewrite in Polars utilizing lazy query optimization.

# @Examples (Do's and Don'ts)

## Building DataFrames
- **[DON'T]** Use `concat` iteratively in a loop:
  ```python
  results = None
  for row_idx in range(df.shape[0]):
      row = df.iloc[row_idx]
      m = calculate_value(row)
      if results is None:
          results = pd.Series([m])
      else:
          results = pd.concat((results, pd.Series([m]))) # Highly inefficient memory copying
  ```
- **[DO]** Collect in a list and create the structure once:
  ```python
  ms = []
  for row_idx, row in df.iterrows():
      m = calculate_value(row)
      ms.append(m)
  results = pd.Series(ms) # Single allocation
  ```

## Row-Wise Operations
- **[DON'T]** Use `iloc` to fetch rows for computation:
  ```python
  ms = []
  for row_idx in range(df.shape[0]):
      row = df.iloc[row_idx] # Horribly slow, creates fresh Series on every tick
      ms.append(ols_lstsq(row))
  ```
- **[DO]** Use `apply` with `raw=True` to pass underlying NumPy arrays directly:
  ```python
  # Idiomatic, bypasses Series creation overhead
  ms = df.apply(ols_lstsq_raw, axis=1, raw=True)
  results = pd.Series(ms)
  ```

## String Processing
- **[DON'T]** Chain multiple `.str` methods if it creates large intermediate Series objects unnecessarily:
  ```python
  # Creates multiple intermediate DataFrames/Series in memory
  locations = df['text_col'].str.split('.', expand=True)[1].str.find('9')
  ```
- **[DO]** Use a custom function via `apply` for complex parsing to reduce overhead:
  ```python
  def find_9(s):
      return s.split('.')[1].find('9')

  # Operates line-by-line without intermediate object creation
  locations = df['text_col'].apply(find_9)
  ```

## Compiling DataFrame Calculations
- **[DON'T]** Rely on standard Python execution for heavy math inside an apply call.
- **[DO]** Use Numba for an order-of-magnitude speedup:
  ```python
  from numba import jit

  @jit(nopython=True)
  def ols_lstsq_raw(row):
      X = np.arange(row.shape[0])
      ones = np.ones(row.shape[0])
      A = np.vstack((X, ones)).T
      m, c = np.linalg.lstsq(A, row, rcond=-1)[0]
      return m

  # Combine compiled code with raw=True
  results = df.apply(ols_lstsq_raw, axis=1, raw=True)
  ```