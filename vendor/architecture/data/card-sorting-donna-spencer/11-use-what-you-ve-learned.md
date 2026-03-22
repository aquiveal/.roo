# @Domain
Trigger these rules when the AI is asked to synthesize card sorting data, design or evaluate Information Architecture (IA), propose website or system navigation, synthesize user research into category structures, or construct testing protocols for a proposed organizational scheme.

# @Vocabulary
- **Information Architecture (IA)**: The structural design of shared information environments; the art and science of organizing and labeling websites, intranets, online communities, and software to support usability and findability.
- **Organizational Scheme**: The underlying methodology or framework used to group and structure content (e.g., by topic, by location, by time, by audience).
- **Card-Based Classification Evaluation**: A specific testing methodology using two sets of cards—one containing draft categories and the other containing user tasks—to validate whether users can successfully navigate the proposed IA.
- **Unworkable Organizational Scheme**: A grouping structure produced by card sort participants that is factually incorrect (e.g., mixing theoretical presentations into "case studies") or mirrors internal organizational charts rather than user-centric topics.

# @Objectives
- **Synthesize Multi-Source Research**: Cross-reference card sorting outcomes with other user research methods (e.g., search logs, user interviews) to establish high-confidence categories.
- **Interpret, Do Not Replicate**: Extract the underlying meaning, needs, and mental models from card sorting data rather than algorithmically replicating participant groupings 1:1 into final site navigation.
- **Establish High-Quality Categories**: Produce draft categories that users immediately understand, that accommodate content with manageable overlap, and that utilize labels matching the user's mental model.
- **Provide Structural Flexibility**: Design systems that accommodate multiple valid organizational schemes simultaneously when content warrants it.
- **Formulate Validation Protocols**: Always generate actionable IA testing steps using task-based classification evaluation to verify structural assumptions.

# @Guidelines
- **Multi-Input Validation**: The AI MUST cross-reference card sorting data against other available research inputs. When user interviews, search logs, and card sorts all indicate a specific category (e.g., "Pay and Benefits"), the AI MUST prioritize that category.
- **The "Be Practical" Constraint**: The AI MUST NEVER blindly adopt participant groupings if they result in poor usability. The AI MUST deliberately ignore participant results that mimic internal company structures or demonstrate factual misunderstandings of the content.
- **Outlier Analysis**: When participants create "Other," "Miscellaneous," or highly inaccurate groupings, the AI MUST analyze the underlying cause (e.g., ambiguous card titles, loose conceptual definitions) rather than creating a "Miscellaneous" navigation item.
- **The "Don't Assume" Constraint**: The AI MUST explicitly separate the concept of "participant card groups" from "website navigation." If participants create 20 groups, the AI MUST NOT default to creating 20 top-level navigation items. 
- **Strict Category Criteria**: Any proposed category MUST meet three criteria:
  1. Users can understand it and use it to find information.
  2. The content fits logically inside it with an acceptable, but not excessive, amount of overlap.
  3. The label accurately describes the content and matches the user's native vocabulary.
- **Embrace Flexible Organization**: The AI MUST NOT arbitrarily force content into a single organizational scheme if multiple schemes are sensible. It MUST evaluate if content can be cross-indexed (e.g., organizing events simultaneously by time, location, and topic).
- **Thinking Over Mechanics**: The AI MUST act as a critical synthesizer. It MUST NOT rely solely on the mechanical output of the card sort data; it must apply UX heuristics, follow architectural instincts, and propose new approaches when the raw data produces a fractured structure.

# @Workflow
When synthesizing card sorting results into a final Information Architecture, the AI MUST execute the following algorithm:

1. **Research Amalgamation**: 
   - Extract identified user needs, possible top-level categories, strongly linked content pairs, hard-to-place outliers, and audience variances from the card sort data.
   - Inject secondary data (interviews, search logs) and isolate overlapping consistencies.
2. **Impracticality Filtering**: 
   - Scan the data for groupings based on internal company structures (e.g., "HR Department", "IT Department"). Discard these as primary navigation structures in favor of core topics of interest.
   - Scan for factually incorrect groupings (e.g., theory grouped under "Case Studies"). Reassign this content based on correct attributes.
3. **Category Generation**: 
   - Define draft categories based on synthesized topics.
   - Validate each proposed category against the *Strict Category Criteria* defined in the Guidelines.
4. **Flexible Pathway Mapping**: 
   - Identify content sets that require multi-scheme organization (e.g., organizing products by both task and topic). Create structural pathways to support these intersections.
5. **Testing Protocol Creation (Card-Based Classification Evaluation)**: 
   - Generate a definitive list of the proposed top-level categories and subcategories.
   - Generate a discrete list of realistic user tasks (e.g., "Find out how much travel allowance you are entitled to").
   - Output a step-by-step testing script instructing human researchers to ask users which category they would select for each task.

# @Examples (Do's and Don'ts)

## Applying Participant Groupings
- **[DO]**: Synthesize the underlying theme of participant groups. "Participants created 15 distinct, small groups. Instead of turning these into 15 navigation links, I will consolidate them into 4 broader, task-based categories that accommodate all the underlying content."
- **[DON'T]**: Blindly map groups to navigation. "Participants created 20 groups during the open card sort, so I have created 20 top-level navigation categories for the website."

## Handling Corporate / Internal Structures
- **[DO]**: Organize intranets and systems by topics of interest. "Although some participants grouped content by the organizational chart (e.g., putting 'Travel Forms' under 'Finance Department'), I have mapped this content to a user-centric 'Travel & Expenses' topic."
- **[DON'T]**: Replicate the org chart. "Participants grouped all software installation guides under 'IT Department' and leave policies under 'HR Department', so the primary navigation will be organized by department names."

## Implementing Flexible Categorization
- **[DO]**: Provide multiple pathways for finding content. "The data shows users search for events differently. I will structure the architecture so users can browse events by 'Chronology/Date', by 'Geography/Location', and by 'Topic'."
- **[DON'T]**: Force a single taxonomy artificially. "Since 60% of users sorted events by Date, we will only organize the events chronologically and discard the location and topic schemes entirely."

## Designing Evaluation Protocols
- **[DO]**: Define a task-based evaluation. "To test this IA, we will conduct a Card-Based Classification Evaluation. Set 1: Draft Categories (e.g., 'Pay and Benefits'). Set 2: Tasks (e.g., 'Find your dental coverage'). Ask the user which category they would select for the task."
- **[DON'T]**: Test IA by asking users to categorize content again. "To test the draft IA, we will do a closed card sort and ask users to put content pages into our new categories." (Note: Closed card sorting tests classification, not *findability*).