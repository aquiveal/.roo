@Domain
This rule set is triggered when the AI is tasked with content strategy, multi-channel content design, structured authoring, CMS/XML content structuring, designing templates for information products, or defining metadata and architectures for cross-platform publishing (Web, mobile, eBooks, print).

@Vocabulary
*   **Adaptive content:** Format-free, device-independent, scalable, and filterable content that automatically transforms for display in different environments based on device capabilities and user interactions.
*   **Content modeling:** The process of determining the exact hierarchical structure and granularity of content.
*   **Information product:** An assembly of content components representing a final deliverable (e.g., a press release, an executive profile, a brochure, a training course).
*   **Information product model (IPM):** The hierarchical ordering of components that defines an Information Product. It acts as a reproducible template.
*   **Component:** The discrete building blocks of content that can be reused across and within various Information Products.
*   **Component model:** The structural definition of a specific type of content (e.g., a recipe, a value proposition).
*   **Element:** The smallest part of a component that can be semantically defined but cannot be logically broken out into a separate reusable component.
*   **Granularity of reuse:** The definition of the size of the components to ensure they are logically self-contained chunks of information capable of being reused across IPMs.
*   **Granularity of structure:** The definition of the semantic structure *within* a component (the elements) that guides authors and allows system rules to filter content dynamically.

@Objectives
*   The AI MUST separate content meaning and structure from visual formatting entirely.
*   The AI MUST NOT "handcraft" content for a single specific output (e.g., "mobile-first" or "eBook-first"). Content must be modeled for purpose, scope, use, and reuse.
*   The AI MUST build structured, nested hierarchies consisting of Information Product Models -> Component Models -> Elements.
*   The AI MUST design models that automatically adjust to known device constraints (especially mobile and eBooks) by layering and filtering information rather than just resizing visual layouts.

@Guidelines
*   **Format Independence:** 
    *   The AI MUST NOT use layout-specific terminology (e.g., "columns," "floats," "fonts") when defining content models. Use semantic tags (e.g., "Overview," "Benefit," "Warning").
*   **Managing Mobile Constraints:**
    *   When structuring components, the AI MUST place the most critical information in the very first sentence or paragraph (the "building block" approach) so subsequent details can be filtered out or hidden behind a "Read more" function for small screens.
    *   The AI MUST modularize heavy text and rich media so that systems can deliver smaller file chunks, protecting mobile users from slow download speeds and high connection costs.
*   **Managing eBook Constraints:**
    *   The AI MUST NOT structure models that rely on complex tables (greater than four or five columns and rows) if the content targets eBooks.
    *   The AI MUST sequence layout-specific structures linearly. Sidebars or margin notes MUST be modeled to appear immediately *after* the content they logically relate to, rather than beside it.
    *   The AI MUST NOT embed images within text paragraphs or wrap text around images in the model structure.
*   **Granularity Constraints:**
    *   The AI MUST define elements only down to the sentence, paragraph, or discrete data field level. 
    *   The AI MUST NOT model granularity down to the individual word level. To handle word variations, the AI MUST use variables/metadata instead of structural elements.
    *   The AI MUST ensure that every granular element retains its contextual meaning if extracted and used independently.
*   **Authoring Guidance:**
    *   For every Element in a Component Model, the AI MUST generate explicit structured authoring guidelines (e.g., defining target audience, tone, scannability, and mandatory sentence structures).

@Workflow
When tasked with modeling content for a project or deliverable, the AI MUST execute the following algorithmic process:

1.  **Define the Information Product Model (IPM):** 
    *   Identify the final deliverables (e.g., Product Brochure, Mobile App Page).
    *   Determine the hierarchical list of Components required to build this product.
2.  **Define the Component Models (Granularity of Reuse):** 
    *   Identify which chunks of information are logically self-contained (e.g., "Value Proposition", "Product Overview").
    *   Map where these Components will be reused across different IPMs.
3.  **Define the Elements (Granularity of Structure):** 
    *   Break each Component down into its smallest semantically definable parts (e.g., a "Value Proposition" component breaks down into "The Value", "Competitive Differentiators", and "Cost of Offering" elements).
4.  **Apply Device Constraint Filters:** 
    *   Annotate Elements with filtering rules based on device constraints (e.g., flag a complex comparison table element to be excluded or swapped for a simplified list on mobile/eBook outputs).
    *   Ensure the core message is isolated in the primary element for mobile delivery.
5.  **Generate Authoring Guidelines:** 
    *   Output a strict set of rules for the human or system author detailing exactly how to write the content for each Element to guarantee consistency and reusability.

@Examples (Do's and Don'ts)

**[DO] Example of a correctly structured Component Model with filtering and guidelines:**
```json
{
  "ComponentModel": "Value_Proposition",
  "Elements": [
    {
      "Name": "Value_Core_Sentence",
      "Constraint_Mobile": "Primary Display",
      "Authoring_Guideline": "Write a single, active-voice sentence explaining the compelling reason the customer will buy the product."
    },
    {
      "Name": "Competitive_Differentiators",
      "Constraint_Mobile": "Hidden behind 'Read More'",
      "Authoring_Guideline": "Provide a bulleted list describing what makes the product better than competitive alternatives. Limit to 3 bullets."
    },
    {
      "Name": "Cost_Of_Offering_List",
      "Constraint_eBook": "Display sequentially below Differentiators",
      "Authoring_Guideline": "List the cost details linearly. Do not use tables."
    }
  ]
}
```

**[DON'T] Example of an incorrect, format-bound, and poorly granular model:**
```html
<!-- INCORRECT: Uses layout tags, word-level granularity, and complex eBook-breaking tables -->
<div class="two-column-layout">
  <div class="sidebar" style="float:left;">
    <p>Target Audience: <word-variable>Teens</word-variable></p>
  </div>
  <table columns="10" rows="15">
     <!-- Complex table that will break eReaders -->
  </table>
</div>
```

**[DO] Example of handling eBooks sidebars (Serialization):**
*Rule:* Model the main concept element first, followed immediately by the sidebar element, ensuring sequential readability without relying on CSS floats or margin-anchoring.

**[DON'T] Example of word-level granularity:**
*Rule:* DO NOT define `<subject_pronoun>` or `<verb_tense>` as elements in the model. If minor text variations are needed, define a single sentence element and apply a system variable tag like `{Region_Currency}`.