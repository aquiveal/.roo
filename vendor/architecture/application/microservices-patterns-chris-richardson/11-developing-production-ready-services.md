@Domain
This rule set is activated when the AI is tasked with designing, developing, refactoring, or reviewing microservices intended for production environments. It is specifically triggered when the context involves application security (authentication/authorization), externalized configuration, observability (monitoring, logging, distributed tracing, metrics, exception tracking, audit logging), or the implementation of cross-cutting concerns via a Microservice Chassis or Service Mesh.

@Vocabulary
- **Principal:** The application or human attempting to access the application.
- **Authentication:** The process of verifying the identity of the principal.
- **Authorization:** The process of verifying that the principal is allowed to perform the requested operation on the specified data (e.g., using Role-based security or ACLs).
- **Session Token:** A token (often opaque, like a cryptographically strong random number) used in traditional monolithic applications to identify an active session.
- **Security Context:** A storage mechanism (like a thread-local variable in Spring Security) that holds information about the user making the current request.
- **Access Token:** A token passed by an API gateway to services containing information about the user (e.g., identity and roles).
- **Opaque Token:** A token (e.g., a UUID) that requires the recipient to make a synchronous RPC call to a security service to validate and retrieve user information.
- **Transparent Token / JWT (JSON Web Token):** A self-contained, signed token containing claims (identity, roles, expiration) that can be validated locally by a service without a synchronous RPC call.
- **OAuth 2.0:** An authorization protocol standard utilizing an Authorization Server, Access Tokens, Refresh Tokens, Resource Servers (microservices), and Clients (API Gateway).
- **Externalized Configuration Pattern:** A pattern where configuration property values (e.g., database credentials) are supplied to a service at runtime using a Push model (environment variables/files) or a Pull model (configuration server).
- **Health Check API Pattern:** An endpoint (e.g., `GET /health`) exposed by a service that returns its health status to the deployment infrastructure.
- **Readiness Probe:** A health check used to determine whether traffic should be routed to a service instance.
- **Liveness Probe:** A health check used to determine whether a service instance should be terminated and restarted.
- **Log Aggregation Pattern:** A pattern where service activity logs are aggregated into a centralized database (e.g., ELK stack: Elasticsearch, Logstash, Kibana).
- **Distributed Tracing Pattern:** A pattern where each external request is assigned a unique ID, recording a tree of service calls (Traces consisting of Spans) to track flow and latency.
- **B3 Standard:** A common standard for propagating trace information using HTTP headers (e.g., `X-B3-TraceId`).
- **Application Metrics Pattern:** A pattern where services report infrastructure and application-level metrics (via Push or Pull models) to a central server (e.g., Prometheus) using dimensions.
- **Exception Tracking Pattern:** A pattern where services report exceptions directly to a centralized tracking service (e.g., Honeybadger, Sentry) for de-duplication and alert management.
- **Audit Logging Pattern:** A pattern recording user actions (who, what, when) in a database using AOP or Event Sourcing.
- **Microservice Chassis Pattern:** A framework (e.g., Spring Boot/Cloud, Go Kit) handling cross-cutting concerns so developers focus only on business logic.
- **Service Mesh Pattern:** A networking infrastructure layer (e.g., Istio, Linkerd) that mediates all communication in and out of services, handling routing, circuit breaking, tracing, and TLS.

@Objectives
- Ensure all microservices are fully production-ready by satisfying three critical quality attributes: security, configurability, and observability.
- Centralize authentication at the API Gateway while distributing authorization logic to individual microservices via transparent tokens (JWTs).
- Decouple environment-specific configurations from the codebase using externalized configuration mechanisms.
- Guarantee deep visibility into distributed systems through comprehensive health checks, centralized logging, distributed tracing, application-specific metrics, and exception tracking.
- Eliminate boilerplate code for cross-cutting concerns by utilizing a Microservice Chassis and/or offloading network capabilities to a Service Mesh.

@Guidelines
- **Security:**
  - The AI MUST NOT use in-memory security contexts (e.g., `ThreadLocal`) or centralized database-backed sessions to pass user identity between microservices.
  - The AI MUST implement authentication centrally in the API Gateway. The API Gateway MUST pass a transparent access token (e.g., JWT) to the backend services.
  - The AI MUST implement authorization (Role-based access control and ACLs) within the individual backend services using the claims extracted from the JWT.
  - When configuring JWTs, the AI MUST use short-lived access tokens combined with refresh tokens (via the OAuth 2.0 protocol) to mitigate the inability to selectively revoke self-contained tokens.
- **Configuration:**
  - The AI MUST apply the Externalized Configuration pattern. The AI MUST NEVER hard-wire environment-specific configuration properties into the source code.
  - The AI MUST secure sensitive data (e.g., database credentials) using a secrets storage mechanism (e.g., Hashicorp Vault, AWS Parameter Store) and ideally use a configuration server that supports transparent decryption.
  - The AI MUST select the Push model (OS environment variables/files) for simple infrastructural configuration, and the Pull model (Configuration Server) when centralized management and dynamic reconfiguration are required.
