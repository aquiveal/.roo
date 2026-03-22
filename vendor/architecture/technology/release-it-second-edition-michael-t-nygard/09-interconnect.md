# @Domain
Activation conditions: Triggers when the AI is configuring, designing, or debugging network communications between services, load balancing, DNS, service discovery, traffic management, network routing, demand control, or distributed system interconnects.

# @Vocabulary
*   **Interconnect Layer**: The networking and communication mechanisms that knit multiple standalone instances together into a highly available, cohesive system.
*   **DNS Round-Robin**: Application-layer (Layer 7) load balancing via DNS address resolution that maps a single hostname to multiple IP addresses.
*   **GSLB (Global Server Load Balancing)**: Geographic routing using specialized DNS servers that monitor pool health and return localized or available IP addresses for disaster recovery and latency reduction.
*   **VIP (Virtual IP)**: An IP address bound to a load balancer that fronts a pool of instances, or a migratory IP address that moves between cluster nodes for failover.
*   **Reverse Proxy Server**: A software load balancer (e.g., HAProxy, Nginx) that demultiplexes incoming calls from a single IP and fans them out to multiple backend addresses.
*   **Hardware Load Balancer**: Specialized, high-throughput network devices operating at Layers 4 through 7 to manage and route traffic.
*   **Health Check**: An endpoint provided by an instance that load balancers poll to determine if the instance is healthy and capable of accepting work.
*   **Stickiness (Session Affinity)**: The routing of repeated client requests to the exact same backend instance to preserve state, typically implemented via cookies or IP hashing.
*   **Content-Based Routing**: Directing traffic to different backend pools based on the URL or request payload.
*   **Load Shedding**: The practice of actively refusing incoming work (e.g., returning HTTP 503) when a system is near or at capacity to prevent non-linear performance degradation.
*   **Listen Queue**: A TCP queue holding connection requests that have completed the three-way handshake but have not yet been accepted by the application thread.
*   **Residence Time**: The total time a request spends in the system, encompassing both time spent in the listen queue and actual processing time.
*   **Bogon**: A delayed network packet from a previously closed connection that arrives out-of-sequence; mitigated by the TCP TIME_WAIT state.
*   **Static Route Definition**: Hardcoded network routes used to prevent ambiguous default gateway routing when multiple paths (e.g., VPN vs. public switch) exist.
*   **SDN (Software-Defined Networking)**: Virtual network overlays utilizing virtual IPs, VLAN tags, and software switches to operate independently of physical hardware constraints.
*   **Migratory Virtual IP**: An IP address mapped dynamically via ARP updates to a standby machine (e.g., in an Active/Passive database cluster) when the primary machine fails.

# @Objectives
*   Knit individual service instances into a highly available, resilient, and transparent system.
*   Distribute workload efficiently and safely using the appropriate scale of load balancing and discovery tools.
*   Protect systems from internet-scale traffic floods and internal cascading failures through aggressive demand control and load shedding.
*   Ensure deterministic, secure routing of sensitive data across multi-homed internal networks.
*   Prevent single points of failure in service communication through defensive programming and dynamic discovery.

# @Guidelines
*   **Interconnect Selection**: Match the interconnect mechanism to the organization's scale and rate of change. Use DNS for stable/static infrastructure. Use dynamic Service Discovery (Consul, ZooKeeper, etcd) for highly dynamic, ephemeral container/cloud environments.
*   **DNS Management**:
    *   Never hardcode physical hostnames. Always use logical aliases (CNAMEs).
    *   Maintain DNS infrastructure diversity. Do not host DNS servers on the same infrastructure as production systems. Ensure no single failure scenario eliminates all DNS servers.
    *   Use GSLB to route traffic across multiple geographic locations. GSLB servers MUST monitor the health of local traffic managers/load balancer pools before resolving addresses.
*   **Load Balancing**:
    *   Hide backend instances completely. Calling applications MUST NOT be aware of the load balancer's presence.
    *   Configure backend services to generate URLs using the VIP's DNS name, not their own internal hostnames.
    *   When using software load balancers (reverse proxies), rely on the `X-Forwarded-For` HTTP header for client IP logging.
    *   Use Cookie-based stickiness for session affinity. Do NOT use Client IP hashing, as it breaks behind outbound proxies (e.g., corporate NATs).
    *   Use Content-Based routing to partition work (e.g., isolate slow search queries from fast sign-up queries onto different instance pools).
*   **Health Checks**:
    *   Implement comprehensive, active health checks on every instance.
    *   Health checks MUST report the application version, runtime version, host IP, connection pool state, cache state, circuit breaker status, and readiness to accept work.
    *   Instances MUST boot with an "unavailable" status and only switch to "available" when fully warmed up (caches loaded, JIT warmed).
