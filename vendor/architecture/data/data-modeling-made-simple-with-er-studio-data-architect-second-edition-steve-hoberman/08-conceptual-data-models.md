# @Domain
Trigger these rules when the user requests assistance with creating, analyzing, or refining a Conceptual Data Model (CDM), identifying high-level business concepts, scoping a new application or database project, gathering initial data requirements, mapping business rules, or designing high-level dimensional/analytical reporting requirements. 

# @Vocabulary
*   **Concept**: A key idea that is both basic (mentioned many times a day by the audience) and critical (the business would be very different or non-existent without it) to the specific audience.
*   **Conceptual Data Model (CDM)**: A one-page data model that captures the business need and project scope for a particular audience, limited to the top (roughly 20) essential concepts, their definitions, and their high-level relationships (including many-to-many).
*   **Relational CDM**: A CDM that captures how the business works by precisely representing business rules.
*   **Dimensional CDM**: A CDM that captures how the business is monitored by precisely representing navigation, measures, and levels of granularity.
*   **Concept Template**: A categorization matrix used in Relational CDMs to identify concepts across six categories: Who, What, When, Where, Why, and How.
*   **Grain Matrix**: A spreadsheet matrix used in Dimensional CDMs where measures from business questions become columns and the dimensional levels become rows.
*   **Meter (Fact Table)**: An entity in a dimensional model containing a related set of measures (a bucket of common measures) used to measure the health of a business process (e.g., Sales). Symbolized by a graph icon.
*   **Dimension**: A subject whose purpose is to add meaning to the measures in a dimensional model, allowing users to filter, sort, and sum measures. Symbolized by a 3-horizontal-lines icon.
*   **Snowflake**: Higher levels in a hierarchy within a dimensional model (e.g., navigating from Region up to Country). Symbolized by a snowflake icon.
*   **Hierarchy**: A structure where an entity instance is a child of at most one other entity instance (e.g., a month belongs to only one year).
*   **Axis Technique**: A visual display format for dimensional CDMs where the measured business process is in the center, axes represent dimensions, and notches on the axes represent levels of detail.
*   **Business Sketch**: A visual display format for non-technical audiences using pictures, intuitive shapes, and buttons instead of traditional data modeling rectangles and crows-feet.

# @Objectives
*   Keep the CDM restricted to a "one-pager" representing only the highest-level, most critical concepts (rule of thumb: ~20 concepts max) to enforce scope and avoid logical/physical level clutter.
*   Define every concept thoroughly and completely to prevent downstream misinterpretation and to build a strong foundation for logical and physical modeling.
*   Distinguish clearly between capturing business rules (Relational) and capturing analytical navigation/questions (Dimensional).
*   Facilitate broad understanding, define application scope, enable proactive analysis, and build rapport between business and IT.
*   Tailor the output format exactly to the technical proficiency of the target audience (Validator and Users).

# @Guidelines
*   **Scope and Size Constraint**: The AI MUST limit the CDM to approximately 20 top-level concepts. If the user provides more, the AI MUST group lower-level details into higher-level concepts (e.g., grouping `Order Line` into `Order` for a high-level view).
*   **Categorization Rule**: When identifying Relational concepts, the AI MUST classify them into one of six categories: Who, What, When, Where, Why, or How.
*   **Definition Mandate**: The AI MUST generate or request a clear, explicit business definition for *every* concept on the CDM. The AI MUST NOT leave any concept undefined.
*   **Relational vs. Dimensional Branching**: The AI MUST determine whether the goal is application/operational data (Relational) or analytics/reporting (Dimensional) and apply the correct methodology.
*   **Relational Relationships Rule**: The AI MUST support and allow many-to-many relationships at the conceptual level.
*   **Dimensional Structure Rule**: The AI MUST model dimensional concepts explicitly using Meters (facts), Dimensions (direct filters), and Snowflakes (hierarchical roll-ups).
*   **Format Adaptation**: The AI MUST adapt the visual/textual representation of the CDM based on the audience. For technical audiences, use traditional entity/relationship notation. For non-technical audiences, the AI MUST use or simulate a Business Sketch or the Axis Technique.

# @Workflow
When tasked with creating or analyzing a Conceptual Data Model, the AI MUST execute the following 5-step algorithm:

