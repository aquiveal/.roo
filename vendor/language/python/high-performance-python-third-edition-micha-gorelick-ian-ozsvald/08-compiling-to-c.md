**@Domain**: 
These rules trigger when the AI is tasked with optimizing CPU-bound mathematical operations, loops with heavy intermediate object creation, compiling Python to machine code, applying JIT/AOT compilers, parallelizing algorithms using OpenMP, or interfacing with native C/Fortran/Rust libraries (FFI). 

**@Vocabulary**:
- **AOT (Ahead of Time) Compiler**: A compiler that builds a static, machine-specific library prior to execution (e.g., Cython).
- **JIT (Just-In-Time) Compiler**: A compiler that compiles code at runtime upon its first execution, resulting in a "cold start" penalty but requiring less upfront developer effort (e.g., Numba, PyPy).
- **Cython**: An AOT compiler that uses a C-like superset of Python to generate C code and compile it into Python extension modules.
- **Numba**: An LLVM-based JIT compiler specialized for compiling NumPy-heavy numerical Python code.
- **PyPy**: A drop-in replacement Python interpreter with a built-in tracing JIT compiler, utilizing a mark-and-sweep garbage collector instead of reference counting.
- **FFI (Foreign Function Interface)**: Protocols and modules (`ctypes`, `cffi`, `f2py`) that allow Python to execute code written and compiled in other languages.
- **OpenMP**: A cross-platform API for shared-memory multiprocessing in C/C++/Fortran, exposed in Python compilers to execute parallel loops outside the GIL.
- **GIL (Global Interpreter Lock)**: A CPython mechanism preventing multiple threads from executing Python bytecodes simultaneously. Must be released (`nogil`) to achieve true parallelism in compiled extensions.
- **Memoryview / Buffer Protocol**: A mechanism to share contiguous blocks of memory (e.g., NumPy arrays) directly with compiled C code without Python object overhead.
- **Strength Reduction**: The practice of replacing expensive mathematical operations with cheaper but equivalent operations (e.g., replacing `abs(z) < 2` with `z.real * z.real + z.imag * z.imag < 4`).
- **Loop Fusion**: A compiler optimization (native to Numba) that combines consecutive loops over the same array into a single loop, minimizing memory lookups and intermediate temporary arrays.
- **PyO3 / Maturin**: The toolchain for writing, building, and publishing Python extensions written in Rust.

**@Objectives**:
- Drastically reduce the number of executed CPU instructions by compiling CPU-bound, looping Python code to machine code.
- Eliminate Python Virtual Machine overhead, dynamic type checking, and reference counting in performance-critical tight inner loops.
- Select the appropriate compilation technology based on the presence of NumPy, the required engineering effort, and the need for external library integration.
- Utilize native types to bypass Python's object overhead.
- Safely release the GIL to utilize multi-core architectures via OpenMP or Rust's thread-safety.

**@Guidelines**:

**1. Tool Selection Constraints**
- **Use PyPy** for pure Python, non-NumPy CPU-bound code when the goal is a drop-in execution speedup with zero code changes.
- **Use Numba** for NumPy-heavy code, local array operations, and tight loops when fast development velocity is required without writing C code. 
- **Use Cython** for maximum control, integrating external C libraries, applying OpenMP, or when both pure Python and NumPy data structures are heavily mixed.
- **Use Rust (PyO3)** when building large-scale, complex native extensions requiring absolute memory safety and thread safety. 
- **Avoid raw CPython C-API modules**: Never manually write raw CPython C extensions (e.g., `PyArg_ParseTuple`, `Py_XINCREF`) unless explicitly demanded. It is brittle, verbose, and version-dependent. Use `cffi` or Rust instead.
- **Other Compiler Options**: Consider *Pythran* for AOT compilation of pure NumPy, *Shed Skin* for pure Python without NumPy, and *PyCUDA/PyOpenCL* for GPU bindings.

