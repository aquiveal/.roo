@Domain
Trigger these rules when executing tasks related to microservice architecture, continuous integration/continuous deployment (CI/CD) pipelines, dependency management, routing and service discovery configuration, or the deprecation and decommissioning of microservices and API endpoints.

@Vocabulary
*   **Stability**: The property of a microservice where development, deployment, new technologies, and decommissioning do not give rise to instability within the larger ecosystem.
*   **Reliability**: The property of a microservice where it has earned the trust of its clients, dependencies, and the ecosystem to serve production traffic.
*   **Development Cycle**: The standardized process of developing, testing, reviewing, building, and releasing code prior to deployment.
*   **Deployment Pipeline**: The structured, multi-stage process (Staging -> Canary -> Production) used to roll out candidates for production.
*   **Staging Environment**: A deployment phase that mirrors production (either fully or partially) used to test a new release without serving real user traffic.
*   **Full Staging**: A staging environment that is a complete mirror copy of the production ecosystem, communicating only with other staging services and using separate test databases.
*   **Partial Staging**: A staging environment where the microservice communicates with upstream and downstream dependencies running in real production, utilizing read-only access or strict test tenancy.
*   **Canary Environment**: A deployment phase where a new build is deployed to a small pool of servers (5%-10%) serving real production traffic to accurately sample behavior before a full rollout.
*   **Traffic Cycle**: A standardized duration of time that a deployment must remain in the canary phase to capture a complete pattern of normal traffic.
*   **Defensive Caching**: A technique (often using a Least Recently Used or LRU cache) to store data from downstream dependencies, mitigating failures if those dependencies become unavailable.
*   **Circuit Breaker**: A routing and discovery mechanism that stops sending requests to a service or host if it experiences an abnormal amount of errors or unhandled exceptions.
*   **Hotfix**: The anti-pattern of bypassing staging and canary environments to deploy code directly to production.

@Objectives
*   Guarantee microservice stability by enforcing a rigid, test-driven development cycle and a multi-stage deployment pipeline.
*   Ensure reliability by proactively identifying and mitigating downstream dependency failures through caching, fallbacks, and circuit breakers.
*   Prevent ecosystem cascading failures by enforcing accurate, deep health checks and strictly separating deployment traffic environments.
*   Enable safe lifecycle management by executing cautious, heavily monitored deprecation and decommissioning procedures.

@Guidelines

**1. The Development Cycle**
*   The AI MUST enforce that all lint, unit, integration, and end-to-end (E2E) tests are executed and pass *before* code is submitted for review.
*   The AI MUST ensure the development environment accurately mirrors the production environment.
*   The AI MUST automate the test, packaging, build, and release processes. Manual intervention in building releases is strictly prohibited.

**2. The Deployment Pipeline**
*   The AI MUST NEVER implement or recommend bypassing the deployment pipeline (i.e., NO direct-to-production hotfixes). In emergency failure scenarios, the AI MUST recommend rolling back to the last known stable build.
*   The AI MUST block deployments for any microservice that has exhausted its downtime quota (failed to meet its SLA) or failed load testing.
*   **Staging Phase Constraints**:
    *   The AI MUST configure the staging environment to run mock/recorded traffic or automated integration/E2E tests.
    *   If configuring *Full Staging*: The AI MUST ensure the service communicates ONLY with other staging services and uses strictly separate test databases.
    *   If configuring *Partial Staging*: The AI MUST ensure the staging service hits production endpoints but is strictly restricted to read-only database access OR uses strictly isolated test tenancy for writes. The AI MUST mandate automated rollbacks for partial staging.
*   **Canary Phase Constraints**:
    *   The AI MUST configure the canary pool to represent 5%-10% of total production capacity.
    *   The AI MUST ensure canary servers are chosen at random, distributed across all active datacenters/regions, and utilize the exact same frontend and backend ports as production.
    *   The AI MUST configure fully automated rollbacks for the canary phase based on predefined error thresholds.
    *   The AI MUST enforce that a build remains in the canary phase for a full, defined "traffic cycle" before production rollout.
*   **Production Phase Constraints**:
    *   The AI MUST configure production deployments to either occur post-canary in one step or be incrementally rolled out by percentage (e.g., 25%, 50%, 75%, 100%) or by region.

**3. Dependency Management**
*   The AI MUST explicitly identify, track, and document all upstream clients and downstream dependencies.
*   For every downstream dependency, the AI MUST implement a mitigation strategy: a backup, an alternative, a fallback mechanism, or defensive caching (e.g., an LRU cache).
*   The AI MUST monitor dependency SLAs and incorporate them into the calling service's availability calculations.

**4. Routing and Discovery**
*   The AI MUST implement accurate, deep health checks. The AI MUST NOT use hardcoded `200 OK` responses that only verify the HTTP server is running. Health checks must verify the actual operational capacity of the service.
*   The AI MUST configure health checks to run on a separate, dedicated communication channel to prevent network congestion from causing false negatives.
*   The AI MUST implement circuit breakers that trip and temporarily halt traffic routing to hosts or services that exhibit a high rate of unhandled exceptions or failing health checks.

