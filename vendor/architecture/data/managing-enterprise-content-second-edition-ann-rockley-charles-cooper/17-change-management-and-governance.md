# @Domain
These rules apply when the AI is tasked with analyzing, designing, implementing, or evaluating change management plans, governance frameworks, organizational rollouts, communication strategies, or business rules for a unified content strategy or content management system (CMS).

# @Vocabulary
*   **Change Management:** The formal process of communicating and managing organizational change to prevent resistance, secure buy-in, and ensure successful adoption of a unified content strategy.
*   **Governance:** The ongoing process of "steering" and maintaining the content, the people who create it, and the systems that support it (including models, reuse, workflow, and metadata).
*   **Governance Board (or Steering Committee):** A cross-functional group of fewer than 10 representatives responsible for setting long-term strategic goals, evaluating requested system changes, and managing day-to-day maintenance of taxonomy, metadata, and workflow.
*   **Change Agents:** Representative users who understand the problems, are open to change, and are enlisted to advocate for the new system and methodologies to their peers.
*   **Champion:** A high-level executive who officially endorses the project, secures resources, and enforces adoption across disparate business units.
*   **Derivative Reuse:** Reused content that has been modified from the source. Requires explicit governance rules to manage ownership and synchronization.
*   **Not Invented Here:** A form of user resistance where authors refuse to use reusable content because they believe content created by others cannot possibly meet their specific audience's needs.

# @Objectives
*   Ensure the AI architects change management plans that communicate the "why" and address user pain points, rather than just dictating new processes.
*   Establish rigid, documented governance structures for every facet of the unified content strategy: content guidelines, content models, reuse rules, workflow, and metadata/taxonomy.
*   Prevent project failure by mandating phased rollouts, selecting appropriate pilot projects, anticipating resistance, and securing ongoing resources post-implementation.
*   Ensure technical systems (CMS, IT) do not dictate taxonomy or workflow changes without prior Governance Board approval to prevent system degradation over time.

# @Guidelines

### Change Management Strategy
*   The AI MUST identify and document the "pain, issues, and consequences" of the current state before proposing any technical solutions.
*   The AI MUST require a formal Communication Plan that explicitly addresses:
    *   **Why change?** (The dangers of the status quo).
    *   **The plan** (Timelines and informal sessions).
    *   **Ongoing status** (Newsletters, wikis, or blogs).
    *   **Successes and Problems** (Admitting faults early to build trust).
    *   **Personal Impact** (Honest assessment of how individual workloads and required skills will change).
*   The AI MUST mandate the identification and mobilization of Change Agents to communicate excitement to their specific teams.
*   The AI MUST require the assignment of an Executive Champion to enforce cross-departmental adoption.
*   The AI MUST ensure two-way communication loops ("Reach out and listen"); the strategy MUST include steps to verify understanding of employee concerns and demonstrate how the design addresses them.

### Overcoming Resistance
When addressing organizational resistance, the AI MUST apply these specific mitigation strategies:
*   **For "Not invented here":** Conduct "seeing is believing" mini-audits to demonstrate how content can be written without format in mind and applied across multiple channels.
*   **For "We do it differently":** Focus on commonalities and business competitors rather than internal competition. Allow process variations if the output remains effective, reusable content.
*   **For "Loss of creativity":** Redefine creativity as information design and usability rather than visual layout. Allow authors optional control over stylesheets or component visual representations if necessary.
*   **For "Too much work":** Emphasize that the heavy workload is strictly upfront during design and implementation, resulting in reduced maintenance workloads later.
*   **For "Job loss fears":** Position the efficiency gains as a way to do more with the same resources, freeing up time to pursue previously unfunded/unstaffed projects.

### Project Failure Prevention
To avoid common failure points, the AI MUST explicitly prohibit:
*   "Big bang" implementations (doing it all at once). The AI MUST mandate phased, prototype-driven rollouts.
*   Mission-critical, tight-deadline projects as the initial pilot. The AI MUST recommend selecting a pilot project that uses existing content requiring major revision.
*   Project-by-project reuse strategies. The AI MUST design the architecture for the entire enterprise scope before implementing locally.
*   Reusing everything. The AI MUST explicitly advise against reusing content if it compromises quality or readability.
*   Treating the project as "done" at launch. The AI MUST mandate budgeting and allocation for *ongoing resources and oversight* to prevent users from reverting to old habits.
*   Relying on a single type of reuse. The AI MUST employ a mix of manual and automated reuse for maximum flexibility.

