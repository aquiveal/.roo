# @Domain

These rules trigger when the AI is tasked with designing, analyzing, or configuring metadata schemas, taxonomies, search and retrieval parameters, content management system (CMS) tags, and XML/DITA element attributes to support a unified enterprise content strategy.

# @Vocabulary

*   **Metadata**: The encoded knowledge of the organization. It encompasses physical data descriptions, technical and business processes, rules, constraints, and the structural hierarchy of the content.
*   **Descriptive (Publication) Metadata**: Customer-facing tags designed specifically to help end-users retrieve completed information products (e.g., books, web pages, PDFs) via search engines or indexes. 
*   **Component Metadata**: Author-facing tags applied at the granular (element/topic) level. Primarily used by content creators to find, track, and reuse individual pieces of content across multiple outputs.
*   **Reuse and Retrieval Metadata**: A subcategory of Component Metadata used to identify where, how, and for whom a specific component is valid (e.g., Product, Content Type, Geography, Audience).
*   **Tracking (Status) Metadata**: A subcategory of Component Metadata used to control workflow routing and lifecycle states (e.g., Draft, Ready for Review, Approved).
*   **Faceted Search**: A search methodology driven by categorized metadata (facets) that allows users to narrow down large volumes of information by applying specific filters.
*   **Vertical Taxonomy**: Pre-existing, industry-specific categorization schemas (e.g., NLM for medicine, SCORM for eLearning).
*   **Crosswalk**: A mapping matrix used to reconcile and link competing metadata terminologies across different departmental systems (e.g., mapping Marketing's "Title" to Service's "Subject").
*   **Dublin Core**: A standard 15-element set of semantic metadata (Contributor, Coverage, Creator, Date, Description, Format, Identifier, Language, Publisher, Relation, Rights, Source, Subject, Title, Type).
*   **RDF (Resource Description Framework)**: A W3C XML-based framework for describing and interchanging metadata with explicitly defined semantics.
*   **XMP (eXtensible Metadata Platform)**: An Adobe framework for embedding and preserving component-level metadata within a container document.

# @Objectives

*   Ensure all content is automatically discoverable, reusable, and reconfigurable by tagging at the component level, not just the document level.
*   Eliminate redundant content creation by enabling authors and CMS platforms to instantly locate existing modular components.
*   Automate workflow routing and lifecycle management by strictly binding tracking metadata to system rules.
*   Resolve enterprise silos by standardizing disparate departmental terminology through Crosswalks and open standards (Dublin Core, RDF, XMP).

# @Guidelines

*   **Reverse-Engineer Metadata Generation**: When defining metadata, the AI MUST first explicitly state the target business result (e.g., dynamic localization, automated workflow routing) and then design the metadata architecture backward to achieve that result.
*   **Enforce the Descriptive vs. Component Split**: The AI MUST categorically separate metadata into Descriptive (for end-users finding products) and Component (for authors finding reusable chunks). Do not merge these contexts.
*   **Component Granularity Rule**: The AI MUST apply Component Metadata to the smallest logical building block of content, capturing properties like Content Type (Concept, Task), Product grouping, Geography, Audience, and Security Level.
*   **Workflow-Driven Tracking**: The AI MUST map Tracking Metadata strictly to the organization's defined workflow states. Status tags (e.g., "Ready for review") MUST be designed as functional triggers that dictate system routing and permissions.
*   **Crosswalk Conflict Resolution**: When encountering or integrating content from multiple departments (e.g., CRM vs. Knowledge Management vs. CMS), the AI MUST generate a Crosswalk table to map divergent terms to a unified semantic standard.
*   **Standardization over Customization**: Before inventing custom tags, the AI MUST attempt to map metadata to existing Vertical Taxonomies and the Dublin Core Metadata Element Set.
*   **Metadata Roll-up (Inheritance)**: The AI MUST design relationships ensuring that component-level metadata logically aggregates to the publication container (e.g., multiple component authors roll up into a single publication contributor list).
*   **User-Centric Terminology**: Descriptive Metadata MUST be derived directly from user personas and observed customer search behaviors, not internal corporate jargon.

