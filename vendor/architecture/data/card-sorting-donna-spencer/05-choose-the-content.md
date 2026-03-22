# @Domain
These rules MUST trigger whenever the user requests assistance with selecting, auditing, evaluating, generating, or refining content lists, items, or "cards" for an information architecture (IA) project, card sorting activity, taxonomy design, or menu structuring task.

# @Vocabulary
*   **Wish List**: A comprehensive, brainstormed list of all types of information to be included on a site built from scratch.
*   **Content Inventory**: A full, exhaustive listing of all current content on an existing website.
*   **Content Audit**: A representative sample of content from an existing website.
*   **Free-listing**: A research activity where users or designers list as many items as they can think of for a particular domain, used to explore abstract ideas.
*   **Functionality vs. Content**: The distinction between actionable system tasks (e.g., "Search," "Apply online") and informational material (e.g., "Leave policy," "Office locations").
*   **Format Words**: Terms that describe the medium or container of the information rather than the topic (e.g., "Policy", "Manual", "Guide", "Fact Sheet").
*   **Pattern Matching**: A flawed user behavior where participants group cards based on repeated identical words rather than underlying conceptual meaning.
*   **Overlapping Sets**: A strategy for large sites where a massive content pool (e.g., 300 items) is randomized and split into multiple smaller card sorts (e.g., four sets of 100) with shared cards to ensure broad coverage.
*   **Topic vs. Detailed Content**: The distinction between high-level subject areas ("Topics") and granular, individual pages ("Detailed Content").

# @Objectives
*   The AI MUST ensure that any generated or evaluated list of content items is highly representative, appropriately sized, and consistently granular.
*   The AI MUST rigorously filter out biases, leading terminology, format-based naming, and structural hints that could artificially influence how users group the content.
*   The AI MUST adapt the content selection strategy dynamically based on the origin of the project (new site, existing site, software application, or abstract idea) and the total scale of the information.

# @Guidelines

## Sourcing Content
*   When working on a **new website**, the AI MUST prompt the user to generate a "Wish List" of content ideas in detail.
*   When working on an **existing website**, the AI MUST base selections on a Content Inventory (full list) or Content Audit (representative sample), choosing from topics, individual pages, products, indexes, or consolidated logical sections (e.g., an entire report, not individual report pages).
*   When working on a **system or application**, the AI MUST extract actionable concepts: menu items, key functions, steps in a process, or key tasks.
*   When **exploring an abstract idea**, the AI MUST source content via brainstorming, analyzing existing domains (e.g., tags), analyzing search queries, or referencing free-listing data.

## Evaluating and Normalizing the Content
*   **Ensure Groupability:** The AI MUST verify that every selected content item has at least one potential logical partner. The AI MUST intentionally include 2-3 "easy" items (highly obvious pairs) to build user confidence early in the sort, while removing complete orphans unless specifically testing them.
*   **Enforce Consistent Granularity (Same Level):** The AI MUST NOT mix broad category terms with highly detailed items in the same list. (e.g., Do not include "Accommodations" alongside "Specific Bed & Breakfast Name").
*   **Separate Content from Functionality:** The AI MUST explicitly flag and separate actionable functions (e.g., "Searching the intranet", "Installing new software") from informational content. If they must be tested together, the AI MUST rewrite the functional terms to sound like content (e.g., change "Applying for leave online" to "Online leave system") or rewrite all content as tasks.
*   **Ensure Representative Coverage:** The AI MUST verify that the selected list accurately represents the full scope of the domain being organized.

## Eliminating Bias and Leading Variables
*   **Strip Format Words:** The AI MUST remove or flag words that represent document formats rather than topics (e.g., "Policy," "Manual," "Guide," "Fact Sheet," "How to") to prevent users from grouping by format instead of meaning.
*   **Prevent Pattern Matching:** The AI MUST ensure no single word is overused across multiple items.
*   **Remove Current Structure Bias:** The AI MUST eliminate any terms that strictly replicate the current site's structural naming conventions or departmental org-charts.
*   **Clarify Jargon:** The AI MUST identify terms users might not understand and prompt the user to rewrite them, or suggest a pre-sort prioritization exercise where users can discard unknown cards.

## Sizing and Scaling Strategies
*   **Standard Sizing:** The AI MUST target a final list size of 30 to 100 items. 
    *   *Warning:* Fewer than 30 cards lacks enough overlap to create meaningful groups.
