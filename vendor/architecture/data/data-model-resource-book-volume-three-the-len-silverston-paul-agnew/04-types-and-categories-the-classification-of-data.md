@Domain
Data modeling, database schema design, enterprise data architecture, and software engineering tasks involving the classification, categorization, or taxonomy development for any business entity (e.g., Products, Parties, Assets, Work Efforts, Orders). Trigger these rules whenever a user requests to add types, groups, families, lines, categories, or reference data to an entity.

@Vocabulary
- **Type**: A number of things or persons sharing a particular characteristic or set of characteristics that cause them to be regarded as a group. A simple classification (e.g., "Sales Order").
- **Categorization**: A general or comprehensive division involving different ways to classify an entity; representing "types of types" (e.g., categorizing a person by income, gender, race).
- **Taxonomy**: A classified collection of elements organized into systems of classification or intuitive familial groups, often supporting hierarchies or aggregations of categories and types.
- **Indicator**: A special case of classification used to capture a specific, binary piece of knowledge about an instance (e.g., "Y/N" for smoker).
- **Level 1 Classification Pattern**: A specific, denormalized conceptual modeling style where classifications are maintained strictly as attributes (columns) within the main entity.
- **Level 2 Classification Pattern**: A normalized modeling style where each distinct classification type (e.g., Product Family, Product Line) is maintained as a separate, explicitly named entity.
- **Level 3 Classification Pattern**: A generalized, highly flexible modeling style where all classifications for an entity are managed within a single generalized Category entity and a Category Type entity, connected via an associative classification entity.
- **Level 3 Classification Pattern with Rollups and Schemes**: An extension of the Level 3 pattern that replaces 1:M recursions with M:M associative rollup entities and adds scheme entities to track internal/external classification providers.
- **Scheme**: A combination of elements connected, adjusted, and integrated by design for the classification of Category Types, provided by a specific internal or external Data Provider (e.g., Standard Industrial Classification).
- **Data Provider**: The internal department or external organization (Party) that designates or originates a specific classification scheme.

@Objectives
- Ensure data classifications are modeled with the precise level of generalization required by the business dynamics (ranging from conceptual scoping to highly flexible, change-tolerant enterprise physical designs).
- Prevent data anomalies, repeating groups, and transitive dependencies in physical database implementations by strictly avoiding Level 1 patterns for production schemas.
- Enable robust analytics by structuring categories to allow seamless drill-up, drill-down, and cross-classification reporting.
- Provide standardized, future-proof schemas for dynamic environments where new classification types frequently emerge.

@Guidelines

- **General Classification Rules:**
  - The AI MUST NOT treat categorization as a mere attribute string in a physical database design unless strictly instructed that the data is entirely static and non-redundant.
  - The AI MUST evaluate the volatility of the business environment to determine the correct pattern level.
  - If an entity possesses subtypes (e.g., `HARDWARE`, `SOFTWARE` subtypes of `PRODUCT`) and is also classified by a "type" or "category" entity, the AI MUST ensure that the subtypes correspond directly to instances within the "type" or "category" entity.
  - When utilizing indicators (e.g., `gender_indicator`), the AI MUST warn the user that indicators can often expand beyond binary values (e.g., Male, Female, Not Given) and suggest a standard classification pattern if future expansion is likely.

- **Level 1 Classification Constraints (Attributes):**
  - The AI MUST restrict the use of Level 1 Classification Patterns to conceptual scoping, business requirements gathering, or rapid disposable prototypes.
  - The AI MUST explicitly warn the user that Level 1 implementations violate First Normal Form (1NF) if multiple classifications of the same type exist (e.g., `product_line_1`, `product_line_2`).
  - The AI MUST explicitly warn the user that Level 1 implementations violate Third Normal Form (3NF) because classification values (e.g., "Disk Drives") are transitively dependent on their own implicit key, not the primary entity key.

