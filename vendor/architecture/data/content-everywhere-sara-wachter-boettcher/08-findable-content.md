# @Domain
These rules are triggered when the AI is tasked with designing content architecture, configuring search engine optimization (SEO) strategies, designing or tuning internal site search algorithms, building faceted search interfaces, aggregating contextual/related content, or defining domain-driven content models.

# @Vocabulary
- **Findability:** The degree to which users can easily discover content on or off a website via external search engines, internal site search, faceted filtering, or contextual links.
- **Unstructured Content:** Information formats (like blobs of text) that rely solely on inline keywords, free-form tags, and hierarchical navigation, heavily limiting findability.
- **Structured Content:** Content broken into meaningful, distinct chunks equipped with semantic markup, metadata, and shared attributes that machines and search engines can parse.
- **Content Hub (Canonical Presence):** A centralized, aggregated page acting as the definitive source for a specific domain entity (e.g., a specific "dish" or "city"), pulling together all related content via shared attributes.
- **Domain-Driven Design (Content):** Defining the entities within a subject domain and their relationships (a graph structure) to drive architecture, rather than relying on taxonomic library science or strict hierarchical sitemaps.
- **Ontological Relationship:** A deep, structural relationship rooted in the core concept or "thingness" of the content (e.g., animal classification taxonomy), as opposed to weak, free-form keyword associations.
- **Site Search Tuning:** The systemic adjustment of internal search algorithms by assigning weights to specific structured content fields or types, rather than applying manual, one-off overrides.
- **Faceted Search:** A search interface that allows users to explore large content inventories by sorting and filtering data using multiple, discrete structural criteria (facets).
- **Linked Data:** Standardized methods of sharing data (e.g., dbPedia) that connect structural content across the web, allowing automated enrichment of content hubs without manual authoring.
- **Curation:** The human act of selecting, arranging, and applying editorial storytelling to create new meaning from content. Distinct from automated algorithmic aggregation.
- **Human-Influenced Robotic Editing:** Designing automated content rules that strictly mirror users' mental models, resulting in aggregated content that feels thematic, useful, and meticulously organized.

# @Objectives
- Move findability strategies away from SEO "hacks" and manual link management towards structural integrity and semantic markup.
- Replace scattered, isolated content pages with canonical, domain-driven Content Hubs.
- Systematically tune internal site search by applying rules to structured content elements (e.g., prioritizing abstracts, demoting outdated content types).
- Build deep, ontological relationships between content types to generate highly relevant, contextual sidebars and related-item lists.
- Differentiate between true human curation and automated aggregation in system labeling and interface design.

# @Guidelines
- **Search Engine Findability:** The AI MUST rely on semantic markup and structured content chunks to communicate relevance to search engines. The AI MUST NOT recommend or implement keyword-stuffing, link schemes, or arbitrary free-form tags.
- **Keyword Integration:** The AI MUST treat keywords simply as natural user language. When optimizing for user queries, the AI MUST map these natural terms to structured attributes (e.g., creating a rule that automatically relates all "things to do" to a "city" attribute) rather than forcing keywords into unstructured body copy.
- **Domain-Driven Content Hubs:** The AI MUST aggregate related content into a single Canonical Presence (Content Hub) based on shared domain entities (e.g., exposing a single URL for "Spaghetti Bolognese" that pulls in recipes, chefs, and techniques). The AI MUST NOT rely purely on top-down hierarchical sitemaps.
- **Site Search Configuration:** The AI MUST tune site search by assigning algorithmic weight to discrete structural elements. For example, the AI MUST assign higher weight to matches found in a "Summary" or "Abstract" chunk, and lower weight to historically irrelevant content types (e.g., "Press Releases" for general queries). The AI MUST NOT use manual hacks or hardcoded overrides to fix systemic search failures.
- **Faceted Search Implementation:** When organizing exploratory content (products, recipes, help articles), the AI MUST ensure each filterable criterion exists as a discrete, independent field in the database. 
- **Contextual and Related Content:** The AI MUST establish Ontological Relationships for related content modules. Content MUST be connected by structural taxonomies (e.g., shared habitats, geographic radii, or Linnaean classification) rather than sales-driven assumptions or generic free-form tags.
- **Linked Data Enrichment:** The AI MUST evaluate opportunities to use Linked Data to automatically pull contextual information from external structured sources to enrich Content Hubs.
- **Curation vs. Aggregation Labeling:** The AI MUST NOT label automated, rule-based lists of links as "Curation" or "Curated Content". The AI MUST reserve "Curation" for human-driven editorial storytelling, and use terms like "Aggregated", "Related", or "Contextual" for automated outputs.
- **Mental Model Alignment:** The AI MUST structure automated content aggregation rules to match the user's mental model, ensuring that automated outputs achieve "Human-Influenced Robotic Editing."

# @Workflow
1. **Domain Entity Identification:** Analyze the content to identify the core domain entities (the "things" the content talks about, like a City, a Dish, or an Animal) and the natural language terms users apply to them.
2. **Graph Structure Mapping:** Map the entities into a Domain-Driven Design graph. Define the shared attributes that will interconnect discrete content types (e.g., connecting a "Recipe" entity to a "Dish" entity).
3. **Content Hub Creation:** Design the architecture for Canonical Content Hubs. Configure rules so that all related content types automatically aggregate onto the single canonical URL for that domain entity.
4. **Site Search Tuning:** Establish internal search logic by writing weighting rules based on the content model. Increase weight for high-value chunks (e.g., Title, Abstract) and decrease weight for low-value or temporal content types (e.g., old Press Releases).
5. **Facet Isolation:** Identify all exploratory criteria users require (size, color, brand, dietary restriction) and isolate them as distinct metadata fields to power Faceted Search.
6. **Ontological Rule Generation:** Write logical conditions for contextually discoverable content. Base rules on deep taxonomy (e.g., "If User is viewing Panda, display other animals in Broadleaf Forest habitat") instead of keyword matching.
7. **Linked Data Integration:** Assess the domain graph to identify gaps in content that can be automatically populated using external Linked Data sources, stitching the hub into the broader Semantic Web.

# @Examples (Do's and Don'ts)

- **Search Engine Optimization**
  - [DO]: Implement a structured rule that automatically ties local business entities and park entities to a shared "City" attribute, generating a rich, keyword-relevant "Things to do in [City]" hub page.
  - [DON'T]: Write a single unstructured page about a city and stuff the body copy with variations of "things to do in [City]".

- **Content Organization**
  - [DO]: Use Domain-Driven Design to create a single canonical resource page for a concept (e.g., "Cheetah") that aggregates videos, news, and habitats via relationship arrows.
  - [DON'T]: Build isolated, hierarchical silos where users must visit separate branches of a sitemap to find videos of cheetahs and articles about cheetahs.

- **Site Search Tuning**
  - [DO]: Write a search algorithm rule: `if query matches chunk [Abstract], multiply relevance score by 1.5. If content_type == "Press Release", reduce relevance score by 0.5.`
  - [DON'T]: Write a manual override: `if query == "dorm costs", force display page ID 452 at position 1.`

- **Contextual Sidebars**
  - [DO]: Populate a related items sidebar using ontological logic: "Display top-rated recipes that share the [Dish] entity attribute of Spaghetti Bolognese."
  - [DON'T]: Populate a sidebar using free-form tags, resulting in a random display of any content an author arbitrarily tagged with the word "pasta".

- **System Labeling**
  - [DO]: Label a dynamically generated list of articles sharing a taxonomic attribute as "Related Content".
  - [DON'T]: Label a dynamically generated list of articles as "Curated for You".