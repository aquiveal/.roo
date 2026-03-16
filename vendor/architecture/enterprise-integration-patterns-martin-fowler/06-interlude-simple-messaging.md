@Domain
This rule file is triggered when the AI is tasked with designing, implementing, or debugging asynchronous messaging endpoints, specifically focusing on Request-Reply interactions, Publish-Subscribe event notifications, Observer pattern implementations over messaging infrastructure, and integrating applications using JMS (Java) or MSMQ (.NET/C#).

@Vocabulary
- **Requestor**: A Message Endpoint that sends a request message and waits to receive a reply message as a response.
- **Replier**: A Message Endpoint that waits to receive a request message and responds by sending a reply message.
- **Messaging Gateway**: A class that encapsulates messaging-specific code and separates it from the rest of the application code, exposing only domain-specific methods.
- **Return Address**: A header property specifying the channel to which the replier should send the reply message (e.g., `JMSReplyTo` in JMS, `ResponseQueue` in .NET).
- **Correlation Identifier**: A unique ID indicating which request a reply is answering. Typically, the replier copies the request's Message ID into the reply's Correlation ID field.
- **Invalid Message Channel**: A dedicated queue where messages that cannot be processed (due to wrong type, missing headers, or parsing errors) are routed to prevent them from blocking the system.
- **Polling Consumer**: A synchronous receiver that explicitly pulls messages from a channel (blocks until a message arrives).
- **Event-Driven Consumer**: An asynchronous receiver invoked automatically by the messaging system when a message arrives via callbacks or delegates.
- **Push Model (Observer)**: A Publish-Subscribe implementation where the subject sends the new state directly within the event notification message.
- **Pull Model (Observer)**: A Publish-Subscribe implementation where the subject sends a generic event notification, and the observer must use a subsequent Request-Reply exchange to retrieve the state.
- **Durable Subscriber**: A subscriber that does not miss messages published while it is temporarily disconnected.

@Objectives
- Ensure robust, decoupled communication between applications using Request-Reply and Publish-Subscribe patterns.
- Hide messaging infrastructure complexities from business logic using Messaging Gateways.
- Maintain message traceability across asynchronous boundaries using Correlation Identifiers and Return Addresses.
- Prevent queue blockages and message loss by implementing proper Invalid Message handling.
- Balance performance and complexity when implementing the Observer pattern across distributed components.

@Guidelines

**1. Request-Reply Implementation**
- The AI MUST use two separate channels for Request-Reply communication: one for the request and one for the reply.
- The AI MUST NOT hardcode the reply channel in the Replier. Instead, the Requestor MUST set the Return Address property on the request message, and the Replier MUST dynamically read this property to route the reply.
- The AI MUST link replies to requests by extracting the Message ID of the incoming request and setting it as the Correlation Identifier of the outgoing reply.

**2. Invalid Message Handling**
- If a Replier receives a message it cannot interpret (wrong data type, missing required headers, deserialization failure), the AI MUST route the message to a designated Invalid Message Channel.
- **CRITICAL**: When resending a bad message to an Invalid Message Channel, the messaging system assigns a new Message ID. Therefore, the AI MUST explicitly copy the original Message ID into the Correlation Identifier field before routing to preserve a record of the original message ID.

**3. Messaging Gateways**
- The AI MUST NOT leak messaging APIs (like `javax.jms.*` or `System.Messaging.*`) into the business logic.
- The AI MUST encapsulate all channel configurations, message formatting, and send/receive logic inside a Messaging Gateway class that exposes only strongly-typed, domain-specific methods (e.g., `notify(String state)`).

**4. Endpoint Consumption Models**
- The AI MUST use a **Polling Consumer** (synchronous `receive()`) when the receiving application needs to control the rate of message consumption to avoid being overwhelmed.
- The AI MUST use an **Event-Driven Consumer** (`MessageListener` in Java, `ReceiveCompletedEventHandler` in .NET) when the application needs to react immediately to incoming messages.
- In .NET Event-Driven Consumers, the AI MUST ensure that `BeginReceive()` is called at the end of the event handler to resume listening for subsequent messages.

**5. Publish-Subscribe and Observer Pattern**
- The AI MUST implement the Push Model by default for distributed Observer implementations, as it requires fewer channels, fewer messages, and less thread management.
- If the Pull Model is required, the AI MUST implement a three-step process: 1) Subject broadcasts empty Event Message. 2) Observer uses a `QueueRequestor` (Request-Reply) to ask for state. 3) Subject replies with the state.
- To prevent an explosion of channels in complex publish-subscribe scenarios, the AI MUST group related notifications of the same schema onto a single Datatype Channel. Observers that require fine-grained filtering MUST use Selective Consumers (e.g., JMS Message Selectors) rather than requiring the creation of separate channels for every notification variant.

