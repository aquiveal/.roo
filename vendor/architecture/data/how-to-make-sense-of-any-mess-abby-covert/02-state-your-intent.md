# @Domain

These rules MUST activate whenever the AI is tasked with project initiation, requirements gathering, defining project scope, establishing architectural or design directions, formulating strategic plans, resolving stakeholder or user misalignments, or translating abstract ideas into concrete project specifications.

# @Vocabulary

*   **Intent**: The deliberate effect or outcome we want to have on something, established through precise language choices.
*   **Language**: Any system of communication that exists to establish shared meaning; the foundational material of intent.
*   **Homograph**: A term that has different meanings depending on its specific situation or context (e.g., "pool").
*   **Perception**: The highly subjective process of considering and interpreting something.
*   **Good**: A subjective, context-dependent state of success or quality that MUST be explicitly defined for both stakeholders and users.
*   **Users**: The people who interact with the end product or process (e.g., customers, the public).
*   **Stakeholders**: People with a viable, legitimate interest in the work (e.g., colleagues, partners, superiors, clients).
*   **Why**: The foundational reason or motivation for undertaking a task or creating change.
*   **What**: The specific vision, parameters, and abilities required to address the "Why."
*   **How**: The varying tactical directions, methods, and implementation details chosen to execute the "What."

# @Objectives

*   **Establish Shared Meaning**: The AI must eliminate ambiguity by defining specific terminology and acknowledging that perception is subjective.
*   **Define "Good"**: The AI must categorically define what constitutes a "good" outcome for the specific project, users, and stakeholders before writing code or designing systems.
*   **Sequence Intent Properly**: The AI must mandate the establishment of *Why* the work is being done and *What* is being made before deciding *How* it will be implemented.
*   **Balance Aesthetics and Utility**: The AI must separate "looking good" from "being good," ensuring underlying architectural utility is never masked by superficial aesthetics.
*   **Materialize Intent via Constraints**: The AI must use language to create explicit boundaries—defining not only what a project *is*, but explicitly what the project *is walking away from*.

# @Guidelines

*   **The Language-Constraint Rule**: When proposing a project direction or design, the AI MUST explicitly state the alternative directions being abandoned. (e.g., "By choosing a highly secure architecture, we are walking away from frictionless, anonymous onboarding").
*   **The Homograph Warning**: The AI MUST flag words that could hold multiple meanings across different stakeholder groups and force explicit definitions for the current context.
*   **The Subjectivity of "Good" Rule**: The AI MUST NEVER assume an objective standard of "good." The AI MUST prompt the user to define what "good" means for the specific lifecycle stage (e.g., 7 weeks vs. 7 years) and the specific target audience.
*   **The Beauty vs. Quality Mandate**: When evaluating a system or design, the AI MUST assess "being good" (utility, architecture) completely independently of "looking good" (aesthetics, UI). The AI MUST flag instances where pretty interfaces hide poor logical architecture.
*   **The Telephone Game Prevention Protocol**: To prevent meaning from getting lost in translation, the AI MUST document the intended meaning of core project concepts in a centralized, easily accessible format before proceeding to technical implementation.
*   **The "Who Matters" Constraint**: Before making any strategic decision, the AI MUST explicitly identify the intended users and stakeholders, assessing their expectations, their openness to change, and how the current state appears to them.
*   **The "Start With Why" Protocol**: The AI MUST NOT generate implementation code or structural diagrams until the fundamental "Why" has been established (Why does this matter? Why is change needed?).
*   **The "What Before How" Directive**: The AI MUST define the vision, the current reality, and historical precedents ("What") before listing technical options, libraries, or architectural directions ("How").
*   **The Neutral Adjective Constraint**: When defining intent via adjectives, the AI MUST rigorously separate adjectives into two lists: "Desired" and "Acceptable not to be." The AI MUST ensure all adjectives used in this exercise are strictly neutral—avoiding inherently negative words like "slow," "bad," or "ugly."

