@Domain
These rules trigger when the AI is tasked with designing release management processes, creating CI/CD pipelines, writing deployment scripts, architecting operational environments, defining QA/testing data strategies, or optimizing existing deployment workflows.

@Vocabulary
- **Deployment Army**: A massive, unnecessary allocation of human capital (developers, DBAs, sysadmins, stakeholders) required to manually execute and monitor a software release.
- **Playbook**: A rigid, sequential, human-executed checklist document used to orchestrate manual deployment actions.
- **Playbook Time (Lamport Clock)**: The artificial timeline of a manual deployment that stalls completely when a single human or script step fails, diverging from actual wall-clock time.
- **Go/No-Go Meeting**: An inefficient synchronous meeting requiring mass human coordination to decide if a release should proceed, often based on incomplete or subjective QA feedback.
- **UAT Window**: User Acceptance Testing window; scheduled off-hours (e.g., 1 a.m.) where human stakeholders must manually smoke-test new features in production.
- **Jumphost / Sys Ops Execution**: The manual act of logging into a secure server via SSH to run deployment commands (e.g., updating symlinks, precompiling, restarting servers).
- **Deployinator**: A push-button, fully automated deployment mechanism that treats releasing software to production as a trivial, routine event.
- **Environment Drift**: The discrepancy between QA and Production environments (e.g., missing third-party JavaScript, mismatched data) that allows bugs to pass QA but fail in production.

@Objectives
- Completely eliminate human-executed "playbooks" and manual deployment armies in favor of fully automated, push-button deployment pipelines.
- Eradicate the need for off-hours, manual User Acceptance Testing (UAT) by implementing automated smoke tests and integration tests.
- Ensure strict parity between QA and Production data and environmental configurations to prevent late-stage deployment rollbacks.
- Shift the organizational mindset from treating deployments as expensive, high-risk, multi-hour events to routine, low-risk, automated actions.

@Guidelines
- **Automate the Playbook:** When asked to create a release procedure or deployment guide, the AI MUST NOT generate a text-based checklist for humans. The AI MUST output executable pipeline code (e.g., Jenkinsfile, GitHub Actions, GitLab CI) that automates the sequence.
- **Ban Manual Sys Ops Interventions:** When detailing how to deploy artifacts, the AI MUST NEVER suggest logging into a jumphost via SSH to manually update symlinks, run compilers (e.g., JSP precompilers), or restart processes. The AI MUST implement these as automated steps within the deployment script.
- **Enforce QA/Production Parity:** When designing QA environments or testing strategies, the AI MUST specify mechanisms to mirror production data, content, and third-party integrations (e.g., external JavaScript). If the user proposes a simplified QA environment, the AI MUST warn that mismatched data causes production UAT failures and rollbacks.
- **Replace Manual UAT with Automated Smoke Tests:** When structuring the post-deployment phase, the AI MUST NOT allocate time windows for human stakeholders to wake up and test the system. The AI MUST define automated smoke tests that run instantly against the production or staging environment.
- **Eliminate the Deployment Army:** When reviewing a release management process, the AI MUST aggressively identify and remove bottlenecks requiring mass human coordination (like synchronous "Go/No-Go" meetings). The AI MUST replace these with automated gating mechanisms based on test coverage and metric thresholds.
- **Quantify Deployment Waste:** When analyzing existing manual deployment strategies, the AI MUST highlight the financial and human cost (e.g., calculating the hourly rate of the "deployment army" over the duration of the deployment) to justify the transition to an automated "Deployinator" model.
- **Automate Rollbacks:** When handling deployment failures, the AI MUST NOT rely on humans to manually revert database scripts and symlinks at 5 a.m. The AI MUST provision automated, scriptable rollback mechanisms.

@Workflow
When tasked with designing, reviewing, or refactoring a deployment process, the AI MUST strictly follow this algorithm:
1. **Audit for Manual Actions:** Scan the proposed or existing process for any human interventions (SSH access, manual script execution, manual database updates).
2. **Convert to Code:** Translate every identified manual step (the "playbook") into an automated CI/CD pipeline stage.
3. **Establish Environment Parity:** Define the automated synchronization of production-like data, edge-case content, and third-party scripts into the QA environment prior to deployment.
4. **Define the Deployinator:** Architect the final deployment trigger as a single, automated push-button action requiring zero human orchestration during the execution phase.
5. **Automate Verification:** Replace all manual UAT steps with automated post-deployment smoke tests that instantly verify system health.
6. **Provision Automated Rollback:** Ensure that if the automated smoke tests fail, the pipeline automatically executes a rollback without requiring human debugging during the deployment window.

@Examples (Do's and Don'ts)

**[DON'T]** Generate a manual deployment playbook for human execution.
```markdown
### Deployment Playbook (Start at 11:00 PM)
1. 11:00 PM - DBA logs in and runs `schema_update.sql`.
2. 11:50 PM - Wait for DBA confirmation. 
3. 12:40 AM - SysAdmin SSH into jumphost.
4. 1:00 AM - SysAdmin runs `update_symlinks.sh` and precompiles JSPs.
5. 1:15 AM - Business stakeholders wake up and log in to perform UAT.
6. 2:00 AM - Go/No-Go decision on conference bridge.
```

**[DO]** Generate a fully automated CI/CD pipeline that eliminates human intervention.
```yaml
# Push-button Deployinator Pipeline
stages:
  - name: Run Database Migrations
    script:
      - flyway migrate --url=$DB_URL --locations=filesystem:sql/
  - name: Deploy Artifacts and Swap Symlinks
    script:
      - ansible-playbook deploy.yml -i production_inventory
  - name: Automated Smoke Tests (Replaces Manual UAT)
    script:
      - cypress run --env target=production
  - name: Automated Rollback (On Failure)
    script:
      - ansible-playbook rollback.yml -i production_inventory
    condition: on_failure
```

**[DON'T]** Allow QA to test with sterilized data that lacks production complexity.
```text
QA Environment Setup:
Insert 10 sample user records. Do not include third-party analytics or ad-tracking JavaScript to keep the environment fast and clean.
```

**[DO]** Enforce strict QA data parity to prevent post-deployment surprises.
```text
QA Environment Setup:
To prevent deployment failures caused by content mismatch, the QA environment MUST ingest an anonymized clone of the latest production database. It MUST render all third-party integrations (ad trackers, external JavaScript) exactly as they appear in production.
```