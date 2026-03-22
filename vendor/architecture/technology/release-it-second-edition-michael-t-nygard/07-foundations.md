## @Domain
These rules MUST trigger when the AI is performing tasks, generating code, or reviewing architecture related to server initialization, network socket binding, containerization (e.g., Dockerfiles), cloud provisioning (e.g., Terraform, AWS, Kubernetes), configuration management, logging/telemetry setup, and distributed system deployment. 

## @Vocabulary
*   **Design for Production**: The engineering practice of treating production environments, operations personnel, and physical/virtual infrastructure constraints as first-class architectural concerns.
*   **FQDN (Fully Qualified Domain Name)**: The concatenation of a machine's internal OS hostname and its default search domain. Crucially, this often differs from the external DNS name.
*   **Multihoming**: The practice of equipping a server with multiple Network Interface Controllers (NICs), typically used to separate production traffic, administrative access, and backend/backup traffic.
*   **Bonding / Teaming**: Configuring two or more network interfaces to share a common IP address for redundancy and failover.
*   **Oversubscription**: A virtualized environment state where the total allocated resources (CPU/RAM) across VMs exceed the physical host's capacity, leading to unpredictable contention and latency.
*   **Overlay Network**: A virtual network (often using VLANs or VXLANs) built on top of physical networks, commonly used in containerized environments to provide isolated IP spaces and software switching.
*   **12-Factor App**: A methodology for building cloud-native, scalable, and deployable applications emphasizing statelessness, environment-based config, and attached backing services.
*   **Ephemeral Identity**: The characteristic of cloud VMs and containers where IP addresses, hostnames, and local storage are short-lived and change upon every boot/restart.
*   **Bastion / Jumphost**: A dedicated server providing the sole administrative entry point (e.g., SSH) into a private network, protecting production interfaces from direct public administrative access.

## @Objectives
*   The AI MUST ensure applications treat operations personnel as primary users by exposing transparent logging, telemetry, and configuration interfaces.
*   The AI MUST decouple applications from underlying physical infrastructure, ensuring safe operation within highly ephemeral, virtualized, or containerized environments.
*   The AI MUST safeguard networking by explicitly defining socket bindings, segregating traffic types, and preventing unintended administrative exposure.
*   The AI MUST guarantee rapid startup times, stateless processing, and strict separation of configuration from code.

## @Guidelines

### 1. Networking and Socket Binding
*   **Explicit Interface Binding**: When writing server initialization code, the AI MUST NOT bind sockets to all interfaces (e.g., `0.0.0.0`, `""`, or `INADDR_ANY`). The AI MUST require the application to read the specific IP address or FQDN to bind to from an external configuration source.
*   **Traffic Segregation**: The AI MUST architect services to support multihoming by allowing different ports and services (e.g., admin panels vs. public APIs) to be bound to different network interfaces.
*   **DNS vs. Hostname Awareness**: The AI MUST NOT assume a machine's local OS hostname resolves to its public DNS name. Code MUST rely on injected configuration for external URLs and self-referential links.
*   **Outbound Routing Limits**: For systems utilizing NIC bonding, the AI MUST ensure routing tables or OS configurations explicitly define a default gateway to prevent outbound connection failures.

### 2. Virtualization and Clocks
*   **Clock Skew Tolerance**: The AI MUST NOT rely on the OS clock for monotonic or strictly sequential timing, as virtual machine suspension and migration cause arbitrary clock jumps. For precise intervals, the AI MUST utilize monotonic clock APIs (if language-supported) or rely on external NTP-synced authoritative time sources.
*   **Contention Resilience**: The AI MUST implement robust timeouts and retries (with backoff) to handle sudden, random latency spikes caused by physical host resource oversubscription.
*   **Avoid Single Points of Failure**: The AI MUST NOT design architectures that rely on a single, statically configured "special" machine (e.g., a centralized lock manager or cluster manager) without automated failover and dynamic leader election.

### 3. Containerization
*   **Externalized State**: The AI MUST NOT write code that stores persistent data, cached data, or stateful session data on the local container filesystem. All state MUST be outsourced to attached backing services (e.g., databases, Redis, SAN/NAS).
*   **Credential Management**: The AI MUST NOT hardcode or bake production passwords, API keys, or certificates into container images. The AI MUST design the application to retrieve credentials securely at runtime via environment variables or a secure password vaulting service.
*   **Network Abstraction**: The AI MUST NOT hardcode hostnames or port numbers into container images. All network topology MUST be injected by the container orchestration control plane at startup.
*   **Rapid Startup**: The AI MUST optimize application startup routines to execute in under one second. The AI MUST NOT block application readiness with synchronous, long-running cache warming or extensive reference data loading during boot.
*   **Telemetry Routing**: The AI MUST write applications to stream logs and telemetry directly to standard output/error (or a centralized data collector). The AI MUST NOT write logs to local flat files that require manual retrieval from inside the container.

