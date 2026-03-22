@Domain
These rules trigger when the AI is asked to synthesize content audit findings, draft a content strategy framework, create strategic content recommendations, build a content roadmap, or execute tasks related to the "Define Phase" of an enterprise content strategy project.

@Vocabulary
- **Define Phase**: The phase where the future content experience is defined based on insights from the assess phase, culminating in a content strategy framework and roadmap.
- **Content Strategy Framework**: A comprehensive document capturing gaps, issues, and opportunities within the current ecosystem alongside strategic recommendations and roadmaps for the future state.
- **Audit Findings and Implications**: The section of the framework that reports current-state realities and ties them to business or consumer impact.
- **Implication**: The specific consequence or impact an issue or gap has on the success of a solution, objective, or user experience.
- **Strategic Recommendation**: A concrete, future-state directive or solution designed to resolve an identified issue, gap, or redundancy.
- **Roadmap**: A phased timeline showing short-term (foundation/launch), near-term (evolution), and long-term (enrichment) projects and focus areas.
- **Quick Wins**: Process adjustments or updates that involve no system updates, minimal cost, and deliver immediate value.
- **Omnichannel Personalization**: Providing tailored content at every point in the customer journey across all channels, serving as a specific track or roadmap focus.

@Objectives
- Transform raw data from the assess phase (audits, inventories, interviews) into a cohesive, structured blueprint for the future-state content ecosystem.
- Frame all current-state issues and gaps objectively, respectfully, and empathetically, avoiding inflammatory or judgmental language.
- Connect every identified issue directly to a business or consumer implication.
- Connect every implication directly to an actionable strategic recommendation.
- Structure recommendations into phased, realistic roadmaps categorized by tracks (Technology, Content Experience, Analytics, Governance).

@Guidelines
- **Tone and Empathy Constraint**: The AI MUST draft all audit findings using value-neutral, objective, and empathetic language. The AI MUST NOT use judgmental descriptors (e.g., "horrible," "ugly," "completely unusable," "mess"). Acknowledge constraints and praise achievements where applicable.
- **Thematic Aggregation**: The AI MUST group audit findings by key themes (e.g., Accessibility, SEO, Content Quality) rather than generating exhaustive lists of individual errors. Minor details must be referenced as living in the audit spreadsheet.
- **Mandatory Finding Format**: For every identified issue, the AI MUST strictly format the output using the following four-part sequence:
  1. **Goal**: The desired benchmark, business objective, or marketing goal.
  2. **Finding**: The value-neutral statement of the issue.
  3. **Examples**: A few specific instances demonstrating the finding.
  4. **Implication**: The resulting negative impact on business objectives or consumer tasks.
- **Framework Structure**: When generating a Content Strategy Framework, the AI MUST use the following exact section hierarchy:
  - *Introduction*: Scope and purpose of the audit.
  - *Approach*: Methodologies used (e.g., interviews, CAT tool, heuristic analysis).
  - *Business Goals and Objectives*: Key project goals.
  - *Audit Findings and Implications*: Subdivided into Business/Marketing/Consumer Goals, Content Quality, Content Structure/Priorities, Accessibility Compliance, Content Lifecycle, Content Analytics, SEO/Taxonomy/Metadata, and Content Governance.
  - *Framework with Strategic Recommendations*: Subdivided to match the findings, detailing how the ecosystem must advance.
  - *Roadmaps*: Visual or tabular timelines for implementation.
- **Website Audit Taxonomy**: If the domain is a website, the AI MUST structure the audit report evaluating these specific areas: Home page, Product-category landing pages, Product landing pages, User-generated content, Social media, User profile, Corporate pages, Tools, Shopping cart, Campaign pages/banners, and Legal/copyright/privacy pages.
- **Highlighting Quick Wins**: The AI MUST explicitly flag recommendations that can be executed immediately with minimal cost and no system updates as "Quick Wins".
- **Roadmap Structuring**: The AI MUST structure roadmaps using a matrix of phases (e.g., Launch, 9–12 months post-launch, 18+ months post-launch) intersected by organizational tracks (e.g., Technology, Content Experience, Analytics, Governance).

@Workflow
1. **Input Ingestion**: Ingest and analyze assess-phase deliverables (business goals, content inventory spreadsheets, stakeholder interview notes, competitive analysis).
2. **Thematic Synthesis**: Identify macro-level issues, gaps, choke points, and redundancies. Group them into the required framework categories (Quality, Lifecycle, Governance, etc.).
3. **Draft Findings**: Write the "Audit findings and implications" section. Apply the strict 4-part format (Goal, Finding, Example, Implication) to every theme. Apply the tone constraint to ensure empathetic, neutral language.
4. **Draft Recommendations**: Write the "Framework with strategic recommendations" section. For every finding drafted in Step 3, write a corresponding recommendation that details the future-state design required to solve it. Identify and explicitly label "Quick Wins".
5. **Develop Roadmaps**: Extract the recommendations and distribute them across a phased timeline (Foundation, Evolution, Enrichment) categorized by tracks (Technology, Content, Analytics, Governance).
6. **Compile Framework**: Assemble Steps 1-5 into the final structured Content Strategy Framework document.
7. **Design Phase Transition**: Generate a concluding project plan brief detailing the requirements, dependencies, and resources needed to begin the "Design Phase" (e.g., wireframing, content modeling).

@Examples (Do's and Don'ts)

**Principle: Tone and Empathy in Audit Findings**
- [DO]: "Finding: The website does not currently support accessibility standards."
- [DON'T]: "Finding: The website is a complete disaster for accessibility and shows zero consideration for visually impaired users."

**Principle: Mandatory Finding Format**
- [DO]: 
  **Marketing goal**: Reach the maximum number of consumers and potential consumers with rich, relevant, timely content.
  **Finding**: The website does not support accessibility.
  **Examples**: Images on the home page, landing pages, and product pages lack alt text. Pages lack a structure to support accessibility.
  **Implication**: The site prevents people with disabilities such as visual impairment from using the site effectively, limiting audience reach and risking compliance issues.
- [DON'T]: 
  - Images are missing alt text on the homepage.
  - Landing pages don't have alt text.
  - Page structure is bad for screen readers.

**Principle: Roadmap Structuring**
- [DO]: 
  | Track | Phase 1: Launch (Foundation) | Phase 2: 9-12 Months (Evolution) | Phase 3: 18+ Months (Enrichment) |
  |---|---|---|---|
  | **Technology** | Implement new CMS | Integrate CRM with publishing tools | Expand publishing to offline materials |
  | **Content Experience** | Establish personas & content mapping | Test assumed customer journeys | Integrate true omnichannel in all channels |
- [DON'T]:
  - Implement new CMS
  - Integrate CRM
  - Establish personas
  (Anti-pattern: A simple bulleted list with no time phases or categorical tracks).

**Principle: Strategic Recommendations**
- [DO]: **Recommendation**: Create meaningful and relevant alt text for all images on the website. Include this work in the scope for future content creation, and create a workflow for this textual creation process that leverages SEO expertise as well. [QUICK WIN]
- [DON'T]: **Recommendation**: Fix the alt text.