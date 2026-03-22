# @Domain
These rules MUST trigger when the user requests architectural design, system integration, messaging infrastructure configuration, or code generation related to asynchronous message routing, enterprise application integration (EAI), message brokers, message flow logic, message splitting/aggregation, or event-driven distributed systems based on Enterprise Integration Patterns.

# @Vocabulary
- **Message Router**: A component that consumes a message from one channel and republishes it to a different channel depending on a set of conditions, without modifying the message content.
- **Predictive Routing**: A central routing strategy (like Content-Based Router) where the router incorporates knowledge of all possible destinations and their capabilities.
- **Reactive Filtering**: A distributed routing strategy where a message is broadcast to all components, and each recipient uses a Message Filter to evaluate relevance.
- **Content-Based Router**: A Message Router that examines the message content and routes it to exactly one channel based on data contained in the message.
- **Message Filter**: A special Message Router with a single output channel that eliminates undesired messages based on criteria.
- **Dynamic Router**: A router that self-configures its routing rules based on control messages received from participating destinations on a separate control channel.
- **Recipient List**: A router that inspects a message, computes a list of recipients, and forwards a copy of the message to each recipient's specific channel.
- **Splitter**: A component that breaks a composite message into a series of individual messages, each containing data related to one item.
- **Aggregator**: A stateful filter that collects and stores individual messages until a complete set of related messages is received, then publishes a single distilled message.
- **Completeness Condition**: The algorithm within an Aggregator that determines when a set of correlated messages is ready to be published (e.g., Wait for All, Timeout, First Best).
- **Resequencer**: A stateful filter that collects out-of-sequence messages and publishes them to the output channel in a specified sequential order.
- **Active Acknowledgment**: A mechanism used by a Resequencer to throttle message producers based on available buffer window size, preventing buffer overruns.
- **Composed Message Processor**: A composite pattern consisting of a Splitter, a Message Router, and an Aggregator to process a message with multiple elements in parallel.
- **Scatter-Gather**: A composite pattern that broadcasts a request to multiple recipients (via Publish-Subscribe or Recipient List) and re-aggregates the responses.
- **Routing Slip**: A routing table attached directly to a message specifying a sequential series of processing steps the message must undergo.
- **Process Manager**: A central processing unit (hub-and-spoke) that maintains the state of a sequence and determines the next processing step based on intermediate results.
- **Message Broker**: An architectural pattern representing a central hub that receives messages from multiple destinations, determines the correct destination, and routes them to avoid integration spaghetti.

# @Objectives
- **Decouple Originators and Destinations**: The AI MUST design systems where message senders remain completely unaware of the ultimate message consumers' locations or identities.
- **Prevent Integration Spaghetti**: The AI MUST avoid point-to-point explosion in multi-system architectures by centralizing routing logic (e.g., using Message Brokers or Process Managers).
- **Ensure Message Sequence and Integrity**: The AI MUST proactively identify and mitigate temporal/sequence risks in asynchronous flows using Aggregators and Resequencers.
- **Optimize Network Traffic vs. Coupling**: The AI MUST evaluate and balance the trade-offs between predictive routing (efficient but tightly coupled) and reactive filtering (loosely coupled but network-intensive).
- **Maintain State Safely**: The AI MUST properly manage stateful routing (Aggregators, Resequencers, Process Managers) while preventing memory leaks (via timeouts) and buffer overruns (via throttling).

# @Guidelines

## General Routing Rules
- The AI MUST NOT modify the payload (body) of a message within a Message Router. Routers strictly determine the destination; transformations must be delegated to a Message Translator.
- The AI MUST select the correct routing pattern based on cardinality and statefulness:
  - 1 input, 1 output, stateless -> Content-Based Router
  - 1 input, 0 or 1 output, stateless -> Message Filter
  - 1 input, multiple outputs, stateless -> Recipient List or Splitter
  - Multiple inputs, 1 output, stateful -> Aggregator
  - Multiple inputs, multiple outputs, stateful -> Resequencer

