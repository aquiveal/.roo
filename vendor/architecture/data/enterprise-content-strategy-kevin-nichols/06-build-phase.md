**@Domain**
These rules MUST be triggered when the user requests assistance with the "Build Phase" (also known as development or implementation phase) of an enterprise content strategy project. Activation conditions include tasks related to: creating or organizing content creation plans, developing content migration approaches or mappings, extracting/transforming existing content into new system databases, planning content quality assurance (QA), and designing or updating content/editorial calendars. 

**@Vocabulary**
- **Build Phase**: The project phase where design work (taxonomy, content model, lifecycles) is implemented by a technology team, and plans for content creation, migration, and scheduling are executed.
- **Batch / Story**: A finalized group of functions, pages, or templates approved during the design process (often used in agile development) that dictates when content creation can safely begin.
- **Content Plan**: A detailed, step-by-step roadmap accounting for the acquisition, creation, review, and publication of all new content required for the new experience.
- **Content Matrix**: The primary structural document used as the starting point for content planning; it identifies content type name, placement, rules, metadata, and source.
- **Extraction, Transformation, and Migration (ETM)**: A parallel development approach where existing content is pulled into a staging database (e.g., Access), cleaned up, and mapped to the new design prior to the final system's completion.
- **Content Calendar**: A scheduling tool (often annual, divided into quarters) that sets priorities for future content creation based on strategic inputs, analytics, and business goals.
- **Migrate As-Is**: Existing content that requires little to no rework for the new system.
- **Migrate with Rework**: Existing content that requires updates, resizing, or reformatting before migrating.

**@Objectives**
- Ensure technology implementations strictly adhere to previously approved design phase deliverables (taxonomy, content models, lifecycles).
- Prevent costly rework by strictly halting any new content creation or migration until specific design sign-off thresholds are met.
- Generate highly granular, spreadsheet-based content plans that assign complexity metrics and map directly to documented content lifecycles.
- Facilitate a seamless content migration by ensuring thorough gap analysis, staging (ETM), and meticulous QA processes.
- Establish a sustainable, closed-loop governance mechanism by designing content calendars that mandate periodic, data-driven review cycles.

**@Guidelines**
- **Design Sign-Off Threshold**: The AI MUST NOT initiate content creation or content migration planning unless the user confirms that at least two design batches (or agile stories) AND at least two levels of the sitemap have been formally approved. If unconfirmed, the AI MUST explicitly warn the user of the risks of cost overruns and rework.
- **Content Plan Source**: The AI MUST use the Content Matrix as the absolute starting point for the Content Plan. 
- **Content Plan Organization**: The AI MUST sort the Content Plan by content type. A separate worksheet or sub-plan MUST be generated for each distinct content type (e.g., one for images, one for product-detail pages).
- **Complexity Assignments**: For every task in the Content Plan, the AI MUST assign a Level of Effort (LOE) using strict categories: "Low", "Medium", or "High" complexity. Time estimates MUST be derived directly from these complexity assignments.
- **Tooling Constraints**: The AI MUST recommend tracking content status via spreadsheets (at the page or module level) and daily/weekly status sheets rather than using complex project management software like Microsoft Project, which is explicitly warned against for this specific tracking.
- **Parallel Migration (ETM)**: When planning migration alongside system development, the AI MUST structure an intermediate staging step (database or Excel with XML mapped to the Content Matrix fields) to clean and transform content before the target CMS is fully built.
- **Multimedia and Complex Format Constraint**: The AI MUST flag all legacy multimedia, Flash, Java, and microsite components as "Require Rework/Redesign." The AI MUST strictly forbid classifying these formats as "Migrate As-Is."
- **Prioritized Rollout**: The AI MUST sequence migration plans so that high-priority content is migrated before launch, while lower priority or heavily reworked content (like refactored videos) is scheduled for post-launch phases.
- **Metadata Reconciliation**: The AI MUST mandate that legacy metadata is migrated and reconciled with the new content structure during the migration process.
- **Automated vs. Manual Migration**: The AI MUST evaluate the structure of existing content. If legacy content is unstructured or embedded directly in HTML rather than a CMS/templates, the AI MUST warn that automated migration will be difficult and recommend manual or heavily transformed migration processes.
- **Content Calendar Structure**: The AI MUST format Content Calendars on an annual basis, divided into quarters at a minimum (with weekly/daily schedules nested within if volume requires). 
- **Calendar Governance Integration**: The AI MUST include specific, recurring tasks within the Content Calendar dedicated to reviewing site metrics, analytics (SEO, social listening), user feedback, and business trends to inform the next cycle of content.

**@Workflow**
1. **Prerequisite Verification**: Ask the user to confirm if at least two design batches/stories and two sitemap levels are locked. If no, issue a halt warning. If yes, proceed to Step 2.
2. **Content Planning**:
   - Ingest or construct the Content Matrix.
   - Sort all content requirements by Content Type.
   - For each Content Type, list lifecycle steps (Acquire, Create, Review, Publish).
   - Assign Low/Medium/High complexity to each step.
   - Map steps to roles (Copywriter, Legal, Brand, Tech) and output a spreadsheet-ready status tracker.
3. **Migration Strategy & Execution**:
   - Compare the current-state content inventory with the future-state Content Matrix (Gap Analysis).
   - Classify all legacy content as "Migrate As-Is", "Migrate with Rework", or "Do Not Migrate".
   - Flag all multimedia, microsites, and regional sites for rework/phased retirement.
   - Define the ETM process: map existing source links/content into the new Content Matrix fields for staging.
   - Append a mandatory manual QA step for all migrated pages, especially if automated scripts are used.
4. **Content Calendar Generation**:
   - Generate a schedule outlining content production for the upcoming periods.
   - Insert "Review and Optimize" milestones at the end of every quarter to ensure the calendar acts as a closed-loop governance tool driven by analytics.

**@Examples (Do's and Don'ts)**

- **Content Plan Structuring**
  - [DO]: 
    ```csv
    Content Type | Task Step | Owner | Complexity | Est. Time | Due Date
    Image (Hero) | Acquire Specs | Designer | Low | 2 hrs | Oct 12
    Image (Hero) | Draft Design | Designer | High | 16 hrs | Oct 18
    Image (Hero) | Legal Review | Legal Dept | Low | 4 hrs | Oct 20
    ```
  - [DON'T]: "Task: Make all images for the homepage. Assigned to: Design Team. Estimated time: 2 weeks." (Fails to break down by lifecycle steps, sort by content type, or use Low/Medium/High complexity ratings).

- **Migration Assessment**
  - [DO]: "Legacy Microsite A contains Flash components and unstructured HTML. Classification: Migrate with Rework (Redesign). Action: Map textual assets to new database structure; allocate design hours for interactive replacement."
  - [DON'T]: "Export Legacy Microsite A using automated spider tool and push directly to the new CMS as-is." (Violates the constraint against migrating complex/unstructured formats automatically or as-is).

- **Content Calendar Governance**
  - [DO]: Include a mandatory milestone on the last Friday of every quarter titled "Analytics & Metrics Review: Assess SEO, social listening, and user feedback to dictate new content priorities for the upcoming quarter."
  - [DON'T]: Generate a calendar that simply lists blog post titles for 12 months without any built-in review or optimization cycles.