# @Domain
These rules MUST trigger whenever the AI is tasked with designing, generating, analyzing, or querying data warehouse (DW) models, data marts, or star schemas specifically targeting Inventory Management, Purchase Orders, Shipments/Logistics, Work Efforts, or Financial Accounting. 

# @Vocabulary
*   **Star Schema**: A multidimensional database design containing a central fact table surrounded by several dimension (look-up) tables.
*   **Fact Table**: The central table in a star schema containing foreign keys to dimension tables and quantitative measures (facts) used for analysis.
*   **Dimension**: A look-up table containing descriptive attributes used to slice, dice, and group data (e.g., Time, Location, Organization, Product).
*   **Measure**: Quantitative, numeric data stored in the fact table (e.g., quantity, amount, cost) used for aggregation.
*   **Geo Level**: A flexible hierarchical representation of geography within a dimension (e.g., city, state, country, or state, country, continent).
*   **Org Level**: A flexible hierarchical representation of an organization within a dimension (e.g., department, division, parent company).
*   **Part**: A raw material, subassembly, or finished good tracked in inventory (interchangeable with "Good" if parts are not explicitly tracked).
*   **Inventory Management Analysis**: Analysis of inventory balances, commitments, optimizations, forecasting, receipts, issues, scrap, and costs.
*   **Purchase Order Analysis**: Evaluation of purchasing metrics, including prices, supplier discounts, supplier promptness (lead times/days late), buyer negotiation effectiveness, and cost center allocations.
*   **Shipment Analysis**: Logistics evaluation covering all shipment types (customer, purchase, transfer, drop), tracking delivery expectations, late shipments, damaged/rejected goods, and freight costs.
*   **Work Effort Analysis**: Evaluation of project/task success, on-time/on-budget performance, actual vs. estimated labor and material costs, and resource performance.
*   **Financial Analysis**: Evaluation of accounting transactions centered on General Ledger (GL) accounts, balance sheets, income statements, cash flow, and financial ratios (debt to equity, current assets, liquidity ratio).

# @Objectives
*   Construct highly optimized, domain-specific star schemas that directly answer core strategic business questions outlined for the five key analysis areas.
*   Establish explicit, flexible hierarchical structures for geographic and organizational dimensions to allow dynamic roll-up and drill-down analysis.
*   Ensure all fact tables contain the correct grain and precisely defined quantitative measures required for the specific subject area.
*   Drive data warehouse design by mapping operational data entities (from corresponding logical data models) to analytical fact and dimension structures.

# @Guidelines
*   **General Star Schema Design Rules:**
    *   The AI MUST ensure every star schema contains a central fact table connected to multiple dimension tables via one-to-many relationships.
    *   The AI MUST include a Time dimension in EVERY star schema design (e.g., `TIME_BY_DAY`, `TIME_BY_MONTH`).
    *   The AI MUST NEVER store operational text descriptions, unstructured notes, or volatile attributes in the fact table. Fact tables MUST contain only keys and numeric measures.
    *   The AI MUST implement `geo_level` columns (e.g., `geo_level_1`, `geo_level_2`) in location dimensions to support flexible geographic hierarchies.
    *   The AI MUST implement `org_level` and `level_org_type` columns in organization dimensions to support flexible corporate hierarchies.
*   **Inventory Management Analysis Rules:**
    *   The AI MUST source Inventory schemas from physical Part/Good entities and Shipment entities.
    *   The AI MUST include the following measures in the Inventory Fact Table: quantity on hand, quantity committed, quantity shipped, quantity received, quantity issued, quantity scrapped, inventory count, item valuation, and inventory costs.
    *   The AI MUST include dimensions for Part/Good, Facility, Internal Organization, and Time.
*   **Purchase Order Analysis Rules:**
    *   The AI MUST include dimensions for Supplier, Internal Organization, Product, and Time.
    *   The AI MUST include measures in the PO Fact Table for: PO quantity, average price, discount amounts, freight amounts, days late (supplier promptness), and lead time days.
    *   The AI MUST ensure the schema supports querying PO allocations by cost center and buyer effectiveness.
*   **Shipment (Logistics) Analysis Rules:**
    *   The AI MUST ensure the Shipment schema accounts for ALL shipment types (customer shipments, purchase shipments, transfers, drop shipments).
    *   The AI MUST include dimensions for Carrier, Facility (From/To), Product/Good, and Time.
    *   The AI MUST include measures in the Shipment Fact Table for: `quantity_damaged`, `quantity_rejected`, `freight_amount`, and late delivery days.
