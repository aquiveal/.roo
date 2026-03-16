# @Domain
This rule file activates when the AI is tasked with designing, implementing, refactoring, or reviewing data access layers, database integrations, ORM usage, repository patterns, or any code that bridges business logic/use cases with data persistence technologies.

# @Vocabulary
- **Database**: A low-level detail, utility, and mechanism used merely to move data back and forth between storage (disk/RAM) and application memory. It is a "non-entity" from an architectural point of view.
- **Data Model**: The architecturally significant structure and organization given to the data *within* the application memory, completely independent of how it is stored on disk.
- **Bucket of Bits**: The conceptual mental model the AI must hold regarding the database—it is merely a long-term storage mechanism, not a driver of system design.
- **Outer Circles**: The lowest-level, peripheral layers of the system architecture where all knowledge of tabular structures, SQL, and database mechanisms must be strictly confined.
- **Narrow and Safe Data Access Channel**: An interface or abstraction that protects the core system from the database, ensuring the core system remains entirely agnostic to the persistence technology.

# @Objectives
- Treat the database as a completely deferrable and replaceable implementation detail.
- Prevent low-level database mechanisms, technologies, and relational structures from polluting the system architecture, business rules, and UI.
- Maintain absolute separation between the application's Data Model (in-memory data structures) and the Database (storage technology).
- Ensure that business rules and use cases are written as if all data resides entirely in RAM, utilizing standard programming data structures (linked lists, trees, hash tables, stacks, queues).
- Completely encapsulate database performance optimizations (indexes, caches, query schemes) away from business rules.

# @Guidelines
- **Restrict Tabular Knowledge**: You MUST restrict all knowledge of tabular structures (tables, rows, columns, relational foreign keys) and query languages (SQL, ORM methods) to the lowest-level utility functions in the outer circles of the architecture.
- **Never Pass Database Objects**: You MUST NOT allow data access frameworks to pass database rows, tables, or ORM-specific entities (like ActiveRecords) into use cases, business rules, or UI components.
- **Design for RAM**: You MUST design the core business logic to manipulate data using standard RAM-based data structures (e.g., pointers, references, collections). Do not design business logic around relational database constraints.
- **Encapsulate Performance**: You MUST address performance concerns (caching, query optimization) exclusively within the low-level data access mechanisms. These concerns MUST NOT influence or leak into the architecture of the business rules.
- **Bolt-On the Database**: You MUST "bolt" the database on the side of the system. The core application must interact with it only through narrow, safe data access channels (interfaces) that do not expose the underlying storage technology.
- **Technology Agnosticism**: You MUST NOT allow the core architecture to care whether the underlying data store is a relational database (Oracle, SQL Server, MySQL), a document store, or simple flat random-access files.

# @Workflow
1. **Define the Application Data Model**: Design the data structures required by the business rules using plain objects, linked lists, trees, or hash tables. Do not include any database annotations, ORM inheritances, or relational mapping logic.
2. **Define the Narrow Data Access Channel**: Create interfaces (e.g., Gateways or Repositories) within the business rule layer that define exactly what data the business rules need to save or retrieve. These interfaces must use ONLY the pure application Data Model objects.
3. **Implement the Detail**: Create concrete classes in the outermost architectural circle that implement these interfaces. This is the ONLY place where you are permitted to use SQL, ORM libraries, or database drivers.
4. **Translate at the Boundary**: Within the concrete implementation classes, write the mapping logic to translate the database-specific row/table structures into the pure application Data Model objects before returning them to the business layer.
5. **Optimize Internally**: If performance optimizations (like caching or specific query tuning) are required, apply them strictly inside the concrete implementation classes. Never alter the interface or business rules to accommodate database speed constraints.

# @Examples (Do's and Don'ts)

### 1. Separation of Data Model and Database
**[DO]** Define pure domain entities and a narrow interface for data access.
```python
# Core Business Logic (Agnostic of Database)
class Customer:
    def __init__(self, id, name, purchase_history_list):
        self.id = id
        self.name = name
        self.purchase_history_list = purchase_history_list # Standard RAM list

class CustomerGateway: # Narrow, safe channel
    def get_customer(self, customer_id: str) -> Customer:
        pass

class CalculateDiscountsUseCase:
    def __init__(self, gateway: CustomerGateway):
        self.gateway = gateway
        
    def execute(self, customer_id: str):
        customer = self.gateway.get_customer(customer_id)
        # Business logic operates on pure RAM structures
        for purchase in customer.purchase_history_list:
            pass 
```

**[DON'T]** Allow ORM models or database structure to leak into the business rules.
```python
# Anti-pattern: Business logic knows about the database mechanism
class CalculateDiscountsUseCase:
    def execute(self, customer_id: str):
        # DON'T: Using ORM syntax, SQL queries, and relational models in a use case
        customer_row = CustomerModel.query.filter_by(id=customer_id).first()
        purchases = db.execute("SELECT * FROM purchases WHERE customer_id = ?", customer_id)
        
        for purchase in purchases: # Operating on database rows
            pass
```

### 2. Passing Data Across Boundaries
**[DO]** Translate database rows into application data structures at the boundary.
```python
# Outer Circle Utility (The Detail)
class SqlCustomerGateway(CustomerGateway):
    def get_customer(self, customer_id: str) -> Customer:
        # 1. Fetch from DB
        row = db.execute("SELECT * FROM customers WHERE id = ?", customer_id)
        # 2. Translate table row to pure in-memory Data Model
        return Customer(id=row['id'], name=row['name'], purchase_history_list=[])
```

**[DON'T]** Pass database rows or tables directly to the UI or Use Cases.
```python
class SqlCustomerGateway:
    def get_customer(self, customer_id: str):
        # DON'T: Returning a raw SQL row or Active Record object to the caller
        return db.execute("SELECT * FROM customers WHERE id = ?", customer_id).fetchone()
```

### 3. Encapsulating Performance
**[DO]** Hide performance strategies (caching, indexing) inside the data access implementation.
```python
class SqlCustomerGateway(CustomerGateway):
    def __init__(self):
        self.cache = {} # Caching encapsulated as a low-level detail

    def get_customer(self, customer_id: str) -> Customer:
        if customer_id in self.cache:
            return self.cache[customer_id]
        
        row = db.execute("SELECT * FROM customers WHERE id = ?", customer_id)
        customer = Customer(id=row['id'], name=row['name'], purchase_history_list=[])
        self.cache[customer_id] = customer
        return customer
```

**[DON'T]** Force the business logic to manage database performance constraints.
```python
class CalculateDiscountsUseCase:
    def execute(self, customer_id: str):
        # DON'T: Business logic handling cache management or DB optimization
        customer = redis_cache.get(customer_id)
        if not customer:
            customer = db.query(f"SELECT * FROM customers USE INDEX(idx_cust) WHERE id={customer_id}")
            redis_cache.set(customer_id, customer)
```