# @Domain

This rule file MUST be activated when the AI is tasked with generating, refactoring, or reviewing code that interacts with architectural boundaries. This includes:
- User Interface (UI) development (Views, Controllers, components, templates).
- Presentation logic and data formatting for user display.
- Database access layers, repository implementations, and Object-Relational Mapping (ORM) integrations.
- External service integrations (APIs, web services, message queues, service listeners).
- Writing unit tests for any component that interacts with I/O, UI, databases, or external frameworks.

# @Vocabulary

- **Humble Object Pattern**: A design pattern used to divide behaviors at architectural boundaries into two distinct modules: one that is "humble" (contains bare-essence, hard-to-test behaviors like UI rendering or I/O) and one that is "testable" (contains all processing, formatting, and logic).
- **View**: The humble object in a UI architecture. It is hard to test, contains absolutely zero processing or formatting logic, and strictly moves data from a View Model to the screen.
- **Presenter**: The highly testable object responsible for accepting application data, processing/formatting it, and placing it into a View Model.
- **View Model**: A simple data structure populated by the Presenter, consisting entirely of primitives (Strings, Booleans, Enums) that represent the exact state and content of the UI.
- **Database Gateway**: A polymorphic interface residing between the use case interactors and the database. It defines CRUD operations.
- **Data Mapper**: The accurate term for an ORM (Object-Relational Mapper). It loads relational data into simple data structures (not true objects with behavior) and must reside strictly within the database layer.
- **Service Listener**: A humble object at a service boundary that receives data from an external interface and formats it into a simple data structure for the application to use.
- **Interactor**: An object that encapsulates application-specific business rules. It is highly testable, NOT humble, and relies on stubs/mocks of Database Gateways during testing.

# @Objectives

- Maximize system testability by ruthlessly separating easy-to-test logic from hard-to-test I/O, framework, or UI logic.
- Establish strict architectural boundaries using the Humble Object pattern.
- Ensure that communication across boundaries relies exclusively on simple, independent data structures.
- Prevent external details (UI, SQL, ORMs, Network protocols) from leaking into the core application business rules and interactors.

# @Guidelines

- **Humble Object Enforcement**: Whenever encountering a component that interacts with a framework, UI, database, or external service, the AI MUST split the component into a Testable Object (logic) and a Humble Object (delivery/execution).
- **View Constraints**: The AI MUST NOT put any formatting, conditional styling, or data processing logic inside a View. The View MUST only bind to or read from primitive values provided by the View Model.
- **Presenter Responsibilities**: The AI MUST place all data formatting logic in the Presenter. 
  - Domain types (e.g., `Date`, `Currency`) MUST be converted to formatted strings inside the Presenter.
  - UI state (e.g., negative value color coding, button disabled/enabled state) MUST be evaluated in the Presenter and assigned to boolean flags in the View Model.
- **Boundary Data Structures**: The AI MUST use simple data structures to cross architectural boundaries. Do not pass domain entities, active records, or complex behavioral objects across boundaries to Humble Objects.
- **Database Gateway Rule**: The AI MUST NOT write SQL, database queries, or ORM calls directly inside use case Interactors. Interactors MUST rely on injected Database Gateway interfaces.
- **Data Mapper (ORM) Isolation**: The AI MUST place all ORM code and framework-specific database logic inside the Humble Object implementation of the Database Gateway. ORM models must be treated as simple data structures mapped to database tables, NOT as behavioral business objects.
- **External Service Isolation**: The AI MUST implement Service Listeners as Humble Objects. They must merely receive external payloads, map them to simple internal data structures, and pass them across the boundary to the testable application logic.
- **Test Double Integration**: The AI MUST write tests for Presenters, Interactors, and core logic by providing stubs, mocks, or test-doubles for the corresponding Humble Objects (Views, Gateways, Listeners).

# @Workflow

When implementing a feature that crosses an architectural boundary (UI, Database, or Service), the AI MUST execute the following step-by-step algorithm:

