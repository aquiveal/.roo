@Domain
Trigger these rules when the user requests the design, implementation, refactoring, or evaluation of a "Microkernel Architecture" (also known as a "Plug-in Architecture"). Activate these rules when tasks involve product-based applications (packaged, downloadable software), or applications requiring high extensibility, adaptability, and the isolation of highly volatile, custom, or client-specific processing logic (e.g., complex rules engines, tax preparation software, insurance claims processing, or hardware assessment tools).

@Vocabulary
- **Microkernel Architecture Style / Plug-in Architecture**: A monolithic architecture style consisting of a core system and independent plug-in components.
- **Core System**: The minimal functionality required to run the system; the general processing flow or "happy path" stripped of custom processing or high cyclomatic complexity.
- **Plug-in Components**: Standalone, independent components containing specialized processing, additional features, and custom code meant to enhance or extend the core system.
- **Point-to-Point Communication**: Direct method invocations or function calls used as the standard pipe connecting the plug-in to the core system.
- **Compile-based Plug-ins**: Plug-ins that require the entire monolithic application to be redeployed when modified, added, or removed.
- **Runtime-based Plug-ins**: Plug-ins that can be added or removed at runtime without redeploying the core system (e.g., using OSGi, Penrose, Jigsaw, Prism).
- **Plug-in Registry**: A mechanism (internal map or external discovery tool like ZooKeeper/Consul) that contains information about available plug-in modules, their contracts, and access details.
- **Contracts**: Standardized definitions of behavior, input data, and output data between the plug-in and the core system.
- **Adapter**: A design pattern used to wrap third-party plug-in components so they conform to the core system's standard contract.
- **Architecture Quantum**: The scope of architecture characteristics. The microkernel architecture is fundamentally a single architecture quantum because all requests must go through the monolithic core system.

@Objectives
- The AI MUST isolate client-specific, volatile, or custom logic from the main application flow to reduce cyclomatic complexity.
- The AI MUST design the system to be highly extensible, allowing new features to be added or removed without impacting the core system or other features.
- The AI MUST enforce strict boundaries between the core system and plug-ins, ensuring plug-ins remain decoupled from one another and from central data stores.

@Guidelines

**Core System Constraints**
- The AI MUST remove complex conditional logic (e.g., massive `if/else` or `switch` statements) from the core system and delegate that logic to discrete plug-in components.
- The AI MAY implement the core system as a layered architecture, a modular monolith, or as separately deployed domain services (provided they manage their own plug-ins).

**Plug-in Constraints**
- The AI MUST ensure plug-in components are entirely independent. Plug-ins MUST NOT possess dependencies on other plug-in components.
- The AI MUST package plug-ins as shared libraries (JAR, DLL, Gem) OR as cleanly separated namespaces/packages within the same codebase.
- When using namespaces for plug-ins, the AI MUST use the semantic structure: `app.plugin.<domain>.<context>` (e.g., `app.plugin.assessment.iphone6s`).

**Communication & Invocation**
- The AI MUST default to point-to-point communication (method/function calls) between the core system and plug-ins.
- The AI MAY use REST or asynchronous messaging to invoke plug-ins ONLY if remote access, dynamic scalability, or asynchronous responsiveness is explicitly required, while noting the trade-off of increased deployment complexity and transition to a distributed architecture.

**Data & State Management**
- The AI MUST strictly prohibit plug-in components from connecting directly to the centrally shared database.
- The AI MUST mandate that the core system retrieves necessary data and passes it into the plug-in component.
- The AI MAY allow plug-in components to own and manage their own separate, isolated data stores (embedded, in-memory, or external) if they require specific rules or isolated reference data.

**Contracts & Registry**
- The AI MUST define a standard contract (e.g., a Java Interface) across a domain of plug-ins specifying standard behavior, input, and output objects.
- The AI MUST implement an Adapter when integrating third-party plug-ins that do not conform to the established standard contract.
- The AI MUST implement a Plug-in Registry within the core system to register, deregister, and locate plug-ins dynamically.

@Workflow
1. **Identify the Core**: Analyze the business requirements to determine the "happy path" or minimal functional flow. Abstract this into the Core System.
2. **Extract Volatility**: Identify all complex rules, jurisdiction-specific logic, client-specific customizations, and volatile features. Move these into discrete Plug-in Components.
3. **Define Contracts**: Create standardized interfaces (Contracts) defining the exact input data, output data, and execution methods required for the extracted plug-ins.
4. **Implement Registry**: Build a registry mechanism (e.g., a hash map of string identifiers to class names or external endpoints) within the core system to route requests to the correct plug-in based on context.
5. **Enforce Data Flow**: Refactor database access so the core system manages all central database queries and passes the results to the plug-ins. Provision local databases for plug-ins if they require isolated data.
6. **Apply Adapters**: Wrap any third-party or non-conforming plug-ins in Adapter classes to satisfy the standard Contract.

@Examples (Do's and Don'ts)

**[DO] Standard Contract and Registry Invocation**
```java
// DO define a standard contract
public interface AssessmentPlugin {
    AssessmentOutput assess(DeviceData data);
}

// DO use a registry to map the context to the plug-in
Map<String, String> pluginRegistry = new HashMap<>();
pluginRegistry.put("iPhone6s", "app.plugin.assessment.iphone6s.Iphone6sPlugin");

// DO instantiate and invoke via the registry
public void assessDevice(String deviceID, DeviceData data) {
    String pluginName = pluginRegistry.get(deviceID);
    Class<?> theClass = Class.forName(pluginName);
    AssessmentPlugin plugin = (AssessmentPlugin) theClass.getDeclaredConstructor().newInstance();
    
    // Core system passes data to the plug-in. Plug-in does NOT query the central DB.
    AssessmentOutput output = plugin.assess(data);
    displayReport(output);
}
```

**[DON'T] Cyclomatic Complexity in Core System**
```java
// DON'T embed highly volatile or custom logic directly into the core system
public void assessDevice(String deviceID) {
    if (deviceID.equals("iPhone6s")) {
        // 500 lines of specific logic
        assessiPhone6s();
    } else if (deviceID.equals("iPad1")) {
        // 500 lines of specific logic
        assessiPad1();
    } else if (deviceID.equals("Galaxy5")) {
        // 500 lines of specific logic
        assessGalaxy5();
    } 
    // This violates Microkernel principles (Entity Trap / Big Ball of Mud)
}
```

**[DO] Isolated Plug-in Namespace**
```java
// DO use semantic namespaces to isolate plug-ins
package app.plugin.assessment.iphone6s;

public class Iphone6sPlugin implements AssessmentPlugin {
    // Self-contained logic. Does not import app.plugin.assessment.ipad1.*
}
```

**[DON'T] Plug-in Direct Database Access**
```java
// DON'T let the plug-in query the central application database directly
package app.plugin.assessment.iphone6s;

public class Iphone6sPlugin implements AssessmentPlugin {
    public AssessmentOutput assess() {
        // ANTI-PATTERN: Direct connection to central shared database
        ResultSet rs = CentralDatabase.query("SELECT * FROM Customers");
        // ...
    }
}
```