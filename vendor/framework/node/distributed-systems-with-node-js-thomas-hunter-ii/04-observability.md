@Domain
Triggered when the user requests tasks related to Node.js application observability, monitoring, logging, metrics collection, distributed request tracing, health checks, alerting, or diagnosing remote service behaviors.

@Vocabulary
- **Observability**: The ability to gain insight into the internal state and health of remote services using external outputs (logs, metrics, traces).
- **Environment**: A segregated context (e.g., Development, Staging, Production) for running isolated application instances.
- **ELK Stack**: Elasticsearch (database/search), Logstash (log ingestion), and Kibana (dashboards/UI).
- **Graphite / StatsD / Grafana**: A stack for collecting, storing, and visualizing numeric time-series data.
- **Metric**: Numeric data associated with time (e.g., request rates, latency, memory usage).
- **Zipkin (OpenZipkin)**: A distributed tracing system used to associate and visualize a hierarchy of related requests across microservices.
- **Trace**: Zipkin concept representing an entire collection (tree) of related requests initiated by a single external action.
- **Span**: Zipkin concept representing a single request between a client and a server.
- **B3 Headers**: HTTP headers (`X-B3-*`) used by Zipkin to propagate tracing metadata across service boundaries.
- **Liveness**: A state indicating a newly deployed service has finished startup and is ready to receive requests.
- **Degraded**: A health check state where an application cannot reach a secondary/caching service but can still fulfill requests via the primary datastore.
- **Runbook**: Documentation associated with an alert that details how to diagnose and fix an issue.
- **UDP (User Datagram Protocol)**: A connectionless network protocol used in observability to transmit logs/metrics without blocking the Node.js event loop or requiring delivery guarantees.

@Objectives
- Establish complete visibility into distributed Node.js services to allow diagnosing issues across multiple servers.
- Ensure monitoring overhead does not negatively impact application performance or block the Node.js event loop.
- Standardize environment names and prevent environment-based hardcoded configuration.
- Implement structured, queryable logs and hierarchical, time-based metrics.
- Track individual requests across service boundaries using distributed tracing headers.
- Differentiate accurately between fully healthy, degraded, and completely unhealthy application states.

@Guidelines

### 1. Environment Management
- The AI MUST use `NODE_ENV` solely to define the environment identity.
- The AI MUST standardize environment names (e.g., `development`, `staging`, `production`). Do not invent custom names like `preprod` without explicit instruction.
- The AI MUST NOT use the environment value to hardcode configuration routing (e.g., `if (env === 'staging') db = 'stage-db'`). All dynamic configuration MUST be provided via generic environment variables.

### 2. Logging (ELK Stack)
- The AI MUST output logs as well-formed JSON objects.
- The AI MUST keep JSON log objects shallow (maximum 1 or 2 levels deep) to ensure easy indexing.
- The AI MUST include standard metadata in every log: `@timestamp` (ISO string), `app` (service name), `environment` (`NODE_ENV`), `severity`, `type`, and `fields`.
- The AI MUST restrict log severities to standard levels: `error`, `warn`, `info`, `verbose`, `debug`, and `silly`.
- The AI SHOULD transmit logs via UDP (e.g., using `dgram` to Logstash) to minimize application overhead and prevent logging failures from crashing the application.
- The AI MUST log incoming requests (path, method, IP, user-agent), outbound requests to other services, server startup, and unhandled errors (with stack traces).

### 3. Metrics (StatsD / Graphite / Grafana)
- The AI MUST capture numeric data over time using the StatsD format (`metric_name:value|type`).
- The AI MUST prefix all metric names with the application's unique name to create a hierarchy (e.g., `web-api.inbound.request-time`).
- The AI MUST distinguish between perceived client time (which includes network overhead) and actual server processing time when tracking latency.
- The AI MUST implement internal Node.js health indicators. An observability module MUST poll and report:
  - Active server connections.
  - Process memory usage (`process.memoryUsage().heapUsed` / `heapTotal`).
  - V8 heap statistics (`v8.getHeapStatistics()`).
  - Open file descriptors (e.g., via `fs.readdir('/proc/self/fd')` on Linux).
  - Event loop lag (measured by calculating the delay of a `setTimeout(fn, 0)` call).

