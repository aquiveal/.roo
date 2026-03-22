# @Domain
This rule file is activated whenever the AI is tasked with designing application deployment strategies, configuring server instances, creating or modifying CI/CD pipelines, implementing logging and monitoring systems, designing application health checks, or managing application configuration and secrets. 

# @Vocabulary
- **Service**: A collection of processes across machines that work together to deliver a unit of functionality.
- **Instance**: An installation on a single machine (container, virtual, or physical) out of a load-balanced array of the same executable.
- **Executable**: An artifact that a machine can launch as a process, created by a build process (e.g., binaries, or interpreted source plus shared libraries).
- **Process**: An operating system process running on a machine; the runtime image of an executable.
- **Installation**: The executable and any attendant directories, configuration files, and other resources as they exist on a machine.
- **Deployment**: The automated act of creating an installation on a machine using definitions kept in source control.
- **Convergence**: An infrastructure approach that applies scripts/recipes to transition a long-lived machine from an unknown current state to a desired state (e.g., Chef, Puppet). The AI must treat this as an anti-pattern.
- **Immutable Infrastructure**: An infrastructure approach where machines are built from a known base image, deployed, and never patched or updated. To change state, a new image is built, deployed, and the old one is destroyed.
- **Black-box Technology**: A transparency technology that sits outside the process (e.g., a log scraper) to observe behavior.
- **White-box Technology**: A transparency technology integrated directly into the application process (e.g., language-specific agents or metric APIs).
- **Voodoo Operations**: Superstitious or incorrect operator actions resulting from ambiguous, poorly worded, or misleading log messages.

# @Objectives
- Enforce a strict "chain of custody" for code from version control to the production instance, entirely isolating production builds from developer environments.
- Design applications exclusively for Immutable and Disposable Infrastructure, eschewing in-place patching or convergence scripts.
- Decouple all environment-specific configurations and secrets from the deployment artifact.
- Maximize system transparency by engineering instances to explicitly radiate their historical trends, present conditions, instantaneous state, and future projections.
- Expose comprehensive instance health and metrics to facilitate safe load balancing and rapid postmortem analysis.

# @Guidelines

## Code & Build Security
- The AI MUST ensure production builds occur ONLY on a Continuous Integration (CI) server. The AI MUST NOT generate deployment artifacts from developer machines.
- The AI MUST NOT configure production builds to pull dependencies directly from the open internet. Dependencies MUST be pulled from a private, controlled repository.
- The AI MUST implement verification of digital signatures against upstream providers before adding libraries to the private repository.
- The AI MUST explicitly audit and secure CI/CD plugins, treating all build plugins as highly privileged attack vectors.

## Infrastructure & Packaging
- The AI MUST build deployment strategies around Immutable Infrastructure. The AI MUST NOT write scripts intended to patch, update, or modify a running production instance (Convergence).

## Configuration Management
- The AI MUST separate per-environment configuration from the executable. The executable MUST look outside its deployment directory to find configurations.
- The AI MUST NOT store production secrets or passwords in the source control repository.
- The AI MUST supply configuration to ephemeral/disposable instances either via startup injection (environment variables, user data blobs) or a dedicated configuration service (e.g., ZooKeeper, etcd).
- The AI MUST default to injected configurations (env vars) for small teams to avoid the operational overhead and Severity-1 risks associated with managing distributed configuration services.
- The AI MUST name configuration properties based on their *function* rather than their *nature* or data type.

## Transparency & Logging
- The AI MUST configure applications to write log files to a dedicated drive or filesystem, NOT the application installation directory.
- The AI MUST make log file locations configurable. If hardcoded paths are unavoidable, the AI MUST use symlinks to redirect logs to the dedicated volume.
- The AI MUST restrict the `ERROR` or `SEVERE` logging levels EXCLUSIVELY to conditions that require immediate human operator action (e.g., circuit breaker tripped, database connection failed).
- The AI MUST log user-input errors, validation failures, and non-fatal exceptions as `WARNING`, `INFO`, or `DEBUG` (not `ERROR`).
- The AI MUST automate the removal of debug and trace logging configurations during the CI build process to prevent debug logs from reaching production.
- The AI MUST format logs strictly for human readability (e.g., avoiding ragged left-to-right scanning patterns) and use unambiguous language to prevent "Voodoo Operations."
- The AI MUST inject tracing identifiers (User ID, Session ID, Transaction ID, or generated Request ID) into every log message.
- The AI MUST log all internal state transitions (e.g., circuit breaker state changes, cache flushes), even if those transitions are also reported via JMX or APM dashboards.

## Health Checks & Metrics
- The AI MUST implement an end-to-end Health Check API endpoint for every service.
- The AI MUST configure the Health Check endpoint to report the following specific data points:
  1. The host IP address(es).
  2. The version number of the runtime or interpreter.
  3. The application version or commit ID.
  4. A boolean flag indicating whether the instance is currently accepting work.
  5. The detailed status of all connection pools, caches, and circuit breakers.

# @Workflow
1. **Build Pipeline Hardening:** When designing a build, establish a secure CI step that resolves dependencies strictly from a vetted private repository and validates signatures. Ensure a step exists to strip debug/trace logging configurations.
2. **Immutable Packaging:** Package the compiled executable into a base container or virtual machine image. Ensure no mutation scripts (e.g., apt-get update) are run on the artifact post-deployment.
3. **Configuration Interface Design:** Define the configuration interface using environment variables or configuration service lookups. Name all keys functionally.
4. **Log Appender Setup:** Configure the logging framework to write to an externalized, configurable volume path. Define a strict, column-aligned log format that inherently includes a transaction/request ID.
5. **Health Check Implementation:** Expose an HTTP endpoint (e.g., `/health`) that aggregates and returns the application's runtime version, commit ID, network bindings, traffic-acceptance status, and the health of all downstream resource pools and circuit breakers.

# @Examples (Do's and Don'ts)

## Configuration Naming
- **[DO]**: Name a property based on what it does: `AUTHENTICATION_PROVIDER_URL=ldap://...` or `PAYMENT_GATEWAY_HOST=...`
- **[DON'T]**: Name a property based on its type or a generic moniker: `HOSTNAME=...` or `STRING_IP=...`

## Logging Levels
- **[DO]**: `logger.error("Circuit breaker 'InventoryService' tripped to OPEN. Administrator intervention may be required.");`
- **[DON'T]**: `logger.error("NullPointerException: User failed to provide a middle name.");`

## Log File Locations
- **[DO]**: Configure the app to write logs to a dedicated, configurable mount: `/var/log/myapp/` or inject the path via `APP_LOG_PATH=/mnt/logs/`.
- **[DON'T]**: Write logs into the application binary folder: `/opt/myapp/bin/logs/application.log`.

## Health Check Payloads
- **[DO]**: 
  ```json
  {
    "host_ip": "10.0.2.14",
    "runtime_version": "Node.js v18.16.0",
    "commit_id": "a1b2c3d4",
    "accepting_work": true,
    "pools": { "db_connections": { "active": 5, "max": 20 } },
    "circuit_breakers": { "payment_api": "CLOSED" }
  }
  ```
- **[DON'T]**: 
  ```json
  {
    "status": "200 OK"
  }
  ```

## Infrastructure Management
- **[DO]**: Write a Dockerfile or Packer script that builds a static image containing the application, which is then deployed and destroyed when a new version is needed.
- **[DON'T]**: Write an Ansible playbook that SSHs into a running production server to run `git pull`, `npm install`, and restart the service.