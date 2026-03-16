# @Domain
Trigger these rules when performing object-oriented software design, structuring class relationships, wiring up dependencies, refactoring controllers, writing unit/acceptance tests, or applying architectural boundary principles (such as SOLID and Simple Design) to separate concerns and decouple modules.

# @Vocabulary
- **Component**: A modular part of an application intended to be assembled into a larger system. Good software design relies on the composition of loosely coupled components.
- **Source Code Dependency**: When a component hard-codes its reliance on another component's concrete implementation, making compilation and isolated testing impossible.
- **Dependency Injection (DI)**: A technique to improve testability by passing required dependencies into a module (typically via the constructor) rather than instantiating them internally.
- **Dependency Inversion Principle (DIP)**: A structural design technique where concrete classes depend on interfaces/abstractions rather than other concrete classes, effectively flipping the dependency graph to create architectural boundaries.
- **Inversion of Control (IoC) / The Hollywood Principle**: "Don't call us, we'll call you." Delegating behavior to be implemented by external plugins/hooks rather than executing rigid, top-down control flow.
- **Separation of Concerns (SoC)**: Dividing code into distinct sections that address specific, independent responsibilities. 
- **Single Responsibility Principle (SRP)**: A principle dictating that a class, module, or component must have only one reason to change, isolating it from ripples caused by unrelated domain shifts.
- **Simple Design**: An Extreme Programming (XP) framework for emergent design consisting of four ordered rules: 1) Runs all tests, 2) No duplication, 3) Maximizes clarity, 4) Minimizes the number of elements.
- **Mock Object**: A fake implementation of an interface (e.g., an in-memory repository) injected during testing to keep tests isolated and fast.
- **CQS (Command Query Separation)**: The principle that a method/use case should either be a command (changes state, returns no data) or a query (returns data, changes no state).

# @Objectives
- Build highly testable, substitutable, and flexible architectures by aggressively decoupling components.
- Prevent monolithic "God classes" (e.g., overloaded controllers) by strictly enforcing the Single Responsibility Principle and Separation of Concerns.
- Rely on abstractions (interfaces) rather than concrete implementations to construct boundaries between layers.
- Foster emergent, readable code by adhering strictly to the four rules of Simple Design in exact order.

# @Guidelines

## Dependency Management & Decoupling
- The AI MUST NOT instantiate concrete implementations of dependencies inside a class's constructor (e.g., `this.repo = new UserRepo()`).
- The AI MUST use Dependency Injection to pass all required dependencies through the constructor.
- The AI MUST program against interfaces, not implementations. When injecting a dependency, the type MUST be an abstraction (e.g., `IUserRepo`) rather than a concrete class.
- The AI MUST enable "Substitutability" by ensuring that any dependency can be swapped with a mock object (e.g., `MockUserRepo`) during testing to keep tests fast and isolated from infrastructure (like databases).
- The AI MUST strive for loose coupling between objects that interact.

## Controllers & Separation of Concerns
- The AI MUST NOT place business logic, data validation, database queries, or external service calls (like sending emails) directly inside API Controllers.
- The AI MUST restrict Controller responsibilities strictly to:
  1. Extracting and sanitizing data from the HTTP request.
  2. Passing execution off to a dedicated Application Service / Use Case.
  3. Handling the returned result and presenting the appropriate HTTP response code.
- The AI MUST NOT use global "God" controllers (e.g., `AppController` handling multiple domains). Controllers MUST be scoped down to a single feature or subdomain (e.g., `CreateUserController`) to satisfy the Single Responsibility Principle.

## Object-Oriented Composition
- The AI MUST favor Composition over Inheritance.
- The AI MUST aim for shallow class hierarchies when inheritance is necessary.
- The AI MUST treat Design Patterns as complexity; introduce them only when strictly necessary to solve a specific problem, not prematurely.

## Simple Design
The AI MUST apply the four elements of Simple Design in this strict order:
1. **Runs all the tests**: Write unit/acceptance tests first to define the functional requirements. The AI MUST ensure code passes these tests before refactoring.
2. **No duplication**: The AI MUST aggressively refactor to remove duplicate code by extracting it into simple abstractions once tests pass.
3. **Maximizes clarity**: The AI MUST rename variables, methods, and classes to be precise, meaningful, and intention-revealing (using the language of the domain).
4. **Minimizes the number of elements**: The AI MUST NOT over-engineer. Keep classes, methods, and abstractions to the absolute minimum required to satisfy the first three rules.

