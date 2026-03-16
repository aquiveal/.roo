# @Domain
Trigger these rules when the user requests tasks related to infrastructure architecture, network configuration, load balancing setup, service discovery implementation, traffic management, DNS configuration, software-defined networking (SDN), or writing client/server code that handles API connections, routing, and demand control.

# @Vocabulary
- **Interconnect**: The layer of mechanisms (load balancing, routing, discovery) that knits individual application instances into a cohesive, highly available system.
- **FQDN (Fully Qualified Domain Name)**: The complete domain name for a specific computer or host on the internet.
- **DNS Round-Robin**: A primitive load-balancing technique utilizing DNS to return multiple IP addresses for a single hostname.
- **GSLB (Global Server Load Balancing)**: Traffic management across multiple geographic locations utilizing specialized DNS servers that monitor pool health.
- **VIP (Virtual IP)**: An IP address not strictly tied to a single physical machine or MAC address; used by load balancers to multiplex services or by cluster servers for high-availability failover.
- **Reverse Proxy**: A software load balancer (e.g., Squid, HAProxy, nginx) that demultiplexes calls coming into a single IP address and fans them out to multiple addresses.
- **Session Stickiness**: A load balancer configuration that directs repeated requests from a client to the same backend instance to utilize in-memory state.
- **Content-Based Routing**: Partitioning traffic to different load-balancer pools based on URL patterns or request contents.
- **Listen Queue**: The OS-level queue where TCP connection requests wait after the three-way handshake until the application calls `accept()`.
- **Residence Time**: The total time a request spends in the system, calculated as queue time plus processing time.
- **Bogon**: A delayed, stray packet left over from an old connection that arrives after the socket is closed.
- **TIME_WAIT**: A TCP socket state that prevents immediate reuse of a port to defend against bogons.
- **SDN (Software-Defined Networking)**: A virtualized network infrastructure using VXLANs and software switches to create isolated networks for containers/VMs on shared physical wires.
- **Migratory VIP**: An IP address in an active/passive cluster that moves to a failover node when the primary node fails.

# @Objectives
- Connect standalone application instances into resilient, cohesive systems.
- Match the scale and dynamism of interconnect tooling to the organization's size and operational maturity.
- Prevent catastrophic system failure by aggressively shedding load at the network edge before resources are exhausted.
- Abstract physical infrastructure from application code using logical DNS aliases, VIPs, and dynamic service discovery.
- Protect data security by explicitly routing sensitive traffic and isolating network interfaces.

# @Guidelines

### 1. Tooling and Scale Selection
- The AI MUST match interconnect solutions to the organizational scale.
- For small teams/static infrastructure: Use DNS, configuration files, and software load balancers.
- For large teams/dynamic environments (e.g., containers/microservices): Use dynamic service discovery (e.g., Consul, etcd) and platform-native routing.

### 2. DNS Architecture
- The AI MUST define logical service names (aliases) rather than exposing physical hostnames to consumers.
- The AI MUST NOT use DNS round-robin for long-running enterprise systems (e.g., Java applications), as built-in DNS caching defeats load balancing.
- The AI MUST use Global Server Load Balancing (GSLB) to route requests geographically, ensuring GSLB only returns IPs for pools passing health checks.
- The AI MUST enforce DNS provider diversity. NEVER host DNS on the same infrastructure as production systems, and use a separate DNS provider for public status pages.

### 3. Load Balancing Implementation
- The AI MUST abstract all backend instances behind a Virtual IP (VIP).
- The AI MUST configure backend instances to generate self-referential URLs using the VIP's DNS name, NEVER their local hostname.
- The AI MUST configure software load balancers (reverse proxies) to append the `X-Forwarded-For` header so applications can log true client IPs.
- The AI MUST define deep health checks for load balancers. Health checks MUST verify critical dependencies (database connection pools, caches, circuit breakers) rather than just confirming a port is open.
- The AI MUST evaluate the risks of Session Stickiness. If required, implement via injected cookies rather than IP hashing (which breaks behind proxies), but warn that stickiness can unbalance cluster load.

### 4. Demand Control & Load Shedding
- The AI MUST implement load shedding as close to the network edge as possible to prevent resource exhaustion.
- When an instance cannot meet its SLA, the AI MUST configure it to fail health checks or actively return `HTTP 503 Service Unavailable` so the load balancer can immediately reject or redirect traffic.
- The AI MUST NOT allow infinite or excessively long listen queues. Queue lengths MUST be bounded to prevent residence time from exceeding caller timeouts.
- Under heavy load, the AI MUST implement a "listen queue purge" pattern—a tight loop that accepts connections and immediately returns a static 503 response.
- For purely internal, secure data center traffic, the AI MUST reduce `TIME_WAIT` duration (e.g., via `tcp_tw_reuse`) to rapidly free up ephemeral sockets.

