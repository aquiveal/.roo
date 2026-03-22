# @Domain
These rules MUST trigger when the AI is tasked with creating, renaming, refactoring, or organizing directory structures, namespaces, packages, or modular boundaries within a software project. They specifically apply when the AI is deciding where to place domain objects (Entities, Value Objects, Aggregates, Domain Services, Repositories) or when organizing architectural layers (User Interface, Application, Infrastructure).

# @Vocabulary
- **Module**: A named container for domain object classes that are highly cohesive with one another (e.g., a `package` in Java, a `namespace` in C#, or a `module` in Ruby).
- **Cohesion**: The degree to which elements inside a Module belong together. In DDD, cohesion is strictly based on domain concepts and the Ubiquitous Language, not technical similarity.
- **Coupling**: The degree of interdependence between software modules. The goal is low coupling between different Modules and high cohesion within them.
- **Deployment Modularity**: The packaging of loosely coupled yet logically cohesive segments of software into a deployment unit by version (e.g., OSGi bundles, Java Jigsaw modules, JAR/DLL files). DDD Modules facilitate this physical separation.
- **Mechanical Organization**: An anti-pattern where classes are grouped by their technical stereotype, architectural pattern, or structural similarities (e.g., putting all interfaces in one module, or all Exceptions in another) rather than their domain meaning.

# @Objectives
- The AI MUST organize domain objects into Modules that tell the story of the system and reflect deep insight into the business domain.
- The AI MUST maintain low coupling between different Modules and high cohesion within individual Modules.
- The AI MUST treat Modules as first-class citizens of the domain model, aggressively renaming and refactoring them as domain insight evolves.
- The AI MUST name Modules strictly using the Ubiquitous Language of the Bounded Context, avoiding commercial brand names and mechanical technical terms.
- The AI MUST prefer separating fuzzy domain concepts using Modules before attempting to split them into entirely new Bounded Contexts.

# @Guidelines

## Module Conceptualization and Cohesion
- When deciding where to place a class, the AI MUST group it with other classes that form a cohesive business concept.
- The AI MUST NOT use Mechanical Organization. For example, never group objects simply because they are "fragile" or "sturdy," or because they are all "Repositories," "Factories," or "Exceptions."
- When evaluating an existing Module, the AI MUST recommend refactoring or renaming it if the current name or structure no longer accurately reflects the Ubiquitous Language.

## Hierarchical Naming Conventions
- When naming a Module, the AI MUST use a hierarchical structure separated by dots (or the language's equivalent namespace separator).
- **Top-Level**: The AI MUST begin the hierarchy with the organization's top-level domain name to prevent namespace collisions (e.g., `com.mycompany`).
- **Bounded Context**: The second segment MUST identify the Bounded Context. The AI MUST NOT use commercial product names or marketing brands for this segment, as brands change and do not reflect the domain model (e.g., use `agilepm`, NOT `projectovation`).
- **Layer Identifier**: The third segment MUST identify the architectural layer. For the domain model, the AI MUST use `.domain`.
- **Model Identifier**: The AI MUST use `.model` directly under `.domain` to house the actual domain objects (e.g., `com.mycompany.agilepm.domain.model`).
- **Concept Identifier**: The final segments MUST be the domain concept named strictly using the Ubiquitous Language (e.g., `...domain.model.product`).

## Module Size and Coupling Trade-offs
- When a Module accumulates too many classes (e.g., an Aggregate with many internal Entities, Value Objects, and Events, making the module cluttered), the AI MUST prioritize cognitive organization over strict acyclic coupling rules.
- To resolve cluttered Modules, the AI MUST create child sub-modules (e.g., splitting a `product` module into `product.backlogitem`, `product.release`, and `product.sprint`).
- When breaking a large module into sub-modules, the AI MAY allow bidirectional coupling between the parent concept and its child sub-modules if it accurately reflects the domain reality (e.g., `Product` acts as a Factory for `BacklogItem`, and `BacklogItem` holds a `ProductId`).

## Structuring Services and Base Classes
- The AI MUST place common, reusable base classes and interfaces (e.g., `Entity`, `DomainEvent`, `DomainRegistry`) at the root of the model layer (e.g., `...domain.model`).
- When placing Domain Services, the AI MAY place them in the same concept Module as the Aggregates they operate on.
- The AI MAY create a separate peer module for Domain Services (e.g., `...domain.service`), but the AI MUST evaluate this carefully and warn the user that doing so can inadvertently encourage an Anemic Domain Model by stripping behavior away from the `.model` classes.

## Modules in Other Layers (UI, Application, Infrastructure)
- When organizing components outside the domain model, the AI MUST apply parallel hierarchical modularity.
- For the Application layer, the AI MUST group Application Services by their use-case coordination boundaries (e.g., `...application.team`, `...application.product`).
- For the User Interface layer, the AI MUST group components by their presentation responsibilities (e.g., `...resources` for REST APIs, `...resources.view` for presentation rendering).
- If the application is simple enough, the AI MAY omit sub-modules in the Application layer and place all Application Services directly in the `...application` module.

## Module Before Bounded Context
- When encountering domain terms that are fuzzy or seemingly overlapping, the AI MUST FIRST attempt to separate these concepts using Modules (the "thinner boundary") within the same Bounded Context.
- The AI MUST NOT recommend creating a new Bounded Context (the "thicker boundary") for organizational purposes unless the linguistics strictly dictate that the terms have fundamentally different meanings requiring explicit context mapping.

# @Workflow
When tasked with creating a new domain concept or organizing an existing codebase, the AI MUST execute the following algorithm:

1. **Identify the Core Concept**: Determine the primary Aggregate or domain concept the class(es) represent.
2. **Determine the Bounded Context**: Identify the logical boundaries of the system. Ensure the name reflects the domain, not the marketing product.
3. **Establish the Hierarchy**: Construct the namespace path: `[TopLevelOrg].[BoundedContext].domain.model.[ConceptName]`.
4. **Evaluate Cohesion**: Verify that all objects placed in this Module tell a unified story about that specific concept. If mechanical groupings (like a `services` or `repositories` package) exist, dismantle them and move the classes into their respective concept Modules.
5. **Check Size and Clutter**: If the Module contains a massive number of associated classes (e.g., > 15-20 classes, including events, factories, and parts), create child Modules for the subordinate concepts.
6. **Apply to Outer Layers**: Mirror this domain-driven organization in the Application, UI, and Infrastructure layers, ensuring implementation classes are kept out of the domain model Modules.

# @Examples (Do's and Don'ts)

## [DO] Organize by Domain Concept
```java
// Correct hierarchical naming and cohesive grouping
package com.saasovation.agilepm.domain.model.product;

public class Product { ... }
public class ProductId { ... }
public class BusinessPriority { ... }
```

## [DON'T] Organize Mechanically
```java
// INCORRECT: Grouping by technical stereotype (Mechanical Organization)
package com.saasovation.agilepm.domain.repositories; // Anti-pattern

public interface ProductRepository { ... }
public interface TeamRepository { ... }
```

## [DO] Sub-Modularize for Organization
```java
// Correctly splitting a large "product" concept into sub-modules for child Aggregates
package com.saasovation.agilepm.domain.model.product.backlogitem;

public class BacklogItem { ... }
public class Task { ... }
```

## [DON'T] Use Brand or Product Names for Contexts
```java
// INCORRECT: Using the commercial software name "projectovation" instead of the domain context "agilepm"
package com.saasovation.projectovation.domain.model.product; 
```

## [DO] Parallel Organization in the Application Layer
```java
// Correctly organizing the Application layer using the same domain boundaries
package com.saasovation.agilepm.application.product;

public class ProductApplicationService { ... }
```

## [DON'T] Mix Infrastructure Implementations into Domain Modules
```java
// INCORRECT: Placing the Hibernate implementation inside the domain model module
package com.saasovation.agilepm.domain.model.product;

public class HibernateProductRepository implements ProductRepository { ... } 
// Fix: Move this to com.saasovation.agilepm.infrastructure.persistence
```