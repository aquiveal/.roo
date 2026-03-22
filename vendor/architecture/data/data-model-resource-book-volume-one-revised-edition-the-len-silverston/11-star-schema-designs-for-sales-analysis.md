@Domain
Triggered when the user requests database design, schema generation, data modeling, OLAP (Online Analytical Processing) design, multidimensional analysis structures, data mart development, or star schema designs specifically relating to Sales Analysis, Product Analysis, or Sales Representative Performance.

@Vocabulary
- **Data Mart**: A departmental data warehouse designed to handle the specific decision support needs of a particular department by taking a slice of the enterprise data warehouse.
- **Star Schema**: A database design containing a central Fact Table with relationships to several look-up tables called Dimensions, forming a star-like pattern. Used to facilitate easy slicing and dicing of data for multidimensional analysis.
- **Fact Table**: The central table in a star schema that contains foreign keys to various dimensions and columns to hold the quantitative data to be reported (Measures).
- **Dimension Table**: Look-up tables surrounding the fact table that provide descriptive attributes by which the facts can be queried, grouped, and analyzed (e.g., Time, Product, Customer).
- **Measure**: A quantitative column within a fact table upon which summaries, aggregations, and trend analyses are performed (e.g., `quantity`, `gross_sales`, `product_cost`).
- **Granularity**: The level of detail stored in a table. In star schemas, this refers to the specific intersection of dimension attributes that defines a single row in the fact table.
- **Drill-Through**: The analytical capability to map back from the summarized data in the data mart to the original, atomic-level transactions in the enterprise data warehouse.
- **Snapshot Data**: Dimension data captured exactly as it existed at the time of the transaction (e.g., customer demographics at the time of sale), regardless of current operational values.

@Objectives
- Design query-optimized, performant departmental data marts using star schema architectures.
- Extract and summarize atomic, transaction-level data from the enterprise data warehouse into multidimensional fact tables.
- Ensure dimension tables support standard business analysis roll-ups (e.g., geographic hierarchies, organizational structures, time periods).
- Avoid transactional granularity in star schemas to prevent complex many-to-many relationship issues and misleading aggregations.

@Guidelines

**Architectural Rules**
- The AI MUST design data marts as star schemas with a single central Fact Table holding Measures and a surrounding set of Dimension Tables.
- The AI MUST define the Primary Key of the Fact Table strictly as the combination (composite key) of all Foreign Keys pointing to its Dimension Tables.
- The AI MUST NOT use operational Transaction IDs (e.g., `invoice_id`, `invoice_item_id`) as the Primary Key of a Fact Table. Star schemas demand 1-to-many relationships from dimensions to facts; transactional keys violate this when complex many-to-many relationships exist (e.g., multiple sales reps splitting a single invoice).
- The AI MUST ensure all Measures in the Fact Table strictly align with the dimensionality of the table. If a dimension is removed from a schema (e.g., removing the Product dimension to view solely Sales Rep performance), the AI MUST remove all measures dependent on that dimension (e.g., `quantity` and `product_cost`).

**Dimension Design Rules**
- **Time Dimension**: The AI MUST include a Time dimension table (e.g., `TIME_BY_DAY` or `TIME_BY_MONTH`) containing explicit pre-calculated columns for time intervals (`fiscal_year`, `quarter`, `month`, `week`, `day`) rather than relying on runtime date extraction functions against the fact table.
- **Customer Demographics Dimension**: The AI MUST design demographics dimensions to store data *as it existed at the time of the sale*. 
  - The AI MUST use ranges for highly volatile continuous variables (e.g., `age` must be "20-25", not an exact integer) to manage dimension size.
- **Customer Dimension**: The AI MUST store current customer names and primary keys, separating them from volatile demographics.
- **Address/Geography Dimension**: The AI MUST create unique address records independent of the customer (e.g., `ADDRESSES` or `GEOGRAPHIC_BOUNDARIES`) to eliminate redundant data and allow geographic analysis across multiple entities.
- **Sales Rep Dimension**: The AI MAY include recursive foreign keys within a dimension (e.g., `manager_rep_id` within the `SALES_REPS` dimension) to allow hierarchical reporting without requiring a separate table for managers.

**Specific Schema Configurations**
- **Sales Analysis Data Mart**: Fact Table = `CUSTOMER_SALES`. Dimensions = `CUSTOMERS`, `CUSTOMER_DEMOGRAPHICS`, `INTERNAL_ORGANIZATIONS`, `SALES_REPS`, `ADDRESSES`, `PRODUCTS`, `TIME_BY_DAY`. Measures = `quantity`, `gross_sales`, `product_cost`.
- **Sales Rep Performance Data Mart**: Fact Table = `CUSTOMER_REP_SALES`. Dimensions = `SALES_REPS`, `CUSTOMERS`, `ADDRESSES`, `TIME_BY_MONTH`. Measures = `gross_sales` (Do NOT include `quantity` or `product_cost` as they are product-dependent).
- **Product Analysis Data Mart**: Fact Table = `PRODUCT_SALES`. Dimensions = `GEOGRAPHIC_BOUNDARIES` (City, State, Country), `PRODUCTS`, `TIME_BY_MONTH`. Measures = `quantity`, `gross_sales`, `product_cost`.

