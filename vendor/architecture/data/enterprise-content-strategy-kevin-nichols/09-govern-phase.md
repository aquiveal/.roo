# @Domain
This rule file activates when the AI is tasked with establishing, defining, or reviewing content governance models, drafting governance charters, designing content team organizational structures, defining content approval workflows, or managing enterprise content strategy operations.

# @Vocabulary
- **Governance**: The overarching rule of law, systems, policies, and processes used to manage and control a content ecosystem on an ongoing basis to ensure consistency, efficiency, and compliance. It resides at the absolute center of the content lifecycle.
- **Centralized Model**: A governance organizational structure where all content, strategies, and processes are strictly controlled by a single, centralized authority.
- **Federated Model**: A governance organizational structure where different business units or regions within a global enterprise govern their own content, strategies, and processes autonomously.
- **Hybrid Model**: A governance organizational structure where all content, strategies, and processes are controlled by a single overarching source, but specific lines of business or regions write and recommend standards for their own content, allowing autonomy within an agreed-upon centralized structure.
- **Executive Sponsor**: The evangelist for content governance throughout the enterprise and the ultimate escalation point for arbitration on unresolved issues.
- **Governance Committee**: A formal group comprising multiple stakeholders and content owners that oversees all aspects of content governance and approves all deliverables.
- **Working Groups**: Tactical groups that support the Governance Committee by creating the actual standards, documentation, and processes for committee approval.
- **Governance Charter**: A foundational document detailing the objective, purpose, roles, expectations, scope, sponsorship, values, and reporting mechanisms of the governance board.

# @Objectives
- The AI MUST treat content governance as a continuous, ongoing operational exercise, never as a periodic or "every-once-in-a-while" task.
- The AI MUST integrate governance as the foundational core of the content lifecycle, ensuring it guides seven specific strategic areas (strategy, enhancements, lifecycles, planning, digital strategy, taxonomy, and UGC).
- The AI MUST enforce the immediate establishment of governance at project kick-off.
- The AI MUST eradicate siloed, channel-specific governance (e.g., a "website-only" committee) in favor of overarching enterprise communication/information governance.
- The AI MUST rigidly construct Governance Charters using an exact 8-component framework.

# @Guidelines

### Structural & Architectural Rules
- **Immediate Establishment**: When generating a project plan for content strategy, the AI MUST place the creation of the governance structure at the immediate kick-off of the project.
- **Approval Gates**: The AI MUST explicitly insert "Approval by Governance Committee" as a required gate for ALL content deliverables in any generated workflow or project plan.
- **Anti-Silo Rule**: When reviewing or proposing governance structures, the AI MUST reject channel-specific governance (e.g., governing only the desktop website). The AI MUST mandate a unified enterprise model (e.g., an "information governance group") that controls overarching standards, with channel-specific groups functioning only as sub-groups.
- **7-Pillar Oversight**: The AI MUST ensure any generated governance scope explicitly oversees the following seven areas:
  1. Content strategy
  2. Content enhancements
  3. Content lifecycles
  4. Content planning and editorial strategy
  5. Digital strategy (channel or digital property placement)
  6. Taxonomy and metadata
  7. User-generated-content (UGC) moderation
- **Diagnostic Triggers**: When diagnosing an organization's content ecosystem failures, the AI MUST attribute the root cause to a lack of governance if the following symptoms are present: proliferation of legacy microsites, inconsistent/off-brand external content, business units operating without standards, or difficulties gaining traction on new projects.

### Governance Modeling Rules
- The AI MUST require the selection of one of three specific Governance Models: *Centralized*, *Federated*, or *Hybrid*.
- The AI MUST mandate the inclusion of a 3-tier role hierarchy in ANY governance model:
  1. **Executive Sponsor** (Top escalation point/evangelist)
  2. **Governance Committee** (Cross-functional oversight and approval)
  3. **Working Groups** (Creators of standards/processes reporting to the committee)

