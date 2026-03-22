@Domain
Trigger these rules when tasked with designing, analyzing, refactoring, or evaluating taxonomy structures, hierarchical classifications, metadata schemas, faceted search configurations, or database architectures intended for knowledge organization, information retrieval, or site navigation.

@Vocabulary
- **Hierarchy / Tree Structure**: An extension of broader term/narrower term relationships including every term within a controlled vocabulary, designed top-down for categorization.
- **Polyhierarchy**: A structure where a single term has more than one broader term (parent) in different hierarchical branches.
- **Recursive Retrieval (Rolled-up Retrieval)**: A search behavior where selecting a broader term automatically retrieves all content indexed to that term AND all content indexed to every narrower term beneath it.
- **Node Label**: A dummy term or heading used strictly to organize the hierarchy. It is displayed to the user but cannot be used to index or link to actual content.
- **Facet Indicator**: A specific type of node label used to subcategorize a large number of narrower sibling terms by their type or facet (e.g., *[by body style]*).
- **Facet**: A categorical, mutually exclusive grouping of terms representing a single dimension or attribute of a query (e.g., Topic, Product, Audience, Geography), used for postcoordinated search.
- **Precoordination**: Combining concepts before indexing (e.g., creating a highly specific hierarchical term). 
- **Postcoordination**: Combining concepts at the time of the search (e.g., selecting one value from multiple different facets).
- **Categories / Classes**: Metadata applied to taxonomy terms themselves (spanning across hierarchies/facets) to designate intended end-use, department routing, or allowable semantic relationships in an ontology.

@Objectives
- Structure knowledge organization systems that strictly align with the target end-users' mental models and expertise levels.
- Balance hierarchical depth and breadth based on the display medium and audience type (public web vs. expert research).
- Prevent indexing ambiguity in recursive retrieval environments by properly implementing "General" and "Other" nodes.
- Architect clean faceted classification systems where dimensions are mutually exclusive and structurally sound.
- Establish robust administrative boundaries by logically separating distinct vocabularies (e.g., named entities vs. topical terms).

@Guidelines

# 1. Structural Arrangement and User Alignment
- The AI MUST determine the arrangement of the hierarchy based on the end-user's perspective, NOT solely on objective reality.
- When designing for laypeople/consumers, the AI MUST group terms by end-use or common association (e.g., organizing products by use rather than manufacturing material; organizing languages by geographic region rather than linguistic family).
- When designing for domain experts, the AI MUST use standard, scientific, or industry-accepted classification structures (e.g., NAICS codes, Linnaean taxonomy).

# 2. Named Entities in Hierarchies
- The AI MUST attach Named Entities (proper nouns/instances) to the generic level most likely to be searched by the user. Do not arbitrarily force entities to the deepest possible leaf if users lack the granular knowledge to find them there (e.g., relate individuals to "heads of state" rather than forcing users to guess between "presidents" and "prime ministers").

# 3. Depth and Breadth Constraints
- For public web or consumer navigation taxonomies, the AI MUST aim for broad hierarchies with a maximum depth of 3 levels, and optimally 6-8 concepts per level to prevent click-fatigue.
- For scholarly, scientific, or internal expert systems, the AI MUST prioritize precise depth over breadth, ignoring the 3-level rule to accurately represent the domain.
- The AI MUST sacrifice structural symmetry (having the exact same number of levels across all branches) in favor of term accuracy and logical organization.

# 4. Managing Recursive Retrieval ("All", "General", "Other")
- If the target system defaults to Recursive Retrieval (selecting a parent selects all children), the AI MUST NOT use the parent term to index general content about that topic.
- To handle broad content in a recursive system, the AI MUST create a specific narrower term containing the word "General" (e.g., "General crafts" or "Crafts in general").
- To handle highly specific content that lacks its own term in a recursive system, the AI MUST create a narrower term labeled "Other [Topic]" (e.g., "Other crafts").
- The AI MUST explicitly configure the sort order for these utility nodes: "General" MUST always be sorted first at the top of the sibling list; "Other" or "Miscellaneous" MUST always be sorted last at the bottom. They MUST NEVER be sorted alphabetically.

