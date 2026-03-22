# @Domain
Trigger these rules when the user requests assistance with designing, implementing, automating, or planning resilience tests, fault injections, disaster simulations, or any tasks explicitly related to Chaos Engineering and testing the behavior of distributed systems under turbulent conditions.

# @Vocabulary
- **Chaos Engineering**: The empirical discipline of experimenting on a distributed system to build confidence in its capability to withstand turbulent conditions in production.
- **Drift into Failure**: The phenomenon where economic and human pressures push a highly optimized system closer to its safety boundaries, making it brittle to disruption.
- **Fundamental Regulator Paradox**: The concept that the better a regulator (feedback/control component) does its job, the less information it gets about how to improve.
- **Volkswagen Microbus Paradox**: The concept that you only learn how to fix things that break frequently; components that rarely break cause dire situations when they eventually do.
- **Antifragile**: A property of systems that actually improve their strength and resilience when exposed to stress and disorder.
- **Blast Radius**: The magnitude of bad experiences caused by a chaos test, measured by the number of customers affected and the degree of disruption.
- **Steady State**: The invariant, healthy baseline of externally observable behavior that a system maintains during normal operations.
- **Fault Injection**: The deliberate introduction of errors into a system, ranging from crude (killing instances) to subtle (latency, dropped service-to-service calls).
- **FIT (Failure Injection Testing)**: A technique that tags specific requests (e.g., via cookies or headers at an API gateway) to simulate a failure down the call tree without actually bringing down the target service.
- **Opt-In / Opt-Out**: Adoption models for chaos testing. "Opt-out" assumes all services are tested by default unless stigmatized by an exemption; "Opt-in" is lower adoption but safer for fragile, entrenched, or immature architectures.
- **Cunning Malevolent Intelligence**: A targeting method that uses traces of normal workload to build a graph of inferences, selectively cutting links to discover unknown redundancies rather than relying on random search.
- **Zombie Apocalypse Simulation**: A business continuity exercise that simulates the sudden incapacitation of a random percentage of the human workforce to expose single points of failure in organizational knowledge or roles.

# @Objectives
- Treat safety and resilience as non-composable emergent properties that must be verified empirically in the whole distributed system, rather than through formal models or isolated component tests.
- Counteract the system's natural "drift into failure" by routinely introducing controlled stress.
- Uncover hidden coupling, unexercised fallback mechanisms, race conditions, and single points of failure.
- Validate that the system can maintain its steady state (externally observable behavior) when subjected to instance death, network latency, or service dependency failures.
- Ensure that chaos experiments never cause irrecoverable damage to the business or its customers.

# @Guidelines
- **Prerequisite Validation**: The AI MUST NEVER propose executing a chaos experiment without first verifying that the system possesses adequate monitoring (to determine steady state), distributed tracing (to track failures/redundancies), and a well-defined recovery plan.
- **Blast Radius Containment**: The AI MUST constrain every experiment's exposure. The AI MUST recommend targeting specific cohorts, tagging requests, or limiting the percentage of traffic affected.
- **Hypothesis Formulation**: The AI MUST define hypotheses based strictly on *externally observable behavior* (e.g., "The application remains responsive under high latency"), NOT internal metrics (e.g., "CPU will spike").
- **Injection Selection**:
  - The AI MUST use *Instance Death* (e.g., Chaos Monkey) to test autoscaling and basic recovery.
  - The AI MUST use *Latency Injection* to test for hidden race conditions, out-of-order responses, and timeout/fallback inadequacies.
  - The AI MUST use *Failure Injection Testing (FIT)* using request tagging (e.g., via HTTP cookies/headers) to simulate downstream service failures without taking the actual provider offline.
- **Targeting Strategies**:
  - For immature chaos implementations, the AI MAY use randomized selection.
  - For mature implementations, the AI MUST use targeted selection based on call-tree analysis (Cunning Malevolent Intelligence), identifying links that the system *thinks* are critical and cutting them to find hidden redundancies.
- **Automation and Moderation**: The AI MUST build safety limits into automation scripts. For example, the AI MUST explicitly prevent a script from killing the very last instance in a cluster or failing a primary service *and* its fallback simultaneously.
- **Human Disaster Simulations**: When addressing operations and team structures, the AI MUST recommend human-focused chaos tests (Zombie Apocalypse Simulations). The AI MUST ensure these human drills include an explicit "abort code word" to halt the simulation during an actual existential crisis.
- **Adoption Strategy**: The AI MUST recommend an "Opt-In" model for organizations new to chaos engineering or possessing entrenched architectures, but MUST recommend transitioning to an "Opt-Out" model for mature, microservice-heavy environments to ensure maximum coverage.

