# @Domain
These rules MUST be activated when the AI is performing software architecture design, system scaffolding, framework integration, dependency management, refactoring for modularity, or setting up initialization/startup sequences for applications. They apply whenever the AI is handling the macro-structure of a system, connecting disparate modules, implementing persistence or security layers, or deciding where to instantiate objects.

# @Vocabulary
- **Separation of Concerns**: The architectural practice of compartmentalizing different responsibilities into distinct modules (e.g., separating system construction from runtime logic).
- **POJO (Plain Old Java Object)**: A simple, domain-focused object completely devoid of framework dependencies, container logic, or cross-cutting infrastructural code. (Applicable conceptually to any language, e.g., POCO in C#).
- **Cross-Cutting Concerns**: System-wide behaviors that naturally span across multiple domain boundaries (e.g., persistence, transactions, security, caching, logging).
- **AOP (Aspect-Oriented Programming)**: A paradigm used to restore modularity for cross-cutting concerns by non-invasively wrapping or proxying target code.
- **Dependency Injection (DI) / Inversion of Control (IoC)**: A mechanism where an object passes the responsibility of instantiating its dependencies to an authoritative mechanism (like a `main` routine or a container) using constructor arguments or setter methods.
- **BDUF (Big Design Up Front)**: The harmful practice of attempting to plan and design all architectural infrastructure before implementing domain logic. 
- **Lazy Initialization / Evaluation**: The idiom of delaying object creation until the moment it is needed. Often an anti-pattern when it hard-codes dependencies into runtime logic.
- **Abstract Factory**: A design pattern used when the application runtime needs control over *when* an object is created, but must remain decoupled from *how* the object is constructed.
- **DSL (Domain-Specific Language)**: A specialized, readable scripting language or API that expresses code using the exact vocabulary of domain experts, minimizing the communication gap.

# @Objectives
- The AI MUST separate the startup/construction process of the system from its runtime logic.
- The AI MUST keep domain logic completely isolated from architectural infrastructure and framework dependencies.
- The AI MUST design systems that can grow incrementally, avoiding monolithic or premature architectural commitments.
- The AI MUST handle all cross-cutting concerns non-invasively, leaving domain objects pristine and unaware of persistence, security, or transaction mechanisms.
- The AI MUST defer architectural decisions to the last responsible moment to ensure choices are made with optimal, up-to-date information.

# @Guidelines

## Construction vs. Runtime Separation
- The AI MUST NOT mix object construction/wiring logic with normal runtime processing. 
- When generating code, the AI MUST ensure that the application runtime has no knowledge of the startup process. All dependency arrows MUST point away from the initialization modules (e.g., `main`) toward the application logic.
- The AI MUST NOT use the Lazy Initialization idiom if it results in hard-coding a concrete dependency into a class.

## Dependency Management
- The AI MUST apply Dependency Injection (DI) to resolve dependencies. Objects MUST NOT take responsibility for instantiating their own dependencies.
- The AI MUST inject dependencies exclusively via constructor arguments or setter methods.
- When the runtime application explicitly needs to dictate the *timing* of an object's creation, the AI MUST provide an `Abstract Factory` interface to the application, while keeping the factory's implementation on the construction/startup side of the system.

## Modularity and POJOs (Domain Isolation)
- The AI MUST implement all domain and business logic as POJOs (or the language equivalent).
- The AI MUST NOT couple domain logic to heavyweight containers, frameworks, or deployment descriptors. Domain code must never inherit from framework classes or implement framework-specific lifecycle methods unless strictly utilizing a non-invasive tool.

## Cross-Cutting Concerns and AOP
- The AI MUST NOT spread identical infrastructure code (e.g., database transactions, security checks, caching) across multiple domain objects.
- The AI MUST utilize Aspect-Oriented Programming (AOP) strategies (e.g., Proxies, Decorators, or pure AOP frameworks) to handle cross-cutting concerns non-invasively.
- The AI MUST encapsulate persistence and architectural mapping details outside of the domain objects (e.g., using configuration files or non-invasive annotations).

## Incremental Architecture and Decision Making
- The AI MUST NOT output a Big Design Up Front (BDUF). Architecture MUST be designed to be test-driven and incrementally expandable.
- The AI MUST start with a naively simple, decoupled architecture that delivers working user stories, and only add infrastructure (caching, virtualization, failover) as the scale demands.
- The AI MUST postpone architectural and dependency decisions until the last possible moment to optimize decision-making based on the most recent knowledge.
- The AI MUST NOT aggressively apply industry standards just because they are standard; it MUST only apply them when they add demonstrable, immediate value.

## Domain-Specific Languages (DSLs)
- The AI MUST write domain logic using APIs, idiomatic wrappers, or custom DSLs that read like structured prose, ensuring the code mirrors the domain expert's language.

# @Workflow
When tasked with designing, scaffolding, or refactoring a system, the AI MUST follow this rigid step-by-step algorithm:

1. **Domain Logic Isolation**: 
   - Define the core business entities and rules as pure POJOs. 
   - Ensure these classes contain zero references to databases, web frameworks, or third-party infrastructure.
2. **Abstract Dependency Declaration**:
   - Identify what the domain POJOs need to operate (e.g., data access, external services).
   - Generate simple Interfaces for these needs.
3. **Application of Inversion of Control**:
   - Equip the POJOs with constructors or setter methods to accept their dependencies.
   - Strip out any `new` keywords inside the domain logic that instantiate concrete service classes.
4. **Cross-Cutting Extraction**:
   - Identify infrastructural requirements (logging, transactions, security).
   - Implement these using Decorators, Proxies, or an AOP framework that wraps the POJOs non-invasively.
5. **Construction Module Setup**:
   - Create a dedicated startup/wiring module (e.g., a `Main` class, a DI container setup, or a Composition Root).
   - Configure this module to instantiate the concrete infrastructure, wrap the POJOs with the necessary Aspects, and inject the dependencies.
6. **Factory Insertion (If Applicable)**:
   - If the application must spawn objects dynamically at runtime, generate an Abstract Factory interface in the domain, and implement it in the construction module.

# @Examples (Do's and Don'ants)

## Separating Construction from Use

**[DON'T]** Mix construction with runtime logic via hard-coded lazy initialization.
```java
public class OrderProcessor {
    private BillingService billingService;

    public void process(Order order) {
        // Anti-pattern: Hard-coded dependency instantiation inside business logic
        if (billingService == null) {
            billingService = new StripeBillingService("api_key"); 
        }
        billingService.bill(order);
    }
}
```

**[DO]** Use Dependency Injection to separate construction from use.
```java
public class OrderProcessor {
    private final BillingService billingService;

    // Correct: Dependency is injected; construction happens elsewhere
    public OrderProcessor(BillingService billingService) {
        this.billingService = billingService;
    }

    public void process(Order order) {
        billingService.bill(order);
    }
}
```

## Using Factories for Runtime Instantiation

**[DON'T]** Let the application construct domain objects using concrete infrastructural classes.
```java
public class OrderProcessingApp {
    public void addLineItem(String productId) {
        // Anti-pattern: Application knows about concrete database/infrastructure details
        LineItem item = new DatabaseBackedLineItem(productId);
        order.add(item);
    }
}
```

**[DO]** Use an Abstract Factory so the application controls *when* to build, but the `Main` module controls *what/how* to build.
```java
// Domain Layer
public interface LineItemFactory {
    LineItem makeLineItem(String productId);
}

public class OrderProcessingApp {
    private final LineItemFactory factory;
    
    public OrderProcessingApp(LineItemFactory factory) {
        this.factory = factory;
    }

    public void addLineItem(String productId) {
        // Correct: The application dictates WHEN to create, without knowing HOW.
        LineItem item = factory.makeLineItem(productId);
        order.add(item);
    }
}

// Main/Construction Layer
public class DatabaseLineItemFactory implements LineItemFactory {
    public LineItem makeLineItem(String productId) {
        return new DatabaseBackedLineItem(productId);
    }
}
```

## Managing Cross-Cutting Concerns

**[DON'T]** Tightly couple domain logic to framework-specific lifecycles or infrastructural APIs (like EJB2 or raw database connections).
```java
public class BankAccount extends FrameworkEntityBean {
    public void deposit(Money amount) {
        // Anti-pattern: Cross-cutting concerns polluting the domain
        FrameworkTransactionManager.beginTransaction();
        try {
            this.balance = this.balance.add(amount);
            Database.save(this);
            FrameworkTransactionManager.commit();
        } catch (Exception e) {
            FrameworkTransactionManager.rollback();
        }
    }
}
```

**[DO]** Write a pure POJO and apply cross-cutting concerns non-invasively (via Decorators, AOP Proxies, or declarative annotations).
```java
// Domain Layer: Pure POJO
public class BankAccount {
    private Money balance;

    public void deposit(Money amount) {
        // Correct: Pure business logic. Zero infrastructure.
        this.balance = this.balance.add(amount);
    }
}

// Infrastructure/Construction Layer (Decorator/Proxy Example)
public class TransactionalBankAccount implements BankAccountInterface {
    private final BankAccount target;
    private final TransactionManager txManager;

    public TransactionalBankAccount(BankAccount target, TransactionManager txManager) {
        this.target = target;
        this.txManager = txManager;
    }

    public void deposit(Money amount) {
        txManager.begin();
        try {
            target.deposit(amount);
            txManager.commit();
        } catch (Exception e) {
            txManager.rollback();
            throw e;
        }
    }
}
```