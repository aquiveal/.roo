# @Domain

These rules MUST be triggered when the AI is tasked with high-level software architecture design, system decomposition, defining component boundaries, domain modeling, resolving business terminology conflicts, designing microservices/subsystems, or assigning team ownership to specific software components.

# @Vocabulary

- **Bounded Context**: An explicit, designed boundary within which a specific Ubiquitous Language and its associated Model are strictly consistent and applicable. It is the applicability context of a model.
- **Model**: A simplified, abstraction-based representation of a real-world system designed to solve a specific problem (e.g., a map, or a cardboard cutout of a refrigerator). 
- **Ubiquitous Language**: The domain-specific language that is ubiquitous *only* within the strict boundaries of a single Bounded Context. It is NOT universal across the enterprise.
- **Subdomain**: A fine-grained area of business activity. Subdomains are *discovered* as part of analyzing the business strategy.
- **Physical Boundary**: The hard technological boundary of a Bounded Context. Each Bounded Context MUST be implemented as an individual service, project, or subsystem with an independent lifecycle and versioning.
- **Logical Boundary**: The internal organizational structures within a Bounded Context, such as namespaces, modules, or packages.
- **Ownership Boundary**: The socio-technical boundary defining team responsibility. A Bounded Context belongs to one and only one team.
- **Semantic Domain**: A lexicographical concept where the area of meaning dictates the definition of a word (e.g., "tomato" is a fruit in botany, but a vegetable in culinary arts). Bounded Contexts mirror this concept in software.

# @Objectives

- The AI MUST tackle domain complexity by dividing inconsistent business models into separate, explicit Bounded Contexts.
- The AI MUST ensure that every term in a Ubiquitous Language has exactly one unambiguous meaning within its Bounded Context.
- The AI MUST design models that are strictly purpose-driven, omitting extraneous details that do not serve the immediate problem (avoiding "jack-of-all-trades" models).
- The AI MUST establish explicit physical and ownership boundaries for all software components, decoupling their implementation and evolution lifecycles.
- The AI MUST clearly distinguish between what is discovered (Subdomains) and what is engineered (Bounded Contexts) when architecting systems.

# @Guidelines

- **Handling Inconsistent Models**: When encountering a business term with multiple, conflicting definitions depending on the department or context (e.g., "Lead" in Marketing vs. "Lead" in Sales), the AI MUST divide the domain into distinct Bounded Contexts.
- **Anti-Pattern Avoidance (Prefixing)**: The AI MUST NOT resolve terminology conflicts by adding context prefixes to class names within a single monolithic model (e.g., `MarketingLead` and `SalesLead`). Instead, the AI MUST separate them into distinct physical Bounded Contexts where the term `Lead` can be used cleanly in both.
- **Anti-Pattern Avoidance (Enterprise Models)**: The AI MUST NOT design a single, universal model or an enterprise-wide Entity Relationship Diagram (ERD). Models MUST be bounded.
- **Sizing and Scope**: When deciding the size of a Bounded Context, the AI MUST prioritize "usefulness" over strict size metrics. The AI MUST NOT split a set of coherent use cases that operate on the same data into multiple Bounded Contexts, as this introduces severe integration overhead and prevents independent evolution.
- **Subdomain vs. Bounded Context Mapping**: The AI MUST treat Subdomains as fixed discoveries of the business strategy, but MUST actively design the Bounded Contexts. The AI MAY map them 1:1, but MAY also design a single Bounded Context that spans multiple subdomains, or define multiple Bounded Contexts for a single subdomain if different models are needed to solve different problems.
- **Physical Boundaries**: The AI MUST enforce Bounded Contexts as physical boundaries. Each Bounded Context MUST be capable of independent implementation, evolution, and versioning. The AI MUST allow different Bounded Contexts to use entirely different technology stacks if appropriate.
- **Ownership Boundaries**: The AI MUST assign ownership of a Bounded Context to ONE team only. The AI MUST NOT allow multiple teams to work on or maintain the same Bounded Context. However, the AI MAY assign multiple Bounded Contexts to a single team.
- **Purpose-Driven Modeling**: When designing a model, the AI MUST follow the "Cardboard Refrigerator" principle: design the simplest model that accurately solves the specific problem at hand (e.g., verifying width vs. height), and intentionally ignore real-world attributes that are irrelevant to that specific context. Over-engineering a highly detailed model to solve a simple problem is strictly forbidden.

