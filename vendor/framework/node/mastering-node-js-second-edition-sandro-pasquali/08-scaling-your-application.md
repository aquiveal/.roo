@Domain
These rules activate whenever the AI is tasked with scaling a Node.js application, implementing load balancing or reverse proxies (via `http-proxy` or NGINX), establishing inter-process or inter-server communication using message queues (RabbitMQ/AMQP) or UDP/multicasting, or integrating third-party cloud services including Amazon Web Services (S3, DynamoDB, SES) and Twilio (via Heroku or similar cloud hosts).

@Vocabulary
- **Scalability vs. Performance:** Performance measures the speed of executing a single request; scalability measures the ability to maintain that performance under increasing load.
- **Horizontal Scaling:** Adding more distinct units/servers to handle traffic, as opposed to vertical scaling (adding CPU/memory to a single server).
- **Forward Proxy:** A server working on behalf of clients in a private network, brokering requests to an outside network.
- **Reverse Proxy:** A server working on behalf of backend servers, accepting requests from a public network and routing them to private network servers (e.g., load balancers).
- **AMQP (Advanced Message Queuing Protocol):** The standard messaging protocol used by RabbitMQ.
- **Direct Exchange:** A message queue exchange that routes messages by matching routing keys exactly.
- **Fanout Exchange:** A message queue exchange that indiscriminately routes messages to all bound queues, ignoring routing keys.
- **Topic Exchange:** A message queue exchange that routes messages based on wildcard matching (`#` for zero or more words, `*` for exactly one word, separated by dots).
- **UDP (User Datagram Protocol):** A lightweight networking protocol that foregoes delivery, ordering, and duplication prevention guarantees in favor of high performance.
- **Multicasting:** Broadcasting a UDP datagram to a reserved range of IP addresses (224.0.0.0 through 239.255.255.255) allowing multiple servers to subscribe to the group.
- **S3 Bucket:** An Amazon Simple Storage Service container for objects. Bucket names are shared globally across ALL AWS users.
- **DynamoDB (DDB):** AWS's NoSQL key/value database. Tables consist of items, which consist of attributes.
- **Eventual Consistency:** A database model (used often in distributed DBs and S3) where data written may not be instantaneously available for reading across all nodes.
- **Webhooks:** User-defined HTTP callbacks triggered by specific events (e.g., receiving an SMS via Twilio).
- **LevelDB:** A fast, local key/value storage library used in Node for rapid, on-disk data persistence.

@Objectives
- Accurately assess the need for horizontal scaling based on explicit system metrics (CPU load, latency, file descriptors, socket usage).
- Implement robust load balancing and reverse proxying using native Node modules (`http-proxy`) or NGINX.
- Decouple distributed system components using appropriate messaging protocols (RabbitMQ for reliable queuing, UDP for high-speed/loss-tolerant broadcasting).
- Seamlessly integrate AWS services (S3, DynamoDB, SES) adhering to strict API configuration, authentication, and data type rules.
- Design SMS-driven microservices using Twilio webhooks, separating data ingestion from client notification using reactive database streams.

@Guidelines

# 1. Monitoring and Scaling Triggers
- **Stress Testing:** Use Apache Bench (`ab`) to test server latency and dropped requests (e.g., `ab -n 10000 -c 100 http://target/`). NEVER run `ab` on the same server running the Node process being tested, as it consumes heavy resources and skews results.
- **CPU Load:** Monitor the 1, 5, and 15-minute load averages (`os.loadavg()`). On a single core, a load average > 0.60 warrants investigation. A load average of 1.00 means the CPU is at absolute maximum capacity (latency will increase). For multicore, capacity is `1.00 * number_of_cores`.
- **Socket Usage:** Monitor persistent connections in your application (e.g., via `io.sockets.clients()`) to know when to scale out WebSocket servers.
- **File Descriptors:** Track open file descriptors using the OS command `lsof | wc -l`. Adding servers is required when nearing the OS limits.

# 2. Reverse Proxies and Load Balancing
- **Node-based (`http-proxy`):** Use `http-proxy` to route distinct domains to different local ports, or to implement custom round-robin logic (e.g., shifting targets from an array, proxying the request, and pushing the target back to the end of the array).
- **NGINX:** Define server clusters using the `upstream` block and route to them using `proxy_pass http://upstream_name`.
- **NGINX Directives:** Apply the following directives to upstream servers to dictate load distribution:
  - `weight`: Determines relative traffic distribution (e.g., `weight=20` receives twice the traffic of `weight=10`).
  - `max_fails` & `fail_timeout`: Set the number of allowed failures within a time window before a server is marked inoperative.
  - `backup`: Marks a server to be used ONLY if all other servers are down.
  - `least_conn`: Routes the request to the server with the fewest active connections.
  - `ip_hash`: Ensures requests from the same client IP always hit the same backend server.

# 3. Message Queues (RabbitMQ/node-amqp)
- Instantiate connections using `amqp.createConnection()`.
- Use `exchange.publish(routingKey, message)` to send data.
- Ensure queue bindings match the exchange type logic (`bind(exchange, routingKey)`).
- Remember that `direct` exchanges are faster than `topic` exchanges because they do not require regex-style parsing.

# 4. UDP and Multicasting (`dgram`)
- Use `dgram.createSocket('udp4')`. 
- **Size Limits:** A single UDP datagram MUST NOT exceed 65,507 bytes (65535 max minus 8 bytes for UDP header minus 20 bytes for IP header).
- **Multicasting:** Use IP addresses strictly in the `224.0.0.0` to `239.255.255.255` range.
- Use `socket.addMembership(multicastAddress)` inside the `listening` event handler to subscribe a socket to a multicast group.
- Optionally configure hops using `socket.setMulticastTTL(number)`.

