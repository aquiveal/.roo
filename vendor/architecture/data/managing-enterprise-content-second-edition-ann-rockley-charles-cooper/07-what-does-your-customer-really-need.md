@Domain
This rule file is triggered whenever the user requests assistance with audience analysis, customer research, user profiling, content strategy planning, persona generation, usability testing frameworks, or any task related to identifying and serving customer needs for information products and enterprise content.

@Vocabulary
*   **Internal Customers:** Individuals within the organization who use content to assist them in doing their jobs, making decisions, and supporting external customers.
*   **External Customers:** Individuals outside the organization, including end-users, prospects, original equipment manufacturers (OEMs), value-added resellers (VARs), stakeholders, and partners.
*   **Needs Assessment:** The formal or informal process of determining exactly what content customers require, how they access it, and what their goals are.
*   **Information Product:** Any packaged piece of content used by a customer, such as a website, mobile site, user guide, help file, mobile app, or eBook.
*   **Contextual Delivery:** The practice of delivering content in a format and location that is completely compatible with the user's physical or digital context (e.g., physical stickers on a shop floor instead of an intranet page).
*   **Usability Testing (Content):** Defining a scenario and assigning tasks to observe how customers navigate an information product, where they get stuck, and what questions remain unanswered.
*   **Persona:** A highly detailed profile of a typical customer written as a description of a real person, including a name, picture/visual description, detailed history, personality type, and a specific set of goals that drive design decisions.
*   **Free-text Questions:** Survey questions that allow open-ended typing, which are inherently difficult to analyze and score.
*   **Scored Questions:** Survey questions that ask customers to rate or rank items, making data easy to measure, chart, and use for business arguments.

@Objectives
*   The AI MUST prevent the restructuring or creation of content without first establishing a deep, verifiable understanding of the customer's needs and identifying existing content gaps.
*   The AI MUST categorically eliminate assumptions about the customer by forcing the cross-referencing of existing knowledge across disparate organizational silos (Marketing, Sales, Customer Service, Analytics).
*   The AI MUST ensure all content design and strategy decisions are explicitly tethered to the defined goals of a specific, realistic user Persona.
*   The AI MUST optimize the method of information gathering, preferring quantifiable survey data and context-appropriate usability tests over disruptive or vague data collection methods.

@Guidelines

**1. Fundamental Customer Identification Rules**
*   The AI MUST categorize all target audiences into either Internal Customers or External Customers.
*   The AI MUST answer or prompt the user to answer the following nine criteria for any content strategy:
    1.  What are the defined customer categories?
    2.  What specific content does each category use, and when do they use it?
    3.  How does the content differ between customer groups (where and why)?
    4.  How do customers currently access the content?
    5.  How do customers *prefer* to access the content?
    6.  What content is "need to know" versus what is "nice to know"?
    7.  At what level of detail do customers want the content? Do they want to switch between top-level overviews and deep details?
    8.  What are the customers' overarching interests in the content?
    9.  What are the customers' specific goals when using the content?

**2. Leveraging Existing Information Rules**
*   When synthesizing customer profiles, the AI MUST simulate or request inputs from the following specific departments using these exact queries:
    *   *Marketing:* Who are the primary/secondary customers? Where do they come from (region, search engine)? What platform do they use? What must they know to make a buying decision? What are the most effective reach methods?
    *   *Sales:* What are the primary/secondary customers experiencing pain? What content is needed for proposals (unique vs. reusable)? What specific collateral do sales reps point customers to?
    *   *Customer Service:* Who do *you* think the customers are (to uncover hidden audiences)? What are the most common questions/problems? What specific content makes callers happy or successfully solves their issues?
    *   *Web Analytics:* What are the entry/exit pages? What are the navigation paths? What keywords are used? What is the frequency and recency of visits?

**3. Gathering New Information Rules**
*   *Surveys:* The AI MUST recommend scored/quantifiable questions over free-text questions. The AI MUST explicitly forbid continuous, repetitive pop-up surveys that annoy customers. The AI MUST suggest incentives for email surveys and automated "thank you" responses.
*   *Usability Testing:* The AI MUST NOT treat usability testing as just "software testing." The AI MUST define a specific scenario, assign information-seeking tasks, and mandate the observation of navigation blockers and unanswered questions.
*   *Social Media:* The AI MUST track conversations across blogs, Twitter, Facebook, and LinkedIn to capture organic customer feedback.

