# @Domain
These rules are activated whenever the AI is tasked with designing, architecting, or implementing asynchronous messaging solutions, integrating distributed applications, configuring Message-Oriented Middleware (MOM), defining Enterprise Service Bus (ESB) message flows, developing JMS/MSMQ/SOAP messaging components, or establishing data exchange protocols between decoupled systems.

# @Vocabulary
*   **Message Intent**: The purpose of the message, categorizing it broadly into Command, Document, or Event.
*   **Command Message**: A message used to reliably invoke a procedure in another application.
*   **Document Message**: A message used to reliably transfer a data structure between applications, leaving the processing decisions to the receiver.
*   **Event Message**: A message used for reliable, asynchronous event notification between applications.
*   **Push Model**: An event notification model where the message's delivery announces the event and the content contains the new state.
*   **Pull Model**: An event notification model where the event message only announces the state change, requiring the observer to request details via a separate Request-Reply.
*   **Request-Reply**: A pair of messages (request and reply) sent over a pair of channels, enabling a two-way conversation between decoupled applications.
*   **Requestor**: The application that sends the request message and waits for the reply message.
*   **Replier**: The application that receives the request message and responds with a reply message.
*   **Synchronous Block**: A Request-Reply approach where a single thread sends the request and blocks (as a Polling Consumer) waiting for the reply.
*   **Asynchronous Callback**: A Request-Reply approach where the sender sets up a callback and a separate thread listens for the reply, allowing multiple outstanding requests to share a single channel.
*   **Return Address**: A header property in the request message that indicates to the replier where to send the reply message.
*   **Correlation Identifier**: A unique token (e.g., Request ID) in the request message that the replier copies into the reply message so the requestor can match the reply to the original request.
*   **Message Sequence**: A technique for transmitting arbitrarily large amounts of data by breaking it into message-size chunks and marking each message with sequence identification fields.
*   **Message Expiration**: A header setting (Time-to-Live or absolute timestamp) that specifies a time limit for how long a message is viable before it should be discarded or sent to a Dead Letter Channel.
*   **Format Indicator**: A value within a message (Version Number, Foreign Key, or Format Document) that specifies the schema or format the message is using to allow for future changes.

# @Objectives
*   Ensure absolute decoupling between sender and receiver applications by embedding all necessary routing, correlation, and formatting metadata directly within the messages.
*   Implement explicit message intents so receivers understand whether they are being commanded to perform an action, receiving data, or being notified of an event.
*   Safely transfer arbitrarily large data sets across constrained messaging infrastructure.
*   Manage time-sensitive data by enforcing strict lifecycle constraints on messages.
*   Establish reliable two-way conversations over inherently one-way asynchronous channels without tightly coupling the participants.
*   Future-proof message definitions to allow disparate systems to evolve their data structures independently over time.

# @Guidelines

*   **Determining Message Intent**
    *   When the application needs to invoke a procedure in a remote application, the AI MUST implement a Command Message.
    *   When transferring a data structure where the receiver determines the processing logic, the AI MUST implement a Document Message.
    *   When notifying remote applications of a state change without dictating their reaction, the AI MUST implement an Event Message.
    *   When deploying Command Messages or Document Messages, the AI MUST generally route them over a Point-to-Point Channel to prevent duplicate processing.
    *   When deploying Event Messages, the AI MUST route them over a Publish-Subscribe Channel to allow multiple observers to react to the state change.

*   **Implementing Event Notification (Push vs. Pull)**
    *   When observers require detailed state data and the data footprint is small, the AI MUST use the Push Model (embed data directly in the Event Message).
    *   When the payload is large or only a subset of observers require the detailed data, the AI MUST use the Pull Model (send a lightweight Event Message, and require interested observers to retrieve state via a subsequent Request-Reply Command Message).

*   **Structuring Request-Reply Conversations**
    *   When an application sends a message and expects a response, the AI MUST define a Request-Reply pattern using a pair of channels (one for the request, one for the reply).
    *   When defining the reply message, the AI MUST ensure it accommodates one of three outcomes: Void (notification of completion), Result Value (a Document Message), or Exception (an error object indicating why the procedure aborted).
    *   When high throughput is required or multiple requests share a reply channel, the AI MUST implement an Asynchronous Callback mechanism rather than a Synchronous Block.

*   **Addressing and Correlation**
    *   When sending a request that requires a reply, the AI MUST place a Return Address inside the request message's header.
    *   When implementing a Replier, the AI MUST NOT hardcode the reply channel; it MUST extract the Return Address from the incoming request and use it to route the reply.
    *   When sending a request, the AI MUST generate a unique Request ID and embed it in the message.
    *   When generating a reply, the AI MUST capture the Request ID from the request message and insert it into the reply message as the Correlation Identifier.
    *   When correlating replies to business workflows, the AI MUST consider using a unique Business Object ID (e.g., Order ID) as the Correlation Identifier rather than the raw infrastructure Message ID.
    *   When requests and replies are chained across multiple components, the AI MUST preserve the original Correlation Identifier in all subsequent replies if the ultimate requestor only cares about the original request.

