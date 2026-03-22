@Domain
These rules are triggered whenever the AI is tasked with designing, architecting, implementing, or configuring software intended for production deployment. This includes containerization (Docker, Kubernetes), virtual machine provisioning, continuous integration/continuous deployment (CI/CD) pipelines, logging, monitoring and telemetry frameworks, API gateway configurations, network socket bindings, load balancing, health checks, and security implementations (OWASP mitigation, authentication, secrets management).

@Vocabulary
- **Fully Qualified Domain Name (FQDN):** The concatenation of a machine's hostname and its default search domain.
- **Multihoming:** The presence of multiple network interface controllers (NICs) on a single machine, often separating public, administrative, and backup networks.
- **Virtual IP (VIP):** An IP address that is not strictly tied to a specific hardware Ethernet MAC address, used for load balancing or failover.
- **Immutable Infrastructure:** A deployment strategy where servers or containers are never modified after deployment. If changes are needed, a new image is built and deployed.
- **12-Factor App:** A methodology for building software-as-a-service apps that use declarative formats, store config in the environment, and treat backing services as attached resources.
- **Reverse Proxy:** A server that demultiplexes calls coming into a single IP address and fans them out to multiple addresses (e.g., HAProxy, Nginx).
- **Load Shedding:** The practice of deliberately refusing new requests when a system is nearing capacity to preserve the ability to process existing requests.
- **Control Plane:** The software and services that run in the background to manage, monitor, scale, and configure production software.
- **Governor:** A stateful, time-aware mechanism that limits the speed/rate of automated actions (e.g., shutting down instances) to prevent runaway automation disasters.
- **RUM (Real-User Monitoring):** Direct measurement of user experience from the client/browser side, rather than relying solely on server-side metrics.
- **XXE (XML External Entity):** An injection vulnerability where XML parsers evaluate external entities, potentially exposing local files or internal networks.
- **XSS (Cross-Site Scripting):** A vulnerability where unescaped user input is rendered into HTML, allowing script execution in the client's browser.
- **CSRF (Cross-Site Request Forgery):** An attack where a malicious site tricks a user's browser into executing unwanted actions on a trusted site where the user is authenticated.
- **Bogon:** A stray, delayed packet from a closed TCP connection that can corrupt a reused socket if `TIME_WAIT` is not respected or properly managed.

@Objectives
- Ensure all instances behave as well-behaved citizens within a complex, multihomed, and distributed production network.
- Enforce the principles of Immutable Infrastructure, strictly separating code, configuration, and state.
- Maximize system-wide transparency through rigorous, actionable logging, metrics exposure, and deep health checks.
- Prevent systemic collapse under excessive demand by implementing aggressive demand control, short listen queues, and load shedding.
- Secure the application against all OWASP Top 10 vulnerabilities, enforce the Principle of Least Privilege, and safely manage cryptographic secrets.
- Provide operators with safe, scriptable mechanisms (Control Plane) to intervene in system behavior without requiring code deployments or restarts.

@Guidelines

**Networking and Socket Binding**
- AI MUST NOT bind sockets to all network interfaces (e.g., `0.0.0.0`) by default.
- AI MUST use specific, configurable IP addresses or hostnames for socket bindings to accommodate multihomed environments (separating public, administrative, and backup traffic).
- AI MUST handle `IOException` and related network errors gracefully when calling migratory Virtual IPs, immediately attempting safe retries to the new endpoint.
- AI MUST NOT embed IP addresses or physical hostnames inside container images or executables. All network routing targets MUST be provided via external configuration.

**Configuration and Immutable Infrastructure**
- AI MUST treat container images and VM images as disposable and immutable. AI MUST NOT write scripts or code that attempts to patch or update a running container.
- AI MUST extract all per-environment configurations out of the codebase.
- AI MUST inject configuration via environment variables, text blobs (e.g., AWS User Data), or a dedicated configuration service (e.g., Consul, etcd).
- AI MUST NOT store passwords, API keys, or production secrets in version control.
- AI MUST ensure application startup times are as fast as possible (target <1 second for containers) to support rapid elastic scaling.

**Transparency, Logging, and Metrics**
- AI MUST output logs to a configurable directory distinct from the application installation directory, or to `stdout` for containerized environments.
- AI MUST include tracing identifiers (e.g., Session ID, Transaction ID) in every log message to facilitate grep/search across distributed requests.
- AI MUST reserve the `ERROR` or `SEVERE` log levels EXCLUSIVELY for system problems that require immediate operator action (e.g., database connection loss, circuit breaker trips).
- AI MUST NOT log business logic exceptions or bad user input (e.g., invalid credit cards, missing fields) as `ERROR`. Log these as `WARNING` or `INFO`.
- AI MUST NOT output debug or trace logs in production configurations.
- AI MUST expose internal application metrics, specifically: request throughput, response latency, resource pool health (active/waiting threads), cache hit rates, and integration point timeouts.

**Load Balancing and Health Checks**
- AI MUST implement a dedicated, deep health check endpoint for every service.
- AI MUST ensure the health check verifies the runtime version, application version, database connectivity, and the state of internal circuit breakers.
- AI MUST configure the health check endpoint to return an HTTP `503 Service Unavailable` status when the instance is starting up, shutting down, or overloaded, instructing the load balancer to route traffic elsewhere.
- AI MUST ensure web applications parsing client IPs properly evaluate the `X-Forwarded-For` header when placed behind a reverse proxy.

