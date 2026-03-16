@Domain
Trigger these rules when the user requests assistance with performance optimization, numerical computation, matrix/vector operations, CPU/GPU profiling, deep learning pipeline optimization, or when working with `numpy`, `numexpr`, or `torch` (PyTorch) in Python.

@Vocabulary
- **Vectorization**: The process of having the CPU perform multiple mathematical operations simultaneously on contiguous chunks of data (SIMD), bypassing explicit loops.
- **Memory Fragmentation**: A state where data (e.g., objects in a standard Python list) is scattered across RAM via pointers, preventing the CPU from fetching contiguous data blocks into its cache and breaking vectorization.
- **Cache-Miss**: Occurs when the CPU requires data that is not in the L1/L2/L3 cache and must halt execution to fetch it from main memory (RAM).
- **Minor Page Fault**: A delay triggered when a program first accesses newly allocated memory, forcing the kernel to pause execution and map the memory space.
- **In-Place Operation**: A mathematical operation that modifies an existing array in memory (e.g., `A += B`) rather than allocating a new memory block to store the result.
- **NumExpr**: A Python library that compiles complex vector expressions into optimized machine code that minimizes intermediate array allocations and maximizes cache utilization.
- **Dynamic Computational Graph**: A graph generated on-the-fly during execution (used by PyTorch), allowing for flexible code flow but requiring explicit optimization steps (like JIT) for peak performance.
- **CUDA_LAUNCH_BLOCKING**: An environment variable that forces GPU operations to execute synchronously, essential for accurate GPU time profiling.
- **Automatic Mixed-Precision (AMP)**: A technique that automatically downcasts certain GPU operations to lower precision (e.g., `float16`) to increase throughput and reduce memory usage without significantly sacrificing accuracy.
- **Pinned Memory (Page-Locked Memory)**: A specific region of system RAM that can be transferred to the GPU via Direct Memory Access (DMA) much faster and asynchronously, bypassing standard OS paging mechanisms.

@Objectives
- Eliminate repetitive memory allocations and OS kernel calls within tight computational loops.
- Structure data contiguously in memory to maximize CPU cache hits and enable hardware-level vectorization.
- Leverage optimized, specialized implementations over generalized library functions when branching and edge-case logic cause bottlenecks.
- Maximize GPU utilization by keeping data on the GPU, avoiding synchronous CPU-GPU transfers, and utilizing low-precision/tensor cores where mathematically appropriate.

@Guidelines

### CPU and Memory Optimization
- The AI MUST hoist invariant computations, memory allocations, and grid/matrix initializations outside of processing loops.
- The AI MUST use `numpy` arrays instead of Python lists or the `array` module for numerical data to guarantee contiguous memory layout and enable C-level vectorization.
- For arrays larger than the CPU cache (e.g., > 1000x1000 `float64`), the AI MUST use in-place operations (`+=`, `*=`, `np.copyto()`) broken into separate lines to avoid allocating large intermediate, out-of-place arrays.
- The AI MUST evaluate the use of the `numexpr` library for complex chained vector expressions (e.g., `A = A * B + C`).
- The AI MUST NOT use `numexpr` for small arrays that fit entirely within the CPU cache, as the compilation and threading overhead will result in a net slowdown.

### GPU and PyTorch Optimization
- The AI MUST NOT execute explicit loop-based iterations for calculations that can be vectorized using matrix/tensor operations.
- The AI MUST minimize data transfers between the CPU and GPU. Debugging statements like `.item()`, `.tolist()`, `.cpu()`, or `.numpy()` MUST NOT be placed inside high-frequency processing loops.
- The AI MUST use `Tensor.pin_memory()` or set `pin_memory=True` in DataLoaders when transferring large datasets from the CPU to the GPU.
- When performing spatial neighborhood calculations (e.g., Laplacians or matrix shifts), the AI MUST use optimized convolution operations (e.g., `torch.nn.Conv2d`) instead of explicit slice-and-shift/roll operations.
- The AI SHOULD utilize Automatic Mixed-Precision (`torch.amp.autocast`) to dynamically downcast operations to `float16` or `bfloat16`, increasing throughput on compatible GPU tensor cores.
- For production inference, the AI MUST consider Model Quantization (e.g., `int8`) or the PyTorch JIT compiler (`torch.jit.script` or `torch.jit.trace`) to optimize and freeze the dynamic computational graph.

