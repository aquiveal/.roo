@Domain
Triggered when the AI is tasked with data modeling, database design, schema creation, ontology development, semantic web structuring, metadata record generation, Resource Description Framework (RDF) implementation, or vocabulary and taxonomy management. 

@Vocabulary
- **Data**: Potential information; raw, unprocessed stuff collected by instrumentation or machinery, analogous to potential energy requiring work to release its meaning.
- **Container Metaphor**: The concept that a metadata record is a "bottle" (container) for data, and the resource itself may also be a container for data (the "wine" or ideas). 
- **Subject Analysis**: The process of analyzing an object to identify its subject or what it is about, noting that aboutness is subjective and context-dependent.
- **Metadata**: A statement about a potentially informative object. (CRITICAL: Do NOT use the ambiguous definition "data about data").
- **Resource**: The "potentially informative object" about which a statement is being made.
- **Triple**: The three-part structure of a descriptive statement, consisting of Subject, Predicate, and Object.
- **Subject (Metadata Context)**: The entity or resource being described (Note: This is the exact opposite of grammatical syntax).
- **Object (Metadata Context)**: The entity being used to describe the Subject (Note: This is the exact opposite of grammatical syntax).
- **Predicate**: The category of relationship or connection between the Subject and the Object (e.g., "creator", "date").
- **Metadata Schema**: A set of rules defining what sorts of Subject-Predicate-Object statements (triples) are allowed and how they may be made.
- **Element**: A category of statement within a schema; the predicate that names an attribute of a resource (e.g., "Title").
- **Value**: The specific data assigned to an element to complete the statement.
- **Encoding Scheme**: A set of rules dictating how signifiers (values) are constructed. 
- **Syntax Encoding Scheme**: Rules dictating the structural format of a specific type of data (e.g., ISO 8601 for dates).
- **Controlled Vocabulary**: A finite, restricted set of allowable strings/terms used as values to describe a resource.
- **Authority File**: A highly restricted controlled vocabulary specific to names (people, places, things) dictating a single authoritative string for an entity.
- **Thesaurus**: A controlled vocabulary that adds hierarchical structure (parents, children, siblings) and relationship rules (IS A, narrower term, broader term, "use for" preferred terms).
- **Network (Graph)**: A set of entities connected by relationships, composed of **Nodes** (entities/Subjects/Objects) and **Edges** (relationships/Predicates).
- **Ontology**: A formal representation built on a thesaurus that includes a set of logical rules and inferences for action based on entity characteristics (e.g., If A is mother of B, A is female).
- **Uncontrolled Vocabulary (Tags)**: A bottom-up, grassroots approach allowing any term, including newly invented, idiosyncratic strings, to be used as a value.
- **Metadata Record**: A set of Subject-Predicate-Object statements about a single resource.
- **One-to-One Principle**: The foundational rule that there must be one and only one metadata record for a single resource, for a single metadata schema.
- **Internal Metadata**: Metadata embedded directly within the resource it describes (authoritative but static).
- **External Metadata**: Metadata stored separately from the resource it describes (flexible, customizable, but requiring linkage).
- **Unique Identifier**: A name or address (e.g., URI, URL, Call Number, ISBN) inherent in or assigned to an object that uniquely specifies one and only one object, essential for linking external records to resources.

@Objectives
- To design metadata systems and records that strictly treat metadata as formal statements about potentially informative objects, rejecting colloquial definitions.
- To map complex real-world objects into simplified, structured proxy representations (maps) to enable effective resource discovery.
- To rigorously enforce the One-to-One Principle to prevent conflation of derived or related resources.
- To differentiate and correctly apply syntax encoding, controlled vocabularies, thesauri, and ontologies based on the required level of control and hierarchy.
- To logically decouple resources from their metadata records when architecting external discovery systems, ensuring robust unique identifier linkage.