# @Workflow
When tasked with designing or implementing a chaos engineering experiment, the AI MUST follow this rigid, step-by-step process:

1. **Assess Prerequisites**:
   - Confirm the ability to measure the "steady state" via existing dashboards/metrics.
   - Confirm distributed tracing is in place to follow a request through the system.
   - Verify that the target environment is production or a scale-accurate replica (since staging environments mask scale-related emergent behaviors).
2. **Formulate the Hypothesis**:
   - Define the expected invariant behavior during the disruption (e.g., "If service X is delayed by 50ms, the client will serve a cached response within 60ms and user checkout will succeed").
   - Define the statistical threshold of failure that will invalidate the hypothesis.
3. **Determine the Blast Radius**:
   - Define the containment strategy (e.g., applying the fault to 0.1% of users, or users with a specific test cookie).
4. **Design the Fault Injection**:
   - Choose the injection type: Instance Termination, Latency, or Request-level Failure (FIT).
   - Write the mechanism (e.g., an Ansible playbook, an API gateway routing rule, or a process-killer script).
5. **Implement Moderation (Safety Limits)**:
   - Add hardcoded checks to the script that abort the injection if the system crosses a defined danger threshold (e.g., "Abort if total cluster capacity drops below 50%").
6. **Define the Recovery & Rollback Plan**:
   - Document the exact steps, commands, or API calls required to revert the injected fault and clean up the environment if the system does not self-heal.
7. **Document for Postmortem**:
   - Provide a template for recording the traces of both failed requests AND requests that unexpectedly succeeded (to capture data on system redundancies).

# @Examples (Do's and Don'ts)

### Hypothesis Formulation
- **[DO]**: "Hypothesis: If the product recommendation service experiences 200ms of latency, the front-end API gateway will trigger its circuit breaker, return a default recommendation list, and overall user checkout success rate will remain within 1% of the steady state."
- **[DON'T]**: "Hypothesis: If we kill the database, the CPU on the application servers will drop to 0%." (This measures internal state, not external invariant behavior, and lacks a blast radius).

### Injection Scripting & Moderation
- **[DO]**:
  ```bash
  #!/bin/bash
  # Chaos injection with moderation
  TOTAL_INSTANCES=$(aws ec2 describe-instances --filters "Name=tag:Role,Values=Worker" | grep InstanceId | wc -l)
  if [ "$TOTAL_INSTANCES" -le 2 ]; then
      echo "Safety limit reached: Only $TOTAL_INSTANCES instances remaining. Aborting chaos injection."
      exit 1
  fi
  TARGET=$(aws ec2 describe-instances --filters "Name=tag:Role,Values=Worker" --query "Reservations[0].Instances[0].InstanceId" --output text)
  echo "Terminating instance $TARGET to test autoscaler recovery..."
  aws ec2 terminate-instances --instance-ids "$TARGET"
  ```
- **[DON'T]**:
  ```bash
  #!/bin/bash
  # Naive, dangerous kill script
  killall -9 java
  ```

### Failure Injection Testing (FIT)
- **[DO]**: Implement failure simulation at the API Gateway using HTTP headers to limit the blast radius.
  ```json
  // API Gateway Route Configuration
  {
    "route": "/checkout",
    "headers": {
      "X-Chaos-Experiment": "simulate-payment-timeout"
    },
    "action": {
      "delay": "5000ms",
      "return_status": 504
    }
  }
  ```
- **[DON'T]**: Randomly drop network packets via `iptables` on the payment gateway without limiting the effect to test traffic, thereby affecting real customers unpredictably.

### Human Chaos Engineering
- **[DO]**: "We will conduct a Zombie Apocalypse Simulation this Friday. 20% of the SRE team will be randomly selected to ignore all pages and emails. If a real Severity 1 incident occurs, the designated Incident Commander will issue the abort code word 'RUMPELSTILTSKIN' to immediately end the simulation."
- **[DON'T]**: "Tell half the team to stay home on Black Friday to see if the other half can handle the load."