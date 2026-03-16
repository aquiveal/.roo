@Domain
Triggered when the AI is creating, modifying, reviewing, or refactoring object-oriented classes. This applies to any object-oriented programming language (Java, TypeScript, C#, Python, C++, etc.) and activates when the AI is tasked with defining class structures, managing dependencies, extracting methods, or evaluating software architecture at the module/class level.

@Vocabulary
- **Responsibility**: A single reason for a class to change. The core metric for determining if a class is too large.
- **God Class**: An anti-pattern describing a class that has grown too large, knows too much, and handles too many responsibilities (e.g., `SuperDashboard`).
- **Weasel Words**: Ambiguous words in class names (e.g., `Processor`, `Manager`, `Super`) that indicate an unfortunate aggregation of unrelated responsibilities.
- **SRP (Single Responsibility Principle)**: A class or module should have one, and only one, reason to change.
- **Cohesion**: The degree to which the methods of a class manipulate its instance variables. A maximally cohesive class has every variable used by every method.
- **Stepdown Rule**: A formatting convention where code reads like a top-down narrative or newspaper article, with private utility methods placed immediately after the public function that calls them.
- **OCP (Open-Closed Principle)**: Classes should be open for extension but closed for modification.
- **DIP (Dependency Inversion Principle)**: Classes should depend upon abstractions (interfaces), not on concrete details.
- **Test Double / Stub**: A simplified implementation of an interface used exclusively for testing to isolate the class from volatile concrete dependencies.

@Objectives
- Ensure classes are extremely small, measured strictly by the number of responsibilities (reasons to change) rather than lines of code.
- Maintain high cohesion by ensuring methods actively utilize the class's instance variables.
- Aggressively split classes when cohesion drops (e.g., when extracting methods results in instance variables used only by a subset of methods).
- Decouple systems by depending on abstractions (interfaces) rather than concrete implementations, explicitly to enable unit testing and isolate the system from change.
- Organize class internals strictly according to the standard visibility-based top-down hierarchy.

@Guidelines
- **Class Organization and Layout**: 
  - The AI MUST structure the internals of a class in the following exact order:
    1. Public static constants.
    2. Private static variables.
    3. Private instance variables.
    4. Public functions.
    5. Private utility functions.
  - The AI MUST NOT create public instance variables unless absolutely necessary and explicitly justified.
  - The AI MUST place private utilities immediately after the public function that invokes them to follow the Stepdown Rule.
- **Encapsulation**:
  - The AI MUST keep variables and utility functions private by default.
  - The AI MAY loosen encapsulation (e.g., making variables/methods `protected` or package-scope) ONLY if it is strictly necessary for a test in the same package to access them. Loosening encapsulation is always the last resort.
- **Sizing and Naming**:
  - The AI MUST evaluate class size by counting responsibilities, not lines of code.
  - The AI MUST name classes concisely based on their exact responsibility.
  - The AI MUST avoid Weasel Words (`Manager`, `Processor`, `Super`) in class names.
  - The AI MUST internally test the class design by writing a 25-word description of the class. If the description requires the words "if," "and," "or," or "but," the class has too many responsibilities and MUST be split.
- **Single Responsibility Principle (SRP)**:
  - The AI MUST ensure every class has only ONE reason to change.
  - The AI MUST NOT stop refactoring simply because the code "works". It MUST proactively evaluate working code to separate concerns into decoupled units.
- **Cohesion**:
  - The AI MUST keep the number of instance variables in a class small.
  - The AI MUST ensure that every method in a class manipulates one or more of those instance variables.
- **Splitting Classes (Maintaining Cohesion)**:
  - When the AI extracts a small method from a large function, and that method requires local variables, the AI SHOULD promote those variables to instance variables to avoid long parameter lists.
  - If promoting variables causes the class to lose cohesion (i.e., the new instance variables are only used by the newly extracted method), the AI MUST extract that method and those variables into a completely new class.
- **Organizing for Change (OCP)**:
  - The AI MUST NOT use large `switch` or `if/else` chains to handle different types of logic within a single class (e.g., parsing different SQL statement types).
  - The AI MUST extract distinct logical branches into separate subclasses inheriting from an abstract base class, ensuring that adding new features only requires adding new subclasses, not modifying existing code.
- **Isolating from Change (DIP)**:
  - The AI MUST NOT make business-logic classes depend on volatile concrete implementation details (e.g., external APIs, third-party libraries).
  - The AI MUST introduce interfaces to abstract volatile concepts and inject those interfaces into the dependent class's constructor.
  - The AI MUST ensure the design allows tests to easily emulate the external dependency using a Stub or Mock.

@Workflow
1. **Initial Assessment**: When analyzing a class, list its public methods and instance variables.
2. **Responsibility Audit**: Formulate a single-sentence description of the class. Identify every distinct "reason to change". If there is more than one reason, plan a split.
3. **Variable Ordering**: Reorder all variables and methods to strictly match the Class Organization standard (Public Statics -> Private Statics -> Private Instances -> Public Methods -> Private Utilities).
4. **Method Extraction & Cohesion Check**: 
   - Break large public methods into smaller private methods.
   - If passing multiple parameters to the private method, promote them to private instance variables.
   - Immediately check class cohesion. If the class now has clusters of methods and variables that operate independently of the rest of the class, slice that cluster out into a new, smaller class.
5. **Volatility Abstraction**: Identify any concrete dependencies (e.g., database connections, external APIs). Extract an interface for the dependency, change the class to depend on the interface, and inject it via the constructor.
6. **Testability Verification**: Verify that the class can be tested in complete isolation by mocking the injected interfaces.

@Examples (Do's and Don'ts)

**Class Organization & Stepdown Rule**
- [DO]:
```java
public class TextParser {
    public static final String DEFAULT_DELIMITER = ",";
    private static final int MAX_BUFFER = 1024;
    private String rawText;

    public TextParser(String rawText) {
        this.rawText = rawText;
    }

    public List<String> parse() {
        String cleaned = cleanText(this.rawText);
        return splitText(cleaned);
    }

    private String cleanText(String text) {
        return text.trim();
    }

    private List<String> splitText(String text) {
        return Arrays.asList(text.split(DEFAULT_DELIMITER));
    }
}
```
- [DON'T]: Place private helpers at the top of the file, mix instance variables between methods, or make instance variables public without strict justification.

**Single Responsibility & Sizing**
- [DO]: Extract distinct responsibilities into highly cohesive, tiny classes.
```java
public class Version {
    private int major;
    private int minor;
    private int build;

    public int getMajorVersionNumber() { return major; }
    public int getMinorVersionNumber() { return minor; }
    public int getBuildNumber() { return build; }
}
```
- [DON'T]: Create a "God Class" that handles UI focus, configuration, and version tracking all at once.
```java
public class SuperDashboard extends JFrame {
    public Component getLastFocusedComponent() { ... }
    public void setLastFocused(Component c) { ... }
    public int getMajorVersionNumber() { ... } // SRP Violation!
    public void setSystemConfigPath(String path) { ... } // SRP Violation!
}
```

**Organizing for Change (OCP)**
- [DO]: Use abstract classes and polymorphism to allow extension without modification.
```java
public abstract class Sql {
    public Sql(String table, Column[] columns) { ... }
    public abstract String generate();
}

public class CreateSql extends Sql {
    public CreateSql(String table, Column[] columns) { super(table, columns); }
    @Override public String generate() { ... }
}

public class SelectSql extends Sql {
    public SelectSql(String table, Column[] columns) { super(table, columns); }
    @Override public String generate() { ... }
}
```
- [DON'T]: Use a single class that must be modified every time a new behavior is added.
```java
public class Sql {
    public String generate(String type) {
        if (type.equals("select")) {
            // ...
        } else if (type.equals("create")) {
            // ... modification required here for every new type!
        }
    }
}
```

**Isolating from Change (DIP)**
- [DO]: Depend on an interface to decouple volatile implementations and enable easy testing.
```java
public interface StockExchange {
    Money currentPrice(String symbol);
}

public class Portfolio {
    private StockExchange exchange;
    public Portfolio(StockExchange exchange) {
        this.exchange = exchange;
    }
    public Money value() {
        // uses this.exchange.currentPrice("SYMBOL")
    }
}
```
- [DON'T]: Hardcode dependencies to concrete classes that make testing difficult or impossible.
```java
public class Portfolio {
    private TokyoStockExchange exchange; // Concrete dependency!
    public Portfolio() {
        this.exchange = new TokyoStockExchange(); 
    }
}
```