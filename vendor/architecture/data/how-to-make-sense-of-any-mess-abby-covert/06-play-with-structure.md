@Domain
Activates when the user requests assistance with structuring data, organizing content, designing navigation systems, establishing database schemas, creating sitemaps, defining metadata/tagging systems, architecting application routing, or outlining multi-step workflows.

@Vocabulary
- **Structure**: A configuration of objects. Unorganized piles, tables of contents, and houses of cards are all structures.
- **Taxonomy**: Methods and structural approaches for organizing and classifying content in ways that convey intended information to users.
- **Form**: The visual shape or configuration something takes, created when content is sorted into a structure for use. Forms combine multiple taxonomies.
- **Sorting**: The physical or programmatic act of arranging content according to strictly established rules.
- **Classification**: The act of deciding *how* to sort something within a taxonomy; the process of creating the rules themselves.
- **Exact Classification**: Precise categorization rules that hold steady and leave no room for argument (e.g., postal codes). Exactitude costs flexibility.
- **Ambiguous Classification**: Subjective categorization open to interpretation and argument (e.g., movie genres). Ambiguity costs clarity and hides in simplicity.
- **Facet**: A discrete piece of knowledge, attribute, or metadata that can be used to classify something (e.g., record name, artist, length, price).
- **Hierarchy**: A taxonomy arranged in successive categories, ranks, or interrelated levels.
  - **Broad and Shallow Hierarchy**: Gives the user many choices up front so they can get to everything in a few steps.
  - **Narrow and Deep Hierarchy**: Gives the user fewer choices at once, requiring deeper traversal.
- **Heterarchy**: A taxonomy where individual pieces exist on a single level without further categorization or rank.
- **Sequence**: A taxonomy based on the order in which something is experienced. Can be logical (linear) or complex (alternative paths/variations based on conditions).
- **Hypertext**: A taxonomy that connects related items through user action, bridging other taxonomies without moving or duplicating content.

@Objectives
- Continuously explore, propose, and compare multiple structural configurations before settling on a final architecture.
- Explicitly separate the act of defining classification rules from the act of sorting data.
- Intentionally balance exact and ambiguous classification methods based on user context and system requirements.
- Combine multiple taxonomic patterns (hierarchies, heterarchies, sequences, and hypertext) to create a comprehensive and intuitive form.
- Use lightweight, conceptual modeling (boxes and arrows) to test structural logic before committing to detailed implementation.

@Guidelines
- **Mandatory Structural Iteration**: NEVER settle for the first structure you generate. You MUST design at least two to three distinct structural approaches for the user to compare, argue against, and refine.
- **Classification Precedes Sorting**: You MUST establish and document clear, unambiguous classification rules before attempting to sort or organize any actual data or content. 
- **Eradicate Hidden Ambiguity**: You MUST identify simple instructions that harbor hidden ambiguity (e.g., "alphabetize this" without specifying "by first name or last name") and replace them with exact logic.
- **Contextual Worldview Alignment**: When defining taxonomies, you MUST evaluate whether the classification serves the specific mental model of the intended user, acknowledging that standard scientific or exact classifications (e.g., "a tomato is a fruit") may fail in contextual use cases (e.g., a grocery store UI).
- **Facet Viability Check**: Before utilizing a facet (metadata field) for classification, you MUST explicitly evaluate the cost/effort of gathering that data. Discard interesting facets if the supporting data is practically impossible or overly time-consuming to collect.
- **Taxonomic Blending**: NEVER force all content into a single taxonomic pattern. You MUST combine patterns appropriately:
  - Use *Hierarchy* for foundational navigation and categorization.
  - Use *Heterarchy* for flat databases, item lists, or tag pools.
  - Use *Sequence* for multi-step processes, wizards, checkouts, or forms.
  - Use *Hypertext* (symlinks, pointers, relational keys) to connect disparate items.
- **Zero-Duplication Rule**: You MUST utilize Hypertext patterns (references/pointers) to bridge taxonomies rather than duplicating content across multiple locations in a hierarchy.
- **Hierarchy Depth Justification**: You MUST explicitly declare and justify whether a hierarchy is "Broad and Shallow" or "Narrow and Deep" based on the volume of information and the user's need for immediate choices vs. guided steps.

@Workflow
1. **Analyze Content & Facets**:
   - Inventory the objects, data, or content to be organized.
   - List all available facets (discrete attributes) for the content.
   - Filter out facets where data is unavailable or too costly to maintain.
2. **Determine Classification Paradigms**:
   - Define which aspects of the structure require Exact Classification (e.g., IDs, region codes) and which require Ambiguous Classification (e.g., themes, tags).
   - Write out explicit classification rules to remove hidden ambiguity.
3. **Conceptualize with Boxes and Arrows**:
   - Create a low-fidelity text-based diagram (using ASCII/Markdown boxes and arrows) to map out the structure conceptually.
   - Avoid adding styling, code, or polish at this stage; keep the structure pliable.
4. **Develop Alternative Structures**:
   - Generate at least two fundamentally different structural arrangements using different combinations of Hierarchical, Heterarchical, Sequential, and Hypertext taxonomies.
   - Present these alternatives to the user for comparison and iteration.
5. **Combine and Finalize Form**:
   - Integrate feedback to refine the chosen structure.
   - Ensure the final architecture explicitly employs Hypertext to prevent duplication and cross-link related taxonomies.
   - Output the finalized structure (e.g., JSON schema, folder tree, routing table).

@Examples

**Example 1: Defining Sorting Rules**
- [DO]: Establish exact classification rules before execution. "Sort user records alphabetically by Last Name, then by First Name. If Last Name is identical, sort by Date of Account Creation (ascending)."
- [DON'T]: Provide ambiguous instructions that hide complexity. "Sort the user records alphabetically."

**Example 2: Combining Taxonomic Patterns**
- [DO]: Architect a system using multiple lenses: "The application will use a Broad and Shallow Hierarchy for the main navigation bar. The product inventory will be stored as a Heterarchy (flat database) using facets like 'Price' and 'Category' for filtering. The checkout process will be a Sequence with alternative paths for guest vs. registered users. Related products will be linked via Hypertext references to avoid database duplication."
- [DON'T]: Force everything into a single pattern: "Put all the application features into a deeply nested hierarchy, requiring the user to click 6 times to find the checkout screen, and duplicate the 'Batteries' product entry inside every single electronics sub-folder."

**Example 3: Contextual Classification over Pedantic Accuracy**
- [DO]: Classify items based on the user's mental model for the specific context. "For this grocery delivery app, we will classify 'Tomatoes' under 'Vegetables' because that matches culinary usage and customer expectations."
- [DON'T]: Use overly exact classification that breaks the user's mental model. "Classify 'Tomatoes' exclusively under 'Fruit', forcing grocery shoppers to look alongside apples and oranges."

**Example 4: Conceptualizing Before Implementation**
- [DO]: Use simple visual structures to test logic first.
  ```text
  [ Home ] --> [ Dashboard ]
                   |
                   +-- (Sequence) --> [ Step 1 ] -> [ Step 2 ] -> [ Complete ]
                   |
                   +-- (Hypertext) -> [ User Settings ]
  ```
- [DON'T]: Immediately write thousands of lines of React Router code without mapping the structural relationships and sequences first.