# @Domain
Trigger these rules when evaluating, designing, refactoring, or documenting the communication, relationships, or integration contracts between multiple Bounded Contexts, subsystems, or microservices within a software architecture.

# @Vocabulary
- **Contract**: A touchpoint or defined interface between bounded contexts that regulates their interaction and data exchange.
- **Cooperation**: An integration relationship reserved for bounded contexts implemented by teams with well-established communication and aligned goals.
- **Partnership**: An ad hoc, two-way integration pattern where teams coordinate seamlessly to resolve API changes without dictating a shared language.
- **Shared Kernel**: A tightly limited, overlapping model (codebase or data structure) shared and co-evolved by multiple bounded contexts.
- **Customer-Supplier**: An integration relationship characterized by an imbalance of power, where one context provides a service (Upstream/Supplier) and another consumes it (Downstream/Customer).
- **Conformist**: A Customer-Supplier pattern where the downstream consumer accepts and strictly adheres to the upstream supplier's model.
- **Anticorruption Layer (ACL)**: A Customer-Supplier pattern where the downstream consumer translates the upstream supplier's model into a model tailored to its own Ubiquitous Language and needs.
- **Open-Host Service (OHS)**: A Customer-Supplier pattern where the upstream supplier decouples its internal implementation model from its public interface to protect consumers from changes.
- **Published Language**: The integration-oriented public protocol/model exposed by an Open-Host Service.
- **Separate Ways**: A pattern where teams deliberately avoid collaboration and duplicate functionality within their own bounded contexts.
- **Context Map**: A visual representation or diagram plotting the system's bounded contexts and the specific integration patterns connecting them.

# @Objectives
- Enforce explicit integration patterns based on team communication levels, power dynamics, and subdomain types.
- Protect the integrity of Core Subdomains from external model corruption or uncontrolled upstream changes.
- Ensure integration costs are balanced against duplication costs.
- Maintain a decoupled internal implementation by translating models at the boundaries of bounded contexts.
- Make architectural, communication, and organizational relationships explicit through the continuous maintenance of a Context Map.

# @Guidelines
- **General Integration Constraints**
  - The AI MUST NEVER treat bounded contexts as entirely independent; always define explicit integration contracts for their touchpoints.
  - The AI MUST resolve language conflicts at the boundaries by explicitly designating which language is used for integration.

- **Applying Cooperation Patterns**
  - *Partnership*: The AI MUST recommend this only for teams with excellent, friction-free communication and Continuous Integration (CI) practices. The AI MUST NOT recommend Partnership for geographically distributed or politically siloed teams.
  - *Shared Kernel*: The AI MUST restrict the shared scope exclusively to integration contracts and data structures intended to cross boundaries. The AI MUST require CI and automated integration tests triggered on every modification to the shared kernel. The AI MUST recommend this only when the cost of duplication strictly outweighs the cost of coordination (e.g., highly volatile core subdomains, or as a temporary bridge during legacy modernization).

- **Applying Customer-Supplier Patterns**
  - *Conformist*: The AI MUST recommend this only if the upstream model is an established industry standard, or if the downstream team has zero leverage to negotiate and the upstream model is "good enough."
  - *Anticorruption Layer (ACL)*: The AI MUST mandate an ACL if the downstream context contains a Core Subdomain. The AI MUST recommend an ACL when integrating with messy legacy systems, or when the upstream contract changes frequently.
  - *Open-Host Service (OHS)*: The AI MUST require the upstream context to decouple its internal models from its integration models. The AI MUST define a "Published Language" for the public API. The AI MUST leverage OHS to concurrently support multiple versions of an API during migrations.

- **Applying Separate Ways**
  - The AI MUST consider this pattern if team communication is impossible or if model differences make ACLs too expensive.
  - The AI MUST allow Separate Ways for Generic Subdomains (e.g., local logging implementations) where duplication is cheaper than integration.
  - **CRITICAL ANTI-PATTERN**: The AI MUST NEVER recommend or allow the Separate Ways pattern for integrating or implementing a Core Subdomain. Duplicating a company's competitive advantage is strictly prohibited.

- **Context Mapping**
  - The AI MUST treat the Context Map as an evolving architectural document (preferably as code, e.g., Context Mapper).
  - The AI MUST use the Context Map to infer organizational issues (e.g., if a single upstream team forces all consumers to build ACLs, the AI MUST flag the upstream model as potentially hostile or inefficient).

# @Workflow
1. **Assess Collaboration Context**: Determine the communication quality, geographical distribution, and power dynamics between the teams owning the bounded contexts.
2. **Identify Subdomain Types**: Classify the subdomains involved as Core, Supporting, or Generic.
3. **Select Integration Pattern**:
   - If communication is excellent and mutual adaptation is easy: Choose *Partnership*.
   - If duplication costs are too high and logic is volatile: Choose *Shared Kernel*.
   - If downstream has no power and upstream is well-designed/standard: Choose *Conformist*.
   - If downstream is a Core Subdomain or upstream is a legacy mess: Choose *Anticorruption Layer*.
   - If upstream wants to protect multiple consumers from its internal changes: Choose *Open-Host Service*.
   - If collaboration is impossible/too costly and it is NOT a Core Subdomain: Choose *Separate Ways*.
4. **Design the Boundary**:
   - For ACL: Generate the translation/mapping logic.
   - For OHS: Define the Published Language (the integration-specific DTOs/Events).
   - For Shared Kernel: Define the minimal shared library structure.
5. **Update the Context Map**: Document the chosen relationship (e.g., `[Upstream OHS] -> [Downstream ACL]`) to maintain a bird's-eye view of system topology.

# @Examples (Do's and Don'ts)

**Shared Kernel**
- [DO]: Extract strictly the API contract interfaces and shared messaging DTOs into a dedicated, version-controlled library referenced by both bounded contexts. Trigger tests for both contexts upon PR.
- [DON'T]: Share the internal database schema, ORM entities, or complex business logic implementations across bounded contexts, causing deployment coupling.

**Anticorruption Layer (ACL)**
- [DO]: Create a translation facade in the downstream context that receives an upstream `Legacy_Customer_Record` XML payload and maps it to a downstream `Subscriber` object using the local Ubiquitous Language.
- [DON'T]: Allow upstream terminology or legacy data structures to leak into the downstream domain logic (e.g., passing a `Legacy_Customer_Record` directly into a downstream domain service).

**Open-Host Service (OHS)**
- [DO]: Define a specific `IntegrationEvent` class (the Published Language) mapped from internal domain events, ensuring that if the internal domain model changes, the integration event contract remains stable.
- [DON'T]: Expose internal Aggregate models directly over a REST API or message bus, forcing consumers to break whenever internal refactoring occurs.

**Separate Ways**
- [DO]: Implement a generic authentication or logging utility locally within two different bounded contexts because integrating a centralized service would cause unnecessary network overhead.
- [DON'T]: Implement a proprietary, business-critical routing algorithm (Core Subdomain) independently in two different bounded contexts, creating duplicate, diverging versions of the company's competitive advantage.