@Domain
These rules MUST trigger whenever the AI is requested to design, evaluate, translate, or refactor data models for specific deployment purposes, including but not limited to: Prototypes, Scope Statements, Application Data Models, Enterprise Data Models (EDM), Relational Data Warehouses (EDW), Star Schema Data Marts, and Master Data Management (MDM) systems. The AI must apply these rules to determine the appropriate level of data model generalization based on the target audience and system requirements.

@Vocabulary
- **Interchangeable Pattern Components**: The concept that data modeling patterns (Levels 1 through 4) can be swapped in and out of a model to adjust the balance between specificity (understandability) and generalization (flexibility).
- **Prototype / Scope Statement Model**: A highly specific data model (primarily Level 1 and 2 patterns) used to communicate exact data requirements, terminology, and business scope to non-technical audiences.
- **Application Data Model**: A production-grade data model that balances current expressed requirements (specific patterns) with future/unknown requirements (generalized patterns).
- **Enterprise Data Model (EDM)**: A comprehensive data landscape that provides a standard view of core entities. Often uses a "Hybrid" approach, showing both specific and generalized alternatives for the same data constructs.
- **Relational Data Warehouse Model (Inmon Approach)**: An enterprise-wide, highly flexible data model (primarily Level 3 patterns) designed to integrate data from multiple diverse source systems and track historical changes over time.
- **Star Schema Model (Kimball Approach)**: A physical reporting design comprising a central Fact table and flattened Dimension tables (which functionally resemble Level 1 or 2 patterns).
- **Precursor Logical Model**: A logical data model constructed prior to Star Schema design to uncover and understand underlying data complexity (e.g., multiple statuses, complex hierarchies) before flattening.
- **Master Data Management (MDM) Model**: A highly flexible, generalized data model (Level 3/4) designed to integrate, synchronize, and conform reference/master data across an enterprise, tightly coupled with Business Rule patterns for identity management.
- **Data Stewardship**: The organizational process of assigning accountability for data management, which becomes critically necessary when implementing generalized data models.
- **Subtype Conversion Strategies**: The four physical database implementation methods for logical subtypes: 1) One table for supertype and subtypes, 2) One table for supertype and one for each subtype, 3) One table per subtype containing inherited supertype attributes, 4) A hybrid of the above.

@Objectives
- The AI MUST select the appropriate data modeling pattern level based strictly on the target audience and the specific systemic purpose of the model.
- The AI MUST sacrifice flexibility for understandability when designing for business users (Prototypes/Scope).
- The AI MUST sacrifice immediate simplicity for flexibility and stability when designing for integration environments (EDW/MDM).
- The AI MUST explicitly document and manage the loss of specific business rules that occurs when utilizing highly generalized (Level 3/4) patterns.
- The AI MUST treat patterns as modular, plug-and-play components, swapping specific patterns for generalized ones when "unknowns" or future requirements are detected.

@Guidelines

**1. Rules for Prototypes and Scope Statements**
- The AI MUST use Level 1 (and occasionally Level 2) patterns when generating models for scope statements, requirements gathering, or prototypes.
- The AI MUST use exact business terminology for entity and attribute names to ensure the model acts as an effective communication baseline.
- **ANTI-PATTERN WARNING**: The AI MUST explicitly warn the user if they attempt to generate production database schemas (DDL) directly from a Level 1 prototype model, highlighting that it will cause severe data redundancy, anomalies, and maintenance failures.
- When an "unknown" is encountered in scoping (e.g., "We know we have statuses, but we don't know what they are yet"), the AI MUST immediately upgrade that specific component to a Level 2 pattern to provide a placeholder.

**2. Rules for Application Data Models**
- The AI MUST blend specific (Level 1/2) and generalized (Level 3) patterns to balance current requirements with future flexibility.
- For data constructs where the business is absolutely certain of the boundaries (e.g., only 3 customer classifications will ever exist), the AI MUST use Level 2 patterns.
- For data constructs where the future is uncertain or complex (e.g., potential new roles, varying statuses), the AI MUST use Level 3 patterns (e.g., `PARTY ROLE`, `ORDER ROLE`).
- The AI MUST enforce data integration readiness by using standard enterprise structures (e.g., the `PARTY` concept) even if the immediate application scope seems narrowly focused on `CUSTOMER`.

**3. Rules for Enterprise Data Models (EDM)**
- The AI MUST construct EDMs to serve as a reusable template repository and quality assurance checkpoint for the entire enterprise.
- The AI MAY use a **Hybrid Modeling Approach**, presenting both a specific construct (e.g., `CUSTOMER SIZE`, `CUSTOMER TYPE`) and a generalized construct (e.g., `PARTY ROLE CATEGORY`) for the same data requirement to offer architectural choices.
- **CRITICAL CONSTRAINT**: When providing hybrid alternatives in an EDM, the AI MUST explicitly document that these are design alternatives and that the enterprise MUST NOT redundantly capture the same data instances in both structures simultaneously.

**4. Rules for Relational Data Warehouses**
- The AI MUST utilize highly generalized patterns (Level 3) consistently across the EDW to support data integration from highly diverse, disparate source systems.
- The AI MUST NOT simply copy source system data structures into the EDW model, as source systems lack the generalized flexibility required for enterprise integration.
- The AI MUST implement associative entities with `from_date` and `thru_date` attributes to capture data warehouse history and track slowly changing relationships over time.

