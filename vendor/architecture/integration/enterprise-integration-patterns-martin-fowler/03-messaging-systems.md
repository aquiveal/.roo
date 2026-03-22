# @Domain
These rules MUST be triggered when the user requests architectural design, system integration, messaging infrastructure configuration, middleware development, or code generation for distributed applications communicating via asynchronous messaging. This applies to files and tasks involving Message-Oriented Middleware (MOM), Enterprise Service Buses (ESB), JMS, MSMQ, Web Services, or custom integration glue code.

# @Vocabulary
The AI MUST adopt and correctly use the following terminology to ensure exact conceptual alignment with the Enterprise Integration Patterns methodology:
*   **Messaging System / MOM:** The infrastructure that coordinates and manages the sending and receiving of messages in a reliable, store-and-forward fashion.
*   **Message:** An atomic packet of data that can be transmitted on a channel. Consists of a **Header** (meta-information used by the messaging system) and a **Body** (application data ignored by the messaging system).
*   **Message Channel:** A predetermined, predictable, virtual pipe that connects a sender to a receiver.
*   **Pipes and Filters:** An architectural style that divides a larger processing task into a sequence of smaller, independent processing steps (Filters) connected by channels (Pipes).
*   **Message Router:** A specialized filter component that consumes a message from one channel and republishes it to a different channel depending on a set of conditions, without modifying the message content.
*   **Message Translator:** A specialized filter component that converts a message from one data format to another to resolve differences between independent applications.
*   **Message Endpoint:** A dedicated code layer bridging the application and the messaging system, encapsulating the messaging API from the business logic.
*   **Send and Forget:** The asynchronous paradigm where the sender adds the message to the channel and immediately moves on to other work.
*   **Store and Forward:** The reliability paradigm where the messaging system stores the message on the sender's computer, forwards it to the receiver's computer, and stores it there until consumed.

# @Objectives
When applying this chapter's knowledge, the AI MUST achieve the following goals:
*   **Decouple Applications:** Ensure applications share data and invoke behavior without direct dependencies on each other's network location, uptime, or internal data formats.
*   **Ensure Reliable Data Transfer:** Implement mechanisms that delegate the responsibility of data delivery to the messaging system, overcoming network limitations and application downtime.
*   **Maintain Predictability:** Route data strictly through explicitly defined, logical Message Channels rather than allowing random or ad-hoc data retrieval.
*   **Maximize Composability:** Break down complex integration tasks into granular, independent, reusable components connected by standard interfaces.
*   **Isolate Domain Logic:** Keep the core business logic of an application completely unaware of the underlying messaging infrastructure.

# @Guidelines
The AI MUST adhere to the following granular, actionable constraints and architectural rules:

### 1. Message Channel Rules
*   **Explicit Channel Definition:** The AI MUST define specific, dedicated Message Channels for specific types of information. It MUST NOT design systems where applications randomly throw data into a global pool.
*   **Design-Time Configuration:** The AI MUST establish the number and purpose of channels at deployment/design time. Applications MUST be designed around a known set of channels.
*   **Unidirectional Flow:** The AI MUST treat channels as unidirectional pathways. If a two-way conversation is required, the AI MUST implement two separate channels (one for requests, one for replies).

### 2. Message Construction Rules
*   **Strict Header/Body Separation:** The AI MUST place all routing, correlation, and system metadata exclusively in the Message Header. The AI MUST place all business/application data exclusively in the Message Body.
*   **Atomic Packaging:** The AI MUST wrap all shared data into discrete, atomic Messages before transmission.
*   **Intent Definition:** The AI MUST classify and design messages based on intent (Command Message to invoke procedures, Document Message to pass data, Event Message to notify of state changes).

### 3. Pipes and Filters Rules
*   **Independent Steps:** The AI MUST separate integration logic into independent filter components. A filter MUST NOT depend on the existence or identity of adjacent filters.
*   **Standardized Interfaces:** The AI MUST ensure each filter exposes a standard interface: consuming messages from an inbound pipe and publishing results to an outbound pipe.
*   **Concurrency:** The AI MUST design filters to operate in their own thread or process, allowing multiple messages to be processed concurrently in a pipeline fashion.

### 4. Message Routing Rules
*   **Immutability in Routing:** When implementing a Message Router, the AI MUST NOT modify the payload/body of the message. A router's sole responsibility is determining the destination.
*   **Decoupled Origins:** The AI MUST use Message Routers when the original sender cannot or should not know the ultimate destination of the message.

### 5. Message Translation Rules
*   **Format Agnosticism:** The AI MUST NOT force independent, legacy, or packaged applications to natively adopt a unified data format.
*   **Intermediary Translation:** The AI MUST insert Message Translators between applications that expect different data formats to decouple them syntactically and semantically.

