@Domain
These rules are activated when the AI is engaged in tasks involving application packaging, deployment configurations, build pipelines (CI/CD), logging mechanisms, health check implementations, telemetry/monitoring setup, configuration management (e.g., environment variables, settings files), and infrastructure-as-code (e.g., Dockerfiles, Terraform).

@Vocabulary
- **Service**: A collection of processes across machines that work together to deliver a unit of functionality. May consist of multiple executables and present a single IP via load balancing.
- **Instance**: An installation on a single machine (container, virtual, or physical) out of a load-balanced array of the same executable.
- **Executable**: An artifact (binary or source) created by a build process that a machine can launch as a process.
- **Process**: An operating system process running on a machine; the runtime image of an executable.
- **Installation**: The executable and any attendant directories, configuration files, and other resources as they exist on a machine.
- **Deployment**: The act of creating an installation on a machine. Must be automated and kept in source control.
- **Immutable Infrastructure**: An approach where machines/containers are never patched or updated in place. Instead, a new image is built from a known base, deployed, and the old one is discarded (Disposable Infrastructure).
- **Convergence**: An older infrastructure pattern where configuration management tools apply scripts to transition a long-lived machine from an unknown state to a desired state (Mutable Infrastructure).
- **Transparency**: The qualities built into a system that allow operators to gain understanding of its historical trends, present conditions, instantaneous state, and future projections.
- **Exoskeleton Monitoring**: A monitoring pattern where policy decisions (thresholds, triggers, alerts) are kept outside the instance itself, rather than being woven into the application code.
- **White-box Technology**: Observability tech running inside the process (e.g., language-specific agents or APIs).
- **Black-box Technology**: Observability tech sitting outside the process (e.g., log file scrapers).

@Objectives
- Guarantee a strict "chain of custody" for code, ensuring production builds only occur on clean CI servers, never on developer workstations.
- Enforce the principles of Immutable and Disposable Infrastructure over in-place server patching.
- Isolate configuration from code, ensuring sensitive credentials are never stored in the source code repository or the compiled binary.
- Architect instances to be completely transparent by emitting standardized, human-readable logs, comprehensive metrics, and detailed health checks.
- Prevent operator error by designing configuration schemas based on function rather than technical nature, and by avoiding complex, unstructured log outputs.

@Guidelines

**Code & Build Pipeline Rules**
- The AI MUST NEVER generate deployment scripts that compile production artifacts on a developer's local machine. All production builds MUST be scripted to run on a Continuous Integration (CI) server.
- The AI MUST configure dependency managers to pull from secure, private repositories for production builds, checking digital signatures where possible, rather than downloading directly from the open internet.
- The AI MUST ensure build scripts include a step to automatically strip or disable `DEBUG` and `TRACE` log levels for production artifacts.

**Infrastructure Rules**
- The AI MUST favor Immutable Infrastructure patterns (e.g., Docker containers, immutable AMIs) over Convergence patterns. Do not generate scripts that patch, update, or mutate running production machines.
- If updates are required, the AI MUST generate configurations that build a completely new image and replace the old instance.

**Configuration Rules**
- The AI MUST externalize all per-environment configurations. Configuration properties MUST NOT be baked into the deployment directory or the application binary.
- The AI MUST NEVER write scripts or code that commits passwords, secrets, or production database credentials into the main source code repository.
- When configuring containers or ephemeral cloud instances, the AI MUST inject configurations at startup via environment variables or a text blob (e.g., EC2 User Data).
- For large-scale dynamic environments, the AI MAY utilize a configuration service (e.g., ZooKeeper, etcd), but MUST default to injected configurations for smaller/simpler services to avoid hard operational dependencies.
- The AI MUST name configuration properties based on their *function* in the system, not their technical *nature* (e.g., use `authenticationProvider` instead of `hostname`).

**Transparency & Logging Rules**
- The AI MUST separate monitoring logic from application logic. Thresholds, alerting rules, and health roll-ups MUST be maintained in external monitoring tools (the "exoskeleton"), not hardcoded in the application.
- The AI MUST NOT place log files inside the application's installation directory. Log file paths MUST be configurable and default to a separate drive, filesystem, or standard output (for containers).
- The AI MUST restrict the use of the `ERROR` or `SEVERE` log level strictly to system problems that require immediate action by operations (e.g., database connection failure, tripped circuit breaker).
- The AI MUST NOT log business logic exceptions or bad user input (e.g., invalid credit card, missing parameters) as `ERROR`. These MUST be logged as `WARN` or `INFO`.
- The AI MUST structure log outputs to be highly human-readable, avoiding ragged left-to-right scanning patterns.
- The AI MUST inject a greppable identifier (e.g., user ID, session ID, transaction ID) into log messages to allow operators to trace a transaction across the system.
- The AI MUST log all interesting state transitions within the application.

**Health Check Rules**
- The AI MUST implement a dedicated endpoint (e.g., `/health`) that reveals the application's internal view of its own health to be consumed by load balancers.
- A generated health check MUST report the following data points:
  1. The host IP address(es).
  2. The version number of the runtime/interpreter.
  3. The application version or commit ID.
  4. A boolean flag indicating whether the instance is ready to accept work.
  5. The status of internal connection pools, caches, and circuit breakers.

@Workflow
1. **Build & Package Validation**: When generating build scripts, verify that the environment is a CI server, dependencies are securely sourced, and debug logging is disabled. Package the output as an immutable artifact (e.g., Docker image).
2. **Configuration Extraction**: Scan the application code for hardcoded environment settings, credentials, or poorly named properties. Extract these into external environment variables and rename them based on business function.
3. **Log Formatting Setup**: Implement a logging framework configuration that routes logs outside the app directory, includes a transaction ID in the pattern, and strictly enforces the `ERROR` level rule.
4. **Health Check Implementation**: Generate a comprehensive health check route that aggregates the status of the host, runtime, application version, and critical internal resources (pools/circuit breakers).
5. **Deployment Generation**: Output infrastructure-as-code that provisions the artifact as a disposable instance, injecting the extracted configuration at runtime.

@Examples (Do's and Don'Don'ts)

**Configuration Naming**
- [DO]: `export EXTERNAL_PAYMENT_GATEWAY_URL="https://..."`
- [DON'T]: `export HOSTNAME="https://..."` (Ambiguous: is this the local host or a remote host?)

**Logging Levels**
- [DO]: `logger.warn("User attempted checkout with invalid credit card format.");`
- [DON'T]: `logger.error("User attempted checkout with invalid credit card format.");` (This is a user error, not a system failure requiring operator intervention).
- [DO]: `logger.error("Failed to acquire connection to database from pool.");`

**Log Readability & Traceability**
- [DO]: `[2023-10-25 14:32:01] [INFO] [TxID: 987234] [OrderService] State transition: PENDING -> FULFILLED`
- [DON'T]: `Exception caught. State changed. null pointer.` (Missing context, ragged format, no transaction ID).

**Health Checks**
- [DO]: 
```json
{
  "status": "UP",
  "accepting_work": true,
  "app_version": "a1b2c3d",
  "runtime_version": "Node.js 18.x",
  "host_ip": "10.0.1.45",
  "resources": {
    "db_pool": "connected",
    "payment_circuit_breaker": "closed"
  }
}
```
- [DON'T]: 
```json
{
  "status": "OK"
}
```
(Insufficient data for operators to understand instance context).

**Deployment Patterns**
- [DO]: Write a Terraform/Kubernetes script that spins up a new pod with the `v2` image and tears down the `v1` pod.
- [DON'T]: Write a Bash script that SSHs into a production server, runs `git pull`, and restarts the service.