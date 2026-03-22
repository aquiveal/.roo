@Domain
These rules are triggered when the AI is tasked with analyzing card sort data, conducting qualitative user research analysis, processing content categorization datasets, evaluating information architecture (IA) structures, or performing "Exploratory Analysis" on grouping and sorting results.

@Vocabulary
*   **Exploratory Analysis:** A qualitative data analysis methodology focused on "playing with data" to discover patterns, group formations, classification schemes, and participant terminology without relying on statistical algorithms.
*   **Standardized Label:** A unified category name created by the analyst to consolidate multiple highly similar, participant-generated labels (e.g., merging "About Region" and "The Region" into "About the Region").
*   **Data Matrix:** A grid where rows represent individual cards, columns represent participants, and the intersecting cells contain the group label assigned by the participant.
*   **Flat Hierarchy:** The result of removing nested layers from participant-created groups to ensure all categories exist on a single, equal level for the purpose of exploratory analysis.
*   **Internal Correctness:** The technically or logically "accurate" placement of a piece of content, which participants may or may not align with depending on their understanding or the ambiguity of the card.
*   **Closed Card Sort Matrix:** A specific analytical grid for closed card sorts where predefined categories form the top row, cards form the first column, and intersecting cells contain the frequency count of placements.
*   **Clumping:** A phenomenon in closed card sorts where content is heavily concentrated into a few categories, indicating that those categories may be too broad.

@Objectives
*   Extract actionable qualitative insights from raw card sorting data to inform Information Architecture (IA) and content strategy.
*   Identify and standardize highly similar participant-generated categories to reveal underlying consensus.
*   Detect discrepancies, surprises, and anomalies in group creation and card placement to uncover user mental models.
*   Evaluate the terminology, formality, and organizational schemes utilized by participants.
*   Diagnose ambiguous content, overlapping categories, and potential labeling failures through the analysis of misplacements and "Other" groupings.

@Guidelines
*   **Data Standardization Rules:**
    *   The AI MUST create Standardized Labels for groups that share highly similar language or identical underlying ideas.
    *   The AI MUST NOT combine groups unless the word or idea is extremely similar; forcing combinations destroys analytical value.
    *   The AI MUST choose the Standardized Label term based on the one most frequently used by participants or the one that represents the idea most clearly.
    *   The AI MUST flatten all hierarchical groupings provided by participants into a single level, choosing either the broader or more detailed label depending on which fits the grouped cards best.
    *   The AI MUST strictly retain a copy of the original, unedited participant labels for reference.
*   **Group Analysis Rules:**
    *   The AI MUST identify "Consistent Groups" (groups where participants use the same label and include the exact same cards) to validate shared understanding.
    *   The AI MUST investigate "Diverse Groups" (groups where participants use the same label but include wildly different cards) to identify ambiguous category definitions.
    *   The AI MUST explicitly analyze "Other," "Miscellaneous," and "Don't Know" groups to identify content that is poorly labeled, poorly understood, or truly orphaned.
    *   The AI MUST value differences as highly as similarities; inconsistencies MUST be flagged as primary sources of insight.
*   **Card Placement Analysis Rules:**
    *   The AI MUST track every group a single card was placed into across all participants to define the multifaceted ways the content is perceived.
    *   The AI MUST NOT over-analyze single-card multi-groupings to assume a *single* user thinks the card belongs to all those groups simultaneously; it reflects the *aggregate* audience variance.
*   **Label and Terminology Rules:**
    *   The AI MUST analyze labels for "Similarities in terminology" to establish confident navigation labels.
    *   The AI MUST analyze labels for "Differences in terminology" (e.g., *Things to Do* vs. *Attractions*) to highlight conceptual synonyms.
    *   The AI MUST analyze labels for "Formality of language" (e.g., *Dining* vs. *Places to Eat*) to match the audience's natural tone.
