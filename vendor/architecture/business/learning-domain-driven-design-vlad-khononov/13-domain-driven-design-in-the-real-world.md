# @Domain
These rules MUST be activated when the AI is tasked with analyzing, refactoring, or modernizing brownfield projects, legacy systems, or "big ball of mud" codebases. They also apply when the AI is asked to decompose monolithic architectures, introduce Domain-Driven Design (DDD) concepts into an existing codebase, or plan migration strategies for existing software systems.

# @Vocabulary
- **Brownfield Project**: An existing software project that has already proven its business viability but suffers from technical debt, legacy code, or design entropy.
- **Big Ball of Mud**: A haphazardly structured, sprawling, sloppy, spaghetti-code jungle that lacks clear boundaries or design.
- **Core Subdomain**: The business capability that differentiates the company from competitors, providing a competitive advantage. It contains complex business logic. In legacy systems, it is often the worst-designed, most feared component that the business refuses to rewrite.
- **Generic Subdomain**: Business capabilities that all companies execute the same way, often fulfilled by off-the-shelf solutions, subscriptions, or open-source software.
- **Supporting Subdomain**: Custom-built capabilities that do not provide a competitive edge but are necessary to support the business.
- **Strangler Pattern (Strangler Fig)**: A migration strategy where new requirements are implemented in a new bounded context, and legacy functionality is gradually extracted to the new context until the legacy system can be retired.
- **Façade Pattern**: A thin abstraction layer acting as the public interface, responsible for routing requests to either the legacy system or the modernized bounded context during a Strangler migration.
- **Ubiquitous Language**: A shared, consistent language used by both domain experts and software engineers to describe the business domain, strictly devoid of technical jargon.
- **Anticorruption Layer (ACL)**: A translation layer used to protect a modernized bounded context from the awkward, messy models of legacy systems.
- **Open-Host Service (OHS)**: A pattern where a component decouples its implementation model from its public API, exposing a published language to protect consumers from internal changes.
- **Logical Boundary**: Organizational structures within a single codebase (e.g., namespaces, modules, packages) that separate concepts without enforcing physical deployment separation.
- **Physical Boundary**: Architectural separation where components (e.g., bounded contexts) are deployed, tested, and evolved independently.

# @Objectives
- Modernize and refactor legacy codebases incrementally without resorting to a risky "big rewrite".
- Discover and recover lost domain knowledge by mapping existing code to business subdomains.
- Align the codebase's logical boundaries with the business's actual subdomains before extracting physical microservices or separate bounded contexts.
- Introduce DDD concepts pragmatically and "undercover" by justifying architectural changes with sound engineering logic rather than dogmatic DDD terminology.
- Protect data consistency and model integrity during migrations using established strategic integration patterns (Strangler, Façade, ACL, OHS).

# @Guidelines

## Strategic Analysis Constraints
- The AI MUST NOT recommend a complete system rewrite from scratch. The AI MUST enforce an incremental modernization strategy ("think big, but start small").
- When analyzing a legacy system, the AI MUST identify the types of subdomains (Core, Generic, Supporting) using structural heuristics (e.g., organizational charts) and code heuristics.
- The AI MUST treat the most poorly designed, complex, and unreplaceable legacy components as high-probability Core Subdomains.
- The AI MUST identify Generic Subdomains by looking for custom code that could be replaced by off-the-shelf or open-source solutions.

## Boundary Reorganization Constraints
- Before suggesting physical separation (e.g., microservices), the AI MUST reorganize logical boundaries (namespaces, packages, modules) to align with subdomain boundaries.
- The AI MUST identify and track business logic hidden in infrastructure or platforms, such as database stored procedures or serverless functions, and mandate their reorganization to reflect the new logical boundaries.
- The AI MUST decouple development lifecycles by defining physical bounded contexts IF AND ONLY IF multiple teams are working on the same codebase, or if conflicting models exist within the same component.

## Integration & Migration Constraints
- The AI MUST use the Strangler Pattern for component replacement.
- When implementing the Strangler Pattern, the AI MUST generate a Façade layer to route traffic dynamically between legacy and modernized contexts.
- The AI MAY suspend the strict "one database per bounded context" rule ONLY during a Strangler migration, allowing the legacy and modernized systems to share a database temporarily to avoid complex distributed transactions.
- The AI MUST apply an Anticorruption Layer (ACL) to protect modernized code from legacy data structures.
- The AI MUST apply an Open-Host Service (OHS) to protect external consumers from breaking changes while the legacy codebase is being refactored.
- If multiple teams experience high friction co-evolving shared, non-core functionality, the AI MUST recommend the "Separate Ways" pattern (duplicating the non-core functionality).

## Tactical Refactoring Constraints
- The AI MUST identify and flag painful mismatches between business value and technical implementation (e.g., a Core Subdomain implemented as a simple Transaction Script).
- The AI MUST NOT refactor procedural legacy code (Transaction Script/Active Record) directly into an Event-Sourced Domain Model.
- Tactical refactoring MUST proceed in safe, incremental steps:
  1. Extract procedural code into Active Records.
  2. Identify immutable data structures and extract Value Objects.
  3. Relocate state-modifying logic inside object boundaries (making setters private).
  4. Identify transactional boundaries and define State-Based Aggregates.
  5. Only transition to an Event-Sourced Domain Model once state-based boundaries are proven solid.

