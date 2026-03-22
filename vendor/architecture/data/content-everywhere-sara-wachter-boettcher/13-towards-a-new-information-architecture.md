# @Domain
These rules MUST trigger when the AI is tasked with content modeling, defining content management system (CMS) schemas, structuring JSON/XML data for APIs, designing information architectures (IA), planning multichannel content distribution strategies, or migrating content from fixed layouts (pages/documents) to modular, reusable systems.

# @Vocabulary
*   **Mindset over Method**: The foundational philosophy that prioritizing a flexible, meaning-based framework (retaining purpose and meaning over defining physical location) is more important than specific technical tools or coding languages.
*   **Architecture from Within (Inside-Out Design)**: The principle of designing content structures based on their internal purpose and inherent meaning, rather than their external visual presentation or container. 
*   **Machine for Living In**: A modernist architectural concept applied to content; content systems must be designed for functional, repeatable purpose, but must not sacrifice the human "life" or spirit of the information.
*   **Mass-Produced Content (The Housing Project Anti-Pattern)**: Content that is heavily modularized and functionally adequate but bleak, sterile, robotic, and disconnected from its context or audience.
*   **Mechanical Reproduction**: The automated, algorithmic reuse, duplication, and publication of content across multiple devices, platforms, or channels.
*   **Aura (Essence)**: The inherent brand, message, art, liveliness, and authenticity of a piece of content that makes it valuable and prevents it from feeling like cold, commoditized data.
*   **Handcrafted to Automated Spectrum**: A scale used to classify content components based on how much manual human care they require versus how easily they can be robotically extracted and republished.
*   **Micro Information Architecture**: The process of determining the internal, inherent shape of a single piece of content before connecting it to macro, human-centered navigation or contextual systems.

# @Objectives
*   Transition content structures from fixed, immutable, physical models (pages, documents) to fluid, enduring, modular systems.
*   Prevent the loss of "Aura" and authenticity when content undergoes Mechanical Reproduction across multiple channels.
*   Avoid the "Mass Production" anti-pattern by ensuring content is not treated as identical, homogenous units or commoditized data blobs.
*   Design human-centered structures that feel "in" and "of" their medium, providing context and liveliness regardless of the output device.
*   Perform content modeling creatively and conceptually before translating it into technical specifications (code, databases).

# @Guidelines
*   **Establish Mindset Before Method**: The AI MUST prioritize the preservation of the content's meaning, purpose, and human value over perfectly optimizing for a specific technical framework or output layout.
*   **Apply Inside-Out Design**: The AI MUST derive external technical structures, database fields, and schemas exclusively from the internal purpose of the content. Do not define a field simply because a visual template requires it.
*   **Preserve the Aura**: When atomizing content into chunks, the AI MUST explicitly create fields, metadata, or rules that carry the "Aura" of the content (e.g., editorial tone, emotional resonance, authorial voice). The AI MUST NOT strip content down to purely sterile facts unless explicitly requested.
*   **Avoid Bleak Mass Production**: The AI MUST NOT create schemas that are functionally complete but devoid of context. Content modules must include metadata that allows them to adapt contextually to their surroundings so they feel native to the device/platform.
*   **Model Creatively First**: The AI MUST analyze and document what the content *means* to the user and how it matches the audience's mental models before writing a single line of technical implementation (JSON, XML, GraphQL).
*   **Utilize the Handcrafted to Automated Spectrum**: The AI MUST evaluate and declare where a specific content type sits on this spectrum. Do not enforce rigid single-sourcing or full automation on content that demands high human, in-the-moment care.
*   **Implement Micro-IA**: The AI MUST define the inherent, granular shape of the content components before designing the macro systems that connect them.
*   **Design for Humans, Not Just Tasks**: The AI MUST ensure that the structural breakdown of content serves human understanding, connection, and storytelling, rather than purely mechanical task-oriented efficiency.

# @Workflow
When tasked with modeling, structuring, or architecting content, the AI MUST follow this rigid algorithm:

1.  **Inside-Out Purpose Analysis**:
    *   Identify the fundamental human purpose of the content.
    *   Define the content's internal meaning without referencing where it will live (e.g., website, app, watch, API).
2.  **Creative Modeling (Aura Preservation)**:
    *   Identify the elements that give the content its "Aura" (brand voice, editorial craft, context, human touch).
    *   Map these abstract concepts into discrete structural requirements.
3.  **Spectrum Classification**:
    *   Evaluate the content type on the Handcrafted to Automated Spectrum.
    *   Determine which specific modules can be safely subjected to Mechanical Reproduction via API/CMS, and which require manual editorial intervention.
4.  **Micro Information Architecture Definition**:
    *   Break the content down into granular, semantic chunks (Micro-IA).
    *   Ensure no chunks are created solely for visual presentation (e.g., "Right Sidebar Text"); all chunks MUST be named for their inherent substance.
5.  **Contextual Rule Generation**:
    *   Define the business rules that will allow the content to adapt to different environments without feeling like a sterile "mass-produced housing project."
    *   Establish relational metadata to connect dots for human users.
6.  **Technical Translation**:
    *   Translate the creative model, Micro-IA, and rules into the required technical format (e.g., CMS schema, JSON payload, XML structure, TypeScript interfaces).

# @Examples (Do's and Don'ts)

**DO: Preserve the Aura and apply Inside-Out Design**
```json
{
  "content_type": "Feature Story",
  "purpose": "Immersive storytelling that connects users to the human impact of our brand.",
  "automation_spectrum": "Hybrid - Core facts automated, narrative elements handcrafted per channel.",
  "micro_architecture": {
    "core_narrative": {
      "headline": "The Semantic Title",
      "authorial_voice_notes": "Preserves the handcrafted tone for consuming applications",
      "immersive_body": "Rich text narrative, preserving editorial flow"
    },
    "contextual_adaptations": {
      "mobile_essence_summary": "A handcrafted 140-character version retaining the emotional hook, not just an automated truncation.",
      "related_human_concepts": ["Empowerment", "Community Resource"]
    }
  }
}
```

**DON'T: Apply the Mass Production/Housing Project Anti-Pattern**
```json
{
  "content_type": "Page",
  "purpose": "Fill the template on the desktop site.",
  "automation_spectrum": "Fully automated, stamp everywhere.",
  "micro_architecture": {
    "h1_text": "Title",
    "left_column_blob": "All copy pasted here, stripped of metadata and context.",
    "right_column_call_to_action": "Buy Now",
    "is_mobile": true
  }
}
```
*Why this is incorrect*: It violates "Mindset over Method" by organizing around a fixed page layout (`left_column_blob`). It strips the "Aura" by commoditizing the content into sterile visual blocks. It assumes full mechanical reproduction without considering human context.