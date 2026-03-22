@Domain
These rules MUST be triggered when the AI is designing, modifying, or refactoring business logic that does not naturally fit within a single Entity or Value Object, when implementing calculations that span multiple Aggregates, when transforming domain objects, or when establishing domain-specific authentication or system integration interfaces.

@Vocabulary
- **Domain Service**: A stateless operation that fulfills a domain-specific task, used when a significant process, transformation, or calculation is not the natural responsibility of an Entity or Value Object.
- **Application Service**: A client of the Domain Model that coordinates use case tasks, manages transactions, and handles security, but contains absolutely NO business domain logic.
- **Anemic Domain Model**: An anti-pattern where Entities and Value Objects hold only data (getters/setters), while all domain logic is improperly pushed into Services.
- **Separated Interface**: A pattern where an interface is defined in one logical boundary (e.g., Domain Layer) and its implementation resides in another (e.g., Infrastructure Layer).
- **Stateless**: The condition of an object (the Service) where it holds no conversational or operational state between method invocations.
- **Transformation Service**: A specific type of Domain Service responsible for translating objects from one composition to another, often acting as an Anticorruption Layer when integrating with foreign Bounded Contexts.

@Objectives
- Execute significant business processes, transformations, or multi-Aggregate calculations without forcing unnatural responsibilities onto Entities or Value Objects.
- Prevent the creation of an Anemic Domain Model by strictly limiting the creation of Domain Services to cases where behavior genuinely spans multiple domain objects or requires technical infrastructural implementations.
- Maintain absolute statelessness within Domain Services.
- Strictly separate Domain Services (business logic) from Application Services (transaction and security coordination).
- Avoid arbitrary, mechanical abstractions such as the `Impl` naming convention, utilizing Separated Interfaces only when technically justified.

@Guidelines

**1. Rules of Identification and Creation**
- The AI MUST NOT create a Domain Service as a "silver bullet" for all business logic. Defaulting to Services for behavior leads to the Anemic Domain Model anti-pattern.
- The AI MUST NOT use static methods on an Aggregate Root to perform multi-aggregate calculations or operations. If the operation does not belong to a specific instance of an Entity or Value Object, the AI MUST create a Domain Service.
- The AI MUST create a Domain Service ONLY for one of three reasons:
  1. To perform a significant business process.
  2. To transform a domain object from one composition to another.
  3. To calculate a Value requiring input from more than one domain object.

**2. Domain Service vs. Application Service**
- The AI MUST NOT place transaction management, database connection lifecycle, or UI/remote endpoint security authorization inside a Domain Service.
- The AI MUST ensure Domain Services contain strictly business/domain logic.
- The AI MUST design Application Services to act as the direct clients of Domain Services. Application Services handle the setup (fetching from Repositories, opening transactions) and then delegate the domain logic to the Domain Service.

**3. State and Dependencies**
- The AI MUST design all Domain Services to be completely stateless. They must not retain any state between method invocations.
- The AI MAY inject and use Repositories within a Domain Service to look up necessary Aggregates to perform its calculations or processes (unlike Aggregates, which should generally not depend on Repositories).

**4. Interface and Implementation Naming (Separated Interfaces)**
- The AI MUST NOT use the `Impl` suffix for implementation classes (e.g., `AuthenticationServiceImpl`). This is strictly forbidden.
- The AI MUST name implementation classes based on their specific defining technical characteristic (e.g., `DefaultEncryptionAuthenticationService` or `MessageDigestEncryptionService`).
- If a Domain Service has only a single, purely domain-specific implementation (no technical/infrastructural dependencies), the AI MUST NOT create a Separated Interface. It MUST implement the Service as a single concrete class named according to the Ubiquitous Language.
- If a Domain Service requires a technical implementation (e.g., encryption, external network integration), the AI MUST define the interface in the Domain Layer and place the implementation class in the Infrastructure Layer (Dependency Inversion Principle).

**5. Return Types and Data Encapsulation**
- The AI SHOULD design Domain Services to return simple, secure Value Objects (e.g., `UserDescriptor`) rather than fully hydrated Entities, especially when the client (Application Service) only requires a lightweight reference or confirmation of the process.

**6. Testing**
- The AI MUST write tests for Domain Services that reflect how the client (Application Service) will use them.
- The AI MUST test both the "happy path" (successful business operations) and domain-specific failure scenarios (e.g., returning `null` or throwing domain-specific exceptions for invalid credentials or logic violations).
- The AI MAY use mocked or fast in-memory Repository implementations to test Domain Services.

