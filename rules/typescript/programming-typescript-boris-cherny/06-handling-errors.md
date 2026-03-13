# @Domain
Triggered when writing, reviewing, or refactoring TypeScript code that involves managing failure states, validating inputs, handling exceptions (such as network, filesystem, or parsing errors), or sequencing operations that might fail. 

# @Vocabulary
- **Returning Null**: The practice of returning `null` (or `undefined`) from a function to signify a generic, unrecoverable failure where the exact cause of the failure is irrelevant to the consumer.
- **Throwing Exceptions**: Using the `throw` keyword to halt execution, utilizing custom subclasses of built-in errors (like `Error` or `RangeError`) to provide metadata about the failure.
- **Returning Exceptions**: Setting a function's return type to a Union Type containing the success value and specific custom Error classes (e.g., `T | Error1 | Error2`), forcing the consumer to handle the errors exhaustively.
- **Option Type (Maybe Type)**: A custom container data type representing a computation that may or may not return a value, used for chaining operations.
- **Some<T>**: A concrete implementation of the Option interface representing a successful computation that contains a value of type `T`.
- **None**: A concrete implementation of the Option interface representing a failed computation that contains no value.
- **flatMap**: An Option method that takes a function (which itself returns an Option) and maps the encapsulated value to a new Option without nesting containers.
- **getOrElse**: An Option method that extracts the encapsulated value if it exists, or returns a provided default fallback value if the Option is `None`.

# @Objectives
- Shift runtime exceptions to compile-time errors by explicitly encoding failure states into the TypeScript type system.
- Select the precise error-handling pattern based on the specific needs of the application: simplicity, error metadata, exhaustiveness, or composability.
- Prevent silent failures and unhandled exceptions by enforcing strict type narrowing (e.g., `instanceof` checks).
- Provide robust, chainable APIs for sequential operations that might fail, avoiding "callback pyramids" or heavily nested `if/else` checks.

# @Guidelines
- **Returning Null**
  - The AI MUST use "Returning Null" ONLY for the most lightweight error handling where the consumer does not need to know *why* the operation failed.
  - The AI MUST NOT use "Returning Null" if operations need to be chained, as this requires tedious and verbose null-checking at every nested step.

- **Throwing Exceptions**
  - The AI MUST define custom error types by subclassing built-in errors (e.g., `class InvalidDateFormatError extends RangeError {}`) rather than throwing generic errors or strings.
  - When catching exceptions, the AI MUST use `instanceof` to identify specific custom errors.
  - The AI MUST ALWAYS explicitly rethrow errors that it does not recognize in a `catch` block to avoid silently swallowing unexpected exceptions.
  - The AI MUST NOT rely solely on JSDoc `@throws` annotations for safety, as the TypeScript compiler does not enforce them.

- **Returning Exceptions**
  - When the consumer MUST be forced to handle specific failure modes at compile time, the AI MUST return a Union Type of the expected value and the specific custom Error classes (e.g., `Date | InvalidDateFormatError`).
  - The AI MUST handle these returned exceptions using `instanceof` type guards to narrow the Union Type down to the success value.

- **The Option Type**
  - When performing multiple sequential operations where each step might fail, the AI MUST implement and utilize the Option pattern instead of returning nested arrays or deeply nested `try/catch` blocks.
  - The AI MUST define an `Option<T>` interface, a `Some<T>` class, and a `None` class.
  - The AI MUST implement a `flatMap` method to chain operations.
  - The AI MUST use overloaded method signatures for `flatMap` to ensure strict typing (e.g., mapping a `None` always yields a `None`, mapping a `Some` yields an `Option`).
  - The AI MUST implement a `getOrElse` method to extract the value safely by providing a default.
  - The AI MUST implement an overloaded `Option` factory function that takes `null | undefined` and returns `None`, and takes `T` and returns `Some<T>`.

# @Workflow
When tasked with implementing error handling for an operation, the AI MUST follow this exact algorithmic process:

1. **Analyze the Failure Context**:
   - Evaluate if the consumer needs to know *why* the error occurred.
   - Evaluate if the operation is part of a sequence/chain of operations.
   - Evaluate if the consumer MUST be forced by the compiler to handle the error.

