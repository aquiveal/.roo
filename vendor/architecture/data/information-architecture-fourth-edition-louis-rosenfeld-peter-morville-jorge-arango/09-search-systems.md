# @Domain

These rules MUST be triggered whenever the AI is tasked with designing, configuring, evaluating, or implementing search systems, search user interfaces, search engine algorithms, indexing logic, search result pages (SERPs), or any feature related to information retrieval within a digital product, website, or application.

# @Vocabulary

*   **Search System**: The complete infrastructure encompassing the search engine, the index, the retrieval algorithms, the query builders, the search interface, and the result presentation.
*   **Search Zones**: Subsets or pockets of an information environment that have been indexed separately to allow users to search within specific, homogeneous content areas (e.g., by topic, audience, date).
*   **Navigation Pages**: Pages whose primary purpose is to route users to other pages (e.g., indexes, sitemaps, category listings).
*   **Destination Pages**: Pages containing the actual target information or content the user is seeking.
*   **Content Components**: Specific, structured elements of a document or record (e.g., author, title, location, price) rather than the full-text body.
*   **Pattern-Matching**: An algorithm that compares the user's query string to the index to find matching text.
*   **Recall**: The proportion of relevant documents retrieved compared to all relevant documents in the system. High recall retrieves many results, prioritizing exhaustiveness over exact relevance.
*   **Precision**: The proportion of highly relevant documents within the retrieved set. High precision retrieves fewer results, prioritizing exact answers over exhaustiveness.
*   **Stemming**: Expanding a search term to include other terms sharing the same root (e.g., "compute" expands to "computer," "computing").
*   **Document Similarity**: Using a known "good" document to generate a query (by stripping stop words) to find structurally or semantically similar documents.
*   **Query Builders**: Tools that enhance a query's performance behind the scenes, such as spell checkers, phonetic tools (e.g., Soundex), stemming tools, and natural language processors.
*   **Best Bets / Editor's Choice**: Manually curated, highly relevant search results explicitly coupled with specific search queries by human editors.
*   **PageRank / Popularity Ranking**: Ranking results based on external indicators of value, such as the quantity and quality of inbound links or user traffic.
*   **Autocomplete / Autosuggest**: UI patterns that preemptively present potential query matches or results alongside the search box based on partial input.
*   **No Dead Ends Policy**: The architectural principle dictating that a zero-results search page must always provide alternate pathways, tips, or browsing links rather than a blank error state.

# @Objectives

*   Critically evaluate whether a search system is necessary or if navigation improvements/indexes are more appropriate.
*   Precisely define what content should and should not be indexed, strictly separating destination pages from navigation pages to prevent result clutter.
*   Configure indexing to leverage specific content components (metadata) rather than relying solely on full-text indexing.
*   Calibrate retrieval algorithms to achieve the optimal balance of precision and recall based on specific user contexts and tasks.
*   Design search interfaces and result pages that support iterative searching, contextual filtering, and seamless transitions between searching and browsing.
*   Eliminate dead ends in the user experience by providing intelligent recovery paths for failed or overwhelming searches.

# @Guidelines

### 1. System Necessity and Strategic Constraints
*   The AI MUST evaluate the necessity of a search system before implementing one. Do NOT use search as a Band-Aid for poorly designed navigation.
*   The AI MUST recommend search implementation IF: the content volume is too large to browse, the site consists of fragmented silos, the content is highly dynamic (e.g., daily news), or user expectations demand it.

### 2. Indexing and Search Zones
*   The AI MUST exclude Navigation Pages from the search index. Only Destination Pages SHALL be indexed to prevent search results from being cluttered with routing pages.
*   The AI MUST define specific Search Zones for heterogeneous environments. Do not default to a single global index if the content spans wildly different domains (e.g., separate zones for "Products," "Support," "Staff Directory").
*   When indexing, the AI MUST extract and index specific Content Components (e.g., title, author, category, price) to enable fielded searching and structured result displays, rather than relying exclusively on full-text blobs.

### 3. Algorithm and Query Processing Configuration
*   The AI MUST explicitly define the algorithm's bias towards Recall (for exhaustive research tasks) or Precision (for specific, known-item tasks).
*   The AI MUST implement Query Builders to intercept and improve user queries. A spell-checker is MANDATORY for all search implementations.
*   The AI MUST consider Phonetic tools (e.g., Soundex) when the search involves human names or complex proper nouns.
*   The AI MUST configure Stemming rules appropriately: use strong stemming for broad topic exploration and weak/no stemming for exact technical specifications.