**2. Cython Architecture Rules**
- **Type Annotation**: Always declare loop counters, local variables, and math primitives at the top of the function using `cdef` (e.g., `cdef unsigned int i`, `cdef double complex z`).
- **Inner Loops**: Ensure the innermost loop is completely free of Python VM calls. Verify this by interpreting `cython -a` HTML output (target pure white lines; avoid yellow/shaded lines).
- **NumPy Integration**: Do not iterate over standard NumPy arrays or Python lists in tight loops. Declare NumPy arrays as typed memoryviews (e.g., `double complex[:] zs`) and use `cimport numpy`.
- **Preallocation**: Never use Python lists to collect results in a compiled loop. Allocate an empty NumPy array (`np.empty(length, dtype=...)`) and assign values by index.
- **Bounds Checking**: Disable bounds checking and wraparound only after the algorithm is fully debugged, using `#cython: boundscheck=False` to shave off final overhead.
- **OpenMP**: To parallelize, release the GIL using `with nogil:` and loop using `for i in prange(length, schedule="guided"):`. Never access or manipulate standard Python objects inside a `nogil` block.
- **Build System**: Use a `setup.py` with `cythonize` for production modules. Use `pyximport` only for quick prototyping.

**3. Numba Architecture Rules**
- **Mode Enforcement**: Always use `@jit(nopython=True)` or `@njit`. Never rely on `forceobj=True` (object mode) for performance. 
- **Data Structures**: Never pass heterogeneous Python lists or dicts to Numba functions. Pass NumPy arrays, scalars, or use Numba's `numba.typed.List` and `numba.typed.Dict`.
- **Refactoring**: Feel free to break large functions into smaller ones. Numba's LLVM backend natively handles function inlining.
- **Loops vs. Vectors**: Do not manually vectorize or unroll loops to outsmart Numba. Standard `for` loops over NumPy arrays are aggressively optimized via Loop Fusion.
- **Escape Hatches**: If you must interact with the Python VM (e.g., to print progress), isolate it inside a `with objmode:` block.
- **Parallelism**: Use `@njit(parallel=True)` and `prange` for simple shared-memory parallelism.
- **Debugging**: Use `func.inspect_types()` to verify that Numba has correctly inferred machine types (e.g., `int64`, `Array(complex128)`).

**4. PyPy Architecture Rules**
- **Garbage Collection**: Do not rely on implicit reference counting to close file handles. Always explicitly `.close()` files or use `with open(...) as f:` context managers, as PyPy uses a deferred mark-and-sweep GC.
- **NumPy Warning**: Do not use PyPy for heavy NumPy workloads unless utilizing `HPy`, as the compatibility layer (`cpyext`) overhead negates compilation speedups.
- **Warmup**: Account for the JIT warmup phase. Do not use PyPy for very short, frequently invoked CLI scripts.

**5. FFI and Native Extension Rules**
- **cffi over ctypes**: Prefer `cffi` (`ffi.cdef`, `ffi.dlopen`, `ffi.verify`) over the built-in `ctypes` module. `cffi` parses standard C headers, preventing dangerous and brittle type-casting mistakes inherent to `ctypes`.
- **Fortran arrays**: When using `f2py` to wrap Fortran routines, ensure input NumPy arrays are instantiated with column-major ordering (`order='F'`). Mismatched memory layouts (C vs. Fortran) will cause extreme cache-miss penalties or corrupt calculations.
- **Rust Mutability**: When using PyO3 and `ndarray`, respect Rust's strict memory safety rules: you cannot have mutable (`ArrayViewMut2`) and read-only (`ArrayView2`) references to the exact same array data simultaneously.

**@Workflow**:
1. **Profile**: Analyze the Python code to ensure the bottleneck is strictly CPU-bound math or heavy looping, not I/O, string manipulation, or DB queries.
2. **Algorithm First**: Apply Strength Reduction. Simplify math (e.g., avoid square roots if comparing relative magnitudes).
3. **Select Engine**: 
   - If purely mathematical with NumPy -> Add Numba `@njit`.
   - If mixed data structures, custom C structs, or OpenMP is needed -> Convert to Cython `.pyx`.
   - If creating a robust, distributable, safe compiled library -> Use Rust (PyO3).
