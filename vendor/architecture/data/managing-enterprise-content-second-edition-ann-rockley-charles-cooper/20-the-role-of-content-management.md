@Domain
Trigger these rules when the user requests assistance designing, evaluating, implementing, or configuring Content Management Systems (CMS), authoring tools, workflow routing, content lifecycles, or multichannel digital/print delivery systems.

@Vocabulary
- **Segmentation / Bursting:** The process of breaking content apart into granular, element-level components before storing it in a CMS based on a defined segmentation map.
- **Traditional Authoring Tools:** Word processing tools, page layout tools, hybrids, and web authoring tools that mingle format with content and offer too much formatting flexibility.
- **Structured Editors:** Authoring tools (full function, simple XML, XML-aware, or forms-based) that enforce the structure of content (via schemas/DTDs) and separate content from format.
- **WCMS (Web Content Management System):** A system designed for web/mobile staging, editions, and personalization, but inadequate for complex print or enterprise-wide component reuse.
- **TCMS (Transactional Content Management System):** A CMS focused on eCommerce (B2B/B2C), shopping carts, and legacy inventory integration.
- **DMS (Document Management System):** A system that manages whole enterprise documents, features imaging capabilities, and has strong audit trails and security, but lacks granular component management.
- **CCMS (Component Content Management System):** A system that manages content at a granular (component) level rather than page/document level, supporting multichannel customer-facing content. Flavors include dedicated, web, publishing, learning, or enterprise.
- **LCMS (Learning Content Management System):** A closed-environment CMS focused on eLearning, SCORM compliance, and multimedia, typically integrating with a Learning Management System (LMS).
- **ECMS (Enterprise Content Management System):** A loosely defined hybrid system intended to manage broader lifecycles, varying widely by vendor.
- **CRM (Customer Relationship Management):** Systems that manage customer data and buyer profiles, often needing integration with a CMS.
- **Automatically Update:** Reused components update immediately when the source changes (risks contextual inaccuracy).
- **Optionally Update:** Reused components notify authors of source changes so they can accept or reject the update (default/recommended behavior).
- **No Update:** Reused components break connection with the source (creates diverging variations; discouraged unless intentionally branching).
- **Process Flow Creation:** The workflow phase involving the graphical representation and simulated testing of tasks.
- **Sequential Routing:** Linear movement of work from one step directly to the next.
- **Rules-based Routing:** Logic-driven movement of work based on conditions or metadata (e.g., if Product X, route to Reviewer A).
- **Parallel Routing:** Simultaneous routing of work to multiple players, usually followed by a "wait" step for integration.
- **Ad Hoc Routing:** Human-decision-driven routing bypassing standard rules, used for emergencies or exceptions.
- **Roles vs. Players:** Tasks must be assigned to functional Roles (e.g., "Senior Graphic Artist") rather than specific Players (e.g., "Nancy Smith") to ensure continuity.
- **Delivery Engine:** The system responsible for transformation, conversion, distribution, assembly, and automation of content into final formats using XSL.

@Objectives
- Enforce the separation of content from format at the authoring stage.
- Guarantee content reuse through granular component storage (segmentation) rather than monolithic document storage.
- Align the specific business/content requirements with the exact correct flavor of CMS (WCMS, CCMS, LCMS, etc.).
- Design workflows that are resilient, role-based, rule-driven, and include explicit exception handling and escalation paths.
- Automate multi-channel content delivery via robust transformation engines (XSL) without manual desktop-publishing intervention.

@Guidelines

**Authoring Tool Selection & Configuration**
- The AI MUST evaluate authoring tools based on the authors' technical capability, familiarity, and structural requirements.
- The AI MUST advocate for Structured Editors over Traditional Word Processing/Page Layout tools to prevent authors from applying arbitrary formatting and to enforce XML/schema validation during content entry.
- The AI MUST design system integrations where the authoring tool is directly linked to the CMS (automatic check-in/out, automatic population of reusable content).
- The AI MUST ensure the authoring interface hides underlying technical complexity (e.g., XML tags) if the authors are casual or non-technical.

**Content Management System (CMS) Architecture**
- The AI MUST define a "Segmentation Map" or "Bursting Map" that dictates exactly at what level content is broken down (e.g., third-level head, specific elements) when saved into the CMS.
- The AI MUST specify that metadata is applied automatically upon check-in based on templates, structure, and context.
- The AI MUST enforce Role-Based Access Control (RBAC) at the most granular component level. If a component is reused, the AI MUST configure it to inherit the most restricted access level of the information product it inhabits.
- The AI MUST require Version Control for every discrete component, not just the finalized document.
- The AI MUST configure reuse update rules to default to "Optionally Update". The AI MUST actively discourage "No Update" (which acts as copy/paste and causes divergence) unless the user explicitly requires intentional branching.
- The AI MUST ensure the CMS maintains explicit relational links between source language components and translated/localized components to trigger automatic updates for translation memory systems.
- The AI MUST NEVER recommend a database as a standalone alternative to a CMS, explicitly noting that rebuilding CMS features (UI, versioning, access control, workflow) from scratch is cost-prohibitive and inefficient.

