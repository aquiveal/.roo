# @Domain

These rules MUST trigger whenever the AI is tasked with database design, logical or physical data modeling, Object-Relational Mapping (ORM) design, system architecture, or schema refactoring involving actors, users, clients, organizations, and the various roles they play within an enterprise. Activation conditions include any user request asking to model "Customers," "Suppliers," "Employees," "Partners," or any entity representing a human or organizational actor interacting with a system.

# @Vocabulary

The AI MUST adopt and strictly adhere to the following precise mental model and terminology:

*   **Party**: A supertype representing either a human being (Person) or a group of persons organized for a particular purpose (Organization). A Party is the fundamental entity representing "who" someone is.
*   **Person**: A subtype of Party representing a physical human being. Contains attributes specific to humans (e.g., first name, last name, gender, date of birth).
*   **Organization**: A subtype of Party representing a structured group of individuals (e.g., corporation, LLC, informal team). Contains attributes specific to organizations (e.g., organization name, tax identifier).
*   **Declarative Role**: The stated actions and activities assigned to or required of a Party within the context of the *enterprise as a whole* (e.g., a Party declared generally as a "Customer" or "Supplier"). This sets up the role independent of any specific transaction.
*   **Contextual Role**: The role a Party plays within the specific context of a discrete transaction, event, or business process (e.g., the "Ship-to Customer" for a specific Order). *Note: Contextual roles are built upon Declarative roles.*
*   **Level 1 Declarative Role Pattern**: A highly specific data model where roles are modeled as distinct, independent entities (e.g., `CUSTOMER` table, `SUPPLIER` table) containing mixed core identity and role-specific attributes.
*   **Level 2 Declarative Role Pattern**: A normalized model separating core identity (`PARTY`, `PERSON`, `ORGANIZATION`) from roles (`DECLARATIVE ROLE 1`). Enforces strict 1:1 mapping between a Party and a specific Role Type instance.
*   **Level 3 Declarative Role Pattern**: A highly generalized and flexible model utilizing a `PARTY ROLE` supertype and a `ROLE TYPE` reference entity, allowing dynamic role additions and tracking role histories over time.
*   **Role Demarcation**: The strict classification and enforcement of whether a specific role can be played by a Person only (e.g., Employee), an Organization only (e.g., Supplier), or Both (e.g., Customer).

# @Objectives

*   Architect systems that explicitly separate core identity data ("who someone is") from role data ("what someone does").
*   Eliminate data redundancies and anomalies caused by duplicating a single actor's profile across multiple functional tables.
*   Enforce strict semantic demarcations to prevent invalid role assignments (e.g., preventing an Organization from being classified as an Employee).
*   Select the exact appropriate level of architectural generalization based on the specific constraints of the project (e.g., rapid prototyping vs. enterprise-scale dynamic extensibility).
*   Ensure temporal accuracy by tracking the lifespan of roles when implementing advanced generalizations.

# @Guidelines

The AI MUST evaluate and apply the following constraints, architectural rules, and anti-patterns during schema generation or code construction:

### Rule 1: Distinguish Declarative from Contextual Roles
*   When a user requests a role (e.g., "Customer"), the AI MUST determine if this is a Declarative Role (a general standing with the enterprise) or a Contextual Role (a state within a specific transaction).
*   The rules in this document govern **Declarative Roles**. Do NOT embed transaction-specific foreign keys (like `order_id`) directly into a Declarative Role entity.

### Rule 2: Enforce the "Party" Supertype/Subtype Architecture (Level 2 & 3)
*   Unless explicitly generating a Level 1 prototype, the AI MUST abstract common identity attributes (non-meaningful surrogate primary key `party_id`) into a `PARTY` entity.
*   The AI MUST create mutually exclusive subtypes for `PERSON` (storing `first_name`, `last_name`, `dob`) and `ORGANIZATION` (storing `organization_name`).
*   The AI MUST NOT store role-specific attributes (e.g., `credit_limit`, `employee_number`) in the `PARTY`, `PERSON`, or `ORGANIZATION` entities.

### Rule 3: Enforce Role Demarcation
*   The AI MUST analyze every requested role to determine its valid player type.
*   **Person-Only Roles** (e.g., Employee, Patient): MUST be physically or logically constrained to relate ONLY to the `PERSON` entity/subtype.
*   **Organization-Only Roles** (e.g., Supplier, Parent Company): MUST be physically or logically constrained to relate ONLY to the `ORGANIZATION` entity/subtype.
*   **Dual Roles** (e.g., Customer, Partner): MUST relate to the generalized `PARTY` supertype.

