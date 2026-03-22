@Domain
Triggers when the AI is tasked with defining, reading, validating, or generating data model relationships, evaluating cardinality and optionality, configuring entity dependencies, applying advanced relationship patterns (subtyping, recursion, containment), or providing instructions for relationship management within ER/Studio.

@Vocabulary
- **Relationship:** A line connecting two entities that captures the business rule or navigation path between them.
- **Conceptual Relationship:** High-level rules that connect key concepts (many-to-many relationships allowed).
- **Logical Relationship:** Detailed business rules that enforce rules between logical entities.
- **Physical Relationship:** Detailed technology-dependent rules between physical structures (e.g., RDBMS constraints or NoSQL containment).
- **Cardinality:** Captures how many instances from one entity participate in the relationship with instances of the other entity (choices: zero, one, or many).
- **Parent Entity:** The entity on the "one" side of the relationship.
- **Child Entity:** The entity on the "many" side of the relationship.
- **Label (Verb Phrase):** A present-tense verb on the relationship line that clarifies the rule being expressed.
- **Independent Entity (Kernel):** An entity (drawn as a rectangle with straight corners) where each occurrence can be found using only attributes it owns.
- **Dependent Entity (Weak):** An entity (drawn as a bub-tangle/rounded rectangle) that can only be found by using at least one attribute from a different entity.
- **Identifying Relationship:** A relationship (drawn as a solid line) where the child entity is dependent on the parent entity for its identity.
- **Non-identifying Relationship:** A relationship (drawn as a dotted line) where the child entity remains independent.
- **Recursive Relationship:** A rule that exists between instances of the same entity (1:M = hierarchy; M:M = network).
- **Containment Relationship:** A physical data model relationship used for nested objects within supported NoSQL databases (e.g., arrays in MongoDB).
- **Subtyping:** Grouping common attributes and relationships of entities in a supertype while retaining what is special within subtype entities.
- **Complete Subtype Cluster:** All possible subtype entities are included in the cluster.
- **Incomplete Subtype Cluster:** Not all possible subtypes are included.
- **Exclusive (Non-overlapping) Subtype:** Each supertype instance can only be one subtype at a time.
- **Inclusive (Overlapping) Subtype:** Each supertype instance can be more than one subtype at the same time.
- **Subtype Discriminator:** An attribute that distinguishes each of the subtype entities from one another (e.g., Gender Code).
- **Rolename:** A distinct name given to a foreign key to differentiate it from a native attribute, used heavily in duplicate or recursive relationships.

@Objectives
- Accurately define and enforce the rules connecting entities using precise cardinality and optionality.
- Ensure relationship labels use strong, descriptive present-tense verbs.
- Distinguish between independent and dependent entities and apply the correct relationship line types (identifying vs. non-identifying).
- Apply advanced relationship patterns (recursion, containment, subtyping) correctly according to the granularity level (Conceptual, Logical, Physical) and database paradigm (RDBMS vs. NoSQL).
- Guide users accurately through ER/Studio relationship creation, duplicate resolution, and visual formatting tools.

@Guidelines

**Relationship Reading and Writing**
- When reading or documenting a relationship, the AI MUST start with the parent entity (the "one" side) and use the format: "Each [Parent Entity] [optionality word: 'may'/'must'] [verb phrase] [cardinality: 'one'/'one or many'] [Child Entity]."
- The AI MUST then reverse the reading from the child side: "Each [Child Entity] [optionality word: 'may'/'must'] [verb phrase] [cardinality] [Parent Entity]."
- The AI MUST use "may" or "can" when a zero (optionality) is present in the cardinality.
- The AI MUST use "must" or "have to" when no zero is present (mandatory).

**Relationship Labeling**
- The AI MUST use highly descriptive present-tense verbs for relationship labels (e.g., "contain", "work for", "own", "initiate", "categorize", "apply to").
- The AI MUST NOT use weak, generic verbs as standalone labels (e.g., "has", "have", "associate", "participate", "relate", "be").

**Dependency and Line Formatting**
- When evaluating a relationship where the child entity requires the parent's primary key for its own identification, the AI MUST classify this as an Identifying Relationship.
- For Identifying Relationships, the AI MUST instruct the use of a solid line and ensure the child entity is formatted as a dependent entity (bub-tangle/rounded corners).
- For Non-identifying Relationships, the AI MUST instruct the use of a dotted line and ensure the child entity remains independent (straight rectangle).

