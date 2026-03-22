@Domain
These rules trigger when the AI is tasked with designing, creating, structuring, formatting, or reviewing taxonomies, controlled vocabularies, or rule sets specifically intended for use with Automated Indexing, Auto-Categorization (Auto-Classification), Text Analytics, or Information Extraction systems. 

@Vocabulary
- **Automated Indexing**: The overarching term for any indexing performed by software rather than humans. Includes information extraction and auto-categorization.
- **Auto-Categorization (Auto-Classification/Auto-Tagging)**: Automatically associating appropriate taxonomy terms (categories) with a document by analyzing the text and comparing it against taxonomy data.
- **Information Extraction (Data Extraction)**: Using natural language processing (computational linguistics/pattern recognition) to pull specific, significant facts, names, or concepts from unstructured content.
- **Entity Extraction (Entity Recognition)**: A subset of information extraction focused specifically on identifying named entities (proper nouns like people, companies, locations).
- **Machine Learning-Based Auto-Categorization (Statistical Method/Catalog by Example)**: An auto-categorization method where the system ingests pre-indexed sample documents ("training documents") and uses algorithms (Bayesian computations, support vector machines, neural networks) to learn text patterns.
- **Training Documents**: Pre-indexed sample documents required to teach a machine-learning system which text patterns correspond to specific taxonomy terms.
- **Tuning**: The human-driven quality control process of adjusting training sets or manually overriding auto-generated keywords to improve machine-learning retrieval accuracy.
- **Rules-Based Auto-Categorization**: An auto-categorization method that relies on human-authored conditional statements (IF/THEN, Boolean logic, word proximity, regular expressions) mapped to each taxonomy term to identify text patterns.
- **Knowledge Base (Rule Set)**: The collection of rules governing a rules-based auto-categorization system.
- **Regular Expressions (Regex)**: Special text strings used in rules-based systems to describe complex search patterns.
- **Fuzzy Matching**: Matching text to taxonomy terms based on linguistic processing or statistical methods that ignore exact spelling, incorporating stemming or variations.
- **Statistical Clustering (Semantic Clustering)**: An automated taxonomy generation method that groups documents sharing words with similar meanings to suggest or build new taxonomy categories.
- **Weighting (Relevancy Ranking)**: The assignment of relative rankings/percentages to synonyms, keywords, or assigned index terms based on their significance to the document or rule.

@Objectives
- Optimize taxonomy terms, relationships, and rule sets for algorithmic text matching rather than human interpretation.
- Prioritize clear, distinct preferred terms over highly granular, subtle distinctions that software cannot reliably differentiate.
- Maximize the volume and variety of nonpreferred terms (synonyms, phrases, verbs) to ensure comprehensive automated string matching.
- Facilitate seamless integration with auto-categorization software (e.g., Data Harmony, SAS, Semaphore, PoolParty, Cogito) by structuring rules, weights, and training sets appropriately.
- Ensure high retrieval accuracy (precision and recall) by strictly controlling term ambiguity through Boolean rules, regex, and contextual text constraints.

@Guidelines

**1. Automated vs. Human Indexing Strategy**
- The AI MUST recommend automated indexing over human indexing when dealing with: vast volumes of documents, rapidly changing content (news), time-critical information, highly structured content types, uniform subject areas, and text-only content.
- The AI MUST recognize that automated indexing taxonomies require less conceptual depth but significantly more varied text-string matching components than human indexing taxonomies.

**2. Term Creation and Granularity**
- The AI MUST NOT create highly granular terms with subtle conceptual differences (e.g., separating "insurance companies," "insurance agents," and "insurance brokers"). Automated systems cannot reliably discern these nuances. Consolidate them into a single broader category unless distinct rules can definitively separate them.
- The AI MUST NOT create both an action term and a topic term sharing the same root within the same facet (e.g., "investing" and "investments" or "contracting" and "contracts"). Choose one to represent the concept.
- The AI MUST utilize **Precoordination** (e.g., "software training", "federal aid to education") rather than relying on postcoordination (e.g., "software" AND "training"). Phrase terms are significantly more effective for exact algorithmic matching.
- The AI MUST NOT use structured indexing subdivisions (second-level indexing). They are too complex for automated indexing systems to parse.
- The AI MUST include scope notes if the taxonomy is visible to end-users, even though there are no human indexers to read them.