## Content-Based Routing & Filtering
- When designing a Content-Based Router, the AI MUST route each message to exactly ONE destination.
- When implementing predictive routing (Content-Based Router), the AI MUST explicitly warn the user about the maintenance dependency of keeping destination logic centralized.
- When implementing reactive filtering (Publish-Subscribe + Message Filters), the AI MUST ensure that dropping uninteresting messages is silent and does not throw system errors.

## Dynamic Routing
- The AI MUST use a Dynamic Router for service discovery architectures or when destinations change frequently at runtime.
- When designing a Dynamic Router, the AI MUST explicitly define the conflict resolution strategy for control messages: 1) Ignore conflicts, 2) Send to first matching, or 3) Send to all matching (turning it into a Recipient List).

## Multiplexing & Recipient Lists
- When implementing a Recipient List, the AI MUST ensure that the process of receiving the source message and dispatching all outbound copies is strictly atomic (via transactions, persistent lists, or idempotent receivers).
- The AI MUST NOT allow recipients to bypass the Recipient List by subscribing directly to the input channel.

## Splitting and Sequencing
- When implementing a Splitter, the AI MUST propagate necessary context (e.g., Correlation ID, Order ID, original message timestamp) to all child messages to allow for stateless processing and future aggregation.
- The AI MUST NOT use a system-generated Message ID as a Sequence Number in a Resequencer. Sequence numbers must be a distinct, consecutive numeric field assigned by the sender or Splitter.
- When designing a Resequencer, the AI MUST implement buffer management to prevent out-of-memory errors due to missing messages (e.g., via Active Acknowledgment throttling or Timeout/Dummy injection).

## Aggregation
- When designing an Aggregator, the AI MUST explicitly define three properties: Correlation (which messages belong together), Completeness Condition (when to publish), and Aggregation Algorithm (how to combine them).
- The AI MUST include a mechanism to purge closed or timed-out aggregates from memory to prevent memory leaks and handle late-arriving messages gracefully.

## Composed Routing (Scatter-Gather, Routing Slip, Process Manager)
- Use a **Composed Message Processor** when the sub-messages are distinct and need specific targeted routing (e.g., order items to different inventory systems).
- Use **Scatter-Gather** when sending the exact same message to multiple components to select the best response (e.g., auction or bidding scenarios).
- Use a **Routing Slip** ONLY for sequential, pipeline-style processing where the sequence is known entirely upfront and does not change based on intermediate results.
- Use a **Process Manager** when the routing sequence requires branches, forks, joins, or dynamic decisions based on intermediate results.
- When designing a Process Manager, the AI MUST separate the Process Definition (the template/rules) from the Process Instance (the stateful execution of one trigger message).

# @Workflow
When tasked with designing or implementing a message routing solution, the AI MUST follow this algorithmic process:

1. **Analyze Cardinality**:
   - Determine how many messages enter the component and how many must leave.
   - If 1:1 -> Go to Step 2.
   - If 1:N -> Go to Step 3.
   - If N:1 or N:N -> Go to Step 4.

2. **Evaluate 1:1 Routing Strategy**:
   - Determine if the route is static or based on content.
   - If content-based: Is the set of destinations fixed? (Use Content-Based Router) or highly dynamic? (Use Dynamic Router).
   - If intermediate processing is conditional based on content, implement a Detour or Routing Slip.

3. **Evaluate 1:N Routing Strategy**:
   - Is it the exact same message sent to multiple parties? (Use Recipient List or Publish-Subscribe).
   - Is it a composite message that must be broken into parts? (Use Splitter). Ensure Correlation IDs are attached to all parts.

4. **Evaluate Stateful Consolidation (N:1 / N:N)**:
   - Does the sequence of incoming messages matter? If yes, implement a Resequencer. Define the consecutive sequence number field and the buffer overflow strategy.
   - Do multiple messages need to be merged into one? If yes, implement an Aggregator. Define the Correlation ID, Completeness Condition (e.g., Wait for All, Timeout), and Aggregation Algorithm.

