# @Domain

These rules MUST trigger when the AI is tasked with generating, reviewing, or structuring architecture diagrams (e.g., PlantUML, Mermaid, Graphviz), structural design documents, presentation slide decks (e.g., Reveal.js, Markdown slides, PowerPoint outlines), or infodecks.

# @Vocabulary

*   **Representational Consistency**: The practice of always showing the relationship between parts of an architecture (the overarching context) before drilling down into or changing specific views.
*   **Irrational Artifact Attachment**: An anti-pattern describing the proportional relationship between a person's irrational attachment to a design artifact and how long it took to produce. (e.g., over-investing in high-fidelity diagrams too early).
*   **C4 Model**: A diagramming technique comprising four levels: Context (entire system and users), Container (physical/logical deployment boundaries), Component (architect's view), and Class (UML class diagrams).
*   **ArchiMate**: An open-source enterprise architecture modeling language from The Open Group designed to be "as small as possible" rather than covering every edge case.
*   **Cookie-Cutter Anti-Pattern**: The flawed practice of artificially padding content to make it appear to fill a presentation slide, ignoring that ideas do not have a predetermined word count.
*   **Bullet-Riddled Corpse Anti-Pattern**: A presentation anti-pattern where a slide is filled with dense text (essentially the speaker's notes) that the presenter slowly reads, overloading the visual channel and starving the verbal channel.
*   **Incremental Build**: A presentation technique that exposes information (especially graphical elements) a portion at a time to maintain suspense and audience interest.
*   **Invisibility Pattern**: The strategic insertion of a blank, black slide within a presentation to turn off the visual information channel and refocus audience attention entirely on the speaker.
*   **Infodeck**: A slide deck not meant to be projected but rather emailed and read independently. It summarizes information graphically and contains comprehensive content without time-based transitions or animations.
*   **Stencils/Templates**: A library of common, reusable visual components that create consistency within architecture diagrams.
*   **Magnets**: Specific attachment points on diagram shapes where connecting lines automatically snap and align.

# @Objectives

*   Enforce **Representational Consistency** by ensuring all detailed architectural views are preceded by or explicitly contextualized within a high-level system topology.
*   Prevent **Irrational Artifact Attachment** by starting with low-fidelity, ephemeral outlines or structural scaffolding before generating complex, high-fidelity diagram code.
*   Apply rigid formatting standards to all architecture diagrams, explicitly distinguishing between synchronous and asynchronous communication, deployment artifacts, and logical containership.
*   Structure presentation materials strictly based on their medium: standalone Infodecks require comprehensive text, while live Presentations require sparse text, Incremental Builds, and Invisibility markers.

# @Guidelines

*   **Diagramming Strategy & Consistency:**
    *   When generating architectural diagrams, the AI MUST provide a high-level Context or Topology diagram first, before providing Component or Class-level drill-down diagrams.
    *   Do not immediately generate complex, deeply styled diagram code for initial exploratory architecture requests. Provide a low-fidelity text-based tree or simple wireframe outline first, requesting user confirmation to avoid Irrational Artifact Attachment.
*   **Diagram Tooling Paradigms (Code Generation):**
    *   *Layers*: Organize diagram code into distinct logical groupings or subgraphs to allow the user to easily hide/show details.
    *   *Stencils*: Use reusable macros, variables, or standard shape definitions (e.g., `!include` in PlantUML) to maintain visual consistency.
*   **Diagramming Standards Selection:**
    *   Default to the **C4 Model** when diagramming monolithic applications, separating Context, Container, Component, and Class views.
    *   Use **UML** strictly for Class diagrams and Sequence workflows.
    *   Use **ArchiMate** conventions for lighter-weight, high-level enterprise architecture models.
*   **Diagram Visual Guidelines:**
    *   *Titles & Labels*: Every element MUST be labeled. No ambiguous shapes. Use sticky/space-efficient text blocks.
    *   *Lines*: 
        *   Use solid lines with arrows for **synchronous** communication.
        *   Use dotted or dashed lines with arrows for **asynchronous** communication.
        *   Lines must clearly indicate directional flow.
    *   *Shapes*: 
        *   Use 3D boxes (or cylinder/node equivalents) to represent physical/deployable artifacts.
        *   Use standard 2D rectangles to represent logical containership or boundaries.
    *   *Color*: Do not rely solely on color, but use distinct colors selectively to differentiate specific interacting components (e.g., coloring two different microservices uniquely during a coordination flow).
    *   *Keys/Legends*: The AI MUST append a visual key or legend to every diagram explaining the meaning of shapes, line types, and colors.
*   **Presentation & Slide Deck Rules:**
    *   The AI MUST ask the user if the requested slides are for an **Infodeck** (to be read independently) or a **Live Presentation** (to be spoken over).
    *   *If Infodeck*: The AI MUST generate comprehensive, self-contained text and diagrams. Do not include transition or animation cues.
    *   *If Live Presentation*: The AI MUST enforce the rule that "Slides are half the story".
        *   Never generate slides that read like a "Bullet-Riddled Corpse" (wall of text). Limit slides to short cues, single phrases, or pure visuals.
        *   Generate speaker notes separate from the slide content.
        *   Embed instructions for **Incremental Builds** (e.g., `[Animation: Reveal diagram Step 1, then Step 2]`) to hide future states and maintain suspense.
        *   Do not pad short ideas to fill a slide (**Cookie-Cutter Anti-Pattern**). Leave empty space.
        *   Insert an **Invisibility Pattern** (a completely blank/black slide cue) before a major pivot or highly important speaker point to force attention onto the speaker.
        *   Specify transition styles explicitly: Use subtle transitions (e.g., *Dissolve*) to stitch together ideas within the same topic, and distinct transitions (e.g., *Door*, *Cube*) to indicate moving to a completely new topic.

# @Workflow

1.  **Determine Output Type**: Identify if the user requires an Architecture Diagram, an Infodeck, or a Live Presentation.
2.  **Establish Context (Representational Consistency)**: If diagramming, explicitly define the macro-level system topology first. If presenting, establish the overarching narrative before diving into technical details.
3.  **Create Low-Fidelity Draft**: Output a quick, plain-text structural outline of the diagram or presentation to prevent Irrational Artifact Attachment. Request user validation.
4.  **Apply Formatting Standards**:
    *   *For Diagrams*: Write the diagram code (e.g., Mermaid/PlantUML). Enforce solid lines for sync, dotted for async. Enforce 3D shapes for deployment, 2D for containers. Apply minimal, strategic coloring.
    *   *For Presentations*: Draft the slides. Extract heavy text into Speaker Notes. Apply Incremental Build cues. Insert Invisibility slides where maximum attention is needed.
5.  **Finalize with Keys/Legends**: Ensure every diagram includes a Legend block defining all line types, shapes, and colors. Ensure slide decks include explicit transition/animation cues.

# @Examples (Do's and Don'ts)

### Representational Consistency
*   **[DO]** Generate a top-level system context diagram showing how the `Payment System` connects to the `E-commerce Monolith`, and *then* generate a second diagram zooming into the `Payment System` internals.
*   **[DON'T]** Instantly generate a highly detailed, low-level sequence diagram of a database interaction without ever explaining where that database lives in the overall system.

### Diagram Lines & Shapes
*   **[DO]** 
    ```mermaid
    graph TD
        subgraph Logical_Boundary [Logical Component]
            A[Web Server] -->|Synchronous API Call| B(Auth Service)
            B -.->|Asynchronous Event| C[(Message Queue)]
        end
        style Logical_Boundary fill:none,stroke:#333,stroke-width:2px
    ```
*   **[DON'T]** 
    ```mermaid
    graph TD
        A --> B
        B --> C
        %% Missing labels, missing distinction between sync/async, missing container boundaries.
    ```

### Diagram Legends
*   **[DO]** Always include a legend in the output code:
    ```plantuml
    legend right
      | Line Style | Meaning |
      | Solid | Synchronous Call |
      | Dotted | Asynchronous Message |
      | 3D Node | Deployable Artifact |
      | Rectangle | Logical Container |
    endlegend
    ```
*   **[DON'T]** Assume the user or audience knows what a blue dashed line means without a legend.

### Presentations vs Infodecks
*   **[DO] (Live Presentation Slide)**
    ```markdown
    ---
    Transition: Cube
    
    # Feature Branching Risks
    
    [Visual: Diagram showing a feature branch diverging.]
    [Animation Cue: Wait for speaker, then Build-Out a red warning icon over the unmerged branch to create suspense].
    
    Note to Speaker: Explain the negative consequences of keeping branches alive too long. Emphasize merge conflicts.
    ---
    Transition: Dissolve
    
    # [Blank Black Slide - Invisibility Pattern]
    
    Note to Speaker: The screen is dark. All eyes are on you. Deliver the ultimate takeaway: "Continuous Integration requires integrating continuously."
    ---
    ```
*   **[DON'T] (Live Presentation Slide - Bullet-Riddled Corpse)**
    ```markdown
    ---
    # Feature Branching Risks
    * Feature branches isolate code from the main line.
    * If kept alive too long, they cause massive merge conflicts.
    * Developers lose the context of what others are doing.
    * It violates the principles of Continuous Integration.
    * (Speaker reads this exact text aloud).
    ---
    ```