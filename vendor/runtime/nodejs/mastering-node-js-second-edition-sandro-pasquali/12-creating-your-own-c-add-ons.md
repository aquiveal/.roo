# @Domain
These rules dictate the AI's behavior when asked to develop, debug, or optimize native C++ add-ons for Node.js. Trigger these rules when a user requests integration of C++ with Node, creates a `binding.gyp` file, uses `node-gyp`, embeds V8 C++ code, or utilizes the `nan` (Native Abstractions for Node) library. 

# @Vocabulary
- **Add-on**: A dynamically linked shared object, written in C++, that can be loaded into Node.js using the `require()` function, functioning identically to an ordinary Node.js module.
- **V8**: Google's open-source JavaScript engine. It provides the C++ API (`v8::Isolate`, `v8::Local`, `v8::Value`) used to bridge JavaScript and C++.
- **libuv**: The C library that implements the Node.js event loop and asynchronous worker threads.
- **GYP (Generate Your Projects)**: A meta-build system that uses text format configuration files to generate platform-specific build files (Makefiles, Visual Studio projects, Xcode projects).
- **node-gyp**: A CLI tool written specifically for compiling native add-on modules for Node.js, bundling GYP.
- **NAN (Native Abstractions for Node)**: A header-only library that provides a layer of abstraction over the V8 API, ensuring C++ add-ons compile smoothly across different and rapidly changing Node/V8 versions.
- **Isolate**: An independent copy of the V8 runtime, including its own heap.
- **Local / HandleScope**: Memory management constructs in V8 to track JavaScript objects allocated in C++ so the garbage collector can safely clean them up.
- **AsyncWorker**: A NAN class used to easily offload blocking, expensive operations from the Node event loop to a background C++ thread.

# @Objectives
- Abstract away the complexity of multi-user, multi-threaded I/O management by wrapping C++ efficiency within Node.js's single-threaded JavaScript interface.
- Maintain absolute cross-version compatibility by defaulting to the `nan` library for all V8 API interactions.
- Prevent the Node.js event loop from blocking by strictly delegating CPU-heavy or long-running tasks to `AsyncWorker` threads.
- Accurately map C++ return values and error handling to standard Node.js callback patterns (error-first callbacks).
- Ensure safe memory management by strictly separating background thread logic (pure C++) from event loop logic (V8/JavaScript API).

# @Guidelines

## Project Setup and Build Automation
- The AI MUST configure C++ add-ons using a `binding.gyp` file.
- The AI MUST include a `"targets"` array containing `"target_name"` (the output binary name) and `"sources"` (an array of C++ source files).
- When using NAN, the AI MUST inject the NAN header path into the `binding.gyp` file using `"include_dirs": ["<!(node -e \"require('nan')\")"]`.
- The AI MUST instruct the developer to build the module using `node-gyp configure build` or the shortcut `node-gyp rebuild`.
- The AI MUST bind the compiled binary to JavaScript by creating a wrapper module (e.g., `index.js`) that uses `require('./build/Release/<target_name>')`.

## Native V8 API Integration (Without NAN)
- The AI MUST extract the V8 isolate using `Isolate* isolate = args.GetIsolate();` when accessing arguments in standard V8.
- The AI MUST validate argument arity (length) using `args.Length()`.
- The AI MUST validate argument types using V8 type checks (e.g., `args[0]->IsNumber()`).
- The AI MUST manually throw V8 exceptions for invalid inputs using `isolate->ThrowException(Exception::TypeError(String::NewFromUtf8(isolate, "Message"))));`.
- The AI MUST set return values using `args.GetReturnValue().Set(<value>)`.
- The AI MUST export the module initialization function using the C++ macro `NODE_MODULE(target_name, InitFunction)`. The AI MUST NOT place a semicolon at the end of the `NODE_MODULE` macro line.

## Using NAN (Native Abstractions for Node)
- The AI MUST strongly prefer using the `nan` library over the raw V8 API to prevent macros tangling and cross-version compilation nightmares.
- The AI MUST use `NAN_METHOD(MethodName)` to define JavaScript-accessible C++ methods.
- Within a `NAN_METHOD`, the AI MUST utilize the implicit `info` object (the bridge object between JS and C++) to access arguments (e.g., `info[0]`) and set return values (e.g., `info.GetReturnValue().Set(value)`).
- The AI MUST use `NAN_MODULE_INIT(Initialize)` for the initialization block.
- The AI MUST use `NAN_EXPORT(target, MethodName)` to bind the C++ method to the module exports.

