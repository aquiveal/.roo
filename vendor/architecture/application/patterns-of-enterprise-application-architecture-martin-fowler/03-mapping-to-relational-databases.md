@Domain
These rules MUST be triggered whenever the AI is tasked with designing, implementing, refactoring, or optimizing data access layers, Object-Relational Mapping (ORM) logic, database connection management, or mapping in-memory domain objects to relational databases. 

@Vocabulary
- **Gateway**: An object that encapsulates access to an external resource (e.g., database table). Includes **Row Data Gateway** (one instance per row) and **Table Data Gateway** (one instance per table, returning Record Sets).
- **Active Record**: An architectural pattern where a domain object wraps a database row, encapsulating both database access and domain logic. Ideal for simple Domain Models isomorphic to the database schema.
- **Data Mapper**: An architectural layer that moves data between objects and a database while keeping them entirely independent of each other. Ideal for complex Domain Models.
- **Unit of Work**: An object that tracks all objects read, created, updated, or deleted during a business transaction, and coordinates the writing out of changes and concurrency resolution in a single commit.
- **Identity Map**: A map/cache tracking every object read from the database within a session to ensure each object is loaded only once, preventing in-memory duplicate identities and inconsistent updates.
- **Lazy Load**: A placeholder object that doesn't contain its full data initially but knows how to fetch it from the database only when explicitly accessed.
- **Identity Field**: A field in an in-memory object that stores the database primary key to maintain identity between the object and the relational row.
- **Foreign Key Mapping**: Mapping an object reference to a foreign key in the database (handles single-valued and collection associations).
- **Association Table Mapping**: Creating an intermediate link table in the database to handle many-to-many object associations.
- **Dependent Mapping**: Having a parent/owner class perform the database mapping for a child class that is only accessed via the parent.
- **Embedded Value**: Mapping a small Value Object (e.g., Money, Date Range) into several fields within its owning object's database table record.
- **Serialized LOB (Large Object)**: Saving a complex graph of objects by serializing them (BLOB or XML CLOB) into a single database field.
- **Single Table Inheritance**: Representing a complete class inheritance hierarchy as a single database table containing columns for all fields of all classes.
- **Concrete Table Inheritance**: Representing an inheritance hierarchy using one table for every concrete class (duplicating superclass fields).
- **Class Table Inheritance**: Representing an inheritance hierarchy using one table for each class in the hierarchy, requiring joins to assemble a single object.
- **Metadata Mapping**: Boiling down ORM mapping into metadata (XML or code) to power code generation or reflective programming.
- **Query Object**: An object representing a database query constructed in terms of in-memory objects/fields rather than database tables/columns.
- **Repository**: An abstraction over the mapping layer that acts like an in-memory collection of domain objects, accepting Query Objects or Specifications.
- **Double Mapping**: A two-step mapping scheme used to map similar in-memory data to slightly different physical data stores via an intermediate logical data schema.

@Objectives
- Isolate SQL access and database schema intricacies away from business/domain logic.
- Prevent duplicate in-memory objects representing the same database row.
- Minimize database roundtrips and remote calls (mitigating latency).
- Enforce transactional integrity and ensure connections are explicitly managed and closed.
- Map complex object-oriented structures (associations, collections, inheritance) into flat relational tables predictably and safely.

@Guidelines
- **Architectural Selection**:
  - The AI MUST use **Active Record** ONLY when domain logic is simple and objects map one-to-one with database tables.
  - The AI MUST use **Data Mapper** when the domain logic is complex and the Domain Model schema diverges from the relational schema.
  - The AI MUST use **Table Data Gateway** when using a Table Module pattern or when the application heavily utilizes Record Sets (e.g., .NET DataSets).
- **Behavioral Constraints**:
  - The AI MUST track all state changes (inserts, updates, deletes) during a business transaction using a **Unit of Work**.
  - The AI MUST check an **Identity Map** before querying the database for a specific object to prevent loading the same database row into two distinct objects.
  - The AI MUST implement **Lazy Load** for connected object graphs to prevent pulling the entire database into memory, UNLESS the data is cheap to load or immediately required.
- **Query Optimization**:
  - The AI MUST pull back multiple rows at once rather than executing repeated identical queries for single rows (avoid N+1 queries).
  - The AI MUST use SQL JOINs to pull multiple tables in a single query, but MUST restrict joins to 3 or 4 per query to prevent database performance degradation.
  - The AI MUST avoid `SELECT *` if using positional column indices. `SELECT *` MAY be used ONLY if mapping code explicitly uses column name indices.
  - The AI MUST use static SQL that can be precompiled (e.g., Prepared Statements) and avoid dynamic string concatenation for SQL queries.
  - The AI MUST batch multiple SQL queries into a single database call when the environment supports it.
