# @Domain
These rules MUST be activated when the AI is tasked with designing, customizing, evaluating, or implementing database architectures, enterprise data models (EDM), logical data models (LDM), physical database designs (PDD), data warehouse schemas, or translating business processes and terminology into relational database structures using Universal Data Model (UDM) principles.

# @Vocabulary
*   **Universal Data Model (UDM)**: A generic, template-based data model (e.g., Party, Product, Order) used as a jump-start for enterprise modeling.
*   **Enterprise Data Model (EDM)**: An integrated, holistic business view of an enterprise's information used to map interrelationships between various systems and act as a corporate data road map.
*   **Logical Data Model (LDM)**: A 3rd Normal Form (3NF) model specific to a project or application, detailing specific business processes, attributes, and data requirements without physical performance optimizations.
*   **Physical Database Design (PDD)**: The implementation-ready database schema derived from the LDM, incorporating denormalization, indexing, and DBMS-specific optimizations for performance and data volume.
*   **Alias Entity**: A business-specific term mapped to a generic UDM concept (e.g., replacing "Party" with "Business Entity").
*   **Subject Data Area**: A segmented grouping of related business concepts (e.g., Party, Product, Work Effort) used to modularize the EDM.
*   **Enterprise-wide Data Warehouse (EDW)**: The centralized, cleansed, and integrated decision support repository. 
*   **Departmental Data Mart**: A subset of the EDW summarized for specific departmental analysis.

# @Objectives
*   Translate generic Universal Data Models into highly customized Enterprise Data Models utilizing exact enterprise-specific terminology.
*   Drive Logical Data Model creation strictly from defined business processes ("how" dictates "what").
*   Guarantee that Physical Database Designs start from a normalized 3NF state and explicitly justify any denormalization based on transaction frequency, data volume, and access patterns.
*   Enforce structured, predictable subtype/supertype physical implementations based on access needs and performance trade-offs.
*   Ensure data warehousing architectures utilize an integrated central EDW rather than directly extracting from operational systems to departmental data marts.

# @Guidelines

### Customization and Impact Analysis
*   When a user requests to add an entity or relationship, the AI MUST first analyze existing UDM structures to prevent redundancy (e.g., check if a requested "Product Package" is already satisfied by "Marketing Package").
*   When a user requests to modify or delete existing UDM entities/relationships, the AI MUST perform and output an Impact Analysis detailing how the removal affects integrated subject data areas.
*   When building the EDM, the AI MUST segment the model by Subject Data Areas (e.g., Party, Product, Order, Shipment) for maintainability.

### Terminology Mapping
*   When mapping UDM constructs to enterprise environments, the AI MUST identify alias terms (e.g., UDM "Party" -> Enterprise "Business Entity"; UDM "Contact Mechanism" -> Enterprise "Contact Method").
*   When multiple aliases exist for a single UDM concept (e.g., "Email Address" and "Web Address" for "Electronic Address"), the AI MUST create the alias entities as subtypes of the generic UDM concept to bridge understanding.
*   The AI MUST NOT force a generic term onto the enterprise if the term already has a conflicting historical meaning within that organization.

### Process-Driven LDM Generation
*   When generating an LDM for a specific application, the AI MUST derive data requirements by analyzing the business process steps.
*   The AI MUST inherit baseline structures from the EDM, but MUST add application-specific attributes (e.g., formatting validation constraints, application-specific permission indicators) directly to the LDM.

### Physical Database Design (PDD) Subtype Implementation
When converting an LDM with Supertypes/Subtypes into a PDD, the AI MUST prompt the user to select, or autonomously select and justify, ONE of the following four implementation strategies:
1.  **Single Table (Supertype + Subtypes)**: Create one table containing all attributes of the supertype and all subtypes, utilizing a "Type" look-up column. Use when total row count is manageable and subtype attributes are sparse.
2.  **Separate Subtype Tables**: Create a separate table for each subtype. Copy all supertype attributes into each subtype table. Do NOT create a supertype table. Use to physically partition data by type (e.g., PERSON table and ORGANIZATION table, skipping PARTY).
3.  **Hybrid (Supertype + Split Subtypes based on access)**: Merge the supertype and the most frequently accessed subtype into one table. Create separate tables for the less accessed subtypes.
4.  **Fully Normalized (Supertype Table + Subtype Tables)**: Create a table for the supertype and separate tables for each subtype, linked via foreign keys (1:1 relationships). Use for ultimate flexibility at the cost of join performance.

