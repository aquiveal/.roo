**@Domain**
These rules trigger when the user requests assistance with managing, facilitating, preparing for, or executing a card sort activity. This includes preparing analysis tools, conducting test runs, generating facilitator scripts, handling participant questions, observing sort behaviors, and recording data.

**@Vocabulary**
- **Test Run**: A mandatory pilot execution of the card sort (conducted first by the facilitator, then with a colleague) to identify errors in instructions, card titles, and analysis tools before the actual session.
- **"About" Descriptions**: Qualitative statements made by participants during a team sort (e.g., "This is all the agriculture stuff") that reveal the underlying rationale for a group, even if the final written label differs.
- **First-Grouped Cards**: Cards that participants place together quickly and easily at the start of the sort, representing straightforward, natural groupings.
- **Last-Grouped Cards**: Cards left until the end of the activity, typically representing obscure content, poorly labeled items, or outliers that do not fit into obvious groups.
- **Spatial Patterns**: The physical arrangement of cards on a table (e.g., tight clusters vs. spread-out groupings, or centrally placed cards), which can indicate the conceptual closeness or broadness of a group.
- **Prototypical Examples**: The one or two specific cards within a group that participants identify as the "best" or most representative examples of that category.

**@Objectives**
- Ensure the card sort is perfectly prepared by mandating test runs and pre-configuring the analysis method.
- Prevent the facilitator from leading participants or allowing participants to focus on website design/hierarchy instead of content grouping.
- Maximize the capture of qualitative data by actively monitoring group dynamics, listening for "about" descriptions, and noting the sequence of card placement.
- Guarantee the safety and accuracy of collected data through immediate, structured recording techniques.

**@Guidelines**
- **Analysis Pre-Check**: The AI MUST prompt the user to define the analysis method (exploratory vs. statistical) *before* the sort begins to ensure the data collected matches the tool's limitations (e.g., handling of duplicate cards, limits on participant numbers).
- **Tool Validation**: The AI MUST instruct the user to enter at least one dummy set of data into their chosen analysis tool/spreadsheet to verify capacity and functionality before conducting the live sort.
- **Test Run Mandate**: The AI MUST explicitly prohibit skipping the test run. The user must be instructed to test for badly worded instructions, duplicate content, ambiguous titles, misspellings, and un-groupable cards.
- **Physical Preparation**: For manual sorts, the AI MUST remind the user to prepare spare index cards (for duplicates/new categories), sticky notes (for labels), rubber bands (for bundling), and pens.
- **Introduction Constraints**: The AI MUST provide scripts that steer participants strictly toward grouping content. The AI MUST instruct the facilitator to explicitly tell participants *not* to worry about creating hierarchies, designing navigation, or cross-linking.
- **Card Distribution Rules**: The AI MUST advise the facilitator to introduce the activity *before* handing out the cards. Cards MUST be spread out on a table (not handed as a tight bundle) so participants can see the entire scope of content before starting. Cards MUST be well-shuffled between different participants.
- **Handling Duplicates**: The AI MUST instruct the facilitator to allow participants to place a card in more than one group using blank spare cards. *Exception*: If using statistical software that forbids duplicates, the facilitator must ask the participant for the "best fit" and manually note the alternate category.
- **Handling Group Sizes**: If asked how many groups to make, the AI MUST provide the guideline: "Make as many as make sense given the content—but two is too few and 100 is too many."
- **Observation Directives**: The AI MUST instruct the facilitator to remain quiet, observe, and document: "About" descriptions, First-grouped cards, Last-grouped cards, and spatial patterns.
- **Delayed Labeling**: The AI MUST instruct the facilitator *not* to mention labeling during the introduction. Labeling prompts MUST only occur after the groups have settled, preventing participants from prematurely focusing on naming rather than grouping.
- **Recording Mandate**: The AI MUST mandate immediate data capture. For physical sorts, the AI MUST instruct the user to write the card numbers directly onto the sticky note label to prevent data loss if cards are dropped.

**@Workflow**
1. **Preparation & Testing Phase**:
   - Verify the chosen analysis tool and its constraints.
   - Run a test sort personally, then with a colleague. Fix any identified card errors (spelling, ambiguity, un-groupable items).
   - Test data entry in the software/spreadsheet using the test run data.
   - Gather physical materials (spare cards, sticky notes, rubber bands, pens).
2. **Introduction Phase**:
   - Deliver the standardized introduction script.
   - Explain the context (e.g., website redesign).
   - Instruct participants to group cards that belong together, explicitly stating there is no right or wrong way and they do not need to design a website structure.
3. **Distribution Phase**:
   - Shuffle the deck.
   - Spread the cards out on the table so the whole set is visible.
4. **Observation Phase**:
   - Step back and monitor group dynamics. Intervene only if one person dominates or someone is excluded.
   - Take notes on verbalized "about" statements.
   - Document which cards are grouped first and which are left until last.
   - Photograph any interesting spatial patterns.
5. **Labeling Phase**:
   - Once grouping slows and settles, prompt the participants to write a label or rough description on a sticky note and place it on each group.
6. **Debriefing Phase**:
   - Ask participants about their overall rationale or underlying method.
   - Ask participants to identify the "best example" (prototypical) cards in each group.
   - Check if all team members are happy with the outcome or if compromises were made.
   - Ask what the easiest and hardest parts of the activity were.
7. **Recording Phase**:
   - Immediately write the corresponding card numbers directly onto the sticky note for each group.
   - Bundle the groups with rubber bands.
   - Enter the data into the validated analysis tool/spreadsheet as soon as possible.

**@Examples (Do's and Don'ts)**

**Principle: Introducing the Activity**
- **[DO]**: "We are reorganizing the intranet. Please sort these cards into groups that make sense to you. Don't worry about creating the perfect website hierarchy or navigation menus; just focus on what content belongs together."
- **[DON'T]**: "Please organize these cards into the top-level navigation menus you would like to see on the new website, and let me know what drop-downs you want." (This leads the participant to design the site rather than group the content).

**Principle: Handing Out Cards**
- **[DO]**: Complete the entire verbal introduction, then spread the well-shuffled cards out across the table so participants can scan the available content before making their first group.
- **[DON'T]**: Hand a tight, ordered stack of cards to the user as they walk in, or fail to shuffle the deck between sessions so the participant just follows the previous user's pattern.

**Principle: Handling Duplicates**
- **[DO]**: "You think this card belongs in both 'HR' and 'Finance'? No problem, here is a blank index card. Write the title on this blank card and you can place it in both groups."
- **[DON'T]**: "You have to pick just one group. Put it wherever you think is slightly better." (Unless strictly required by an inflexible statistical analysis tool, in which case the alternate choice MUST still be noted manually).

**Principle: Labeling**
- **[DO]**: Wait until the participants have finished grouping the cards, then hand them sticky notes and say, "Now take a look at the groups you've made and write a brief description or label for why these go together."
- **[DON'T]**: Say in the initial instructions: "Sort these cards into groups and make sure you come up with a good name for every group you make." (This forces them to think about labels too early, stifling organic grouping).

**Principle: Recording Data**
- **[DO]**: Take the sticky note labeled "Company Policies", write the numbers "12, 45, 6, 88" directly on the note, place it on top of the stack, and wrap it in a rubber band.
- **[DON'T]**: Stack all the loose cards under loose sticky notes and throw them in a bag to sort out at the office later.