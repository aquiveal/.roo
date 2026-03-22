# @Domain
Trigger these rules when the AI is tasked with structuring, categorizing, or organizing information, content, files, features, or data models within a digital product, website, application, or system architecture.

# @Vocabulary
*   **Information Organization:** The categorization of information to provide answers, context, and support for casual browsing and directed searching.
*   **Organization System:** The combination of organization schemes and organization structures used to arrange content.
*   **Organization Scheme:** Defines the shared characteristics of content items and influences the logical grouping of those items (e.g., alphabetical, topical).
*   **Organization Structure:** Defines the types of relationships between content items and groups (e.g., hierarchical, relational/database, hypertext).
*   **Heterogeneity:** An object or collection composed of unrelated or unlike parts (e.g., websites with varying granularities and formats).
*   **Homogeneity:** An object or collection composed of similar or identical elements (e.g., an index of purely alphabetical contacts).
*   **Exact (Objective) Organization Scheme:** Divides information into well-defined, mutually exclusive sections (Alphabetical, Chronological, Geographical). Used for known-item searching.
*   **Ambiguous (Subjective) Organization Scheme:** Divides information into categories that defy exact definition (Topical, Task-oriented, Audience-specific, Metaphor-driven). Used for exploratory seeking.
*   **Polyhierarchy:** A hierarchical structure that allows cross-listing, permitting items to reside in multiple categories simultaneously.
*   **Breadth vs. Depth:** Breadth refers to the number of options at each level of a hierarchy; depth refers to the number of levels.
*   **Faceted Classification:** Categorizing information across multiple independent dimensions (facets) rather than a single strict hierarchy.
*   **Social Classification (Free Tagging/Folksonomy):** User-generated keyword tagging that drives informal, bottom-up organization.

# @Objectives
*   Design organization systems that balance the needs of the users with the goals of the business, neutralizing internal politics and perspective biases.
*   Isolate the design of the organization system from interface and navigation details to ensure a solid structural foundation.
*   Provide robust pathways for both known-item searching (via exact schemes) and serendipitous/exploratory browsing (via ambiguous schemes).
*   Create hierarchies that are scalable, favoring broad-and-shallow structures over narrow-and-deep structures to minimize user cognitive load and interaction friction.

# @Guidelines

## Managing Organizational Challenges
*   **Address Ambiguity:** The AI MUST recognize that language is ambiguous (the "tomato" problem: is it a fruit or a vegetable?). When categorizing ambiguous items, the AI MUST utilize Polyhierarchy to cross-list items in all expected categories.
*   **Handle Heterogeneity:** The AI MUST NOT force a one-size-fits-all structured organization system onto heterogeneous content. The AI MUST evaluate different content formats and granularities independently.
*   **Neutralize Internal Politics & Perspectives:** The AI MUST explicitly reject organization schemes based on internal corporate structures or org charts. The AI MUST prioritize the mental models of external users and customers.
*   **Isolate Organization from Interface:** The AI MUST group information logically before considering navigation UI (e.g., menus, buttons) or exact labels.

## Designing Organization Schemes
*   **Deploy Exact Schemes for Known Items:** The AI MUST use Exact Organization Schemes ONLY when the user knows exactly what they are looking for. 
    *   Use *Alphabetical* for dictionaries, directories, and indexes.
    *   Use *Chronological* for press releases, history, diaries, and logs.
    *   Use *Geographical* for location-dependent data, weather, or local directories.
*   **Deploy Ambiguous Schemes for Exploration:** The AI MUST use Ambiguous Organization Schemes to support associative learning and browsing.
    *   Use *Topical* schemes to define the universe of content by subject.
    *   Use *Task-oriented* schemes for applications prioritizing frequent processes/functions.
    *   Use *Audience-specific* schemes ONLY when there are clearly definable audiences with distinct content needs (determine if the scheme should be open or closed/secured).
*   **Constrain Metaphor-Driven Schemes:** The AI MUST exercise extreme caution with metaphors. The AI MUST NOT use metaphors if they require users to understand unfamiliar concepts (e.g., internal motherboard layouts) or if they introduce unwanted physical constraints.
*   **Restrict Hybrid Schemes:** The AI MUST NOT mix multiple organization schemes (e.g., topic, task, and audience) deeply within a single hierarchy. The AI MUST restrict Hybrid schemes ONLY to shallow, surface-level navigation (e.g., the main page or global navigation).

