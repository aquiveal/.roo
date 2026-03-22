# @Domain

These rules MUST trigger whenever the AI is requested to design, audit, structure, implement, or evaluate ANY knowledge organization system (KOS). This includes, but is not limited to, tasks involving taxonomies, controlled vocabularies, thesauri, synonym rings (synsets), authority files, metadata schemas, ontologies, faceted search configurations, or website navigational hierarchies.

# @Vocabulary

The AI MUST utilize the following precise mental model and terminology when conceptualizing and discussing knowledge organization systems:

*   **Taxonomy**: In the broad sense, any Knowledge Organization System (KOS) used to support information/content findability, discovery, and access. In the narrow sense, a hierarchical classification system of concepts.
*   **Knowledge Organization System (KOS)**: An umbrella term encompassing term lists (authority files, glossaries), classifications and categories (subject headings, taxonomies), and relationship lists (thesauri, ontologies).
*   **SKOS (Simple Knowledge Organization System)**: A World Wide Web Consortium (W3C) recommended framework for representing controlled vocabularies and knowledge organization systems in a machine-readable format.
*   **Controlled Vocabulary**: A restricted, rigorously managed list of words or terms for a specialized purpose (indexing, labeling, categorizing). Features a preferred vs. nonpreferred cross-reference system to ensure consistency and eliminate ambiguity.
*   **Synonym Ring (Synset)**: A specific type of controlled vocabulary where all synonyms for a concept are treated as equal (no preferred term is designated), typically utilized invisibly behind the scenes in search engine retrieval.
*   **Authority File**: A controlled vocabulary explicitly restricted to managing **Named Entities** (proper nouns such as people, organizations, geographic locations, and product names).
*   **Hierarchical Taxonomy**: A tree-structured controlled vocabulary consisting of nested categories where every term (except top/bottom levels) is connected to a broader term (parent) and narrower term (child).
*   **Polyhierarchy**: A structural condition within a hierarchical taxonomy where a single term is permitted to have multiple broader terms (parents).
*   **Alpha-Numeric Classification System**: Rigid, relatively unchanging systems (e.g., Dewey Decimal, NAICS, SIC) utilizing codes to put documents into a single physical or conceptual class.
*   **Thesaurus (Information Retrieval)**: A highly structured controlled vocabulary strictly governing equivalence (USE/UF), hierarchical (BT/NT), and associative (RT) relationships between terms.
*   **Ontology**: The most complex taxonomy type, defining a domain of knowledge through specific terms (individuals/instances), classes, attributes (properties), and user-defined, meaning-specific semantic relationships (e.g., *owns/belongs to*).
*   **Metadata**: Data about data. Divided into **Descriptive** (what a resource is about), **Structural** (features like pagination/size), and **Administrative** (management data like creation date/rights). Taxonomies serve primarily as Descriptive metadata.
*   **Controlled List**: A simple finite list of values (e.g., Yes/No, Small/Medium/Large, 50 US States) that does NOT require concept-naming decisions. Distinct from a Controlled Vocabulary.
*   **Facet**: A subset or aspect of information (e.g., People, Places, Document Type) used to create a faceted taxonomy for advanced, refined post-coordinate searching.
*   **Navigational Taxonomy**: A classification scheme specifically designed for website information architecture (site maps, navigation menus), optimizing user browsing rather than granular document indexing.

# @Objectives

*   The AI MUST enforce absolute consistency and ambiguity-resolution in the application of tags, index terms, and labels by strictly adhering to controlled vocabulary principles.
*   The AI MUST accurately select and construct the correct type of Knowledge Organization System (from simple synonym rings to complex ontologies) based on the precise business application (human indexing, automated search retrieval, or website navigation).
*   The AI MUST rigorously distinguish between descriptive metadata requiring a taxonomy and mere structural/administrative metadata requiring simple controlled lists.
*   The AI MUST adhere to established library science and information architecture standards (e.g., ANSI/NISO Z39.19, ISO 25964, W3C SKOS, RDF, OWL) when defining term relationships.

# @Guidelines

### 1. KOS Type Selection and Application
*   **Determine Taxonomy Purpose**: The AI MUST categorize the user's request into one of three primary applications:
    1.  *Indexing Support*: Demands a highly structured **Thesaurus** or **Authority File** with defined preferred/nonpreferred terms to guide human indexers.
    2.  *Retrieval Support*: Demands **Synonym Rings** (backend) or **Faceted Taxonomies** (frontend) to help users expand or narrow search results.
    3.  *Organization & Navigation*: Demands a shallower **Navigational Taxonomy** (Hierarchical) optimized for site maps and UI menus rather than granular document metadata.
