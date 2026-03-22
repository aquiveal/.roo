@Domain
These rules MUST activate when the AI is tasked with implementing, modifying, or refactoring Object-Relational Mapping (ORM) layers, data access objects (DAOs), dynamic database query generators, or layers that mediate between a Domain Model and a relational database. Specifically, these rules apply when the user requests the creation of Metadata Mappings, Query Objects, or Repositories to decouple in-memory domain objects from database schemas.

@Vocabulary
- **Metadata Mapping**: A pattern that holds the details of object-relational mapping in a tabular form or metadata (XML, DB, or code structures) to drive generic code that reads, inserts, and updates data, removing repetitive handwritten mapping code.
- **Code Generation**: A Metadata Mapping implementation strategy where mapping code is generated at build time.
- **Reflective Programming**: A Metadata Mapping implementation strategy where generic code uses reflection at runtime to dynamically inspect classes and execute mapping based on metadata.
- **Query Object**: An object representing a database query using the Interpreter pattern. It allows clients to form queries using the language of in-memory objects (classes and fields) rather than database schemas (tables and columns).
- **Criteria (Specification)**: An object representing the parameters or constraints of a query (e.g., `field > value`), used to compose a Query Object.
- **Repository**: An architectural layer that mediates between the domain and data mapping layers. It acts as an in-memory domain object collection, accepting declarative Criteria objects to select and filter domain objects.
- **Repository Strategy**: A pattern used within a Repository to swap out the underlying data source (e.g., swapping a `RelationalStrategy` that issues SQL for an `InMemoryStrategy` that iterates over collections for unit testing).
- **DataMap**: A metadata construct mapping a single domain class to a database table.
- **ColumnMap**: A metadata construct mapping a single database column to an object field.

@Objectives
- Completely isolate the Domain Model from the database schema and SQL syntax.
- Eliminate repetitive, boilerplate CRUD mapping code by abstracting it into generic Layer Supertypes driven by metadata.
- Allow developers to construct database queries safely and dynamically using Domain concepts (classes/fields) rather than relational concepts (tables/columns).
- Provide a collection-like interface to the persistent layer so domain logic interacts with data as if it were an in-memory collection.
- Support seamless switching of underlying data sources (e.g., for fast, isolated unit testing) without modifying domain logic.

@Guidelines

**Metadata Mapping Rules**
- When implementing mapping logic for multiple domain objects, the AI MUST NOT write repetitive, explicit SQL mapping code for each class. Instead, the AI MUST use Metadata Mapping (either via Code Generation or Reflective Programming) to drive generic CRUD operations.
- When using Code Generation, the AI MUST ensure that the generated code is completely integrated into the build process. The AI MUST NOT modify generated mapping classes by hand.
- When using Reflective Programming, the AI MUST read mappings from a centralized definition (XML, properties, or setup code) and use reflection to bypass visibility rules (e.g., `field.setAccessible(true)`) to populate domain objects.
- When encountering special-case mapping requirements that do not fit the generic metadata schema, the AI MUST NOT overcomplicate the metadata definition. Instead, the AI MUST override the specific generic hook method (e.g., `doLoad` or `loadFields`) in a handwritten subclass mapped to that specific domain object.

**Query Object Rules**
- When constructing queries dynamically, the AI MUST implement a Query Object that utilizes the Interpreter pattern. 
- The AI MUST ensure that Query Objects accept Criteria defined strictly in terms of Domain Model class names and field names, NOT database table and column names.
- The AI MUST use the Metadata Mapping (e.g., `DataMap` and `ColumnMap`) within the Query Object to translate the domain-level Criteria into the correct SQL strings.
- The AI MUST design the Query Object iteratively; start with minimally functional query capabilities (e.g., simple `AND` clauses) and expand only as application needs grow.

**Repository Rules**
- When domain logic requires access to data, the AI MUST NOT allow domain objects to directly invoke SQL finders or instantiate Query Objects. Instead, the AI MUST implement a Repository.
- The AI MUST design the Repository to mimic a simple in-memory collection (e.g., using methods like `matching(Criteria c)`, `all()`, or `soleMatch(Criteria c)`).
- When implementing the Repository's internal execution, the AI MUST encapsulate the instantiation of Query Objects and the generation of SQL. 
- The AI MUST implement Repository Strategies (e.g., `RepositoryStrategy` interface) to allow the underlying data source to be swapped. At minimum, support a `RelationalStrategy` (for production) and an `InMemoryStrategy` (for testing or immutable object caching).

