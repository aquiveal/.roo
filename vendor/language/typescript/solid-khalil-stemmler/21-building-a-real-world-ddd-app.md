@Domain
This rule file is activated when the AI is tasked with designing or implementing business logic, planning application architecture, refactoring legacy CRUD/MVC applications that have become complex, modeling domain entities, implementing CQRS (Command Query Responsibility Segregation), or building scalable enterprise web applications using Domain-Driven Design (DDD) principles.

@Vocabulary
- **Domain Model:** The declarative layer of code (the "solution space") that encapsulates the business rules of the problem domain, completely isolated from external dependencies or infrastructure concerns.
- **Ubiquitous Language:** The shared terminology agreed upon by domain experts and developers, strictly reflected in the naming of classes, methods, files, and variables.
- **Transaction Script:** A simplistic architectural pattern where domain logic is executed procedurally (e.g., via `if/else` statements in controllers or services); suitable only for simple CRUD applications.
- **Anemic Domain Model:** An anti-pattern where domain objects are just data structures (getters/setters) and all business logic is pushed into separate "service" classes.
- **Entity:** A domain object with a unique identity, capable of state changes over time, compared by its identifier (UUID/Primary Key) rather than its properties.
- **Value Object:** An immutable domain object defined purely by its structural attributes, possessing no identity, and compared by structural equality. Often used to encapsulate validation rules (e.g., `UserEmail`, `UserName`).
- **Aggregate (Aggregate Root):** A collection of logically related Entities and Value Objects bound together by a root Entity. It acts as a transactional consistency boundary.
- **Domain Service:** A class encapsulating domain logic that spans multiple Aggregates and does not naturally fit inside a single Entity.
- **Repository:** An Interface Adapter used to fetch and persist domain objects from/to underlying data stores, keeping infrastructure concerns out of the domain layer.
- **Factory:** A method or class responsible for enforcing the creation rules and constraints of a domain object, often returning a `Result` or `Either` type.
- **Domain Event:** A past-tense record of a meaningful business occurrence (e.g., `UserCreated`, `PostUpvoted`) used to decouple side-effects across subdomains.
- **Subdomain:** A logical slice of the problem space, categorized as Core (the money-maker), Generic (e.g., authentication), or Supporting (e.g., notifications).
- **Bounded Context:** The physical deployment boundary (the solution space) that encapsulates one or more subdomains (e.g., a Modular Monolith or a Microservice).
- **Application Service / Use Case:** An application-layer orchestrator that handles a specific Command or Query. It fetches aggregates via Repositories, invokes domain methods, and persists results. It MUST NOT contain domain logic.
- **Mapper:** An infrastructure class strictly responsible for translating objects between Domain, Persistence (e.g., ORM models), and DTO formats.
- **WatchedList:** A collection abstraction that tracks initial, newly added, and removed items within an aggregate to facilitate accurate persistence of complex relationships.
- **Conway’s Law:** The principle that system boundaries should reflect the communication structures and roles of the organization building them.
- **Event Storming:** A highly interactive design process using sticky notes to sequentially map Domain Events, Commands, Aggregates, boundaries, and views.

@Objectives
- **Elevate Architecture:** Transition the AI's mental model from simple imperative CRUD/MVC architectures to declarative, behavior-first Domain-Driven Design for handling complex business requirements.
- **Protect the Domain:** Strictly enforce the Dependency Rule by isolating the domain layer from all outer-layer concerns (frameworks, ORMs, databases, APIs).
- **Encapsulate Complexity:** Eliminate Anemic Domain Models by embedding validation, constraints, and business rules deeply inside Entities, Value Objects, and Domain Services.
- **Enforce CQRS and CQS:** Architect systems where Write models (Aggregates) are strictly separated from Read models (DTOs/Views), and methods either mutate state (Command) or return data (Query), but never both.
- **Decouple Modules:** Implement cross-boundary communication exclusively via Domain Events rather than direct method calls or source-code dependencies.
- **Domain-Level Error Handling:** Elevate errors to explicit domain concepts using Monads (`Result`, `Either`), forcing clients to handle predictable failure states.

@Guidelines

### 1. Project Planning and Use Case Design
- When planning features, the AI MUST identify actors by **Role** (e.g., `Member`, `Admin`, `Visitor`, `Trader`), avoiding the generic term "User" unless building an Identity/Access Management context.
- The AI MUST define application capabilities strictly as Use Cases, categorized as either Commands (state-mutating) or Queries (data-fetching).
- The AI MUST document business rules and scenarios using Gherkin/BDD syntax (`Given`, `When`, `Then`).
- The AI MUST apply Conway's Law to logically group Use Cases into Subdomains to establish architectural boundaries before writing code.

