# @Domain

These rules MUST be triggered whenever the AI is tasked with data modeling, database design, or requirements elicitation involving the identification, creation, modification, or organization of "Entities." This includes evaluating business concepts, structuring data at conceptual, logical, or physical levels, and generating or editing data models specifically using or referencing ER/Studio Data Architect principles.

# @Vocabulary

*   **Entity**: A collection of information about something the business deems important and worthy of capture. It MUST be identified by a noun or noun phrase and fit into one of six categories: who, what, when, where, why, or how.
*   **Entity Instance**: The occurrences or actual values of a particular entity (e.g., if the entity is "Customer", the instances are "Bob", "IBM", or "Walmart").
*   **Conceptual Entity**: A basic and critical business concept defined within a specific scope. It contains NO attributes.
*   **Logical Entity**: A detailed business representation of an entity containing properties (attributes) independent of any technology, hardware, or software.
*   **Physical Entity (Structure)**: A technology-specific representation of an entity (e.g., a database table in an RDBMS or a collection in a NoSQL database like MongoDB). It includes specific datatypes, lengths, and nullability constraints.
*   **Text Block**: A diagram object used to insert useful contextual information, such as examples of an entity, to add clarity and organization.
*   **Sticky Buttons**: An ER/Studio UI feature where a tool remains active for multiple clicks until explicitly deselected (via right-click), allowing rapid creation of multiple entities.
*   **Definition**: The explicit meaning of an entity, which can be forward-engineered into a database as a table comment.
*   **Note**: A secondary text field used for capturing non-definition text, such as questions for business experts, known issues, or action items.
*   **Universal Naming Utility**: An ER/Studio feature used to globally search and replace names, strings, and attachment value overrides across specific objects within models.
*   **Layout (Circular)**: An arrangement emphasizing group structures or dependencies by placing objects in circular patterns (ideal for star schemas or grouping subject areas).
*   **Layout (Hierarchical)**: A top-down arrangement based on the direction of relationships (ideal for logical dimensions).
*   **Layout (Orthogonal)**: A square-line, rectangular arrangement with minimal line crossing (ideal for highly normalized models).
*   **Layout (Symmetric)**: A symmetrical pattern centered on a single entity (ideal for star schemas).
*   **Layout (Tree)**: An arrangement featuring a root entity with parent-child sibling branches (ideal for hierarchies, taxonomies, and subtyping structures).

# @Objectives

*   Precisely classify every identified entity into one of the six fundamental business categories (who, what, when, where, why, how).
*   Strictly separate entity modeling into Conceptual, Logical, and Physical levels, ensuring no leakage of technical details into business models or vice versa.
*   Enforce absolute precision in entity naming using strictly nouns or noun phrases.
*   Utilize appropriate layout algorithms to visually communicate the underlying data architecture effectively based on the model's structure (normalized, dimensional, hierarchical).
*   Ensure all entities have complete metadata, distinctly separating formal definitions from project notes, issues, or questions.

# @Guidelines

*   **Entity Categorization**: Every entity proposed or analyzed MUST be categorized as:
    *   *Who*: Person or organization of interest (e.g., Employee, Patient, Customer).
    *   *What*: Product or service of interest (e.g., Product, Service, Course).
    *   *When*: Calendar or time interval of interest (e.g., Time, Month, Quarter).
    *   *Where*: Location of interest, physical or electronic (e.g., Mailing Address, IP Address).
    *   *Why*: Event or transaction keeping the business afloat (e.g., Order, Return, Claim).
    *   *How*: Documentation of the event (e.g., Invoice, Contract, Purchase Order).
*   **Naming Standards**: Entity names MUST be singular nouns or noun phrases. Never use verbs or adjectives without a noun.
*   **Level Enforcement**:
    *   *Conceptual Models*: The AI MUST NOT include attributes, datatypes, or technical constraints. Entities must represent only broad concepts.
    *   *Logical Models*: The AI MUST include business attributes but MUST NOT include database-specific datatypes (like VARCHAR), index constraints, or platform-specific nomenclature.
    *   *Physical Models*: The AI MUST map logical entities to specific structures (Tables for RDBMS, Collections for MongoDB/NoSQL) and include database-specific lengths, formats, and nullability (e.g., `NOT NULL`).
