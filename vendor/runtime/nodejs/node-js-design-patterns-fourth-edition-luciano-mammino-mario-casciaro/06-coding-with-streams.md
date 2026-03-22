@Domain
This rule file applies to any task, file, or user request involving Node.js streams, including data ingestion, file I/O, network communication, large dataset processing, data transformation pipelines, backpressure management, and stream composition/piping.

@Vocabulary
- **Buffer Mode**: An I/O pattern where all data is accumulated into memory until the operation completes before being passed to the consumer.
- **Stream Mode**: An I/O pattern where data is processed incrementally as it arrives in chunks.
- **Spatial Efficiency**: The memory-saving characteristic of streams, achieved by keeping only small chunks of data in memory at any given time.
- **Time Efficiency**: The speed advantage of streams, achieved by starting data processing as soon as the first chunk arrives (concurrent assembly line) rather than waiting for the entire payload.
- **Backpressure**: A signaling mechanism in Node.js streams where `write()` returns `false` to indicate that the internal buffer has exceeded the `highWaterMark`, alerting the producer to pause sending data until a `drain` event is emitted.
- **Readable Stream**: A stream representing a source of data.
- **Writable Stream**: A stream representing a data destination.
- **Duplex Stream**: A stream that is both Readable and Writable (e.g., a network socket).
- **Transform Stream**: A special Duplex stream that applies transformations to the data as it flows from the Writable side to the Readable side.
- **PassThrough Stream**: A Transform stream that outputs every chunk without modification; used for observability, late piping, or lazy initialization.
- **Non-flowing (Paused) Mode**: The default Readable mode where data is explicitly pulled on demand using the `readable` event and the `read()` method.
- **Flowing Mode**: A Readable mode where data is pushed continuously as soon as it arrives, activated by attaching a `data` event listener or calling `resume()`.
- **Binary Mode**: The default stream mode handling chunks as Buffers or Strings.
- **Object Mode**: A stream mode handling data as sequences of discrete JavaScript objects.
- **pipeline()**: A utility from `node:stream/promises` or `node:stream` used to safely connect multiple streams and automatically manage cleanup and error propagation.
- **compose()**: A utility from `node:stream` used to merge multiple streams into a single reusable Duplex stream while preserving backpressure and error propagation.
- **Multiplexing/Demultiplexing**: Combining multiple logically separated streams into a single shared channel (e.g., using packet switching with channel IDs and length prefixes), and separating them at the destination.
- **Web Streams**: The WHATWG standard streaming API (`ReadableStream`, `WritableStream`, `TransformStream`), available in Node.js and browsers.

@Objectives
- Maximize spatial and time efficiency by strictly preferring streaming APIs over buffered APIs for data processing and I/O.
- Ensure application stability by rigorously respecting and managing stream backpressure.
- Prevent resource leaks and dangling file descriptors by completely avoiding the raw `.pipe()` method in favor of `pipeline()` or `compose()`.
- Reduce boilerplate and manual string/buffer concatenation by utilizing built-in `node:stream/consumers` and native Readable stream utility methods (`.map()`, `.filter()`, etc.).
- Maintain robust stream architectures through proper implementation of stream interfaces (`_read`, `_write`, `_transform`, `_flush`) and accurate error propagation.

@Guidelines

- **General Streaming Rules**
  - The AI MUST use streaming APIs (e.g., `createReadStream`, `createWriteStream`) instead of buffered APIs (e.g., `readFile`, `writeFile`) when handling large files, network requests, or operations with unknown data sizes to ensure spatial and time efficiency.
  - The AI MUST explicitly set `objectMode: true` in the stream options when building streams that consume or emit JavaScript objects instead of Buffers or strings.
  - The AI MUST define the `highWaterMark` option when the default buffer limit (16KB) is inappropriate for the specific use case.

- **Consuming Readable Streams**
  - The AI MUST prefer async iterators (`for await (const chunk of stream)`) as the primary mechanism for consuming Readable streams due to their superior readability and native backpressure handling.
  - If event-based consumption is required, the AI MUST prefer the Non-flowing mode by listening to the `readable` event and using a `while ((chunk = stream.read()) !== null)` loop.
  - The AI MUST avoid Flowing mode (listening to the `data` event) unless interacting with legacy code, as it offers less control over data flow.
  - When streaming text data in binary mode, the AI MUST call `setEncoding('utf8')` on the Readable stream to ensure multibyte characters are properly decoded without being split across chunks.

