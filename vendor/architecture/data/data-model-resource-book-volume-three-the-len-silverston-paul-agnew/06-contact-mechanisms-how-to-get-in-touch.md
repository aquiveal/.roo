# @Domain

These rules MUST trigger whenever the AI is tasked with designing, analyzing, refactoring, or generating database schemas, data models, object-oriented classes, or architectural requirements that involve tracking how to communicate with or locate entities. Triggering keywords include but are not limited to: addresses, phone numbers, emails, URLs, contact information, contact mechanisms, communication channels, shipping/billing addresses, customer contact data, or geographic boundaries. 

# @Vocabulary

The AI MUST strictly adhere to the following definitions and mental models to ensure alignment with the reference text:

*   **Contact Mechanism (CM)**: An agency or means by which two or more persons, groups (parties), or other items (facilities) are placed in communication (e.g., telephone number, email address, postal address). It is a virtual method or "label" for getting in touch, NOT a physical structure.
*   **Device**: A physical instrument (e.g., the physical telephone hardware). A device is NOT a contact mechanism. 
*   **Facility**: A physical structure used to accommodate people or organizations (e.g., warehouse, building, room). A facility is NOT a contact mechanism; rather, a facility *has* contact mechanisms.
*   **Purpose**: The specific reason or intention for which a contact mechanism is used (e.g., 'Bill to', 'Ship to', 'Payment follow up').
*   **Usage**: The common customary context of a contact mechanism's use (e.g., 'Business', 'Personal', 'Emergency').
*   **Location (Classification)**: Where the contact mechanism is directed physically (e.g., 'Home', 'Office'). Distinct from "Usage" (e.g., a phone can be located at 'Home' but used for 'Business').
*   **Priority (Classification)**: The level of importance tied to the CM (e.g., 'Primary', 'Secondary').
*   **Level 1 Contact Mechanism Pattern**: A denormalized, specific pattern where contact mechanisms and their purposes/usages are modeled explicitly as attributes of the owning entity (e.g., `ship_to_address_part_1`, `personal_phone_number`).
*   **Level 2 Contact Mechanism Pattern**: A normalized pattern where CMs are modeled as separate entities (`POSTAL_ADDRESS`, `TELECOMMUNICATIONS_NUMBER`) or dependent entities (`PARTY_ELECTRONIC_ADDRESS`) and linked to parent entities via associative entities.
*   **Level 3 Contact Mechanism Pattern**: A generalized pattern using a `CONTACT_MECHANISM` supertype entity with subtypes (`POSTAL_ADDRESS`, etc.) and a highly flexible Level 3 Classification Pattern (`CONTACT_MECHANISM_CATEGORY`) for usages, purposes, and types.
*   **Level 4 Contact Mechanism Pattern**: The "Plug-and-Play" interface pattern using a single universal associative entity called `CONTACT_MECHANISM_APPLICATION` to link *any* entity in the enterprise to the `CONTACT_MECHANISM` supertype and its categories.
*   **Geographic Boundary**: An encompassing jurisdictional area (e.g., City, State, Postal Code, Province, Prefecture) used as a fundamental element of a postal address, phone code, or internet domain.
*   **Flexible Address Part**: A single atomic piece of postal address information (e.g., "Apt 5A", "100 Main Street").
*   **Non-solicitation Indicator**: A data attribute specifying whether a CM can legally/ethically be used to solicit business.

# @Objectives

*   Model contact mechanisms as abstract routing methods rather than physical devices or facilities.
*   Ensure the data model selected (Level 1 through 4) perfectly matches the enterprise's requirements for flexibility, scalability, and normalization.
*   Prevent 1NF and 3NF normalization violations in production systems by avoiding repeating contact attributes, unless explicitly developing a Level 1 prototype/scoping document.
*   Implement highly flexible, international-ready address structures that decouple atomic address parts from geographic boundaries.
*   Accurately assign auxiliary contact data (extensions, instructions, non-solicitation flags) to the correct associative or core entity to prevent data anomalies.

# @Guidelines

### 1. Separation of Concepts
*   The AI MUST NEVER merge the concept of a `FACILITY` (physical building, coordinates, square footage) with a `POSTAL_ADDRESS` (mailing label, street text). Facilities *have* addresses.
*   The AI MUST NEVER merge the concept of a `DEVICE` (hardware) with a `TELECOMMUNICATIONS_NUMBER` (the routing string). 

