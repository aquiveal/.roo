@Domain
These rules are triggered whenever the AI is tasked with designing, evaluating, refactoring, or implementing communication, data exchange, or integration between two or more disparate software applications, systems, or services.

@Vocabulary
- **Application Integration**: The process of making independent, disparate applications work together to produce a unified set of functionality.
- **Application Coupling**: The degree to which integrated applications depend on each other. Tightly coupled applications make numerous assumptions about each other; loosely coupled applications minimize dependencies.
- **Intrusiveness**: The extent to which existing application code must be modified to support integration.
- **Semantic Dissonance**: Conflicts arising from incompatible ways of defining or conceptualizing data (e.g., differing definitions of an "account" or "oil well") between applications.
- **File Transfer**: An integration style where applications produce and consume files of shared data.
- **Shared Database**: An integration style where applications store and read data from a single, unified database schema.
- **Remote Procedure Invocation (RPI / RPC)**: An integration style where an application exposes procedures (methods) to be invoked remotely by other applications (e.g., CORBA, COM, .NET Remoting, Java RMI, Web Services).
- **Messaging**: An integration style where applications connect to a common messaging system to asynchronously exchange packets of data (messages) frequently, immediately, and reliably.
- **Asynchronous Communication**: A communication model where the sender does not wait for the receiver to process the message before continuing its own work.

@Objectives
- Evaluate integration scenarios against core criteria: coupling, intrusiveness, technology constraints, data format, data timeliness, functional vs. data sharing, and network reliability.
- Select the integration style (File Transfer, Shared Database, RPI, or Messaging) that best balances the specific functional and non-functional requirements of the given scenario.
- Treat remote communication as fundamentally different from local communication, specifically regarding latency, reliability, and concurrency.
- Enforce loose coupling to ensure independent application evolution whenever possible.

@Guidelines

**General Integration Criteria**
- The AI MUST evaluate the need for integration. If a standalone application suffices, avoid integration overhead.
- The AI MUST minimize application coupling. Interfaces MUST be specific enough to be useful but general enough to allow underlying implementations to change.
- The AI MUST account for data timeliness. If lag/staleness is unacceptable, the AI MUST reject File Transfer and prefer Shared Database or Messaging.
- The AI MUST NOT design remote interactions assuming local method call performance or reliability.

**File Transfer Rules**
- When implementing File Transfer, the AI MUST define and enforce strict file-naming conventions and directory structures.
- The AI MUST implement file locking or strict timing conventions to prevent an application from reading a file while another is still writing it.
- The AI MUST define the lifecycle of the file, explicitly designating which application is responsible for deleting old or processed files.
- The AI MUST account for data staleness and synchronization lags in the business logic when using this style.

**Shared Database Rules**
- When implementing a Shared Database, the AI MUST define a unified schema that handles the needs of all integrated applications.
- The AI MUST force the resolution of semantic dissonance during schema design, before code execution.
- The AI MUST utilize transaction management systems to handle simultaneous updates gracefully.
- The AI MUST NOT deploy a Shared Database integration across a Wide Area Network (WAN) due to severe performance bottlenecks and locking conflicts.
- The AI MUST verify if third-party/packaged applications support external schema changes; if not, Shared Database MUST be rejected or strictly bounded.

**Remote Procedure Invocation (RPI) Rules**
- When implementing RPI, the AI MUST encapsulate data behind a function call interface to maintain data integrity within the owning application.
- The AI MUST provide multiple interfaces to the same data if necessary to resolve semantic dissonance for different clients.
- The AI MUST implement strict error handling and timeout mechanisms for remote calls. The AI MUST NOT treat an RPI exactly like a local procedure call.
- The AI MUST avoid creating tightly coupled behavioral knots caused by strict sequencing of remote calls between multiple systems.

**Messaging Rules**
- When implementing Messaging, the AI MUST package data into discrete, customizable messages sent over message channels.
- The AI MUST use asynchronous design to ensure the sender does not block while waiting for the receiver.
- The AI MUST decouple applications by utilizing intermediary message transformers and routers (so senders and receivers do not need to know about each other's internal formats or locations).
- The AI MUST explicitly address the complexities of asynchronous design, including out-of-sequence messages, callback handling, and asynchronous testing/debugging.

@Workflow
1. **Analyze the Context**: Identify the applications to be integrated, their platforms, ownership (internal vs. external/third-party), and whether functionality or just data needs to be shared.
2. **Evaluate Integration Criteria**:
    - Assess required timeliness (real-time vs. batch).
    - Assess data format differences and semantic dissonance.
    - Assess required reliability and network constraints.
    - Assess tolerance for intrusiveness (can the existing application code be modified?).
3. **Select the Integration Style**:
    - Choose *File Transfer* if batch processing is acceptable, data is voluminous, and applications cannot be heavily modified.
    - Choose *Shared Database* if real-time consistency is critical, applications are co-located, and schema control is centralized.
    - Choose *Remote Procedure Invocation* if real-time behavioral collaboration (functional sharing) is required and applications can handle synchronous blocking.
    - Choose *Messaging* if frequent, reliable, asynchronous data and functional sharing is required across decoupled systems.
4. **Implement Style-Specific Mechanics**: Apply the constraints listed in the Guidelines section for the chosen style (e.g., file locks for File Transfer, timeout handling for RPI).
5. **Mitigate Drawbacks**: Explicitly generate code or architectural notes to handle the known drawbacks of the chosen style (e.g., staleness in files, deadlocks in databases, failure handling in RPI, debugging complexity in messaging).

@Examples

**File Transfer**
- [DO]: Implement a writer that locks a file, writes data using a standard format (e.g., XML), releases the lock, and relies on a scheduled cron job to read the file and delete it upon successful processing.
- [DON'T]: Have an application silently overwrite a file while another application is attempting to read it, or leave processed files accumulating in a directory forever.

**Shared Database**
- [DO]: Design a unified SQL schema where Application A and Application B read and write to the same relational tables using database transactions to prevent concurrent update anomalies.
- [DON'T]: Design a Shared Database integration across a WAN connecting systems in different countries, causing local applications to hang due to remote database locking conflicts.

**Remote Procedure Invocation (RPI)**
- [DO]: Expose a SOAP or REST Web Service that encapsulates internal state, and wrap the client invocation in a try/catch block with a defined timeout to handle network unavailability gracefully.
- [DON'T]: Write a remote method call without error handling, assuming the remote server will always be up and the network will always be instantaneous, mimicking a local method call.

**Messaging**
- [DO]: Send a request to a message channel asynchronously, allowing the main thread to immediately continue processing, and use a separate callback or listener to process the response when the receiver eventually completes the task.
- [DON'T]: Force the sending application to wait and block its execution indefinitely until the receiving messaging application processes the message, negating the benefits of asynchronous messaging.