5. **Evaluate Complex Workflows**:
   - If the business process involves parallel dispatches followed by consolidation, implement Scatter-Gather or Composed Message Processor.
   - If the workflow requires stateful decision-making based on intermediate results, design a central Process Manager. Ensure a persistent datastore backs the process instances if high reliability is required.

# @Examples (Do's and Don'ts)

### Content-Based Router
- **[DO]** Use a generic dictionary, map, or external rule base to map message criteria to destination channels.
```csharp
// DO: Data-driven routing
protected void OnMessage(Message message) {
    String key = ((String)message.Body).Substring(0, 1);
    if (routingTable.Contains(key)) {
        MessageQueue destination = (MessageQueue)routingTable[key];
        destination.Send(message);
    } else {
        invalidQueue.Send(message);
    }
}
```
- **[DON'T]** Hardcode endless `if/else` or `switch` statements tightly coupling the router to specific downstream applications unless prototyping.

### Splitter
- **[DO]** Ensure all child messages receive a correlation identifier linking them back to the parent context.
```java
// DO: Attaching parent context to child messages
for (int i=0; i < item.ChildNodes.Count; i++) {
    XmlDocument orderItemDoc = new XmlDocument();
    XmlElement orderItem = orderItemDoc.DocumentElement;
    // Append parent correlation data
    orderItem.AppendChild(orderItemDoc.ImportNode(orderNumber, true));
    orderItem.AppendChild(orderItemDoc.ImportNode(customerId, true));
    // Append actual item data
    orderItem.AppendChild(orderItemDoc.ImportNode(item.ChildNodes[i], true));
    outQueue.Send(orderItem.OuterXml);
}
```
- **[DON'T]** Strip the parent ID when splitting messages; the downstream Aggregator will be unable to reconcile the messages.

### Aggregator
- **[DO]** Maintain active aggregates using a Dictionary/Map keyed by Correlation ID, and explicitly evaluate a completeness condition.
```java
// DO: Managing aggregate state
public void onMessage(Message msg) {
    String correlationID = msg.getStringProperty("AuctionID");
    Aggregate aggregate = (Aggregate)activeAggregates.get(correlationID);
    if (aggregate == null) {
        aggregate = new AuctionAggregate();
        activeAggregates.put(correlationID, aggregate);
    }
    if (!aggregate.isComplete()) {
        aggregate.addMessage(msg);
        if (aggregate.isComplete()) {
            out.send(aggregate.getResultMessage());
            activeAggregates.remove(correlationID); // Prevent memory leaks
        }
    }
}
```
- **[DON'T]** Store unbounded aggregate instances indefinitely without a timeout/purge condition, which will cause memory exhaustion for incomplete groups.

### Resequencer
- **[DO]** Use a specific, sequential `Sequence Number` property inside the payload or message header.
- **[DON'T]** Attempt to use a standard Message ID or GUID to resequence messages, as these values are non-sequential and incomparable.

### Dynamic Recipient List
- **[DO]** Allow recipients to subscribe dynamically using a control queue, maintaining an array of endpoints for a specific criteria.
```csharp
// DO: Maintaining dynamic subscriptions
protected void OnControlMessage(Message message) {
    String text = ((String)message.Body);
    String [] split = (text.Split(new char[] {':'}, 2));
    char[] keys = split[0].ToCharArray();
    MessageQueue queue = FindQueue(split[1]);

    foreach (char c in keys) {
        if (!routingTable.Contains(c)) {
            routingTable.Add(c, new ArrayList());
        }
        ((ArrayList)(routingTable[c])).Add(queue);
    }
}
```
- **[DON'T]** Expect the message sender to formulate and attach the specific physical routing list, which breaks loose coupling.