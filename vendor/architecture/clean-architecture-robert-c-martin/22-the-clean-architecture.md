# @Domain
Trigger these rules when tasked with designing system architecture, restructuring or refactoring code bases, implementing separation of concerns, defining software layers, establishing module dependencies, or writing features that cross boundaries between business logic, user interfaces, and external systems (such as databases or frameworks).

# @Vocabulary
- **Clean Architecture**: A layered software architecture model that separates concerns, ensuring systems are independent of frameworks, testable, and independent of UIs, databases, and external agencies.
- **The Dependency Rule**: The overriding architectural rule stating that source code dependencies must point *only* inward, toward higher-level policies.
- **Entities**: The innermost circle encapsulating enterprise-wide Critical Business Rules. Can be objects with methods or a set of data structures and functions.
- **Use Cases**: The layer containing application-specific business rules. It orchestrates the flow of data to and from Entities and directs them to achieve specific goals.
- **Interface Adapters**: The layer containing adapters that convert data from the format most convenient for Use Cases and Entities into the format most convenient for external agencies (e.g., the Web or a Database). Includes MVC components (Controllers, Presenters, Views).
- **Frameworks and Drivers**: The outermost circle composed of details, frameworks, and tools such as databases and web servers. Contains mostly glue code.
- **Boundary Crossing**: The point where the flow of control crosses from one layer to another. 
- **Dependency Inversion Principle (DIP)**: Used at boundary crossings to invert source code dependencies against the flow of control (e.g., using polymorphic interfaces) so the Dependency Rule is maintained.
- **InputBoundary / OutputBoundary**: Interfaces defined in the inner circle (Use Cases) that are called by or implemented by outer circles to facilitate boundary crossing.
- **Data Transfer Objects (DTOs)**: Isolated, simple data structures passed across boundaries.
- **ViewModel**: A simple data structure constructed by a Presenter containing mostly Strings and boolean flags perfectly formatted for the View to blindly render.

# @Objectives
- Achieve total separation of concerns by dividing the software into strict concentric layers.
- Ensure the system is fundamentally testable without requiring the UI, database, web server, or any external element.
- Maintain strict independence from frameworks, treating them as interchangeable tools rather than architectural constraints.
- Maintain strict independence from the UI, allowing interfaces to change (e.g., Web to Console) without impacting business rules.
- Maintain strict independence from the Database and external agencies, ensuring business rules have zero knowledge of the outside world.

# @Guidelines
- **Enforce the Dependency Rule:** Nothing in an inner circle can know anything at all about something in an outer circle. Do not mention functions, classes, variables, or any named software entity from an outer circle in an inner circle.
- **Protect the Inner Circles from Outer Formats:** Data formats declared in an outer circle (e.g., framework-generated objects or database row structures) MUST NOT be used by an inner circle. 
- **Entity Layer Constraints:** Entities must encapsulate the most general and high-level rules. They must not be affected by operational changes, page navigation, or security features.
- **Use Case Layer Constraints:** Use Cases must encapsulate all application-specific business rules. They must not be affected by changes to the database, UI, or frameworks. They orchestrate Entities but do not contain Entity-level rules.
- **Interface Adapter Constraints:** All MVC components (Presenters, Views, Controllers) live exclusively in this layer. All SQL queries must be restricted entirely to the database parts of this layer. Code inward of this layer must not know anything about the database.
- **Frameworks and Drivers Constraints:** Keep frameworks, web servers, and databases on the absolute outside of the architecture. Write only glue code here to communicate with the next circle inward.
- **Data Crossing Constraints:** Data passed across boundaries MUST consist of isolated, simple data structures (basic structs, simple DTOs, function arguments, or hashmaps). 
- **Prevent Boundary Cheating:** You MUST NOT pass Entity objects or raw database rows across architectural boundaries. Always convert data into the form most convenient for the inner circle.
- **Resolve Control Flow Contradictions:** When the flow of control points outward (e.g., Use Case calling a Presenter), use the Dependency Inversion Principle. Define an interface (Output Port) in the inner circle, and have the outer circle class (Presenter) implement it.
- **Dumb Views:** The View must have almost nothing to do. The Presenter must pre-format all Dates, Currency, button names, and state flags (e.g., graying out a button) into a ViewModel of simple Strings and booleans.

