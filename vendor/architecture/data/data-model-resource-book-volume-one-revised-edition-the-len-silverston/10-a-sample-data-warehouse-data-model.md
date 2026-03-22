# @Domain
When the user requests the design, creation, or analysis of Data Warehouse Data Models, ETL (Extract, Transform, Load) transformation logic, or the integration of operational schemas into a decision support system (DSS), the AI MUST activate and strictly adhere to these rules.

# @Vocabulary
- **Enterprise Data Warehouse (EDW)**: A central, integrated, subject-oriented, and very granular base of strategic information extracted from operational environments to serve as a single source for decision support.
- **Data Mart / Departmental Data Warehouse**: A subset of the EDW containing lightly or highly summarized data tailored for specific departmental analysis.
- **Atomic Level**: The lowest, most detailed level of granularity in the data warehouse, representing individual transactions (e.g., an individual invoice item) rather than summaries.
- **Relationship Artifact**: The representation of a relationship that existed at a specific point in time in the operational system, resolved into an explicit, role-specific foreign key or data attribute in the data warehouse.
- **Snapshot Date**: A key column added to a dimension table to track historical point-in-time changes to volatile attributes (e.g., demographics).
- **Derived Data**: Data calculated from atomic operational fields (e.g., `extended_amount` = `quantity` * `amount`) and stored physically in the warehouse to reduce query processing overhead.
- **Scrubbing/Cleansing**: The process of examining data from multiple operational sources, identifying inconsistencies, and transforming it into a common, unified format for the warehouse.
- **Common Reference Tables**: Dimension tables (e.g., `GEOGRAPHIC_BOUNDARIES`, `PRODUCTS`) that span multiple subject data areas and are used consistently across different departmental views.
- **Stability Separation**: The architectural practice of splitting an entity into multiple tables based on the volatility of its attributes (e.g., splitting static customer names from rapidly changing customer demographics).

# @Objectives
- The AI MUST design the data warehouse data model to support enterprise-wide strategic decision making by capturing trends, performance metrics, and key business indicators.
- The AI MUST transform normalized operational data into analytical schemas by removing non-strategic data, merging related tables, resolving relationship artifacts, and adding time elements.
- The AI MUST store data at the most atomic level of granularity in the central warehouse, deferring higher-level summarization to departmental data marts.
- The AI MUST ensure data consistency across the enterprise by enforcing the use of Common Reference Tables for shared dimensions.

# @Guidelines
- **Removing Operational Data**: When extracting data for the warehouse, the AI MUST omit purely operational information (e.g., messages, textual descriptions, workflow statuses, transactional terms) that lacks strategic analytical value.
- **Time Variance Enforcement**: For tables containing stateful or descriptive data that changes over time, the AI MUST add an element of time to the primary key. The AI MUST use `snapshot_date` for point-in-time historical tracking, or `from_date` and `thru_date` for interval tracking.
- **Exclusion of Time Elements on Immutable Transactions**: The AI MUST NOT add time elements to the primary key of atomic transactional records (e.g., `invoice_item`) if the transaction itself is not time-variant (i.e., it does not change after being posted).
- **Derived Data Materialization**: The AI MUST physically calculate and store frequently accessed derived data (e.g., `extended_amount`, `product_cost`) to ensure algorithmic consistency and optimize read performance.
- **Role-Specific Relationship Artifacts**: The AI MUST resolve generic operational foreign keys into explicit, role-specific relationship artifacts. For example, the AI MUST rename a generic `party_id` to `billed_to_customer_id` or `internal_organization_id` to clearly define the DSS context.
- **Recursive Hierarchies**: The AI MUST implement recursive relationships (e.g., `manager_rep_id` referencing `sales_rep_id`) to support organizational reporting structures without requiring excessive table joins.
- **Granularity Preservation**: The AI MUST design the core data warehouse fact tables at the atomic transaction level (e.g., `CUSTOMER_INVOICES` at the invoice item level) to allow data marts to summarize data at any required level.
- **Table Merging**: The AI MUST merge separate operational tables (e.g., `INVOICE` header and `INVOICE_ITEM` detail) into a single warehouse table IF they share a common key, are frequently queried together, and share the exact same insertion pattern.
- **Stability-Based Separation**: The AI MUST separate highly volatile attributes into distinct tables (e.g., moving age and credit rating to `CUSTOMER_DEMOGRAPHICS` away from `CUSTOMERS`) to prevent redundant storage of static attributes whenever a new historical snapshot is taken.
- **Load Auditing**: The AI MUST include a `load_date` column in warehouse tables to identify exactly when the data was extracted and loaded into the warehouse.
- **Common Reference Tables**: The AI MUST define universally applicable dimension tables (e.g., `PRODUCTS`, `GEOGRAPHIC_BOUNDARIES` using a `geo_id`) and reuse them across all integrated subject areas (Sales, Budgeting, HR).
- **Iterative Integration**: The AI MUST design the warehouse to allow iterative integration of subject data areas one at a time, ensuring new subject areas link back to existing Common Reference Tables.

