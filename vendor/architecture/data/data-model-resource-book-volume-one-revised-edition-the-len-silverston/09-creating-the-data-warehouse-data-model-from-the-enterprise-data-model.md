# @Domain

These rules MUST trigger whenever the AI is tasked with data warehouse architecture, converting a logical or Enterprise Data Model (EDM) into a Data Warehouse (DW) design, generating dimensional models, designing Data Marts, establishing Decision Support System (DSS) structures, or restructuring normalized relational databases into optimized analytical databases.

# @Vocabulary

*   **Enterprise Data Model (EDM)**: The highly normalized, integrated, corporate-wide logical data model providing the foundation for both operational systems and the data warehouse.
*   **Data Warehouse Design (DW)**: An integrated, subject-oriented, highly granular database design derived from the EDM, acting as the single central source of truth for the decision support environment.
*   **Data Mart (Departmental Data Warehouse)**: A subset or summarized extraction of data built specifically for departmental analysis, sourced strictly from the central Data Warehouse.
*   **Decision Support System (DSS)**: The environment and applications used by executives and analysts to extract strategic information, synonymous with the usage of the Data Warehouse.
*   **Process Models**: Models concerning functional decomposition, data flow diagrams, or pseudocode; strictly applicable to operational environments and strictly ignored in DW design.
*   **Relationship Artifact**: A static, captured instance of a relationship as it existed at a specific moment in time (a snapshot), used in DWs to replace live operational foreign-key relationships.
*   **Granularity**: The level of detail or summarization of the data (e.g., daily transaction level vs. monthly summary level).
*   **Snapshot**: A record of data and its relationship artifacts captured at a specific moment, typically incorporating a date into its primary key.
*   **Stability / Volatility**: The propensity or rate of change of data attributes, used to segregate tables in the DW.
*   **Array of Data**: A repeating group of columns within a single table row, used in DW design when occurrences are highly predictable and fixed (e.g., 12 months in a year).

# @Objectives

*   The AI MUST convert normalized, operational Enterprise Data Models into optimized, analytical Data Warehouse designs.
*   The AI MUST strictly enforce the "Architected Data Warehouse Environment" pipeline: Operational -> Enterprise Data Model -> Data Warehouse -> Departmental Data Mart.
*   The AI MUST systematically apply the 8 designated transformation steps to convert EDM structures to DW structures.
*   The AI MUST balance query performance, database volume (VLDB concerns), and historical accuracy through the strategic use of snapshots, derived data, and artifacts.

# @Guidelines

*   **Architectural Pipeline Enforcement**: The AI MUST NEVER design a Departmental Data Mart that extracts directly from operational sources. All Data Marts MUST source their data from the central, integrated Data Warehouse.
*   **Scope Iteration**: The AI MUST build the Data Warehouse iteratively, one major subject area at a time (e.g., "Product" first, then "Orders"), rather than attempting a massive, all-at-once enterprise transformation.
*   **Exclusion of Process Models**: When designing the DW, the AI MUST explicitly ignore operational process models (functional decomposition, HIPO charts, state transition diagrams). The DW design relies solely on the EDM (Entities, Keys, Attributes, Subtypes, Relationships).
*   **Strict Application of Transformation Steps**: The AI MUST apply the 8 transformation criteria generally in the specified sequence (Operational removal first, Stability grouping last), though minor iterations are permitted.
*   **Relationship Artifact Handling**: Because traditional data modeling assumes a single business value for a relationship (current state), the AI MUST use artifacts (storing historical states via snapshots or discrete historical transaction records) to capture relationships that change over time.
*   **Table Merging Criteria**: The AI MUST ONLY merge two normalized tables into one DW table if they meet ALL three conditions: 1) They share a common key, 2) The data is queried/used together frequently, 3) The pattern of insertion is roughly the same.
*   **Array Creation Criteria**: The AI MUST ONLY use arrays (repeating groups) in a DW table if ALL four conditions are met: 1) The number of occurrences is predictable, 2) Occurrences are small in physical size, 3) Occurrences are frequently queried together, 4) The pattern of insertion/deletion is stable.

# @Workflow

When instructed to create or review a Data Warehouse design from an existing logical model, the AI MUST execute the following algorithmic process:

