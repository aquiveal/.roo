# @Domain

These rules MUST trigger when the AI encounters tasks, files, or user requests involving the data modeling, database design, or architectural structuring of self-associating data, hierarchies, aggregations, bill of materials (BOM), organizational charts, peer-to-peer relationships, reporting drill-down/roll-up structures, or any scenario where a class of information relates to itself (recursive relationships).

# @Vocabulary

To ensure perfect alignment with the underlying data modeling methodology, the AI MUST strictly adhere to the following definitions:

*   **Recursive Relationship**: A semantic connection between objects of the same class. Also known as a self-referencing relationship, involuted relationship, or "pig's ear" relationship.
*   **Hierarchy**: An inverted tree structure with one or few things at the top and several things below. **Crucial characteristic**: Implies *ownership*. If the owning (top) object is destroyed, all child elements MUST be destroyed (cascading delete).
*   **Aggregation**: A total considered with reference to its constituent parts. **Crucial characteristic**: Does *not* imply ownership. If the owning element is destroyed, the constituent parts remain intact and are NOT destroyed.
*   **Peer-to-Peer Relationship**: A connection of persons, things, or ideas by a common factor at the same level. No owning element exists. Supports 1:1, 1:M, and M:M relationships.
*   **Level 1 Recursive Pattern**: A specific, rigid data model using distinct entities for each level of a hierarchy/aggregation (e.g., Country -> State -> City).
*   **Level 2 Recursive Pattern**: A generalized data model using a single entity with a 1:M self-referencing foreign key, coupled with a Type entity to label the levels.
*   **Level 2 Expanded Recursive Pattern**: A pattern utilizing an associative (intersection) entity to resolve Many-to-Many (M:M) recursive relationships.
*   **Level 3 Recursive Pattern**: A highly flexible pattern generalizing all recursive relationships into a single Entity Association structure classified by Association Types.
*   **Level 3 Recursive Pattern with Rules**: An enhancement to Level 3 that separates the *classification* of the relationship (Type) from the *behavior* of the relationship (Rule).

# @Objectives

*   The AI MUST accurately differentiate between Hierarchies, Aggregations, and Peer-to-Peer structures and apply the correct ownership and deletion logic to the data model.
*   The AI MUST select the appropriate level of generalization (Level 1, Level 2, Level 2 Expanded, Level 3, or Level 3 with Rules) based on the specific stability, complexity, and flexibility requirements of the prompt.
*   The AI MUST prevent data anomalies such as sum-aggregation discrepancies (e.g., counting hours at both project and task levels redundantly) when implementing rigid patterns.
*   The AI MUST design recursive structures that empower end-users to drill down, roll up, and perform multi-dimensional analysis effectively.

# @Guidelines

When modeling recursive relationships, the AI MUST adhere to the following granular rules and constraints:

### Differentiating Structural Types
*   **When designing a Hierarchy**: The AI MUST enforce cascading deletes in the database schema or document the strict ownership rules (e.g., deleting a University deletes its Schools and Departments).
*   **When designing an Aggregation**: The AI MUST NOT enforce cascading deletes (e.g., deleting the European Union does not delete France or Germany).
*   **When designing a Peer-to-Peer Relationship**: The AI MUST evaluate and document *transitive dependencies*. (e.g., If Task A must precede Task B, and Task B must precede Task C, does Task A precede Task C?). The AI MUST ensure peer-to-peer models support safe deletion without unintended cascading effects.

### Implementing the Level 1 Recursive Pattern
*   **Trigger**: Use when the hierarchy is static, well-defined, requires explicit business rules per level, and demands high understandability for non-technical stakeholders.
*   **Action**: The AI MUST create distinct entities for each level (e.g., `PROJECT`, `PHASE`, `TASK`).
*   **Action**: The AI MUST create strict 1:M relationships from the top entity down to the bottom entity.
*   **Constraint (Anti-Pattern)**: The AI MUST warn against capturing the same measurable attribute (e.g., `estimated_hours`) at multiple levels unless strictly required with distinct definitions. Otherwise, it causes sum-aggregation data anomalies. The AI MUST recommend deriving higher-level totals from the lowest granular entity.
*   **Constraint**: The AI MUST NOT use this pattern if M:M relationships are required or if the hierarchy levels are expected to change.

### Implementing the Level 2 Recursive Pattern
*   **Trigger**: Use when a flexible 1:M hierarchy is needed, allowing unlimited levels without changing the underlying schema, and all levels share similar attributes.
*   **Action**: The AI MUST create a single generalized entity (e.g., `WORK_EFFORT`).
*   **Action**: The AI MUST add an optional self-referencing foreign key (e.g., `parent_work_effort_id`) to support the 1:M hierarchy. *CRITICAL: This foreign key MUST be optional to support the top node of the hierarchy.*
*   **Action**: The AI MUST create an `ENTITY_TYPE` entity (e.g., `WORK_EFFORT_TYPE`) to label the instances (e.g., "Project", "Phase").
*   **Action**: The AI MUST implement a recursive relationship on the `ENTITY_TYPE` entity to define the allowable hierarchy of types (e.g., defining that "Phases" roll up to "Projects").
*   **Constraint**: The AI MUST NOT use this pattern if an instance requires multiple parents (M:M).

### Implementing the Level 2 Expanded Recursive Pattern
*   **Trigger**: Use when instances require multiple parents (M:M recursive relationships) or when peer-to-peer associations are needed.
*   **Action**: The AI MUST create an associative/intersection entity (e.g., `ENTITY_ASSOCIATION`) with two foreign keys pointing back to the base entity (e.g., `from_entity_id`, `to_entity_id`).
*   **Action**: The AI MUST create an `ENTITY_ASSOCIATION_TYPE` entity to classify the nature of the M:M relationship (e.g., "Precedent", "Concurrent").
*   **Constraint**: The AI MUST document that this pattern loses the ability to enforce strict 1:M cardinality constraints via the schema alone.

