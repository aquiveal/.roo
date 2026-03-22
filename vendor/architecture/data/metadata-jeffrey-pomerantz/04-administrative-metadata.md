# @Domain
These rules MUST trigger when the AI is tasked with designing, generating, or managing file systems, digital asset management (DAM) platforms, data schemas, file archiving protocols, digital object preservation strategies, copyright/licensing data models, or any request involving the tracking, structuring, and lifecycle management of digital resources.

# @Vocabulary
*   **Administrative Metadata**: Information used to inform the management of an object throughout its full life cycle. An umbrella term covering technical, structural, preservation, provenance, and rights metadata.
*   **Technical Metadata**: Information about how a system functions or system-level details about resources that require no human judgment to identify and can be captured automatically by software.
*   **Exif (Exchangeable Image File Format)**: A technical metadata schema used by digital cameras to embed manufacturer, user-configurable, and dynamic data (e.g., GPS, date/time) directly into an image file.
*   **Structural Metadata**: Information capturing how a resource is organized or the relationships between parts of a complex digital object.
*   **MPEG-21 / DIDL (Digital Item Declaration Language)**: A structural metadata standard defining an open framework for multimedia files using terms like *Container*, *Item*, *Descriptor*, and *Condition*.
*   **Provenance Metadata**: A record describing the history of a resource and the entities/processes involved in producing, delivering, or influencing that resource to establish trustworthiness.
*   **W3C Provenance Data Model**: A model defining three core structures for provenance: *Entity* (the resource), *Agent* (the entity influencing the resource), and *Activity* (the nature of the influence).
*   **Preservation Metadata**: Information a repository uses to support the digital preservation process, ensuring viability, renderability, understandability, authenticity, and identity of digital objects.
*   **PREMIS (Preservation Metadata Implementation Strategies)**: A core preservation metadata schema defining four entities: *Objects*, *Agents*, *Events*, and *Rights statements*, comprised of *Semantic Units* (elements).
*   **Semantic Units**: The equivalent of metadata "elements" specifically within the PREMIS data model (e.g., `significantProperties`, `preservationLevel`).
*   **Rights Metadata**: Information used to control who gets access to a resource, under what conditions, and what they can do with it.
*   **CC REL (Creative Commons Rights Expression Language)**: A rights metadata schema articulating *Work properties* (title, type, source, attribution) and *License properties* (permits, prohibits, requires, jurisdiction, legalCode).
*   **RightsDeclarationMD (METSRights)**: A rights metadata schema with three top-level elements: *RightsDeclaration*, *RightsHolder*, and *Context* (which includes *Permissions*).
*   **Meta-Metadata**: Metadata about metadata records themselves.
*   **METS (Metadata Encoding and Transmission Standard)**: A standard providing a container ("document") structure to wrap or link multiple metadata records for a single digital library object.

# @Objectives
*   Act as a proxy generator, creating simplified representations of objects to inform their maintenance, history, state, and future preservation.
*   Automate the capture of objective, system-level technical details without requiring human judgment.
*   Clearly delineate the organizational structure of composite or multimedia objects.
*   Establish resource trustworthiness and context by mapping its social and historical network (Provenance).
*   Ensure the long-term viability, renderability, understandability, authenticity, and identity of digital objects (Preservation).
*   Explicitly define access control, permissions, and intellectual property constraints (Rights).
*   Package dispersed and varied metadata records into a unified, standardized transmission document (METS).

# @Guidelines
*   **Technical Metadata Constraints**: 
    *   The AI MUST automatically extract or define technical metadata that requires no human judgment (e.g., creation/modification dates, file size, access permissions, creating application).
    *   When handling image files, the AI MUST explicitly support or simulate Exif data structures, separating data into manufacturer-set, user-configurable, and dynamic values.
