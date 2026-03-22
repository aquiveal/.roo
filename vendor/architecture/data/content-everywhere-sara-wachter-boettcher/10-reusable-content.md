# @Domain
Trigger these rules when the user requests assistance with: architecting content models, designing Content Management System (CMS) schemas, building Application Programming Interfaces (APIs) for content distribution, developing cross-platform or omni-channel applications, migrating legacy or print content to digital platforms, structuring centralized databases, or developing user-personalized dashboards and widgets.

# @Vocabulary
- **Content Reuse**: The practice of pushing a single piece of structured content out to multiple places, assembling it on the fly, or displaying it in different combinations for different purposes.
- **Central Content Store / Repository**: A centralized database or asset library serving as the single source of truth where content is authored in a structured environment and accessed by multiple systems.
- **Content Chunk / Topic**: A discrete, semantic module of content (e.g., a "short summary" or a "tasting note") that can exist independently of a monolithic document.
- **Contextual Presentation**: The practice of exposing, prioritizing, or hiding specific content chunks based on the specific device, use case, or application (e.g., image-heavy for tablets, text-heavy for barcode scanners).
- **Arbitrary Truncation**: An anti-pattern where content is cut off at a specific character limit (e.g., 120 characters) resulting in broken narratives, instead of utilizing dedicated, appropriately sized semantic chunks.
- **Personalized Content**: Content that is dynamically repurposed and reorganized based on the unique requirements, desires, or saved dashboards of an individual user.
- **Customer-Centric Structure**: Organizing and syndicating content based on user needs and tasks rather than the internal organizational chart or agency silos.
- **Editorial Scoring**: A programmatic method of assessing print/legacy layout attributes (page number, space devoted, headline sizing) to automatically determine the digital hierarchy and priority of reused content.
- **Source Content**: The latest, most updated original content asset maintained in the central store, from which all automated variants and handcrafted exceptions are derived.

# @Objectives
- Break down monolithic documents and pages into discrete, machine-readable, and highly structured content components.
- Establish a central content repository as the single source of truth to eliminate redundant authoring and ensure cross-platform accuracy.
- Enable automated, API-driven content distribution that adapts semantically to different platforms (web, mobile, native apps, print).
- Support user-driven personalization by tagging and structuring content so it can be remixed into custom dashboards or widgets.
- Prevent the loss of editorial intent during automation by utilizing structural hierarchy rules rather than flat data dumps.
- Balance automation with human craft by designing systems that handle repetitive publishing but allow for manual overrides where deep editorial care is required.

# @Guidelines
- **Centralize Content Authority:** The AI MUST architect databases and APIs so that content is authored and updated in one central location, completely decoupled from its final presentation layer.
- **Modularize by Semantics, Not Formatting:** The AI MUST break content down into distinct semantic elements (e.g., `product_name`, `quick_facts`, `deep_review`) to allow individual platforms to fetch only what they need.
- **Avoid Arbitrary Truncation:** The AI MUST NEVER design front-end components or APIs that rely on mathematical truncation (e.g., `substring(0, 120)`) to fit content into smaller viewports. It MUST require the creation of dedicated "short" or "teaser" content fields in the schema.
- **Context-Aware Prioritization:** When distributing content to multiple apps/devices, the AI MUST define rules that alter the priority of content elements based on user context (e.g., prioritizing visual elements for browsing apps, and actionable metrics/pricing for utilitarian/scanner apps).
- **Design for Personalization:** The AI MUST architect content models with metadata structures robust enough to allow end-users to filter, save, and aggregate specific content modules into personalized dashboards.
- **Bust Organizational Silos:** The AI MUST map data relationships based on the end-user's mental model and tasks, NOT the internal departmental structure of the publisher (e.g., aggregating all relevant data under a single topical hub, regardless of which internal agency produced it).
- **Preserve Editorial Hierarchy in Migration:** When migrating content from visual/print layouts to digital databases, the AI MUST extract structural signals (size, position, page placement) and translate them into digital weighting/scoring algorithms to preserve the human editorial intent.
- **Support Hybrid Publishing:** The AI MUST NOT force 100% automated reuse if it degrades the user experience. The system MUST provide mechanisms for human editors to manually override automated layouts or handcraft content for high-value contexts, while still pulling foundational data from the central source.
- **Maintain Multi-Variant Assets:** The AI MUST structure repositories to support multiple variations of the same content chunk (e.g., localization, varying technical depths) tied to the same parent entity.