*   **Accuracy and Anomaly Rules:**
    *   The AI MUST compare participant placements against the "Internal Correctness" of the content.
    *   When participants place cards "inaccurately," the AI MUST assess if the card title was ambiguous, if the participant misunderstood the domain, or if the category was used as a dumping ground.
    *   The AI MUST actively identify and correct obvious physical/data-entry mistakes (e.g., a clearly jumbled card drop that breaks all other established patterns for that user).
*   **Closed Card Sort Rules:**
    *   The AI MUST calculate the frequency of each card's placement into predefined categories.
    *   The AI MUST identify "Clumping"; if a category absorbs a disproportionate amount of content, the AI MUST flag it as potentially "too broad."
    *   The AI MUST identify cards placed evenly across multiple categories and flag them as having overlapping category definitions or ambiguous content.

@Workflow
1.  **Construct the Data Matrix:** Format the raw data into a grid. Assign cards to rows, participants to columns, and populate cells with the participant-generated group labels.
2.  **Standardize the Labels:**
    *   Extract all unique participant labels.
    *   Group highly similar concepts.
    *   Flatten any hierarchies into a single level.
    *   Select the dominant/clearest term as the Standardized Label.
    *   Map original labels to Standardized Labels while retaining the original data.
3.  **Execute Group Analysis:**
    *   Identify groups with high consensus (same label, same cards).
    *   Identify groups with high divergence (same label, different cards).
    *   Isolate and review all "Miscellaneous/Other" groups.
4.  **Execute Card Placement Analysis:**
    *   Iterate through each card.
    *   List all distinct groups the card was assigned to.
    *   Synthesize the perceived meaning of the card based on its distribution.
5.  **Evaluate Organizational Schemes and Terminology:**
    *   Determine the primary organizational scheme used by participants (e.g., topic, audience, task, chronology).
    *   Evaluate the formality and variance of the language used for labels.
6.  **Assess Accuracy and Synthesize Qualitative Data:**
    *   Compare groupings against the known internal correctness of the content.
    *   Diagnose reasons for "wrong" placements.
    *   Integrate facilitator observations, participant quotes, and spatial patterns into the final insights.
7.  **Closed Sort Execution (If Applicable):**
    *   Generate a Closed Card Sort Matrix (Categories on top, Cards on side).
    *   Count placement frequencies.
    *   Flag Clumping and highly distributed (overlapping) cards.

@Examples (Do's and Don'ts)

*   **Standardizing Labels**
    *   [DO]: Map "About Region", "The Region", and "About the Region" into a single Standardized Label: "About the Region".
    *   [DON'T]: Map "Things to Do" and "Accommodations" together into "Tourism" just to reduce the number of categories. They represent fundamentally different user concepts.

*   **Handling Hierarchies**
    *   [DO]: Flatten a participant's nested group "Dining -> Restaurants -> Fast Food" into a single-level label like "Restaurants" or "Dining" depending on the scope of the cards.
    *   [DON'T]: Maintain nested associative arrays in the data matrix, which prevents side-by-side exploratory comparison across participants.

*   **Analyzing Diverse Groups**
    *   [DO]: Notice that the group "Case Studies" contains 50 different cards across participants, and deduce that participants are using it as a "Miscellaneous" dumping ground for content they don't understand.
    *   [DON'T]: Assume that because 18 people created a group called "Case Studies", all cards placed inside it actually belong together.

*   **Interpreting "Wrong" Placements**
    *   [DO]: Treat a card systematically placed in the "wrong" departmental group as evidence that the organizational structure is opaque to users and the content title is ambiguous.
    *   [DON'T]: Discard data where a user grouped an item incorrectly under the assumption that the user simply made a mistake.

*   **Closed Card Sort Analysis**
    *   [DO]: Flag a category named "General Information" that receives 70% of all card placements as "Clumped" and recommend breaking it down into more specific sub-categories.
    *   [DON'T]: Accept a highly clumped distribution as a success simply because users found a place to put the cards.