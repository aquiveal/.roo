@Domain
These rules are triggered when the AI is tasked with designing error handling architecture, managing exceptions, writing application use cases, defining method/function return types, or modeling failure states within a codebase (specifically in TypeScript/JavaScript or object-oriented environments).

@Vocabulary
- **Domain Concept Error**: An error that is explicitly modeled as a part of the business domain, rather than treated as a generic language-level exception.
- **UseCaseError**: A base abstract class or interface used to represent any error that can occur within a specific use case. It universally contains a `message` property.
- **Error Namespace**: A TypeScript `namespace` used to logically group all specific, predictable failure states (errors) associated with a single Use Case.
- **Result**: A wrapper class/object used to encapsulate the outcome of an operation, indicating whether it was a success or failure, and containing the associated error or value.
- **Either**: A functional programming monad (often structured as `Either<L, R>`) used to strictly segregate failure states (Left) from success states (Right).
- **GOTO-like Disruption**: The anti-pattern of using `throw` to handle expected errors, which abruptly breaks the natural flow of the program in a manner similar to legacy GOTO statements.

@Objectives
- Eliminate implicit, unpredictable error handling mechanisms across the codebase.
- Prevent the disruption of natural program flow caused by throwing exceptions for expected business rule violations.
- Ensure methods and functions adhere to the "single return type" principle.
- Elevate errors to first-class domain concepts that explicitly communicate how operations can fail.
- Force API clients and callers to explicitly handle all possible error and success states using strict, statically-analyzed type signatures.

@Guidelines
- **Avoid Throwing Exceptions**: The AI MUST NOT use `throw new Error()` for expected business logic failures or validation errors. Throwing exceptions should be strictly reserved for truly unexpected, catastrophic system failures.
- **Avoid Returning Null**: The AI MUST NOT return `null` or `undefined` to indicate a failure state. This breaks the principle that a method should return a single, predictable type and leads to trust issues in the API.
- **Model Errors as Domain Concepts**: The AI MUST explicitly define error states as objects/classes within the domain, giving them descriptive, business-relevant names (e.g., `EmailAlreadyExistsError` rather than a generic `Error`).
- **Use Base Error Classes**: The AI MUST implement a base `UseCaseError` abstract class (implementing an `IUseCaseError` interface) that guarantees an error `message` property exists on all domain errors.
- **Group Errors via Namespaces**: The AI MUST group all possible errors for a specific Use Case inside an exported `namespace` named after the Use Case (e.g., `export namespace CreateUserErrors`).
- **Use the Result Class**: Specific error classes MUST extend a `Result` class (e.g., `Result<UseCaseError>`) to standardize how success and failure are evaluated.
- **Leverage the Either Monad**: The AI MUST define Use Case return types using the `Either` type to explicitly declare all possible failure states on the Left, and the success state on the Right (e.g., `Either<SpecificErrorA | SpecificErrorB, Result<SuccessData>>`).
- **Strict Return Paths**: Use Case implementations MUST return errors using a `left()` wrapper and successes using a `right()` wrapper.

@Workflow
1. **Identify Failure States**: Before writing the implementation of a Use Case, analyze the business rules and list every possible way the operation could fail (e.g., resource not found, conflict, invalid state).
2. **Define Base Error Interface**: Ensure a base `UseCaseError` abstract class exists in the shared core of the project.
3. **Create Error Namespace**: Create a dedicated file or block for the Use Case's errors. Define an `export namespace [UseCaseName]Errors`.
4. **Implement Specific Errors**: Inside the namespace, create a specific class for each failure state identified in Step 1. Have each class extend `Result<UseCaseError>` and pass a rigidly formatted, descriptive message to the `super()` constructor.
5. **Define Use Case Response Type**: Define the Use Case's return type as an `Either` type. List every specific error class from the namespace (plus any generic AppErrors) in the Left union type, and the successful `Result<T>` in the Right type.
6. **Execute and Return**: Write the Use Case execution logic. When a failure condition is met, return `left(new [Namespace].[SpecificError](args))`. When successful, return `right(Result.ok(data))`.
7. **Handle in Controller**: In the calling code (e.g., an HTTP Controller), evaluate the `Either` result. If it is `.isLeft()`, use a `switch` statement on the `error.constructor` to map specific domain errors to their appropriate HTTP response codes (e.g., 409 Conflict, 404 Not Found).

@Examples (Do's and Don'ts)

[DON'T]
```typescript
// Anti-pattern: Returning null and throwing errors disrupts flow and obscures intent.
export class CreateUserUseCase {
  public async execute(request: CreateUserDTO): Promise<User | null> {
    const userExists = await this.userRepo.exists(request.email);
    
    // BAD: Returning null obscures the exact reason for failure
    if (!userExists) {
      return null; 
    }

    // BAD: Throwing an error breaks program flow and isn't caught by the type system
    if (request.username.length < 3) {
      throw new Error("Username taken or invalid");
    }

    const user = User.create(request);
    await this.userRepo.save(user);
    return user;
  }
}
```

[DO]
```typescript
// Best Practice: Errors are explicit domain concepts grouped in namespaces and returned via Either/Result monads.

// 1. Define the Domain Errors
export namespace CreateUserErrors {
  export class EmailAlreadyExistsError extends Result<UseCaseError> {
    constructor(email: string) {
      super(false, {
        message: `The email ${email} associated for this account already exists`
      } as UseCaseError);
    }
  }

  export class UsernameTakenError extends Result<UseCaseError> {
    constructor(username: string) {
      super(false, {
        message: `The username ${username} was already taken`
      } as UseCaseError);
    }
  }
}

// 2. Define the explicit Response Type
export type CreateUserResponse = Either<
  CreateUserErrors.EmailAlreadyExistsError |
  CreateUserErrors.UsernameTakenError |
  AppError.UnexpectedError |
  Result<any>, 
  Result<void>
>;

// 3. Implement the Use Case
export class CreateUserUseCase implements UseCase<CreateUserDTO, Promise<CreateUserResponse>> {
  constructor(private userRepo: IUserRepo) {}

  public async execute(request: CreateUserDTO): Promise<CreateUserResponse> {
    try {
      const emailExists = await this.userRepo.exists(request.email);
      
      // GOOD: Returning explicit domain error state
      if (emailExists) {
        return left(new CreateUserErrors.EmailAlreadyExistsError(request.email));
      }

      const userNameTaken = await this.userRepo.getUserByUserName(request.username);
      
      // GOOD: Returning explicit domain error state
      if (userNameTaken) {
        return left(new CreateUserErrors.UsernameTakenError(request.username));
      }

      const user = User.create(request);
      await this.userRepo.save(user);
      
      // GOOD: Returning explicit success state
      return right(Result.ok<void>());
      
    } catch (err) {
      return left(new AppError.UnexpectedError(err));
    }
  }
}
```