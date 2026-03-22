@Domain
These rules MUST be triggered whenever the AI is tasked with designing, reviewing, or implementing data models, database schemas, class structures, or application logic that involves people, organizations, customers, suppliers, employees, contact information (addresses, phone numbers, emails), physical facilities, or communication tracking (CRM systems, contact management, activity tracking).

@Vocabulary
- **PARTY**: A supertype entity representing any person or organization of interest to the enterprise. Allows shared relationships (like contact mechanisms and roles) to be modeled once.
- **ORGANIZATION**: A subtype of PARTY representing a group of individuals with a common purpose. 
- **LEGAL ORGANIZATION**: A formally recognized organization (e.g., Corporation, Government Agency). Capable of entering into contracts.
- **INFORMAL ORGANIZATION**: A loosely associated group of people (e.g., Team, Family).
- **PERSON**: A subtype of PARTY representing a specific human being, independent of their jobs or roles.
- **PARTY CLASSIFICATION**: Categories into which parties belong (e.g., Industry Classification, Minority Classification, EEOC Classification, Income Classification).
- **PARTY ROLE**: Defines how a party acts within the context of the enterprise (e.g., Customer, Supplier, Employee, Internal Organization, Distribution Channel).
- **PARTY RELATIONSHIP**: An entity that tracks the specific relationship between two PARTY ROLEs (e.g., an Employment relationship between an Employee and an Internal Organization; a Customer Relationship between a Customer and an Internal Organization).
- **CONTACT MECHANISM**: A supertype for any method used to contact a party. Subtypes include POSTAL ADDRESS, TELECOMMUNICATIONS NUMBER, and ELECTRONIC ADDRESS.
- **PARTY CONTACT MECHANISM**: An associative entity linking a PARTY to a CONTACT MECHANISM, allowing many-to-many relationships.
- **CONTACT MECHANISM PURPOSE**: Defines the specific use of a contact mechanism for a party at a given time (e.g., "billing address", "primary home phone").
- **GEOGRAPHIC BOUNDARY**: An encompassing area (e.g., City, State, Country, Postal Code) linked to a Postal Address.
- **FACILITY**: A physical structure (e.g., Warehouse, Plant, Building, Room) where things are located, distinct from a postal address.
- **COMMUNICATION EVENT**: The interchange of information between parties (e.g., Phone Call, Email, Meeting) linked to a PARTY RELATIONSHIP or COMMUNICATION EVENT ROLE.
- **CASE**: A grouping of related COMMUNICATION EVENTs regarding a particular issue.

@Objectives
- Eliminate data redundancy by consolidating common attributes of people and organizations into a unified PARTY supertype.
- Decouple a party's intrinsic identity (who they are) from their situational roles (how they act/what they do).
- Decouple contact details from the party entity to support infinite, flexible contact methods without schema changes.
- Ensure all historical changes (name changes, role changes, relationship changes, contact method changes) are trackable using validity date ranges.
- Accurately model the context of business interactions by attaching statuses, priorities, and communication events to the *relationship* between parties, not to the parties themselves.

@Guidelines

**1. Party and Organization Modeling**
- The AI MUST NOT create separate, disconnected entities for `CUSTOMER`, `VENDOR`, `EMPLOYEE`, or `DEPARTMENT` that redundantly store names or demographics.
- The AI MUST create a `PARTY` supertype with `PERSON` and `ORGANIZATION` as mutually exclusive subtypes.
- The AI MUST store intrinsic human attributes (first name, last name, birth date, gender) strictly in the `PERSON` entity (or related historical entities like `PERSON NAME` or `PHYSICAL CHARACTERISTIC` if tracking history is required).
- The AI MUST store intrinsic organizational attributes (name, federal tax ID) strictly in the `ORGANIZATION` entity.
- The AI MUST subtype `ORGANIZATION` into `LEGAL ORGANIZATION` (for contract-capable entities) and `INFORMAL ORGANIZATION` (for internal teams or families).
- The AI MUST use `PARTY CLASSIFICATION` (linked to `PARTY TYPE`) to categorize parties demographically (e.g., Income, EEOC, Industry, Size), ensuring classifications include `from_date` and `thru_date` to track history.

