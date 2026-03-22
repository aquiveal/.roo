@Domain
This rule file MUST be triggered when the AI is tasked with designing, evaluating, implementing, or documenting a unified content strategy, customer content journeys, content matrices, editorial workflows, content lifecycles, or multichannel publishing architectures.

@Vocabulary
*   **Front Stage**: The customer-facing unified content strategy that dictates exactly what types of content the customer needs, what format/media they need it in, and when they need it.
*   **Back Stage**: The unified content lifecycle; the internal organizational processes and technologies that support the creation, management, and delivery of the strategy.
*   **Scenario**: A rigid description of an everyday customer situation that explicitly answers four questions: Who is involved? What triggers the experience? What happens? What is the result?
*   **Customer Content Lifecycle**: The four distinct stages a customer experiences when interacting with an organization and its content: Explore, Buy, Use, and Maintain.
*   **Content Matrix**: A framework that matches the phases of the Customer Content Lifecycle with the specific information products required to reach the goals defined in the customer Scenarios.
*   **Component**: A modular chunk of content. In this architecture, content is authored, reviewed, and managed at the component level, not the document level.
*   **Inheritance (Metadata/Security)**: The automated process where metadata or access controls applied to a parent container (document or assembly) are automatically applied to all its constituent subcomponents.
*   **Segmentation/Bursting**: Breaking content apart into its individual structural components before it is stored in the repository.

@Objectives
*   Bridge the gap between customer needs (Front Stage) and organizational execution (Back Stage) by formalizing strict strategic matrices and lifecycle processes.
*   Map all proposed content to rigorous, 4-step user Scenarios and align them to the four Customer Content Lifecycle phases.
*   Architect a highly structured content creation process that mandates cross-silo planning, modular authoring, component-level review, automated metadata inheritance, and formatting-free delivery.
*   Translate identified organizational business challenges directly into targeted lifecycle process improvements (e.g., solving translation costs by tracking source components).

@Guidelines

### 1. Front Stage Strategy Rules (Customer-Facing)
*   The AI MUST construct **Scenarios** for every customer persona before defining content deliverables.
*   Every Scenario MUST explicitly contain four labeled sections: `Who:`, `Trigger:`, `Happens:`, and `Result:`.
*   The AI MUST map content requirements using a **Content Matrix** that categorizes content strictly into one of four Customer Content Lifecycle stages: `Explore`, `Buy`, `Use`, or `Maintain`.

### 2. Back Stage Lifecycle Rules (Internal Processes)
*   **Create Phase (Planning)**: The AI MUST mandate cross-departmental (silo-breaking) planning sessions (e.g., press, web, education) and the establishment of a shared, centralized editorial calendar.
*   **Create Phase (Authoring)**: 
    *   Content MUST be authored in a modular fashion to facilitate component-level reuse.
    *   The AI MUST rigidly enforce the separation of content from format. Content must be written to structural templates (XML or XML-backed Word) devoid of layout parameters.
    *   Core content MUST be designed to accommodate dynamic rebranding and reordering for custom outputs.
*   **Edit and Review Phase**:
    *   Reviews MUST be conducted at the **Component Level**, never at the monolithic document level.
    *   The workflow MUST support parallel review, allowing reviewers to see each other's compiled annotations and the complete version history of the component simultaneously.
    *   Approval MUST be managed via metadata flags (e.g., `Status: Ready for Final Approval`) rather than email handoffs.
*   **Manage Phase**:
    *   **Metadata**: MUST be applied to every single assembly and component. The AI MUST automate metadata application based on taxonomy and structure wherever possible.
    *   **Metadata Inheritance**: Any metadata applied to a higher-level document/assembly MUST automatically cascade down to all subcomponents.
    *   **Controlled Vocabularies**: Metadata values MUST be selected from predefined lists; free-text tagging is prohibited unless explicitly justified.
    *   **Version Control**: The system MUST enforce two levels of versioning: `Draft` (unapproved) and `Full Version` (approved). Detailed history (who, when, why) MUST be tracked per component.
    *   **Access Control Inheritance**: Security permissions MUST cascade. If a component is reused across multiple locations with different security levels, the system MUST enforce the *most restricted* level of access on that component.
    *   **Check-in Protocol**: Authors MUST check in content to the CMS daily at minimum; local drive storage of working files is strictly prohibited.
    *   **Reporting**: The AI MUST specify the generation of six mandatory report types: `Where Used`, `Status`, `Responsible Party`, `Project Review (durations)`, `Inactive Modules`, and `Subject-based Aggregations`.
*   **Delivery Phase**:
    *   Delivery MUST rely exclusively on stylesheets (e.g., XSLT, CSS) to format content for Web, Print, Mobile, and eBooks.
    *   The AI MUST NOT recommend manual desktop publishing tweaks post-XML extraction. 