### 2. Selecting the Pattern Level
*   **Level 1 (Attributes)**: Use ONLY for prototyping, scoping, or capturing non-reusable, highly static, single-instance CMs (e.g., a one-off `skype_name` on a user profile). Do NOT use for production relational database designs due to repeating groups and update anomalies.
*   **Level 2 (Specific Entities)**: Use when the enterprise requires a normalized structure but wants distinct tables/classes for `POSTAL_ADDRESS`, `TELECOMMUNICATIONS_NUMBER`, and `ELECTRONIC_ADDRESS`. Use associative entities (e.g., `PARTY_TELECOMMUNICATIONS_NUMBER`) to assign Usage and Purpose.
*   **Level 3 (Supertype)**: Use when the enterprise needs to consolidate common relationships. Create a `CONTACT_MECHANISM` supertype table/class with subtypes. Use a `CONTACT_MECHANISM_CATEGORY` to dynamically assign types, purposes, usages, locations, and priorities without altering the schema.
*   **Level 4 (Application Interface)**: Use for highly dynamic, data-driven architectures. Implement a single `CONTACT_MECHANISM_APPLICATION` associative entity. Any new entity (Party, Order, Shipment) simply links to this interface to gain full CM capabilities.

### 3. Classification Nuances
*   The AI MUST distinguish between **Usage** (Personal vs. Business) and **Location** (Home vs. Office).
*   If using Level 2, model `CONTACT_MECHANISM_PURPOSE` as a 1:M relationship from the associative entity, and `CONTACT_MECHANISM_USAGE` as a 1:1 relationship from the associative entity (or M:M if "Business and Personal" overlapping is strictly required as separate instances).
*   If using Level 3 or 4, use the Category Classification structure so new classifications (e.g., Technology Type like "Fax Machine" or "PDA") can be added dynamically.

### 4. Geographic Boundaries
*   Do NOT hardcode geographic boundaries (City, State, Country, Zip) as simple string attributes on a Postal Address in normalized (Level 2-4) models.
*   Model a `GEOGRAPHIC_BOUNDARY` entity with subtypes or boundary types (City, Province, Prefecture, Country).
*   Link `CONTACT_MECHANISM` to `GEOGRAPHIC_BOUNDARY` via a `CONTACT_MECHANISM_BOUNDARY` associative entity.
*   Relate boundaries to one another (e.g., City belongs to State) using a `GEOGRAPHIC_BOUNDARY_ASSOCIATION` entity to enable validation and hierarchical drill-down.
*   Use Geographic Boundaries to store `country_telephone_code` (on the Country boundary) and `geographic_internet_region_code` (e.g., ".uk", ".in" on the Country boundary) rather than putting them on the CM directly.

### 5. Flexible Address Parts (Internationalization)
*   For systems requiring global address support, decompose addresses into `POSTAL_ADDRESS_PART` entities.
*   **CRITICAL XOR CONSTRAINT**: A `POSTAL_ADDRESS_PART` MUST link to EITHER a `POSTAL_ADDRESS_PART_TYPE` (e.g., 'Suite', 'Building Name', 'Street') OR a `GEOGRAPHIC_BOUNDARY` (e.g., 'New York City'), but NEVER both simultaneously.

### 6. Auxiliary Contact Data Placement
*   **Telephone Extensions**: Do NOT place the `extension` attribute on the `TELECOMMUNICATIONS_NUMBER` base entity. Base numbers (e.g., a company switchboard) are shared. The `extension` MUST be placed on the associative entity (e.g., `PARTY_TELECOMMUNICATIONS_NUMBER`, `PARTY_CONTACT_MECHANISM`, or `CONTACT_MECHANISM_APPLICATION`).
*   **Non-Solicitation**: Place the `non_solicitation_indicator` on the associative entity (link between Party and CM) if the CM is shared (e.g., two people share a home phone, one opts out, one opts in). Only place it on the base CM entity if the restriction applies universally regardless of the party.
*   **Instructions**: Place routing/timing instructions (e.g., "Deliver to back door") on the associative entity if context-specific (e.g., specific to an Order or Party), or on the base CM if universally true for that address.
*   **Directions**: Place travel directions ("Turn left at the barn") directly on the `POSTAL_ADDRESS` entity, or create a `DIRECTIONS` entity linked to the `POSTAL_ADDRESS`.