**2. Roles and Relationships**
- The AI MUST model roles (e.g., Customer, Supplier, Employee) as instances of a `PARTY ROLE` entity, NOT as static attributes or rigid subtypes of the Person/Organization entities.
- The AI MUST allow a single `PARTY` to play multiple `PARTY ROLE`s simultaneously or over time.
- The AI MUST model the interactions between parties using a `PARTY RELATIONSHIP` entity that connects two `PARTY ROLE` instances (e.g., connecting a "Customer" role to an "Internal Organization" role).
- The AI MUST attach relationship-specific attributes (Statuses, Priorities, Notes) strictly to the `PARTY RELATIONSHIP` entity, NOT to the `PARTY` or the `CONTACT`. (e.g., Sales rep A and Sales rep B can have different relationship statuses with the same Customer Contact).
- The AI MUST include `from_date` and `thru_date` on all `PARTY ROLE` and `PARTY RELATIONSHIP` entities to maintain historical accuracy.

**3. Contact Information Architecture**
- The AI MUST NOT store contact information as direct attributes of a Person or Organization (e.g., NO `address_line_1`, `home_phone`, or `email` columns on the `PERSON` or `CUSTOMER` tables).
- The AI MUST create a central `CONTACT MECHANISM` supertype, with subtypes for `POSTAL ADDRESS`, `TELECOMMUNICATIONS NUMBER`, and `ELECTRONIC ADDRESS`.
- The AI MUST link parties to contact mechanisms via a many-to-many associative entity (`PARTY CONTACT MECHANISM`).
- The AI MUST use a `PARTY CONTACT MECHANISM PURPOSE` entity (linked to a `CONTACT MECHANISM PURPOSE TYPE`) to define what a contact method is used for (e.g., "Mailing Address", "Headquarters", "Emergency Phone"). A single contact mechanism for a single party can have multiple purposes simultaneously.
- The AI MUST resolve many-to-many geographic lookups by linking `POSTAL ADDRESS` to a `GEOGRAPHIC BOUNDARY` entity (which itself is recursively related to handle City -> State -> Country hierarchies).

**4. Facilities vs. Contact Mechanisms**
- The AI MUST clearly distinguish between a `CONTACT MECHANISM` (how to reach someone, a label) and a `FACILITY` (a physical structure like a building or room).
- The AI MUST link `FACILITY` to `CONTACT MECHANISM` via a many-to-many associative entity (`FACILITY CONTACT MECHANISM`), acknowledging that one address might serve multiple buildings, or one building might have multiple addresses/phones.

**5. Communication and Activity Tracking**
- The AI MUST track interactions using a `COMMUNICATION EVENT` entity.
- The AI MUST link `COMMUNICATION EVENT`s to the specific `PARTY RELATIONSHIP` in which the communication occurred, rather than directly to the party, to preserve business context.
- The AI MUST categorize communications using `CONTACT MECHANISM TYPE` (how it occurred) and `COMMUNICATION EVENT PURPOSE` (why it occurred).
- The AI MUST support follow-up actions by linking `COMMUNICATION EVENT`s to a `CASE` (for issue grouping) and to `WORK EFFORT`s (for resultant tasks/actions).

@Workflow
When architecting a system involving people and organizations, the AI MUST follow this exact sequence:

1.  **Establish Core Identity:** Define the `PARTY` supertype. Implement `PERSON` and `ORGANIZATION` subtypes. Move all core demographic attributes to these entities.
2.  **Define Classifications:** Implement `PARTY CLASSIFICATION` to handle grouping (e.g., Industry types, minority status) independent of roles.
3.  **Extract Roles:** Identify all contextual hats a party wears (Customer, Employee, Partner). Implement these as `PARTY ROLE` records linking back to the `PARTY`.
4.  **Map Relationships:** Identify how roles interact. Create `PARTY RELATIONSHIP` records connecting two `PARTY ROLE`s. Move all interaction statuses and priorities to this relationship layer.
5.  **Abstract Contact Mechanisms:** Remove all hardcoded phone/address/email fields from entity tables. Create the `CONTACT MECHANISM` structure.
6.  **Assign Contact Purposes:** Link `PARTY` to `CONTACT MECHANISM` via an associative table, and strictly define the reason for the link using `PARTY CONTACT MECHANISM PURPOSE`.
7.  **Establish Physical Boundaries/Facilities:** Model `GEOGRAPHIC BOUNDARY` for address normalization, and `FACILITY` for physical building tracking.
8.  **Model Event Tracking:** Implement `COMMUNICATION EVENT` tied to the `PARTY RELATIONSHIP` to track the history of contacts, phone calls, and meetings. Link these to `CASE` and `WORK EFFORT` for task management.

