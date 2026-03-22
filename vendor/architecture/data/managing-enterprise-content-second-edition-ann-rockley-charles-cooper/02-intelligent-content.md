@Domain
Trigger these rules when tasked with designing, migrating, structuring, evaluating, or generating content architectures, content models, or multi-channel publishing workflows. These rules activate when the AI is manipulating content destined for reuse, enterprise delivery, or automated publishing systems.

@Vocabulary
- **Intelligent Content**: Content that is structurally rich and semantically categorized, making it automatically discoverable, reusable, reconfigurable, and adaptable.
- **Structure**: The hierarchical order in which content occurs in an information product.
- **Semantic/Semantic Structure**: The meaning of words, phrases, or systems. Content tagging based on what the content *is* (e.g., `Ingredient`, `Step`), not what it *looks like* (e.g., `Normal`, `Heading 1`, `Bulleted List`).
- **Metadata**: Tags applied to content to semantically categorize it, identifying context such as industry, audience, or subject area.
- **Discoverability**: The ability for search engines, systems, or humans to find specific content components automatically via applied metadata.
- **Content Reuse**: The practice of using existing components of content to develop new materials, eliminating copy-and-paste practices.
- **Reconfigurable**: Content designed as modular components that can be reordered, included, excluded, or combined to build entirely new information products.
- **Adaptable**: Content stripped of formatting, capable of being structurally and visually transformed to suit multiple devices (e.g., linear for print, multi-tabbed for mobile).
- **Translation Memory Systems (TMS)**: Systems utilizing pattern matching to identify and reuse already-translated content strings, saving costs based on exact string matching.

@Objectives
- Transform unstructured, document-bound ("black box") content into intelligent, modular content.
- Guarantee the absolute separation of content meaning (semantics) from visual presentation (format/style).
- Ensure all generated content structures enforce a rigid hierarchy that automated systems can reliably parse and manipulate.
- Maximize content reuse to reduce development, review, and translation costs.
- Future-proof content by utilizing open standards (e.g., XML) to avoid vendor lock-in and enable seamless automated multi-channel publishing.

@Guidelines
- **Enforce Structural Richness**: The AI MUST organize content into strict hierarchical structures. Child elements MUST be logically subordinate to parent elements.
- **Apply Semantic Tagging**: The AI MUST label content based on its exact meaning and function (e.g., `<Suggestion>`, `<Action>`, `<Warning>`) rather than its visual layout.
- **Prohibit Embedded Formatting**: The AI MUST NEVER embed visual formatting (e.g., bolding, italics, hardcoded list numbers, font sizes) within the content data. Formatting MUST be completely delegated to external stylesheets.
- **Enforce Absolute Reuse**: When generating content variations, the AI MUST isolate shared components and reference them. The AI MUST NOT duplicate or "copy-paste" text strings, as even minor variations (spaces, commas) destroy Translation Memory System (TMS) pattern matching and increase costs.
- **Categorize via Metadata**: The AI MUST append descriptive metadata (e.g., `industry=medical`, `audience=physician`, `subject=diabetes`) to all content components (text, video, audio) to guarantee automated discoverability.
- **Ensure Reconfigurability**: The AI MUST author content as self-contained, modular blocks. A module MUST NOT rely on preceding or succeeding text outside of its hierarchical boundary to make sense.
- **Design for Adaptability**: The AI MUST structure content so that publishing engines can conditionally filter or structurally adapt it based on the target device (e.g., identifying tables that should be filtered out or transformed for a mobile interface).
- **Maintain Open Standards**: The AI MUST utilize open, flexible environments and syntax (such as XML paradigms) to structure data, preventing constraints tied to proprietary authoring tools like Microsoft Word.

@Workflow
1. **Analyze Unstructured Data**: Evaluate the source text to identify its inherent meaning, purpose, and hierarchical relationships (e.g., breaking a recipe into Description, Sub-recipes, Ingredients, and Actions).
2. **Strip Presentation Elements**: Remove all visual formatting, implied hierarchies (e.g., font size differences), and hardcoded sequencing (e.g., numbered list periods).
3. **Define Semantic Hierarchy**: Wrap the stripped text in strictly defined, descriptive semantic tags that represent the true nature of the data.
4. **Apply Contextual Metadata**: Assign granular metadata tags to the structured modules to categorize the content by industry, audience, and subject matter.
5. **Modularize for Reuse**: Extract standalone components (e.g., a "Description" or a "Sub-recipe") into distinct modules that can be referenced by parent documents without modification.
6. **Establish Adaptation Rules**: Define how the structured modules can be mapped to different delivery channels, verifying that the semantic tags provide enough intelligence for a system to format the content dynamically.

@Examples (Do's and Don'ts)

**Semantic Structuring**
- [DO] `<Recipe><Title>Celery Salad</Title><Ingredients><Ingredient>Celery</Ingredient></Ingredients><Instructions><Step>Chop celery</Step></Instructions></Recipe>`
- [DON'T] `<h1>Celery Salad</h1><p><b>Ingredients:</b></p><ul><li>Celery</li></ul><p><b>Instructions:</b></p><ol><li>Chop celery</li></ol>` (This describes appearance and generic HTML concepts, not the actual meaning of the content).

**Handling Formatting and Sequence**
- [DO] `<Step>Chop carrots</Step>` (Relying on the automated publishing stylesheet to append the "1." and the period during rendering).
- [DON'T] `<Step>1. Chop carrots.</Step>` (Hardcoding the sequence number and punctuation directly into the content string).

**Translation and Reuse Optimization**
- [DO] Create a single `<Disclaimer>` module and reference it across 50 different product manuals. When the disclaimer changes, update the single source.
- [DON'T] Copy the text of the disclaimer into 50 separate documents. Adding a comma to one instance will cause the Translation Memory System (TMS) to mark it as new text, incurring unnecessary translation costs.

**Metadata Application**
- [DO] Attach key-value metadata to the component: `<Component id="123" metadata="industry:pharmaceutical; audience:pharmacist; subject:hypoglycemia">...`
- [DON'T] Rely solely on the document filename (e.g., `pharmacist_hypoglycemia_info.docx`) to provide context, leaving the internal content untagged and undiscoverable.