**3. Nonpreferred Terms (Synonyms & Variants)**
- The AI MUST generate a vastly higher quantity of nonpreferred terms for automated indexing than for human indexing.
- The AI MUST include non-noun phrases and verbal phrases as nonpreferred terms (e.g., for preferred term "presidential candidates," include nonpreferred terms "campaigning for president," "running for president").
- The AI MUST NOT generate phrase-inverted nonpreferred terms (e.g., "photography, digital"). These exist only for human alphabetical browsing and are useless to an automated string-matching system.
- The AI MUST explicitly designate and separate acronyms from standard nonpreferred terms, and apply strict contextual rules to them to avoid severe ambiguity (e.g., "CDs" matching "compact discs" vs. "certificates of deposit").

**4. Term Relationships**
- The AI MUST fully build out standard hierarchical relationships (BT/NT), as they function identically in both human and automated indexing.
- The AI MUST minimize or omit associative relationships (Related Terms / RT) UNLESS the taxonomy will be displayed to end-users for browsing. Associative relationships provide no utility to the backend text-matching algorithm itself.

**5. Rules-Based System Configuration**
- When configuring rules for terms, the AI MUST use conditional logic to resolve ambiguity.
- The AI MUST use operators such as `IF`, `AND`, `OR`, `NOT`, and `MENTIONS` to restrict matches (e.g., `IF (MENTIONS "earthquakes") AND NOT (MENTIONS "sports")`).
- The AI MUST consider text constraints such as truncation, word proximity, initial capitalization, and sentence placement when writing rules.
- The AI MUST apply relative weightings to supporting keywords (e.g., keyword A gives 50% threshold, keyword B gives 20% threshold).

**6. Machine-Learning System Configuration**
- The AI MUST advise the collection of representative "training documents" for each taxonomy term to train statistical models (Bayesian, Support Vector, Neural Networks).
- The AI MUST outline a "Tuning" process: periodically reviewing automatically indexed documents, identifying false positives (noise) and false negatives (misses), and adjusting the training documents or term variants accordingly.

@Workflow
1. **Analyze Indexing Method**: Determine if the target system utilizes Machine Learning (Statistical), Rules-Based matching, Entity Extraction, or a Hybrid approach.
2. **Generate Preferred Terms**: Define concepts using precoordinated phrases. Consolidate terms that have overly subtle semantic differences.
3. **Populate Nonpreferred Terms Exhaustively**: Generate all possible text strings that could represent the concept in raw text. Include verb phrases and exact string matches. Strip out any phrase-inversions.
4. **Develop Concept Rules (If Rules-Based)**: 
   - Write explicit Boolean or Regex rules for ambiguous terms.
   - Assign numeric weights to synonyms if the software requires relevance threshold scoring.
5. **Establish Training Criteria (If Machine-Learning)**: 
   - Define the required volume and nature of training documents for the concepts. 
   - Establish tuning parameters for false positive/negative reviews.
6. **Structure Hierarchies**: Build BT/NT relationships for recursive retrieval, omitting RTs unless an end-user UI requires them.
7. **Format for Export**: Ensure the structure maps to standard automated software requirements (e.g., SKOS, OWL, or specific vendor formats like Data Harmony MAIstro or Semaphore Classification Server).

@Examples (Do's and Don'ts)

**Term Granularity**
- [DO]: Consolidate similar concepts: `Preferred Term: Insurance industry professionals` (capturing agents, brokers, underwriters in raw text).
- [DON'T]: Separate highly nuanced concepts: `Preferred Term 1: Insurance brokers`, `Preferred Term 2: Insurance agents` (Algorithms will struggle to differentiate these reliably without extreme rule constraints).

**Term Coordination**
- [DO]: Use precoordination: `Preferred Term: plastic motor vehicle parts`.
- [DON'T]: Rely on postcoordination: `Preferred Term 1: plastic parts`, `Preferred Term 2: motor vehicles` (This creates false positives when text mentions "plastic parts in toys and motor vehicles of steel").

**Nonpreferred Terms**
- [DO]: Include verb phrases: `Preferred Term: stock market crash` | `Nonpreferred: crashing stock market`, `market crashed`, `stocks crashed`.
- [DON'T]: Use phrase inversions: `Preferred Term: public libraries` | `Nonpreferred: libraries, public`.

**Handling Ambiguous Acronyms (Rules-Based)**
- [DO]: Write contextual rules.
  ```text
  IF (MENTIONS "CDs") AND (MENTIONS "interest rate" OR "bank")
  USE certificates of deposit
  ELSE IF (MENTIONS "CDs") AND (MENTIONS "music" OR "album")
  USE compact discs
  ```
- [DON'T]: Blindly assign "CDs" as a generic nonpreferred term for "compact discs" without contextual rules.

**Action vs. Topic Terms**
- [DO]: Choose one standard morphological form for a facet: `Preferred Term: investments`.
- [DON'T]: Include both `investments` and `investing` as separate preferred terms in the same facet, as statistical text analysis will hopelessly blur them.