- **Implementing Custom Streams**
  - **Readable Streams**: The AI MUST implement the `_read(size)` method. The AI MUST signal the end of the stream by calling `this.push(null)`.
  - **Writable Streams**: The AI MUST implement the `_write(chunk, encoding, cb)` method. The AI MUST invoke the `cb(error)` callback when the chunk is flushed to the underlying resource.
  - **Transform Streams**: The AI MUST implement the `_transform(chunk, encoding, cb)` method. The AI MUST call `this.push(data)` to pass transformed data forward and MUST invoke `cb()` when done.
  - **Transform Flush**: The AI MUST implement the `_flush(cb)` method in Transform streams if there is leftover state or buffered data (e.g., an incomplete chunk or a "tail" variable) that needs to be pushed before the stream closes.
  - **Simplified Construction**: For simple streams without complex internal state, the AI MUST prefer the simplified construction syntax (`new Readable({ read(size) { ... } })`, `new Writable({ write(...) { ... } })`, `new Transform({ transform(...) { ... } })`).

- **Handling Backpressure**
  - When writing manually to a Writable stream, the AI MUST check the boolean return value of `writable.write(chunk)`.
  - If `write()` returns `false`, the AI MUST stop writing immediately and MUST wait for the `drain` event to be emitted by the Writable stream before resuming writes.

- **Composing and Piping Streams**
  - The AI MUST NOT use the raw `.pipe()` method for production stream pipelines, as it fails to propagate errors and leaves streams open if an intermediate stream crashes.
  - The AI MUST use `pipeline` from `node:stream/promises` (or `node:stream` with callbacks) to connect streams, ensuring that all streams are destroyed and resources are cleaned up if an error occurs.
  - When creating a reusable pipeline of streams that needs to be exported and consumed as a single black-box stream, the AI MUST use `compose(stream1, stream2, ...)` from `node:stream` to generate a single Duplex stream.

- **Piping Patterns**
  - **Forking**: When piping one Readable stream into multiple Writable streams, the AI MUST account for the fact that backpressure is dictated by the slowest Writable stream, which can bottleneck the entire pipeline.
  - **Merging**: When piping multiple Readable streams into a single Writable stream, the AI MUST pass `{ end: false }` to the pipe/pipeline options to prevent the destination from closing prematurely. The AI MUST manually call `end()` on the Writable stream only when all source Readable streams have emitted the `end` event.
  - **PassThrough**: The AI MUST use `PassThrough` streams to implement observability (e.g., counting bytes flowing through a pipeline without altering data) or to enable late piping (providing a stream placeholder when the data source/destination is determined asynchronously).
  - **Multiplexing**: To transmit multiple streams over a single shared channel, the AI MUST implement packet switching by prepending a Channel ID and a Length Prefix (e.g., using `Buffer.alloc(1 + 4 + chunk.length)`) to each chunk.
  - **Demultiplexing**: The AI MUST process multiplexed streams in Non-flowing mode (`read(size)`) to accurately extract the Channel ID, evaluate the Length Prefix, and extract the exact payload chunk for routing.

- **Advanced Stream Utilities and Processing**
  - The AI MUST utilize built-in Readable stream helpers (`.map()`, `.filter()`, `.reduce()`, `.flatMap()`, `.drop()`, `.take()`, `.some()`, `.every()`, `.find()`) for data transformation pipelines instead of writing custom Transform streams for simple operations.
  - If a full stream payload must be accumulated into memory (e.g., to parse a JSON response), the AI MUST use the `node:stream/consumers` module (e.g., `await consumers.json(stream)`, `consumers.text(stream)`, `consumers.buffer(stream)`) instead of manually concatenating chunks in a `data` event listener.
  - The AI MUST use `Readable.from(iterable)` to convert arrays, generators, or async iterables into Readable streams, avoiding loading massive arrays into memory upfront.

- **Web Streams Interoperability**
  - When interacting with APIs requiring Web Streams (e.g., `fetch`), the AI MUST convert Node.js streams to Web Streams using `Readable.toWeb()`, `Writable.toWeb()`, or `Transform.toWeb()`.
  - When adapting Web Streams back to Node.js streams, the AI MUST use `Readable.fromWeb()`, `Writable.fromWeb()`, or `Transform.fromWeb()`.

@Workflow
1. **Analyze I/O Constraints**: Determine if the operation deals with potentially large files, network requests, or continuous data. If yes, select a streaming approach.
2. **Determine Stream Mode**: Decide whether the stream handles raw bytes (Binary Mode) or discrete JavaScript objects (Object Mode).
3. **Select Implementation Strategy**: Use simplified construction (`new Transform({ ... })`) for straightforward logic, or class inheritance (`class MyStream extends Transform`) if complex internal state management is required.
4. **Build Transformation Logic**: If implementing a Transform stream, write logic in `_transform`. If the transformation requires aggregating partial chunks across boundaries, buffer them in a class variable and process the remainder in `_flush`.
5. **Assemble Pipeline**: Chain the readable, transform, and writable streams using `await pipeline(...)` to guarantee safe error handling and cleanup.
6. **Evaluate Final Consumption**: If the final step requires full aggregation in memory, pass the pipeline's output (or the raw stream) to `consumers.json()` or `consumers.text()`.

