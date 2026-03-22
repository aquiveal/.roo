# @Domain

This rule file MUST be triggered when the AI is tasked with designing, auditing, or implementing information retrieval systems, content management systems (CMS), tagging infrastructures, database schemas, search engine configurations, faceted navigation interfaces, or structural metadata frameworks. It is applicable whenever user requests involve categorizing content, defining system taxonomies, building search synonyms, establishing naming conventions, or creating navigational labeling structures.

# @Vocabulary

- **Metadata:** Data providing information about one or more aspects of the data (e.g., creation, purpose, time, author, location, standards). Forms the basis for dynamic, distributed authoring and powerful navigation.
- **Controlled Vocabulary:** A defined subset of natural language used to describe content. Ranges from simple synonym rings to complex thesauri.
- **Synonym Ring:** A list of words defined as equivalent for the purposes of search retrieval (e.g., exploding a search for "blender" to include "food processor"). Increases recall.
- **Authority File:** A list of preferred terms or acceptable values. Functions as a synonym ring where one specific term is elevated as the standard identifier.
- **Classification Scheme (Taxonomy):** A hierarchical arrangement of preferred terms used as a frontend browsable interface or a backend tagging tool.
- **Thesaurus:** A controlled vocabulary that explicitly defines equivalence, hierarchical, and associative relationships between terms to improve retrieval.
- **Precision:** The relevance of documents within a given result set (quality). 
- **Recall:** The proportion of relevant documents retrieved compared to all relevant documents in the system (quantity).
- **Preferred Term (PT):** The accepted term, acceptable value, subject heading, or descriptor. The center of a semantic network.
- **Variant Term (VT):** Non-preferred or entry terms defined as equivalent or loosely synonymous to the PT.
- **Broader Term (BT):** The parent of the PT; one level higher in the hierarchy.
- **Narrower Term (NT):** The child of the PT; one level lower in the hierarchy.
- **Related Term (RT):** A term connected to the PT through an associative relationship (e.g., "See Also").
- **Use (U) / See:** Syntax directing the indexer or user from a VT to a PT (e.g., "Tilenol Use Tylenol").
- **Used For (UF):** Syntax indicating the reciprocal relationship, showing the full list of variants for a PT (e.g., "Tylenol UF Tilenol").
- **Scope Note (SN):** A specific type of definition used deliberately to restrict the meaning of a PT to rule out ambiguity.
- **Parenthetical Term Qualifier:** A clarifier appended to a homograph to disambiguate meaning (e.g., "Cells (biology)").
- **Polyhierarchy:** A classification structure where a term can be cross-listed in multiple categories simultaneously.
- **Faceted Classification:** An organizational system that describes objects along multiple independent dimensions (facets) rather than forcing them into a single top-down hierarchy.
- **Classic Thesaurus:** Used at both the point of indexing and the point of searching.
- **Indexing Thesaurus:** Used only at the point of indexing to structure the process and promote consistency.
- **Searching Thesaurus:** Leveraged at the point of searching to expand queries (e.g., mapping a keyword to a controlled vocabulary before executing against a full-text index).

# @Objectives

- Transform unstructured, ambiguous natural language into a highly structured, machine-readable semantic network.
- Balance the inverse relationship between Precision and Recall based on the specific information needs of the user.
- Eliminate "apples-to-oranges" search failures by mapping diverse user inputs (variants, misspellings, acronyms) to standardized Preferred Terms.
- Facilitate guided, multidimensional navigation by implementing Faceted Classification architectures instead of brittle, single-path hierarchies.
- Ensure cross-channel and cross-database compatibility by adhering to established conceptual guidelines (e.g., ANSI/NISO Z39.19) while adapting flexibly to modern digital environments.

# @Guidelines

- **Metadata Implementation:** 
  - The AI MUST define metadata at administrative (owner, date), descriptive (topic, audience), and structural (chunks, sections) levels.
  - The AI MUST NOT rely solely on physical placement (e.g., folders) for organization; rely on metadata to ask "How can I describe this?" instead of "Where do I put this?".
- **Vocabulary Control & Synonym Management:**
  - The AI MUST link common misspellings, abbreviations, and lexical variants as Variant Terms (VT) to a single Preferred Term (PT).
  - When expanding queries via Synonym Rings, the AI MUST mitigate the reduction in precision by ordering exact keyword matches at the top of search result lists.
- **Defining Preferred Terms (PTs):**
  - **Grammatical Form:** The AI MUST strongly default to using NOUNS for PTs. Verbs and adjectives should only be used when strictly necessary for task-oriented or faceted descriptions (e.g., Price, Color).
  - **Plurality:** The AI MUST use the plural form for "count nouns" (e.g., "cars", "maps") and the singular form for "conceptual nouns" (e.g., "biology", "math").
  - **Spelling Consistency:** The AI MUST select a defined authority (specific dictionary or house style) and rigorously apply it.
  - **Acronyms:** The AI MUST default to popular use. If an acronym (e.g., "IRS", "TV") is vastly more recognized than the full phrase, make the acronym the PT and the full phrase the VT.
  - **Disambiguation:** The AI MUST use Parenthetical Term Qualifiers for homographs (e.g., "Mercury (planet)" vs "Mercury (element)") and MUST write Scope Notes (SN) to deliberately restrict the meaning of a term.