### Profiling and Algorithmic Tuning
- The AI MUST NOT assume handwritten C/C++ code or built-in library functions (e.g., `scipy.ndimage.filters.laplace` or `np.roll`) are automatically optimal; generalized functions often contain excessive branching. The AI MUST recommend custom specialized functions if profiling indicates branching or allocation bottlenecks.
- To profile CPU instruction efficiency, cache misses, and page faults on Linux, the AI MUST recommend the `perf` tool: `perf stat -e cycles,instructions,cache-references,cache-misses,branches,branch-misses,task-clock,faults,minor-faults,cs,migrations python script.py`.
- To profile GPU code, the AI MUST recommend prefixing the execution with `CUDA_LAUNCH_BLOCKING=1` and utilizing `torch.utils.bottleneck` or `torch.profile` to identify bottlenecks.

@Workflow
1. **Profile First**: Instrument the code using `line_profiler` (for Python time/line), `perf stat` (for CPU/Cache metrics), or `torch.utils.bottleneck` (for GPU) to find the exact bottleneck. Generate a hypothesis before optimizing.
2. **Pre-Allocate Memory**: Move all array and matrix initializations (`np.zeros`, `np.empty`) outside of the operational loops. Pass these pre-allocated output arrays into functions using `out=` parameters.
3. **Convert to In-Place Arithmetic**: Rewrite vectorized mathematical expressions into sequential in-place steps (`*=`, `+=`) to eliminate intermediate minor page faults.
4. **Evaluate `numexpr`**: If the matrices exceed CPU cache limits, rewrite the sequential in-place steps into a single string expression executed by `numexpr.evaluate(expr, out=pre_allocated_array)`.
5. **Migrate to GPU (If Applicable)**: If the logic is highly parallel, branch-free, and exceeds CPU constraints, port the arrays to PyTorch tensors and send them to the device (`.to('cuda')`).
6. **Refine GPU Execution**: Replace manual matrix rolling with PyTorch convolutions. Apply `torch.amp.autocast` for mixed precision, and test `torch.jit.trace` for static graph compilation.
7. **Verify**: Run the identical profiling step from Step 1 to objectively prove the optimization reduced instructions, cache misses, or total runtime.

@Examples

### Pre-Allocating and In-Place Operations (NumPy)

[DO]
```python
import numpy as np

def evolve_optimized(grid, dt, out, D=1):
    # Perform math sequentially in-place to avoid intermediate array allocations
    np.copyto(out, grid)
    out *= -4
    out += np.roll(grid, 1, axis=0)
    out += np.roll(grid, -1, axis=0)
    out *= D * dt
    out += grid

# Pre-allocate outside the loop
grid = np.random.random((2048, 2048))
next_grid = np.zeros((2048, 2048))

for _ in range(1000):
    evolve_optimized(grid, 0.1, next_grid)
    grid, next_grid = next_grid, grid # Swap references, do not copy
```

[DON'T]
```python
import numpy as np

def evolve_slow(grid, dt, D=1):
    # This creates multiple hidden intermediate arrays, triggering page faults and cache misses
    laplacian = (np.roll(grid, 1, 0) + np.roll(grid, -1, 0) - 2 * grid)
    return grid + D * dt * laplacian

grid = np.random.random((2048, 2048))

for _ in range(1000):
    # Allocates a brand new array on every single iteration
    grid = evolve_slow(grid, 0.1)
```

### Complex Vector Expressions (NumExpr)

[DO]
```python
import numpy as np
import numexpr as ne

a = np.random.rand(4096, 4096)
b = np.random.rand(4096, 4096)
c = np.random.rand(4096, 4096)
out = np.empty((4096, 4096))

# Compiles to optimized machine code, handles chunking for CPU cache automatically
ne.evaluate("a * b - 4.1 * a > 2.5 * c", out=out)
```

[DON'T]
```python
import numpy as np

a = np.random.rand(4096, 4096)
b = np.random.rand(4096, 4096)
c = np.random.rand(4096, 4096)

# Creates 4 massive temporary arrays in memory before yielding the final result
out = a * b - 4.1 * a > 2.5 * c
```

### GPU Data Transfer

[DO]
```python
import torch

device = torch.device('cuda')
# Send to GPU once
data = torch.rand(10000, 10000, device=device)
multiplier = torch.tensor([2.0], device=device)

# Perform loops entirely on device
for _ in range(1000):
    data *= multiplier

# Bring to CPU only when strictly necessary
final_result = data.cpu().numpy()
```

[DON'T]
```python
import torch

device = torch.device('cuda')
data = torch.rand(10000, 10000, device=device)

for _ in range(1000):
    data *= 2.0
    # Forcing GPU synchronization and data transfer over the PCIe bus on every loop
    if data[0,0].item() > 1000: 
        print("Threshold reached")
```