@Domain
These rules MUST trigger when the user requests assistance with scaling, optimizing, performance-tuning, paginating, or rate-limiting a Web API. They also apply when designing strategies to evolve an existing API architecture (e.g., adding bulk endpoints, filtering, async operations), or when generating/modifying client SDKs to interact with an API.

@Vocabulary
- **Throughput**: The number of API calls per second an API can handle.
- **Vertical Scaling**: Adding more power (CPU, RAM, disk storage) to existing servers.
- **Horizontal Scaling**: Adding more server instances to a pool of resources to distribute load.
- **Database Sharding**: Partitioning data so that rows of a database table are stored across different servers.
- **Edge Caching**: Caching API results physically closer to end users (e.g., via CDNs) to achieve higher throughput and lower latency.
- **Asynchronous Operation**: Moving expensive, slow operations (e.g., indexing a file) outside the HTTP request-response cycle via task queues.
- **Offset-based Pagination**: Pagination utilizing a `limit` (max items) and an `offset` (number of items to skip).
- **Cursor-based Pagination**: Pagination utilizing a pointer (`cursor`) indicating the exact starting position for the next set of items.
- **Opaque String**: An encoded string (often base64) used as a cursor to hide implementation details (like DB IDs) and allow embedding multiple data points (like shard pointers).
- **Rate-Limiting**: Controlling the rate of traffic sent or received on a network interface to protect infrastructure and prevent abuse.
- **Token Bucket**: A rate-limiting algorithm that maintains a steady upper limit while permitting occasional bursts.
- **Fixed-window Counter**: A rate-limiting algorithm that tracks requests in strict time windows (e.g., 1 minute); can allow up to 2x traffic spikes at window boundaries.
- **Sliding-window Counter**: A rate-limiting algorithm that divides time into smaller buckets to smooth traffic and prevent bursts at boundaries.
- **Dark Launching**: Testing a feature (like rate limits) by logging what *would* happen (e.g., logging rejected requests) without actually enforcing the block, to tune thresholds.
- **Exponential Back-off**: An error-handling strategy in client SDKs where failed requests are retried over exponentially increasing intervals of time.

@Objectives
- Ensure the API handles increased throughput by identifying bottlenecks before applying premature optimizations.
- Evolve API design to reduce unnecessary HTTP round trips, minimize payload sizes, and prevent polling.
- Safely serve large datasets by enforcing robust, performant pagination strategies.
- Protect application infrastructure and product integrity via structured, well-communicated rate-limiting policies.
- Build resilient client SDKs that actively assist in load management by respecting limits and handling errors gracefully.

@Guidelines

### 1. Identifying and Resolving Bottlenecks
- The AI MUST NOT apply scaling optimizations prematurely. It MUST first instruct or implement profiling/instrumentation (e.g., AWS CloudWatch, New Relic, Stackdriver).
- When analyzing bottlenecks, the AI MUST categorize them into: Disk I/O, Network I/O, CPU, or Memory.
- **Scaling approach**: The AI MUST PREFER horizontal scalability (sharding, load balancing, replication) over vertical scalability.
- **Database Indexes**: The AI MUST add indexes to database columns used in `WHERE`, `ORDER BY`, and `GROUP BY` clauses. It MUST NOT over-index, as this causes write-performance degradation.
- **Caching**: The AI MUST identify frequently accessed, slow-to-compute data and apply in-memory caching (e.g., Memcached, Redis). The AI MUST simultaneously implement strict cache invalidation logic for when underlying data updates.
- **Async Processing**: The AI MUST move operations that take a long time to execute (e.g., file processing, search indexing) out of the main request thread using asynchronous task queues (e.g., Celery).

### 2. Evolving API Design (Without Breaking Clients)
- **Polling Reduction**: If clients are repeatedly polling the API, the AI MUST recommend transitioning to WebHooks, WebSockets, or HTTP Streaming.
- **Payload Optimization**: If clients request large objects but use few fields, the AI MUST introduce targeted API methods (e.g., returning only a connection URL instead of full state) or introduce GraphQL.
- **Bulk Endpoints**: If clients frequently perform operations on multiple items one by one, the AI MUST implement bulk endpoints that accept arrays of IDs to reduce HTTP round trips and database load.
- **Filtering**: To minimize payload sizes, the AI MUST implement:
  - Search filters (fuzzy match/regex).
  - Date filters (`since`, `until`).
  - Order filters (sort by popularity, date).
  - Field selection filters (options to explicitly include or exclude specific fields in the JSON response).

### 3. Paginating APIs
- The AI MUST implement pagination on any endpoint returning a list of items.
- The AI MUST set reasonable default and maximum values for page sizes (e.g., default 100, max 1000).
- **Sorting**: The AI SHOULD sort paginated data with newest items first and older items later to reduce the need for deep traversal.
- **Next Page URL**: The AI MUST include a URL pointing to the subsequent page of results in the response. A null/empty value indicates the end of the list.
- **Offset-Based Pagination Guidelines**:
  - Use ONLY for small datasets where deep traversal is unlikely.
  - The AI MUST NOT use offset pagination for massive datasets due to high database counting/skipping costs.
