@Domain
This rule set activates when the AI is tasked with analyzing a complex system ("a mess"), mapping project requirements, designing software architecture, evaluating user experiences or workflows, structuring information, or diagnosing misaligned project goals. It applies strictly to the planning, mapping, and architectural phases before finalized code, design polish, or content generation begins.

@Vocabulary
- **Reality**: The specific experiences, constraints, and conditions that determine how things appear to and affect a person or project.
- **Players**: The individuals involved in or affected by the mess. Includes Current Users, Potential Users, Stakeholders, Competitors, and Distractors.
- **Factors**: The constraints shaping reality: Time, Resources, Skillset, Environment, Personality, Politics, Ethics, and Integrity.
- **Channel**: Anything that carries or transmits information (e.g., a website, an email, a smartphone app).
- **Context**: The situation a user is in, including location, intent, and emotional state, which shapes their experience.
- **Mental Model**: The internal map, belief structure, and thought process a person uses to understand the world or a specific system.
- **Object**: An externalized representation (map, diagram, prototype, or list) used to share, compare, and align differing mental models.
- **Scope**: The clearly stated purpose and the strict edges/boundaries of a diagram or map.
- **Scale**: The relative size and granularity of a diagrammatic work.
- **Timescale**: The specific period represented by an object (Then/Past, Now/Present, When/Future).
- **Rhetoric**: The persuasive intent behind a diagram (Reflection, Options, Improvements, Identification, or Plan).
- **Block Diagram**: Depicts how objects and attributes interrelate to create a concept.
- **Flow Diagram**: Outlines the steps, conditions, and connections in a discrete process.
- **Gantt Chart**: Depicts how processes and tasks relate to one another over time.
- **Quadrant Diagram**: Illustrates how things compare to one another across exact or ambiguous data spectrums.
- **Venn Diagram**: Highlights overlapping concepts or objects to determine relationships.
- **Swim Lane Diagram**: Depicts how multiple players/actors work together to complete a task within a process.
- **Hierarchy Diagram (Sitemap)**: Depicts how objects, concepts, people, and places relate hierarchically (often using L-brackets or trees).
- **Mind Map**: Illustrates connections between concepts/objects outside of established hierarchies or sequences.
- **Schematic (Wireframe/Blueprint)**: A simplified diagram of an object or interface for the sake of clarity; can be "exploded" to show how pieces form a whole.
- **Journey Map**: Shows the sequential events, contexts, and locations that make up a user's experience.
- **Matrix Diagram**: A grid of boxes collecting tasks or questions (e.g., crossing users with channels) used to identify limits and missing information.

@Objectives
- Confront the reality of the system by explicitly defining all constraints, actors, and environmental factors before proposing solutions.
- Translate internal, unstated mental models into explicit, shared "Objects" (text-based diagrams and maps) to ensure absolute alignment with the user.
- Architect information using flexible, foundational structures (boxes, arrows, diamonds) before applying any aesthetic design or complex code patterns.
- Ensure that the choice of architecture serves the system's unique objectives rather than blindly copying existing industry patterns.

@Guidelines
- **Player Identification**: The AI MUST explicitly list all 5 types of Players (Current Users, Potential Users, Stakeholders, Competitors, Distractors) involved in the prompt before generating structural logic.
- **Factor Evaluation**: The AI MUST evaluate the system against the 8 Factors of reality (Time, Resources, Skillset, Environment, Personality, Politics, Ethics, Integrity). If any factor is unknown, the AI MUST ask the user or state its assumptions.
- **Channel vs. Context Separation**: The AI MUST evaluate Channels and Contexts independently, and then map their intersections. Do NOT assume a 1:1 relationship between a device/channel and a user's context.
- **Anti-Pattern Warning**: The AI MUST NOT implement a solution simply because it fits an "existing pattern." The AI MUST validate that the pattern fits the exact context and reality of the current project.
- **Define Diagram Parameters**: Before creating any architectural object, the AI MUST explicitly declare its:
  - **Scope**: What is included and what is strictly excluded.
  - **Scale**: The level of detail.
  - **Timescale**: Then (Past), Now (Present), or When (Future).
  - **Rhetoric**: The persuasive goal (Reflection, Options, Improvements, Identification, Plan).
