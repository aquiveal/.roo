# @Domain
These rules are activated when the AI is tasked with defining system architecture, organizing project directory structures, modularizing monolithic codebases, establishing build and deployment pipelines, configuring package managers (e.g., Maven, RubyGems, NuGet), or designing plugin systems and dynamic module loaders. 

# @Vocabulary
*   **Component**: The fundamental unit of deployment in a software system; the smallest entity that can be independently deployed (e.g., `.jar` files in Java, `.gem` files in Ruby, `.dll` files in .NET, aggregations of binary files in compiled languages, or aggregations of source files in interpreted languages).
*   **Independent Deployability**: The architectural property where a component can be deployed or updated in a system without requiring the recompilation or redeployment of the entire system.
*   **Independent Developability**: The architectural property where a component can be constructed, modified, and tested by a developer or team in isolation from the rest of the system.
*   **Relocatability**: The ability of a component to be loaded and executed at any arbitrary location within the system or memory, completely free of hard-coded execution paths, fixed memory addresses, or rigid environmental assumptions.
*   **Component Plugin Architecture**: A software design paradigm where independently deployable components are dynamically linked and loaded at runtime as plugins to an existing core application, rather than being statically linked into a single monolithic executable.
*   **Murphy’s Law of Program Size**: The principle that "Programs will grow to fill all available compile and link time," necessitating the separation of components to avoid monolithic build bottlenecks.
*   **Linker/Loader Separation**: The historical and architectural distinction between compiling code, linking it into a relocatable format, and dynamically loading it at runtime to drastically reduce turnaround times.

# @Objectives
*   Design every system such that its functional parts are segregated into smallest deployable entities (Components).
*   Guarantee that components retain the absolute ability to be independently developable and independently deployable.
*   Eliminate monolithic compile-link bottlenecks by shifting from static compilation to dynamic runtime linking.
*   Ensure all code is perfectly relocatable and never bound to hardware-specific or absolute environmental locations.
*   Establish Component Plugin Architecture as the casual default for all modular system extensions.

# @Guidelines
*   **When encountering monolithic source code structures**, the AI MUST identify logical boundaries and extract them into discrete components (aggregations of binaries or source files) appropriate to the target language (e.g., extracting to `.jar`, `.dll`, or `.gem`).
*   **When determining deployment strategies**, the AI MUST default to configuring components so they can be independently deployed as separate dynamically loaded plugins, rather than defaulting to a single statically linked executable.
*   **When encountering fixed execution environments, hard-coded absolute paths, or static memory allocations (modern analogs to early "origin statements")**, the AI MUST refactor the code to utilize dynamic resolution and relative referencing to guarantee strict Relocatability.
*   **When configuring build tools and package managers**, the AI MUST ensure that the output artifacts represent independent units of deployment that do not force unrelated components to recompile.
*   **When encountering long compile-link turnaround times (Murphy’s Law of Program Size)**, the AI MUST mitigate the bottleneck by transitioning statically linked libraries into dynamically linked shared libraries that are resolved by a loader at runtime.
*   **When designing extensibility or new feature additions**, the AI MUST implement a Component Plugin Architecture, ensuring that the new feature can be dropped into a specific directory or environment and dynamically linked at runtime without recompiling the host application.
*   **When aggregating components for a specific release**, the AI MAY link components into a single executable or aggregate them into a single archive (e.g., a `.war` file), but MUST NOT do so in a way that destroys their intrinsic ability to be independently deployed in future iterations.

# @Workflow
1.  **Identify Component Granularity**: Analyze the codebase to determine the smallest entities that can be logically deployed as standalone units based on the programming language (e.g., grouping related classes into a Java `.jar` target).
2.  **Enforce Relocatability**: Scan the identified component source code for any hard-coded paths, environmental assumptions, or static initialization constraints. Replace these with dynamic lookups, relative paths, and context-injected configurations.
3.  **Decouple Build Pipelines**: Modify the build configurations (e.g., `pom.xml`, `package.json`, `.csproj`) so that each component builds into its own distinct, versioned deployment artifact without statically linking unnecessary dependencies.
4.  **Implement Plugin Loading**: Abstract the core application's dependency resolution mechanism to dynamically discover and load these components at runtime (e.g., scanning a `/plugins` directory for `.dll` or `.jar` files).
5.  **Verify Independent Deployability**: Simulate a deployment by updating and building exactly one component, then hot-swapping it into the runtime environment to ensure the host application accepts the new component without a full system rebuild.

# @Examples (Do's and Don'ts)

### Component Plugin Architecture & Independent Deployability
**[DO]** Design the host application to dynamically load independent components at runtime based on the language's specific deployment units.
```csharp
// The host application dynamically loads a component (.dll) at runtime
public IEnumerable<IPlugin> LoadPlugins(string pluginDirectory)
{
    var plugins = new List<IPlugin>();
    foreach (var file in Directory.GetFiles(pluginDirectory, "*.dll"))
    {
        // Dynamically linking the component at load time
        var assembly = Assembly.LoadFrom(file);
        var pluginTypes = assembly.GetTypes().Where(t => typeof(IPlugin).IsAssignableFrom(t) && !t.IsInterface);
        
        foreach (var type in pluginTypes)
        {
            plugins.Add((IPlugin)Activator.CreateInstance(type));
        }
    }
    return plugins;
}
```

**[DON'T]** Statically link all modules into a single monolithic execution block that destroys independent deployability and developability.
```csharp
// Anti-pattern: Statically linking everything prevents independent deployment.
// Any change to PaymentProcessor or InventoryManager requires rebuilding the entire application.
public class MonolithicApp
{
    private PaymentProcessor _paymentProcessor = new PaymentProcessor();
    private InventoryManager _inventoryManager = new InventoryManager();

    public void Run()
    {
        _paymentProcessor.Process();
        _inventoryManager.Update();
    }
}
```

### Relocatability
**[DO]** Use dynamic, environment-agnostic path resolution so the component can be executed or loaded anywhere in the system.
```javascript
// Interpreted language component aggregation
const path = require('path');

// Dynamically resolving paths ensures the component is fully relocatable
const configPath = path.join(__dirname, 'config', 'settings.json');
const loadConfig = () => require(configPath);
```

**[DON'T]** Hard-code absolute paths or environment-specific locations (the modern equivalent of the historical absolute memory "origin statement").
```javascript
// Anti-pattern: Hard-coded absolute paths destroy relocatability.
// The component will fail if deployed to a different directory or operating system.
const loadConfig = () => require('/var/www/html/myapp/components/auth/config/settings.json');
```