# @Domain
These rules MUST trigger when the AI is tasked with analyzing business requirements, defining system architecture, decomposing monolithic applications, determining build-vs-buy strategies, scoping software components, or organizing features into modules and services based on business value.

# @Vocabulary
- **Business Domain**: The company's main area of activity and the overarching service it provides to its clients (e.g., retail, public transportation, coffeehouse chain).
- **Subdomain**: A fine-grained area of business activity that acts as a building block for the overall Business Domain. Resembles a set of interrelated, coherent use cases.
- **Core Subdomain (Core Domain)**: The business area providing a competitive advantage. It is what the company does differently from its competitors. Characterized by high complexity, high volatility, and requires in-house implementation.
- **Generic Subdomain**: A business activity all companies perform in the same way. It provides no competitive edge. Characterized by high complexity, low volatility, and solved by buying or adopting existing solutions.
- **Supporting Subdomain**: An activity that supports the core business but provides no competitive advantage. Characterized by low complexity (CRUD/ETL operations), low volatility, and implemented in-house using rapid development tools or outsourced.
- **Coherent Use Cases**: A set of closely related use cases that involve the same actor, operate on the same business entities, and manipulate a closely related set of data. Used to define accurate Subdomain boundaries.
- **Domain Experts**: Subject matter experts who know the intricacies of the business. They are the knowledge authorities (often requirement creators or end users), not the software engineers or systems analysts.

# @Objectives
- The AI MUST accurately identify and distill the overarching Business Domain into precise, fine-grained Subdomains.
- The AI MUST categorize every identified Subdomain strictly into Core, Generic, or Supporting types.
- The AI MUST align technical design and implementation strategies precisely with the categorized Subdomain type, avoiding over-engineering simple problems or under-engineering complex competitive advantages.
- The AI MUST establish explicit boundaries around sets of Coherent Use Cases.
- The AI MUST defer to Domain Experts for business logic rules rather than inventing technical assumptions.

# @Guidelines

## Subdomain Identification and Boundary Definition
- When analyzing a system, the AI MUST begin by breaking down organizational departments or coarse-grained functions into finer-grained components.
- The AI MUST define Subdomain boundaries by grouping "Coherent Use Cases." The AI MUST check that grouped use cases share the same actor, manipulate the same data, and involve the same business entities.
- The AI MUST stop distilling Subdomains into finer levels when further decomposition no longer reveals new strategic insights or when all finer-grained subdomains are of the exact same type as the parent.
- The AI MUST exclude and ignore business functions that have no relation to the software being built (focus on the essentials).

## Subdomain Categorization
- The AI MUST classify a Subdomain as **Core** if it meets the following criteria: It is an invention, smart optimization, or business know-how; it directly affects the bottom line; it is hard for competitors to copy; it justifies being spun off as a standalone side business.
- The AI MUST classify a Subdomain as **Generic** if it meets the following criteria: It is a complex, already solved problem; all competitors do it the exact same way; standard industry practices exist (e.g., authentication, encryption, payment clearing).
- The AI MUST classify a Subdomain as **Supporting** if it meets the following criteria: The business logic is simple (obvious data entry, CRUD, ETL); it does not provide a competitive edge; it is cheaper/simpler to hack an in-house implementation than to integrate an external generic solution.

## Implementation Strategies by Subdomain Type
- **Core Subdomain Implementation**: The AI MUST prescribe custom, in-house development. The AI MUST apply the most advanced engineering techniques and design patterns. The AI MUST prepare the architecture for high volatility and emergent, continuously evolving requirements. The AI MUST NOT suggest outsourcing or buying off-the-shelf products for these components.
- **Generic Subdomain Implementation**: The AI MUST prescribe buying off-the-shelf products or adopting battle-tested open-source solutions. The AI MUST NOT suggest building custom logic for these problems from scratch.
- **Supporting Subdomain Implementation**: The AI MUST prescribe simple technical solutions (Rapid Application Development frameworks, simple CRUD applications). The AI MUST permit cutting technical corners. The AI MUST suggest outsourcing or assigning junior talent if requested for resource allocation. The AI MUST NOT recommend elaborate design patterns or advanced architectures here.

