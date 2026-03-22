@Domain
These rules activate when the AI is designing, architecting, or implementing composed messaging solutions, particularly those involving multi-step message flows, composite integration patterns (e.g., Loan Broker scenarios), service orchestration, scatter-gather architectures, and process managers across synchronous (Web Services) or asynchronous (Message Queues, Pub-Sub) middleware.

@Vocabulary
- **Composed Messaging:** The combination of multiple routing and transformation patterns (e.g., Content Enricher, Scatter-Gather, Aggregator) to achieve a complex business process.
- **Content Enricher:** A pattern/component that retrieves missing information from an external resource and appends it to a message.
- **Scatter-Gather:** A composite pattern that broadcasts a request to multiple recipients and re-aggregates the responses into a single message.
- **Recipient List (Distribution Addressing):** A routing mechanism where the sender explicitly determines the list of recipients based on business rules.
- **Publish-Subscribe (Auction Addressing):** A routing mechanism where the sender broadcasts to a channel, and any interested recipient can subscribe and respond.
- **Normalizer:** A message translator that converts various proprietary incoming message formats into a single, common Canonical Data Model.
- **Synchronous/Sequential Sequencing:** Executing external requests one at a time, blocking the thread until a response is received.
- **Asynchronous/Parallel Sequencing:** Emitting all external requests simultaneously without blocking, processing responses as they arrive.
- **Process Manager:** A central component that maintains the state of a multi-step sequence, managing multiple concurrent process instances.
- **Asynchronous Completion Token (ACT):** A data structure or object reference passed along with a request and returned with the reply, used to maintain state across asynchronous callbacks.
- **Process Object:** An object-oriented refinement of the ACT that combines the state of the process instance with the callback logic and event handlers.
- **Messaging Gateway:** A design pattern that abstracts specific messaging APIs (e.g., MSMQ, JMS) behind domain-specific method calls to decouple business logic from infrastructure.
- **Correlation Identifier:** A unique ID used to match reply messages to their original request messages. 
- **Service Stub / Mock Queue:** A fake implementation of a messaging gateway or queue used to test business logic without relying on physical messaging infrastructure.

@Objectives
- Architect complex message flows by decomposing them into fundamental integration patterns (Enrich, Route, Scatter, Gather, Translate).
- Maximize system throughput by favoring Asynchronous/Parallel message sequencing over Synchronous/Sequential blocking calls.
- Decouple business logic from messaging infrastructure APIs using Messaging Gateways and Process Objects.
- Ensure robust concurrent processing by rigorously managing conversational state and message correlation.
- Eliminate systemic bottlenecks through dynamic routing rules or by deploying Competing Consumers.
- Guarantee testability by isolating messaging dependencies and utilizing Mock implementations.

@Guidelines
- **Pattern Composition:** When building a multi-step integration (like a Loan Broker), the AI MUST decompose the flow into discrete patterns: Use a Content Enricher to gather prerequisite data, a Scatter-Gather to query multiple providers, Message Translators/Normalizers to handle proprietary formats, and an Aggregator to select the final result.
- **Sequencing Strategy:** The AI MUST prefer Asynchronous (Parallel) sequencing. Avoid Synchronous (Sequential) processing unless explicitly required by legacy constraints, as blocking threads severely limits scalability and increases total response time.
- **Addressing Strategy:** 
  - Use "Distribution" (Recipient List) when the broker must control which participants are eligible (e.g., based on credit score or business rules) and when minimizing network traffic is critical.
  - Use "Auction" (Publish-Subscribe) when you want zero-maintenance participant addition/removal, pushing the filtering responsibility to the recipients (Selective Consumers).
- **Concurrency & State Management:** When implementing asynchronous solutions, the AI MUST NOT rely on sequential code blocks. Instead, use an Event-Driven Consumer model.
- **Asynchronous Completion Tokens (ACT):** To maintain state across decoupled asynchronous event handlers, the AI MUST encapsulate request data and callback delegates into an ACT. 
- **Process Objects:** The AI MUST favor refactoring ACTs into a "Process Object" (e.g., `LoanBrokerProcess`) that houses both the state variables and the event-handling methods, rather than separating data and functionality.
- **Correlation Identifier Selection:** The AI MUST NOT use the infrastructure-generated `MessageID` as the `CorrelationID` if the message will pass through intermediaries (e.g., routers or proxies). Intermediaries often consume and republish messages, altering the `MessageID`. Instead, the AI MUST generate and use a separate application-level property (e.g., `AppSpecific` or a custom header field) for correlation.
- **Gateway Abstraction:** The AI MUST hide all messaging-specific API calls (e.g., MSMQ `BeginReceive`, JMS `QueueConnection`) behind a Messaging Gateway. The rest of the application MUST interact only with domain-specific methods (e.g., `GetCreditScore()`).
- **Aggregation Completeness:** When aggregating responses from a Recipient List, the Aggregator MUST be initialized with the exact number of expected messages. When aggregating from a Publish-Subscribe channel (where the number of recipients is unknown), the Aggregator MUST rely on a Timeout condition.
- **Bottleneck Resolution:**
  - If a specific external service causes a queue backup, the AI MUST propose deploying multiple instances of that service (Competing Consumers).
  - If a "catch-all" or slow service causes bottlenecks, the AI MUST modify the routing rules (Recipient List) to only invoke that service when absolutely necessary.