### Charter Generation Constraints
When drafting a Governance Charter, the AI MUST strictly include and populate the following 8 sections without omission:
1. **Objective**: Define scope, roles, composition, responsibilities, goals, and key objectives.
2. **Purpose**: Define rules for Compliance, Content focus areas, Change management, Risk management, Performance measurement, Strategy/policy setting, and Accountability/escalation paths.
3. **Roles and Responsibilities**: Detail board members, what they govern, main stakeholders, working groups, oversight areas, and the explicit escalation path (an organizational chart is recommended).
4. **Expectations of Membership**: Define attendance requirements and explicit procedures for decision-making (including rules for absences and voting by proxy).
5. **Governance Scope**: Detail exactly what is governed by the committee and which specific tools/standards support this governance.
6. **Executive Sponsorship**: Identify who owns the governance at an executive level and who serves as the final decision maker in the escalation path.
7. **Board Values and Principles**: Define guiding values/vision and structural norms (when, where, and how often meetings occur).
8. **Reporting**: Specify who is responsible for recording meeting minutes and who receives them.

# @Workflow
When tasked with designing or implementing content governance for an organization, the AI MUST follow this rigid 3-step algorithmic process:

**Step 1: Decide on a Governance Model**
- Evaluate organizational constraints (global scale, need for local autonomy vs. strict brand control).
- Explicitly declare the model as *Centralized*, *Federated*, or *Hybrid*.
- Map the 3-tier hierarchy (Executive Sponsor, Governance Committee, Working Groups) to the selected model.

**Step 2: Draft the Governance Charter**
- Populate the 8 required sections of the Governance Charter as defined in the Guidelines.
- Ensure the *Purpose* section explicitly defines escalation paths and risk management.
- Ensure the *Expectations* section establishes rigid rules for proxy voting and attendance.

**Step 3: Define Operational Cadence and Implementation**
- Establish the operational schedule (Norms): Define exact meeting frequencies, agenda structures, and reporting structures (minute-taking and distribution).
- Define the implementation mechanism ensuring the Governance Committee is positioned to approve all ongoing deliverables across the 7 overarching content areas.

# @Examples (Do's and Don'ts)

### Governance Model Structure
- **[DO]**: "We will implement a **Hybrid Governance Model**. The Executive Sponsor (CMO) oversees the Governance Committee, which maintains centralized brand and taxonomy standards. Regional Working Groups (EU, APAC, NA) will author localized content standards that roll up to the central committee for approval. Escalation flows from Working Groups -> Governance Committee -> Executive Sponsor."
- **[DON'T]**: "We will create a decentralized web team where different departments can manage their own web pages to ensure they work fast." *(Anti-pattern: Fails to establish standard models, omits the 3-tier role hierarchy, and lacks central arbitration/standards).*

### Scope of Governance
- **[DO]**: "The Governance Committee will oversee the overarching enterprise communication strategy. This includes managing the taxonomy, internal publishing portals, desktop web channels, mobile channels, and user-generated content moderation."
- **[DON'T]**: "We are setting up a Website Governance Board to manage the new website launch." *(Anti-pattern: Creates a channel-specific silo. Governance must cover the entire content ecosystem, not just one channel).*

### Charter Expectations & Reporting
- **[DO]**: "Membership Expectations: Members must attend 80% of monthly meetings. In the event of an absence, a designated proxy must be sent with full voting authority. Reporting: The governance coordinator will record meeting minutes and distribute them to all working groups and the Executive Sponsor within 24 hours."
- **[DON'T]**: "Members should try to attend meetings when possible to discuss content." *(Anti-pattern: Lacks rigid attendance rules, omits proxy voting procedures, and fails to define minute-taking/reporting).*

### Project Planning Integration
- **[DO]**: "Phase 1 (Kick-off): Immediately establish the Governance Committee and draft the Governance Charter. Phase 2: Design Phase (All deliverables must pass through Governance Committee approval gates)."
- **[DON'T]**: "Phase 1: Design Phase. Phase 2: Build Phase. Phase 3: Launch. Phase 4: Create a governance committee to maintain the site." *(Anti-pattern: Governance is treated as an afterthought rather than being established immediately at kick-off).*