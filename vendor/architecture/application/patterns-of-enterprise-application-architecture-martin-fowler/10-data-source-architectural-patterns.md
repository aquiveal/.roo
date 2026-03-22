@Domain
Trigger these rules when the user requests the implementation, refactoring, or design of database access layers, object-relational mapping (ORM), SQL encapsulation, persistence mechanisms, or data source architectures.

@Vocabulary
- **Table Data Gateway**: An object that acts as a Gateway to a database table or view. One instance handles all rows in the table.
- **Row Data Gateway**: An object that acts as a Gateway to a single record in a data source. One instance per row. Contains NO domain logic.
- **Active Record**: An object that wraps a row in a database table or view, encapsulates the database access, AND adds domain logic to that data.
- **Data Mapper**: A layer of Mappers that moves data between objects and a database while keeping them completely independent of each other and the mapper itself.
- **Record Set**: An in-memory representation of tabular data (e.g., ADO.NET DataSet or JDBC ResultSet).
- **Identity Map**: A cache/map used by finders to ensure each object is loaded only once per session, preventing duplicate reads and identity collisions.
- **Lazy Load**: An object placeholder that doesn't contain all data but knows how to fetch it from the database on demand, preventing massive object graph loading.
- **Metadata Mapping**: The practice of storing object-relational mapping details in metadata to automate DB interactions via code generation or reflection.
- **Separated Interface**: An architectural tactic where the interface is defined in a client package (e.g., Domain) but implemented in another (e.g., Data Source) to break dependencies.
- **Isomorphic Schema**: A condition where the in-memory object structure exactly mirrors the relational database table structure (one field per column).

@Objectives
- Completely decouple SQL logic from user interface components and, when applicable, from pure domain models.
- Centralize database access to prevent SQL duplication and to provide DBAs with a single location to tune queries.
- Select the strictly appropriate Data Source pattern (Table Data Gateway, Row Data Gateway, Active Record, or Data Mapper) based on the specific complexity of the application's domain logic.
- Ensure proper object identity management using Identity Maps to avoid data corruption caused by loading multiple instances of the same database row.

@Guidelines

**Pattern Selection Constraints**
- If the application uses a **Table Module** for domain logic, you MUST use a **Table Data Gateway**.
- If the application uses a **Transaction Script**, you MUST use either a **Table Data Gateway** or a **Row Data Gateway**.
- If the application uses a **Domain Model** with simple logic and an isomorphic schema, you MUST use **Active Record**.
- If the application uses a complex **Domain Model** where the object schema diverges from the database schema, you MUST use **Data Mapper**.

**Table Data Gateway Rules**
- Implement exactly one instance per database table or view.
- Ensure the Gateway class is stateless.
- When returning data, return a Record Set or a Data Transfer Object (DTO). NEVER return a generic Map or Dictionary, as it defeats compile-time checking and obscures the interface.
- Use column name indices (e.g., `rs.getString("lastname")`) instead of positional indices (`rs.getString(2)`) to prevent breakages if database columns are reordered.

**Row Data Gateway Rules**
- Create exactly one instance of the object per database row.
- The class MUST NOT contain any domain logic, validations, or calculations. It must purely contain database access logic (CRUD operations) and getters/setters.
- Avoid placing static `find` methods on the Gateway class itself, as it precludes polymorphism. Instead, implement separate Finder classes (e.g., `PersonFinder`) that execute the SQL and return instances of the Row Data Gateway.

**Active Record Rules**
- Maintain an isomorphic schema: create one field in the class for each column in the table without applying complex type conversions.
- Combine both data access logic (insert, update, delete) and domain logic (derivations, single-record validations) into the same class.
- Do NOT use this pattern if the domain logic requires complex relationships, collections, or inheritance.

**Data Mapper Rules**
- Ensure Domain Objects have NO knowledge of the database, SQL, or the Mapper itself.
- You MUST use an **Identity Map** to check if an object is already loaded before executing a database query. This check must occur twice: once in the `find` method (to avoid hitting the DB if possible) and once in the `load` method (to prevent creating duplicate objects from a query that returned already-loaded records).
- To prevent infinite recursive loops when loading cyclical references, instantiate an empty domain object using a no-argument constructor, immediately place it into the Identity Map, and ONLY THEN populate its fields.
- Mappers require access to domain object fields. To populate fields without violating encapsulation, use reflection, package-visibility setters, or public setters guarded by a strict state field (e.g., throw an exception if `state != LOADING`). Do NOT expose raw public setters intended only for DB initialization.
- If Domain Objects need to invoke find methods to fetch related data, define a **Separated Interface** (e.g., `ArtistFinder`) in the Domain package and implement it in the Data Mapper package.