# @Workflow
1. **Analyze Operational Source**: Identify the operational entities, relationships, and attributes comprising the target subject area.
2. **Remove Operational Data**: Strip out all fields primarily used for operational processing (messages, handling instructions, text logs, operational statuses).
3. **Merge Tables**: Identify header/detail tables (e.g., `ORDER` / `ORDER_ITEM`) that share insertion patterns and merge them into a single, flattened transactional warehouse table.
4. **Add Derived Data**: Identify mathematically related fields and create pre-calculated metric columns (e.g., calculate and store `product_cost` or `extended_amount`).
5. **Resolve Relationship Artifacts**: Translate complex operational relationship links into clear, role-named foreign keys (e.g., traverse `INVOICE_ROLE` to extract `sales_rep_id`).
6. **Apply Time Variance**: Add `snapshot_date` to the primary key of dimension tables where attributes change over time. Add `load_date` to all tables for auditability.
7. **Separate by Stability**: Review dimension tables. If a dimension contains a mix of static data (names) and highly volatile data (demographics, credit scores), split them into separate tables linked by the entity ID and `snapshot_date`.
8. **Link to Common Reference Tables**: Ensure all geographic, product, or organizational keys point to enterprise-wide Common Reference Tables.

# @Examples (Do's and Don'ts)

**Principle: Removing Operational Data & Merging Tables**
- **[DO]**: Merge the `INVOICE` header and `INVOICE_ITEM` detail into a single `CUSTOMER_INVOICES` table containing `invoice_id`, `invoice_item_seq_id`, `invoice_date`, `product_id`, `quantity`, and `amount`.
- **[DON'T]**: Include fields like `invoice_message`, `shipping_instructions`, or `invoice_status` in the `CUSTOMER_INVOICES` warehouse table.

**Principle: Adding an Element of Time & Stability-Based Separation**
- **[DO]**: Create a `CUSTOMERS` table for static data (Key: `customer_id`) and a `CUSTOMER_DEMOGRAPHICS` table for volatile data (Key: `customer_id`, `snapshot_date` containing `credit_rating`, `marital_status`).
- **[DON'T]**: Store `credit_rating` directly in the `CUSTOMERS` table without a snapshot date, which would either overwrite history or force redundant storage of the static customer name upon every credit rating change.

**Principle: Creating Relationship Artifacts**
- **[DO]**: Name the foreign key in the `CUSTOMER_INVOICES` table `billed_to_customer_id` to explicitly declare the role the party played in the transaction.
- **[DON'T]**: Bring over the generic `party_id` column from the operational system into the warehouse fact table, which would force the DSS user to join multiple role-resolution tables to figure out what the party did.

**Principle: Adding Derived Data**
- **[DO]**: Add an `extended_amount` column to the `CUSTOMER_INVOICES` warehouse table and populate it during the ETL process by multiplying `quantity` by `amount`.
- **[DON'T]**: Force the data mart or the end-user query tool to multiply `quantity` by `amount` every time a strategic sales report is run.

**Principle: Accommodating Levels of Granularity**
- **[DO]**: Store transactions at the lowest atomic level (e.g., individual `invoice_item_seq_id`) in the Enterprise Data Warehouse so that departmental data marts can independently decide whether to aggregate by day, week, or month.
- **[DON'T]**: Pre-aggregate the core Enterprise Data Warehouse tables up to the monthly level, stripping out the transaction IDs and permanently destroying the ability to drill down to the atomic data.