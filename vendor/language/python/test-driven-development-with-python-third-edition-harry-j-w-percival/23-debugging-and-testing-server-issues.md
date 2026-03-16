# @Domain

These rules MUST be triggered when the user requests assistance with or the AI encounters tasks involving:
- Debugging Django applications deployed to Docker containers, staging, or production environments.
- Resolving HTTP 500 Server Errors in environments where `DEBUG=False`.
- Adapting Functional Tests (FTs) to run against remote or persistent databases instead of local in-memory test databases.
- Implementing test fixtures for remote environments (e.g., pre-authenticated sessions).
- Passing environment variables and secrets securely to Docker or Ansible.
- Cleaning up or resetting databases after remote functional test runs.

# @Vocabulary

- **Host-Inherited Environment Variable**: The practice of passing an environment variable into a Docker container by using the `-e VAR_NAME` flag without specifying a value, causing Docker to inherit the value from the host's active shell.
- **Console Logging**: A Django logging configuration using `logging.StreamHandler` that forces tracebacks to standard output, allowing them to be captured by `docker logs` when `DEBUG=False`.
- **Remote Fixture**: Test data injected into a real, persistent database (inside Docker or on a server) using a custom Django Management Command, bypassing the standard local-only test database limitations.
- **Early Return (in FTs)**: The practice of halting a functional test midway through (`if self.test_server: return`) to bypass assertions that rely on local-only framework state, such as `django.core.mail.outbox`.
- **Remote Command Execution Wrapper**: A Python `subprocess` script used within tests to dynamically dispatch commands to a target environment using either `docker exec` (for local containers) or `ssh user@host docker exec` (for remote servers).
- **Database Flush**: The process of wiping a remote test database clean between test runs using `manage.py flush --noinput` to ensure test isolation.

# @Objectives

- Confidently reproduce server and CI issues locally using mapped Docker containers.
- Guarantee that tracebacks and application errors are visible in containerized environments.
- Execute end-to-end Functional Tests against real databases without relying on in-memory mocks or local Django state.
- Automate the setup and teardown of test data in remote environments securely and deterministically.
- Strictly safeguard production environments against destructive test cleanup operations.

# @Guidelines

### Debugging and Logging
- The AI MUST ensure Django's `LOGGING` dictionary is configured to use a `StreamHandler` for the `console` when `DEBUG=False`. Tracebacks MUST NOT be swallowed; they must be accessible via `docker logs <container_name>`.
- The AI MUST reproduce staging/production bugs locally by building and running the Docker container on the host machine before attempting blind fixes on the server.
- The AI MUST use `sqlite3 <database_file>` (or the equivalent database shell) to manually inspect database states (e.g., `select * from django_session;`) when debugging remote fixture or state issues.

### Secrets and Environment Variables
- The AI MUST pass secret environment variables to local Docker runs by exporting them in the host shell and passing them using the `-e VAR_NAME` flag (without a value assignment) to prevent secrets from being hardcoded in commands or scripts.
- The AI MUST utilize Ansible's `lookup('env', 'VAR_NAME')` function in playbooks as a stateless alternative for injecting secrets into server deployments, avoiding the need to persist secret files on the remote disk.

### Remote Testing and Fixtures
- The AI MUST NOT use `django.core.mail.outbox` to verify email delivery when running tests against a remote server or Docker container. The AI MUST implement an Early Return in the FT (`if self.test_server: return`) immediately prior to the outbox assertions.
- The AI MUST NOT attempt to use Django's `SessionStore` or ORM to create fixtures directly from the FT file when testing against a remote server.
- The AI MUST encapsulate remote fixture creation logic (e.g., bypassing login) into custom Django Management Commands (e.g., `manage.py create_session`).
- The AI MUST execute these remote management commands from the FT suite using Python's `subprocess.run`. 
- The AI MUST dynamically route the subprocess execution based on the target host: using `docker exec` for local containers, and `ssh <user>@<host> docker exec` for staging servers.
- The AI MUST automatically acquire the local Docker container ID for execution wrappers using `docker ps --filter=ancestor=<image_name> -q`.

