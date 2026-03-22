# @Domain
These rules MUST trigger whenever the AI is tasked with designing, architecting, structuring, or managing content creation workflows, Content Management System (CMS) configurations, multi-channel publishing systems, or information product models. They activate specifically when a request involves content reuse, single-sourcing, dynamic content assembly, multi-device content adaptation (e.g., Web, mobile, print, eBook), or reducing content duplication across an enterprise.

# @Vocabulary
*   **Reuse Strategy:** A defined plan specifying the method (manual vs. automated), security (locked vs. derivative), types of reuse, granularity, and governance rules for reusing content.
*   **Content Reuse:** The process of reusing specific pieces of content (e.g., a specific product description) across different outputs.
*   **Structural Reuse:** The process of reusing common structures or templates across a variety of information products (e.g., reusing the "Value Proposition" model for different products).
*   **Manual Reuse:** An author-driven process where a user searches for, retrieves, and inserts a link/pointer to a source component.
*   **Automated Reuse:** A system-driven process where reusable components are automatically inserted into documents based on information product models, metadata, and business rules.
*   **Locked Reuse:** Reusable content that cannot be changed by anyone other than the content owner (e.g., legal disclaimers, warnings).
*   **Derivative Reuse:** Reuse with change. The reused component becomes a "child" of the "parent" source, allowing local modifications while maintaining a synchronization link for future updates.
*   **Identical Reuse:** Content reused without any changes.
*   **Section-based Reuse:** Reusing an entire section or grouping of components at once (e.g., an entire training module).
*   **Component-based Reuse:** Reusing a discrete, self-contained piece of content with a specific subject and purpose.
*   **Conditional (Filtered) Reuse:** Housing multiple variant versions of content within a single component, using conditional tags/metadata to filter out irrelevant content during publication.
*   **Fragment-based Reuse:** Reusing a piece of a component (e.g., a single paragraph, step, or bullet point). 
*   **Warehouse Component:** A specialized component created specifically to group and hold multiple fragments of content for easier retrieval; it is never published as a whole component.
*   **Variable Reuse:** Utilizing named variables for small pieces of content that have different values in different situations (e.g., product names, regional measurements).
*   **Adaptive Content:** Content designed to scale and adapt automatically based on the constraints of the delivery channel by retrieving only the semantically appropriate component types.

# @Objectives
*   Eliminate the "copy and paste" anti-pattern; mandate reference-based (pointer) single-source reuse.
*   Ensure every reuse implementation explicitly defines the 5 parameters: method, security, type, granularity, and governance.
*   Maximize Content Management System (CMS) efficiency by balancing the high ROI of automated reuse with the flexibility of manual and derivative reuse.
*   Preserve content quality, tone, and usability; prevent the degradation of readability caused by forcing overly generic content into inappropriate contexts.
*   Support multi-channel adaptive design by associating the correct types of reusable components with the specific constraints of target devices (e.g., mobile vs. print).

# @Guidelines

### Core Architectural Rules
*   **The 5-Pillar Rule:** Whenever defining a new reuse architecture, the AI MUST explicitly establish: 1) Method (Manual/Automated), 2) Security (Locked/Derivative), 3) Types (Identical, Section, Component, Conditional, Fragment, Variable), 4) Granularity level, and 5) Governance strategy.
*   **Pointer Over Duplication:** The AI MUST explicitly configure reuse as a reference/pointer to a source component. The AI MUST NEVER recommend copying and pasting text.
*   **Structural vs. Content Segregation:** The AI MUST separate structural reuse (defining the empty elements in an Information Product Model) from content reuse (populating the specific text/data).

### Method Guidelines
*   **Manual Reuse:** When recommending manual reuse, the AI MUST mandate the implementation of rich metadata, strict categorization, and rigorous author guidelines to ensure authors can easily discover the content.
*   **Automated Reuse:** When recommending automated reuse, the AI MUST design strict Information Product Models that dictate exactly where content populates. The AI MUST restrict authors from deleting or modifying automatically populated required content.

### Security / Governance Guidelines
*   **Locked Reuse Constraints:** The AI MUST reserve Locked Reuse strictly for content that poses a legal, safety, or strict branding risk (e.g., copyright notices, warranty info, warnings). The AI SHOULD target a maximum of 10-15% of the overall content repository for Locked Reuse.
*   **Derivative Reuse Constraints:** The AI MUST restrict the proliferation of Derivative Reuse to prevent repository bloat. When implementing Derivative Reuse, the AI MUST establish a parent-child relationship workflow so the derivative author is automatically notified when the source parent is updated.

