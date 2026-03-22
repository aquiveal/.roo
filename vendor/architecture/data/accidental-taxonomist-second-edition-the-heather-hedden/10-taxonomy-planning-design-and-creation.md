@Domain
Activation conditions: Triggers when the AI is instructed to plan, design, construct, test, audit, or establish governance for a taxonomy, thesaurus, or controlled vocabulary. This includes tasks related to enterprise taxonomy initiatives, content auditing, stakeholder research, taxonomy user interface planning, taxonomy project management, or the documentation of taxonomy policies and editorial style guides.

@Vocabulary
- **Stakeholder**: Anyone who has a vested interest in the project, can be affected by the change initiative that the project represents, or has the power to influence the project.
- **Content Audit / Content Inventory**: A detailed survey identifying the most critical core content to be covered by the taxonomy.
- **ROT**: Content determined to be Redundant, Obsolete, or Trivial during a content audit.
- **Straw-man Taxonomy**: An initial top-level draft of a taxonomy (usually the top two levels) presented to stakeholders for early review, designed to be easily torn down and rebuilt if necessary.
- **Card Sorting**: A technique used to design hierarchical taxonomies where participants sort candidate taxonomy terms into categories. 
- **Open Card Sort**: A card sort where participants categorize cards as they deem appropriate, naming the categories themselves.
- **Closed Card Sort**: A card sort where the top-level categories are predefined, and participants sort lower-level concepts into them.
- **Taxonomy Validation**: The dual-process testing of a taxonomy prior to full availability, testing both its effectiveness for indexing content and finding (retrieving) content.
- **Taxonomy Governance**: The documented policies and procedures for managing and maintaining a taxonomy over time, including roles, accountabilities, standards, process methodologies, and communication methods.
- **Enterprise Taxonomy**: A taxonomy whose primary users are internal enterprise members, organizing content largely created by members of the enterprise, unifying concepts across multiple departments to serve the entire organization.

@Objectives
- Execute a structured, rigorously documented planning phase for all taxonomy projects, systematically identifying purpose, users, content, scope, and resources.
- Tailor the research, design, and creation methodologies strictly to the target structure (Hierarchical, Faceted, or Thesaurus) and the target environment (Enterprise vs. Public/Consumer).
- Conduct exhaustive content audits and user research (including search log and click-trail analysis) to inform term selection and structural hierarchy.
- Validate the taxonomy structure through empirical testing methodologies (e.g., card sorting, indexing tests, retrieval precision/recall tests) prior to deployment.
- Establish comprehensive, living taxonomy governance frameworks that dictate ongoing maintenance, editorial style, and administrative policies.

@Guidelines

**Project Planning & Scoping**
- The AI MUST define the taxonomy's primary purpose early: determine if it is primarily for indexing support (manual/automated), retrieval support (search/discovery), or organization and navigation support.
- The AI MUST define the users: distinguish between indexers (dedicated vs. content creators) and end-users (internal employees, students, general public, subject matter experts), as this dictates taxonomy depth, breadth, and term style.
- The AI MUST establish the subject area scope and explicitly state policies for what types of subjects and named entities (people, organizations, products, places) are included or excluded.
- The AI MUST identify technical resources and constraints, including software capabilities (e.g., does the system support polyhierarchies? faceted search? node labels?).

**Research & Information Gathering**
- The AI MUST propose stakeholder interviews (30-60 minutes) exploring business goals, current search weaknesses, content types, and system challenges. Distinguish question sets for content-creators/taggers vs. end-users/searchers.
- The AI MUST utilize Search Query Logs to identify user-entered keywords for preferred and nonpreferred term generation.
- The AI MUST utilize Click-Trail Reports to understand prevailing navigation paths, which inform the logical hierarchy and arrangement of top-level terms.

**Enterprise Taxonomy Specifics**
- When working on an Enterprise Taxonomy, the AI MUST propose a cross-functional stakeholder workshop (full-day or two-day) to brainstorm facets and terms interactively.
- The AI MUST identify and include proprietary/nonpublic terminology (internal jargon, acronyms, project code names) unique to the enterprise.
- The AI MUST conduct an Enterprise Content Audit targeting "critical core content". Do NOT attempt to inventory every single piece of enterprise content. Exclude emails, confidential records, receipts, forms, and third-party literature.
- The AI MUST record the following data points in an Enterprise Content Audit: Content (or document), Category (document type), Source (application/database), Location (URL/path), Stakeholder (author/consumer), Organization (affiliation), and Term. Flag items as ROT where applicable.

**Taxonomy Creation Strategy**
- The AI MUST differentiate the creation approach based on the taxonomy type:
  - *Hierarchical/Faceted*: Use a top-down approach (or hybrid). Define top categories, sample second-level terms, build a "straw-man", get feedback, then build out to lower levels.
  - *Thesaurus*: Use a bottom-up approach. Gather concepts from content, organize into offline lists (spreadsheets), import to software, then fully build out relationships and notes.
