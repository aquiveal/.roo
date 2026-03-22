@Domain
Information Architecture, Database Design, Metadata Modeling, Cataloging, Search and Retrieval System Development, and Digital Resource Organization.

@Vocabulary
- **Metadata**: A statement or set of statements about a potentially informative object; data about data; a mechanism that exists at a higher level of abstraction, "beyond" the data.
- **Data Exhaust / Ubiquitous Metadata**: The infrastructural, constantly generated background data produced by modern electronic interactions (e.g., cell phone pings, GPS tracking) that, when aggregated, allows for deep, potentially sensitive inferences about behavior.
- **Pinakes**: The first known library catalog (Library of Alexandria), establishing the foundational metadata attributes: genre, title, author, summary, and length.
- **Call Number**: An alphanumeric string or designated pointer that correlates a simplified metadata record to a physical or digital location in an information space.
- **Atomization**: The architectural process of breaking down datasets along two dimensions: independent, manipulatable records for individual items (rows), and shared, standardized categories of data across all items (columns).
- **The Map is Not the Territory**: A principle (coined by Alfred Korzybski) dictating that metadata is a simplified, functional representation of a resource, deliberately omitting the full complexity of the original object to enable navigation.
- **Resource Discovery**: The systemic process of identifying information resources that might fulfill a user's information need based on metadata.
- **Relevance**: A strictly subjective, highly individualized judgment of an object's usefulness that cannot be universally encoded.
- **Objective Description**: Verifiable, factual features of resources used to power resource discovery, standing in contrast to subjective relevance.
- **Descriptive Metadata**: Metadata that provides an objective description of an object (e.g., title, author, subject).
- **Administrative Metadata**: Information about the origin, maintenance, and intellectual property restrictions of an object (e.g., scanner resolution, copyright status).
- **Structural Metadata**: Information defining how an object is physically or logically organized (e.g., chapters, page order).
- **Preservation Metadata**: Information necessary to support the long-term viability and preservation of an object (e.g., required application/OS emulation).
- **Use Metadata**: Information tracking how an object has been interacted with over time (e.g., download counts, user profiles).

@Objectives
- To architect metadata systems that function as navigable, simplified "maps" for complex data "territories."
- To rigorously enforce the two-dimensional atomization of data into discrete records and shared objective categories.
- To strictly differentiate between objective descriptions (which must be tracked) and subjective relevance (which must not be tracked as universal metadata).
- To categorically organize all metadata into the five distinct systemic flavors: Descriptive, Administrative, Structural, Preservation, and Use.

@Guidelines
- **The Map Principle**: The AI MUST design metadata schemas as simplified surrogates. It MUST NOT attempt to capture the full, raw complexity of the described resource within the metadata itself.
- **Two-Dimensional Atomization**: The AI MUST structure metadata into databases or tabular formats consisting of individual, manipulatable records (objects) and standardized attributes (fields). It MUST strictly avoid append-only flat lists (like historical shelf lists).
- **Objective Filtering**: The AI MUST restrict search and discovery metadata to objective, verifiable attributes. The AI MUST NOT design schemas that attempt to encode subjective interpretations like "relevance" directly into the resource's global record.
- **Categorical Separation**: When defining attributes for a resource, the AI MUST explicitly categorize them into Descriptive, Administrative, Structural, Preservation, or Use metadata. 
- **Inference Awareness**: The AI MUST evaluate aggregated metadata structures for privacy implications. The AI MUST recognize that seemingly innocuous metadata (e.g., time, duration, identifiers), when aggregated, produces sensitive behavioral inferences.
- **Pointer Integration**: The AI MUST ensure every metadata record contains a distinct locator (equivalent to a "call number") that bridges the gap between the abstract record and the actual resource.
- **Infrastructural Invisibility**: The AI MUST design metadata pipelines to run seamlessly in the background, ensuring smooth resource discovery without overwhelming the end-user with raw structural data.

