@Domain
These rules MUST trigger when the AI is tasked with executing taxonomy data exchange, format conversions (e.g., XML, Zthes, RDF, OWL, SKOS), taxonomy maintenance and updating (merging, splitting, deleting terms), vocabulary integration, taxonomy merging, cross-vocabulary mapping, Linked Data configuration, or the development and localization of multilingual taxonomies.

@Vocabulary
- **Interoperability / Exchange**: The ability to export taxonomy data from one system and import it into another, retaining complex structures and relationships using standard formats (XML, Zthes, SKOS, OWL).
- **Zthes**: A legacy XML schema specific for semantic hierarchies of terms as described in ANSI/NISO Z39.19. Uses elements like `termId`, `termName`, and `relation`.
- **RDF (Resource Description Framework)**: A W3C framework utilizing classes, properties, and URIs to describe web resources; expressible in XML.
- **OWL (Web Ontology Language)**: A W3C semantic markup language with strong syntax and machine interpretability, designed specifically for publishing and sharing complex ontologies.
- **SKOS (Simple Knowledge Organization System)**: A W3C recommendation for representing taxonomies. Focuses on "Concepts" rather than "Terms," utilizing `prefLabel` (preferred) and `altLabel` (nonpreferred), and supports multilingual vocabularies inherently.
- **SKOS-XL**: An extension of SKOS that describes "lexical entities" to support added metadata for specific labels.
- **Integrating**: Combining separate, non-overlapping taxonomies on different subjects into a single master taxonomy for combined use.
- **Merging**: Combining two redundant taxonomies in the same subject area into one. Requires designating one as the "primary" (dominant) taxonomy and the other as the "merging" taxonomy.
- **Mapping**: Enabling one taxonomy to be used for another while retaining them as distinct (e.g., front-end vs. back-end). Employs term-by-term equivalence matching.
- **Indexing Taxonomy**: In a mapping relationship, the back-end taxonomy linked directly to the content (treated collectively as nonpreferred).
- **Retrieval Taxonomy**: In a mapping relationship, the front-end taxonomy exposed to the searcher's user interface (treated collectively as preferred).
- **Upward Posting (Generic Posting)**: A mapping practice where a narrower term in the Indexing Taxonomy is mapped to a broader term in the Retrieval Taxonomy.
- **Fuzzy Match**: Inexact matches evaluated during merging, based on punctuation, plural/singular forms, abbreviations, word order variations, or grammatical stemming.
- **Linked Data / Linked Open Data (LOD)**: Taxonomies utilizing URIs/HTTP URIs and RDF/SPARQL to create semantic links to external web content or other vocabularies (e.g., DBpedia).
- **Localization**: The translation of taxonomy content combined with region-specific adaptations (user interface, sorting algorithms, dates, currencies).

@Objectives
- Execute seamless, loss-less taxonomy interoperability using ISO 25964 and W3C standard schemas (specifically SKOS and OWL).
- Perform strict, standardized taxonomy maintenance based on user search logs and term usage statistics.
- Execute flawless taxonomy integration, merging, and mapping algorithms, respecting the distinct directionality and constraints of each operation.
- Implement robust multilingual taxonomies using precise bidirectional equivalence, avoiding asymmetrical mapping techniques.

@Guidelines
- **Taxonomy Formatting & Exporting**:
  - When exchanging taxonomy data, the AI MUST prioritize W3C standards (SKOS, OWL) or ISO 25964-compliant XML schemas.
  - When encountering legacy systems using Zthes, the AI MUST support the schema but strongly RECOMMEND migration to SKOS.
  - When formatting in SKOS, the AI MUST model the taxonomy using Concepts (`skos:Concept`), Preferred Labels (`skos:prefLabel`), and Alternate Labels (`skos:altLabel`), NOT traditional term structures.
- **Taxonomy Maintenance**:
  - When analyzing term usage data, the AI MUST flag "high-use" terms for potential splitting or the addition of narrower specific terms.
  - When analyzing term usage data, the AI MUST flag "low-use" terms for potential deletion, merging, or upward posting.
  - When merging obsolete terms into preferred terms, the AI MUST transfer all nonpreferred terms and scope notes of the obsolete term to the newly merged preferred term.
  - When creating new terms or splitting existing terms, the AI MUST flag associated legacy documents for retroactive indexing.
- **Taxonomy Integration**:
  - When integrating taxonomies (combining non-overlapping domains), the AI MUST identify structural differences, resolve missing metadata fields (e.g., categories, standard relationships), and ensure cross-file relational integrity.
- **Taxonomy Merging**:
  - When tasked with merging two redundant taxonomies, the AI MUST establish one as the "Primary Taxonomy" and the other as the "Merging Taxonomy."
  - The AI MUST automatically accept exact matches between a Merging Preferred term and a Primary Preferred or Nonpreferred term.
  - The AI MUST require human review for matches between two Nonpreferred terms or any Fuzzy Matches.
  - When a Fuzzy Match is evaluated, the AI MUST check for: hyphens/spacing, plurals/singulars, known abbreviations, word order inversions, added broad words (e.g., "services", "industry"), and grammatical stemming.
- **Taxonomy Mapping**:
  - When mapping taxonomies, the AI MUST map directionally: from the Indexing Taxonomy (source/content) TO the Retrieval Taxonomy (target/UI).
  - The AI MUST permit Upward Posting (many-to-one mapping) where narrower indexing terms map to a broader retrieval term.
  - The AI MUST evaluate phrase-within-phrase matches (e.g., "HDTV television sets" to "television sets") as potential Upward Posting mappings.
  - When mapping in SKOS, the AI MUST utilize specific mapping properties: `skos:closeMatch`, `skos:exactMatch`, `skos:broadMatch`, `skos:narrowerMatch`, and `skos:relatedMatch`.
