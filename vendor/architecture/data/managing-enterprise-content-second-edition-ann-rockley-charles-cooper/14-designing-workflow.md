# @Domain
These rules MUST be triggered whenever the AI is tasked with designing, analyzing, modeling, or documenting business processes, content lifecycles, and automated or manual workflows. This includes any user request to map out procedures, define approval processes, configure content management workflows, or optimize operational efficiency.

# @Vocabulary
*   **Workflow**: The way work or tasks flow through a cycle to perform a job in an efficient and repeatable manner; the embodiment of the content lifecycle.
*   **Players**: Any person, group, or system (including the CMS) that handles work between the initial event and completion.
*   **Roles**: The specific functions or "hats" worn by players in a workflow (e.g., SME, Reviewer, Approver, Author, Editor). Workflow tasks are assigned to Roles, not to individual Players.
*   **Responsibilities (Tasks)**: The specific steps or actions required to complete a piece of work. If it must "get done," it is a task.
*   **Processes (Flow)**: The complete flow of tasks from a defined start point to an end point, illustrating the interactions and interdependencies among players.
*   **Linear Flowchart**: A diagram depicting a process from beginning to end using specific symbols; generally discouraged for complex processes as they become unwieldy without clear task descriptions.
*   **Swimlane Diagram (Process Map)**: A diagram that shows processes in horizontal or vertical "lanes" assigned to specific roles, clearly depicting concurrent tasks, handoffs, and interdependencies.
*   **Work Tasks**: Tasks that add value by changing the work item in some way (e.g., writing, editing, approving).
*   **Transport Tasks**: Tasks that move the work item from one location or person to another without altering the content itself (e.g., courier, email routing).
*   **Notification Tasks**: System-generated alerts informing players that a work item has changed state and is ready for interaction.
*   **Wait Tasks**: Tasks that introduce a necessary delay, pausing the process temporarily until a prerequisite is met (e.g., waiting for graphics).
*   **Business Rules**: Organizational constraints that govern processes, such as budgets, working hours, union rules, or physical locations.
*   **What-ifs (Exceptions)**: Predefined alternative routing rules triggered when a standard workflow path is blocked (e.g., an approver is on vacation).

# @Objectives
*   The AI MUST design workflows that are highly efficient, eliminating historical bloat, redundant steps, and unnecessary exception loops.
*   The AI MUST ensure tasks are assigned strictly to abstract roles and systems, never to specific individuals.
*   The AI MUST formulate task descriptions using unambiguous, verb-noun structures.
*   The AI MUST comprehensively map the entire content lifecycle, definitively marking the triggering event (start) and the final storage/resolution (end).
*   The AI MUST incorporate necessary wait states, transport actions, and exception handling ("what-ifs") into all workflow models.

# @Guidelines
*   **Role-Based Assignment**: When defining a workflow step, the AI MUST assign the task to a generic Role (e.g., "Senior Approver", "Information Architect") and MUST NOT assign tasks to specific individuals (e.g., "John Doe"). 
*   **CMS as a Player**: The AI MUST treat the Content Management System (CMS) or automated workflow engine as an explicit Role in the workflow, assigning it specific tasks like notifications, automated routing, and report generation.
*   **Verb-Noun Task Formatting**: The AI MUST write all task descriptions starting with an action verb followed by a specific noun (e.g., "Sort graphics requests"). The AI MUST NOT use cryptic code names (e.g., "Form CP-13") or passive voice/result-oriented phrases (e.g., "Graphics are sorted").
*   **Comprehensive Task Categorization**: When auditing or creating a workflow, the AI MUST explicitly identify and include all four task types: Work Tasks, Transport Tasks, Notification Tasks, and Wait Tasks. The AI MUST NOT omit Transport or Wait tasks, as they are critical for accurate time and dependency mapping.
*   **Swimlane Organization**: When generating visual representations or structured markdown outlining a workflow, the AI MUST group tasks by Role (mimicking a Swimlane Diagram) to clearly show dependencies and handoffs, rather than producing a single, flat, linear list.
*   **Distinguish Notification from Approval**: The AI MUST critically evaluate whether a Role needs to approve a step or merely be notified of it. If a Role only needs awareness, the AI MUST assign a Notification Task, NOT an Approval Task, to prevent artificial bottlenecks.
*   **Future-State Focus**: When asked to improve a process, the AI MUST generate a simplified "to-be" workflow that strips away historical, ad-hoc workarounds and focuses strictly on best practices and core business rules.
*   **Exception Handling**: The AI MUST prompt for or automatically generate "what-if" exception paths for critical bottlenecks (e.g., defining escalation paths or alternate reviewers if a deadline is missed).
*   **Clear Boundaries**: Every workflow MUST have an explicitly defined trigger event (Start) and a logical conclusion (End), which typically involves the final content being securely stored in the repository.

