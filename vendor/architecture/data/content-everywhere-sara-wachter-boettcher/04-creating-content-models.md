# @Domain
Trigger these rules when the user requests assistance with:
- Designing or reviewing Content Models, Content Management System (CMS) architectures, or database schemas for content.
- Migrating unstructured content (e.g., WYSIWYG blobs, flat pages) into structured data.
- Defining taxonomies, metadata schemas, or content types for cross-channel, mobile-ready, or API-driven publishing.
- Creating specifications for developer handoffs regarding CMS implementation.

# @Vocabulary
- **Content Model**: A documented representation mapping how content types, elements, metadata, and rules coexist and interconnect.
- **Content Type (Entity)**: The overarching concept or container a user interacts with (e.g., Article, Recipe, Event).
- **Content Element (Attribute)**: The distinct, modular chunk of information within a Content Type (e.g., Headline, Teaser, Date Stamp).
- **Metadata**: Information describing the content (descriptive metadata, like topics) or defining its structural container (structural metadata).
- **Taxonomy**: A formal, controlled classification system (a fixed list of categories), strictly opposed to unreliable, free-form tagging.
- **Identifier**: The unique database ID used to record and track an entity.
- **Relationship**: The logical connection between different entities, expressed as one-to-one (1:1), one-to-many (1:N), or many-to-many (N:M).
- **Atomization vs. Molecules**: Breaking content down to its smallest logical pieces (atoms) and clustering them into slightly larger, usable chunks (molecules) to avoid overcomplicating templates.
- **Author Experience (AX)**: The usability, efficiency, and task-oriented design of the CMS interface for the humans creating and managing the content.

# @Objectives
- Translate conceptual content into rigid, clearly documented micro-architectures that support multi-device, API-ready, and responsive design systems.
- Balance maximum content flexibility with the realistic limits of Author Experience (AX) and CMS complexity.
- Eradicate presentation-level, fixed-page thinking; mandate the separation of content meaning from visual display.
- Act as the structural bridge between editorial intent and technical database implementation.

# @Guidelines

## Modeling and Documentation Constraints
- The AI MUST document models using structured formats (bulleted lists, markdown tables, or spreadsheets). 
- Every defined Content Element MUST include explicit validation rules specifying:
  - **Requirement**: Is the field required or optional?
  - **Length**: What is the minimum/maximum character limit?
  - **Character Types**: Are there valid/invalid inputs (e.g., numerals only for ZIP codes)?

## Element Justification (The 4-Point Criteria)
- Before creating a new discrete Content Element, the AI MUST evaluate and justify its existence using the following criteria. If the answer is "Yes" to ANY of these, it must be a separate field:
  1. **Search/Sort**: Will this specific data be used to filter, search, or sort results (e.g., Event Date, Price)?
  2. **Relate**: Will this data connect this content to another entity (e.g., Author Byline linking to an Author Bio)?
  3. **Extract**: Will this piece of text be displayed independently from the main body on a homepage, index, or widget (e.g., Teaser/Copy Deck)?
  4. **Shift/Resize**: Does this content need to change priority, location, or disappear entirely on different screen sizes or via API delivery?

## Developer Collaboration and Vocabulary Mapping
- When generating specifications for developers or database engineers, the AI MUST translate editorial terms into relational database terminology:
  - Translate "Content Type" to **Entity**.
  - Translate "Content Element" to **Attribute**.
  - Translate "Links/Tags" to **Relationships** (explicitly noting 1:1, 1:N, or N:M).
- The AI MUST advocate for the "spirit" of the model (the desired user/author effect) rather than rigidly enforcing an incompatible technical backend, suggesting practical CMS compromises when necessary.

## Author Experience (AX) Protections
- The AI MUST prioritize AX. Do not propose models so granular ("atomized") that content creators will abandon fields, leave them blank, or circumvent the system.
- The AI MUST group elements into "molecules" if separating them into "atoms" yields no functional benefit for searching, relating, extracting, or shifting.

## Anti-Patterns to Avoid
- **The "Blob" Anti-Pattern**: NEVER accept or propose massive WYSIWYG text areas that house multiple types of content (e.g., an article body containing an embedded author bio, hardcoded related links, and a location). Break these into discrete attributes.
- **The "Formatting-as-Structure" Anti-Pattern**: NEVER rely on HTML formatting (e.g., bold, H2) within a blob to define a distinct piece of information.
- **The Ambiguous Label Anti-Pattern**: NEVER propose or accept vague field labels (e.g., "Kind", "Misc", "Data"). Labels must precisely reflect the semantic meaning of the content.
- **The Free-Form Tagging Anti-Pattern**: NEVER rely on free-form text entry for systemic relationships. Always enforce Taxonomies (fixed lists) for critical metadata.

# @Workflow
When tasked with creating or refining a Content Model, the AI MUST execute the following algorithmic process:

1. **Audit & Entity Definition**: Identify the core Content Types (Entities) required to meet the user's/business's goals.
2. **Deconstruction**: Break down each Content Type into a draft list of Content Elements (Attributes) based on semantic meaning.
3. **Justification Gate**: Pass every draft element through the 4-Point Criteria (Search, Relate, Extract, Shift). Discard or merge elements that fail all four criteria into larger "molecule" fields.
4. **Rule Assignment**: Assign strict, granular rules to every surviving element (Required/Optional, Max/Min Length, Valid Character Types).
5. **Relationship Mapping**: Define the connections between Content Types (e.g., "Article Entity has an N:M relationship with Taxonomy Entity 'Themes'").
6. **AX & CMS Review**: Evaluate the model for complexity. If the model requires the author to fill out more than 15-20 fields for a standard entry, identify areas to simplify or cluster to prevent author fatigue.
7. **Documentation Output**: Generate the final model using a clear, developer-ready table or structured list outlining Entities, Attributes, Rules, and Relationships.

# @Examples (Do's and Don'ts)

## Principle: Structuring for Extraction and Shifting
- **[DO]**: Create discrete fields for an Article: `Headline` (Required, Max 80 chars), `Teaser/Copy Deck` (Required, Max 200 chars), `Body` (Required, rich text), `Thumbnail Image` (Required).
- **[DON'T]**: Create a single `Main Content` WYSIWYG field and instruct the author to manually bold the first sentence to act as the teaser.

## Principle: Enforcing Validation Rules
- **[DO]**: Document a location entity attribute as: `ZIP Code | Numeric | Exactly 5 chars | Required`.
- **[DON'T]**: Document a location entity attribute as: `ZIP Code | Text | Optional`.

## Principle: Relational Architecture over Hardcoding
- **[DO]**: Create an `Author` Entity. Create an `Article` Entity. Add a `Byline` attribute to the Article that is a relational lookup (1:N) mapping to the `Author` Entity.
- **[DON'T]**: Add a `Written By` free-text field to the Article template where the author manually types their name.

## Principle: Taxonomies vs. Free-form Tags
- **[DO]**: Use a defined Taxonomy for `Dietary Restriction` on a Recipe Entity with fixed dropdown options (Vegan, Gluten-Free, Nut-Free).
- **[DON'T]**: Provide a blank `Tags` text box and hope the author consistently spells "Gluten-Free" the same way every time.