### Test Cleanup and Production Safeguards
- The AI MUST guarantee test isolation in remote databases by explicitly triggering `manage.py flush --noinput` via the Remote Command Execution Wrapper in the `setUp` or `tearDown` phase of the FT.
- The AI MUST NEVER execute a database `flush` command against a production environment. 
- The AI MUST NOT include test-specific apps (containing fixture management commands) in the `INSTALLED_APPS` setting of a production environment.

# @Workflow

**When tasked with debugging a server issue or adapting tests for remote execution, the AI MUST follow this algorithmic process:**

1. **Local Reproduction via Docker**:
   - Rebuild the Docker image.
   - Run the container locally, mounting the database and passing required environment variables using `-e VAR_NAME`.
   - Run the Functional Test against the local container to verify the failure reproduces.
2. **Log Inspection**:
   - Ensure Django `LOGGING` is routed to the console.
   - Run `docker logs <container>` to identify the exact Python traceback causing the 500 error.
3. **Bypass Local-Only State**:
   - Identify any assertions in the FT relying on local memory (e.g., `mail.outbox`).
   - Insert an `if self.test_server: return` statement before these assertions.
4. **Implement Remote Fixtures (If necessary)**:
   - Create a Django Management Command (e.g., `management/commands/create_session.py`) that performs the necessary ORM operations.
   - Add the app containing this command to `INSTALLED_APPS` (excluding production).
5. **Construct the Remote Execution Wrapper**:
   - Write a helper script using `subprocess.run`.
   - Implement conditional routing: if the host contains "localhost", execute `['docker', 'exec', container_id, ...]`. If remote, execute `['ssh', 'user@host', 'docker', 'exec', container_name, ...]`.
6. **Enforce Remote Teardown**:
   - Use the Remote Execution Wrapper to dispatch `/venv/bin/python /src/manage.py flush --noinput` during the test runner's `setUp` phase to ensure a clean remote database.

# @Examples (Do's and Don'ts)

### Console Logging in Production
**[DO]** Configure `settings.py` to ensure tracebacks are caught by Docker:
```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "root": {"handlers": ["console"], "level": "INFO"},
    },
}
```
**[DON'T]** Leave logging unconfigured when `DEBUG=False`, which causes 500 errors to fail silently without terminal output.

### Passing Secrets to Docker
**[DO]** Rely on host-inherited variables:
```bash
export EMAIL_PASSWORD="supersecretpassword"
docker run -e EMAIL_PASSWORD -p 8888:8888 my_image
```
**[DON'T]** Hardcode secrets in the command line invocation:
```bash
docker run -e EMAIL_PASSWORD="supersecretpassword" -p 8888:8888 my_image
```

### Passing Secrets via Ansible
**[DO]** Look up variables from the local environment running Ansible:
```yaml
env:
  EMAIL_PASSWORD: "{{ lookup('env', 'EMAIL_PASSWORD') }}"
```
**[DON'T]** Hardcode the secret in the playbook YAML:
```yaml
env:
  EMAIL_PASSWORD: "supersecretpassword"
```

### Testing Email in Remote Environments
**[DO]** Bail out early before checking in-memory outboxes:
```python
self.wait_for(lambda: self.assertIn("Check your email", self.browser.find_element(By.CSS_SELECTOR, "body").text))

if self.test_server:
    return # Testing real email sending from the server is not worth it.

email = mail.outbox.pop()
```
**[DON'T]** Attempt to call `mail.outbox.pop()` when testing against Docker or Staging, as it will raise an `IndexError`.

### Creating Remote Fixtures
**[DO]** Create a Django management command to wrap fixture creation:
```python
# management/commands/create_session.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email")

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options["email"])
        self.stdout.write(session_key)
```
**[DON'T]** Attempt to import `SessionStore` and create ORM objects directly inside the Functional Test file when the FT is pointed at a remote server.

### Executing Commands Remotely
**[DO]** Route command execution intelligently based on the target host using `subprocess`:
```python
def _exec_in_container_on_server(host, commands):
    return subprocess.run(
        ["ssh", f"user@{host}", "docker", "exec", "superlists"] + commands,
        stdout=subprocess.PIPE,
        check=True
    )
```
**[DON'T]** Assume `subprocess.run(['python', 'manage.py', ...])` will affect the Docker database.