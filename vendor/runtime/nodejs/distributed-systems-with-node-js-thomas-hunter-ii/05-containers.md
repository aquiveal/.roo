# @Domain
These rules MUST be activated when the user requests assistance with containerizing a Node.js application, writing or modifying `Dockerfile`s, configuring `docker-compose.yml` files, optimizing Docker image sizes, deploying applications via Docker Registries, or designing container orchestration for local development or production.

# @Vocabulary
- **Container**: An isolated environment that encapsulates an application, its private filesystem, shared libraries, isolated PIDs, and ports, while sharing the host operating system's kernel.
- **Virtual Machine (VM)**: An emulation of computer hardware that runs an entire redundant guest operating system (OS).
- **Docker Image**: An immutable representation of a filesystem used to instantiate containers. It is composed of stacked layers.
- **Dockerfile**: A declarative text file describing the directives (steps) required to build a Docker image.
- **Layer**: A partial filesystem representation created by a single directive in a Dockerfile. Layers are cached by their hash.
- **Alpine**: A highly stripped-down, minimal Linux distribution used as a base image to reduce container storage size and attack surface.
- **Multi-stage Build**: A Dockerfile pattern using multiple `FROM` directives to separate build-time dependencies (like compilers or full npm installs) from the final production runtime image.
- **.dockerignore**: A file dictating which host files and directories MUST NOT be copied into the Docker image.
- **Docker Compose**: A tool and YAML specification (`docker-compose.yml`) used to define, configure, and orchestrate relationships between multiple dependent containers.
- **Docker Registry**: A centralized service (public like Docker Hub, or self-hosted/internal) for storing, pushing, and pulling Docker images.
- **Sidecar**: An external process running alongside the main application within a container (or pod) that performs supporting duties (e.g., proxying, health-checking).

# @Objectives
- The AI MUST optimize Docker images for size, security, and build speed by utilizing multi-stage builds and minimal base images (Alpine).
- The AI MUST strictly enforce layer caching by ordering Dockerfile directives from least-frequently-changed to most-frequently-changed.
- The AI MUST prevent host-environment contamination by ignoring local dependencies (`node_modules`) and deterministic package installation.
- The AI MUST orchestrate multi-container setups using Docker Compose, explicitly defining dependencies, environment variables, and network ports.
- The AI MUST ensure containers are designed to be ephemeral, stateless, and portable.

# @Guidelines