- The AI MUST NOT assign multiple taxonomists to work randomly; divide work strictly by hierarchy/facet/subject area, OR by functional task (e.g., auditing, structuring, relationship-building).

**Card Sorting Constraints**
- The AI MUST ONLY use card sorting for the top two levels of a hierarchical taxonomy.
- The AI MUST NOT use card sorting for faceted taxonomies, unless testing a single facet in isolation.
- The AI MUST restrict card sorting exercises to 4-8 top-level categories and a total of 20-60 second-level terms to prevent participant fatigue.

**Taxonomy Testing (Validation)**
- The AI MUST test the taxonomy for *Indexing*: simulate indexing with sample content to identify missing terms or terms needing clarification.
- The AI MUST test the taxonomy for *Retrieval*: execute queries for known content to evaluate Recall (can users find it?) and Precision (are incorrect documents retrieved?).

**Governance & Maintenance**
- The AI MUST transition the initial "Taxonomy Design Plan" into a permanent "Governance Document" upon project completion.
- The AI MUST ensure the governance documentation includes: rules for adding/changing/deleting terms, identifying the maintenance group, process for handling comments/appeals, an editorial style guide, an end-user guide, and indexing guidelines.

@Workflow

1. **Phase 1: Project Initiation & Questioning**
   - Identify the taxonomy project manager and stakeholders.
   - Answer the 5 Fundamental Questions: Purpose, Users, Content, Scope, Resources.
   - Clarify structural prerequisites (flat, hierarchical, or faceted? polyhierarchies allowed? associative relationships supported?).

2. **Phase 2: Research & Auditing**
   - Execute Stakeholder Interviews.
   - Analyze Search Logs (for term formulation) and Click-Trail reports (for hierarchical structuring).
   - Conduct Content Audit. Record metadata (Category, Source, Location, Stakeholder, Term) and exclude ROT.
   - *If Enterprise:* Conduct Stakeholder Workshop to extract internal jargon and establish preliminary facets.

3. **Phase 3: Taxonomy Design Plan Formulation**
   - Draft the Taxonomy Design Plan detailing: Purpose, Scope, Tools, Sources, Implementation Systems, Interface Features, Indexing Method, Structure/Relationship Types, and Timetable.

4. **Phase 4: Taxonomy Construction**
   - *If Hierarchical/Faceted:*
     a. Identify top categories/facets based on audit patterns.
     b. Generate sample second-level terms.
     c. Present a "straw-man" taxonomy for stakeholder review.
     d. Revise based on feedback.
     e. Build out full taxonomy to lower levels.
   - *If Thesaurus:*
     a. Extract term concepts from sample content.
     b. Organize terms offline (e.g., via spreadsheet) by subject area.
     c. Import structured lists into taxonomy management software.
     d. Sequentially build out nonpreferred terms, scope notes, and cross-relationships (BT, NT, RT).

5. **Phase 5: User Testing & Validation**
   - Conduct Card Sorting (Open, then Closed) for top 2 levels if structural validation is needed.
   - Perform Indexing Test: Have users map sample content to the taxonomy. Identify gaps.
   - Perform Retrieval Test: Run sample queries. Analyze precision (ambiguity checks) and recall (depth checks).

6. **Phase 6: Governance Establishment**
   - Formalize the Taxonomy Design Plan into a Governance Document.
   - Establish ongoing maintenance schedules, change-request procedures, and an editorial style guide.

@Examples (Do's and Don'ts)

**Enterprise Content Audit**
- [DO]: Create a spreadsheet tracking: Content Name, Document Type (Category), Source Application, URL, Stakeholder, Organization, Taxonomy Term, and ROT status.
- [DON'T]: Perform an audit that includes transient emails, personal employee forms, and vendor receipts, or fail to track the source application.

**Taxonomy Creation Process (Hierarchical)**
- [DO]: Create a "straw-man" taxonomy consisting of only the top-level terms and a few sample second-level terms to present to stakeholders for early feedback before committing to a deep structure.
- [DON'T]: Build a complete 5-level hierarchical taxonomy in a vacuum and present it as a finished product to stakeholders without intermediate structural review.

**Card Sorting Application**
- [DO]: Set up an open card sorting exercise with exactly 40 second-level terms and ask users to group them and name the resulting 4 to 8 top-level categories.
- [DON'T]: Give users 500 terms spanning 5 levels of depth and ask them to sort them, or use card sorting to determine the structure of mutually exclusive top-level facets.

**Taxonomy Testing**
- [DO]: Test precision and recall by creating sample queries for known content within the repository and verifying that the correct documents (and only the correct documents) are returned.
- [DON'T]: Assume the taxonomy is functional just because the terms look logically structured in the taxonomy management software.

**Governance Documentation**
- [DO]: Define strict rules in the editorial style guide regarding capitalization, abbreviations, polyhierarchy limitations, and the specific process for how a user requests a new term.
- [DON'T]: Treat the taxonomy as a finished, static project upon deployment without assigning long-term maintenance roles or update procedures.