# @Domain
This rule file MUST be triggered when the AI is tasked with performing a substantive audit of organizational requirements, identifying business pain points, preparing stakeholder interview scripts, analyzing D.O.S. (Dangers, Opportunities, Strengths), or aligning a unified content strategy with high-level corporate goals. 

# @Vocabulary
*   **Pain Point**: A specific area within an organization where content processes, tools, or technologies are failing, resulting in missed deadlines, inconsistent content, or customer complaints.
*   **D.O.S.®**: An analytical framework used to categorize an organization's Dangers, Opportunities, and Strengths.
*   **Dangers**: Potential or perceived threats reflecting the fear of losing competitive position, not meeting revenue, or missing opportunities.
*   **Opportunities**: Chances for improvement or growth that either arise from dangers or exist independently in the market.
*   **Strengths**: The existing positive capabilities, skills, and resources an organization can build upon to realize its opportunities.
*   **Senior Stakeholders**: C-level executives or directors who provide the broad-picture perspective on strategic goals and hold the authority to fund and sign off on content strategy projects.
*   **Success Factors**: The specific, measurable outcomes that define the successful implementation of the content strategy project.

# @Objectives
*   Identify and prioritize the organizational areas experiencing the most severe "pain" to maximize the initial return on investment (ROI) of the content strategy.
*   Synthesize a realistic organizational picture by combining the broad, strategic perspective of management with the specific, tactical pain points of departmental groups.
*   Secure executive support by rigidly aligning all proposed content strategies with documented corporate goals.
*   Clearly define the boundaries of the unified content strategy, explicitly excluding organizational problems that content cannot solve.

# @Guidelines
*   **Targeting Pain**: When proposing where to begin a unified content strategy, the AI MUST select the areas with the highest concentration of failing processes and management/customer complaints.
*   **Dual-Perspective Synthesis**: The AI MUST explicitly require and synthesize input from both C-level management (for overarching goals) and frontline content lifecycle groups (for specific functional pain).
*   **Executive Interview Constraints**: When generating interview scripts or schedules for Senior Stakeholders, the AI MUST:
    *   Limit the requested interview time to a maximum of 15 to 30 minutes.
    *   Require that questions be provided to the stakeholder in advance.
    *   Strictly prohibit the use of leading questions or drawing conclusions before the interview begins.
*   **D.O.S. Categorization**: The AI MUST extract organizational context and classify it strictly into Dangers (asking for the top three), Opportunities, and Strengths.
*   **Goal Alignment**: The AI MUST map every aspect of the proposed content strategy directly to tangible corporate or departmental strategic plans (e.g., 1-year, 2-year, or 5-year goals). Without this alignment, the AI MUST flag the strategy as lacking executive viability.
*   **Challenge Identification**: The AI MUST explicitly catalog anticipated challenges categorized by money, time, technology, and people, and mandate a mitigation plan for each.
*   **Strict Scope Bounding**: The AI MUST actively filter out organizational dangers or problems that a unified content strategy cannot solve (e.g., employee turnover, general HR issues, non-content product defects) and explicitly state that the strategy is only one piece of the corporate solution.

# @Workflow
When tasked with determining business requirements and identifying where an organization "hurts," the AI MUST execute the following algorithmic process:

1.  **Stakeholder Matrix Generation**: 
    *   Identify target interviewees, ensuring a mix of Senior Stakeholders (C-level/Directors) and content lifecycle participants.
2.  **Interview Script Compilation**: 
    *   Generate an interview prep document utilizing ONLY the following permitted base questions:
        *   *What are the business reasons behind this project?*
        *   *What problems do you hope to solve?*
        *   *What are the greatest dangers facing the organization right now?*
        *   *What do you believe are the opportunities available to the organization?*
        *   *What do you think your organization's greatest strengths are?*
        *   *What challenges do you think the organization may face bringing this project to success?*
        *   *What are the success factors for this project?*
3.  **D.O.S. and Goal Extraction**:
    *   Analyze provided organizational data or interview transcripts.
    *   Extract the top 3 Dangers.
    *   Extract actionable Opportunities.
    *   Extract organizational Strengths.
    *   Extract 1-to-5-year corporate Goals.
4.  **Scope Boundary Check**:
    *   Review the extracted Dangers and Problems.
    *   Identify and isolate any issues that are outside the scope of content creation, management, delivery, and customer communication.
    *   Label these as "Out of Scope for Content Strategy."
5.  **Strategy Alignment & Output Generation**:
    *   Map the valid pain points and opportunities to the corporate goals.
    *   Output a structured "Business Requirements & Pain Point Analysis" document containing EXACTLY the following headings:
        *   *Business goals of the project*
        *   *Problems to be solved*
        *   *Dangers*
        *   *Opportunities*
        *   *Strengths*
        *   *Challenges*
        *   *Success factors*

# @Examples (Do's and Don'ts)

**[DO] Format an Executive Interview Request Properly**
```markdown
**Interviewee:** Chief Marketing Officer
**Duration:** 20 Minutes
**Pre-Meeting Action:** Questions provided 3 days in advance.

**Questions:**
1. What are the business reasons behind this content project?
2. What are the top three greatest dangers facing the organization right now if we do not meet our goals?
3. What do you believe are the opportunities available to the organization?
```

**[DON'T] Format an Executive Interview Request Incorrectly**
```markdown
**Interviewee:** Chief Marketing Officer
**Duration:** 60 Minutes (Anti-pattern: Too long for C-level)
**Pre-Meeting Action:** None. (Anti-pattern: Questions must be provided in advance)

**Questions:**
1. Don't you agree that our current CMS is causing us to lose money? (Anti-pattern: Leading question)
2. How can we fix the high employee turnover in the engineering department? (Anti-pattern: Out of scope for content strategy)
```

**[DO] Categorize D.O.S. and Scope Boundaries Properly**
```markdown
### Problems to be solved
* Content is manually reused in 48 different places, causing severe inconsistencies when updates are required.
* We cannot support requests for customized content without incurring massive manual labor costs.

### Dangers
* [IN SCOPE] Competitors are delivering content to mobile devices faster than we can, risking customer churn.
* [OUT OF SCOPE] The new factory location is experiencing supply chain delays for raw physical materials. (Note: Unified content strategy will not solve this).

### Strengths
* Highly dedicated subject matter experts trusted by the industry.

### Challenges
* Time constraints due to a small team; implementing new processes must not disrupt daily operations.
```

**[DON'T] Mix Non-Content Goals into the Strategy**
```markdown
### Goals of the Content Strategy
* Publish effective eBooks.
* Improve website navigation.
* Renegotiate our real estate lease for the downtown office. (Anti-pattern: Content strategy cannot solve real estate or facility issues).
```