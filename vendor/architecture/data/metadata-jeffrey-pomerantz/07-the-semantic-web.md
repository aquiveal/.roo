@Domain
These rules MUST trigger when the AI is tasked with designing data models, creating web markup (HTML), implementing Search Engine Optimization (SEO) strategies, designing APIs that exchange structured data, or building systems intended for the Semantic Web, Linked Data, or metadata syndication.

@Vocabulary
- **Semantic Web**: A web of explicitly structured data capable of being processed by software applications/agents, not just consumed by human users.
- **Software Agent**: An application or algorithm that interacts with web services using structured metadata to automatically carry out sophisticated tasks on behalf of users.
- **Linked Data**: The application of World Wide Web architecture (HTTP, URIs) to share structured data on a global scale.
- **URI (Uniform Resource Identifier)**: A unique identifier formatted according to HTTP protocols, acting as an unambiguous reference/address for a resource.
- **Dereferenceable**: The property of a URI that, when queried by software, returns not only the resource itself but also metadata about the resource and links to other resources.
- **RDF (Resource Description Framework)**: A data model utilizing subject-predicate-object relationships (triples) to explicitly structure data.
- **Triple**: A subject-predicate-object statement where the subject and object are uniquely identified resources (URIs) and the predicate is the relationship linking them.
- **sameAs**: A specific metadata element used to explicitly declare that two different URIs refer to the exact same real-world entity, bridging isolated data networks.
- **Linked Open Data (LOD)**: Structured data published openly on the web using RDF triples and shared standards.
- **Schema.org**: A collaborative metadata standard (by Google, Microsoft, Yahoo) used to embed structured entity and property data directly into HTML.
- **Microdata**: An HTML specification used by Schema.org allowing metadata to be embedded anywhere in a webpage using specific attributes (`itemscope`, `itemtype`, `itemprop`).
- **Open Graph Protocol (OGP)**: A metadata schema used to transform a web resource into a rich object within a social graph.

@Objectives
- Transform implicit, natural-language web content into explicit, machine-readable structured data.
- Ensure all resources are uniquely identifiable, addressable, and interconnected via HTTP URIs.
- Maximize interoperability by strictly reusing existing, shared metadata standards rather than inventing proprietary schemas.
- Construct extensive webs of data by actively linking internal resources to external knowledge graphs (e.g., DBpedia, Wikidata, Getty Vocabularies).

@Guidelines

**1. Vocabulary and Standard Selection**
- The AI MUST NOT invent new metadata schemas or vocabularies if a suitable shared standard already exists. Reuse is strictly mandated.
- The AI MUST implement recognized vocabularies for specific domains (e.g., Schema.org for general web content, iCalendar/ISO 8601 for dates/events, Open Graph Protocol for social sharing, Exif for digital images).

**2. Linked Data Architecture (Tim Berners-Lee’s Rules)**
- The AI MUST assign HTTP URIs as the primary identifiers for all generated resources.
- The AI MUST ensure URIs are dereferenceable. When a software agent queries a URI, the system MUST return the resource alongside its structured metadata and links to related resources.
- The AI MUST structure relationships as RDF triples (Subject -> Predicate -> Object). Both the Subject and the Object MUST be URIs when referencing entities.
- The AI MUST allow a single resource to have multiple metadata records across different schemas (e.g., LOC vs. ULAN) if they serve different purposes, provided they link back to the core resource.

**3. HTML Embedding and Microdata (Schema.org)**
- The AI MUST embed structured data directly into the HTML payload using Microdata or equivalent semantic formats.
- The AI MUST use HTML `<div>` or `<span>` tags coupled with `itemscope` to declare an entity boundary.
- The AI MUST declare the entity type using the `itemtype` attribute, pointing to a valid Schema.org URL (e.g., `http://schema.org/Book`).
- The AI MUST assign specific properties to HTML children using the `itemprop` attribute.
- The AI MUST respect Schema.org inheritance hierarchies (e.g., a `PostalAddress` inherits from `ContactPoint`, which inherits from `StructuredValue`, down to `Thing`). Child entities MUST inherit and properly implement the properties of their parent entities.

**4. Entity Resolution and Network Bridging**
- The AI MUST utilize the `sameAs` element (or its semantic equivalent) whenever a local entity corresponds to a known entity in an external dataset (e.g., DBpedia, VIAF, Library of Congress, New York Times Linked Open Data).
- The AI MUST include an array or list of `sameAs` URIs to prevent the local dataset from becoming an isolated silo, extending the data to the "edge of human knowledge."

**5. Software Agent Interoperability (APIs)**
- When designing APIs, the AI MUST expose the structured metadata of resources, not just the raw resource payloads, to allow software agents to perform filtering and logic operations (e.g., scheduling based on unbooked ISO 8601 timestamps).

@Workflow
1. **Analyze Content & Domain**: Evaluate the unstructured content or data to determine the primary entities, properties, and relationships.
2. **Select Shared Vocabularies**: Identify the existing open standards required (e.g., Schema.org for web text, Open Graph Protocol for social metadata). Do not create custom fields unless absolutely no standard exists.
3. **Assign HTTP URIs**: Ensure every entity has a unique HTTP URI that can be dereferenced by software agents.
4. **Link to External Graphs (`sameAs`)**: Search external datasets (DBpedia, VIAF, Wikidata) for the entities. Compile matching URIs and apply the `sameAs` predicate to link the local entity to the global semantic web.
5. **Construct Triples**: Define the internal relationships between entities using subject-predicate-object logic.
6. **Embed Semantic Markup**: If generating web content, wrap the unstructured text in HTML Microdata tags (`itemscope`, `itemtype`, `itemprop`). Verify that nested entities respect the inheritance rules of the chosen schema.
7. **Verify API/Agent Readiness**: Ensure the output allows external software agents to effortlessly extract the metadata required to perform autonomous tasks.

@Examples (Do's and Don'ts)

**[DO] Embed explicitly structured Linked Data using Schema.org Microdata**
```html
<div itemscope itemtype="http://schema.org/Book">
  <img itemprop="image" src="metadata-bookcover.jpg">
  <h1 itemprop="name"><a href="http://mitpress.mit.edu/books/metadata">Metadata</a></h1>
  <span itemprop="author" itemscope itemtype="http://schema.org/Person">
    by <a itemprop="url" href="http://mitpress.mit.edu/authors/jeffrey-pomerantz"><span itemprop="name">Jeffrey Pomerantz</span></a>
    <link itemprop="sameAs" href="http://viaf.org/viaf/123456789">
  </span>
  <span itemprop="description">Everything we need to know about metadata, the usually invisible infrastructure for information with which we interact every day.</span>
</div>
```

**[DON'T] Rely on implicit structure and formatting without machine-readable semantic vocabularies**
```html
<div>
  <img src="metadata-bookcover.jpg">
  <h1><a href="http://mitpress.mit.edu/books/metadata">Metadata</a></h1>
  <span>by <a href="http://mitpress.mit.edu/authors/jeffrey-pomerantz"> Jeffrey Pomerantz</a></span>
  <span>Everything we need to know about metadata, the usually invisible infrastructure for information with which we interact every day.</span>
</div>
```
*(Explanation: The DON'T example relies purely on human-readable layout and untyped links. It fails Tim Berners-Lee's rules because a software agent cannot explicitly determine that this is a Book, who the Author is, or how it connects to the global knowledge graph).*