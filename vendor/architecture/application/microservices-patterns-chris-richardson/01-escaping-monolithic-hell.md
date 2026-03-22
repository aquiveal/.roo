# @Domain
These rules MUST be triggered when the AI is tasked with analyzing software architecture, migrating legacy systems, assessing system scalability, decomposing applications into modules/services, designing interprocess communication or database schemas for distributed systems, or establishing DevOps, CI/CD, and team structures for software delivery.

# @Vocabulary
- **Monolithic Hell**: A state where a successful, monolithic application outgrows its architecture, resulting in overwhelming complexity, slow development, difficult deployment, poor scaling, lack of reliability, and lock-in to obsolete technology stacks.
- **Scale Cube**: A three-dimensional model for scaling an application:
  - **X-axis scaling**: Load balancing requests across multiple identical instances (cloning).
  - **Z-axis scaling**: Routing requests based on a request attribute to instances responsible for a subset of data (partitioning/sharding).
  - **Y-axis scaling**: Functionally decomposing an application into narrowly focused services (microservices).
- **Microservice Architecture**: An architectural style that applies Y-axis scaling to functionally decompose an application into a set of loosely coupled, independently deployable services, each with its own database.
- **Distributed Monolith**: An anti-pattern consisting of tightly coupled services that must be developed and deployed together, inheriting the drawbacks of both monoliths and microservices.
- **SOA (Service-Oriented Architecture)**: A legacy architectural style that integrates large monolithic applications using "smart pipes" (Enterprise Service Bus/ESB), heavyweight protocols (SOAP/WS*), and a shared global data model. Distinct from microservices.
- **Pattern**: A reusable, objective solution to a problem in a specific context. It includes:
  - **Forces**: Competing issues that must be addressed/prioritized.
  - **Resulting Context**: The consequences of applying the pattern (Benefits, Drawbacks, and new Issues).
  - **Related Patterns**: Other patterns related by relationship types (Predecessor, Successor, Alternative, Generalization, Specialization).
- **Continuous Delivery/Deployment**: DevOps practices ensuring software is always releasable and rapidly, safely deployed to production.
- **Reverse Conway Maneuver**: Designing an organization's communication structures (small, autonomous teams) to deliberately mirror the desired loosely coupled software architecture.
- **Transition Model**: The three-stage emotional process humans undergo during change (Ending/Losing/Letting Go, The Neutral Zone, The New Beginning).

# @Objectives
- Evaluate systems to determine if they are in "monolithic hell" and require modernization, or if they are simple enough to remain as monoliths.
- Apply the Scale Cube to prescribe the exact dimension of scaling required for capacity, data, or complexity issues.
- Enforce strict encapsulation and modularity by designing microservices as completely independent units with private datastores and API-only communication.
- Prevent the creation of "distributed monoliths" by ensuring services are loosely coupled and independently deployable.
- Evaluate and propose architectural solutions objectively using the formal Pattern format (Forces, Resulting Context, Related Patterns) rather than presenting any technology as a "silver bullet."
- Align architectural recommendations with team organization, deployment processes, and human emotional transitions.

# @Guidelines
- **Architecture Selection Constraints**:
  - The AI MUST NOT treat microservices as a silver bullet.
  - For startups or new, simple applications requiring rapid iteration of the business model, the AI MUST recommend the Monolithic Architecture pattern.
  - For large, complex, long-lived applications requiring high development velocity, testability, and deployability, the AI MUST recommend the Microservice Architecture pattern.
- **Scale Cube Application**:
  - When asked to scale an application, the AI MUST explicitly analyze all three axes.
  - Use X-axis for simple capacity/availability.
  - Use Z-axis for transaction/data volume scaling.
  - Use Y-axis (microservices) EXCLUSIVELY to solve increasing development complexity and team scaling issues.
- **Strict Database Isolation**:
  - The AI MUST ensure each microservice has its own private datastore. 
  - The AI MUST REJECT any design that proposes sharing a relational database schema or global data model across multiple microservices.
- **API Encapsulation**:
  - Services MUST communicate strictly via APIs. The AI MUST design communication using "dumb pipes" (e.g., message brokers, REST, gRPC).
  - The AI MUST NOT use SOA anti-patterns such as Enterprise Service Buses (ESBs) containing business logic.
