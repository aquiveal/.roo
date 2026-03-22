# @Domain
The AI MUST activate and apply these rules when processing requests related to Information Architecture (IA), content organization, taxonomy and ontology creation, navigation design, database metadata structuring, classification schemes, or evaluating user-centered categorization of digital and physical items.

# @Vocabulary
*   **Information Architecture (IA)**: The structural design of shared environments; organizing and labeling items so people can find and use them.
*   **Hierarchical Structure**: A top-down or bottom-up organizational model where groups are broken down into sub-groups (e.g., file folders, organizational charts).
*   **Database Structure**: A flat organizational model resembling a bucket of objects where items are stored independently and structured via metadata tags, allowing dynamic resorting.
*   **Classification Scheme**: The governing logical principle used to sort items. 
*   **Topic Scheme**: Organizing by subject matter, aspect, or functional characteristic (e.g., sorting wine by flavor profile).
*   **Chronology Scheme**: Organizing by a defined point or range of time.
*   **Geography Scheme**: Organizing by location or physical origin.
*   **Alphabetical Scheme**: Organizing strictly by the A-Z name of the item.
*   **Numerical Scheme**: Organizing sequentially by count, measure, or quantitative performance.
*   **Task Scheme**: Organizing by a series of user actions or steps (common in applications).
*   **Audience Scheme**: Organizing by user demographic or role.
*   **Classical View of Categories**: A flawed, rigid mental model treating categories as discrete abstract containers with clear boundaries where all members are perfectly equal and mutually exclusive.
*   **Family Resemblance**: The cognitive reality that items in a category share overlapping similarities rather than a single unifying identical trait.
*   **Extendable Boundaries**: The fluid nature of categories, allowing new or novel items to stretch the definition of the group (e.g., adding "online multiplayer" to the category of "games").
*   **Central Member / Prototypical Item**: The "best" or most representative example of a category (e.g., a "kitchen chair" for chairs, or a "robin" for birds).
*   **Basic-Level Category**: The cognitive "middle" level of a hierarchy that people naturally think in. It is learned earliest, has a short common name, and evokes a single mental image (e.g., "Dog" instead of the overly broad "Mammal" or the overly specific "Dalmatian").

# @Objectives
*   The AI MUST organize information strictly based on user context, mental models, and usage needs, entirely discarding the assumption that there is "one true way" to structure data.
*   The AI MUST design classification systems that account for the fluidity of human cognition, embracing overlapping boundaries, family resemblance, and basic-level categories.
*   The AI MUST select the appropriate structural model (Hierarchy vs. Database) and combination of classification schemes (Topic, Task, Chronology, etc.) tailored precisely to the data type and the user's operational context.
*   The AI MUST generate labels that are universally understood, contextually appropriate, and free of isolating jargon.

# @Guidelines

## General Organizational Rules
*   **Embrace Multiplicity**: The AI MUST recognize that digital information can exist in multiple places simultaneously. It MUST NOT force items into a single category if they logically belong in several.
*   **Context Dependency**: The AI MUST define the user's task context before proposing an organizational structure (e.g., a site's structure may need to shift from "broad topics" to "specific logistics" depending on the user's timeline or phase).
*   **Labeling Rigor**: The AI MUST standardize labels, resolving internal jargon, colloquialisms, and synonyms. When encountering "one of these things is not like the others" (a mismatched menu term), the AI MUST re-evaluate and align the tone, granularity, and format of the outlier to match the set.

## Structural Constraints
*   **Hierarchy Use-Case**: The AI MUST prescribe a Hierarchical Structure when users need to drill down from broad concepts to specific sub-groups organically.
*   **Database Use-Case**: The AI MUST prescribe a Database Structure when managing content with consistent, repeatable features (e.g., product catalogs, event lists). The AI MUST define the structural metadata required for this (e.g., Title, Speaker, Time, Location).

## Classification Scheme Selection
*   **Topic**: The AI MUST use this as the default or primary scheme for most general content, adapting the 'subject' to the user's mental model.
*   **Chronology**: The AI MUST use this for time-dependent content (news, events) but MUST ALWAYS pair it with a secondary scheme (like Topic or Geography) because time alone rarely satisfies all user tasks.
*   **Geography**: The AI MUST limit this to explicitly location-based needs (travel, localized events) and MUST NOT use it if the user only cares about the item's traits, not its origin.
*   **Alphabetical**: The AI MUST restrict this scheme strictly to scenarios where the user (1) knows exactly what they are looking for, (2) knows what it is called, AND (3) their naming convention identically matches the system's labels. It MUST typically be a secondary scheme.
*   **Numerical**: The AI MUST use this for sorting/sequencing lists (price, capacity, popularity) rather than for primary content grouping.
*   **Task**: The AI MUST utilize this primarily for interactive applications or transactional interfaces (Shop, Send, Learn), rather than content-heavy knowledge bases.
*   **Audience**: The AI MUST AVOID audience schemes unless the audiences are clearly defined, users perfectly self-identify, and content does NOT heavily overlap. If content overlaps across audiences, the AI MUST pivot to a Topic scheme.

