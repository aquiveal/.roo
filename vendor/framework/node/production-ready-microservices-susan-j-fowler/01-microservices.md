@Domain
This rule file MUST be triggered when the AI is tasked with designing, architecting, evaluating, migrating, or refactoring microservice architectures. It applies to requests involving splitting monolithic applications, designing distributed system infrastructure, structuring microservice repositories, defining API endpoints, configuring communication protocols (RPCs/messaging), or establishing organizational engineering standards for distributed systems.

@Vocabulary
- **Three-Tier Architecture**: The baseline software structure consisting of a frontend (client-side), backend (heavy lifting), and datastore.
- **Monolith**: An application where all features, functions, and client/backend code are contained within one codebase and deployed as a single executable, scaling only vertically or by duplicating the entire app horizontally.
- **Concurrency**: Breaking a task into smaller pieces to process it efficiently.
- **Partitioning**: Processing the smaller pieces of a task in parallel across multiple workers.
- **Microservice**: A small, autonomous, independent, and self-contained application that performs exactly one function and does it well.
- **Remote Procedure Call (RPC)**: Calls over a network designed to look and behave exactly like local procedure calls, used for inter-service communication.
- **Microservice Ecosystem**: The environment comprising four distinct layers (Hardware, Communication, Application Platform, Microservices) required to sustain microservice architecture.
- **Service Discovery**: Infrastructure (e.g., etcd, Consul) that dynamically tracks healthy IPs and ports of microservices for routing requests.
- **Service Registry**: A database that tracks all ports and IPs of all microservices.
- **Inverse Conway’s Law**: The principle that the organizational structure of a company is determined by the architecture of its product (e.g., isolated microservices necessitate small, isolated, independent development teams).
- **Technical Sprawl**: The anti-pattern where organizational isolation leads to a fragmented ecosystem of disparate tools, languages, and deployment mechanisms.

@Objectives
- Transform monolithic, coupled logic into isolated, single-responsibility microservices optimized for concurrency and partitioning.
- Abstract microservices completely from underlying infrastructure layers (hardware, network, build pipelines).
- Prevent technical sprawl by enforcing strict standardization of API endpoints, communication protocols, and supported programming languages.
- Ensure that configuration, communication, and deployment paradigms are resilient, highly available, and capable of operating in a constantly changing ecosystem.

@Guidelines
- **Monolith to Microservice Migration:**
  - When advising on splitting a monolith, the AI MUST explicitly identify key overall functionalities and componentize them into independent services.
  - The AI MUST warn against adopting microservices for very small or early-stage companies lacking a dedicated infrastructure organization.
- **Microservice Layering & Abstraction:**
  - The AI MUST structure architectures strictly according to the Four-Layer Model:
    1. **Hardware Layer**: Bare metal/cloud servers, OS, resource isolation (Docker/Mesos), configuration management (Ansible/Chef/Puppet), and host-level monitoring.
    2. **Communication Layer**: Network, DNS, RPCs, API endpoints, messaging (Kafka/Celery/Redis), service discovery, service registry, and load balancing.
    3. **Application Platform Layer**: Internal self-service tools, development environments mirroring production, CI/CD pipelines, and microservice-level logging/monitoring.
    4. **Microservice Layer**: The microservices themselves and *only* their service-specific configurations.
- **API and Communication Standards:**
  - The AI MUST standardize API endpoint types across the ecosystem (e.g., strictly REST or strictly Apache Thrift). Do not mix endpoint types arbitrarily.
  - When implementing asynchronous messaging (pubsub or request-response), the AI MUST implement structural protections against race conditions and endless loops.
- **Anti-Versioning Rule (CRITICAL):**
  - The AI MUST NEVER version microservices or API endpoints (e.g., do not use `/api/v1/` or label dependencies with static versions). Microservices must be treated as living, evolving entities; versioning creates organizational nightmares and fragile pins.
- **Configuration Management:**
  - The AI MUST place microservice-specific configurations inside the microservice's own repository. Do NOT store application-specific configs centrally in deployment or infrastructure tool codebases.
  - The AI MUST NOT allow microservice application code to alter system-level or infrastructure-level configurations.
- **Technical Sprawl Prevention:**
  - When selecting programming languages or tools, the AI MUST constrain choices to a small, pre-defined set of supported languages to avoid the impossibility of maintaining multi-language libraries.
- **Operational Responsibility:**
  - The AI MUST design the system assuming the microservice developers are fully responsible for the operational duties (on-call, monitoring) of their service. Operations are not thrown over the wall.

@Workflow
1. **Assessment & Capacity Check**: Evaluate if the target system is mature enough for microservices. If it is a young startup without infrastructure teams, recommend against microservices.
2. **Componentization Definition**: Identify the single, explicit business function the microservice will perform. Break down concurrent and parallel partitioned tasks.
3. **Layer Separation**: 
   - Assign infrastructure logic (load balancing, discovery) to the Communication Layer.
   - Assign deployment/CI logic to the Application Platform Layer.
   - Restrict the microservice codebase solely to business logic and service-specific configurations.
4. **Endpoint & Communication Design**: Define the API using a standardized protocol (HTTP+REST or Thrift). Exclude all versioning from the URL and payload structures. Define RPC or messaging patterns, adding fail-safes for async loops.
5. **Configuration Localization**: Generate configurations (e.g., YAML, JSON) and place them directly in the root of the microservice workspace, ensuring no bleed-over into Layer 1, 2, or 3 tools.

@Examples (Do's and Don'ts)

**[DO] API Endpoint Definition (No Versioning)**
```python
# The AI generates a standard, unversioned REST endpoint for a single-responsibility service.
@app.route('/customers', methods=['GET'])
def get_customer_information():
    # Retrieves customer information treating the service as a living application
    pass
```

**[DON'T] API Endpoint Definition (Anti-Pattern: Versioning)**
```python
# The AI MUST NOT generate versioned endpoints. This pins clients to outdated versions.
@app.route('/api/v1/customers', methods=['GET'])
def get_customer_information_v1():
    pass
```

**[DO] Configuration Localization**
```text
# Directory structure generated by AI keeps specific configs IN the microservice repo
/customer-service
  /src
    app.py
  /config
    production.yaml  <-- Microservice-specific configs live here
  Dockerfile
```

**[DON'T] Configuration Localization (Anti-Pattern: Centralized App Configs)**
```text
# The AI MUST NOT put microservice configs in the infrastructure deployment repository
/ansible-deployment-repo
  /playbooks
  /vars
    customer-service-config.yaml <-- Wrong! Developer will forget this exists.
    order-service-config.yaml
```

**[DO] Async Messaging with Protections**
```python
# The AI includes safeguards (like max_retries or TTL) when using messaging to prevent endless loops.
@celery.task(bind=True, max_retries=3)
def process_data(self, data):
    try:
        perform_task(data)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

**[DON'T] Async Messaging without Protections**
```python
# The AI MUST NOT create unbounded async message processing.
@celery.task
def process_data(data):
    try:
        perform_task(data)
    except Exception:
        # Endless loop waiting to happen, risking queuing failure
        publish_message_to_queue(data)
```