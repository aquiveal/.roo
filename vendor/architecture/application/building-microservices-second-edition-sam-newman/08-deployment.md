# @Domain

This rule file MUST trigger when the AI is instructed to perform tasks related to the deployment, provisioning, physical architecture design, or operational configuration of a microservice architecture. Activation conditions include:
- Writing or configuring Infrastructure as Code (IaC) (e.g., Terraform, Pulumi, AWS CloudFormation).
- Creating containerization configurations (e.g., Dockerfiles, docker-compose).
- Designing or writing orchestration manifests (e.g., Kubernetes Pods, Services, Deployments, Helm charts).
- Configuring Serverless or Function-as-a-Service (FaaS) deployments (e.g., AWS Lambda, Serverless Framework).
- Designing CI/CD deployment pipelines, environment promotion strategies, or release configurations.
- Implementing progressive delivery mechanisms (e.g., feature toggles, canary releases, blue-green deployments).
- Mapping logical microservice architectures to physical infrastructure and database topologies.

# @Vocabulary

- **Logical to Physical Mapping**: The translation of a conceptual microservice into concrete deployment artifacts, network routes, scaled instances, and physical database nodes.
- **Isolated Execution**: The principle of running each microservice instance in its own ring-fenced operating environment (e.g., a dedicated container or VM) to prevent resource contention and side effects.
- **Infrastructure as Code (IaC)**: The practice of representing infrastructure configuration via machine-readable code, allowing environments to be version-controlled, tested, and repeatedly provisioned.
- **Zero-Downtime Deployment**: The ability to deploy a new version of a microservice without interrupting service for consumers, often achieved via rolling upgrades or blue-green deployments.
- **Desired State Management**: Utilizing a platform (like Kubernetes or AWS Auto Scaling) where the operator defines the target infrastructure requirements, and the platform automatically maintains that state (e.g., replacing dead instances).
- **GitOps**: An operational framework combining IaC and desired state management, where the desired state is stored in Git and automated tooling (e.g., Flux) synchronizes the running system to the repository.
- **Type 2 Virtualization**: Virtualization utilizing a hypervisor over a host OS (e.g., AWS EC2, VMware). Provides strong isolation but high resource overhead.
- **Containers**: Lightweight virtualized environments sharing the host OS kernel (e.g., Docker). Provides fast spin-up and high density but slightly weaker isolation than VMs.
- **Application Container**: An anti-pattern in microservices (e.g., Tomcat, IIS) where multiple distinct application instances share a single language runtime.
- **Function as a Service (FaaS)**: A serverless deployment model where arbitrary code is executed in response to triggers, abstracting away underlying server management (e.g., AWS Lambda).
- **Read Replica**: A duplicate database node designated for read-only traffic to horizontally scale database reads.
- **Pod**: The smallest deployable computing unit in Kubernetes, containing one or more containers that share network and storage.
- **Service (Kubernetes)**: A stable routing endpoint inside a Kubernetes cluster that routes traffic to ephemeral Pods.
- **Deployment (Kubernetes)**: A resource used to apply declarative updates to Pods and ReplicaSets (e.g., scaling, rolling updates).
- **Progressive Delivery**: The practice of separating the *deployment* of software from the *release* of features, offering fine-grained control over the "blast radius" of changes.
- **Feature Toggles (Flags)**: Code-level switches used to hide, enable, or route functionality dynamically at runtime.
- **Canary Release**: Routing a small subset of live traffic to a newly deployed version of a microservice to validate its health before rolling it out globally.
- **Parallel Run**: Executing two different implementations of the same functionality side-by-side on production traffic and comparing the results without exposing the new implementation's output to the user.

# @Objectives

- Ensure every microservice is deployed in a strictly isolated execution environment to prevent cascading resource failures.
- Automate all infrastructure and deployment configurations using declarative IaC, eliminating manual operational steps.
- Design deployment topologies that gracefully handle failure through redundancy, load balancing, and desired state management.
- Decouple the deployment of code from the release of features to minimize risk and enable progressive delivery.
- Select the appropriate deployment abstraction (VM, Container, PaaS, FaaS) based on the specific constraints of the microservice, favoring Containers (Kubernetes) or FaaS for optimal resource utilization.

# @Guidelines

## Execution & Isolation Constraints
- The AI MUST deploy only ONE logical microservice per host/container boundary. 
- The AI MUST NOT group different microservices onto the same physical/virtual host or application container (e.g., placing multiple WAR files in one Tomcat instance is strictly forbidden).
- When generating container configurations, the AI MUST optimize for fast startup times to aid in rapid horizontal scaling and desired state recovery.

## Logical to Physical Topologies
- **Redundancy:** The AI MUST provision multiple instances of a microservice behind a load balancer/service abstraction. The AI MUST spread these instances across multiple failure domains (e.g., AWS Availability Zones) for high availability.
- **Database Mapping:** The AI MUST configure multiple scaled instances of the *same* microservice to connect to a *shared* database infrastructure.
- **Database Scaling:** When read bottlenecks are detected or anticipated, the AI MUST configure Read Replicas and route read-only traffic to them, reserving the primary node for write operations.
- **Database Isolation:** When multiple microservices share the same physical database engine for cost efficiency, the AI MUST configure logically isolated schemas/databases with restricted credentials for each microservice.

## Infrastructure as Code & Desired State
- The AI MUST generate infrastructure definitions using declarative IaC tools (e.g., Terraform, Pulumi, Kubernetes YAML).
- The AI MUST configure desired state mechanisms (e.g., Kubernetes Deployments, Auto Scaling Groups) rather than imperative deployment scripts.
- The AI MUST parameterize environment-specific configurations (e.g., instance counts, log levels) so that the exact same build artifact (e.g., Docker image) can be deployed across all environments.

