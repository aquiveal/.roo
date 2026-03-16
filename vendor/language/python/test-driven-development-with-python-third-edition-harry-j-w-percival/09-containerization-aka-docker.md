@Domain
These rules apply when the AI is tasked with containerizing a Python/Django application using Docker, restructuring an application for production deployment, configuring network port bindings for containers, setting up host-to-container volume mounts (specifically for SQLite databases or stateful data), and modifying functional tests to target remote or containerized servers.

@Vocabulary
- **Virtualization**: Hardware-level simulation of multiple physical computers, running separate operating systems (e.g., VMs).
- **Containerization**: OS-level virtualization sharing a single host kernel, allowing lightweight, fast packaging of source code and system dependencies.
- **Docker Image**: The pre-prepared, stateless root filesystem and instructions (like a Class).
- **Docker Container**: A running instance of a Docker Image.
- **Walrus Operator (`:=`)**: Python 3.8+ assignment expression operator, used here to concisely check and assign environment variables (e.g., `TEST_SERVER`).
- **Port Mapping/Publishing**: Connecting a port inside the Docker container's isolated network to a port on the host machine.
- **Wildcard IP (`0.0.0.0`)**: The IP address required for Django's `runserver` inside a container to expose it to the host network (as opposed to the default `127.0.0.1` loopback).
- **Colima / Podman / nerdctl**: Alternative container runtimes and CLIs that can be used interchangeably with Docker.
- **Bind Mount (`--mount type=bind`)**: Mounting a specific file or directory from the host into the container at runtime, preserving state outside the stateless image.
- **Stateful vs. Stateless**: Databases (like `db.sqlite3`) are stateful and must live outside the image. Docker images must remain stateless.

@Objectives
- Package Python applications, their virtual environments, and system dependencies reproducibly using Docker.
- Adapt functional test suites to seamlessly execute against local development servers, local Docker containers, or remote staging servers.
- Strictly separate stateful data (databases) from stateless infrastructure (Docker images).
- Ensure reliable container networking by properly binding inner processes to wildcard IPs and mapping ports to the host.
- Maintain a clean project structure by isolating application source code from deployment configurations.

@Guidelines
- **Project Structure**: The AI MUST move all application source code (e.g., `manage.py`, Django apps, functional tests) into a dedicated `src/` directory, leaving infrastructure files (`Dockerfile`, `.dockerignore`) in the repository root.
- **Functional Test Routing**: The AI MUST configure functional tests to check for a `TEST_SERVER` environment variable. If present, the test MUST target this server instead of the local test server. The AI SHOULD use the walrus operator (`:=`) for this check (e.g., `if test_server := os.environ.get("TEST_SERVER"):`).
- **Port Selection**: The AI MUST NOT use Django's default port `8080` or `8000` for the containerized server to avoid conflicts with stray local `runserver` instances. The AI SHOULD use an alternative port like `8888`.
- **Base Images**: The AI MUST use lightweight, specific base images (e.g., `FROM python:3.14-slim`).
- **Virtual Environments in Docker**: The AI MUST create a virtualenv inside the container (`RUN python -m venv /venv`).
- **Virtual Environment Activation**: The AI MUST NOT attempt to use `RUN source .venv/bin/activate` in a Dockerfile. The AI MUST activate the virtualenv by prepending its `bin` directory to the system PATH: `ENV PATH="/venv/bin:$PATH"`.
- **Dockerfile CMD Syntax**: The AI MUST use the JSON array syntax for the `CMD` instruction (e.g., `CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]`).
- **Container Networking**: When running Django's `runserver` inside Docker, the AI MUST bind the server to `0.0.0.0` (e.g., `0.0.0.0:8888`). Binding to `127.0.0.1` or omitting the IP will result in "Connection refused" or "Empty reply from server" errors outside the container.
- **Running Containers**: The AI MUST run web server containers with interactive flags (`-it`) so they can be terminated via `Ctrl+C`. The AI MUST map ports using the `-p OUTSIDE:INSIDE` flag (e.g., `-p 8888:8888`).
- **Stateful Data / Databases**: The AI MUST NOT run database migrations (e.g., `RUN python manage.py migrate`) inside the `Dockerfile`. Doing so bakes stateful data into the stateless image, causing data loss upon container rebuilds.
- **Bind Mounts**: The AI MUST mount stateful files (like `db.sqlite3`) at runtime using the `--mount type=bind,source=...,target=...` syntax. The AI MUST NOT use the legacy `-v` syntax, as `--mount` provides stricter validation (failing safely if the source path does not exist).
- **Ignore Files**: The AI MUST add stateful database files (e.g., `src/db.sqlite3`) to both `.gitignore` and `.dockerignore` to prevent them from being committed to version control or copied into the container image during the build context transfer.
- **Debugging Networking**: The AI MUST use `curl -iv <url>` to test HTTP connectivity from the host. If connection fails, the AI MUST use `docker exec -it <container-id> bash` to enter the running container and test connectivity from the inside using `curl`.
- **Stopping Hung Containers**: If a container hangs, the AI MUST instruct the user to find the ID using `docker ps` and terminate it using `docker stop <container-id>` from a separate terminal.

