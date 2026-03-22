**@Domain**
These rules MUST be triggered whenever the AI is tasked with configuring analytics, defining Key Performance Indicators (KPIs), establishing conversion funnels, setting up reporting dashboards, defining operational efficiency metrics for content systems, or analyzing post-publish content data. This applies to any code, documentation, or configuration related to tracking, measuring, and reporting on content performance.

**@Vocabulary**
*   **Analytics**: The capture and assessment of data specifically focused on performance.
*   **Metrics**: Specific units of measurement (e.g., number of downloads, bounce rate).
*   **Key Performance Indicator (KPI)**: A metric used to evaluate the performance of an organization’s high-level objectives.
*   **Conversion Metrics**: Measurement of a specific conversion or task completion (e.g., purchase, add to cart, download, profile creation, call, registration).
*   **Strategic Intent**: The umbrella strategy or overarching mission of the content experience.
*   **Goal**: A general, lofty aspiration for the content experience.
*   **Objective**: A specific, measurable desired outcome that supports the goal.
*   **Point of Entry**: The exact location or method by which a consumer enters the experience (e.g., keyword search, banner ad, direct URL).
*   **Exit Metrics**: Measurement of where a content consumer leaves an experience. (An exit is not inherently negative if the user accomplished their task).
*   **Bounce Rate**: Measurement of visitors who reach an experience and leave *immediately* without further interaction.
*   **Share of Voice**: The frequency with which social media mentions the brand, experience, or organization.
*   **Social Sentiment**: Tracking of what others are writing/perceiving about the brand, experience, or content in social media.
*   **Operational Metrics**: Internal measurements of process efficiency (e.g., cost to produce, time saved, decrease in redundancy, employee attrition).
*   **Content Experience Metrics**: Measurements of the qualitative user experience (e.g., brand consistency, content quality, relevance, localized content error rates).

**@Objectives**
*   Design a performance-driven content model where metrics are mapped directly to business objectives, not tracked in a vacuum.
*   Establish measurement requirements *early* in the design and implementation phases to ensure technology solutions are customized to capture necessary data.
*   Ensure analytics go beyond the "what" (the data) to mandate structured investigation into the "why" (the root cause of success or failure).
*   Capture a holistic view of performance by integrating Common, Social, Operational, and Content Experience metrics.

**@Guidelines**
*   **Metric Hierarchy Mapping**: The AI MUST explicitly map every metric to a three-tier hierarchy: Strategic Intent -> Goal -> Objective. Do not create orphaned metrics.
*   **SMART Criteria Enforcement**: Every Objective defined MUST pass the SMART test: Specific, Measurable, Accountable, Realistic, Timely.
*   **The 5 Specificity Parameters**: When defining a metric, the AI MUST explicitly answer:
    1. *Who*: The target audience/persona/segment.
    2. *When/How*: The timeframe for completion.
    3. *How many*: The specific volume, percentage, or target number.
    4. *Where*: The geographical location, channel, or specific site area.
    5. *Why*: The business reason for the target (e.g., to increase sales).
*   **Early Technology Alignment**: The AI MUST flag system or database constraints early, noting that tracking features (e.g., custom events, onsite search logging, conversion paths) may require programming changes during the build phase.
*   **Journey Validation**: When defining User/Consumer Path, Clickstream, or Conversion metrics, the AI MUST define an *assumed* user journey to compare against the actual path taken.
*   **Onsite vs. External Search**: The AI MUST separate "External keyword search terms" (organic SEO) from "Onsite search keywords." For onsite search, explicitly track failed searches (zero results), refined searches, and facet usage to identify navigation failures.
*   **Exit vs. Bounce**: The AI MUST strictly separate Exit Metrics (leaving after spending time/accomplishing a task) from Bounce Rates (leaving immediately). Bounce rate analysis MUST include the Point of Entry.
*   **Diagnostic Resolution Protocol**: If content performs poorly, the AI MUST NOT stop at reporting the failure. It MUST generate a diagnostic checklist evaluating:
    1. Is the content actually found? (Check navigation/search/placement).
    2. How is it engaged? (Check format suitability, long-form vs. mobile).
    3. Is the user journey broken? (Check next-step friction).
    4. Is it relevant/on-brand? (Check quality and UX).
    5. Were the objectives realistic? (Compare against competitors).
