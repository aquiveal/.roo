@Domain
These rules MUST trigger when the user requests assistance with Information Architecture (IA) projects, navigation restructuring, online help structuring, document-management classification, knowledge-base categorization, software menu organization, or process step mapping. They specifically activate when planning, designing, executing, or analyzing a "Card Sort" user research activity.

@Vocabulary
- **Card Sorting**: A user research technique used to understand people's mental models, how they think about categories/concepts, how they describe them, and what information belongs together.
- **Open Card Sort**: A generative method where participants are given cards with content ideas and asked to group them however it makes sense to them, and then provide their own labels for those groups.
- **Closed Card Sort**: An evaluative method where participants are given content cards and asked to slot them into a pre-existing, predetermined set of categories.
- **Information Architecture (IA)**: The practice of organizing, grouping, and labeling items (often content) that other people must use.
- **Mental Model**: The internal, often idiosyncratic and highly personal way a user perceives connections and organization within a universe of information.

@Objectives
- The AI MUST treat card sorting primarily as a tool to understand the people being designed for, NOT as a definitive, automated method for creating a website's navigation.
- The AI MUST use card sorting to break internal project assumptions and gain a fresh, external perspective on content relationships.
- The AI MUST leverage open card sorts to extract user-generated vocabulary for labeling content groups.
- The AI MUST integrate card sorting as just ONE component of a broader research strategy, explicitly combining it with complementary techniques.

@Guidelines

**Project Timing & Prerequisites**
- The AI MUST NOT recommend conducting a card sort as the very first activity in a project.
- The AI MUST ensure that a baseline understanding of the project, the users, and the content is established BEFORE planning the sort. If the content is unknown, the AI MUST prompt the user to analyze the content first.
- The AI MUST use card sorting early in the process to explore broad questions about content groups, or later in the process to explore specific, detailed questions (e.g., small content sections, gathering additional labeling ideas).
- The AI MUST advise against running a card sort if the user already possesses sufficient research and a verified understanding of the required categorization.

**Methodology Selection**
- The AI MUST recommend an **Open Card Sort** when the goal is brainstorming models, exploring topic perceptions, and discovering lists of words users utilize to describe groups.
- The AI MUST recommend a **Closed Card Sort** ONLY to learn where users think content goes within an established structure.
- The AI MUST warn the user that a closed card sort DOES NOT test if users can *find* information. To test findability, the AI MUST recommend a task-based usability test instead.

**Card Creation & Facilitation Rules**
- The AI MUST instruct the user to create cards that have the content title clearly written on the front, with a couple of paragraphs of the actual content printed (or glued) on the back for context.
- The AI MUST encourage running team-based sorts (e.g., groups of three) to facilitate observable discussions, arguments, and consensus-building, which often yield more value than the final card piles.

**Data Interpretation & Application Rules**
- The AI MUST strictly prohibit taking the raw outputs of a card sort and directly copy-pasting them into a live navigation structure or IA.
- The AI MUST treat the results as "evidence" and "insights" to support design recommendations, looking for similarities and differences rather than a single "statistically significant" true answer.
- The AI MUST correlate card sort data with complementary research, specifically:
  - *Interviews*: To understand context, tasks, and information needs.
  - *Surveys*: To compare and contrast responses of large numbers of individuals.
  - *Analysis of Existing Info*: To cross-reference with website statistics, search terms (internal/external), customer emails, and help-desk logs.

@Workflow
1. **Prerequisite Verification**: Ask the user to confirm their understanding of the domain and the specific content to be sorted. If inadequate, halt and recommend content analysis or user interviews.
2. **Goal Definition**: Prompt the user to define exactly what they want to learn (e.g., brainstorming broad models, generating labels, or testing an existing set of categories).
3. **Method Selection**: Based on the goals, define the method: Open vs. Closed, face-to-face vs. remote, manual vs. software.
4. **Content Curation**: Generate the content for the cards. Ensure each item represents realistic content, featuring a clear title and a brief descriptive paragraph for the back of the card.
5. **Participant Planning**: Define the target participants. Strongly recommend recruiting real end-users and grouping them into teams (groups of 3 are optimal) to encourage verbal negotiation during the sort.
6. **Execution & Observation**: Instruct the user to record not just the final groupings, but the reasoning, vocabulary, and discussions that occurred during the sorting process.
7. **Multi-source Analysis**: Analyze the card sort results by cross-referencing the identified patterns and user-generated labels against search logs, website analytics, and interview data.
8. **IA Synthesis**: Propose a drafted Information Architecture that synthesizes these combined insights, explicitly documenting the rationale behind the groupings.

@Examples (Do's and Don'ts)

**Example 1: Translating Results to Navigation**
- [DO]: Analyze the user-generated card piles, extract the common terminology they used to label those piles, cross-reference those terms with internal search logs, and use the combined data to design a draft navigation menu.
- [DON'T]: Look at a user's completed card sort and say, "The user made 5 piles with these exact names; let's make these our 5 main website tabs immediately."

**Example 2: Testing Information Findability**
- [DO]: Give participants a scenario (e.g., "Where would you look to find a specific form?") and observe their navigation path to test the IA.
- [DON'T]: Run a Closed Card Sort and assume that because a user successfully slotted a card into the "Forms" category, they will easily find it in a real-world browsing scenario.

**Example 3: Project Timing**
- [DO]: Schedule the card sort after initial stakeholder interviews and a basic content audit, so you know exactly which ambiguous content areas need clarification.
- [DON'T]: Schedule a usability test and a card sort as the very first two activities on a new project, using an outdated sitemap to generate the cards.

**Example 4: Designing the Cards**
- [DO]: Create cards that say "Travel Allowance Rates" on the front, with two paragraphs explaining the policy on the back so the user understands the context.
- [DON'T]: Write vague single words on sticky notes without any supporting context, forcing the user to guess what the content actually represents.