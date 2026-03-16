@Domain
Trigger these rules when initiating a new Django project, setting up the initial testing infrastructure, writing the first Selenium-based Functional Tests (FTs), establishing a new Git repository for a Python web project, or when the user requests to follow strict Test-Driven Development (TDD) from scratch.

@Vocabulary
- **Testing Goat**: The personification of strict TDD discipline. Represents the voice that dictates: "Test first, test first!" and enforces taking one minimal step at a time.
- **Functional Test (FT)**: A test that uses a browser automation tool (like Selenium) to drive a real web browser, testing the application from the user's point of view. 
- **Expected Failure**: A test failure that occurs exactly as predicted (e.g., an `AssertionError` or `WebDriverException` because the server is not running or code is unwritten). This validates that the test is checking the right conditions.
- **Working Directory**: The root folder of the project containing `manage.py`. All relative paths and terminal commands must be executed from this location.
- **Trailing Dot (`.`)**: A critical syntax component when running `django-admin startproject <name> .` to ensure the project is generated in the current directory rather than creating a redundant nested directory.

@Objectives
- Enforce the absolute foundational rule of TDD: Write a failing test before writing any application code or configuration.
- Validate infrastructure (Django installation and local development server) via a Functional Test before proceeding to application logic.
- Ensure the Django project is instantiated cleanly without redundant nested folders.
- Establish strict version control hygiene from the very first commit, ensuring ephemeral and local files are ignored.

@Guidelines
- **The Testing Goat Rule**: When asked to start a project or add a feature, the AI MUST NOT write Django configuration, `manage.py` commands, or application code first. The AI MUST write a test, run it, and verify it fails before building the app.
- **Minimal Steps**: The AI MUST proceed in nice, small, incremental steps, refusing to jump ahead to complex configurations.
- **Functional Test Implementation**: The AI MUST use Selenium WebDriver (specifically Firefox) to write the initial FT, testing against `http://localhost:8000`.
- **Project Instantiation**: When creating the Django project, the AI MUST append a space and a period (` .`) to the `django-admin startproject` command.
- **Working Directory Discipline**: The AI MUST always assume the working directory is the folder containing `manage.py` and run all shell commands from there.
- **Git Initialization**: The AI MUST initialize version control (`git init .`) immediately after the first test passes.
- **Default Branch**: The AI MUST configure the initial Git branch name to `main`.
- **Version Control Hygiene**: Before the first commit, the AI MUST create a `.gitignore` file and explicitly exclude databases (`db.sqlite3`), virtual environments (`.venv`), and compiled Python files (`__pycache__`, `*.pyc`).
- **Cache Removal**: If `__pycache__` files are accidentally staged, the AI MUST remove them using `git rm -r --cached` before committing.

@Workflow
1. **Write the FT First**: Create a file named `functional_tests.py` in the desired project folder. Instantiate a Selenium Firefox webdriver, navigate to `http://localhost:8000`, and assert that the expected default Django text ("Congratulations!") is in the browser title.
2. **Execute and Fail**: Run `python functional_tests.py`. Observe and acknowledge the expected failure (e.g., `WebDriverException` indicating unable to connect).
3. **Initialize Django**: Run `django-admin startproject <project_name> .` to create the project files (`manage.py` and the inner project folder).
4. **Start the Server**: Start the Django development server using `python manage.py runserver` in a primary terminal.
5. **Verify the Pass**: In a separate terminal, re-run `python functional_tests.py`. Acknowledge the passing test (silent completion without `AssertionError`).
6. **Initialize Git**: Run `git init .` to start the repository.
7. **Configure Git**: Run `git config --global init.defaultBranch main` (or rename the branch to `main`).
8. **Create .gitignore**: Append `db.sqlite3`, `.venv`, `__pycache__`, and `*.pyc` to a new `.gitignore` file.
9. **Stage and Check**: Run `git add .` followed by `git status` to ensure only correct source files (e.g., `manage.py`, `functional_tests.py`, `.gitignore`, `urls.py`, `settings.py`) are staged.
10. **First Commit**: Commit the code with a descriptive message (e.g., `git commit -m "First commit: functional test and basic Django setup"`).

@Examples (Do's and Don'ts)

**TDD Execution Order**
- [DO]: Create `functional_tests.py`, run it, watch it fail, and *then* run `django-admin startproject superlists .`
- [DON'T]: Run `django-admin startproject superlists` before writing a test.

**Django Project Creation**
- [DO]: `django-admin startproject superlists .` (Includes the trailing dot to maintain a flat structure).
- [DON'T]: `django-admin startproject superlists` (Omits the trailing dot, resulting in confusing `superlists/superlists` nested directories).

**Git Ignored Files**
- [DO]: Add `.venv` and `__pycache__` to `.gitignore` and verify with `git status` before committing.
- [DON'T]: Blindly run `git add .` and `git commit` without checking if `db.sqlite3` or compiled `.pyc` files are included in the initial commit.

**Functional Test Assertion (Initial)**
- [DO]: 
```python
from selenium import webdriver
browser = webdriver.Firefox()
browser.get("http://localhost:8000")
assert "Congratulations!" in browser.title
print("OK")
```
- [DON'T]: Write complex `unittest` classes or assertions before validating the basic server connection with a raw `assert` statement.