# 5. AWS Integration (`aws-sdk`)
- **Authentication & Time Drift:** Always supply `accessKeyId`, `secretAccessKey`, and `region`. If you receive a `SignatureDoesNotMatch` or `RequestTimeTooSkewed` (403 Forbidden) error, it indicates the host server's clock is out of sync with AWS. The AI MUST recommend syncing the server time using NTP (e.g., `ntpdate`).
- **S3:**
  - Remember that Bucket names are globally unique across the entire AWS ecosystem.
  - Always stream files directly from S3 to HTTP responses using `.createReadStream().pipe(response)`. Use `S3.headObject()` first to retrieve headers (`Content-Length`, `ContentType`, `ETag`, `LastModified`) and handle 404s before initializing the read stream.
- **DynamoDB:**
  - Table creation is asynchronous (`TableStatus: 'CREATING'`); logic cannot assume the table is instantly readable/writable.
  - An item is limited to 65KB.
  - Data types MUST be explicitly declared in the object schema: `S` (String), `N` (Number), `B` (Base64), `SS` (String Set), `NS` (Number Set), `BS` (Base64 Set).
  - Use `query` for direct key lookups. Use `scan` with `ScanFilter` ONLY when necessary, as `scan` traverses the entire database and is resource-heavy.
- **SES:** Note that new accounts are in "Sandbox" mode and can only send emails to verified addresses or the Amazon mailbox simulator.

# 6. Webhooks and SMS (Twilio/Heroku)
- Configure Twilio endpoints programmatically when possible using `twilioAPI.incomingPhoneNumbers(SID).update({ smsUrl: ... })`.
- **Decoupling Data Ingestion from Notifications:** When receiving a webhook (e.g., an incoming SMS), DO NOT optimistically broadcast the message to connected WebSockets within the webhook route handler. Instead:
  1. Write the payload to the database (e.g., LevelDB).
  2. End the HTTP response to the webhook provider.
  3. Use a separate reactive database stream (e.g., `level-live-stream`) to listen for confirmed write events.
  4. Broadcast the update to connected WebSocket clients ONLY when the database stream emits the data.

@Workflow
When tasked with horizontal scaling or external service integration, follow this strict process:
1. **Analyze Bottlenecks:** Determine the specific metric failing (CPU vs Memory vs Network Latency vs Sockets). Select the architectural solution (NGINX load balancer, message queue, or UDP cache broadcast).
2. **Architecture Topology:** Define the layout. If using proxies, specify the backend ports/IPs and routing rules (weight, ip_hash).
3. **Data Decoupling:** If the task involves massive real-time communication, implement RabbitMQ for reliable targeted communication, or UDP multicasting for volatile, high-speed broadcasts.
4. **Cloud Integration Setup:** If integrating AWS, define the `config.json` with strict `apiVersions`. Ensure data objects sent to DynamoDB strictly adhere to the `{ "Type": "Value" }` format.
5. **Event-Driven Resilience:** For webhooks or external API listeners, separate the HTTP ingest layer from the client-broadcast layer using a database write-stream watcher.

@Examples (Do's and Don'ts)

[DO] Implement a custom round-robin load balancer in Node using `http-proxy`:
```javascript
const httpProxy = require('http-proxy');
let addresses = [
    { host: 'one.example.com', port: 80 },
    { host: 'two.example.com', port: 80 }
];
httpProxy.createServer((req, res, proxy) => {
    let target = addresses.shift();
    proxy.proxyRequest(req, res, target);
    addresses.push(target); // push target to the back of the queue
}).listen(80);
```

[DON'T] Use generic variable names or omit data types when interacting with DynamoDB.
```javascript
// INCORRECT
db.putItem({
    TableName: "purchases",
    Item: { Id: 123, Action: "buy" }
});
```

[DO] Explicitly define DDB data types for every attribute:
```javascript
// CORRECT
db.putItem({
    TableName: "purchases",
    Item: {
        Id: { "N": "123" },
        Action: { "S": "buy" }
    }
}, callback);
```

[DON'T] Read an entire file from S3 into memory before sending it to a client.
```javascript
// INCORRECT
S3.getObject({ Key: 'file.jpg' }, (err, data) => {
    response.end(data.Body);
});
```

[DO] Perform a HEAD request to secure headers, then stream the file directly from S3 to the client:
```javascript
// CORRECT
S3.headObject({ Key: requestedFile }, (err, data) => {
    if (err) {
        response.writeHead(err.statusCode);
        return response.end(err.name);
    }
    response.writeHead(200, {
        "Last-Modified": data.LastModified,
        "Content-Length": data.ContentLength,
        "Content-Type": data.ContentType,
        "ETag": data.ETag
    });
    S3.getObject({ Key: requestedFile }).createReadStream().pipe(response);
});
```

[DON'T] Broadcast a webhook event to WebSocket clients directly from the HTTP route handler.
```javascript
// INCORRECT (Susceptible to false positives if DB write fails)
server.post('/smswebhook', (req, res) => {
    db.save(req.body);
    websocketServer.broadcast(req.body); 
    res.end();
});
```

[DO] Write to the DB in the route, and use a separate DB listener to broadcast the verified data to clients:
```javascript
// CORRECT
server.post('/smswebhook', (req, res) => {
    dbApi.addToNumberHistory(req.body.From, meta);
    res.end();
});

// Elsewhere in the application
const dbStream = require('level-live-stream')(db);
dbStream.on('data', data => {
    let boundClient = Clients.withNumber(data.key);
    if(boundClient) {
        boundClient.send(JSON.stringify({ type: 'update', list: data.value }));
    }
});
```