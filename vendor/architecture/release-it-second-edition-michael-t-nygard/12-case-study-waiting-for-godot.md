# @Domain
These rules MUST activate when the user requests assistance with:
- Designing, creating, or modifying deployment processes, CI/CD pipelines, or release architectures.
- Writing shell scripts, automation scripts, or infrastructure-as-code for server provisioning, symlink management, or application restarts.
- Configuring QA, staging, or testing environments and defining their data sources.
- Defining User Acceptance Testing (UAT) processes or post-deployment validation steps.
- Creating rollback mechanisms for failed deployments.

# @Vocabulary
- **Deployment Army**: An antipattern describing a massive coordination of human effort (e.g., 40+ people) required to execute a single deployment.
- **Playbook**: A manual, row-by-row checklist of tasks executed by humans to perform a deployment. Treated as a strict antipattern that must be replaced by executable code.
- **Lamport Clock (Deployment Context)**: A logical time scale tied to the progression of manual deployment playbook steps rather than actual solar time, causing prolonged, stagnant deployment windows.
- **Solar Time**: Actual, real-world wall-clock time.
- **Go/No-Go Meeting**: A manual coordination meeting to decide if a deployment proceeds; a symptom of high-risk, unautomated release processes.
- **Deployinator**: The target architectural ideal (inspired by Etsy) where a deployment is so fully automated and risk-free that it can be triggered by a single button press from a non-technical user.
- **UAT Window**: User Acceptance Testing window; a designated time (often late at night) for business stakeholders to manually verify a deployment.
- **Human-as-a-bot**: The antipattern of requiring human engineers to manually execute rote commands (e.g., SSHing into servers to run scripts).
- **QA Data Mismatch**: An environmental failure where QA environments lack the messy, real-world data and third-party integrations (like JavaScript overrides) present in production, leading to false confidence and production crashes.

# @Objectives
- Eradicate manual deployment procedures, "playbooks," and human coordination meetings by translating all deployment logic into fully automated, executable scripts.
- Eliminate "Deployment Armies" and "Human-as-a-bot" operations by architecting single-click deployment triggers (the "Deployinator" standard).
- Guarantee absolute parity between QA/Testing environments and Production, specifically enforcing the inclusion of messy production data and third-party content/scripts.
- Prevent prolonged, late-night UAT failures and manual rollback scrambles by mandating automated, instantaneous rollback mechanisms for every deployment.

# @Guidelines

- **Eradicate Manual Playbooks**: When asked to document a deployment process, the AI MUST NOT generate a manual Markdown checklist or runbook for humans to follow. The AI MUST generate executable infrastructure-as-code or CI/CD pipeline configurations (e.g., bash, GitHub Actions, Jenkinsfiles).
- **Automate the "Sys Ops" Role**: When encountering tasks that require updating symlinks, running precompilers (e.g., JSP precompilation), or starting/stopping server processes, the AI MUST write scripts that execute these tasks programmatically across all target machines without human intervention. The AI MUST NOT instruct the user to SSH into a jumphost to run commands manually.
- **Enforce QA/Production Data Parity**: When scaffolding QA or test environments, the AI MUST include mechanisms to replicate or ingest true production state. The AI MUST explicitly account for third-party integrations, external JavaScripts, and unstructured content that exist in production to prevent late-stage UAT failures.
- **Isolate UAT Scope**: When generating validation or UAT test suites, the AI MUST ensure tests are strictly scoped to the features being released. The AI MUST implement safeguards to prevent automated deployment failures caused by known, pre-existing legacy bugs on unrelated pages.
- **Architect for the "Deployinator"**: When designing a release flow, the AI MUST structure the pipeline so that the entire deployment (from code drop to symlink swap to server restart) is triggered by a single, unified action. 
- **Mandate Instantaneous Rollbacks**: For every deployment script generated, the AI MUST simultaneously generate a corresponding, fully automated rollback script. The AI MUST NEVER leave the user in a state where a failed deployment requires hours of manual commands to revert.
- **Eliminate the "Lamport Clock"**: Deployments must be designed to execute at machine speed. The AI MUST NOT design deployment workflows that require pauses for manual human verification between technical steps (e.g., waiting for DBA script confirmation before swapping symlinks).