@Guidelines
- **Define Metadata Actionably**: The AI MUST NEVER conceptualize metadata simply as "data about data". The AI MUST treat metadata as an explicit declaration: "A statement about a potentially informative object."
- **Enforce Triple Structure**: The AI MUST structure all metadata statements as Triples (Subject-Predicate-Object). 
- **Invert Grammatical Logic**: When defining Triples, the AI MUST assign the Resource being described as the Subject, the attribute category as the Predicate (Element), and the descriptive data as the Object (Value). (e.g., Subject: Mona Lisa -> Predicate: Creator -> Object: Leonardo da Vinci).
- **Distinguish Elements and Values**: The AI MUST treat the Element as the blank on a form (the allowed category) and the Value as the data filling that blank.
- **Apply Syntax Encoding**: When a value represents structured data (like dates or times), the AI MUST apply a Syntax Encoding Scheme (e.g., ISO 8601 formatting: `2015-03-14T09:26:53`) rather than natural language strings.
- **Enforce Authority Files**: When generating metadata for proper names, the AI MUST utilize a single, authoritative string and reject pseudonyms or alternate spellings. The AI MUST implement "use for" relationships redirecting invalid names to the preferred term.
- **Build Thesauri with Hierarchy**: When creating a thesaurus, the AI MUST explicitly map parent-child-sibling structures and transitive asymmetric relations (e.g., X IS A Y. Y IS A Z. Therefore X IS A Z).
- **Elevate Thesauri to Ontologies**: To convert a thesaurus into an ontology, the AI MUST embed programmable rules/inferences for action (e.g., establishing default software behaviors based on a node's gender or classification).
- **Permit Idiosyncrasy in Uncontrolled Vocabularies**: When implementing tagging systems, the AI MUST NOT flag "weird" or highly idiosyncratic tags as errors. If an uncontrolled vocabulary is requested, the AI MUST allow infinite term generation.
- **Strictly Adhere to the One-to-One Principle**: The AI MUST NEVER merge descriptions of a physical object and a digital surrogate of that object into a single record. The AI MUST generate unique records for each iteration/format (e.g., Original Painting vs. High-Res Digital Scan) and link them using relational predicates (e.g., "Related Works" or "Relation").
- **Define Record Location Constraints**: 
  - The AI MUST use Internal Metadata when the requirement calls for authoritative, static data inherently tied to the file (e.g., HTML schema.org markup).
  - The AI MUST use External Metadata when the requirement calls for easily modifiable, customizable search databases (e.g., a library catalog).
- **Mandate Unique Identifiers for External Records**: If metadata is External, the AI MUST ensure a Unique Identifier (URI, DOI, Call Number) exists as internal metadata within the resource, so the external record has a definitive pointer to the object.

@Workflow
1. **Identify the Resource**: Define the exact boundaries of the "potentially informative object" (e.g., Is it the physical book, or the digital PDF of the book?).
2. **Assign Unique Identifiers**: Ensure the resource possesses a URI, DOI, or alternative unique identifier to serve as its network/database address.
3. **Establish the Schema & Elements**: Select the appropriate metadata schema and define the required Elements (Predicates) representing the resource's attributes.
4. **Formulate Triples**: Construct Subject-Predicate-Object statements, strictly placing the Resource as the Subject.
5. **Apply Encoding & Vocabularies**: 
   - Apply Syntax Encoding to strictly format dates, measurements, etc.
   - Apply Authority Files/Controlled Vocabularies to standardize names and subjects.
   - Map hierarchical relationships if building a Thesaurus, or programmatic inferences if building an Ontology.
6. **Enforce One-to-One Principle**: Audit the resource. If the resource is derived from another (e.g., a photo of a statue), create a separate metadata record for the derivative and link them via relation predicates.
7. **Deploy Record**: Embed the metadata record internally within the resource OR store it externally based on the system's mutability and authority requirements.

@Examples (Do's and Don'ts)

**Principle: Structuring the Triple (Grammar Inversion)**
- [DO]: Formulate the relationship as: Subject=[Resource being described: "Mona Lisa"] -> Predicate=[Element: "Creator"] -> Object=[Value: "Leonardo da Vinci"].
- [DON'T]: Formulate the relationship using standard sentence grammar: Subject=["Leonardo da Vinci"] -> Predicate=["Painted"] -> Object=["Mona Lisa"].

**Principle: The One-to-One Principle**
- [DO]: Create Record A for the physical 1851 print of "Moby Dick". Create a separate Record B for the 2015 EPUB version. Add a predicate "Relation: Derived From" in Record B pointing to Record A.
- [DON'T]: Create a single record for "Moby Dick" and list the format as "Physical Book, EPUB" under the same record.

**Principle: Syntax Encoding**
- [DO]: Apply strict ISO 8601 formatting for time-based metadata: `Date: 2015-03-14T09:26:53`.
- [DON'T]: Use natural language or localized syntax for time-based metadata: `Date: Pi Day 2015` or `Date: 3/14/15`.

**Principle: Authority Files & "Use For" relations**
- [DO]: Enforce the exact authorized string: `Twain, Mark, 1835-1910`. If a user inputs "Samuel Clemens", redirect using the rule: `Use For: Twain, Mark, 1835-1910`.
- [DON'T]: Allow "Samuel Clemens" and "Mark Twain" to exist as separate, disconnected entity values for the same person in a controlled database.

**Principle: External Metadata Linkage**
- [DO]: Create a database record (external metadata) that includes a URI or Call Number corresponding exactly to a physical/digital identifier attached directly to the resource (internal metadata).
- [DON'T]: Create a database record describing a resource's attributes without including a unique identifier that points to the actual location of the resource in physical or digital space.