*   **Structural Metadata Constraints**:
    *   For multi-part files or multimedia, the AI MUST use structural metadata (like DIDL) to define the exact order, relationship, and conditions of the parts (e.g., tracking which audio track plays alongside which video item, or the sequential order of a book's chapters).
*   **Provenance Metadata Constraints**:
    *   The AI MUST record not just the history of a digital file (which is easily duplicated/edited), but the relationships between the file and the entities that influenced it.
    *   The AI MUST map provenance using the W3C core structures: *Entity* (the file), *Agent* (person/org modifying it), and *Activity* (the action taken).
*   **Preservation Metadata Constraints**:
    *   When designing long-term storage or archiving schemas, the AI MUST utilize the PREMIS model.
    *   The AI MUST strictly define PREMIS *Entities* (*Objects*, *Agents*, *Events*, *Rights statements*) and populate them with granular *Semantic Units* (e.g., `formatName`, `formatVersion`, `formatRegistry`).
    *   The AI MUST identify `significantProperties` (characteristics crucial to preserve) and `preservationLevel` (functions to be applied).
*   **Rights Metadata Constraints**:
    *   The AI MUST NOT use overly broad, undefined rights statements if detailed access control is required.
    *   The AI MUST implement CC REL or RightsDeclarationMD logic to explicitly parse copyright into specific allowances and restrictions (e.g., *permits* [Reproduction, Distribution], *prohibits* [CommercialUse]).
*   **METS Packaging Constraints**:
    *   When aggregating multiple metadata schemas for a single resource, the AI MUST use the METS document structure consisting of exactly 7 parts.
    *   The AI MUST segment the METS Administrative section into exactly four sub-sections: *technical*, *intellectual property rights*, *source*, and *provenance*.
    *   The AI MUST use the METS *File* section to inventory linked records and the *Structural map* (the only explicitly required METS section) to organize the physical/logical structure of the object.
    *   The AI MUST use the METS *Header* to provide meta-metadata (metadata about the METS document itself, such as document creation date and archivist role).

# @Workflow
When tasked with designing a comprehensive metadata model for a digital resource, the AI MUST follow this algorithmic process:

1.  **Technical Extraction (Auto-Capture)**: Define the schema for capturing system-level data (file size, MIME type, Exif data). Ensure this requires zero human intervention.
2.  **Structural Definition**: If the object has multiple parts (e.g., an album with tracks, a book with pages, a video with subtitles), define a structural map (using DIDL concepts: Container, Item, Descriptor, Condition) indicating how the pieces assemble.
3.  **Provenance Tracking**: Establish a network tracking system. Log the *Entity*, the *Agent* that created/modified it, and the specific *Activity* (e.g., "derived from", "attributed to").
4.  **Preservation Strategy (PREMIS)**: Add preservation metadata. Define the digital *Object*, the preservation *Events* occurring over time, the acting *Agents*, and the *Semantic Units* required to guarantee future renderability (e.g., linking to a `formatRegistry`).
5.  **Rights Declaration**: Attach intellectual property and access constraints using CC REL or METSRights. Define the *RightsHolder*, the *Context*, and granular *Permissions* (discover, display, copy, modify, delete).
6.  **Meta-Metadata Packaging (METS)**: Wrap all the above schemas into a unified METS document.
    *   Generate a *Header* (data about the wrapper).
    *   Link/Wrap Descriptive metadata.
    *   Link/Wrap Administrative metadata (divided into technical, rights, source, provenance).
    *   List all linked files in the *File* section.
    *   Organize the object in the *Structural map*.
    *   Map relationships in the *Structural link* section.
    *   Define executable software rules in the *Behavior* section.

# @Examples (Do's and Don'ts)

### Technical Metadata
*   **[DO]**: Structure technical metadata to be automatically parsed by machines, separating static device data from dynamic data.
    ```json
    "TechnicalMetadata": {
      "Manufacturer": "Nikon",
      "Model": "D850",
      "Dynamic": {
        "DateTime": "2023-10-14T09:26:53Z",
        "GPS": "40.7128° N, 74.0060° W"
      }
    }
    ```
*   **[DON'T]**: Rely on human-generated subjective descriptions for technical attributes.
    ```json
    "TechnicalMetadata": {
      "CameraType": "A really nice professional camera",
      "TimeTaken": "Sometime in the afternoon"
    }
    ```

### Provenance Metadata
*   **[DO]**: Use W3C Provenance structures to map the exact relationship between the resource and its historical influencers.
    ```json
    "Provenance": {
      "Entity": "document_v2.pdf",
      "Activity": "Revision",
      "Agent": {
        "Name": "Jane Doe",
        "IP_Address": "192.168.1.15"
      },
      "DerivedFrom": "document_v1.pdf"
    }
    ```
*   **[DON'T]**: Overwrite previous states without tracking the agent and activity that caused the change, breaking the chain of trust.

### Preservation Metadata (PREMIS)
*   **[DO]**: Use specific Semantic Units and registries to ensure the file can be rendered decades later.
    ```xml
    <object>
      <significantProperties>color depth</significantProperties>
      <preservationLevel>bit-level preservation</preservationLevel>
      <format>
        <formatName>image/tiff</formatName>
        <formatVersion>6.0</formatVersion>
        <formatRegistry>http://www.nationalarchives.gov.uk/PRONOM/fmt/353</formatRegistry>
      </format>
    </object>
    ```
*   **[DON'T]**: Use generic, non-actionable preservation tags like `<preservation>Keep safe</preservation>`.

### Rights Metadata
*   **[DO]**: Break copyright down into specific machine-readable allowances and restrictions (CC REL / METSRights style).
    ```json
    "Rights": {
      "RightsHolder": "MIT Press",
      "LicenseProperties": {
        "Permits": ["Reproduction", "Distribution"],
        "Prohibits": ["CommercialUse", "DerivativeWorks"]
      }
    }
    ```
*   **[DON'T]**: Use a single, unparsed text string that software agents cannot interpret.
    ```json
    "Rights": "Copyright 2015 all rights reserved do not steal."
    ```

### METS Packaging
*   **[DO]**: Separate administrative metadata into its four strict sub-sections within a METS container.
    ```xml
    <mets>
      <metsHdr CREATEDATE="2023-10-24" />
      <amdSec>
        <techMD ID="tech1">...</techMD>
        <rightsMD ID="rights1">...</rightsMD>
        <sourceMD ID="source1">...</sourceMD>
        <digiprovMD ID="prov1">...</digiprovMD>
      </amdSec>
      <structMap TYPE="logical">...</structMap>
    </mets>
    ```
*   **[DON'T]**: Create a flat file where descriptive, technical, and preservation metadata are mixed indiscriminately without a structural map.