1. **Identify the Boundary**: Determine if the task involves UI rendering, Database I/O, or Network/Service communication.
2. **Define the Data Structure**: Create a simple data structure (e.g., a View Model for UI, or a Data Transfer Object for services) composed solely of primitives. This structure will cross the boundary.
3. **Build the Testable Component (Presenter/Interactor)**:
   - For UI: Create a Presenter that takes application/domain data, formats it completely, and populates the View Model.
   - For DB/Services: Create an Interactor that performs the business logic and calls a boundary interface (Database Gateway).
4. **Build the Humble Component (View/Mapper/Listener)**:
   - For UI: Create a View that passively reads the View Model and updates the screen.
   - For DB: Create a repository implementation that uses SQL/ORM to satisfy the Database Gateway interface.
5. **Verify Testability**: Ensure the Testable Component can be fully unit-tested without instantiating the GUI, the Database, or the Network. Write the tests using mocks for the Humble interfaces.

# @Examples (Do's and Don'ts)

### Presenters and Views

- **[DO]**: Separate formatting into a Presenter and a dumb View using a View Model.
  ```javascript
  // View Model (Simple Data Structure)
  class AccountViewModel {
      constructor() {
          this.formattedBalance = "";
          this.isBalanceNegative = false;
          this.submitButtonEnabled = false;
      }
  }

  // Presenter (Testable Object)
  class AccountPresenter {
      constructor(view) {
          this.view = view;
      }
      present(account) {
          const viewModel = new AccountViewModel();
          viewModel.formattedBalance = `$${account.balance.toFixed(2)}`;
          viewModel.isBalanceNegative = account.balance < 0;
          viewModel.submitButtonEnabled = account.isActive;
          this.view.render(viewModel);
      }
  }

  // View (Humble Object)
  class AccountView {
      render(viewModel) {
          document.getElementById('balance').innerText = viewModel.formattedBalance;
          document.getElementById('balance').style.color = viewModel.isBalanceNegative ? 'red' : 'black';
          document.getElementById('submitBtn').disabled = !viewModel.submitButtonEnabled;
      }
  }
  ```

- **[DON'T]**: Pass domain objects to the View and embed formatting/conditional logic inside the UI.
  ```javascript
  // ANTI-PATTERN: View contains processing and formatting logic
  class AccountView {
      render(account) {
          // DON'T do formatting in the view
          const formatted = "$" + account.balance.toFixed(2);
          document.getElementById('balance').innerText = formatted;
          
          // DON'T do conditional business logic in the view
          if (account.balance < 0) {
              document.getElementById('balance').style.color = 'red';
          }
      }
  }
  ```

### Database Gateways and ORMs

- **[DO]**: Use a Gateway interface for the Interactor, and hide the ORM in the implementation.
  ```javascript
  // Database Gateway Interface
  class UserGateway {
      getLastNamesOfUsersWhoLoggedInAfter(date) { throw new Error("Not implemented"); }
  }

  // Interactor (Testable, Application Rules)
  class ReportInteractor {
      constructor(userGateway) {
          this.userGateway = userGateway; // Injected
      }
      generateRecentUsersReport(date) {
          // Ignorant of SQL/ORM
          const names = this.userGateway.getLastNamesOfUsersWhoLoggedInAfter(date);
          return names.join(", ");
      }
  }

  // Database Implementation (Humble Object / Data Mapper)
  class HibernateUserGateway extends UserGateway {
      getLastNamesOfUsersWhoLoggedInAfter(date) {
          // ORM logic is isolated here
          const records = ORM.query("SELECT last_name FROM users WHERE last_login > ?", [date]);
          return records.map(record => record.last_name);
      }
  }
  ```

- **[DON'T]**: Leak ORM details or SQL directly into the Interactor.
  ```javascript
  // ANTI-PATTERN: Interactor is coupled to the database framework
  class ReportInteractor {
      generateRecentUsersReport(date) {
          // DON'T use ORM/SQL directly in the business logic
          const records = ORM.query("SELECT last_name FROM users WHERE last_login > ?", [date]);
          return records.map(record => record.last_name).join(", ");
      }
  }
  ```