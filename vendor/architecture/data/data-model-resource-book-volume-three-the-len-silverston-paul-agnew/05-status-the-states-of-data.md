@Domain
These rules are triggered when the AI is modeling, designing, updating, or reviewing database schemas, data models, class structures, or system architectures that require tracking the state, condition, life cycle, or event timestamps of business entities (e.g., Orders, Shipments, Products, Parties, Invoices, Work Efforts).

@Vocabulary
- **Status**: A state or condition of affairs at a particular time that applies to business data (e.g., "Open", "Closed", "Pending").
- **Derived Status**: A status inferred from a related entity's status rather than stored directly on the primary entity (e.g., an Order's "Shipped" status derived from the related Shipment entity).
- **Point-in-Time Status**: A status that occurs at a specific moment, modeled using a `DATETIME` or `DATE` data type.
- **Range-of-Time Status**: A status that exists over a period, modeled using `from date` and `thru date` boundaries.
- **Level 1 Status Pattern**: A highly specific modeling approach where allowable statuses are explicitly defined as "event" attributes within the entity (e.g., `order received datetime`, `order opened from date`).
- **Level 2 Status Pattern (Current Status)**: A generalized approach using a `STATUS TYPE` entity to define states, but storing only a single, active status on the base entity via a foreign key, overwriting historical states.
- **Level 3 Status Pattern**: A flexible approach using an associative entity (e.g., `ENTITY STATUS`) resolving a many-to-many relationship between the base entity and `STATUS TYPE`, capturing status history and multiple simultaneous statuses.
- **Level 4 Status Pattern**: A "plug-and-play" enterprise interface using a central `STATUS APPLICATION` entity that links any number of different base entities to `STATUS TYPE` via exclusive OR (XOR) relationships.
- **Status Category Pattern**: A classification structure (e.g., `STATUS TYPE CATEGORY`) used to group statuses into sets (e.g., "Order Processing Statuses" vs. "Scheduling Statuses").
- **Status Type Association**: A pattern modeling how different status types relate to one another within a context.
- **Status Type Association Rule**: The business logic governing state transitions, taking values such as:
  - **Precedence**: One status must occur before another.
  - **Compatible**: Two statuses can exist simultaneously.
  - **Implied**: One status infers the existence of another.
  - **Exclusion**: The existence of one status strictly prevents another.
  - **Substitution**: Two statuses are interchangeable.
  - **Obsolescent**: One status replaces a deprecated status.

@Objectives
- Consistently model entity states, life cycles, and transitions according to exact business requirements for historical tracking, flexibility, and rule enforcement.
- Select the precise level of architectural generalization (Level 1 through 4) based on the trade-offs between system flexibility and model understandability.
- Prevent data redundancy by eliminating derived statuses and avoiding dual-purpose indicator/datetime attributes.
- Ensure temporal accuracy by distinguishing between the time a status represents (event time) and the time a record was enacted (system tracking time).
- Explicitly define business constraints using rule patterns when strict regulatory, compliance, or operational transition paths are required.

@Guidelines

- **Derived Statuses**: 
  - The AI MUST NOT redundantly model a status on an entity if it can be derived from a related entity. For example, if an Order has associated Shipments, the "Shipped" status of the Order MUST be derived from the Shipment's status, not stored as an independent attribute on the Order.

- **Status Attributes vs. Indicators**: 
  - The AI MUST NOT create separate boolean indicator attributes (e.g., `received indicator`) alongside status datetime attributes (e.g., `received datetime`). The presence of a datetime value inherently implies the status is active or the event has occurred. Combine these into a single event datetime attribute.

- **Level 1 Status Pattern Constraints**:
  - The AI MUST use Level 1 ONLY for static, well-defined life cycles where history tracking is unnecessary, and the audience requires a simple, non-abstract visual scope.
  - Represent statuses strictly as point-in-time (`event 1 datetime`) or range-of-time (`event 1 from date`, `event 1 thru date`) attributes directly on the entity.

- **Level 2 Status Pattern (Current Status) Constraints**:
  - The AI MUST use Level 2 ONLY when the business strictly requires a single active status at any given time, and historical state changes do not need to be preserved.
  - Create a `STATUS TYPE` reference entity. Add a `status type id` foreign key and an optional `status datetime` attribute directly on the base entity.

