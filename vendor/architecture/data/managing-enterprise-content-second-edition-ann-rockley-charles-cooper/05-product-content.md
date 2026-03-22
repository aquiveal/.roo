# @Domain
Triggered when the user requests the generation, structuring, architecture, or management of technical product content, documentation, user manuals, online help, learning materials, or any multichannel publishing system.

# @Vocabulary
*   **Single Sourcing:** A method of reusing content where information is written once, stored in a single source location, and reused or referenced many times across different outputs.
*   **Help Authoring Tools (HAT):** Software tools used to support single-source publishing, allowing stand-alone topics to be published to multiple formats (e.g., print and HTML).
*   **Customized Content:** Content deliberately built for specific output from a single source, using sub-elements to provide greater or lesser detail based on the audience or channel context.
*   **Dynamic Content:** Information that exists as a series of components and is assembled on the fly only when requested, often based on user profiles or specific requirements.
*   **DITA (Darwin Information Typing Architecture):** An open XML-based content standard that defines a common structure for content, promoting consistent creation, sharing, and reuse of modular topics.
*   **Specialization:** The process of customizing the basic DITA content model to map exactly to specific, non-standard content requirements.
*   **Intelligent Content:** Content that is not limited to one purpose, technology, or output; it bridges structured authoring with dynamic environments (like the social Web).
*   **Core Content:** The central, definitive source of information that can be augmented by curated customer/community input.
*   **Curation:** The process of selecting the best, most highly rated, or most frequently viewed customer-generated information (from wikis or forums) and transferring it back into the structured core environment.
*   **Augmented Reality (AR) Content:** Three-dimensional or interactive renditions of content designed to be overlaid on physical products via device cameras (e.g., clearing a paper jam).

# @Objectives
*   Transition product content from handcrafted, monolithic documents to modular, reusable, single-sourced components.
*   Completely separate the structural meaning of content from its visual format and device-specific presentation.
*   Enable true multichannel delivery (Print, Web, Mobile, Augmented Reality) from a single content repository using automated stylesheet transformations.
*   Marry the intelligence of strict XML/DITA structures with the flexibility and breadth of the social Web and community wikis.
*   Future-proof technical and product content so it can instantly adapt to new, unforeseen devices and user requirements.

# @Guidelines
*   **Single-Source Mandate:** The AI MUST ensure all content is written once and stored in a central source. When content needs to appear in multiple places, the AI MUST reference the source component rather than duplicating the text.
*   **Modular Topic Creation:** The AI MUST write content as stand-alone, modular topics rather than long, linear documents.
*   **Strict Format Separation:** The AI MUST NOT include inline styles, layout rules, or device-specific formatting (e.g., `<font>`, hardcoded widths) within the content itself. Content MUST remain pure data/structure.
*   **Channel-Agnostic Authoring:** The AI MUST NOT create separate files or copies of content for different channels (e.g., a desktop file and a mobile file). Adaptation MUST be handled via stylesheets applied to the single source.
*   **Sub-Element Customization:** When audiences require different information (e.g., an expert vs. a novice), the AI MUST use conditional sub-elements within the same source topic rather than creating entirely separate topics.
*   **Dynamic Assembly Readiness:** The AI MUST structure content so that it can be easily extracted, queried, and assembled on the fly based on user profiles or real-time requests.
*   **Social Web Integration:** The AI MUST architect content so it can be pushed to wikis or community portals for user enhancement, while maintaining a clear pathway to ingest curated, highly-rated community feedback back into the core XML/DITA source.
*   **Mobile Adaptation:** The AI MUST apply stylesheets to optimize modular structured content for mobile viewing, ensuring the core content remains untouched.
*   **Augmented Reality Hooks:** The AI MUST structure task-oriented product content (e.g., troubleshooting, service documentation) with metadata or hooks that can trigger AR overlays or 3D interactions on supported devices.
*   **Avoid the Multiple-Copy Anti-Pattern:** The AI MUST actively identify and eliminate workflows where content is copied, pasted, and then modified slightly to fit a new medium. 

# @Workflow
1.  **Establish the Single Source:** Define the central repository and base XML/DITA structural model for the product content. 
2.  **Author Modular Topics:** Break down all product knowledge into discrete, stand-alone topics (Concepts, Tasks, References). Write the content focusing entirely on semantics, completely ignoring how it will visually look.
3.  **Define Customization Sub-Elements:** Identify audience-specific or channel-specific variations within the topics. Tag these variations using conditional metadata (e.g., `audience="expert"` or `product="enterprise"`).
4.  **Configure Stylesheet Transformations:** Develop or specify the stylesheets (e.g., XSLT, CSS) required to translate the raw structured components into specific deliverables (Web HTML, Print PDF, Mobile App views).
5.  **Establish the Community Feedback Loop:** 
    *   Push the published content to user-facing platforms (wikis, support portals).
    *   Define a curation process where highly-rated user comments, tips, or solutions are extracted.
    *   Integrate this curated community knowledge back into the core structured repository as augmented sub-elements.
6.  **Enable Dynamic Delivery:** Set up the architecture so the CMS or delivery engine can read user requests or profiles and automatically assemble the required modular topics on the fly.

# @Examples (Do's and Don'ts)

**Principle: Single Sourcing and Sub-Element Customization**

[DO] Create a single structured topic with conditional sub-elements for different contexts.
<task id="t_replace_battery">
  <title>Replacing the Device Battery</title>
  <taskbody>
    <context>Ensure the device is powered off before beginning.</context>
    <steps>
      <step><cmd>Remove the back cover.</cmd></step>
      <step audience="novice">
        <cmd>Locate the small green latch at the top of the battery compartment and gently press it upwards.</cmd>
      </step>
      <step audience="expert">
        <cmd>Release the battery latch.</cmd>
      </step>
      <step><cmd>Remove the old battery and insert the new one.</cmd></step>
    </steps>
  </taskbody>
</task>

[DON'T] Create multiple copied versions of the same file with embedded formatting for different audiences.
<!-- File: Replace_Battery_Novice.html -->
<div style="font-family: Arial; padding: 10px;">
  <h2>Replacing the Device Battery</h2>
  <p>Ensure the device is powered off before beginning.</p>
  <ol>
    <li>Remove the back cover.</li>
    <li><i>Locate the small green latch at the top of the battery compartment and gently press it upwards.</i></li>
    <li>Remove the old battery and insert the new one.</li>
  </ol>
</div>

<!-- File: Replace_Battery_Expert.html -->
<div style="font-family: Arial; padding: 10px;">
  <h2>Replacing the Device Battery</h2>
  <p>Ensure the device is powered off before beginning.</p>
  <ol>
    <li>Remove the back cover.</li>
    <li>Release the battery latch.</li>
    <li>Remove the old battery and insert the new one.</li>
  </ol>
</div>

**Principle: Format Separation for Multichannel Delivery**

[DO] Write semantically, allowing stylesheets to handle the mobile vs. desktop display.
<concept id="c_system_overview">
  <title>System Overview</title>
  <conbody>
    <p>The system monitors output in real-time.</p>
    <image href="system_architecture.svg" placement="break" id="arch_diagram"/>
  </conbody>
</concept>

[DON'T] Hardcode layout constraints that break multichannel delivery (e.g., fixing an image width for a desktop browser, which breaks on mobile).
<div class="overview">
  <h1>System Overview</h1>
  <p>The system monitors output in real-time.</p>
  <img src="system_architecture.jpg" width="800px" height="600px" align="left" />
</div>