### 3. Challenge Mitigation Mapping
When addressing specific organizational challenges, the AI MUST map the solution to the exact lifecycle phase as follows:
*   *If Time-to-Market is slow*: Mandate parallel workflows, clear handoffs, and component reuse in the **Manage (Workflow)** phase.
*   *If Delivery to multiple channels is failing*: Mandate separation of content from format and XML stylesheets in the **Delivery** phase.
*   *If Content lacks standardization*: Mandate information models and author training in the **Create** phase.
*   *If Reviews take too long*: Mandate component-level review and parallel automated workflow in the **Edit/Review** phase.
*   *If Content cannot be found*: Mandate rich metadata and robust search in the **Manage** phase.
*   *If Translation costs are too high*: Mandate source-tracking, sending only changed components to translation, and maximizing reuse in the **Manage** phase.

@Workflow
When tasked with envisioning a unified content strategy and lifecycle, the AI MUST execute the following algorithmic sequence:

1.  **Define the Front Stage (Strategy)**
    *   *Step 1*: Identify the target personas.
    *   *Step 2*: Generate a 4-part Scenario for each persona (`Who`, `Trigger`, `Happens`, `Result`).
    *   *Step 3*: Map the customer's journey across the Customer Content Lifecycle (`Explore`, `Buy`, `Use`, `Maintain`).
    *   *Step 4*: Construct the Content Matrix by assigning specific information products to the intersections of Scenarios and Lifecycle stages.

2.  **Define the Back Stage (Lifecycle)**
    *   *Step 5 (Create)*: Define the cross-silo planning mechanism (e.g., unified editorial calendar). Define the structural authoring templates (XML/modular) required for the content identified in Step 4.
    *   *Step 6 (Edit/Review)*: Architect the component-level review workflow. Specify how parallel reviewers will annotate chunks and how version history will be exposed.
    *   *Step 7 (Manage)*: Define the metadata taxonomy. Explicitly document the Inheritance Rules for metadata and access control. Detail the versioning states (Draft vs. Full) and mandate the required systemic reports.
    *   *Step 8 (Deliver)*: Specify the stylesheets and automated publishing rules required to map the format-free components to their final multichannel outputs (Web, eBook, Print, App).
    *   *Step 9 (Challenge Check)*: Cross-reference the proposed lifecycle against the organization's stated pain points using the *Challenge Mitigation Mapping* guidelines to ensure all business issues are structurally resolved.

@Examples (Do's and Don'ts)

### Scenarios
*   **[DO]** Write strict, 4-part scenarios.
    *   *Who*: Sharon, 30s, recently diagnosed diabetic, busy working mother.
    *   *Trigger*: Experiences a blood sugar crash at a soccer game and decides she needs immediate dietary guidance.
    *   *Happens*: Searches website on her mobile phone for quick food reference, watches a 3-minute overview video, finds a 1-week recipe plan.
    *   *Result*: Prints the recipe plan, signs up for the newsletter, feels empowered to grocery shop.
*   **[DON'T]** Write vague user stories.
    *   *Anti-pattern*: "Sharon wants to learn about diabetes so she goes to the website and reads some articles." (Lacks rigid structure and clear trigger/result mapping).

### Content Matrix Alignment
*   **[DO]** Categorize content strictly by the customer's lifecycle phase.
    *   *Explore Phase*: 3-minute Overview Video, Generic Definition Component.
    *   *Use Phase*: 1-week Recipe Plan, Mobile App Database Lookup.
*   **[DON'T]** Present a flat list of deliverables without lifecycle context.
    *   *Anti-pattern*: "Deliverables: Video, PDF, App, Web Pages."

### Component-Level Review
*   **[DO]** Structure workflow to route modular chunks.
    *   "Route `Component: Value Proposition v2.1` to Legal and Marketing simultaneously. Compile annotations on the component layer. Do not wait for `Component: Technical Specs` to be written before beginning review."
*   **[DON'T]** Route monolithic documents.
    *   *Anti-pattern*: "Wait until the 50-page brochure is fully drafted, generate a PDF, and email it to Legal and Marketing for serial review."

### Metadata Inheritance & Security
*   **[DO]** Automate cascading constraints.
    *   "Apply `Access: Highly Restricted (Senior Management)` to the container `Q3 Audit Report`. The system automatically inherits this restriction to `Component: Company Logo` while it is assembled in this report, preventing unauthorized viewing of the draft."
*   **[DON'T]** Rely on manual tagging or ignore context.
    *   *Anti-pattern*: "Ask the author to manually tag all 400 components in the Audit Report as Restricted."

### Delivery and Formatting
*   **[DO]** Separate content from format entirely.
    *   "Author standard text in XML. System automatically applies `Print_Stylesheet.xsl` for PDF generation, dropping secondary tables, and applies `Mobile_Stylesheet.css` for app delivery, chunking headers into accordions."
*   **[DON'T]** Embed formatting in the authoring phase.
    *   *Anti-pattern*: "Author creates a complex 6-column table in Word and manually inserts page breaks so it looks good in the PDF." (This fails on mobile and eBooks).