- **Level 3 Status Pattern Constraints**:
  - The AI MUST use Level 3 for dynamic environments requiring history preservation and the ability for an entity to hold multiple statuses simultaneously (e.g., "Active" and "Under Investigation").
  - Create an associative entity (e.g., `ORDER STATUS`) linking the base entity and `STATUS TYPE`.
  - The AI MUST separate event dates from tracking dates: Include `status datetime` (when the event happened) AND tracking boundaries (`from date`, `thru date` indicating when the system record is valid). The `from date` MUST be part of the Unique Identifier (UID).

- **Level 4 Status Pattern Constraints**:
  - The AI MUST use Level 4 when designing an enterprise-wide, modular architecture where multiple disparate entities must hook into a uniform status engine.
  - Create a central `STATUS APPLICATION` associative entity linking to `STATUS TYPE`.
  - The AI MUST implement an Exclusive OR (XOR) constraint across the foreign keys in `STATUS APPLICATION` that point to the base entities, ensuring a specific status record applies to one and only one base entity instance.

- **Categories and Rules Constraints**:
  - If a single entity requires multiple sets of disjointed statuses (e.g., Billing Status vs. Shipping Status), the AI MUST apply the Status Category Pattern (`STATUS TYPE CATEGORY`).
  - If compliance, audit, or complex state machines mandate strict transition paths, the AI MUST apply the Status Type with Multi Rollup and Rules Pattern, capturing transitions in `STATUS TYPE ASSOCIATION` and validating them via `STATUS TYPE ASSOCIATION RULE` (e.g., Precedence, Exclusion).

@Workflow
1. **Requirement Analysis**: Identify all data requirements involving the state, condition, or life cycle events of an entity. 
2. **Derivation Check**: Determine if the required status is inherently tracked by a downstream transactional entity (e.g., Invoice, Shipment). If yes, document the derivation logic and omit physical storage of the status on the parent entity.
3. **Temporal Analysis**: Determine whether the status is a Point-in-Time event (requires `datetime`) or a Range-of-Time condition (requires `from date` / `thru date`).
4. **Generalization Selection**:
   - Apply **Level 1** if the schema is for a prototype, scope statement, or extremely static entity with fewer than three state transitions.
   - Apply **Level 2** if the system tracks only "Current Status" and intentionally overwrites history.
   - Apply **Level 3** if the system must preserve a history of all state changes, allow concurrent statuses, and easily absorb new status types without DDL schema changes.
   - Apply **Level 4** if building a centralized master data management (MDM) or enterprise service bus architecture.
5. **Rule and Category Attachment**: If the statuses belong to multiple distinct functional workflows (e.g., Fulfillment vs. Support), introduce `STATUS TYPE CATEGORY`. If strict transition paths exist, introduce `STATUS TYPE ASSOCIATION RULE`.

@Examples (Do's and Don'ts)

**[DO]** Consolidate event occurrence and event timing into a single attribute in Level 1 patterns.
```sql
CREATE TABLE Order (
    order_id INT PRIMARY KEY,
    order_received_datetime DATETIME,
    order_closed_thru_date DATE
);
```

**[DON'T]** Split event occurrence and timing into redundant indicator/datetime pairs.
```sql
-- Anti-pattern: Redundant indicator and datetime attributes
CREATE TABLE Order (
    order_id INT PRIMARY KEY,
    is_received BOOLEAN,
    order_received_datetime DATETIME
);
```

**[DO]** Use the Level 3 associative entity to track both the event time AND the record validity time.
```sql
CREATE TABLE Order_Status (
    order_id INT,
    status_type_id INT,
    from_date DATETIME, -- Record enacted time (Part of UID)
    thru_date DATETIME, -- Record expiration time
    status_datetime DATETIME, -- Point in time the event occurred
    PRIMARY KEY (order_id, status_type_id, from_date)
);
```

**[DON'T]** Model a status directly on an entity if it can be derived from a contextual child process.
```text
-- Anti-pattern: Storing "Shipped" on the Order when Shipments exist.
Entity: ORDER
Attributes: order_id, status_shipped_datetime (WRONG: Derive this from SHIPMENT.status_shipped_datetime)
```

**[DO]** Use Exclusive OR (XOR) logic when applying the Level 4 Status Pattern across multiple entities.
```text
Entity: STATUS_APPLICATION
Attributes:
  status_application_id (PK)
  status_type_id (FK)
  order_id (FK, Optional)
  shipment_id (FK, Optional)
  work_effort_id (FK, Optional)
Constraint: XOR(order_id, shipment_id, work_effort_id) -- Exactly ONE must be populated.
```