### 4. Cloud Environments and 12-Factor Compliance
*   **Ephemeral Adaptation**: The AI MUST ensure applications do not rely on static IP addresses. Instances MUST actively "volunteer" for work by registering with dynamic load balancers, service registries, or competing consumer message queues.
*   **Socket Exhaustion Mitigation**: For high-throughput services, the AI MUST recommend spanning traffic across multiple NICs to bypass the ~64,000 ephemeral socket limit per IP address.
*   **Administrative Isolation**: The AI MUST NOT expose administrative protocols (e.g., SSH, RDP) on public-facing NICs. The AI MUST assume administrative access routes exclusively through an internal Bastion/Jumphost.

## @Workflow
When generating, refactoring, or reviewing server setup and deployment code, the AI MUST execute the following algorithmic process:

1.  **Environment Assessment**: Determine the target deployment model (Physical, VM, Container, or Cloud). Identify constraints regarding network interfaces, storage, and machine lifecycle.
2.  **Network Binding Enforcement**: Scan all network listener initialization code. Reject any bindings to default/global interfaces. Inject configuration properties to specify exact binding addresses.
3.  **State & Secret Extraction**: Audit the codebase for local file writes, hardcoded hostnames, and embedded credentials. Move all state to external backing services and migrate configuration to environment variables/vaults.
4.  **Startup Optimization**: Analyze the application boot sequence. Defer heavy initialization, cache-warming, or batch data loading to asynchronous background processes to ensure sub-second readiness.
5.  **Telemetry Integration**: Verify that logging mechanisms are configured as event streams (stdout/stderr) and that metrics are pushed to external collectors, avoiding local filesystem dependencies.

## @Examples (Do's and Don'ts)

### Network Socket Binding
*   **[DON'T]** Bind a web server to all interfaces indiscriminately.
    ```go
    // ANTI-PATTERN: Binds to all available interfaces, ignoring multihomed security.
    http.ListenAndServe(":8080", mux)
    ```
*   **[DO]** Bind explicitly to a configured address.
    ```go
    // CORRECT: Binds to a specific interface dictated by environment configuration.
    bindAddress := os.Getenv("APP_BIND_ADDRESS") // e.g., "spock.example.com:8080"
    if bindAddress == "" {
        log.Fatal("APP_BIND_ADDRESS environment variable is required")
    }
    http.ListenAndServe(bindAddress, mux)
    ```

### Configuration and Credentials in Containers
*   **[DON'T]** Bake configuration or credentials into a Dockerfile or configuration file included in the image.
    ```dockerfile
    # ANTI-PATTERN: Hardcoding credentials and environment-specific hostnames into the image.
    ENV DB_HOST=production-db.internal.net
    ENV DB_PASSWORD=superSecretProductionPassword!
    COPY prod-config.json /app/config.json
    ```
*   **[DO]** Require configuration to be injected at runtime via the environment or a secure vault.
    ```dockerfile
    # CORRECT: Image remains generic; relies on orchestrator to inject variables at runtime.
    ENTRYPOINT ["./app"]
    # At runtime: docker run -e DB_HOST=$VAULT_DB_HOST -e DB_PASSWORD=$VAULT_DB_PASS myapp
    ```

### Clock Skew and Time Measurement
*   **[DON'T]** Use the system wall-clock time to measure elapsed durations, as VM suspension can cause time jumps.
    ```python
    # ANTI-PATTERN: Wall clock time can jump backwards or forwards unpredictably in VMs.
    import time
    start_time = time.time()
    perform_network_request()
    elapsed = time.time() - start_time
    ```
*   **[DO]** Use monotonic clocks for calculating intervals and durations.
    ```python
    # CORRECT: Monotonic clocks are immune to OS clock adjustments and VM clock skew.
    import time
    start_time = time.monotonic()
    perform_network_request()
    elapsed = time.monotonic() - start_time
    ```

### Machine Identity and Work Volunteering
*   **[DON'T]** Build architectures where a central dispatcher holds a static list of worker IP addresses.
    ```yaml
    # ANTI-PATTERN: Hardcoded IP addresses will break immediately in ephemeral cloud environments.
    workers:
      - 10.0.1.15
      - 10.0.1.16
    ```
*   **[DO]** Implement pattern where workers volunteer by pulling from a queue or registering with a dynamic load balancer.
    ```javascript
    // CORRECT: The ephemeral instance volunteers for work regardless of its current IP.
    const amqp = require('amqplib');
    async function volunteerForWork() {
        const conn = await amqp.connect(process.env.QUEUE_URL);
        const channel = await conn.createChannel();
        channel.consume('work_queue', processJob, { noAck: false });
    }
    ```