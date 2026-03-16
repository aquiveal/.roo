# @Domain

Triggers when the user requests the creation, architecture, or refactoring of real-time Node.js network applications, including collaborative tools, chat systems, live data dashboards, polling systems, Server-Sent Events (SSE) implementations, and WebSocket or socket.io integrations.

# @Vocabulary

*   **Real-Time Software**: Network applications where data I/O updates occur along subsecond time frames, immediately communicating reactions to change to connected clients.
*   **AJAX (Asynchronous JavaScript and XML)**: A technique for requesting chunks of HTML or data from servers to apply partial, dynamic updates to a web page without a full refresh.
*   **Polling**: A client-server communication pattern where the client periodically requests status updates from the server, regardless of whether new data is available.
*   **Long-Polling**: An improved polling technique where the server holds onto a client connection until new data is available to send, reducing redundant network chatter and connection tear-downs.
*   **WebSockets**: A protocol and API enabling persistent, low-latency, bidirectional communication between web applications and server-side processes over a single TCP connection.
*   **socket.io**: A library providing a Node-based socket server and a client-side emulation layer that falls back to long-polling for legacy browsers that do not support native WebSockets.
*   **SSE (Server-Sent Events)**: A unidirectional (server-to-client) push technology utilizing standard HTTP protocols to broadcast simple text messages and state changes.
*   **EventSource**: The browser API used to establish an SSE connection and listen for data events emitted by the server.
*   **Operational Transformation (OT)**: A technology that enables live, concurrent collaborative document editing by managing and merging sequences of changesets (deltas).
*   **ShareDB (formerly ShareJS)**: An OT backend database and framework for Node.js used to sync collaborative state.
*   **Quill**: A rich text editor uniquely suited for OT as it represents documents as a sequence of JSON changesets.

# @Objectives

*   Select the most efficient and appropriate real-time transport protocol (AJAX, WebSockets, SSE) based on message volume, required directionality, and network latency constraints.
*   Implement completely non-blocking, asynchronous event-driven real-time architectures.
*   Safely manage distributed client states, unique client identifiers, and concurrent connection pools on the server.
*   Minimize network overhead by preventing futile client polling and utilizing dynamic back-off strategies.
*   Enable massively concurrent, state-synced applications (like collaborative editors) using Operational Transformation.

# @Guidelines

*   **Protocol Selection Strategy**:
    *   The AI MUST use **Server-Sent Events (SSE)** when the majority of data transfer proceeds unidirectionally from server to clients (e.g., live scoreboards, server monitoring).
    *   The AI MUST use **WebSockets** or **socket.io** for multiuser environments requiring continuous, rapid, bidirectional data transfer (e.g., multiplayer network games, chat rooms, collaborative drawing).
    *   The AI MUST use **AJAX Polling / Long-Polling** only for simple applications where the ideal polling interval is well known and occasional communication breakdowns are acceptable.
*   **AJAX Polling Constraints**:
    *   The AI MUST implement dynamic server-controlled polling intervals. The server MUST send a `callIn` (or equivalent) property indicating the number of milliseconds the client should wait before polling again.
    *   The AI MUST increase the polling interval (back-off) when the server encounters an error or receives an empty data set to prevent exceeding rate limits or overwhelming external APIs.
*   **WebSocket & socket.io Implementation**:
    *   The AI MUST uniquely identify each client connection (e.g., utilizing `socket.id` in socket.io or generating a unique ID upon connection).
    *   The AI MUST manage disconnected clients by listening to the `close` or `disconnect` event and broadcasting a `clientdisconnect` event to all other clients to clean up UI state.
    *   The AI MUST use `socket.broadcast.emit` (or loop through a client map) to send state changes to all connected clients *except* the originating client when appropriate.
*   **Server-Sent Events (SSE) Implementation**:
    *   The AI MUST set the following HTTP headers for SSE endpoints: `Content-Type: text/event-stream`, `Cache-Control: no-cache`, and `Connection: keep-alive`.
    *   The AI MUST prefix SSE streams with a 2-KB padding write (`":" + Array(2049).join(" ") + "\n"`) immediately upon connection to bypass XHR implementation buffering in certain browsers.
    *   The AI MUST set an automatic reconnection interval for the client by sending a `retry` field (e.g., `retry: 2000\n`).
    *   The AI MUST terminate every SSE message payload with a double newline (`\n\n`) to indicate the end of the message block.
    *   The AI MUST implement a server-side "heartbeat" (e.g., a `setInterval` sending a ping every 10-15 seconds) to keep the SSE connection alive and prevent browser timeouts.
    *   The AI MAY use the `event: [name]\n` field to create custom event channels for clients to listen to via `addEventListener`.
*   **Collaborative OT Integration**:
    *   The AI MUST use an OT-compliant library (like ShareDB) combined with a JSON-changeset compatible frontend (like Quill) for concurrent document editing.
    *   The AI MUST pipe WebSocket connections into JSON streams (e.g., `websocket-json-stream`) to integrate with the ShareDB backend.

# @Workflow

