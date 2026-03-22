# @Domain

These rules MUST be activated when the AI is tasked with designing content models, authoring structured content, developing markup languages, implementing automated publishing pipelines, defining content schemas (DTDs/XML Schemas), writing transformation scripts (XSLT/XPath), or advising on content architecture frameworks (such as DITA, DocBook, NLM, or TEI) within an enterprise content management or unified content strategy context.

# @Vocabulary

To ensure alignment with the specified architectural mental model, the AI MUST adopt and strictly adhere to the following definitions:

*   **XML (Extensible Markup Language):** A streamlined subset of SGML designed for web delivery that focuses purely on describing what data is and its structure, completely devoid of formatting characteristics.
*   **SGML (Standard Generalized Markup Language):** The parent language of XML, based on principles of common file formats, extensible markup, and consistent document structure identification.
*   **WYSIWYG XML Editors:** Authoring tools that hide the underlying XML tags ("codes on" mode) under a user-friendly interface, allowing authors to focus on content without managing raw code.
*   **Element:** The fundamental building block of XML, consisting of a start tag (e.g., `<Title>`), an end tag (e.g., `</Title>`), and the content in between.
*   **Attribute:** Additional descriptive information nested within a start tag, consisting of a name and a value (e.g., `Audience="All"`).
*   **Node Tree (Document Tree):** The structural hierarchy of an XML document indicated by embedded (nested) elements.
*   **DTD (Document Type Definition):** A formal document written in a non-XML syntax that describes allowable elements, attributes, child elements, sequences, and content models.
*   **XML Schema:** An updated, more capable alternative to DTDs, written in well-formed XML, that provides rich data typing capabilities and supports local/global variables.
*   **Parser:** A specialized tool that reads an XML schema or DTD and enforces structural rules, reporting errors when content does not match the model.
*   **XSL (eXtensible Stylesheet Language):** An XML-based vocabulary used for formatting and transforming XML documents.
*   **XSLT (XSL Transformations):** A language for transforming XML documents into other markup languages (e.g., HTML, mobile markup).
*   **XSL-FO (XSL Formatting Objects):** A language used to format XML for paper-based delivery (e.g., PDF), managing page layouts, headers, and recto/verso pages.
*   **XPath:** A language used within XSL to navigate through elements and attributes in an XML document.
*   **DITA (Darwin Information Typing Architecture):** An open, output-independent standard developed by IBM and managed by OASIS, defining a common structure for creating, sharing, and reusing topic-based content.
*   **Topic:** The basic building block of DITA content.
*   **Generic Topic:** The base DITA structure containing a title, short description, prolog (metadata), topic body, and related links.
*   **Concept Topic:** A specialized DITA topic used to explain background information or "what is" data.
*   **Task Topic:** A specialized DITA topic providing procedural instructions, structured with steps, actions, and results.
*   **Reference Topic:** A specialized DITA topic used for factual, quick-reference data, such as interface documentation.
*   **DITA Map:** An index or virtual table of contents that aggregates DITA topics by pointing to them (via topic references) without containing the content itself.
*   **DocBook:** A mature, robust, but complex industry-standard DTD originally for UNIX manuals, typically used for narrative documents and books rather than web content.
*   **XQuery:** A query language (similar to SQL) used to extract data, elements, and attributes from XML repositories, often used alongside DocBook.
*   **TEI (Text Encoding Initiative):** An extremely rich and complex XML tag set (nearly 500 elements) designed to encode any genre of text from any period.
*   **NLM (National Library of Medicine):** The de facto XML DTD standard for scientific, medical journals, and publications.

# @Objectives

*   **Enforce Strict Content-Format Separation:** The AI MUST ensure that all content is authored purely for structure and semantic meaning, delegating all presentation and layout responsibilities exclusively to XSL stylesheets.
*   **Drive Maximum Component Reuse:** The AI MUST architect content into modular, single-sourced building blocks (like DITA topics) that can be aggregated dynamically across multiple outputs.
*   **Ensure Structural Consistency:** The AI MUST employ formal, rich-data-typed validation mechanisms (Schemas) to prevent inconsistent authoring and ensure predictable content retrieval.
*   **Select Appropriate Architectures:** The AI MUST correctly align the chosen XML framework (DITA, DocBook, NLM, TEI) with the specific industry, output requirement, and reuse goals of the user.

# @Guidelines