- **Observability - Health Checks:**
  - The AI MUST expose a Health Check API endpoint (e.g., `/actuator/health`).
  - The AI MUST ensure the health check logic verifies the service instance's connections to external infrastructure services (e.g., executing a test query against an RDBMS).
- **Observability - Logging & Tracing:**
  - The AI MUST configure services to log to `stdout` rather than local files, allowing the deployment infrastructure to handle log shipping to an aggregation server (e.g., ELK).
  - The AI MUST implement the Distributed Tracing pattern using an instrumentation library (e.g., Spring Cloud Sleuth) to automatically assign Trace IDs and Span IDs.
  - The AI MUST ensure that the Trace ID and Span ID are automatically included in every application log entry (e.g., via SLF4J MDC) to correlate logs across services.
- **Observability - Metrics & Exceptions:**
  - The AI MUST implement the Application Metrics pattern to record business-level metrics (e.g., counting orders placed, approved, rejected) alongside JVM/infrastructure metrics.
  - The AI MUST NOT rely on standard logging to track unhandled exceptions. The AI MUST configure the service to report exceptions to a dedicated Exception Tracking service (e.g., Honeybadger, Sentry) using the service's client library or servlet filter.
- **Observability - Audit Logging:**
  - The AI MUST implement the Audit Logging pattern to track user actions for compliance and support.
  - The AI MUST NOT manually sprinkle audit logging code throughout business logic. The AI MUST use Aspect-Oriented Programming (AOP) or Event Sourcing to automatically generate audit entries.
- **Microservice Chassis & Service Mesh:**
  - The AI MUST base the service implementation on a Microservice Chassis (e.g., Spring Boot/Cloud) to automatically handle configuration, metrics, and health checks.
  - If a Service Mesh (e.g., Istio) is present, the AI MUST offload network-related concerns (circuit breakers, service discovery, load balancing, TLS) to the mesh, simplifying the chassis configuration.

@Workflow
1. **Security Setup:** 
   - Define API Gateway authentication using an OAuth 2.0 Authorization Server.
   - Configure the API Gateway to generate/forward a JWT Access Token.
   - Implement JWT validation and Role/ACL-based authorization directly in the target microservice controllers/services.
2. **Configuration Extraction:**
   - Identify all environment-dependent properties (URLs, ports, credentials).
   - Abstract them into externalized configuration sources (e.g., Spring Boot `@ConfigurationProperties`).
   - Integrate a secret manager for sensitive credentials.
3. **Health & Metrics Instrumentation:**
   - Enable and customize the Health Check API to explicitly test all outbound database/broker connections.
   - Inject a metrics registry (e.g., Micrometer `MeterRegistry`) into domain services to increment custom business-logic counters.
4. **Tracing & Logging Integration:**
   - Add the distributed tracing library dependency (e.g., Spring Cloud Sleuth).
   - Configure the logging framework to output to `stdout` and include MDC tracing variables in the log pattern.
   - Integrate an exception-tracking client library to catch and forward unhandled exceptions.
5. **Auditing Verification:**
   - Create AOP pointcuts targeting domain service execution, extracting user ID from the security context, and persisting the action to an audit table.
6. **Chassis & Mesh Abstraction Check:**
   - Remove any manual HTTP retry loops or circuit breaker implementations if a Service Mesh sidecar (Envoy) is handling traffic management.

@Examples (Do's and Don'ts)
- **Security Context**
  - [DO]: Extract user information from an injected JWT token passed via HTTP headers: `String userId = jwtToken.getClaim("userId");`
  - [DON'T]: Attempt to share a session or use `ThreadLocal` storage across services: `SecurityContextHolder.getContext().getAuthentication();` (when expecting context from an upstream service without token propagation).
- **Configuration**
  - [DO]: Bind properties dynamically from the environment using chassis features: `@Value("${aws.region}") private String awsRegion;`
  - [DON'T]: Use hardcoded environment checks to set configurations: `if (env.equals("PROD")) { dbUrl = "jdbc:mysql://prod-db"; }`
- **Health Checks**
  - [DO]: Implement a custom `HealthIndicator` that runs a lightweight `SELECT 1` against the database to verify connectivity.
  - [DON'T]: Create a simple `GET /health` that unconditionally returns `HTTP 200 OK` regardless of backend infrastructure status.
- **Logging & Tracing**
  - [DO]: Ensure log patterns output to `stdout` and include trace variables: `%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} [traceId=%X{X-B3-TraceId}, spanId=%X{X-B3-SpanId}] - %msg%n`
  - [DON'T]: Configure the service to write logs to `/var/log/app/service.log` within a containerized environment.
- **Exception Tracking**
  - [DO]: Add a dependency for an exception tracking service (e.g., Sentry) and configure its servlet filter to catch and ship errors automatically.
  - [DON'T]: Simply write `logger.error("Exception occurred", e);` and rely on developers searching raw log streams for stack traces.
- **Metrics**
  - [DO]: Inject a `MeterRegistry` and increment specific business outcomes: `meterRegistry.counter("placed_orders").increment();`
  - [DON'T]: Execute expensive SQL aggregations (e.g., `SELECT COUNT(*) FROM orders`) on demand to monitor application health.