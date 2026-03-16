@Domain
These rules activate when the AI is requested to perform Node.js filesystem operations (I/O), path manipulations, static file serving, HTTP caching implementations, multipart file uploads, or when building desktop applications bridging Node.js and Chromium via Electron.

@Vocabulary
- **Ordinary Files**: A one-dimensional array of bytes that cannot contain other files.
- **Directories**: Files implemented in a special way to describe collections of other files.
- **Sockets**: Files used for Inter-Process Communication (IPC), allowing processes to exchange data.
- **Named Pipes**: Persistent, addressable pipes used for IPC across multiple processes (created via `mkfifo`).
- **Device Files**: Representations of I/O devices (e.g., character device `/dev/null`, block device `/dev/sda`).
- **Hard Link**: A direct pointer to a file, indistinguishable from the target, which shares the target's exact byte length.
- **Symbolic Link**: An indirect pointer to a file that does not react to changes in the target file's length.
- **File Descriptor (fd)**: A non-negative integer uniquely referencing a specific opened file in POSIX systems (e.g., 0 for stdin, 1 for stdout, 2 for stderr).
- **POSIX Flags**: String indicators for file operations (e.g., `r` for read, `w` for write, `a` for append, `x` for exclusive mode).
- **ETag (Entity Tag)**: An HTTP response header used to uniquely identify cached file entities based on size and modification time.
- **Location Header**: HTTP header used to indicate a redirection or the location of a newly created resource (status 201/202).
- **Content-Location Header**: HTTP header used to indicate the original location of an entity enclosed in a response, often used in content format negotiation.
- **Main Process (Electron)**: The underlying browser process that runs `main.js`, creates `BrowserWindow` objects, and manages the desktop application lifecycle.
- **Renderer Process (Electron)**: The process running within the web page that manipulates the DOM and can require Node modules.

@Objectives
The AI MUST achieve highly concurrent, non-blocking file I/O operations. The AI MUST prevent memory leaks and event loop blocking by strictly preferring stream-based processing over memory-buffering for large files. The AI MUST implement robust HTTP caching for static file servers to prevent redundant network transfers. The AI MUST handle file paths safely across diverse environments.

@Guidelines

- **Path Manipulation**: When parsing, building, or relating file paths, the AI MUST use the native `path` module (`path.normalize`, `path.join`, `path.dirname`, `path.basename`, `path.extname`, `path.relative`, `path.resolve`). The AI MUST NOT use manual string concatenation or regex for path building.
- **Untrusted Paths**: When handling file paths from untrusted or unreliable sources, the AI MUST use `path.normalize` to ensure a predictable format and resolve extraneous slashes or malformed segments via `fs.realpath`.
- **Synchronicity constraints**: The AI MUST strictly use asynchronous, non-blocking `fs` methods (e.g., `fs.readFile`, `fs.mkdir`). The AI MAY ONLY use synchronous methods (e.g., `fs.readFileSync`) during the initial loading and startup phase of a daemon/server (e.g., loading config files) before the event loop starts serving requests. The AI MUST NEVER use synchronous file I/O in route handlers or network request callbacks.
- **Stream vs. Memory**: When reading or copying files, the AI MUST assess file size constraints. For large files or files of unknown size, the AI MUST NOT use `fs.readFile` to prevent `RangeError` (exceeding 32-bit integer limits) or memory bloat. The AI MUST use `fs.createReadStream` and pipe to a `WritableStream`.
- **Line-by-Line Processing**: When a text file (like a logfile) needs to be read line-by-line, the AI MUST use the native `readline` module, passing the readable stream to `input` and setting `terminal: false`.
- **Concurrent Write Safety**: When multiple processes might simultaneously try to create the same file, the AI MUST use the exclusive write flags (`wx`, `wx+`, `ax`, `ax+`) in `fs.open` to fail safely if the file already exists.
- **Sequential Write Safety**: When using the low-level `fs.write` method, the AI MUST NOT call it multiple times on the same file without waiting for the callback to resolve. For chunked or continuous data writes, the AI MUST use `fs.createWriteStream` instead.
- **Flushing Core Buffers**: When a write operation requires absolute certainty that data exists on a stable storage device (e.g., recovering from system crashes), the AI MUST call `fs.fsync(fd)` to flush in-core data buffers to disk.
- **Link Attributes**: When checking or changing attributes of symbolic links, the AI MUST use link-specific methods (`fs.lstat`, `fs.lchown`, `fs.lchmod`) to avoid unintentionally modifying the target file.
- **File Descriptor Management**: When explicitly opening files via `fs.open`, the AI MUST ensure that every opened file descriptor is eventually closed using `fs.close(fd)` to prevent OS file descriptor limit exhaustion.
- **MIME Type Validation**: When streaming files to an HTTP response, the AI MUST set the correct `Content-Type` header. When accepting untrusted file uploads, the AI MUST NOT rely solely on the file extension. If true validation is needed, the AI MUST spawn a child process using `file --brief --mime [filename]` to query the Unix system for the true MIME type.
- **Static File Caching**: When building static file servers, the AI MUST implement Entity Tags (ETags). The AI MUST generate the ETag (e.g., `crypto.createHash('md5').update(stat.size + stat.mtime).digest('hex')`), check the incoming `If-None-Match` header, and return HTTP status `304` (Not Modified) without the body if they match.
- **Content Length Calculation**: When setting the `Content-Length` header, the AI MUST use bytes, not character lengths. The AI MUST use `stat.size` for files or `Buffer.byteLength` for string/buffer streams.
- **Multipart Uploads**: When handling POST file uploads, the AI MUST NOT attempt to parse multipart form data manually. The AI MUST use a proven module like `formidable`. The AI MUST configure `formidable.IncomingForm()`, set the `uploadDir`, and attach listeners to `file`, `field`, and `end` events.
- **Electron Architecture**: When building Electron applications, the AI MUST properly separate logic between the Main Process (creating `BrowserWindow`, `app` lifecycle events) and the Renderer Process (DOM manipulation, UI framework). The AI MAY safely require Node modules (like `fs` or `bluebird` for promisification) directly inside the Renderer Process scripts.

