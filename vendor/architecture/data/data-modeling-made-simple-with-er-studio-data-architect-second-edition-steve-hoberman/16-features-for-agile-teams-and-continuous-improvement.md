# @Domain
These rules MUST be triggered whenever the AI is assisting with or performing tasks related to ER/Studio automation, iterative/agile data modeling, creating or editing macros, writing reusable database procedural logic (triggers, procedures, libraries), running model validations, or managing versions/changes using the ER/Studio Repository.

# @Vocabulary
- **Macro**: A function written in the Sax Basic language (a Visual Basic for Applications derivative) that automates or simplifies complex or repetitive tasks within ER/Studio.
- **Top 5 Macros**: Specific built-in macros highly recommended for efficiency: *Export Meta Data to Excel*, *Definition Editor*, *Notes Editor*, *Get Related Tables*, and *Convert Name Case*.
- **Reusable Procedure Logic**: Code created once and used many times, organized by database platform under the Data Dictionary tab. Includes Triggers, Procedures, and Libraries.
- **Database Trigger**: Customizable procedural code automatically executed in response to data modification operations (INSERT, UPDATE, DELETE) to maintain referential integrity.
- **Reusable Procedure**: A compartmentalized set of code that performs one or more operations (e.g., business logic checks).
- **Library**: Blocks of Sax Basic code used to generate SQL for Reusable Triggers and Reusable Procedures.
- **Change Management Center**: A Repository feature for model check-in/check-out that allows multiple modelers to work concurrently, tracking every change and associating model changes with agile user stories/tasks.
- **Named Release**: A read-only archived snapshot of a diagram managed within the Repository, representing the state of a data model at a specific point in time (e.g., end of an agile sprint).
- **Rollback Diagram**: A repository operation that takes a Named Release and checks it in as the latest version of a diagram.
- **Model Validation**: A wizard containing over 50 checks to improve logical/physical model quality by catching errors like missing definitions, unused domains, identical unique indexes, and circular relationships.

# @Objectives
- Automate tedious, routine modeling tasks and enforce organizational practices using macros.
- Promote code reuse and consistency by centralizing triggers, procedures, and libraries in the Data Dictionary.
- Ensure data models maintain the highest quality standards before deployment by enforcing Model Validation.
- Align data modeling workflows with agile development processes by utilizing Change Management tasks, user stories, and Named Releases.

# @Guidelines
- **Macro Language Constraint**: The AI MUST use the Sax Basic language (compatible with Visual Basic) when generating or editing Macros or Library logic.
- **Macro Utilization**: Before generating custom macro scripts, the AI MUST suggest checking for existing built-in macros, specifically the Top 5 Macros, to avoid reinventing the wheel.
- **Macro Execution Pathing**: When instructing users, the AI MUST direct them to the *Macros tab* at the bottom of the Explorer pane to run, edit, delete, or rename macros.
- **Reusable Logic Placement**: The AI MUST instruct users to create triggers, procedures, and libraries strictly under the *Data Dictionary tab* -> *Reusable Procedural Logic* node, categorized by the target database platform.
- **File Extensions**: The AI MUST specify the `.bas` file extension when importing or exporting Reusable Triggers and Reusable Procedures code.
- **Agile Integration**: When advising on collaborative/agile environments, the AI MUST mandate the use of the *Repository > Change Management Center* to associate data model modifications with specific agile tasks or user stories during check-in/check-out.
- **Version Control**: The AI MUST advise against saving iterative files locally (e.g., `model_v1`, `model_v2`). Instead, it MUST instruct the user to use *Named Releases* via `Repository > Releases` to capture sprint completions.
- **Validation Mandate**: The AI MUST require the execution of the *Compare and Merge Utility* or *Model Validation* before finalizing any model to catch missing definitions, unused domains, identical unique indexes, or circular relationships.
- **Reporting Validation**: The AI MUST suggest exporting the Model Validation results to a comma-delimited file for team review if a high number of errors are detected.

# @Workflow
When guiding a user through agile model improvements and automation in ER/Studio, the AI MUST adhere to the following step-by-step algorithm:

1.  **Automation Assessment**: 
    - Ask the user if they are performing a repetitive task (e.g., changing casing, adding definitions).
    - If yes, instruct them to use the *Macro tab* to run built-in macros (e.g., *Convert Name Case*, *Definition Editor*).
    - If no built-in macro exists, generate a custom Sax Basic script and instruct the user to create it via `Tools > Basic Macro Editor`.
2.  **Logic Centralization**:
    - Identify if the user is writing database triggers or procedures.
    - Instruct the user to open the *Data Dictionary* tab.
    - Guide them to right-click the target database under *Reusable Procedural Logic* and select *New Trigger*, *New Procedure*, or *New Library*.
3.  **Model Validation**:
    - Before check-in, instruct the user to run `Model > Validate Model...`.
    - Tell the user to click `<Select All>` on the Object Selection tab, then `<Run Validation>`.
    - Instruct them to resolve any missing object definitions, unused domains, identical unique indexes, or circular relationships.
4.  **Agile Change Management**:
    - Instruct the user to open `Repository > Change Management Center`.
    - Guide them to associate their current changes with the corresponding agile task/user story during the Check-in process.
5.  **Sprint Finalization (Named Releases)**:
    - If the current task marks the end of an agile sprint, instruct the user to navigate to `Repository > Releases`.
    - Guide them to create a *Named Release* to archive a read-only snapshot of the completed sprint.

# @Examples (Do's and Don'ts)

**Macro Automation**
- [DO]: Write ER/Studio macros using Sax Basic syntax (Visual Basic compatible) to interface with the ER/Studio API.
- [DON'T]: Provide Python, Python-based COM wrappers, or JavaScript scripts when asked to write an ER/Studio macro.

**Handling Iterative Changes**
- [DO]: "To save the state of your model at the end of this sprint, go to `Repository > Releases` and create a Named Release. Be sure to link your changes to your Agile tasks in the Change Management Center."
- [DON'T]: "To version your model for this sprint, go to File > Save As and name it `Publishing_Model_Sprint_4.dm1`."

**Applying Business Logic**
- [DO]: "Navigate to the Data Dictionary tab, expand Reusable Procedural Logic, right-click your database platform, and select 'New Trigger' to ensure this logic is centralized and reusable."
- [DON'T]: "Manually type the trigger SQL into the PreSQL/PostSQL tab of every individual physical table."

**Quality Assurance / Validation**
- [DO]: "Before checking in your model, run `Model > Validate Model...` and review the Output tab to ensure there are no unused domains or missing object definitions. Export the results to a CSV if needed."
- [DON'T]: "Just do a quick visual scan of the diagram to make sure your relationships look correct before checking the model into the repository."

**Handling Definitions and Notes**
- [DO]: "Use the Top 5 built-in macro *Definition Editor* or *Notes Editor* from the Macros tab to quickly enter definitions and notes for multiple entities at once."
- [DON'T]: "Double-click every single entity one by one and manually paste definitions into the Entity Editor."