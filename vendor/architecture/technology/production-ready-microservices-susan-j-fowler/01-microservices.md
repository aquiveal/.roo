@Domain
Trigger these rules when tasked with designing, architecting, extracting, or refactoring microservices, transitioning from monolithic applications to distributed systems, defining API endpoints, configuring inter-service communication, or organizing microservice repositories and ecosystem infrastructure.

@Vocabulary
- **Three-Tier Architecture**: The baseline architectural pattern comprising a frontend (client-side), backend, and datastore.
- **Monolith**: A software application where all features, functions, and codebase elements are contained and deployed as one executable file, making concurrency and partitioning difficult.
- **Microservice**: A small, autonomous, independently developed, and independently deployable application responsible for performing exactly one function.
- **Concurrency**: The ability to break tasks into smaller pieces to process them efficiently.
- **Partitioning**: The ability to process divided tasks in parallel (e.g., using a set of workers).
- **RPC (Remote Procedure Call)**: Network calls designed to look and behave like local procedure calls used for microservice interaction.
- **Publish-Subscribe (Pubsub)**: An asynchronous messaging model where clients subscribe to a topic and receive messages published to that topic.
- **Request-Response Messaging**: An asynchronous messaging model where a client sends a request to a message broker and awaits a response.
- **Service Discovery**: Infrastructure (e.g., etcd, Consul, ZooKeeper) that tracks dynamic IP addresses and ports to route requests only to healthy microservice instances.
- **Service Registry**: The database underlying service discovery that tracks all ports and IPs of microservices.
- **Microservice Ecosystem**: The four-layered environment (Hardware, Communication, Application Platform, Microservices) required to run distributed services.
- **Inverse Conway’s Law**: The principle that the organizational structure of a company is determined by the architecture of its product (resulting in isolated, specialized microservice teams).
- **Technical Sprawl**: The anti-pattern of having hundreds of unstandardized ways to perform operations, deploy, or write code (especially language sprawl).
- **Black Box**: The paradigm of treating a microservice purely in terms of its inputs (requests to endpoints) and outputs (responses), without needing to know its internal workings.

@Objectives
- Architect applications for extreme horizontal scalability by prioritizing concurrency and partitioning.
- Ensure strict isolation of boundaries so that each microservice performs only one designated function.
- Abstract microservices away from low-level infrastructure (hardware, networks, deployment pipelines).
- Prevent technical sprawl by standardizing endpoints, logging, and limiting programming language choices.
- Eliminate dependency on static IPs and ports by enforcing the use of service discovery and dynamic routing.
- Maintain microservices as living, changing entities by strictly forbidding the versioning of microservices or their API endpoints.

@Guidelines

**Monolith to Microservice Extraction**
- When extracting microservices from a monolith, the AI MUST identify and pinpoint key overall functionalities and isolate them into simple, independent components.
- When planning migration, the AI MUST propose either shadowing the monolith’s traffic with the new service or building from scratch and redirecting traffic only after testing.
- The AI MUST NOT recommend adopting microservice architecture for early-stage companies lacking dedicated infrastructure and operational capacity.

**Microservice Architecture & Endpoints**
- When defining a microservice, the AI MUST structure it with three distinct elements: an API frontend (static endpoints), a backend processing unit, and localized data storage/retrieval.
- When generating API endpoints, the AI MUST standardise communication using either REST or Apache Thrift protocols over HTTP.
- When naming or structuring API endpoints, the AI MUST NOT version the microservice or its endpoints (e.g., avoid `/v1/`, `/v2/`). Treat the service as a living, continuously changing entity.
- When interacting with other services, the AI MUST implement interactions strictly via RPCs or standardized messaging, treating external services entirely as black boxes.

**Ecosystem Abstraction (The 4 Layers)**
- When configuring infrastructure, the AI MUST clearly separate concerns across the 4 layers: Hardware (Layer 1), Communication (Layer 2), Application Platform (Layer 3), and Microservices (Layer 4).
- When configuring hardware or OS resources, the AI MUST assume the use of resource isolation/abstraction (e.g., Docker, Apache Mesos) and configuration management (e.g., Ansible, Chef, Puppet).
- When configuring service communication, the AI MUST NOT use static IP addresses or hardcoded ports. The AI MUST utilize Service Discovery (e.g., Consul, etcd) and Load Balancing.
- When implementing messaging (Kafka, Celery/Redis, RabbitMQ), the AI MUST implement explicit safeguards against race conditions and endless loops.
- When handling microservice-specific configurations, the AI MUST store these configurations directly within the microservice's own repository (Layer 4), NOT in centralized deployment or platform repositories (Layer 3).

**Mitigating Organizational Challenges & Sprawl**
- When selecting languages or frameworks for a microservice, the AI MUST restrict choices to a small, predefined list of supported languages within the organization to prevent language sprawl.
- When generating operational logic, the AI MUST embed logging, monitoring, and on-call operational metrics directly into the service, as developers (not a separate Ops team) will be responsible for operating the microservice.
- When architecting communication, the AI MUST design synchronous systems (HTTP+REST) for simplicity and reliability, or asynchronous systems (Messaging) only when high scalability is explicitly required and broker bottlenecks are mitigated.

@Workflow
1. **Scope the Microservice**: Define the *single* key functionality the microservice will handle. Ensure it processes tasks efficiently through concurrency and partitioning.
2. **Define the Interface**: Create static API endpoints (REST or Thrift) to act as the client-side frontend. Ensure no versioning numbers are present in the interface paths.
3. **Design the Communication**: Establish whether the service will communicate synchronously (HTTP/RPC) or asynchronously (Pubsub/Request-Response Messaging). If async, add code to mitigate race conditions.
4. **Abstract the Infrastructure**: Implement service discovery clients. Remove any hardcoded IPs or static ports. Ensure the service can dynamically register itself.
5. **Localize Configuration**: Create the configuration files (e.g., `.yaml`, `.json`) and place them strictly within the microservice's local repository.
6. **Implement Operations**: Add microservice-level logging and monitoring hooks, assuming the development team will be solely responsible for on-call operations.

@Examples (Do's and Don'ts)

**Versioning API Endpoints**
- [DO]: `/api/users/get_customer_information`
- [DON'T]: `/api/v1/users/get_customer_information` or pinning client services to specific static releases of a microservice.

**Configuration Management**
- [DO]: Store custom deployment configurations and environment variables inside the microservice repository (e.g., `user-service/deploy-config.yaml`).
- [DON'T]: Centralize application configurations in the infrastructure/deployment tool repository (e.g., `jenkins-repo/configs/user-service-config.yaml`).

**Service Communication & Discovery**
- [DO]: Use service discovery to resolve endpoints dynamically: `request(ServiceDiscovery.resolve('customer-service') + '/get_customer_information')`.
- [DON'T]: Hardcode static IPs or ports for inter-service communication: `request('http://10.0.1.54:8080/get_customer_information')`.

**Scaling Methodology**
- [DO]: Architect tasks to be broken down and processed in parallel by multiple stateless workers (Partitioning and Concurrency).
- [DON'T]: Build a single large process that handles a complex task sequentially from start to finish.