- **Testing:** The AI MUST design the system so that messaging layers can be swapped with Mock objects (e.g., a `MockQueue` that immediately invokes a callback) to allow unit testing of business and routing logic in a single address space.

@Workflow
1. **Flow Decomposition:** Map the business requirements to structural patterns (e.g., Content Enricher -> Recipient List -> Translators -> Aggregator).
2. **Select Sequencing:** Choose Asynchronous/Parallel processing for high performance.
3. **Select Addressing:** Determine if the solution requires Distribution (Recipient List) or Auction (Publish-Subscribe) semantics.
4. **Design Gateways:** Create Messaging Gateways for all external communication to shield business logic from the messaging API.
5. **Implement State Management:** Define an ACT or Process Object to hold contextual data and handle callbacks for asynchronous replies.
6. **Establish Correlation:** Generate application-specific Correlation IDs to map replies to the correct Process Object instance.
7. **Build Aggregation Logic:** Implement the Aggregator with the correct completeness condition (Count-based for Recipient List, Timeout-based for Pub-Sub).
8. **Test and Optimize:** Create Mock components for testing. Analyze message queues for bottlenecks and adjust routing rules or instance counts accordingly.

@Examples (Do's and Don'ts)

- [DO] Abstract messaging APIs behind domain-specific Gateways.
```csharp
// Business logic only sees domain concepts
public interface ICreditBureauGateway {
    void GetCreditScore(CreditBureauRequest request, OnCreditReplyEvent callback, Object ACT);
}
```

- [DON'T] Leak messaging infrastructure details into business processing logic.
```csharp
// Anti-pattern: Business logic tightly coupled to MSMQ
public void GetCreditScore(int ssn) {
    MessageQueue q = new MessageQueue(".\\creditQueue");
    Message msg = new Message(ssn);
    q.Send(msg);
    // Blocks thread, couples to MSMQ API
}
```

- [DO] Use an application-generated ID for Correlation when intermediaries are involved.
```csharp
// Generating a stable correlation ID independent of physical Message ID
Message requestMessage = new Message(quoteRequest);
requestMessage.AppSpecific = random.Next(); // Stable correlation ID
requestMessage.ResponseQueue = replyQueue.GetQueue();
creditRequestQueue.Send(requestMessage);
```

- [DON'T] Rely on the infrastructure `MessageId` for correlation if the message passes through a Router, as the physical message will change.
```csharp
// Anti-pattern: Will break if a router or proxy sits between sender and receiver
replyMessage.CorrelationId = requestMessage.Id; 
```

- [DO] Encapsulate asynchronous state and callbacks into a Process Object.
```csharp
internal class LoanBrokerProcess {
    protected LoanBrokerPM broker;
    protected string processID;
    protected LoanQuoteRequest request;

    public LoanBrokerProcess(...) { // Initialization }

    // Event handler tied to instance state
    private void OnCreditReply(CreditBureauReply reply, Object act) {
        BankQuoteRequest bankReq = Translator.GetBankQuoteRequest(request, reply);
        bankInterface.GetBestQuote(bankReq, new OnBestQuoteEvent(OnBestQuote), null);
    }
}
```

- [DON'T] Scatter procedural callbacks that require constant up-casting of loose ACT arrays/objects throughout a monolithic class, separating state from behavior.

- [DO] Solve queue bottlenecks by refining Recipient List logic to exclude slow, "catch-all" participants unless strictly required.
```csharp
public IMessageSender[] GetEligibleBankQueues(...) {
    ArrayList lenders = new ArrayList();
    // Only add specific banks based on rules...
    
    // Only fallback to the slow/expensive catch-all if NO other banks match
    if (lenders.Count == 0) lenders.Add(catchAll.Queue); 
    return (IMessageSender[])lenders.ToArray(typeof(IMessageSender));
}
```