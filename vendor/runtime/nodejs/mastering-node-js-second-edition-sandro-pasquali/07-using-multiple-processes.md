@Domain
Node.js applications requiring vertical scaling, high-volume data parsing, CPU-heavy computations, multicore utilization, and the management or orchestration of multiple child processes or server clusters.

@Vocabulary
- **Concurrency**: A structural approach to modeling complex, simultaneous processes using non-blocking, event-driven callbacks within a single thread.
- **Parallelism**: A performance-focused approach that divides tasks across multiple available workers (e.g., CPU cores) to execute simultaneously.
- **Share-Nothing Architecture**: A design model where distinct processes operate in completely isolated memory spaces, avoiding synchronization collisions, race conditions, and deadlocks.
- **libuv**: The highly-efficient, multithreaded system delegate library that powers Node's asynchronous, event-driven I/O engine.
- **IPC (Inter-Process Communication)**: A communication channel established between a parent and child process (native to `fork`) allowing them to pass messages and socket handles.
- **Spawn**: A `child_process` method for executing native OS commands or non-Node programs as separate processes, returning streams for standard I/O.
- **Fork**: A `child_process` method specifically designed to execute Node.js programs, providing a built-in IPC channel.
- **Exec**: A `child_process` method that spawns a subshell, executes a command, and buffers the complete output (up to a `maxBuffer` limit) before passing it to a callback.
- **ExecFile**: A `child_process` method similar to `exec` but more efficient because it does not spawn a new subshell.
- **Cluster**: A native Node.js module that formalizes the master-worker pattern, allowing multiple child processes to transparently share the same network port.
- **PM2**: An enterprise-level process manager for Node.js used to daemonize, monitor, and cluster processes using declarative JSON manifests.

@Objectives
- Achieve application parallelism without resorting to custom multithreading or shared-memory locking within JavaScript.
- Distribute CPU-intensive operations and massive data processing tasks across multiple decoupled child processes.
- Maximize hardware utilization by spawning worker processes equal to the number of available CPU cores.
- Guarantee application resilience and continuous uptime by using isolated process memory spaces and managed restart policies.
- Ensure efficient and non-blocking Inter-Process Communication (IPC) by passing messages and socket handles between parent and child processes.

@Guidelines
- **Process Selection Strategy**:
  - The AI MUST use `child_process.spawn` when running system commands or non-Node applications (e.g., PHP, Ruby, Unix utilities).
  - The AI MUST use `child_process.fork` when spinning up Node.js child processes to guarantee an IPC channel.
  - The AI MUST use `child_process.exec` ONLY when the complete buffered output of a command is required and the output size is predictable and finite.
  - The AI MUST use `child_process.execFile` instead of `exec` when executing a Node file directly to avoid the overhead of a subshell.
- **Managing Child Processes (`spawn` / `fork`)**:
  - The AI MUST handle I/O streams using `child.stdout.on('readable', ...)` or by defining `stdio` inheritance.
  - When explicitly detaching a process using `{ detached: true }`, the AI MUST call `child.unref()` if the parent process should not wait for the child to exit.
  - The AI MUST explicitly call `process.exit()` within a forked child process when its work is complete, as forked processes do not exit automatically.
  - The AI MUST NOT attempt to call `child.kill()` on a process that has already exited, as the OS may have reassigned the PID to a new, unrelated process.
- **Managing Exec Buffers**:
  - When using `exec`, the AI MUST account for the `maxBuffer` limit (default 200 KB) and handle potential crashes if the output exceeds this limit.
- **Implementing Clusters**:
  - The AI MUST conditionally branch cluster logic using `cluster.isMaster` (to fork workers) and `cluster.isWorker` (to instantiate the shared server/logic).
  - The AI MUST dynamically determine the number of child processes to fork using `require('os').cpus().length`.
  - The AI MUST gracefully terminate clusters using `worker.disconnect()`, allowing existing connections to close normally, rather than forcefully calling `worker.kill()`.
  - The AI MUST check a worker's `suicide` property (as defined in the text's API) during an `exit` event to distinguish between an intentional disconnect and an accidental crash.
- **Passing Sockets**:
  - The AI MUST pass socket handles to child processes via the second argument of the `send` method: `child.send(message, socketHandle)`.