### Content and Reuse Governance
*   **Content Guidelines:** The AI MUST assign an Editor to own structured writing guidelines. If embedded in an authoring tool, the AI MUST allow authors to toggle guidelines off, but force them to auto-enable when a rule changes.
*   **Content Models:** The AI MUST assign a Content Strategist or Governance Board to own models. Arbitrary model changes MUST be strictly prohibited to prevent the loss of automation.
*   **Reuse Business Rules:** The AI MUST define explicit operational rules for reuse, answering:
    *   Who creates the component?
    *   Who reviews it?
    *   Who is allowed to modify the source? (Only the owner).
    *   Are other authors allowed to modify it? (Only with owner approval).
    *   How do updates propagate? (Automatically or by author choice).
    *   Who modifies derivative versions? (The derivative owner).

### Workflow, Taxonomy, and Metadata Governance
*   The AI MUST establish a Governance Board to manage the taxonomy and workflow over the long term.
*   The AI MUST restrict IT from unilaterally making taxonomy or metadata changes. All requested changes MUST be reviewed by the Governance Board to ensure they support new products without impeding access to existing content.
*   The AI MUST structure Governance Board operations as follows:
    *   **Size:** Fewer than 10 people.
    *   **Representation:** Content creators, management, IT/systems, and customer-facing roles (marketing, sales, support).
    *   **Frequency:** 6–8 times in the first year (for rapid implementation decisions), shifting to quarterly or release-aligned schedules in subsequent years.
    *   **Process:** Materials for requested changes MUST be distributed one week prior to the meeting. Members MUST arrive with a clear "accept/reject" recommendation based on departmental impact.

# @Workflow
When tasked with designing a unified content strategy rollout and governance plan, the AI MUST execute the following algorithm:

1.  **Analyze Pain and Establish Case:** Document current organizational pains, content inconsistencies, and business consequences. Use this to draft the "Why change?" narrative.
2.  **Establish the Governance Board:** Define the board's composition (<10 people, cross-functional), meeting cadence (frequent during year 1, quarterly after), and review protocols.
3.  **Draft the Communication and Change Plan:** Build a multi-channel communication plan. Identify the Executive Champion and select/train Change Agents from within content creation teams.
4.  **Define Governance Business Rules:** Draft explicit rules matrix for:
    *   Content model maintenance.
    *   Reuse operations (source ownership, update propagation, derivative handling).
    *   Workflow routing exceptions.
    *   Taxonomy and metadata modification requests.
5.  **Select Pilot Project:** Identify a low-risk, existing-content revision project for the initial prototype. Explicitly exclude mission-critical, tight-deadline projects.
6.  **Formulate Resistance Mitigation Strategies:** Anticipate specific user pushback (e.g., "Loss of creativity", "Not invented here") and script targeted interventions (mini-audits, shifting focus to usability).
7.  **Define Post-Implementation Support:** Mandate the ongoing resource allocations, continuous Governance Board operations, and system maintenance budgets required to sustain the strategy permanently.

# @Examples (Do's and Don'ts)

### Change Management Communication
*   **[DO]:** "We are moving to structured content because our current manual copy-paste process resulted in 48 contradictory versions of our product specs, causing high translation costs and customer confusion. This change will require learning a new XML editor, but will ultimately eliminate manual formatting work. Here are our change agents who will assist you during the transition."
*   **[DON'T]:** "Starting Monday, everyone must use the new CMS and follow XML schemas to increase our enterprise efficiency. Training is available on the intranet." *(Fails to explain the specific pain, ignores personal impact, lacks two-way communication).*

### Reuse Governance Business Rules
*   **[DO]:** Define a rule: "Source component ownership belongs to the original author. If Author B wishes to reuse and modify the component, they must create a derivative. When the source is updated, Author B will receive an 'optionally update' notification and is responsible for reviewing and updating the derivative."
*   **[DON'T]:** "All users should try to reuse content from the repository. If a component is close to what you need, just edit the text to fit your document." *(Fails to establish ownership, allows source destruction, ruins synchronization).*

### Pilot Project Selection
*   **[DO]:** Select a legacy product manual that is due for an annual update in 6 months. Use this to test the content models, metadata tagging, and workflow, allowing time to learn from mistakes.
*   **[DON'T]:** Select the launch materials for the company's brand-new flagship product releasing next month. *(Too high risk, guarantees shortcuts will be taken, ensures failure of the unified methodology).*

### Taxonomy/Metadata Governance
*   **[DO]:** When a new target demographic is identified, submit a proposal to the Governance Board detailing the requested metadata tags, how they interact with existing tags, and proving they will not flood the CMS with irrelevant search results for other departments. IT implements only after Board approval.
*   **[DON'T]:** Have an author email IT asking to add a new dropdown category for "Young Adults", which IT immediately hardcodes into the CMS, causing reporting errors for the legacy marketing team.