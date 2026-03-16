# @Domain

These rules MUST trigger when the AI is tasked with designing a new software system, architecting a feature, evaluating or refactoring project structure, establishing technical stacks, or making decisions about component relationships, dependencies, and high-level code organization.

# @Vocabulary

- **Software Architecture**: The high-level design of the system, including the choice of architectural patterns and protection of System Quality Attributes (SQAs).
- **Software Design**: The low-level implementation details (classes, functions, clean code) that must support the high-level architecture.
- **The Stack / Roadmap**: The hierarchical layers of software design, building from Clean Code at the bottom to Enterprise Patterns at the top.
- **System Quality Attributes (SQAs)**: The critical metrics and non-functional requirements (e.g., flexibility, scalability) that an architecture must protect.
- **Clean Code**: Code demonstrating developer empathy, consistency, proper formatting, and adherence to team conventions.
- **Programming Paradigms**: The fundamental style of coding. Includes Object-Oriented Programming (OOP), Functional Programming (FP), and Structured Programming.
- **Domain-Modeling**: The practice of encapsulating real-world business concepts and rules into a zero-dependency software implementation.
- **Design Principles**: Guardrails for object-oriented programming (e.g., SOLID, DRY, YAGNI, Composition over Inheritance, Hollywood Principle).
- **Design Patterns**: Generic, class-level solutions to commonly occurring problems (Creational, Structural, Behavioral).
- **Architectural Principles**: Rules governing the relationships, boundaries, and dependency flow between higher-level components.
- **Architectural Styles**: High-level structural categories of architecture designed to protect specific SQAs (Structural, Message-based, Distributed).
- **Architectural Patterns**: Tactical, specific implementations of Architectural Styles (e.g., Domain-Driven Design, MVC, Event Sourcing).
- **Enterprise Patterns**: The specific, intimate technical constructs required to implement a chosen Architectural Pattern (e.g., Entities, Value Objects, Domain Events).

# @Objectives

