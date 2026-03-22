@Domain
Trigger these rules when the user requests the design, creation, extraction, evaluation, or formatting of taxonomy terms, controlled vocabularies, thesauri, synonym rings, or concept metadata. This includes tasks involving content audits for term extraction, standardizing term formats, resolving synonym conflicts, deciding on term precoordination, and structuring taxonomy node attributes and scope notes.

@Vocabulary
*   **Concept**: A thing, idea, or shared understanding of something; the combination of a preferred term and its nonpreferred terms.
*   **Term**: A label (word or phrase) for a concept. Also referred to as *Vocabulary term* or *Subject term*.
*   **Preferred Term**: The official, displayed word or phrase for a concept. Also referred to as *Descriptor*, *Subject descriptor*, *Authorized term*, or *Node name*.
*   **Nonpreferred Term**: Synonyms, variants, or equivalent words/phrases used as cross-references pointing to the preferred term.
*   **Candidate Term**: A temporary term entered into a taxonomy that requires further review and approval before it can be used for indexing.
*   **Term Record / Term Details**: The complete database record regarding a term, including its relationships, notes, categories, administrative information, and attributes.
*   **Synonym Ring / Synset**: A controlled vocabulary in which all synonyms are equal and none is designated as the preferred term (often used invisibly for search engines).
*   **Node**: A concept expressed within a hierarchical taxonomy.
*   **Individual / Instance**: A concept or specific named entity within an ontology or hierarchy.
*   **Precoordinated Term**: A single term that combines two or more concepts prior to indexing (e.g., "software testing" instead of "software" AND "testing").
*   **Postcoordination**: The process of combining multiple distinct terms at the search stage (e.g., Boolean searching).
*   **Scope Note (SN)**: A note attached to a term to clarify its usage context within the taxonomy, restrict/expand its application, or distinguish it from overlapping terms.
*   **Homograph**: Terms with identical spelling but different meanings (requires parenthetical qualifiers for disambiguation).
*   **Content Audit / Content Inventory**: The process of extracting potential concepts from source materials using spreadsheet matrices.

@Objectives
*   Accurately extract and identify valid concepts from source content while discarding trivial, out-of-scope, or insufficiently documented ideas.
*   Differentiate strictly between a "concept" (the idea) and a "term" (the label), ensuring every concept is assigned one optimal preferred term.
*   Format all terms in strict adherence to ANSI/NISO Z39.19 guidelines (proper noun phrasing, correct pluralization, and standardized capitalization).
*   Resolve synonym and near-synonym conflicts by prioritizing the language of the target user while maintaining systemic structural consistency.
*   Apply precoordination to complex concepts when postcoordination would cause search ambiguity or when the subject area demands deep specificity.
*   Enrich terms with structured attributes, administrative metadata, and concise scope notes that aid human indexers and end-users without providing redundant dictionary definitions.

@Guidelines

**Concept Identification and Evaluation**
*   The AI MUST extract potential concepts from high-value content locations: titles, section headings, abstracts, captions, menu labels, site maps, and lead paragraphs.
*   The AI MUST evaluate every extracted concept for inclusion based on four criteria: 
    1. Is it within the taxonomy's subject area scope?
    2. Is it important/likely to be looked up by a user?
    3. Is there enough information/content on the concept to justify its inclusion?
    4. Do users expect the concept to be covered?
*   If a concept fails any of the four criteria, the AI MUST exclude it or merge it into a broader term.

**Choosing the Preferred Term**
*   The AI MUST select a single preferred term for each concept and designate all other variations as nonpreferred terms.
*   When choosing between synonyms, the AI MUST prioritize the wording most likely to be looked up by the intended end-user.
*   Secondary criteria for preferred terms MUST be evaluated in this order: taxonomy scope/focus, enterprise vocabulary enforcement, academic/industry standards, style consistency (formal vs. informal), and content wording.
*   When dealing with near-synonyms (e.g., "books" vs "literature"), the AI MUST merge them (choose one as preferred, the other as nonpreferred) UNLESS the taxonomy is highly specialized and content volume justifies separating them into different facets.
*   The AI MUST pick one consistent morphological form (e.g., "contracts" vs "contracting") and maintain that style throughout the hierarchy.
*   The AI MUST NOT use ambiguous designations like *Categories*, *Subjects*, *Subject areas*, or *Topics* as structural element names internally if it creates confusion with the actual terms.

