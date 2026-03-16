# @Domain
These rules apply when the AI is tasked with initializing a new Django project, setting up the first Selenium Functional Test (FT), and configuring the initial Git repository environment. Activation triggers include requests to "start a Django project," "write a first functional test," "setup Selenium for Django," or "initialize Git for Django."

# @Vocabulary
- **Testing Goat**: The guiding mindset of Test-Driven Development (TDD). It dictates a strict, single-minded rule: "Test first, test first!"
- **Functional Test (FT)**: A test that drives a real web browser (e.g., using Selenium) to see how the application functions from the user's point of view.
- **Expected Failure**: A test failure that occurs exactly as predicted because the underlying application code or setup does not yet exist. This is a positive milestone in TDD.
- **Working Directory**: The root project folder that contains the `manage.py` file. All terminal commands and relative paths must originate from here.
- **Atomic Steps**: Taking one small, verifiable step at a time (like a goat on a steep incline) rather than writing large blocks of untested code.

# @Objectives
- Enforce a rigorous "Test-First" methodology: the AI MUST write a test and observe it fail *before* writing or generating any application code or framework boilerplate.
- Validate the local environment and framework installation using a Selenium Functional Test.
- Generate a clean, flat Django project structure without unnecessary nested directories.
- Establish a secure and clean version control foundation by initializing Git and strictly configuring a `.gitignore` file before the first commit.

# @Guidelines
- **Test First Mandate**: The AI MUST NEVER generate Django application code, models, or views without first establishing a failing Functional Test. 
- **Start with Selenium**: The first file created MUST be `functional_tests.py` in the project root, utilizing `selenium.webdriver.Firefox()`.
- **Expected Failure Verification**: The AI MUST prompt the user to run the Functional Test to observe the expected `WebDriverException` (Unable to connect) before instructing the user to start the Django server.
- **Flat Project Initialization**: When running `django-admin startproject`, the AI MUST append a trailing dot (`.`) to the command to prevent nested project folders.
- **Working Directory Integrity**: The AI MUST ensure all subsequent file creations, path references, and terminal commands are executed relative to the directory containing `manage.py`.
- **Ignore Initial Migration Warnings**: When starting the Django development server for the first time, the AI MUST inform the user that warnings regarding "unapplied migrations" are safe to ignore at this stage.
- **Strict Version Control Hygiene**: Before performing the initial Git commit, the AI MUST generate a `.gitignore` file.
- **Excluded Files**: The `.gitignore` MUST explicitly exclude `db.sqlite3`, the virtual environment directory (e.g., `.venv`), `__pycache__/`, and `*.pyc` files.
- **Staging Verification**: The AI MUST instruct the user or use tools to check `git status` to ensure `__pycache__` or `.pyc` files are not staged. If they are, the AI MUST explicitly remove them using `git rm -r --cached`.

# @Workflow
1. **Write the Initial Functional Test**: Create `functional_tests.py` at the project root to open a browser, navigate to `http://localhost:8000`, assert the presence of "Congratulations!" (Django's default install success text) in the title, and print "OK".
2. **Execute and Fail**: Run `python functional_tests.py`. Acknowledge the expected failure (connection refused) because the server is not yet running.
3. **Initialize Django**: Execute `django-admin startproject <project_name> .` (strictly enforcing the trailing `.`).
4. **Start the Development Server**: Execute `python manage.py runserver` in a separate terminal process.
5. **Verify the Test Passes**: Execute `python functional_tests.py` again. It must pass without `AssertionError` and output "OK".
6. **Initialize Git**: Run `git init .`. Optionally set the default branch to `main`.
7. **Configure Git Ignore**: Create `.gitignore` and append `db.sqlite3`, `.venv`, `__pycache__`, and `*.pyc`.
8. **Stage and Commit**: Stage the files (`git add .`), verify the status (`git status`), remove any cached `.pyc` files if accidentally staged, and create the initial commit.

# @Examples (Do's and Don'ts)

**Project Initialization**
- [DO]: `django-admin startproject superlists .` (Includes the trailing dot to maintain a flat structure alongside `manage.py`).
- [DON'T]: `django-admin startproject superlists` (Creates a nested `superlists/superlists` directory structure, which violates the working directory standard).

**Writing the First Functional Test**
- [DO]:
  ```python
  from selenium import webdriver

  browser = webdriver.Firefox()
  browser.get("http://localhost:8000")

  assert "Congratulations!" in browser.title
  print("OK")
  ```
- [DON'T]: Jump straight to writing `views.py` or `models.py`. The FT MUST be written and executed first.

**Configuring Version Control (.gitignore)**
- [DO]: 
  ```bash
  echo "db.sqlite3" >> .gitignore
  echo ".venv" >> .gitignore
  echo "__pycache__" >> .gitignore
  echo "*.pyc" >> .gitignore
  git add .gitignore
  ```
- [DON'T]: Run `git add .` and `git commit` immediately after project creation without ignoring the local database, virtual environment, and compiled Python files.

**Handling Accidental Staging of Compiled Files**
- [DO]: 
  ```bash
  git rm -r --cached superlists/__pycache__
  ```
- [DON'T]: Leave `.pyc` files in the Git staging area or commit them to the repository.