# @Domain
This rule file is activated when the AI is tasked with generating, structuring, or reviewing documentation, reports, summaries, or deliverables based on card sorting activities or categorization-based user research. It applies to tasks involving the communication of research findings to internal teams, stakeholders, or clients.

# @Vocabulary
- **Documentation**: The formal process of writing down the findings of a card sort, strictly serving to justify findings, give legitimacy to the process, share learnings, and provide transparency for future design decisions.
- **Bare-Bones Report**: The least detailed level of documentation. A basic, rapid-delivery record of what occurred during the card sort without in-depth analysis, aimed at internal teams or colleagues.
- **Detailed Report**: The intermediate level of documentation. Builds upon the Bare-Bones Report by providing deep interpretation of the results and concrete, data-backed recommendations.
- **Comprehensive Report**: The highest level of documentation. A highly polished deliverable, typically for clients or external stakeholders, that situates the card sort within the broader context of all user research activities.

# @Objectives
- **Force Justification**: The AI must ensure that every conclusion written in the documentation is strictly supported by the actual card sort data. 
- **Establish Legitimacy**: The AI must structure reports to demonstrate that the methodology was well-thought-out and rigorous.
- **Facilitate Sharing**: The AI must format documentation so that the insights can be easily understood and accurately represented by third parties who did not attend the card sort.
- **Provide Transparency**: The AI must clearly link final design recommendations back to the specific data points or participant behaviors that inspired them.
- **Tailor Detail to Context**: The AI must adapt the depth of the report to the specific audience, available time, and project complexity.

# @Guidelines

### General Documentation Rules
- The AI MUST explicitly ask the user to define the target audience and communication goals before drafting any card sort documentation.
- If a user states that documentation is unnecessary because the insights are already known, the AI MUST briefly advocate for creating at least a Bare-Bones Report to ensure transparency, shareability, and justification of decisions.
- The AI MUST cross-check all drafted conclusions against the provided raw data. If a conclusion is unsupported, the AI MUST revise or remove it.

### Level 1: Bare-Bones Report Execution
- When the user requests a quick summary, an internal wrap-up, or a basic record, the AI MUST generate a Bare-Bones Report.
- The AI MUST NOT include deep interpretation or extensive analysis in this report level.
- The AI MUST include EXACTLY the following sections:
  1. **Background**: A brief explanation of what card sorting is and what it helps achieve.
  2. **Goals**: The specific reasons this card sort was run and the intended achievements.
  3. **Demographics**: The exact number of participants involved and the recruitment methodology.
  4. **Methodology**: A description of how the card sort was administered (e.g., open/closed, remote/in-person, software/physical).
  5. **Data Summary**: A summary table of the raw data.
  6. **Consistencies & Inconsistencies**: A high-level summary of the most prominent patterns found in the data.
  7. **Key Insights**: Bullet points highlighting the most important takeaways.
  8. **Data Reference**: A direct link, appendix, or reference to the full, raw results.

### Level 2: Detailed Report Execution
- When the user requires actionable design changes, interpretation of user behavior, or is presenting to decision-makers, the AI MUST generate a Detailed Report.
- The AI MUST include ALL elements of the Bare-Bones Report.
- Additionally, the AI MUST include EXACTLY the following interpretive sections:
  1. **Issue Summary & Recommendations**: An executive summary of key issues identified during the sort and actionable recommendations to solve them.
  2. **Group Breakdown**: A detailed list of the categories/groups created by participants, explicitly listing the most common cards placed in each group.
  3. **Terminology Variations**: A qualitative list showing the different words or phrases participants used to describe similar conceptual groups.
  4. **Issue Analysis**: A deep-dive interpretation of *why* specific issues or unexpected groupings occurred.
  5. **Data-Backed Recommendations**: A granular list of structural or labeling recommendations, explicitly citing the specific data points that back up each decision.

### Level 3: Comprehensive Report Execution
- When the user is working as a consultant, delivering a final milestone, or presenting to executive clients, the AI MUST generate a Comprehensive Report.
- The AI MUST include ALL elements of the Detailed Report.
- The AI MUST apply a high level of professional polish to the tone and formatting.
- Additionally, the AI MUST include EXACTLY the following contextual sections:
  1. **Cross-Research Synthesis**: Explicit connections showing how information from other user research activities (e.g., interviews, analytics) either supports or contradicts the card sort findings.
  2. **Deep Qualitative Analysis**: Extensive analysis of participant quotes, spatial sorting behaviors, and session observations.
  3. **Project Application**: A definitive explanation of exactly how the card sort outcomes will be (or have been) implemented in the final project deliverables.

# @Workflow
When tasked with documenting a card sort, the AI MUST execute the following algorithm:
1. **Audience Assessment**: Query the user regarding the intended audience (e.g., internal team vs. external client), the complexity of the project, and the time available for reporting.
2. **Level Selection**: Based on Step 1, explicitly state which documentation level (Bare-Bones, Detailed, or Comprehensive) will be applied.
3. **Data Ingestion**: Ingest and review the raw card sort data, participant quotes, and methodology details provided by the user.
4. **Justification Check**: Map every planned insight or recommendation directly to a piece of ingested data. Discard any insights lacking data support.
5. **Drafting Foundation (Level 1)**: Draft the 8 required sections of the Bare-Bones Report. Stop here if Level 1 was selected.
6. **Drafting Interpretation (Level 2)**: Draft the 5 interpretive sections required for the Detailed Report. Stop here if Level 2 was selected.
7. **Drafting Context & Polish (Level 3)**: Draft the 3 contextual sections required for the Comprehensive report, integrating secondary research data.
8. **Final Validation**: Review the entire document to ensure tone matches the audience and that transparency/legitimacy objectives are met.

# @Examples (Do's and Don'ts)

### Principle: Forcing Justification of Findings
- **[DO]**: "Recommendation: Create a top-level category named 'Pay and Benefits'. Justification: 85% of participants grouped 'Salary', 'Leave', and 'Health Insurance' together, and 12 out of 20 teams specifically used the label 'Pay and Benefits'."
- **[DON'T]**: "Recommendation: Create a top-level category named 'Pay and Benefits' because it seems like the most logical way to structure the employee portal." *(Anti-pattern: Making a recommendation based on personal assumption rather than forcing justification from the data).*

### Principle: Appropriate Level Selection (Bare-Bones)
- **[DO]**: "To keep the internal team updated quickly, here is a Bare-Bones summary: We tested 15 users. The most consistent pattern was grouping all 'IT Help' cards together. Full raw spreadsheet is attached."
- **[DON'T]**: "Here is the quick update for the devs: [Proceeds to write a 10-page analysis of the psychological reasons participants struggled with the word 'Network', cross-referencing it with three other ethnographic studies]." *(Anti-pattern: Providing Comprehensive-level qualitative analysis when a Bare-Bones record was required for internal speed).*

### Principle: Interpreting Issues in a Detailed Report
- **[DO]**: "Issue Analysis: Participants frequently placed theoretical papers into the 'Case Studies' group. Interpretation: 'Case Studies' was likely used as a 'Miscellaneous' bucket for items with ambiguous titles, rather than a strict grouping of real-world examples."
- **[DON'T]**: "Users put theoretical papers into 'Case Studies'. Therefore, we should put theoretical papers into the 'Case Studies' folder on the live website." *(Anti-pattern: Failing to interpret *why* an error occurred, resulting in the blind adoption of flawed user groupings).*