**Step 1: Ask the Five Strategic Questions**
Before defining any entities, the AI MUST elicit or infer the answers to:
1. *What is the application going to do?* (Establish exact scope).
2. *"As is" or "to be"?* (Current state vs. proposed state).
3. *Is analytics a requirement?* (Determines Relational vs. Dimensional path).
4. *Who is the audience?* (Identifies the validator and user to determine technical format).
5. *Flexibility or simplicity?* (Determines whether to use generic abstract concepts like "Event" or specific ones like "Order").

**Step 2: Identify and Define the Concepts**
*   *If Relational*: The AI MUST generate a Concept Template filling in concepts under Who (e.g., Customer), What (e.g., Product), When (e.g., Fiscal Period), Where (e.g., Branch), Why (e.g., Order), and How (e.g., Invoice). The AI MUST then write comprehensive definitions for each.
*   *If Dimensional*: The AI MUST request or generate specific business questions (e.g., "Show me X by Y over Z timeframe").

**Step 3: Capture the Relationships**
*   *If Relational*: For every pair of related concepts, the AI MUST answer 8 specific questions:
    1. Can Entity A be related to more than one Entity B? (Participation/Many)
    2. Can Entity B be related to more than one Entity A? (Participation/Many)
    3. Can Entity A exist without Entity B? (Optionality/Zero)
    4. Can Entity B exist without Entity A? (Optionality/Zero)
    5. Are there examples of Entity A that would be valuable to show? (Subtyping)
    6. Are there examples of Entity B that would be valuable to show? (Subtyping)
    7. Does Entity A go through a lifecycle? (Subtyping)
    8. Does Entity B go through a lifecycle? (Subtyping)
*   *If Dimensional*: The AI MUST parse the business questions and create a Grain Matrix. Map the Measures as Columns and the Dimensional Levels (navigational paths) as Rows.

**Step 4: Determine the Most Useful Form**
Based on the audience identified in Step 1:
*   *If Relational & Technical*: Output standard entities, relationships, and cardinalities.
*   *If Relational & Non-Technical*: Output a descriptive "Business Sketch" outline using analogies, shapes, and real-world documents instead of database terminology.
*   *If Dimensional & Technical*: Output standard Meter, Dimension, and Snowflake definitions.
*   *If Dimensional & Non-Technical*: Output an "Axis Technique" representation (Meter in center, Dimensions as radiating axes with notches for hierarchies).

**Step 5: Review and Confirm**
The AI MUST present the CDM to the user for validation. If the user identifies missing scope or incorrect definitions, the AI MUST return to Step 2 and iterate.

# @Examples (Do's and Don'ts)

### 1. Concept Selection and Scope
*   **[DO]**: Limit the CDM to top-level concepts. *Example:* `Order`, `Customer`, `Product`, `Invoice`.
*   **[DON'T]**: Clutter the CDM with low-level logical details. *Example:* Adding `Order Line`, `Customer Address`, `Product Description`, `Invoice Discount`.

### 2. Concept Definitions
*   **[DO]**: Provide deep, unambiguous definitions. *Example:* "Customer: A person or organization who obtains our product for resale. Prospects are not customers. Once a customer, always a customer, regardless of inactivity."
*   **[DON'T]**: Provide weak, circular definitions. *Example:* "Customer: Someone who is a customer of the company."

### 3. Relational Concept Template (Step 2)
*   **[DO]**: Categorize concepts systematically:
    *   *Who*: Customer, Employee
    *   *What*: Account, Product
    *   *When*: Account Open Date, Fiscal Quarter
    *   *Where*: Branch, Region
    *   *Why*: Deposit, Withdrawal
    *   *How*: Bank Statement, Deposit Slip
*   **[DON'T]**: List concepts randomly without verifying they cover the Who, What, When, Where, Why, and How of the business process.

### 4. Dimensional Grain Matrix (Step 3)
*   **[DO]**: Build a grid to parse business questions.
    *   *Business Question:* "Show me student count by department and semester."
    *   *Measure (Column):* Student Count
    *   *Dimension Level (Row):* Semester, Department
*   **[DON'T]**: Map physical tables or foreign keys when designing dimensional conceptual requirements. 

### 5. Audience-Driven Presentation (Step 4)
*   **[DO]**: For a non-technical business user, use the Axis Technique for analytics. *Example Output:* "At the center of our board is the 'Student Attrition' meter. Radiating out are axes: The Time axis has notches for Semester and Year. The Geography axis has notches for Campus and State."
*   **[DON'T]**: Present an IDEF1X or IE Crows-Foot normalized diagram to a non-technical marketing executive who just needs to understand business concepts.