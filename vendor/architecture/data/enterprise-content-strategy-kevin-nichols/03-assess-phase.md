# @Domain
These rules MUST trigger when the AI is tasked with any of the following activities: conducting a content strategy assessment, performing a current-state or discovery analysis, planning or generating stakeholder interview protocols, executing a content inventory (quantitative), executing a content audit (qualitative), performing competitive content analysis, or mapping current-state content lifecycles. 

# @Vocabulary
- **Assess Phase (Discovery Phase / Current-State Analysis):** The phase providing a holistic snapshot of an organization's content ecosystem, including business logic, lifecycles, taxonomy, competitors, governance, and content quality.
- **Content Inventory:** A quantitative exercise that answers the question: "What content, and how much content, do I have?"
- **Content Audit:** A qualitative exercise that answers the question: "Does that content meet my and my users’ needs?"
- **Content Ecosystem:** The total sum of business logic, content lifecycles, content organization (taxonomies/metadata), competitive treatment, social content, governance, and systems integration.
- **CAT (Content Analysis Tool):** An automated tool used to extract a preliminary content inventory, which MUST be manually verified.
- **M/D/R:** A qualitative assessment metric indicating if content will be Migrated (M), Deleted (D), or Revised (R).
- **Spider/Crawler:** An automated inventory application that the AI must never trust blindly without manual qualitative evaluation.
- **Quality Scale (E, G, S, P):** A prioritization scheme for content quality rating: Excellent (E), Good (G), Satisfactory (S), or Poor (P).

# @Objectives
- The AI MUST enforce a thorough, meticulous assessment of the current-state content ecosystem to serve as the blueprint for all future design decisions. 
- The AI MUST prevent the user from executing a "light" or "quick-fix" assess phase, warning that this will result in multimillion-dollar cost overruns or compromised future-state designs.
- The AI MUST treat Content Inventories (quantitative) and Content Audits (qualitative) as simultaneous, interconnected exercises.
- The AI MUST map the current-state content lifecycles and identify issues, gaps, redundancies, and choke points.
- The AI MUST enforce manual verification of all automated inventory tools.

# @Guidelines

### Assessment Timeframes & Scope
- The AI MUST mandate realistic timeframes for the Assess phase (8–12 weeks for large organizations; 4–6 weeks for smaller organizations).
- The AI MUST NOT allow the assess phase to be skipped or abbreviated, even if the project is agile or already underway.
- The AI MUST establish auditing criteria based on business goals before beginning the inventory/audit (e.g., "What constitutes success and good content?").

### Stakeholder Interviews
- The AI MUST structure stakeholder interview protocols into exactly these 11 categories:
  1. Business and project strategy
  2. Content inventory and scope
  3. Production and publication processes
  4. Technology
  5. Marketing strategy
  6. Analytics
  7. Content structure, including metadata and taxonomy
  8. Content experience
  9. Omnichannel and multichannel strategy
  10. Governance
  11. Entitlements
- The AI MUST recommend that interviews last 2 hours, be conducted with one person/line of business at a time, and that the protocol is sent in advance.

### Content Inventory & Audit Execution
- The AI MUST conduct the inventory and audit simultaneously.
- The AI MUST strictly require the following specific fields to be captured in the Content Inventory/Audit spreadsheet:
  - **Volume and Scope:** ID #, Document owner, Document title/topic, Level 2 subtopic (levels 2-X), Content type, Notable functionality, Description, URLs, Volume.
  - **Metadata and SEO:** HTML page title, Meta description, Meta keywords.
  - **Additional Aspects:** Doc format, Author, Last updated/published, Update frequency, CMS template.
  - **Business Rules:** Audience, Instances/variations, Rules for use, Channel.
  - **Qualitative Assessment:** High/medium/low priority, Redundancy, Quality (E, G, S, P), M/D/R (Migrate, Delete, Revise), Issues, Rating (numerical scale).
  - **Inputs/Outputs:** System inputs/sources, Channel outputs, Document inputs/sources, Document outputs.

### Automated Tools and Spiders Constraints
- The AI MUST explicitly warn against relying solely on spiders or inventory applications.
- When an automated tool (like CAT) is used, the AI MUST mandate manual verification to capture un-indexed content and perform the qualitative audit.

### Competitive & Industry Analysis
- The AI MUST conduct competitive analysis on external channels by answering: How do home pages show products/services/brand story? How is social-engagement integrated? How is video used? How are metadata/keywords treated?
- For internal portals, the AI MUST reference analyst reports (Alexa, Nielsen, Pew Internet, Comscore, Forrester, Gartner).

### Workflow & Lifecycle Documentation
- The AI MUST prompt the user to capture end-to-end lifecycle processes visually (using Visio or similar formats) using a workshop approach.
- The AI MUST mandate formal sign-off from all content owners on the final inventory and audit before progressing to any migration or design work. "Sign-off" strictly means the inventory captures *all* current-state content.

# @Workflow
1. **Define Scope & Criteria:** Establish the exact scope of the assessment (desktop, mobile, social, call center, internal portals) and define the evaluation criteria based on project/business goals.
2. **Conduct Stakeholder Interviews:** Generate the 11-category interview protocol and advise the user to schedule 2-hour sessions, sending the protocol in advance.
3. **Execute Simultaneous Inventory & Audit:** Generate a spreadsheet matrix containing the exact prescribed columns (Volume, Metadata, Business Rules, Qualitative, Inputs/Outputs). Import automated crawler data if available, but mandate manual qualitative evaluation and gap-checking.
4. **Perform Competitive Analysis:** Analyze competitor channels (home, landing, section, article pages) and industry reports to identify external content trends and gaps.
5. **Document Lifecycles:** Map out the current-state content lifecycles visually, noting issues, gaps, and redundancies uncovered during stakeholder interviews.
6. **Obtain Formal Sign-off:** Halt progression to the Define/Design phases until the AI explicitly prompts the user to secure formal sign-off from all content-owning stakeholders on the inventory and audit.

# @Examples (Do's and Don'ts)

### Content Inventory & Audit Structure
- **[DO]** Generate an inventory matrix with hyper-specific columns:
  `| ID # | Doc Owner | Content Type | URL | Meta Desc | Meta Keywords | Update Freq | Audience | Rule for Use | Quality (E/G/S/P) | M/D/R | Issues | Doc Inputs |`
- **[DON'T]** Generate a simplified, basic inventory:
  `| Page Name | URL | Keep/Delete | Notes |`

### Automated Tools Usage
- **[DO]** "I have imported the sitemap data from the Content Analysis Tool (CAT). Next, we MUST manually verify this list to identify hidden content the crawler missed, and manually assign a Quality (E,G,S,P) and M/D/R rating to each asset, as automated tools cannot assess content quality."
- **[DON'T]** "The spider has finished crawling the site. The inventory is complete. We can move on to the Define phase."

### Stakeholder Interview Questions
- **[DO]** Generate structured questions tailored to the 11 categories:
  *Content Structure (Metadata/Taxonomy):* "What taxonomies, metadata structures, or controlled vocabularies are in place? What tools are used to manage them? Do you use XML (e.g., DITA) to structure documents?"
- **[DON'T]** Ask vague, unstructured questions:
  "What do you think of the current website? What content do you want on the new site?"

### Assessment Phase Planning
- **[DO]** Allocate appropriate timeframes: "For an enterprise of this size, the Assess phase should be scheduled for 8 to 12 weeks to ensure a complete audit of all digital, print, and call-center content ecosystems."
- **[DON'T]** Rush the process: "Let's do a quick one-week content sweep so we can start designing the wireframes."