# @Workflow
When tasked with designing or overhauling an effective workflow, the AI MUST execute the following step-by-step algorithmic process:

1.  **Understand Current State**: Elicit or analyze the "as-is" workflow. Identify current bottlenecks, successes, and historical bloat.
2.  **Define Boundaries**: Determine the exact starting point (the triggering incoming event) and the logical end point (when the event is fully resolved and content is stored). Determine exactly where the *automated* portion of the workflow begins.
3.  **Identify Roles**: List all players from beginning to end. Map all individuals to functional Roles. Include the System/CMS as a discrete Role.
4.  **Sketch the Tasks**: Generate the sequential and parallel tasks required. Write every task in strict verb-noun format. Include Work, Transport, Notification, and Wait tasks.
5.  **Map Interactions (Swimlanes)**: Organize the tasks into lanes based on Role. Define the dependencies (who relies on whom) and exact handoff points where tasks cross from one Role to another.
6.  **Allocate Time Frames**: Assign durations or deadlines to specific tasks and to the overall process to establish baseline expectations.
7.  **Define Notifications**: Map out exactly who needs to be notified (and by whom/what system) at each phase change.
8.  **Define Approvals**: Map out who has the authority to approve, reject, or request modifications. Ensure no unnecessary approval steps are blocking the flow.
9.  **Engineer "What-Ifs"**: Identify potential derailments (missed deadlines, unavailable approvers). Define automated escalation paths, alternate routing rules, and exception handling for these scenarios.
10. **Simplify and Streamline**: Review the generated workflow. Delete redundant tasks, combine overlapping steps, and move sequential steps into parallel where possible to maximize efficiency.
11. **Final Output Generation**: Output the optimized workflow grouped by Role/Swimlane, explicitly detailing the routing rules, task types, and constraints.

# @Examples (Do's and Don'ts)

### Task Formulation
*   **[DO]**: "Review draft for technical accuracy." / "Submit graphics request using Form CP-13."
*   **[DON'T]**: "Draft is reviewed." (Passive voice) / "Form CP-13." (Cryptic and lacks action).

### Role Assignment
*   **[DO]**: "Assign approval task to: Regional Marketing Manager."
*   **[DON'T]**: "Assign approval task to: Fred Turnbull." (Hardcoding individuals breaks the workflow if the person changes roles).

### Workflow Boundaries
*   **[DO]**: "Start Event: Receipt of signed contract. End Event: Final approved PDF is checked into the CMS."
*   **[DON'T]**: "Start Event: We decide to write something. End Event: It gets published." (Too vague; lacks strict system triggers).

### Task Type Inclusion
*   **[DO]**: 
    *   *Work Task*: Write introduction.
    *   *Wait Task*: Hold draft pending arrival of product schematics.
    *   *Transport Task*: Route physical artwork via courier to agency.
    *   *Notification Task*: System emails Editor that draft is ready.
*   **[DON'T]**: Only listing "Write introduction" and "Approve introduction", ignoring the wait times, system notifications, and transport methods between those two steps.

### Approval vs. Notification
*   **[DO]**: "Task: System notifies Customer Service that new brochure is published."
*   **[DON'T]**: "Task: Customer Service approves final brochure." (Customer Service only needs awareness to answer phones, not editorial veto power; making them approvers creates a bottleneck).