1.  **Step 0: EDM Validation**: Verify the source EDM contains required definitions: Major subjects, Entities, Keys, Attributes, Subtypes, and Relationships.
2.  **Step 1: Removing Operational Data**: Scan the source entities and aggressively remove any purely operational attributes (e.g., UI messages, transaction statuses, workflow descriptions) that have no reasonable chance of being queried for strategic DSS analysis.
3.  **Step 2: Adding an Element of Time**: Append a time element to the Primary Key of the DW table if one does not exist. Use either a discrete `snapshot_date` or continuous `from_date` / `thru_date` columns to ensure historical data tracking.
4.  **Step 3: Adding Derived Data**: Identify calculations frequently performed on access (e.g., `total_amount` = `quantity` * `amount`). Add these derived columns directly into the DW model to save processing time and ensure algorithmic consistency.
5.  **Step 4: Creating Relationship Artifacts**: Identify operational foreign key relationships that change over time. Replace or supplement them with textual/descriptive artifacts directly in the snapshot table (e.g., storing `primary_supplier_name` and `supplier_location` directly on a Product snapshot).
6.  **Step 5: Changing Granularity of Data**: Determine if the detailed operational data should be summarized. If yes, aggregate the data by time period (e.g., daily to monthly) or geographic dimension, evaluating the trade-off between keeping granular details vs. VLDB storage/performance costs.
7.  **Step 6: Merging Tables**: Evaluate parent-child or 1-to-1 operational tables (e.g., `INVOICE` and `INVOICE_ITEM`). If they share a key, are inserted together, and queried together, flatten and merge them into a single DW table.
8.  **Step 7: Creation of Arrays**: Identify periodic operational records (e.g., 12 monthly budget rows per year). Pivot these rows into a single arrayed DW row (e.g., one row per year, with columns `month_1_budget` through `month_12_budget`) to reduce index size and improve physical I/O.
9.  **Step 8: Organizing by Stability**: Analyze the remaining DW table attributes for their propensity to change. Split tables into separate structures based on volatility (e.g., isolate slowly changing attributes like `date_of_birth` into one table, and rapidly changing attributes like `customer_status` into another) to prevent massive redundancy during snapshots.

# @Examples (Do's and Don'ts)

### Step 1: Removing Operational Data
*   [DO]: Drop `error_message`, `print_status`, and `approval_routing_code` when creating the DW `INVOICE` table.
*   [DON'T]: Bring every operational attribute into the DW using the excuse that "someone might use it for DSS someday."

### Step 2: Adding an Element of Time
*   [DO]: Define the DW `CUSTOMER` table Primary Key as a composite of `customer_id` AND `snapshot_date`.
*   [DON'T]: Use only `customer_id` as the primary key, which would force the DW to constantly overwrite historical demographic profiles with current operational data.

### Step 3: Adding Derived Data
*   [DO]: Add `total_invoice_amount` to the DW table by calculating it during the ETL process, so every DSS query doesn't have to perform the math.
*   [DON'T]: Omit derived data out of a misguided adherence to 3rd Normal Form (3NF) logical modeling practices.

### Step 4: Creating Relationship Artifacts
*   [DO]: Store `primary_supplier_name` directly as a text column in the `PRODUCT_SNAPSHOT` table, preserving the supplier's name as it was at that exact moment in time.
*   [DON'T]: Only store `supplier_id` in the snapshot, which would cause historical queries to retrieve the *current* supplier name if a join is performed against the live supplier table.

### Step 6: Merging Tables
*   [DO]: Merge operational `ORDER_HEADER` and `ORDER_LINE` into a single `DW_ORDER_FACT` table because they share an order ID, are inserted simultaneously, and are nearly always queried together.
*   [DON'T]: Merge `CUSTOMER` and `ORDER` tables; they have vastly different insertion patterns (orders are inserted continuously, customers are inserted once).

### Step 7: Creation of Arrays of Data
*   [DO]: Design a DW `BUDGET` table with a Primary Key of `budget_id` and `year`, and columns `jan_amount`, `feb_amount`, `mar_amount`, etc., to save 25% of table space and reduce I/O.
*   [DON'T]: Create an array for unpredictable, unbounded occurrences, such as `order_item_1`, `order_item_2`... `order_item_N`.

### Step 8: Organizing Data According to Its Stability
*   [DO]: Split DW `CUSTOMER_SNAPSHOT` into two tables: `CUSTOMER_STATIC` (containing `date_of_birth`, `gender`) and `CUSTOMER_VOLATILE` (containing `current_account_balance`, `frequent_shopper_status`).
*   [DON'T]: Keep rapidly changing fields in the same table as static fields, causing the system to replicate static data million of times just to record a daily balance change.