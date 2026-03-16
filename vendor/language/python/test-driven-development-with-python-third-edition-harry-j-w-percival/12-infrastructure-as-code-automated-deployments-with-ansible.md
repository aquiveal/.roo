@Domain
These rules activate when the AI is tasked with creating, modifying, or executing Ansible playbooks, automating server deployments, configuring infrastructure as code (IaC), managing remote Docker containers via Ansible, or troubleshooting remote server deployments using SSH and Docker commands.

@Vocabulary
*   **Infrastructure as Code (IaC):** The practice of automating deployments and server provisioning through code (playbooks) rather than manual procedural steps.
*   **Ansible Playbook:** A YAML file containing a series of tasks that describe the desired state of a server.
*   **Module:** An Ansible tool used to accomplish a specific task (e.g., `ansible.builtin.apt`, `community.docker.docker_container`).
*   **Idempotence:** The property of a deployment script where running it multiple times yields the exact same state as running it once, without causing unintended side effects or errors.
*   **Declarative:** Specifying the *desired state* (e.g., `state: started`, `state: present`) rather than the procedural steps to achieve it.
*   **Inventory:** The list of target servers Ansible runs against, specified inline with the `-i` flag.
*   **Slurp:** An Ansible module (`ansible.builtin.slurp`) used to read the contents of a remote file into a variable, base64-encoded.
*   **Delegate_to:** An Ansible directive used to run a specific task on the local control machine (e.g., `127.0.0.1`) instead of the remote server.
*   **inventory_hostname:** An Ansible magic variable representing the hostname of the current server being deployed to.

@Objectives
*   Automate all deployment steps to enable small, frequent, and reliable deployments.
*   Ensure absolute parity between staging and production environments by using the exact same automation scripts for both.
*   Enforce idempotence and declarative configuration across all infrastructure tasks.
*   Isolate the deployment process from external commercial registries by packaging, exporting, and importing Docker images explicitly via Ansible.
*   Manage secrets and environment variables securely without hardcoding them into source control.
*   Establish seamless host-to-container database mounts with strict UID permission controls.

@Guidelines

**Ansible Command Execution**
*   The AI MUST use the `ansible-playbook` command with the `-i` flag for the inventory.
*   When passing a single hostname to `-i`, the AI MUST append a trailing comma (e.g., `-i staging.example.com,`) to ensure Ansible interprets it as a list, not a file path.
*   The AI MUST use `--user=<username>` to specify the SSH user.
*   The AI MUST use the `-v` or `-vv` flags to increase verbosity for debugging.
*   If sudo privileges fail, the AI MUST recommend or append the `--ask-become-pass` argument.

**Playbook Structure and Modules**
*   The AI MUST format playbooks using strictly valid YAML.
*   The AI MUST define a human-readable `name` attribute for every task.
*   The AI MUST use Fully Qualified Collection Names (FQCNs) for modules (e.g., `ansible.builtin.apt`, `ansible.builtin.copy`, `community.docker.docker_container`).
*   The AI MUST explicitly declare the desired state in tasks (e.g., `state: latest`, `state: started`, `state: present`).

**Server Dependency Management**
*   The AI MUST ensure dependencies (like Docker) are installed using the `ansible.builtin.apt` module with `update_cache: true` and `become: true`.
*   To avoid running Docker with `sudo` in subsequent tasks, the AI MUST add the deployment user to the `docker` group using `ansible.builtin.user` with `append: true`.
*   Immediately following the group addition, the AI MUST run the `ansible.builtin.meta: reset_connection` task to ensure the new group permissions take effect for the remainder of the playbook.

**Image Packaging and Transfer (Registry-less Deployment)**
*   The AI MUST build the container image locally using `community.docker.docker_image` with `source: build`, `force_source: true`, and `delegate_to: 127.0.0.1`.
*   The AI MUST account for architecture mismatches between the control machine and the server by specifying the platform during the local build (e.g., `platform: linux/amd64`).
*   The AI MUST export the image to a local archive (`archive_path`), use `ansible.builtin.copy` to upload the `.tar` file to the remote server, and use `community.docker.docker_image` with `source: load` to import it remotely.

**Secrets and Environment Variables**
*   The AI MUST NOT hardcode secrets in the playbook.
*   To generate one-off remote secrets (like a Django `SECRET_KEY`), the AI MUST use `ansible.builtin.copy` combined with an Ansible lookup (e.g., `lookup('password', '/dev/null length=32 chars=ascii_letters')`) and set `force: false` to preserve idempotence (do not recreate if it exists).
*   The AI MUST use `ansible.builtin.slurp` to read remote secret files into a registered variable.
*   The AI MUST decode slurped variables using the `b64decode` filter (e.g., `{{ secret_key.content | b64decode }}`).
*   The AI MUST use the `env` dictionary within the `docker_container` module to pass environment variables to the application.

