# @Domain
These rules trigger when the AI is tasked with designing, developing, or modifying system management, monitoring, or failover mechanisms for asynchronous, message-based integration solutions. This includes implementing metrics collection, health verification (active and passive), dynamic routing for failover, and management console mediation, particularly using MSMQ, C#, or similar queue-oriented messaging architectures (like JMS or WebSphere MQ).

# @Vocabulary
*   **Control Bus:** A dedicated messaging channel used strictly to transmit management, configuration, and metric data, keeping it isolated from application data flows.
*   **Smart Proxy:** An intermediary component that intercepts request messages, replaces the original Return Address with its own, tracks performance metrics (like processing time and queue size), and forwards the reply back to the original requester.
*   **Test Message:** A message injected into the normal data stream with specific, verifiable payload data (e.g., a fixed test SSN) to actively probe the health and accuracy of a message processing component.
*   **Context-Based Router:** A Message Router whose routing decisions are dictated by external environmental states or control events (e.g., failover commands) rather than the content of the message itself.
*   **Management Console:** A centralized application (acting as a Mediator) that aggregates system metrics, visualizes system health, and issues control commands to routers or components based on monitor status changes.
*   **Active Monitoring:** A monitoring strategy that actively probes components by injecting test data, ensuring deep validation of the processing steps.
*   **Passive Monitoring:** A monitoring strategy relying on information generated natively by the components, such as heartbeat messages or log files.
*   **Send Timer:** A timer used within a monitor to dictate the interval between the injection of consecutive Test Messages.
*   **Timeout Timer:** A timer used within a monitor to track the maximum allowable time for a response to a Test Message before a failure is declared.
*   **Asynchronous Completion Token (ACT):** An object reference or identifier passed along with an asynchronous request that is returned with the reply, allowing the caller to restore context and state.

# @Objectives
*   Treat existing business components as black boxes; instrument and monitor them from the outside without modifying their internal business logic.
*   Accurately measure the Quality of Service (QoS) (e.g., response times, queue depth) using non-intrusive intermediaries.
*   Actively verify the correct operation and data accuracy of external services using verifiable Test Messages.
*   Ensure high availability by implementing explicit failover routing mechanisms controlled by a central management entity.
*   Maintain a decoupled architecture even within the Management Console by utilizing delegates and event-driven observer patterns.
*   Optimize network and processing resources by intelligently aggregating metrics and controlling Test Message priority.