### Reuse Type Constraints
*   **Managing Output Variations:** The AI MUST use **Conditional Reuse** when dealing with content that slightly changes based on the delivery channel (e.g., a traditional table for print vs. a simplified list for mobile). All variants MUST be contained within the *same* single source component.
*   **Managing Micro-Variations:** The AI MUST NOT use Fragment-based Reuse for single words or short phrases. For minor text variations (e.g., regional spellings, product names, measurements like Celsius vs. Fahrenheit), the AI MUST use **Variable Reuse**.
*   **Managing Fragments:** When implementing Fragment-based Reuse (e.g., a single bullet or shared procedural step), the AI MUST group these fragments into a **Warehouse Component** to prevent them from getting lost in the CMS.

### Adaptive Design & Quality Constraints
*   **Device Context:** The AI MUST map reusable components to the constraints of the delivery channel. (e.g., For mobile outputs, the AI MUST retrieve only short, lookup-focused components, filtering out deep conceptual background components).
*   **Quality Veto:** The AI MUST NOT force reuse if the resulting component becomes so generic that it compromises comprehensibility. If a completely different tone or audience focus is required, the AI MUST advise creating a new, separate component or using Derivative Reuse.

# @Workflow
When tasked with designing or auditing a content reuse strategy, the AI MUST execute the following algorithm:

1.  **Define the Scope and Parameters:**
    *   Determine the target content set.
    *   Define the Granularity (Component-level, Section-level, Fragment-level).
    *   Define the Governance model (Who owns the source? Who is notified of changes?).
2.  **Determine the Reuse Method:**
    *   Select *Automated Reuse* if the content is highly structured, predictable, and compliance-driven. Map the specific metadata triggers.
    *   Select *Manual Reuse* if authors require maximum flexibility to mix-and-match content. Define the search/retrieval metadata taxonomy to support this.
3.  **Establish Security Rules:**
    *   Identify standard/legal content -> Apply *Locked Reuse*.
    *   Identify content requiring audience/regional tweaking -> Apply *Derivative Reuse*. Define the notification link between parent and child.
4.  **Select the Granular Reuse Types:**
    *   For exact matches -> Use *Identical Reuse*.
    *   For grouping modules -> Use *Section Reuse*.
    *   For discrete topics -> Use *Component Reuse*.
    *   For channel/audience variations in a single topic -> Use *Conditional Reuse*.
    *   For shared lists/steps -> Create a *Warehouse Component* and use *Fragment Reuse*.
    *   For terminology/measurement switching -> Use *Variable Reuse*.
5.  **Align with Adaptive Delivery Constraints:**
    *   Evaluate the target channels (e.g., Print, Web, Mobile).
    *   Establish filtering rules based on device constraints (e.g., Exclude heavy tables for eReaders; Exclude long-form concept components for Mobile apps).
6.  **Validate Quality and Context:**
    *   Review the resulting assembled output.
    *   Ensure the narrative flows logically. Ensure the attempt to maximize reuse percentage has not degraded the human readability of the text.

# @Examples (Do's and Don'ts)

### Principle: Implementation of Content Reuse Mechanism
*   **[DO]** Insert a dynamic reference link (e.g., `<conref href="components/legal/warranty.xml"/>` or equivalent CMS pointer) that pulls the source content into the active document at publish time.
*   **[DON'T]** Instruct the author to search for the warranty document, highlight the text, copy it, and paste it into the new brochure.

### Principle: Managing Channel Variations
*   **[DO]** Use **Conditional Reuse**: Create a single component named `Setup_Instructions`. Write both the print instructions and the mobile instructions inside this single component, tagging the print elements with `audience="print"` and the mobile elements with `audience="mobile"`. Let the publishing engine filter out the irrelevant tags.
*   **[DON'T]** Create two separate components named `Setup_Instructions_Print` and `Setup_Instructions_Mobile` and attempt to manage them independently as identical reuse blocks.

### Principle: Managing Micro-Text Differences
*   **[DO]** Use **Variable Reuse**: Write the sentence as "The patient's target reading is `<variable name="glucose_metric"/>`." Map the variable to display "blood sugar" for the US market and "blood glucose" for the UK market.
*   **[DON'T]** Use Fragment Reuse to isolate the words "blood sugar" and "blood glucose" and try to point to them contextually in the middle of sentences.

### Principle: Fragment Organization
*   **[DO]** Create a dedicated file called `Warehouse_Warnings.xml`. Store 50 different standalone warning fragments inside this file. When an author needs warning #12, they point specifically to fragment #12 inside the Warehouse component.
*   **[DON'T]** Tell an author to point to a warning that happens to be embedded halfway down page 4 of the "User Manual Chapter 2" component, making it impossible for future authors to discover it.

### Principle: Balancing Reuse with Quality
*   **[DO]** Use **Derivative Reuse** to take a standard corporate "Value Proposition" and rewrite it with a slightly different, more persuasive tone for a high-level executive sales pitch, linking it to the parent source so the author is notified if the core corporate specs change.
*   **[DON'T]** Force the author to use the exact **Identical Reuse** of a dry, highly technical product description in a flashy, consumer-facing mobile app just to hit an 80% content reuse metric.