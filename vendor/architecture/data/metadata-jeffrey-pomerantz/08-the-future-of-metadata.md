@Domain
Triggered when the AI is tasked with designing or managing metadata schemas, integrating APIs for data exchange, structuring scientific or big data sets (eScience), building domain-specific classification systems (e.g., cultural heritage, music, education, publishing), or implementing telematics, logging, and data exhaust capture systems that involve user data.

@Vocabulary
- **Europeana Data Model (EDM) / DPLA Metadata Application Profile (MAP):** Custom, domain-specific metadata schemas that blend standard models with domain-specific properties to serve as portals for cultural heritage institutions.
- **SourceResource:** An entity class distinguishing the original physical, cultural, or intellectual object from its digital web representation.
- **Domain-Specific Metadata:** Highly tailored schemas designed for specialized fields (e.g., Pandora's Music Genome Project, IEEE LOM for education), which must continuously evolve to capture subjective or emerging characteristics.
- **API (Application Programming Interface):** Bidirectional technical interfaces that act as an end-run around graphical front-ends, serving as the primary mechanism for algorithmic metadata access, import, and export.
- **Small Pieces Loosely Joined:** An architectural philosophy where decentralized web services pass structured metadata back and forth to create complex, mashup applications (e.g., IFTTT).
- **eScience:** Computation-intensive and data-intensive research methods where data volume is too large for human comprehension, necessitating metadata surrogates.
- **Provenance Metadata (Dataset-level):** Statements regarding the origin of a dataset as a whole, including funding agencies, researchers, and macro-methodologies.
- **Provenance Metadata (Value-level):** Statements regarding the origin of individual data points within a dataset.
- **Paradata (eScience context):** Automatically captured metadata regarding the physical process of data collection (e.g., keystrokes, timestamps, unanswered calls during a survey).
- **Auxiliary Data:** External metadata imported into a dataset to provide context, such as demographic variables from a census.
- **Data Exhaust:** Vast quantities of routine metadata produced incidentally by users interacting with consumer products and digital services.
- **Third-Party Doctrine:** A legal principle stating individuals have no legitimate expectation of privacy for data (such as metadata) voluntarily provided to a third party (e.g., an ISP or telecom).
- **Pen Register / Trap and Trace:** Surveillance technologies that legally collect routing and addressing metadata rather than the content of communications.
- **Prejudicial Inferences:** Highly sensitive, personal conclusions drawn by aggregating seemingly innocuous, non-content metadata (e.g., MetaPhone study).

@Objectives
- Architect domain-specific metadata schemas that inherit from core standards but incorporate highly specialized, evolving properties.
- Utilize APIs strictly as bidirectional metadata delivery mechanisms to foster decentralized, interconnected application ecosystems.
- Construct metadata surrogates and multi-tiered provenance systems to ensure trust, discoverability, and reproducibility in large-scale data and eScience environments.
- Protect user privacy by treating metadata, logging, and data exhaust as unambiguously sensitive information capable of generating invasive personal inferences.

@Guidelines
- **Schema Hybridization:** The AI MUST construct metadata schemas by combining foundational element sets (e.g., Dublin Core, CC REL) with custom, domain-specific properties (e.g., `incorporates`, `isDerivativeOf`) rather than relying on a single, rigid standard.
- **Resource Disambiguation:** When modeling physical or cultural heritage items, the AI MUST explicitly create separate entity classes for the original physical item (`SourceResource`) and its digital surrogate/representation.
- **Evolutionary Vocabulary Design:** When building schemas for subjective or rapidly changing domains (e.g., music genres, publishing), the AI MUST design controlled vocabularies to be easily updateable to accommodate emerging subgenres and new characteristics.
- **API-First Metadata:** The AI MUST design and interact with APIs under the assumption that they are the primary conduits for structured metadata. APIs MUST be built to support "mashups" and cross-service automation (e.g., conditional triggers).
- **Metadata as Big Data Surrogate:** When managing large datasets (> GB/TB scale), the AI MUST NOT present raw data directly to human users; it MUST generate and present a descriptive metadata record as the primary access point.
- **Two-Tiered Provenance:** For all scientific, research, or analytical data, the AI MUST implement provenance tracking at two levels: the macro-level (dataset authors, funding, overarching methodology) and the micro-level (individual value paradata, auto-captured collection metrics, and auxiliary data).
- **Mandatory History Tracking:** To ensure trust in data products, the AI MUST implement robust history-tracking and version control for datasets, treating edit history as a fundamental component of provenance.
- **Privacy by Design for Data Exhaust:** The AI MUST explicitly reject the "it's only metadata" fallacy. All telematics, logging, and data exhaust MUST be secured and treated as personally identifiable information (PII) due to the risk of prejudicial inferences.
- **Third-Party Doctrine Awareness:** When designing systems that share user metadata with third-party services, the AI MUST enforce strict consent mechanisms and access controls, acknowledging that shared metadata loses constitutional privacy protections.

@Workflow
1. **Domain Contextualization:** Analyze the target domain. Identify standard schemas that can serve as a baseline (e.g., Dublin Core) and define the unique, evolving entities and properties required by the specific use case.
2. **Entity Modeling:** Separate the conceptual/physical object from the digital file. Define aggregations, spatial contexts, and temporal contexts as distinct classes.
3. **API Architecture:** Structure the system's APIs to bidirectionally expose this metadata, ensuring algorithms and external services can consume and append structured data.
4. **eScience & Provenance Structuring:** If handling datasets, automatically generate a descriptive surrogate. Append dataset-level provenance and architect the database to capture paradata (auto-generated collection metrics) for every incoming data point.
5. **Privacy & Inference Auditing:** Review all generated metadata and system logs. Identify patterns that could lead to sensitive inferences about users. Apply security measures equivalent to those used for direct communication content.

@Examples (Do's and Don'ts)

- **Domain-Specific Schema Creation**
  - [DO]: `{"Class": "SourceResource", "dc:title": "Mona Lisa", "edm:isDerivativeOf": "URI_to_previous_work", "DigitalRepresentation": "URI_to_image_file"}`
  - [DON'T]: Use a flat structure that conflates the physical painting with the JPEG file and ignores domain-specific relationships.

- **eScience Provenance**
  - [DO]: Embed two-tiered provenance in a dataset: `{"dataset_provenance": {"authors": "Smith et al.", "funding": "NSF"}, "data_points": [{"value": 42.5, "paradata": {"collection_timestamp": "2023-10-12T14:32:00Z", "sensor_uptime_ms": 402}}}`
  - [DON'T]: Store raw data arrays without collection methodology, paradata, or historical versioning, as this destroys scientific trust.

- **API Metadata Exchange**
  - [DO]: Design API endpoints to emit granular, structured metadata that other applications can logically bind to conditional triggers (e.g., "If `item_type` == 'educational_object', then import to LMS").
  - [DON'T]: Build APIs that only serve unstructured HTML blocks or raw files without accompanying descriptive and administrative metadata.

- **Handling Data Exhaust & Privacy**
  - [DO]: Encrypt and restrict access to a database of user application interactions, API calls, and location pings, explicitly documenting the risk of sensitive behavioral inferences.
  - [DON'T]: Leave system logs, call routing data, or location pings unsecured under the justification that "it's only metadata and doesn't contain the user's actual messages."