# @Guidelines
*   **Black-Box Instrumentation:** When adding management to existing systems, the AI MUST NOT alter the internal code of the target application. Instead, use intermediaries like a Smart Proxy or Wire Tap on the application's external message queues.
*   **Quality of Service Measurement:** To measure response times without losing the original client's routing info, the AI MUST implement a Smart Proxy. The proxy must store the original `Return Address`, substitute its own reply channel, calculate the duration upon receiving the reply, and then forward the reply to the original address.
*   **Metric Aggregation:** When dealing with high message volumes, the AI MUST NOT send a control message for every single application message processed. Instead, accumulate data points locally and use a timer to periodically publish summary statistics (Minimum, Maximum, Average) to the Control Bus.
*   **Test Message Injection:** To verify external services, the AI MUST use a Test Data Generator that creates messages with known, fixed data (e.g., a specific test SSN). The Verifier must check that the returned data falls within acceptable predetermined ranges.
*   **Dual-Timer Monitoring:** When implementing active monitors, the AI MUST utilize two distinct timers: a *Send Timer* to control the frequency of the test requests, and a *Timeout Timer* to flag an exception if a reply is not received within the specified SLA.
*   **Test Message Prioritization:** The AI MUST set Test Messages to a higher priority (e.g., `MessagePriority.AboveNormal` in MSMQ) to ensure they bypass queued application messages and accurately reflect component availability. However, the volume of these messages MUST be kept strictly low to avoid disrupting standard traffic.
*   **State-Change Notification:** To minimize Control Bus traffic, health monitors MUST ONLY notify the Management Console when a state change occurs (e.g., transitioning from "OK" to "Error", or "Error" to "OK"), rather than sending continuous "Error" messages.
*   **Failover Mediation:** Failover logic MUST NOT be hardcoded into the health monitor. Instead, the Monitor sends status updates to the Management Console. The Console (acting as a Mediator) analyzes the status (e.g., using a logical XOR `^` to detect state change) and issues a command to a Context-Based Router to redirect traffic to a secondary provider.
*   **Loose Coupling in UI/Console:** The internal architecture of the Management Console MUST utilize event delegates (e.g., C# `delegate` and `event` constructs) to distribute Control Bus messages to various internal handlers and UI controls, emulating an internal Publish-Subscribe model.
*   **Robust Control Message Parsing:** When reading messages from the Control Bus, the AI MUST parse XML payloads loosely (e.g., reading individual nodes/fields via XPath or DOM traversal) rather than requiring strict, rigid schema deserialization. This prevents console crashes if components add new diagnostic fields to the messages.

# @Workflow
1.  **Map External Interfaces:** Identify the request and reply channels of the component to be monitored, treating the component itself as a black box.
2.  **Establish the Control Bus:** Provision a dedicated messaging channel (Queue or Topic) exclusively for management, status, and metric messages.
3.  **Implement QoS Proxying:** 
    *   Insert a Smart Proxy between the client and the service.
    *   Configure the proxy to calculate time elapsed between request and response.
    *   Track active queue depth by maintaining a synchronized collection of outstanding requests.
    *   Implement a timer to periodically summarize and flush these metrics to the Control Bus.
4.  **Implement Active Monitoring:**
    *   Create a Monitor component that injects a Test Message with known data and `AboveNormal` priority.
    *   Start a Timeout Timer upon sending.
    *   If the reply arrives, validate the data payload (e.g., values within range) and cancel the Timeout Timer.
    *   If validation fails or the Timeout Timer expires, publish an error status to the Control Bus.
5.  **Implement Explicit Failover:**
    *   Insert a Context-Based Router into the primary request channel.
    *   Configure the router to listen to a specific command channel connected to the Management Console.
    *   Upon receiving a failover command, toggle the routing destination to the secondary/backup service channel.
6.  **Construct the Management Console:**
    *   Create a Message Consumer listening to the Control Bus.
    *   Parse incoming XML status messages and trigger internal delegates.
    *   Implement a `FailOverHandler` that listens to these delegates, evaluates if a component has failed, and sends the redirect command to the Context-Based Router.

# @Examples (Do's and Don'ts)

**[DO]** Aggregate QoS metrics using a timer to prevent flooding the Control Bus.
```csharp
protected void OnTimerEvent(Object state) {
    ArrayList currentQueueStats;
    ArrayList currentPerformanceStats;
    
    lock (queueStats) {
        currentQueueStats = (ArrayList)(queueStats.Clone());
        queueStats.Clear();
    }
    lock (performanceStats) {
        currentPerformanceStats = (ArrayList)(performanceStats.Clone());
        performanceStats.Clear();
    }
    
    // Compute min, max, avg locally before sending over the wire
    SummaryStats summary = new SummaryStats(currentQueueStats, currentPerformanceStats);
    if (controlBus != null) {
        controlBus.Send(summary);
    }
}
```

**[DON'T]** Send a metric message to the Control Bus for every single application message processed, which will double or triple network traffic.
```csharp
// ANTI-PATTERN: Flooding the control bus
protected override void AnalyzeMessage(MessageData data, Message replyMessage) {
    TimeSpan duration = DateTime.Now - data.SentTime;
    // Sending a message over the network for every single business transaction
    controlBus.Send(duration.TotalSeconds.ToString()); 
}
```

**[DO]** Use high priority for low-volume Test Messages to accurately gauge service availability without waiting behind large batches of application data.
```csharp
protected void OnSendTimerEvent(Object state) {
    CreditBureauRequest request = new CreditBureauRequest();
    request.SSN = TEST_SSN;
    Message requestMessage = new Message(request);
    
    // Bypass queued application messages to check service health instantly
    requestMessage.Priority = MessagePriority.AboveNormal; 
    requestMessage.ResponseQueue = inputQueue;
    
    requestQueue.Send(requestMessage);
    timeoutTimer = new Timer(new TimerCallback(OnTimeoutEvent), null, timeout*1000, Timeout.Infinite);
}
```

**[DON'T]** Allow a monitor to continuously spam the Control Bus with error messages if a service goes down. Only notify on state changes.
```csharp
// ANTI-PATTERN: Spamming errors
protected void OnTimeoutEvent(Object state) {
    MonitorStatus status = new MonitorStatus(MonitorStatus.STATUS_TIMEOUT, "Timeout", null, MonitorID);
    // This will fire every interval and flood the console log if the service is down
    controlQueue.Send(status); 
}
```

**[DO]** Track state changes in the monitor and only publish to the Control Bus when the status actually changes.
```csharp
if (status.Status != MonitorStatus.STATUS_OK || 
   (status.Status == MonitorStatus.STATUS_OK && lastStatus != MonitorStatus.STATUS_OK)) {
    controlQueue.Send(status);
}
lastStatus = status.Status;
```

**[DO]** Mediate failover logic centrally in the Management Console, using a logical XOR (`^`) to detect state changes before commanding the router.
```csharp
public void OnMonitorStatusUpdate(String ID, int status) {
    if (componentID == ID) {
        if (IsOK(status) ^ IsOK(currentStatus)) { // XOR to detect change
            String command = IsOK(status) ? "0" : "1";
            commandQueue.Send(command); // Send command to Context-Based Router
            currentStatus = status;
            updateEvent(ID, command);
        }
    }
}
```

**[DON'T]** Hardcode the failover routing logic directly inside the Monitor component, which tightly couples monitoring to routing decisions.
```csharp
// ANTI-PATTERN: Tight coupling of monitoring and routing
protected void OnTimeoutEvent(Object state) {
    // The monitor shouldn't know about the ContextBasedRouter's command queue!
    routerCommandQueue.Send("1"); 
}
```