@Domain
This rule file is triggered whenever the AI is tasked with designing, extending, or analyzing data models, database schemas, object-relational mapping (ORM) entities, or application logic that involve relationships between parties (people or organizations) and specific business transactions, events, or entities (e.g., Orders, Projects, Shipments, Invoices). 

@Vocabulary
- **Contextual Role**: The specific actions, activities, or involvements a person or organization plays within the context of a specific business event, transaction, or piece of data (e.g., the "Ship-To Customer" for an order, the "Project Lead" for a project).
- **Declarative Role**: A role defined within the context of the enterprise as a whole, independent of specific transactions (e.g., a "Customer" or "Employee" in general).
- **Level 1 Contextual Role Pattern (Attributes)**: A specific modeling style where contextual roles are captured as direct attributes of the target entity (e.g., `project_sponsor_name`, `project_worker_name` directly on the `PROJECT` table).
- **Level 1 Contextual Role Pattern (Relationships)**: A specific modeling style where contextual roles are defined as explicit associative entities (e.g., `PROJECT_SPONSOR`) connecting a specific declarative role entity (e.g., `SPONSOR`) to the target entity (`PROJECT`).
- **Level 2 Contextual Role Pattern**: A moderately flexible modeling style that links an entity's contextual roles to the `PARTY ROLE` supertype/subtype structure, meaning a party must be "declared" in a role before acting in that context.
- **Level 2 Contextual Role Pattern (PARTY Only Alternative)**: An alternative Level 2 model that links contextual roles directly to the `PARTY` entity, removing the requirement to explicitly declare a party's enterprise role before they participate in a transaction.
- **Level 3 Contextual Role Pattern**: A highly generalized and flexible pattern using a generic associative entity (e.g., `PROJECT_ROLE` or `CONTEXTUAL_ROLE`) that acts as a three-way intersection between the target `ENTITY`, a `PARTY`, and a `ROLE_TYPE`. 
- **Hybrid Contextual Role Pattern**: A data model that integrates both specific (Level 2) and generalized (Level 3) contextual role patterns within the same schema to support both core, static business rules and dynamic, future role types.

@Objectives
- Accurately model how parties interact with and are involved in specific business entities.
- Differentiate clearly between enterprise-wide roles (Declarative) and transaction-scoped roles (Contextual).
- Select the appropriate level of generalization (Level 1, 2, 3, or Hybrid) based on the specific business requirements, environmental volatility, and the need for rigorous constraint enforcement versus structural flexibility.
- Prevent data redundancy, synchronization errors, and schema fragility when business rules or role classifications change over time.

@Guidelines

### 1. Differentiating Contextual vs. Declarative Roles
- The AI MUST explicitly evaluate if a requested role is Contextual (scoped to a specific transaction/event like an Order) or Declarative (scoped to the enterprise).
- Contextual roles MUST NOT be modeled as standalone enterprise parties. They MUST be modeled as a relationship or attribute belonging to the specific context entity.

### 2. Implementing Level 1 Contextual Roles (Attributes)
- The AI MUST NOT use the Level 1 Attributes pattern for standard relational database implementations, as it violates normalization (e.g., repeating groups for multiple workers) and causes data inconsistency.
- The AI MAY use the Level 1 Attributes pattern ONLY if the requirement is for a rapid scoping prototype, a star schema dimension design, or if the business requires capturing just a single piece of data (e.g., a name) without maintaining an entire related party record (e.g., "Mother's maiden name" on an application).

### 3. Implementing Level 1 Contextual Roles (Relationships)
- The AI MUST use associative entities (e.g., `PROJECT_WORKER`) or direct relationships to link a target entity to a Declarative Role entity when specific, static cardinality rules must be strictly enforced by the schema (e.g., "A Project can have one and only one Project Lead").
- The AI MUST NOT use this pattern if the environment is dynamic or if new roles are frequently discovered, as schema alterations would be continuously required.

### 4. Implementing Level 2 Contextual Roles (PARTY ROLE connection)
- The AI MUST use this pattern when the enterprise requires strict semantic rigor, specifically the business rule that a party MUST be declared in an enterprise role before they can act in a context (e.g., a party MUST be a `WORKER` before they can be a `PROJECT_WORKER`).
- The AI MUST relate the contextual role associative entity to the `PARTY_ROLE` supertype or its specific subtypes.

### 5. Implementing Level 2 Contextual Roles (PARTY-Only Alternative)
- The AI MUST use the PARTY-Only Alternative when the business allows any party to play a contextual role without prior declaration (e.g., an invoice `RECEIVER` does not need to be predefined as an enterprise `CUSTOMER`).
- The AI MUST link the contextual associative entity directly to the `PARTY` entity.

### 6. Implementing Level 3 Contextual Roles (Generic Intersection)
- The AI MUST use the Level 3 pattern in highly dynamic environments where the types of contextual roles frequently change, or are not fully known during design.
- The AI MUST create a 3-way intersection entity (e.g., `CONTEXTUAL_ROLE`) joining `PARTY`, the target `ENTITY`, and `ROLE_TYPE`. 
- The AI MUST utilize `from_date` and `thru_date` attributes on the intersection entity to track the history of role assignments over time.
- **Constraint Warning**: Because the Level 3 pattern inherently supports Many-to-Many relationships, schema-level cardinality constraints (e.g., "Only 1 Project Lead") are lost. The AI MUST explicitly document these business rules so they can be enforced via application logic, triggers, or a separate Business Rules pattern.

