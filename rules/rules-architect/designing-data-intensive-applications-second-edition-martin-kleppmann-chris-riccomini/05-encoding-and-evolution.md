@Domain
These rules MUST be activated when the AI is engaged in tasks involving data modeling, schema definition, API design (REST/RPC), database migrations, message broker configuration, workflow/durable execution implementation, or writing data encoding/decoding logic.

@Vocabulary
- **Evolvability:** The ability of a system to easily adapt to changes (new features, requirements) without requiring simultaneous, system-wide updates.
- **Rolling Upgrade (Staged Rollout):** Deploying a new version of software to a few nodes at a time to prevent downtime, resulting in old and new code running concurrently.
- **Backward Compatibility:** Newer code can read data that was written by older code.
- **Forward Compatibility:** Older code can read data that was written by newer code.
- **Encoding (Serialization/Marshalling):** Translating in-memory data structures (objects, pointers) into a flat byte sequence suitable for network transmission or disk storage.
- **Decoding (Deserialization/Unmarshalling):** Translating a byte sequence back into an in-memory data structure.
- **Field Tag:** A numeric identifier used in schema-driven formats (like Protocol Buffers/Thrift) to alias field names, saving space and enabling schema evolution.
- **Writer's Schema:** The exact schema version used by an application when encoding data.
- **Reader's Schema:** The schema version expected by the application decoding the data, which may differ from the Writer's Schema.
- **Data Outlives Code:** The concept that database contents persist much longer than the application code version that originally wrote them.
- **Location Transparency:** The flawed abstraction that a remote network request (RPC) acts and behaves exactly like a local function call.
- **Service Mesh:** A networking layer (typically using sidecar proxies) that handles load balancing, service discovery, connection encryption (TLS), and observability between microservices.
- **Durable Execution:** Workflows that log RPC calls and state changes to a write-ahead log, allowing them to resume exactly where they left off after a crash, providing exactly-once semantics.
- **Idempotence:** The property of an operation that allows it to be retried multiple times without changing the result beyond the initial application.

@Objectives
- Architect data structures, schemas, and APIs that support zero-downtime rolling upgrades by strictly maintaining both forward and backward compatibility.
- Select the optimal encoding format (textual, binary, schema-driven, or columnar) based on the specific mode of dataflow (databases, service calls, asynchronous events, or archival storage).
- Prevent data loss during read-modify-write cycles by ensuring old code explicitly preserves unknown fields authored by newer code.
- Design distributed communication to be resilient against network fallibility, avoiding the pitfalls of location transparency.
- Ensure strict deterministic behavior in durable execution workflows to prevent replay failures.

@Guidelines

- **Language-Specific Encodings:**
  - The AI MUST FORBID the use of language-specific encoding libraries (e.g., Java `java.io.Serializable`, Python `pickle`, Ruby `Marshal`) for any data that is persisted to disk or sent across a network.
  - Rationale: These tie the data to a single language, pose severe security risks (arbitrary code execution via class instantiation), and lack forward/backward compatibility mechanisms.

- **JSON, XML, and CSV Formats:**
  - When designing JSON data models containing large integers (e.g., database IDs, Twitter/X post IDs), the AI MUST encode integers greater than 2^53 as strings or provide a string fallback to prevent precision loss in languages using IEEE 754 double-precision floats (like JavaScript).
  - The AI MUST encode binary strings inside JSON/XML strictly using Base64, and the schema MUST explicitly document this requirement.
  - When using JSON Schema, the AI MUST explicitly define whether the content model is open (`additionalProperties: true`) or closed (`additionalProperties: false`) and handle the complexity of open validation appropriately.

- **Binary Schema-Driven Formats (Protocol Buffers, Thrift):**
  - The AI MUST utilize field tags (numbers) to identify fields, not field names.
  - **Evolution Rules:**
    - The AI MUST NEVER change the tag number of an existing field.
    - The AI MUST NEVER reuse a tag number from a deleted field. Deleted field tags MUST be explicitly reserved.
    - The AI MUST NOT change the datatype of a field if it risks truncation (e.g., changing a 64-bit integer to a 32-bit integer).
    - When an application reads data, modifies it, and writes it back, the AI MUST ensure the decoder preserves unknown fields (fields with unrecognized tags) and includes them in the subsequent write to prevent data loss.

- **Avro Formats:**
  - The AI MUST define schemas without tag numbers.
  - To support schema evolution, the AI MUST only add or remove fields that have explicitly defined default values.
  - To make a field nullable in Avro, the AI MUST use a union type with `null` as the first branch (e.g., `union { null, string } field = null;`).
  - When dumping relational databases to files, the AI SHOULD recommend Avro, as its lack of tag numbers allows for simple, dynamic schema generation mapped directly from column names.
  - The AI MUST track the Writer's Schema (via Object Container File headers, Schema Registry version numbers, or connection negotiation) so the Reader's Schema can resolve differences.