*   **XML vs. HTML Constraints:** The AI MUST NEVER use HTML presentation tags (e.g., `<h2>`, `<i>`, `<b>`, `<p>`) when designing raw XML content models. The AI MUST design XML tags to describe the *meaning* of the data (e.g., `<Procedure>`, `<Step>`, `<Fieldname>`).
*   **Schema over DTD:** When defining content structures, the AI MUST default to proposing and generating XML Schemas rather than DTDs to leverage well-formed XML syntax, rich data typing (e.g., restricting a `<year>` to four numeric characters), and global/local variables.
*   **Parser-Ready Design:** The AI MUST design all XML models under the assumption that a strict parser will validate them; therefore, models must be fully exhaustive regarding child elements, sequences, and empty elements.
*   **XSL Transformation Rules:** When publishing or formatting is required, the AI MUST output formatting logic separately using XSLT for digital/HTML transformations, XSL-FO for print/PDF formatting, or specific scripts bridging XML to composition tools (e.g., Adobe InDesign).
*   **DITA Implementation Rules:**
    *   The AI MUST separate content into discrete DITA topics (Concept, Task, Reference) inheriting from the Generic topic.
    *   The AI MUST NEVER embed heavy document hierarchy within the topics themselves.
    *   The AI MUST use DITA Maps to define the hierarchy, sequence, and aggregation of topics.
    *   The AI MUST apply the principle of minimalism, reducing information glut by providing only what the user needs.
*   **Alternative Framework Selection:**
    *   Use **DocBook** ONLY when the requirement is strictly book-based, narrative documentation (e.g., software manuals) with minimal component reuse requirements, or when paired heavily with XQuery databases.
    *   Use **NLM** strictly for scientific and medical journal publishing.
    *   Use **TEI** strictly for complex academic, historical, or literary text encoding.
    *   Use **DITA for Publishers** if the requirement bridges DITA's component reuse with traditional publishing components (articles, chapters, sidebars) targeting EPUB/Kindle.

# @Workflow

When executing an XML-based content strategy or architecture task, the AI MUST follow this rigid, step-by-step algorithmic process:

1.  **Requirements Analysis & Framework Selection:**
    *   Assess the content's domain (e.g., medical, literary, software, general enterprise).
    *   Assess the reuse requirements (high granular reuse = DITA; monolithic book output = DocBook; medical journals = NLM).
    *   Declare the chosen architectural framework before writing any code.
2.  **Semantic Tag Definition:**
    *   Analyze the required information product.
    *   Define custom, semantic XML tags that describe *what* the content is (e.g., `<Intro>`, `<ProcedureSteps>`) without any reference to *how* it looks.
3.  **Structural Rule Enforcement (Schema Generation):**
    *   Generate an XML Schema defining the exact hierarchy, sequences, and rich data typing for the semantic tags.
    *   Ensure strict validation rules are explicitly coded into the Schema.
4.  **Content Modularization (If using DITA):**
    *   Break the sample text into distinct topic types: Task (steps, actions, results), Concept (background info), and Reference (factual data).
    *   Create a DITA Map that aggregates these topic references via pointers.
5.  **Stylesheet Assignment (Transformation Design):**
    *   Generate the necessary XSLT code to transform the semantic XML into HTML/mobile-ready code.
    *   Generate the necessary XSL-FO code if paper/PDF output is requested.
6.  **Validation Review:**
    *   Simulate a parser check to ensure the generated XML complies perfectly with the generated Schema. Reject and regenerate if any formatting tags or structural violations exist.

# @Examples (Do's and Don'ts)

### XML Content Tagging
**[DO]** Use semantic, meaning-focused tags with structural hierarchy.
```xml
<Procedure Audience="All">
  <Title>Logging On to AccSoft</Title>
  <Text>You must log on to the system before you can complete any tasks.</Text>
  <Intro>To log on to AccSoft:</Intro>
  <ProcedureSteps>
    <Step>Double-click the AccSoft application</Step>
    <Step>Type your USERID into the <Fieldname>Name</Fieldname> field</Step>
    <Step>Click the OK button.</Step>
  </ProcedureSteps>
</Procedure>
```

**[DON'T]** Use presentation-focused HTML-style tags to structure enterprise content.
```html
<h2>Logging On to AccSoft </h2>
<p>You must log on to the system before you can complete any tasks.</p>
<h3>To log on to AccSoft:</h3>
<ol>
  <li>Double-click the AccSoft application</li>
  <li>Type your USERID into the <i>Name field</i></li>
  <li>Click the OK button.</li>
</ol>
```

### Schema vs DTD Usage
**[DO]** Define structure and data types using XML Schema for robust validation.
```xml
<xs:element name="year">
  <xs:simpleType>
    <xs:restriction base="xs:integer">
      <xs:pattern value="[0-9]{4}"/>
    </xs:restriction>
  </xs:simpleType>
</xs:element>
```

**[DON'T]** Rely solely on DTDs which lack rich data typing and cannot restrict character input types.
```dtd
<!ELEMENT year (#PCDATA)>
```

### Content Aggregation (DITA)
**[DO]** Use a DITA Map to aggregate independent modular topics.
```xml
<map title="AccSoft User Guide">
  <topicref href="concepts/c_about_accsoft.xml"/>
  <topicref href="tasks/t_logging_on.xml"/>
  <topicref href="reference/r_interface_buttons.xml"/>
</map>
```

**[DON'T]** Hardcode a monolithic document containing multiple distinct topics in a single rigid file that prevents topic-level reuse across different manuals.