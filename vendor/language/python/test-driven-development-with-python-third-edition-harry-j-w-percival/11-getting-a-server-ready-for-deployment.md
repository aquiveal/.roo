@Domain
This rule file activates whenever the AI is tasked with server provisioning, deployment preparation, infrastructure-as-code (IaC) configuration, DNS setup, Ansible playbook creation, or debugging remote SSH connectivity for web applications.

@Vocabulary
- **Provisioning**: The act of setting up the bare server infrastructure, including choosing the operating system, establishing basic login credentials, and configuring DNS routing.
- **Deploying**: The process of moving the application code (or Docker containers) onto an existing provisioned server, starting it, and configuring it to communicate with the outside world.
- **VPS (Virtual Private Server)**: A virtual machine sold as a service by an internet hosting provider. Preferred over PaaS in this context for gaining deeper administrative control and understanding.
- **PaaS (Platform as a Service)**: A cloud computing model (e.g., Heroku) that hides server administration; noted as an alternative but intentionally bypassed here for educational control.
- **A-Record**: A DNS record that points a domain or subdomain directly to the IPv4 address of the hosting server.
- **TTL (Time To Live)**: A DNS setting that dictates how long it takes for DNS record changes to propagate across the internet.
- **IaC (Infrastructure as Code)**: Managing and provisioning computing infrastructure through machine-readable definition files (e.g., Ansible YAML) rather than physical hardware configuration or interactive configuration tools.
- **Declarative Configuration**: Specifying the *desired state* of the server in code, rather than writing a procedural script of sequential commands to achieve that state.
- **Ansible Playbook**: A YAML file describing a set of tasks (using Ansible modules) to be executed on a target server.
- **WSL (Windows Subsystem for Linux)**: A compatibility layer for running Linux binary executables natively on Windows. Required for running Ansible on Windows machines.

@Objectives
- Separate the concerns of server provisioning from application deployment.
- Construct server configuration declaratively using Ansible, treating infrastructure entirely as code.
- Ensure the server environment is secured using nonroot, sudo-privileged users and SSH public/private key authentication.
- Methodically debug and resolve network, DNS, and SSH authentication issues before attempting automated deployments.
- Apply test-driven development (TDD) principles to infrastructure: work incrementally, make one change at a time, and revert to a known working state instead of randomly guessing when a failure occurs.

@Guidelines

- **Server Prerequisites Constraint**: The AI MUST assume the target server is running Ubuntu 22.04 (Jammy/LTS), is accessible via the public internet (has a public IP), and provides root and nonroot access.
- **Authentication Constraint**: The AI MUST configure and enforce SSH access via public/private key pairs for a nonroot user with `sudo` privileges.
- **DNS Setup Rules**: 
  - The AI MUST instruct the user to configure distinct DNS A-records for both `staging` and `live` (production) domains.
  - The AI MUST remind the user that DNS propagation depends on TTL and may require waiting; recommend propagation checking tools (e.g., whatsmydns) if name resolution fails.
- **Windows Subsystem for Linux (WSL) Rules**:
  - If the user is operating on Windows, the AI MUST strictly route all Ansible and infrastructure execution through WSL.
  - The AI MUST instruct the creation and activation of a dedicated virtual environment specifically for WSL (e.g., `.venv-wsl`).
- **Ansible Playbook Formatting**:
  - The AI MUST write Ansible playbooks in YAML format, typically stored in a dedicated infrastructure directory (e.g., `infra/`).
  - Playbook tasks MUST prioritize declarative Ansible modules over procedural shell commands to ensure idempotency.
- **Ansible CLI Execution Rules**:
  - When providing the `ansible-playbook` command targeting a single host, the AI MUST append a trailing comma to the inventory argument (e.g., `-i staging.domain.com,`).
  - The AI MUST explicitly declare the SSH user using the `--user=` flag.
  - The AI MUST append the `-v` or `-vv` flag to increase verbosity for easier debugging.
- **Systematic SSH Debugging**: If an SSH connection fails, the AI MUST guide the user through a strict sequence of checks:
  1. **Network/DNS**: Run `ping <domain>` or `ping <ip>`, followed by `nslookup <domain>` to verify resolution.
  2. **Auth Details**: Run SSH with the verbose flag (`ssh -v user@domain`) to trace exactly which keys are being offered and accepted/rejected.
  3. **Root Fallback**: Try connecting as the root user (`ssh root@domain`) to determine if the issue is isolated to the nonroot user's `authorized_keys` file.
- **Infrastructure Refactoring Cat Trap**: When infrastructure breaks, the AI MUST advise the user to stop, investigate the specific failure, and revert to a known working state rather than making unrelated speculative changes.
- **Security Hardening**: The AI MUST highlight the need for basic server security, explicitly recommending tools like Fail2Ban to protect against automated SSH brute-force attacks.

@Workflow
1. **Domain and DNS Validation**: Confirm the user has registered a domain and mapped A-records for staging and production environments to the VPS IP address. Verify resolution using `nslookup`.
2. **Manual SSH Verification**: Test SSH connectivity to the server manually using the nonroot user and key (`ssh user@server`). If this fails, execute the systematic SSH debugging steps defined in the guidelines.
3. **Ansible Preparation**: Create a dedicated infrastructure directory (`mkdir infra`). If on Windows, ensure the user transitions to WSL and initializes a WSL-specific Python virtual environment.
4. **Initial Playbook Creation**: Write a minimal Ansible playbook (`deploy-playbook.yaml`) containing only a `hosts: all` definition and a single `ansible.builtin.ping` task to establish baseline IaC communication.
5. **Ansible Connectivity Test**: Execute the playbook using the strict CLI format: `ansible-playbook --user=<username> -i <domain>, infra/deploy-playbook.yaml -vv`.
6. **Incremental Expansion**: Once the ping task succeeds, iteratively add and test further deployment tasks (e.g., Docker installation, environment variable configuration) one at a time.

@Examples (Do's and Don'ts)

- **Ansible Inventory Flag**
  - [DO]: `ansible-playbook -i staging.example.com, infra/deploy-playbook.yaml` (Includes the required trailing comma for a single host list).
  - [DON'T]: `ansible-playbook -i staging.example.com infra/deploy-playbook.yaml` (Omits the comma, causing Ansible to look for a file named "staging.example.com").

- **Ansible Task Definition**
  - [DO]: 
    ```yaml
    tasks:
      - name: Ping to make sure we can talk to our server
        ansible.builtin.ping:
    ```
  - [DON'T]: 
    ```yaml
    tasks:
      - name: Ping server
        ansible.builtin.shell: ping -c 1 localhost
    ```
    (Avoids procedural shell commands in favor of declarative built-in modules).

- **Debugging Connection Failures**
  - [DO]: Run `ssh -v nonrootuser@domain.com`, analyze the output for rejected keys, and if it fails, test `ssh -v root@domain.com` to isolate the user configuration.
  - [DON'T]: Immediately destroy the server or wildly change firewall rules when a basic `ssh` command hangs without investigating the verbose output.

- **Windows Infrastructure Execution**
  - [DO]: Open a WSL terminal, create `python -m venv .venv-wsl`, activate it, and run `pip install ansible`.
  - [DON'T]: Attempt to run `pip install ansible` or `ansible-playbook` natively in Windows Command Prompt or PowerShell.