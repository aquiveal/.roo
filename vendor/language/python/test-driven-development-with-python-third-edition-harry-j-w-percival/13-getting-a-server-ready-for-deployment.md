# @Domain
Server provisioning, domain name system (DNS) configuration, remote access (SSH) setup, debugging, and initial infrastructure-as-code (IaC) configuration using Ansible. These rules trigger whenever the AI is tasked with preparing a server environment, managing remote connections, configuring domains, or writing initial deployment automation scripts.

# @Vocabulary
*   **Provisioning**: The manual or automated process of setting up a new server, choosing an operating system, securing basic login credentials, and configuring DNS.
*   **Deploying**: The process of getting application code (e.g., Docker images) onto an existing server, starting containers, and configuring database and network interactions.
*   **VPS (Virtual Private Server)**: A virtualized server acting as a dedicated server. The required environment for this system (specifically Ubuntu 22.04 LTS).
*   **PaaS (Platform as a Service)**: A hosted service (like Heroku) that abstracts away server administration. Acknowledged as useful, but explicitly avoided here in favor of manual server administration for learning purposes.
*   **A-record**: A DNS record that points a domain or subdomain directly to an IPv4 address.
*   **AAAA-record**: A DNS record that points a domain or subdomain to an IPv6 address.
*   **TTL (Time To Live)**: A DNS setting dictating how long a record is cached, affecting how quickly DNS propagation occurs globally.
*   **Infrastructure as Code (IaC)**: Managing and provisioning computer data centers through machine-readable definition files rather than physical hardware configuration or interactive configuration tools.
*   **Ansible**: A declarative infrastructure-as-code tool used to automate server deployment.
*   **Playbook**: An Ansible YAML file that defines the desired declarative state of the server.
*   **WSL (Windows Subsystem for Linux)**: A compatibility layer for running Linux binary executables natively on Windows, absolutely required for running Ansible on Windows hosts.
*   **Fail2Ban**: A security utility that scans log files and bans IPs that show malicious signs (e.g., too many password failures), recommended for SSH security.

# @Objectives
*   Strictly separate server provisioning concerns from application deployment concerns.
*   Configure servers using a standardized baseline: Ubuntu 22.04 LTS, public IP, nonroot user with `sudo` privileges, and public/private key authentication.
*   Establish reliable remote management workflows utilizing SSH for manual debugging and Ansible for automated, declarative configuration.
*   Map staging and production environments to distinct domain names via DNS A-records.
*   Enforce a highly disciplined, incremental approach to infrastructure changes to avoid the "Refactoring Cat" trap (flailing and making unrelated changes when things break).

# @Guidelines
*   **Server Baseline**: When assuming or requiring a server environment, the AI MUST target Ubuntu 22.04 (Jammy/LTS).
*   **Authentication Standards**: The AI MUST NEVER rely on password-based SSH authentication. The AI MUST require public/private key authentication and the use of a nonroot user with `sudo` access (e.g., `elspeth`).
*   **DNS Configuration**: When configuring URLs, the AI MUST instruct the user to create an A-record (or AAAA-record for IPv6) at their registrar pointing their domain/subdomain to the server's public IP address. The AI MUST advise utilizing a DNS propagation checker if resolution fails initially.
*   **Ansible over Manual Commands**: Once initial SSH access is confirmed, the AI MUST prefer declarative Ansible playbooks over procedural bash scripts for configuring the server.
*   **Ansible Playbook Structure**: The AI MUST format Ansible playbooks in YAML and store them in a dedicated infrastructure directory (e.g., `infra/deploy-playbook.yaml`).
*   **Ansible Execution Syntax**: When providing `ansible-playbook` commands, the AI MUST use the `--user` flag, the `-vv` flag for verbose debugging, and the `-i` (inventory) flag. 
*   **The Trailing Comma Rule**: CRITICAL: When specifying an inline host for the Ansible `-i` flag, the AI MUST append a trailing comma to the hostname (e.g., `-i staging.domain.com,`). If omitted, Ansible will fail to parse the inventory.
*   **Ansible Dependencies**: The AI MUST ensure both `ansible` and `docker` (the Docker SDK for Python) are installed in the local virtual environment via pip before executing playbooks.
*   **Windows Execution**: If the host operating system is Windows, the AI MUST instruct the user to execute Ansible inside WSL, utilizing a dedicated virtual environment within the WSL file system.
*   **Systematic SSH Debugging**: When SSH fails, the AI MUST follow a rigid diagnostic tree:
    1. Check network connectivity: `ping <domain>` and `ping <IP>`.
    2. Check DNS resolution: `nslookup <domain>`.
    3. Check SSH handshake: `ssh -v <user>@<domain>` to trace key offerings.
    4. Test root fallback: `ssh root@<domain>` to verify if the issue is isolated to the nonroot user's `~/.ssh/authorized_keys` file.
*   **Incremental Infrastructure Changes**: When infrastructure code breaks, the AI MUST NOT suggest random, unrelated changes. The AI MUST instruct the user to stop, revert to the last working state, identify the exact error, and move forward with a single new change.

# @Workflow
1.  **Provisioning Verification**: Confirm the server is running Ubuntu 22.04 LTS, has a public IP, and has a nonroot user with `sudo` access.
2.  **DNS Routing**: Verify that the staging/production domains possess valid A-records pointing to the server's IP address. Wait for TTL propagation if necessary.
3.  **SSH Validation**: Manually test the SSH connection to the server (`ssh user@domain`). If it fails, initiate the Systematic SSH Debugging protocol defined in the Guidelines.
4.  **Local Tooling Setup**: Install deployment dependencies (`pip install ansible docker`) in the local project virtual environment. If on Windows, initialize a WSL session first.
5.  **Playbook Initialization**: Create an `infra/` directory and instantiate an initial YAML playbook (e.g., `deploy-playbook.yaml`).
6.  **Declarative Ping**: Populate the playbook with a basic `ansible.builtin.ping` task targeting `hosts: all`.
7.  **Execution & Verification**: Run the playbook utilizing the strict syntax: `ansible-playbook --user=<user> -i <domain>, infra/deploy-playbook.yaml -vv`. Ensure the "pong" response is successfully received.

# @Examples (Do's and Don'ts)

*   **[DO]** Use a trailing comma when passing an inline hostname to the Ansible inventory flag.
    ```bash
    ansible-playbook --user=elspeth -i staging.ottg.co.uk, infra/deploy-playbook.yaml -vv
    ```

*   **[DON'T]** Omit the trailing comma on the Ansible inventory flag, which will cause a parsing failure.
    ```bash
    # INCORRECT
    ansible-playbook --user=elspeth -i staging.ottg.co.uk infra/deploy-playbook.yaml
    ```

*   **[DO]** Write a minimal, declarative Ansible playbook to test server connectivity.
    ```yaml
    ---
    - hosts: all
      tasks:
        - name: Ping to make sure we can talk to our server
          ansible.builtin.ping:
    ```

*   **[DON'T]** Attempt to run Ansible natively on a Windows command prompt or PowerShell.
    ```bash
    # INCORRECT (On Windows cmd.exe)
    pip install ansible
    ansible-playbook ...
    ```
    *(Instead, the AI MUST explicitly require WSL for Windows users).*

*   **[DO]** Use verbose logging and systematic steps to debug SSH connection issues.
    ```bash
    ping staging.ottg.co.uk
    nslookup staging.ottg.co.uk
    ssh -v elspeth@staging.ottg.co.uk
    ```

*   **[DON'T]** "Flail" or make simultaneous, unrelated configuration changes when an infrastructure connection fails. Revert to a known working state before attempting a new, isolated fix.