- **Structural Mapping Constraints**:
  - The AI MUST map relationships using **Identity Fields** to track primary keys. Use **Foreign Key Mapping** for 1:N and **Association Table Mapping** for N:M relationships.
  - The AI MUST map isolated, non-queryable object graphs to a **Serialized LOB** if they do not require SQL querying outside the application.
  - The AI MUST map Value Objects (like Money) using **Embedded Value** rather than creating dedicated database tables for them.
  - The AI MUST resolve inheritance mapping by choosing **Single Table Inheritance** for simplicity, **Class Table Inheritance** to save space but incur JOINs, or **Concrete Table Inheritance** to avoid JOINs but risk key uniqueness issues.
  - If mapping data from multiple slightly different schemas, the AI MUST use **Double Mapping** (Memory -> Logical Schema -> Physical Schema).
  - If updating database Views or Queries, the AI MUST encapsulate the underlying table update logic to prevent unexpected inconsistencies.
- **Connection Management**:
  - The AI MUST explicitly close database connections when they are no longer in use.
  - The AI MUST NEVER rely on the Garbage Collector to close database connections.
  - The AI MUST tie database connections to transactions. Open the connection at transaction start, close it on commit/rollback.
  - The AI MUST pass connections via a thread-scoped **Registry** or transaction object, rather than cluttering method signatures with connection parameters.

@Workflow
1. **Analyze Domain Complexity**: Determine the architectural pattern. (Simple = Active Record / Row Data Gateway. Record Set UI = Table Data Gateway. Complex = Data Mapper).
2. **Setup Connection and Transaction Strategy**: Implement a thread-scoped Registry to hold connections and a Unit of Work to govern transaction boundaries.
3. **Establish Identity Map**: Create an Identity Map for the session to cache loaded objects and prevent duplicate instantiation.
4. **Implement Data Retrieval (Finders)**: 
   - Check the Identity Map first.
   - Formulate static, precompiled SQL using Prepared Statements.
   - Apply Joins strategically (max 3-4) or implement Lazy Load placeholders for deep object graphs.
5. **Implement Data Persistence**:
   - Defer updates, inserts, and deletes to the Unit of Work commit phase.
   - Use Identity Fields to map foreign keys and handle relational integrity.
6. **Apply Structural Mappings**: Resolve any Value Objects (Embedded Value), hierarchies (Table Inheritance), or complex isolated graphs (Serialized LOB).

@Examples (Do's and Don'ts)

- **[DO]** Check the Identity Map before fetching from the database.
```java
public Person find(Long id) {
    Person result = (Person) Registry.getPerson(id);
    if (result != null) return result; // Return from Identity Map
    
    // Proceed to load from Database using Prepared Statement
    PreparedStatement stmt = DB.prepare("SELECT id, lastname, firstname FROM people WHERE id = ?");
    // ... load and put into Identity Map
}
```

- **[DON'T]** Query the database blindly, creating duplicate memory identities.
```java
// ANTI-PATTERN: Creates two different objects for the same database row
public Person find(Long id) {
    PreparedStatement stmt = DB.prepare("SELECT * FROM people WHERE id = " + id);
    // Directly instantiating new objects ignores the Identity Map
    return new Person(rs.getLong("id")); 
}
```

- **[DO]** Use explicitly named columns in SQL OR use column name indices when processing results.
```java
// Safe against column reordering
String sql = "SELECT id, lastname, firstname FROM people";
// OR using column names in the result set
String lastName = rs.getString("lastname");
```

- **[DON'T]** Use `SELECT *` combined with positional indices.
```java
// ANTI-PATTERN: Breaks if the database administrator adds or reorders a column
String sql = "SELECT * FROM people";
String lastName = rs.getString(2); // DANGEROUS
```

- **[DO]** Explicitly close database connections in a `finally` block or Unit of Work boundary.
```java
PreparedStatement stmt = null;
try {
    stmt = DB.prepare(sql);
    // ... execute query
} finally {
    DB.cleanUp(stmt); // Explicitly release resources
}
```

- **[DON'T]** Leave connections open and rely on Garbage Collection.
```java
// ANTI-PATTERN: Relies on finalizers/GC, leading to connection pool exhaustion
public void executeQuery() {
    Connection conn = pool.getConnection();
    // ... code executes, method ends, connection is leaked
}
```

- **[DO]** Use Embedded Value for small Value Objects.
```java
// Mapping a Money object directly into the 'orders' table
stmt.setBigDecimal(1, baseCost.amount());
stmt.setString(2, baseCost.currency().code());
```

- **[DON'T]** Create separate database tables for Value Objects.
```sql
-- ANTI-PATTERN: Creating a table for Money
CREATE TABLE money_values (id INT, amount DECIMAL, currency VARCHAR);
```