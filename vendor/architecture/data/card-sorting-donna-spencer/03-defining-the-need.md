# @Domain

This rule file is triggered whenever the AI is tasked with planning, scoping, initiating, or consulting on a card sorting activity, information architecture (IA) project, or categorization research. It specifically activates when determining the purpose, scale, target audience, and analytical approach of the research before any tactical execution (like creating cards or recruiting) begins.

# @Vocabulary

*   **Written Goal State:** A mandatory documentation artifact containing two distinct parts: 1) What specifically needs to be learned, and 2) Exactly how that information will be applied to the project.
*   **Broad Ideas Sort:** A card sort used for large, unfamiliar domains to learn how people think about content and how they describe it. Characterized by broad topics and face-to-face team sessions.
*   **On-Track Sort:** A validation sort used to confirm that the creator's intuitive organization makes sense to others. Characterized by small participant numbers and subset content.
*   **Detailed Exploration Sort:** A deep-dive sort focusing on a small, specific section of content with high granularity. Characterized by high participant counts, remote/online tools, and dual analysis (exploratory and statistical).
*   **Comparative Sort:** A sorting activity designed to identify differences in mental models between distinct user segments, demographics, or languages. Characterized by massive participant pools and strict statistical comparison.
*   **Justification Sort:** A sort driven by political or organizational need to convince skeptical stakeholders or managers. Characterized by artificially doubled participant counts and rigorous statistical analysis upfront.
*   **Actionable Goal Mapping:** The translation of abstract user behaviors (e.g., "Users distinguish events from regular classes") into concrete design decisions (e.g., "Separate top-level navigation for 'Activities' and 'Going Out'").

# @Objectives

*   The AI MUST prevent the user from executing tactical card sorting steps (method selection, card creation, recruitment) until a precise, documented need is established.
*   The AI MUST map the user's stated problem to one of the five specific card sorting archetypes (Broad, On-Track, Detailed, Comparative, Justification).
*   The AI MUST dictate the architectural parameters of the sort (participant scale, analysis method, content granularity) directly based on the chosen archetype.
*   The AI MUST force the explicit documentation of the "Written Goal State" to ensure the sorting data will directly impact project decisions.

# @Guidelines

*   **Archetype Constraint Enforcement:** The AI MUST enforce the following structural constraints based on the identified need:
    *   *If the need is "Learn Broad Ideas":* The AI MUST recommend face-to-face team card sorts, use broad topics instead of detailed pages, and prioritize qualitative discussion tracking over actual card placement.
    *   *If the need is "Check You're On Track":* The AI MUST constrain the scope to a small number of participants (e.g., 5-6), use a limited subset of basic content, and restrict analysis to simple exploratory validation. Statistical analysis MUST NOT be recommended.
    *   *If the need is "Explore an Idea in Detail":* The AI MUST recommend a large participant pool (e.g., 30+), use granular/detailed content cards, and mandate planning for *both* exploratory and statistical analysis upfront.
    *   *If the need is "Compare People":* The AI MUST require highly scaled participant counts distributed evenly across the target audiences, and mandate rigorous statistical analysis to identify divergences between groups.
    *   *If the need is "Justify a Recommendation":* The AI MUST double the standard calculated participant count and prepare statistical analysis formatting upfront, even if the AI determines qualitative analysis would technically suffice.
*   **Goal Extraction Protocol:** The AI MUST interrogate the user/client to move beyond generic statements ("We should run a card sort"). The AI MUST ask: "What do you really want to learn, and what will you do with that information?"
*   **Common Goals Alignment:** The AI MUST align the user's project with one of the following validated goals:
    *   Determine top-level categories and subcategories.
    *   Identify high-level concepts and relationships within content.
    *   Demonstrate to internal authors/stakeholders that external users think differently.
    *   Determine if a single classification scheme or multiple schemes are needed.
    *   Diagnose why a specific existing website section is failing.
    *   Harvest organic user vocabulary for navigation labels.
*   **Mental Model Mapping:** When analyzing goals, the AI MUST explicitly design the sort to uncover the users' mental models (e.g., detecting if users group by concrete nouns rather than abstract concepts, or by schedule-type rather than category-type), ensuring the design relies on user reality rather than organizational structures.
*   **Anti-Pattern Avoidance:** 
    *   The AI MUST NOT allow a card sort to proceed as the *only* user research method if the goal is "Checking You're On Track"; it MUST recommend complementary methods.
    *   The AI MUST NOT allow a large-scale statistical sort for a simple "Checking You're On Track" goal.

# @Workflow

1.  **Halt Execution:** If the user requests to create cards, pick software, or recruit users, the AI MUST halt and initiate the "Need Definition" phase.
2.  **Elicit the Goal:** Ask the user to explicitly define the project challenges and what they hope to extract from the users.
3.  **Identify the Archetype:** Analyze the user's response and categorize the need into one of the five archetypes: Broad Ideas, On-Track, Detailed Exploration, Compare People, or Justify Recommendation.
4.  **Draft the Written Goal State:** Generate a two-part statement for user approval containing:
    *   *Learning Objective:* (e.g., "Learn whether our three audience groups categorize train travel information differently.")
    *   *Application Plan:* (e.g., "Use this information to decide whether to build a unified global navigation or three audience-specific portals.")
5.  **Configure Parameters:** Based on the approved archetype, output the exact parameters required for the sort:
    *   Target participant volume.
    *   Content granularity (broad topics vs. detailed items).
    *   Recommended environment (face-to-face team vs. remote individual).
    *   Required analysis preparation (Exploratory only vs. Exploratory + Statistical).
6.  **Finalize Definition:** Lock these parameters as the foundational constraints for all subsequent card sorting prompts in the session.

# @Examples (Do's and Don'ts)

**Principle: Documenting the Written Goal State**
*   [DO]: "Goal State Defined: 1) We want to explore whether there is one main classification scheme for the HR portal or multiple. 2) We will use this information to decide whether to offer HR information strictly by 'Life Event' or provide cross-linked faceted navigation."
*   [DON'T]: "Goal State Defined: We need to do a card sort to figure out the HR portal."

**Principle: Matching the Scale to the Need (On-Track vs. Detailed)**
*   [DO]: "Since you are just checking if your draft structure for the conference site is on track, we will only need 5 participants and a small subset of the basic conference info cards. We will only use exploratory analysis."
*   [DON'T]: "To check if your draft conference site structure is on track, we need 30 participants doing an online sort, and we will run a statistical cluster analysis on all 99 pages."

**Principle: Justifying a Recommendation**
*   [DO]: "Because your management team consists of scientists who are highly skeptical of the redesign, we must run a 'Justification Sort'. I am doubling the recommended participant count and we must format the data for statistical analysis (dendrograms/cluster analysis) to provide undeniable quantitative proof."
*   [DON'T]: "Since management doesn't believe the staff gets confused by the intranet, let's just get 5 people in a room to group cards so we have some qualitative quotes to show them."

**Principle: Discovering Mental Models (Case Study Application)**
*   [DO]: "Goal: Determine how young people conceptualize their schedules. Strategy: Include cards with both abstract terms ('Culture') and concrete terms ('Rock Concert') to see if they categorize by field, or by time-commitment (spontaneous vs. planned in advance)."
*   [DON'T]: "Goal: Find out where young people put 'Culture'. Strategy: See if they put 'Rock Concert' under 'Culture'."