# @Workflow
When tasked with creating or refactoring a component, the AI MUST follow this exact algorithmic process:

1. **Identify Dependencies**: Analyze the class for hidden source code dependencies (e.g., usage of the `new` keyword for services/repositories).
2. **Abstract and Invert**: Define an interface (e.g., `I{DependencyName}`) that declares the required contract for the dependency. 
3. **Inject**: Refactor the target class's constructor to accept the interface. Assign the injected instance to private member variables.
4. **Isolate Testing**: Generate a Mock implementation of the interface using an in-memory data structure (e.g., an array). Write tests injecting this Mock object.
5. **Enforce SoC (If analyzing a Controller)**: 
   - Extract validation logic into Value Objects or DTOs.
   - Extract domain/business rules (DB checks, email sending) into a separate UseCase/Service class.
   - Reduce the Controller to solely mapping requests to the UseCase and formatting the HTTP response.
6. **Apply Simple Design**: Run tests -> Remove duplication -> Rename for clarity -> Delete unused elements.

# @Examples (Do's and Don'ts)

## Dependency Inversion & Injection

**[DON'T]** Hard-coding source dependencies inside the constructor.
```typescript
import { UserRepo } from '../repos';

class UserController {
  private userRepo: UserRepo;

  constructor() {
    // ANTI-PATTERN: Hard source-code dependency. Impossible to test in isolation.
    this.userRepo = new UserRepo(); 
  }

  async handleGetUsers(req, res): Promise<void> {
    const users = await this.userRepo.getUsers();
    return res.status(200).json({ users });
  }
}
```

**[DO]** Programming against interfaces and using Dependency Injection.
```typescript
import { IUserRepo } from '../repos';

class UserController {
  private userRepo: IUserRepo;

  // DEPENDENCY INJECTION: Relying on the interface, flipping the dependency graph.
  constructor(userRepo: IUserRepo) { 
    this.userRepo = userRepo;
  }

  async handleGetUsers(req, res): Promise<void> {
    const users = await this.userRepo.getUsers();
    return res.status(200).json({ users });
  }
}

// TEST IN ISOLATION (Fast & Mocked)
class MockUserRepo implements IUserRepo {
  private users: User[] = [];
  async getUsers(): Promise<User[]> {
    return this.users;
  }
}
const controller = new UserController(new MockUserRepo());
```

## Separation of Concerns (Controllers)

**[DON'T]** Overloaded God-Controller violating SRP and SoC.
```typescript
export class AppController {
  async createUser(req: Request, res: Response): Promise<void> {
    const { username, email, password } = req.body;
    
    // ANTI-PATTERN: Controller handling validation
    if (!TextUtils.isValidEmail(email)) return res.status(400).json({ error: "Bad email" });
    
    // ANTI-PATTERN: Controller handling DB logic directly
    const existing = await this.userRepo.getUserByEmail(email);
    if (existing) return res.status(409).json({ message: "Taken" });
    
    const user = await this.userRepo.create({ username, email, password });
    
    // ANTI-PATTERN: Controller handling side-effects
    await this.emailService.sendVerificationEmail(user.email);
    
    res.status(200).json({ success: true });
  }
}
```

**[DO]** Scoped Controller restricted strictly to HTTP concerns.
```typescript
export class CreateUserController extends BaseController {
  private createUserUseCase: CreateUserUseCase;

  constructor(createUserUseCase: CreateUserUseCase) {
    super();
    this.createUserUseCase = createUserUseCase;
  }

  async createUser(req: Request, res: Response): Promise<any> {
    // 1. Extract and sanitize
    const dto: CreateUserDTO = {
      username: TextUtils.sanitize(req.body.username),
      email: TextUtils.sanitize(req.body.email),
      password: req.body.password
    };

    try {
      // 2. Delegate to Application Service / Use Case
      const result = await this.createUserUseCase.execute(dto);

      // 3. Handle response routing
      if (result.isLeft()) {
        const error = result.value;
        switch (error.constructor) {
          case CreateUserErrors.UsernameTakenError:
          case CreateUserErrors.EmailAlreadyExistsError:
            return this.conflict(res, error.errorValue().message);
          default:
            return this.fail(res, error.errorValue().message);
        }
      } else {
        return this.ok(res);
      }
    } catch (err) {
      return this.fail(res, err);
    }
  }
}
```