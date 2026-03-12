@Domain
This rule set is activated whenever the AI is tasked with designing, implementing, configuring, or troubleshooting software deployment topologies, CI/CD pipelines, container orchestration (e.g., Kubernetes, Docker), Infrastructure as Code (IaC) (e.g., Terraform, Pulumi), serverless/Function-as-a-Service (FaaS) deployments, or progressive delivery mechanisms (feature toggles, canary releases) in a microservice architecture context.

@Vocabulary
- **Logical vs. Physical Architecture**: The distinction between the conceptual design of interacting services (logical) and the actual servers, containers, networks, and instances they run on (physical).
- **Availability Zone (AZ)**: An isolated data center within a cloud provider's region. Used for physical redundancy.
- **Read Replica**: A read-only copy of a database used to scale read traffic horizontally while leaving the primary node to handle writes.
- **Isolated Execution**: Running each microservice in its own ring-fenced computing environment (e.g., a container or VM) to prevent resource contention and side effects from other services.
- **Infrastructure as Code (IaC)**: Managing and provisioning infrastructure through machine-readable definition files (e.g., Terraform, Pulumi) rather than manual configuration.
- **Zero-Downtime Deployment**: Deploying a new version of a service without interrupting users or upstream consumers (e.g., via rolling upgrades or blue-green deployment).
- **Desired State Management**: A platform capability (e.g., Kubernetes) that automatically maintains infrastructure to match a declarative configuration (e.g., automatically replacing dead instances).
- **GitOps**: An operational framework where the desired state of infrastructure is version-controlled in Git, and automated tooling (e.g., Flux) applies it to the cluster.
- **Type 2 Virtualization**: Virtual machines running on a host operating system via a hypervisor, providing strong isolation but carrying resource overhead.
- **Linux Containers**: Lightweight isolated execution environments sharing the same underlying host OS kernel (e.g., Docker).
- **Application Container**: A single runtime process (e.g., Tomcat, IIS) hosting multiple different applications/services. Strictly considered an anti-pattern for microservices.
- **Platform as a Service (PaaS)**: Highly abstracted deployment platforms (e.g., Heroku) that manage underlying servers dynamically.
- **Function as a Service (FaaS)**: Event-driven serverless computing (e.g., AWS Lambda, Azure Functions) where functions scale to zero and are spun up on demand.
- **Cold Start**: The latency delay experienced when a FaaS platform spins up a new instance of a function.
- **Kubernetes Pod**: The smallest deployable computing unit in Kubernetes, containing one or more tightly coupled containers.
- **Kubernetes Service**: A stable network routing endpoint that abstracts away ephemeral Pod IPs.
- **Kubernetes Deployment**: A controller that provides declarative updates for Pods and ReplicaSets (e.g., managing rolling upgrades).
- **Custom Resource Definitions (CRDs)**: Extensions to the Kubernetes API allowing for the creation of custom abstractions.
- **Progressive Delivery**: Continuous delivery augmented with fine-grained control over the blast radius of releases.
- **Feature Toggle (Feature Flag)**: A mechanism to hide, enable, or disable functionality at runtime.
- **Canary Release**: Routing a small percentage of user traffic to a new version of a service to validate it before a full rollout.
- **Parallel Run**: Executing both the old and new implementations of a service side-by-side, routing the same request to both, and comparing results without exposing the new result to the user.

@Objectives
- **Ensure Independent Deployability**: Design systems so that any microservice can be deployed to production without requiring lock-step deployments of other services.
- **Guarantee Execution Isolation**: Prevent systemic failures and "noisy neighbor" problems by dedicating specific computing resources to single microservices.
- **Enforce Immutable Artifacts**: Decouple the software build from the environment configuration to ensure the exact code tested is the exact code deployed to production.
- **Automate Everything**: Eliminate manual provisioning, configuration, and deployment steps using CI/CD and IaC.
- **Separate Deployment from Release**: Allow software to be pushed to production infrastructure safely (deployment) before exposing it to users (release) using progressive delivery techniques.

@Guidelines

**Physical Topology & Isolation Constraints**
- The AI MUST configure deployments such that each microservice instance runs in its own isolated execution environment (e.g., one Docker container per service, or one VM per service).
- The AI MUST NEVER suggest or configure Application Containers (e.g., running multiple `.war` files in one Tomcat instance) for microservices.
- The AI MUST configure high availability by distributing multiple instances of a microservice across multiple distinct physical domains (e.g., multiple AWS Availability Zones).
- For public cloud deployments, the AI MUST FAVOR dedicated, managed database infrastructure (e.g., AWS RDS) per microservice over shared multi-tenant database clusters.
- The AI MUST configure load balancers to route traffic to active instances and seamlessly handle instance termination.

**Environment & Artifact Rules**
- The AI MUST design CI/CD pipelines that build a deployment artifact EXACTLY ONCE early in the pipeline.
- The AI MUST NOT configure pipelines that recompile or rebuild code for different target environments.
- The AI MUST inject environment-specific configuration (e.g., URLs, logging levels, secrets) dynamically at runtime, external to the immutable artifact.
- The AI MUST design pre-production environments to optimize for fast feedback (e.g., local Docker, lightweight CI stubs) while late-stage environments MUST optimize for production-parity.

