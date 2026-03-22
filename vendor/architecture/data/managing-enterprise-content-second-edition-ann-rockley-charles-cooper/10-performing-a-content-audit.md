# @Domain
These rules trigger when the AI is tasked with analyzing existing text or documentation, performing a content audit, evaluating content for reuse and unification, assessing content quality, determining the scope of a content inventory, or preparing information products for transition to a unified content strategy (including multi-channel delivery like Web, print, mobile, or eBooks).

# @Vocabulary
- **Content Audit**: The qualitative process of looking at content analytically and critically to assess its value, quality, and opportunities for reuse (distinct from a Content Inventory).
- **Content Inventory**: A quantitative accounting or complete list of all content to be managed (not an evaluation of its quality or structure).
- **Representative Materials**: A curated subset of content spanning different departments and platforms used to identify patterns without evaluating every single piece of content in the organization.
- **Top-level Analysis**: The first phase of a content audit involving the scanning of various information products (e.g., comparing tables of contents, chapter headings, copyright notices, and disclaimers) to locate common or repeated information.
- **In-depth Analysis**: The second phase of a content audit involving the side-by-side (often tabular) examination of repeated information to determine if variations are identical, similar, justified, or arbitrary.
- **Copy-and-paste**: An anti-pattern masquerading as reuse. It creates unlinked, disconnected instances of content that result in inconsistency, high update costs, and errors.
- **RLO (Reusable Learning Object)**: A chunk of information used consistently across learning materials, serving as a core component that can be augmented for more advanced courses.
- **Adaptive Content**: Content designed to scale and adapt to different environments without being locked into the layout constraints of a specific medium (e.g., print).

# @Objectives
- Evaluate content against strict quality and customer-centric criteria.
- Uncover hidden or ad-hoc content reuse (copy-and-paste) across different information products and channels.
- Differentiate between justified content variations (based on audience or context) and unjustified inconsistencies.
- Translate unstructured, siloed content into a standardized, unified format ready for automated reuse.
- Provide concrete, tabular evidence of content overlap to drive the creation of a formal reuse strategy and content models.

# @Guidelines
- **Scope and Selection**
  - The AI MUST NOT attempt to audit every piece of content blindly; it MUST define a specific scope and select Representative Materials.
  - The AI MUST ensure selected materials cross departmental silos and platforms (e.g., analyzing the Web page, the printed brochure, and the mobile app containing the same topic).
  - Material Selection Rules based on domain:
    - *Marketing*: Select brochures, website pages, packaging, point-of-sale materials, newsletters, press releases, ads.
    - *Publishing*: Select trade press, textbooks, ancillary learning materials, eBooks, apps, journals.
    - *Product Content*: Select help materials, manuals, wikis, OEM customer-branded content, tech support knowledge bases.
    - *Learning Materials*: Select instructor-led materials, self-paced eLearning, virtual classrooms, mobile learning.
- **Quality Assessment Constraints**
  - Before evaluating for reuse, the AI MUST assess content quality by answering these eight explicit criteria:
    1. Is the content appropriate to the customer(s)?
    2. Does it use the customer's terminology?
    3. How well is it written?
    4. Is the tone correct?
    5. Is the level of detail correct?
    6. Will it support the customer content scenarios?
    7. Are there any gaps?
    8. Does it help customers complete tasks, make decisions, and satisfy needs?
- **Reuse Assessment Constraints**
  - The AI MUST treat "copy-and-paste" as a critical failure in content strategy. It MUST highlight unlinked duplicate instances as targets for unification.
  - When performing **Top-level Analysis**, the AI MUST look for structural overlaps: copyright notices, warranty info, product descriptions, intros, procedures, and tables of contents.
  - When performing **In-depth Analysis**, the AI MUST place compared text in a tabular format.
  - The AI MUST question every variation found during In-depth Analysis: "Are the parts that differ necessary? Is there a valid reason for the difference?" If no valid reason exists, the AI MUST recommend rewriting the content so it is identical for reuse.
- **Channel and Domain-Specific Auditing Rules**
  - *Enterprise/Marketing*: If the AI detects manual reuse across web, social, and print, it MUST recommend generating all channels from a single source to eliminate agency/manual layout costs.
  - *Publishing/eBooks*: The AI MUST audit for layout elements that break on E Ink/eReaders. It MUST flag complex tables (>4-5 columns), multi-page images, sidebars, multi-column layouts, and dense paragraphs for structural simplification.
  - *Product Content*: The AI MUST audit step-by-step procedures across different guides (e.g., Quick Start vs. User Manual). Slight wording variations in steps MUST be flagged for unification.
  - *Learning Materials*: The AI MUST look for identical topics taught at different depths. It MUST recommend extracting the common text as a core RLO, with advanced details appended separately.

# @Workflow
1. **Identify Scope and Select Materials**: Define the boundaries of the audit and select a representative cross-section of content from various channels (Web, print, mobile, etc.).
2. **Perform Quality Assessment**: Evaluate the selected text against the 8-point quality checklist (appropriateness, terminology, writing, tone, detail, scenarios, gaps, task support).
3. **Execute Top-level Analysis**: Scan the materials to identify broad areas of overlapping information. Compare headings, TOCs, disclaimers, and intro text. Output a summary of potential reuse targets.
4. **Execute In-depth Analysis**: 
   - Extract the specific text of the overlapping sections identified in step 3.
   - Place the text side-by-side in a Markdown table.
   - Identify whether the text is exactly identical or just similar.
5. **Analyze Variations**: For any text marked "similar," algorithmically determine if the variation is driven by a valid structural/contextual need (e.g., short summary for mobile) or arbitrary authoring inconsistency.
6. **Formulate Unification Recommendations**: Output the final, unified core text that eliminates arbitrary differences, and define how it should be chunked or filtered for different information products.

# @Examples (Do's and Don'ts)

**[DO] Use Tabular Format for In-Depth Analysis**
```markdown
| Information Product | Procedure Text | Analysis |
| :--- | :--- | :--- |
| Owner's Guide | 1. Wash your hands with soap and warm water. Dry well. | Similar. Detailed steps suitable for full manual. |
| Quick Reference | 1. Wash your hands with soap and warm water. Dry completely. | Similar. "Dry completely" vs "Dry well" is arbitrary. Unify. |
| Quick Start Card | Wash hands. | Different format. Fails to use numbered step. Unify structure. |

**Recommendation**: Unify Step 1 across all products to: "1. Wash your hands with soap and warm water. Dry well."
```

**[DON'T] Recommend Copy-and-Paste for Content Generation**
```markdown
*Incorrect AI Output:*
To ensure the marketing brochure matches the website, simply copy the "About Us" paragraph from the webpage and paste it into the InDesign layout file.
```

**[DO] Flag Complex Print Layouts During eBook Audits**
```markdown
*Correct AI Output:*
**Content Flag**: The biological sciences textbook contains a 6-column digestive system table and sidebars with wrapped text.
**Recommendation**: This violates eBook constraints. The table must be simplified or transformed into list-based text, and sidebars must be structurally placed inline following the logically related paragraph to prevent breaking on E Ink devices.
```

**[DON'T] Allow Unjustified Discrepancies in Core Definitions**
```markdown
*Incorrect AI Output:*
The website defines the product as "a tool to measure glucose," while the print manual defines it as "a device measuring blood sugar." Both are fine since they mean the same thing.
```
*(The AI MUST flag this as an inconsistency in terminology and recommend a single unified definition component).*