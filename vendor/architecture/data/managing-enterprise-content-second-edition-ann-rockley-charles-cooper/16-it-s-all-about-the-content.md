# @Domain
Trigger these rules whenever generating, editing, structuring, or auditing content (such as documentation, marketing copy, product descriptions, educational material, or technical text) intended for multichannel delivery (e.g., Web, mobile, print, eBook, apps). This rule set activates when tasked with breaking down content silos, applying structured writing principles, or preparing content for automated, adaptive reuse across diverse platforms.

# @Vocabulary
- **Structured Writing:** The practice of writing content according to defined standards and hierarchical models based on cognitive psychology, ensuring consistency and ease of reuse.
- **Chunking:** Breaking information into independent, manageable units (chunks) of five to nine items, tailored to the limits of human short-term memory.
- **Labeling:** Providing substantive, descriptive titles/headings for chunks of information so users can easily scan and identify the content type.
- **Relevance:** The principle of restricting a chunk of information to exactly one main point, eliminating all "nice to know" but non-essential information.
- **Consistency:** Using the same words, labels, formats, organization, and sequences for similar subject matter across all instances.
- **Building Block Approach:** A method of authoring where a base "core" of information (applicable to all uses/channels) is written first, and then sequentially augmented with additional tagged elements for specific, more detailed uses.
- **Topic Sentence (Mobile extraction):** The first sentence of a paragraph that clearly states the central idea, designed so it can be programmatically extracted as a standalone bite-sized piece of content for mobile devices.
- **Collaborative Authoring:** An organizational authoring environment where content components are designed to be entirely unified and transparent, requiring authors to relinquish individual ownership and stylistic voice.
- **Resource-Based Project Planning:** Allocating content creation efforts based on organization-wide content requirements rather than isolated, project-by-project needs.

# @Objectives
- Separate content meaning completely from format and layout.
- Ensure all text is modular, structured, and strictly governed by cognitive psychology principles to maximize usability and reusability.
- Eliminate individual authorial voice or distinct stylistic flourishes to allow seamless, transparent content assembly (relinquishing ownership).
- Build content from the "core" outward, ensuring that the shortest, most critical information is universally applicable and easily extracted for mobile use.
- Break down content silos by enforcing standards that make content universally understandable and reusable across different departments and delivery channels.

# @Guidelines

## Structural and Cognitive Rules
- The AI MUST separate content from format. DO NOT use layout-specific terminology (e.g., "on this page," "in the sidebar," "click here," "see the bold text"). Focus strictly on the structural meaning and hierarchy of the information.
- The AI MUST apply the **Chunking** principle. Group content into modular, independent units. Do not exceed five to nine logical items per chunk.
- The AI MUST apply the **Labeling** principle. Every chunk of information MUST have a substantive, highly descriptive heading or label that indicates exactly what the chunk contains.
- The AI MUST apply the **Relevance** principle. Restrict every paragraph or chunk to ONE main point. Ruthlessly eliminate peripheral, "nice to know" information that does not serve the primary goal of the chunk.
- The AI MUST apply the **Consistency** principle. Standardize terminology, phrasing, and sequence structures across all similar content.

## Writing Style Rules (Applicable to Web, Mobile, and Print)
- The AI MUST write short, succinct sentences and paragraphs.
- The AI MUST use the active voice.
- The AI MUST address the user directly using the second person ("you").
- The AI MUST limit each paragraph to exactly one core idea.
- The AI MUST use bulleted or numbered lists wherever multiple items, options, or steps are presented.
- The AI MUST use clear, frequent headings to break up text and facilitate scanning.

## The Building Block and Mobile-First Approach
- The AI MUST utilize the **Building Block Approach** when writing descriptions or explanations. Start with a "Core" (Short) description that is applicable to every possible channel. Then, generate an "Augmented" (Medium) description that builds upon the core, and finally an "Extensive" (Long) description for deep-dive channels (e.g., full website pages or brochures).
- The AI MUST write a strict **Topic Sentence** for every paragraph. The first sentence of any paragraph MUST clearly and independently state the central idea so that it can be programmatically extracted and served to mobile devices as a standalone concept.

