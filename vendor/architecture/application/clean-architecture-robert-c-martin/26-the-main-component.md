# @Domain
Activation conditions: Triggers when the AI is creating, modifying, architecting, or refactoring the entry point of a software system (e.g., `main()` functions, `index.js`, `Program.cs`, application bootstrappers), dependency injection composition roots, or environment-specific configuration loaders.

# @Vocabulary
- **Main Component**: The ultimate detail and lowest-level policy of the system; the initial entry point that creates, coordinates, and oversees all other components.
- **Dirty Component**: A module that deliberately contains messy, low-level details (such as string literals, UI configurations, and dependency wirings) to keep the rest of the architecture clean. Main is the "dirtiest of all the dirty components."
- **Plugin (Main as a Plugin)**: The concept that the Main component is an interchangeable module representing a specific configuration of the application (e.g., Dev, Test, Production), which plugs into the high-level policy.
- **High-Level Policy**: The abstract, core business logic of the system that receives control from Main and remains completely ignorant of Main's implementation details.

# @Objectives
- Establish the Main component as the ultimate detail, ensuring it contains no core business logic.
- Centralize all system initialization, object instantiation, and dependency wiring within the Main component.
- Protect the high-level architectural core from frameworks, hardware details, configuration strings, and instantiation logic.
- Ensure the application supports multiple distinct deployment configurations by treating the Main component as an interchangeable plugin.

# @Guidelines
- **Absolute Dependency Rule**: The AI MUST ensure that NO component in the system depends on the Main component. The only entity that depends on Main is the operating system.
- **Centralized Creation**: The AI MUST place the creation and initialization of all Factories, Strategies, and global facilities exclusively within the Main component.
- **Dependency Injection Restriction**: The AI MUST restrict the use of Dependency Injection (DI) frameworks to the Main component. Once dependencies are injected into Main, Main MUST distribute those dependencies to the rest of the system normally (via constructors or method parameters), without spreading the DI framework into the high-level abstract portions of the system.
- **Quarantine of Details**: The AI MUST place hardcoded strings, configuration arrays (e.g., lists of display names, environment variables), and initial state values inside Main to ensure the main body of the code has no knowledge of these low-level details.
- **Decoupled Handoff**: The AI MUST ensure that Main acts only as a setup and coordination layer. After establishing the initial conditions and gathering outside resources, Main MUST explicitly hand control over to the high-level policy of the application and defer all actual processing to those components.
- **String-Based Instantiation**: To prevent changes in dirty sub-components from causing Main to recompile or redeploy, the AI SHOULD instantiate dirty facade classes using strings (e.g., `Factory.make("com.app.Facade")`) where appropriate.
- **Main as a Plugin**: The AI MUST architect the system such that Main is an interchangeable plugin. The AI MUST support the creation of multiple Main components to handle different configurations (e.g., a Main plugin for Development, a Main plugin for Testing, a Main plugin for Production, or distinct Main plugins for different customers/jurisdictions).

# @Workflow
1. **Identify Entry Point**: Locate the application's root entry point (the Main component).
2. **Strip Business Logic**: Extract any and all business rules, algorithms, or high-level policies currently residing in Main and move them into independent, abstract high-level components.
3. **Consolidate Initialization**: Move all object instantiation, factory creation, and strategy definitions into Main.
4. **Isolate Frameworks**: Locate any DI framework annotations or framework-specific wiring spread across the business logic. Remove them and centralize the DI container configuration entirely within Main. 
5. **Extract Low-Level Strings**: Identify hard-coded configuration strings, display lists, and environmental constants in the business rules. Extract these and define them in Main, passing them inward only as needed via generic data structures.
6. **Implement Control Handoff**: Write the core execution loop (if applicable) or startup sequence in Main, ensuring it delegates all commands and events to the high-level components without processing the business logic itself.
7. **Create Configuration Variants**: If the system targets multiple environments (e.g., Test, Prod), create separate Main components (plugins) for each environment, keeping the core application entirely unchanged.

# @Examples (Do's and Don'ts)

**[DO]**
```java
// Main acts as a dirty plugin, handles DI, string constants, and hands off control.
public class MainProdPlugin {
    // Dirty details kept out of the business logic
    private static final String[] DB_CONFIG = {"prod_db_url", "user", "pass"};
    
    public static void main(String[] args) {
        // DI Framework used ONLY here
        DIContainer container = new DIContainer();
        container.register(Database.class, new ProductionDatabase(DB_CONFIG));
        
        // Main creates factories and strategies
        GameFactory factory = new GameFactory(container.resolve(Database.class));
        
        // Handoff to high-level abstract policy
        // Using string to prevent recompilation dependencies on the concrete class
        Game game = factory.makeGame("com.example.game.ProdGameFacade");
        
        // Deferring all processing to the high-level policy
        InputReader reader = new InputReader(System.in);
        while(true) {
            Command c = reader.getCommand();
            if (c.isQuit()) break;
            game.executeCommand(c); // Main does not process the command
        }
    }
}
```

**[DON'T]**
```java
// Anti-pattern: Main contains business logic, and DI frameworks pollute the core.
public class Main {
    public static void main(String[] args) {
        // Main processing business rules directly
        int hitPoints = 10;
        String playerCommand = System.console().readLine();
        
        if (playerCommand.equals("n")) {
            // Anti-pattern: Main handling core domain logic
            hitPoints -= 2; 
            System.out.println("You moved north and took damage.");
        }
    }
}

// Anti-pattern: Core business logic knows about the DI framework.
import org.springframework.beans.factory.annotation.Autowired;

public class Game {
    @Autowired // VIOLATION: The high-level policy is polluted by the DI framework!
    private Database database;
    
    // VIOLATION: Dirty string configurations living inside high-level policy!
    private String[] environments = {"bright", "humid", "dry"}; 
    
    public void executeCommand(Command c) {
        // ...
    }
}
```