@Workflow
1. **Analyze Domain Complexity**: Evaluate the business logic complexity provided by the user. Determine if the architecture employs Transaction Script, Table Module, or Domain Model.
2. **Select Data Source Pattern**: Map the domain strategy to the appropriate Data Source pattern strictly adhering to the "Pattern Selection Constraints" in the Guidelines.
3. **Design the Schema Mapping**:
   - If Active Record or Row/Table Gateways: map table columns directly to fields.
   - If Data Mapper: define how the disparate object graph maps to relational tables (utilizing Foreign Key Mapping or Association Table Mapping if necessary).
4. **Implement Data Access**: Write the SQL statements (Select, Insert, Update, Delete) and wrap them inside the chosen pattern's methods. Use precompiled static SQL statements.
5. **Implement Finders**: 
   - For Gateways, return Record Sets or DTOs.
   - For Data Mappers, implement Identity Map checks before SQL execution and before object hydration.
6. **Handle Cyclical Dependencies (Data Mapper only)**: Implement empty-object instantiation and Identity Map registration prior to executing field population routines.
7. **Verify Isolation**: Review the codebase to guarantee that no SQL or database API code leaks into the Presentation layer or pure Domain Model layer.

@Examples (Do's and Don'ts)

**Table Data Gateway Returns**
- [DO]: Return explicit data structures or standard Record Sets.
  ```java
  public ResultSet findWithLastName(String lastName) {
      PreparedStatement stmt = db.prepareStatement("SELECT * FROM person WHERE lastname = ?");
      stmt.setString(1, lastName);
      return stmt.executeQuery();
  }
  ```
- [DON'T]: Return a generic Map that obscures the data contract.
  ```java
  public Map<String, Object> findWithLastName(String lastName) { ... } // ANTI-PATTERN
  ```

**Row Data Gateway vs Active Record**
- [DO]: Separate domain logic from DB access if using Row Data Gateway.
  ```java
  // Row Data Gateway - Pure DB Access
  class PersonGateway {
      private String lastName;
      public void update() { /* SQL UPDATE */ }
  }
  // Domain Logic in a separate Transaction Script
  ```
- [DON'T]: Put domain logic inside a Row Data Gateway (this accidentally creates an Active Record).
  ```java
  class PersonGateway {
      public void update() { /* SQL UPDATE */ }
      public Money getExemption() { return base.add(dependents.multiply(750)); } // ANTI-PATTERN for Row Data Gateway
  }
  ```

**Data Mapper - Breaking Cyclical References**
- [DO]: Create the empty object, register it, then load data.
  ```java
  protected DomainObject load(ResultSet rs) throws SQLException {
      Long id = new Long(rs.getLong(1));
      if (loadedMap.containsKey(id)) return loadedMap.get(id);
      
      DomainObject result = createEmptyDomainObject();
      result.setID(id);
      loadedMap.put(id, result); // REGISTER BEFORE LOADING FIELDS
      
      doLoadFields(result, rs);
      return result;
  }
  ```
- [DON'T]: Use a rich constructor that fetches associations before the object is registered in the Identity Map, which will cause a StackOverflow on cyclic relations.
  ```java
  protected DomainObject load(ResultSet rs) {
      // ANTI-PATTERN: Will infinitely recurse if Department also loads this Person
      return new Person(rs.getString("name"), MapperRegistry.department().find(rs.getLong("dept_id")));
  }
  ```

**Data Mapper - Domain Independence**
- [DO]: Use a Separated Interface so the Domain relies only on abstractions.
  ```java
  // In Domain Package
  interface TrackFinder { List findForAlbum(Long albumID); }
  
  // In Data Source Package
  class TrackMapper implements TrackFinder { ... }
  ```
- [DON'T]: Have the Domain Object call the Mapper directly.
  ```java
  // In Domain Package
  class Album {
      public List getTracks() {
          return new TrackMapper().findForAlbum(this.id); // ANTI-PATTERN: Strong coupling to Mapper
      }
  }
  ```