- **Linked Data**:
  - When configuring Linked Data taxonomies, the AI MUST assign unique HTTP URIs to concepts and establish `skos:exactMatch` or similar alignments to external web vocabularies.
- **Multilingual Taxonomies**:
  - When creating a multilingual taxonomy, the AI MUST map concepts based on strict bidirectional equivalence.
  - The AI MUST NOT use Upward Posting (narrower-to-broader mapping) in multilingual taxonomies.
  - When using SKOS for multilingual taxonomies, the AI MUST assign multiple language tags to `prefLabel` and `altLabel` within the same concept entity rather than creating separate relational crosswalks.
  - The AI MUST verify that all UI elements, sorting methodologies, and character encodings undergo comprehensive Localization.

@Workflow
**Process 1: Taxonomy Merging Algorithm**
1. Identify and declare the Primary Taxonomy and the Merging Taxonomy.
2. Execute an automated comparison pass across all terms.
3. Automatically merge Exact Match (Pref to Pref): Take no further action.
4. Automatically merge Exact Match (Pref [Merging] to Nonpref [Primary]): Take no further action.
5. Flag for Review Exact Match (Pref [Primary] to Nonpref [Merging]): Prepare to convert the merging nonpreferred term into a new nonpreferred term in the Primary Taxonomy.
6. Flag for Review Exact Match (Nonpref to Nonpref): Prepare to add the merging term's preferred parent as a new nonpreferred term to the primary term's preferred parent.
7. Flag for Review Fuzzy Matches: Evaluate based on punctuation, plurals, abbreviations, word order, and stemming.
8. Consolidate all unmatched terms from the Merging Taxonomy and present them for hierarchical insertion into the Primary Taxonomy.

**Process 2: Cross-Vocabulary Mapping**
1. Identify the Indexing Taxonomy (back-end/content) and the Retrieval Taxonomy (front-end/UI).
2. Create a mapping table (Column A: Indexing Term, Column C: Retrieval Term, Column B: Match Status [ok, b (broader), n (no match)]).
3. Execute exact match algorithms.
4. Execute Upward Posting algorithms (evaluating if Indexing Term is a narrower concept or phrase containing the Retrieval Term).
5. Output the mapping table, flagging all inexact and Upward Posting matches for human verification.
6. Convert verified mappings to standard interoperable outputs (e.g., `skos:broadMatch` or `skos:exactMatch`).

**Process 3: SKOS Conversion & Linked Data Deployment**
1. Parse traditional thesaurus relationships (BT, NT, RT, UF).
2. Instantiate each entity as a `skos:Concept` with a unique HTTP URI.
3. Translate the preferred term to `skos:prefLabel` (specifying language tag, e.g., `@en`).
4. Translate nonpreferred terms (UF) to `skos:altLabel`.
5. Translate BT to `skos:broader`, NT to `skos:narrower`, and RT to `skos:related`.
6. Append external Linked Data alignments using `skos:exactMatch` pointing to external URIs (e.g., DBpedia).

@Examples (Do's and Don'ts)

**Principle: SKOS Format Conversion**
- [DO]: Model standard thesaurus concepts using semantic web URIs and labels.
  ```xml
  <skos:Concept rdf:about="http://example.com/taxonomy/galactic_clusters">
    <skos:prefLabel xml:lang="en">galactic clusters</skos:prefLabel>
    <skos:altLabel xml:lang="en">star clusters</skos:altLabel>
    <skos:broader rdf:resource="http://example.com/taxonomy/galaxies"/>
  </skos:Concept>
  ```
- [DON'T]: Use legacy XML tag structures without defined schemas or treat nonpreferred terms as standalone concepts.
  ```xml
  <term>
    <name>galactic clusters</name>
    <nonpreferred>star clusters</nonpreferred>
    <BT>galaxies</BT>
  </term>
  ```

**Principle: Taxonomy Merging (Term Resolution)**
- [DO]: When retiring an obsolete term ("automobiles") and merging it into a preferred term ("cars"), automatically migrate "autos" (a nonpreferred term of automobiles) to become a nonpreferred term of "cars".
- [DON'T]: Delete the obsolete term without rescuing and transferring its nonpreferred terms and scope notes to the new preferred term.

**Principle: Taxonomy Mapping (Upward Posting)**
- [DO]: In a mapping table, map the Indexing term "HDTV television sets" to the Retrieval term "television sets" and mark the match status as "b" (broader/upward posting).
- [DON'T]: Map the Indexing term "television sets" to the Retrieval term "HDTV television sets", as this maps broader to narrower, causing users to retrieve content missing the specific criteria they clicked on.

**Principle: Multilingual Taxonomies**
- [DO]: Map concepts strictly on bidirectional exact equivalences, and embed them within the same SKOS concept using language tags.
  ```xml
  <skos:prefLabel xml:lang="en">Low-protein diets</skos:prefLabel>
  <skos:prefLabel xml:lang="fr">Régime hypoprotéique</skos:prefLabel>
  ```
- [DON'T]: Use Upward Posting (narrower-to-broader) when translating or mapping between languages, as the retrieval dynamic changes depending on the native language of the searcher.