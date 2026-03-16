@Domain
These rules MUST be triggered when the user requests architectural design, project scaffolding, structural refactoring, or the implementation of specific architectural patterns, including Clean Architecture, Domain-Driven Design (DDD), Hexagonal Architecture (Ports & Adapters), Vertical-Slice Architecture, Command Query Responsibility Segregation (CQRS), or Event Sourcing. They also apply when the AI is deciding where to place business logic, use cases, or infrastructural dependencies within a codebase.

@Vocabulary
- **Architectural Patterns**: Tactical implementations of one or more architectural styles blown-up in scale to a high-level system structure.
- **Clean Architecture**: A layered architecture that separates the concerns of a domain model from infrastructural details (databases, web servers, caches).
- **Domain Layer**: The innermost layer of Clean Architecture containing the highest-level policy, business rules, entities, and value objects. It MUST have zero external dependencies.
- **Application Layer**: The layer containing use cases and application services. It orchestrates the flow of data to and from the domain entities but contains NO domain business rules.
- **Infrastructure Layer**: The outermost layer containing external agencies, frameworks, databases, web servers, and UI components.
- **Adapter Layer**: The layer that converts data between the format most convenient for the use cases/domain and the format most convenient for the external infrastructure (e.g., mapping HTTP requests to DTOs or ORM models to Domain Entities).
- **Ports & Adapters (Hexagonal Architecture)**: An architecture similar to Clean Architecture where the core application defines "Ports" (interfaces) and the infrastructure implements "Adapters" (concrete implementations).
- **Vertical-Slice Architecture**: An architecture that organizes code by feature or use case (a vertical slice) rather than by technical horizontal layers.
- **Domain-Driven Design (DDD)**: An approach to software development against complex problem domains that encapsulates business rules within a pure domain model.
- **Event Sourcing (ES)**: A functional approach to architecture where state is NEVER stored directly. Only transactions (events) are stored.
- **CQRS (Command Query Responsibility Segregation)**: The separation of write models (commands/aggregates) from read models (queries/projections) to prevent structured data for state management from introducing accidental complexity.
- **Projections**: The mechanism in Event Sourcing used to deserialize events and rebuild the current state for read models.
- **Accidental Complexity**: Complexity introduced by the chosen implementation or architecture (e.g., messy state management) rather than the inherent difficulty of the business problem.

@Objectives
- Protect the Domain Model by strictly separating it from infrastructural and technical details.
- Eliminate accidental complexity in state management by separating write operations from read operations using CQRS.
- Ensure the Dependency Rule is strictly followed: source code dependencies MUST ONLY point inward toward the Domain Layer.
- Utilize Event Sourcing to maintain a perfect historical record of transactions when state management becomes too messy or complex.

@Guidelines

**1. Layered Constraints & The Dependency Rule**
- The AI MUST enforce the Dependency Rule: Outer layers (Infrastructure, Adapters) can import inner layers (Application, Domain), but inner layers MUST NEVER import outer layers.
- The **Domain Layer** MUST NOT contain any references to databases, ORMs, HTTP request objects, or UI frameworks.
- The **Application Layer** MUST ONLY contain orchestration logic (Use Cases). The AI MUST NOT place core business logic (validation, state mutations) inside the Application Layer; it MUST delegate this to the Domain Layer.
- The **Infrastructure Layer** MUST contain all the dirty details: SQL queries, ORM definitions, Express/React components, and API controllers.

**2. Ports & Adapters (Hexagonal Architecture) Implementation**
- The AI MUST define "Ports" as interfaces within the Application or Domain layers (e.g., `IUserRepository`).
- The AI MUST implement "Adapters" within the Infrastructure layer (e.g., `PostgresUserRepository implements IUserRepository`).
- The AI MUST inject Adapters into Use Cases via Dependency Injection. Use Cases MUST NEVER instantiate concrete infrastructure classes directly.

**3. Vertical-Slice Architecture Considerations**
- When Vertical-Slice architecture is requested, the AI MUST group all files related to a specific feature (Controller, Use Case, DTO, Errors) into a single cohesive module or folder, rather than splitting them globally by type (e.g., no global `/controllers` or `/useCases` folders).

**4. CQRS (Command Query Responsibility Segregation)**
- The AI MUST NOT use the same model for both updating state (writes) and presenting state to the UI (reads).
- The AI MUST implement a Write Model (usually a Domain Aggregate) that enforces strict business invariants.
- The AI MUST implement a Read Model (a simple DTO, View Model, or Projection) that is optimized specifically for the data required by the presentation layer.