**Demand Control and Load Shedding**
- AI MUST implement load shedding at the network edge or application boundary. If a service calculates that its response time will exceed the SLA (due to queue depth or resource exhaustion), it MUST immediately return an HTTP `503` rather than making the client wait.
- AI MUST limit the length of socket listen queues based on the maximum acceptable residence time.
- AI MUST explicitly set network read and write timeouts to prevent TCP buffer exhaustion and blocked threads during high load.

**Control Plane and Automation Safety**
- AI MUST expose a scriptable administrative API (e.g., over a separate port/network interface) for live control operations like adjusting connection pools, toggling features, and resetting circuit breakers.
- AI MUST NOT build GUIs for routine operational tasks; prioritize CLIs and API endpoints.
- AI MUST implement a "Governor" pattern for automated destructive actions (e.g., scaling down, deleting records). If an automated system attempts to delete >50% of capacity, the AI MUST require manual human override.
- AI MUST ensure services can start and operate safely even if the centralized configuration service is temporarily partitioned or unavailable.

**Security and Attack Protection**
- AI MUST use parameterized queries (e.g., `PreparedStatement`) for all database interactions to prevent SQL Injection. AI MUST NEVER concatenate user input into database queries.
- AI MUST explicitly configure XML parsers to disable external entities (XXE) and DTD processing.
- AI MUST manage session IDs securely: generate IDs using cryptographically secure PRNGs, require a fresh session ID upon authentication, and transmit session IDs ONLY via secure cookies (never in URLs).
- AI MUST scrub and escape all user input before rendering it in UI components to prevent XSS.
- AI MUST verify authorization on EVERY object access request. Do not rely on obscured URLs.
- AI MUST return a `404 Not Found` (rather than `403 Forbidden`) if an unauthorized user attempts to access an existing object to prevent information leakage via URL probing.
- AI MUST map uploaded files to randomly generated internal filenames. AI MUST NEVER use user-supplied filenames for filesystem storage to prevent directory traversal.
- AI MUST NOT configure or deploy servers with default admin credentials.
- AI MUST implement CSRF protection using anti-CSRF tokens and/or the `SameSite=strict` cookie attribute for state-changing requests.
- AI MUST ensure decryption of sensitive data relies on the authenticated user's authorization, not the server's global permissions.

@Workflow
1. **Infrastructure Definition:** Define the deployment target (Container, VM, Physical). Extract all environmental configurations into environment variables or injected files. Remove all hardcoded IP addresses or environment-specific hostnames.
2. **Network and Routing:** Define specific network bindings. Ensure administrative and public endpoints are bound to separate, configurable interfaces. Implement load balancer compatibility (e.g., `X-Forwarded-For`).
3. **Telemetry Integration:** Add structured logging with correlation IDs. Separate user/business errors from system-level `ERROR` logs. Implement a comprehensive `/health` endpoint that checks all backing services.
4. **Resilience and Demand Control:** Add timeout parameters to all external calls. Implement load-shedding logic that returns `503` responses immediately when thread pools or listen queues are saturated.
5. **Security Hardening:** Review all input parsing (SQL, XML, JSON). Apply parameterized queries, disable XML external entities, secure session cookie configurations (`HttpOnly`, `Secure`, `SameSite`), and ensure uploaded files are completely decoupled from filesystem paths.
6. **Control Surface Provisioning:** Expose a secure, scriptable administrative API on the internal network interface for live operational control without requiring instance reboots.

@Examples (Do's and Don'ts)

**Socket Binding**
- [DO] `server.listen(config.get("PRODUCTION_BIND_IP"), config.get("PORT"))`
- [DON'T] `server.listen("0.0.0.0", 8080)` (Binds to all interfaces, exposing administrative ports to public networks).

**Logging Levels**
- [DO] `logger.warn("User {id} failed checkout: Insufficient funds")`
- [DON'T] `logger.error("User {id} failed checkout: Insufficient funds")` (Wastes operator time and triggers false alarms).
- [DO] `logger.error("Transaction {id} failed: Database connection pool exhausted")`

**Database Queries**
- [DO] `db.execute("SELECT * FROM users WHERE email = ?", [userInputEmail])`
- [DON'T] `db.execute("SELECT * FROM users WHERE email = '" + userInputEmail + "'")` (Vulnerable to SQL Injection).

**Session Management**
- [DO] `response.setHeader("Set-Cookie", "session_id=randomCryptoHash; Secure; HttpOnly; SameSite=Strict")`
- [DON'T] `response.redirect("/dashboard?session_id=" + sessionId)` (Vulnerable to session hijacking and leakage via Referer headers).

**XML Parsing**
- [DO] `DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance(); dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);`
- [DON'T] `DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance(); Document doc = dbf.newDocumentBuilder().parse(inputStream);` (Vulnerable to XXE Injection).

**File Uploads**
- [DO] `String internalName = UUID.randomUUID().toString(); storage.save(internalName, fileStream); db.saveMapping(userInputName, internalName);`
- [DON'T] `storage.save("/var/uploads/" + userInputName, fileStream);` (Vulnerable to Directory Traversal via `../../`).

**Health Checks**
- [DO] Define a health check that verifies the DB connection pool is not exhausted, checks the status of internal circuit breakers, and returns `503` if the system is intentionally draining connections.
- [DON'T] Return `200 OK` simply because the HTTP server process is running, while the underlying database connection is dead.