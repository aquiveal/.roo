@Domain
This rule file activates when the AI is assisting with the architectural design, refactoring, performance tuning, capacity planning, database selection, or infrastructure configuration of microservices. It is specifically triggered by user requests related to handling increased traffic, scaling a service, optimizing task processing, reducing latency, allocating hardware resources, or evaluating programming languages and datastores for microservice architecture.

@Vocabulary
- **Concurrency**: The architectural principle of breaking a task up into smaller pieces to avoid a single process executing all work sequentially.
- **Partitioning**: The architectural principle of processing the smaller pieces of concurrent tasks in parallel using a distributed set of workers.
- **Qualitative Growth Scale**: A high-level, non-technical measure of how a service scales, tied to business metrics (e.g., scales with "eyeballs", "user signups", "orders placed"). For internal tools, this scales with "number of deployments", "services", or "gigabytes of logs".
- **Quantitative Growth Scale**: The mathematical translation of the Qualitative Growth Scale into measurable technical metrics (e.g., Requests Per Second [RPS], Queries Per Second [QPS], Transactions Per Second [TPS]).
- **Horizontal Scaling**: Adding more individual instances/servers to handle increased traffic (the required scaling method for microservices).
- **Vertical Scaling**: Increasing the physical resources (CPU, RAM) of a single host to handle increased traffic (an anti-pattern in microservice architecture).
- **Resource Requirements**: The exact hardware resources (CPU, RAM, threads, file descriptors, database connections) required to run exactly *one* instance of a microservice.
- **Resource Bottlenecks**: Inherent limitations in how a microservice utilizes resources that prevent horizontal scaling (e.g., reaching maximum database connections).
- **Resource Abstraction**: Technologies (like Apache Mesos) that treat hardware as a fluid pool of resources rather than individual physical hosts.
- **Test Tenancy**: The practice of securely handling test data in shared or production databases by clearly marking it as test data and routinely deleting it.

@Objectives
- Ensure the microservice scales horizontally through strict adherence to concurrency and partitioning.
- Map high-level business goals to specific technical capacity requirements using Qualitative and Quantitative Growth Scales.
- Prevent resource starvation by accurately calculating single-instance Resource Requirements and eliminating Vertical Scaling anti-patterns.
- Optimize task processing efficiency by enforcing the use of appropriate programming languages and asynchronous frameworks.
- Select and configure data storage solutions based strictly on TPS, consistency requirements, read/write ratios, and horizontal scalability needs.
- Protect shared databases by explicitly managing connections and implementing test tenancy.

@Guidelines

**Growth Scales & Capacity Planning**
- The AI MUST define both the Qualitative Growth Scale and Quantitative Growth Scale before making any scaling recommendations.
- When generating capacity plans, the AI MUST calculate future hardware needs by linking high-level business growth predictions (Qualitative) to RPS/QPS increases (Quantitative).
- The AI MUST incorporate hardware acquisition "lead times" into any generated capacity planning schedules to prevent resource shortages.

**Resource Management & Bottlenecks**
- The AI MUST define Resource Requirements based exclusively on the needs of a *single* instance of the microservice.
- The AI MUST flag Vertical Scaling as a severe anti-pattern. If a service requires more CPU/RAM per host to scale, the AI MUST recommend refactoring the architecture to support Concurrency and Partitioning.
- If a service shares hardware with other services, the AI MUST enforce containerization (e.g., Docker) and resource isolation to prevent "bad neighbor" resource starvation.
- The AI MUST monitor for non-standard resource requirements, such as file descriptor limits, logging quotas, and database connection limits, identifying them as potential Resource Bottlenecks.

**Dependencies & Traffic Management**
- The AI MUST remind the user that a microservice's scalability is limited by its dependencies. Any planned capacity increase MUST include a step to notify upstream clients and downstream dependencies.
- The AI MUST recommend scheduling deployments, routine maintenance, and operational downtimes strictly during known low-traffic periods.
- The AI MUST architect the service to handle traffic spikes gracefully, recommending multi-datacenter deployment and automated cross-datacenter traffic rerouting in the event of localized failures.