*   **Handling Large Payloads**
    *   When a data structure exceeds the practical or absolute size limits of a single message, the AI MUST break the data into chunks and transmit it as a Message Sequence.
    *   When implementing a Message Sequence, the AI MUST include three fields in every message header: a Sequence Identifier (to group the messages), a Position Identifier (to order the message), and a Size or End Indicator (to explicitly define the sequence boundaries).
    *   When both applications share a common data store, the AI MUST evaluate using a Claim Check instead of a Message Sequence to reduce messaging overhead.
    *   When a receiver processes a Message Sequence, the AI MUST implement logic to detect missing parts and route the incomplete sequence to an Invalid Message Channel if the sequence cannot be fulfilled.

*   **Enforcing Time Constraints**
    *   When a message's contents or request is time-sensitive, the AI MUST set a Message Expiration in the message header.
    *   When defining Message Expiration, the AI MUST use either an absolute timestamp (adjusting for time zones) or a relative "time-to-live" value that the messaging system converts upon dispatch.
    *   When receiving a message, the AI MUST explicitly check the Message Expiration (if the infrastructure does not do it automatically) and discard the message or route it to a Dead Letter Channel if it is stale.

*   **Future-Proofing Formats**
    *   When designing a shared data format (Canonical Data Model), the AI MUST include a Format Indicator within the message.
    *   When implementing a Format Indicator, the AI MUST use one of three techniques: a Version Number, a Foreign Key (URI pointing to a schema), or a Format Document (embedding the schema/DTD directly in the message).
    *   When parsing a message, the receiver MUST inspect the Format Indicator first to determine the correct unmarshaling logic.

# @Workflow
1.  **Analyze the Data Exhange**: Determine the exact nature of the communication. Is it an action (Command), data transfer (Document), or state change (Event)?
2.  **Define Message Structure**: Construct the message envelope, clearly separating header metadata (infrastructure rules) from the body payload (business data).
3.  **Apply Addressing and Correlation**: If a response is required, inject a `ReplyTo` (Return Address) and a `MessageID` (to be used as the Correlation Identifier) into the request header. Program the Replier to respect and reflect these fields.
4.  **Evaluate Constraints**:
    *   If the payload is massive, chunk it into a Message Sequence with `SequenceID`, `Position`, and `TotalSize` headers.
    *   If the data is time-sensitive, apply a Message Expiration rule (Time-to-Live).
5.  **Finalize Format**: Inject a Format Indicator (e.g., schema version) into the message to ensure current and future receivers can safely parse the content.

# @Examples (Do's and Don'ts)

**Return Address & Correlation Identifier**
*   [DO] Embed the reply channel dynamically in the request header and map the IDs.
```json
// Request Message Header
{
  "MessageID": "REQ-99482",
  "ReplyTo": "jms/queue/ClientX_Replies",
  "Intent": "Command"
}

// Reply Message Header
{
  "MessageID": "REP-11023",
  "CorrelationID": "REQ-99482",
  "Intent": "Document"
}
```
*   [DON'T] Hardcode the reply destination in the receiving application or assume synchronous thread blocking will naturally match the response to the request.

**Message Sequence**
*   [DO] Use explicit sequencing headers when splitting large files across an asynchronous channel.
```json
// Message 2 of 3
{
  "SequenceID": "SEQ-BATCH-991",
  "PositionID": 2,
  "TotalSize": 3,
  "Payload": "...chunk 2..."
}
```
*   [DON'T] Send multiple messages without sequence metadata and rely on the receiver to guess when the transmission is complete.

**Message Expiration**
*   [DO] Explicitly define the Time-to-Live (TTL) or Expiration Date in the header for volatile data (e.g., a stock quote valid only for 5 seconds).
```json
{
  "MessageID": "QUOTE-551",
  "CreationTime": "2023-10-25T10:00:00Z",
  "ExpirationTime": "2023-10-25T10:00:05Z"
}
```
*   [DON'T] Allow time-sensitive messages to sit in a queue indefinitely, which could cause a receiver to act on dangerously stale data.

**Format Indicator**
*   [DO] Specify the exact version or schema of the message payload.
```xml
<!-- Using a Version Number Format Indicator -->
<CustomerUpdate version="2.1">
   <CustomerID>8849</CustomerID>
   <Status>Active</Status>
</CustomerUpdate>
```
*   [DON'T] Send raw XML or JSON payloads without declaring the schema version, breaking the system when the data model inevitably evolves.