### 7. Implementing Hybrid Contextual Roles
- The AI MUST use the Hybrid pattern when the enterprise possesses a set of strict, core roles that require schema-level enforcement (using Level 2), alongside a need to dynamically capture unpredictable auxiliary roles (using Level 3).
- **Anti-Redundancy Mandate**: The AI MUST explicitly implement logic or constraints to ensure that a contextual role is NOT stored redundantly in both the specific structure and the generic structure simultaneously.

@Workflow
1. **Analyze the Context**: Identify the core target entity (e.g., `Order`, `Project`, `Shipment`) and the parties interacting with it.
2. **Determine Role Volatility**: Ask if the roles are static (never changing), dynamic (new roles expected), or mixed. 
3. **Determine Rule Rigidity**: Ask if the business requires database-level enforcement of cardinality (e.g., exactly one Bill-To customer) or if application-level enforcement is acceptable.
4. **Select the Pattern**:
   - Static + Schema-enforced -> Level 1 (Relationships) or Level 2.
   - Requires pre-declared roles -> Level 2 (`PARTY ROLE`).
   - Open participation -> Level 2 (`PARTY`-Only).
   - Dynamic + App-enforced -> Level 3.
   - Mixed requirements -> Hybrid.
5. **Generate Schema/Logic**: Draft the tables, foreign keys, and associative entities based on the selected pattern.
6. **Define Constraints**: If using Level 3 or Hybrid, explicitly output the business rules that must be handled by the application layer (e.g., enforcing 1:1 constraints lost in M:M generalized tables).

@Examples (Do's and Don'ts)

### Level 1 Contextual Role (Attributes)
[DO] Use for a simple, non-relational extraction or where only a string is needed.
```sql
CREATE TABLE EMPLOYMENT_APPLICATION (
    application_id INT PRIMARY KEY,
    applicant_name VARCHAR(100),
    mother_maiden_name VARCHAR(100) -- Acceptable Level 1 use case: no other info needed about the mother
);
```

[DON'T] Use attributes for roles that require multiplicity or history.
```sql
CREATE TABLE PROJECT (
    project_id INT PRIMARY KEY,
    worker_1_name VARCHAR(100), -- ANTI-PATTERN: Fails First Normal Form
    worker_2_name VARCHAR(100), -- ANTI-PATTERN: Requires schema changes for worker 3
    lead_name VARCHAR(100)
);
```

### Level 2 Contextual Role (PARTY ROLE vs PARTY)
[DO] Require a PARTY ROLE when the business demands enterprise declaration first.
```sql
CREATE TABLE PROJECT_WORKER (
    project_id INT REFERENCES PROJECT(project_id),
    party_role_id INT REFERENCES WORKER(party_role_id), -- Correct Level 2 usage
    from_date DATE,
    PRIMARY KEY (project_id, party_role_id, from_date)
);
```

[DON'T] Force a PARTY ROLE when the business process is ad-hoc (Use PARTY instead).
```sql
-- If an Invoice Sender doesn't need to be an approved enterprise Vendor:
CREATE TABLE INVOICE_SENDER (
    invoice_id INT REFERENCES INVOICE(invoice_id),
    party_id INT REFERENCES PARTY(party_id) -- Correct PARTY-Only alternative
);
```

### Level 3 Contextual Role
[DO] Create a flexible 3-way intersection for dynamic roles.
```sql
CREATE TABLE PROJECT_ROLE (
    project_role_id INT PRIMARY KEY,
    project_id INT REFERENCES PROJECT(project_id),
    party_id INT REFERENCES PARTY(party_id),
    role_type_id INT REFERENCES ROLE_TYPE(role_type_id), -- Handles "Lead", "Worker", "QA", etc. dynamically
    from_date DATE,
    thru_date DATE
);
```

[DON'T] Rely on the Level 3 schema alone to enforce single-role assignment.
```java
// ANTI-PATTERN: Inserting without checking application-level business rules
public void assignProjectLead(int projectId, int partyId) {
    // Missing check! The Level 3 schema allows infinite "Leads" per project.
    db.insert("PROJECT_ROLE", projectId, partyId, ROLE_TYPE_LEAD); 
}
```

### Hybrid Contextual Role
[DO] Separate core schema-enforced roles from dynamic auxiliary roles without overlapping data.
```sql
-- Specific structure for strict business rule (Only 1 Lead)
ALTER TABLE PROJECT ADD COLUMN lead_party_id INT REFERENCES PARTY(party_id);

-- Generic structure for flexible roles (Workers, Writers, QA)
CREATE TABLE PROJECT_ROLE (
    project_id INT REFERENCES PROJECT(project_id),
    party_id INT REFERENCES PARTY(party_id),
    role_type_id INT REFERENCES ROLE_TYPE(role_type_id)
);
-- Application logic MUST prevent ROLE_TYPE_LEAD from being inserted into PROJECT_ROLE.
```