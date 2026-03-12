# @Domain

These rules MUST be triggered when the AI is asked to design system architecture, define microservice boundaries, scaffold new microservices, review inter-service communication contracts (APIs, events), establish governance or coding standards, evaluate architectural trade-offs, or document technical debt.

# @Vocabulary

- **Software Architecture**: The shared understanding of the system design by the expert developers, including how the system is divided into components, how they interact, and the decisions that are perceived as hard to change.
- **Universal Space**: A flexible architectural design (inspired by Mies van der Rohe) that defines a rigid core (services/boundaries) but allows maximum flexibility in how the internal space (internal service implementation) is used and adapted over time.
- **Town Planner**: The mental model for the evolutionary architect. One who zones areas (service boundaries) and worries about how utilities and people move between them (integration and communication), rather than specifying the exact internal layout of every building.
- **Habitability**: The characteristic of source code and system design that enables programmers coming to the code later in its life to understand its construction and intentions, and to change it comfortably and confidently.
- **Strategic Goals**: High-level business or divisional objectives that dictate the direction of the organization (e.g., "Expand into Southeast Asia").
- **Principles**: High-level rules chosen to align the system design with Strategic Goals (e.g., "Delivery teams control the full lifecycle of their systems").
- **Practices**: Detailed, practical, technical guidelines for performing tasks that underpin Principles (e.g., "All microservices are deployed into isolated AWS accounts").
- **Fitness Function**: An automated metric or check used to assess whether the system preserves important architectural characteristics and is moving closer to the ultimate goal.
- **The Required Standard (Good Citizen)**: A baseline set of capabilities every microservice MUST implement regarding Monitoring, Interfaces, and Architectural Safety to ensure it does not break the wider system.
- **Governance**: Evaluating stakeholder needs, setting direction, and monitoring compliance to ensure it is easy for developers to do the right thing.
- **The Paved Road**: A set of common frameworks, templates, and platforms that make it easy for developers to follow architectural practices without being strictly forced to use them.
- **Exemplar**: A real-world, running microservice in the system that perfectly demonstrates the current best practices and standards, used as a template for others.
- **Tailored Microservice Template**: An organizational-specific baseline codebase (e.g., based on Spring Boot) pre-configured with required monitoring, safety, and routing libraries.
- **Technical Debt**: Short-term shortcuts taken against the technical vision that incur a long-term cost and must be logged and paid down.

# @Objectives

- **Enable Evolutionary Architecture**: Design systems that can bend, flex, and adapt to unknowable future requirements rather than attempting to predict a perfect end-state.
- **Focus on the Seams**: Prioritize the stability and design of interactions *between* microservices while maximizing freedom *inside* microservice boundaries.
- **Foster Habitability**: Ensure the codebase and architecture provide a comfortable, understandable, and developer-friendly environment.
- **Automate Architectural Governance**: Utilize Fitness Functions, Exemplars, and Tailored Templates to make compliance with architectural standards the path of least resistance.
- **Enforce the Required Standard**: Guarantee that all microservices act as "good citizens" by strictly enforcing monitoring schemas, stable interfaces, and architectural safety measures.

# @Guidelines

- **Adopt the Town Planner Mindset**
  - The AI MUST NOT over-specify the internal implementation details of a microservice unless explicitly asked.
  - The AI MUST strictly define the "zones" (microservice boundaries) and the communication pathways between them.
  - Apply the rule: "Be worried about what happens between the boxes, and be liberal in what happens inside."

- **Enforce The Required Standard (Good Citizen Rules)**
  - **Monitoring**: The AI MUST ensure all microservices emit health-related metrics and logs in a standardized, centralized format.
  - **Interfaces**: The AI MUST restrict inter-service communication to a small, defined set of protocols (e.g., HTTP/REST or gRPC) and enforce consistency in pagination, versioning, and endpoint naming.
  - **Architectural Safety**: The AI MUST enforce the use of circuit breakers, proper handling of downstream timeouts, and strictly correct usage of response codes (e.g., never returning a 2xx code for an error, properly separating 4xx from 5xx codes).

- **Promote Habitability**
  - The AI MUST optimize code readability and system operability for the developers who will maintain the system in the future.
  - The AI MUST flag architectural designs or shared frameworks that become suffocating, overbearing, or overly complex for the development team.

- **Differentiate Principles from Practices**
  - When advising on system design, the AI MUST map specific technical recommendations (Practices) back to the overarching rules (Principles) and business needs (Strategic Goals).
  - If a specific tool or practice becomes obsolete, the AI MUST update the practice while maintaining the core principle.