# 5. Node Labels and Facet Indicators
- When a term is created purely for structural organization and should not be used for tagging content, the AI MUST designate it as a Node Label.
- The AI MUST visually distinguish Node Labels and Facet Indicators in the structural design (e.g., enclosing them in brackets `[ ]`, angle brackets `< >`, or marking them as italicized/unselectable in the schema).

# 6. Facet Design and Implementation
- The AI MUST use faceted structures for highly uniform content records (e.g., product catalogs, job postings, recipe databases).
- The AI MUST ensure facets are mutually exclusive dimensions (e.g., Personality, Matter, Energy, Space, Time, Topic, Geography, Price).
- To validate a facet, the AI MUST apply the "By" test: Prefix the facet name with "By" (e.g., "By Location", "By Price"). If it does not make logical sense as a search refinement, it is not a valid facet.
- The AI MUST NOT treat hierarchical subjects as facets. Hierarchies define what a thing *is*; facets define the *attributes* or *perspectives* of a thing.

# 7. Separating Vocabularies
- The AI MUST partition large vocabularies into separate administrative files or database tables based on term behavior and editorial rules.
- Specifically, the AI MUST separate Named Entities (proper nouns like people, places, organizations) from Topical Subjects.
- When generating schemas, the AI MUST apply different formatting rules to these separate files (e.g., title capitalization for Named Entities, lowercase for Topical Subjects).

# 8. Assigning Categories
- The AI MUST use Categories to tag the taxonomy terms themselves when routing terms to different departments, UIs, or to govern allowable semantic relationships (e.g., tagging terms as "HR", "External", "Class: Person").

@Workflow
1. **Analyze Constraints**: Determine the target audience (public vs. expert) and the content uniformity (uniform = faceted; disparate = hierarchical).
2. **Determine Retrieval Logic**: Check if the host software uses Recursive Retrieval. If yes, automatically generate "General [Topic]" and "Other [Topic]" terms for broad categories.
3. **Partition Vocabularies**: Identify all proper nouns in the data set and isolate them into a separate Named Entity authority file with distinct casing rules.
4. **Establish Top-Level Structure**: 
   - For Hierarchies: Define top terms based on user mental models.
   - For Facets: Define dimensions using the "By [Dimension]" validation test.
5. **Apply Node Labels**: Identify terms that exist only to group other terms. Mark them with `[ ]` brackets so indexers know they are un-postable.
6. **Apply Sort Rules**: Override alphabetical sorting for logical sequences (chronological, sequential, NAICS standard) and lock "General" to the top and "Other" to the bottom of sibling lists.

@Examples (Do's and Don'ts)

# Handling Recursive Retrieval
[DO]
```text
Crafts
  > General crafts (Sort Order: 1)
  > Beadwork (Sort Order: 2)
  > Embroidery (Sort Order: 3)
  > Other crafts (Sort Order: 4)
```
[DON'T]
```text
Crafts (Used for both recursive ALL searches and specific general documents)
  > Beadwork
  > Embroidery
  > General crafts (Sorted alphabetically under G)
  > Other crafts (Sorted alphabetically under O)
```

# Using Node Labels and Facet Indicators
[DO]
```text
Automobiles
  [By body style]
    Coupes
    Sedans
    Station wagons
```
[DON'T]
```text
Automobiles
  By body style (Available as a selectable tag for content)
    Coupes
    Sedans
    Station wagons
```

# Named Entity Hierarchical Placement (For General Audiences)
[DO]
```text
Heads of state & government
  > Barack Obama
  > David Cameron
  > Vladimir Putin
```
[DON'T]
```text
Heads of state & government
  > Presidents
    > Barack Obama
    > Vladimir Putin (Moved from PM to President causing administrative tracking errors)
  > Prime ministers
    > David Cameron
```

# Facet Validation
[DO] Create facets based on orthogonal dimensions.
```text
Facet 1: [By Location] (North America, Europe, Asia)
Facet 2: [By Document Type] (Report, Manual, Policy)
Facet 3: [By Audience] (Public, Internal, Partners)
```
[DON'T] Mix broad subject hierarchies and attributes in the same facet structure.
```text
Facet 1: Geography
Facet 2: Human Resources (This is a topic hierarchy, not an orthogonal facet)
Facet 3: PDF Files (This is a specific value, the facet should be 'Document Type')
```