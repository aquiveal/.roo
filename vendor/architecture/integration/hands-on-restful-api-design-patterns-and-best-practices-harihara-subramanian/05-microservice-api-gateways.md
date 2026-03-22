# @Domain

These rules MUST activate when the AI is engaged in tasks involving the design, architecture, implementation, configuration, or debugging of Microservice Architectures (MSA), specifically focusing on API Gateways, service registries, service discovery, microservice orchestration, distributed system security, or when deciding between/configuring API Gateways and Service Meshes.

# @Vocabulary

- **Microservice Architecture (MSA)**: An architectural style where applications consist of a suite of small, modular, independent, horizontally scalable, and highly cohesive services running in unique processes and communicating via well-defined APIs.
- **API Gateway**: A multifaceted reverse proxy that provides a single, unified entry point for external clients to access internal microservices. It abstracts cross-cutting concerns (security, routing, transformation).
- **Service Registry**: A centralized database/repository that keeps track of the network locations and changing availability status of registered microservice instances.
- **Client-side Discovery**: A pattern where the client microservice queries the Service Registry directly to get instance locations, then applies a load balancing algorithm to make the request.
- **Server-side Discovery**: A pattern where the client makes a request to the API Gateway, which then queries the Service Registry to route the request to the appropriate microservice.
- **Composition/Orchestration**: The process of linking multiple microservices together (often via the API Gateway) to create composite, process-aware, and business-centric applications.
- **Transformation**: The translation of data formats (e.g., XML to JSON) and transmission protocols (e.g., HTTP to AMQP, ProtoBuf, or COAP) facilitated by the API Gateway to support heterogeneous clients.
- **CAP (Content Attack Protection)**: Security policies configured in the API Gateway for inbound and outbound traffic to scan and protect against malicious payload insertions (e.g., SQL/XPATH injections, text patterns, special characters).
- **Federated Identity**: A security mechanism utilizing protocols like OpenID, SAML, or OAuth to delegate authentication and authorization to a third-party server, typically utilizing a JSON Web Token (JWT).
- **Service Mesh**: A network communication infrastructure operating primarily at Layer 4 (TCP), deployed alongside applications (e.g., as a sidecar), focused on internal service-to-service resiliency (circuit breakers, retries, timeouts).
- **Sticky Session**: A routing mechanism that creates an affinity between a client and a specific server; to be explicitly avoided at the API Gateway layer to maintain statelessness.

# @Objectives

- Ensure the API Gateway acts as the strict, unified facade decoupling external clients from internal microservices.
- Enforce absolute statelessness within the API Gateway instances, delegating state and counters to distributed caches to ensure horizontal scalability and zero-downtime rolling updates.
- Secure microservice boundaries by offloading identity verification to Federated Identity servers and enforcing Content Attack Protection (CAP) policies at the gateway layer.
- Guarantee High Availability (HA) of the microservice ecosystem by deploying gateways in Active/Active clusters behind standard Load Balancers.
- Clearly delineate architectural responsibilities: use API Gateways (Layer 7) for external exposure, routing, and business-agnostic cross-cutting concerns; use Service Meshes (Layer 4) for internal service-to-service resiliency and network reliability.

# @Guidelines

- **Gateway as a Facade Pattern**: The AI MUST route all external client requests through the API Gateway. Direct external access to internal microservices is STRICTLY FORBIDDEN.
- **Stateless Gateway Enforcement**: The AI MUST configure API Gateways to be entirely stateless. Any counters, rate-limiting quotas, or cached states MUST be maintained in a distributed cache (e.g., a Redis cluster), NEVER in the gateway's local memory.
- **Service Registry Integration**:
  - Microservices MUST register themselves with the Service Registry on startup and deregister on shutdown.
  - The AI MUST configure a heartbeat mechanism to periodically refresh service instance registrations.
  - The AI MUST NOT cache network location details obtained from the Service Registry directly at the API Gateway or registry-aware client. The gateway must dynamically resolve locations to prevent routing failures to stale IPs.
- **Load Balancing and Clustering**:
  - The AI MUST deploy API Gateway instances in an Active/Active clustered mode behind a standard Load Balancer (LB) to prevent the gateway from becoming a Single Point of Failure (SPOF).
  - The AI MUST configure the LB to continuously probe API gateway instances for health and performance to route traffic effectively.
- **Security & Federated Identity**:
  - The AI MUST NOT implement user credential validation logic directly inside the API Gateway or downstream microservices.
  - The AI MUST implement Federated Identity (OAuth, OpenID, SAML). The client retrieves a JWT from a 3rd party Authorization Server and embeds it in the HTTP `Authorization` header.
  - The API Gateway MUST validate the JWT access token with the authorization server before passing the token to downstream microservices.
- **Content Attack Protection (CAP)**:
  - The AI MUST configure inbound CAP policies on the API Gateway to scan requests for SQL injections, XPATH injections, and malicious text patterns.
  - The AI MUST configure outbound CAP policies on the API Gateway to scan reply messages for content-based attacks before delivering them to clients.
  - The AI MUST restrict HTTP methods, HTTP versions, URL paths, query parameters, and enforce IP/domain whitelists at the gateway level.
- **Data Protection and Communication**:
  - The AI MUST enforce SSL/TLS termination at the API Gateway to protect against Man-in-the-Middle (MITM) attacks.
  - The AI MUST apply hashing algorithms on service messages to ensure data integrity during transit.
