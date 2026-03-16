# @Domain
This rule set is activated when the AI is tasked with software architecture design, component modeling, boundary identification, API definition, refactoring existing architectures, evaluating system scaling strategies, or decoupling system modules.

# @Vocabulary
- **Axis of Change**: A specific vector or reason for which a component might need modification (e.g., localizing language vs. changing the text delivery mechanism).
- **Data Stream**: A specific, isolated flow of data representing a distinct system concern (e.g., UI input/output, network communication, data persistence).
- **Central Transform (Top Component)**: The highest-level policy component where distinct, isolated data streams converge and are processed.
- **Upstream Component**: The higher-level, more abstract component that dictates policy and defines the API interfaces it needs to operate.
- **Downstream Component**: The lower-level, concrete component that implements the API defined by the upstream component.
- **Inflection Point**: The exact moment in a system's evolution where the cost and risk of implementing an architectural boundary becomes less than the cost of ignoring it.
- **YAGNI (You Aren't Going to Need It)**: The software principle dictating that abstractions or boundaries should not be implemented before they are strictly necessary, to prevent over-engineering.

# @Objectives
- Identify and isolate all axes of change to determine where potential architectural boundaries exist.
- Define APIs such that upstream (higher-level) components own the interfaces, which are then implemented by downstream (lower-level) components.
- Structure architectures as multiple converging data streams rather than monolithic blocks.
- Prevent over-engineering by dynamically evaluating the cost of boundary implementation versus the friction of lacking boundaries, applying full boundaries precisely at the inflection point.

# @Guidelines
- The AI MUST NOT limit architectural design to a basic three-tier structure (UI, Business Rules, Database); it MUST actively search for and isolate additional axes of change.
- The AI MUST separate mechanisms from semantics (e.g., decouple the language translation policy from the physical text delivery mechanism).
- The AI MUST ensure that higher-level policy components define the abstract interfaces (APIs) they require, forcing lower-level detail components to implement those interfaces (Dependency Inversion).
- The AI MUST direct all source code dependencies upward toward the highest-level policy component.
- The AI MUST divide data flow into distinct streams (e.g., User Communication, Persistence, Network) that remain isolated from one another until they meet at the central processing policy component.
- The AI MUST analyze the "top" policy component to determine if it contains multiple levels of policy (e.g., low-level mechanical rules vs. high-level state/health management). If different levels are found, the AI MUST split them into separate components divided by a boundary.
- The AI MUST NOT over-engineer systems by implementing full, expensive architectural boundaries prematurely (adhering to YAGNI).
- The AI MUST monitor systems (or user requests) for development friction caused by missing boundaries and MUST implement the boundary immediately at the inflection point.

# @Workflow
1. **Analyze Axes of Change**: Review the system requirements or current code to identify all independent axes of change (e.g., UI delivery mechanism, UI localization/language, data persistence, networking).
2. **Isolate Data Streams**: Segregate system responsibilities into distinct data streams based on the identified axes. Ensure these streams do not cross-communicate at low levels.
3. **Identify the Central Transform**: Determine the highest-level policy component where these data streams must converge to process the core business logic.
4. **Evaluate Policy Levels**: Inspect the Central Transform component. If it handles multiple levels of abstraction (e.g., `MoveManagement` handling local mechanics vs. `PlayerManagement` handling overall state), split it into separate components and establish a boundary between them.
5. **Define APIs (Dependency Inversion)**: Within the higher-level components, define the abstract APIs. Ensure the lower-level components implement these APIs, ensuring source code dependencies point upward.
6. **Assess Boundary Costs (Inflection Point Analysis)**: Evaluate the immediate cost of implementing each identified boundary against the current development friction.
7. **Execute Boundary Implementation**: Implement full, reciprocal polymorphic boundaries only for components that have reached the inflection point. For all other potential boundaries, use partial boundaries or standard logical separation to avoid over-engineering.

# @Examples (Do's and Don'ts)

### Defining APIs and Dependency Direction
- **[DO]**: Define an interface `DataStorageAPI` inside the `GameRules` (high-level) package. Have the `CloudStorage` (low-level) class implement `DataStorageAPI`.
- **[DON'T]**: Define a `CloudStorage` class in a database package and have the `GameRules` package import and call `CloudStorage` directly.

### Separating Axes of Change
- **[DO]**: Create a `Language` component that translates system events into Spanish, and a separate `TextDelivery` component that sends those translated strings via SMS. The `Language` component defines the delivery API that the `TextDelivery` component implements.
- **[DON'T]**: Create a single `SpanishSMS` class that hardcodes both the Spanish translation dictionary and the Twilio SMS API logic.

### Splitting the Streams (Levels of Policy)
- **[DO]**: Separate game logic into `MoveManagement` (calculating valid moves and collisions) and `PlayerManagement` (calculating overall health and win/loss state based on events emitted by `MoveManagement`).
- **[DON'T]**: Place X/Y coordinate collision math and Player Account billing logic in the same `GameEngine` class.

### Managing the Inflection Point (YAGNI)
- **[DO]**: Start with logical separation of components within the same codebase. When a specific component (e.g., `PlayerManagement`) needs to be scaled independently on a separate server, introduce a full micro-service architectural boundary.
- **[DON'T]**: Build a massive multi-server micro-service architecture with complex routing and reciprocal polymorphic boundaries for a simple command-line game before it has any network requirements.