## Designing Organization Structures
*   **Build the Hierarchy (Top-Down):** The AI MUST use a hierarchy as the primary foundation of the architecture. Categories should be mutually exclusive conceptually, but the AI MUST allow cross-listing of specific items (Polyhierarchy) where ambiguity exists.
*   **Balance Breadth and Depth:** The AI MUST heavily favor broad-and-shallow hierarchies over narrow-and-deep hierarchies. Users MUST NOT be forced to click through more than two or three levels to find content. 
*   **Group at the Page Level:** To safely increase breadth without overwhelming the user, the AI MUST group and structure information visually/logically at the page level (chunking).
*   **Leverage the Database Model (Bottom-Up):** For highly homogeneous sub-sites (directories, catalogs), the AI MUST use a relational database model. The AI MUST define structural metadata tags to enable dynamic searching, filtering, sorting, and associative linking.
*   **Constrain Hypertext:** The AI MUST NOT use hypertext (loose webs of links) as the primary organization structure. The AI MUST use hypertext only as a supplementary system to complement hierarchies and databases via associative linking.
*   **Incorporate Social Classification:** Where applicable for shared digital environments, the AI MUST consider incorporating user-generated tagging architectures (hashtags, endorsements) to supplement top-down structures.

# @Workflow
When tasked with organizing an information environment, the AI MUST follow this algorithmic process:
1.  **Analyze the Content:** Determine if the content is homogeneous (similar items, like a contact list) or heterogeneous (varied formats and granularities, like a corporate intranet).
2.  **Define the Perspective:** Explicitly discard any internal organizational charts. Identify the target audience's mental models and tasks.
3.  **Select Organization Schemes:** 
    *   Identify components requiring Exact Schemes (Alphabetical, Chronological, Geographical).
    *   Identify components requiring Ambiguous Schemes (Topical, Task, Audience).
4.  **Draft the Primary Hierarchy:** Build a top-down hierarchical tree. Ensure the structure is broad-and-shallow. Limit depth to a maximum of 3 levels where possible.
5.  **Apply Polyhierarchy:** Review the hierarchy for ambiguous items. Cross-list items that naturally belong in more than one category.
6.  **Resolve Hybrid Conflicts:** If mixing schemes (e.g., Audience and Topic), move the mixture to the shallowest level (home page) and maintain pure schemes in the deeper levels.
7.  **Integrate Bottom-Up Models:** Identify highly structured subsets of content. Define the metadata schema (entities and attributes) needed to organize this subset using the Database Model.
8.  **Define Associative Links:** Map out where Hypertext or Social Classification will be used to horizontally connect related chunks of information across the hierarchy.

# @Examples (Do's and Don'ts)

## Perspectives and Internal Politics
*   **[DO]:** Organize a consumer electronics site by task and topic: "Buy Products," "Get Technical Support," "Download Drivers."
*   **[DON'T]:** Organize a consumer electronics site by internal corporate division: "Retail Sales Division," "Customer Service Department," "Information Systems."

## Hybrid Organization Schemes
*   **[DO]:** Provide separate, distinct menus on a home page: one grouped by Audience ("For Students", "For Faculty") and another grouped by Topic ("Academics", "Athletics").
*   **[DON'T]:** Mix schemes within a single deep drop-down menu: "Students", "Academics", "Pay Tuition" (mixing audience, topic, and task).

## Hierarchy: Breadth vs. Depth
*   **[DO]:** Design a broad-and-shallow hierarchy presenting 10 categorized options on the main menu, leading directly to the 10 destination content items.
*   **[DON'T]:** Design a narrow-and-deep hierarchy forcing the user through 6 levels of clicking (e.g., Category -> Subcategory -> Sub-subcategory) to reach the destination content.

## Polyhierarchy and Ambiguity
*   **[DO]:** Place "Alternative Healing" under both the "Religion/Philosophy" category and the "Health and Medicine" category to account for semantic ambiguity.
*   **[DON'T]:** Force "Alternative Healing" into only one category, stranding users who navigate using a different mental model.

## Metaphor-Driven Schemes
*   **[DO]:** Use familiar digital metaphors that instantly convey function (e.g., "Trash Can" or "Folders").
*   **[DON'T]:** Force an entire site into a literal physical metaphor (e.g., a "Virtual Village" where the user must click a "Post Office" building to contact support and a "Library" building to read documentation).