### 2. Domain Modeling (Entities, Value Objects, and Aggregates)
- The AI MUST NOT use primitive data types ("string-ly typed" code) for properties that carry business rules, constraints, or specific formats. It MUST create and use **Value Objects** instead.
- The AI MUST enforce object creation rules by making Aggregate/Entity constructors `private` and exposing a `static create` factory method.
- The AI MUST NOT include public setters that allow an object to enter an illegal state. All state mutations MUST happen through intention-revealing methods.
- **Aggregate Design Rules:**
  1. All write transactions MUST happen exclusively against Aggregates.
  2. Aggregates MUST be designed as small as possible, containing only what is needed to protect invariants.
  3. Outer-layer code MUST NOT alter entities inside an aggregate boundary directly; mutations MUST route through the Aggregate Root.
  4. Aggregates MUST reference other Aggregates strictly by their ID (e.g., `UserId`), never by holding a direct object reference.
- The AI MUST extract logic into a **Domain Service** if a business operation requires coordinating multiple distinct Aggregates.

### 3. Application Services (Use Cases)
- Use Cases MUST reside in the Application Layer and MUST NOT contain any domain logic, validation logic, or business rules.
- Cyclomatic complexity inside a Use Case MUST be minimal. If the AI writes nested `if/switch` blocks, it MUST recognize a "leaky domain logic" smell and refactor the logic into the Domain Layer.
- Use Cases MUST accept a simple Data Transfer Object (DTO) as input (Command/Query object) and return a predictable Monad (e.g., `Either<Error, Result>`).
- Use Cases MUST interact with persistence purely through Dependency-Injected Repository Interfaces, not concrete ORM implementations.