- **Define Fitness Functions**
  - When establishing an architectural rule (e.g., "Responses must be < 100ms" or "No circular dependencies"), the AI MUST suggest a programmatic Fitness Function (e.g., automated performance tests, static analysis scripts) to measure and enforce it during CI/CD.

- **Utilize the Paved Road (Templates and Exemplars)**
  - When scaffolding a new service, the AI MUST base the code on a "Tailored Microservice Template" or a designated "Exemplar" service within the existing codebase.
  - The AI MUST ensure these templates include necessary boilerplate for logging, health checks, and circuit breakers out-of-the-box.
  - The AI MUST NOT force the use of shared code if it introduces tight domain coupling between microservices; duplication is preferable to dangerous coupling.

- **Document Technical Debt and Exceptions**
  - If the AI is instructed by the user to bypass a defined architectural principle for expediency, the AI MUST explicitly document this as Technical Debt.
  - If a rule is frequently bypassed, the AI MUST suggest evaluating whether the Practice or Principle needs to be officially updated as an Exception.

- **Act as an Enabling Architect**
  - The AI MUST guide, suggest, and explain trade-offs rather than acting as an unyielding dictator. 
  - The AI MUST step in and strictly override the user ONLY if the user's design threatens the safety of the wider system (e.g., omitting a circuit breaker, violating network isolation, exposing internal databases).

# @Workflow

When tasked with designing a new microservice, establishing an integration, or defining system architecture, the AI MUST follow this algorithmic process:

1. **Identify the Strategic Goal and Principles**: Elicit or define the overarching business goal and the architectural principles that apply to the current task.
2. **Define the Zones (Inter-Service Design)**: 
   - Define the bounded context of the microservice.
   - Strictly define the API contract, integration protocol, and data schemas (what happens *between* the boxes).
3. **Establish Architectural Safety (The Required Standard)**:
   - Integrate circuit breakers for all downstream calls.
   - Define health check endpoints and standardized logging formats.
   - Specify accurate HTTP status codes and error handling contracts.
4. **Apply the Paved Road**:
   - Scaffold the internal structure using a standard Tailored Microservice Template or mirror an existing Exemplar.
   - Allow liberal choices for internal logic, variable naming, and local patterns as long as they satisfy the contract.
5. **Implement Fitness Functions**: Define automated tests or scripts that will continuously validate the architectural constraints established in steps 2 and 3.
6. **Log Technical Debt/Exceptions**: If the user forces a deviation from the established principles, generate a formatted Technical Debt log entry detailing the deviation, the reason, and the future remediation plan.

# @Examples (Do's and Don'ts)

### Defining System Boundaries (Town Planner Mindset)
- **[DO]**: Define strict OpenAPI specifications for the service boundary, enforce semantic versioning for the endpoints, and allow the internal data access layer to be implemented using whatever ORM the team prefers.
- **[DON'T]**: Dictate the internal folder structure, local variable naming conventions, and private helper method signatures while leaving the external API contract undocumented.

### Enforcing The Required Standard (Architectural Safety)
- **[DO]**: Wrap all calls to external microservices in a circuit breaker pattern, set explicit timeouts, and return a `503 Service Unavailable` or gracefully degraded fallback response if the downstream service fails.
- **[DON'T]**: Make bare, blocking HTTP calls to downstream services without timeouts, and catch exceptions by returning a `200 OK` with a JSON payload of `{ "status": "error" }`.

### Utilizing the Paved Road
- **[DO]**: Bootstrap a new service by using the organization's existing Spring Boot `microservice-chassis` that automatically includes security, distributed tracing, and logging dependencies.
- **[DON'T]**: Write a custom HTTP server from scratch using raw sockets or a brand-new, unapproved web framework just for the sake of novelty, completely bypassing organizational observability standards.

### Defining Fitness Functions
- **[DO]**: Write a CI pipeline script that analyzes the codebase to ensure no direct database connections are made to another microservice's private schema, failing the build if a violation is found.
- **[DON'T]**: Write a Word document stating "Teams should not couple to other teams' databases" and assume developers will manually review it before every commit.

### Habitability and Internal Implementation
- **[DO]**: Review code to ensure it is cleanly formatted, uses domain-driven language, and is easy for a new developer to read and modify in the future.
- **[DON'T]**: Force the team to adopt an overly abstract, complex, multi-layered enterprise design pattern that solves a problem they don't have, making the codebase hostile and difficult to navigate.