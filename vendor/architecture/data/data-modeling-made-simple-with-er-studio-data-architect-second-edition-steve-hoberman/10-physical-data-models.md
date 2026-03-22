# @Domain
Trigger these rules when the user requests assistance with physical data modeling, database schema design, forward engineering, reverse engineering of databases (SQL, Microsoft Access, Oracle, Teradata, MongoDB, Hive), performance tuning of data models (denormalization, indexing, partitioning), database view creation, or ER/Studio physical model manipulation.

# @Vocabulary
*   **Physical Data Model (PDM)**: The detailed technical solution. A logical data model compromised and modified for a specific set of software or hardware constraints (e.g., speed, space, security).
*   **Table/Column**: The physical RDBMS equivalents of the logical "Entity" and "Attribute".
*   **Collection/Nested Object**: The physical NoSQL (e.g., MongoDB) equivalents of tables and related child tables, utilizing containment relationships.
*   **Forward Engineering**: The process of generating database code (DDL or JSON) from a physical data model.
*   **Reverse Engineering**: The process of building a physical data model by importing an existing database schema or SQL file.
*   **Datatype Mapping**: The translation of generic logical formats/lengths (e.g., integer, character) into database-specific physical types (e.g., NUMBER in Oracle, TINYINT).
*   **Denormalization**: The process of selectively violating normalization rules and reintroducing redundancy into the model to reduce data retrieval time or create a more user-friendly structure.
*   **Rolldown (Denormalization)**: Moving the parent entity's columns and relationships down into the child entity (the "many" side), eliminating the parent entity.
*   **Rollup (Denormalization)**: Moving the child entity's columns and relationships up into the parent entity, often creating arrays or repeating groups with a fixed maximum number of occurrences.
*   **Identity (Subtype Resolution)**: Resolving a logical subtype structure by replacing the subtyping symbol with one-to-one relationships for each supertype/subtype combination.
*   **Star Schema**: The most common dimensional PDM structure where each logical dimension hierarchy is flattened (collapsed) into a single table connected to a central fact table.
*   **View**: A virtual table defined by a stored SQL query, providing a dynamic window into one or more underlying tables.
*   **Index**: A database object containing a value and a pointer to instances of that value, used to speed up data retrieval. Primary/Alternate keys become Unique Indexes; Inversion Entries become Non-unique Indexes.
*   **Partitioning**: Splitting a table into multiple tables to improve performance. Vertical partitioning separates columns; horizontal partitioning separates rows.

# @Objectives
*   Translate technology-independent Logical Data Models (LDMs) into highly optimized, platform-specific Physical Data Models (PDMs).
*   Enforce the architectural rule that Physical Data Models must *never* be created from scratch; they must always originate from an LDM or be reverse-engineered.
*   Apply performance-tuning techniques such as denormalization, partitioning, and indexing based on specific query patterns and business needs.
*   Accurately resolve logical constructs (like many-to-many relationships and subtyping) into physical constructs that target platforms (RDBMS or NoSQL) can support natively.
*   Ensure accurate datatype mapping from logical abstractions to specific database syntax (e.g., DDL for relational, JSON for MongoDB).

# @Guidelines
*   **Model Instantiation**: The AI MUST NEVER create a Physical Data Model from scratch. The AI MUST base the PDM on an existing Logical Data Model (forward engineering) or an existing database/SQL file (reverse engineering).
*   **Terminology Shift**: The AI MUST shift its vocabulary when transitioning from Logical to Physical modeling. Use "Table", "Column", and "Foreign Key" for relational databases, or "Collection", "Document", and "Nested Object" for document-based databases like MongoDB.
*   **Database Platform Specificity**: The AI MUST tailor the PDM to the target DBMS. If targeting MongoDB, implement relationships as arrays/containment. If targeting RDBMS (Oracle, Teradata), utilize standard foreign keys and constraints.
*   **Datatype Mapping**: The AI MUST convert logical datatypes to physical datatypes utilizing explicit mappings (e.g., converting a logical `character` length to a `VARCHAR2` or `CHAR` depending on the platform).
*   **Subtype Resolution Matrix**: The AI MUST explicitly decide how to resolve logical subtyping in the physical model using one of three methods:
    *   *Identity*: Use when strict enforcement of rules at both supertype and subtype levels is required. (Pro: accurate constraints. Con: slower retrieval due to joins).
    *   *Rolldown*: Use when subtypes are distinct and user-friendliness is paramount. Move supertype attributes down. (Pro: fewer joins. Con: loses supertype-level rules, hard to add new subtypes).
    *   *Rollup*: Use to maximize flexibility. Move subtype attributes up into the supertype and add a discriminator column (e.g., `Type_Code`). (Pro: highly flexible for new types. Con: Subtype-specific columns must become optional/nullable).