## Base Images and Sizing
- The AI MUST prefer `alpine` base images (e.g., `node:14-alpine`) for Node.js services to minimize storage and attack surface. `debian` or `ubuntu` bases MUST ONLY be used if the application requires complex shared libraries (e.g., C++ binaries) that are incompatible with Alpine's `musl`.
- The AI MUST clean up package manager caches within the same `RUN` directive layer to prevent bloat (e.g., use `apk add --no-cache` or `apk del`).
- The AI MUST group related shell commands using `&&` and line breaks (`\`) within a single `RUN` directive to minimize the total number of layers.

## Layer Caching and Ordering
- The AI MUST place directives that change infrequently (e.g., OS package installs) at the top of the Dockerfile.
- The AI MUST separate the copying of package files from application code. `COPY package*.json ./` MUST precede the installation directive.
- The AI MUST execute `COPY . .` (application source code) AFTER the dependency installation directive. Application code changes frequently; placing it after dependency installation ensures the dependency layer remains cached.

## Deterministic Builds and Isolation
- The AI MUST create a `.dockerignore` file for every containerized Node.js project.
- The `.dockerignore` file MUST contain `node_modules`, `npm-debug.log`, and `Dockerfile` at a minimum. Host machine native modules MUST NEVER be copied into the Linux container environment.
- The AI MUST use `npm ci --only=production` (or `yarn install --production`) instead of `npm install` to ensure deterministic, clean dependency trees.

## Multi-Stage Builds
- The AI MUST use a multi-stage Dockerfile for production Node.js applications.
- **Stage 1 (deps)**: MUST use a fully featured Node.js base image to run `npm ci`.
- **Stage 2 (release)**: MUST use a minimal base image (e.g., plain `alpine` or `node:alpine`), copy `node_modules` exclusively from the `deps` stage, and configure the runtime environment.

## Container Networking and Configuration
- The AI MUST set the Node.js application to listen on `0.0.0.0` inside the container using an environment variable (e.g., `ENV HOST 0.0.0.0`). Listening on `127.0.0.1` inside a container makes the service unreachable to the host or other containers.
- The AI MUST document intended exposed ports using the `EXPOSE <port>` directive.
- The AI MUST define the default runtime execution via the `CMD` directive (e.g., `CMD [ "node", "server.js" ]`).

## Docker Compose Orchestration
- The AI MUST use Docker Compose (`docker-compose.yml`) when an application requires backing services (e.g., Redis, Zipkin, Postgres) or downstream APIs.
- The AI MUST explicitly map host-to-container ports using the `ports` key (`"HOST_PORT:CONTAINER_PORT"`).
- The AI MUST explicitly define startup order and service dependencies using the `depends_on` array.
- The AI MUST pass service addresses using the `environment` array, utilizing the exact service name defined in the YAML file as the hostname (e.g., `TARGET: recipe-api:4000`).

## Image Tagging and Registries
- The AI MUST assign explicit version tags (e.g., `repository/name:v1.0.0`) when building or pushing images. The AI MUST NOT rely solely on the implicit `latest` tag, as it makes rollback and version tracking difficult.

# @Workflow
When tasked with containerizing a Node.js project, the AI MUST strictly follow this algorithm:

1.  **Isolation Setup**: Create a `.dockerignore` file to exclude `node_modules`, `Dockerfile`, and local logs/temp files.
2.  **Define `deps` Stage**:
    *   Start the Dockerfile with `FROM node:<version>-alpine AS deps`.
    *   Set `WORKDIR /srv` (or equivalent).
    *   `COPY package*.json ./`.
    *   `RUN npm ci --only=production`.
3.  **Define `release` Stage**:
    *   Start the second stage with `FROM alpine:<version> AS release` (or a slim node base).
    *   If applicable, install required runtime OS libraries using `apk add --no-cache`.
    *   Set `WORKDIR /srv`.
    *   Copy dependencies from stage 1: `COPY --from=deps /srv/node_modules ./node_modules`.
    *   Copy application source: `COPY . .`.
4.  **Configure Runtime**:
    *   Set required networking ENV vars: `ENV HOST 0.0.0.0` and `ENV PORT <port>`.
    *   Add `EXPOSE <port>`.
    *   Define process entrypoint: `CMD [ "node", "app.js" ]`.
5.  **Orchestration (If multi-service)**:
    *   Create a `docker-compose.yml` file.
    *   Define each service under the `services:` block.
    *   Use `build: context: .` for local builds or `image: <name>` for pulled images.
    *   Configure `ports`, `environment`, and `depends_on` correctly.

# @Examples (Do's and Don'ts)

## [DO] Proper Multi-Stage Dockerfile with Optimized Caching
```dockerfile
# Stage 1: Dependencies
FROM node:14.8.0-alpine AS deps
WORKDIR /srv
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Release
FROM node:14.8.0-alpine AS release
WORKDIR /srv
# Copy compiled/installed modules from deps stage
COPY --from=deps /srv/node_modules ./node_modules
# Copy application code AFTER dependencies to preserve layer cache
COPY . .
# Bind to 0.0.0.0 so external traffic can reach the container
ENV HOST 0.0.0.0
ENV PORT 1337
EXPOSE 1337
CMD [ "node", "server.js" ]
```

## [DON'T] Unoptimized, Single-Stage Dockerfile (Anti-Pattern)
```dockerfile
FROM ubuntu:latest
WORKDIR /app
# Anti-pattern: Copying everything at once invalidates the npm install cache on ANY code change
COPY . .
# Anti-pattern: Using standard npm install instead of ci
RUN npm install
# Anti-pattern: Defaulting to localhost means the container is inaccessible
ENV HOST 127.0.0.1
CMD [ "node", "server.js" ]
```

## [DO] Proper .dockerignore File
```text
node_modules
npm-debug.log
Dockerfile
.git
.env
```

## [DON'T] Missing .dockerignore (Anti-Pattern)
Failing to provide a `.dockerignore` file copies the host's `node_modules` into the container, overwriting container-compiled binaries and transferring potentially incompatible architectures (e.g., macOS native modules to Linux).

## [DO] Well-Structured Docker Compose Orchestration
```yaml
version: "3.7"
services:
  recipe-api:
    build:
      context: ./recipe-api
      dockerfile: Dockerfile
    ports:
      - "127.0.0.1:4000:4000"
    environment:
      HOST: 0.0.0.0

  web-api:
    build:
      context: ./web-api
      dockerfile: Dockerfile
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      # DO: Use the docker-compose service name as the hostname
      TARGET: recipe-api:4000
      HOST: 0.0.0.0
    depends_on:
      - recipe-api
```

## [DON'T] Brittle OS Package Management in Dockerfiles
```dockerfile
# Anti-pattern: Leaves apt caches in the image layer, bloating the container size
RUN apt-get update
RUN apt-get install -y curl
```
*Instead, use `apk add --no-cache curl` (for Alpine) or combine `apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*` into a single `RUN` directive.*