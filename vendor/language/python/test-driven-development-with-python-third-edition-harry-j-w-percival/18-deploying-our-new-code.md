# @Domain
Trigger these rules when the user requests to deploy code to servers, run pre-deployment checks, manage server environments (staging or production) via Ansible, handle deployment-related database migrations, or tag repository releases.

# @Vocabulary
- **Deployment Checklist**: A strict, sequential series of tasks that must be executed to safely transition code from local development to production.
- **CI/CD**: Continuous Integration / Continuous Development (the eventual goal of automating the manual deployment checklist).
- **Staging**: A server environment designed to faithfully reproduce the production environment for final pre-deployment testing.
- **Production (Live)**: The public-facing server environment.
- **Ansible Playbook**: A YAML file used to automate the deployment procedure across different servers (`infra/deploy-playbook.yaml`).
- **Data Migration**: A Django mechanism used to safely transform existing database data to comply with new constraints, utilized when structural migrations fail due to existing data conflicts.
- **Git Tag**: A version control marker used to officially track the exact state of the codebase that is live on the server.

# @Objectives
- Guarantee that no code is shipped to production without passing tests in three progressively realistic environments: locally, locally inside Docker, and remotely on Staging.
- Ensure deployments are executed entirely via automated Ansible scripts rather than manual server changes.
- Maintain a strict historical record of deployed code using forced Git tags and timestamped tags.
- Safely resolve database integrity errors during deployment, strictly differentiating between destructive actions allowed on staging versus safe data migrations required for production.

# @Guidelines
- The AI MUST strictly follow the four-stage Deployment Checklist without skipping steps: Local Tests -> Docker Tests -> Staging Deploy & Tests -> Production Deploy.
- The AI MUST verify local tests are green using `cd src && python manage.py test` before proceeding to Docker.
- The AI MUST rebuild the Docker image and run the container locally before deploying.
- The AI MUST run functional tests (FTs) against the local Docker container using `TEST_SERVER=localhost:<port> python src/manage.py test functional_tests`.
- The AI MUST automate remote server deployments using `ansible-playbook`, passing the exact target host using the `-i <hostname>,` flag (note the trailing comma).
- The AI MUST deploy to Staging first, and MUST run FTs against the staging URL using the `TEST_SERVER` environment variable before touching Production.
- **CRITICAL DATABASE SAFETY**: If an `IntegrityError` occurs during migration on the Staging server, the AI MAY suggest deleting the database (`rm db.sqlite3` via SSH) as staging data is disposable. 
- **CRITICAL DATABASE SAFETY**: If an `IntegrityError` occurs during migration on the Production server, the AI MUST NEVER suggest deleting the database. The AI MUST recommend creating a Django data migration to resolve the conflict.
- The AI MUST tag the codebase immediately after a successful production deploy using a moving `LIVE` tag and a static timestamped `DEPLOYED-YYYY-MM-DD/HHMM` tag.

# @Workflow
When tasked with deploying new code, the AI MUST execute the following algorithmic process:

1. **Local Test Run**:
   - Execute the full unit and functional test suite locally.
   - Command: `cd src && python manage.py test`

2. **Docker Test Run**:
   - Rebuild the local Docker image and start the container with appropriate environment variables and volume mounts.
   - Run Functional Tests against the container.
   - Command: `TEST_SERVER=localhost:8888 python src/manage.py test functional_tests`

3. **Staging Deployment**:
   - Deploy the code to the staging server using Ansible.
   - Command: `ansible-playbook --user=<user> -i <staging_domain>, infra/deploy-playbook.yaml -vv`
   - If an `IntegrityError` occurs due to schema conflicts, SSH into staging and remove the database (`ssh <user>@<staging_domain> rm db.sqlite3`), then re-run the deployment.

4. **Staging Test Run**:
   - Run Functional Tests against the live staging server.
   - Command: `TEST_SERVER=<staging_domain> python src/manage.py test functional_tests`

5. **Production Deployment**:
   - Deploy the code to the production server using Ansible.
   - Command: `ansible-playbook --user=<user> -i <production_domain>, infra/deploy-playbook.yaml -vv`
   - If an `IntegrityError` occurs, STOP. Do not delete the database. Create a Django data migration to fix the violating records.

6. **Release Tagging**:
   - Tag the release in Git to mark the live codebase.
   - Command: `git tag -f LIVE`
   - Command: `export TAG=$(date +DEPLOYED-%F/%H%M)`
   - Command: `git tag $TAG`
   - Command: `git push -f origin LIVE $TAG`

# @Examples (Do's and Don'ts)

**[DO] Properly test against a remote staging server before production:**
```bash
# 1. Deploy to staging
ansible-playbook --user=elspeth -i staging.ottg.co.uk, infra/deploy-playbook.yaml -vv
# 2. Test staging
TEST_SERVER=staging.ottg.co.uk python src/manage.py test functional_tests
# 3. Only if the above passes, deploy to prod
ansible-playbook --user=elspeth -i www.ottg.co.uk, infra/deploy-playbook.yaml -vv
```

**[DON'T] Skip directly to production or skip functional tests:**
```bash
# ANTI-PATTERN: Deploying straight to prod without staging verification
ansible-playbook --user=elspeth -i www.ottg.co.uk, infra/deploy-playbook.yaml -vv
```

**[DO] Tag releases dynamically and overwrite the LIVE tag:**
```bash
git tag -f LIVE
export TAG=$(date +DEPLOYED-%F/%H%M)
git tag $TAG
git push -f origin LIVE $TAG
```

**[DON'T] Manually type static timestamps for tags:**
```bash
# ANTI-PATTERN: Hardcoding timestamps which leads to errors or forgotten updates
git tag DEPLOYED-2023-10-14/1200
```

**[DO] Handle Staging IntegrityErrors destructively if needed:**
```bash
ssh elspeth@staging.ottg.co.uk rm db.sqlite3
```

**[DON'T] Handle Production IntegrityErrors destructively:**
```bash
# ANTI-PATTERN: NEVER do this in production!
ssh elspeth@www.ottg.co.uk rm db.sqlite3 
```