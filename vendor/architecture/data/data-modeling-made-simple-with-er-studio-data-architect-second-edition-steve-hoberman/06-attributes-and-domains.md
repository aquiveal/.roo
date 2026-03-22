# @Domain
These rules MUST trigger whenever the AI is tasked with data modeling, database design, defining data schemas, creating or analyzing entity-relationship diagrams (ERDs), assigning datatypes, defining validation rules/constraints, resolving database keys (Primary, Foreign, Alternate, Surrogate), or configuring metadata for ER/Studio Data Architect.

# @Vocabulary
*   **Attribute**: An elementary piece of information of importance to the business that identifies, describes, or measures instances of an entity. Analogous to column headings in a spreadsheet.
*   **Conceptual Attribute**: A property that is both basic and critical to the business at a universal or industry level (e.g., Phone Number).
*   **Logical Attribute**: A business property representing a solution independent of technology (software/hardware).
*   **Physical Attribute**: A database-specific representation of a logical attribute (e.g., a column in an RDBMS or a field in a NoSQL document).
*   **Key**: One or more attributes whose purposes include enforcing rules, efficiently retrieving data, and allowing navigation from one entity to another.
*   **Candidate Key**: One or more attributes that uniquely identify an entity instance. Must be Unique, Mandatory (not null), Non-volatile (never changes), and Minimal (only necessary attributes included).
*   **Composite Key**: A key composed of more than one attribute.
*   **Primary Key (PK)**: The single candidate key chosen to be the unique identifier for an entity.
*   **Alternate Key (AK)**: A candidate key that is unique but was not chosen as the primary key.
*   **Surrogate Key**: A system-generated unique identifier (often a counter) with no embedded intelligence/business meaning. Used for efficiency and integration.
*   **Natural Key**: The business-recognized way to uniquely identify an entity.
*   **Foreign Key (FK)**: One or more attributes that provide a link/navigation path to another entity.
*   **Rolename**: An alias or specific name given to a foreign key to differentiate it from its primary key, especially when multiple relationships exist between the same entities.
*   **Inversion Entry (IE)**: A non-unique index (or secondary key) created to allow rapid data retrieval for frequently queried attributes.
*   **Domain**: The complete set of all possible validation criteria and values that an attribute can be assigned. Promotes reusability and standardization.
*   **Format Domain**: Specifies the standard data type (e.g., Integer, Character(30), Date).
*   **List Domain**: A finite, drop-down style set of allowed values (e.g., {Open, Shipped, Closed}).
*   **Range Domain**: All values permitted between a minimum and maximum boundary.
*   **Identity Property**: A physical setting for surrogate keys defining a starting number (Seed) and an amount to add for each new instance (Increment).

# @Objectives
*   Ensure every data model accurately translates abstract business properties into strictly defined, validated attributes.
*   Enforce absolute precision in key selection, prioritizing succinctness and data privacy while rigorously maintaining referential integrity.
*   Standardize attribute characteristics globally across all data models by mandating the use of Domains (Format, List, Range) to prevent data anomalies.
*   Replicate the ER/Studio architectural mindset by rigidly separating Logical data definitions (business rules) from Physical data definitions (database implementation details).

# @Guidelines

## Attribute Definition & Management
*   The AI MUST ensure every attribute clearly identifies, describes, or measures the entity it belongs to.
*   The AI MUST differentiate between Logical Attribute Names (business-friendly, e.g., `Author Last Name`) and Physical Column Names (database-friendly, e.g., `AUTH_LAST_NM`).
*   The AI MUST explicitly define the nullability of every attribute (`Allow Nulls? Yes/No`).
*   The AI MUST utilize the `Logical Only` flag for attributes that are necessary for business requirements but should not be generated in the physical database schema.

## Key Identification & Selection Rules
*   **Candidate Key Validation**: Before designating any Primary Key, the AI MUST explicitly evaluate potential Candidate Keys against four rules:
    1.  *Unique*: Must not identify more than one instance.
    2.  *Mandatory*: Must never be null.
    3.  *Non-volatile*: Value must never change once created.
    4.  *Minimal*: Must contain only the exact number of attributes needed for uniqueness.
*   **Primary Key Selection Criteria**: When multiple Candidate Keys exist, the AI MUST select the Primary Key based on:
    *   *Succinctness*: Choose the key with the fewest attributes or shortest data length.
    *   *Privacy*: The Primary Key MUST NOT contain sensitive data (e.g., Social Security Numbers, Tax IDs), because the PK will propagate as a Foreign Key to other tables, creating a massive security risk.
*   **Surrogate vs. Natural Keys**: If no natural candidate key meets the Succinctness and Privacy criteria, the AI MUST create a Surrogate Key (e.g., an Identity Column with a specified Seed and Increment). The original Natural Key MUST then be designated as an Alternate Key (AK).
*   **Foreign Key Configuration**: The AI MUST automatically propagate the parent's Primary Key to the child entity as a Foreign Key. If the FK name causes a naming collision or requires business clarity, the AI MUST assign a Logical Rolename and synchronize it with the Physical Column Rolename.
*   **Partial Keys / Hiding**: The AI MUST strictly AVOID using the "Hide Key Attribute" (partial key propagation) feature unless explicitly commanded by the user, as it degrades database integrity.
*   **Inversion Entries (IE)**: The AI MUST define Inversion Entries (non-unique indexes) for attributes that are known to be heavily queried (e.g., `Last Name`, `Status`).