# @Workflow

1. **Analyze Domain Terminology**: Scan the provided requirements and business rules for terms that hold conflicting meanings, behaviors, or lifecycles across different user groups or departments.
2. **Identify Model Boundaries**: If conflicting mental models exist, define explicit Bounded Contexts for each distinct problem domain to serve as consistency boundaries.
3. **Define the Ubiquitous Language**: Within each newly defined Bounded Context, establish a strict, unambiguous Ubiquitous Language free of prefixes or technical jargon.
4. **Determine Scope and Grouping**: Evaluate sets of coherent use cases. Group use cases that manipulate the same data into the same Bounded Context to minimize integration overhead.
5. **Establish Physical Boundaries**: Define the architectural structure by separating Bounded Contexts into independent services, projects, or subsystems.
6. **Assign Ownership**: Explicitly state the team ownership for each Bounded Context, enforcing the rule that no two teams may share a single Bounded Context.
7. **Map to Subdomains**: Document the relationship between the designed Bounded Contexts and the discovered business Subdomains, justifying the mapping strategy (e.g., 1:1 for clarity, or encompassing multiple subdomains to group related workflows).
8. **Refine Models**: Strip away extraneous properties from the domain objects within each Bounded Context, ensuring they contain *only* the data and behavior necessary to fulfill their specific, bounded purpose.

# @Examples (Do's and Don'ts)

### Resolving Terminology Conflicts
- **[DO]**: Separate conflicting terms into distinct physical services/namespaces.
  ```csharp
  // Bounded Context: Marketing
  namespace MarketingContext.Domain 
  {
      public class Lead 
      {
          // Represents a simple notification/event of interest
          public string ContactInfo { get; set; }
          public string CampaignSource { get; set; }
      }
  }

  // Bounded Context: Sales
  namespace SalesContext.Domain 
  {
      public class Lead 
      {
          // Represents a complex, long-running sales process lifecycle
          public SalesPipeline Pipeline { get; set; }
          public List<Interaction> InteractionHistory { get; set; }
      }
  }
  ```
- **[DON'T]**: Shoehorn conflicting models into a single context using prefixes, inducing cognitive load.
  ```csharp
  // Monolithic Context
  namespace Enterprise.Domain 
  {
      public class MarketingLead { ... }
      public class SalesLead { ... }
  }
  ```

### Purpose-Driven Modeling
- **[DO]**: Create simple, hyper-focused models that solve exact problems (The Cardboard Refrigerator rule).
  ```csharp
  // Bounded Context: Delivery Navigation (Solving: Can the truck pass under the bridge?)
  public class TruckClearanceModel 
  {
      public double HeightInMeters { get; set; }
  }

  // Bounded Context: Cargo Capacity (Solving: Can the boxes fit in the truck?)
  public class TruckVolumeModel 
  {
      public double VolumeInCubicMeters { get; set; }
      public double MaxWeightCapacity { get; set; }
  }
  ```
- **[DON'T]**: Create an omnipotent, real-world copy of an entity that includes everything.
  ```csharp
  // Jack-of-all-trades Model
  public class Truck 
  {
      public double HeightInMeters { get; set; }
      public double VolumeInCubicMeters { get; set; }
      public double MaxWeightCapacity { get; set; }
      public string EngineType { get; set; }
      public string DriverName { get; set; }
      public string RadioBrand { get; set; } // Irrelevant data bloating the model
  }
  ```

### Team Ownership Boundaries
- **[DO]**: Declare explicit ownership constraints in architectural definitions.
  `Bounded Context A (Billing) -> Owned entirely by Team Alpha.`
  `Bounded Context B (Shipping) -> Owned entirely by Team Alpha.`
- **[DON'T]**: Split ownership of a single context.
  `Bounded Context C (Inventory) -> Maintained by Team Alpha AND Team Beta.`