# @Domain

These rules MUST trigger when the AI is tasked with designing, evaluating, analyzing, or structuring information architectures, content layouts, search system configurations, navigation menus, sitemaps, or taxonomy schemas for any digital product, website, or application.

# @Vocabulary

*   **Information Architecture (IA)**: The underlying structure of an information environment, encompassing both visible UI elements and invisible backend algorithms, divided into top-down, bottom-up, and invisible architectures.
*   **Top-Down IA**: Architecture defined "from above" that anticipates major user questions (e.g., "Where am I?", "How do I get around?") through global organization, labeling, and navigation systems.
*   **Bottom-Up IA**: Architecture suggested by and inherent in the content itself (e.g., chunking, sequencing, tagging) that supports users who bypass top-down navigation (e.g., arriving via search engines).
*   **Invisible IA**: Backend architectural decisions unknown to users, such as search engine configuration, stop-word removal, and editorial algorithms.
*   **Organization Systems**: Methods of categorizing or grouping content (e.g., by subject, task, audience, or chronology).
*   **Labeling Systems**: The specific language used to represent information categories, options, and links (e.g., scientific vs. lay terminology).
*   **Navigation Systems**: Browsing aids that help users move through information (e.g., clicking through a hierarchy).
*   **Searching Systems**: Mechanisms that allow users to execute queries against an index to find information.
*   **Browsing Aids**: Components presenting predetermined paths to help users navigate and build a sense of place (e.g., menus, links).
*   **Search Aids**: Components allowing user-defined queries and presenting dynamic, automated results.
*   **Chunks**: Logical, nested units of content varying in granularity (e.g., a section, a chapter).
*   **Search Zones**: Subsets of site content separately indexed to support narrower searching.
*   **Query Builders**: Backend ways of enhancing a search query (e.g., spell checkers, stemming, concept searching, synonyms).
*   **Best Bets**: Preferred search results manually coupled with specific search queries by editors or Subject Matter Experts (SMEs).
*   **Controlled Vocabularies/Thesauri**: Predetermined vocabularies of preferred terms, variant terms, broader/narrower terms, and scope notes used to enhance queries.
*   **Identifiers**: Clues suggesting where the user is in the system (e.g., a logo or a breadcrumb).
*   **Sequential Aids**: Clues suggesting where the user is in a process (e.g., "step 3 of 8").

# @Objectives

*   To visualize and implement Information Architecture as a synthesis of Organization, Labeling, Navigation, and Search systems.
*   To seamlessly integrate Top-Down structural pathways with Bottom-Up content-embedded structures.
*   To explicitly define and configure Invisible IA components that power the user experience from behind the scenes.
*   To categorize and implement architectural components rigidly into Browsing Aids, Search Aids, Content/Tasks, and Invisible Components.

# @Guidelines

### Top-Down Information Architecture
*   The AI MUST anticipate and provide structural answers to the following user questions: *Where am I? How do I search? How do I get around? What's important/unique? What's available? What's happening? How do I engage? How do I contact a human? What is the address? How do I access my account?*
*   The AI MUST design global categories, labels, and menus to systematically represent the site's content from a bird's-eye view.

### Bottom-Up Information Architecture
*   The AI MUST chunk content into logical, distinct units.
*   The AI MUST sequence chunks logically (e.g., in a recipe, ingredients must precede mixing instructions).
*   The AI MUST embed metadata and tags into content chunks to answer: *Where am I? What's here? Where can I go from here?* when a user lands deep in the site, bypassing top-down navigation.

### Browsing Aids
When designing browsing systems, the AI MUST explicitly define the following components where applicable:
*   **Organization Systems:** Main categories/taxonomies and user-generated tags.
*   **General Navigation:** Primary systems for global movement.
*   **Local Navigation:** Primary systems for movement within a subsite or specific portion of the environment.
*   **Sitemaps/TOCs:** Condensed overviews of major content areas in outline form.
*   **Indices:** Alphabetized lists of links to content.
*   **Guides:** Specialized information paths on specific topics.
*   **Walkthroughs/Wizards:** Sequential sets of steps.
*   **Contextual Navigation:** Consistently presented links to related content embedded within text.