## Cognitive Categorization Rules
*   **Abandon the Classical View**: The AI MUST NOT attempt to create perfect, mutually exclusive, collectively exhaustive categories. It MUST allow for messy boundaries and edge cases.
*   **Target the Basic-Level**: When generating primary navigation or top-level groups, the AI MUST formulate "Basic-Level Categories". It MUST NOT use terms that are too abstract (e.g., "Canine") or too granular (e.g., "Poodle") when the basic level ("Dog") is the natural cognitive entry point.
*   **Utilize Prototypicality**: When validating a category, the AI MUST ensure the category contains clear "Central Members" (prototypes) to establish the group's meaning to the user.

# @Workflow
To properly organize a provided dataset, content inventory, or abstract concept list, the AI MUST execute the following algorithm:

1.  **Contextual Profiling**: Determine the target user's context. Identify *why* the user needs the information, *what* their primary tasks are, and *when* they are accessing it.
2.  **Structural Assessment**: Analyze the content items. If they are diverse nested concepts, establish a `Hierarchical Structure`. If they are uniform items with repeatable attributes, establish a `Database Structure` and explicitly define the metadata fields.
3.  **Classification Mapping**: Evaluate the content against the seven schemes (Topic, Chronology, Geography, Alphabetical, Numerical, Task, Audience). Select the optimal Primary scheme. If the Primary scheme creates task friction, select a Secondary scheme to provide faceted filtering or alternative views.
4.  **Cognitive Leveling (Category Creation)**: Group the content. Adjust the granularity of the group labels up or down the hierarchy until they reach the "Basic-Level Category" for the target audience.
5.  **Prototypical Validation**: For each created category, identify its most central/prototypical item. If a category lacks a clear prototype, or if the items share no "family resemblance", dissolve and reorganize the category.
6.  **Boundary Smoothing (Edge Cases)**: Identify items that fit into multiple categories. In a Database structure, tag them with multiple metadata values. In a Hierarchy, duplicate the entry or provide cross-links rather than forcing a false mutual exclusivity.
7.  **Label Standardization**: Review all generated category names. Remove internal jargon, ensure parallel phrasing, and eradicate outliers.

# @Examples (Do's and Don'ts)

## Selecting Classification Schemes
*   **[DO]**: Use a Topic scheme (e.g., "Taste: Sweet, Dry, Bold") for a wine retail site where casual users want a specific flavor to pair with dinner.
*   **[DON'T]**: Use a Geographic scheme (e.g., "Regions: Bordeaux, Napa, Barossa") for casual wine buyers who do not understand global wine regions, causing navigation failure.

## Audience Schemes
*   **[DO]**: Use an Audience scheme ONLY when user needs are completely walled off (e.g., "Prospective Students" vs. "Current Faculty").
*   **[DON'T]**: Use an Audience scheme for internal corporate intranets (e.g., "Managers" vs. "Sales Staff") when both groups frequently need the exact same HR and procedure documents, leading to confusion over where to look.

## Basic-Level Categories
*   **[DO]**: Use "Chairs", "Tables", and "Beds" for a standard furniture e-commerce navigation menu.
*   **[DON'T]**: Use overly broad labels like "Indoor Dwellings" or overly specific labels like "Ergonomic Mesh Task Chairs" as primary top-level categories.

## Alphabetical Ordering
*   **[DO]**: Use Alphabetical sorting for a medical glossary where users know the exact scientific name of the condition they are looking up.
*   **[DON'T]**: Use Alphabetical sorting as the primary navigation for a clothing store (e.g., "A - Argyle Sweaters, B - Blue Jeans") because users browse by garment type, not by the specific spelling of the item's name.

## Handling Boundaries
*   **[DO]**: Allow a recipe containing chicken, noodles, and broth to exist simultaneously under "Soups", "Poultry", and "Winter Warmers" in a digital database.
*   **[DON'T]**: Force the user to guess which single rigid classical container the recipe was placed in because "categories must be mutually exclusive."