**Term Formatting (ANSI/NISO Z39.19)**
*   **Capitalization**: The AI MUST format terms using either all lowercase OR initial capitalization (Sentence case). The AI MUST NEVER use Title Case for generic terms (to avoid confusion with proper nouns).
*   **Length**: The AI MUST keep terms to 1-4 words unless it is a proper noun/named entity.
*   **Grammar**: The AI MUST formulate terms as nouns or noun phrases (adjective + noun). Verbal nouns (e.g., "teaching") are permitted. Verbs (e.g., "teach") are STRICTLY PROHIBITED. Adjectives standing alone are PROHIBITED unless they are values within a specific facet (e.g., colors).
*   **Plurality**: The AI MUST use plural forms for countable nouns (e.g., "hospitals"). The AI MUST use singular forms for abstract concepts, substances, collective nouns, and body parts (e.g., "healthcare", "water", "ear").
*   **Disambiguation**: The AI MUST use parenthetical qualifiers to distinguish homographs (e.g., "French (language)" and "French (people)"). The format (domain vs. category) of the qualifier MUST be consistent across the taxonomy.
*   **No Inversions**: The AI MUST NOT use inverted phrase formats for preferred terms (e.g., "loans, commercial"). Inversions are strictly reserved for nonpreferred terms in alphabetical browse lists.
*   **Acronyms**: The AI MUST use an acronym as the preferred term ONLY if it is more widely known than the spelled-out form AND is entirely unambiguous within the scope. Otherwise, the full spelled-out form MUST be the preferred term.

**Precoordinated Terms**
*   The AI MUST generate precoordinated terms (e.g., "Hispanic actors", "software testing") when:
    *   Postcoordination (Boolean search) would retrieve unreliable/ambiguous results (e.g., "Russia AND foreign policy" pulling articles about foreign policy *toward* Russia, rather than *Russian* foreign policy).
    *   The subject area is focused and highly granular.
    *   There is a significant volume of content specific to the combined concept.
*   The AI MUST NOT precoordinate terms if the taxonomy is strictly faceted (facets naturally rely on postcoordination).

**Notes and Attributes**
*   The AI MUST create Scope Notes (SN) to restrict or expand term application, distinguish overlapping terms, or provide usage advice.
*   The AI MUST NOT write Scope Notes as standard dictionary definitions, unless the subject is highly technical. Notes must be concise.
*   The AI MUST attach descriptive attributes to named entities (proper nouns), such as birth dates, NAICS codes, or geolocation data.
*   The AI MUST include administrative attributes for terms: unique identifiers, approval status (e.g., candidate vs. approved), and creation/modification tracking.

@Workflow
1.  **Content Audit & Concept Extraction**: Perform a content audit using a spreadsheet matrix. Use either Method A (unique row for each concept with a source column) or Method B (unique row for each source file with multiple concepts in subsequent columns).
2.  **Concept Validation**: Filter the extracted list. Discard concepts that are trivial, out-of-scope, or have insufficient content backing.
3.  **Preferred Term Selection**: For each surviving concept cluster, select the single best term based on user expectation, context, and standard consistency. Classify all remaining terms in the cluster as nonpreferred.
4.  **Term Formatting Application**: Apply ANSI/NISO Z39.19 formatting. Convert countables to plurals, abstracts/body parts to singular. Enforce lowercase or initial capitalization. Remove all inversions from preferred terms.
5.  **Precoordination Assessment**: Scan the term list for complex ideas. If an idea requires multiple words to prevent search ambiguity, merge them into a single precoordinated noun phrase.
6.  **Disambiguation & Scope Notes**: Identify homographs and apply parenthetical qualifiers. Draft concise scope notes for terms with overlapping meanings or specific indexing boundaries.
7.  **Attribute Assignment**: Assign structured administrative metadata (ID, Candidate/Approved status) and entity-specific attributes (coordinates, codes) to the final term records.

@Examples (Do's and Don'ts)

**Capitalization**
*   [DO]: `business services` OR `Business services`
*   [DON'T]: `Business Services` (Avoid Title Case to prevent confusion with proper nouns).

**Plurality (Countable vs. Abstract/Body Parts)**
*   [DO]: `hospitals` (Plural for countable noun).
*   [DON'T]: `hospital`
*   [DO]: `healthcare` (Singular for abstract concept).
*   [DON'T]: `healthcares`
*   [DO]: `ear` (Singular for body parts).
*   [DON'T]: `ears`

**Term Inversions**
*   [DO]: `commercial loans` (Standard natural language order).
*   [DON'T]: `loans, commercial` (Never use inversions for preferred terms).
*   [DO]: `elementary schools`
*   [DON'T]: `schools (elementary)` (Never use parentheses to mimic an inverted adjective).

**Disambiguation (Homographs)**
*   [DO]: `Saturn (planet)` AND `Saturn (mythology)`
*   [DON'T]: `Saturn` (When the context allows for ambiguity).

**Precoordination**
*   [DO]: `software testing` (Precoordinated to ensure exact matches for the specific discipline).
*   [DON'T]: Relying solely on `software` AND `testing` as separate postcoordinated terms, which might falsely retrieve documents about "using software to conduct educational testing".

**Scope Notes**
*   [DO]: "SN: Excludes devices for performing mathematical analysis." (Concise boundary definition).
*   [DON'T]: "SN: An analyzer is a machine or device that analyzes something, originating from the Greek..." (Unnecessary dictionary definition).

**Grammar**
*   [DO]: `teaching` (Verbal noun).
*   [DON'T]: `teach` (Verb).