*   **Denormalization Rules**: The AI MUST justify denormalization with performance (query speed) or usability needs.
    *   Use *Rolldown* to combine a 1:M relationship into the child table to reduce join complexity.
    *   Use *Rollup* (arrays/repeating groups) ONLY when the maximum number of child occurrences is strictly fixed and static (e.g., exactly up to 3 categories).
*   **Dimensional Flattening**: When building a dimensional PDM, the AI MUST flatten multi-level dimensional hierarchies (snowflakes) into a single table per dimension to create a Star Schema.
*   **Indexing Strategy**: 
    *   Primary keys MUST map to Unique Indexes.
    *   Alternate keys MUST map to Unique Indexes.
    *   Inversion Entries (frequently queried non-key columns) MUST map to Non-Unique Indexes.
    *   For composite indexes, the AI MUST sequence the columns based on which column is accessed/filtered most frequently.
*   **Partitioning Strategy**: 
    *   Apply *Horizontal Partitioning* to split rows based on logic (e.g., `Price < 10` vs `Price >= 10`, or by Year) to optimize query speed on large datasets.
    *   Apply *Vertical Partitioning* to isolate volatile/frequently updated columns from static columns.
*   **Views Creation**: The AI MUST encapsulate complex joins, aggregations, or derived columns within Views, ensuring the underlying `SELECT`, `FROM`, `WHERE`, `GROUP BY`, and `HAVING` clauses are syntactically valid for the target DBMS.

# @Workflow
1.  **Determine Origin**: Identify if the task requires Forward Engineering (generating PDM from LDM) or Reverse Engineering (importing DB/SQL).
2.  **Define Target Platform**: Request or identify the specific target DBMS (e.g., Oracle 11g, Hive, MongoDB).
3.  **Translate Structures**: Convert logical entities/attributes to tables/columns (or collections/fields). Convert logical datatypes to physical datatypes.
4.  **Resolve Subtypes**: Identify any subtype clusters from the LDM and apply Identity, Rolldown, or Rollup based on flexibility and constraint requirements.
5.  **Apply Denormalization**: Evaluate 1:M relationships. Determine if Rolldown or Rollup is required to meet performance or usability thresholds. Document the reasoning.
6.  **Convert to Star Schema (If Dimensional)**: Flatten all normalized dimension hierarchies into single dimension tables linked directly to the central Fact table.
7.  **Generate Indexes**: Create Unique Indexes for Primary/Alternate keys. Create Non-Unique Indexes for frequently queried columns. Sequence composite index columns optimally.
8.  **Define Partitions**: If dataset size or query patterns dictate, specify horizontal or vertical partition schemas.
9.  **Develop Views**: Write the DDL for any requested Views to simplify user querying of the underlying tables.
10. **Generate Output**: Provide the physical schema representation, DDL script, or JSON structure based on the final PDM configurations.

# @Examples (Do's and Don'ts)

**Principle: Subtype Resolution (Rollup vs. Identity)**
*   [DO]: Resolve a `Person` supertype and `Employee`/`Customer` subtypes using Rollup by creating a single `Person` table with a `Party_Role_Code` column, making `Employee_Start_Date` nullable.
*   [DON'T]: Leave the subtyping symbol in the physical model, as relational databases do not natively support conceptual subtyping structures.

**Principle: Denormalization (Rollup / Arrays)**
*   [DO]: Use Rollup denormalization to store `Phone_1`, `Phone_2`, and `Phone_3` in a `Contact` table ONLY if the business rule strictly dictates a maximum of exactly 3 phones.
*   [DON'T]: Use Rollup for `Customer_Orders` in a relational DB, as a customer can have an infinite, unknown number of orders, which would break the fixed-column array constraint.

**Principle: MongoDB/NoSQL PDM Design**
*   [DO]: Map a Logical 1:M relationship between `Order` and `Order_Line` into a MongoDB PDM using a containment relationship, resulting in a single `Order` JSON document containing an array of `Order_Line` nested objects.
*   [DON'T]: Map `Order` and `Order_Line` as two separate collections with a relational foreign key in MongoDB unless explicitly required by an abnormal access pattern.

**Principle: Index Column Sequencing**
*   [DO]: When creating a composite index on `Last_Name` and `First_Name`, place `Last_Name` first in the sequence if users predominantly search by Last Name.
*   [DON'T]: Arbitrarily order columns in a composite index without considering the WHERE clause filtering frequency of the target application.