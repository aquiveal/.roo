# @Domain
Trigger these rules when executing tasks related to system architecture design, microservice boundary definition, cross-service communication planning, technical governance, implementing "paved road" templates, defining fitness functions, or making trade-offs regarding technical debt and system evolution.

# @Vocabulary
- **Evolutionary Architecture**: An architecture designed to accommodate and facilitate constant change and evolution rather than a rigid, static end-state.
- **Town Planner Model**: An architectural approach where the architect defines broad zones and communication pathways (inter-service boundaries) but leaves specific building details (intra-service implementations) to the teams.
- **Habitability**: The characteristic of a codebase or system that makes it easy, comfortable, and confident for developers to understand and modify later in its life.
- **Strategic Goals**: High-level business directions that technology must align with.
- **Principles**: High-level rules (ideally fewer than 10) that align system design with strategic goals (e.g., "deploy independently").
- **Practices**: Detailed, practical, and technology-specific guidelines for performing tasks that underpin principles (e.g., "use HTTP/REST").
- **Fitness Functions**: Automated checks or metrics used to assess whether the architecture preserves important characteristics (e.g., performance thresholds, coupling limits) as it evolves.
- **Good Citizen Microservice**: A microservice that follows required standards for monitoring, interfaces, and architectural safety to ensure it does not compromise the wider system.
- **Governance**: The process of agreeing on how things should be done, setting direction, and ensuring the system matches the technical vision.
- **The Paved Road**: A platform or set of tools that makes doing the "right thing" the easiest option, without strictly mandating its use.
- **Exemplars**: Real-world, running microservices used as templates or reference points to demonstrate best practices to developers.
- **Tailored Microservice Template**: A pre-configured boilerplate (e.g., Spring Boot with predefined circuit breakers and JWT handling) provided by platform teams to accelerate development safely.

# @Objectives
- Treat software architecture as a continually evolving shape rather than a fixed construction plan.
- Act as a "Town Planner," prioritizing strict governance over inter-service communication while maximizing developer autonomy within individual microservices.
- Ensure all microservices act as "Good Citizens" by enforcing standardized monitoring, robust architectural safety, and consistent interface paradigms.
- Foster "Habitability" by prioritizing developer experience, readability, and ease of modification in all architectural and code-level decisions.
- Support decentralized decision-making by creating "Paved Roads" and providing "Exemplars" rather than rigid, mandatory frameworks.

# @Guidelines

## The Town Planner Approach
- The AI MUST restrict rigid architectural rules to interactions *between* microservices (APIs, network protocols, data exchange formats).
- The AI MUST permit and encourage technical flexibility and autonomy *inside* microservice boundaries (internal code structure, local data storage, language choice).
- When defining boundaries, the AI MUST group related concepts into "zones" (bounded contexts) and focus optimization efforts on the communication between these zones.

## Ensuring "Good Citizen" Microservices
- **Monitoring Standardization:** The AI MUST ensure every generated microservice emits health and monitoring metrics in a standardized format and centralizes its logs.
- **Interface Consistency:** The AI MUST enforce a small, defined set of interface technologies (e.g., HTTP/REST using standard verbs and nouns, or gRPC) across the system.
- **Architectural Safety:** The AI MUST implement fault-tolerance mechanisms on all synchronous downstream calls. This includes mandatory timeouts, retries (where idempotent), and circuit breakers.
- **Strict Protocol Adherence:** The AI MUST enforce strict adherence to underlying protocol rules (e.g., returning proper 4xx vs. 5xx HTTP status codes) so that circuit breakers and monitoring systems function correctly.

## Guiding Evolution via Principles and Practices
- When proposing technical solutions, the AI MUST explicitly link the implementation (the Practice) to the overarching goal (the Principle).
- The AI MUST document any intentional deviation from established principles as an "Exception" and explicitly flag it as Technical Debt with a proposed tracking mechanism.

## Fitness Functions
- The AI MUST define automated "Fitness Functions" for critical architectural characteristics. When designing a system, the AI MUST propose how to measure its success (e.g., automated load tests checking if response time remains < 100ms).

## Governance and Habitability
- The AI MUST prioritize solutions that create a "Habitable" environment—code and architectures that are easy for future developers to navigate and modify.
- When establishing patterns, the AI MUST recommend the "Paved Road" approach: providing optional but highly convenient tailored microservice templates or exemplars, rather than enforcing the use of bloated, mandatory central frameworks.

# @Workflow
1. **Identify the Strategic Goal:** Begin by asking for or defining the underlying business or strategic goal driving the architectural change.
2. **Establish Principles and Practices:** Define the architectural principles relevant to the task, followed by the specific technical practices that will fulfill them.
3. **Map the Zones (Town Planning):** Define the system boundaries. Heavily specify the cross-service contracts (APIs, events) and leave the internal implementation details loosely coupled and flexible.
4. **Enforce Good Citizenship:** Scaffold the microservice architecture to include required monitoring, standardized interfaces, and architectural safety (circuit breakers/timeouts).
5. **Define Fitness Functions:** Create automated metrics or test conditions to continuously evaluate whether the architecture maintains its desired state.
6. **Pave the Road:** Generate "Exemplars" or tailored templates that encapsulate these best practices, making it easier for human developers to adopt the pattern voluntarily.
7. **Log Exceptions:** If a compromise or shortcut is necessary, explicitly log it as Technical Debt and define the conditions under which it should be repaid or codified as a new practice.

# @Examples (Do's and Don'ts)

## Town Planner Boundaries
- **[DO]**: Define a strict OpenAPI specification for how the `Recommendation` service talks to the `Sales` service, but allow the `Recommendation` service team to choose their own internal folder structure and local database.
- **[DON'T]**: Mandate that every microservice across the entire organization must use the exact same internal object-relational mapping (ORM) library or internal directory layout.

## Architectural Safety & Protocol Adherence
- **[DO]**: Return a `503 Service Unavailable` or `504 Gateway Timeout` when a downstream database fails, allowing upstream circuit breakers to trip appropriately. Wrap downstream network calls in a circuit breaker pattern.
- **[DON'T]**: Catch a database connection error and return a `200 OK` with a JSON payload of `{ "error": "database down" }`. (This prevents safety mechanisms from recognizing the failure).

## The Paved Road vs. Ivory Tower
- **[DO]**: Provide a lightweight, pre-configured `Spring Boot` or `Express.js` template that automatically includes JWT validation, centralized logging configurations, and health-check endpoints for developers to clone and modify.
- **[DON'T]**: Force all teams to inherit their services from a massive, centrally controlled, monolithic base class or library that cannot be updated without a lockstep release across the organization.

## Fitness Functions
- **[DO]**: Implement a CI pipeline step that fails the build if the new microservice exceeds a defined maximum acceptable latency under simulated load, or if cyclic dependencies between services are detected.
- **[DON'T]**: Rely solely on a manual review board of external architects to determine if a service is "fast enough" or "decoupled enough" right before production deployment.