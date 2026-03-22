# @Domain
These rules are activated when the AI is tasked with designing, documenting, analyzing, or implementing data lineage, Extraction, Transformation, and Load (ETL) processes, source-to-target mappings, data movement rules, or utilizing ER/Studio's Data Lineage, Table Editor Lineage, Column Editor Lineage, and User-Defined Mapping (UDM) features.

# @Vocabulary
*   **Data Lineage**: The comprehensive documentation of data movement from a starting point (Point A) to an end point (Point B), including any intermediate steps or transformations.
*   **ETL**: Extraction, Transformation, and Load; the process of moving and cleansing data from operational source systems to target systems like data warehouses.
*   **Source**: The starting point for data lineage. Can be other data models, SQL files, flat files (e.g., XML, Excel), or databases (e.g., MongoDB, Access, Teradata, Oracle, DB2).
*   **Target**: The specific structures (entities/tables) on the current active model that are being loaded with data.
*   **Data Movement Rule**: A documented directive describing the generic type of change or action applied to source data prior to loading (e.g., Create, Update, Archive, Backup, Delete) and the text instructions for that action.
*   **Data Flow**: An encapsulated organizational object representing one complete mapping. It includes the specific sources, transformation objects, data streams, and targets.
*   **Transformation**: An intermediary object within a Data Flow that alters input columns to output columns. Common types include *Direct Map* and *Lookup*.
*   **Data Stream**: The directional line (connection) that maps a Source to a Transformation, or a Transformation to a Target.
*   **User-Defined Mapping (UDM)**: An informal, non-executable relationship built between any objects within the *same* ER/Studio file, strictly for communication or gap/overlap analysis.
*   **Universal Mapping**: An informal, non-executable relationship built between objects across *different* ER/Studio files.
*   **Table Level Lineage**: High-level lineage metadata captured at the entity/table level, such as sourcing frequency and last sourced timestamps.
*   **Column Level Lineage**: Granular transformation logic and source/target mapping captured specifically at the attribute/column level.

# @Objectives
*   Ensure all data movement is meticulously mapped using the rigid tripartite structure: Sources, Rules, and Data Flows.
*   Prevent direct point-to-point data mapping without the explicit use of Transformation objects and Data Streams.
*   Enforce the distinction between executable/formal Data Flows and informal User-Defined/Universal Mappings.
*   Guarantee that data transformations are documented down to the granular column/attribute level.
*   Simulate ER/Studio's strict metadata hierarchies when managing Data Movement Rules and Transformation bindings.

# @Guidelines

## Structural Requirements for Data Lineage
*   The AI MUST separate lineage architecture into exactly three primary components: `Sources`, `Data Movement Rules`, and `Data Flows`.
*   A `Data Flow` MUST NEVER directly connect a Source to a Target. The AI MUST enforce the sequence: `Source` -> `Data Stream` -> `Transformation` -> `Data Stream` -> `Target`.

## Source Definition Constraints
*   When defining a Data Source, the AI MUST explicitly categorize it as one of the following types: `Logical`, `Physical`, `Flat File`, or `Other`.
*   If the source is a database, the AI MUST prompt for or define `Connectivity Properties`.
*   When importing a new source, the AI MUST account for name collisions by specifying a resolution strategy (e.g., rename with suffix, update existing, or skip duplicate).

## Data Movement Rule Constraints
*   Every `Data Movement Rule` MUST include a strictly defined `Rule Type` (e.g., Create, Update, Archive, Backup) and descriptive `Rule Text` detailing the business logic or contingency plans.
*   Rules MUST be bound explicitly to object classes or specific objects using `Binding Information`.

## Transformation Object Constraints
*   Every `Transformation` MUST possess a Name and a Type (e.g., `Direct Map`, `Lookup`, `Unspecified`).
*   The AI MUST define transformations using four strict metadata categories:
    1.  **Columns**: Explicit lists of Input columns and Output columns.
    2.  **Definition**: A text description of the transformation and/or the actual execution code.
    3.  **Data Movement Rules**: The specific rules bound to this transformation, including any customized/actual values injected into the rule variables.
    4.  **Attachments**: Any bound external documentation (e.g., requirements docs).

## Granular Lineage Documentation
*   The AI MUST document operational metadata (e.g., how often data is sourced, when it was last sourced) at the Table/Entity level via the `Table Editor Lineage` concept.
*   The AI MUST map explicit attribute-to-attribute logic using the `Column Editor Lineage` concept for precise ETL developer instructions.