# @Workflow
When tasked with designing a system for reusable content, the AI MUST follow this algorithmic process:

1.  **Deconstruction & Schema Design:** 
    - Analyze the monolithic content. 
    - Define discrete semantic chunks (Title, Teaser, Metadata, Full Body, Media, Contextual Metrics).
    - Map these into a centralized database schema.
2.  **API Distribution Mapping:**
    - Identify all target endpoints, devices, and platforms (Desktop, Mobile Web, Browsing App, Utility App).
    - Map specific content chunks from the schema to specific platforms based on user context.
3.  **Truncation Prevention Check:**
    - Audit the target platforms for space constraints.
    - If space is constrained, ensure a dedicated "short-form" field exists in the schema. Reject any reliance on character-count truncation.
4.  **Personalization & Aggregation Layering:**
    - Apply metadata and taxonomy tags to the content schema to allow for filtering.
    - Design API parameters that allow user-facing applications to request specific widgets or dashboards based on those tags.
5.  **Editorial Priority Translation (If Applicable):**
    - If sourcing from legacy/print material, define an algorithm that translates physical prominence (font size, column inches) into a digital priority score (`priority_weight: 1-10`).
6.  **Override Provisioning:**
    - Implement a flag or workflow stage that allows human editors to fork the automated content for handcrafted presentation without deleting the underlying source data.

# @Examples (Do's and Don'ts)

**Principle: Avoiding Arbitrary Truncation**
- **[DO]**: Architect schemas with multiple resolution fields.
  ```json
  {
    "product_id": "12345",
    "title": "Bleak House",
    "teaser_short": "A satirical look at the byzantine legal system in England.",
    "review_full": "Bleak House is a satirical look at the byzantine legal system in England as it consumes the minds and talents of generations of families..."
  }
  ```
  *Front-end uses `teaser_short` for mobile screens.*
- **[DON'T]**: Rely on string manipulation that breaks the narrative.
  ```javascript
  // Anti-pattern: Cutting off text mid-sentence
  const mobileTeaser = review_full.substring(0, 120) + "..."; 
  ```

**Principle: Context-Aware Prioritization**
- **[DO]**: Design API responses tailored to the specific application's user journey.
  - *Browsing Tablet App Response*: Prioritizes `hero_image_url`, `mood_tags`, and `author_bio`.
  - *In-Store Barcode Scanner App Response*: Prioritizes `item_price`, `stock_status`, and `quick_specs`.
- **[DON'T]**: Send a massive, monolithic HTML blob to all devices and force the client to use CSS `display: none;` to hide irrelevant data.

**Principle: Customer-Centric Structure**
- **[DO]**: Aggregate content by the user's topical need.
  ```text
  Endpoint: /api/topics/flu
  Sources: 
  - CDC (Symptoms Data)
  - NIH (Research Data)
  - FDA (Vaccine Availability)
  ```
- **[DON'T]**: Force the user to navigate the organization's org chart.
  ```text
  Anti-pattern Endpoints:
  - /api/cdc/flu-symptoms
  - /api/nih/flu-research
  - /api/fda/flu-vaccines
  ```

**Principle: Preserving Editorial Hierarchy**
- **[DO]**: Use programmatic scoring to maintain editorial intent when transforming layout to data.
  ```python
  function calculateDigitalPriority(printLayout) {
      let score = 0;
      if (printLayout.page == 1) score += 5;
      if (printLayout.headerFontSize > 24) score += 3;
      return score; // Use this score to order the digital JSON array
  }
  ```
- **[DON'T]**: Ingest print articles alphabetically or chronologically by ingestion time, completely destroying the editor's original front-page curation.