@Workflow
1. **Analyze Incoming Request**: Identify if the task requires reading, writing, path manipulation, file serving, uploading, or Electron setup.
2. **Path Resolution**: Pass all raw string paths through `path.join` or `path.resolve`. Run `path.normalize` on any user-provided path string.
3. **Stat Evaluation**: If serving or reading the file, execute `fs.stat` (or `fs.lstat` for symlinks).
   - If `err.errno === 34` or `err.code === 'ENOENT'`, return a 404 response.
   - For other errors, return a 500 response.
   - Validate if it is a directory using `stat.isDirectory()` or a file using `stat.isFile()`.
4. **Cache Negotiation (HTTP Serving)**:
   - Extract `stat.mtime` and `stat.size`.
   - Set `Last-Modified` header.
   - Generate MD5 ETag. Set `ETag` header.
   - Compare with `request.headers['if-none-match']`.
   - If matched, execute `response.statusCode = 304; return response.end();`.
5. **Stream Execution**:
   - If serving/copying, set `Content-Length` to `stat.size`.
   - Instantiate `fs.createReadStream(filename)` and attach `.pipe(response)`.
6. **Upload Processing (POST)**:
   - Verify request method is POST.
   - Instantiate `new formidable.IncomingForm()`.
   - Assign `form.uploadDir`.
   - Bind `.on('file')`, `.on('field')`, and `.on('end')` to parse and respond to the data stream.
7. **Electron Bootstrap** (If applicable):
   - In `main.js`, bind to `app.on('ready')` to initialize `BrowserWindow` and load the target `index.html`.
   - In `renderer.js`, initialize Promisified `fs` methods (e.g., `fs.lstatAsync`) and bind data to the UI (e.g., Vue.js).

@Examples (Do's and Don'ts)

- **Path Handling**
  - [DO]: `const target = path.join(__dirname, 'public', request.url);`
  - [DON'T]: `const target = __dirname + '/' + request.url;`

- **Serving Static Files**
  - [DO]:
    ```javascript
    fs.stat(filename, (err, stat) => {
        if (err) return response.end("Not found");
        const etag = crypto.createHash('md5').update(stat.size + stat.mtime).digest('hex');
        if (request.headers['if-none-match'] === etag) {
            response.statusCode = 304;
            return response.end();
        }
        response.writeHead(200, { 'Content-Length': stat.size, 'ETag': etag });
        fs.createReadStream(filename).pipe(response);
    });
    ```
  - [DON'T]:
    ```javascript
    // Blocks the event loop and loads entire file into memory; no caching.
    const data = fs.readFileSync(filename);
    response.end(data);
    ```

- **Reading Files Line by Line**
  - [DO]:
    ```javascript
    const rl = readline.createInterface({
        input: fs.createReadStream('server.log'),
        terminal: false
    });
    rl.on('line', (line) => { console.log(line); });
    ```
  - [DON'T]:
    ```javascript
    // Will run out of memory on large files
    const lines = fs.readFileSync('server.log', 'utf8').split('\n');
    lines.forEach(line => console.log(line));
    ```

- **File Creation / Concurrent Write Protection**
  - [DO]:
    ```javascript
    // Fails safely if 'config.json' already exists
    fs.open('config.json', 'wx', (err, fd) => {
        if (err) return console.error('File already exists or cannot be created');
        // proceed with writing
    });
    ```
  - [DON'T]:
    ```javascript
    // Blindly overwrites, creating race conditions if multiple processes run this
    fs.open('config.json', 'w', (err, fd) => { ... });
    ```

- **Handling File Uploads**
  - [DO]:
    ```javascript
    const form = new formidable.IncomingForm();
    form.uploadDir = process.cwd();
    form.on('file', (field, file) => { /* handle file */ })
        .on('end', () => { response.end('Upload complete'); });
    form.parse(request);
    ```
  - [DON'T]:
    ```javascript
    // Manually buffering chunked multipart data from requests
    let body = '';
    request.on('data', chunk => body += chunk);
    request.on('end', () => { parseMultipart(body); });
    ```