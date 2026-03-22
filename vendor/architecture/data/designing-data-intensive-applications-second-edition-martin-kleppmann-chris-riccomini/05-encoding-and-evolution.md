@Domain
These rules trigger whenever the AI is tasked with defining, modifying, or evaluating data models, schemas, serialization/encoding formats (e.g., JSON, Protocol Buffers, Avro), API designs (REST, gRPC, RPC), workflow definitions (durable execution), or asynchronous message-passing architectures (message brokers, actor models).

@Vocabulary
- **Encoding/Serialization/Marshalling**: The translation from in-memory data representations (objects, structs) to a byte sequence for network transmission or file storage.
- **Decoding/Parsing/Deserialization/Unmarshalling**: The reverse of encoding; translating a byte sequence back into an in-memory data structure.
- **Backward Compatibility**: The ability of newer code to read data that was written by older code.
- **Forward Compatibility**: The ability of older code to read data that was written by newer code (requires ignoring unknown additions).
- **Rolling Upgrade / Staged Rollout**: Deploying a new version of an application to a few nodes at a time to avoid downtime, requiring old and new versions to coexist and communicate.
- **Field Tags**: Numeric identifiers used in Protocol Buffers (and Thrift) to represent fields in the binary encoding instead of using field names.
- **Writer's Schema**: The specific schema version used by an application when encoding/writing data (e.g., in Avro).
- **Reader's Schema**: The specific schema version used by an application when decoding/reading data (e.g., in Avro).
- **RPC (Remote Procedure Call)**: A network communication model that attempts to make a remote network request look like a local function call (concept known as location transparency).
- **Idempotence**: A property of operations where performing them multiple times yields the same result as performing them exactly once; critical for safely retrying failed network requests.
- **Durable Execution**: A framework pattern (e.g., Temporal) that provides exactly-once semantics for workflows by logging all RPCs and state changes to a write-ahead log (WAL), replaying them deterministically upon failure.
- **Message Broker**: An intermediary system (e.g., Kafka, RabbitMQ) that stores and routes asynchronous messages between decoupled senders and recipients.
- **Actor Model**: A concurrency model where logic is encapsulated in independent entities (actors) that communicate exclusively via asynchronous message passing.

@Objectives
- Guarantee safe schema evolution by strictly adhering to forward and backward compatibility rules.
- Prevent data loss during read-modify-write cycles in systems undergoing rolling upgrades.
- Select the optimal encoding format based on the system's requirements (e.g., avoiding language-specific encodings for persistent data).
- Design robust network interactions that account for the fundamental unpredictability, latency, and partial failure states of remote procedure calls.
- Ensure strict determinism in durable execution workflows.

@Guidelines

**1. Encoding Format Selection & Restrictions**
- The AI MUST NOT use or recommend language-specific encoding formats (e.g., Java `java.io.Serializable`, Python `pickle`, Ruby `Marshal`) for saving data to databases, writing to files, or sending data across the network to other services. These formats pose severe security risks (arbitrary code execution), tie the system to a single language, and lack versioning.
- The AI MUST prefer standardized binary encodings (Protocol Buffers, Avro) for internal microservice communication and persistent data storage.
- The AI MUST use JSON or XML primarily for public-facing web APIs (RESTful services) or data interchange between distinct organizations, recognizing their verbosity and parsing overhead.

**2. JSON and Textual Format Handling**
- When working with JSON, the AI MUST encode 64-bit integers (e.g., Twitter/X snowflake IDs) as strings, or include a redundant string representation, because languages that parse JSON numbers into IEEE 754 double-precision floating-point numbers (like JavaScript) will lose precision for integers greater than 2^53.
- The AI MUST NOT use Base64-encoded strings inside JSON/XML if a highly efficient, high-volume binary data transfer is required; it must switch to a schema-driven binary format instead.

**3. Protocol Buffers (and Thrift) Schema Evolution**
- The AI MUST NOT change the tag number of an existing field.
- The AI MUST NOT reuse a tag number that was previously used by a deleted field. It MUST explicitly mark deleted tag numbers as `reserved` to prevent accidental reuse.
- When adding a new field, the AI MUST assign it a new, previously unused tag number.
- When removing a field, the AI MUST ensure the field is not required (or is removed from the codebase entirely) before removing it from the schema.
- The AI MUST warn against changing field datatypes (e.g., changing an `int32` to an `int64`), as this can lead to silent truncation when newer data is read by older code.

**4. Avro Schema Evolution**
- The AI MUST ensure that any field added to or removed from an Avro schema has a defined `default` value to maintain both forward and backward compatibility.
- If a field is intended to be nullable in Avro, the AI MUST define it using a union type where `null` is the first branch (e.g., `union { null, string } field_name = null;`).
- The AI MUST recognize that changing a field name in Avro breaks forward compatibility unless aliases are carefully managed in the reader's schema.
- When generating schemas dynamically from a relational database, the AI MUST recommend Avro over Protocol Buffers because Avro matches fields by name rather than requiring manually maintained tag numbers.