## Asynchronous C++ Execution
- The AI MUST NOT run expensive, blocking calculations synchronously on the main thread.
- The AI MUST use `Nan::AsyncWorker` to create asynchronous operations.
- The AI MUST implement the `Execute()` method for background processing. 
- **CRITICAL**: The AI MUST NEVER use V8/JavaScript APIs (like `Local<Value>`) inside the `Execute()` method. `Execute()` runs in a separate thread, and V8 is NOT thread-safe.
- The AI MUST implement the `HandleOKCallback()` method to process the results of `Execute()`. This method runs on the main event loop, and the AI MUST use V8/NAN APIs here to pass data back to JavaScript.
- The AI MUST follow the Node.js error-first callback pattern in `HandleOKCallback()` by passing `Null()` as the first argument, and the result as the second argument: `callback->Call(2, argv);`.
- The AI MUST initialize the async worker using `Nan::AsyncQueueWorker(new WorkerClass(callback, ...args));`.

## Performance and Architecture Trade-offs
- The AI MUST evaluate whether a C++ add-on is truly necessary. Context-switching between the JavaScript execution context and C++ V8 bridges carries a time cost.
- The AI MUST NOT use C++ add-ons for simple, fast operations where the context-switch overhead exceeds the performance gain.
- The AI MUST use C++ add-ons strictly for deep, expensive CPU operations (e.g., heavy math, complex image processing, synchronous OS-level tasks) where getting close to the metal makes logical sense.
- The AI MUST use the `volatile` C++ keyword on looping variables if constructing dummy/mock functions intended to waste CPU cycles, to prevent the V8 C++ compiler from aggressively optimizing the loop away.

# @Workflow
When tasked with creating a C++ add-on, the AI MUST follow this rigid step-by-step process:

1. **Scaffold the Environment**:
   - Create a `package.json` file.
   - Include `nan` and `node-gyp` in the dependencies/devDependencies.
   - Add `"gypfile": true` to the package.json.
   - Add build scripts: `"build": "node-gyp rebuild"`.
2. **Configure GYP**:
   - Create `binding.gyp`.
   - Define the `targets` array, `target_name`, `sources`, and `include_dirs` executing a Node evaluation to dynamically locate `nan` headers.
3. **Write the C++ Implementation**:
   - Include `<nan.h>`.
   - Define worker classes inheriting from `Nan::AsyncWorker` if the task is blocking.
   - Define methods using `NAN_METHOD`.
   - Validate arguments using NAN type checks.
   - Define the module initializer using `NAN_MODULE_INIT` and `NAN_EXPORT`.
   - Bind the module using `NODE_MODULE`.
4. **Create the JavaScript Interface**:
   - Create an `index.js` file.
   - Require the binary output from `./build/Release/target_name`.
   - Wrap or directly export the native methods to the rest of the Node application.
5. **Verify Thread Safety**:
   - Perform a final check of any `AsyncWorker::Execute()` functions to ensure absolutely zero V8 namespace calls are present in the worker thread.

# @Examples (Do's and Don'ts)

## Project Compilation Configuration
**[DO]** Include NAN dynamically in `binding.gyp`
```json
{
  "targets": [{
    "target_name": "my_addon",
    "sources": ["addon.cc"],
    "include_dirs": ["<!(node -e \"require('nan')\")"]
  }]
}
```
**[DON'T]** Hardcode absolute paths to NAN headers, as they will break across environments.

## Module Exporting
**[DO]** Use the NODE_MODULE macro without a semicolon.
```cpp
NAN_MODULE_INIT(Initialize) {
  NAN_EXPORT(target, sayHello);
}
NODE_MODULE(hello, Initialize)
```
**[DON'T]** Place a semicolon after the NODE_MODULE macro.
```cpp
NODE_MODULE(hello, Initialize); // INCORRECT: Macro does not take a semicolon.
```

## Argument Validation
**[DO]** Validate inputs before executing C++ logic.
```cpp
NAN_METHOD(Add) {
  if (info.Length() < 2) {
    return Nan::ThrowTypeError("Must send two arguments to #add");
  }
  if (!info[0]->IsNumber() || !info[1]->IsNumber()) {
    return Nan::ThrowTypeError("#add only accepts numbers");
  }
  // Proceed with logic...
}
```
**[DON'T]** Assume argument types blindly, which will cause native C++ segmentation faults and crash the entire Node process.

## Asynchronous Worker Thread Safety
**[DO]** Strictly separate C++ native types (in `Execute`) from V8 types (in `HandleOKCallback`).
```cpp
class MyWorker : public Nan::AsyncWorker {
 public:
  MyWorker(Nan::Callback *callback, int input) 
    : Nan::AsyncWorker(callback), input(input) {}

  void Execute () {
    // Pure C++ here. Runs in a background thread.
    result = input * 2; 
  }

  void HandleOKCallback () {
    // Back on the Node event loop. V8 is safe to use here.
    Nan::HandleScope scope;
    v8::Local<v8::Value> argv[] = {
      Nan::Null(),
      Nan::New<v8::Number>(result)
    };
    callback->Call(2, argv);
  }

 private:
  int input;
  int result;
};
```

**[DON'T]** Allocate or interact with V8 variables inside the background thread.
```cpp
void Execute () {
  // INCORRECT: FATAL ERROR. V8 is not thread safe!
  v8::Local<v8::Number> num = Nan::New<v8::Number>(input * 2);
}
```