*   **Alpha-Numeric Classification constraint**: The AI MUST NOT use Alpha-Numeric Classification systems (like NAICS or Dewey) for deep topical indexing of what a document is *about*. These MUST only be used to classify what class a document *belongs in* at a macro level.

### 2. Terminology and Vocabulary Control Rules
*   **Preferred vs. Nonpreferred**: In any system other than a Synonym Ring, the AI MUST explicitly designate one "Preferred Term" per concept and map all variations, misspellings, and synonyms as "Nonpreferred Terms" pointing to the preferred term via a *USE/UF (Used For)* relationship.
*   **Synonym Ring constraints**: When designing search-engine backend logic, the AI MUST use Synonym Rings where no term is preferred. The AI MUST link terms equally (e.g., applications = software = computer programs = tools).
*   **Authority File constraints**: When managing proper nouns (Named Entities), the AI MUST isolate them into an Authority File, formatting them consistently (e.g., handling abbreviations, spelling, entity types) without applying topical associative/hierarchical relationships.
*   **Controlled Vocabulary vs. Controlled List**: The AI MUST NOT classify simple, universally standardized finite lists (e.g., Days of the Week, Gender, 50 States) as Controlled Vocabularies. These MUST be treated as simple Metadata Controlled Lists.

### 3. Hierarchical Taxonomy Rules
*   **Tree Structure Construction**: The AI MUST build hierarchies top-down ("drill down"). Every term MUST have a parent (Broader Term) unless it is a top-level node, and a child (Narrower Term) unless it is a bottom-level leaf.
*   **Polyhierarchy evaluation**: The AI MUST explicitly query the user or determine system constraints before allowing a term to exist under multiple parents (Polyhierarchy).

### 4. Thesaurus Construction Rules
*   **Standardized Relationships**: When building a Thesaurus, the AI MUST map the following relationships explicitly:
    *   **BT (Broader Term)** / **NT (Narrower Term)**: Strict hierarchical relationships.
    *   **RT (Related Term)**: Associative relationships between terms that are mentally linked but not hierarchically dependent.
    *   **USE / UF (Used For)**: Equivalence relationships routing nonpreferred terms to preferred ones.
*   **Scope Notes**: The AI MUST append Scope Notes to terms that are potentially ambiguous to clarify precise usage for indexers.

### 5. Ontology Construction Rules
*   **Semantic Relationships**: The AI MUST NOT limit relationships to BT/NT/RT when building an Ontology. The AI MUST invent and document custom, semantic, domain-specific relationship pairs (e.g., *produces / is produced by*, *has members / is a member of*).
*   **Classes and Attributes**: The AI MUST assign explicit classes to terms and define structured attributes (properties, features, parameters) for the instances.
*   **Standards format**: The AI MUST output or structure Ontology logic using W3C Semantic Web recommendations such as RDF, OWL, or Topic Maps.

### 6. Metadata Integration Rules
*   **Descriptive Metadata Mapping**: The AI MUST map taxonomies exclusively to *Descriptive Metadata* fields (e.g., Subject, Topic, Descriptor).
*   **Schema Rule Definitions**: For every taxonomy-backed metadata field, the AI MUST define:
    1. Whether the field is required or optional.
    2. Whether it permits a single value or multiple values.
    3. Whether the taxonomy terms will be permanently attached to the content record (metadata) or dynamically matched "on the fly" (search execution).

### 7. Faceted Taxonomy Rules
*   **Facet Definition**: The AI MUST define facets as mutually exclusive attributes (e.g., Resource Type, Geography, Grade Level).
*   **Facet Implementation**: The AI MUST structure faceted taxonomies specifically to allow users to combine terms across different facets (Boolean AND searching) rather than forcing them down a single hierarchical tree.

# @Workflow

When requested to create, organize, or review a Knowledge Organization System, the AI MUST follow this rigid algorithmic process:

1.  **Requirement & Domain Analysis**
    *   Identify the exact nature of the content (e.g., proper nouns, e-commerce products, medical articles).
    *   Determine the intended application (Human Indexing, Automated Search, Website Navigation, Enterprise DB).
    *   Identify if the system requires standards compliance (ANSI/NISO Z39.19, ISO 25964, W3C SKOS, OWL).