## Informal Mapping Constraints (UDM & Universal Mapping)
*   If a mapping is requested purely for gap analysis, overlap analysis, or communication, the AI MUST use `User-Defined Mappings` (same file) or `Universal Mappings` (cross-file).
*   The AI MUST explicitly state that UDMs and Universal Mappings will NEVER be forward-engineered into code.

# @Workflow
When tasked with creating or documenting a Data Lineage process, the AI MUST execute the following algorithmic steps:

1.  **Initialize Target and Scope**:
    *   Identify the target entities/tables within the current active model.
    *   Acknowledge that any UI simulation of creating new sources may clear the undo history buffer (ER/Studio standard warning).

2.  **Define Sources**:
    *   Identify Point A (origin data).
    *   Specify the Source type (`Logical`, `Physical`, `Flat File`, `Other`).
    *   Extract and list all relevant source entities and columns.

3.  **Define Data Movement Rules**:
    *   Determine the operational requirement (e.g., is this adding new records, updating existing ones, or archiving?).
    *   Create the generic rule, assign the `Rule Type`, and draft the `Rule Text`.

4.  **Construct the Data Flow**:
    *   Create a named `Data Flow` container.
    *   Instantiate the `Source` object and the `Target` object within the flow.
    *   Instantiate a `Transformation` object between them.
    *   Define the `Transformation Type` (Direct Map / Lookup).
    *   Create `Data Stream 1`: Source -> Transformation.
    *   Create `Data Stream 2`: Transformation -> Target.

5.  **Configure Granular Bindings**:
    *   Map the exact Input Columns from the Source to the Output Columns of the Target within the Transformation object.
    *   Bind the previously created `Data Movement Rule` to the Transformation.
    *   Document Table Level metadata (frequency of load).
    *   Document Column Level metadata (specific functional logic applied to the attribute).

6.  **Review against UDM Rules**:
    *   Verify if the request implies physical ETL generation or informal gap analysis. If informal, discard steps 2-5 and map via `Where Used... -> User-Defined Mapping`.

# @Examples (Do's and Don'ts)

## Data Flow Structure
*   **[DO]**: Structure a mapping explicitly through a Transformation object.
    ```markdown
    Data Flow: AuthorPopulation
    1. Source: Person_Model.Person (Columns: SSN, FName, LName)
    2. Data Stream: Person -> PersonToAuthorCreate (Transformation)
    3. Transformation: PersonToAuthorCreate
       - Type: Direct Map
       - Input: Person.FName, Person.LName
       - Output: Author.First_Name, Author.Last_Name
       - Rule Bound: "Create Rule - Insert if SSN not exists"
    4. Data Stream: PersonToAuthorCreate -> Local_Model.Author
    5. Target: Local_Model.Author
    ```
*   **[DON'T]**: Map a source directly to a target without a Transformation object.
    ```markdown
    Source: Person -> Target: Author (Invalid flow structure, missing Transformation and Streams)
    ```

## Data Movement Rule Definition
*   **[DO]**: Define reusable, specific Data Movement Rules with explicit types and textual conditions.
    ```markdown
    Rule Name: InsertNewAuthor
    Rule Type: Create
    Rule Text: "Evaluate incoming source SSN against target Tax ID. If no match exists, generate a new Author record. Do not update existing records."
    ```
*   **[DON'T]**: Create vague or typeless movement rules.
    ```markdown
    Rule: Move data from person to author so the tables match.
    ```

## Applying User-Defined Mappings (UDMs)
*   **[DO]**: Use UDMs strictly for documentation and gap analysis without assuming ETL execution.
    ```markdown
    Requirement: Show how the Legacy DB maps to our new Logical Model for stakeholder review.
    Action: Use User-Defined Mappings (UDM). Link Legacy.Client to Logical.Customer via the 'Where Used' mapping. Note: This will not generate ETL code.
    ```
*   **[DON'T]**: Use UDMs to instruct an ETL developer on how data is physically loaded.
    ```markdown
    Requirement: Create the ETL mapping for the nightly batch load.
    Action: I have created a User-Defined Mapping between Legacy and Target. (Incorrect: UDMs are informal. A Data Flow must be created for ETL documentation).
    ```