1.  **Analyze Real-Time Requirements**: Evaluate the expected message volume, payload size, directionality (1-way vs. 2-way), and latency tolerance.
2.  **Route Protocol Implementation**:
    *   *If AJAX/Polling*: Create a REST endpoint that fetches data. Append a `callIn` millisecond value to the JSON response based on server load or error state. Implement a recursive `setTimeout` loop on the client driven by the `callIn` value.
    *   *If SSE*: Create an HTTP GET route. Write required SSE headers. Send the 2KB whitespace padding and `retry` interval. Establish a `setInterval` heartbeat. Store the `response` object in a mapped dictionary of connected clients. Create a `broadcast` function that iterates the dictionary and writes `data: [string]\n\n` to all open response streams.
    *   *If WebSocket*: Instantiate a `ws` or `socket.io` server attached to the HTTP server. On `connection`, assign an ID. Setup listeners for `message` or custom events. On state-changing events, broadcast the payload and the originating ID to all connected peers. Implement a `close` listener to clean up the client dictionary.
3.  **State Management**: Store global application state (e.g., active questions, document state, connected user coordinates) centrally on the server.
4.  **Client-Side Binding**: Implement the browser counterpart (`$.getJSON` with timeout, `new EventSource()`, or `new WebSocket()`) and bind incoming data to DOM rendering functions.

# @Examples (Do's and Don'ts)

### AJAX Dynamic Polling

**[DO]** Control the client polling interval from the server to protect server resources and handle errors gracefully.
```javascript
// Server (Node.js)
response.writeHead(200, { "Content-type": "application/json" });
// Send 5000ms if successful, 10000ms if error
response.end(JSON.stringify({
    quote: data,
    callIn: isError ? 10000 : 5000,
    error: isError ? err.message : null
}));

// Client (Browser)
function fetch() {
    clearTimeout(caller);
    $.getJSON('/?symbol=IBM', function(data) {
        if (!data.callIn) return;
        caller = setTimeout(fetch, data.callIn); // Let server dictate next poll
        if (!data.error) updateDisplay(data.quote);
    });
}
fetch();
```

**[DON'T]** Use hardcoded `setInterval` loops on the client that blindly hammer the server regardless of error states or network limits.
```javascript
// Anti-pattern: Blind client-side polling
setInterval(function() {
    $.getJSON('/?symbol=IBM', function(data) {
        updateDisplay(data);
    });
}, 1000); // Danger: Will overwhelm the server if API limits are reached
```

### Server-Sent Events (SSE) Setup

**[DO]** Send proper headers, a 2KB padding to bypass browser buffering, a retry interval, and maintain a heartbeat.
```javascript
http.createServer((request, response) => {
    if (request.url === "/login") {
        response.writeHead(200, {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        });
        
        // 2KB padding for older browser XHR implementations
        response.write(":" + Array(2049).join(" ") + "\n");
        response.write("retry: 2000\n"); // Auto-reconnect interval
        
        // Heartbeat to keep connection alive
        let heartbeat = setInterval(() => {
            response.write("event: ping\n");
            response.write("data: " + new Date().getTime() + "\n\n");
        }, 10000);

        response.on("close", () => clearInterval(heartbeat));
    }
});
```

**[DON'T]** Send standard HTTP text responses without the required `\n\n` termination or event-stream headers.
```javascript
// Anti-pattern: Missing headers, padding, and double newlines
http.createServer((request, response) => {
    // Missing Content-Type: text/event-stream
    setInterval(() => {
        response.write("data: Hello"); // Missing \n\n termination! EventSource will fail to parse.
    }, 1000);
});
```

### WebSocket Broadcasting and State Management

**[DO]** Track clients via unique IDs, broadcast updates to peers, and clean up connections on disconnect.
```javascript
let clients = {};

io.sockets.on('connection', socket => {
    let id = socket.id;
    clients[id] = { x: 0, y: 0 };

    socket.on('mousemove', data => {
        data.id = id;
        clients[id] = data;
        // Broadcast to all OTHER clients
        socket.broadcast.emit('moving', data); 
    });

    socket.on('disconnect', () => {
        delete clients[id];
        socket.broadcast.emit('clientdisconnect', id);
    });
});
```

**[DON'T]** Leave disconnected clients in memory or broadcast updates back to the sender unnecessarily (causing echo/feedback loops).
```javascript
// Anti-pattern: Memory leak and feedback loop
let activeUsers = [];

io.sockets.on('connection', socket => {
    activeUsers.push(socket); // Memory leak: never removed on disconnect
    
    socket.on('mousemove', data => {
        // Anti-pattern: emitting back to the sender causes UI stuttering
        io.sockets.emit('moving', data); 
    });
});
```

### Operational Transformation Initialization

**[DO]** Pipe WebSocket connections through a JSON stream wrapper to interface with ShareDB.
```javascript
const ShareDB = require('sharedb');
const WebSocketJSONStream = require('websocket-json-stream');

const backend = new ShareDB();
const wss = new WebSocket.Server({ server: server });

wss.on('connection', (ws) => {
    // Correctly wrap the raw websocket in a JSON stream for OT processing
    backend.listen(new WebSocketJSONStream(ws)); 
});
```