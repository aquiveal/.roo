# @Domain
These rules MUST be triggered whenever the AI is tasked with implementing Node.js I/O operations, reading or writing files, building network servers or clients (HTTP/HTTPS/TCP/UDP), proxying network traffic, processing large datasets or payloads, manipulating memory buffers, or explicitly working with the Node.js `stream`, `http`, `https`, `url`, or `querystring` modules.

# @Vocabulary
- **Stream**: An object representing a sequence of bytes (or objects) representing data flows that can be written to and read from asynchronously. An instance of `EventEmitter`.
- **Readable Stream**: A stream producing data that a consumer can read from. Implements a private `_read` method.
- **Writable Stream**: A stream responsible for accepting data and writing it to a destination. Implements a private `_write` method.
- **Duplex Stream**: A stream that is both readable and writable (e.g., a TCP socket).
- **Transform Stream**: A Duplex stream that modifies or transforms data as it is written and read. Implements a private `_transform` method.
- **PassThrough Stream**: A trivial Transform stream that simply passes input bytes to output. Useful as a spy or watcher.
- **Backpressure**: A build-up of unread data. Occurs when data is pushed into a stream faster than it can be drained, risking memory limits or buffer overflows.
- **highWaterMark**: The maximum number of bytes (default 16KB) a stream's internal buffer will accept before indicating that the producer should stop pushing or writing data.
- **objectMode**: A stream configuration flag (`true`/`false`) that forces the stream to behave as a stream of discrete JavaScript objects instead of string/byte buffers.
- **Pipe**: A method (`.pipe()`) used to redirect fluid data from a Readable stream directly to a Writable stream, automatically managing flow and backpressure.
- **Tunneling**: Using a proxy server as an intermediary to communicate with a remote server on behalf of a client, commonly established via the HTTP `CONNECT` method.
- **Protocol-relative URL**: A network-path reference starting with `//` instead of a protocol (e.g., `//www.example.org`). 

# @Objectives
- Build scalable, non-blocking network applications by utilizing asynchronous data streams.
- Ensure the Node.js event loop is never blocked by large payload processing or synchronous file I/O.
- Enforce strict memory management by respecting stream backpressure and avoiding loading entire files or payloads into memory.
- Standardize the creation of custom streams using Node's abstract base classes (`Readable`, `Writable`, `Duplex`, `Transform`).
- Facilitate composable, decoupled network architectures using streams, proxying, and tunneling.

# @Guidelines

## General Stream Constraints
- The AI MUST NEVER use synchronous file operations (e.g., `fs.readFileSync`, `fs.writeFileSync`) when copying, serving, or processing large files. 
- The AI MUST treat all streams as event emitters and explicitly handle stream lifecycle events, particularly `error`, `readable`, `drain`, and `end`/`finish`.

## Implementing Custom Streams
- **Readable Streams**: 
  - The AI MUST extend the `Readable` base class and implement the `_read()` method.
  - The AI MUST push data downstream using `this.push(data)`.
  - When the data source is exhausted, the AI MUST push a `null` value (`this.push(null)`) to trigger the `end` event.
  - If `this.push()` returns `false`, the AI MUST stop reading from the source until the next `_read` request is made to prevent backpressure.
- **Writable Streams**:
  - The AI MUST extend the `Writable` base class and implement the `_write(chunk, encoding, callback)` method.
  - The AI MUST invoke the `callback()` immediately after processing the chunk to indicate success or failure.
  - When writing to a Writable stream using `.write(data)`, the AI MUST check the return value. If it returns `false`, the AI MUST NOT send more data until the stream emits a `drain` event.
- **Duplex Streams**:
  - The AI MUST implement both `_read()` and `_write()` methods according to the rules above.
- **Transform Streams**:
  - The AI MUST extend the `Transform` base class and implement the `_transform(chunk, encoding, callback)` method.
  - The AI MUST NOT implement `_read` or `_write` for Transform streams.
  - The AI MUST invoke the `callback()` when the transformation of the current chunk is complete. Data is passed downstream via `this.push(transformedData)`.
- **PassThrough Streams**:
  - The AI MUST use `stream.PassThrough()` when a minimal spy, watcher, or placeholder stream is required (e.g., in testing).

## HTTP Servers and Clients
- The AI MUST treat HTTP `request` objects as `Readable` streams and HTTP `response` objects as `Writable` streams.
- **Headers**: 
  - The AI MUST write response headers (using `response.writeHead` or `response.setHeader`) BEFORE writing any body data.
  - To remove a header, the AI MUST use `response.removeHeader(name)` before the response is sent.
- **Favicon Requests**: 
  - When building a raw HTTP server, the AI MUST explicitly intercept requests for `/favicon.ico` and handle them (e.g., return a 200 with `image/x-icon` or stream an image) to prevent double-execution of application logic.
- **POST Data**: 
  - The AI MUST collect POST body chunks asynchronously by listening to `readable` (or `data`) events, and process the fully assembled data on the `end` event. The AI MUST NOT assume the body is available synchronously.
- **Cookies**: 
  - The AI MUST manually parse `request.headers.cookie` or use a reliable parsing mechanism. 
  - The AI MUST set cookies using `response.setHeader('Set-Cookie', cookieText)`.