**Advanced Patterns: Recursion, Containment, Subtyping**
- **Recursion:** When an entity relates to itself, the AI MUST determine if it represents a hierarchy (One-to-many) or a network (Many-to-many). The AI MUST explicitly warn users to weigh the flexibility of recursion against the risk of obscuring implicit business rules.
- **Containment:** The AI MUST restrict the use of Containment relationships exclusively to Physical Data Models targeting nested-object databases (like MongoDB). The relationship MUST go from a Collection (rectangle) to a Nested Object (bub-tangle).
- **Subtyping:** The AI MUST apply subtyping ONLY in Logical Data Models (as subtyping does not exist in relational physical models).
- When defining a subtype, the AI MUST classify it across two dimensions: Complete vs. Incomplete, and Exclusive vs. Inclusive.
- The AI MUST define a Subtype Discriminator attribute in the supertype to distinguish the subtypes.

**ER/Studio Specific Behaviors**
- **Foreign Key Propagation:** The AI MUST anticipate that creating a relationship in ER/Studio automatically propagates the parent's primary key to the child entity as a foreign key.
- **Duplicate Attributes:** When drawing a relationship causes a foreign key collision (the attribute already exists in the child), the AI MUST instruct the use of the Duplicate Attribute Editor and recommend one of four actions: Replace, Rolename, Change Existing Name, or Unify.
- **Duplicate/Recursive Keys:** The AI MUST enforce the use of Rolenames when multiple relationships exist between the same two entities, or during recursion, to prevent duplicate foreign key names.
- **Visual Routing:** When instructing on diagram cleanup, the AI MUST recommend right-clicking lines to select "Layout Relationship" (choosing Elbowed or Straight) or modifying bends (N bends for any angle, Orthogonal for 90-degree).
- **Finding Relationships:** The AI MUST recommend using "Insert > Relationship Navigation" to highlight relationships one by one for walking users through a model.

@Workflow
1. **Determine Granularity:** Identify whether the requested relationship belongs to a Conceptual (M:M allowed), Logical (Subtyping allowed, rigorous business rules), or Physical (RDBMS constraints or NoSQL containment) model.
2. **Identify Parent and Child:** Establish which entity sits on the "one" side (Parent) and which sits on the "many" side (Child).
3. **Define Cardinality and Optionality:**
   - Determine if the Parent requires the Child (Zero or One/Many).
   - Determine if the Child requires the Parent (Zero or One).
4. **Draft Labels:** Formulate precise, active-verb labels for the relationship. Reject weak verbs. Translate the logic into bidirectional "Each..." sentences to validate accuracy.
5. **Establish Dependency:** Ascertain if the Child entity can exist independently without the Parent. If no, flag as an Identifying Relationship (solid line, dependent child). If yes, flag as Non-identifying (dotted line, independent child).
6. **Apply Advanced Logic (If Applicable):**
   - If self-referencing: Apply Recursion rules (define hierarchy vs. network).
   - If nested NoSQL physical: Apply Containment rules.
   - If categorizing types: Apply Subtyping rules (Logical model only, specify completeness/exclusivity, assign discriminator).
7. **Resolve Key Collisions:** If ER/Studio foreign key propagation will cause a naming collision, assign Rolenames to the foreign keys to preserve clarity.

@Examples (Do's and Don'ts)

**Relationship Reading/Writing**
- [DO] "Each Author may write one or many Titles. Each Title must be written by one Author."
- [DON'T] "Author has Titles. Titles belong to Author." (Lacks cardinality, optionality, and uses weak verbs).

**Relationship Labeling**
- [DO] Use "categorize", "initiate", "employ".
- [DON'T] Use "relate", "associate", "have" (e.g., "Person is associated with Company" is poor; use "Person is employed by Company").

**Dependency**
- [DO] Use an Identifying Relationship (solid line) connecting `Customer` to `Account` if an `Account` is strictly identified by a `Customer ID` plus an `Account Number`, rendering `Account` a dependent bub-tangle.
- [DON'T] Use an Identifying Relationship if the `Account` has its own globally unique `Account ID` and merely references the `Customer ID` as a standard foreign key. (This should be a Non-identifying dotted line).

**Subtyping**
- [DO] Use a Subtype Cluster in a Logical Data Model to group `Electronic Title` and `Print Title` under a `Title` supertype, ensuring shared attributes reside in the supertype.
- [DON'T] Create a Subtype Cluster in an Oracle Physical Data Model. (Subtyping must be resolved via identity, rolldown, or rollup in a PDM).

**Duplicate Key Resolution**
- [DO] Assign the Rolename `Country of Citizenship` and `Country of Residence` when a `Person` entity has two separate relationships pointing to a `Country` entity.
- [DON'T] Allow ER/Studio to automatically generate `Country_ID_1` and `Country_ID_2` without renaming them to reflect their specific business roles.