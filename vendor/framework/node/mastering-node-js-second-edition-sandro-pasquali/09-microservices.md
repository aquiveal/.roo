# @Domain
Triggered when tasks involve designing, refactoring, or building distributed architectures, specifically focusing on microservices, Service-Oriented Architectures (SOA), serverless deployments (AWS Lambda via Claudia.js), Seneca pattern-based microservices, Docker containerization, or Kubernetes container orchestration within a Node.js ecosystem.

# @Vocabulary
*   **Microservice**: A small, independent, stateless, and clearly delineated service that does one thing well, communicates via standard protocols, and can be hot-reloaded, scaled, or replaced without affecting the larger system.
*   **Monolith**: An architecture where the presentation, application, and data layers are tightly coupled within the same process, machine, or code repository.
*   **3-Tier Architecture**: A traditional application structure comprising a Presentation tier (UI), an Application tier (business logic), and a Data tier (database).
*   **4-Tier Architecture**: A modern distributed structure comprising a Services tier (abstracted data sources), an Aggregation tier (business logic and data shaping), a Delivery tier (device/client-specific data transformation), and a Client tier (final rendering).
*   **Seneca**: A Node.js microservices toolkit that organizes code into actions triggered by JSON pattern matching (e.g., `role` and `cmd`).
*   **Mesh**: An autodiscovery network plugin for Seneca (`seneca-mesh`) that removes the need for services to know the specific host/port of other services.
*   **Serverless/AWS Lambda**: A cloud computing execution model where the cloud provider dynamically manages the allocation and provisioning of servers. Lambda functions are containerized Node applications built and deployed automatically.
*   **Claudia (claudia-api-builder)**: A deployment framework/tool for creating simple Node.js microservices and deploying them to AWS Lambda and API Gateway.
*   **Docker**: A containerization technology. Containers are isolated, secure application platforms launched from templates (Images) running on a shared host OS.
*   **Kubernetes (K8s)**: An orchestration system for managing, deploying, and scaling containerized applications across clusters of machines.
*   **Minikube**: A tool that runs a single-node Kubernetes cluster inside a Virtual Machine for local development.
*   **Pod**: The basic organizational unit of Kubernetes; an abstract wrapper around one or more containers that share an IP address, localhost network, and storage volumes.
*   **YAML (Yet Ain't Markup Language)**: The declarative format used to specify Kubernetes manifests (Pods, Deployments, Volumes).

# @Objectives
*   Decompose large, monolithic applications into small, single-purpose, and loosely coupled microservices.
*   Ensure services are stateless, isolating dependencies and making processes disposable and easily replicable.
*   Implement robust service discovery and communication using JSON pattern matching (Seneca) or orchestrated networking (Kubernetes).
*   Facilitate zero-downtime deployments, independent scaling, and graceful degradation by isolating failure boundaries.
*   Utilize Serverless (Lambda) architectures for low-overhead, infinitely scalable compute tasks when local persistent storage is unnecessary.
*   Abstract deployment implementation details through declarative orchestration (Docker and Kubernetes).

# @Guidelines
*   **Microservice Principles**
    *   MUST limit service code to a small, readable size (aiming for ~100 lines of code where practical).
    *   MUST NOT allow a service to depend on or know about the underlying implementation details of another service.
    *   MUST decentralize data models; prefer having each service maintain its own data state or database connection.
    *   MUST design services to fail gracefully, isolating points of failure to prevent cascading system outages.
*   **Seneca Framework**
    *   MUST use consistent JSON pattern matching (e.g., `role: 'category', cmd: 'action'`) to trigger service actions.
    *   MUST use `seneca({ log: 'silent' })` to suppress verbose default logging during standard development/testing unless debugging.
    *   MUST use the `seneca-mesh` plugin to enable service autodiscovery; AVOID hardcoding `seneca.client({ port: XXXX })` when deploying fleets of interacting services.
*   **Serverless and AWS Lambda (via Claudia)**
    *   MUST respect AWS Lambda resource limits: max memory (1536 MB), ephemeral disk space (`/tmp` 512 MB), execution timeout (300 seconds max), and payload sizes.
    *   MUST NOT rely on persistent local state or background daemon processes inside a Lambda function.
    *   MUST use the `request` argument (specifically `request.lambdaContext` when using Claudia API Builder) to access invocation IDs and execution contexts.
*   **Docker Containerization**
    *   MUST use explicit base images with version tags in `Dockerfile` (e.g., `FROM node:9` instead of `FROM node`).
    *   MUST use the `EXPOSE` directive to explicitly declare the ports the container listens on.
    *   MUST use standard directives: `WORKDIR` to set the execution context, `COPY` to transfer application files, `RUN` to execute build steps (like `npm i`), and `CMD` to define the startup process.
*   **Kubernetes Orchestration**
    *   MUST use YAML manifest files to declaratively define Pods, volumes, and deployment strategies rather than relying solely on imperative `kubectl` terminal commands.
    *   MUST group containers that require shared local data or direct network proximity into the same Pod.
    *   MUST use shared volumes (e.g., `emptyDir`) to share ephemeral data between containers within the same Pod.
    *   MUST communicate between containers in the same Pod using `localhost:<port>`.

# @Workflow
1.  **Domain Decomposition**: Analyze the business logic to identify distinct operations. Separate these into the 4-Tier model: Data sources (Services), Business logic (Aggregation), Client-specific formatting (Delivery), and UI (Client).
2.  **Service Definition**: Write small, isolated Node.js scripts for each operation. If using Seneca, define actions using `.add({ role, cmd })`.
3.  **Service Integration & Discovery**: Link services using decoupled mechanisms. Use Seneca mesh for peer-to-peer discovery, or define distinct REST endpoints if using standard HTTP routing.
4.  **Deployment Strategy Selection**:
    *   *If Serverless*: Wrap the service in `claudia-api-builder`. Test locally, then deploy using `claudia create --region <region> --api-module <entry_file>`.
    *   *If Containerized*: Create a `Dockerfile` specifying the Node.js runtime, dependencies, and exposed ports. Build the image using `docker build -t <image_name>:<version> .`.
5.  **Orchestration (Kubernetes)**:
    *   Create a YAML manifest (`kind: Pod` or `Deployment`).
    *   Map container ports and define shared volumes if multiple containers reside in the Pod.
    *   Deploy the cluster via `kubectl create -f <manifest.yaml>`.
    *   Expose the deployment to the network using `kubectl expose deployment <name> --type=LoadBalancer`.
6.  **Scale and Monitor**: Scale the service horizontally (`kubectl scale deployment <name> --replicas=<count>`) based on CPU, memory, or specific load requirements.

# @Examples (Do's and Don'ts)

**Microservices Pattern Matching (Seneca)**
*   [DO] Use standard property patterns to define and call services, and use mesh for discovery.
```javascript
// Base Node
require('seneca')().use('mesh', { base: true });

// Service definition
require('seneca')()
  .add({ role: 'calculator', cmd: 'add' }, (args, done) => {
    done(null, { result: args.operands[0] + args.operands[1] });
  })
  .use('mesh', { pin: { role: 'calculator', cmd: 'add' } })
  .listen({ host: 'localhost', port: 8080 });

// Service consumption
require('seneca')()
  .use('mesh')
  .ready(function() {
    this.act({ role: 'calculator', cmd: 'add', operands: [7,3] }, (err, op) => {
      console.log(op.result);
    });
  });
```
*   [DON'T] Tightly couple services by hardcoding client ports when an autodiscovery mesh is appropriate for the architecture.
```javascript
// Anti-pattern: Hardcoding ports makes scaling and routing difficult
const seneca = require('seneca')();
const mathClient = seneca.client(8080); // Brittle connection
mathClient.act({ role: 'calculator', cmd: 'add' }, callback);
```

**Serverless Functions (AWS Lambda / Claudia)**
*   [DO] Define lightweight, stateless HTTP handlers returning immediate results or Promises.
```javascript
const ApiBuilder = require('claudia-api-builder');
const api = new ApiBuilder();
module.exports = api;

api.get('/hello', function (request) {
  // Use request.lambdaContext for AWS specific execution details
  return 'Hello from AWS!';
});
```
*   [DON'T] Attempt to spin up local background processes, HTTP servers, or rely on persistent disk state in a Lambda function.
```javascript
// Anti-pattern: Serverless environments do not support long-running listeners
const express = require('express');
const app = express();
app.listen(8080); // Will cause execution timeout/failure in AWS Lambda
```

**Docker Containerization**
*   [DO] Use explicit build steps and version tags in the Dockerfile.
```dockerfile
FROM node:9
LABEL maintainer="dev@example.com"
ENV NODE_ENV=development
WORKDIR /app
COPY ./app .
RUN npm i
EXPOSE 8087
CMD [ "npm", "start" ]
```
*   [DON'T] Run multiple unrelated processes (e.g., Node server + MongoDB) inside a single Dockerfile; use separate containers.

**Kubernetes Pod Communication**
*   [DO] Allow containers within the same Pod to communicate via `localhost` and share files via volumes.
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: paired-services
spec:
  volumes:
    - name: shared-data
      emptyDir: {}
  containers:
    - name: node-server
      image: my-node-server:v1
      volumeMounts:
        - name: shared-data
          mountPath: /app/public
    - name: helper-service
      image: my-helper:v1
      # Communicates with node-server via http://localhost:<port>
```
*   [DON'T] Attempt to use external IPs to communicate between containers defined within the exact same Pod definition.