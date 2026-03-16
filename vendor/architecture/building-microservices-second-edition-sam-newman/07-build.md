# @Domain
These rules MUST be triggered whenever the AI is tasked with generating, modifying, or reviewing CI/CD pipelines, source control configurations, branching strategies, repository structures, artifact generation scripts (e.g., Dockerfiles, build.sh), or release automation workflows in a microservices environment.

# @Vocabulary
- **Continuous Integration (CI)**: The practice of frequently (at least daily) integrating code changes into a mainline branch, validated by an automated suite of tests.
- **Continuous Delivery (CD)**: An approach where every check-in is treated as a release candidate, explicitly modeled through a pipeline to assess production readiness.
- **Continuous Deployment**: An extension of CD where any build that passes all automated steps is deployed to production without manual intervention.
- **Trunk-Based Development**: A branching model where all developers check code into a single mainline (trunk) frequently, using feature toggles to hide incomplete work, rather than relying on long-lived feature branches.
- **Build Pipeline**: A multi-stage process (e.g., fast tests, slow tests, packaging) designed to balance fast developer feedback with rigorous production-like verification.
- **Artifact**: A compiled binary, container image, or package built once during the CI process and promoted through the pipeline.
- **Multirepo (One Repository per Microservice)**: An organizational pattern where each microservice resides in its own isolated source control repository with its own independent build pipeline.
- **Monorepo**: A pattern where code for multiple microservices is stored in a single repository.
- **Per-Team Monorepo**: A compromise pattern where a single repository contains only the microservices owned by one specific team.
- **CODEOWNERS**: A configuration file used in monorepos to map specific directories or file paths to strong ownership groups.
- **Lockstep Release**: The anti-pattern of deploying multiple microservices simultaneously due to tightly coupled code or monolithic build processes.
- **Test Snow Cone (Inverted Pyramid)**: An anti-pattern describing a test suite with very few fast, small-scoped tests and a massive amount of slow, large-scoped tests.

# @Objectives
- Ensure the absolute independent deployability of every microservice by decoupling build pipelines and repositories.
- Enforce the "Build Once, Deploy Anywhere" principle for all deployable artifacts.
- Optimize CI/CD pipelines to provide the fastest possible feedback to developers.
- Prevent cross-service deployment coupling and lockstep releases.
- Establish strict boundaries and clear ownership within source control repositories.

# @Guidelines

## Branching and Integration
- The AI MUST advocate for and configure workflows supporting **Trunk-Based Development**.
- The AI MUST NOT configure long-lived feature branches. If branching is required, the AI MUST constrain configurations to assume branches live for less than one day.
- The AI MUST enforce that a broken build is the highest priority. If tasked with writing code while a build is failing, the AI MUST prompt the user to fix the build first.

## Artifact Creation and Management
- The AI MUST strictly enforce that an artifact (e.g., Docker image, JAR file) is built **once and only once** early in the pipeline.
- The AI MUST NOT embed environment-specific configurations (e.g., database URLs, credentials) inside the artifact. The AI MUST configure the artifact to accept environment variables at runtime.
- The AI MUST configure deployment scripts to pull the exact same versioned artifact (by hash or immutable tag) across all environments (e.g., CI, UAT, Production).

## Build Pipeline Structure
- The AI MUST segment verification steps in the pipeline to prioritize fast feedback. Fast, small-scoped tests MUST run before slow, large-scoped tests or performance tests.
- The AI MUST configure pipelines such that a failure in an early stage completely halts the pipeline, preventing subsequent stages from running.

## Source Control and Repository Patterns
- **Default to Multirepo**: When scaffolding new microservices, the AI MUST isolate the service into its own repository (or distinct logical boundary) with a completely independent CI/CD pipeline.
- **Monorepo Constraints**: If forced to use a Monorepo, the AI MUST configure the CI/CD pipeline (e.g., using path filtering in GitHub Actions) so that a commit only triggers the build/test pipeline for the specific microservice(s) modified.
- **Avoid Giant Builds**: The AI MUST NEVER configure a single, monolithic build script that compiles and tests all microservices sequentially or as a single unit.
- **Ownership**: If configuring a monorepo, the AI MUST generate a `CODEOWNERS` file mapping specific microservice directories to their respective owning teams.

