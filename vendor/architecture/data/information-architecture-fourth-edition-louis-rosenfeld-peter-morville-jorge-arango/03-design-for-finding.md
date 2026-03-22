# @Domain
These rules MUST trigger when the AI is tasked with designing, evaluating, or modifying website architectures, navigation systems, search functionalities, user journeys, user personas, information-retrieval workflows, or conducting user research related to how humans find and consume information within digital ecosystems.

# @Vocabulary
*   **Information Need**: The root motivation driving a user to visit a site or app. Needs dictate specific information-seeking behaviors.
*   **The "Too-Simple" Information Model**: A flawed, mechanistic algorithmic model of user behavior (User asks question -> Something happens -> User receives answer). It falsely assumes predictable users, ignores context, and erroneously measures success purely by speed or minimized clicks.
*   **Known-Item Seeking (The Perfect Catch)**: Searching for a single, specific, known "right" answer or item (e.g., a colleague's phone number or the population of a city).
*   **Exploratory Seeking (Lobster Trapping)**: Open-ended searching where the user lacks a precise articulation of their need and hopes to gather a few useful items, suggestions, or ideas to learn from and make decisions.
*   **Exhaustive Research (Indiscriminate Driftnetting)**: Leaving no stone unturned to find everything available on a specific topic. Requires patience and the use of highly varied terminology.
*   **Refinding (Moby Dick)**: The behavior of attempting to locate a piece of useful information previously encountered.
*   **Information-Seeking Behaviors**: The actual methods users employ to find information, consisting of searching (queries), browsing (links), and asking (human help).
*   **Integration**: The fluid combination of searching, browsing, and asking within a single finding session.
*   **Iteration**: The process of a user's information need changing as they learn, prompting them to try new search/browse approaches sequentially.
*   **Berry-Picking Model**: A behavioral model by Marcia Bates where users start with a need, formulate a query, move iteratively through a system, pick bits of information ("berries") along the way, and constantly modify their requests as they learn.
*   **Pearl-Growing Model**: A behavioral model where users start with one or a few good documents ("pearls") and utilize system features to find "more like this one."
*   **Two-Step Model**: A behavioral model typical of corporate portals where users first locate the correct sub-site/directory (Step 1) and then search for specific information within that sub-site (Step 2).
*   **Search Analytics**: The review of common search queries in logfiles to diagnose problems with search performance, metadata, navigation, and content.
*   **Contextual Inquiry**: An ethnographic user research method involving observing users interacting with information in their "natural" settings and asking them the reasoning behind their actions.

# @Objectives
*   The AI MUST completely discard the mechanistic "Too-Simple" query-to-answer model of information retrieval.
*   The AI MUST explicitly define the user's specific *Information Need* before proposing any structural or navigational solutions.
*   The AI MUST architect systems that accommodate iterative, messy, non-linear human thought processes, specifically supporting the integration of searching, browsing, and asking.
*   The AI MUST propose structural mechanisms that cater to the four distinct metaphorical finding behaviors: The Perfect Catch, Lobster Trapping, Indiscriminate Driftnetting, and Refinding.

# @Guidelines

*   **Handling the "Too-Simple" Model**: When evaluating user journeys or search architectures, the AI MUST reject workflows that treat the user as an automaton entering a query and receiving a perfect answer. The AI MUST NOT use time-on-task, click-counts, or page-views as the sole quantifiable metrics for findability success, as partial satisfaction and learning mid-journey are valid human experiences.
*   **Designing for Known-Item Seeking (The Perfect Catch)**: When encountering tasks where users know exactly what they are looking for, the AI MUST implement direct, exact-match database search functionality and explicit, structured sorting (e.g., alphabetical staff directories).
*   **Designing for Exploratory Seeking (Lobster Trapping)**: When encountering users attempting to learn or compare concepts without a clear "right" answer, the AI MUST design broad categorization, associative browsing links, and guided step-by-step tutorials to help users iteratively define their needs.
*   **Designing for Exhaustive Research (Indiscriminate Driftnetting)**: When encountering academic, competitive, or medical research personas, the AI MUST implement advanced search filters, robust metadata tagging, and support for highly varied synonymous terminology to ensure all relevant documents can be captured.
*   **Designing for Refinding (Moby Dick)**: When encountering dense information environments, the AI MUST implement mechanisms for users to tag, save, favorite, bookmark, or "read later" to combat human memory failure and scheduling constraints.
*   **Supporting Integration**: When architecting navigation, the AI MUST provide pathways to search, browse, and ask for human help (e.g., chat interfaces, email links) on the same interface layer, allowing users to pivot seamlessly between methods.
*   **Supporting the Berry-Picking Model**: When structuring product pages or content hubs, the AI MUST allow users to search *within* browsed categories, and browse *from* search results. The AI MUST NOT trap users in a dead-end search results page without category browsing options.
*   **Supporting the Pearl-Growing Model**: When displaying highly relevant documents or items, the AI MUST design features such as "Similar pages," "More like this," co-citation links, or shared user-supplied tags to allow users to pivot from one perfect result to related content.
*   **Supporting the Two-Step Model**: When tasked with organizing large intranets or portals containing hundreds of departmental subsites, the AI MUST design a macro-level directory or search-to-navigate system (Step 1) that cleanly hands the user off to the micro-level subsite architectures (Step 2).
*   **Conducting User Research (Search Analytics)**: When tasked with discovering user needs, the AI MUST request, simulate, or analyze search engine logfiles (Search Analytics) to diagnose vocabulary mismatches, metadata gaps, and true user intent.
*   **Conducting User Research (Contextual Inquiry)**: When proposing user testing methodologies, the AI MUST prioritize Contextual Inquiry (observing users in their natural environment) to capture the context preceding and following the keyboard interaction, rather than relying strictly on sterile focus groups.

# @Workflow
When tasked with designing or evaluating an information architecture for findability, the AI MUST follow this rigid step-by-step algorithm:

1.  **Identify Information Needs**: Map the project's user personas to the four metaphorical needs. Explicitly state whether the user is pursuing a Perfect Catch, Lobster Trapping, Driftnetting, or Refinding.
2.  **Reject the Too-Simple Model**: Audit the proposed or existing user journey. Identify and eliminate assumptions that the user knows exactly what to type and will find the exact answer on the first try.
3.  **Map the Seeking Behaviors**:
    *   Design the *Berry-picking* loop: Ensure search results offer contextual category links, and category pages offer localized search boxes.
    *   Design the *Pearl-growing* pivot: Add "related items" or metadata tag links to destination pages.
    *   Verify *Integration*: Ensure searching, browsing, and asking (contacting a human/support) are concurrently available.
4.  **Select Research Methods**: If tasked with validation, prescribe Search Analytics to gather quantitative vocabulary data, and Contextual Inquiry to observe environmental and iterative behavioral constraints.

# @Examples (Do's and Don'ts)

**Principle: Supporting the Berry-Picking Model (Integration of Search and Browse)**
*   [DO]: A layout where a user searches for "camping gear", receives a list of items, and alongside the items is a sidebar allowing them to browse by categories (e.g., "Tents", "Sleeping Bags") found *within* those search results. Conversely, while browsing the "Tents" category, a search bar is provided restricted to "Search within Tents".
*   [DON'T]: A layout where a user searches for "camping gear", receives a flat list of 1,000 items, and must hit the "Back" button to return to the homepage directory if they wish to browse categories. 

**Principle: Supporting the Pearl-Growing Model**
*   [DO]: At the bottom of a highly technical article on "CSS Grid Architecture," including a section labeled "Articles sharing the tags: CSS, Layout, Frontend" and a button reading "Find Similar Articles."
*   [DON'T]: An article page that ends abruptly, forcing the user to return to the global search box and attempt to guess which keywords might yield an article of similar quality.

**Principle: Evaluating Findability Success (Avoiding the Too-Simple Model)**
*   [DO]: Measuring success by observing how easily a user transitions from a broad search ("retirement plans") to a narrower browse path ("Roth IRA"), acknowledging that learning occurred during the session.
*   [DON'T]: Flagging a user session as a "failure" simply because the user executed 4 different searches and clicked 12 times, falsely assuming a 1-click query-to-answer ratio is the only valid metric of good IA.