@Workflow
1. **Identify Business Questions**: Determine exactly what trends, summaries, or performance metrics the specific department needs to evaluate.
2. **Determine Schema Dimensions**: Select the appropriate dimension tables required to slice the data (e.g., Time, Product, Geographic Region). Drop any dimensions irrelevant to the specific analysis.
3. **Define Granularity**: Establish the level of detail based on the time dimension (e.g., daily vs. monthly) and intersection of selected dimensions. Summarize source data to this level.
4. **Select Measures**: Define the quantitative columns for the Fact Table. Rigorously check that no selected measure depends on a dimension that has been excluded from the schema.
5. **Construct Time Dimension**: Build the time lookup table mapping the chosen granularity (e.g., `day_id` or `month_id`) to business-relevant calendar/fiscal groupings.
6. **Design Demographics/Attributes**: Extract snapshots of volatile data (like credit ratings or age brackets) to attach to the fact table representing the state at the time of the event.

@Examples (Do's and Don'ts)

**Principle: Fact Table Primary Key Granularity**
- [DO]: Define the fact table primary key as a composite of its dimension foreign keys to hold pre-summarized data.
  ```sql
  CREATE TABLE CUSTOMER_SALES (
      product_id INT,
      sales_rep_id INT,
      customer_id INT,
      customer_demographics_id INT,
      internal_organization_id INT,
      address_id INT,
      day_id INT,
      quantity INT,
      gross_sales DECIMAL(15,2),
      product_cost DECIMAL(15,2),
      PRIMARY KEY (product_id, sales_rep_id, customer_id, customer_demographics_id, internal_organization_id, address_id, day_id)
  );
  ```
- [DON'T]: Design a star schema fact table centered on operational transactional keys, which breaks dimensional modeling paradigms when transactions split credit among multiple dimensions.
  ```sql
  CREATE TABLE TRANSACTIONAL_SALES_FACT (
      invoice_id INT,
      invoice_item_id INT,
      sales_rep_id INT, -- ANTI-PATTERN: Invoices might have multiple reps, breaking the 1-to-many rule
      gross_sales DECIMAL(15,2),
      PRIMARY KEY (invoice_id, invoice_item_id)
  );
  ```

**Principle: Validating Measures Against Dimensions**
- [DO]: Remove product-dependent measures when creating a high-level Sales Rep Performance data mart that drops the Product dimension.
  ```sql
  CREATE TABLE CUSTOMER_REP_SALES (
      sales_rep_id INT,
      customer_id INT,
      address_id INT,
      month_id INT,
      gross_sales DECIMAL(15,2), -- Notice quantity and product_cost are rightfully excluded
      PRIMARY KEY (sales_rep_id, customer_id, address_id, month_id)
  );
  ```
- [DON'T]: Include measures in a fact table that cannot be accurately aggregated because their defining dimension is missing.
  ```sql
  CREATE TABLE CUSTOMER_REP_SALES (
      sales_rep_id INT,
      customer_id INT,
      month_id INT,
      gross_sales DECIMAL(15,2),
      quantity INT, -- ANTI-PATTERN: Meaningless without the PRODUCT dimension
      product_cost DECIMAL(15,2) -- ANTI-PATTERN: Cannot sum costs accurately without knowing the product
  );
  ```

**Principle: Time Dimension Design**
- [DO]: Use a dedicated Time Dimension table to support complex, high-performance rollups by business intervals.
  ```sql
  CREATE TABLE TIME_BY_DAY (
      day_id INT PRIMARY KEY,
      full_date DATE,
      fiscal_year INT,
      calendar_year INT,
      quarter INT,
      month INT,
      week INT
  );
  ```
- [DON'T]: Store raw dates directly in the fact table expecting the BI tool or runtime SQL to dynamically group by fiscal quarters or weeks.

**Principle: Demographic Snapshot Ranges**
- [DO]: Use ranged values in demographic dimensions to prevent dimension table bloat.
  ```sql
  CREATE TABLE CUSTOMER_DEMOGRAPHICS (
      customer_demographics_id INT PRIMARY KEY,
      age_range VARCHAR(20), -- e.g., '20-25'
      marital_status VARCHAR(20),
      credit_rating VARCHAR(10)
  );
  ```
- [DON'T]: Store exact integer values for highly variable demographics in a dimension table.
  ```sql
  CREATE TABLE CUSTOMER_DEMOGRAPHICS (
      customer_demographics_id INT,
      exact_age INT, -- ANTI-PATTERN: Creates too many distinct rows in the dimension
      credit_score INT
  );
  ```