@Workflow
1. **Prepare Source Code**: Create a `src/` directory and move all application code into it.
2. **Adapt Tests**: Modify functional tests to accept a `TEST_SERVER` environment variable, overriding the default local test server URL.
3. **Ignore Stateful Data**: Add database files (e.g., `db.sqlite3`) to `.gitignore` and `.dockerignore`.
4. **Draft Dockerfile**:
   - Define a minimal base image.
   - Create a virtualenv and add it to the system `PATH`.
   - Install dependencies (e.g., Django).
   - `COPY` the `src/` directory into the image and set `WORKDIR`.
   - Set the `CMD` to run the server, ensuring it binds to `0.0.0.0` and a non-default port (e.g., `8888`).
5. **Build Image**: Run `docker build -t <image-name> .`
6. **Prepare Host Database**: Ensure the local database file exists on the host machine before mounting.
7. **Run Container**: Run the container using `docker run -it -p <host-port>:<container-port> --mount type=bind,source="<host-path>",target="<container-path>" <image-name>`.
8. **Verify and Debug**: Run functional tests against the exposed port. If errors occur, use `curl` and `docker exec` to debug container networking and port binding.

@Examples (Do's and Don'ts)

- **Configuring FTs for Remote/Docker Servers**:
  - [DO]: 
    ```python
    if test_server := os.environ.get("TEST_SERVER"):
        self.live_server_url = "http://" + test_server
    ```
  - [DON'T]: Hardcode URLs or use global state without checking the environment.
    ```python
    self.live_server_url = "http://localhost:8888" # Hardcoded
    ```

- **Activating Virtualenvs in Dockerfiles**:
  - [DO]:
    ```dockerfile
    RUN python -m venv /venv
    ENV PATH="/venv/bin:$PATH"
    RUN pip install "django<6"
    ```
  - [DON'T]:
    ```dockerfile
    RUN python -m venv /venv
    RUN source /venv/bin/activate
    RUN pip install "django<6"
    ```

- **Binding Django runserver in Docker**:
  - [DO]:
    ```dockerfile
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]
    ```
  - [DON'T]: Omitting the IP binds to the container's isolated `127.0.0.1`, breaking external access.
    ```dockerfile
    CMD ["python", "manage.py", "runserver", "8888"]
    ```

- **Handling Database Migrations**:
  - [DO]: Run migrations against the live database from the host or via `docker exec` *after* the container is running with a mounted volume.
  - [DON'T]: Bake the database into the image.
    ```dockerfile
    # Anti-pattern: Bakes state into the stateless image
    RUN python manage.py migrate --noinput
    ```

- **Mounting Volumes at Runtime**:
  - [DO]: Use strict bind mounts.
    ```bash
    docker run -it -p 8888:8888 --mount type=bind,source="$PWD/src/db.sqlite3",target=/src/db.sqlite3 superlists
    ```
  - [DON'T]: Use legacy syntax without strict path checking, or forget to publish ports.
    ```bash
    docker run -v $PWD/src/db.sqlite3:/src/db.sqlite3 superlists
    ```