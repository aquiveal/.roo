# @Domain
Trigger these rules when the user requests the design, formatting, generation, or structural organization of a taxonomy display, thesaurus output report, search/browse user interface, or faceted navigation system. This applies to UI/UX design tasks for information retrieval, structuring taxonomy data for specific audiences (indexers vs. end-users), and formatting exported vocabulary lists.

# @Vocabulary
- **Alphabetical Simple List**: A display format where terms are listed alphabetically without any relationship details, used for quick browsing by users who know the target term.
- **Alphabetical Flat Format**: A display format listing each preferred term alphabetically, immediately followed by its direct relationships (UF, BT, NT, RT) and scope notes.
- **Full-Term Hierarchy**: A display showing a term alongside its multiple relationship levels (BT1, BT2, NT1, NT2). Subtypes include *multilevel* (using brackets/numbers) and *two-way hierarchy* (graphical representation using indents/periods).
- **Top Term Hierarchy**: An alphabetical list of only the broadest terms (top terms), each displaying its full hierarchy of narrower terms underneath.
- **Permuted / Rotated Index**: An alphabetical index of constituent words within terms. Variations include KWIC (Keyword In Context) and KWOC (Keyword Out of Context).
- **One Level per Page**: A web display format where each hierarchical level occupies a separate page, with terms hyperlinked to their immediate narrower terms.
- **Expandable Tree Hierarchy**: An interactive, graphical display allowing users to click a term or plus sign to reveal indented narrower terms beneath it without leaving the page.
- **Fly-Out Subcategory Lists**: A display where subcategories appear to the side or below (like submenus) when a top-level category is selected.
- **Breadcrumb Trail**: A navigation path display (e.g., Home > Category > Subcategory) showing the hierarchy of broader terms and allowing backwards navigation.
- **Node Labels / Facet Indicators**: Dummy terms used purely to organize and label a category of narrower terms. They are not linked to content/indexing and must be visually distinct.
- **Recursive (Rolled up) Retrieval**: A search behavior where selecting a broader term retrieves all content indexed to that term PLUS all content indexed to its narrower terms.
- **Faceted Search / Navigation**: A fielded display allowing users to select terms from multiple distinct facets (dimensions/attributes) to combine in a postcoordinated query.
- **Fielded / Advanced Search**: A display providing separate search boxes or dropdowns for distinct vocabulary files or metadata types, not strictly limited to facets.

# @Objectives
- The AI MUST tailor the taxonomy output and display format strictly to the intended audience (e.g., detailed relationship abbreviations for indexers/taxonomists; simplified, interactive graphical trees or fly-outs for end-users).
- The AI MUST select the optimal hierarchical web display format based on the taxonomy's size, depth, breadth, and polyhierarchical complexity.
- The AI MUST enforce strict sorting logic, prioritizing chronological or logical sequencing over alphabetical sorting when lists are short, and handling "General" and "Other" categories with rigid placement rules.
- The AI MUST design faceted search interfaces to support progressive, step-by-step refinement and clearly indicate zero-result paths.

# @Guidelines

## Audience-Specific Formatting
- When generating displays for **Taxonomists, Indexers, or Subject Area Researchers**:
  - The AI MUST utilize formats such as Alphabetical Flat Format, Full-Term Hierarchy, or Top Term Hierarchy.
  - The AI MUST explicitly display relationship abbreviations (USE, UF, BT, NT, RT, TT) and Scope Notes (SN).
  - The AI MUST include phrase inversions (e.g., "libraries, public") as nonpreferred terms to aid alphabetical lookup.
- When generating displays for **End-User Searchers**:
  - The AI MUST hide complex relationship abbreviations (BT, NT, RT).
  - The AI MUST NOT use Alphabetical Flat Formats or Permuted Indexes.
  - The AI MUST use interactive visual formats (Expandable Trees, Fly-Out Lists, or Faceted Navigation).
  - The AI MUST provide a search box that supports both "begins with" and "contains" matching alongside any browsable tree.

## Hierarchical Web Display Selection
- The AI MUST use **One Level per Page** when:
  - The taxonomy is extremely broad (many terms per level).
  - Polyhierarchies are present (preventing the UI confusion of repeating branches on a single screen).
  - The depth exceeds 4 levels.
- The AI MUST use an **Expandable Tree Hierarchy** when:
  - The taxonomy is relatively small or has deep but narrow branches.
  - The UI requires displaying search results simultaneously on the same screen (e.g., tree on the left, results on the right).
  - Polyhierarchies are minimal or absent.
  - The taxonomy is limited to approximately 4 levels (to prevent excessive scrolling).
- The AI MUST use **Fly-Out Subcategory Lists** for retail/e-commerce or public website navigation where rapid visual scanning of subcategories is required without page loads.