- **Architecture Before Design**: The AI MUST use structural primitives to map systems. Concepts must be represented as "boxes" (things), relationships as "arrows" (one-way or two-way), and decision points as "diamonds".
- **Pliable and Tidy Structures**: The AI MUST keep early architectural models simple, text-based (e.g., Markdown lists, ASCII, or Mermaid.js), and highly flexible. Diagrams MUST be tidy, logically consistent, and free of typos to maintain trust, but MUST NOT contain premature styling, CSS, or finalized UI code.
- **Diagram Selection**: The AI MUST utilize the specific diagram type from the 10 defined formats that best fits the analytical need (e.g., use a Swim Lane for multi-actor processes, a Block diagram for abstract concepts).

@Workflow
1. **Face Reality Assessment**:
   - Create a Matrix Diagram crossing the 5 Players against the 8 Factors.
   - Map the required Channels against the possible User Contexts to identify intersections.
2. **Mental Model Extraction**:
   - Output a preliminary list of concepts to compare against the user's mental model. Ask clarifying questions to surface unstated assumptions or jargon.
3. **Parameter Declaration**:
   - Explicitly output the Scope, Scale, Timescale, and Rhetoric for the architectural work to be done.
4. **Architectural Drafting**:
   - Select the most appropriate diagram(s) from the 10 core types (Block, Flow, Gantt, Quadrant, Venn, Swim Lane, Hierarchy, Mind Map, Schematic, Journey Map).
   - Generate the diagram using strictly structural representations (boxes, arrows, diamonds) via Markdown formatting or Mermaid.js.
5. **Pliable Review Phase**:
   - Present the tidy, unpolished diagram to the user. Explicitly ask for structural adjustments ("moving the boxes around") before proceeding to code generation or visual design.

@Examples (Do's and Don'ts)

**Principle: Architecture Before Design (Pliable Structures)**
- [DO]: "Here is the Flow Diagram for the checkout process.
  [Box: Cart] -> [Arrow: Proceed] -> [Diamond: Logged In?]
  -> (Yes) -> [Box: Payment]
  -> (No) -> [Box: Guest Checkout]
  Please review this logic. Should we move any of these boxes before I generate the interface code?"
- [DON'T]: "Here is the React code and CSS for the checkout process using a standard e-commerce UI framework." (Fails to architect before designing; applies existing patterns without structural agreement).

**Principle: Parameter Declaration (Scope, Scale, Timescale)**
- [DO]: 
  "**Timescale**: Now (Current State)
  **Scope**: User registration flow only. Excludes password recovery.
  **Scale**: High-level page sequence.
  **Rhetoric**: Identification (Showing the system as it is today)."
- [DON'T]: "Here is a diagram of the user flow." (Fails to define the boundaries, timeline, or purpose of the object).

**Principle: Evaluating Channels and Contexts**
- [DO]: "We are building a notification system. 
  *Channel*: SMS and Email. 
  *Context*: The user is in a hurry, likely walking, relying on a mobile network.
  *Intersection*: An SMS channel fits the 'in a hurry' context better than a dense email."
- [DON'T]: "Since it's a mobile app, the context is mobile." (Conflates Channel with Context).

**Principle: Selecting the Correct Toolbox Object**
- [DO]: "Because this process involves the Customer, the Sales Team, and the Database, I will use a **Swim Lane Diagram** to depict how these multiple players work together to complete the task."
- [DON'T]: "Here is a Block Diagram showing the customer, sales team, and database." (Uses a concept diagram for a multi-actor workflow process).