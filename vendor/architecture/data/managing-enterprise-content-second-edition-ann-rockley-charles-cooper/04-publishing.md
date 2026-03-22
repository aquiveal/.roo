@Domain
This rule file MUST be triggered when the AI is tasked with designing digital publishing workflows, engineering content management systems (CMS), structuring content for eBooks or applications, converting legacy documents (e.g., Word, PDF) into structured formats, or architecting any multichannel content delivery systems and unified content strategies for publishing environments.

@Vocabulary
*   **Digital Publishing**: A holistic approach to preparing content for device-independent, multichannel delivery (not merely the production of eBooks).
*   **Multichannel Delivery**: The automated distribution of a single content source to diverse endpoints (e.g., print, EPUB, iOS/Android apps, interactive web, GPS devices).
*   **Traditional Publishing Workflow**: An anti-pattern where a document is created as a single, format-bound entity (e.g., Microsoft Word) and managed as a "black box," making multichannel distribution a manual, costly process.
*   **In-house eBook Publishing Workflow**: An anti-pattern where print-publishing software is used to directly export digital formats (like EPUB), resulting in print-constrained digital files that require unsustainable "hand-tweaking" for different devices.
*   **XML Early (Structure Early)**: A workflow methodology where content is converted to a portable, open, structured markup format (XML) at the very beginning of the publishing process to enable automated formatting and reuse.
*   **Intelligent Content**: Content that is structurally rich, semantically categorized, and decoupled from its presentation format, rendering it discoverable and reusable.
*   **Repouring**: The automated process of regenerating all required output formats (e.g., HTML, PDF, EPUB) simultaneously from a single updated structured source file, eliminating the need to transfer files back and forth.
*   **WYSIWYG (What You See Is What You Get)**: A paradigm that is explicitly obsolete and invalid in an XML Early, multichannel publishing environment.
*   **Taxonomy**: A master integrated language of terms applied to content down to granular levels (e.g., article or chapter level) to drive custom content packaging, personalization, and findability.
*   **Component**: A modular, reusable piece of content, as opposed to a monolithic, complete document.

@Objectives
*   Transform publishing architectures from handcrafted, output-based workflows into automated, device-independent manufacturing pipelines.
*   Implement and enforce an "XML Early" (or equivalent Structure Early) methodology where content semantics and structure precede layout and formatting.
*   Free content from the "black box" of completed files (like PDFs or monolithic Word documents) by decomposing it into intelligent, manageable components.
*   Eliminate manual, device-specific "hand-tweaking" by relying strictly on automated template/stylesheet transformations.
*   Establish a unified content strategy that acts as a future-proof foundation, allowing the publisher to pivot instantly from standard eBooks to enhanced apps, custom packages, or unforeseen future devices.

@Guidelines
*   **Separation of Format and Content**: The AI MUST NEVER embed visual layout directives, page breaks, rigid column widths, or device-specific styling directly into the source content.
*   **Enforce XML Early**: The AI MUST engineer workflows that convert incoming content (e.g., legacy Word or InDesign files) into structured data (XML, JSON, or semantic Markdown) BEFORE entering the editorial or production loops.
*   **Componentization**: The AI MUST design databases and repositories to manage content as discrete, reusable components rather than complete documents. 
*   **Single Source of Truth**: The AI MUST implement a "repour" methodology. Corrections and edits MUST be applied exclusively to the source structured content. The AI MUST NEVER apply edits directly to the output files (e.g., tweaking an EPUB or HTML file).
*   **Agnostic Authoring**: The AI MUST NOT design authoring environments around WYSIWYG principles. Authors must interface with semantic structures, not visual layouts.
*   **Taxonomy Application**: The AI MUST define a master taxonomy and ensure the system tags content at granular levels (chapter, article, or node) to allow systems to instantly generate custom packages of content based on user contexts.
*   **Frictionless Integration**: When architecting toolchains, the AI MUST attempt to integrate structured data (XML) under the hood of tools staff already use (e.g., Word, Excel, InDesign) rather than forcing complex new tools that cause user rejection.
*   **Automated Formatting**: The AI MUST utilize stylesheet-driven transformations (e.g., XSLT, CSS, template engines) to adapt content for specific channels (e.g., Web, Print, Mobile). If a display issue occurs on a specific eReader or mobile device, the AI MUST update the global stylesheet/template, not the content.
*   **Scalability & Performance**: The AI MUST architect the content schema to handle "flavors" of outputs (e.g., multiple flavors of HTML, PDF, EPUB) from the exact same source tree.

@Workflow
1.  **Workflow Mapping**: Map out the current production workflow. Identify existing silos and handcrafted conversion steps that act as bottlenecks.
2.  **Legacy Conversion**: Convert the back catalog and front list files into a structured data format (XML/Semantic structure). Extract all hardcoded formatting.
3.  **Componentization & Integration**: Break the monolithic content down into modular components. Integrate XML tracking transparently into existing authoring tools (Word/InDesign) to prevent user friction.
4.  **Taxonomy & Metadata Application**: Develop an integrated master taxonomy. Tag all content down to the article and chapter level to enable advanced filtering, routing, and packaging.
5.  **Collaborative Editing Environment**: Implement online, collaborative review tools where copy editors and stakeholders edit the structured text dynamically, preserving the XML underneath.
6.  **Automated Transformation Pipelines**: Build automated format transformations (stylesheets/templates) that map the semantic XML structure into specific output "flavors" (Print PDF, Web HTML, Mobile App APIs, EPUB).
7.  **Dynamic Repouring**: When an edit is requested, modify the XML source component. Trigger the automated pipeline to instantly "repour" the content into all associated output channels simultaneously.
8.  **Custom Packaging**: Utilize the rich XML repository and taxonomy to build user interfaces (APIs) that dynamically generate custom content packages or feed new digital apps without requiring any manual content rework.

@Examples (Do's and Don'ts)

**Principle: XML Early & Separation of Format**
*   [DO]: Convert incoming manuscripts into a semantic XML structure: `<procedure><step>Turn the dial.</step><warning>Do not over-tighten.</warning></procedure>`. Use a separate transformation engine to output this to an EPUB file with specific CSS for warnings.
*   [DON'T]: Accept a Microsoft Word document formatted with 14pt red bold text for warnings, run it through an EPUB converter, and pass the resulting hard-coded HTML to the production team.

**Principle: Correcting Content (Repouring)**
*   [DO]: Fix a typo by accessing the central component CMS, updating the text in the source `<chapter>` node, and triggering an automated script that regenerates the updated PDF, Web HTML, and EPUB files automatically.
*   [DON'T]: Unzip the generated EPUB file, fix the typo in the `chapter1.xhtml` file, re-zip it, and leave the original source database and the Print PDF containing the error.

**Principle: Device Adaptation**
*   [DO]: Define content semantically so the delivery engine can apply device-independent rules. For example, rendering a complex table as an interactive, scrollable data-grid on a mobile app, but as a standard printed table in the PDF.
*   [DON'T]: Manually create a separate "Mobile_Version" of the content where the table has been manually chopped into bulleted lists by an editor to make it fit on a small screen. 

**Principle: Tool Integration**
*   [DO]: Configure existing tools (like Microsoft Word or InDesign) with schema-enforcing plugins that save structural XML to the repository behind the scenes, reducing the learning curve for non-technical authors.
*   [DON'T]: Force copy editors and subject matter experts to manually write XML tags in a raw text editor, causing project abandonment due to complexity.