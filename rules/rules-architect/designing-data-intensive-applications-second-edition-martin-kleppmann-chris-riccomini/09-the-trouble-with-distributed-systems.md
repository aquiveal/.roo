@Domain
Trigger these rules when designing, implementing, configuring, or troubleshooting distributed systems, microservices architectures, and network communications between services. This includes tasks addressing system overload, network fault tolerance, cross-service data consistency, and distributed observability.

@Vocabulary
- **Distributed System:** A system involving several machines communicating via a network, inherently subject to network delays, interruptions, and partial failures.
- **Node:** An individual process or machine participating in a distributed system.
- **Observability:** Techniques for diagnosing problems in distributed systems by collecting execution data, allowing both high-level metrics and individual events to be analyzed.
- **Tracing Tools:** Infrastructure (e.g., OpenTelemetry, Zipkin, Jaeger) used to track which client called which server for which operation, and how long each call took.
- **Metastable Failure:** A vicious cycle where a system enters an overloaded state, becomes less efficient, and cannot recover even after the initial load is reduced (often requiring a reboot or reset).
- **Retry Storm:** A catastrophic event where delayed responses cause clients to timeout and resend requests, multiplying the load on an already struggling server.
- **Exponential Backoff:** A client-side strategy of increasing the wait time between successive retries to avoid overwhelming a service.
- **Jitter:** Randomization applied to retry intervals to prevent synchronized spikes of retries from multiple clients.
- **Circuit Breaker:** A client-side mechanism that temporarily halts requests to a service that has recently returned errors or timed out.
- **Token Bucket:** An algorithm used for rate limiting and managing the flow of requests.
- **Load Shedding:** A server-side protective measure where the server detects it is approaching overload and proactively rejects incoming requests.
- **Backpressure:** A server-side mechanism of sending responses that explicitly ask clients to slow down their request rate.
- **Split Brain:** A dangerous failure scenario where two nodes simultaneously believe they are the leader, potentially leading to data corruption and conflicting writes.

@Objectives
- Maximize system resilience by assuming all network calls will eventually fail, time out, or be delayed.
- Prevent cascading failures, metastable states, and retry storms through defensive client and server network strategies.
- Maintain data consistency across microservices explicitly at the application level, avoiding brittle distributed transactions.
- Guarantee comprehensive observability to allow rapid troubleshooting of complex, multi-node interactions.
- Prioritize single-node simplicity over distributed complexity; do not distribute systems prematurely.

@Guidelines
- **Architectural Simplicity:** The AI MUST evaluate single-node alternatives (e.g., utilizing DuckDB, SQLite, or KùzuDB) before defaulting to a distributed architecture. If a workload can fit on a single machine, the AI MUST prefer the single-node approach to avoid distributed complexity.
- **Data Locality Over Network Transfer:** The AI MUST push computation to the data (e.g., executing aggregations directly in the database) rather than transferring large volumes of raw data over the network to a separate processing machine.
- **Unsafe Retries:** The AI MUST NOT implement blind retries for network calls. Because a timeout does not indicate whether the server processed the request, the AI MUST ensure the target operation is idempotent before implementing a retry.
- **Overload Prevention (Client-Side):** The AI MUST implement exponential backoff and randomized jitter for all network retries.
- **Circuit Breaking (Client-Side):** The AI MUST utilize circuit breakers or token bucket algorithms to pause requests to downstream services that are failing or degraded.
- **Server Protection (Server-Side):** The AI MUST implement load shedding and backpressure mechanisms in server logic to proactively reject traffic when the system approaches capacity limits.
- **Cross-Service Consistency:** The AI MUST NOT use or rely upon distributed transactions in a microservices context. Maintaining data consistency across different services MUST be handled explicitly by application-level logic (e.g., asynchronous event streams or compensating transactions).
- **Distributed Tracing:** The AI MUST implement observability for all inter-service network calls. Code MUST integrate tracing tools (like OpenTelemetry) to track caller ID, server ID, operation type, and exact latency.