*   **Metadata Separation**: The AI MUST place the formal business description in the `Definition` field. Questions, issues, examples, and action items MUST be placed in the `Note` field.
*   **Clarity through Text Blocks**: When generating diagram descriptions or documentation, the AI MUST use or recommend "Text Blocks" to provide concrete instances/examples of entities to clarify abstract concepts.
*   **Layout Selection**: When recommending or organizing diagram layouts, the AI MUST adhere to these rules:
    *   Use *Orthogonal* for highly normalized relational models.
    *   Use *Tree* for subtyping, taxonomies, or complex parent-child hierarchies.
    *   Use *Circular* or *Symmetric* for Star Schemas or grouping large models by subject area clumps.
    *   Use *Hierarchical* for logical dimensions.
*   **Entity Duplication/Copying**: When simulating the copying of an entity, the AI MUST append `_1` to the original name (e.g., `Entity_1`, `Entity_2`) to prevent namespace collisions.
*   **Global Updates**: When tasked with renaming a pervasive concept across a model, the AI MUST simulate or recommend the use of the "Universal Naming Utility" to ensure the term is replaced in names, strings, and bound attachments globally.

# @Workflow

When tasked with generating, defining, or organizing entities for a data model, the AI MUST execute the following algorithmic sequence:

1.  **Scope Identification**: Determine if the request requires a Conceptual, Logical, or Physical data model.
2.  **Concept Extraction**: Extract nouns from the user's prompt or requirements.
3.  **Categorization & Validation**:
    *   Test each extracted noun against the six categories (Who, What, When, Where, Why, How).
    *   If a concept cannot fit into one of these categories, discard or redefine it until it fits.
4.  **Naming & Instantiation**: Ensure the entity name is a singular noun/noun phrase. Mentally generate 2-3 "Entity Instances" to verify the entity represents a valid collection (e.g., if Entity is "Language", instances are "Japanese", "Spanish").
5.  **Level Application**:
    *   If *Conceptual*: Output only the Entity Name and Definition.
    *   If *Logical*: Add business attributes.
    *   If *Physical*: Translate the entity into a Table/Collection, add specific datatypes, and set nullability rules.
6.  **Metadata Generation**:
    *   Write a strict, clear `Definition`.
    *   Write any pending questions or assumptions in a `Note`.
7.  **Layout Recommendation**: Recommend the specific layout pattern (Orthogonal, Tree, Circular, Hierarchical, Symmetric) that best fits the generated model's architecture.

# @Examples (Do's and Don'ts)

**Entity Naming and Categorization**
*   [DO]: Name an entity "Electronic Title" (Noun Phrase). Categorize as "What".
*   [DON'T]: Name an entity "Downloadable" (Adjective) or "Buy Book" (Verb).

**Conceptual vs. Physical Separation**
*   [DO]: In a Conceptual Data Model, output: `[Entity: Author] -> Definition: The person or organization that writes a title.`
*   [DON'T]: In a Conceptual Data Model, output: `[Entity: Author] -> Attributes: Author_ID (INT, NOT NULL), Last_Name (VARCHAR 50).` (This violates Conceptual level rules by including physical attributes and datatypes).

**Metadata Separation (Definitions vs. Notes)**
*   [DO]:
    *   `Definition`: "A forum for getting speakers and attendees together for discussing a topic of interest."
    *   `Note`: "Issue: Do we need to track virtual vs. physical conferences? Ask the business expert."
*   [DON'T]:
    *   `Definition`: "A forum for getting speakers together. Do we need to track virtual conferences here?" (Violates rule: Do not mix action items/questions into the formal definition).

**Layout Recommendations**
*   [DO]: "Since this is a highly normalized logical data model, I recommend applying the **Orthogonal layout** to ensure horizontal and vertical line routing with minimal crossing."
*   [DON'T]: "I recommend placing the entities randomly on the screen." (Violates the requirement to use ER/Studio's predefined layout algorithms).

**Entity Copying**
*   [DO]: "To create a duplicate of the `Category` entity for your submodel, copy it and name the new object `Category_1`."
*   [DON'T]: "Copy the `Category` entity and name it `Category_Copy` or `Category_Final`." (Violates ER/Studio standard naming convention for copied objects).