# @Domain

These rules MUST be triggered whenever the AI is tasked with preparing a Django web application for production deployment, containerizing an application with Docker for production, managing environment variables and secrets, configuring static files for production, or transitioning an application from a local development server (like `runserver`) to a production-grade server.

# @Vocabulary

- **Gunicorn**: A Python WSGI HTTP Server for UNIX, used in production environments to handle concurrent requests, replacing Django's built-in `runserver`.
- **WSGI (Web Server Gateway Interface)**: The standard interface for communication between a web server and a Python web application.
- **WhiteNoise**: A Python library designed to allow web apps to serve their own static files directly, streamlining production deployments.
- **requirements.txt**: A file used to explicitly declare top-level production dependencies for the application.
- **Transitive Dependencies**: Dependencies of dependencies (e.g., `asgiref` is a dependency of `django`). 
- **12-Factor App Config**: A methodology that mandates storing configuration that varies between environments (dev, staging, prod) in environment variables.
- **ALLOWED_HOSTS**: A Django security setting required when `DEBUG=False` to prevent HTTP Host header attacks.
- **collectstatic**: A Django management command that gathers all static files into a single directory (`STATIC_ROOT`) for production serving.
- **Nonroot User**: An unprivileged user created inside a Docker container to prevent the application from running as `root`, improving security.
- **UID (User ID)**: An integer used in Linux to map file permissions across the host and the container.
- **Console StreamHandler**: A logging configuration that outputs tracebacks and logs to standard output, allowing Docker to capture and display them.
- **check --deploy**: A Django management command used to self-check the application for outstanding production security issues.

# @Objectives

- **Achieve Production-Readiness Incrementally**: Apply the red/green/refactor cycle to infrastructure changes, checking that functional tests (FTs) pass after every configuration modification.
- **Ensure Reproducibility**: Use Docker and `requirements.txt` to replicate the production environment locally.
- **Enhance Security**: Never run production code with `DEBUG=True`, never hardcode secrets, never run containers as `root`, and strictly validate `ALLOWED_HOSTS`.
- **Ensure Observability**: Configure Django's logging to output errors to standard output when `DEBUG=False` so container logs are visible.
- **Isolate Environments**: Maintain strict separation between development dependencies (e.g., Selenium) and production dependencies.

# @Guidelines

- **Production Server Replacement**: 
  - The AI MUST NOT use Django's `runserver` in a production Dockerfile.
  - The AI MUST use a production-ready WSGI server like `Gunicorn`.
- **Static File Serving**:
  - The AI MUST integrate `WhiteNoise` into `MIDDLEWARE` to serve static files in production.
  - The AI MUST invoke `collectstatic` inside the Dockerfile when building production images.
- **Dependency Management**:
  - The AI MUST extract top-level dependencies into a `requirements.txt` file (e.g., `django`, `gunicorn`, `whitenoise`).
  - The AI MUST NOT include development or testing dependencies (e.g., `selenium`) in the production `requirements.txt` file.