## Undercover DDD & Ubiquitous Language Constraints
- The AI MUST enforce the Ubiquitous Language by renaming classes, methods, and variables to remove technical jargon and reflect the business domain.
- The AI MUST resolve inconsistent legacy terminology by making hidden contexts explicit (e.g., unifying terms or splitting models).
- When justifying a design change to users, the AI MUST use fundamental engineering logic rather than DDD buzzwords. (e.g., Justify Aggregates by stating: "We must protect data consistency by modifying this state in a single transaction," NOT by stating "DDD requires an Aggregate Root here").
- To justify small aggregate boundaries, the AI MUST cite performance impacts and complexity reduction.

# @Workflow
When tasked with refactoring, migrating, or analyzing a brownfield project, the AI MUST follow this rigid, step-by-step algorithm:

1. **Strategic Domain Analysis**:
   - Ask the user to define or help deduce the overarching business domains, customers, and competitive advantages.
   - Categorize the existing system components into Core, Generic, and Supporting subdomains using legacy code characteristics as heuristics.

2. **Explore the Current Design**:
   - Map the current subsystems, focusing on decoupled lifecycles and tactical patterns currently in use (e.g., Active Record, Transaction Script).
   - Identify suboptimal strategic decisions (e.g., shared databases across unrelated domains, multiple teams on one monolith, duplicated core logic).

3. **Modernize Logical Boundaries**:
   - Generate refactoring steps to group existing code into namespaces, packages, or folders that accurately reflect the identified subdomains.
   - Reorganize associated database artifacts (like stored procedures) into schemas matching the new logical boundaries.

4. **Strategic Modernization**:
   - Determine whether to extract physical bounded contexts based on team friction or conflicting models.
   - Select the appropriate integration pattern (Strangler with Façade, ACL, OHS, or Separate Ways).

5. **Tactical Refactoring Execution**:
   - Enforce the Ubiquitous Language by renaming variables and methods.
   - Apply the incremental tactical refactoring steps: encapsulate data, introduce Value Objects, enforce private setters, define transaction boundaries (Aggregates).
   - Implement the Façade routing logic if applying the Strangler pattern.

# @Examples (Do's and Don'ts)

## 1. Logical Boundary Alignment
- **[DO]** Reorganize a monolithic folder structure to reflect business capabilities:
  ```text
  /src
    /Marketing
      /Campaigns
      /CreativeCatalog
    /CRM
      /Leads
      /AgentCommissions
  ```
- **[DON'T]** Organize legacy code by technical concern:
  ```text
  /src
    /Controllers
    /Models
    /Views
    /Services
    /Repositories
  ```

## 2. Strangler Pattern with Façade
- **[DO]** Implement a Façade to route requests during migration:
  ```csharp
  public class OrderFacade 
  {
      private readonly LegacyOrderService _legacyService;
      private readonly ModernizedOrderContext _newContext;
      private readonly FeatureFlags _flags;

      public OrderResponse ProcessOrder(OrderRequest request) 
      {
          if (_flags.IsModernizedOrderFlowEnabled(request.CustomerId)) 
          {
              return _newContext.Process(request);
          }
          return _legacyService.Process(request);
      }
  }
  ```
- **[DON'T]** Immediately delete the legacy code and point all endpoints to a partially completed new system, or force a "big bang" release.

## 3. Incremental Tactical Refactoring
- **[DO]** Refactor an anemic domain model by making setters private and moving logic inside the boundary:
  ```csharp
  public class Player 
  {
      public Guid Id { get; private set; }
      public int Points { get; private set; }

      public void ApplyBonus(int percentage) 
      {
          this.Points = (int)(this.Points * (1 + percentage / 100.0));
      }
  }
  ```
- **[DON'T]** Leave setters public and execute business logic in a scattered transaction script:
  ```csharp
  public class ApplyBonus 
  {
      public void Execute(Guid playerId, byte percentage) 
      {
          var player = _repository.Load(playerId);
          player.Points *= 1 + percentage / 100.0; // Logic leaked outside entity
          _repository.Save(player);
      }
  }
  ```

## 4. "Undercover" DDD Explanations
- **[DO]** Justify design choices using engineering principles:
  *"We should restrict external components from directly modifying the `Player.Points` property to ensure that the bonus calculation logic is collocated, preventing logic duplication and data corruption."*
- **[DON'T]** Use dogmatic DDD terminology to justify decisions:
  *"We must make `Player.Points` private because `Player` is an Aggregate Root, and DDD principles dictate that state modifications must go through the Root."*

## 5. Ubiquitous Language Enforcement
- **[DO]** Use terms native to the business process:
  ```csharp
  public class SalesLead 
  {
      public void ConvertToCustomer() { ... }
      public void ScheduleFollowUp(DateTime date) { ... }
  }
  ```
- **[DON'T]** Use CRUD-based technical jargon in the domain model:
  ```csharp
  public class CrmLeadDbRecord 
  {
      public void UpdateStatusFlag(int statusId) { ... }
      public void InsertFollowUpRow(DateTime date) { ... }
  }
  ```