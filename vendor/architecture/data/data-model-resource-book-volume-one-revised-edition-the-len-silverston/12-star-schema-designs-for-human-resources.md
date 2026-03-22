# @Domain
These rules MUST be triggered when the AI is tasked with designing, analyzing, refactoring, or generating SQL code for Human Resources (HR) data warehouses, data marts, EEOC (Equal Employment Opportunity Commission) compliance reporting, multidimensional HR data models, or HR-specific star schemas.

# @Vocabulary
*   **Star Schema**: A database design containing a central fact table surrounded by lookup tables called dimensions, optimized for multidimensional analysis.
*   **Data Mart**: A departmental data warehouse that takes a slice of the enterprise data warehouse for easy analysis by specific end users (e.g., the EEOC division).
*   **Fact Table**: The central table in a star schema containing keys to dimension tables and the numeric measures to be analyzed.
*   **Measure**: A numeric value stored in a fact table used for summaries and trend analysis (e.g., counts, averages).
*   **Dimension Table**: A table used to group, filter, and constrain fact data (e.g., Organizations, Position Types, Genders).
*   **EEOC Category / Type**: Classifications of race/ethnicity used for compliance reporting (e.g., white, Hispanic, African-American, Asian, Native American).
*   **Level 1 Organization**: The lowest level unit in a flattened organizational hierarchy structure used for dimension modeling.
*   **Snapshot**: A view of the enterprise's data at a specific point in time (e.g., month-end) rather than a transactional record.
*   **Higher Level of Granularization**: A secondary, more summarized fact table created to optimize query performance and provide data security by restricting access to sensitive detailed data.

# @Objectives
*   Design HR star schemas that answer complex demographic, salary, performance, and tenure questions (e.g., average salary by gender and EEOC category, tenure by position type).
*   Model HR facts as periodic snapshots (e.g., month-end) rather than individual transactions.
*   Structure organizational dimensions as flattened hierarchies to prevent recursive queries and enhance performance.
*   Provide multiple levels of granularity by generating both a detailed HR fact table and a summarized HR fact table to address performance and data security requirements.

# @Guidelines
*   **Fact Table Key Definition**: The AI MUST define the primary key of any HR fact table as the combination of the primary keys of all its associated dimension tables.
*   **Monthly Snapshot Grain**: The AI MUST model HR fact tables (e.g., `HUMAN_RESOURCES_FACT`) to be loaded periodically (e.g., at the end of each month) using a `TIME_BY_MONTH` dimension.
*   **Required HR Measures**: When creating a detailed HR fact table, the AI MUST include the following specific measures:
    *   `number_of_employees`: The count of employees meeting the dimension criteria.
    *   `average_age`: The mean age of the employees.
    *   `average_years_experience`: The mean number of years of total work experience (both inside and outside the enterprise).
    *   `average_years_employed`: The average tenure/number of years employed specifically by the enterprise.
    *   `average_annual_pay`: The annualized salary at the time the snapshot was taken.
*   **Required HR Dimensions**: The detailed HR star schema MUST include the following dimensions: `ORGANIZATIONS`, `POSITION_TYPES`, `GENDERS`, `LENGTH_OF_SERVICES`, `STATUSES`, `PAY_GRADES`, `EEOC_TYPES`, and `TIME_BY_MONTH`.
*   **Flattened Organizational Hierarchy**: The AI MUST denormalize the `ORGANIZATIONS` dimension to store the hierarchy (e.g., `level1_org_type`, `level2_org_type`, `level1_name`, `level2_name`). The AI MUST NOT include IDs for higher-level organizations; only the lowest level (`organization_id` for Level 1) is kept as the identifier.
*   **Specific Gender Classifications**: The AI MUST define the `GENDERS` dimension using exactly these five categories: "male", "female", "male to female", "female to male", and "not provided".
*   **Length of Service Grouping**: The AI MUST utilize a `LENGTH_OF_SERVICES` dimension to group tenure into ranges (e.g., 5-9 years, 10-15 years) to allow analysis in conjunction with the `average_years_employed` measure.
*   **Status Groupings**: The AI MUST include a `STATUSES` dimension to track employment states (e.g., part-time, full-time, exempt, temporary).
*   **Summary Fact Tables**: The AI MUST design a higher-level summary fact table (e.g., `HUMAN_RESOURCES_SUMMARY_FACT`) when requested, which drops granular dimensions (like Length of Service, Statuses, and Pay Grades) while retaining broader dimensions (`ORGANIZATIONS`, `POSITION_TYPES`, `EEOC_TYPES`, `GENDERS`). 
*   **Summary Table Rationale**: The AI MUST justify the creation of summary fact tables based on two factors: optimizing query performance and providing data security (restricting sensitive HR data from certain groups of individuals).
*   **Iterative Requirements Gathering**: The AI MUST prompt the user for their specific HR reporting requirements (e.g., "What specific demographic or salary trends do you need to analyze?") before finalizing the schema, ensuring the design matches the business questions.

