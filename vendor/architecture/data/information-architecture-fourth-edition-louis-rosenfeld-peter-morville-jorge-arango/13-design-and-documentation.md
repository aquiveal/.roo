# @Domain
These rules are activated when the AI is tasked with creating, reviewing, or structuring Information Architecture (IA) deliverables. Triggering requests include generating sitemaps, designing wireframes, conducting content mapping, building content inventories, formulating content models, establishing controlled vocabularies, or drafting Information Architecture style guides.

# @Vocabulary
- **Content Component (or Content Chunk):** The most finely grained portion of content that merits or requires individual architectural treatment, indexing, or repurposing.
- **Sitemap:** A visual or structural representation showing the relationships between information elements (pages, chunks), used to portray organization, navigation, and labeling systems.
- **High-Level Sitemap:** A top-down, bird's-eye view diagram omitting page-level details, used to explore primary organization schemes and approaches.
- **Detailed Sitemap:** A granular diagram utilizing a strict vocabulary and unique identification scheme to communicate specific organization, labeling, and navigation decisions to production teams.
- **Wireframe:** An architectural blueprint of an individual page or template demonstrating grouping, ordering, and priority of content components and connecting IA with interaction design.
- **Content Mapping:** The process of separating content from its container and mapping source content chunks to destination content chunks using unique identifiers.
- **Content Inventory:** A comprehensive spreadsheet or database cataloging available content, locations, IDs, and content gaps.
- **Content Model:** An IA framework made up of small chunks of interconnected content, utilizing metadata attributes to automatically generate contextual navigation (e.g., "See Also" links).
- **Metadata Matrix:** A table evaluating the value, description, and maintenance cost of various controlled vocabularies to prioritize their implementation.
- **IA Style Guide:** A governing document explaining the "Why" (rationale, audiences) and "How" (standards, guidelines, pattern libraries) of an information architecture to prevent architectural drift over time.
- **Pattern Library:** A documented collection of reusable UI/IA design patterns (e.g., navigation widgets) to ensure consistency and prevent redundant design work.

# @Objectives
- Translate abstract IA strategies into concrete, actionable deliverables (sitemaps, wireframes, content models).
- Facilitate interdisciplinary collaboration by generating artifacts tailored to specific audiences (stakeholders, designers, developers).
- Ensure scalability and modularity in IA documentation through strict hierarchical numbering, consistent metadata logic, and clear separation of content from presentation containers.
- Prevent architectural drift by formalizing design decisions, rules, and guidelines into comprehensive IA Style Guides.

# @Guidelines

## Diagramming and Visual Communication
- The AI MUST provide multiple "views" of an information architecture; it MUST NOT attempt to cram all IA dimensions into a single monolithic diagram.
- The AI MUST tailor the fidelity and complexity of IA diagrams to the specific audience (e.g., conceptual overviews for stakeholders; highly detailed, numbered schemas for developers).
- The AI MUST explicitly define content components (what constitutes a unit) and their connections (how they link) in any structural diagram.

## Sitemaps
- **High-Level Sitemaps:** When generating conceptual sitemaps, the AI MUST omit granular page-level details, focus on major content areas, and include a "Notes" section to verbally explain the architectural approach.
- **Detailed Sitemaps:** The AI MUST use a simplified, explicitly defined vocabulary (via a legend) for detailed sitemaps.
- **Modularization:** The AI MUST employ a unique ID numbering system (e.g., 1.0, 1.1, 1.1.1) to modularize large sitemaps, allowing subsidiary sections to be mapped independently while retaining their relational context.
- **Inheritance & Navigation:** The AI MUST clearly distinguish between "local" pages (which inherit global/local navigation and graphic identity from a parent) and "remote" pages (which belong to a different branch). It MUST use sidebars or annotations to define global and local navigation systems for specific areas.

## Wireframes
- **Scope limitation:** The AI MUST NOT generate wireframes for every page. It MUST restrict wireframes to the most important pages, major category interfaces, search interfaces, and reusable templates.
- **Disclaimers:** The AI MUST prominently include a disclaimer on all wireframes stating that the wireframe represents architectural layout and content priority, NOT final visual or interaction design.
- **Content Priority:** The AI MUST demonstrate the priority of content groupings through sizing, ordering, and placement (e.g., primary tasks above secondary helpers).
- **Responsive Context:** When applicable, the AI MUST indicate how page structure and navigation elements adapt or reflow across different screen sizes (desktop, tablet, mobile).
- **Annotations:** The AI MUST include callouts/annotations to detail the functionality of page elements, alongside project metadata (page numbers, titles, revision dates).

## Content Mapping and Modeling
- **Content Mapping:** The AI MUST assign unique IDs to every identified content chunk. The AI MUST map source content (e.g., `Source P36-1`) to destination architectural nodes (e.g., `Node 2.2.3`).
- **Content Inventory:** The AI MUST structure content inventories using tables/spreadsheets that track Title, Unique ID, URL/Location, Content Type, and missing gaps.
- **Content Modeling:** To support deep contextual navigation, the AI MUST define logical connection rules utilizing shared metadata attributes.
- **Metadata Logic:** The AI MUST express content model relationships using conditional logic (e.g., `IF ObjectA.Metadata1 = ObjectB.Metadata1 THEN LINK`).
- **Prioritization:** The AI MUST prioritize content models for content that is highly homogeneous, high volume, and high value.

