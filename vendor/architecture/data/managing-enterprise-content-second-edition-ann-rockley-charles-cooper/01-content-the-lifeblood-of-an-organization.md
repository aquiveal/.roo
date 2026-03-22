# @Domain
Trigger these rules when the user requests assistance with content strategy, content architecture, multi-channel publishing (Web, mobile, print, eBook, apps), content management system (CMS) design, technical documentation planning, content auditing, or enterprise content restructuring.

# @Vocabulary
*   **Content Silo Trap**: The anti-pattern where content is created in isolation by different groups or specifically for one channel, leading to duplicated, inconsistent, and costly content iterations that cannot be easily shared.
*   **Unified Content Strategy**: A repeatable method of identifying all content requirements up front, creating consistently structured content for reuse, managing that content in a definitive source, and assembling content on demand to meet customer needs.
*   **Information Product**: The final compiled deliverable (e.g., a website, training manual, or marketing brochure) that is assembled from modular content components.
*   **Content Object / Component**: A modular, structured piece of content designed to be written once and compiled into multiple information products.
*   **Core Content**: Information components that are reused across multiple information products and channels.
*   **Unique Content**: Information components that are specific to a single information product and not reused.
*   **Channel**: The delivery mechanism or platform for content (e.g., print, Web, mobile, smartphone, tablet, eBook).

# @Objectives
*   Break down content silos by enforcing a unified, collaborative, cross-departmental content architecture.
*   Maximize content reuse to reduce creation, management, delivery, and translation costs.
*   Design content as modular, device-agnostic components rather than monolithic, handcrafted documents.
*   Ensure a consistent customer experience by maintaining a single source of truth for information used across marketing, sales, support, and technical publications.
*   Enable unlimited, automated device delivery by separating content structure from its presentation format.

# @Guidelines
*   The AI MUST NEVER design or generate content structures that are tightly coupled to a specific delivery channel (e.g., creating separate "mobile text" and "desktop text" versions of the exact same information).
*   When requested to draft or structure content, the AI MUST break the content down into granular components (objects) rather than writing a single monolithic document.
*   The AI MUST explicitly separate "Core" (reusable) content from "Unique" (context-specific) content in any proposed architecture.
*   The AI MUST strictly avoid the "copy and paste" methodology for content reuse; it MUST define a single definitive source module that is referenced, queried, or assembled dynamically.
*   When analyzing an organization's existing content or processes, the AI MUST actively flag symptoms of the "Content Silo Trap" (e.g., duplication of effort, inconsistent messaging across departments, disparate software initiatives, handcrafting deliverables).
*   The AI MUST enforce consistent structure across content components to ensure they can be automatically adapted to new devices with little or no human intervention.
*   The AI MUST prompt the user to identify existing content before generating entirely new content from scratch to prevent duplication of effort.

# @Workflow
1.  **Requirement Analysis**: Identify all cross-departmental content requirements up front. Determine exactly what content needs to be created, for whom, and by whom.
2.  **Audit Current State**: Evaluate how content is currently created, managed, and delivered to identify existing content silos, inconsistencies, and areas of duplicated effort.
3.  **Component Identification**: Break down the required information products into modular "Content Objects" or "Components." 
4.  **Core vs. Unique Classification**: Categorize each component as either "Core content" (to be reused across multiple products/channels) or "Unique content" (specific to a single deliverable).
5.  **Definitive Source Creation**: Establish a single, structured source of truth for each component. Ensure the structure is device-agnostic and completely separated from presentation formatting.
6.  **Assembly Definition**: Define the programmatic or systematic assembly process where components are compiled on demand into varied information products (Web, print, mobile, eBook) without manual reworking.

# @Examples (Do's and Don'ts)

**Principle: Modular Content Creation vs. Monolithic Documents**
*   [DO]: Define a JSON, XML, or Markdown structure that separates a product page into reusable objects. 
    ```json
    {
      "core_product_description": "Standardized text used across web, print, and mobile.",
      "technical_specs": "Tabular data component.",
      "marketing_tagline": "Short copy for social media and headers."
    }
    ```
*   [DON'T]: Generate a single, highly formatted text document titled "Website_Product_Page_Final" that weaves layout instructions, standard text, and channel-specific formatting inextricably together.

**Principle: Multi-Channel Adaptation vs. Siloed Duplication**
*   [DO]: Architect a single source file for a company promotion that is dynamically compiled by a CMS into the customer support knowledge base, the mobile app alert system, and the printed retail flyer.
*   [DON'T]: Create three distinct files (`promo_web.html`, `promo_mobile.xml`, `promo_print.pdf`) that require marketing, customer support, and IT to manually and independently update their own siloed versions.

**Principle: Content Assembly**
*   [DO]: Construct an Information Product (like a Training Manual) by referencing existing modules: `[Include: Core_Feature_Overview]`, `[Include: Safety_Warnings_Global]`, `[Write: Unique_Instructor_Notes]`.
*   [DON'T]: Copy the text from the `Core_Feature_Overview`, paste it directly into the new Training Manual draft, and alter the wording slightly, thereby breaking the single source of truth.