# @Domain
Trigger these rules when defining system architecture, organizing project directories, establishing module boundaries, managing cross-component dependencies, designing interfaces between business logic and external systems (databases, UI, web servers), or setting up new frameworks within an application.

# @Vocabulary
- **Boundary**: A dividing line that separates software elements from one another and restricts the elements on one side from knowing about the elements on the other.
- **Premature Decision**: A decision regarding peripheral details (frameworks, databases, web servers, utility libraries) made before it is strictly necessary, which couples and pollutes the core business logic.
- **Business Rules**: The core application logic and use cases; the "things that matter" which must be protected and isolated from peripheral concerns.
- **Details**: The peripheral mechanisms and technologies (GUI, Database, Web, IO) that support the business rules but are irrelevant to their execution; the "things that don't matter."
- **Plugin Architecture**: A structural pattern where peripheral components (Details) are designed as swappable modules that plug into the core logic (Business Rules) without the core knowing about them.
- **Axis of Change**: The rate and reason a component changes. Boundaries are drawn where an axis of change exists, fulfilling the Single Responsibility Principle (SRP).
- **Asymmetric Relationship**: A dependency structure where one component (the plugin) completely depends on another (the core), but the core is entirely immune to and ignorant of the plugin (e.g., ReSharper depending on Visual Studio).
- **Download and Go**: A deployment goal where users are not burdened with unnecessary external dependencies (like a heavy database) just to run or test the core application.

# @Objectives
- Minimize the human resources required to build and maintain the software system.
- Radically defer and delay all decisions regarding frameworks, databases, web servers, and external environments to the latest possible moment.
- Keep the core business logic pure, untainted, and completely ignorant of the database schema, web delivery mechanisms, and user interface.
- Establish highly asymmetric dependencies where the UI and Database depend entirely on the Business Rules, but the Business Rules depend on nothing.
- Create architectural firewalls (boundaries) across which changes cannot propagate, preventing fragile codebases.

# @Guidelines
- **Defer Peripheral Decisions**: You MUST design the system so that the core business logic can be built, executed, and tested without a database, a web server, or a UI framework.
- **Draw Lines Between Matters and Details**: You MUST explicitly separate components into "things that matter" (Business Rules) and "things that don't" (Details/IO).
- **Invert Dependencies at Boundaries**: The database component and GUI component MUST depend on the Business Rules component. The Business Rules component MUST NEVER depend on the database or GUI.
- **Use Interfaces for Data Access**: You MUST define data access interfaces within the Business Rules component. The actual database implementation MUST reside in a separate component and implement this interface.
- **Treat IO and GUI as Irrelevant**: You MUST abstract input and output. The business rules must accept and return data structures, completely agnostic to whether the UI is a web page, a console, or a thick client.
- **Implement Plugin Architectures**: You MUST treat the Database and the GUI as plugins to the Business Rules. The Business Rules must be capable of accepting any plugin that implements its defined interfaces.
- **Beware Premature 3-Tier/SOA Anti-patterns**: You MUST NOT prematurely adopt massive enterprise-scale, Service-Oriented Architectures, or rigid 3-tier domain object mirroring unless explicitly required by current deployment realities. Avoid unnecessary object serialization, marshaling, and message bus overhead for features that run on a single server.
- **Isolate Axes of Change**: You MUST place boundaries between components that change at different rates and for different reasons (e.g., GUIs change for different reasons than business rules).

# @Workflow
1. **Identify the Core**: Determine the core Business Rules and use cases of the feature requested.
2. **Define the Boundary Interfaces**: Create abstract interfaces within the Business Rules component that define the exact data access and IO services the core logic needs (e.g., a `DataAccessInterface`).
3. **Develop Core in Isolation**: Implement the Business Rules using the interfaces. Do not import or reference any database, framework, or UI libraries.
4. **Create In-Memory Mocks**: Build stubbed or in-memory implementations of the interfaces (e.g., `InMemoryRepository`) to allow the Business Rules to be thoroughly tested and developed without external infrastructure.
5. **Defer External Implementation**: Delay the implementation of the actual database or web delivery mechanism until the core business logic dictates it is absolutely necessary.
6. **Implement Plugins**: When required, create the peripheral components (Database, GUI) as plugins. These components MUST import the Business Rules interfaces and implement them.
7. **Verify Dependency Direction**: Audit the source code dependencies to ensure all arrows point inward toward the Business Rules. Ensure no DB-specific or UI-specific types cross the boundary into the core.

# @Examples (Do's and Don'ts)

**[DO]**
```typescript
// Core Business Rules Component
// Defines what it needs, knows nothing about SQL or HTTP
export interface WikiPageRepository {
  savePage(title: string, content: string): void;
  getPage(title: string): string | null;
}

export class PageEditor {
  constructor(private repo: WikiPageRepository) {}
  
  edit(title: string, newContent: string) {
    // Core business logic operates purely on the interface
    this.repo.savePage(title, newContent);
  }
}

// Database Plugin Component (Outer detail)
// Imports the interface from the core and implements it
import { WikiPageRepository } from '../core/WikiPageRepository';
import { Database } from 'mysql-driver';

export class MySqlWikiPageRepository implements WikiPageRepository {
  savePage(title: string, content: string): void {
    Database.execute("INSERT INTO pages...", [title, content]);
  }
  getPage(title: string): string | null { ... }
}
```

**[DON'T]**
```typescript
// Core Business Rules Component
// ANTI-PATTERN: Core logic imports and couples directly to the database driver
import { MySQLConnection } from 'mysql-driver'; // VIOLATION: Coupling to DB

export class PageEditor {
  private db: MySQLConnection;

  constructor() {
    this.db = new MySQLConnection("mysql://localhost/wiki"); // VIOLATION: Premature decision
  }
  
  edit(title: string, newContent: string) {
    // VIOLATION: Business logic knows about SQL and schemas
    this.db.execute("UPDATE pages SET content = ? WHERE title = ?", [newContent, title]);
  }
}
```

**[DO]**
Start database/persistence development by writing a `MockWikiPage` or `InMemoryPage` class that fulfills the `WikiPageRepository` interface using simple HashMaps/Arrays. Prove the business logic works for months before writing a single line of SQL or configuring a database server.

**[DON'T]**
Create a massive Service-Oriented Architecture with a `ServiceRegistry`, `ContactService`, and `MessageBus` where simple operations require serializing data, faking fields, and bouncing messages across queues for a monolithic deployment. Do not write premature distributed architecture.