2. **Select the Error Handling Pattern**:
   - *Pattern 1*: If no error metadata is needed and the operation is isolated, select **Returning Null**.
   - *Pattern 2*: If error metadata is needed, boilerplate must be minimized, and the compiler does not need to force exhaustiveness, select **Throwing Exceptions**.
   - *Pattern 3*: If error metadata is needed and the consumer MUST handle all failure states explicitly, select **Returning Exceptions**.
   - *Pattern 4*: If multiple operations that might fail need to be chained compositionally, select **The Option Type**.

3. **Implement the Selected Pattern**:
   - *For Pattern 1*: Update the return type to `T | null`. Return `null` on failure.
   - *For Pattern 2*: Create `class CustomError extends Error {}`. Use `throw new CustomError()`. Wrap consumer execution in `try / catch (e)`, check `e instanceof CustomError`, and `else { throw e }`.
   - *For Pattern 3*: Update the return type to `T | CustomError1 | CustomError2`. Return instances of errors on failure. In the consumer, use `if (result instanceof Error)` to narrow the type.
   - *For Pattern 4*: 
     - Define `interface Option<T> { flatMap... getOrElse... }`.
     - Define `class Some<T>` and `class None`.
     - Create the `Option<T>` factory function with overloads.
     - Chain the consumer operations using `.flatMap()` and terminate with `.getOrElse()`.

# @Examples (Do's and Don'ts)

### Returning Null
- **[DO]** Return `null` for simple checks and force the consumer to check truthiness.
  ```typescript
  function parse(date: string): Date | null {
    let d = new Date(date);
    if (!isValid(d)) return null;
    return d;
  }
  let parsed = parse(input);
  if (parsed) { console.log(parsed.toISOString()); }
  ```
- **[DON'T]** Use `null` when the user requires specific, actionable feedback (e.g., "Date must be YYYY-MM-DD").

### Throwing Exceptions
- **[DO]** Subclass built-in errors and explicitly rethrow unknown errors.
  ```typescript
  class InvalidDateFormatError extends RangeError {}

  try {
    let date = parseThrows(input);
  } catch (e) {
    if (e instanceof InvalidDateFormatError) {
      console.error(e.message);
    } else {
      throw e; // Explicitly rethrow unknown errors
    }
  }
  ```
- **[DON'T]** Silently swallow errors by omitting the `else { throw e }` block, or throw raw strings like `throw "Error formatting"`.

### Returning Exceptions
- **[DO]** Use union types to force exhaustive compiler checks.
  ```typescript
  class InvalidDateFormatError extends Error {}
  class DateInFutureError extends Error {}

  function parse(date: string): Date | InvalidDateFormatError | DateInFutureError {
    // ...
    if (isFuture) return new DateInFutureError('Time traveler?');
    return new Date(date);
  }

  let result = parse(input);
  if (result instanceof Error) {
    console.error(result.message);
  } else {
    console.info(result.toISOString()); // Type is narrowed to Date
  }
  ```
- **[DON'T]** Assume `@throws` in JSDoc will enforce consumer handling in TypeScript.

### The Option Type
- **[DO]** Implement a strictly typed Option structure with overloads for `flatMap`.
  ```typescript
  interface Option<T> {
    flatMap<U>(f: (value: T) => None): None;
    flatMap<U>(f: (value: T) => Option<U>): Option<U>;
    getOrElse(value: T): T;
  }

  class Some<T> implements Option<T> {
    constructor(private value: T) {}
    flatMap<U>(f: (value: T) => None): None;
    flatMap<U>(f: (value: T) => Some<U>): Some<U>;
    flatMap<U>(f: (value: T) => Option<U>): Option<U> {
      return f(this.value);
    }
    getOrElse(): T { return this.value; }
  }

  class None implements Option<never> {
    flatMap(): None { return this; }
    getOrElse<U>(value: U): U { return value; }
  }

  function Option<T>(value: null | undefined): None;
  function Option<T>(value: T): Some<T>;
  function Option<T>(value: T): Option<T> {
    if (value == null) return new None();
    return new Some(value);
  }

  // Chaining usage
  Option(input)
    .flatMap(parseToOption)
    .flatMap(date => Option(date.toISOString()))
    .getOrElse('Error parsing');
  ```
- **[DON'T]** Use arrays as a "naive" Option container (e.g., returning `[]` for failure and `[value]` for success) which requires manual array flattening (`T[][]` to `T[]`) when chaining computations.