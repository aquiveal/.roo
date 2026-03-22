**@Domain**
These rules trigger when the AI is tasked with generating, reviewing, organizing, structuring, or formatting content intended for Card Sorting exercises (both physical and software-based), specifically focusing on drafting card titles, descriptions, and category labels.

**@Vocabulary**
- **Content Card**: The physical (e.g., 3"x5" index card) or digital artifact representing a single piece of information, topic, or functionality to be sorted by a participant.
- **Category Card**: A predetermined grouping label used exclusively in Closed Card Sorts, which participants use as the target destination for Content Cards.
- **Software-Based Sort**: A card sorting exercise conducted via a digital tool, requiring specific attention to character limits, display constraints, and data import mechanisms (e.g., spreadsheet formatting).
- **Physical Card Sort**: A sorting exercise conducted in person using printed or handwritten artifacts (typically 3"x5" index cards with copier labels).
- **Jargon/Acronyms**: Internal organizational language or shorthand that may not be understood by the external end-user, strictly prohibited on card titles unless defining the user's natural language.

**@Objectives**
- Ensure every generated card title is unambiguous, easy to understand, and accurately represents the underlying content.
- Eliminate all internal jargon, acronyms, and vague terminology from card text.
- Differentiate near-duplicate concepts so participants can clearly distinguish between cards.
- Guarantee that Category Cards (for closed sorts) are visually and structurally distinct from Content Cards.
- Enforce format-specific constraints (physical dimensions or software display limits) prior to finalizing card lists.
- Act as an independent QA reviewer to spot spelling errors, confusing titles, and ambiguous phrasing before card lists are finalized.

**@Guidelines**
- **Title Clarity over Brevity**: Titles must provide enough context to be understood in isolation. If a short title is vague, expand it to accurately describe the content.
- **Jargon and Acronym Eradication**: The AI MUST spell out all acronyms and translate internal organizational jargon into plain, user-centric language.
- **Content Duplication**: The AI MUST identify and consolidate, or explicitly differentiate, overlapping concepts (e.g., do not include both "Venue" and "Venue facilities" unless they are intentionally and clearly separated by detailed descriptions).
- **Supplemental Information**: If a title alone is insufficient to convey the concept, the AI MUST append a fuller description, a few paragraphs of context, or a placeholder for an image.
- **Alternative Content Types**: When standard cards are insufficient, the AI MUST suggest using printed pages of existing content with navigation elements removed to provide maximum context.
- **Closed Sort Distinction**: When generating lists for Closed Card Sorts, the AI MUST format Category Cards to be distinctly different from Content Cards (e.g., specifying ALL CAPS, distinct colors, or "Large Sticky Note" formatting).
- **Software Tool Constraints**: For digital sorts, the AI MUST prompt the user to verify allowed character lengths, check on-screen display formatting, and format the output for easy system import (e.g., CSV or structured spreadsheet formatting).
- **Spelling and QA**: The AI MUST strictly proofread all card data; spelling errors distract participants and undermine the integrity of the sort.

**@Workflow**
1. **Analyze Raw Input**: Review the raw list of topics, pages, or content inventory items provided by the user.
2. **Title Refinement**:
   - Identify and translate any internal jargon or acronyms.
   - Expand overly brief titles to include necessary context.
   - Flag and resolve near-duplicate items.
3. **Determine Sort Type Constraints**:
   - *If Physical*: Format output to map easily to printable copier labels or 3"x5" index cards.
   - *If Software-Based*: Verify character limits and format output as a structured table/CSV for easy digital import.
   - *If Closed Sort*: Generate a separate, visually distinct list of Category Cards (e.g., formatted in ALL CAPS).
4. **Context Addition**: Evaluate if any refined title is still ambiguous. If so, generate a secondary "Description" field to be printed or displayed alongside the title.
5. **Simulate Uninvolved QA**: Perform a final pass pretending to be a participant with zero domain knowledge. Highlight any remaining cards that are confusing, ambiguous, or susceptible to misinterpretation, and propose revisions.

**@Examples (Do's and Don'ts)**

**Principle: Expanding Titles for Context**
- [DON'T] Generate vague, single-word titles: `Registration`
- [DO] Generate descriptive, contextual titles: `Conference registration and fees`

**Principle: Eliminating Jargon**
- [DON'T] Use internal organizational shorthand: `Papers`, `Sessions`
- [DO] Translate to user-friendly language: `Conference presentations`

**Principle: Resolving Near-Duplicates**
- [DON'T] Include overlapping concepts that will confuse participants: `Conference venue` AND `Conference venue facilities`
- [DO] Consolidate into a single comprehensive card or clarify the distinct difference: `Information about the conference venue`

**Principle: Formatting Category Cards for Closed Sorts**
- [DON'T] Format category cards identically to content cards:
  `Content: Travel policies`
  `Category: Human Resources`
- [DO] Apply distinct structural formatting to categories:
  `Content: Travel policies`
  `Category: HUMAN RESOURCES (Print on Yellow Card / Large Sticky Note)`

**Principle: Avoiding Problematic Terminology**
- [DON'T] Use words that carry negative or outdated connotations to the user base (e.g., `Computing`, `Training`).
- [DO] Use modern, user-centric alternatives based on research (e.g., `Technology support`, `Professional development`).