### 4. Search Result Presentation
*   **Component Density**: The AI MUST display LESS information per result if users know exactly what they are looking for (e.g., a phone directory). The AI MUST display MORE information (summaries, abstracts, keywords) if users are exploring or comparing.
*   **Contextual Highlighting**: The AI MUST bold or highlight the user's query terms within the surrounding context/snippet in the result list.
*   **Sorting**: When sorting alphabetically, the AI MUST configure the engine to omit initial articles ("a", "an", "the").
*   **Ranking**: The AI MUST NOT use relevance ranking for highly heterogeneous content without metadata. Use Best Bets (manual curation) for the most frequent queries derived from search analytics.
*   **Calls to Action**: If a result represents an actionable item (e.g., an app to download, a product to buy), the AI MUST include a direct call-to-action button within the search result snippet.

### 5. Search Interface Design
*   **The Box**: The AI MUST provide a simple, single-field search box by default. Do not force users to use Boolean operators or advanced syntax in the primary interface.
*   **Autosuggest**: The AI MUST implement autocomplete or autosuggest features to help users identify matches based on partial information.
*   **Query Retention**: The AI MUST retain and display the user's original query in the search box on the results page to support immediate revision.
*   **Transparency**: The AI MUST explain the parameters of the search on the SERP (e.g., "Showing 15 results for '[Query]' in [Search Zone] sorted by [Parameter]").
*   **No Dead Ends Policy**: For zero-result pages, the AI MUST NEVER display a blank page or a simple "No results found" message. The AI MUST provide:
    1. A means to revise the search (the box with the query retained).
    2. Search tips or spelling suggestions.
    3. Alternate browsing links (e.g., sitemap, top categories).
    4. Human contact options if applicable.

# @Workflow

1.  **Assess Requirement**: Determine if the task requires a search system. Evaluate content volume, user interaction preference, and the current state of browsing/navigation.
2.  **Define the Index Space**:
    *   Identify and isolate Destination Pages.
    *   Exclude Navigation Pages.
    *   Define Content Components to be indexed as distinct fields.
    *   Establish Search Zones based on audience, topic, or date.
3.  **Configure Retrieval Mechanics**:
    *   Determine the required balance of Precision vs. Recall.
    *   Apply Stemming, Spell-checking, and Phonetic algorithms.
    *   Define Ranking logic (Relevance, Popularity, Best Bets) or Sorting logic (Alphabetical, Chronological).
4.  **Design the Interface & Input**:
    *   Create a simple global Search Box.
    *   Implement Autocomplete/Autosuggest mechanisms.
    *   Design Advanced Search *only* if the target audience consists of expert researchers.
5.  **Design the Result & Recovery Experience (SERP)**:
    *   Determine data density for result snippets.
    *   Apply contextual highlighting (bolding) to matched terms.
    *   Retain the user's query in the search box.
    *   Display total result counts and active filters.
    *   Implement the "No Dead Ends" fallback for zero-hit states.
    *   Provide options to act on results (save, buy, filter within results).

# @Examples (Do's and Don'ts)

### Indexing Scope
*   **[DO]**: Index only the individual product pages (Destination Pages) and specific metadata fields (Title, Price, SKU).
*   **[DON'T]**: Index the "Browse All Smartphones" category page (Navigation Page), causing it to appear in search results when a user searches for a specific phone.

### Result Snippet Presentation
*   **[DO]**: `**Apple iPhone 14** - 128GB... The **iPhone 14** features a new dual-camera system...` (Highlighting query terms in context).
*   **[DON'T]**: Displaying a generic page meta-description that does not contain the user's specific search term, forcing them to guess why the page was returned.

### Alphabetical Sorting
*   **[DO]**: Sort "The Matrix" under "M" when returning alphabetically sorted movie results.
*   **[DON'T]**: Sort "The Matrix" under "T", causing user confusion.

### SERP UI (Search Engine Results Page)
*   **[DO]**: Display a header stating: `Showing 42 results for "wireless headphones" in Electronics. [Search Box: "wireless headphones"]`.
*   **[DON'T]**: Clear the search box after the user hits enter, forcing them to re-type the entire query if they made a typo.

### Zero-Hit State (No Dead Ends)
*   **[DO]**: `We couldn't find any exact matches for "blutooth hedphones". Did you mean "bluetooth headphones"? Here are our top categories to browse instead: [Link 1] [Link 2].`
*   **[DON'T]**: `0 Results Found.` (Leaving the user stranded with no further actions).

### Search Interfaces
*   **[DO]**: Provide a single, prominent text input field labeled "Search" for the global navigation bar, augmented by autosuggest.
*   **[DON'T]**: Place multiple search boxes (e.g., "Search by Title", "Search by Author") in the global header, confusing users about which box to use.