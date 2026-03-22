@Domain
Trigger these rules whenever the AI is tasked with processing, cleaning, analyzing, interpreting, or generating statistical algorithms for Information Architecture (IA) research, specifically quantitative user research, card-sorting datasets, cluster analysis, and audience comparison data. 

@Vocabulary
- **Statistical Analysis**: The use of mathematical algorithms to highlight consistent patterns and variations in large datasets, secondary to qualitative/exploratory analysis.
- **Control Parameters**: Specific variables chosen by the analyst that dictate how a statistical algorithm processes data (e.g., number of clusters, distance metrics).
- **K-Means Cluster Analysis**: A partitioning algorithm where the user pre-defines the number of groups (k), and the tool calculates the best assignment of objects to those groups by moving objects until a similarity threshold is met.
- **Hierarchical Cluster Analysis (HCA)**: A statistical method that builds a hierarchy of object relationships based on calculating the distance between pairs of objects and clustering the closest ones iteratively.
- **Euclidean Distance**: The primary and most common mathematical method used to calculate the distance/dissimilarity between objects in HCA and MDS.
- **Linkage**: The method by which distance between clusters is calculated in HCA.
  - *Single Linkage*: Distance based on the two closest objects in different clusters (often produces "chained" clusters).
  - *Complete Linkage*: Distance based on the greatest distance between any two objects in different clusters (produces compact clusters).
  - *Average Linkage*: Distance based on the average distance between all objects in the clusters (a compromise producing both chaining and compact traits).
- **Dendrogram**: A hierarchical tree diagram used to visually represent the output of HCA.
- **Multidimensional Scaling (MDS)**: A statistical visualization technique that plots objects on a 2D or 3D spatial map, positioning similar objects close together and dissimilar objects far apart.
- **Metric MDS**: The specific subset of MDS appropriate for measured distances, required for card-sorting dissimilarity matrices.
- **Dissimilarity Matrix**: A matrix calculating a mathematical value representing how far apart two objects are, used as the foundational input for MDS and HCA.

@Objectives
- To rigorously sanitize and format raw structural data so that it conforms strictly to the mathematical requirements of statistical algorithms.
- To execute statistical models (K-Means, HCA, MDS) not as definitive truth-generators, but as exploratory lenses to highlight consistency, variance, and outliers.
- To prevent the algorithmic stripping of human context by always correlating statistical outputs with qualitative insights.
- To systematically isolate and compare distinct user segments or sorting strategies to uncover fundamental audience differences.

@Guidelines

**Data Preparation Constraints**
- The AI MUST resolve "Other", "Miscellaneous", or "Don't Know" groupings by stripping the group and making each contained card an independent, separate entity. Do NOT treat these as valid conceptual clusters.
- The AI MUST truncate or shorten long item titles before passing data into visual statistical tools (like MDS or Dendrograms) to prevent unreadable output.
- The AI MUST flatten all hierarchical groupings provided by users into a single level (either by aggregating up to the broader group or splitting into smaller distinct groups). Statistical models reject nested hierarchies.
- The AI MUST evaluate the target software's constraints regarding discarded cards. If the software rejects missing variables, the AI must explicitly define a handling protocol for discards.
- The AI MUST resolve item duplication. If an item exists in multiple places for a single user, the AI must assign it to the one "best" location. Most statistical software fundamentally fails when processing duplicate objects.
- The AI MUST NEVER combine disparate demographic cohorts (e.g., business vs. personal consumers) into a single analytical batch. These must be analyzed as separate matrices to compare outcomes.
- The AI MUST NEVER combine distinctly different organizational schemes (e.g., users who sorted by genre vs. users who sorted by year). Analyze divergent schemes independently.