## Sorting and Ordering Rules
- **Default Order**: The AI MUST default to alphabetical sorting for lists of 10 or more terms.
- **Logical Order**: For shorter lists (<10 terms), the AI MUST evaluate if a chronological, sequential, or logical order (e.g., by popularity or standard industry codes) is more appropriate than alphabetical. If a logical order is chosen, it MUST be applied consistently throughout that specific hierarchical level.
- **General and Other Categories**: 
  - The AI MUST place any "General" (or "All") term at the absolute TOP of the list. It MUST NOT be sorted alphabetically under 'G'.
  - The AI MUST place any "Other" or "Miscellaneous" term at the absolute BOTTOM of the list. It MUST NOT be sorted alphabetically under 'O' or 'M'.

## Contextual Display Names
- When terms are displayed within a strict hierarchical visual context, the AI MUST shorten the term names to remove redundant broader concepts (e.g., "Recruiting" instead of "Recruiting employees" when under the parent "Human resource management"). Note: The underlying administrative term ID and full name must remain intact for indexing purposes.

## Node Labels
- When a term is a Node Label (a category header not used for indexing), the AI MUST visually distinguish it from selectable terms using brackets (e.g., `[Politics & Government]`), italics, or a distinct font style. 
- The AI MUST ensure Node Labels do not generate recursive retrieval search queries.

## Faceted and Fielded Search Interfaces
- When designing faceted navigation, the AI MUST allow users to select terms from facets in any order (step-by-step refinement).
- The AI MUST provide checkboxes next to terms within a facet if the UI supports multiple selections within the same facet (an OR combination within an AND query).
- The AI MUST order quantitative facets (e.g., date, price, size) numerically from lowest to highest.
- For Fielded/Advanced Search without strictly defined facets, the AI MUST provide distinct search boxes or dropdowns mapped to separate vocabulary files (e.g., "Personal Names", "Company Names", "Topics") to prevent term ambiguity.

# @Workflow
1. **Analyze Request Context**: Determine the target audience (indexer vs. end-user) and the primary taxonomy structure (thesaurus, hierarchy, or facets).
2. **Select Display Architecture**: 
   - For end-users, choose between One Level per Page, Expandable Tree, Fly-Out, or Faceted Search based on taxonomy breadth, depth, and content uniformity.
   - For internal/admin output, choose between Flat Format, Top Term, or Full-Term Hierarchy.
3. **Format Term Hierarchy**: Organize the terms applying the required indentation, bracketing for Node Labels, and contextual name shortening.
4. **Apply Sorting Rules**: Sort the sibling terms at each level. Apply alphabetical sorting for long lists; apply logical sorting for short lists. Force "General" to the top and "Other" to the bottom.
5. **Integrate Search Modalities**: Ensure the design includes text search inputs capable of "begins with" and "contains" queries to supplement the browsable structure.
6. **Refine Facets (If Applicable)**: Group attribute-based terms into facets, order them logically, and implement multi-select UI elements (checkboxes) and breadcrumb trails.

# @Examples (Do's and Don'ts)

**Audience-Specific Formatting (Indexers vs. End-Users)**
- [DO] For indexers: Display `Water supply \n UF Water utilities \n BT Utilities \n NT Reservoirs`
- [DON'T] For end-users: Display `Water supply \n UF Water utilities \n BT Utilities`. (Instead, show an interactive tree: `[-] Utilities \n    Water supply`).

**Sorting "General" and "Other"**
- [DO] Sort as:
  `Crafts in general`
  `Beadwork`
  `Embroidery`
  `Other crafts`
- [DON'T] Sort strictly alphabetically as:
  `Beadwork`
  `Crafts in general`
  `Embroidery`
  `Other crafts`

**Contextual Display Names**
- [DO] Display in UI:
  `Human resource management`
  `-- Recruiting`
  `-- Training`
- [DON'T] Display redundant text when the context is clear:
  `Human resource management`
  `-- Recruiting employees`
  `-- Training employees`

**Node Labels**
- [DO] Format a non-indexable category header as: `[Clothing, Shoes & Jewelry]` or `*Clothing, Shoes & Jewelry*`.
- [DON'T] Format a non-indexable header identically to an indexable term, misleading the user into clicking it to retrieve specific content.

**Full-Term Hierarchy Display (Multilevel)**
- [DO] Output thesaurus reports using standardized hierarchy indicators:
  `<< Facilities & infrastructure`
  `< Public buildings & facilities`
  `Recreation facilities`
  `> Amusement parks`
  `>> Athletic facilities`
- [DON'T] Output a full-term hierarchy as a flat list without directional hierarchy markers (`<`, `>`) or level numbers (`BT1`, `NT2`).