## Controlled Vocabularies
- **Metadata Matrices:** The AI MUST generate a metadata matrix when planning vocabularies, evaluating each vocabulary by Name, Description, Examples, and Maintenance Difficulty to aid in prioritization.
- **Vocabulary Management:** The AI MUST output tabular schemas for tracking controlled vocabularies, strictly mapping `Unique ID`, `Accepted Term`, and `Variant Terms`.

## Information Architecture Style Guides
- **The "Why":** The AI MUST document the rationale behind architectural decisions, including mission, vision, audience definitions, and content policies, to fireproof the design against arbitrary future changes.
- **The "How":** The AI MUST specify strict *Standards* (mandatory rules for indexing/publishing) and *Guidelines* (best practices for layout/titling).
- **Maintenance:** The AI MUST outline specific maintenance procedures for updating the architecture (e.g., rules for adding new hierarchy levels or index terms).

# @Workflow
1. **View Assessment:** Determine the audience and required fidelity of the requested deliverable (conceptual vs. production-level).
2. **Structural Outlining (Sitemaps):** 
   - Define the unique ID taxonomy (1.0, 2.0). 
   - Draft the high-level map focusing on main categories.
   - Expand into detailed modular sitemaps separating content chunks from page containers.
3. **Layout Definition (Wireframing):** 
   - Select critical templates. 
   - Map content components into layout zones based on priority. 
   - Add interaction callouts, metadata, and visual design disclaimers.
4. **Content Analysis (Mapping & Modeling):** 
   - Generate a content inventory table. 
   - Assign unique IDs to content chunks. 
   - Define metadata linkage logic for automated contextual navigation.
5. **Vocabulary Definition:** Draft the metadata matrix to prioritize vocabularies, then generate accepted/variant term mappings.
6. **Governance Documentation (Style Guide):** Compile the "Why" (rationale) and "How" (standards, maintenance, pattern library) into a unified IA Style Guide.

# @Examples (Do's and Don'ts)

## Sitemaps and ID Numbering
**[DO]**
```text
Legend: 
[P] = Page container, [C] = Content Chunk, [L] = Local Navigation, [R] = Remote Link

1.0 [P] Global Home
    1.1 [P] Products Landing
        1.1.1 [C] Featured Product Carousel
        1.1.2 [P] Product Detail Template
            - Inherits: [L] Products Sidebar
    1.2 [P] Support Hub
        1.2.1 [C] Contact Us Form (Global Chunk ID: C-99)
        1.2.2 [R] Link to external ticketing system

Notes: Section 1.2 utilizes a unique local navigation system distinct from 1.1.
```

**[DON'T]**
```text
Home -> Products
Home -> Support -> Contact
(Incorrect: Lacks unique IDs, fails to separate pages from content chunks, and omits structural inheritance notes.)
```

## Wireframe Specifications
**[DO]**
```text
======================================================================
WIREFRAME: Product Detail Template (ID: WF-04) | Date: 2023-10-25
*DISCLAIMER: This document represents architectural layout and content 
priority only. It does not dictate final visual, typographic, or brand design.*
======================================================================

[Header Area] 
Global Navigation | [Search Box]

[Main Content Zone - Priority 1]
Product Title (H1)
Product Image Placeholder | Price & [Call to Action: ADD TO CART]

[Secondary Content Zone - Priority 2]
Product Specifications (Data Table)
Callout A: This table dynamically expands on tablet/desktop, collapses to accordion on mobile.

[Contextual Navigation Zone - Priority 3]
"Related Accessories" (Driven by Content Model logic)
======================================================================
```

**[DON'T]**
```text
Make the header blue with a 14pt Arial font. 
Put the product image on the left.
Put accessories at the bottom.
(Incorrect: Assumes visual design duties, lacks priority hierarchy, lacks disclaimer, omits responsive behavior annotations.)
```

## Content Modeling Logic
**[DO]**
```text
Content Model: Album Ecosystem

Target Objects: Album Detail Page, Artist Biography, Album Review
Required Metadata Attributes: Artist_Name, Album_Name, Release_Date

Linkage Logic:
1. IF Album_Detail.Artist_Name = Artist_Biography.Artist_Name 
   THEN GENERATE Two-Way Link ("View Artist Bio" / "View Albums by Artist")
   
2. IF Album_Review.Album_Name = Album_Detail.Album_Name 
   AND Album_Review.Artist_Name = Album_Detail.Artist_Name
   THEN GENERATE One-Way Link (Album_Detail -> Album_Review: "Read Review")
```

**[DON'T]**
```text
Link the album page to the review page and the artist page.
(Incorrect: Fails to define the specific metadata attributes and conditional logic required to automate the contextual navigation.)
```

## Controlled Vocabulary / Metadata Matrix
**[DO]**
```text
| Vocabulary | Description | Examples | Maintenance |
|---|---|---|---|
| Product Type | Categories of hardware sold | Router, Switch | Low |
| Audience | Target user profiles | Enterprise, Home | Low |

Vocabulary Table: Product Type
| Unique ID | Accepted Term | Variant Terms (Used For) |
|---|---|---|
| PT-01 | Router | Wi-Fi Router, Hub, Wireless Router |
```

**[DON'T]**
```text
Make sure we tag things with the right product type and audience so search works.
(Incorrect: Fails to provide a structured matrix evaluating maintenance cost and fails to distinguish between accepted and variant terms using unique IDs.)
```