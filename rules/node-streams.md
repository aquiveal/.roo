# Node.js Streams & Data Processing Rules

## Stream vs. Buffer (Prefer Streaming)
**Context:** Loading entire files into memory (Buffering) is inefficient and can crash the application with "Out of Memory" errors when dealing with large datasets. Streams process data chunk-by-chunk, keeping memory usage constant regardless of file size (Chapter 6).
**Directive:** ALWAYS prefer Streams over Buffers for file I/O, network responses, or large data transformation tasks.

### ❌ Anti-Pattern (What to avoid)
```javascript
// Reading a massive log file fully into memory before processing.
// If the file is 4GB and the heap limit is 2GB, the process will crash.
import { readFile, writeFile } from 'node:fs/promises';
import { gzip } from 'node:zlib';
import { promisify } from 'node:util';

const gzipPromise = promisify(gzip);

async function compressFile(inputPath, outputPath) {
  // Reads entire content into a Buffer
  const content = await readFile(inputPath);
  
  // Allocates another huge buffer for compressed data
  const compressed = await gzipPromise(content);
  
  // Writes entire buffer to disk
  await writeFile(outputPath, compressed);
}
```

### ✅ Best Practice (What to do)
```javascript
// Piping data through streams.
// Memory usage remains low (e.g., 64KB chunks) regardless of file size.
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';
import { pipeline } from 'node:stream/promises';

async function compressFile(inputPath, outputPath) {
  // Data flows from source -> transform -> destination
  await pipeline(
    createReadStream(inputPath),
    createGzip(),
    createWriteStream(outputPath)
  );
  console.log('Compression complete');
}
```

## Use Pipeline over Pipe
**Context:** The `.pipe()` method does not automatically destroy source/destination streams if an error occurs in the middle of the chain, leading to memory leaks and hanging file descriptors. `pipeline` handles error propagation and cleanup correctly (Chapter 6).
**Directive:** ALWAYS use `stream.pipeline` (callback) or `stream/promises.pipeline` (async) instead of `.pipe()` for production code.

### ❌ Anti-Pattern (What to avoid)
```javascript
// Traditional piping.
// If 'transform' emits an error, 'source' is not closed automatically.
// Error handling is fragmented and verbose.
source
  .pipe(transform)
  .pipe(destination)
  .on('error', (err) => {
    console.error('Pipeline failed', err);
    // Must manually destroy streams to prevent leaks
    source.destroy();
    destination.destroy();
  });
```

### ✅ Best Practice (What to do)
```javascript
// Using pipeline ensures that if ANY stream fails, ALL are destroyed.
// It provides a single point for error handling.
import { pipeline } from 'node:stream/promises';

try {
  await pipeline(
    source,
    transform,
    destination
  );
  console.log('Pipeline succeeded');
} catch (err) {
  console.error('Pipeline failed, all streams cleaned up', err);
}
```

## Composable Transforms
**Context:** Monolithic transform functions are hard to reuse and test. Creating small, focused Transform streams allows you to compose complex processing pipelines from reusable blocks (Chapter 6).
**Directive:** Break complex data processing into small, single-purpose Transform streams (e.g., `Filter`, `Map`, `Compress`) and compose them.

### ❌ Anti-Pattern (What to avoid)
```javascript
// A "God stream" that does too much.
// It parses CSV, filters rows, and encrypts data all in one place.
// Hard to test just the filtering logic or reuse the encryption part.
const complexTransform = new Transform({
  transform(chunk, encoding, callback) {
    const lines = chunk.toString().split('\n');
    for (const line of lines) {
      const data = parseCSV(line);
      if (data.isValid) {
        const encrypted = encrypt(data);
        this.push(encrypted);
      }
    }
    callback();
  }
});
```

### ✅ Best Practice (What to do)
```javascript
// Composing small streams using `stream.compose` (Node 16+) or simple piping.
// Each stream does ONE thing well.
import { compose } from 'node:stream';

const csvParser = new Transform({ /* ... logic to parse chunks to objects ... */ });
const validDataFilter = new Transform({ 
  objectMode: true,
  transform(chunk, enc, cb) {
    if (chunk.isValid) this.push(chunk);
    cb();
  }
});
const encryptor = new Transform({ /* ... logic to encrypt objects ... */ });

// The combined stream can be used as a single unit
const processingPipeline = compose(csvParser, validDataFilter, encryptor);

source.pipe(processingPipeline).pipe(destination);
```

## Handle Backpressure
**Context:** If a Readable stream pushes data faster than a Writable stream can consume it (e.g., reading from SSD, writing to a slow network), data accumulates in memory buffers. Ignoring `write()` return values leads to unlimited buffering and crashes (Chapter 6).
**Directive:** ALWAYS handle backpressure by checking `stream.write()` return value and waiting for the `drain` event if it returns `false`.

### ❌ Anti-Pattern (What to avoid)
```javascript
// Naive implementation of a writable stream interface.
// It ignores the return value of push/write.
// If the destination is slow, 'internalBuffer' grows indefinitely.
function writeData(source, destination) {
  source.on('data', (chunk) => {
    // DANGEROUS: Keeps pushing even if destination is overwhelmed
    destination.write(chunk);
  });
}
```

### ✅ Best Practice (What to do)
```javascript
// Respecting the stream's capacity.
// If write returns false, we pause reading until the destination drains.
function writeData(source, destination) {
  source.on('data', (chunk) => {
    const canContinue = destination.write(chunk);
    
    if (!canContinue) {
      // Pause the source to stop influx of data
      source.pause();
      
      // Wait for destination to be ready again
      destination.once('drain', () => {
        source.resume();
      });
    }
  });
}
// Note: using `pipeline()` handles this automatically for you!
```