- **Level 2 Classification Constraints (Specific Entities):**
  - The AI MUST use this pattern when classification types are well-understood, static, and require their own specific attributes and relationships.
  - For mutually exclusive classifications (an entity can only have one classification of this type), the AI MUST create a 1:M relationship from the `[ENTITY] TYPE` to the `[ENTITY]`.
  - For classifications where an entity can belong to multiple instances of the type, the AI MUST create a Many-to-Many (M:M) associative entity (e.g., `[ENTITY] [ENTITY] TYPE CLASSIFICATION`).
  - The AI MUST optionally include a 1:M recursive relationship on the `[ENTITY] TYPE` entity to support simple hierarchies (e.g., "Hardware" -> "Storage Devices").

- **Level 3 Classification Constraints (Generalized Categories):**
  - The AI MUST use this pattern when the environment is dynamic, new classification types emerge frequently, or an entity requires a massive number of diverse classifications.
  - The AI MUST implement the following specific triad of entities:
    1.  `[ENTITY] CATEGORY TYPE`: Maintains the labels/headings of the classifications (e.g., "Product Family").
    2.  `[ENTITY] CATEGORY`: Maintains the actual classification values (e.g., "Laptop"). Must include a mandatory foreign key to `[ENTITY] CATEGORY TYPE`.
    3.  `[ENTITY] CATEGORY CLASSIFICATION`: An associative entity resolving the M:M relationship between `[ENTITY]` and `[ENTITY] CATEGORY`. Must include `from_date` and `thru_date` to track history.
  - The AI MUST include 1:M recursive relationships on both `[ENTITY] CATEGORY` and `[ENTITY] CATEGORY TYPE` to support rollups and drill-downs.
  - The AI MUST allow the creation of "aggregation-only" categories (e.g., "Profit and Loss Reporting Categories") that are never directly assigned to an entity instance but are used to aggregate lower-level categories.

- **Level 3 with Rollups and Schemes Constraints:**
  - The AI MUST use this pattern when classifications belong to standard taxonomies provided by third parties (e.g., government bodies, data vendors) or when categories belong to multiple, conflicting hierarchical structures (M:M rollups).
  - The AI MUST create an `[ENTITY] CATEGORY TYPE SCHEME` entity.
  - The AI MUST relate `[ENTITY] CATEGORY TYPE` to `[ENTITY] CATEGORY TYPE SCHEME` (1:M).
  - The AI MUST relate `[ENTITY] CATEGORY TYPE SCHEME` to a `DATA PROVIDER` entity (representing the Party providing the scheme).
  - The AI MUST NOT merge identical classification names from different schemes into a single instance; they must remain distinct instances tied to their respective schemes.
  - The AI MUST replace the 1:M recursive relationships on categories with M:M associative entities: `[ENTITY] CATEGORY ROLLUP` and `[ENTITY] CATEGORY TYPE ROLLUP`.
  - The AI MUST classify the rollup associative entities using `[ENTITY] CATEGORY ROLLUP TYPE` and `[ENTITY] CATEGORY TYPE ROLLUP TYPE` (e.g., "Sales reporting rollup" vs. "Service reporting rollup").

@Workflow
1.  **Requirement Analysis**: Upon receiving a request to classify an entity, the AI MUST interrogate the request to determine:
    - Are the classification types static or highly dynamic?
    - Will the entity belong to multiple categories of the same type?
    - Do the categories originate from external/internal regulatory schemes?
    - Are complex M:M rollups required?
2.  **Pattern Selection**:
    - Select **Level 1** ONLY for conceptual models or explicit user overrides for flat-file generation.
    - Select **Level 2** for stable, specific schemas where each classification type needs discrete attributes.
    - Select **Level 3** for enterprise-scale, dynamic schemas requiring the addition of new classification types without altering DDL.
    - Select **Level 3 with Rollups/Schemes** for master data management, reference data integration, or handling external taxonomies.
3.  **Schema Generation**: Generate the entities, primary keys (PK), foreign keys (FK), and attributes according to the selected pattern.
4.  **Temporal History Injection**: Ensure all associative entities (e.g., `CLASSIFICATION`, `ROLLUP`) contain `from_date` (part of the PK/UID) and `thru_date` to support historical tracking.
5.  **Validation**: Verify that generalized models (Level 3) do not erroneously blend apples and oranges (e.g., rolling up a "Product Type" into a "Product Line"); instruct the user to handle cross-type validations via a business rules layer, as generalized models do not enforce these strictly at the database level.