@Examples (Do's and Don'ts)

- **[DO] Connect streams safely using `pipeline` from `stream/promises`:**
  ```javascript
  import { createReadStream, createWriteStream } from 'node:fs';
  import { createGzip } from 'node:zlib';
  import { pipeline } from 'node:stream/promises';

  try {
    await pipeline(
      createReadStream('input.txt'),
      createGzip(),
      createWriteStream('input.txt.gz')
    );
    console.log('Pipeline succeeded.');
  } catch (err) {
    console.error('Pipeline failed.', err);
  }
  ```

- **[DON'T] Use raw `.pipe()` to connect streams in production (causes resource leaks on error):**
  ```javascript
  import { createReadStream, createWriteStream } from 'node:fs';
  import { createGzip } from 'node:zlib';

  // ANTI-PATTERN: Errors in the read stream or gzip stream will not be caught
  // and streams will not be properly destroyed.
  createReadStream('input.txt')
    .pipe(createGzip())
    .pipe(createWriteStream('input.txt.gz'))
    .on('finish', () => console.log('Done'));
  ```

- **[DO] Handle backpressure manually when writing to a stream:**
  ```javascript
  function writeData(writable, dataArray) {
    let i = 0;
    function generateMore() {
      while (i < dataArray.length) {
        const chunk = dataArray[i++];
        const canContinue = writable.write(chunk);
        if (!canContinue) {
          // Backpressure reached: wait for drain event before resuming
          writable.once('drain', generateMore);
          return;
        }
      }
      writable.end();
    }
    generateMore();
  }
  ```

- **[DON'T] Ignore the return value of `write()` (causes memory bloat):**
  ```javascript
  function writeData(writable, dataArray) {
    // ANTI-PATTERN: Pushing data without checking backpressure
    for (const chunk of dataArray) {
      writable.write(chunk); 
    }
    writable.end();
  }
  ```

- **[DO] Use `node:stream/consumers` to aggregate stream data into memory:**
  ```javascript
  import { request } from 'node:https';
  import consumers from 'node:stream/consumers';

  const req = request('https://example.com/data.json', async (res) => {
    try {
      const data = await consumers.json(res);
      console.log('Parsed JSON:', data);
    } catch (err) {
      console.error('Failed to parse:', err);
    }
  });
  req.end();
  ```

- **[DON'T] Manually concatenate string/buffer chunks for JSON parsing:**
  ```javascript
  import { request } from 'node:https';

  const req = request('https://example.com/data.json', (res) => {
    let buffer = '';
    res.on('data', chunk => {
      buffer += chunk; // ANTI-PATTERN: Error prone, character splitting issues
    });
    res.on('end', () => {
      console.log('Parsed JSON:', JSON.parse(buffer));
    });
  });
  req.end();
  ```

- **[DO] Use `compose` to create a reusable black-box stream pipeline:**
  ```javascript
  import { compose } from 'node:stream';
  import { createGzip } from 'node:zlib';
  import { createCipheriv } from 'node:crypto';

  export function createCompressAndEncrypt(key, iv) {
    // Returns a single Duplex stream merging Gzip and Cipher
    return compose(
      createGzip(),
      createCipheriv('aes192', key, iv)
    );
  }
  ```

- **[DO] Implement `_flush` in a Transform stream to handle leftover buffer data:**
  ```javascript
  import { Transform } from 'node:stream';

  export class ReplaceStream extends Transform {
    constructor(searchStr, replaceStr, options) {
      super({ ...options });
      this.searchStr = searchStr;
      this.replaceStr = replaceStr;
      this.tail = '';
    }

    _transform(chunk, enc, cb) {
      const pieces = (this.tail + chunk).split(this.searchStr);
      const lastPiece = pieces[pieces.length - 1];
      const tailLen = this.searchStr.length - 1;
      this.tail = lastPiece.slice(-tailLen);
      pieces[pieces.length - 1] = lastPiece.slice(0, -tailLen);
      this.push(pieces.join(this.replaceStr));
      cb();
    }

    _flush(cb) {
      // Push any remaining data in the tail before closing
      this.push(this.tail);
      cb();
    }
  }
  ```