## Domain Enforcement
*   The AI MUST NOT leave an attribute without a defined Domain.
*   The AI MUST classify every domain into one of three types:
    1.  *Format Domain* (e.g., `Date`, `Decimal(15,2)`).
    2.  *List Domain* (e.g., `GenderCode: {M, F}`).
    3.  *Range Domain* (e.g., `DeliveryDate: > Today`).
*   The AI MUST bind attributes to these Domains to ensure data quality checks occur before data insertion.

## ER/Studio-Specific Tool Behaviors
*   **Display Order**: When listing attributes, the AI MUST mimic ER/Studio's `Attribute (Logical Order)` mode, always listing Primary Keys at the top of the entity, followed by Alternate Keys, Foreign Keys, and non-key attributes.
*   **Universal Naming Utility**: When renaming an attribute or concept globally, the AI MUST systematically apply the change across all foreign key references, indexes, and bound attachments, mirroring the behavior of the Universal Naming Utility.
*   **Data Lineage Mapping**: If documenting data movement, the AI MUST specify Source-to-Target mapping at the attribute level, including Data Movement Rules (e.g., lookup, direct map).

# @Workflow
When instructed to define attributes, domains, and keys for a specific entity or data model, the AI MUST execute the following algorithmic process:

1.  **Attribute Elicitation**: Analyze the business entity and list all elementary pieces of information required. Assign business-friendly Logical Names and system-friendly Physical Column Names.
2.  **Domain Assignment**: Create or assign a Domain (Format, List, or Range) to every single attribute. Define Datatype, Length, Scale, and Nullability.
3.  **Candidate Key Discovery**: Scan the attribute list for unique identifiers. Validate each against the Unique, Mandatory, Non-volatile, and Minimal rules.
4.  **Key Designation**:
    *   Select the most succinct, non-sensitive Candidate Key as the Primary Key (PK).
    *   If no Candidate Key is secure or efficient, generate a Surrogate Key (Identity counter) to act as the PK.
    *   Mark all unselected Candidate Keys as Alternate Keys (AK1, AK2, etc.).
5.  **Index Optimization**: Identify attributes frequently used in searches/sorting and designate them as Inversion Entries (IE1, IE2, etc.).
6.  **Referential Integrity**: Map incoming Foreign Keys (FK). Assign Rolenames if the FK represents a specific relationship (e.g., `Billing_Address_ID` vs `Shipping_Address_ID`).
7.  **Documentation**: Generate definitions for every attribute, explicitly noting its domain restrictions and key status.

# @Examples (Do's and Don'ts)

## Primary Key Selection (Privacy & Succinctness)
*   **[DO]**
    ```markdown
    Entity: Employee
    - Employee_ID (PK, Surrogate Key, Domain: Integer Format, Identity Seed: 1, Increment: 1)
    - Social_Security_Number (AK1, Natural Key, Domain: SSN Format)
    - Employee_Last_Name (IE1, Domain: Name Format)
    ```
*   **[DON'T]**
    ```markdown
    Entity: Employee
    - Social_Security_Number (PK)  <!-- ANTI-PATTERN: Violates privacy rule; propagates sensitive data to child tables. -->
    - Employee_First_Name + Employee_Last_Name + Employee_Birth_Date (PK) <!-- ANTI-PATTERN: Violates succinctness; composite key is too large and inefficient. -->
    ```

## Domain Assignment
*   **[DO]**
    ```markdown
    Attribute: Order_Status_Code
    Domain Type: List Domain
    Datatype: CHAR(1)
    Nullability: NOT NULL
    Allowed Values: {O: Open, S: Shipped, C: Closed}
    Default Value: 'O'
    ```
*   **[DON'T]**
    ```markdown
    Attribute: Order_Status_Code
    Datatype: VARCHAR(50) <!-- ANTI-PATTERN: Lacks a restrictive List Domain, allowing invalid data entries like 'Pending', 'X', or 'NULL'. -->
    ```

## Foreign Key Rolenaming
*   **[DO]**
    ```markdown
    Entity: Flight
    - Flight_Number (PK)
    - Departure_Airport_Code (FK, Rolename mapped from Airport.Airport_Code)
    - Arrival_Airport_Code (FK, Rolename mapped from Airport.Airport_Code)
    ```
*   **[DON'T]**
    ```markdown
    Entity: Flight
    - Flight_Number (PK)
    - Airport_Code (FK)
    - Airport_Code_1 (FK) <!-- ANTI-PATTERN: Fails to use Logical Rolenames, creating ambiguity about which FK is departure vs arrival. -->
    ```

## Key Characteristics (Volatility)
*   **[DO]**
    ```markdown
    Candidate Key Evaluation for 'Class':
    - Class_Full_Name: Valid AK. Unique, Mandatory, Minimal, Non-volatile.
    ```
*   **[DON'T]**
    ```markdown
    Candidate Key Evaluation for 'Class':
    - Class_Description_Text: (PK) <!-- ANTI-PATTERN: Descriptions are highly volatile and can be empty. Violates Non-volatile and Mandatory rules. -->
    ```