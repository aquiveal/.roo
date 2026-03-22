@Domain
These rules MUST be triggered whenever the AI is tasked with designing, architecting, or structuring content management systems (CMS), website architectures, omnichannel strategies, content models, content matrices, metadata schemas, taxonomies, or page-level content layouts.

@Vocabulary
- **Strategic Intent**: The overarching strategy defining who the audience is, what business and consumer goals the content fulfills, in which channels it resides, and when it is required.
- **Content Type**: A representation of the essence of the content itself (e.g., Annual reports, FAQs, Press releases, Videos). Separated from format types, though media like video/images are treated as content types when they possess unique lifecycles.
- **Content Lifecycle**: The end-to-end process a piece of content undergoes: Acquire, Create, Review, Publish, Measure, Optimize, and Archive.
- **Page-Level Strategic Intent**: A blueprint required before wireframing that defines the specific intent, goals, objectives, audience, content requirements, and prioritization for a specific page or template to prevent the "NASCAR effect" (cluttered, disconnected content).
- **Content Matrix**: A content-capture tool mapping consumer-facing content elements to wireframes, used by authors to input copy into a CMS.
- **Content Model**: A design blueprint for technology implementation, mapping content types to system templates, logic, metadata, character limits, and system data.
- **Editorial Guidelines**: Authoring guidelines specific to an experience (e.g., how to write a homepage), drawing from voice/tone but focusing on structural and contextual requirements.
- **Omnichannel**: A user-centric approach tailoring content across all customer journey touchpoints (analog, digital, in-store), rather than simply publishing the same content everywhere.
- **Responsive Design**: A design approach used when channels share the exact same content, optimizing the layout across devices.
- **Adaptive Design**: A design approach used when content is unique or optimized specifically for different channels/devices.
- **Shared Content**: Content that remains exactly the same regardless of channel (e.g., a logo).
- **Shared-but-edited Content**: Content that remains thematically the same but is optimized for the channel (e.g., long description for desktop, short for mobile).
- **Unique per channel Content**: Content existing only in one or two specific channels (e.g., a QR scan function on a mobile app).
- **Intelligent Content**: Content that is structured, modular, reusable, format-free, and tagged with metadata to enable personalization and omnichannel delivery.
- **Predictive Search / Semantic Web**: Logic specifying relationships between units of content driven by ontologies and metadata to predict user intent.

@Objectives
- To architect content experiences that are structurally sound, scalable, and inherently tied to business and consumer objectives.
- To prevent UI/UX design from preceding content strategy (i.e., avoiding the design of containers without knowing the content requirements).
- To distinguish clearly between content capture (Matrix) and technology implementation (Model).
- To engineer intelligent content workflows that enable personalization, dynamic recommendation, and true omnichannel distribution.
- To establish strict metadata and taxonomical rules that disambiguate terms, drive search, and facilitate content reuse.

@Guidelines

**1. Strategic Intent Generation**
- The AI MUST NEVER generate page structures, CMS architectures, or code without first defining or requesting the Strategic Intent.
- The AI MUST structure the Strategic Intent with exactly five components: 
  1. Mission of the site/experience.
  2. Objectives the site/experience must achieve.
  3. Audience (targeted consumers) and channels.
  4. Types of content necessary to support the experience.
  5. Prioritization of that content.

**2. Page-Level Strategic Intent Enforcement**
- Before generating wireframe code (HTML/CSS/React), the AI MUST define a Page-Level Strategic Intent to prevent the "NASCAR effect".
- This definition MUST include: Intent of the page, Goal, Objectives, Audience, Required Content (specific themes, not just types), Priority of content, and Channels.

**3. Content Types and Lifecycles**
- The AI MUST identify and list specific Content Types for any architecture. 
- The AI MUST NOT conflate format (e.g., PDF) with Content Type (e.g., Annual Report), except for media requiring unique workflows (Videos, Images).
- When asked to map workflows, the AI MUST use the standard lifecycle stages: Acquire, Create, Review, Publish, Measure, Optimize, Archive.
- The AI MUST define workflows using a "Swim-lane" approach (mapping Actors to Actions/States).

**4. Content Matrix vs. Content Model Architecture**
- **Content Matrix (Copy/Content Capture):** When creating a Matrix, the AI MUST output a structure containing these exact fields: Sitemap ID#, Wireframe ID, Page Title, CMS template, Level 1 field, Level 2 field, Level 3 field, Copy or label, and URL. It MUST include accessibility requirements (e.g., alt text) and SEO metadata directly in the matrix.
- **Content Model (Tech/Database Blueprint):** When creating a Model, the AI MUST output a structure containing these exact fields: ID#, Sitemap/Wireframe ID, CMS template, Content type, Content object/module (levels 1-x), Persona or consumer target, Authenticated (Yes/No), Format, Max/Min character length, New/Migrated, Source, Other rules (business logic), and Metadata.