# @Workflow

When executing a metadata design or configuration task, the AI MUST follow this exact sequence:

1.  **Define Business Outcomes**: Identify the specific automation, retrieval, or reuse goal the metadata is intended to solve (e.g., filtering content by mobile constraints, translating only updated components).
2.  **Analyze the Audience**: Determine if the primary consumer of the metadata is an end-user (Descriptive) or an internal author/system (Component).
3.  **Establish Descriptive Metadata (End-User)**:
    *   Group content into facets/categories based on customer mental models and search behaviors.
    *   Integrate industry-standard Vertical Taxonomies if available.
    *   Apply Dublin Core standards for structural consistency.
4.  **Establish Component Metadata (Internal Reuse)**:
    *   Define Reuse/Retrieval tags: Identify Product, Content Type, Geography/Language, Audience, and Security Level.
    *   Define Tracking tags: Establish lifecycle states (Draft, In Review, Approved) and assign administrative tags (Author, Editor, Time, Translation Status).
5.  **Reconcile Terminology (Crosswalk)**: If integrating across multiple systems, build a Crosswalk table mapping legacy department terms to the newly established unified metadata standard.
6.  **Define Roll-up Rules**: Explicitly declare how granular component tags will aggregate when published as a compiled information product.

# @Examples (Do's and Don'ts)

**[DO]** Design a granular, separated metadata schema that addresses both retrieval and tracking, utilizing standard frameworks and Crosswalks.

```xml
<!-- Context: Designing Metadata for a modular "Glycemic Index" component -->

<!-- 1. COMPONENT METADATA: Reuse & Retrieval (Author-Facing) -->
<metadata type="component-reuse">
    <product>GI_Database</product>
    <content_type>Definition_Short</content_type>
    <audience>Patient</audience>
    <geography>Global</geography>
    <security_level>Public</security_level>
</metadata>

<!-- 2. COMPONENT METADATA: Tracking & Status (System-Facing) -->
<metadata type="component-tracking">
    <lifecycle_status>Ready_for_Review</lifecycle_status> <!-- Triggers workflow routing -->
    <author>Sharon S.</author>
    <last_modified>2023-10-24</last_modified>
    <translation_status>Source_English</translation_status>
</metadata>

<!-- 3. DESCRIPTIVE METADATA: Publication Roll-up (End-User Facing using Dublin Core) -->
<metadata type="descriptive-publication">
    <dc:title>Understanding the Glycemic Index</dc:title>
    <dc:creator>Sharon S., Dr. Jenkins</dc:creator> <!-- Rolled up from components -->
    <dc:subject>Diabetes Management, Diet</dc:subject>
    <dc:format>application/epub+zip</dc:format>
</metadata>

<!-- 4. SYSTEM CROSSWALK DEFINITION -->
<!-- Mapping CRM "Topic" and KM "Subject" to CMS unified standard -->
<crosswalk>
    <map from_system="CRM" term="Topic" to_unified="dc:subject" />
    <map from_system="KM" term="Keyword" to_unified="dc:subject" />
</crosswalk>
```

**[DON'T]** Define generic, document-level metadata without separating author reuse states from customer search tags, ignoring business outcomes and workflows.

```xml
<!-- ANTI-PATTERN: Monolithic, generic metadata that traps content in a silo -->
<doc_properties>
    <filename>GI_Info_Final_v2.docx</filename>
    <title>GI Info</title>
    <author>Marketing Dept</author>
    <status>Done</status>
    <tags>health, food, index</tags>
    <!-- Fails to define component granularity -->
    <!-- Fails to use Dublin Core standards -->
    <!-- Fails to include workflow routing triggers like "Ready for Review" -->
    <!-- Fails to define reuse facets like Audience or Content Type -->
</doc_properties>
```