**5. Preserving Data During Rolling Upgrades**
- When implementing a read-modify-write cycle (e.g., decoding a record, updating a field, and encoding it back to the database), the AI MUST ensure that the application code preserves unknown fields. If older code reads data written by newer code, it must not drop the new fields when saving the record back.

**6. Network Communication & RPC Design**
- The AI MUST NOT treat network calls (RPC/REST) identically to local function calls.
- The AI MUST implement explicit timeout handling for all network requests.
- The AI MUST implement retry logic using exponential backoff, while explicitly avoiding retry storms during system overloads.
- The AI MUST ensure that all retriable endpoints are idempotent (e.g., by requiring unique request IDs/deduplication keys) to prevent duplicate execution when network responses are lost.
- For public APIs, the AI MUST implement explicit API versioning (e.g., via URL paths or HTTP `Accept` headers). For internal RPC, the AI MUST rely on the forward/backward compatibility of the underlying schema (Protobuf/Avro).

**7. Durable Execution and Workflows**
- When writing tasks/activities for durable execution frameworks (e.g., Temporal, Restate), the AI MUST ensure the workflow definition is strictly deterministic.
- The AI MUST NOT use standard system clocks (e.g., `time.now()`), random number generators (RNG), or direct I/O inside the workflow orchestration code. It MUST use the framework's provided deterministic APIs (e.g., `workflow.now()`).
- The AI MUST NOT reorder existing function/activity calls in a workflow definition if those workflows have running executions, as this will break the event history replay.

**8. Event-Driven Messaging**
- When configuring message brokers (Kafka, RabbitMQ), the AI MUST define a schema registry to manage and validate the writer's/reader's schemas.
- If an actor or consumer republishes a message to another topic, the AI MUST guarantee that unknown fields are preserved to prevent data loss.

@Workflow
1. **Analyze Context**: Determine the mode of dataflow: Database storage, REST/RPC service communication, Durable Workflow, or Asynchronous Messaging.
2. **Format Selection**: Choose the serialization format. Rule out language-specific encoders. Select JSON/XML for web/public APIs, and Protobuf/Avro for internal RPC/storage.
3. **Schema Definition & Modification**:
   - If Protobuf: Verify tag numbers are immutable and deleted tags are `reserved`.
   - If Avro: Verify `default` values are provided for all additions/removals and unions are used for `null`.
   - If JSON: Validate 64-bit integer handling (stringify large numbers).
4. **Compatibility Check**: Validate that the schema change supports both backward compatibility (new reader, old writer) and forward compatibility (old reader, new writer) to support staged rollouts.
5. **Network / Workflow Hardening**: 
   - Add idempotency keys, timeouts, and safe retry logic for RPCs.
   - Enforce determinism (no local clocks/RNG) if writing workflow orchestrations.
6. **Data Preservation Check**: Ensure decoding/encoding cycles in the application explicitly retain unknown fields.

@Examples (Do's and Don'ts)

**Example 1: Language-Specific Serialization**
- [DO]: Use standard data formats like JSON or Protobuf for caching objects in Redis.
- [DON'T]: Use Python's `pickle.dumps()` or Java's `ObjectOutputStream` to serialize objects into a database, as this locks the data to the language and introduces severe remote code execution vulnerabilities.

**Example 2: 64-bit Integers in JSON**
- [DO]: Represent a large database ID in JSON as a string or provide a stringified fallback: `{"post_id": 10453840294839201, "post_id_str": "10453840294839201"}`.
- [DON'T]: Send raw 64-bit integers `{"post_id": 10453840294839201}` to web clients, as JavaScript will parse it into a floating-point number and alter the trailing digits, corrupting the ID.

**Example 3: Protocol Buffers Schema Evolution**
- [DO]: When removing a field, reserve its tag number to prevent future use:
  ```proto
  message Person {
    reserved 2; // Old favorite_number field
    string user_name = 1;
    repeated string interests = 3;
  }
  ```
- [DON'T]: Re-use a tag number for a new field:
  ```proto
  message Person {
    string user_name = 1;
    string new_favorite_color = 2; // BAD: Re-using tag 2 will corrupt older data
    repeated string interests = 3;
  }
  ```

**Example 4: Avro Schema Nullability**
- [DO]: Define nullable fields with a union type and a default:
  `{"name": "favoriteNumber", "type": ["null", "long"], "default": null}`
- [DON'T]: Define a field as just `long` if it needs to be optional or nullable, as Avro requires explicit unions for nulls to enforce strict typing.

**Example 5: Durable Execution Workflows**
- [DO]: Use framework-provided deterministic functions:
  `current_time = await workflow.now()`
- [DON'T]: Use native system time functions inside the workflow definition:
  `current_time = datetime.now() // BAD: Breaks deterministic replay upon failure recovery.`

**Example 6: Preserving Data in Read-Modify-Write**
- [DO]: Deserialize data into an object model that captures unknown fields into a generic map, and serialize those unknown fields back out when writing to the database.
- [DON'T]: Deserialize data into a strict struct that drops unknown fields, update one field, and save the strict struct back to the database. If an older code version does this to a record written by a newer code version, the newly added fields will be permanently deleted.