*   **Demand Control & Load Shedding**:
    *   Reject unserviceable work as close to the network edge as possible.
    *   Monitor the application's SLA internally. If response times exceed the SLA, the health check MUST return HTTP 503 to signal the load balancer to stop sending traffic.
    *   Keep TCP listen queues short to prevent excessive Residence Time. Formula for queue length: `((Max Wait Time / Mean Processing Time) + 1) * Request Handling Threads * 1.5`.
    *   Implement a "Listen Queue Purge" (a fast loop returning a hardcoded HTTP 503 string) during extreme overloads to immediately shed excess connections.
*   **TCP Configuration**:
    *   For internal data center traffic where bogons are a low risk, configure a low `TIME_WAIT` interval to free ephemeral sockets quickly.
    *   In Linux, enable `tcp_tw_reuse` and appropriately reduce the packet Time-To-Live (TTL).
*   **Network Routing**:
    *   Never rely exclusively on OS default gateway routing for multi-homed machines handling sensitive data (PII).
    *   Explicitly configure Static Route Definitions or leverage SDN to force sensitive traffic over secure interfaces (e.g., VPNs) and prevent accidental leakage over public-facing switches due to unreliable interface enumeration (e.g., eth0 vs eth1 swapping).
*   **Service Discovery**:
    *   Do NOT build custom service discovery mechanisms. Use established, battle-tested tools (Consul, ZooKeeper, etcd) or native PaaS control planes (Kubernetes, Docker Swarm).
    *   Client applications MUST cache service discovery lookups locally to survive temporary partitions from the discovery service.
*   **Migratory Virtual IPs**:
    *   Applications connecting to clustered resources (like Active/Passive databases) via a migratory VIP MUST anticipate ungraceful connection drops during failovers.
    *   Write robust exception handling for `IOException` and `SQLException` to catch failover events.
    *   Implement bounded, circuit-broken retry logic against the VIP to reconnect once the new node claims the IP and MAC via ARP broadcast.

# @Workflow
1.  **Evaluate Infrastructure Scale**: Assess the deployment environment. For static VMs/Bare Metal, implement DNS CNAMEs and Load Balancers. For containers/cloud, integrate native Service Discovery mechanisms.
2.  **Configure Naming & Routing**: Establish logical DNS aliases for all services. If spanning multiple data centers, configure GSLB to route to local Virtual IPs (VIPs).
3.  **Establish the Load Balancing Tier**: Define the load balancer pools. Assign VIPs to software (HAProxy/Nginx) or hardware load balancers. Configure content-based routing rules and session stickiness via cookies if required.
4.  **Implement Health Checks**: Code deep health check endpoints (`/health` or `/status`) in the application that evaluate internal resource exhaustion (DB pools, caches) and boot readiness.
5.  **Configure Demand Control**: Set operating system TCP settings (`TIME_WAIT`, `tcp_tw_reuse`). Calculate and set the application listen queue length based on the specified SLA formula.
6.  **Implement Load Shedding**: Tie the health check to the SLA. If the moving average of response times exceeds the SLA, trigger the health check to return `503 Service Unavailable` so the load balancer drops the instance from the active pool temporarily.
7.  **Secure Network Routes**: Audit the routing table. If integrating with third parties or transmitting PII, hardcode static routes or configure SDN rules to guarantee traffic flows over the correct NIC/VPN.
8.  **Write Failover Logic**: Wrap database and external service client calls in connection-drop handling logic. Implement bounded retries to survive Migratory VIP handoffs.

# @Examples (Do's and Don'ts)

**DNS & Service Naming**
*   [DO]: Connect to a database using a logical alias: `jdbc:oracle:thin:@db-orders-primary.internal.example.com:1521/ORCL`
*   [DON'T]: Hardcode physical machine names: `jdbc:oracle:thin:@server-rack4-node12.example.com:1521/ORCL`

**Load Balancing & Stickiness**
*   [DO]: Configure the load balancer to inject a routing cookie (e.g., `Set-Cookie: SERVERID=instance_A`) and route subsequent requests containing that cookie to `instance_A`.
*   [DON'T]: Configure the load balancer to hash the Client IP address to assign backend instances, causing all users behind a corporate NAT proxy to overwhelm a single instance.

**Demand Control & Health Checks**
*   [DO]: Return an HTTP 503 from the `/health` endpoint when the database connection pool is exhausted or the average response time exceeds 100ms.
*   [DON'T]: Allow the listen queue to grow infinitely, leaving clients waiting for minutes before eventually timing out locally.

**TCP Settings (Internal Traffic)**
*   [DO]: Configure sysctl settings for internal microservices to aggressively recycle sockets: `sysctl -w net.ipv4.tcp_tw_reuse=1`.
*   [DON'T]: Leave default `TIME_WAIT` settings (e.g., 60 seconds) on high-throughput internal API nodes, leading to port exhaustion.

**Handling Migratory VIPs**
*   [DO]: Wrap the DB connection checkout in a try-catch block for `SQLException`. If a connection drop is detected, back off for a randomized interval, and retry acquiring a new connection from the VIP.
*   [DON'T]: Assume a TCP connection will live forever. Let the application crash permanently when the database cluster fails over to a secondary node.