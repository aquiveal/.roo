@Domain
Trigger these rules when the user requests assistance with database design, logical data modeling, relational normalization, schema architecture, dimensional modeling (star schema/data warehousing design at the logical level), or analyzing and organizing attributes into entities.

@Vocabulary
- **Logical Data Model (LDM)**: A detailed business solution to a business problem that captures business requirements completely independent of implementation concerns such as software, hardware, or database platform.
- **Relational LDM**: A data modeling mindset that captures *how the business works* by precisely representing business rules, entities, attributes, and relationships.
- **Dimensional LDM**: A data modeling mindset that captures *how the business is monitored* by precisely representing navigation, measures, and hierarchies.
- **Normalization**: A formal process of asking business questions to apply a set of rules with the goal of organizing attributes.
- **Single-valued**: An attribute must contain only one piece of information.
- **Provides a fact**: A given primary key (PK) value will always return no more than one of every attribute identified by this key.
- **Completely (Minimal)**: The minimal set of attributes that uniquely identify an instance of the entity is present in the PK.
- **Only**: Each attribute must provide a fact about the PK and nothing else (no hidden dependencies).
- **Derived Attribute**: An attribute whose value is calculated from other attributes.
- **Repeating Attributes**: Two or more of the same attribute in the same entity (violates 1NF).
- **Multi-valued Attributes**: Storing at least two distinct values or business concepts hiding in one attribute (violates 1NF).
- **1NF (First Normal Form)**: Every attribute is single-valued.
- **2NF (Second Normal Form)**: Every attribute is a fact about the *whole* key.
- **3NF (Third Normal Form)**: Every attribute is a fact about *nothing but* the key.
- **Abstraction**: An optional technique of redefining and combining attributes, entities, and relationships into more generic terms (e.g., `Employee` -> `Party Role`).
- **Meter (Fact Table)**: An entity containing a related set of measures (a bucket of common measures) used to gauge the health of a business process.
- **Aggregate Fact**: Summarization containing information stored at a higher level of granularity than transaction details.
- **Atomic Fact**: Contains the lowest level of detail available in the business.
- **Cumulative Fact**: Captures how long it takes to complete a business process.
- **Snapshot Fact**: Contains time-related information detailing specific steps in the life of an entity.
- **Dimension**: A subject whose purpose is to add meaning to the measures (filtering, sorting, summing).
- **Fixed Dimension (Type 0 SCD)**: Contains values that do not change over time.
- **Degenerate Dimension**: A dimension whose attribute(s) have been moved directly to the fact table (e.g., transaction identifiers).
- **Multi-Valued Dimension**: Models a situation where there are multiple values for an attribute/column, weighted so the total adds up to one.
- **Ragged Dimension**: A hierarchy of indeterminate depth where the parent of at least one member is missing from the level immediately above.
- **Shrunken Dimension**: A version of the fact table containing non-measure attributes (e.g., large text strings stored separately for query efficiency).
- **Slowly Changing Dimension (SCD)**: Tracks history. Type 1 (current only), Type 2 (all history), Type 3 (current + some history), Type 6 (complex, combining 1, 2, and 3).
- **Snowflake**: Higher levels in a hierarchy representing how measures in a meter can be viewed at rolled-up levels (e.g., Month -> Quarter -> Year).

@Objectives
- Ensure all logical data models strictly represent business solutions independent of any physical technology (hardware/software).
- For Relational LDMs, ensure the AI rigorously applies normalization principles to guarantee every attribute is single-valued and provides a fact completely and only about its primary key.
- For Dimensional LDMs, ensure the AI properly isolates measures into discrete meters (facts) and descriptive attributes into appropriate dimensions and snowflakes.
- Balance the tradeoffs between rigidity (strict normalization) and flexibility (abstraction) deliberately, ensuring abstraction is only applied when justified by future extensibility needs.

@Guidelines
- **Relational LDM Enforcement**:
  - The AI MUST treat Normalization as a mandatory process of asking business questions.
  - The AI MUST actively query the user using specific template questions to determine 1NF, 2NF, and 3NF compliance.
  - The AI MUST resolve 1NF violations by isolating repeating groups into new entities and splitting multi-valued attributes into discrete attributes.
  - The AI MUST resolve 2NF violations by ensuring that composite primary keys contain only the absolute minimal set of attributes required for uniqueness.
  - The AI MUST resolve 3NF violations by removing calculated/derived attributes from the model entirely, or by creating a new entity with a different primary key for attributes dependent on non-PK attributes.
