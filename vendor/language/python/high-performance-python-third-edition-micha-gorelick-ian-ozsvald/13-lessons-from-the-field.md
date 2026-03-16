@Domain
High performance Python programming, data science pipelines, machine learning engineering, large-scale web scraping, and quantitative finance system development. These rules trigger when building, refactoring, or optimizing data-intensive Python applications, machine learning models, or web scrapers.

@Vocabulary
- **Hypothesis-Driven Research**: Formulating a list of hypotheses for technical hurdles and devising specific experiments to test each one sequentially.
- **Defensive Programming**: A coding style focused on anticipating errors using assertions, exception handling, logging, and type hints.
- **TDD (Test-Driven Development)**: Writing unit, integration, and acceptance tests to cover both "happy" (expected inputs) and "sad" (unexpected inputs) paths.
- **MLOps**: Machine Learning Operations; leveraging cloud platforms (e.g., Azure ML, MLflow) to automate model deployment, monitoring, versioning, and retraining to manage technical debt.
- **Look-Ahead Bias**: An error in time-series analysis/backtesting where future data is accidentally included in historical computations.
- **Aho-Corasick**: A string-matching algorithm/trie structure used for high-performance, simultaneous matching of thousands of regex patterns or keywords.
- **Loop Fusion**: An optimization technique in Numba that combines multiple loops over arithmetic array operations into a single loop to reduce memory lookups.
- **nopython mode (`@njit`)**: A Numba compilation mode that infers all types and completely bypasses the Python C-API for maximum performance.
- **MVP (Minimum Viable Product)**: A lean, early version of a solution (e.g., simple scripts or SQL queries) used to validate assumptions before building production-ready systems.
- **Streaming (Generators)**: Processing input data one point or chunk at a time to maintain a small, constant memory footprint, rather than loading everything into RAM.

@Objectives
- Ensure the right problem is being solved; always prioritize simpler, exact technologies (e.g., SQL) over complex implementations (e.g., Machine Learning) if they achieve the business goal.
- Maintain code flexibility to allow for radical algorithmic refactoring (which yields 10x-100x speedups) rather than focusing exclusively on premature line-by-line micro-optimizations.
- Build robust, defensive data pipelines using explicit type hints, runtime assertions, graceful exception handling, and dataframe validation (e.g., Pandera).
- Ensure reproducibility and stability by writing unit tests during the research and prototyping phases, not just at the end of the project.
- Leverage the most scalable and appropriate tools for specific bottlenecks (e.g., `aiohttp` over browser automation for scraping; Numba over Pandas vectorization for path-dependent time-series; Tries/Aho-Corasick for multi-string matching).

@Guidelines
- **Problem Definition & Flexibility**: 
  - The AI MUST evaluate if a problem can be solved by redefining it or using simpler tools (e.g., a SQL database query instead of a predictive ML model).
  - The AI MUST minimize code coupling and avoid premature optimization (like over-vectorization that hurts readability) to maintain the ability to quickly refactor.
  - For complex conditional logic on floating-point vectors/tensors, the AI MUST consider using arithmetic equivalents (e.g., logical-AND as element-wise multiplication, logical-OR as `max(a, b)`, NOT as `1-x`) for performance.
- **Defensive Data Programming**: 
  - The AI MUST insert `assert` statements to codify assumptions and check the state of the data/environment at runtime.
  - The AI MUST use `try-except` blocks with meaningful error messages, and `raise` statements to conditionally halt execution on bad data.
  - The AI MUST add standard Python type hints to specify expected types for variables and arguments.
  - The AI MUST use the `pandera` library to define schemas and validate Pandas/Polars dataframes at runtime.
- **Testing & Reproducibility**: 
  - The AI MUST write unit, integration, and acceptance tests during the research/development phase to minimize deployment refactoring.
  - The AI MUST test both the "happy path" and the "sad path".
- **Data Pipeline Architecture & Memory Management**: 
  - The AI MUST use Python generators to stream data (processing one point or a small batch at a time) to keep the memory footprint constant.
  - The AI MUST keep high-level bookkeeping and application logic in clean Python, restricting low-level optimizations (C/Cython/Numba) only to identified bottlenecks.
  - The AI MUST sprinkle manual sanity checks and `logging` statements throughout data pipelines to catch hidden data impurities (e.g., unexpected tokenization, wrong encodings) early.
- **Machine Learning & Feature Engineering**: 
  - The AI MUST package feature engineering transformations into reusable, testable classes using the scikit-learn `fit`/`transform` API.
  - The AI MUST NOT use hardcoded configuration files for parameters that should be learned directly from the data.
  - The AI MUST select or design evaluation metrics that perfectly match the real-world use case (e.g., exact coordinate matching for text extraction, not generalized bounding box overlap).
  - The AI MUST leverage MLOps tools (e.g., MLflow) to track experiments, package code, and manage model registries.
- **Fast Approximate Solutions**: 
  - When searching for intersections or matches at scale, the AI MUST implement a fast, approximate solution with a false-positive bias (e.g., bounding boxes, K-D Trees, precomputed spatial indices) to filter data before applying a slower, exact evaluation.