**5. Deprecation and Decommissioning**
*   The AI MUST NOT completely delete or immediately decommission an API endpoint or microservice without a transition phase.
*   The AI MUST implement monitoring on any deprecated endpoint to track residual incoming requests.
*   The AI MUST provide scripts or communication templates to alert client services and advise them on new endpoints or fallback accommodations.

@Workflow
When tasked with developing, configuring, or updating a microservice, the AI MUST execute the following algorithm:

1.  **Development & Pre-Commit Validation**:
    *   Write the feature/fix.
    *   Generate/update lint, unit, integration, and E2E tests.
    *   Run tests locally. If any fail, correct the code. Only proceed to Code Review/Merge when all tests pass.
2.  **Pipeline Configuration (If applicable)**:
    *   Verify/configure Staging Phase (Full or Partial). Implement read-only constraints for Partial staging.
    *   Verify/configure Canary Phase. Set capacity to 5%-10% and wire automated rollback triggers based on logging/monitoring alerts.
    *   Verify/configure Production Phase for incremental rollout.
3.  **Dependency Resilience Injection**:
    *   Analyze external calls. Inject LRU defensive caching or fallback queues for every downstream dependency.
4.  **Routing & Health Configuration**:
    *   Write a `/health` endpoint that checks internal state (e.g., db connectivity, worker thread availability).
    *   Wrap outbound RPC/HTTP calls in Circuit Breaker logic.
5.  **Deprecation Execution (If applicable)**:
    *   Mark endpoint as deprecated in code (e.g., using `@Deprecated` tags or warning headers).
    *   Add specific logging for requests hitting the deprecated endpoint.
    *   Retain the endpoint until monitoring confirms zero traffic, then remove.

@Examples (Do's and Don'ts)

**Principle: Dependency Mitigation (Defensive Caching)**

[DO]
```python
from cachetools import LRUCache
import requests

# Defensive LRU cache for dependency
dependency_cache = LRUCache(maxsize=1000)

def get_customer_info(customer_id):
    try:
        # Attempt to call downstream dependency
        response = requests.get(f"http://customers-service/api/v1/users/{customer_id}", timeout=2)
        response.raise_for_status()
        data = response.json()
        dependency_cache[customer_id] = data # Update cache
        return data
    except requests.exceptions.RequestException:
        # Fallback to defensive cache if dependency fails
        if customer_id in dependency_cache:
            return dependency_cache[customer_id]
        raise CustomerServiceUnavailableException("Dependency down and data not in cache")
```

[DON'T]
```python
import requests

def get_customer_info(customer_id):
    # Single point of failure: No fallback, no cache, no timeout. 
    # If customers-service is down, this service goes down.
    response = requests.get(f"http://customers-service/api/v1/users/{customer_id}")
    return response.json()
```

**Principle: Routing and Health Checks**

[DO]
```python
@app.route('/health')
def health_check():
    # Deep health check verifying operational capacity
    db_status = check_database_connection()
    worker_status = check_available_workers()
    
    if db_status and worker_status:
        return jsonify({"status": "healthy", "db": "ok", "workers": "ok"}), 200
    else:
        return jsonify({"status": "unhealthy", "db": db_status, "workers": worker_status}), 503
```

[DON'T]
```python
@app.route('/health')
def health_check():
    # Anti-pattern: Hardcoded response that doesn't actually check service health
    return "200 OK", 200
```

**Principle: Deployment Fixes**

[DO]
```bash
# Incident detected in production deployment
# 1. Automated/Manual Rollback to last known stable build
deploy-cli rollback --service receipt-sender --target production

# 2. Fix the bug locally, run tests
pytest tests/

# 3. Push through the pipeline again
git commit -m "Fix bug causing production incident"
git push
# CI/CD automatically handles Staging -> Canary -> Prod
```

[DON'T]
```bash
# Anti-pattern: Hotfixing directly to production bypassing the pipeline
git commit -m "Emergency hotfix"
deploy-cli deploy --service receipt-sender --target production --force --skip-canary
```

**Principle: Deprecation of an API Endpoint**

[DO]
```python
import logging

@app.route('/api/v1/old-endpoint')
def deprecated_endpoint():
    # Monitor usage to ensure clients have migrated before decommissioning
    logging.warning("DEPRECATED_ENDPOINT_ACCESSED: Client IP %s is still using v1/old-endpoint", request.remote_addr)
    
    # Include deprecation headers in response
    response = make_response(process_old_request())
    response.headers['Deprecation'] = 'true'
    response.headers['Link'] = '<http://api/v2/new-endpoint>; rel="alternate"'
    return response
```

[DON'T]
```python
# Anti-pattern: Simply deleting the endpoint from the codebase without monitoring traffic
# This immediately breaks upstream clients that haven't updated yet.
# (Code deleted)
```