- **Transformation**: The AI MUST utilize the API gateway to translate protocols (e.g., HTTP to AMQP) and data formats to accommodate resource-constrained/heterogeneous clients (e.g., IoT devices).
- **Monitoring & Analytics**: The AI MUST configure the gateway to capture and expose metrics including total requests, throughput, exception messages, blocked messages, and categorized traffic data to centralized monitoring tools.
- **API Gateway vs. Service Mesh Selection**:
  - If the user requires external-facing API exposure, rate limiting, authentication, or protocol transformation, the AI MUST implement an API Gateway (Layer 7).
  - If the user requires internal service-to-service resiliency (circuit breakers, retries, timeouts, health checks), the AI MUST implement a Service Mesh (Layer 4) like Envoy, Istio, or Linkerd.

# @Workflow

When designing, implementing, or reviewing a Microservice API Gateway architecture, the AI MUST adhere to the following rigid step-by-step process:

1. **Architecture & Discovery Strategy Setup**:
   - Determine if the architecture uses Client-Side Discovery or Server-Side Discovery.
   - Establish a highly available, clustered Service Registry.
   - Ensure the API Gateway resolves upstream endpoints dynamically from the Service Registry without indefinitely caching location data.

2. **Gateway Deployment & High Availability Initialization**:
   - Deploy the chosen API Gateway solution (e.g., Kong, Envoy, Tyk, Ambassador).
   - Configure multiple gateway instances in an Active/Active cluster.
   - Provision a distributed cache for storing rate-limiting counters and gateway state.
   - Place a Load Balancer in front of the gateway cluster with active health-probing configured.

3. **Security & Federated Identity Implementation**:
   - Integrate the API Gateway with an external Authorization Server.
   - Configure the gateway to intercept incoming requests, extract the JWT from the `Authorization` header, and validate it.
   - Configure the gateway to forward the validated JWT to the backend microservices.
   - Enforce SSL/TLS termination at the gateway.

4. **Policy Enforcement & Transformation Configuration**:
   - Define and apply inbound CAP policies to reject malicious payloads (SQL/XPATH injection, special characters).
   - Define and apply outbound CAP policies to sanitize responses.
   - Implement required data and protocol translation adapters (e.g., HTTP to backend ProtoBuf or AMQP).

5. **Monitoring, Analytics, & Resiliency Offloading**:
   - Connect gateway logs and metrics (throughput, blocked requests, latency) to an external monitoring tool (e.g., Prometheus, Moesif, ELK).
   - Delegate internal inter-service resiliency (circuit breaking, retries) to a Service Mesh layer (if applicable), ensuring the gateway strictly handles edge traffic.

# @Examples (Do's and Don'ts)

### High Availability & Gateway State
**[DO]** Configure the API Gateway to be entirely stateless, utilizing a distributed cache (like Redis) for rate-limiting.
```yaml
# Gateway configuration
rate_limiting:
  strategy: distributed
  storage: redis
  redis_endpoint: "redis-cluster.internal:6379"
```
**[DON'T]** Store rate-limiting counters in the gateway's local memory or use sticky sessions.
```yaml
# ANTI-PATTERN: Local memory state limits scalability
rate_limiting:
  strategy: local
  storage: memory
```

### Identity Validation
**[DO]** Delegate authentication to an external Federated Identity provider and validate the JWT at the gateway.
```javascript
// Correct: Gateway validating JWT from Auth server
function gatewayAuthMiddleware(req, res, next) {
    const token = req.headers.authorization.split(' ')[1];
    jwtValidator.verifyWithExternalAuthServer(token, (err, decoded) => {
        if (err) return res.status(401).send("Unauthorized");
        req.headers['x-user-context'] = decoded; // Pass context to microservice
        next();
    });
}
```
**[DON'T]** Implement raw user credential checking (e.g., checking passwords against a database) directly inside the API Gateway or backend microservice.
```javascript
// ANTI-PATTERN: Gateway checking DB directly for passwords
function gatewayAuthMiddleware(req, res, next) {
    db.query("SELECT * FROM users WHERE username=? AND password=?", [req.body.user, req.body.pass], (err, result) => {
        if (result) next();
    });
}
```

### Content Attack Protection (CAP)
**[DO]** Enforce strict CAP policies on the API Gateway to filter out malicious input.
```yaml
# Correct: Inbound CAP policy on API Gateway
security_policies:
  inbound:
    - type: sql_injection_filter
      action: block
    - type: xpath_injection_filter
      action: block
    - type: method_restriction
      allowed_methods: ["GET", "POST"]
```
**[DON'T]** Allow all HTTP verbs, parameters, and raw data payloads to pass directly to internal microservices without inspection at the gateway.

### Gateway vs Service Mesh Responsibilities
**[DO]** Use the API Gateway for external API exposure, rate limiting, and JWT validation. Use a Service Mesh sidecar for internal service-to-service retries and circuit breaking.
**[DON'T]** Program complex, internal-only service-to-service circuit breaking logic directly into the API Gateway routing rules, conflating the Layer 7 edge proxy with Layer 4 mesh responsibilities.

### Service Registry Interaction
**[DO]** Have the API Gateway dynamically query the Service Registry for the target microservice's network location.
**[DON'T]** Cache the Service Registry's IP location details permanently in the API Gateway's configuration files, which prevents routing to dynamically scaled or replaced containers.