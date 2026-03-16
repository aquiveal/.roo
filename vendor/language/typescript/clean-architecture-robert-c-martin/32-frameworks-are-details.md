# @Domain
This rule file MUST be activated whenever the AI is tasked with:
- Evaluating, selecting, or integrating a new framework or third-party library.
- Scaffolding a new application architecture or structuring project directories.
- Writing, modifying, or refactoring core business rules, Entities, or Use Cases.
- Configuring Dependency Injection (DI) containers or wiring application components.
- Resolving architectural coupling, circular dependencies, or boundary violations involving external frameworks.

# @Vocabulary
- **Framework**: A third-party library, tool, or utility designed to solve specific problems. It is a low-level implementation detail, NEVER an architecture.
- **Asymmetric Marriage**: An architectural anti-pattern where an application becomes inextricably tightly coupled to a framework, taking on all the risks and burdens, while the framework author assumes no reciprocal commitment to the application.
- **Inner Circles**: The core areas of the architecture containing Business Objects, Entities, and Use Cases.
- **Outer Circles**: The peripheral areas of the architecture containing mechanisms, IO, databases, Web, and Frameworks.
- **Main Component**: The "dirtiest," lowest-level component in the architecture responsible for bootstrapping the system, configuring frameworks, and wiring dependencies.
- **Proxy/Adapter**: A class derived from or wrapping framework base classes, placed in an outer circle to prevent the framework from infecting inner circles.

# @Objectives
- Treat all frameworks strictly as optional, interchangeable tools (details) rather than the foundational architecture of the system.
- Protect inner architectural circles (Entities, Business Rules, Use Cases) from any knowledge of or coupling to outer-circle frameworks.
- Minimize the risk of framework obsolescence, unhelpful evolutionary paths, and vendor lock-in by keeping frameworks at arm's length.
- Preserve the ability to test core business logic completely independent of any framework, database, or web server.
- Ensure that the decision to deeply integrate any framework is heavily scrutinized and restricted strictly to unavoidable standard language libraries.

# @Guidelines

## Framework Integration Constraints
- The AI MUST NOT treat a framework as the architecture of the application. The architecture MUST be centered around the system's Use Cases, not the framework's idioms.
- The AI MUST NOT allow framework imports, annotations, or base classes to cross into the Inner Circles.
- The AI MUST treat the framework as a peripheral detail residing exclusively in the Frameworks and Drivers layer (the outermost circle).

## Preventing Asymmetric Marriages
- The AI MUST explicitly reject any framework documentation or tutorial advice that encourages deriving core Business Objects or Entities from the framework's base classes.
- When a framework requires inheritance from its base classes to function, the AI MUST derive **Proxies** or **Adapters** from those base classes. These Proxies MUST be stored in external plugin components, keeping the core Business Objects entirely clean.

## Dependency Injection (DI) and Wiring
- The AI MUST NOT sprinkle framework-specific annotations (e.g., Spring's `@Autowired`, `@Inject`, `@Component`) throughout core business logic, Entities, or Use Case objects.
- The AI MUST restrict all framework-driven Dependency Injection auto-wiring to the **Main Component**. 
- The Main Component is the ONLY place permitted to know about the DI framework. Main MUST instantiate the clean dependencies and pass them inward to the agnostic business rules.

## Exceptions for Standard Libraries
- The AI MAY permit deep coupling to foundational, standard language libraries (e.g., C++ STL, Java Standard Library, C# Base Class Library) as these represent unavoidable, permanent architectural commitments ("marriages"). 
- Before coupling to any non-standard library, the AI MUST evaluate if it can be kept behind an architectural boundary.

# @Workflow
When instructed to implement a feature that requires a framework or third-party library, the AI MUST follow this algorithmic process:

1. **Assess the Framework Requirement**: Identify exactly what mechanism the framework provides (e.g., persistence, web delivery, dependency injection).
2. **Define the Core Interface**: Within the inner circle (Business Rules/Use Cases), define a pure, framework-agnostic interface that dictates what the core application needs.
3. **Isolate the Framework Implementation**: In the outermost architectural circle, create a Proxy, Adapter, or Implementation class that inherits from or utilizes the framework.
4. **Implement the Mapping**: Write the logic within the outer-circle Proxy to translate between the framework's native data formats and the pure data structures required by the inner circle.
5. **Wire in Main**: Open the `Main` component (or its equivalent application bootstrapper). Use the framework (e.g., DI container) strictly within this component to inject the outer-circle Proxy into the inner-circle Interface.
6. **Verify Boundary Integrity**: Scan the imports of the inner-circle files to ensure ZERO references to the framework's namespace exist.

# @Examples (Do's and Don'Ts)

## Handling Dependency Injection
**[DON'T]** Sprinkle framework annotations inside core business logic.
```java
package com.myapp.core.usecases;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.myapp.core.entities.User;

@Service // ANTI-PATTERN: Framework annotation in core use case
public class UserRegistrationUseCase {
    
    @Autowired // ANTI-PATTERN: DI framework coupled directly to business logic
    private UserRepository userRepository;

    public void registerUser(User user) {
        userRepository.save(user);
    }
}
```

**[DO]** Keep the Use Case pure and handle injection in the Main component/configuration.
```java
// File: com/myapp/core/usecases/UserRegistrationUseCase.java
package com.myapp.core.usecases;

import com.myapp.core.entities.User;

// PURE: No framework imports or annotations
public class UserRegistrationUseCase {
    private final UserRepository userRepository;

    // Standard constructor injection
    public UserRegistrationUseCase(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public void registerUser(User user) {
        userRepository.save(user);
    }
}

// File: com/myapp/main/ApplicationConfig.java
package com.myapp.main;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import com.myapp.core.usecases.UserRegistrationUseCase;
import com.myapp.infrastructure.db.PostgresUserRepository;

@Configuration // PERMITTED: Framework annotations restricted to the Main/Config component
public class ApplicationConfig {
    
    @Bean
    public UserRegistrationUseCase userRegistrationUseCase(PostgresUserRepository repo) {
        return new UserRegistrationUseCase(repo); // DI framework wires dependencies here
    }
}
```

## Handling Framework Base Classes
**[DON'T]** Derive core business entities from framework base classes.
```java
import javax.persistence.Entity;
import javax.persistence.Table;
import org.hibernate.annotations.GenericGenerator;
import com.framework.ActiveRecordBase;

@Entity
@Table(name = "users")
// ANTI-PATTERN: Marrying the framework by inheriting from its base class
public class User extends ActiveRecordBase { 
    private String id;
    private String email;
    // ...
}
```

**[DO]** Create a pure Entity, and use a Proxy/Adapter in the outer layer.
```java
// Inner Circle: Pure Business Object
public class User {
    private String id;
    private String email;
    // Business methods...
}

// Outer Circle: Framework Proxy/Adapter
import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name = "users")
public class UserDbModel {
    private String id;
    private String email;
    
    // Translation logic to convert to/from the pure User entity
    public User toDomainEntity() {
        return new User(this.id, this.email);
    }
    
    public static UserDbModel fromDomainEntity(User user) {
        // map fields...
    }
}
```