@Workflow
1. **Architecture Assessment:** Evaluate the data volume and throughput. If the system can operate on a single machine, implement a single-node architecture. Proceed to distributed steps only if strictly necessary.
2. **Data Locality Optimization:** Review data transfer patterns. Ensure algorithms bring the computation to the node containing the data rather than extracting data over the network.
3. **Failure Path Definition:** For every cross-node network call, define the timeout threshold. Write explicit error-handling paths for dropped connections, timeouts, and unavailable services.
4. **Client-Side Resilience:** 
   - Verify the target endpoint is idempotent.
   - Implement a retry mechanism using exponential backoff and jitter.
   - Wrap the network call in a circuit breaker to protect the downstream service.
5. **Server-Side Resilience:** Implement load shedding to drop requests when CPU/memory utilization crosses critical thresholds, and return backpressure signals (e.g., HTTP 429) to clients.
6. **Consistency Mapping:** Map out application-level mechanisms to maintain data consistency across separate service databases without distributed transactions.
7. **Observability Injection:** Inject tracing spans (e.g., OpenTelemetry) around the network call to log the trace ID, latency, and high-level metrics.

@Examples (Do's and Don'ts)

**Network Retries & Overload Prevention**
- [DO]: Implement retries with exponential backoff, jitter, and idempotency checks.
  ```python
  import random
  import time
  import requests

  def fetch_data_with_backoff(url, max_retries=3):
      for attempt in range(max_retries):
          try:
              # Include idempotency key in headers for safe retries
              headers = {"Idempotency-Key": "unique-request-id"}
              response = requests.post(url, headers=headers, timeout=2.0)
              response.raise_for_status()
              return response.json()
          except requests.exceptions.RequestException:
              if attempt == max_retries - 1:
                  raise
              # Exponential backoff with jitter
              sleep_time = (2 ** attempt) + random.uniform(0, 1)
              time.sleep(sleep_time)
  ```
- [DON'T]: Use a tight loop to immediately retry a failed network request, which creates a retry storm and causes metastable failures.
  ```python
  # ANTI-PATTERN: Blind, immediate retries cause retry storms
  while True:
      try:
          response = requests.post(url)
          break
      except:
          continue
  ```

**Data Locality**
- [DO]: Run aggregation queries directly on the database to minimize network transfer.
  ```sql
  /* DO: Bring computation to the data */
  SELECT store_id, SUM(revenue) 
  FROM sales 
  WHERE month = 'January' 
  GROUP BY store_id;
  ```
- [DON'T]: Fetch millions of raw rows over the network to the application server just to compute a sum in memory.
  ```python
  # ANTI-PATTERN: Transferring data to computation
  sales = db.query("SELECT store_id, revenue FROM sales WHERE month = 'January'")
  totals = {}
  for sale in sales: # Processing millions of rows over the network
      totals[sale.store_id] = totals.get(sale.store_id, 0) + sale.revenue
  ```

**Observability**
- [DO]: Wrap inter-service calls with distributed tracing spans to capture operation durations and dependencies.
  ```python
  from opentelemetry import trace

  tracer = trace.get_tracer(__name__)

  with tracer.start_as_current_span("call_inventory_service") as span:
      span.set_attribute("target.service", "inventory")
      response = requests.get("http://inventory/api/v1/stock")
  ```
- [DON'T]: Make raw HTTP calls across microservices without passing trace context or logging execution metrics, rendering the distributed system impossible to troubleshoot.

**Cross-Service Consistency**
- [DO]: Handle consistency explicitly in the application layer using reliable event streams or compensating transactions when interacting with multiple microservices.
- [DON'T]: Attempt to implement strict distributed transactions (e.g., Two-Phase Commit) across independent microservice databases, as this tightly couples services and degrades availability.