### 5. Network Routing and Interfaces
- The AI MUST configure applications to explicitly bind to specific network interfaces (NICs) configured via environment/properties, NEVER defaulting to `0.0.0.0` (all interfaces).
- The AI MUST use static route definitions for sensitive connections (e.g., partner integrations over VPN) to prevent default gateway race conditions from leaking PII onto public interfaces.
- The AI MUST document every external route, destination name, and IP address for firewall rule provisioning.

### 6. Service Discovery
- The AI MUST NEVER roll a custom service discovery mechanism.
- If using ZooKeeper (CP), the AI MUST implement client-side caching of discovery lookups to maintain availability during network partitions.
- If using Consul (AP), the AI MUST configure consumers to handle potentially stale endpoint data gracefully.

### 7. Migratory VIP Failover Handling
- The AI MUST design clients connecting to Migratory VIPs (e.g., active/passive databases) to expect and safely handle `SQLException` or `IOException` when TCP state is lost during a failover.
- The AI MUST NOT implement updates/inserts automatically upon connection drops; transactions must roll back cleanly, and applications must utilize circuit breakers before retrying.

# @Workflow
1. **Analyze Environment and Scale**: Determine if the deployment target is a static data center (favor DNS/static configs) or a dynamic cloud/container environment (favor SDN, Service Discovery, PaaS routing).
2. **Design DNS & Aliasing**: Define logical DNS names for all services. Map these to GSLB or Load Balancer VIPs. Verify DNS infrastructure diversity.
3. **Configure Load Balancing**:
   - Define VIPs and instance pools.
   - Write deep health check endpoints in the application code.
   - Configure the LB to query the health check and remove instances returning non-200 responses.
   - Add `X-Forwarded-For` injection.
4. **Implement Demand Control**:
   - Calculate acceptable residence time based on client timeouts.
   - Configure connection limits and listen queue bounds in the application server.
   - Implement `HTTP 503` fast-failure responses for overloaded states.
5. **Secure Routing & Binding**:
   - Expose configuration properties for the application to bind to specific NICs.
   - Identify sensitive outbound integration points and define static routes.
6. **Integrate Discovery & Failover**:
   - Connect the application to the Service Discovery registry (if applicable).
   - Implement client-side caching for discovery lookups.
   - Wrap all stateful/database connections in try/catch blocks that handle Migratory VIP connection resets, coupled with Circuit Breaker patterns.

# @Examples (Do's and Don'ts)

### DNS and Addressing
- **[DO]** Use logical DNS aliases representing the service: `db-primary.example.com` or `shipping-api.internal`.
- **[DON'T]** Hardcode physical hostnames into application configuration: `us-east-srv-014.example.com`.

### Health Checks
- **[DO]** Write an application health check that validates dependencies:
  ```json
  // GET /health
  {
    "status": "UP",
    "db_pool": "nominal",
    "circuit_breakers": "closed",
    "version": "1.4.2"
  }
  ```
- **[DON'T]** Use a static HTML file or a shallow TCP ping to port 8080 as a load balancer health check.

### Demand Control
- **[DO]** Track request response times and shed load actively:
  ```java
  if (averageResponseTime > SLA_TIMEOUT) {
      return new HttpResponse(503, "Service Overloaded - Try Again Later");
  }
  ```
- **[DON'T]** Accept infinite connections into an unbounded thread pool or listen queue, which causes the application to silently lock up.

### Application Network Binding
- **[DO]** Bind servers explicitly to configured interfaces:
  ```go
  // Good approach
  host := os.Getenv("BIND_HOST") // e.g., 10.0.1.5
  ln, err := net.Listen("tcp", host+":8080")
  ```
- **[DON'T]** Listen on all interfaces blindly, exposing admin panels to public NICs:
  ```go
  // Bad approach
  ln, err := net.Listen("tcp", ":8080") // Binds to 0.0.0.0
  ```

### Migratory VIP Failover
- **[DO]** Catch and handle network-level resets gracefully, assuming connection state is lost when a database VIP fails over to a secondary node.
- **[DON'T]** Assume a TCP connection remains valid infinitely just because no packets have actively failed.