# @Workflow

When establishing the intent and direction for a new project, feature, or system, the AI MUST execute the following algorithmic steps in rigid order:

1.  **Identify Who Matters**:
    *   List all key groups: Who is most important to get agreement from? Who is most important to serve?
    *   Identify potential emotional triggers: What words might make them defensive or put them at ease?

2.  **Establish the "Why"**:
    *   Document the precise reason the work needs to be done.
    *   Document why change is needed and why it matters to the target audience.
    *   Document past failures or attempts, and explain why this attempt will be different.

3.  **Establish the "What"**:
    *   Define the vision for the future.
    *   Assess the quality of the current state.
    *   Analyze historical context: What has been done before? What can be learned from past failures/successes?

4.  **Explore the "How" (Options)**:
    *   Generate a comprehensive list of implementation options.
    *   For each option, evaluate: Time/effort required, potential look/feel, production method, maintenance strategy, and success measurement metrics.

5.  **State the Intent (The Adjective Exercise)**:
    *   Step 5a: Generate a list of 3-5 neutral adjectives that users *should* use to describe the end product.
    *   Step 5b: Generate a list of 3-5 neutral adjectives that the project is *okay with NOT being described as*.
    *   Step 5c: Verify that the lists do not repeat, do not directly contradict/oppose each other, and contain NO inherently negative words. A third-party reader should not be able to guess which list is the "desired" list vs the "acceptable not to be" list.

6.  **Define "Good"**:
    *   Synthesize the findings from Steps 1-5 into a concrete, context-specific definition of what constitutes a "good" outcome for this specific project and audience.

# @Examples (Do's and Don'ts)

### Defining Intent via Adjectives
*   **[DO]**:
    *   *Intended Adjectives*: Professional, Comprehensive, Structured.
    *   *Okay with NOT being*: Playful, Lightweight, Spontaneous.
    *(Note: Both lists contain neutral, valid design adjectives. Neither is inherently "bad", but they clarify the exact intent by showing what is being sacrificed).*
*   **[DON'T]**:
    *   *Intended Adjectives*: Fast, Beautiful, Good.
    *   *Okay with NOT being*: Slow, Ugly, Bad.
    *(Note: Violates the neutral adjective constraint. Includes negative adjectives. Makes it obvious which list is "positive", failing the intent-clarification test).*

### Sequencing Why, What, and How
*   **[DO]**:
    *   *Why*: Our content is currently unsearchable, causing user frustration and abandoning the platform.
    *   *What*: We need a centralized, organized repository of articles with a clear taxonomy.
    *   *How*: We will implement an ElasticSearch backend with a faceted React frontend.
*   **[DON'T]**:
    *   *Intent*: We need to build an ElasticSearch React app (How) because it's fast (What) and the CEO wants it (Why).
    *(Note: Jumps straight to the "How", applies subjective/undefined terms like "fast", and uses a weak "Why" that will not sustain project momentum).*

### Defining "Good"
*   **[DO]**: "For this internal administrative dashboard, 'good' means high data density, keyboard-navigable tables, and zero latency on filtering. We are willing to sacrifice visual white-space and modern animations to achieve this."
*   **[DON'T]**: "The dashboard needs to be good, user-friendly, and look sleek."
    *(Note: Uses undefined subjective terms ("user-friendly", "sleek") and fails to establish a shared meaning of "good" based on the specific context of internal administrative tools).*

### Handling "Beauty vs. Quality"
*   **[DO]**: "The proposed UI mockups are visually appealing (looking good), but the underlying user flow requires 6 clicks to complete a basic checkout, and the error states are undocumented (failing at being good). We must revise the architecture before approving the visual design."
*   **[DON'T]**: "The new UI looks amazing and the color palette is perfect. Let's start building it immediately."
    *(Note: Falls victim to pretty things lying; fails to go deeper to question the actual utility and architectural soundness of the design).*