@Workflow
When tasked with building an object-relational metadata mapping system, the AI MUST follow this rigid step-by-step process:

1. **Define the Metadata Structure**: Create `DataMap` and `ColumnMap` classes (or equivalent XML/configuration structures) that pair domain classes to tables and fields to columns. 
2. **Implement the Abstract Mapper**: Create a Layer Supertype that reads the metadata and implements generic `find`, `insert`, `update`, and `load` methods. 
3. **Handle Instantiation and Population**: Within the Abstract Mapper, use reflection (or build-time generation) to instantiate domain objects and inject data into fields based on the `ColumnMap`.
4. **Implement Criteria and Query Objects**: Create a `Criteria` class (to hold fields, operators, and values) and a `QueryObject` class. Program the `QueryObject` to translate `Criteria` into SQL by querying the `DataMap`.
5. **Build the Repository Interface**: Define a `Repository` interface that accepts `Criteria` objects and returns Domain Objects.
6. **Implement Repository Strategies**: Create a `RelationalStrategy` that feeds the `Criteria` into the `QueryObject` for DB execution, and an `InMemoryStrategy` that uses reflection to evaluate the `Criteria` against an in-memory `Set` or `List` of domain objects.
7. **Address Edge Cases**: For any mapping that breaks the generic metadata rules, create a subclass of the Abstract Mapper and explicitly override the necessary mapping phase (e.g., `loadFields`).

@Examples (Do's and Don'ts)

**[DO] Use handwritten subclasses to override complex, special-case mappings.**
```java
// DO: Extend the generic metadata mapper for a special case
class PersonMapper extends AbstractMetadataMapper {
    protected void loadFields(ResultSet rs, DomainObject result) throws SQLException {
        super.loadFields(rs, result); // Do standard metadata mapping
        // Handle the weird special case explicitly
        Person person = (Person) result;
        person.setCustomCalculatedField(rs.getString("weird_legacy_column") + " format");
    }
}
```

**[DON'T] Tangle the metadata schema with boolean flags for one-off edge cases.**
```java
// DON'T: Pollute generic metadata with one-off rules
dataMap.addColumn("weird_legacy_column", "varchar", "customCalculatedField", true, false, " format");
```

**[DO] Use domain terminology in Query Objects and translate using Metadata.**
```java
// DO: Form queries using Domain concepts
QueryObject query = new QueryObject(Person.class);
query.addCriteria(Criteria.greaterThan("numberOfDependents", 0));
query.addCriteria(Criteria.matches("lastName", "F%"));

// The Query Object translates this internally:
public String generateSql(DataMap dataMap) {
    return dataMap.getColumnForField(field) + sqlOperator + value;
}
```

**[DON'T] Leak database schema details into dynamic query construction.**
```java
// DON'T: Write SQL or table names directly in domain-level querying
QueryObject query = new QueryObject();
query.addSql("SELECT * FROM people p WHERE p.number_of_dependents > 0 AND p.lastname LIKE 'F%'");
```

**[DO] Use a Repository to hide querying mechanics from the Domain.**
```java
// DO: Interact with the Repository as if it were a collection
public class Person {
    public List dependents() {
        Repository repository = Registry.personRepository();
        Criteria criteria = new Criteria();
        criteria.equal(Person.BENEFACTOR, this);
        return repository.matching(criteria); // Declarative
    }
}
```

**[DON'T] Invoke SQL or Mappers directly from the Domain layer when Repositories are needed.**
```java
// DON'T: Mix mapping/SQL execution directly in the domain logic
public class Person {
    public List dependents() {
        PersonMapper mapper = new PersonMapper();
        return mapper.findObjectsWhere("benefactor_id = " + this.getId());
    }
}
```

**[DO] Abstract Repository execution into swappable strategies.**
```java
// DO: Provide an InMemoryStrategy for tests
public class InMemoryStrategy implements RepositoryStrategy {
    private Set domainObjects;
    protected List matching(Criteria criteria) {
        List results = new ArrayList();
        for (DomainObject each : domainObjects) {
            if (criteria.isSatisfiedBy(each)) {
                results.add(each);
            }
        }
        return results;
    }
}
```