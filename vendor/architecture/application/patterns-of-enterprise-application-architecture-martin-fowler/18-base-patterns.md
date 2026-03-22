# @Domain
These rules MUST be triggered whenever the AI is tasked with designing or implementing base architectural abstractions, integrating with external systems or APIs, handling monetary or primitive value calculations, decoupling architectural layers, managing global/shared state, or creating test fixtures for external dependencies.

# @Vocabulary
- **Gateway**: An object that encapsulates access to an external system or resource, translating its specialized API into a simple interface for the application.
- **Mapper**: An insulating layer that sets up communication between two independent subsystems without either being aware of the other.
- **Layer Supertype**: A base class (supertype) containing common behavior and fields for all objects within a specific architectural layer.
- **Separated Interface**: An interface defined in one package (often the client's package) but implemented in another, used to break dependencies.
- **Registry**: A well-known global object accessed via static methods that other objects use to find common services or data. 
- **Value Object**: A small, simple, immutable object (e.g., Money, DateRange) whose equality is based on its field values rather than identity.
- **Aliasing Bug**: A bug caused when two objects share a mutable Value Object and one owner changes it, unintentionally affecting the other.
- **Money**: A specific Value Object representing monetary value, consisting of a numeric amount and a currency.
- **Special Case**: A subclass that provides harmless or default behavior for particular edge cases (such as missing data), used to eliminate repetitive null checks.
- **Plugin**: A factory pattern variant that links classes during configuration (e.g., via a properties file and reflection) rather than compilation.
- **Service Stub**: A simple, fast, in-memory implementation of a Gateway used specifically to remove dependence on problematic external services during testing.
- **Record Set**: An in-memory, disconnected representation of tabular data (e.g., ADO.NET DataSet, JDBC RowSet).
- **Implicit Interface**: Accessing Record Set fields generically via string keys (e.g., `record["passenger"]`).
- **Explicit Interface**: Accessing Record Set fields via typed object properties (e.g., `record.passenger`).

# @Objectives
- Isolate the application from external dependencies and complex APIs.
- Eliminate dependency cycles and tight coupling between architectural layers.
- Prevent rounding errors and currency mismatches in financial calculations.
- Eradicate runtime null reference errors and repetitive conditional checks.
- Ensure global state is strictly scoped, safely accessed, and easily stubbed for testing.
- Guarantee that tests run quickly and reliably without requiring live external services.

# @Guidelines

## External Resource Integration (Gateway & Mapper)
- The AI MUST use a **Gateway** whenever the application interacts with an external resource, proprietary messaging service, or foreign API.
- The AI MUST design the Gateway interface to match the vocabulary and needs of the *client* application, not the external API.
- The AI MUST NOT place complex domain logic, workflow, or business rules inside a Gateway. Gateways are dumb translators.
- The AI MUST translate specialized error codes from the external API into standard exceptions native to the application's language within the Gateway.
- The AI MUST only use a **Mapper** (instead of a Gateway) if *both* interacting subsystems must remain entirely ignorant of each other and the interaction mechanism.

## Layer Structuring & Decoupling (Layer Supertype & Separated Interface)
- The AI MUST extract repetitive boilerplate (e.g., ID fields, standard database load/save logic) into a **Layer Supertype**.
- The AI MUST use a **Separated Interface** to invert dependencies if lower-level code (e.g., framework or data layer) needs to call higher-level code (e.g., domain layer), or if a domain layer needs to call a data mapper.
- The AI MUST define the Separated Interface in the package of the *client* (the caller) and place the implementation in a separate package.

## Global State Management (Registry & Plugin)
- The AI MUST treat global data as "guilty until proven innocent" and attempt to pass dependencies via parameters or constructors before falling back to a **Registry**.
- If a Registry is required, the AI MUST expose it via static methods, but the AI MUST NOT use static mutable fields to store the data.
- The AI MUST scope the Registry data appropriately: use Singletons for process-scoped *immutable* data, and Thread-Specific Storage (e.g., `ThreadLocal`) for thread-scoped or session-scoped data.
- The AI MUST allow the Registry to be re-initialized or substituted with a Service Stub for testing.
- The AI MUST use a **Plugin** (configuration files + reflection/dynamic loading) to bind implementations to Separated Interfaces at runtime, preventing compile-time dependencies on specific environments (e.g., swapping a test ID generator for a production database generator).

## Domain Primitives (Value Object & Money)
- The AI MUST implement small, identity-less objects as **Value Objects**.
- The AI MUST make all Value Objects completely immutable to prevent Aliasing Bugs. Any change to a value must result in a new object instance.
- The AI MUST override the equality (`equals`) and hash code operations for all Value Objects to compare field values, not memory identity.
- The AI MUST NEVER use floating-point types (`float`, `double`) for **Money** amounts. The AI MUST use integral types (e.g., `long` representing cents) or fixed-point decimals (e.g., `BigDecimal`).
- The AI MUST assert that currencies match before performing any addition or subtraction on Money objects.
- The AI MUST implement an `allocate(ratios)` method on Money objects to divide funds without losing or creating pennies due to rounding. The algorithm must distribute any remainder pennies across the resulting allocations.

## Edge Case Handling (Special Case)
- The AI MUST create **Special Case** classes (e.g., `NullEmployee`, `UnknownCustomer`) instead of returning `null` when a specific condition results in standard, repetitive fallback behavior.
- The AI MUST ensure the Special Case class implements the exact same interface as the expected domain class, providing harmless default returns (e.g., returning 0 for totals, or returning other Special Case objects for nested calls).

## Testing (Service Stub)
- The AI MUST build a **Service Stub** for any Gateway that connects to an external third-party service.
- The AI MUST keep the Service Stub extremely simple (e.g., returning flat rates or hardcoded configurations) rather than replicating the complex logic of the real service.

## Tabular Data (Record Set)
- If the architecture relies heavily on UI tools bound to data sets, the AI MUST use a **Record Set** (with a Table Module pattern).
- The AI MUST prefer Explicit Interfaces (strongly typed data sets) over Implicit Interfaces (dictionary/map lookups) for Record Sets to preserve compile-time type safety.

# @Workflow
When tasked with designing a system component or refactoring an existing module, the AI MUST follow this algorithmic process:

1.  **Analyze Dependencies**: Scan the requirements for external APIs, databases, or third-party services.
    *   *Action*: Define a **Gateway** interface for each.
    *   *Action*: Implement a concrete Gateway for the real service.
    *   *Action*: Implement a **Service Stub** for testing.
2.  **Define Domain Primitives**: Identify small data clumps (currencies, date ranges, measurements).
    *   *Action*: Generate immutable **Value Objects** for these.
    *   *Action*: If dealing with currency, generate a **Money** class with an `allocate` algorithm and integer-based storage.
3.  **Structure Layers**: Group identified domain and data objects by layer.
    *   *Action*: Extract common fields/methods into a **Layer Supertype** for each layer.
4.  **Decouple Packages**: Analyze package dependencies.
    *   *If Package A calls Package B but A should not depend on B*: Create a **Separated Interface** in Package A. Implement it in Package B.
    *   *Action*: Wire them together dynamically using a **Plugin** configuration.
5.  **Eliminate Nulls**: Search for nullable domain object returns.
    *   *Action*: Generate **Special Case** subclasses for missing/unknown data to enforce polymorphism over conditional logic.
6.  **Manage Shared State**: Identify any data that must be globally accessible (e.g., DB connections, Finders).
    *   *Action*: Implement a **Registry** with static accessors.
    *   *Action*: Back the Registry with `ThreadLocal` storage (if mutable) or a mockable Singleton (if immutable).

# @Examples (Do's and Don'ts)

## Money & Allocation
- **[DO]** Use integers/decimals and an allocation algorithm for distributing Money:
```java
class Money {
    private long amount; // stored in cents
    private Currency currency;

    public Money[] allocate(long[] ratios) {
        long total = 0;
        for (int i = 0; i < ratios.length; i++) total += ratios[i];
        long remainder = amount;
        Money[] results = new Money[ratios.length];
        for (int i = 0; i < results.length; i++) {
            results[i] = newMoney(amount * ratios[i] / total);
            remainder -= results[i].amount;
        }
        for (int i = 0; i < remainder; i++) {
            results[i].amount++; // distribute remainder pennies
        }
        return results;
    }
}
```
- **[DON'T]** Use floating point math or standard division, which loses pennies:
```java
// ANTI-PATTERN
double amount = 0.05;
double part1 = amount * 0.7; // 0.035
double part2 = amount * 0.3; // 0.015
// Fails when rounding leads to 0.04 and 0.02 (Total 0.06)
```

## Special Case
- **[DO]** Return a Special Case object that fulfills the contract harmlessly:
```csharp
class NullEmployee : Employee {
    public override String Name {
        get { return "Unknown Employee"; }
        set { /* Do nothing */ }
    }
    public override Decimal GrossToDate {
        get { return 0m; }
    }
    public override Contract Contract {
        get { return Contract.NULL; } // Return another Special Case
    }
}
```
- **[DON'T]** Return null and force the client to handle it:
```csharp
// ANTI-PATTERN
Employee emp = finder.GetEmployee(id);
if (emp != null && emp.Contract != null) {
    // do something
}
```

## Gateway & Service Stub
- **[DO]** Define an explicit interface representing the application's perspective, and provide a test stub:
```java
interface TaxGateway {
    TaxInfo getSalesTax(String productCode, Address addr, Money amount);
}

class FlatRateTaxStub implements TaxGateway {
    public TaxInfo getSalesTax(String productCode, Address addr, Money amount) {
        return new TaxInfo(0.05, amount.multiply(0.05)); // Simple test logic
    }
}
```
- **[DON'T]** Leak external, weakly-typed messaging APIs into the domain:
```java
// ANTI-PATTERN
// Domain object calling external API directly with weakly typed arguments
externalMessageSystem.send("TAX_REQ", new Object[] { "123", "NY", 500 });
```

## Registry
- **[DO]** Use static methods backed by thread-safe or stubbable storage:
```java
class Registry {
    private static ThreadLocal instances = new ThreadLocal();

    public static PersonFinder personFinder() {
        return ((Registry)instances.get()).personFinder;
    }
}
```
- **[DON'T]** Expose global static mutable fields:
```java
// ANTI-PATTERN
class Registry {
    public static PersonFinder personFinder = new PersonFinder(); // Not thread safe, hard to mock
}
```

## Separated Interface
- **[DO]** Place the interface in the client's package and the implementation in the infrastructure package, dynamically loaded via a Plugin factory.
- **[DON'T]** Make the domain layer import and instantiate infrastructure classes directly (e.g., `new OracleIdGenerator()`).