4. **Isolate**: Extract the tight loop into a distinct, isolated function. 
5. **Type**: Apply static types to the arguments and all variables inside the loop.
6. **Compile & Inspect**: Check compilation output (e.g., Cython HTML or Numba `inspect_types()`). Ensure the inner loop handles only primitive machine types.
7. **Parallelize**: Add `nogil` / `prange` if the loop iterations are strictly independent.
8. **Verify**: Ensure the compiled function's output exactly matches the pure Python implementation using an automated unit test.

**@Examples (Do's and Don'ts)**:

**[DO] Use Numba `nopython` mode for zero-overhead loop acceleration:**
```python
import numpy as np
from numba import njit, prange

@njit(parallel=True)
def calculate_z(maxiter, zs, cs):
    # Allocate the output array natively
    output = np.empty(len(zs), dtype=np.int32)
    
    # prange allows thread-level parallelism
    for i in prange(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        # Strength reduction: removed abs() and sqrt
        while n < maxiter and (z.real*z.real + z.imag*z.imag) < 4:
            z = z * z + c
            n += 1
        output[i] = n
    return output
```

**[DON'T] Pass standard Python lists into Numba or write them inside `@njit`:**
```python
from numba import jit

# ANTI-PATTERN: Numba cannot optimize heterogeneous Python lists.
@jit(forceobj=True) 
def calculate_bad(maxiter, zs):
    output = [] # Python object instantiation in tight loop
    for z in zs:
        output.append(z * z) # Python VM method call
    return output
```

**[DO] Use Cython memoryviews, C-types, and disable bounds checking for tight loops:**
```python
#cython: boundscheck=False
#cython: wraparound=False
import numpy as np
cimport numpy as np
from cython.parallel import prange

def calculate_z(int maxiter, double complex[:] zs, double complex[:] cs):
    cdef unsigned int i, length
    cdef double complex z, c
    cdef int[:] output = np.empty(len(zs), dtype=np.int32)
    length = len(zs)
    
    with nogil: # Explicitly release the GIL
        for i in prange(length, schedule="guided"):
            z = zs[i]
            c = cs[i]
            output[i] = 0
            while output[i] < maxiter and (z.real * z.real + z.imag * z.imag) < 4:
                z = z * z + c
                output[i] += 1
    return output
```

**[DON'T] Access Python objects or allocate Python memory inside a `nogil` block:**
```python
cdef list output = [] # Python object
with nogil:
    for i in prange(100):
        # ANTI-PATTERN: Appending to a Python list without the GIL will corrupt memory/crash
        output.append(i) 
```

**[DO] Use `cffi` to safely bind external C code via headers:**
```python
from cffi import FFI
ffi = FFI()

# Define the C header interface
ffi.cdef("void evolve(double **in, double **out, double D, double dt);")

# Load the compiled shared object
lib = ffi.dlopen("./diffusion.so")

def evolve(grid, out, dt, D=1.0):
    # Safely cast NumPy pointers
    pointer_grid = ffi.cast("double**", grid.ctypes.data)
    pointer_out = ffi.cast("double**", out.ctypes.data)
    lib.evolve(pointer_grid, pointer_out, D, dt)
```

**[DON'T] Write brittle raw CPython C-API extensions to parse arguments:**
```c
// ANTI-PATTERN: Highly verbose, prone to memory leaks, bound to specific CPython version
PyArrayObject *py_evolve(PyObject *self, PyObject *args) {
    PyArrayObject *data;
    if (!PyArg_ParseTuple(args, "O", &data)) {
        return NULL;
    }
    // Manual reference counting and contiguous checks...
}
```

**[DO] Respect memory layouts when calling Fortran via `f2py`:**
```python
import numpy as np
from diffusion import evolve # Auto-generated by f2py

# Initialize data using Fortran column-major ordering
grid = np.zeros((512, 512), dtype=np.double, order="F")
scratch = np.zeros((512, 512), dtype=np.double, order="F")

evolve(grid, scratch, 1.0, 0.1)
```

**[DON'T] Use implicit file closure when writing code intended for PyPy:**
```python
# ANTI-PATTERN: Will not immediately flush/close in PyPy
open("output.txt", "w").write("Data") 
```

**[DO] Use explicit resource management for PyPy compatibility:**
```python
with open("output.txt", "w") as f:
    f.write("Data")
```