- **Semantic Relationship Mapping:**
  - **Equivalence:** The AI MUST manage synonyms by funneling multiple VTs to one PT.
  - **Hierarchical:** The AI MUST strictly define parent-child relationships using one of three subtypes: Generic (class-species, e.g., Bird NT Magpie), Whole-part (e.g., Foot NT Big Toe), or Instance (e.g., Seas NT Mediterranean Sea).
  - **Associative:** The AI MUST define strongly implied semantic connections that fall outside equivalence or hierarchy (e.g., Action/Product: Eating RT Indigestion) to support cross-selling or serendipitous discovery.
- **Handling Complexity:**
  - **Term Specificity:** The AI MUST balance uniterms vs. compound terms based on system size. For large collections, use compound terms (e.g., "knowledge management software") to increase precision. For broad portals, split into simpler elements (e.g., "knowledge management" and "software").
  - **Polyhierarchy:** The AI MUST allow items to live in multiple hierarchical branches if they exhibit characteristics of multiple categories, avoiding the physical-world limitation of "one place for each item."
- **Faceted Navigation:**
  - The AI MUST reject attempts to build a single "pure" taxonomy for complex heterogeneous content.
  - The AI MUST define independent dimensions (e.g., Topic, Product, Document Type, Audience, Geography, Price) to allow users to mix and match filters dynamically.

# @Workflow

1. **Content and Vocabulary Auditing:** 
   - Analyze the target domain and existing content to identify natural language variances, misspellings, and search log behaviors. 
   - Determine if the system requires a Classic, Indexing, or Searching Thesaurus.
2. **Facet Definition:**
   - Instead of forcing a single tree structure, define the core attributes (facets) of the content (e.g., format, topic, audience).
3. **Term Extraction and Normalization:**
   - Extract candidate terms.
   - Convert task/action terms to nouns where possible.
   - Standardize plural/singular forms based on count vs. conceptual nouns.
   - Select Preferred Terms (PTs) based on user warrant (what users search for) or literary warrant (what exists in the documents).
4. **Relationship Modeling:**
   - Establish **Equivalence:** Map all acronyms, synonyms, and variants (VTs) to their PTs.
   - Establish **Hierarchy:** Connect PTs using BT (Broader) and NT (Narrower) relationships. Permit Polyhierarchy where logical.
   - Establish **Association:** Link related PTs (RTs) to support "See Also" contextual navigation.
5. **Disambiguation:**
   - Identify homographs. Apply Parenthetical Qualifiers.
   - Write Scope Notes (SN) for abstract or easily misunderstood terms.
6. **Integration:**
   - Structure the output into a database schema, JSON structure, or CMS taxonomy map that explicitly codes the BT, NT, RT, PT, and VT relationships.

# @Examples (Do's and Don'ts)

**[DO] Standardize term grammatical forms appropriately:**
```json
{
  "PT": "Automobiles",
  "Type": "Count Noun",
  "Form": "Plural"
},
{
  "PT": "Physics",
  "Type": "Conceptual Noun",
  "Form": "Singular"
}
```

**[DON'T] Mix verbs, adjectives, and singular/plural nouns arbitrarily:**
```json
{
  "Categories": ["Drive", "Car", "Physical", "Fast"]
}
```

**[DO] Use explicit semantic relationships for a Thesaurus mapping:**
```text
PT: Migraine
UF: Severe headache
UF: Migraine headache
BT: Headache
NT: Ophthalmic migraine
RT: Aspirin
SN: A recurrent, throbbing, usually unilateral headache, often accompanied by nausea and visual disturbances.
```

**[DON'T] Build flat synonym lists that lack hierarchy or definition:**
```text
Synonyms: Migraine, Headache, Aspirin, Head pain, Bad head
```

**[DO] Use Faceted Classification for complex datasets:**
```yaml
Facets:
  - Wine Type: [Red, White, Sparkling, Pink, Dessert]
  - Region: [Australia, California, France, Italy]
  - Year: [1990, 1999, 2000, 2015]
  - Price: [Cheap, Moderate, Expensive]
```

**[DON'T] Force multidimensional content into a rigid single hierarchy:**
```yaml
Hierarchy:
  - Red Wines
    - California Red Wines
      - 1990 California Red Wines
        - Cheap 1990 California Red Wines
```

**[DO] Disambiguate homographs using parenthetical qualifiers:**
```text
PT: Mercury (element)
PT: Mercury (planet)
PT: Mercury (Roman deity)
```

**[DON'T] Leave ambiguous terms undefined, relying on context alone:**
```text
PT: Mercury
```

**[DO] Establish Associative relationships for cross-discovery:**
```text
PT: Termite Control
RT: Pesticides
```

**[DON'T] Confuse Associative relationships with Hierarchical relationships:**
```text
PT: Termite Control
NT: Pesticides 
// (Pesticides are not a "child" of Termite Control; they are a related agent).
```