- **Pattern-Based Evaluation**:
  - When proposing an architectural pattern, the AI MUST explicitly list the *Forces* involved.
  - The AI MUST explicitly state the *Resulting Context*, dividing it rigidly into Benefits, Drawbacks, and Issues (new problems introduced).
  - The AI MUST link *Related Patterns* (e.g., if Microservices are chosen, the AI must explicitly identify successor patterns like Service Discovery, Circuit Breaker, or Saga).
- **Organizational Alignment**:
  - The AI MUST apply the Reverse Conway Maneuver. If asked about team structure, the AI must recommend small ("two-pizza"), cross-functional, autonomous teams that perfectly map to service boundaries.
- **Change Management**:
  - When planning an architectural migration, the AI MUST factor in the human element by referencing the Transition Model, acknowledging the emotional resistance teams will face during the "Ending" and "Neutral Zone" phases.

# @Workflow
1. **Context Assessment**: Analyze the application's lifecycle stage, size, team size, and delivery velocity. Identify specific symptoms of "monolithic hell" (e.g., slow IDEs, painful merges, conflicting resource requirements, obsolete tech stacks).
2. **Scaling Strategy Formulation**: Apply the Scale Cube. Define exactly how the system will scale along the X, Z, and Y axes. If Y-axis scaling is required, proceed to microservice decomposition.
3. **Service & Data Decomposition**: Functionally decompose the application into narrowly focused services. Immediately assign a private, isolated database/data model to every defined service.
4. **Communication & API Design**: Define the boundaries. Establish lightweight, dumb-pipe communication mechanisms (REST, gRPC, message brokers) between the newly defined services.
5. **Objective Pattern Validation**: Format the proposed architecture using the Pattern Language structure. Document the Forces, detail the Resulting Context (Benefits, Drawbacks, Issues), and list Successor patterns required to make the architecture function (e.g., how to handle distributed transactions or querying).
6. **Process & Organization Mapping**: Define the automated continuous deployment pipeline requirements and restructure the development teams into small, autonomous units aligned with the new service boundaries. Formulate a transition plan for the human emotional impact.

# @Examples (Do's and Don'ts)

- **Database per Service**
  - [DO]: "We will extract the `Order Service` and the `Customer Service`. The `Order Service` will have its own private database containing the `ORDERS` table, and the `Customer Service` will have a separate database containing the `CUSTOMERS` table. They will communicate solely via REST APIs."
  - [DON'T]: "We will create an `Order Service` and a `Customer Service` that both connect to the centralized legacy Oracle database to ensure data remains consistent."

- **Pattern-Based Evaluation**
  - [DO]: "Applying the Microservice Architecture pattern. **Forces**: Need for maintainability vs network latency. **Resulting Context - Benefits**: Independent deployability, fault isolation. **Drawbacks**: Distributed system complexity. **Issues**: Requires distributed transaction management. **Successor Patterns**: We must now apply the Saga pattern to handle data consistency."
  - [DON'T]: "You should switch to microservices because it will make your application infinitely scalable and solve all your deployment problems automatically."

- **Scaling Strategies**
  - [DO]: "To handle the growing number of users, we will implement Z-axis scaling by sharding the monolith based on the `userId` attribute. To handle the overwhelming complexity of the codebase, we will apply Y-axis scaling by breaking it into distinct microservices."
  - [DON'T]: "The code is too complex to read and merges take days. We should add a load balancer and run 10 instances of the monolith."

- **Organizational Design (Conway's Law)**
  - [DO]: "We will form a cross-functional, 8-person team dedicated solely to the `Kitchen Service`. They will completely own its development, database, and deployment pipeline."
  - [DON'T]: "We will keep the centralized Database Team to manage all schemas, and the UI team will submit tickets to the Backend Team to update the microservices."

- **SOA vs Microservices**
  - [DO]: "Services will communicate using asynchronous messaging via a lightweight message broker, acting as a dumb pipe."
  - [DON'T]: "Services will be integrated using an Enterprise Service Bus (ESB) that contains message routing and business logic to orchestrate the services."