**5. Event Sourcing**
- When Event Sourcing is mandated, the AI MUST NOT write destructive state updates (e.g., SQL `UPDATE` or `DELETE` mutating the current state row).
- The AI MUST store a sequential, immutable list of transactions (Domain Events).
- The AI MUST compute current state by applying all transactions from the beginning of time.
- The AI MUST implement "Projections" to deserialize events into optimized read models.

@Workflow
When scaffolding a new architecture or refactoring an existing system into these patterns, the AI MUST follow this exact sequence:

1.  **Identify the Architectural Style**: Determine if the task requires Clean Architecture/Hexagonal, Vertical-Slice, or Event Sourcing based on the user's prompt or project complexity.
2.  **Establish the Domain Layer**:
    *   Define the core Entities and Value Objects.
    *   Ensure NO imports from libraries, frameworks, or outer project folders exist in these files.
3.  **Establish the Application Layer (Ports & Orchestration)**:
    *   Define the Request and Response DTOs.
    *   Define the Use Case (Application Service) that orchestrates the workflow.
    *   Define the Ports (Interfaces) required by the Use Case (e.g., Repositories, external services).
4.  **Establish the CQRS Separation**:
    *   If handling a command (write), route the Use Case to manipulate the Domain Aggregate.
    *   If handling a query (read), route the Use Case to a Projection or a dedicated Read Model, bypassing complex domain invariants.
5.  **Establish the Infrastructure & Adapter Layer**:
    *   Implement the Ports defined in Step 3 using concrete technologies (e.g., ORMs, external APIs).
    *   Create the Controllers/Resolvers that receive external input and pass it to the Use Case.
6.  **Implement Event Sourcing (If Applicable)**:
    *   Instead of saving the Domain Entity directly, dispatch and append Domain Events to an Event Store.
    *   Create Projection handlers that listen to these events and update the Read Models.

@Examples (Do's and Don'ts)

**Principle: The Dependency Rule / Clean Architecture**

[DO]
```typescript
// domain/User.ts
// CORRECT: Zero external dependencies. Pure TypeScript.
export class User {
  constructor(public id: string, public email: string) {}
  
  public updateEmail(newEmail: string): void {
    // business logic
    this.email = newEmail;
  }
}

// application/UpdateUserEmailUseCase.ts
// CORRECT: Relies on Domain and Interfaces (Ports), not implementations.
import { User } from '../domain/User';
import { IUserRepository } from './ports/IUserRepository';

export class UpdateUserEmailUseCase {
  constructor(private userRepo: IUserRepository) {}
  
  async execute(userId: string, newEmail: string) {
    const user = await this.userRepo.findById(userId);
    user.updateEmail(newEmail);
    await this.userRepo.save(user);
  }
}
```

[DON'T]
```typescript
// domain/User.ts
// INCORRECT: Domain layer imports Infrastructure layer details (TypeORM).
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: string;

  @Column()
  email: string;
}
```

**Principle: CQRS & Event Sourcing**

[DO]
```typescript
// Write side (Event Sourcing)
class BankAccount {
  private balance: number = 0;

  // Rebuild state from history
  public loadFromHistory(events: BankEvent[]) {
    events.forEach(event => this.apply(event));
  }

  // Store the transaction, not the state
  public deposit(amount: number): BankEvent {
    return new MoneyDepositedEvent(amount, new Date());
  }

  private apply(event: BankEvent) {
    if (event instanceof MoneyDepositedEvent) {
      this.balance += event.amount;
    }
  }
}

// Read side (Projection)
// Optimized strictly for the UI
type AccountBalanceReadModel = {
  accountId: string;
  currentBalance: number;
  lastUpdated: Date;
}
```

[DON'T]
```typescript
// INCORRECT: Destructive updates mixing complex write invariants and read needs, causing accidental complexity.
class BankAccountService {
  async deposit(accountId: string, amount: number) {
    const account = await db.query('SELECT * FROM accounts WHERE id = ?', [accountId]);
    // State is directly overwritten; history is lost.
    account.balance += amount; 
    await db.query('UPDATE accounts SET balance = ? WHERE id = ?', [account.balance, accountId]);
    return account; // Returning the write model directly to the UI
  }
}
```