**4. Persona Generation Rules**
*   The AI MUST NOT generate vague, generic, or demographic-only customer segments.
*   The AI MUST generate Personas that include:
    *   A specific Name.
    *   A visual description or placeholder for a picture.
    *   A detailed history/background (e.g., job role, daily commute, family life, specific challenges).
    *   A rigidly defined set of Goals (e.g., "Keep blood sugars under control", "Lose 10-15 lbs").
*   The AI MUST explicitly state how the generated Persona's goals dictate the proposed content design.

**5. Contextual Delivery Constraints**
*   The AI MUST evaluate the physical environment of the customer when recommending a delivery channel. (e.g., If the user is on a factory floor without desk access, the AI MUST NOT recommend an intranet portal; it MUST recommend offline, physical, or mobile contextual delivery).

@Workflow
When tasked with evaluating customer needs or defining a content strategy audience, the AI MUST strictly follow this step-by-step algorithm:

1.  **Define the Audience Taxonomy:** Map out all potential readers, explicitly dividing them into Internal Customers and External Customers.
2.  **Audit Existing Knowledge:** Generate a gap-analysis questionnaire targeting Marketing, Sales, and Customer Service. Extract known data regarding platforms, pain points, proposal needs, and analytics (entry/exit pages, keywords).
3.  **Propose a New Data Gathering Plan:** If gaps exist, select the appropriate method:
    *   Design a non-intrusive, incentive-driven, scored survey.
    *   Draft a usability test plan defining 3 specific scenarios and tasks for an existing Information Product.
    *   Draft a social media listening script.
4.  **Construct Personas:** Synthesize the data into 1-3 distinct Personas. Assign names, rich backgrounds, and 3-5 concrete, actionable goals for each.
5.  **Map Content to Context:** For each Persona, map their "need to know" content against their physical/digital context to determine the optimal delivery mechanism and level of detail.
6.  **Validate against Goals:** Perform a final check to ensure every proposed piece of content directly serves a specific Persona's defined goal.

@Examples (Do's and Don'ts)

**Principle: Persona Generation**
*   [DO] "Persona: Sharon Stockla. 30-something HR manager and mother of two. Recently diagnosed with Type 2 diabetes. Has a 2-hour daily commute and attends kids' soccer games on weekends. Passed out at a game due to poor concession food. Goals: 1. Keep blood sugars under control. 2. Lose 10-15 lbs. 3. Get energy back."
*   [DON'T] "Target Audience: Diabetic Women. Age 30-45. Middle income. Wants to be healthier." (Anti-pattern: Impersonal, generic demographic data lacking specific history and actionable goals).

**Principle: Usability Testing for Content**
*   [DO] "Usability Test Plan for GI Database: Scenario: You are at the grocery store trying to decide between two types of rice. Task: Use the mobile site to find the GI index of Basmati rice versus Jasmine rice. Observation: Note if the user has to scroll excessively, if they use the search bar, and if the table formatting breaks on their device screen."
*   [DON'T] "Usability Test Plan: Ask the user to click around the website and tell us if they like the colors and if the pages load fast." (Anti-pattern: Lacks specific scenario, task, and content-focused observation).

**Principle: Survey Design**
*   [DO] "We will email a customized URL to our top 100 enterprise customers offering a chance to win a tablet. The survey will use a 1-5 scoring system to rate the usefulness of our API documentation, minimizing free-text fields to ensure data can be easily charted."
*   [DON'T] "We will implement a pop-up survey that triggers every time a user downloads a PDF, asking 'What did you think of this document?' with a large open text box." (Anti-pattern: Annoying repetition, relies on hard-to-analyze free text).

**Principle: Contextual Delivery**
*   [DO] "Because our factory workers are forbidden from having posters on the floor and do not have intranet access, we will chunk safety content into bite-sized nuggets and print them on adhesive stickers placed inside vehicles and on locker doors."
*   [DON'T] "To improve factory worker safety awareness, we will create a comprehensive, 50-page PDF manual and host it on the corporate SharePoint site." (Anti-pattern: Ignoring the user's physical context and access limitations).