## Kubernetes Orchestration Rules
- The AI MUST map a microservice instance to a single container within a `Pod` (unless a sidecar, like Envoy, is explicitly required).
- The AI MUST define a Kubernetes `Service` to provide stable internal routing to ephemeral Pods.
- The AI MUST use a Kubernetes `Deployment` to define replica counts and update strategies.
- The AI MUST configure readiness and liveness probes to enable zero-downtime rolling upgrades.

## FaaS / Serverless Rules
- When deploying to a FaaS platform, the AI MUST map functions using one of two models:
  1. **Function per Microservice:** A single function handles all endpoints for the microservice, utilizing internal routing based on the trigger/path.
  2. **Function per Aggregate:** Split the microservice into multiple functions, where each function is strictly aligned to a DDD Aggregate.
- The AI MUST NOT split the state transitions of a *single* aggregate across multiple functions to avoid distributed transaction complexities.
- If using Function per Aggregate, the AI MUST configure these functions to share the same underlying database if they are logically part of the same microservice and owned by the same team.
- The AI MUST provide a coarse-grained external API interface (e.g., an API Gateway) to hide the underlying FaaS decomposition from consumers.

## Progressive Delivery & Release
- The AI MUST treat deployment (installing software into an environment) and release (exposing functionality to users) as two separate technical implementations.
- The AI MUST implement mechanisms for progressive delivery when defining deployment pipelines, utilizing:
  - **Feature Toggles:** To deploy unfinished or risky code safely hidden from users.
  - **Canary Releases:** To route percentage-based traffic via ingress controllers/API gateways to new microservice versions.
  - **Parallel Runs:** To send duplicated traffic to an old and new microservice version simultaneously for output comparison.

# @Workflow

When instructed to design, implement, or modify the deployment architecture for a microservice, the AI MUST adhere to the following algorithm:

1. **Analyze Logical Architecture & Constraints:**
   - Identify the microservice(s) to be deployed.
   - Determine load characteristics, availability requirements, and database dependencies.
   - Select the target deployment abstraction (VM, Container/Kubernetes, or FaaS).

2. **Define the Execution Environment:**
   - *If Container:* Generate the `Dockerfile` ensuring an isolated runtime.
   - *If FaaS:* Determine the mapping strategy (per-microservice or per-aggregate) and generate the serverless configuration (e.g., `serverless.yml`).

3. **Design the Physical Topology (IaC):**
   - Define the load balancer or ingress configuration.
   - Define the desired state configuration (e.g., replica count, auto-scaling rules, deployment strategies).
   - Configure the database layer, explicitly separating write nodes and read replicas if required, ensuring credentials are scoped via least privilege.
   - Inject environment variables to separate configuration from the immutable build artifact.

4. **Implement Progressive Delivery:**
   - Introduce feature toggles in the application code or routing rules in the infrastructure code (e.g., Istio VirtualService for canary weighting).
   - Define health checks and readiness probes to ensure the platform can safely perform zero-downtime rollouts.

5. **Review Against Principles:**
   - Verify isolation: Is there any shared host/runtime state with other microservices? (Must be NO).
   - Verify artifacts: Is the artifact immutable across environments? (Must be YES).
   - Verify desired state: Will the system automatically replace a failed instance? (Must be YES).

# @Examples (Do's and Don'ts)

## Microservice Isolation
- **[DO]**: Deploy `InvoiceService` as a standalone Docker container and `OrderService` as a standalone Docker container, orchestrated by Kubernetes.
- **[DON'T]**: Create a single `docker-compose.yml` that mounts the source code of both `InvoiceService` and `OrderService` into a shared Nginx/PHP-FPM container.
- **[DON'T]**: Deploy multiple Spring Boot microservices into a single shared Tomcat `webapps` folder.

## Artifact Creation & Environments
- **[DO]**: Build `ghcr.io/musiccorp/catalog:v1.2.3` in the CI pipeline. Use this exact image tag in the Dev, QA, and Production Kubernetes `Deployment` manifests, altering only the `ConfigMap` for environment variables.
- **[DON'T]**: Run `npm run build --prod` during the deployment step of the Production pipeline, creating a newly compiled binary that differs from what was tested in the QA pipeline.

## Database Scaling & Mapping
- **[DO]**: Run 5 instances of `OrderService`. Configure all 5 instances to connect to `order-db-primary` for writes, and load balance reads across `order-db-replica-1` and `order-db-replica-2`.
- **[DON'T]**: Give each of the 5 instances of `OrderService` its own completely separate database, fragmenting the data for the same logical microservice.

## FaaS / Serverless Mapping
- **[DO]**: Map an `Expenses` microservice to FaaS by creating one function for the `Receipt` aggregate and one function for the `Claim` aggregate. Point both functions to the shared `Expenses` database.
- **[DON'T]**: Create an `Expenses` FaaS function for "Change Claim Status to Pending" and a separate function for "Change Claim Status to Approved", splitting the state transitions of a single aggregate.

## Progressive Delivery
- **[DO]**: Deploy version `v2` of the `RecommendationService` to production pods. Configure the Kubernetes Ingress to route 95% of traffic to `v1` and 5% of traffic to `v2` (Canary). Monitor error rates on `v2` before increasing traffic.
- **[DON'T]**: Hard-switch a load balancer to send 100% of traffic to a newly deployed microservice immediately, relying solely on pre-production end-to-end tests for safety.