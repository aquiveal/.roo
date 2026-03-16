@Domain
These rules must be triggered whenever the AI is tasked with initializing a new project, generating file scaffolding, creating new features, restructuring or refactoring an existing project's directory layout, determining where to place test files, or organizing related code for both front-end and back-end environments. 

@Vocabulary
- **Screaming Architecture:** A structural design paradigm where the top-level directory layout instantly communicates the system's business purpose, use cases, and features, rather than its underlying frameworks or technical infrastructure.
- **Feature / Use Case:** A vertical slice of functionality that cuts through all architectural layers (presentation, UI logic, interaction, transport, and persistence). It acts as the primary entry point for development work.
- **Feature-Driven Folder Structure:** Organizing files cohesively into dedicated workspaces around specific application use cases or features to minimize cognitive load and prevent flipping between distant directories.
- **Page Component (Front-end):** A container component representing a specific route that encapsulates the features, child components, and state required specifically for that view.
- **Shared Content:** Generic infrastructure, UI components, configurations, or global state that do not belong to one specific feature and are utilized across the application.
- **Package by Infrastructure / Type:** A structural anti-pattern where files are grouped by their technical role (e.g., `controllers/`, `services/`, `components/`).
- **Package by Domain:** A structural approach that groups files by top-level domain but fails to create cohesive workspaces for individual use cases.
- **Cognitive Load / File Distance:** The mental effort and time wasted tracking down related files (e.g., DTOs, controllers, and tests) when they are separated by infrastructure-based packaging.

@Objectives
- Ensure the project structure maximizes discoverability so that any developer instantly understands what the system does simply by looking at the folder names.
- Eliminate the energy spent flipping back and forth between disparate files by creating self-contained, cohesive feature workspaces.
- Treat every feature as a vertical slice of the application that encapsulates all necessary execution logic, interfaces, and error handling.
- Simplify refactoring, module scaling, and testability by strictly co-locating production code with its corresponding tests.
- Resist and override framework defaults if they mandate packaging by technical infrastructure rather than by feature.

@Guidelines
- **Rule: Implement Screaming Architecture.** Folder names must communicate the application's capabilities (e.g., `createPost/`, `checkout/`, `billing/`), not the tech stack or framework.
- **Rule: The Binary Placement Law.** Every single file must belong exclusively to a specific feature/use case directory OR be placed in a generic `/shared` (or `/core`) directory. There is no middle ground.
- **Rule: Vertical Slice Grouping.** A feature directory must contain everything required to execute that use case. 
  - For back-end, this includes the Use Case, Controller, DTO, Errors, and the Test file.
  - For front-end, this includes the Page component, Page-specific hooks, Page-specific child components, and the Test file.
- **Rule: Front-End Pages dictate Features.** In client-side applications, treat "Pages" as the boundary for features. A page has a 1-to-many relationship with features. Group all components, state, and interaction logic specific to a route inside that route's directory.
- **Rule: Co-locate Tests.** Test files MUST live immediately next to the production code they test within the specific feature directory. You must never create a mirrored `tests/` directory at the root of the project.
- **Rule: Extract Shared Content Properly.** If an entity, component (e.g., generic `Button`), configuration, or database infrastructure is utilized by multiple independent features, it must be placed in a global `/shared` directory.
- **Rule: Fight the Framework.** Do not yield to frameworks that enforce packaging by type (MVC folder structures). If forced to use framework-specific configuration files, tuck them away into `/shared/infrastructure/<framework_name>/` to protect the feature-driven domain architecture.
- **Anti-Pattern: Package by Type.** Never group files by their technical classification. Do not create global `src/controllers/`, `src/hooks/`, `src/services/`, or `src/utils/` directories to hold domain-specific logic.
- **Anti-Pattern: Natural Evolution.** Do not let file structures "evolve" naturally over time without a plan, as this leads to merge conflicts, high cognitive load, and zero discoverability. 

@Workflow
1. **Analyze the Request:** Identify whether the task involves creating a new feature, a shared utility, or restructuring existing code.
2. **Determine the Domain & Use Case:** Categorize the requested feature into its parent domain (e.g., `users`, `forum`) and define its exact Use Case name (e.g., `createUser`, `upvotePost`).
3. **Establish the Workspace:** Create a dedicated directory explicitly named after the Use Case or Page (e.g., `src/modules/users/useCases/createUser/` or `src/pages/dashboard/`).
4. **Co-locate Feature Files:** Generate and place all related architectural files strictly inside this new directory. For a backend use case, generate the UseCase, Controller, DTO, and Custom Errors in this folder.
5. **Write Co-located Tests:** Generate the test specification file (e.g., `[featureName].spec.ts`) inside the exact same workspace directory.
6. **Isolate Shared Logic:** Scan the feature for generic elements (e.g., Database connections, GraphQL setups, UI Primitives). Extract these into `src/shared/`.
7. **Verify Screaming Architecture:** Review the resulting directory tree. Confirm that a developer looking at the top-level folders would instantly know the business purpose of the application.

@Examples (Do's and Don'ts)

**Principle: Back-End Project Organization (Feature-Driven vs. Package-by-Type)**
- [DO] Organize by Domain and strictly by Use Case:
  ```text
  src/
    modules/
      users/
        useCases/
          createUser/
            CreateUserUseCase.ts
            CreateUserController.ts
            CreateUserDTO.ts
            CreateUserErrors.ts
            createUser.spec.ts
          deleteUser/
            ...
    shared/
      infra/
  ```
- [DON'T] Organize by technical infrastructure:
  ```text
  src/
    controllers/
      UserController.ts
    services/
      UserService.ts
    errors/
      UserErrors.ts
    dtos/
      UserDTO.ts
  ```

**Principle: Front-End Project Organization (Page-Driven vs. Package-by-Type)**
- [DO] Organize around Pages and their specific features:
  ```text
  src/
    pages/
      checkout/
        checkout.page.ts
        checkout.spec.ts
        useCheckout.ts
        components/
          billingInfo/
          confirmOrder/
    shared/
      components/
        Button.ts
  ```
- [DON'T] Scatter page components across global tech folders:
  ```text
  src/
    components/
      Checkout.ts
      BillingInfo.ts
      Button.ts
    hooks/
      useCheckout.ts
    tests/
      checkout.spec.ts
  ```

**Principle: Test Co-location**
- [DO] Place tests directly next to the production code they validate to ensure cohesive refactoring:
  ```text
  src/modules/users/useCases/createUser/createUser.ts
  src/modules/users/useCases/createUser/createUser.spec.ts
  ```
- [DON'T] Maintain a mirrored test directory that increases cognitive load and path distance:
  ```text
  src/modules/users/useCases/createUser/createUser.ts
  tests/modules/users/useCases/createUser/createUser.spec.ts
  ```

**Principle: Shared vs. Feature Code Placement**
- [DO] Put global routing, API clients, and generic UI components in `shared`:
  ```text
  src/shared/infra/graphql/client.ts
  src/shared/components/TextInput.tsx
  ```
- [DON'T] Trap generic, reusable infrastructure code inside a specific feature's workspace:
  ```text
  src/pages/login/graphql/client.ts
  src/pages/login/components/TextInput.tsx
  ```