### Search Aids
When designing search systems, the AI MUST specify:
*   **Search Interface:** Mechanisms for entering/revising queries and configuring searches.
*   **Query Language:** Support for Boolean operators (AND, OR, NOT), proximity operators (ADJACENT, NEAR), and fielded searches (e.g., AUTHOR="Shakespeare").
*   **Query Builders:** Mechanisms for spell-checking, stemming, and injecting synonyms from a thesaurus.
*   **Retrieval Algorithms:** Logic for determining matches and ranking relevance.
*   **Search Zones:** Defined subsets of indexed content to allow focused searching.
*   **Search Results:** The presentation layout of matched content, including what data populates each result, sorting, ranking, and clustering logic.

### Content and Tasks
When structuring actual pages or content components, the AI MUST utilize:
*   **Headings:** Accurate labels for the content that immediately follows.
*   **Embedded Links:** Text-embedded hyperlinks that accurately represent the destination content.
*   **Embedded Metadata:** Extractable information (e.g., tagging an ingredient within a recipe body).
*   **Lists:** Ordered or unordered groups of chunks sharing common traits.
*   **Sequential Aids:** Process indicators (e.g., "Step 1 of 3").
*   **Identifiers:** Contextual location markers like breadcrumbs and logos.

### Invisible Components
*   The AI MUST define backend rules for **Retrieval Algorithms** to rank results.
*   The AI MUST establish **Controlled Vocabularies/Thesauri** to map variant terms (synonyms) to preferred search queries.
*   The AI MUST configure **Best Bets** to manually push editorially selected, highly relevant pages to the top of specific query results.

# @Workflow

1.  **Analyze the Request:** Determine if the task requires Top-Down IA (menus, global structure), Bottom-Up IA (content modeling, chunking, tagging), or Invisible IA (search algorithms, metadata).
2.  **Define Top-Down Browsing Aids:** 
    *   Map out general and local navigation systems.
    *   Establish organization categories and labeling conventions.
    *   Determine if supplementary aids (sitemaps, indices, guides, wizards) are required.
3.  **Structure Bottom-Up Content & Tasks:**
    *   Break content into logical chunks.
    *   Define sequence, headings, embedded links, identifiers, and sequential aids.
    *   Assign embedded metadata to the chunks.
4.  **Configure Search Aids:**
    *   Define the search interface and allowable query languages.
    *   Establish search zones for targeted indexing.
    *   Define the presentation format of search results.
5.  **Specify Invisible Components:**
    *   Define query builders (stemming, spell checking).
    *   Map controlled vocabularies/thesauri.
    *   Assign "Best Bets" for high-priority search terms.

# @Examples (Do's and Don'ts)

### Bottom-Up Content Chunking
*   **[DO]** Structure a recipe document into granular, sequence-aware chunks: `Title` (Label), `Metadata` (Author, Date, Tags), `Ingredients List` (Chunk 1), `Preparation Steps` (Chunk 2, Sequential Aids), `Serving Info` (Chunk 3).
*   **[DON'T]** Present a recipe as a single, monolithic block of text that cannot be indexed by specific fields (e.g., searching specifically by "Ingredients").

### Search System Configuration (Invisible IA)
*   **[DO]** Configure search query builders to handle synonyms and stemming: "If user searches for 'Ukraine', map to variant terms, remove stop words ('the', 'of'), and pin 'Editor's Choice' article at rank #1 using Best Bets."
*   **[DON'T]** Rely strictly on exact-match retrieval algorithms that fail if a user types a plural or a related synonym.

### Search Zones
*   **[DO]** Define search zones for a large software vendor site: "Zone 1: Tech Support Area. Zone 2: Store/Products. Zone 3: Community Forums." Provide interface options for the user to restrict their query to these zones.
*   **[DON'T]** Force a user looking for a technical support troubleshooting article to sift through marketing pages and forum chatter in a single, unfiltered global search result list.

### Navigation and Identifiers
*   **[DO]** Use identifiers (breadcrumbs: Home > Electronics > Audio > Headphones) and local navigation alongside the main content to answer "Where am I?" and "Where can I go from here?".
*   **[DON'T]** Create disconnected "orphan" pages from deep links that lack global navigation, logos, or breadcrumbs, leaving bottom-up users completely disoriented.