### 4. Distributed Request Tracing (Zipkin)
- The AI MUST propagate trace context to all upstream services using B3 HTTP headers: `X-B3-TraceId`, `X-B3-SpanId`, `X-B3-ParentSpanId`, `X-B3-Sampled`, and `X-B3-Flags`.
- The AI MUST ensure `X-B3-TraceId` remains unchanged throughout the entire lifecycle of the distributed request.
- The AI MUST generate a new `X-B3-SpanId` for every new outbound request, passing the current `SpanId` as the `X-B3-ParentSpanId`.
- The AI MUST define Zipkin span names using a finite, static set of string values (e.g., `get_recipe`). Do NOT use dynamic identifiers (like user IDs) as span names.
- The AI MUST record and transmit both `CLIENT` (outbound) and `SERVER` (inbound) messages to Zipkin, calculating `timestamp` and `duration` in microseconds.

### 5. Health Checks and Alerting (Cabot)
- The AI MUST expose a dedicated `/health` HTTP endpoint.
- The AI MUST check the connection to the primary datastore (e.g., PostgreSQL). If the primary datastore is unreachable, the AI MUST return an HTTP `500` status with a `DOWN` message.
- The AI MUST check connections to secondary/caching datastores (e.g., Redis). If a cache is unreachable, the AI MUST return an HTTP `200` status but include a `DEGRADED` message. A missing cache should not fail the overall liveness check.
- The AI MUST ensure health check overhead is minimal so periodic polling (e.g., every 2-10 seconds) does not overwhelm the process or database.
- The AI MUST design health endpoints to be compatible with automated alerting tools that parse HTTP status codes and response bodies.

@Workflow
1. **Analyze Observability Requirements**: Identify the target microservice, its upstream dependencies, primary datastores, and secondary datastores.
2. **Implement Structured Logging**: Wrap all `console.log`/`error` calls in a JSON logging utility. Add middleware to log inbound and outbound network requests.
3. **Instrument Metrics**: Add StatsD middleware to record HTTP status codes and latencies. Set up a `setInterval` to report Node.js internal metrics (memory, file descriptors, event loop lag).
4. **Implement Distributed Tracing**: Intercept incoming requests to parse or generate B3 headers. Wrap outgoing HTTP/RPC clients to inject B3 headers and send spans to Zipkin.
5. **Construct the Health Check**: Create the `/health` route. Write `try/catch` logic to query primary datastores (fail with 500) and secondary datastores (flag as DEGRADED, pass with 200).

@Examples (Do's and Don'ts)

### Structured Logging
- **[DO]** Log events as shallow JSON objects over UDP.
  ```javascript
  const payload = JSON.stringify({
    '@timestamp': new Date().toISOString(),
    app: 'web-api',
    environment: process.env.NODE_ENV,
    severity: 'error',
    type: 'request-failure',
    fields: { path: req.url, method: req.method, error: err.message }
  });
  client.send(payload, LS_PORT, LS_HOST);
  ```
- **[DON'T]** Use unstructured string concatenation for production logs.
  ```javascript
  console.error("Error on " + req.url + ": " + err.message); // Violates observability rules
  ```

### Health Checks (Liveness and Degradation)
- **[DO]** Return a 200 OK for a degraded state when a cache is down but the primary DB is up.
  ```javascript
  server.get('/health', async (req, reply) => {
    try {
      await pg.query('SELECT 1'); // Primary DB
    } catch(e) {
      return reply.code(500).send('DOWN');
    }

    let status = 'OK';
    try {
      if (await redis.ping() !== 'PONG') status = 'DEGRADED'; // Secondary DB
    } catch(e) {
      status = 'DEGRADED';
    }

    return reply.code(200).send(status);
  });
  ```
- **[DON'T]** Return a 500 error and crash the pod just because the Redis cache is unreachable.
  ```javascript
  // DON'T do this:
  await redis.ping(); // If this throws, unhandled exception returns 500, taking down the API!
  ```

### Event Loop Lag Metrics
- **[DO]** Measure event loop lag by comparing expected vs. actual execution time of a timer.
  ```javascript
  setInterval(() => {
    const begin = Date.now();
    setTimeout(() => {
      statsd.timing('eventlag', Date.now() - begin);
    }, 0);
  }, 10000);
  ```
- **[DON'T]** Assume the Node.js process is healthy just because it responds to a basic HTTP request without checking event loop delay or file descriptor leaks.

### Environment Variables
- **[DO]** Route dynamic configuration through environment variables.
  ```javascript
  const dbUrl = process.env.DATABASE_URL;
  ```
- **[DON'T]** Map configuration inside the code based on the `NODE_ENV` string.
  ```javascript
  // DON'T do this
  let dbUrl;
  if (process.env.NODE_ENV === 'staging') dbUrl = 'stage-db.internal';
  ```