### 6. Message Endpoint Rules
*   **API Encapsulation:** The AI MUST NOT embed vendor-specific messaging APIs (e.g., JMS, System.Messaging) directly into business logic.
*   **Custom Bridge Layers:** The AI MUST generate Message Endpoints as a custom bridge layer that understands both the application domain and the messaging system API.
*   **Single-Role Instances:** The AI MUST ensure a single Message Endpoint instance acts as either a sender or a receiver, but never both simultaneously.

# @Workflow
When tasked with designing or implementing a messaging-based integration solution, the AI MUST strictly follow this step-by-step algorithmic process:

1.  **System Identification:** Identify the independent applications/components that need to exchange data or invoke remote behavior.
2.  **Channel Topology Definition:**
    *   Determine the logical pathways required.
    *   Define the specific Message Channels needed, separating them by the type of data they will carry.
    *   Establish whether each channel requires one-to-one (Point-to-Point) or one-to-many (Publish-Subscribe) semantics.
3.  **Message Definition:**
    *   Define the structure of the Messages traveling on the channels.
    *   Separate system metadata into the Header and business data into the Body.
    *   Determine the semantic intent of the message (Command, Document, or Event).
4.  **Pipeline Construction (Pipes and Filters):**
    *   Identify any intermediate processing required (validation, encryption, deduplication).
    *   Break these requirements down into discrete, single-purpose Filter components.
    *   Connect the Filters sequentially using intermediate Message Channels (Pipes).
5.  **Routing Implementation:**
    *   If the message destination is dynamic or conditional, insert a Message Router.
    *   Extract destination decision logic out of the endpoints and place it into the Router.
6.  **Translation Implementation:**
    *   Analyze the required inbound and outbound data formats of the integrated applications.
    *   If formats differ, insert a Message Translator in the pipeline to convert the Message Body from the source format to the target format.
7.  **Endpoint Integration:**
    *   Generate Message Endpoint code for each application.
    *   Wrap the messaging API connections, instantiations, and transaction handling within the Endpoint.
    *   Expose standard application-specific method calls to the business logic layer.

# @Examples (Do's and Don'ts)

### Message Channel Definition
*   **[DO]** Define specific channels based on data types: `Channel orderChannel = new Channel("NEW_ORDERS"); Channel customerChannel = new Channel("CUSTOMER_UPDATES");`
*   **[DON'T]** Use a generic global channel for all application traffic: `Channel globalChannel = new Channel("ALL_MESSAGES"); // Anti-pattern`

### Message Structure (Header vs. Body)
*   **[DO]** Store routing metadata in the header and business data in the body:
    ```java
    Message msg = new Message();
    msg.setHeader("CorrelationID", "12345");
    msg.setBody("<Order><Total>500</Total></Order>");
    ```
*   **[DON'T]** Bury messaging system metadata inside the application payload:
    ```java
    // Anti-pattern: The messaging system shouldn't need to parse XML to route
    msg.setBody("<Envelope><CorrelationID>12345</CorrelationID><Order>...</Order></Envelope>");
    ```

### Pipes and Filters
*   **[DO]** Create isolated, single-responsibility components that read from an input channel and write to an output channel.
*   **[DON'T]** Build a monolithic script that pulls a message, transforms it, encrypts it, decides who it belongs to, and pushes it to a final destination all in one function block.

### Message Router
*   **[DO]** Read the message, evaluate a condition, and route to the appropriate channel without touching the payload:
    ```java
    if (msg.getHeader("Region").equals("US")) {
        usChannel.send(msg);
    } else {
        euChannel.send(msg);
    }
    ```
*   **[DON'T]** Alter the application data while routing:
    ```java
    // Anti-pattern: Modifying the body inside a router violates single responsibility
    msg.setBody(msg.getBody() + "<Routed>True</Routed>");
    euChannel.send(msg);
    ```

### Message Endpoint
*   **[DO]** Create a Gateway class that abstracts messaging from business logic:
    ```java
    public class OrderGateway {
        public void sendOrder(Order order) {
            Message msg = convertToMessage(order);
            messagingApi.send("ORDER_CHANNEL", msg);
        }
    }
    ```
*   **[DON'T]** Expose messaging APIs (JMS, MSMQ) directly inside the UI or domain logic layers:
    ```java
    // Anti-pattern: Business logic tightly coupled to JMS
    public void calculateTotal(Order order) {
        JMSContext context = connectionFactory.createContext();
        JMSProducer producer = context.createProducer();
        // ... business logic mixed with infrastructure
    }
    ```