**5. Rules for Star Schemas / Data Marts**
- The AI MUST generate a **Precursor Logical Model** using appropriate patterns (e.g., Level 3 Classifications) to fully analyze and understand data complexities (multi-categories, multiple valid statuses) BEFORE outputting Star Schema DDL.
- The AI MUST "flatten" the complex logical patterns into specific Dimension tables (which structurally resemble Level 1 or 2 patterns).
- When a dimension entity has multiple simultaneous classifications (e.g., a Product in multiple Categories), the AI MUST decouple them into separate Dimension tables (e.g., `PRODUCT_DIM` and `PRODUCT_CATEGORY_DIM`) to prevent erroneous aggregations or reporting double-counts.
- The AI MUST map recursive structures (Level 2/3 Recursive Patterns) into flattened dimensional levels (e.g., Parent Company, Company, Division, Department) within the Dimension table, warning the user if the hierarchy depth exceeds the hardcoded design.

**6. Rules for Master Data Management (MDM)**
- The AI MUST utilize the highest level of generalization (Level 3 and 4 patterns) to accommodate the "least common denominator" of structural variations coming from multiple disparate source systems.
- The AI MUST integrate Business Rule patterns (from Chapter 8) directly into the MDM model to handle Identity Management, record matching, merge rules, and survivorship (System of Record determination).

**7. Rules for Physical Database Design Translation**
- When translating a logical pattern containing Subtypes/Supertypes into physical DDL, the AI MUST explicitly prompt the user or state its chosen Subtype Conversion Strategy:
  1. Single table for Supertype and all Subtypes (Single Table Inheritance).
  2. One table for the Supertype and one separate table for each Subtype (Class Table Inheritance).
  3. Tables ONLY for Subtypes, inheriting all Supertype attributes (Concrete Table Inheritance).
  4. Hybrid combination of the above.
- The AI MUST document that adopting generalized patterns shifts the organizational burden from traditional DB developers to Data Stewards, who must manage the data instances that drive the model's structure.

@Workflow
1. **Context Identification**: The AI MUST ask or deduce the target system type (Prototype, Application, EDM, Relational DW, Star Schema, MDM).
2. **Pattern Level Selection**: Based on the target, the AI MUST select the appropriate pattern levels (e.g., Level 1 for Scope, Level 3 for MDM).
3. **Draft Precursor/Logical Model**: The AI MUST construct the initial logical entities, applying generalized patterns to any identified "unknowns" or volatile requirements.
4. **Complexity Resolution (Star Schema Only)**: If the target is a Star Schema, the AI MUST explicitly document the underlying logical complexity (e.g., multi-status relationships) and output the flattened dimensional mapping.
5. **Rule Integration (MDM/EDW Only)**: If the target requires heavy data governance, the AI MUST attach Business Rule entities to the generalized structures.
6. **Physical Translation**: The AI MUST apply the correct Subtype Conversion Strategy and output the physical schema, attaching warnings regarding data stewardship and missing explicit business rules for generalized components.

@Examples

**[DO]**
*Scenario: Generating an Enterprise Data Model (EDM) incorporating a Hybrid Pattern.*
```markdown
### Enterprise Data Model: Customer Classification (Hybrid Approach)

To serve both business users and technical architects, this EDM provides two design alternatives for Customer Classification. 
**Note to Implementers**: Choose ONE path for physical implementation to avoid data redundancy. Do NOT populate both structures with the same instances.

**Specific Alternative (Level 2 Classification)**
- `CUSTOMER` (Entity)
- `CUSTOMER_TYPE` (Entity)
- `CUSTOMER_SIZE` (Entity)
- *Relationships*: `CUSTOMER` has one `CUSTOMER_TYPE`; `CUSTOMER` has one `CUSTOMER_SIZE`.

**Generalized Alternative (Level 3 Classification)**
- `PARTY_ROLE` (Supertype containing Customer)
- `PARTY_ROLE_CATEGORY` (Entity)
- `PARTY_ROLE_CATEGORY_CLASSIFICATION` (Associative Entity)
- `PARTY_ROLE_CATEGORY_TYPE` (Entity)
- *Relationships*: `PARTY_ROLE` is classified by many `PARTY_ROLE_CATEGORY_CLASSIFICATION`s.
```

**[DON'T]**
*Scenario: Designing an Application Database.*
```sql
/* INCORRECT: The AI used a Level 1 pattern for a production application where contact mechanism requirements are expected to grow. */
CREATE TABLE CUSTOMER (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    home_phone VARCHAR(20),
    work_phone VARCHAR(20),
    fax_number VARCHAR(20),
    primary_email VARCHAR(100),
    secondary_email VARCHAR(100) -- Violates First Normal Form; inflexible to new contact types.
);
```

**[DO]**
*Scenario: Designing a Star Schema from a complex logical model.*
```markdown
### Star Schema Dimension Design: Customer Status
**Precursor Logical Analysis**: The underlying logical model (Level 3 Status Pattern) indicates that a `CUSTOMER` can hold multiple valid statuses simultaneously during the lifecycle of an `ORDER`. 

**Dimensional Flattening**: 
Because a Customer can have multiple statuses, embedding Status directly into the `CUSTOMER_DIM` will cause Cartesian products or force the selection of only the "latest" status, dropping historical context. 

*Resolution*: Create a separate `CUSTOMER_STATUS_DIM`. 
- `ORDER_FACT` (contains foreign keys to `CUSTOMER_DIM` and `CUSTOMER_STATUS_DIM`)
- `CUSTOMER_DIM` (Customer demographic data)
- `CUSTOMER_STATUS_DIM` (Levels: Status Name, Status Category)
```

**[DON'T]**
*Scenario: Generating a Relational Data Warehouse Model.*
```markdown
/* INCORRECT: The AI copied the source system schema directly into the EDW without applying Level 3 patterns or historical tracking. */
Table: SOURCE_ORDER_STATUS
- order_id
- status_name
- status_date
(Missing generalization into `STATUS_TYPE`, missing `from_date` / `thru_date` for historical tracking required in a Data Warehouse).
```