## Cross-Service Dependencies
- If a microservice requires code from another microservice/repository, the AI MUST configure this dependency via a versioned, packaged library artifact (e.g., npm package, Maven artifact).
- The AI MUST NOT use local relative path linking (e.g., `../shared-lib`) across microservice boundaries in a multirepo setup.

# @Workflow
When tasked with creating or modifying a CI/CD pipeline or repository structure for a microservice, the AI MUST follow this exact algorithm:

1. **Determine the Repository Strategy**:
   - Identify whether the project is using Multirepo, Monorepo, or Per-Team Monorepo.
   - If Monorepo, immediately define path-based triggers for the pipeline to ensure isolation.
2. **Define the Build/Artifact Stage**:
   - Write the script to compile the code and package the artifact.
   - Assign a unique, immutable identifier (e.g., Git commit SHA) to the artifact.
   - Push the artifact to a central registry.
3. **Structure the Verification Pipeline**:
   - *Stage 1*: Fast Unit Tests (Fail fast).
   - *Stage 2*: Service-level tests (Mocked dependencies).
   - *Stage 3*: Slower End-to-End or Performance tests (using the packaged artifact).
4. **Implement Environment Agnosticism**:
   - Review the deployment steps to ensure no environment variables are baked into the build stage.
   - Write deployment configurations (e.g., Kubernetes manifests, Docker Compose) that inject the environment variables at runtime.
5. **Configure Trunk-Based Workflows**:
   - Set the primary CI triggers to run on pushes to `main`/`master`.
   - Ensure PR/branch builds run the exact same verification steps as the main branch.

# @Examples (Do's and Don'ts)

## Artifact Creation
- **[DO]** Build a Docker image once, tag it with the Git commit hash, and push it to a registry. Use that specific tag for all deployments.
```yaml
build:
  steps:
    - run: docker build -t my-registry/my-service:${{ github.sha }} .
    - run: docker push my-registry/my-service:${{ github.sha }}
deploy_uat:
  steps:
    - run: helm upgrade my-service --set image.tag=${{ github.sha }}
```
- **[DON'T]** Rebuild the source code or Docker image in every environment stage.
```yaml
# ANTI-PATTERN: Rebuilding for every environment
deploy_uat:
  steps:
    - run: docker build -t my-service:uat --build-arg ENV=uat .
deploy_prod:
  steps:
    - run: docker build -t my-service:prod --build-arg ENV=prod .
```

## Monorepo Pipeline Triggers
- **[DO]** Use path filtering to ensure only the modified microservice is built and tested.
```yaml
on:
  push:
    paths:
      - 'services/inventory/**'
jobs:
  build-inventory:
    runs-on: ubuntu-latest
```
- **[DON'T]** Trigger a global build script that tests every service in the repository on every commit.
```yaml
# ANTI-PATTERN: One Giant Build
on: push
jobs:
  build-all:
    steps:
      - run: make test-all-services
```

## Environment Configuration
- **[DO]** Pass configuration into the container at runtime.
```dockerfile
# Dockerfile
ENTRYPOINT ["node", "server.js"]
# Runtime injection via deployment orchestrator
```
- **[DON'T]** Bake environment-specific configurations into the build artifact.
```dockerfile
# ANTI-PATTERN
COPY ./config/prod.json /app/config.json
RUN npm run build:prod
```

## Code Ownership in Monorepos
- **[DO]** Use a `CODEOWNERS` file to enforce strong ownership of specific microservice directories.
```text
/services/catalog/ @musiccorp/catalog-team
/services/payment/ @musiccorp/finance-team
```
- **[DON'T]** Allow collective ownership of all directories in a large monorepo without explicit review paths, which leads to tightly coupled architectures.