**CMS Type Selection**
- When the user requires multi-channel publishing (print, web, mobile) with granular reuse, the AI MUST recommend a CCMS (Component Content Management System).
- When the user needs to manage eCommerce, shopping carts, and legacy inventory, the AI MUST recommend a TCMS.
- When the user only needs staging, editions, and personalization for web/mobile, the AI MUST recommend a WCMS, but MUST warn that WCMS is inadequate for complex print or enterprise content reuse.
- When the user requires strict regulatory compliance, imaging of paper records, and secure audit trails for whole documents, the AI MUST recommend a DMS.
- When the user creates eLearning, SCORM objects, and multimedia, the AI MUST recommend an LCMS, but warn that it is a closed environment not suited for general enterprise publishing.
- If recommending a "Best of Breed" multi-system approach, the AI MUST enforce a common information model, common tagging structures, and a centralized metadata crosswalk.

**Workflow System Design**
- The AI MUST design workflows separating tasks into: Work tasks (adding value), Transport tasks (moving work), Notification tasks (status changes), and Wait tasks (introducing necessary delays/dependencies).
- The AI MUST enforce the rule that workflow tasks are assigned to Roles, NEVER to specific individual Players.
- The AI MUST configure exception-handling rules for every step (e.g., "If Reviewer 3 is unavailable, route to Manager A").
- The AI MUST define parallel routing for concurrent tasks (e.g., writing and graphics creation) and insert a specific "Wait" step to synchronize them before the next sequential phase.
- The AI MUST configure Deadlines (durations or specific dates) at both the Step and Task level, and define automated Escalation paths (e.g., 3 reminders -> notify manager).
- The AI MUST define automated reporting triggers (Deadline reports, Work-in-process reports, Exception reports, Workload balance reports).

**Delivery & Publishing**
- The AI MUST design delivery systems that support centralized, automated publishing (e.g., outputting PDF, HTML, and XML simultaneously from a single request).
- The AI MUST utilize XSL (XSLT for transformation to HTML/Mobile, XSL-FO for paper/PDF layout) for all output rendering.
- The AI MUST strictly prohibit workflows that rely on manual cleanup or manual formatting in desktop publishing tools prior to final delivery.

@Workflow
When tasked with designing a unified content management and delivery architecture, the AI MUST execute the following algorithm:

1. **Authoring Analysis:**
   - Assess user personas (casual vs. technical authors).
   - Recommend the appropriate authoring tool category (Traditional vs. Structured Editor).
   - Define rules for separating content from format.
   - Specify the segmentation/bursting rules for component storage.

2. **CMS Selection & Configuration:**
   - Analyze the target content lifecycle (Web only, eCommerce, Regulatory Docs, eLearning, or Multi-channel Component).
   - Select the exact CMS type (WCMS, TCMS, DMS, LCMS, or CCMS).
   - Define Access Control matrices, Versioning rules, and Translation linkage configurations.
   - Set the global rule for component updates (Default: Optionally Update).

3. **Workflow Engineering:**
   - Map the end-to-end process utilizing Work, Transport, Notification, and Wait tasks.
   - Define Sequential, Rules-based, and Parallel routing paths.
   - Map all tasks to designated Roles.
   - Establish exceptions, deadlines, and escalation triggers for every critical bottleneck.

4. **Delivery Engine Mapping:**
   - Define the required output formats.
   - Map the XSL transformation requirements (XSLT for digital, XSL-FO/Composition integration for print).
   - Establish the automation triggers to eliminate manual publishing interventions.

@Examples (Do's and Don'ts)

**[DO]**
- **DO** assign workflow steps to roles: `"Task: 'Review draft for technical accuracy' -> Assigned to Role: 'SME_ProductX' (Players: John, Mary, Ahmed)."`
- **DO** configure parallel workflows with wait states: `"Route content to Editor AND request graphic from Art Dept simultaneously. Initiate WAIT step until both are 'Approved' before routing to Publishing."`
- **DO** default reuse mechanics to prompt the author: `"Configure component #8842 to 'Optionally Update'. When Source #112 is modified, notify Author B to accept or reject the changes."`
- **DO** recommend a CCMS for an enterprise needing to publish the exact same product description to a printed catalog, a web page, and a mobile app.
- **DO** enforce strict XML-based structured authoring tools with predefined schemas to prevent users from applying arbitrary font sizes or layout tweaks.

**[DON'T]**
- **DON'T** assign workflow tasks to specific individuals (e.g., "Send to Bob for approval"), as this breaks the workflow when Bob is promoted or goes on vacation.
- **DON'T** recommend a WCMS to a publisher whose primary outputs include complex printed textbooks and cross-departmental printed training manuals.
- **DON'T** configure reusable components to "No Update" unless the explicit business requirement is to fork the content into two permanently separate, diverging versions.
- **DON'T** allow authors to manually tweak the final layout of an enterprise document using desktop publishing tools; all layout must be handled via automated XSL stylesheets.
- **DON'T** suggest building a custom CMS from a raw database to save money; explicitly warn the user about the hidden costs of rebuilding versioning, access control, and workflow UI from scratch.