# @Domain
These rules MUST activate when the AI is performing tasks related to structuring content, designing Content Management System (CMS) schemas, writing HTML, formatting data payloads (JSON/XML), building APIs for content delivery, creating text-authoring environments, or migrating content from legacy systems.

# @Vocabulary
- **Markup**: Code that wraps around content chunks to give them machine-readable meaning, allowing automated decisions about display and usage across systems.
- **Presentational Markup**: Anti-pattern. Code that dictates exclusively how content should *look* (e.g., inline font colors, explicit sizing) rather than what it *is*.
- **Semantic Markup**: Code that reveals the intrinsic meaning and structure of the content (e.g., "this is a headline" rather than "this is large text"), leaving visual presentation to external style sheets.
- **WYSIWYG Anti-pattern**: "What You See Is What You Get" editors that inject fixed presentational markup permanently into databases, creating "blobs" of un-reusable content.
- **Microformats**: Open data standard using specific HTML classes to add metadata to content snippets, identifying them as distinct entities (e.g., a "person" or "location").
- **HTML5 Microdata**: Native HTML5 extensions used to mark up content with standards-compliant, semantically rich data.
- **Schema.org**: An HTML5 microdata vocabulary/taxonomy created by search engines to standardize the description of common entities.
- **Structural Markup**: Enterprise-level markup used for data storage and transport, describing entities and relationships independently of presentation (e.g., XML, JSON, DITA).
- **XML (Extensible Markup Language)**: Structural markup that allows the definition of custom tags for modular content.
- **RDF (Resource Description Framework)**: A structural method used to describe things and relationships via subject-predicate-object statements.
- **OWL (Web Ontology Language)**: Built on RDF to express complex, rich relationships between content entities (e.g., symmetrical relationships).
- **DITA (Darwin Information Type Architecture)**: XML-based data model used primarily for organizing technical documentation into topic-based modules.
- **JSON (JavaScript Object Notation)**: A lightweight data interchange format favored in APIs for its ease of reading, writing, and machine-parsing.
- **Linked Data**: Data connected to other equivalent sets of data in the cloud based on shared attributes, allowing content enrichment across different sources.
- **Markdown**: A lightweight, human-readable authoring syntax that strips away HTML crutches, forcing semantic text structure without presentation hacks.

# @Objectives
- The AI MUST give content a "voice" by wrapping all text in machine-readable, semantic code.
- The AI MUST strictly separate content structure and meaning from visual presentation and styling.
- The AI MUST prevent content from being locked into a single display format or device.
- The AI MUST structure data so it can be seamlessly translated between different markup languages and APIs.

# @Guidelines

- **Eliminate Presentational Tags:** When generating or refactoring HTML, the AI MUST NOT use presentational tags (e.g., `<b>`, `<i>`, `<font>`) or inline CSS styles (`style="color: purple; font-size: 18pt"`).
- **Enforce Semantic HTML:** The AI MUST use semantic HTML tags (`<h1>` to `<h6>`, `<strong>`, `<em>`, `<aside>`, `<article>`) to define what the content *is*, not how it *looks*.
- **Prevent WYSIWYG Blobs:** When designing databases or CMS architectures, the AI MUST NOT create single, wide-open text fields intended for mixed HTML. The AI MUST create discrete, structured fields (e.g., `title`, `copy_deck`, `author_byline`) that match the content model.
- **Implement Microdata/Schema.org:** When writing HTML for identifiable entities (people, places, events, recipes), the AI MUST enrich the HTML with Schema.org microdata or microformats to provide deep machine-readable context.
- **Utilize Structural Markup for Transport:** When designing APIs or data exchange layers, the AI MUST serialize content chunks into JSON or XML to preserve structural integrity during transport.
- **Model Relationships (RDF/OWL logic):** When structuring databases, the AI MUST preserve relationships between content entities (e.g., linking a "copy deck" to its "parent article") to support Linked Data principles.
- **Advocate Markdown for Authoring:** When generating text-authoring workflows or documentation, the AI MUST use or recommend Markdown. The AI MUST NOT use `<div>` soup or non-semantic HTML hacks just to achieve a temporary visual layout in text documents.
- **Content Translatability:** The AI MUST structure data agnostically, ensuring the core content model is clean enough to be converted from Markdown to JSON, JSON to XML, or XML to HTML without losing its intrinsic meaning.

# @Workflow
When tasked with creating, migrating, or structuring content, the AI MUST follow this exact sequence:

1. **Deconstruct the Content:** Analyze the provided text and identify distinct, meaningful chunks (e.g., headline, summary, body, date, author).
2. **Define the Structural Storage:** Map these chunks into a structured data format (JSON or XML) where each chunk has its own key/tag. Strip away all visual formatting.
3. **Select Semantic Tags:** If generating a presentation layer (HTML), wrap each chunk in the most accurate semantic tag available (`<header>`, `<time>`, `<p>`, `<cite>`).
4. **Apply Microdata:** Evaluate the content type. If it matches a known entity (e.g., Event, Product, Person), inject Schema.org microdata attributes (`itemscope`, `itemtype`, `itemprop`) into the semantic HTML.
5. **Delegate Styling:** Ensure absolutely no layout or aesthetic data is present in the markup. Defer all visual instructions to external stylesheets or downstream platform renderers.

# @Examples (Do's and Don'ts)

## Example 1: Basic Text Formatting
- **[DON'T]** Use presentational markup or inline styles to emphasize text.
  `<span style="font-size: 24px; font-weight: bold; color: purple;">Important Announcement</span>`
- **[DO]** Use semantic markup to denote the text's role, leaving styling to external CSS.
  `<h1>Important Announcement</h1>`

## Example 2: CMS Architecture & Data Storage
- **[DON'T]** Store an entire article as a single HTML blob from a WYSIWYG editor.
  ```json
  {
    "id": "101",
    "page_content": "<h2>My Trip</h2><p><i>By Jane Doe</i></p><p>Here is the story...</p>"
  }
  ```
- **[DO]** Use structural markup (JSON/XML) to separate the content into machine-readable elements.
  ```json
  {
    "id": "101",
    "headline": "My Trip",
    "author": "Jane Doe",
    "body": "Here is the story..."
  }
  ```

## Example 3: Enhancing HTML with Microdata
- **[DON'T]** Output bare HTML for specific entities without providing machine context.
  ```html
  <div>
    <h2>Steve Jobs</h2>
    <p>Co-founder of Apple Inc.</p>
  </div>
  ```
- **[DO]** Apply Schema.org microdata to turn the HTML into deeply semantic, linked-data-ready markup.
  ```html
  <div itemscope itemtype="http://schema.org/Person">
    <h2 itemprop="name">Steve Jobs</h2>
    <p itemprop="jobTitle">Co-founder of <span itemprop="worksFor">Apple Inc.</span></p>
  </div>
  ```

## Example 4: Authoring Content
- **[DON'T]** Use HTML crutches (`<div>` soup) just to force line breaks or visual structure in raw text.
  `<div><br><br>Chapter 1<br></div><div>The beginning</div>`
- **[DO]** Use Markdown to force purely semantic authoring.
  `# Chapter 1`
  `The beginning`