- **Environment Variables and Secrets**:
  - The AI MUST extract settings that vary by environment (`DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, Database paths) into environment variables.
  - The AI MUST implement "fail hard" logic for secrets. If `DEBUG=False`, the application MUST raise a `KeyError` if `SECRET_KEY` is not provided in the environment. Do not silently fall back to insecure defaults in production.
- **Security Settings**:
  - The AI MUST configure `ALLOWED_HOSTS` to accept domains via environment variables when `DEBUG=False`.
- **Docker Privilege Restrictions**:
  - The AI MUST configure Dockerfiles to run the application as an unprivileged, nonroot user using the `RUN adduser` and `USER` directives.
  - When utilizing file-based databases like SQLite via Docker mounts, the AI MUST ensure the host file's permissions match the exact UID of the container's nonroot user.
- **Logging Configuration**:
  - The AI MUST configure Django's `LOGGING` dictionary to use a `StreamHandler` outputting to the console. Without this, 500 errors will not produce tracebacks in Docker logs when `DEBUG=False`.
- **Verification**:
  - The AI MUST verify production readiness by executing `python manage.py check --deploy`.

# @Workflow

When instructed to make a Django application production-ready, the AI MUST follow this exact incremental sequence:

1. **Replace the Web Server**:
   - Add `gunicorn` to dependencies.
   - Update the Dockerfile `CMD` to execute `gunicorn` bound to the correct port (`0.0.0.0:PORT`) and pointing to the `wsgi:application`.
2. **Configure Static Files**:
   - Add `whitenoise` to dependencies.
   - Insert `whitenoise.middleware.WhiteNoiseMiddleware` directly after `SecurityMiddleware` in `settings.py`.
3. **Lock Dependencies**:
   - Create a clean `requirements.txt` containing only production requirements.
   - Update the Dockerfile to `COPY requirements.txt` and `RUN pip install -r requirements.txt`.
4. **Implement Environment Variable Logic**:
   - Modify `settings.py` to check for a specific environment variable (e.g., `DJANGO_DEBUG_FALSE`).
   - If present, set `DEBUG = False`, read `SECRET_KEY` from the environment, and read `ALLOWED_HOSTS` from the environment.
   - If absent, default to `DEBUG = True` and insecure dev settings.
   - Ensure the DB path is also configurable via environment variables.
5. **Add collectstatic**:
   - Add `RUN python manage.py collectstatic` to the Dockerfile (ensure the `DJANGO_DEBUG_FALSE` env var is set before this run so it behaves correctly).
6. **Implement Nonroot User**:
   - Modify the Dockerfile to create a nonroot user with a specific UID (e.g., `1234`).
   - Use the `USER` directive to switch contexts.
   - Adjust host machine file creation to `chown` the mounted files (e.g., `db.sqlite3`) to the matching UID.
7. **Configure Logging**:
   - Append a `LOGGING` configuration dictionary to `settings.py` that routes `INFO` and higher logs to `console`.
8. **Final Verification**:
   - Build the container, run it locally with mapped ports and `-e` flags for variables, run functional tests to ensure nothing broke, and run `check --deploy`.

# @Examples (Do's and Don'ts)

### Environment Variable Configuration
**[DO]** Implement "fail hard" logic for secrets to prevent accidental secure exposure.
```python
import os

if "DJANGO_DEBUG_FALSE" in os.environ:
    DEBUG = False
    # Fails hard with KeyError if missing, which is highly desirable in prod
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
    ALLOWED_HOSTS = [os.environ["DJANGO_ALLOWED_HOST"]]
else:
    DEBUG = True
    SECRET_KEY = "insecure-key-for-dev"
    ALLOWED_HOSTS = []
```

**[DON'T]** Use `.get()` with insecure defaults in production.
```python
# ANTI-PATTERN: Fails silently and runs insecurely in production
DEBUG = os.environ.get("DEBUG", False)
SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-key-for-dev")
```

### Dockerfile Production Configuration
**[DO]** Use requirements files, collectstatic, unprivileged users, and Gunicorn.
```dockerfile
FROM python:3.14-slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY src /src
WORKDIR /src

RUN python manage.py collectstatic --noinput

# Create and switch to nonroot user
RUN adduser --uid 1234 nonroot
USER nonroot

# Run production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:8888", "superlists.wsgi:application"]
```

**[DON'T]** Run as root, use `runserver`, or install test dependencies in the production image.
```dockerfile
# ANTI-PATTERN
FROM python:3.14-slim
COPY . /src
WORKDIR /src
RUN pip install django selenium
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Logging Configuration
**[DO]** Explicitly configure console logging so Docker can capture stdout tracebacks when DEBUG=False.
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

**[DON'T]** Leave logging unconfigured when transitioning to `DEBUG=False`, which will result in silent 500 errors inside containers.

### Dependency Management
**[DO]** Maintain a minimal `requirements.txt` for production.
```text
django==5.2.3
gunicorn==23.0.0
whitenoise==6.11.0
```

**[DON'T]** Blindly pipe `pip freeze > requirements.txt` without stripping test tools like `selenium` or irrelevant local system packages.