*   **Work Effort Analysis Rules:**
    *   The AI MUST include dimensions for Facility, Project Manager/Party, Work Effort Type, and Time.
    *   The AI MUST include measures in the Work Effort Fact Table that compare actuals vs. estimates: `actual_labor_cost`, `estimated_labor_cost`, `actual_material_cost`, `estimated_material_cost`, `actual_total_cost`, `estimated_total_cost`, and time spent (duration).
*   **Financial Analysis Rules:**
    *   The AI MUST center the Financial Fact Table around summarized Accounting Transactions.
    *   The AI MUST include dimensions for `GENERAL_LEDGER_ACCOUNTS`, `INTERNAL_ORGANIZATIONS`, `LOCATIONS`, and `TIME_BY_MONTH`.
    *   The AI MUST design the schema to support the calculation of key financial ratios: debt to equity, current assets, and liquidity ratio.
    *   The AI MUST track both income and expense account variances over time.

# @Workflow
1.  **Determine Analysis Domain**: Analyze the user's request and categorize it into one of the target domains (Inventory, Purchase Order, Shipment, Work Effort, Financial).
2.  **Define Business Questions**: Map the requirements to the standard business questions for that domain (e.g., "How many shipments are late by which carriers?" for Shipment Analysis).
3.  **Construct Dimensions**:
    *   Identify necessary look-up tables.
    *   Inject `geo_level` hierarchies for location-based dimensions.
    *   Inject `org_level` hierarchies for internal organization dimensions.
    *   Define the Time dimension at the appropriate grain (Day or Month).
4.  **Construct Fact Table**:
    *   Define the composite primary key utilizing the foreign keys from all associated dimensions.
    *   Add the domain-specific quantitative measures (e.g., `freight_amount`, `actual_labor_cost`).
5.  **Validate Analytical Capability**: Verify that the generated star schema can successfully execute queries to answer all defined business questions (e.g., ensuring financial ratios can be calculated from the Financial Fact Table).

# @Examples (Do's and Don't's)

**Dimension Hierarchy Design**
*   [DO] Design dimension tables with flexible hierarchy columns:
    ```sql
    CREATE TABLE INTERNAL_ORGANIZATIONS_DIM (
        internal_org_id INT PRIMARY KEY,
        org_name VARCHAR(100),
        level1_org_type VARCHAR(50), /* e.g., Department */
        level2_org_type VARCHAR(50), /* e.g., Division */
        level3_org_type VARCHAR(50)  /* e.g., Parent Company */
    );
    ```
*   [DON'T] Hardcode rigid, flat organization tables that cannot roll up:
    ```sql
    CREATE TABLE INTERNAL_ORGANIZATIONS_DIM (
        internal_org_id INT PRIMARY KEY,
        department_name VARCHAR(100) /* Cannot roll up to division or parent company */
    );
    ```

**Shipment Fact Table Construction**
*   [DO] Include measures for quality and logistics costs across all shipment types:
    ```sql
    CREATE TABLE SHIPMENT_FACT (
        shipment_id INT,
        carrier_id INT,
        product_id INT,
        time_id INT,
        quantity_shipped DECIMAL,
        quantity_damaged DECIMAL,
        quantity_rejected DECIMAL,
        freight_amount DECIMAL,
        days_late INT,
        PRIMARY KEY (shipment_id, carrier_id, product_id, time_id)
    );
    ```
*   [DON'T] Create a shipment fact table that only tracks successful customer deliveries without cost or failure metrics:
    ```sql
    CREATE TABLE SHIPMENT_FACT (
        shipment_id INT,
        customer_id INT,
        quantity_delivered DECIMAL
        /* Missing carrier, damage metrics, rejection metrics, and freight costs */
    );
    ```

**Work Effort Fact Table Construction**
*   [DO] Include comparison metrics for actual vs. estimated costs:
    ```sql
    CREATE TABLE WORK_EFFORT_FACT (
        work_effort_id INT,
        facility_id INT,
        pm_party_id INT,
        time_id INT,
        actual_labor_cost DECIMAL,
        estimated_labor_cost DECIMAL,
        actual_material_cost DECIMAL,
        estimated_material_cost DECIMAL,
        time_spent_hours DECIMAL
    );
    ```
*   [DON'T] Only track the final cost, preventing variance analysis:
    ```sql
    CREATE TABLE WORK_EFFORT_FACT (
        work_effort_id INT,
        total_cost DECIMAL /* Cannot determine if labor or materials caused budget overruns */
    );
    ```