@Workflow
1. **Analyze the Behavior**: Upon encountering unassigned business logic, the AI MUST first attempt to assign it to an existing Entity or Value Object.
2. **Justify the Service**: If assigning it to an Entity/VO creates an unnatural dependency, requires static methods, or spans multiple Aggregates, the AI MUST provision a Domain Service.
3. **Determine Interface Necessity**: The AI MUST check if the implementation requires technical infrastructure (e.g., database, external API, encryption).
   - If YES: Create an Interface in the Domain model and the implementation in the Infrastructure module.
   - If NO: Create a single concrete class in the Domain model.
4. **Draft the Signature**: The AI MUST name the class and its methods strictly using the Ubiquitous Language.
5. **Implement Stateless Logic**: The AI MUST implement the method logic using passed parameters and/or injected Repositories, ensuring no instance state is mutated or retained.
6. **Integrate with Application Service**: The AI MUST invoke the new Domain Service from an Application Service, keeping transaction boundaries in the Application Service.
7. **Write Client-Perspective Tests**: The AI MUST write unit tests validating the business rules executed by the Service.

@Examples (Do's and Don'ts)

**[DON'T]** Use a static method on an Aggregate to calculate data spanning multiple Aggregates.
```java
public class Product extends ConcurrencySafeEntity {
    // ANTI-PATTERN: Static method on an Entity for multi-aggregate calculations
    public static BusinessPriorityTotals businessPriorityTotals(Set<BacklogItem> aBacklogItems) {
        // ... calculation logic
    }
}
```

**[DO]** Create a dedicated, stateless Domain Service for multi-Aggregate calculations without a Separated Interface if there is no technical infrastructure required.
```java
package com.saasovation.agilepm.domain.model.product;

public class BusinessPriorityCalculator {
    public BusinessPriorityCalculator() { super(); }

    public BusinessPriorityTotals businessPriorityTotals(Tenant aTenant, ProductId aProductId) {
        int totalBenefit = 0;
        int totalPenalty = 0;
        // ...
        Collection<BacklogItem> outstanding = DomainRegistry.backlogItemRepository()
            .allOutstandingProductBacklogItems(aTenant, aProductId);
        
        for (BacklogItem item : outstanding) {
            // ... accumulate totals
        }
        return new BusinessPriorityTotals(totalBenefit, totalPenalty, ...);
    }
}
```

**[DON'T]** Name an implementation class using the `Impl` suffix or leak domain logic into the Application Service.
```java
// ANTI-PATTERN: Leaking domain logic into App Service and using Impl suffix
public class AuthenticationServiceImpl implements AuthenticationService {
    @Transactional // ANTI-PATTERN: Transactions belong in Application Services, not Domain Services
    public User authenticate(String tenantId, String username, String password) {
        // ...
    }
}
```

**[DO]** Use a Separated Interface for technical implementations, naming the implementation based on its technical mechanism, and placing it in the Infrastructure layer.
```java
// Domain Layer
package com.saasovation.identityaccess.domain.model.identity;

public interface AuthenticationService {
    public UserDescriptor authenticate(TenantId aTenantId, String aUsername, String aPassword);
}

// Infrastructure Layer
package com.saasovation.identityaccess.infrastructure.services;

public class DefaultEncryptionAuthenticationService implements AuthenticationService {
    public DefaultEncryptionAuthenticationService() { super(); }

    @Override
    public UserDescriptor authenticate(TenantId aTenantId, String aUsername, String aPassword) {
        // Domain logic relying on technical infrastructure (EncryptionService)
        Tenant tenant = DomainRegistry.tenantRepository().tenantOfId(aTenantId);
        if (tenant != null && tenant.isActive()) {
            String encryptedPassword = DomainRegistry.encryptionService().encryptedValue(aPassword);
            User user = DomainRegistry.userRepository().userFromAuthenticCredentials(aTenantId, aUsername, encryptedPassword);
            if (user != null && user.isEnabled()) {
                return user.userDescriptor();
            }
        }
        return null;
    }
}
```

**[DON'T]** Force authentication or encryption logic into an Entity where it breaks the Single Responsibility Principle.
```java
// ANTI-PATTERN: Forcing technical domain processes onto Entities
public class Tenant extends Entity {
    public boolean authenticate(User user, String clearTextPassword) {
        // Tenant now has to know about encryption and password validation
    }
}
```

**[DO]** Allow the Application Service to coordinate the task by calling the Domain Service, keeping the Application Service devoid of business logic.
```java
// Application Layer
public class AccessService {
    @Transactional(readOnly=true)
    public UserDescriptor authenticate(String aTenantId, String aUsername, String aPassword) {
        // Clean delegation: Application service coordinates, Domain Service executes business rules
        return DomainRegistry.authenticationService()
            .authenticate(new TenantId(aTenantId), aUsername, aPassword);
    }
}
```