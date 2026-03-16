@Domain
These rules MUST be activated when the AI is tasked with analyzing business requirements, defining system architecture, identifying microservice boundaries, breaking down monolithic systems ("Big Ball of Mud"), creating top-level project structures (packages/namespaces), resolving naming collisions in domain models, or planning system integrations. 

@Vocabulary
- **Domain**: The broad realm of what an organization does and the world in which it operates.
- **Subdomain**: A specific, logical functional area within the broader Domain (e.g., Inventory, Shipping, Product Catalog).
- **Core Domain**: The most important Subdomain to the business's ongoing success. The primary strategic initiative that requires the highest priority, the best developers, and provides a distinct competitive advantage.
- **Supporting Subdomain**: An essential area of the business that supports the Core Domain but does not provide a distinguishing competitive advantage. It requires custom development because off-the-shelf solutions do not exist or fit.
- **Generic Subdomain**: A Subdomain required for the overall business solution but captures nothing special to the business (e.g., Identity/Access, Geographical Mapping). Can often be replaced by off-the-shelf software.
- **Bounded Context**: An explicit conceptual and linguistic boundary within which a specific domain model exists. Inside this boundary, every term of the Ubiquitous Language has a strict, unambiguous meaning.
- **Problem Space**: The conceptual combination of the Core Domain and the Subdomains needed to solve a strategic business challenge. Assessed using Subdomains.
- **Solution Space**: The physical/technical implementation realized as software. Assessed and defined using Bounded Contexts.
- **Ubiquitous Language**: A shared, precise language agreed upon by both domain experts and developers, valid strictly within a single Bounded Context.
- **Big Ball of Mud**: An anti-pattern where distinct domain models and languages are intertwined and mixed indiscriminately, leading to tightly coupled, brittle systems.

@Objectives
- Explicitly segregate distinct business models linguistically and technically using Bounded Contexts.
- Prevent the creation of a single, all-encompassing enterprise domain model.
- Treat context as king: Ensure every term inside a Bounded Context has exactly one unambiguous meaning.
- Keep Bounded Contexts pure by aggressively factoring out extraneous, supporting, or generic concepts into their own boundaries.
- Align the Problem Space (Subdomains) one-to-one with the Solution Space (Bounded Contexts) whenever possible, particularly in greenfield development.

@Guidelines
- **Linguistic Boundaries**: You MUST enforce Bounded Contexts as linguistic boundaries. If the same term (e.g., "Customer", "Book", "Account") has different meanings, lifecycles, or properties in different business processes, you MUST model them as completely different objects in separate Bounded Contexts.
- **Enterprise Models**: You MUST NOT attempt to model the entire business enterprise in a single domain model.
- **Subdomain Classification**: You MUST classify every identified concept/subdomain as Core, Supporting, or Generic to prioritize architectural and developmental investments.
- **Problem vs. Solution Space Assessment**: You MUST use Subdomains to analyze the problem space (business needs) and Bounded Contexts to define the solution space (software realization).
- **Separation of Generic Concerns**: You MUST completely decouple Generic Subdomains (e.g., Security, Permissions, Identity) from the Core Domain. The Core Domain must rely on translated concepts (e.g., `Author`, `Moderator`) rather than raw generic concepts (e.g., `User`, `Role`).
- **Bounded Context Contents**: A Bounded Context MUST encapsulate the Domain Model, but it MUST ALSO encompass the User Interface, Application Services, RESTful endpoints, and the Database Schema (if the schema is maintained by the modeling team).
- **Sizing Contexts**: You MUST size a Bounded Context to be exactly as large as needed to fully express its Ubiquitous Language—neither more nor less. 
- **Artificial Boundaries**: You MUST NOT create fake or miniature Bounded Context boundaries to accommodate architectural frameworks, deployment modularity, or developer task distribution.
- **Team Alignment**: You MUST assign exactly one cohesive team to a single Bounded Context. Multiple teams working in the same Bounded Context inevitably fragment the Ubiquitous Language.
- **Package Naming**: You MUST align technical components (packages/namespaces) with the Bounded Context. The naming convention MUST reflect the context (e.g., `com.companyname.contextname`), excluding arbitrary marketing product names that could change over time.

@Workflow
1. **Assess the Problem Space**: Break the overarching business Domain down into logical Subdomains. List all business functions involved in the system.
2. **Classify Subdomains**: Categorize each identified Subdomain as the Core Domain, a Supporting Subdomain, or a Generic Subdomain. 
3. **Assess the Solution Space**: Identify existing legacy systems, software assets, and physical subsystems. Evaluate how they map to the identified Subdomains.
4. **Define Linguistic Boundaries (Bounded Contexts)**: Group highly cohesive domain concepts together. Where definitions, lifecycles, or rules differ for a specific term, draw a strict boundary and create a new Bounded Context.
5. **Isolate Extraneous Concepts (Segregated Core)**: Identify technical or generic capabilities (like users, permissions, or access control) embedded in the Core Domain. Factor these out into separate Bounded Contexts.
6. **Establish Technical Alignment**: Create the top-level technical container (package/namespace) named for the Bounded Context (e.g., `com.saasovation.agilepm`). 
7. **Enclose Related Components**: Ensure that the database schema, User Interface, Application Services, and the domain model itself are strictly housed within the specific Bounded Context.

@Examples (Do's and Don'ts)

**Linguistic Boundaries and Object Naming**
- [DO] Model a single concept differently based on context. For example, in an e-commerce system, create a `Customer` object in the `CatalogContext` (focused on browsing, loyalty, discounts) and a completely separate `Customer` object in the `OrderContext` (focused strictly on billing and shipping addresses).
- [DON'T] Create a massive, all-knowing `Customer` object that contains loyalty points, shopping carts, shipping addresses, and support tickets, attempting to satisfy every department in the enterprise.

**Separating Generic Subdomains from Core Domains**
- [DO] Extract identity/security into an `Identity and Access Context`. Pass only the specific, translated business role (e.g., `Author` or `Moderator`) into the `Collaboration Context` when a user attempts to act.
- [DON'T] Couple core business logic to generic security concepts. Do not write code inside a core domain object like `Forum` that directly checks user permissions: `if (!user.hasPermissionTo(Permission.Forum.StartDiscussion)) { throw ... }`.

**Database Schema Alignment**
- [DO] Let the domain model drive the database schema inside the Bounded Context. Table names and columns must reflect the Ubiquitous Language explicitly (e.g., `tbl_backlog_item` with columns mapping directly to Value Object properties).
- [DON'T] Allow a centralized, enterprise-wide database schema or a separate data-modeling team to force structural compromises onto the localized domain model.

**Sizing Bounded Contexts**
- [DO] Keep all naturally cohesive domain concepts (e.g., `Forum`, `Post`, `Discussion`, `Calendar`) that share a common language together inside a single `Collaboration Context`. 
- [DON'T] Arbitrarily miniaturize contexts (e.g., creating a separate Bounded Context for `Forum` and another for `Calendar`) just because they can be deployed independently or assigned to different developers. Use *Modules* (namespaces/packages) for internal organization, not Bounded Contexts.