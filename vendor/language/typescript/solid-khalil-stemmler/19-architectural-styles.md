# @Domain
Trigger these rules when tasked with scaffolding new projects, defining high-level folder structures, designing system module relationships, separating system concerns, decoupling large applications, or evaluating system scalability and deployment strategies.

# @Vocabulary
- **System Quality Attributes (SQAs)**: Metrics and characteristics (e.g., flexibility, scalability, messaging) that the system's architecture must protect and maintain to ensure the project's success.
- **Architectural Styles**: High-level groupings of architecture types (similar to design patterns blown up in scale) uniquely suited to protect specific SQAs.
- **Structural Style**: An architectural category focused on the "flexibility" SQA. It organizes code to make the system easier to extend and separate concerns.
- **Component-based Architecture**: A structural style that emphasizes horizontal separation of concerns between loosely coupled, independent components or applications (e.g., separating an enterprise into Docs, Drive, Maps).
- **Layered Architecture**: A structural style that emphasizes vertical separation of concerns by cutting software into specific layers: infrastructure, application, and domain.
- **Monolithic Architecture**: A structural style where the application is combined into a single platform or program and deployed all together as one piece. (Note: A monolith can still be component-based internally).
- **Message-based Style**: An architectural category focused on systems where messaging and behavioral reactivity are crucial. Built on functional programming principles and behavioral patterns.
- **Event-Driven Architecture**: A message-based style viewing all significant state changes as events. It uses Commands and Events as the primary mechanisms to invoke and react to changes.
- **Publish-Subscribe Architecture**: A message-based style that heavily utilizes the Observer design pattern, enabling subscribers to listen to streams or events of interest and publishers to broadcast to them.
- **Distributed Style**: An architectural category focused on the SQAs of scaling throughput, scaling teams, and delegating expensive responsibilities. Components are deployed separately and communicate over network protocols.
- **Client-Server Architecture**: A distributed style dividing work between presentation (client) and business logic (server).
- **Peer-to-Peer Architecture**: A distributed style distributing application-layer tasks between equally-privileged participants forming a network.

# @Objectives
- The AI MUST identify the project's primary System Quality Attribute (SQA) before deciding on an architectural structure.
- The AI MUST treat architectural styles as high-level design patterns and apply them specifically to solve high-level component relationship problems.
- The AI MUST explicitly distinguish between horizontal separation (component-based) and vertical separation (layered) when organizing files and modules.
- The AI MUST prioritize flexibility, scalable messaging, or network distribution based strictly on the chosen architectural style category.

# @Guidelines
- **SQA Mapping Constraint**: The AI MUST explicitly match the architectural style to the required SQA. 
  - If the user requires **Flexibility and Concern Separation**, the AI MUST implement a **Structural** style.
  - If the user requires **Reactivity, State-Change Tracking, or Messaging**, the AI MUST implement a **Message-based** style.
  - If the user requires **Throughput Scaling, Team Scaling, or Task Delegation**, the AI MUST implement a **Distributed** style.
- **Structural/Layered Constraint**: When implementing Layered Architecture, the AI MUST explicitly separate code into `domain`, `application`, and `infrastructure` layers. This is a strict vertical separation.
- **Structural/Component Constraint**: When implementing Component-based Architecture, the AI MUST separate independent features/applications horizontally, ensuring no tight coupling between sibling components.
- **Structural/Monolith Constraint**: The AI MUST NOT assume "Monolithic" means disorganized. When designing a Monolith, the AI MUST deploy the app as a single unit while still applying internal Structural separation (Layered or Component-based).
- **Message-Based/Event Constraint**: When implementing Event-Driven architecture, the AI MUST define clear `Commands` (to invoke changes) and `Events` (to react to changes). 
- **Message-Based/Pub-Sub Constraint**: When implementing Publish-Subscribe, the AI MUST utilize the Observer design pattern to decouple the publisher of an event from its subscribers.
- **Distributed Constraint**: When implementing Distributed architectures, the AI MUST establish clear network boundaries and payload contracts between the separated components (e.g., Client and Server).

# @Workflow
1. **Identify the SQA**: Analyze the user's request to determine the primary System Quality Attribute (Flexibility, Messaging, or Distributed Scaling).
2. **Select the Category**: 
   - Choose *Structural* for complex systems needing logical separation.
   - Choose *Message-based* for systems requiring asynchronous state-change reactions.
   - Choose *Distributed* for systems requiring network-level deployment separation.
3. **Determine the Pattern**:
   - *Structural*: Choose between Component-based (horizontal apps), Layered (vertical tech concerns), or Monolithic (single deployment).
   - *Message-based*: Choose between Event-Driven (Commands/Events) or Publish-Subscribe (Observer pattern).
   - *Distributed*: Choose between Client-Server (Presentation/Logic) or Peer-to-Peer.
4. **Scaffold/Refactor**: Generate the directory structure, class interfaces, or communication boundaries strictly adhering to the definitions of the chosen pattern. 
5. **Enforce Boundaries**: Ensure that dependencies flow correctly according to the chosen separation (e.g., infrastructure must not leak into the domain layer in a Layered architecture).

# @Examples (Do's and Don'ts)

**Principle: Structural Layered Architecture (Vertical Separation)**
- [DO] Structure a layered system strictly into infrastructure, application, and domain layers.
```typescript
src/
  ├── domain/         # Core business rules (zero dependencies)
  ├── application/    # Use cases orchestration
  └── infrastructure/ # Databases, Web Servers, Adapters
```
- [DON'T] Mix infrastructure logic (like database queries) horizontally across the codebase.
```typescript
src/
  ├── components/
  │   ├── User/
  │   │   ├── UserModel.ts
  │   │   └── UserDbQuery.ts # ANTI-PATTERN: Infrastructure mixed into structural domain component
```

**Principle: Message-Based Publish-Subscribe (Observer Pattern)**
- [DO] Use the Observer pattern to decouple publishers from subscribers.
```typescript
class OrderService {
  private dispatcher: EventDispatcher;
  
  createOrder(order: Order) {
    this.db.save(order);
    // Publish-Subscribe architecture
    this.dispatcher.publish(new OrderCreatedEvent(order));
  }
}
```
- [DON'T] Tightly couple components when a message-based architecture is requested.
```typescript
class OrderService {
  private emailService: EmailService; // ANTI-PATTERN: Direct coupling instead of messaging
  
  createOrder(order: Order) {
    this.db.save(order);
    this.emailService.sendOrderEmail(order); 
  }
}
```

**Principle: Component-Based Monolith (Horizontal Separation)**
- [DO] Design a monolith that separates distinct applications/features horizontally while deploying as one unit.
```typescript
src/
  ├── billingApp/     # Independent component
  ├── shippingApp/    # Independent component
  └── server.ts       # Monolithic entry point deploying all components together
```
- [DON'T] Build a monolith as a single entangled mass of logic without component boundaries.
```typescript
src/
  ├── allFunctions.ts # ANTI-PATTERN: Monolith without structural style
  └── server.ts
```