**Task Handling & Language Choice**
- The AI MUST evaluate the programming language's native ability to handle concurrency and partitioning.
- If a service is built in a language with known scalability limitations (e.g., synchronous Python) and is experiencing bottlenecks, the AI MUST suggest adopting asynchronous frameworks (e.g., Tornado, Celery + RabbitMQ/Redis) or rewriting the service in a language optimized for concurrency (e.g., Go, Java, C++).
- The AI MUST NOT allow tasks to be processed by a single, monolithic, synchronous process.

**Data Storage & Databases**
- The AI MUST evaluate database choices based on the following strict criteria: Transactions Per Second (TPS), schema flexibility, strong vs. eventual consistency, read/write heaviness, and horizontal scalability.
- If the service requires horizontal database scaling or parallel reads and writes, the AI MUST recommend a NoSQL database (e.g., Cassandra, MongoDB, Dynamo) over a Relational Database (SQL).
- The AI MUST enforce the explicit closing of database connections in the code to prevent connection limit bottlenecks.
- If the microservice uses a shared database, the AI MUST implement Test Tenancy (tagging all data generated by staging/load tests as test data and implementing automated deletion scripts).

@Workflow
When tasked with designing, reviewing, or optimizing a microservice for scalability and performance, the AI MUST execute the following steps in order:

1. **Define Growth Scales**: Ask the user for the business metric the service scales with (Qualitative) and convert it to technical metrics like RPS/QPS (Quantitative).
2. **Determine Single-Instance Requirements**: Calculate the CPU, RAM, threads, and DB connections needed for one isolated instance of the service.
3. **Identify Bottlenecks**: Analyze the architecture for Vertical Scaling requirements, single-process execution flows, or hard limits (e.g., max DB connections). Refactor to eliminate them.
4. **Evaluate Processing Efficiency**: Review the programming language and frameworks. Ensure tasks are handled concurrently and partitioned across parallel workers.
5. **Architect Data Storage**: Select the datastore based on read/write patterns and horizontal scaling needs. Implement connection pooling/closing and Test Tenancy.
6. **Plan Ecosystem Integration**: Draft a plan to communicate traffic growth to dependency owners and configure multi-datacenter traffic rerouting.

@Examples (Do's and Don'ts)

**Scaling Strategy**
- [DO]: Scale the microservice by adding more instances of the application behind a load balancer (Horizontal Scaling), ensuring tasks are partitioned across the new instances.
- [DON'T]: Scale the microservice by requesting a server upgrade from 16GB of RAM to 64GB of RAM to handle a larger in-memory queue (Vertical Scaling).

**Task Processing**
- [DO]: Break an incoming video processing request into chunks, dispatch them to a distributed Celery worker queue, and process them in parallel.
- [DON'T]: Accept an incoming request and execute steps A, B, and C sequentially in a single blocking thread before returning a response.

**Database Connections**
- [DO]: Use a connection pool with strictly enforced timeouts, ensuring every `open()` has a corresponding `finally { close() }` block to prevent exhausting database resources.
- [DON'T]: Open a database connection globally per instance and leave it open indefinitely while waiting for incoming traffic.

**Growth Scale Definition**
- [DO]: Document the scale as: "Qualitative: Scales with user sign-ups. Quantitative: 1 user signup = 5 RPS to the profile-service and 2 TPS to the database."
- [DON'T]: Document the scale simply as: "The service currently handles 500 RPS."

**Handling Test Data in Shared Databases**
- [DO]: Append a `tenant_id: "test"` flag to all records generated by staging environments and run a cron job to purge these records every 24 hours.
- [DON'T]: Write test data directly into production tables without identifiers, risking corruption of real-world business metrics.