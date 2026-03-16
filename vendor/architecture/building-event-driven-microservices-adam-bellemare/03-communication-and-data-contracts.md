# @Domain
These rules MUST trigger when the AI is tasked with designing, implementing, evaluating, or modifying event structures, data contracts, schemas, event streams, payload serializations, or cross-service communication layers within an event-driven architecture. 

# @Vocabulary
- **Data Contract**: The combination of the data definition (what will be produced) and the triggering logic (why it is produced) agreed upon by producers and consumers.
- **Explicit Schema**: A formally defined, strongly typed contract (e.g., Avro, Protobuf, Thrift) that explicitly dictates the event structure and evolutionary rules.
- **Implicit Schema**: An anti-pattern where data structures (like plain JSON or key/value pairs) lack a formal contract, forcing consumers to infer types, structure, and meaning.
- **Schema Evolution**: The controlled mechanism of changing an explicit schema over time without breaking downstream consumers.
- **Forward Compatibility**: Data produced with a newer schema can be read as though it were produced with an older schema.
- **Backward Compatibility**: Data produced with an older schema can be read as though it were produced with a newer schema.
- **Full Compatibility**: The union of both forward and backward compatibility; the strongest evolutionary guarantee.
- **Breaking Schema Change**: A change to a schema that violates compatibility rules, requiring renegotiation of the data contract and typically the creation of a new event stream.
- **Semaphore/Signal Event**: An anti-pattern where an event merely indicates an action occurred (e.g., "WorkDone") without containing the actual state or result data, forcing consumers to look up the result elsewhere.
- **Tombstone**: A keyed event with a null value used to represent the deletion of an entity.

# @Objectives
- Establish unbreakable, strictly defined explicit schemas for all inter-service communication to completely isolate producers and consumers.
- Guarantee schema evolution compatibility to decouple microservice deployment lifecycles.
- Design events as the "single source of truth," ensuring they contain the whole truth of an occurrence and require no secondary data lookups.
- Enforce the Single Responsibility Principle for event streams (one event definition per stream).
- Eliminate all implicit, loosely typed, or generic event definitions (e.g., untyped JSON).

# @Guidelines

## Schema Definition & Formatting Constraints
- The AI MUST define all events using an Explicit Schema framework that supports code generation and evolutionary rules (e.g., Apache Avro, Google Protobuf).
- The AI MUST NOT use plain JSON, plain text, or loosely structured key/value maps for event data contracts, as these lack full-compatibility evolution rules.
- The AI MUST include a block header comment at the top of every schema file explicitly detailing the *triggering logic* (exactly *why* and *when* the event is produced).
- The AI MUST add inline comments for specific fields to provide context (e.g., specifying if a datetime is UTC, ISO, or Unix epoch).

## Data Types & Field Constraints
- The AI MUST use the absolutely narrowest data types available.
- The AI MUST NOT use a `String` to store a numeric value (e.g., GPS coordinates) or a boolean value.
- The AI MUST NOT use an `Integer` to represent a boolean.
- The AI MUST NOT use a `String` as a pseudo-enum. The AI MUST use native Enum types to enforce boundaries.
- The AI MUST instruct consumers to handle unknown enum tokens (using framework features like Avro/Protobuf default or unknown token handlers) instead of throwing fatal exceptions.

## Event & Stream Design Architecture
- **Singular Event Definition:** The AI MUST map one, and only one, logical event definition/schema to a specific event stream. The AI MUST NOT mix completely different event schemas in a single stream.
- **Single-Purpose Events:** The AI MUST ensure events serve a single business purpose. 
- **No Overloading:** The AI MUST NOT use overloaded generic events with a `type` parameter (e.g., `TypeEnum: Book, Movie`) that requires a sprawling schema of nullable, type-specific fields. Overloaded schemas MUST be decomposed into distinct, single-purpose schemas and mapped to separate streams.
- **Single Source of Truth:** The AI MUST ensure the event contains the complete description of what happened. Consumers MUST NOT need to query the producer's database to fulfill the event context.
- **Payload Sizing:** The AI MUST keep events small. If an event generates a massive artifact (e.g., a large image or PDF), the AI MUST use a URI pointer to the external storage within the event, acknowledging the payload mutability risk.

## Schema Evolution & Breaking Changes
- The AI MUST prefer **Full Compatibility** for all schema updates.
- If a Breaking Schema Change is unavoidable for **Entity Events**: The AI MUST prompt the user to choose between migrating all old entities to a new schema/stream OR creating a new stream for new schemas while maintaining the old one. The AI MUST NOT offload divergent entity schema resolution to the downstream consumer.
- If a Breaking Schema Change is unavoidable for **Non-Entity Events**: The AI MUST create a new event stream for the new schema and notify the user to deprecate the old stream.