# @Workflow
1. **Identify the Layers**: Categorize the requested feature into Frameworks/Drivers, Interface Adapters, Use Cases, and Entities.
2. **Define the Data Structures**: Create simple, isolated POJOs/DTOs for data crossing boundaries (e.g., `InputData`, `OutputData`, `ViewModel`). Ensure no database or framework-specific types leak into these structures.
3. **Implement the Entities**: Draft the high-level, enterprise-critical business rules completely devoid of external dependencies.
4. **Implement the Use Cases (Interactors)**: 
   - Define an `InputBoundary` interface.
   - Write the Interactor implementing the `InputBoundary`.
   - Orchestrate the Entities.
   - Define an `OutputBoundary` interface for the result.
5. **Implement the Interface Adapters**:
   - Create the Controller to gather user input, package it into the `InputData` structure, and pass it to the `InputBoundary`.
   - Create the Presenter implementing the `OutputBoundary` interface. It must receive `OutputData` and repackage it into a `ViewModel` (Strings and boolean flags).
   - Create the Database Adapters implementing data access interfaces defined by the Use Case. Isolate all SQL here.
6. **Implement the Frameworks/Drivers**: Wire the web framework to the Controller and the View to the `ViewModel`. Wire the actual database driver to the Database Adapter.
7. **Verify the Dependency Rule**: Audit all `import` or `using` statements. Ensure no module imports a module from a layer closer to the edges of the architecture.

# @Examples (Do's and Don'ts)

- **[DO]** Use Dependency Inversion for outward control flow.
```java
// Inner Circle (Use Case Layer)
public class OutputData { 
    public final Date creationDate; 
    public OutputData(Date creationDate) { this.creationDate = creationDate; }
}

public interface UseCaseOutputBoundary {
    void present(OutputData data);
}

public class UseCaseInteractor {
    private final UseCaseOutputBoundary presenter;
    public UseCaseInteractor(UseCaseOutputBoundary presenter) { this.presenter = presenter; }
    
    public void execute() {
        OutputData data = new OutputData(new Date());
        presenter.present(data); // Flow goes outward, but dependency points inward
    }
}

// Outer Circle (Interface Adapters Layer)
public class ViewModel { public String formattedDate; }

public class WebPresenter implements UseCaseOutputBoundary {
    public ViewModel viewModel = new ViewModel();
    public void present(OutputData data) {
        viewModel.formattedDate = new SimpleDateFormat("yyyy-MM-dd").format(data.creationDate);
    }
}
```

- **[DON'T]** Allow Use Cases to know about outer-circle formats or pass Entities to the UI.
```java
// ANTI-PATTERN: Inner circle importing web framework details and returning an Entity directly
import javax.servlet.http.HttpServletRequest; // VIOLATION: Framework detail in Use Case
import com.database.sql.ResultSet; // VIOLATION: Database detail in Use Case

public class UseCaseInteractor {
    public UserEntity execute(HttpServletRequest request, ResultSet dbRow) {
        // ... business logic ...
        return new UserEntity(); // VIOLATION: Passing Entity object across boundary
    }
}
```

- **[DO]** Keep the View extremely dumb by doing all formatting in the Presenter.
```java
// Interface Adapters Layer
public class CheckoutViewModel {
    public String displayPrice;
    public boolean isCheckoutButtonDisabled;
}

public class CheckoutPresenter implements CheckoutOutputBoundary {
    public CheckoutViewModel present(CheckoutResponse response) {
        CheckoutViewModel model = new CheckoutViewModel();
        model.displayPrice = "$" + String.format("%.2f", response.price);
        model.isCheckoutButtonDisabled = response.inventoryCount <= 0;
        return model;
    }
}
```

- **[DON'T]** Put formatting logic or business logic inside the View or Controller.
```html
<!-- ANTI-PATTERN: View doing formatting and conditional logic -->
<div>
    <span> Price: $<%= String.format("%.2f", entity.getPrice()) %> </span>
    <% if (entity.getInventoryCount() <= 0) { %>
        <button disabled>Checkout</button>
    <% } else { %>
        <button>Checkout</button>
    <% } %>
</div>
```

- **[DO]** Restrict all SQL to the Interface Adapters layer using polymorphic interfaces.
```java
// Inner Circle (Use Case Layer)
public interface UserRepository {
    void save(User userDto);
}

// Outer Circle (Interface Adapters Layer)
public class SqlUserRepository implements UserRepository {
    public void save(User userDto) {
        String sql = "INSERT INTO users (name) VALUES (?)"; // SQL stays in this layer
        // execute SQL...
    }
}
```

- **[DON'T]** Leak SQL or database mechanisms into the Use Case layer.
```java
// ANTI-PATTERN: SQL in the Use Case
public class UserInteractor {
    public void createUser(String name) {
        String sql = "INSERT INTO users (name) VALUES ('" + name + "')"; // VIOLATION
        Database.execute(sql);
    }
}
```