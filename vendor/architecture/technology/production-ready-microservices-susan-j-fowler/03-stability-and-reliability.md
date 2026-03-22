# @Domain
These rules MUST be triggered whenever the AI is tasked with designing, implementing, configuring, or reviewing:
- Microservice architecture, architecture reviews, or system design.
- Continuous Integration / Continuous Deployment (CI/CD) pipelines or deployment workflows.
- Development cycle processes (version control, testing requirements, code reviews).
- Dependency management, defensive programming, or caching strategies between microservices.
- Service discovery, load balancing, health checks, or circuit breaker configurations.
- Microservice or API endpoint deprecation and decommissioning procedures.

# @Vocabulary
- **Stability**: The property of a microservice where development, deployment, new technologies, and deprecation do not cause instability across the ecosystem. Mitigation of negative side-effects of change.
- **Reliability**: The property of a microservice where it can be trusted by its clients, dependencies, and the ecosystem to meet its Service-Level Agreements (SLAs) without failure.
- **Candidate for Production**: A specific code build that has successfully passed all lint, unit, integration, and end-to-end tests and code review, and is ready for the deployment pipeline.
- **Deployment Pipeline**: The rigid, standardized sequence of stages a candidate for production must pass through before serving 100% of real-world traffic: Staging -> Canary -> Production.
- **Full Staging**: A staging environment that is a complete mirror copy of the production ecosystem, communicating only with other staging services, utilizing completely separate test databases.
- **Partial Staging**: A staging environment that communicates with actual production upstream clients and downstream dependencies, requiring read-only database access or Test Tenancy for writes, and necessitating automated rollbacks.
- **Host Parity**: The state where a testing or staging environment has the exact same number of hosts as the production environment.
- **Canary Environment**: A deployment pool containing 5%–10% of randomly selected production servers, hosting live production traffic, used to test a new release before a full production rollout.
- **Traffic Cycle**: A standard, cyclical pattern of traffic a microservice experiences; a canary must survive at least one full traffic cycle before proceeding to production.
- **Defensive Caching**: Implementing an in-memory cache (typically a Least Recently Used / LRU cache) to store data from downstream dependencies, ensuring the microservice remains available even if the dependency fails.
- **Circuit Breaker**: A mechanism within the routing and discovery layer that automatically stops routing traffic to a service or host if it experiences an abnormal amount of errors (e.g., unhandled exceptions) or fails health checks.
- **Deprecation**: The process of alerting clients that an API endpoint or microservice is no longer supported and directing them to a new endpoint.
- **Decommissioning**: The final process of turning off a microservice or endpoint after verifying no clients are still utilizing it.
- **Test Tenancy**: The practice of strictly marking/identifying test data written by a partial staging environment so it does not corrupt real-world production data.

# @Objectives
- **Eliminate Uncaught Bugs**: Catch all defects in the development phase via rigorous, automated testing (lint, unit, integration, end-to-end) *before* human code review.
- **De-Risk Deployments**: Prevent "bad deployments" (the leading cause of microservice outages) by enforcing a strict Staging -> Canary -> Production pipeline with automated rollbacks.
- **Isolate Failures (Fault Tolerance)**: Protect microservice SLAs from downstream dependency failures via defensive caching, fallbacks, and queueing.
- **Ensure Routing Integrity**: Implement accurate, deep health checks on isolated channels and enforce circuit breaking for unhealthy instances.
- **Safe Sunsetting**: Ensure no upstream clients are broken during the deprecation or decommissioning of services and endpoints.

# @Guidelines

### 1. The Development Cycle
- The AI MUST enforce the use of a central repository (git/svn) with individual branch creation for any code changes.
- The AI MUST require that the development environment accurately mirrors the production world (including dependencies and databases).
- The AI MUST mandate that all lint, unit, integration, and end-to-end tests are executed and pass *before* a code review is allowed to begin.
- The AI MUST configure continuous integration to automatically test, build, and package the release.

### 2. The Deployment Pipeline
- The AI MUST design deployment pipelines with exactly three stages: Staging, Canary, and Production.
- **Staging Requirements**:
  - The AI MUST configure staging to act as an exact reflection of the real world without receiving real user traffic.
  - If designing **Full Staging**: The AI MUST isolate network calls to only other staging services and mandate separate test databases.
  - If designing **Partial Staging**: The AI MUST enforce read-only access to production databases OR strictly implement Test Tenancy for writes. Automated rollbacks MUST be enabled for Partial Staging.
  - The AI MUST ensure staging environments possess dashboards, monitoring, and logging identical to production.
- **Canary Requirements**:
  - The AI MUST size the canary pool at 5% to 10% of total production hardware.
  - The AI MUST allocate the exact same frontend and backend ports for the canary as used in production (never separate ports).
  - The AI MUST ensure canary hosts are chosen entirely at random from the production pool.
  - The AI MUST configure automated rollbacks for the canary phase triggered by error thresholds.
  - The AI MUST require the canary to run for at least one full Traffic Cycle before advancing.
- **Production Requirements**:
  - The AI MUST NEVER allow direct deployments or hotfixes to production bypassing Staging and Canary.
  - In emergencies, the AI MUST recommend rolling back to the last stable build rather than pushing a hotfix forward.
  - The AI MUST block new deployments if the microservice is currently violating its SLA downtime quota.