**Deployment Platform Selection**
- The AI MUST apply "Sam's Rules of Thumb" for platform selection:
  1. If an existing process works perfectly, do not force a migration.
  2. Favor offloading operational burden to managed PaaS/FaaS where the application fits the platform constraints.
  3. Default to Containerization (Docker) and Container Orchestration (Kubernetes) for standard microservice workloads requiring custom configurations or multi-language support.
- If implementing FaaS (Serverless), the AI MUST map architectural boundaries accurately. Map either one function per microservice OR one function per Domain-Driven Design (DDD) Aggregate.
- The AI MUST NEVER map a single FaaS function to an individual state transition within an aggregate, as this breaks aggregate transactional boundaries and requires complex saga coordination unnecessarily.

**Kubernetes Orchestration Rules**
- When generating Kubernetes manifests, the AI MUST define a `Deployment` to handle Pod life cycles and rolling upgrades; the AI MUST NEVER manage raw `ReplicaSets` or `Pods` directly unless explicitly required by an edge-case automation.
- The AI MUST define a `Service` for intra-cluster routing to abstract away ephemeral Pod instances.
- The AI MUST configure readiness and liveness probes to enable Kubernetes to execute Desired State Management effectively.

**Progressive Delivery & Release Strategy**
- The AI MUST structure systems to support Zero-Downtime Deployments (e.g., Rolling Updates in K8s).
- The AI MUST actively decouple "Deployment" from "Release".
- When asked to reduce release risk, the AI MUST generate architectures supporting Feature Toggles, Canary Releases (using traffic weighting), or Parallel Runs.
- When generating a Parallel Run, the AI MUST ensure that the new implementation's outputs are compared and logged but NEVER sent back to the client or allowed to cause side-effect state mutations.

**Infrastructure as Code (IaC)**
- All infrastructure recommendations provided by the AI MUST be accompanied by IaC definitions (e.g., Terraform, Pulumi, Kubernetes YAML).
- The AI MUST ensure GitOps compatibility by defining infrastructure declaratively so a control plane (e.g., Flux, ArgoCD) can reconcile the desired state.

@Workflow
When tasked with designing or implementing a microservice deployment pipeline or architecture, the AI MUST execute the following algorithmic steps:

1. **Platform Selection Assessment**: 
   - Analyze the target workload constraints.
   - If workload is highly event-driven, sporadic, and stateless, default to FaaS (e.g., AWS Lambda).
   - If workload is standard web/RPC and requires fine-grained control, default to Containers (Kubernetes/Docker).
2. **Topology Generation**:
   - Define the physical scale: How many instances? Across how many availability zones?
   - Define the data tier: Allocate dedicated database infrastructure or provision read replicas if read-heavy scaling is needed.
3. **Artifact & Configuration Pipeline Setup**:
   - Generate a CI/CD build script that produces a single immutable container image or binary.
   - Define the external configuration mechanism (e.g., Kubernetes ConfigMaps, AWS Parameter Store) for each target environment (Dev, CI, Preprod, Prod).
4. **Isolation & Orchestration Configuration**:
   - If Kubernetes is chosen, generate the exact `Deployment`, `Service`, and `ConfigMap` YAML files. Implement liveness/readiness probes.
   - If FaaS is chosen, map functions correctly at the Microservice or Aggregate level.
5. **Progressive Delivery Implementation**:
   - Implement the release strategy. Create configuration for feature toggles or define traffic-routing rules for a Canary Release (e.g., via a Service Mesh or Ingress controller).
6. **Disaster Recovery & Desired State Config**:
   - Verify that the IaC templates allow the entire microservice and its infrastructure to be rebuilt from scratch from source control without manual intervention.

@Examples (Do's and Don'ts)

**Artifact Creation**
- [DO]: A Dockerfile that compiles a Go binary, wrapped in an Alpine image, which is built once in a GitHub Actions pipeline and pushed to an Elastic Container Registry (ECR). The same image tag is deployed to Staging and Production.
- [DON'T]: A CI pipeline that runs `npm run build:staging` for the staging environment and `npm run build:prod` for the production environment, generating two different artifacts.

**Execution Isolation**
- [DO]: Deploying the `Inventory` service in its own Kubernetes Pod with dedicated CPU and Memory requests/limits, while the `Customer` service runs in a completely separate Pod.
- [DON'T]: Deploying a Tomcat server on an EC2 instance and dropping `inventory.war`, `customer.war`, and `billing.war` into the `webapps/` folder.

**Database Infrastructure**
- [DO]: Provisioning an AWS RDS PostgreSQL instance exclusively for the `Order` microservice, and a separate DynamoDB table exclusively for the `Session` microservice.
- [DON'T]: Installing MySQL on the same physical VM that is running the Node.js application process.

**FaaS Mapping**
- [DO]: Creating a single AWS Lambda function handling the entirety of the `Expense` aggregate (Create Expense, Update Expense, Approve Expense) using internal path routing.
- [DON'T]: Creating `CreateExpenseLambda`, `UpdateExpenseLambda`, and `ApproveExpenseLambda` where each function manages a fraction of the aggregate's lifecycle, resulting in distributed transaction nightmares.

**Progressive Delivery**
- [DO]: Deploying v2.0 of a microservice to Kubernetes and configuring the Ingress controller to route 5% of live traffic to v2.0 (Canary) while monitoring 5xx error rates before scaling to 100%.
- [DON'T]: Updating the production load balancer to instantly cut over 100% of traffic from v1.0 to v2.0 without validation, requiring a manual scramble to roll back if a critical bug appears.