@Examples

**[DO] - Level 2 Classification Pattern (Normalized, Static)**
```sql
CREATE TABLE PRODUCT_TYPE (
    product_type_id ID PK,
    parent_product_type_id ID FK NULL, -- 1:M Hierarchy
    name VARCHAR
);

CREATE TABLE PRODUCT_LINE (
    product_line_id ID PK,
    name VARCHAR
);

CREATE TABLE PRODUCT (
    product_id ID PK,
    product_type_id ID FK NOT NULL, -- Mutually exclusive classification
    name VARCHAR
);

-- M:M Classification Resolution
CREATE TABLE PRODUCT_PRODUCT_LINE_CLASS (
    product_id ID FK,
    product_line_id ID FK,
    from_date DATE,
    thru_date DATE NULL,
    PRIMARY KEY (product_id, product_line_id, from_date)
);
```

**[DON'T] - Level 1 Classification Pattern in a Physical Relational Database**
```sql
-- ANTI-PATTERN: Violates 1NF and 3NF. Do not use for physical implementations.
CREATE TABLE PRODUCT (
    product_id ID PK,
    product_type VARCHAR,          -- Transitive dependency violation
    product_family VARCHAR,
    product_line_1 VARCHAR,        -- Repeating group violation (1NF)
    product_line_2 VARCHAR         -- Repeating group violation (1NF)
);
```

**[DO] - Level 3 Classification Pattern (Generalized, Dynamic)**
```sql
CREATE TABLE PRODUCT_CATEGORY_TYPE (
    product_category_type_id ID PK,
    parent_product_category_type_id ID FK NULL,
    name VARCHAR -- e.g., "Product Family", "Product Line"
);

CREATE TABLE PRODUCT_CATEGORY (
    product_category_id ID PK,
    product_category_type_id ID FK NOT NULL,
    parent_product_category_id ID FK NULL,
    name VARCHAR -- e.g., "Laptop", "Home Use"
);

CREATE TABLE PRODUCT_CATEGORY_CLASSIFICATION (
    product_id ID FK,
    product_category_id ID FK,
    from_date DATE,
    thru_date DATE NULL,
    PRIMARY KEY (product_id, product_category_id, from_date)
);
```

**[DO] - Level 3 Classification with Rollups and Schemes (Master Data/Taxonomy)**
```sql
CREATE TABLE DATA_PROVIDER (
    data_provider_id ID PK,
    name VARCHAR -- e.g., "World Customs Organization"
);

CREATE TABLE PRODUCT_CATEGORY_TYPE_SCHEME (
    scheme_id ID PK,
    data_provider_id ID FK NOT NULL,
    name VARCHAR -- e.g., "Harmonized System (HS)"
);

CREATE TABLE PRODUCT_CATEGORY_TYPE (
    product_category_type_id ID PK,
    scheme_id ID FK NOT NULL,
    name VARCHAR 
);

-- M:M Rollup replacing the 1:M recursion
CREATE TABLE PRODUCT_CATEGORY_ROLLUP (
    parent_product_category_id ID FK,
    child_product_category_id ID FK,
    rollup_type_id ID FK, -- e.g., "Sales Rollup" vs "Support Rollup"
    from_date DATE,
    thru_date DATE NULL,
    PRIMARY KEY (parent_product_category_id, child_product_category_id, rollup_type_id, from_date)
);
```

**[DON'T] - Merging Schemes Incorrectly**
```text
-- ANTI-PATTERN: Reusing the exact same Category Type instance across different provider schemes.
-- Even if "Computer Disks" exists in both the "Harmonized System" and "Schedule B" schemes, 
-- they MUST be modeled as two separate instances in PRODUCT_CATEGORY_TYPE tied to their respective SCHEME_ID.
```