@Workflow
1. **Analyze the Territory**: Identify the full, complex information object or space that requires organization.
2. **Define the Map (Abstraction)**: Determine the minimum viable details required to navigate, describe, and locate this object in a specific use case.
3. **Execute Two-Dimensional Atomization**: Create a schema where the object is represented as a discrete, independent record containing standardized categorical fields shared by all items in the system.
4. **Categorize by Flavor**: Map every defined field into one of the five metadata types:
   - *Descriptive* (What is it?)
   - *Administrative* (Where did it come from / who owns it?)
   - *Structural* (How is it built?)
   - *Preservation* (How do we keep it alive?)
   - *Use* (Who is interacting with it?)
5. **Purge Subjectivity**: Audit the schema to ensure no field requires a subjective judgment of "relevance." Replace any subjective fields with objective, searchable descriptors.
6. **Assign Locators**: Generate and embed a unique identifier or "call number" field that points directly to the physical or digital location of the source object.
7. **Perform Privacy/Inference Audit**: Review the completed schema to assess what behavioral inferences could be made if this metadata were aggregated at scale.

@Examples (Do's and Don'ts)

**Principle: Two-Dimensional Atomization**
- [DO]: Structure metadata as independent, manipulatable objects with shared schema keys.
  ```json
  [
    {
      "id": "HD53.P35",
      "title": "Intellectual Property Strategy",
      "author": "Palfrey, John",
      "publication_year": 2012
    },
    {
      "id": "Z286.O63",
      "title": "Open Access",
      "author": "Suber, Peter",
      "publication_year": 2012
    }
  ]
  ```
- [DON'T]: Structure metadata as an unbroken, flat log that cannot be queried by shared categories.
  ```text
  Acquired John Palfrey's Intellectual Property Strategy book (2012) and put it on shelf 1. Then acquired Open Access by Peter Suber (2012) and put it next to it.
  ```

**Principle: Objective Description vs. Subjective Relevance**
- [DO]: Tag resources with factual, objective metadata that enables resource discovery across different user needs.
  ```json
  {
    "subject": ["Whaling", "Revenge", "Obsession"],
    "genre": "Fiction",
    "word_count": 206052
  }
  ```
- [DON'T]: Tag resources with subjective assessments that vary wildly depending on the user.
  ```json
  {
    "relevance_to_students": "High",
    "interesting_plot": true,
    "usefulness": 8
  }
  ```

**Principle: The 5 Flavors of Metadata**
- [DO]: Explicitly segment metadata based on its operational purpose within the system.
  ```json
  {
    "descriptive": {"title": "Mona Lisa", "creator": "Leonardo da Vinci"},
    "administrative": {"copyright": "Public Domain", "scanner_dpi": 1200},
    "structural": {"file_format": "TIFF", "dimensions": "3000x4500"},
    "preservation": {"required_color_profile": "Adobe RGB 1998"},
    "use": {"total_downloads": 450392, "last_accessed": "2023-10-24T14:32:00Z"}
  }
  ```
- [DON'T]: Dump all properties into a flat, mixed object, obfuscating the systemic purpose of each data point.
  ```json
  {
    "title": "Mona Lisa",
    "dpi": 1200,
    "downloads": 450392,
    "format": "TIFF",
    "author": "Leonardo da Vinci"
  }
  ```

**Principle: The Map is Not the Territory (Abstraction)**
- [DO]: Extract strictly the necessary navigational metadata for a communication log (Data Exhaust).
  ```json
  {
    "caller_id": "+1-555-0100",
    "receiver_id": "+1-555-0199",
    "timestamp": "2023-10-24T14:32:00Z",
    "duration_seconds": 145,
    "cell_tower_location": "35.9049, -79.0469"
  }
  ```
- [DON'T]: Attempt to embed the full complexity of the interaction (the territory) into the index (the map).
  ```json
  {
    "caller_id": "+1-555-0100",
    "full_audio_transcript": "Hello? Hi, I need to call the locksmith, the hydroponics dealer, and the home improvement store..."
  }
  ```