### Implementing the Level 3 Recursive Pattern
*   **Trigger**: Use in dynamic environments where all current and future types of recursive relationships (hierarchies, aggregations, peer-to-peer) must be handled by a single unified model.
*   **Action**: The AI MUST generalize all recursive relationships into a single `ENTITY_ASSOCIATION` entity.
*   **Action**: The AI MUST classify every association using an `ENTITY_ASSOCIATION_TYPE` entity.
*   **Action**: The AI MUST add a recursive relationship to the `ENTITY_ASSOCIATION_TYPE` entity to allow hierarchies of association types (e.g., "Precedent" is a child of "Dependency").
*   **Constraint**: The AI MUST warn the user that this high level of generalization obscures specific business rules and makes the model harder to read for non-technical users.

### Implementing the Level 3 Recursive Pattern with Rules
*   **Trigger**: Use when an enterprise is rule-driven and needs to explicitly separate *how* entities are structurally classified from *how* they behaviorally interact.
*   **Action**: The AI MUST implement the Level 3 pattern architecture.
*   **Action**: The AI MUST add an `ENTITY_ASSOCIATION_RULE` entity linked to the `ENTITY_ASSOCIATION` entity.
*   **Action**: The AI MUST populate the Rule entity with behavioral directives. Standard allowable rules include:
    *   *Substitution*: Entity A can replace Entity B.
    *   *Exclusion*: If Entity A exists, Entity B is disallowed.
    *   *Concurrent*: Entity A and Entity B must happen simultaneously.
    *   *Precedent*: Entity A must be completed before Entity B.
    *   *Complementary*: Entity A and Entity B mutually assist each other.
    *   *Implied*: Entity A implies the existence of Entity B.
    *   *Obsolescent*: Entity A has been superseded by Entity B.

# @Workflow

When prompted to design, refactor, or analyze a data model involving recursive or self-associating relationships, the AI MUST execute the following algorithmic steps:

1.  **Requirement Analysis**:
    *   Determine the exact nature of the relationship: Is it a Hierarchy (ownership/cascading delete), an Aggregation (no ownership), or Peer-to-Peer (same level)?
    *   Determine cardinality: Is it strictly 1:M, or does it require M:M (e.g., a part belonging to multiple assemblies)?
2.  **Pattern Selection**:
    *   If static, non-technical audience, strictly 1:M, and level-specific attributes exist -> Select **Level 1**.
    *   If dynamic levels, strictly 1:M, and attributes are shared -> Select **Level 2**.
    *   If M:M relationships or basic peer-to-peer are required -> Select **Level 2 Expanded**.
    *   If the environment is highly dynamic, unknown future relationship types exist, and a unified structure is needed -> Select **Level 3**.
    *   If behavioral constraints (Exclusion, Substitution) must be databased alongside the relationships -> Select **Level 3 with Rules**.
3.  **Entity & Relationship Generation**:
    *   Generate the tables/entities per the selected pattern constraints.
    *   Explicitly define Primary Keys (PK) and Foreign Keys (FK).
    *   When creating self-referencing FKs (e.g., `parent_id`), set them to *optional* (nullable) to support root nodes.
    *   When creating M:M associative entities, use `from_id` and `to_id` naming conventions rather than `parent/child` to semantically support peer-to-peer associations.
4.  **Anomaly Prevention & Validation Check**:
    *   Verify that quantifiable measures (amounts, hours, costs) are placed at the correct level of granularity to prevent sum-aggregation duplication.
    *   Document the deletion behavior (Cascade vs. Restrict/Set Null) based on the Hierarchy vs. Aggregation decision made in Step 1.

# @Examples (Do's and Don'ts)

### Level 1 Pattern
*   **[DO]**: Use distinct entities for a static organizational structure:
    `COUNTRY (country_id PK, name)` -> `STATE (state_id PK, country_id FK, name)` -> `CITY (city_id PK, state_id FK, name)`.
*   **[DON'T]**: Include a `total_population` attribute at the `COUNTRY`, `STATE`, and `CITY` levels simultaneously, as summing them up will result in triple-counting the population.

### Level 2 Pattern
*   **[DO]**: Use an optional self-referencing foreign key to allow root nodes.
    `WORK_EFFORT (work_effort_id PK, parent_work_effort_id FK NULL, name, work_effort_type_id FK)`.
*   **[DON'T]**: Make the `parent_work_effort_id` mandatory (NOT NULL). If it is mandatory, the top-most root node (e.g., the CEO, or the Master Project) cannot be inserted into the database.

### Level 2 Expanded Pattern (M:M)
*   **[DO]**: Use an associative entity to map parts to multiple assemblies (Bill of Materials).
    `PART (part_id PK, name)`
    `PART_ASSOCIATION (from_part_id FK, to_part_id FK, association_type_id FK)`
*   **[DON'T]**: Rely on a simple 1:M self-referencing key if a Sub-Assembly can be used in multiple different Finished Goods.

### Level 3 with Rules Pattern
*   **[DO]**: Separate the structural classification from the behavioral rule.
    *Association Type*: "Work Breakdown Structure"
    *Association Rule*: "Exclusion" (e.g., Task A cannot be performed if Task B is in the same breakdown).
*   **[DON'T]**: Conflate rules and types by creating a messy hybrid type like "Work Breakdown Exclusion Type". Keep structural taxonomies separate from behavioral logic.