### Rule 4: Selection of Generalization Level
The AI MUST select the implementation pattern based on the project phase and system dynamics:
*   **Level 1 Requirements**: Use ONLY for communicating initial scope to business users, generating UI prototypes, or mapping to legacy non-relational systems.
    *   *Constraint*: The AI MUST output a warning regarding data redundancy (e.g., updating a user's name requires updating both the Customer and Employee tables).
*   **Level 2 Requirements**: Use for standard relational applications where the list of roles is highly static and well-known, and a Party plays a specific role only once at a given time.
    *   *Constraint*: Implement discrete tables for each role (`CUSTOMER`, `EMPLOYEE`) with a mandatory foreign key mapping back to `PARTY`, `PERSON`, or `ORGANIZATION`.
*   **Level 3 Requirements**: Use for enterprise architectures, master data management (MDM), or dynamic systems where roles change frequently, and historical tracking is required.
    *   *Constraint*: Implement a `PARTY_ROLE` intersection entity.
    *   *Constraint*: Implement a `ROLE_TYPE` entity to act as a dynamic lookup/domain table.
    *   *Constraint*: Include `from_date` (mandatory) and `thru_date` (optional) in the `PARTY_ROLE` entity to track historical state.

### Rule 5: Implement Level 3 Demarcation Strategically
When using Level 3, the AI MUST implement Role Demarcation using one of three approved architectural methods:
1.  **Hierarchy**: Implement a recursive relationship on `ROLE_TYPE` (parent-child). Create top-level instances for "Person Role" and "Organization Role", and nest specific roles underneath them.
2.  **Subtyping**: Create explicit subtypes of `PARTY_ROLE` named `PERSON_PARTY_ROLE` (linked to `PERSON`) and `ORGANIZATION_PARTY_ROLE` (linked to `ORGANIZATION`).
3.  **Intersection**: Create a `PARTY_TYPE` entity (values: Person, Org) and a `VALID_PARTY_TYPE_ROLE_TYPE` intersection entity to strictly define which roles correspond to which party types.

### Rule 6: Primary Key Architecture
*   The AI MUST use non-meaningful, auto-incrementing, or UUID surrogate keys for all entities (e.g., `party_id`, `role_type_id`).
*   Natural keys (e.g., SSN, Tax ID) MUST NOT be used as primary or foreign keys; they must be modeled as standard attributes within the specific entity or role.

# @Workflow

When executing a schema design or system architecture task involving actors/roles, the AI MUST process the request using the following rigid sequence:

1.  **Requirement Parsing & Classification**: Analyze the user's prompt to extract all mentioned actors. Determine if they represent Declarative Roles (general relationship) or Contextual Roles (transactional).
2.  **Demarcation Analysis**: For every identified Declarative Role, explicitly document whether it is a Person, an Organization, or Both.
3.  **Level Selection Strategy**: Assess the prompt's context.
    *   If "prototype", "simple", or "flat" is requested -> Generate Level 1 (with redundancy warnings).
    *   If "standard relational", "strict constraints", or "static roles" is requested -> Generate Level 2.
    *   If "enterprise", "dynamic", "historical", or "flexible" is requested -> Generate Level 3.
4.  **Schema Generation**:
    *   Create the core identity tables (`PARTY`, `PERSON`, `ORGANIZATION`).
    *   Create the role structures dictated by the selected Level.
    *   Apply Demarcation Constraints via foreign keys (Level 2) or lookup validation strategies (Level 3).
5.  **Attribute Distribution**: Place attributes exactly where they belong. Core identity attributes go to `PERSON`/`ORGANIZATION`. Role-specific attributes go to the explicit role table (Level 2) or specific role subtypes (Level 3).
6.  **Historical Implementation**: If Level 3 is selected, inject `from_date` and `thru_date` into the role assignment entities.

# @Examples (Do's and Don'ts)

### Principle: Separation of Identity and Role (Avoiding Level 1 in Production)

**[DON'T]** - Creating flat tables that mix identity and role, resulting in data anomalies.
```sql
-- Anti-Pattern: Level 1 logic applied to a relational database
CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    dob DATE,
    credit_limit DECIMAL
);

CREATE TABLE employee (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),  -- Redundant! If John is a customer and employee, data diverges.
    last_name VARCHAR(50),   -- Redundant!
    dob DATE,                -- Redundant!
    employee_number VARCHAR(20)
);
```

**[DO]** - Implementing Level 2: Normalizing Identity via the Party concept.
```sql
-- Correct: Level 2 Pattern separating identity from what they do.
CREATE TABLE party (
    party_id INT PRIMARY KEY,
    party_type VARCHAR(20) -- 'PERSON' or 'ORGANIZATION'
);

CREATE TABLE person (
    party_id INT PRIMARY KEY REFERENCES party(party_id),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    dob DATE
);

CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    party_id INT REFERENCES party(party_id), -- Dual role: connects to generalized party
    credit_limit DECIMAL
);

CREATE TABLE employee (
    employee_id INT PRIMARY KEY,
    party_id INT REFERENCES person(party_id), -- Demarcation: Person-only role
    employee_number VARCHAR(20)
);
```

### Principle: Level 3 Dynamic Extensibility and History

**[DON'T]** - Using static tables when the system requires dynamic addition of new role types and historical tracking.
```sql
-- Anti-Pattern for Dynamic Environments
CREATE TABLE supplier (
    supplier_id INT PRIMARY KEY,
    party_id INT REFERENCES organization(party_id),
    tax_id VARCHAR(50)
);
-- If the business suddenly needs "Logistics Partner", a DB migration & schema change is required.
-- No way to track WHEN a party stopped being a supplier.
```

**[DO]** - Implementing Level 3 for maximum enterprise flexibility and temporal tracking.
```sql
-- Correct: Level 3 Pattern
CREATE TABLE role_type (
    role_type_id INT PRIMARY KEY,
    parent_role_type_id INT REFERENCES role_type(role_type_id), -- Hierarchy for demarcation (e.g., 'Org Role')
    name VARCHAR(50) -- e.g., 'Supplier', 'Logistics Partner'
);

CREATE TABLE party_role (
    party_role_id INT PRIMARY KEY,
    party_id INT REFERENCES party(party_id),
    role_type_id INT REFERENCES role_type(role_type_id),
    from_date DATE NOT NULL,
    thru_date DATE,
    UNIQUE (party_id, role_type_id, from_date) -- Allows the same role at different times
);

-- Specific attributes for a role are pushed to a subtype of party_role
CREATE TABLE supplier_role_data (
    party_role_id INT PRIMARY KEY REFERENCES party_role(party_role_id),
    tax_identifier VARCHAR(50)
);
```