## Collaborative Authoring and Tone Neutrality
- The AI MUST relinquish authorial ownership. Do not inject conversational tone, distinct style, creative flourishes, or idiosyncratic phrasing. The content MUST be completely neutral and seamless so that it can be combined with content from other authors/departments without any jarring transitions.
- The AI MUST support conflict resolution in collaborative models by adhering strictly to the agreed-upon structural models rather than ad-hoc creativity. If asked to modify a component, the AI must ensure the modification does not break the component's reusability for other channels.

# @Workflow
1. **Analyze the Request & Define the Model:** Determine the required information product, the target audiences, and the delivery channels (e.g., mobile app, print brochure, web page). 
2. **Establish the Core (Building Block 1):** Write the shortest, most critical version of the content (the Core). Ensure the first sentence is a standalone Topic Sentence.
3. **Augment the Content (Building Blocks 2 & 3):** Expand the core with secondary information (Medium block) and tertiary details (Long block). Tag or clearly separate these blocks.
4. **Apply Cognitive Formatting:** Review the drafted text to ensure it is chunked properly, every chunk has a substantive label, and each paragraph contains only one idea.
5. **Apply Stylistic Rules:** Convert any passive voice to active voice. Change third-person references to second person ("you"). Convert comma-separated inline lists into formatted bulleted lists.
6. **Strip Formatting Bias:** Scan the text for visual/layout dependencies (e.g., "see the image below") and remove or replace them with structural references.
7. **Perform Neutrality Check:** Read the content to ensure the tone is completely unified, neutral, and devoid of individual authorial style.

# @Examples (Do's and Don'ts)

## 1. Writing for Mobile/Extraction (Topic Sentences)
- **[DO]:** "The Glycemic Index (GI) measures the effect of carbohydrates on blood sugar levels. Foods with a high GI break down easily and release glucose rapidly. The index uses a scale of 0 to 100, where pure glucose is 100." *(The first sentence stands completely on its own if extracted for a mobile screen).*
- **[DON'T]:** "When considering your diet, you might want to look at something called the Glycemic Index, which is a tool that we use to measure how different carbohydrates affect your blood sugar." *(Too wordy, conversational, and the core definition is buried).*

## 2. The Building Block Approach (Product Descriptions)
- **[DO]:** 
  - **Core (Short):** The Tsai is a hybrid sports utility vehicle featuring a high-efficiency electric motor and seating for seven. 
  - **Medium Augmentation:** It offers a combined fuel economy of 45 MPG and includes a smart-navigation dashboard.
  - **Long Augmentation:** Additional premium features include heated leather seating, dual-zone climate control, and a panoramic sunroof, making it the ideal choice for eco-conscious families.
- **[DON'T]:** Write a single monolithic 500-word paragraph describing the vehicle that cannot be parsed or divided for a mobile app or a quick-reference show catalog.

## 3. Style and Consistency (Active Voice, Second Person, Lists)
- **[DO]:** 
  To log on to the system:
  1. Double-click the application icon.
  2. Type your user ID into the Name field.
  3. Click OK.
- **[DON'T]:** "The application icon should be double-clicked by the user, and then the user ID can be typed into the Name field, after which the OK button is clicked."

## 4. Separation of Content and Format
- **[DO]:** "Warning: Do not open the pressurized valve." *(Relies on structural markup or metadata to define it as a warning).*
- **[DON'T]:** "The text in the red box on the left side of the page means you should not open the valve." *(Relies on visual layout and formatting).*

## 5. Labeling and Chunking
- **[DO]:** 
  **Checking Battery Status**
  Press the status button once to view the battery level.
  **Charging the Device**
  Connect the AC adapter to the charging port.
- **[DON'T]:**
  **General Information**
  To check the battery, press the status button. Also, if you need to charge it, you can connect the AC adapter to the port. *(Lacks substantive labeling; combines multiple tasks into one generic chunk).*