- **Time-Series & Quant Finance**: 
  - To prevent memory bloat and look-ahead bias in path-dependent time-series data, the AI MUST prefer localized performance boosts using Numba over naive "whole history" Pandas vectorization.
  - The AI MUST containerize and horizontally scale backtesting workflows (e.g., via Kubernetes) rather than running them sequentially.
- **String Matching & NLP**: 
  - When matching hundreds of incoming strings against thousands of regex patterns, the AI MUST use a Trie structure or the Aho-Corasick algorithm as a pre-filter instead of evaluating all regexes sequentially.
- **Large-Scale Web Scraping**: 
  - The AI MUST prefer undocumented APIs using `requests.Session` or `aiohttp.ClientSession` (to persist headers/cookies) over heavy browser automation (Selenium/Playwright) for scale.
  - The AI MUST handle rate limiting and IP blocking gracefully, utilizing asynchronous batching and (when necessary/responsible) residential IP rotators.
- **Numba Best Practices**: 
  - The AI MUST use the `@njit` (nopython=True) decorator whenever possible.
  - The AI MUST use Numba's typed containers (`numba.typed.List`, `numba.typed.Dict`) instead of standard Python lists/dicts inside compiled functions.
  - The AI MUST rely on Numba's loop fusion capabilities for array math; it MUST NOT manually rewrite NumPy array expressions into `for` loops just to satisfy the compiler.
- **Human-in-the-Loop & Tooling**: 
  - The AI MUST utilize lightweight frameworks like `Streamlit` or `Dash` to quickly build interactive data applications for subject matter experts, rather than building full web stacks (Flask/JS/CSS).

@Workflow
1. **Discovery & Scoping**: Start by outputting pseudocode, defining test harnesses, model evaluation metrics, and data integration interfaces. Ask "What is the definition of done?" and "Can we solve this without ML?"
2. **Data Inspection & Defensive Setup**: Implement data loading using generators. Add `pandera` schemas, `assert` statements, type hints, and `logging` to visualize data samples early in the pipeline.
3. **Prototyping (MVP)**: Build a flexible, simple Minimum Viable Product. Wrap feature engineering steps in scikit-learn `fit`/`transform` classes. Write unit tests for these steps immediately.
4. **Profiling & Bottleneck Identification**: Analyze the MVP to find the true bottleneck. 
5. **Targeted Optimization**: 
   - If I/O bound (e.g., scraping): Refactor to `aiohttp.ClientSession`.
   - If CPU/Time-Series bound: Extract the specific hotspot into a function and apply Numba `@njit`.
   - If String Matching bound: Implement an Aho-Corasick trie pre-filter.
   - If Geometry/Search bound: Implement a K-D tree or bounding-box approximate search first.
6. **Deployment & Tracking**: Wrap the final solution using MLOps tracking (e.g., MLflow) and provide a lightweight UI (Streamlit) for end-user interaction.

@Examples (Do's and Don'ts)

**Defensive Data Validation**
- [DO] Use `pandera` to validate dataframes dynamically.
```python
import pandera as pa
from pandera.typing import DataFrame, Series

class Schema(pa.SchemaModel):
    income: Series[float] = pa.Field(ge=0)
    category: Series[str] = pa.Field(isin=["A", "B", "C"])

@pa.check_types
def process_data(df: DataFrame[Schema]) -> DataFrame[Schema]:
    return df
```
- [DON'T] Pass dataframes through pipelines without runtime assertions or schema checks, which leads to silent failures and compounded technical debt.

**Large-Scale Web Scraping**
- [DO] Use asynchronous sessions to hit backend APIs for scale.
```python
import aiohttp
import asyncio

async def fetch_data(url: str, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        return await response.json()

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(url, session) for url in urls]
        return await asyncio.gather(*tasks)
```
- [DON'T] Use Selenium or Puppeteer to load full web pages if undocumented backend APIs are available and scalable.

**Time-Series Optimization (Numba)**
- [DO] Use Numba `@njit` to efficiently loop through time-series data without memory overhead.
```python
from numba import njit
import numpy as np

@njit
def compute_path_dependent_risk(positions, risk_matrix):
    T, N = positions.shape
    result = np.empty(T, dtype=np.float64)
    for t in range(T):
        # Efficient as-of slice lookups without allocating massive T x N x N arrays
        pos = positions[t]
        risk = risk_matrix[t]
        result[t] = pos.dot(risk).dot(pos)
    return result
```
- [DON'T] Naively vectorize time-series operations in Pandas using `shift()` or large 3D broadcasts that cause memory exhaustion and risk look-ahead bias.

**Numba Array Operations**
- [DO] Keep NumPy array expressions as they are; Numba will optimize them via loop fusion.
```python
from numba import njit

@njit
def array_math(a, b):
    return a * b - 4.1 * a > 2.5 * b
```
- [DON'T] Manually unroll array math into `for` loops inside Numba assuming it will be faster; it negates readability and Numba's automatic loop fusion.

**Feature Engineering Pipelines**
- [DO] Wrap feature engineering logic in scikit-learn compatible classes to ensure parameters learned during `fit` are correctly applied during `transform`.
```python
from sklearn.base import BaseEstimator, TransformerMixin

class CustomImputer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.fill_value_ = X.mean()
        return self
        
    def transform(self, X):
        return X.fillna(self.fill_value_)
```
- [DON'T] Hardcode parameters (like means or specific categories) into config files or standalone scripts that break reproducibility between research and production.