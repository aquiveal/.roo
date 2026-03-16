@Domain
This rule file is triggered when the AI is tasked with designing software architecture, structuring high-level code, selecting programming paradigms (Object-Oriented, Functional, or Structured), categorizing organizational archetypes (state, behavior, namespaces), or refactoring code to balance performance efficiency against human readability.

@Vocabulary
- **Object-Oriented Programming (OOP):** The programming paradigm best suited for defining how to cross architectural boundaries using polymorphism and plugins.
- **Functional Programming (FP):** The programming paradigm best suited for elegantly handling program flow and pushing data to the edges of an application.
- **Structured Programming:** The programming paradigm best suited for composing algorithms.
- **Hybrid Paradigm Approach:** The methodology of using all three mainstream programming paradigms (OOP, FP, Structured) together at different times in robust software, rather than relying on a single "golden hammer."
- **Organizational Archetypes:** The three fundamental structural categories that make up the majority of software design: Behavioral objects, State objects, and Namespaces.
- **Behavioral Objects:** An organizational archetype representing system actions; implemented as Domain Events in Domain-Driven Design (DDD).
- **State Objects:** An organizational archetype representing entities and data conditions; implemented as Aggregates in DDD.
- **Namespaces:** An organizational archetype used for grouping and boundaries; implemented as Subdomains or Bounded Contexts in DDD.
- **Human-Optimized Code:** Code designed to be easily read and understood by developers.
- **Computer-Optimized Code:** Code designed to execute as efficiently as possible for machines, often at the expense of readability.

@Objectives
- Prevent the "golden hammer" anti-pattern by utilizing a hybrid approach of OOP, FP, and Structured Programming where each excels.
- Organize all architectural components strictly into three archetypes: behavioral objects, state objects, and namespaces.
- Seamlessly map foundational organizational archetypes to Domain-Driven Design (DDD) constructs.
- Always prioritize the developer experience (human readability) over raw machine efficiency when optimizing code.

@Guidelines
- **Paradigm Selection:** The AI MUST NOT apply a strictly functional or strictly object-oriented approach across an entire project. It MUST use a hybrid approach.
- **Applying OOP:** The AI MUST use Object-Oriented Programming (interfaces, polymorphism, abstract classes) specifically to define and cross architectural boundaries.
- **Applying FP:** The AI MUST use Functional Programming principles to push data to the edges of the application and to manage program flow elegantly.
- **Applying Structured Programming:** The AI MUST use Structured Programming constructs specifically for composing and executing internal algorithms.
- **Architectural Organization:** The AI MUST categorize and design all components using exactly three organizational archetypes: 
  1. Behavioral objects
  2. State objects
  3. Namespaces
- **DDD Implementation:** When the context is Domain-Driven Design, the AI MUST map the organizational archetypes precisely as follows:
  - Implement *Behavioral objects* as *Domain Events*.
  - Implement *State objects* as *Aggregates*.
  - Implement *Namespaces* as *Subdomains / Bounded Contexts*.
- **Code Optimization Priority:** The AI MUST prioritize optimizing code for humans (> computers). If making a block of code highly efficient makes it significantly less readable, the AI MUST choose the more readable, slightly less efficient approach.

@Workflow
1. **Analyze the Feature:** When designing a feature, determine the primary responsibility of the code block being written (e.g., crossing a system boundary, routing data flow, or performing a calculation).
2. **Assign the Paradigm:** 
   - Apply OOP if the code requires a plugin architecture or crosses an architectural boundary.
   - Apply FP if the code handles pure data flow or pushes data to the application's I/O edges.
   - Apply Structured Programming if the code is an isolated algorithmic calculation.
3. **Define the Archetypes:** Structure the feature into State objects (data/entities), Behavioral objects (actions/events), and Namespaces (grouping/boundaries).
4. **Translate to DDD (If applicable):** Convert the established State objects to Aggregates, Behavioral objects to Domain Events, and Namespaces to Subdomains/Bounded Contexts.
5. **Optimize and Refactor:** Review the generated code. Ask: "Is this optimized for the computer at the expense of the human?" If yes, refactor the code to maximize human readability and understandability, accepting minor performance trade-offs.

@Examples (Do's and Don'ts)

**Example 1: Selecting Programming Paradigms**
- [DO] Use OOP interfaces to define boundaries, while using FP pure functions for data transformations:
  ```typescript
  // OOP for architectural boundary
  export interface IPaymentGateway {
    process(amount: number): Promise<boolean>;
  }

  // FP for data manipulation
  export const calculateTotalWithTax = (items: Item[], taxRate: number): number => 
    items.reduce((sum, item) => sum + item.price, 0) * (1 + taxRate);
  ```
- [DON'T] Force a single paradigm for everything (e.g., using complex OOP classes just to perform a simple math algorithm, or using FP to attempt to define complex plugin boundaries without interfaces).

**Example 2: Organizational Archetypes in DDD**
- [DO] Clearly map the three archetypes into their respective DDD constructs:
  ```typescript
  // Namespace (Subdomain/Bounded Context)
  namespace BillingSubdomain {
    
    // State Object (Aggregate)
    export class Invoice extends AggregateRoot<InvoiceProps> {
      // ...
    }

    // Behavioral Object (Domain Event)
    export class InvoicePaidEvent implements IDomainEvent {
      // ...
    }
  }
  ```
- [DON'T] Mix archetypes indiscriminately, such as placing raw state mutation logic inside a Domain Event, or treating an Aggregate as a Namespace.

**Example 3: Optimizing Code**
- [DO] Write code that is expressive and easy for a human to understand, even if it requires an extra iteration.
  ```typescript
  // Optimized for humans
  const activeUsers = users.filter(user => user.isActive);
  const activeUserEmails = activeUsers.map(user => user.email);
  ```
- [DON'T] Write cryptic, highly condensed code solely to save CPU cycles or memory, at the expense of human comprehension.
  ```typescript
  // Optimized for computers (Harder for humans to read)
  const activeUserEmails = users.reduce((acc, user) => {
    if (user.isActive) acc.push(user.email);
    return acc;
  }, []);
  ```