- Ensure a symbiotic relationship between high-level architecture and low-level software design; low-level details MUST never violate high-level policy.
- Satisfy user needs while minimizing the effort required to change and maintain the system over time.
- Avoid the "Golden Hammer" anti-pattern by utilizing a hybrid of programming paradigms tailored to their specific strengths.
- Defend the system against accidental complexity by ruthlessly applying YAGNI (You Aren't Gonna Need It) to design patterns and abstractions.
- Build architectures that encapsulate business complexity away from infrastructure and delivery mechanisms.

# @Guidelines

### Step 1: Clean Code & Empathy
- The AI MUST optimize code for human readability (empathy for future maintainers).
- The AI MUST enforce coding conventions consistently: meaningful variable/method/class names, proper indentation, obvious spacing, and strict adherence to formatting rules.
- The AI MUST prefer pure functions with no side effects and avoid passing `null`.

### Step 2: Programming Paradigms (Hybrid Approach)
- The AI MUST NOT strictly confine a project to a single programming paradigm unless explicitly requested.
- The AI MUST use **Object-Oriented Programming (OOP)** to define architectural boundaries, polymorphism, and plugin architectures.
- The AI MUST use **Functional Programming (FP)** to push data to the edges of the application and elegantly handle program flow.
- The AI MUST use **Structured Programming** to compose algorithms.

### Step 3: OOP and Domain-Modeling
- The AI MUST encapsulate the core business rules within a zero-dependency domain model.
- The AI MUST use OOP mechanics (encapsulation, abstraction) to create a software implementation that maps directly to the real-world problem domain.

### Step 4: Design Principles
- The AI MUST favor **Composition over Inheritance**.
- The AI MUST encapsulate what varies.
- The AI MUST program against abstractions (interfaces/types), NOT concretions (implementations).
- The AI MUST adhere to the **Hollywood Principle**: "Don't call us, we'll call you" (Inversion of Control).
- The AI MUST strictly apply SOLID principles, prioritizing the Single Responsibility Principle.

### Step 5: Design Patterns
- The AI MUST apply class-level Design Patterns ONLY when absolutely necessary to solve a specific, recognizable problem.
- **Creational Patterns**: Use Singleton, Abstract Factory, or Prototype to control object creation.
- **Structural Patterns**: Use Adapter, Bridge, or Decorator to simplify relationships between components.
- **Behavioral Patterns**: Use Template, Mediator, or Observer to facilitate elegant communication between objects.
- **Anti-Pattern Warning**: The AI MUST NOT introduce design patterns preemptively. Design patterns introduce complexity and must be justified by the requirements.

### Step 6: Architectural Principles
- The AI MUST explicitly define architectural boundaries to separate concerns and improve modularity based on use cases.
- The AI MUST separate high-level Policy (business rules) from low-level Details (infrastructure, UI, DB).
- The AI MUST enforce component design principles: Stable Abstractions, Stable Dependencies, and Acyclic Dependencies (no circular imports/dependencies).

### Step 7: Architectural Styles
- The AI MUST identify the primary SQAs of the project to determine the Architectural Style.
- **Structural Styles** (for flexibility/separation of concerns): Component-based, Layered, or Monolithic.
- **Message-based Styles** (for real-time/high-throughput): Event-Driven or Publish-Subscribe.
- **Distributed Styles** (for scaling/delegation): Client-server or Peer-to-peer.

### Step 8 & 9: Architectural and Enterprise Patterns
- The AI MUST select a tactical pattern that fulfills the style:
  - Complex business logic -> **Domain-Driven Design (DDD)** (Structural/Layered). Requires: Entities, Value Objects, Domain Events.
  - UI-based interaction -> **Model-View-Controller (MVC)** (Distributed).
  - High auditability/event history -> **Event Sourcing** (Message-based/Event-Driven). Requires: Retroactive Events, Eventual Consistency.

# @Workflow

When instructed to design or structure a software system, the AI MUST follow this top-down analytical, bottom-up implementation workflow:

1. **Identify System Quality Attributes (SQAs):** Determine what metrics (flexibility, throughput, scale, complexity) dictate the project's success.
2. **Select Architectural Style (Step 7):** Choose Structural, Message-based, or Distributed based on the SQAs.
3. **Select Architectural Pattern (Step 8):** Pick the tactical implementation (DDD, MVC, Event Sourcing, etc.) that fits the Style.
4. **Identify Enterprise Patterns (Step 9):** Establish the domain-specific jargon and constructs (Entities, Domain Events) required for the pattern.
5. **Establish Architectural Principles (Step 6):** Define the dependency flow. Ensure high-level policy is isolated from low-level details.
6. **Apply Design Patterns (Step 5):** Identify if any generic class-level problems require Creational, Structural, or Behavioral patterns. Do not over-engineer.
7. **Apply Design Principles (Step 4):** Structure the relationships using Interfaces, Composition over Inheritance, and SOLID.
8. **Model the Domain (Step 3):** Draft the core business logic using OOP, ensuring zero dependencies on external frameworks.
9. **Implement Paradigms (Step 2):** Write the code using OOP for boundaries, FP for data flow, and Structured programming for algorithms.
10. **Refine Clean Code (Step 1):** Review the output for human readability, empathy, meaningful naming, and structural consistency.

# @Examples (Do's and Don'ts)

### 1. Hybrid Programming Paradigms
- **[DO]** Use OOP for boundaries and FP for data manipulation:
  ```typescript
  // OOP for Boundary/Plugin Architecture
  interface PaymentStrategy {
    process(amount: number): boolean;
  }

  class StripeAdapter implements PaymentStrategy {
    process(amount: number): boolean { /* ... */ return true; }
  }

  // FP for Data Flow at the edges
  const calculateTotal = (items: CartItem[]): number => 
    items.filter(item => item.isActive)
         .reduce((total, item) => total + item.price, 0);
  ```
- **[DON'T]** Force a single paradigm inappropriately (e.g., using heavy OOP state mutation for a simple data transformation pipeline).

### 2. Dependency Inversion & Programming to Abstractions
- **[DO]** Depend on an abstraction (Interface) to protect high-level policy from low-level details:
  ```typescript
  // High-level policy depends on abstraction
  interface UserRepository {
    save(user: User): void;
  }

  class RegisterUserService {
    constructor(private repo: UserRepository) {} // Depends on interface
    execute(user: User) {
      this.repo.save(user);
    }
  }
  ```
- **[DON'T]** Depend directly on concretions (infrastructure details):
  ```typescript
  import { PostgresDatabase } from './infrastructure/db';

  class RegisterUserService {
    private db = new PostgresDatabase(); // Tightly coupled low-level detail
    execute(user: User) {
      this.db.insert('users', user);
    }
  }
  ```

### 3. Composition Over Inheritance
- **[DO]** Compose behaviors using interfaces and injected dependencies:
  ```typescript
  class Logger { log(msg: string) { /*...*/ } }
  class EmailSender { send(email: string) { /*...*/ } }

  class NotificationService {
    constructor(private logger: Logger, private emailer: EmailSender) {}
    notify(user: string) {
      this.emailer.send(user);
      this.logger.log(`Notified ${user}`);
    }
  }
  ```
- **[DON'T]** Create deep, rigid inheritance chains:
  ```typescript
  class BaseService { /*...*/ }
  class LoggingService extends BaseService { /*...*/ }
  class EmailLoggingService extends LoggingService { /*...*/ } // Brittle and inflexible
  ```

### 4. Zero-Dependency Domain Model
- **[DO]** Ensure domain objects rely only on language primitives or other domain objects:
  ```typescript
  class User {
    constructor(private id: string, private status: string) {}
    activate(): void {
      if (this.status === 'BANNED') throw new Error("Cannot activate");
      this.status = 'ACTIVE';
    }
  }
  ```
- **[DON'T]** Import ORMs, frameworks, or external libraries into the domain model:
  ```typescript
  import { Entity, Column } from 'typeorm'; // VIOLATION: Framework in Domain

  @Entity()
  class User {
    @Column()
    status: string;
  }
  ```