@Examples (Do's and Don'ts)

**Principle: Party and Role Modeling**

[DON'T] Create separate operational tables with redundant demographic data.
```sql
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    credit_rating VARCHAR(10)
);
CREATE TABLE Employee (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    ssn VARCHAR(11)
);
```

[DO] Decouple the intrinsic person from the roles they play.
```sql
CREATE TABLE Party (
    party_id INT PRIMARY KEY,
    party_type VARCHAR(20) -- 'PERSON' or 'ORGANIZATION'
);
CREATE TABLE Person (
    party_id INT PRIMARY KEY REFERENCES Party(party_id),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE
);
CREATE TABLE Party_Role (
    party_role_id INT PRIMARY KEY,
    party_id INT REFERENCES Party(party_id),
    role_type VARCHAR(50), -- e.g., 'CUSTOMER', 'EMPLOYEE'
    from_date DATE,
    thru_date DATE
);
```

**Principle: Contact Mechanism Abstraction**

[DON'T] Hardcode contact fields onto the party or role tables.
```sql
CREATE TABLE Vendor (
    vendor_id INT PRIMARY KEY,
    company_name VARCHAR(100),
    address_line_1 VARCHAR(100),
    address_line_2 VARCHAR(100),
    city VARCHAR(50),
    office_phone VARCHAR(20),
    fax_number VARCHAR(20),
    email_address VARCHAR(100)
);
```

[DO] Abstract contacts into mechanisms and link them with purposes.
```sql
CREATE TABLE Contact_Mechanism (
    contact_mechanism_id INT PRIMARY KEY,
    mechanism_type VARCHAR(50) -- 'POSTAL', 'TELECOM', 'EMAIL'
);
CREATE TABLE Postal_Address (
    contact_mechanism_id INT PRIMARY KEY REFERENCES Contact_Mechanism(contact_mechanism_id),
    address_line_1 VARCHAR(100),
    address_line_2 VARCHAR(100),
    directions TEXT
);
CREATE TABLE Party_Contact_Mechanism (
    party_id INT REFERENCES Party(party_id),
    contact_mechanism_id INT REFERENCES Contact_Mechanism(contact_mechanism_id),
    from_date DATE,
    thru_date DATE,
    non_solicitation_ind BOOLEAN,
    PRIMARY KEY (party_id, contact_mechanism_id, from_date)
);
CREATE TABLE Party_Contact_Mechanism_Purpose (
    party_id INT,
    contact_mechanism_id INT,
    from_date DATE,
    purpose_type VARCHAR(50), -- e.g., 'BILLING_ADDRESS', 'MAIN_FAX'
    purpose_from_date DATE,
    purpose_thru_date DATE,
    FOREIGN KEY (party_id, contact_mechanism_id, from_date) REFERENCES Party_Contact_Mechanism(party_id, contact_mechanism_id, from_date)
);
```

**Principle: Party Relationships**

[DON'T] Attach CRM statuses directly to a Contact or Customer record, ignoring the perspective of the specific salesperson or internal organization.
```sql
CREATE TABLE Customer_Contact (
    contact_id INT PRIMARY KEY,
    person_id INT,
    sales_rep_id INT,
    relationship_status VARCHAR(20), -- WRONG: Overwritten if a 2nd sales rep interacts with them
    notes TEXT
);
```

[DO] Model the relationship between two specific roles and attach statuses to that specific relationship.
```sql
CREATE TABLE Party_Relationship (
    party_relationship_id INT PRIMARY KEY,
    from_party_role_id INT REFERENCES Party_Role(party_role_id), -- e.g., Sales Rep Role
    to_party_role_id INT REFERENCES Party_Role(party_role_id),   -- e.g., Customer Role
    relationship_type VARCHAR(50), -- e.g., 'ACCOUNT_MANAGEMENT'
    from_date DATE,
    thru_date DATE
);
CREATE TABLE Party_Relationship_Status (
    party_relationship_id INT REFERENCES Party_Relationship(party_relationship_id),
    status_type VARCHAR(50), -- e.g., 'ACTIVE', 'INACTIVE'
    status_date DATE,
    PRIMARY KEY (party_relationship_id, status_type, status_date)
);
```