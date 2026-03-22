# @Domain
Database architecture, logical data modeling, physical database design, data warehouse creation, dimensional modeling (star schema design), and cross-industry schema adaptation. These rules trigger when the AI is tasked with designing databases, creating data models, defining data warehouses, or adapting existing data structures for a new business application or industry.

# @Vocabulary
- **Logical Data Model**: A normalized, non-redundant perspective of an enterprise's information requirements, focusing on data nature and relationships independently of performance constraints.
- **Physical Database Design**: The actual implementation of the logical data model, requiring modifications such as denormalization to accommodate performance and ease-of-access considerations.
- **Dimensional Modeling (Star Schema)**: A data warehouse design technique using fact tables and dimension tables to support decision-support databases.
- **Fact Table**: The central table in a star schema containing measures/metrics.
- **Universal Data Model**: A broad, generic template data model designed to be flexible, stable, and integrated, rather than hyper-specific to a narrow industry.
- **Modularized Construct**: A reusable data model module classified by its function (e.g., "time and activity tracking", "bill of materials") rather than its original industry label, allowing for cross-industry application.
- **Denormalization**: The process of strategically adding redundancy to a physical database design to improve query performance.

# @Objectives
- Translate logical data models into optimal physical database designs by intelligently applying denormalization and assessing access considerations.
- Prevent data warehouse design errors by strictly deriving dimensional models (star schemas) from a deep understanding of the underlying logical data model and its relationships.
- Maximize enterprise stability, flexibility, and integration by defaulting to broad, universal data models over isolated, hyper-specific industry models.
- Facilitate rapid, high-quality system development by mixing, matching, and adapting functional data model modules across diverse industries.

# @Guidelines
- **Logical vs. Physical Implementation**: The AI MUST NOT blindly implement a logical data model directly as a physical database design without assessing performance and ease-of-access. The AI MUST apply denormalization where necessary for the physical schema.
- **Data Warehouse Pre-requisites**: The AI MUST NOT jump directly into dimensional modeling (star schema design) without first analyzing the logical data model. 
- **Many-to-Many Awareness**: When designing fact tables and measures, the AI MUST explicitly account for many-to-many relationships present in the logical model to prevent faulty measures or miscalculated/duplicate totals (e.g., an invoice related to multiple shipment items).
- **Broad Over Specific**: The AI MUST default to broad, general industry models rather than creating narrow, highly specific models. Broad models MUST be used to ensure a framework that accommodates future vision, system integration, and business rule changes.
- **Cross-Industry Adaptation**: The AI MUST reuse data structures from seemingly unrelated industries if the underlying business function matches. When adapting, the AI MUST modify the entity names to fit the new business context while retaining the structural logic. 
  - *Constraint*: Use Telecommunications network constructs for facility/usage management (e.g., Oil and Gas).
  - *Constraint*: Use Manufacturing structures (BOM, substitutions) for Distributors.
  - *Constraint*: Use Travel structures (reservations, ticketing) for Sports or Entertainment Event Management.
  - *Constraint*: Use Financial Services structures (risk assessment, market segments) for Venture Capital companies.
  - *Constraint*: Use Professional Services structures for any enterprise delivering services that complement physical goods.
  - *Constraint*: Use E-Commerce/Web structures for any organization promoting products online to maintain needs, subscriptions, and visits.
- **Modular Mix-and-Match**: If an enterprise spans multiple business types, the AI MUST pull from multiple universal data model modules to fulfill the complete requirement rather than forcing all requirements into a single industry's paradigm.

# @Workflow
1. **Requirement Analysis & Module Selection**:
   - Evaluate the target enterprise's functional requirements.
   - Identify the appropriate universal data model modules based on *functionality* (e.g., parts composition, reservation tracking, facility management), ignoring the original industry label of the module.
2. **Logical Model Consolidation**:
   - Merge the selected generic constructs and industry-specific modules into a cohesive logical data model.
   - Map out all entities, sub-types, and granular relationships, explicitly documenting many-to-many intersections.
   - Rename entities as necessary to match the target enterprise's terminology while preserving the structural integrity of the relationships.
3. **Physical Database Translation (If building a transaction-oriented system)**:
   - Analyze the logical data model for performance bottlenecks.
   - Apply strategic denormalization and indexing.
   - Generate the physical schema tailored for transaction speed and data access efficiency.
4. **Data Warehouse Translation (If building a decision-support system)**:
   - Map the dimensions and fact tables strictly against the logical data model.
   - Trace all relationships to ensure that product classifications or hierarchical roll-ups do not result in duplicate aggregations in the fact table.
   - Define measures carefully, ensuring that many-to-many relationships (e.g., shipment items to invoice items) are resolved correctly at the chosen level of granularity.

# @Examples (Do's and Don'ts)

**Dimensional Modeling Approach**
- [DO]: First define the logical data model showing that `PRODUCT` has a many-to-many relationship with `PRODUCT_CATEGORY`. Then, design the star schema by creating a bridge table or handling the many-to-many dimension properly to ensure product sales totals are not artificially inflated when queried.
- [DON'T]: Jump straight into designing a star schema, assuming a 1-to-many relationship between `PRODUCT_CATEGORY` and `PRODUCT`, leading to a fact table that double-counts revenue when a product belongs to multiple categories.

**Physical Database Implementation**
- [DO]: Take a highly normalized logical model (e.g., `PARTY` -> `PARTY_ROLE` -> `CUSTOMER`) and denormalize it into a physical `CUSTOMER` table with embedded party details if the system requires microsecond read access for a specific customer-facing application.
- [DON'T]: Generate a physical SQL schema that exactly mirrors a heavily normalized 5th Normal Form logical model without evaluating if the resulting 12-table joins will destroy query performance.

**Cross-Industry Module Adaptation**
- [DO]: Use the "Travel" reservation and ticketing data model (Nodes: `RESERVATION`, `SCHEDULED_OFFERING`, `TICKET`, `COUPON`) for a theater company by renaming the entities to `EVENT_BOOKING`, `SCHEDULED_SHOW`, `ADMISSION_TICKET`, and `SEAT_COUPON`, preserving the relationships.
- [DON'T]: Build a reservation system from scratch for a theater company because "theatre isn't covered in the travel chapter."

**General vs Specific Models**
- [DO]: Implement a generic `AGREEMENT` and `INSURANCE_POLICY` structure that can handle Auto, Life, and Health insurance via sub-typing and feature interactions.
- [DON'T]: Create a hyper-specific `AUTO_INSURANCE_POLICY_DB` that cannot be extended if the company later decides to sell Homeowners insurance.