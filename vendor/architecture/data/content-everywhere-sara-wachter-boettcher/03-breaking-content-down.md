# @Domain
Trigger these rules when executing tasks involving content modeling, content strategy, website information architecture, defining CMS (Content Management System) requirements, database schema design for digital content, content auditing, or separating monolithic text into structured data formats. 

# @Vocabulary
*   **Content:** A generic, expansive term for digital information that must be strictly avoided as a monolithic concept; it must always be deconstructed into specific types and elements.
*   **Content Type:** The actual, holistic item a user reads or interacts with (e.g., article, recipe, help guide entry, product listing, podcast).
*   **Content Element (Chunk/Module):** The distinct, micro-level building blocks that make up a specific Content Type (e.g., title, teaser, ingredients, pull quote). 
*   **Content Model:** The connective tissue and architectural expression of how specific Content Types and their respective Content Elements coexist and interrelate.
*   **Blobs vs. Chunks:** The dichotomy between shapeless, fixed, unstructured text (blobs) and modular, flexible, purposeful components (chunks).
*   **Content Audit:** An in-depth accounting and qualitative/quantitative evaluation of existing content to uncover existing Content Types, assess consistency, and identify gaps.
*   **Copy Deck / Teaser / Synopsis:** Short, punchy introductory text that leads users into the main content.
*   **Complementary Content:** Sidebars, timelines, or quick facts that are independent of the main narrative but add contextual value.

# @Objectives
*   Deconstruct unstructured, page-based "blobs" of text into flexible, future-ready "chunks" of structured content.
*   Ensure every structural decision is preceded by a deep understanding of the content's inherent meaning, purpose, and audience intent.
*   Define Content Types and Content Elements with absolute precision, tailored specifically to the unique business goals and user needs of the given context.
*   Establish micro-information architectures that empower UX designers, developers, and content creators to build systematic, repeatable, and scalable digital products.

# @Guidelines
*   **Meaning Before Modeling:** The AI MUST NOT generate technical database fields, CMS specifications, or rigid schemas without first defining what the content is supposed to be, what it means, and what it is intended to do.
*   **Goal-Driven Architecture:** The AI MUST adapt content models based on specific organizational contexts. A single concept (e.g., a "Recipe") MUST be modeled differently for a grocery store (focusing on prep time, dietary tags, and ingredient shopping) than for an ad-driven publisher (focusing on related menus, reviews, and page views).
*   **Granular Content Typing:** The AI MUST define Content Types with sufficient granularity based on the organization's industry. Avoid overly broad catch-alls (e.g., do not use "Article" for a media company if they actually publish distinct "Features", "Editorials", and "News Briefs").
*   **Element Distinctness:** When breaking a Content Type down, every Content Element MUST be structurally distinct from others. 
*   **Unit of Information:** Every Content Element MUST contain enough information to communicate something specific.
*   **Avoid Arbitrary Chunking:** If forcing content into multiple elements breaks the narrative flow or feels arbitrary, the AI MUST leave it as a unified "Body Content" chunk.
*   **Semantic Naming:** The AI MUST name elements based on their intrinsic meaning and substance (e.g., "Preparation Time", "Author Attribution"), avoiding indecipherable technical labels (e.g., "Dsd", "Kind") and purely visual/layout-based names.
*   **Extraneous Elimination:** The AI MUST explicitly flag and exclude any proposed Content Type or Element that does not clearly support an identified organizational goal or user need.
*   **Strategic Alignment:** Every Content Element extracted MUST map back to a defined content strategy component: Organizational Goals, Resources, Key Messages, or Voice/Tone.

# @Workflow
1.  **Macro Strategy Assessment:** Identify the overarching goals of the project. Ask and answer: What must this content accomplish for the organization? What do the users need?
2.  **Content Auditing & Type Identification:** Analyze the existing or proposed content to extract specific "Content Types". Validate each type by asking:
    *   Which content goal does this support?
    *   Why would a user want this?
    *   What is the desired post-consumption action?
3.  **Element Deconstruction:** View the identified Content Type from the user's perspective. Break it down into micro-level "Content Elements" (e.g., Headline, Copy deck, Date stamp, Body, Pull quotes, Transcripts).
4.  **Element Validation:** Filter the extracted elements through the dual-requirement test: Is it distinct from the other parts? Does it represent a cohesive unit of information? 
5.  **Substance & Priority Mapping:** Weigh each validated element against the organizational goals (e.g., if brand credibility is a goal, an "Author Byline/Bio" element becomes high priority). Discard elements that do not serve the substance of the specific use case.
6.  **Draft the Content Model:** Document the final architecture, clearly listing the Content Type and its hierarchical, purposeful Content Elements to serve as a blueprint for subsequent CMS and database design.

# @Examples (Do's and Don'ts)

**Principle: Context-Dependent Content Modeling**
*   [DO]: Model a "Recipe" for a public television fundraising campaign with elements like: `Title`, `Chef Name`, `Episode Tie-in`, `Donation Call-to-Action Text`, `Premium Gift Teaser`, `Ingredients`, `Directions`.
*   [DON'T]: Use a generic, one-size-fits-all model for all recipes (`Title`, `Ingredients`, `Directions`) without analyzing the specific business goals of the publisher.

**Principle: Semantic Element Naming vs. Arbitrary Database Fields**
*   [DO]: Name CMS fields based on meaning: `Dietary Category`, `Nutritional Profile`, `Copy Deck`, `Author Attribution`.
*   [DON'T]: Accept or generate legacy, thoughtless, or presentation-based field names: `Kind`, `Dsd`, `Top_Right_Text`, `Big_Red_Header`.

**Principle: Content Type Granularity**
*   [DO]: Audit a university's site and define specific content types: `Faculty Bios`, `Event Listings`, `Degree Program Descriptions`, `Student Testimonials`.
*   [DON'T]: Audit a university's site and group all text under vague types like `Webpage`, `Article`, or `General Text`.

**Principle: Distinct Units of Information**
*   [DO]: Break a long feature story into `Headline`, `Synopsis/Teaser`, `Author Byline`, `Body Content`, and `Complementary Sidebar (Quick Facts)`.
*   [DON'T]: Arbitrarily chop a single, flowing narrative paragraph into `Body_Part_1` and `Body_Part_2` just to create more chunks.