# @Workflow
When tasked with designing a deployment, release process, or environment configuration, the AI MUST adhere to this rigid algorithmic process:

1. **Process Ingestion & Deconstruction**: Analyze the requested deployment steps. Identify any step requiring human coordination, manual SSH access, or manual playbook verification.
2. **Translation to Code**: Convert every identified manual step (e.g., SQL script execution, code dropping, symlink updating, precompiling, server restarting) into automated scripts.
3. **Environment Parity Verification**: Define the QA/Testing environment scaffolding. Explicitly inject configurations that pull production-like data, user-generated content, and third-party scripts to ensure exact behavioral matching.
4. **Single-Trigger Integration**: Wrap all automated scripts into a single CI/CD pipeline or master script (the "Deployinator").
5. **Rollback Generation**: Write a secondary script that instantly reverses the symlinks, restores the previous database state (or relies on backward-compatible schema design), and restarts the servers to their pre-deployment state.
6. **Validation Scoping**: Generate automated post-deployment smoke tests that verify *only* the mutated paths, ensuring unrelated legacy issues do not block the pipeline.

# @Examples (Do's and Don'ts)

### Playbooks vs. Automation
- **[DON'T]** Generate a manual playbook for the team:
  ```markdown
  ## Deployment Playbook
  1. 11:50 PM: DBAs run the SQL migration scripts.
  2. 12:40 AM: SysOps SSH into the jumphost.
  3. 1:17 AM: SysOps update the symlinks to point to the new code drop.
  4. 1:20 AM: SysOps run the JSP precompiler.
  5. 1:30 AM: SysOps restart the application servers.
  6. 1:30 AM - 3:00 AM: Business stakeholders perform UAT.
  ```
- **[DO]** Generate an automated deployment script:
  ```bash
  #!/bin/bash
  # deployinator.sh - Single-click deployment
  set -e
  echo "Executing DB Migrations..."
  flyway update -url=$DB_URL -user=$DB_USER -password=$DB_PASS
  echo "Updating Symlinks across all web servers..."
  ansible webservers -m file -a "src=/opt/app/releases/$1 dest=/opt/app/current state=link"
  echo "Running precompilation..."
  ansible webservers -m command -a "/opt/app/current/bin/precompile.sh"
  echo "Restarting services..."
  ansible webservers -m service -a "name=app-server state=restarted"
  echo "Deployment $1 Complete. Initiating targeted smoke tests..."
  npm run test:smoke -- --tags "@release-$1"
  ```

### QA Environment Parity
- **[DON'T]** Stub out third-party scripts in QA to make testing "easier":
  ```html
  <!-- QA Environment: Mocking 3rd party scripts -->
  <script>
    // Mocking 3rd party vendor JS that rewrites DOM
    window.VendorUI = { render: () => console.log("Mocked") };
  </script>
  ```
- **[DO]** Ensure exact production parity in QA to catch structural conflicts:
  ```html
  <!-- QA Environment: Using actual production scripts to catch DOM rewrite conflicts -->
  <script src="https://cdn.thirdpartyvendor.com/ui-rewriter.prod.js"></script>
  <script>
    // System must test against the actual DOM mutation caused by the 3rd party
    window.VendorUI.init({ environment: "qa-mirroring-prod" });
  </script>
  ```

### Rollback Mechanisms
- **[DON'T]** Rely on human intervention for rollbacks:
  "If the deployment fails during the UAT window, page the SysOps team to SSH back into the servers, manually change the symlinks back to the previous timestamp, and restart the servers. Expect this to take until 5:00 AM."
- **[DO]** Architect an immediate, automated rollback script:
  ```bash
  #!/bin/bash
  # rollback.sh
  set -e
  PREVIOUS_RELEASE=$(cat /opt/app/.previous_release)
  echo "UAT Failed. Initiating instant rollback to $PREVIOUS_RELEASE..."
  ansible webservers -m file -a "src=/opt/app/releases/$PREVIOUS_RELEASE dest=/opt/app/current state=link"
  ansible webservers -m service -a "name=app-server state=restarted"
  echo "Rollback complete. System restored."
  ```