## Anti-Patterns to Avoid
- **Implicit Parsing Libraries:** The AI MUST NOT create centralized common libraries that parse generic events for all services. Each consumer MUST use schema-generated code classes.
- **Semaphore Anti-Pattern:** The AI MUST NOT create events that act only as signals (e.g., `{"jobId": 123, "status": "done"}`) if the consumer needs the resulting data. The event MUST contain the resulting data.
- **Deferred Resolution:** The AI MUST NOT defer the handling of divergent, broken schemas to the consumer. Producers MUST resolve data definitions before writing to the broker.

# @Workflow
When tasked with designing a new event or modifying an existing event contract, the AI MUST strictly follow this algorithmic process:

1. **Elicit Triggering Logic:** Identify and document exactly *why* this event is happening. Define this explicitly in a block comment.
2. **Determine Schema Format:** Ensure the project uses Avro, Protobuf, or a comparable explicit format. If asked to use JSON for cross-service events, warn the user against it citing lack of safe evolutionary frameworks.
3. **Decompose Responsibilities:** Check if the event tries to do too many things. If the event uses a generic `type` flag with conditional fields, break it down into multiple distinct schemas.
4. **Select Narrowest Types:** Review every field. Convert Strings holding numbers to Integers/Longs/Doubles. Convert Strings holding bounded sets to Enums. Add specific inline comments to dates and complex types.
5. **Validate Source of Truth:** Review the payload. Does it tell the whole truth? Ensure the event is not a Semaphore/Signal and contains the actual state changes.
6. **Perform Compatibility Check (If modifying):** Compare the new schema against the old schema. Ensure Forward and Backward compatibility. If a change breaks compatibility, immediately halt and output a Breaking Change Strategy (new stream vs migration).
7. **Generate Output:** Output the explicit schema definition, complete with headers and comments. 

# @Examples (Do's and Don'ts)

## Explicit Schemas vs Implicit Data
**[DO] Use an explicit, typed schema (e.g., Avro) with documentation.**
```avro
{
  "namespace": "com.retail.orders",
  "type": "record",
  "name": "OrderShipped",
  "doc": "Triggered when the fulfillment center physically hands over the package to the courier.",
  "fields": [
    {"name": "orderId", "type": "long"},
    {"name": "shippedAt", "type": "long", "doc": "Unix epoch timestamp in milliseconds"},
    {"name": "courier", "type": {"type": "enum", "name": "CourierType", "symbols": ["FEDEX", "UPS", "USPS"]}}
  ]
}
```

**[DON'T] Use generic JSON with implicit types and missing context.**
```json
{
  "orderId": "12345",
  "shippedAt": "2023-10-01 12:00:00",
  "courier": "FEDEX"
}
```

## Single-Purpose Events vs Overloaded Events
**[DO] Decompose distinct actions into dedicated, strict schemas.**
```protobuf
// Stream: movie-clicks
message MovieClick {
  int64 movie_id = 1;
  bool watched_preview = 2; 
}

// Stream: book-clicks
message BookClick {
  int64 book_id = 1;
}
```

**[DON'T] Overload a single event with type parameters and nullable conditional fields.**
```protobuf
// Stream: product-engagements
message ProductEngagement {
  int64 product_id = 1;
  string product_type = 2; // "MOVIE" or "BOOK"
  string action_type = 3; 
  // Only applies to MOVIE
  bool watched_preview = 4;
  // Only applies to BOOK
  int32 bookmark_page = 5;
}
```

## Narrowest Data Types
**[DO] Use strict native types.**
```protobuf
message SensorReading {
  double temperature_celsius = 1;
  bool is_active = 2;
  ReadingStatus status = 3; // Enum: [OK, WARNING, ERROR]
}
```

**[DON'T] Stringify numeric, boolean, or bounded data.**
```protobuf
message SensorReading {
  string temperature = 1; // "23.5"
  int32 is_active = 2;    // 1 or 0, or maybe 2?
  string status = 3;      // "OK", prone to typos like "O.K."
}
```

## Events vs Semaphores
**[DO] Send the resulting truth in the event payload.**
```protobuf
message UserReportGenerated {
  int64 report_id = 1;
  int64 user_id = 2;
  string report_uri = 3; // Pointer to the actual artifact
  int32 total_transactions_calculated = 4;
}
```

**[DON'T] Send a semaphore requiring the consumer to fetch the data.**
```protobuf
message UserReportGenerated {
  int64 report_id = 1;
  string status = "DONE";
  // The consumer now has to synchronously call the Report API to find out what happened.
}
```