### Data Warehouse Architecture Rules
*   When designing decision support environments, the AI MUST route data flow as follows: Operational Systems -> Enterprise-wide Data Warehouse (EDW) -> Departmental Data Marts.
*   The AI MUST NOT extract data directly from operational systems to departmental data marts to prevent the "inconsistent data" (e.g., two blood types) anti-pattern. All cleansing and consolidation MUST occur centrally in the EDW.

# @Workflow
1.  **Discovery & Terminology**: Evaluate the target business environment. Map UDM generic terms to enterprise-specific aliases. Define the EDM scope and segment into Subject Data Areas.
2.  **Process Mapping**: Request or define the procedural steps (the "how"). Extract the data entities required for each step (the "what").
3.  **LDM Refinement**: Construct the 3NF Logical Data Model. Inherit EDM foundations and append application-specific rules, constraints, and granular attributes.
4.  **PDD Translation**: 
    *   Transition from 3NF to the physical design.
    *   Select a Subtype Implementation Strategy (1 through 4) and document the rationale (Flexibility vs. Join Overhead vs. Row Count).
    *   Apply denormalization (e.g., derived fields, merged tables) based strictly on defined performance profiles (read-heavy vs. write-heavy).
5.  **EDW/Data Mart Staging (If Applicable)**: Define the transformation routines targeting a central EDW first, followed by dimensional star-schema designs for the data marts.

# @Examples (Do's and Don'ts)

### Terminology Mapping
*   **[DO]**: Map UDM terms to enterprise terminology by using subtypes if multiple aliases exist.
    *   *Example*: `SUPERTYPE: Electronic Address` -> `SUBTYPES: Email Address, Web Address`.
*   **[DON'T]**: Discard the underlying UDM relationship structure just because the business uses a different name.
    *   *Anti-pattern*: Rebuilding a flat contact table from scratch because the client calls it "Business Entity Contact Method" instead of "Party Contact Mechanism."

### Physical Database Design - Subtype Implementation
*   **[DO]**: Explicitly define the subtype physical strategy. If using Strategy 2 (Separate Subtype Tables), duplicate the supertype attributes into the subtype tables to avoid complex polymorphic joins.
    *   *Example*: Creating `PERSON` and `ORGANIZATION` tables, both containing `contact_method_id` and skipping the `PARTY` table, enabling sales teams to steward `ORGANIZATION` data while HR stewards `PERSON` data.
*   **[DON'T]**: Default to Strategy 4 (Fully Normalized Supertype + Subtypes) without acknowledging the performance penalty of multi-table joins for high-volume transactions.
    *   *Anti-pattern*: Creating `PARTY`, `PARTY_ROLE`, `PERSON`, `ORGANIZATION`, `CUSTOMER`, and `EMPLOYEE` tables for an application requiring sub-millisecond read times on customer profiles.

### Data Warehouse Architecture
*   **[DO]**: Define a central transformation routine that resolves discrepancies (e.g., System A says "O-Positive", System B says "O-Negative") before loading data into the EDW, then feed the Sales Data Mart and HR Data Mart from the EDW.
*   **[DON'T]**: Write extraction scripts that pull sales data directly from the Operational Order Entry system into the Sales Data Mart, while HR pulls directly from the Operational HR system into the HR Data Mart.
    *   *Anti-pattern*: Point-to-point operational-to-mart pipelines that bypass the Enterprise Data Warehouse, causing enterprise-wide reporting inconsistencies.

### Application-Specific Logical Modeling
*   **[DO]**: Retain the enterprise structure but add depth. If the EDM tracks `PARTY CONTACT MECHANISM`, the Sales Application LDM should add `use_permission_ind` to the specific Sales model to handle solicitation rules without forcing HR to track solicitation rules.
*   **[DON'T]**: Denormalize application-specific attributes into the global Enterprise Data Model if they only serve a single department's workflow.