**Database and Mount Management**
*   When mounting a host database file (like SQLite) into a container, the AI MUST use `ansible.builtin.file` with `state: touch` to ensure the host file exists before the container starts.
*   The AI MUST explicitly set the host file ownership (e.g., `owner: 1234`) to match the non-root UID used *inside* the container, running this specific task with `become: true`.
*   The AI MUST use the explicit `mounts` syntax in `docker_container` (specifying `type: bind`, `source`, and `target`) rather than legacy `-v` volume strings.

**Post-Deployment Execution**
*   The AI MUST map the public HTTP port to the container's internal port using the `ports` directive (e.g., `80:8888`).
*   The AI MUST force container recreation upon deployment using `recreate: true` in the `docker_container` module.
*   The AI MUST run database migrations inside the newly started container using `community.docker.docker_container_exec`.

**Release Tagging**
*   Following a successful production deployment, the AI MUST advise the user to tag the release in Git (e.g., `git tag LIVE`, `git push -f origin LIVE $TAG`) to maintain a historical marker of the production state.

@Workflow
1.  **Preparation:** Verify SSH access to the remote server and install local prerequisites (`pip install ansible docker`).
2.  **Server Provisioning:** Write tasks to install Docker via `apt`, add the user to the `docker` group, and reset the SSH connection.
3.  **Local Image Build:** Write a delegated task to build the Docker image locally for the target architecture, then archive it to a `.tar` file.
4.  **Image Transfer:** Write tasks to copy the archive to the remote server and load it into the remote Docker daemon.
5.  **State Management:** Write tasks to generate (if missing) and slurp secret keys, and `touch` the target database file with proper UID ownership.
6.  **Container Launch:** Write the `docker_container` task, passing all required environment variables, port mappings, and bind mounts, ensuring `recreate: true` is set.
7.  **Migrations:** Write a `docker_container_exec` task to apply database schema changes.
8.  **Execution & Testing:** Execute the playbook against the staging inventory, run functional tests against staging, and upon success, execute the exact same playbook against the production inventory.
9.  **Tagging:** Execute Git commands to tag the deployed state.

@Examples

**[DO] Execute Ansible with a single host inventory properly**
```bash
ansible-playbook --user=elspeth -i staging.example.com, infra/deploy-playbook.yaml -vv
```

**[DON'T] Forget the trailing comma for a single host inventory**
```bash
ansible-playbook --user=elspeth -i staging.example.com infra/deploy-playbook.yaml -vv
```

**[DO] Safely handle rootless Docker setup in a playbook**
```yaml
    - name: Add our user to the docker group
      ansible.builtin.user:
        name: "{{ ansible_user }}"
        groups: docker
        append: true
      become: true

    - name: Reset ssh connection to allow the user/group change to take effect
      ansible.builtin.meta:
        reset_connection
```

**[DON'T] Rely on `become: true` for every Docker task instead of configuring the group**
```yaml
    - name: Run container
      community.docker.docker_container:
        name: myapp
        # BAD: Relying on sudo instead of configuring rootless docker access
      become: true 
```

**[DO] Build and export the image locally before transfer**
```yaml
    - name: Build container image locally
      community.docker.docker_image:
        name: superlists
        source: build
        state: present
        build:
          path: ..
          platform: linux/amd64
        force_source: true
      delegate_to: 127.0.0.1

    - name: Export container image locally
      community.docker.docker_image:
        name: superlists
        archive_path: /tmp/superlists-img.tar
        source: local
      delegate_to: 127.0.0.1
```

**[DON'T] Build the image on the production server pulling raw source code**
```yaml
    # BAD: Unpredictable build environment, requires Git/SSH keys on the prod server
    - name: Clone repo and build on server
      ansible.builtin.git:
        repo: git@github.com:user/repo.git
```

**[DO] Manage secrets securely via lookup and slurp**
```yaml
    - name: Ensure .secret-key file exists
      ansible.builtin.copy:
        dest: ~/.secret-key
        content: "{{ lookup('password', '/dev/null length=32 chars=ascii_letters') }}"
        mode: 0600
        force: false

    - name: Read secret key back from file
      ansible.builtin.slurp:
        src: ~/.secret-key
      register: secret_key

    - name: Run container
      community.docker.docker_container:
        # ...
        env:
          DJANGO_SECRET_KEY: "{{ secret_key.content | b64decode }}"
```

**[DON'T] Hardcode secrets into the playbook**
```yaml
    - name: Run container
      community.docker.docker_container:
        # ...
        env:
          # BAD: Hardcoded secret committed to version control
          DJANGO_SECRET_KEY: "super-secret-key-123"
```

**[DO] Ensure database file ownership matches container UID before mounting**
```yaml
    - name: Ensure db.sqlite3 file exists outside container
      ansible.builtin.file:
        path: "{{ ansible_env.HOME }}/db.sqlite3"
        state: touch
        owner: 1234
      become: true

    - name: Run container
      community.docker.docker_container:
        # ...
        mounts:
          - type: bind
            source: "{{ ansible_env.HOME }}/db.sqlite3"
            target: /home/nonroot/db.sqlite3
```