### 4. Cross-Boundary Communication (Domain Events)
- When an Aggregate changes state, the AI MUST instantiate a past-tense Domain Event (e.g., `UserCreated`) and queue it internally within the Aggregate (e.g., `this.addDomainEvent(...)`).
- The AI MUST NOT dispatch events immediately upon Aggregate mutation. Events MUST be dispatched via a Domain Events Subject ONLY after the infrastructure layer successfully commits the transaction (e.g., using ORM hooks like Sequelize's `afterCreate`/`afterSave`).
- When one Subdomain needs to react to an action in another Subdomain (e.g., Forum reacting to User), the AI MUST NOT directly invoke the target Use Case. It MUST create an `IHandle` Subscriber class listening for the Domain Event to trigger the target Use Case.

### 5. Error Handling
- The AI MUST NOT throw raw exceptions for expected business failures (e.g., `throw new Error('Username taken')`).
- The AI MUST define errors as explicit classes (e.g., `UsernameTakenError extends Result<UseCaseError>`) organized in a Use Case Errors namespace.
- The AI MUST use the `Either<L, R>` pattern as the return type for Use Cases, forcing controllers to explicitly handle the `Left` (Failure) and `Right` (Success) paths.

### 6. Persistence and Interface Adapters
- The AI MUST NOT pollute Domain Models with ORM decorators (e.g., `@Column`, `@Entity`).
- The AI MUST use a `Mapper` class with `toDomain`, `toPersistence`, and `toDTO` methods to translate objects across layers.
- For complex aggregates with 1-to-many relationships, the AI MUST use a `WatchedList` implementation to track new, updated, and removed items, and persist them using unmanaged database transactions (commit/rollback).
- For Read Operations (Queries), the AI MAY bypass Aggregates entirely and use Repositories to execute raw SQL or ORM queries that return Read Models (DTOs or specific Value Objects).

@Workflow

1. **Intake & Boundary Definition:**
   - Ask clarifying questions to determine if the requested feature requires a CRUD (Imperative) or DDD (Declarative) approach.
   - Map the feature's actors by Role.
   - Define the Subdomain and Bounded Context.

2. **Domain Layer Implementation (Core Business Rules):**
   - Create Value Objects for input properties, enforcing validation inside their `static create` methods.
   - Define the Entity/Aggregate Root, using private constructors and nesting properties inside an internal `props` interface.
   - Implement state-mutating methods on the Aggregate Root that enforce business rules.
   - Implement `IDomainEvent` classes for meaningful state changes and queue them inside the Aggregate.

3. **Application Layer Implementation (Orchestration):**
   - Define a DTO interface for the Use Case input.
   - Define an Errors namespace covering all possible failure states.
   - Define the Response type as an `Either<LeftErrors, RightSuccess>`.
   - Implement the Use Case class: inject repository interfaces -> validate Value Objects from DTO -> fetch existing aggregates -> invoke Aggregate methods -> save to repository -> return `Either`.

4. **Infrastructure & Persistence Layer Implementation:**
   - Define the ORM model (e.g., Sequelize/TypeORM/Prisma schema).
   - Create a `Mapper` class to translate between the ORM model and the Aggregate.
   - Implement the Repository interface, managing database transactions and using `WatchedList` for nested collections.
   - Attach lifecycle hooks to the ORM models to trigger `DomainEvents.dispatchEventsForAggregate` upon successful save.

5. **Presentation Layer Implementation (Controllers/Resolvers):**
   - Create a Controller class, injecting the Use Case.
   - Parse the incoming HTTP request/GraphQL args to the DTO.
   - `await useCase.execute(dto)`.
   - Evaluate the `Either` result. Map specific error classes to appropriate HTTP status codes (e.g., `UsernameTakenError` -> 409 Conflict).

@Examples (Do's and Don'ts)

### 1. Domain Modeling: Value Objects & Aggregates

[DON'T]: Use an Anemic Domain Model with public setters and primitive typing.
```typescript
// BAD: Anemic Model
export class User {
  public id: string;
  public email: string;
  
  constructor() {} // No constraints on creation
  
  public setEmail(email: string) {
    this.email = email; // No validation!
  }
}
```

[DO]: Use Rich Domain Models with Value Objects and private constructors.
```typescript
// GOOD: Rich Aggregate Root
interface UserProps {
  email: UserEmail;
  username: UserName;
}

export class User extends AggregateRoot<UserProps> {
  private constructor(props: UserProps, id?: UniqueEntityID) {
    super(props, id);
  }

  public get email(): UserEmail { return this.props.email; }

  public static create(props: UserProps, id?: UniqueEntityID): Result<User> {
    const isNewUser = !!id === false;
    const user = new User(props, id);
    
    if (isNewUser) {
      user.addDomainEvent(new UserCreated(user)); // Queue domain event
    }
    
    return Result.ok<User>(user);
  }
}
```

### 2. Application Layer: Use Cases

[DON'T]: Put business logic or ORM dependencies in the Use Case.
```typescript
// BAD: Transaction Script / Fat Use Case
import { models } from '../../../infra/sequelize/models';

export class CreateUserUseCase {
  public async execute(req: CreateUserDTO) {
    // Bad: Domain logic in use case
    if (!req.email.includes('@')) throw new Error("Invalid email");
    
    // Bad: Direct ORM dependency
    await models.User.create({ email: req.email }); 
  }
}
```

[DO]: Orchestrate Domain Objects and use Repository Interfaces.
```typescript
// GOOD: Application Service / Use Case
export class CreateUserUseCase implements UseCase<CreateUserDTO, Promise<CreateUserResponse>> {
  constructor(private userRepo: IUserRepo) {}

  async execute(request: CreateUserDTO): Promise<CreateUserResponse> {
    // 1. Delegate validation to Value Objects
    const emailOrError = UserEmail.create(request.email);
    if (emailOrError.isFailure) return left(Result.fail(emailOrError.error));

    // 2. Fetch via abstractions
    const exists = await this.userRepo.exists(emailOrError.getValue());
    if (exists) return left(new CreateUserErrors.EmailAlreadyExistsError());

    // 3. Delegate creation to Aggregate
    const userOrError = User.create({ email: emailOrError.getValue() });
    
    // 4. Persist
    await this.userRepo.save(userOrError.getValue());
    return right(Result.ok<void>());
  }
}
```

### 3. Error Handling

[DON'T]: Throw raw errors to control flow.
```typescript
// BAD
if (userExists) {
  throw new Error("User already exists");
}
```

[DO]: Use explicit namespaces and Monadic return types (`Either`).
```typescript
// GOOD
export namespace CreateUserErrors {
  export class EmailAlreadyExistsError extends Result<UseCaseError> {
    constructor() {
      super(false, { message: "Email already exists" } as UseCaseError);
    }
  }
}

// Controller usage
const result = await useCase.execute(dto);
if (result.isLeft()) {
  const error = result.value;
  switch (error.constructor) {
    case CreateUserErrors.EmailAlreadyExistsError:
      return res.status(409).json({ message: error.errorValue().message });
    default:
      return res.status(500).json({ message: "Unexpected error" });
  }
}
```

### 4. Cross-Boundary Communication

[DON'T]: Directly import a Use Case from another subdomain.
```typescript
// BAD: Forum subdomain directly calling Users subdomain Use Case
import { createUserUseCase } from '../../users/useCases/createUser';

export class ForumService {
  async handle() {
    await createUserUseCase.execute({...}); // Tightly coupled!
  }
}
```

[DO]: Subscribe to Domain Events triggered by ORM hooks.
```typescript
// GOOD: Event-Driven Subscription
export class AfterUserCreated implements IHandle<UserCreated> {
  constructor(private createMember: CreateMemberUseCase) {
    this.setupSubscriptions();
  }

  setupSubscriptions(): void {
    DomainEvents.register(this.onUserCreated.bind(this), UserCreated.name);
  }

  private async onUserCreated(event: UserCreated): Promise<void> {
    await this.createMember.execute({ userId: event.user.userId.id.toString() });
  }
}
```