### 3. Dependency Management
- The AI MUST identify and track all upstream clients and downstream dependencies.
- The AI MUST implement mitigation strategies for the failure of *every* downstream dependency.
- The AI MUST utilize Defensive Caching (specifically LRU caches) for downstream data to preserve the host service's SLA if the dependency goes offline.
- The AI MUST implement message queues or fallback endpoints if caching is not applicable.

### 4. Routing and Discovery
- The AI MUST design health checks that evaluate the actual internal health of the application, explicitly avoiding hardcoded `200 OK` responses.
- The AI MUST run health checks on a separate communication channel from standard RPC traffic to prevent network congestion from disrupting health status.
- The AI MUST configure Load Balancers / Service Discovery to immediately stop routing traffic to instances failing health checks.
- The AI MUST implement Circuit Breakers that trip and stop traffic routing if a service experiences an abnormal amount of unhandled exceptions, independent of standard health checks.

### 5. Deprecation and Decommissioning
- The AI MUST strictly forbid the "abandonment" of outdated microservices. Unused services MUST be formally decommissioned.
- The AI MUST mandate a communication phase to alert all client services before shutting down an endpoint or service.
- The AI MUST implement endpoint monitoring during the deprecation phase to explicitly verify zero incoming traffic before executing the final decommissioning.

# @Workflow
When tasked with designing a microservice pipeline, deployment, or architecture, the AI MUST follow this exact algorithm:

1. **Development Environment & Testing Setup**:
   - Define the central repository and branching strategy.
   - Define the local/dev environment so it perfectly mirrors production dependencies.
   - Configure the CI pipeline to run Lint -> Unit -> Integration -> End-to-End tests automatically.
   - Apply a strict gate: Code Review cannot commence until CI tests pass.

2. **Deployment Pipeline Configuration**:
   - **Step 2a (Staging)**: Determine if the service uses Full or Partial Staging. Configure DB access rules (Test DB vs. Test Tenancy/Read-only). Replicate production dashboards/logs here.
   - **Step 2b (Canary)**: Route 5-10% of traffic to a random subset of nodes using *identical* ports. Set the duration to one full traffic cycle. Configure automatic rollback thresholds.
   - **Step 2c (Production)**: Configure the final rollout strategy (all-at-once or staged percentage). Add a hard block to CI/CD preventing deployment if the SLA is currently violated.

3. **Dependency Resiliency Integration**:
   - Map all downstream dependencies.
   - For data-fetching dependencies, inject an LRU Cache into the data-retrieval code block.
   - For task-based dependencies, implement a retry queue or fallback alternative.

4. **Routing & Health Check Configuration**:
   - Write a semantic `/health` endpoint that queries internal DB connections and basic processing capabilities.
   - Expose the `/health` endpoint on an isolated administrative port/channel.
   - Configure the Circuit Breaker to trip on `x` unhandled exceptions over `y` time.

5. **Lifecycle Management**:
   - If a service/endpoint is being removed, output the deprecation runbook:
     - 1) Document new endpoint. 2) Broadcast to upstream owners. 3) Monitor old endpoint logs. 4) Delete code only when logs show 0 hits over a full traffic cycle.

# @Examples (Do's and Don'ts)

### 1. Deployment and Hotfixes
- **[DON'T]**: Create a CI/CD pipeline that allows an emergency "hotfix" branch to be deployed directly to production.
- **[DO]**: Automate a "Rollback" feature that immediately reverts production to the previous known-stable build, and force the "hotfix" code through Staging and Canary.

### 2. Canary Ports
- **[DON'T]**: Assign port `8080` to production and `8081` to the canary pool to explicitly route test traffic.
- **[DO]**: Assign port `8080` to both canary and production, using the Load Balancer to randomly distribute 5% of standard production traffic to the canary instances.

### 3. Health Checks
- **[DON'T]**: Implement a basic health check endpoint that just returns a static status.
  ```javascript
  app.get('/health', (req, res) => {
      res.status(200).send("OK");
  });
  ```
- **[DO]**: Implement a semantic health check on a dedicated internal port that verifies local state.
  ```javascript
  // Hosted on internal administrative port 9090, while main traffic is on 8080
  app.get('/health', async (req, res) => {
      try {
          await db.ping();
          res.status(200).send("Healthy");
      } catch (error) {
          res.status(500).send("Database connection failed");
      }
  });
  ```

### 4. Dependency Mitigation (Defensive Caching)
- **[DON'T]**: Query a downstream dependency synchronously without a fallback, causing the host service to fail if the downstream service times out.
- **[DO]**: Wrap downstream queries in a Defensive LRU cache.
  ```python
  from functools import lru_cache
  import requests

  @lru_cache(maxsize=1000)
  def get_user_data_fallback(user_id):
      # Returns the last known good state from the LRU cache
      pass

  def fetch_user_data(user_id):
      try:
          response = requests.get(f"http://user-service/users/{user_id}", timeout=2)
          data = response.json()
          get_user_data_fallback.cache_clear() # simplify for example: update cache
          return data
      except requests.exceptions.RequestException:
          return get_user_data_fallback(user_id) # Defensive fallback
  ```

### 5. Deprecation
- **[DON'T]**: Delete an API endpoint in a PR because a new endpoint was created and the frontend team was verbally notified.
- **[DO]**: Mark the endpoint as `@Deprecated`, update the architecture documentation, notify client teams, monitor the endpoint's metrics for a minimum of one traffic cycle, and only remove the code when metrics prove the endpoint hits equal 0.