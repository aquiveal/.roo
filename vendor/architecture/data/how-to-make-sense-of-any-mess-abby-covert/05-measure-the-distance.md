# @Domain
These rules are triggered when the user requests assistance with defining project milestones, establishing Key Performance Indicators (KPIs), planning project timelines, creating testing and success criteria, defining metrics, evaluating system performance, or measuring progress for any system, product, or architecture.

# @Vocabulary
- **Goal**: A specific, well-defined target containing three elements: Intent, Baseline, and Progress.
- **Intent**: The specific results or effect you want to see for your efforts when you are "all grown up."
- **Baseline**: The exact measurement of something *before* any changes are made, used as a point of reference to judge performance.
- **Progress**: The specific method or metric used to measure movement toward or away from a goal.
- **Dependency**: A condition that has to be in place for something else to happen.
- **Indicator**: A sign or metric (measured by systems or people) that tells you if you are moving toward or away from your intent.
- **Flag**: A proactive notification attached to an indicator that alerts you when something important happens.
- **Rhythm**: The frequency at which an indicator is measured (e.g., moment-to-moment, weekly, yearly), determined by timeframe and data access.
- **Worksheet**: A tool used to mine data from people's heads or personal records, constrained by Time, Access, and Bias.
- **Murk**: Alternative truths or opinions that exist about what is being made or achieved.
- **Fuzzy Data**: Incomplete, subjective, or highly difficult-to-measure indicators that must still be used to maintain forward momentum.

# @Objectives
- Translate abstract intentions into specific, measurable goals.
- Identify the exact distance between the current reality and the intended future state.
- Establish rigid baselines before proposing or evaluating any changes or solutions.
- Define actionable indicators, proactive flags, and strict measurement rhythms to track progress.
- Prevent project paralysis by accepting "fuzzy" or incomplete data as a valid starting point for measurement.
- Architect data-mining processes (worksheets/surveys) that explicitly account for human constraints (time, access, and bias).

# @Guidelines

## Goal Definition Constraints
- The AI MUST NEVER accept or generate a "Goal" that lacks any of the three foundational elements: Intent, Baseline, and Progress.
- When generating tasks, the AI MUST explicitly map and sequence all Dependencies before defining the timeline.
- The AI MUST ensure that the chosen measurement of Progress explicitly reinforces the Intent (e.g., if the intent is to finish a project, measure words written toward the project, not just time spent writing).

## Indicator Selection Constraints
- The AI MUST identify and categorize Indicators to monitor progress. The AI MUST consider the following common indicators when proposing metrics: 
  - *Positive/Growth:* Satisfaction, Kudos, Profit, Value, Loyalty, Traffic, Conversion, Spread.
  - *Negative/Risk:* Complaints, Backlash, Expenses, Debt, Lost time, Drop-off, Waste, Murk.
  - *Contextual:* Perception, Competition.
- The AI MUST NOT rely solely on system-generated data; it MUST propose ways to mine data from people when appropriate.

## Human Data-Mining Constraints
- When the AI generates surveys, questionnaires, or "Worksheets" to gather metrics from users or stakeholders, it MUST evaluate and optimize the questions against three criteria:
  - **Time**: How much time is being asked of the respondent?
  - **Access**: How many sources or other people must the respondent consult to answer?
  - **Bias**: Is the tool capturing objective data or the respondent's personal preferences/opinions?

## Baseline and Flag Constraints
- The AI MUST NOT evaluate the success or failure of a system, test, or feature without first defining its Baseline.
- The AI MUST attach a "Flag" to every critical Indicator. The flag must specify the exact threshold or condition that triggers a proactive notification.
- The AI MUST define a "Rhythm" for every measurement, specifying both the Timeframe (when to measure) and Access (how readily available the data is).

## Fuzzy Data Directives
- When the AI encounters incomplete data, subjective measurements, or unreliable data sources, it MUST NOT halt progress or request infinite clarification.
- The AI MUST explicitly acknowledge the data as "Fuzzy," establish a best-guess baseline, and proceed with goal-setting to maintain momentum.

# @Workflow
When tasked with measuring progress, setting KPIs, or defining project goals, the AI MUST follow this exact algorithmic sequence:

1. **State the Intent**: Prompt the user to clarify the overarching intent and "why" behind the project.
2. **Break Down into Goals**: Translate the intent into specific, discrete goals.
3. **Draft a Dream List**: Generate an ideal list of measurable indicators (assuming a perfect world with perfect data). Include system-measured and people-measured data.
4. **Establish Baselines**: Narrow the dream list down to an achievable set of indicators and immediately define or request the Baseline measurement for each.
5. **Select Indicators & Progress Metrics**: Define exactly how movement away from or toward the baseline will be measured.
6. **Configure Flags**: Define the specific conditions, thresholds, and notification methods for when the user needs to be alerted about changes in the indicators.
7. **Determine Measurement Rhythm**: Assign a specific timeframe and data-access protocol for checking each indicator.

# @Examples (Do's and Don'ts)

## Defining Goals and Progress
- **[DO]**: "Goal: Write a novel within one year. Intent: Complete a long-form fiction book. Baseline: 0 words currently written. Progress Measurement: Write 500 words specifically toward the novel per day."
- **[DON'T]**: "Goal: Become a better writer. Progress: Write every day." *(Anti-pattern: The progress measurement does not explicitly reinforce a specific, finite intent, nor does it establish a baseline).*

## Establishing Baselines
- **[DO]**: "Before evaluating the success of the new marketing campaign, we must establish that the standard baseline for Q1 profit increases is $5.5M. We will compare the campaign's $1.5M increase against this $5.5M baseline to determine actual performance."
- **[DON'T]**: "Profits increased by $1.5M after the campaign launched, which means the campaign was highly successful." *(Anti-pattern: Judging performance without stating the historical baseline, leading to false assumptions).*

## Setting Flags
- **[DO]**: "Indicator: User Drop-off during registration. Flag: Send a weekly automated email report detailing the exact percentage of users who abandoned the process at Step 3."
- **[DON'T]**: "Indicator: User Drop-off. We will check this periodically to see if people are leaving." *(Anti-pattern: Lacks a proactive notification mechanism, specific threshold, and rhythm).*

## Handling Fuzzy Data
- **[DO]**: "The indicator for 'Brand Perception' is currently fuzzy and subjective. However, we will use the current volume of positive social media mentions as our best-guess baseline and begin measuring weekly to maintain momentum."
- **[DON'T]**: "We cannot measure 'Brand Perception' because the data is too subjective and unreliable. We must wait until we have a perfect sentiment-analysis tool before setting goals." *(Anti-pattern: Procrastinating and halting progress due to the fear of incomplete or fuzzy data).*