# @Workflow

When required to design, audit, or refactor a contact mechanism data structure, the AI MUST follow this algorithmic process:

1.  **Requirement Analysis & Pattern Selection**:
    *   Determine if the request is for a quick prototype/scope (Select Level 1) or a robust production schema (Select Level 2, 3, or 4).
    *   Determine the level of dynamic flexibility needed. If CM types are static, use Level 2. If new CM types and entities frequently appear, use Level 4.
2.  **Entity Separation Check**:
    *   Ensure NO physical properties (square footage, GPS points) are mixed with virtual routing labels (postal addresses). Separate `FACILITY` from `POSTAL_ADDRESS`.
3.  **Model Core CM Structures**:
    *   Define the base CM entities/supertypes based on the selected pattern.
    *   Define the associative entities linking the CM to the target subject (Party, Order, Facility).
4.  **Assign Classifications**:
    *   Attach Usage, Purpose, Location, and Priority classifications to the *associative* entities (not the base CM, to allow shared CMs to have different contexts).
5.  **Model Auxiliary Data**:
    *   Place `extension` and `non_solicitation_flag` on the associative linking entity.
6.  **Model Geographic & Address Parts (If international/complex)**:
    *   Extract City, State, Country, Zip into a `GEOGRAPHIC_BOUNDARY` structure.
    *   Construct the `POSTAL_ADDRESS_PART` entity with the strict XOR relationship to Boundary vs. Part Type.
7.  **Review against Anti-Patterns**:
    *   Ensure phone numbers don't contain hardcoded country codes if linked to a geographic boundary.
    *   Ensure no repeating groups (e.g., `phone_1`, `phone_2`) exist unless explicitly asked for a Level 1 model.

# @Examples (Do's and Don'ts)

### 1. Conceptual Separation: Facility vs. Address
*   **[DO]**: Create a `Facility` entity (attributes: `square_footage`, `has_loading_dock`) and link it to a `PostalAddress` entity (attributes: `street_text`, `postal_code`) via a `FacilityContactMechanism` associative entity.
*   **[DON'T]**: Add `square_footage` or `loading_dock_instructions` directly to the `PostalAddress` table.

### 2. Telephone Extensions
*   **[DO]**: Place the `extension` attribute in the `PartyTelecommunicationsNumber` associative table, allowing the base company phone number to be stored exactly once in the `TelecommunicationsNumber` table.
*   **[DON'T]**: Place the `extension` attribute in the `TelecommunicationsNumber` table, forcing the creation of duplicate rows for the same base company phone number just to store different extensions.

### 3. International Address Modeling
*   **[DO]**: Use a `PostalAddressPart` table where row 1 maps to a `PartType` ("Street Name": "Andheri Kurla Road") and row 2 maps to a `GeographicBoundary` ("City": "Mumbai"). This perfectly models varying international formats (e.g., Japanese Prefectures vs. US States).
*   **[DON'T]**: Hardcode `city`, `state`, `zip`, `province`, `prefecture`, `canton` as static columns on the `PostalAddress` table, resulting in massively sparse, denormalized, and rigid tables.

### 4. Classifying Shared Contact Mechanisms
*   **[DO]**: Model 'Purpose' and 'Usage' on the `PartyContactMechanism` table. Person A uses phone 555-1234 for 'Business' (Usage) and 'Technical Support' (Purpose). Person B uses phone 555-1234 for 'Personal' (Usage).
*   **[DON'T]**: Put 'Usage' directly on the `TelecommunicationsNumber` table, which makes it impossible for two people to share a home/business line under different contexts.

### 5. Level 4 Interface Modeling
*   **[DO]**: Create a `ContactMechanismApplication` table. When the business introduces a `Shipment` entity, simply add a `shipment_id` foreign key to `ContactMechanismApplication` so shipments immediately inherit all CM types, email validations, and phone routing rules.
*   **[DON'T]**: Re-create `ShipmentPostalAddress`, `ShipmentEmailAddress`, and `ShipmentTelecommunicationsNumber` tables from scratch, duplicating business logic.