*   **Success Replication Protocol**: If content performs exceptionally well, the AI MUST recommend actions to replicate success (e.g., elevate placement, place in additional channels, develop supporting stories).
*   **Reporting Cadence Specification**: The AI MUST define the reporting schedule based on metric type:
    *   Operational metrics: Quarterly.
    *   Content Experience metrics: Monthly or Quarterly (Hourly for e-commerce).

**@Workflow**
1. **Establish the Business Framework**: Define the Strategic Intent, Goal, and Objective for the content scope. Apply SMART criteria to the Objective.
2. **Formulate the Specific Metric**: Translate the Objective into a measurable data point. Ensure the 5 Specificity Parameters (Who, When, Volume, Where, Why) are fully documented.
3. **Select Measurement Categories**: Allocate required metrics across the four operational domains:
    *   *Common Metrics*: User path, length/depth of visit, conversions, external/onsite search terms, point of entry, value of interaction, cost to convert, exit metrics, bounce rates, user-interaction history.
    *   *Social Metrics*: Post rates, share of voice, referrals, sentiment, repeat engagement.
    *   *Operational Metrics*: Cost reduction (production/localization), time saved, internal satisfaction, redundancy decrease, employee attrition.
    *   *Experience Metrics*: Retention, acquisition, quality audits, content efficacy (A/B testing results).
4. **Define the Tracking Mechanism**: Specify the exact tool or method required to capture the metric (e.g., Google Analytics, Operational Dashboard, CRM, Quality Standard Audit, Customer Survey).
5. **Establish the Analysis Protocol**: Define the recurring schedule for reviewing the data (e.g., monthly). Formulate the "Why" investigation steps for both over-performing and under-performing content.
6. **Determine Content Lifecycle Action**: Based on the analysis protocol, dictate whether the content will be:
    *   *Optimized/Replicated* (if over-performing or slightly missing targets).
    *   *Left As Is* (if perfectly meeting objectives without decay).
    *   *Archived/Sunset* (if failing diagnostic checks, legally expired, or run its course).

**@Examples (Do's and Don'ts)**

*   **[DO]** Define a metric with full SMART and Specificity parameters mapped to a business goal.
    ```markdown
    **Strategic Intent**: Become the premium educational resource for software engineers.
    **Goal**: Outperform competitors in engagement and community growth.
    **Objective**: Increase the number of registered user profiles by 20% within the next 6 months.
    **Metric Definition**:
    - *Who*: Unauthenticated software engineers visiting from organic search.
    - *When*: Within 6 months of the new portal launch.
    - *How many*: 20% increase over the current baseline of 5,000 monthly registrations.
    - *Where*: The desktop and mobile article pages.
    - *Why*: To build an authenticated audience for targeted personalization and cross-selling.
    - *Tracking Mechanism*: Web analytics conversion funnel + CRM database.
    ```
*   **[DON'T]** Define a metric in a vacuum without business context or specific parameters.
    ```markdown
    **Metric**: Track page views and bounce rates on the new blog. (INCORRECT: Lacks Strategic Intent, Goal, SMART Objective, and the 5 specific parameters).
    ```

*   **[DO]** Prescribe a structured diagnostic checklist for failing metrics.
    ```markdown
    **Observation**: The "Cloud Deployment" whitepaper has a 90% bounce rate.
    **Diagnostic Action Plan**:
    1. Check Point of Entry: Are visitors arriving via misleading external keywords?
    2. Check Onsite Search: Did they search for a specific facet we don't offer?
    3. Check UX: Is the PDF format causing friction on mobile devices?
    4. Competitor Check: Compare our whitepaper length and format against industry standards.
    ```
*   **[DON'T]** Conflate Exit Rates with Bounce Rates or fail to ask "Why".
    ```markdown
    **Observation**: Exit rates on the "Thank You for Downloading" page are 95%. This content is failing, we must archive it. (INCORRECT: An exit on a post-conversion page indicates task success, not failure. Do not treat exits as bounces).
    ```

*   **[DO]** Define specific internal operational metrics to measure content ecosystem health.
    ```markdown
    **Operational Metric**: Reduction in localization cost.
    **Measurement Tool**: Operational metrics dashboard and translation vendor invoices.
    **Target**: 15% decrease in cost-per-word over Q3 due to improved CMS translation workflows and reduced content redundancy.
    ```
*   **[DON'T]** Rely solely on web traffic to determine enterprise content success.
    ```markdown
    **Measurement Plan**: We will evaluate the success of the new CMS solely through Google Analytics page views. (INCORRECT: Fails to measure Operational Metrics like time-saved authoring, or Content Experience metrics like brand consistency audits).
    ```