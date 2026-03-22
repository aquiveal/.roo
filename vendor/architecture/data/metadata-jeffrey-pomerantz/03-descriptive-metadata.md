@Domain
These rules trigger when the AI is tasked with generating, structuring, analyzing, or embedding descriptive metadata for any resource (digital or physical), specifically when utilizing the Dublin Core metadata schema, constructing resource discovery access points, or writing HTML `<meta>` tags for web pages and search engine optimization.

@Vocabulary
- **Resource**: A potentially informative object (digital file, physical object, webpage) that is the subject of the description.
- **Dublin Core (DC)**: A "lowest common denominator" metadata schema comprising a core set of 15 elements designed to describe any networked or physical resource simply and universally.
- **Element**: A category of statement or predicate that names an attribute of a resource (e.g., Title, Creator, Date).
- **Value**: The specific data assigned to an element to complete the descriptive statement.
- **Access Point**: An element-value pair that provides a mechanism for a user or discovery tool to find a resource.
- **Qualifier**: An extension specific to an individual element that specifies a narrower interpretation or refinement of that element (e.g., `Date.Created`, `Date.Modified`).
- **Encoding Scheme**: A standardized set of rules for formatting a specific type of data value (e.g., ISO 8601 for dates, MIME types for formats).
- **Keyword Stuffing**: An unethical (black hat) Search Engine Optimization (SEO) anti-pattern involving the injection of excessive or irrelevant terms into HTML metadata.

@Objectives
- Generate metadata records that adhere to the principle of "lowest common denominator" simplicity, ensuring broad interoperability.
- Maximize resource discovery by creating robust access points that anticipate diverse user search strategies.
- Accurately apply the Dublin Core framework, strictly observing the rules of element repeatability, optionality, and semantic flattening.
- Embed structured descriptive metadata into web documents correctly while avoiding deprecated or penalized SEO practices.

@Guidelines
- **Core Element Restriction**: Default to utilizing the 15 core Dublin Core elements (Contributor, Coverage, Creator, Date, Description, Format, Identifier, Language, Publisher, Relation, Rights, Source, Subject, Title, Type).
- **Semantic Flattening**: Flatten specific, domain-nuanced creation roles into broad Dublin Core semantics. (e.g., A painter, an author, and a choreographer must all be categorized uniformly as `Creator`).
- **Element Repeatability**: The AI MUST repeat elements to capture multiple values rather than concatenating values. If a resource has multiple titles (e.g., in different languages) or multiple creators, generate a separate element-value pair for each.
- **Element Optionality**: The AI MUST omit any element that is irrelevant to the resource (e.g., omitting `Language` for a painting). NEVER use placeholder values like "N/A", "None", or "Unknown".
- **Refinement via Qualifiers**: When a core element is too broad to accurately describe a resource's lifecycle event, the AI MUST append a qualifier to the element (e.g., use `Date.Created`, `Date.Modified`, or `Date.Valid` instead of a generic `Date`).
- **Syntax Encoding Schemes**: The AI MUST format specific data types using established syntax encoding schemes. Use ISO 8601 for all dates. Use formal Internet MIME types for digital formats. Use formal unique identifier systems (like ISBN or URI) for Identifiers, Relations, and Sources.
- **HTML Embedding Requirements**: When embedding metadata into HTML, the AI MUST use the `<meta>` tag within the `<head>` element. Attributes must be mapped as `name="[schema].[element]"` and `content="[value]"`.
- **Search Engine Optimization constraints**: The AI MUST NOT generate `<meta name="keywords">` tags, as modern search engines ignore them due to historic keyword stuffing. The AI MUST generate a concise, accurate `<meta name="description">` tag, as search engines utilize this content for search result snippets.

@Workflow
1. **Analyze the Resource**: Identify the resource being described and define its core attributes (who made it, what is it called, when was it made, what is its format).
2. **Map to Core Elements**: Translate these attributes into the 15 Dublin Core elements, flattening nuanced roles into broad DC semantics.
3. **Handle Multiplicity**: For any attribute with more than one data point, duplicate the element to create a distinct, separate element-value pair for every data point.
4. **Prune Irrelevant Elements**: Discard any of the 15 core elements that do not logically apply to the resource.
5. **Apply Encoding & Qualification**: 
   - Format all date values into ISO 8601 (YYYY-MM-DD).
   - Format all file types into standard MIME types.
   - Attach qualifiers to elements if specificity is required (e.g., separating creation dates from modification dates).
6. **Format Output**:
   - If generating a raw record, output as a list of `Element: Value` pairs.
   - If embedding in a webpage, format as HTML `<meta>` tags, prefixing the `name` attribute with `dc.` or `dcterms.` (e.g., `dc.creator`). Ensure a standard HTML `description` meta tag is included and omit any `keywords` meta tags.

@Examples (Do's and Don'ts)

**Principle: Element Repeatability**
- [DO] 
  Title: Mona Lisa
  Title: La Gioconda
  Title: La Joconde
- [DON'T] 
  Title: Mona Lisa, La Gioconda, La Joconde

**Principle: Element Optionality**
- [DO] 
  Title: Leaf
  Date: 2014-10-12
- [DON'T] 
  Title: Leaf
  Language: N/A
  Creator: None

**Principle: Semantic Flattening**
- [DO] 
  Creator: Leonardo da Vinci
- [DON'T] 
  Painter: Leonardo da Vinci

**Principle: Qualified Elements and Encoding Schemes**
- [DO]
  Date.Created: 2014-12-01
  Date.Modified: 2014-12-05
  Format: text/html
- [DON'T]
  Date: December 1st 2014
  Date: Edited on Dec 5
  Format: Web page document

**Principle: HTML Embedding and SEO**
- [DO]
  <meta name="dc.creator" content="Jeffrey Pomerantz">
  <meta name="dc.identifier" content="978-0-262-52851-1" scheme="ISBN">
  <meta name="description" content="Chapter 3 of the book Metadata, published by MIT Press">
- [DON'T]
  <meta name="creator" content="Jeffrey Pomerantz">
  <meta name="ISBN" content="978-0-262-52851-1">
  <meta name="keywords" content="metadata, Dublin Core, schema, tags, SEO, search">