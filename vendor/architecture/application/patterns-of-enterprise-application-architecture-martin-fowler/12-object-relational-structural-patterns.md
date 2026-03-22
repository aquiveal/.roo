## @Domain
These rules MUST trigger whenever the AI is tasked with designing, implementing, refactoring, or reviewing Object-Relational Mapping (ORM) logic, database schemas for object models, data persistence layers, inheritance hierarchy mapping to relational tables, or managing associations and state translations between in-memory objects and relational database rows.

## @Vocabulary
- **Identity Field**: A field in an in-memory object used exclusively to store the primary key of the corresponding relational database table, maintaining identity between the object and the database row.
- **Meaningless Key**: An auto-generated or random primary key (e.g., surrogate key) that holds no domain or human-readable meaning.
- **Meaningful Key**: A primary key derived from domain data (e.g., Social Security Number).
- **Foreign Key Mapping**: A structural pattern that maps an object reference or collection of references to a foreign key in a relational database.
- **Association Table Mapping**: A structural pattern that uses an intermediate link table to represent a many-to-many association between two objects.
- **Dependent Mapping**: A pattern where a child (dependent) class has no database mapping code of its own; its persistence is entirely handled by its parent (owner) class mapper.
- **Embedded Value**: A pattern that maps a small object (usually a Value Object) into several fields within the database table of the object's owner.
- **Serialized LOB (Large Object)**: A pattern that saves a complex graph of objects by serializing them into a single binary (BLOB), textual (CLOB), or XML structure stored in a single database field.
- **Single Table Inheritance**: A mapping strategy representing an entire class inheritance hierarchy as a single relational table, using columns for all fields of all classes and leaving unused columns empty.
- **Class Table Inheritance**: A mapping strategy representing an inheritance hierarchy with one table for each class (both abstract and concrete), linking them via common primary keys or foreign keys.
- **Concrete Table Inheritance**: A mapping strategy using one database table for each concrete class in a hierarchy, duplicating inherited superclass fields into each concrete table.
- **Inheritance Mappers**: A structural organization of database mappers for hierarchies, utilizing an abstract mapper for superclass data and concrete mappers for subclass data.

## @Objectives
- Create clean, maintainable boundaries between in-memory object models and relational database schemas.
- Prevent identity collisions, infinite cyclic references, and redundant data loading during persistence operations.
- Resolve the object-relational "impedance mismatch" by rigidly mapping object references, collections, and inheritance trees to optimized tabular structures.
- Select the most performant and architecturally appropriate inheritance mapping strategy based on schema flexibility, query performance, and domain complexity.
- Ensure that persistence mechanisms do not leak database-specific constraints into the pure domain logic.

## @Guidelines

### Identity Field Rules
- The AI MUST use Meaningless Keys for Identity Fields. Meaningful keys (e.g., SSN, email) MUST NOT be used due to human error and mutability risks.
- The AI MUST favor simple (single-field) keys over compound keys to ensure uniform key manipulation across the system. Compound keys MUST ONLY be used if retrofitting to an unchangeable legacy schema.
- The AI MUST use a long integer type for the Identity Field to ensure fast equality checking. Strings MAY be used only if mandated by DB administrators, but dates/times MUST NEVER be used as keys due to precision synchronization issues.
- When generating keys without database auto-generation, the AI MUST implement a separate Key Table. The Key Table read/update MUST be executed in a separate, short transaction to avoid locking the primary tables during long business transactions.

### Foreign Key Mapping Rules
- When mapping a 1:M collection, the AI MUST reverse the reference direction in the relational schema by placing the foreign key on the "many" side's table.
- To handle updates to a collection, the AI MUST use one of three strategies: 
  1. Delete and insert (if dependents are exclusively owned).
  2. Add a back pointer to make the association bidirectional.
  3. Diff the collection against the database or original read state.
- To prevent infinite cycles when loading interconnected objects, the AI MUST create empty objects and place them into the Identity Map immediately, BEFORE attempting to load their foreign key dependencies.

### Association Table Mapping Rules
- The AI MUST use Association Table Mapping exclusively for many-to-many associations or when linking two legacy tables that cannot be structurally altered.
- The AI MUST NOT create an in-memory domain object for the link table itself unless the link table carries additional domain logic (e.g., an "Employment" object containing hire dates between Person and Company).

### Dependent Mapping Rules
- The AI MUST ONLY use Dependent Mapping if the dependent object has exactly one owner and is never referenced by any object other than the owner.
- The AI MUST NOT assign an Identity Field to a dependent object.
- The AI MUST NOT create a separate Mapper class or Finder method for the dependent object. All persistence operations (CRUD) for the dependent MUST be encapsulated within the owner's Mapper.
- The AI MUST NOT use Dependent Mapping if tracking changes via a Unit of Work, as the delete-and-reinsert strategy creates orphaned rows in testing and tracking environments.

### Embedded Value Rules
- The AI MUST use Embedded Value for small, immutable Value Objects (e.g., Money, Date Range). 
- The AI MUST NOT create separate relational tables for Value Objects.
- The AI MUST ensure that changes to the Embedded Value mark the owner object as "dirty" for persistence tracking.