## Handling Ambiguity and Domain Experts
- When the AI detects missing business rules, implicit constraints, or unclear requirements, it MUST explicitly instruct the user to consult "Domain Experts" to capture their mental models, rather than generating assumed technical workarounds.

# @Workflow
When tasked with designing a new system, evaluating an architecture, or writing a feature breakdown, the AI MUST execute the following algorithmic process:

1. **Contextualize the Business Domain**: State the overarching service the company provides to its clients.
2. **Decompose Organizational Units**: List the coarse-grained departments or activities involved in the requirement.
3. **Distill into Coherent Use Cases**: Break down the coarse-grained activities into discrete sets of use cases bound by actors and data sets.
4. **Categorize Subdomains**: Apply the complexity, volatility, and competitive advantage checks to label each distilled set as a Core, Generic, or Supporting Subdomain.
5. **Assign Solution Strategy**:
    - For Core: Define a highly maintainable, custom-coded architecture.
    - For Generic: Identify and list 2-3 specific open-source or commercial off-the-shelf (COTS) alternatives to integrate.
    - For Supporting: Define a minimal, fast-to-build CRUD/ETL approach.
6. **Validate Relevance**: Filter out any identified subdomains that do not require software representation.

# @Examples (Do's and Don'ts)

## Core Subdomains
- **[DO]**
  ```markdown
  **Subdomain**: Rideshare Route Optimization
  **Type**: Core Subdomain
  **Strategy**: Implement in-house using advanced pathfinding algorithms. The architecture must support continuous iteration and emergent design to maintain a competitive advantage. Do not use standard off-the-shelf mapping tools for the core matching logic.
  ```
- **[DON'T]**
  ```markdown
  **Subdomain**: Fraud Detection Analysis
  **Type**: Core Subdomain
  **Strategy**: Let's integrate a generic third-party SaaS to handle our proprietary fraud detection to save development time.
  ```
  *(Anti-pattern: Outsourcing a core competitive advantage destroys high entry barriers for competitors).*

## Generic Subdomains
- **[DO]**
  ```markdown
  **Subdomain**: User Authentication & Authorization
  **Type**: Generic Subdomain
  **Strategy**: Adopt an existing identity provider (e.g., Auth0, Keycloak). The problem is complex, but provides no business differentiation. Do not build custom password hashing or session management.
  ```
- **[DON'T]**
  ```markdown
  **Subdomain**: Payment Clearing
  **Type**: Generic Subdomain
  **Strategy**: We will write a custom transaction ledger and cryptographic token system from scratch to process credit cards.
  ```
  *(Anti-pattern: Wasting in-house engineering effort on "known unknowns" that are already solved by the industry).*

## Supporting Subdomains
- **[DO]**
  ```markdown
  **Subdomain**: Promo Code Management
  **Type**: Supporting Subdomain
  **Strategy**: Build a simple CRUD interface using a Rapid Application Development framework (e.g., Django Admin or Ruby on Rails scaffolding). The logic is simple data entry and does not require complex design patterns.
  ```
- **[DON'T]**
  ```markdown
  **Subdomain**: Employee Shift Scheduling
  **Type**: Supporting Subdomain
  **Strategy**: Implement a highly decoupled microservices architecture with Event Sourcing and CQRS to manage the creation and reading of employee shifts.
  ```
  *(Anti-pattern: Applying advanced engineering techniques and high complexity to a subdomain with obvious, low-value business logic).*

## Subdomain Boundaries (Coherent Use Cases)
- **[DO]**
  ```markdown
  **Boundary Definition**: The "Help Desk" subdomain is too coarse. We must distill it. 
  - Subdomain 1: "Ticket Routing Algorithm" (Core - specific actor, proprietary data).
  - Subdomain 2: "Agent Shift Management" (Supporting - simple CRUD, separate data).
  - Subdomain 3: "Telephony/VoIP" (Generic - off-the-shelf integration).
  ```
- **[DON'T]**
  ```markdown
  **Boundary Definition**: The "Customer Service" department uses tickets, phones, and shift schedules. We will build one single "Customer Service Subdomain" to handle all of these because they belong to the same department.
  ```
  *(Anti-pattern: Failing to distill coarse-grained organizational units into distinct subdomains with different strategic values).*