- **Abstraction Constraints**:
  - The AI MUST treat Abstraction as an optional technique.
  - Before applying abstraction, the AI MUST explicitly warn the user of the three specific costs: 1) Loss of communication (obscures explicit terms), 2) Loss of business rules (enforcement shifts to programming code), 3) Additional development complexity (complex ETL/population code).
- **Dimensional LDM Enforcement**:
  - The AI MUST classify every fact table/meter as exactly one of the following: Aggregate, Atomic, Cumulative, or Snapshot.
  - The AI MUST classify every dimension as exactly one of the following: Fixed, Degenerate, Multi-Valued, Ragged, Shrunken, or SCD (Type 0, 1, 2, 3, or 6).
  - The AI MUST derive dimensional snowflakes (hierarchies) properly, ensuring a lower level belongs to at most one higher level.

@Workflow
1. **Determine the Mindset**: The AI MUST first ask the user or determine from context whether the logical data model is Relational (capturing business rules) or Dimensional (capturing business monitoring/analytics).
2. **Relational LDM Normalization Process**:
   - **Step 1: Identify Initial Chaos**: Collect all proposed attributes regardless of entity assignment.
   - **Step 2: Apply 1NF (Single-Valued)**:
     - Ask: "Can a [Entity] have more than one [Attribute]?" If Yes -> Move to a new entity.
     - Ask: "Does [Attribute] contain more than one piece of business information?" If Yes -> Split the attribute.
   - **Step 3: Apply 2NF (Completely)**:
     - Ask: "Are all of the attributes in the primary key needed to retrieve a single instance of [Attribute]?" If No -> Adjust the PK to be minimal or move the attribute to the entity identified by the partial key.
   - **Step 4: Apply 3NF (Only)**:
     - Ask: "Is [Attribute] a fact about any other attribute in this same entity?" If Yes -> Remove derived attributes or create a new entity for the hidden dependency.
   - **Step 5: Evaluate Abstraction**: Ask if the entity is expected to frequently spawn new types in the near future. If yes, abstract (e.g., Employee -> Party Role) while noting the three specific costs.
3. **Dimensional LDM Structuring Process**:
   - **Step 1: Define the Meter (Fact)**: Isolate the business measures. Classify as Aggregate, Atomic, Cumulative, or Snapshot.
   - **Step 2: Define Dimensions**: Identify the context subjects. Classify as Fixed, Degenerate, Multi-Valued, Ragged, Shrunken, or define the SCD Type.
   - **Step 3: Define Snowflakes**: Map the dimension hierarchies (e.g., Branch Code -> Region -> Country) required for navigation.

@Examples (Do's and Don'ts)

**Principle: 1NF Single-Valued Attributes**
- [DO]: Split `Employee Name` into `Employee First Name` and `Employee Last Name`. Assign `Phone 1`, `Phone 2`, and `Phone 3` to appropriate distinct business concepts if they represent different things (e.g., `Employee Phone`, `Department Phone`, `Organization Phone`), OR move them to a new `Employee Phone` entity if they are just repeating instances of the same concept.
- [DON'T]: Leave `Employee Name` as a single attribute when the business requires querying by last name, or retain `Phone 1`, `Phone 2`, `Phone 3` as repeating attributes in the `Employee` entity.

**Principle: 3NF Hidden Dependencies and Derived Attributes**
- [DO]: Remove `Employee Vested Indicator` from the `Employee` entity if the vesting status is calculated purely based on `Employee Start Date`.
- [DON'T]: Store `Order On Time Indicator` in the `Order` entity if it is mathematically derived by comparing `Order Actual Delivery Date` and `Order Scheduled Delivery Date`.

**Principle: Abstraction**
- [DO]: Abstract `Employee` and `Consumer` into `Party Role` ONLY IF the user confirms that new roles (like `Contractor`, `Vendor`) will be continually added, and accept that explicit business rules (like "Employees must have a Start Date") will now have to be enforced via application code.
- [DON'T]: Abstract structures by default without warning the user that it causes Loss of Communication, Loss of Business Rules, and Additional Development Complexity.

**Principle: Dimensional Modeling Fact Classification**
- [DO]: Label `Account Balance` as an Aggregate Meter (Fact), and label `Gender` as a Fixed Dimension (SCD Type 0).
- [DON'T]: Mix transaction ID numbers as standard dimensions; they MUST be categorized as Degenerate Dimensions housed directly inside the Fact table.