2.  **KOS Type Selection**
    *   Select the precise KOS type: *Synonym Ring* (backend search), *Authority File* (Named Entities), *Hierarchical Taxonomy* (Navigation/Categorization), *Thesaurus* (Human Indexing), or *Ontology* (Semantic inference).
    *   Separate structural/administrative metadata fields (Controlled Lists) from descriptive metadata fields (Controlled Vocabularies).
3.  **Concept & Term Standardization**
    *   Extract concepts.
    *   Define the Preferred Term for each concept.
    *   Gather all synonyms, abbreviations, and acronyms as Nonpreferred terms.
4.  **Relationship Mapping**
    *   *If Thesaurus*: Map USE/UF for equivalence. Map BT/NT for hierarchy. Map RT for associative links. Add Scope Notes.
    *   *If Hierarchical Taxonomy*: Define parent/child nesting. Map Polyhierarchies if permitted.
    *   *If Ontology*: Define Classes, Attributes, and Custom Semantic Relationship pairs.
5.  **Architecture & Deployment Formatting**
    *   *If Faceted*: Break concepts into orthogonal, mutually exclusive facets.
    *   *If for Export/License*: Format the output schema accurately (e.g., CSV mapping, XML, SKOS, RDF/OWL).

# @Examples (Do's and Don'ts)

### 1. KOS Classification (Controlled Vocabularies vs. Controlled Lists)
*   **[DO]**: Treat a list of "Scientific Activity Types" as a Controlled Vocabulary (Taxonomy) because concepts require subjective naming decisions and mapping of synonyms.
*   **[DON'T]**: Treat a list of "The 50 US States" as a Controlled Vocabulary. It is a simple Metadata Controlled List because no concept-naming decisions are required.

### 2. Synonym Rings (Backend Search)
*   **[DO]**: Format a synonym ring as a flat, equal array for backend search parsing:
    `[ "Automobile", "Car", "Vehicle", "Auto" ]` (All terms trigger the same search result equally).
*   **[DON'T]**: Apply hierarchical preferred/nonpreferred logic to a synonym ring:
    `Automobile (Preferred) -> USE Car` (This defeats the purpose of a flat synonym ring).

### 3. Thesaurus Construction (Information Retrieval)
*   **[DO]**: Use strict relationship tagging to guide indexers and eliminate ambiguity:
    ```text
    Preferred Term: Neoplasms
    UF (Used For): Cancer
    UF (Used For): Tumors
    BT (Broader Term): Diseases
    NT (Narrower Term): Carcinoma
    RT (Related Term): Oncology
    Scope Note: Use for all general articles regarding malignant and benign tumors.
    ```
*   **[DON'T]**: Mix hierarchical and associative relationships loosely without explicit standardized tags, leaving the indexer guessing how terms relate.

### 4. Ontology Semantic Relationships
*   **[DO]**: Define explicit, domain-specific semantic relationships and properties:
    ```text
    Class: Organization
    Instance: "Acme Corp"
    Property: "Headquarters_Location" -> "New York"
    Semantic Relationship: [Acme Corp] <employs> [John Doe]
    Semantic Relationship: [John Doe] <is employed by> [Acme Corp]
    ```
*   **[DON'T]**: Use generic BT/NT/RT tags when building an Ontology, failing to capture the exact contextual meaning of the relationship (e.g., simply saying "Acme Corp" RT "John Doe").

### 5. Authority Files
*   **[DO]**: Isolate Named Entities into a specific Authority File without topical hierarchy:
    `Preferred Entity: International Business Machines`
    `UF: IBM`
*   **[DON'T]**: Mix Named Entities (like IBM) directly into a topical subject hierarchy (like "Computer Science") without utilizing an Authority File mechanism or instance-relationship rule.

### 6. Faceted Taxonomies
*   **[DO]**: Create mutually exclusive facets that allow a user to combine terms (e.g., searching for `Facet 1 [Resource Type: Video]` AND `Facet 2 [Ocean Environment: Deep Sea]`).
*   **[DON'T]**: Force orthogonal attributes into a single rigid hierarchy (e.g., forcing a user to click `Deep Sea -> Videos`, thereby hiding `Deep Sea -> Text Articles` in a completely different, un-filterable tree).