**Algorithmic Execution Constraints**
- **K-Means Constraints**: The AI MUST NEVER run K-Means only once. Because initial object assignment is randomized, the output changes every run. The AI MUST execute K-Means multiple times using varying values of `k` (derived from the raw data's minimum, maximum, and average group counts). 
- **K-Means Anti-Pattern**: The AI MUST NEVER use K-Means output to definitively dictate top-level navigation categories. It must only be used to evaluate if a specific number of clusters yields conceptually labelable groups.
- **HCA Constraints**: The AI MUST execute HCA multiple times using different linkage control parameters (Single, Complete, Average). The AI MUST compare the resulting dendrograms to identify which items are consistently paired regardless of linkage, and which are highly volatile.
- **MDS Constraints**: The AI MUST utilize *Metric* MDS (not nonmetric). The AI MUST run the spatial mapping multiple times to account for varied starting coordinates, using the output strictly to identify visual clusters and isolated outliers.

**Analytical Philosophy Constraints**
- The AI MUST recognize and document the fundamental flaw of Cluster Analysis: algorithms process *pairwise distances* (assuming item A is related to item B), whereas humans group by *conceptual themes* (item A and item B are both about Concept X). 
- The AI MUST document that statistical analysis combines all users into a unified average, explicitly noting that the resulting model likely does not reflect *any single individual's* actual mental model.
- The AI MUST use statistical consistency to build confidence in obvious categories, while explicitly highlighting statistical inconsistencies as areas requiring deeper qualitative investigation.

@Workflow

1. **Context and Data Auditing**
   - Assess the volume of the dataset. Confirm dataset is large enough to warrant statistical analysis (do not use statistics for sets <15 participants unless explicitly requested for justification purposes).
   - Identify demographic metadata. Split the dataset into isolated analytical batches based on user personas or drastically different sorting schemes.
2. **Data Sanitization**
   - Flatten all multi-level hierarchies into 1D arrays.
   - Force 1:1 card-to-category relationships (remove all duplicates based on highest qualitative affinity).
   - Explode "Miscellaneous/Other" categories into individual, ungrouped objects.
   - Generate short-codes for all long text labels.
3. **K-Means Iteration**
   - Calculate the Min, Max, and Mode of the total groups created by users.
   - Execute K-Means using `k = Mode`. Evaluate if the output clusters share a coherent, labelable theme.
   - Execute K-Means using `k = Min` and `k = Max`.
   - Document how cluster coherence degrades or tightens at different `k` values.
4. **Hierarchical Cluster Analysis (HCA)**
   - Generate a Euclidean dissimilarity matrix.
   - Process HCA using Single Linkage; output/log dendrogram data.
   - Process HCA using Complete Linkage; output/log dendrogram data.
   - Process HCA using Average Linkage; output/log dendrogram data.
   - Cross-reference outputs to define "Absolute Pairs" (items clustered at distance 0 across all linkages) and "Volatile Pairs".
5. **Multidimensional Scaling (MDS)**
   - Generate a Metric MDS 2D/3D spatial map from the dissimilarity matrix.
   - Run the algorithm 3 separate times to account for randomized initial coordinates.
   - Identify spatial overlaps (strong consensus) and extreme spatial isolation (outliers).
6. **Synthesis and Warning Application**
   - Combine statistical outputs with qualitative findings.
   - Output recommendations with an explicit disclaimer noting the limitations of pairwise algorithm logic against actual human contextual sorting.

@Examples (Do's and Don'ts)

**Handling Miscellaneous Categories**
- [DO]: Isolate "Misc". User A puts "Apple", "Car", and "Shoe" into a group called "Other". The AI sanitizes this by mapping "Apple -> Null", "Car -> Null", "Shoe -> Null" prior to generating the dissimilarity matrix.
- [DON'T]: Treat "Misc" as a valid conceptual link, creating a false statistical pairing that calculates "Apple" and "Car" as highly related because they share the "Other" bucket.

**HCA Execution**
- [DO]: Run HCA using Euclidean distance with Average Linkage to find a balanced dendrogram, then compare it against a Complete Linkage run to see if the compact clusters hold their shape.
- [DON'T]: Run HCA using only Single Linkage and accept the heavily "chained" outputs as the definitive structure of the user's mental model.

**K-Means Application**
- [DO]: Use K-Means to explore boundaries: "When running K-Means with 4 clusters, the groups are too broad to name accurately. When increased to 7 clusters, coherent concepts like 'Financial Policies' and 'HR Forms' emerge, indicating 7 is a more natural cognitive boundary."
- [DON'T]: "The K-Means algorithm was set to 6 clusters, therefore the optimal Global Navigation structure for the website must be exactly these 6 categories."

**Audience Comparison**
- [DO]: Create 'Matrix A' for European users and 'Matrix B' for North American users. Run MDS on both separately, and overlay the findings to highlight spatial differences in how the two demographics perceive specific content.
- [DON'T]: Dump all European and North American user data into a single dissimilarity matrix, allowing the opposing mental models to average each other out into a gray, unusable mathematical middle ground.

**Data Sanitization (Hierarchies and Duplicates)**
- [DO]: If a user placed "Tax Guide" under 'Finance -> Guidelines', the AI flattens the input to record "Tax Guide" solely under the group "Finance Guidelines" (or similar 1D equivalent).
- [DON'T]: Feed nested arrays (e.g., `{"Finance": {"Guidelines": ["Tax Guide"]}}`) into clustering algorithms designed for flat, mutually exclusive category assignments.