# @Domain
These rules MUST trigger when the AI is tasked with designing, analyzing, reviewing, or implementing a Developer Relations (DevRel) strategy, developer ecosystem plan, API marketing strategy, developer segmentation model, or developer funnel metric system. 

# @Vocabulary
- **Developer Ecosystem**: A virtual system of members that are collaborating, depending, and sometimes competing on the same platform, technology, or API.
- **The Hobbyist**: An early-adopter developer who explores edge cases and limitations for non-professional joy; prone to using APIs for unintended low-impact edge uses.
- **The Hacker**: An early-adopter professional/entrepreneur who seeks to put an API to practical use quickly; highly proficient, motivated by innovation, and tolerant of high learning curves without requiring heavy SDK/tooling support.
- **The Business-Focused, Tech-Savvy User**: A user focused entirely on solving a specific business use case (e.g., IT person, financial analyst); highly sensitive to breaking changes and reliant on accessible tools/services.
- **The Professional Developer**: A developer who evaluates an API based on product fit and maturity; willing to pay, highly sensitive to breaking changes, and reliant on SDKs and tools to save time.
- **Developer Funnel**: The documented journey a developer takes, consisting of four distinct stages: Aware, Proficient, Building, Successful.
- **Funnel Indicators**: Quantifiable metrics or milestones that reflect a developer's transition through the Developer Funnel.
- **Market Potential**: The long-term addressable size of a specific developer segment.
- **Short-Term Targets**: Time-boxed (e.g., quarterly) goals defined for specific funnel indicators.
- **Tactics**: Concrete actions and developer resources utilized to move developers through specific stages of the Developer Funnel.
- **Value Proposition**: A concrete, compelling, and validated statement articulating exactly why developers should use the API and what core problem it solves (distinct from consumer marketing "positioning").

# @Objectives
- To architect comprehensive developer ecosystem strategies that treat API adoption as a structured, measurable funnel.
- To enforce rigorous, multi-dimensional segmentation of developer audiences.
- To align actionable Developer Relations tactics strictly with their appropriate funnel stages (Awareness, Proficiency, Usage, Success).
- To establish data-driven feedback loops connecting tactics to specific Key Performance Indicators (KPIs).

# @Guidelines
- **Audience Segmentation Constraints**:
  - The AI MUST NEVER accept or propose "everyone" or "all developers" as a target audience.
  - The AI MUST segment developers using seven specific dimensions: Identity, Developer Proficiency, Platform of Choice, Preferred Development Language/Framework/Tools, Common Use Cases and Tasks, Preferred Means of Communication, and Market Size/Geographical Distribution.
  - The AI MUST categorize target audiences into recognized archetypes (Hobbyist, Hacker, Business-Focused, Professional) to dictate the required support materials.
- **Value Proposition Rules**:
  - The AI MUST formulate a Value Proposition focused on concrete benefits (e.g., "resizes images on the fly in under 10ms") rather than generic marketing fluff ("a slightly better way to manage images").
  - The AI MUST ensure the Value Proposition is directly tied to the defined "Common Use Cases" of the target segment.
- **Developer Funnel Structuring**:
  - The AI MUST map developer journeys using exactly four stages: 
    1. **Aware**: Developer knows about the API.
    2. **Proficient**: Developer knows how to use the API (e.g., achieves "Hello World").
    3. **Building**: Developer actively uses the API in pre-production/active development.
    4. **Successful**: Developer achieves their defined goal (e.g., production launch, generating revenue).
  - The AI MUST define distinct Funnel Indicators for each stage.
- **Current and Future State Mapping**:
  - The AI MUST generate metrics matrices containing: Current Monthly Status, Short-Term Targets (e.g., Q2 Goals), and Market Potential (total addressable market).
  - The AI MUST identify whether funnel indicators are direct (e.g., number of registered developers) or derived (e.g., volume of API calls based on usage).
- **Tactical Alignment Rules**:
  - The AI MUST strictly align tactics to the appropriate funnel stage.
  - *Awareness Tactics*: MUST include activities like ad campaigns, swag, event booths, open source contributions, or Product Hunt launches.
  - *Proficiency Tactics*: MUST include tutorials, code labs, SDKs, hackathons, whitepapers, or certification programs. The AI MUST NEVER classify hackathons as a tactic for revenue or production usage.
  - *Usage Tactics*: MUST include API registration systems, free tiers/coupons, design sprints, beta programs, or feedback loops.
  - *Success Tactics*: MUST include co-marketing, shared content writing, optimization workshops, or top developer highlight programs.
- **Measurement and KPI Constraints**:
  - The AI MUST link every proposed tactic to a specific KPI, tracking "Current", "Goal", "Expected Impact", and "Actual" metrics.
  - The AI MUST explicitly state that ecosystem building requires measuring, iterating, and improving based on actual KPI feedback.

# @Workflow
1. **Segment the Developer Audience**: Analyze the target user base using the seven required dimensions (Identity, Proficiency, Platform, Languages/Tools, Use Cases, Communication, Market Size).
2. **Distill the Value Proposition**: Define a concrete, compelling value proposition tied directly to the segment's primary use case.
3. **Map the Developer Funnel**: Establish the Aware, Proficient, Building, and Successful stages, and define concrete Funnel Indicators for each.
4. **Define State and Targets**: Document the Current State of indicators, project the Market Potential, and set Short-Term Targets.
5. **Formulate Tactics**: Select and assign targeted activities (Tactics) that logically move developers from one specific funnel stage to the next.
6. **Establish KPI Measurements**: Create a measurement matrix mapping every Tactic to an Expected Impact and a verifiable KPI.

# @Examples (Do's and Don'ts)

**Principle: Developer Segmentation**
- [DO]: "Target Segment: Enterprise internal developers. Proficiency: High in business logic, relies on Java/.NET and AWS. Communication: Prefers email newsletters. Market Size: 200,000 active devs globally."
- [DON'T]: "Target Segment: All developers who need to integrate messaging into their applications."

**Principle: Value Proposition Formulation**
- [DO]: "Value Proposition: Our API provides an out-of-the-box conversational framework that reduces Time-to-Hello-World for AI chatbots from 3 days to 15 minutes."
- [DON'T]: "Value Proposition: We are the leading, most synergistic messaging platform for modern developers."

**Principle: Tactical Alignment to Funnel Stages**
- [DO]: "Tactic for Proficiency: Host a 24-hour hackathon. Expected Indicator Impact: 1,000 developers successfully generate an API token and execute a test environment call."
- [DON'T]: "Tactic for Success: Host a 24-hour hackathon to drive $10,000 in new recurring revenue from enterprise production apps."

**Principle: Deriving Measurements**
- [DO]: "Measurement Plan - Tactic: Speak at SXSW. Target KPI: Website entries. Current: 10,000. Goal: 15,000. Expected Impact: 5,000 new developers visiting the landing page."
- [DON'T]: "Measurement Plan - Tactic: Speak at SXSW. Target KPI: Enhance developer goodwill and make people like our brand."