- **Dataflow Through Databases:**
  - The AI MUST treat database records as having mixed schema versions ("Data Outlives Code").
  - The AI MUST perform database migrations in a way that avoids locking and rewriting the entire table (e.g., add new columns with a `null` default value).

- **Dataflow Through Services (REST & RPC):**
  - The AI MUST assume servers are updated before clients. Therefore, servers require backward compatibility on requests (read old) and forward compatibility on responses (write old).
  - The AI MUST reject the illusion of "Location Transparency." Code making network calls MUST explicitly handle unpredictable latency, timeouts, and network failures.
  - The AI MUST implement retry mechanisms with exponential backoff and circuit breakers, and MUST guarantee that the target endpoint is idempotent to prevent duplicate executions on retries.
  - The AI MUST explicitly version APIs (e.g., via URL paths or HTTP Accept headers) when breaking changes are unavoidable.

- **Durable Execution and Workflows (Temporal, Restate):**
  - The AI MUST enforce strict determinism in workflow definitions. Workflow code MUST NOT use standard system clocks, standard random number generators, or thread-blocking calls. It MUST use the deterministic equivalents provided by the workflow framework.
  - The AI MUST NOT reorder, add, or remove RPC/activity calls in an existing workflow definition, as this breaks the write-ahead log replay mechanism for active executions.

- **Event-Driven Architectures (Message Brokers/Actors):**
  - The AI MUST ensure messages are self-contained and encoded using a schema-driven format, ideally integrated with a Schema Registry.
  - If a consumer reads a message and republishes it to another topic, the consumer MUST preserve any unknown fields present in the original message.

@Workflow
1. **Determine the Dataflow Context:** Identify whether the data is at rest in a database, in motion over REST/RPC, managed by a workflow engine, or streaming via an event broker.
2. **Select the Encoding Format:** 
   - Public-facing web APIs: Use JSON (with OpenAPI schemas).
   - Internal microservices/Events: Use Protocol Buffers, gRPC, or Avro.
   - Archival/Analytics: Use Avro Object Container Files or columnar formats like Parquet.
3. **Design for Evolution:** 
   - For Protobuf: Assign tag numbers. Reserve deleted tags. 
   - For Avro: Assign explicit default values for new fields. Ensure nullability is modeled via unions.
4. **Implement Resilient Network Logic:** For service-to-service communication, wrap calls in timeout, retry, and idempotency logic. Do not treat remote calls as local function calls.
5. **Secure the Read-Modify-Write Cycle:** If the system is updating a record, inject code to retain unknown fields/tags parsed from the input, ensuring newer data attributes are not silently dropped.
6. **Verify Workflow Determinism:** If writing durable execution workflows, run static analysis or manual checks to remove all non-deterministic system calls.

@Examples (Do's and Don'ts)

- **Protobuf Schema Evolution**
  - [DO]: Mark deleted fields as reserved to prevent tag reuse.
    ```proto
    message User {
      reserved 2; // Old favorite_number field
      string user_name = 1;
      repeated string interests = 3;
    }
    ```
  - [DON'T]: Reuse an old tag number for a new field, which corrupts data when old code reads new messages.
    ```proto
    message User {
      string user_name = 1;
      string new_email_field = 2; // DANGEROUS: Reused tag 2
    }
    ```

- **JSON Large Integer Handling**
  - [DO]: Return large database IDs as strings in JSON to protect JavaScript clients.
    ```json
    {
      "post_id": "1234567890123456789",
      "author": "Alice"
    }
    ```
  - [DON'T]: Return raw 64-bit integers in JSON.
    ```json
    {
      "post_id": 1234567890123456789, // DANGEROUS: Will be truncated to 1234567890123456768 in JS
      "author": "Alice"
    }
    ```

- **Avro Nullable Fields**
  - [DO]: Use a union with null as the first element to define a default null value.
    ```json
    {
      "name": "favoriteNumber",
      "type": ["null", "long"],
      "default": null
    }
    ```
  - [DON'T]: Use a single type and attempt to assign null, which breaks Avro parsing.
    ```json
    {
      "name": "favoriteNumber",
      "type": "long",
      "default": null // DANGEROUS: Invalid Avro schema
    }
    ```

- **Durable Workflow Determinism**
  - [DO]: Use the framework's deterministic time function.
    ```python
    # Temporal workflow example
    current_time = workflow.now() 
    ```
  - [DON'T]: Use system time in a durable workflow, which causes replay failures.
    ```python
    # Temporal workflow example
    current_time = datetime.now() # DANGEROUS: Non-deterministic
    ```

- **Language-Specific Serialization**
  - [DO]: Use standard interchange formats (JSON, Protobuf, Avro) for storing data in a database.
  - [DON'T]: Store language-specific serialized objects.
    ```python
    import pickle
    db.save("user:1", pickle.dumps(user_object)) # DANGEROUS: Security risk and not evolvable
    ```