# @Workflow
1.  **Requirement Analysis**: Identify the specific HR questions the data mart must answer (e.g., salary disparities by gender/race, employee tenure distribution).
2.  **Grain Definition**: Establish the snapshot period. Define the time dimension strictly as `TIME_BY_MONTH` (fiscal year and month combination).
3.  **Dimension Construction**: 
    *   Flatten the `ORGANIZATIONS` hierarchy into a single table with level-based columns.
    *   Define `GENDERS` with the 5 mandated categories.
    *   Define `EEOC_TYPES`, `POSITION_TYPES`, `STATUSES`, `PAY_GRADES`, and `LENGTH_OF_SERVICES`.
4.  **Detailed Fact Construction**: Create `HUMAN_RESOURCES_FACT`. Assign the primary key as the composite of all dimension foreign keys. Add the 5 mandated average/count measures.
5.  **Summary Fact Construction**: Create `HUMAN_RESOURCES_SUMMARY_FACT`. Select only the high-level dimensions (`ORGANIZATIONS`, `POSITION_TYPES`, `EEOC_TYPES`, `GENDERS`). Re-aggregate the 5 measures over this broader range to ensure performance and secure sensitive data.

# @Examples (Do's and Don'ts)

**[DO]** Flatten organizational hierarchies in the dimension table to avoid recursive joins in the data mart.
```sql
CREATE TABLE ORGANIZATIONS_DIM (
    organization_id INT PRIMARY KEY, -- ID only for the lowest level
    level1_name VARCHAR(100),
    level1_org_type VARCHAR(50),
    level2_name VARCHAR(100),
    level2_org_type VARCHAR(50),
    level3_name VARCHAR(100),
    level3_org_type VARCHAR(50)
);
```

**[DON'T]** Use a recursive relationship (e.g., `parent_organization_id`) in a star schema dimension, as it forces the end-user or DSS tool to execute complex recursive queries.
```sql
-- INCORRECT: Recursive dimension
CREATE TABLE ORGANIZATIONS_DIM (
    organization_id INT PRIMARY KEY,
    organization_name VARCHAR(100),
    parent_organization_id INT -- Do not do this in a star schema
);
```

**[DO]** Define the primary key of the HR Fact table as the combination of all dimension keys.
```sql
CREATE TABLE HUMAN_RESOURCES_FACT (
    month_id INT,
    organization_id INT,
    position_type_id INT,
    gender_id INT,
    length_of_service_id INT,
    status_id INT,
    pay_grade_id INT,
    eeoc_type_id INT,
    number_of_employees INT,
    average_age DECIMAL(5,2),
    average_years_experience DECIMAL(5,2),
    average_years_employed DECIMAL(5,2),
    average_annual_pay DECIMAL(15,2),
    PRIMARY KEY (month_id, organization_id, position_type_id, gender_id, length_of_service_id, status_id, pay_grade_id, eeoc_type_id)
);
```

**[DON'T]** Store transactional HR events (like individual paychecks or daily status changes) in the HR data mart fact table. The grain MUST be a periodic snapshot (e.g., month-end balances/averages).

**[DO]** Differentiate between `average_years_experience` (total career experience) and `average_years_employed` (tenure at the specific company) as distinct measures in the fact table.

**[DON'T]** Omit non-binary gender classifications. Always include the 5 specific statuses: "male", "female", "male to female", "female to male", and "not provided".