### Serialized LOB Rules
- The AI MUST use Serialized LOB for complex object graphs that do not need to be queried via SQL outside the application.
- The AI MUST NOT use Serialized LOB if external reporting systems require SQL access to the internal data (unless using XML and XPath-compatible databases).
- The AI MUST ensure that overlapping Serialized LOBs do not result in duplicated data that causes update anomalies; a LOB MUST be owned by a single aggregate root.

### Inheritance Mapping Rules
- **Single Table Inheritance**: The AI MUST use this as the default inheritance mapping for simple hierarchies to avoid SQL joins. The table MUST include a "Type Code" field to identify the class to instantiate. The AI MUST tolerate wasted/empty columns for subclass-specific fields.
- **Class Table Inheritance**: The AI MUST use this when database space constraints strictly forbid empty columns. The AI MUST mitigate the performance hit of multiple joins by optimizing queries or providing outer joins.
- **Concrete Table Inheritance**: The AI MUST duplicate all superclass fields across all concrete tables. The AI MUST implement key uniqueness across the *entire* hierarchy (all related tables), bypassing standard table-level auto-increment constraints.
- **Inheritance Mappers**: The AI MUST separate mapping logic into an abstract mapper (for superclass fields) and concrete mappers (for subclass fields) to avoid code duplication. The concrete mapper MUST call the superclass mapper's load/save hooks.

## @Workflow
When tasked with designing or implementing an object-relational mapping, the AI MUST execute the following step-by-step algorithmic process:

1. **Identity Phase**: Assign a meaningless long integer Identity Field to all Reference Objects. Ensure Value Objects have no Identity Field.
2. **Value Object Phase**: Locate all Value Objects (e.g., Currency, Date Ranges). Map them to their owner's table using the **Embedded Value** pattern.
3. **Complex Graph Phase**: Identify complex, heavily nested subgraphs that do not require independent SQL querying. Map them using the **Serialized LOB** pattern (preferring XML if human-readability is required).
4. **Association Phase**:
   - For 1:1 or 1:M relationships, apply **Foreign Key Mapping**. Implement cycle-breaking via immediate Identity Map registration.
   - For exclusively owned 1:M collections without external references, apply **Dependent Mapping**.
   - For M:M relationships, apply **Association Table Mapping**.
5. **Inheritance Phase**: Evaluate class hierarchies and select the mapping strategy:
   - Default to **Single Table Inheritance** (add a Type Code).
   - If polymorphic queries are rare and separation is strictly required by external systems, use **Concrete Table Inheritance** (ensure cross-table key uniqueness).
   - If database normalization/space is a critical constraint, use **Class Table Inheritance** (prepare for complex joins).
6. **Mapper Organization Phase**: Build **Inheritance Mappers** utilizing Layer Supertypes to handle shared ID generation, database connection management, and common load/save behaviors.

## @Examples (Do's and Don'ts)

### Identity Field
- **[DO]**: Use a meaningless `long` integer for an object's ID: `private Long id;`
- **[DON'T]**: Use a domain-meaningful string as a primary key: `private String socialSecurityNumber;`

### Resolving Cyclic References in Foreign Key Mapping
- **[DO]**: Create an empty object, register it in the Identity Map, then load its foreign key dependencies:
  ```java
  DomainObject result = new Order();
  loadedMap.put(id, result); // Register immediately
  result.setCustomer(mapper.find(rs.getLong("customer_id"))); // Load dependency safely
  ```
- **[DON'T]**: Load all dependencies before registering the object, which causes infinite loops if the customer references the order:
  ```java
  Customer c = mapper.find(rs.getLong("customer_id")); // Infinite loop risk
  DomainObject result = new Order(c);
  loadedMap.put(id, result);
  ```

### Dependent Mapping
- **[DO]**: Handle the insertion of `Track` objects entirely within the `AlbumMapper.update()` method by deleting old tracks and inserting new ones.
- **[DON'T]**: Create a `TrackMapper` or give `Track` an Identity Field when it is exclusively owned by `Album`.

### Embedded Value
- **[DO]**: Map a `Money` object into `base_cost_amount` and `base_cost_currency` columns within the `Product` table.
- **[DON'T]**: Create a separate `Money` table with a foreign key from the `Product` table.

### Single Table Inheritance
- **[DO]**: Create one `Players` table with a `type_code` column (e.g., 'B' for Bowler, 'C' for Cricketer) and tolerate null values in the `batting_average` column for Bowlers.
- **[DON'T]**: Create a `Players` table without a type code, relying on guessing the object type based on which fields are null.

### Concrete Table Inheritance
- **[DO]**: Ensure the `IdGenerator` issues unique IDs across both the `Bowlers` and `Cricketers` tables so that ID `101` belongs to exactly one player globally.
- **[DON'T]**: Rely on the database's native table-level auto-increment, which would result in a Bowler and a Cricketer both having ID `1`.