- **HTTPS/TLS**: 
  - When creating a secure server, the AI MUST use the `https` module and provide a configuration object containing `key` and `cert` (read via `fs.readFileSync` at startup).
- **Proxying and Tunnelling**:
  - When proxying requests, the AI MUST pipe the incoming `request` directly to the outgoing `http.request` stream, and pipe the outgoing response directly to the client `response` stream.
  - When handling HTTP `CONNECT` requests for tunneling, the AI MUST listen for the `connect` event on the HTTP server, establish a TCP connection (via `net.connect`) to the destination, and pipe the client socket and remote socket to each other.

## URLs and Routing
- The AI MUST use `url.parse(request.url, true)` to automatically parse query strings into key/value maps.
- When parsing protocol-relative URLs (e.g., `//www.example.org`), the AI MUST pass `true` as the third argument to `url.parse` (`url.parse(string, null, true)`) to correctly identify the host instead of treating it as a path.
- The AI MUST use the `querystring` module when a custom delimiter or assignment character is needed, or when parsing URL-encoded POST bodies.

# @Workflow
When tasked with moving, processing, or serving data across nodes or clients, the AI MUST follow this algorithmic process:

1. **Identify Data Source and Sink**: Determine where the data originates (file, HTTP request, child process stdout) and where it is going (file, HTTP response, child process stdin).
2. **Determine Stream Mode**: Decide whether the stream should operate in byte/string mode (default) or object mode (`{ objectMode: true }` for discrete JS objects).
3. **Establish Stream Interfaces**: 
   - Instantiate or implement the appropriate streams (`fs.createReadStream`, `fs.createWriteStream`, custom `Transform`, etc.).
   - If using child processes (e.g., ImageMagick, grep), map `child.stdout` and `child.stdin` as streams.
4. **Implement Backpressure Management**: 
   - Connect the streams using `.pipe()` which manages backpressure automatically.
   - If piping is not applicable, implement manual backpressure control: monitor `.write()` return values and bind to `.once('drain', ...)` to resume.
5. **Handle HTTP Specifics**: 
   - Parse the URL/Query parameters using the `url` module.
   - Resolve the MIME type (e.g., via the OS `file --brief --mime` command or an equivalent library) to set accurate `Content-Type` headers.
   - Set cache headers (`ETag`, `Last-Modified`) if applicable.
6. **Error Handling**: Attach `.on('error')` listeners to all streams to prevent unhandled exceptions from crashing the Node process.

# @Examples (Do's and Don'ts)

## File Copying and Serving
- **[DON'T]** Load entire files into memory.
```javascript
// Anti-pattern: Blocks event loop and risks memory overflow for large files
const block = fs.readFileSync('source.bin');
fs.writeFileSync('destination.bin', block);
```

- **[DO]** Use streams for file I/O to maintain constant memory usage.
```javascript
// Correct pattern: Pipes data smoothly without memory spikes
fs.createReadStream('source.bin')
  .pipe(fs.createWriteStream('destination.bin'))
  .on('close', () => console.log('Done.'));
```

## Implementing Custom Writable Streams with Backpressure
- **[DON'T]** Ignore the return value of a write operation.
```javascript
// Anti-pattern: Floods the buffer if the consumer is slower than the producer
while (dataHasMore()) {
    writable.write(getData());
}
```

- **[DO]** Observe the `highWaterMark` and wait for the `drain` event.
```javascript
// Correct pattern: Respects backpressure
function writeData(iterations, writer, data, encoding, cb) {
  (function write() {
    if (!iterations--) return cb();
    if (!writer.write(data, encoding)) {
      writer.once('drain', write); // Wait for drain before writing again
    } else {
      write(); // Continue immediately
    }
  })();
}
```

## Handling POST Data in HTTP Servers
- **[DON'T]** Attempt to read POST data synchronously or natively without stream listeners.
```javascript
// Anti-pattern: Fails to capture asynchronous chunks
http.createServer((req, res) => {
  if (req.method === 'POST') {
    let body = req.body; // Undefined in native HTTP module
    res.end(body);
  }
});
```

- **[DO]** Concatenate data chunks from the `readable` (or `data`) event and process on `end`.
```javascript
// Correct pattern: Buffers stream events appropriately
http.createServer((req, res) => {
  if (req.url === "/submit" && req.method === "POST") {
    let body = "";
    req.setEncoding('utf8');
    req.on('readable', () => {
      let data = req.read();
      if (data) body += data;
    });
    req.on('end', () => {
      let fields = querystring.parse(body);
      res.end(`Received: ${fields.sometext}`);
    });
  }
});
```

## Implementing Transform Streams
- **[DON'T]** Forget to call the callback or try to use `return` to pass transformed data.
```javascript
// Anti-pattern: Stalls the stream
converter._transform = function(chunk, encoding, cb) {
  return chunk.toString().toUpperCase(); 
};
```

- **[DO]** Use `this.push()` to send data and trigger `cb()` to indicate completion.
```javascript
// Correct pattern: Follows the Transform API
converter._transform = function(chunk, encoding, cb) {
  this.push(chunk.toString().toUpperCase());
  cb(); 
};
```