- **Cursor-Based Pagination Guidelines**:
  - The AI MUST use cursor-based pagination for high-traffic, large, or frequently changing datasets.
  - The AI MUST PREFER "Opaque Strings" (encoded values) as the cursor to hide database implementation and allow for future data structure changes.
  - The AI MUST NOT encode sensitive information (e.g., PII, passwords) inside cursors.
  - The underlying database column used for the cursor MUST be unique, sequential, and indexed.

### 4. Rate-Limiting APIs
- The AI MUST implement rate-limiting via high-performance, in-memory data stores (e.g., Redis, Memcached).
- **Algorithm Selection**:
  - Use **Token Bucket** if the API needs to tolerate occasional traffic bursts (common for paid/enterprise APIs).
  - Use **Fixed-window Counter** for simple use cases where brief spikes at the minute-mark are acceptable.
  - Use **Sliding-window Counter** to strictly smooth traffic and completely reject bursts.
- **HTTP Status & Headers**:
  - When a rate limit is exceeded, the AI MUST return an HTTP `429 Too Many Requests` status code.
  - The AI MUST include a `Retry-After` header.
  - The AI MUST include custom informational headers on requests: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` (UTC epoch seconds).
- **Deployment**: The AI MUST recommend "Dark Launching" new rate limits (logging rejections without enforcing them) to tune thresholds before full enforcement.

### 5. Developer SDKs
- When generating SDKs, the AI MUST build in graceful handling of `429` errors and automatically pause requests using the `Retry-After` or `X-RateLimit-Reset` data.
- The AI MUST implement **Exponential Back-off** for retries on failed requests to prevent flooding the server during an outage.
- The AI MUST implement automatic pagination traversal (e.g., an iterator or generator that seamlessly fetches the next page up to a sensible limit).
- The AI MUST configure SDKs to use `gzip` compression for requests/responses to save bandwidth.
- The AI MUST perform local parameter validation in the SDK before sending the HTTP request to save server load.

@Workflow
1. **Analyze Load/Bottlenecks**: Define the scaling objective. Identify if the issue is throughput (needs DB indexing/caching), payload size (needs filtering/new methods), or abuse (needs rate-limiting).
2. **Optimize Data Retrieval**: Apply indexes to query columns. Implement Memcached/Redis for frequent queries. Offload heavy processing to async workers.
3. **Evolve the Interface**: Create bulk operation endpoints and add query parameters for sorting, filtering, and field exclusion.
4. **Implement Pagination**: 
   - Define max limits.
   - Set up Cursor-based logic (encode a unique indexed column into an opaque string).
   - Inject the `next_page` URL into the JSON response.
5. **Enforce Rate Limits**:
   - Select algorithm (Token Bucket, Fixed, or Sliding window).
   - Write Redis logic to track counts per User ID or IP.
   - Inject `X-RateLimit-*` headers into successful responses.
   - Configure HTTP 429 response with `Retry-After` for blocked requests.
6. **Upgrade SDKs**: Wrap SDK HTTP clients with exponential back-off logic, gzip compression, and rate-limit parsing.

@Examples (Do's and Don'ts)

### Pagination
- **[DO]** Return an opaque cursor and a pre-formatted URL to help the client easily navigate.
```json
{
  "data": [...],
  "next_cursor": "eyJpZCI6MTIzNDV9",
  "next_page_url": "https://api.example.com/v1/items?limit=100&cursor=eyJpZCI6MTIzNDV9"
}
```
- **[DON'T]** Use offset pagination on large datasets where clients skip tens of thousands of rows.
```sql
/* DON'T DO THIS AT SCALE */
SELECT * FROM items ORDER BY created_at LIMIT 10 OFFSET 50000;
```

### Rate Limiting
- **[DO]** Return HTTP 429 with explicit instructions on when the client can retry.
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 36
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1510378642

{
  "error": "too_many_requests",
  "message": "You have made too many requests. Try again in 36 seconds."
}
```
- **[DON'T]** Silently drop requests or return generic 500 errors without rate-limit headers.

### SDK Implementation (Exponential Back-off)
- **[DO]** Implement a retry loop with increasing delays.
```javascript
// DO: Exponential back-off implementation
async function fetchWithBackoff(url, retries = 3, delay = 1000) {
  try {
    const response = await fetch(url);
    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After') * 1000;
      await sleep(retryAfter || delay);
      return fetchWithBackoff(url, retries - 1, delay * 2);
    }
    return response;
  } catch (error) {
    if (retries === 0) throw error;
    await sleep(delay);
    return fetchWithBackoff(url, retries - 1, delay * 2);
  }
}
```
- **[DON'T]** Catch errors and immediately loop requests back to a struggling server.

### Evolving API Endpoints
- **[DO]** Support bulk operations to save HTTP round trips and database queries.
```http
POST /api/conversations.invite
{
  "channel": "C01234",
  "users": ["U111", "U222", "U333"]
}
```
- **[DON'T]** Force the client to loop and make individual HTTP POST requests for every single user they want to invite.