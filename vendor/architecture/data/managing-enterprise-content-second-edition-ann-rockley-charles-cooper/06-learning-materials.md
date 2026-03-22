@Domain
Trigger these rules when the user requests the design, creation, structuring, translation, or management of learning materials, including Instructor-Led Training (ILT), virtual classroom assets, eLearning modules, mobile learning (mLearning), or Reusable Learning Objects (RLOs).

@Vocabulary
*   **ADL (Advanced Distributed Learning):** The organization that began working on a reference model for reusable learning content in 1997.
*   **SCORM (Sharable Content Object Reference Model):** A collection of standards for eLearning materials that facilitates delivery through an LMS. While it enables delivery, it does not inherently promote the true concept of reusable learning content.
*   **LMS (Learning Management System):** A platform for delivering SCORM-compliant eLearning.
*   **LCMS (Learning Content Management System):** A system that manages learning content components, enabling the delivery to all required learning channels and languages.
*   **ILT (Instructor-Led Training):** Face-to-face training utilizing an instructor, presentation slides (e.g., PowerPoint), instructor guides, and participant materials. 
*   **Virtual Classroom Training:** Web-based, instructor-led sessions featuring whiteboard sharing, breakout sessions, and collaboration.
*   **eLearning:** Web-based training for self-paced learning, ranging from basic "page-turners" to high-end simulations and virtual worlds.
*   **mLearning (Mobile Learning):** Learning delivered in bite-sized pieces on mobile devices, optimized for short, rapid usage and performance support.
*   **RLO (Reusable Learning Object):** Modular, format-agnostic content components that can be mixed and matched to create custom learning experiences.
*   **Page-Turner:** The most basic form of eLearning where content is presented on a screen and the learner clicks a "next" button.
*   **Performance Support:** Job aids, checklists, and rapid-access information lookups ideally suited for mLearning.

@Objectives
*   Free the learning development process from the constraints of specific deliverables (e.g., thinking exclusively in terms of a PowerPoint presentation or an eLearning module).
*   Create format-free, modular Reusable Learning Objects (RLOs) that can be dynamically assembled for any channel (Web, print, mobile).
*   Eliminate the manual synchronization errors between instructor materials, presentation slides, and participant handouts.
*   Drastically reduce the cost of localization, customization, and updates by writing content once and reusing it across global markets.
*   Optimize mobile learning exclusively for performance support and bite-sized consumption, avoiding the forced conversion of monolithic classroom content to small screens.

@Guidelines

*   **Format Separation:** You MUST separate learning content from its delivery format. Never hardcode presentation logic, page layouts (e.g., two-page spreads with instructor notes on the left and participant notes on the right), or slide numbers into the source content.
*   **Modularization:** Break down all learning content into discrete RLOs. Do not generate single, monolithic "chunks" of eLearning content, as these are prohibitively expensive to customize, localize, or update.
*   **Component Synchronization:** Establish relational links between related components. An instructor's note, a participant's exercise, and a presentation slide covering the same concept MUST be linked structurally so that an update to the core concept automatically flags or updates all associated materials.
*   **Metadata Tagging:** You MUST apply specific, granular metadata to every RLO to facilitate automated assembly. Required metadata tags include, but are not limited to: `Instructor`, `Objective`, `Quiz`, `Concept`, and `Support`.
*   **eLearning Constraints:** 
    *   Always account for bandwidth constraints. Design systems that can gracefully degrade or function effectively without high-speed internet streaming.
    *   NEVER use or recommend Adobe Flash. Flash is obsolete on major mobile platforms (like iOS). You MUST use HTML5 for all interactive and simulation-based content.
*   **mLearning Constraints:** 
    *   Do not simply convert classroom or eLearning materials to mobile formats.
    *   Design mLearning strictly for performance support (e.g., job aids, checklists, bite-sized reference material).
    *   Account for small screens, short attention spans, and rapid usage.
*   **Global/Customization Architecture:** Design a core set of corporate operational standards/materials. Provide modular "hooks" allowing regional markets or specific clients to localize, append, or customize the content without altering the core corporate RLOs.
*   **Cost Awareness:** Recognize and design to mitigate the high costs of learning development. (Standard baselines: ILT = 30 hours development per 1 hour instruction; Basic eLearning = 100 hours; Medium eLearning = 200 hours; High-end eLearning = 300+ hours). Maximize reuse to justify these costs.

@Workflow
1.  **Analyze the Learning Request:** Identify the required knowledge domain and the target channels (ILT, Virtual, eLearning, mLearning).
2.  **Deconstruct into RLOs:** Break the instructional material down into the smallest logical Reusable Learning Objects (e.g., a single concept, a single quiz question, a single procedure).
3.  **Strip Format:** Remove all channel-specific formatting (e.g., "On the next slide", "Turn to page 4"). 
4.  **Apply Metadata:** Tag every RLO with standard tags: `Instructor`, `Objective`, `Quiz`, `Concept`, or `Support`. Add regional or market-specific metadata if localization is required.
5.  **Map Relationships:** Define structural links between sibling components. Link an `Instructor` component to its corresponding `Concept` and `Quiz` components.
6.  **Define Assembly Rules:** Create the logic for how these RLOs will be assembled per channel. (e.g., For ILT: Assemble `Concept` + `Instructor` into the Instructor Guide, and `Concept` + `Quiz` into the Participant Guide. For mLearning: Assemble only `Support` and short `Concept` components).
7.  **Generate Output:** Output the structured XML/JSON data ready for ingestion into an LCMS or HTML5 wrapper.

@Examples (Do's and Don'ts)

[DO] Structure learning content as format-agnostic RLOs with strict metadata mapping and HTML5 interactive elements.
```json
{
  "learning_object": {
    "id": "concept_hygiene_101",
    "metadata": {
      "type": "Concept",
      "target": ["eLearning", "ILT", "mLearning"],
      "language": "en_US"
    },
    "content": {
      "title": "Basic Hand Washing",
      "body": "Thorough hand washing prevents cross-contamination.",
      "html5_interactive_asset": "assets/handwash_sim.html"
    },
    "linked_components": [
      {
        "id": "instructor_hygiene_101",
        "metadata": { "type": "Instructor", "target": ["ILT", "Virtual"] },
        "content": "Demonstrate the 20-second scrub technique. Ask participants to pair up and critique."
      },
      {
        "id": "support_hygiene_101",
        "metadata": { "type": "Support", "target": ["mLearning"] },
        "content": "Checklist: 1. Soap, 2. 20-sec scrub, 3. Rinse, 4. Dry."
      }
    ]
  }
}
```

[DON'T] Create monolithic, format-locked content with hardcoded deliverables, manual synchronization markers, and deprecated technology.
```html
<!-- ANTI-PATTERN: Monolithic, format-locked, Flash-dependent -->
<div class="elearning-module">
  <h1>Module 1: Hygiene</h1>
  <p>Welcome to Module 1. Turn to page 5 in your participant guide.</p>
  <p>Instructors: Make sure you are on slide 12.</p>
  <p>Thorough hand washing prevents cross-contamination.</p>
  <object data="assets/handwash_sim.swf" type="application/x-shockwave-flash"></object>
  <p>If you are on a mobile phone, please zoom in to read the slide above.</p>
</div>
```