*   **Exceptions for Large Sizes (Up to 200 items):** The AI MAY allow up to 200 items ONLY IF the user confirms the sort is for individuals (not teams), the content is highly straightforward/easy to group, or the cards represent broad topics rather than detailed content.
*   **Strategies for Large Sites:** If the user presents a massive site (e.g., thousands of pages), the AI MUST implement one or more of the following reduction strategies:
    *   *Exclude Knowns:* Ignore sections of the site where the architecture is already agreed upon.
    *   *Sort Small Groups:* Focus the selection on a specific subsection of the site.
    *   *Topic Abstraction:* Elevate the selection from detailed content pages to high-level "Topics."
    *   *Overlapping Sets:* Split a large pool (e.g., 300 cards) into multiple overlapping subsets (e.g., 4 sorts of 100 cards).
    *   *Iterative Sorting:* Recommend starting with broad groups in a first round, then running follow-up sorts for internal content.

# @Workflow
When tasked with generating, evaluating, or refining a content list for a card sort, the AI MUST follow this rigid algorithm:

1.  **Context Definition:** Ask the user whether the project is a new website, an existing website, a software application, or an abstract idea, and determine the overall size of the domain.
2.  **Raw Extraction:** Ingest the raw data (Wish list, Audit, Inventory, or Task list).
3.  **Level Analysis (Granularity Check):** Scan the list for hierarchical mismatches. Segregate broad, parent-level terms from granular, child-level terms. Ask the user which level they wish to test, and discard the other.
4.  **Type Normalization:** Scan for active verbs or system tasks mixed with passive content. Isolate functionality from content and rewrite if necessary to maintain a single lexical type.
5.  **Bias Scrubbing:**
    *   Identify and strip repetitive format words (Policy, Guide, Form).
    *   Identify and rewrite items sharing too many common keywords to prevent pattern matching.
    *   Identify internal jargon and acronyms; expand or rewrite them in user-centric language.
6.  **Partner Validation:** Algorithmically evaluate the remaining list. Ensure >95% of items have a clear conceptual pair or cluster. Flag any standalone outliers for user review. Ensure the presence of 2-3 blatantly obvious pairs to serve as "easy" confidence-builders.
7.  **Quantity Enforcement & Large Site Strategy:** 
    *   Count the items.
    *   If the count is 30-100, finalize the list.
    *   If the count is >100, query the user: *Will this be an individual sort, or a team sort? Are these broad topics or detailed pages?*
    *   If conditions do not support >100 cards, automatically apply a Large Site Strategy (e.g., generate Overlapping Sets, or abstract the content up to broader Topics) until the 30-100 threshold is met.
8.  **Output Output:** Present the finalized, normalized, and bias-scrubbed list.

# @Examples (Do's and Don'ts)

### 1. Granularity and Level Mismatch
*   **[DON'T]** Mix broad concepts with the details that fall inside them:
    *   Accommodations
    *   Bed and breakfasts
    *   Upmarket hotels
    *   Things to do and see
    *   City Zoo
*   **[DO]** Keep all items at the same hierarchical level (either all broad or all detailed):
    *   City Zoo
    *   Science and technology museum
    *   Exhibition of local art
    *   List of bed and breakfasts
    *   List of upmarket hotels

### 2. Mixing Content and Functionality
*   **[DON'T]** Include system tools and passive content in the same unedited list:
    *   Travel policy
    *   Maternity leave provisions
    *   Searching the intranet
    *   People finder
    *   Applying for leave online
*   **[DO]** Segregate functions, or normalize the terminology to read like content:
    *   Travel allowance rules
    *   Maternity leave provisions
    *   Staff directory (normalized from "People finder")
    *   Online leave system (normalized from "Applying for leave online")

### 3. Format Words and Pattern Matching
*   **[DON'T]** Use format words that cause users to group by document type rather than subject:
    *   Travel Policy
    *   IT Security Policy
    *   Hardware Purchasing Form
    *   Leave Request Form
    *   Maternity Leave Guide
*   **[DO]** Strip the format to force users to evaluate the actual topic:
    *   Travel allowances
    *   IT security
    *   Hardware purchasing
    *   Requesting leave
    *   Maternity leave rules

### 4. Overwhelming Size (Large Sites)
*   **[DON'T]** Take every 100th page from a 10,000-page intranet to get 100 cards. This results in random, disconnected content that cannot be grouped.
*   **[DO]** Abstract the detailed pages into "Topics" based on search logs, or focus exclusively on one section at a time (e.g., "Today we are only sorting the Administrative and HR topics, ignoring the Core Business Operations which are already established").