- **Using PM2**:
  - The AI MUST define PM2 deployments using a declarative JSON process file (e.g., `process.json`).
  - The AI MUST use the PM2 setting `"exec_mode": "cluster"` and `"instances": 0` (or `"instances": "max"`) to automatically load-balance across all available CPU cores.
  - The AI MUST configure PM2 watchers via the `"watch"` array and exclude log files using `"ignore_watch"` to prevent infinite restart loops.

@Workflow
1. **Analyze the Scaling Requirement**: Determine if the task requires executing a system command (`spawn`), processing a finite script output (`exec`), running a background Node task (`fork`), or load-balancing a web server (`cluster` / PM2).
2. **Implement the Master/Parent Context**:
   - Initialize the `os` module to count CPU cores.
   - If clustering, wrap the master logic in `if (cluster.isMaster)`.
   - Iterate over the CPU count to trigger the required number of `fork()` calls.
3. **Implement the Worker/Child Context**:
   - Wrap worker execution in `if (cluster.isWorker)` (if using `cluster`) or place it in a separate file (if using `fork`).
   - Instantiate the server, binding it to the designated port (the OS/Node will handle port sharing automatically).
   - Establish `process.on('message', ...)` listeners to handle incoming IPC data.
4. **Implement Communication and Data Aggregation**:
   - In the master, attach `.on('message', ...)` listeners to the created workers to aggregate results or broadcast updates (e.g., via Server-Sent Events or WebSockets) to connected clients.
5. **Implement Graceful Exits and Error Handling**:
   - Listen for `exit` or `disconnect` events on the master.
   - Check if the exit was intentional; if not, invoke a new `fork()` to maintain the worker pool.
6. **Abstract to PM2 (For Production)**:
   - Generate a `process.json` file defining the application environment, setting instances, execution mode, and memory restart limits (`max_memory_restart`).

@Examples (Do's and Don'ts)

- **[DO]** Use `cluster` to share a single port across multiple CPU cores natively:
  ```javascript
  const cluster = require('cluster');
  const http = require('http');
  const numCPUs = require('os').cpus().length;

  if (cluster.isMaster) {
    for (let i = 0; i < numCPUs; i++) {
      cluster.fork();
    }
    cluster.on('exit', (worker, code, signal) => {
      if (!worker.suicide) {
        console.log(`Worker ${worker.process.pid} died accidentally. Restarting...`);
        cluster.fork();
      }
    });
  } else {
    http.createServer((req, res) => {
      res.writeHead(200);
      res.end(`Handled by worker ${cluster.worker.id}`);
    }).listen(8080);
  }
  ```

- **[DON'T]** Use `exec` for processes with massive or infinite output, as it will crash when exceeding `maxBuffer`:
  ```javascript
  const { exec } = require('child_process');
  // ANTI-PATTERN: `tail -f` runs forever, exceeding maxBuffer and crashing.
  exec('tail -f /var/log/system.log', (err, stdout, stderr) => {
    console.log(stdout); 
  });
  ```

- **[DO]** Pass a socket handle from a parent to a child process using IPC:
  ```javascript
  // Parent Process
  const fork = require('child_process').fork;
  const net = require('net');
  const child = fork('./child.js');

  net.createServer((socket) => {
    child.send('socket', socket);
  }).listen(8080);

  // Child Process (child.js)
  process.on('message', (msg, socket) => {
    if (msg === 'socket') {
      socket.write(`Child handled your connection.\r\n`);
      socket.end();
    }
  });
  ```

- **[DON'T]** Forget to explicitly exit a forked child process once its work is complete, leaving zombie processes in memory:
  ```javascript
  // ANTI-PATTERN: No process.exit() called.
  process.on('message', (msg) => {
    let result = heavyComputation(msg);
    process.send(result);
    // Missing process.exit() here
  });
  ```

- **[DO]** Create a PM2 `process.json` for declarative cluster configuration:
  ```json
  {
    "apps": [{
      "name": "api-server",
      "script": "./server.js",
      "watch": true,
      "ignore_watch": ["**/*.log"],
      "env": {
        "NODE_ENV": "production"
      },
      "instances": 0,
      "exec_mode": "cluster",
      "max_memory_restart": "300M"
    }]
  }
  ```