**5. Building Content Logic and Personalization**
- The AI MUST define rules for dynamic content based on the following logic types: Cross-sell/up-sell, Recommendation logic, Personalization, and Semantic web.
- When defining Personalization, the AI MUST explicitly separate rules for Authenticated users (driven by profile data) vs. Unauthenticated users (driven by point of entry, clickstream, location, time, or device).

**6. Omnichannel and Multichannel Rules**
- The AI MUST evaluate required content and categorize it as: Shared, Shared-but-edited, or Unique per channel.
- The AI MUST recommend Responsive Design ONLY for "Shared" content.
- The AI MUST recommend Adaptive (or Hybrid) Design when content is "Shared-but-edited" or "Unique per channel".
- The AI MUST design content to be Structured, Modular, Reusable, Metadata-driven, and Format-free.

**7. Taxonomy and Metadata Standards**
- The AI MUST define metadata schemas supporting inheritance (e.g., Level 3 inherits Level 2 metadata).
- The AI MUST structure taxonomy definitions using the following columns/fields: Level 1, Level 2, Level 3, Synonyms (Synonym Rings), Consumer-facing nomenclature, and System metadata rules.

@Workflow
When tasked with designing a new content experience, website, or CMS structure, the AI MUST strictly follow this algorithmic process:

1. **Establish Macro Strategic Intent**: Output the 5-point strategic intent (Mission, Objectives, Audience, Content Types, Priorities).
2. **Define Content Types & Lifecycles**: List all required content types. If asked for workflows, generate a swim-lane matrix mapping the 7 lifecycle steps to actors.
3. **Establish Page-Level Intent**: For each major page/view, output the 7-point page-level strategy (Intent, Goal, Objectives, Audience, Required Content, Priority, Channels) to dictate the UX.
4. **Generate Matrix or Model**: 
   - If the user needs to capture copy/text: Generate a Content Matrix.
   - If the user is building the database/CMS backend: Generate a Content Model.
5. **Define Content Logic**: Map targeted personas/segments to content objects, explicitly defining logic for authenticated vs. unauthenticated states.
6. **Apply Omnichannel Filtering**: Categorize content into Shared, Shared-but-edited, or Unique, and declare the Responsive vs. Adaptive approach.
7. **Define Taxonomy**: Output the hierarchical taxonomy structure, including synonym rings and inheritance rules.

@Examples (Do's and Don'ts)

**Principle: Page-Level Strategic Intent**
- [DO] Define intent before structure: 
  "**Page-Level Intent: Product Detail Page**
  *Intent:* Provide comprehensive product data to drive purchase.
  *Audience:* Unauthenticated prospective buyers.
  *Required Content:* High-res image carousel (Priority 1), Shared-but-edited product description (Priority 2), Cross-sell recommendation module (Priority 3).
  *Now generating React component structure based on priorities...*"
- [DON'T] Immediately generate UI components or wireframes filled with generic `Lorem Ipsum` without establishing what content actually belongs on the page and why.

**Principle: Content Matrix Definition**
- [DO] Structure a Matrix for copywriters:
  `| Sitemap ID | WF ID | Page Title | CMS Template | Level 1 Field | Level 2 Field | Copy/Label | Alt Text/Meta |`
  `| 3.1.0 | A | Summer Sale | Landing Page | Hero Space | H1 Title | "Save 20% Today" | N/A |`
- [DON'T] Mix system database logic into the copywriter's matrix (e.g., putting `Max Characters: 255` or `Database Source: CRM` in the matrix instead of the Content Model).

**Principle: Content Model Definition**
- [DO] Structure a Model for developers:
  `| ID# | CMS Template | Content Object | Persona Target | Authenticated | Format | Max Length | Source | Logic/Rules |`
  `| 001 | Product_View | Cross_Sell_Mod | Frequent_Shopper | Yes | JSON/Text | 150 chars | Rec_Engine | If User=VIP, show 10% discount text |`
- [DON'T] Use a Content Model to draft consumer-facing copy or paragraph text.

**Principle: Omnichannel Design**
- [DO] "This product description is 'Shared-but-edited'. We will use an Adaptive approach: the backend CMS will hold a 'Long_Desc' field for the desktop view, and a 'Short_Desc' field for the mobile app view."
- [DON'T] "We will use a Responsive design so the exact same 1,000-word product description scales down to fit on the user's smartphone screen."

**Principle: Content Logic & Personalization**
- [DO] Define logic based on state: "For Unauthenticated users, point-of-entry logic applies: if referring URL is a Facebook ad for shoes, populate the Hero module with the Shoe Campaign. For Authenticated users, use purchase history metadata to populate the Hero module."
- [DON'T] Assume personalization only applies to logged-in users, ignoring point-of-entry, clickstream, or device-based contextual metadata.