@Domain
This rule file is triggered whenever the AI is tasked with designing, implementing, refactoring, or evaluating Continuous Integration (CI), Continuous Delivery (CD), repository structures, branching models, build pipelines, or artifact generation processes within a microservice architecture.

@Vocabulary
- **Continuous Integration (CI)**: The practice of frequently (at least daily) integrating code changes into a shared mainline, validated by an automated suite of tests.
- **Continuous Delivery (CD)**: A delivery approach where every check-in is treated as a release candidate, with its production-readiness continually assessed through an explicit build pipeline.
- **Continuous Deployment**: An extension of Continuous Delivery where any build that passes all automated verification steps is automatically deployed to production without human intervention.
- **Build Pipeline**: A modeled path to production consisting of multiple discrete stages (e.g., fast tests, slow tests, UAT, production) that a deployment artifact must pass through.
- **Artifact**: A single, immutable, deployable binary or package created once during the CI process and promoted through all pipeline environments.
- **Trunk-Based Development**: A branching model where all developers check code directly into the same mainline (trunk), using feature toggles to hide incomplete work.
- **Feature Branching**: A branching model (often an anti-pattern if long-lived) where work is isolated on a separate branch and integrated only when complete.
- **Feature Toggle (Feature Flag)**: A mechanism to dynamically switch functionality on or off, enabling incomplete code to be merged to the mainline safely.
- **Lockstep Release**: A highly discouraged anti-pattern in microservices where multiple services must be built and deployed simultaneously.
- **Monorepo**: An organizational pattern where code for multiple microservices is stored in a single source code repository.
- **Multirepo (One Repository per Microservice)**: An organizational pattern where the code for each microservice is isolated in its own dedicated repository.
- **CODEOWNERS**: A configuration file used in Monorepo structures to define and enforce fine-grained ownership and review requirements for specific directories.

@Objectives
- Guarantee the independent deployability of every microservice.
- Ensure fast, automated feedback cycles for developers.
- Eliminate configuration-specific build anti-patterns by enforcing the "build once" rule for artifacts.
- Enforce the prioritization of broken builds over new feature development.
- Align repository architectures with organizational ownership boundaries to minimize cross-team coordination and delivery bottlenecks.

@Guidelines

**Continuous Integration (CI) Rules**
- When evaluating a CI setup, the AI MUST verify Jez Humble's three criteria: 1) Code is checked into the mainline daily, 2) A suite of automated tests validates changes, 3) Fixing a broken build is the absolute #1 priority for the team.
- When the user reports a broken build, the AI MUST refuse to write new feature code until the build failure is diagnosed and resolved.

**Branching and Version Control**
- The AI MUST default to recommending Trunk-Based Development over Feature Branching.
- When a user asks to implement a new feature, the AI MUST suggest encapsulating the incomplete work behind a Feature Toggle rather than creating a long-lived branch.
- If branches are strictly required by the user, the AI MUST strongly advise that branches be short-lived (less than a day) and merged rapidly to avoid complex, delayed integrations.

**Build Pipelines and Environments**
- When designing a build pipeline, the AI MUST separate verification into multiple stages to optimize for fast feedback (e.g., Stage 1: Fast/Unit tests; Stage 2: Slow/Integration tests).
- The AI MUST architect the pipeline so that earlier environments prioritize developer feedback speed, while later environments progressively prioritize production-like fidelity.

**Artifact Generation and Configuration**
- The AI MUST adhere to the "Build Once" principle. A microservice MUST NOT be recompiled or rebuilt for different environments (e.g., dev, QA, prod).
- The AI MUST ensure that build scripts generate a single, environment-agnostic artifact.
- The AI MUST enforce that all environment-specific configuration is injected at runtime (e.g., via environment variables or external configuration stores) and never baked into the artifact itself.

**Repository Structure and Mapping**
- The AI MUST default to the Multirepo (One Repository per Microservice) pattern, generating a dedicated 1:1 mapping between a repository, its CI build, and its microservice.
- When a user requests a cross-repository change, the AI MUST warn the user that frequent cross-service changes indicate poor microservice boundaries and tight coupling.
- The AI MUST reject architectures that utilize "One Giant Repo, One Giant Build" (where a single check-in triggers a monolithic build of all services leading to a lockstep release).
- If the user explicitly mandates a Monorepo approach, the AI MUST:
  1. Map subdirectories explicitly to independent CI build triggers (using tools like Bazel, Lerna, or folder-specific CI paths).
  2. Generate a `CODEOWNERS` file to enforce strong ownership boundaries per microservice directory.
  3. Warn the user that atomic commits across services do NOT justify atomic, lockstep deployments.

**Code Reuse**
- When the user wishes to share code between microservices, the AI MUST package the shared code as a versioned artifact (library) rather than sharing raw source files.
- The AI MUST warn the user that updating a shared library requires independent, asynchronous deployments of all consuming microservices, avoiding simultaneous lockstep releases.

@Workflow
When tasked with designing or modifying a microservice build or repository architecture, the AI MUST execute the following algorithm:
1. **Analyze Repository Strategy**: Determine if the architecture is Multirepo (preferred) or Monorepo. If Monorepo, immediately instantiate directory-specific build triggers and `CODEOWNERS` boundaries.
2. **Define the Branching Model**: Configure the version control workflow for Trunk-Based Development utilizing Feature Toggles.
3. **Design the CI Pipeline**:
   - Step A: Compile/Package the code.
   - Step B: Run fast, small-scoped tests.
   - Step C: Package the outcome into a single, immutable deployment artifact.
4. **Design the CD Pipeline**:
   - Step D: Deploy the immutable artifact to a test environment (injecting test config) and run slow/integration tests.
   - Step E: Promote the exact same artifact to staging/UAT.
   - Step F: Promote the exact same artifact to production (injecting prod config).
5. **Validate Independence**: Audit the proposed workflow to ensure no step requires another microservice to be compiled or deployed simultaneously.

@Examples (Do's and Don'ts)

**Artifact Generation**
- [DO]: Create a single `Dockerfile` that copies compiled code and relies on external runtime variables. 
  ```dockerfile
  FROM openjdk:11-jre-slim
  COPY target/myservice.jar /app.jar
  ENTRYPOINT ["java", "-jar", "/app.jar"]
  # Configuration is supplied via environment variables at runtime
  ```
- [DON'T]: Create multiple Dockerfiles or build scripts for different environments that bake in configuration.
  ```dockerfile
  # Anti-pattern: Baking in environment config
  FROM openjdk:11-jre-slim
  COPY target/myservice.jar /app.jar
  COPY config/prod-db-credentials.xml /config.xml 
  ```

**Repository triggers**
- [DO]: Isolate build triggers in a Monorepo to specific folders so only the modified service builds.
  ```yaml
  # GitHub Actions example
  on:
    push:
      paths:
        - 'services/inventory/**'
  ```
- [DON'T]: Trigger a global build script that tests and builds all microservices whenever a single file in the repository changes.

**Branching & Integration**
- [DO]: Merge an incomplete feature directly into the `main` branch but wrap it in a feature flag so it is functionally dormant in production.
- [DON'T]: Maintain a `feature/new-checkout-flow` branch for three weeks, leading to a massive, conflict-ridden merge resolution prior to deployment.

**Cross-Service Code Reuse**
- [DO]: Publish shared domain logic as a versioned package (e.g., `com.musiccorp:common-domain:1.2.0`) that individual microservices can independently upgrade to at their own pace.
- [DON'T]: Link microservice build paths directly to a shared sibling folder in the file system, forcing all services to inherit changes instantly and necessitating a lockstep release.