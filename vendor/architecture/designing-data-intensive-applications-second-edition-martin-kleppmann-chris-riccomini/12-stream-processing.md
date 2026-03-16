**@Domain**
Activation condition: Any task, file, or user request involving Stream Processing, Event Sourcing, Command Query Responsibility Segregation (CQRS), or Event-Driven Architectures (Message Brokers/Actor Frameworks). *(Note: Because Chapter 12 "Stream Processing" is explicitly marked unavailable in the source text, these rules are exhaustively synthesized from the corresponding stream processing and event-driven architecture methodologies detailed in Chapters 1, 3, and 5 of the provided text).*

**@Vocabulary**
- **Stream Processing**: The practice of handling events and data changes as soon as they occur, allowing systems to respond to events on the order of seconds (e.g., for fraud detection).
- **System of Record (Source of Truth)**: The authoritative data system where new data/user input is first written. Each fact is represented exactly once.
- **Derived Data System**: A system containing data that is the result of taking existing data from another system and transforming it. It can be recreated from the original source if lost.
- **Event Sourcing**: A data modeling pattern where the source of truth is an append-only log of immutable events. Every state change is recorded as a separate event.
- **Command**: An incoming user request that must be validated before it is accepted.
- **Fact / Event**: A validated command that has occurred in the past and has been appended to the event log. 
- **Materialized View (Projection / Read Model)**: A read-optimized representation of data that is deterministically derived from the event log.
- **CQRS (Command Query Responsibility Segregation)**: The architectural principle of maintaining separate data representations optimized for writing (event logs) and reading (materialized views), deriving the latter from the former.
- **Message Broker (Event Broker / Message Queue)**: An intermediary system that stores asynchronous messages temporarily to decouple senders from recipients and buffer load.
- **Queue**: A message distribution pattern where a message is added by one process and delivered to exactly one of multiple competing consumers.
- **Topic**: A message distribution pattern where a message is published and delivered to all subscribed consumers.
- **Distributed Actor Framework**: A concurrency model scaled across multiple nodes where state is encapsulated in actors that communicate exclusively via asynchronous messages.

**@Objectives**
- Separate write-optimized storage from read-optimized storage to maximize performance for both transaction processing and analytic queries.
- Ensure that derived data systems (materialized views) can be reliably, deterministically, and identically rebuilt from the immutable event log at any time.
- Leverage asynchronous message brokers to decouple services, buffer unexpected load spikes, and prevent cascading failures caused by synchronous RPC network issues.

**@Guidelines**
- The AI MUST treat the primary event log as an append-only, immutable System of Record. Existing events MUST NEVER be modified or deleted in place to change state.
- The AI MUST name events in the past tense (e.g., `seats_were_booked`, `booking_cancelled`) to reflect that the event is a historical fact rather than an imperative action.
- The AI MUST perform all business validation during the Command phase. Once a Command is accepted and written as an Event, downstream consumers MUST NOT reject it.
- The AI MUST ensure event processing logic is strictly deterministic. If an event requires volatile external information (e.g., a currency exchange rate), the AI MUST embed that information directly into the event payload at write time, or use a timestamped historical query that guarantees the same result during future replays.
- The AI MUST decouple services using asynchronous message brokers rather than direct synchronous RPC calls when the sender does not strictly require an immediate response from the recipient.
- The AI MUST design Materialized Views such that they can be safely dropped and entirely recomputed from the event log using the exact same processing code.
- The AI MUST preserve unknown fields when consuming and republishing messages in an event stream. Dropping unknown fields destroys forward compatibility when older code interacts with data written by newer code.
- The AI MUST strictly isolate personal user data from the immutable event log (e.g., storing it in a separate system or using cryptographic erasure) to comply with data privacy regulations like the GDPR, which mandate the right to deletion.
- The AI MUST carefully isolate or disable external side effects (e.g., sending confirmation emails) when rebuilding or reprocessing materialized views from the event log.

**@Workflow**
1. Receive an incoming user action or system request (Command).
2. Validate the Command against business logic, current database constraints, and permissions.
3. If valid, transform the Command into an immutable Fact (Event), naming it in the past tense. 
4. Embed any dynamic or external state (e.g., current prices, exchange rates) directly into the Event to guarantee future determinism.
5. Append the Event to the write-optimized event log (System of Record).
6. Publish the Event asynchronously to a Message Broker (using a Queue for load-balanced processing or a Topic for fan-out).
7. Consume the Event stream asynchronously to derive, update, or aggregate data into read-optimized Materialized Views (CQRS).
8. Expose the updated Materialized Views to client queries and business analysts.

**@Examples (Do's and Don'ts)**

**1. Event Naming and Determinism**
- **[DO]**: Use past-tense naming and embed volatile external context directly into the event payload so that it can be deterministically replayed 5 years later.
  ```json
  {
    "event_type": "subscription_purchased",
    "timestamp": 1693143014,
    "payload": {
      "user_id": 9942,
      "base_price": 50.00,
      "currency": "EUR",
      "exchange_rate_to_usd_at_purchase": 1.08 
    }
  }
  ```
- **[DON'T]**: Use imperative naming and rely on downstream stream processors to fetch external data, which will yield different results if the view is rebuilt later.
  ```json
  {
    "event_type": "purchase_subscription",
    "timestamp": 1693143014,
    "payload": {
      "user_id": 9942,
      "base_price": 50.00,
      "currency": "EUR"
      // Anti-pattern: Consumer must look up the exchange rate, breaking determinism
    }
  }
  ```

**2. Forward Compatibility (Preserving Unknown Fields)**
- **[DO]**: Copy all properties from the incoming event—including those not explicitly recognized by the current schema version—before modifying and republishing to a message broker.
  ```python
  def process_event(incoming_event):
      # Safely clone the entire event to preserve fields added by newer code versions
      outgoing_event = incoming_event.copy() 
      
      # Perform the necessary transformations
      outgoing_event['processed_timestamp'] = current_time()
      
      publish_to_topic("processed_events", outgoing_event)
  ```
- **[DON'T]**: Map only explicitly known fields into a rigid object, silently dropping fields added by newer versions of the application (destroying forward compatibility).
  ```python
  def process_event(incoming_event):
      # Anti-pattern: Unrecognized fields in incoming_event are lost here
      outgoing_event = {
          'event_type': incoming_event['event_type'],
          'user_id': incoming_event['user_id'],
          'processed_timestamp': current_time()
      }
      
      publish_to_topic("processed_events", outgoing_event)
  ```

**3. Separation of Concerns (CQRS)**
- **[DO]**: Append the event to a log, then use a background stream processor to update a denormalized cache (materialized view) optimized for fast reads.
- **[DON'T]**: Attempt to execute complex multi-table joins on a highly normalized OLTP database during a low-latency synchronous user read request.