@Workflow
**Implementing a Request-Reply Interaction:**
1. **Define Channels**: Establish a Request Queue, a Reply Queue, and an Invalid Message Queue.
2. **Build Requestor Gateway**:
   - Instantiate consumer/producer objects.
   - Expose a domain method (e.g., `send()`).
   - Create the message, attach the Reply Queue to the Return Address header, and send.
   - Implement a Polling Consumer to synchronously block and wait for the reply.
3. **Build Replier Gateway**:
   - Implement an Event-Driven Consumer listening on the Request Queue.
   - In the callback, validate the message type and the presence of the Return Address.
   - If invalid, copy the Message ID to the Correlation ID and route to the Invalid Message Queue.
   - If valid, extract payload, perform business logic, create reply message.
   - Copy request's Message ID to the reply's Correlation ID.
   - Extract the Return Address and send the reply to that destination.
   - (For .NET) Invoke `BeginReceive()` to continue listening.

@Examples (Do's and Don'ts)

**[DO] Implement Replier handling Return Address, Correlation ID, and Invalid Messages (JMS)**
```java
public void onMessage(Message message) {
    try {
        if ((message instanceof TextMessage) && (message.getJMSReplyTo() != null)) {
            TextMessage requestMessage = (TextMessage) message;
            String contents = requestMessage.getText();
            
            // Extract Return Address
            Destination replyDestination = message.getJMSReplyTo();
            MessageProducer replyProducer = session.createProducer(replyDestination);
            
            // Create Reply and set Correlation ID
            TextMessage replyMessage = session.createTextMessage();
            replyMessage.setText(contents); // Echo logic
            replyMessage.setJMSCorrelationID(requestMessage.getJMSMessageID());
            
            replyProducer.send(replyMessage);
        } else {
            // Invalid Message Handling: preserve ID and route to invalid queue
            message.setJMSCorrelationID(message.getJMSMessageID());
            invalidProducer.send(message);
        }
    } catch (JMSException e) {
        e.printStackTrace();
    }
}
```

**[DON'T] Hardcode the reply queue in the replier**
```java
// Anti-pattern: Ignoring Return Address
Destination replyDestination = JndiUtil.getDestination("jms/HardCodedReplyQueue");
MessageProducer replyProducer = session.createProducer(replyDestination);
replyProducer.send(replyMessage);
```

**[DO] Implement Event-Driven Consumer correctly in .NET/MSMQ**
```csharp
public void Process() {
    inputQueue.ReceiveCompleted += new ReceiveCompletedEventHandler(OnReceiveCompleted);
    inputQueue.BeginReceive(); // Start asynchronous listening
}

private void OnReceiveCompleted(Object source, ReceiveCompletedEventArgs asyncResult) {
    MessageQueue mq = (MessageQueue)source;
    Message message = mq.EndReceive(asyncResult.AsyncResult);
    
    try {
        // Business logic / Extract Return Address & Correlation ID
        MessageQueue replyQueue = message.ResponseQueue;
        Message replyMessage = new Message();
        replyMessage.Body = message.Body;
        replyMessage.CorrelationId = message.Id;
        replyQueue.Send(replyMessage);
    } catch (Exception) {
        // Invalid Message Handling
        message.CorrelationId = message.Id;
        invalidQueue.Send(message);
    }
    
    // CRITICAL: Call BeginReceive again to keep listening
    mq.BeginReceive(); 
}
```

**[DON'T] Forget to call BeginReceive() after processing an MSMQ message**
```csharp
private void OnReceiveCompleted(Object source, ReceiveCompletedEventArgs asyncResult) {
    MessageQueue mq = (MessageQueue)source;
    Message message = mq.EndReceive(asyncResult.AsyncResult);
    ProcessMessage(message);
    // Anti-pattern: Missing mq.BeginReceive(); The consumer will stop listening after one message!
}
```

**[DO] Use Messaging Gateways to encapsulate Pub-Sub Push Model**
```java
public class SubjectGateway {
    private MessageProducer updateProducer;
    private Session session;

    // Encapsulate JMS details away from the Subject business logic
    public void notify(String state) throws JMSException {
        TextMessage message = session.createTextMessage(state);
        updateProducer.send(message);
    }
}
```

**[DON'T] Use the Pull Model for Pub-Sub without considering overhead**
```java
// Anti-pattern: Overusing the Pull model when state could just be pushed.
// Requires 3 trips: Event Notification -> Request State -> Reply State.
// Avoid this unless observers specifically require subsets of heavy state payloads.
```