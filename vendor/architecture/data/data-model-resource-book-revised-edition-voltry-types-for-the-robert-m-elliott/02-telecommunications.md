@Domain
Data modeling, database design, software architecture, and schema generation tasks specifically targeting Telecommunications enterprises. This includes Local Exchange Carriers (LECs), Regional Bell Operating Companies (RBOCs), Competitive Local Exchange Carriers (CLECs), Digital Local Exchange Carriers (DLECs), Interexchange Carriers (IEC/Long Distance), wireless communications providers, cable companies, and resellers of telecommunications services.

@Vocabulary
*   **TELECOMMUNICATIONS CARRIER**: An organization role for enterprises that provide telecommunication services (e.g., IECs, CLECs, DLECs).
*   **BILLING AGENT**: An organization role for a party that handles billing on behalf of another telecommunications carrier.
*   **RESIDENTIAL CUSTOMER / ORGANIZATION CUSTOMER**: Subtypes of the customer role separating individual home users from business entities.
*   **CONNECTIVITY SERVICE**: A service product subtype (e.g., LOCAL CONNECTIVITY, LONG DISTANCE CONNECTIVITY, WIRELESS CONNECTIVITY, DEDICATED LINE, INTERNET ACCESS).
*   **CONNECTIVITY FEATURE**: A product subtype providing additional functionality to a service (e.g., call waiting, caller ID, call forwarding).
*   **PERFORMANCE CHARACTERISTIC**: A product feature subtype measuring capacity or quality (e.g., bandwidth, noise rating), quantified with a UNIT OF MEASURE.
*   **NETWORK COMPONENT**: A physical network infrastructure element. Subtypes include NETWORK SUPPORT STRUCTURE (poles, towers), NETWORK SERVER (SWITCH, ROUTER, COMMUNICATION APPEARANCE), DEVICE (AMPLIFIER, FILTER, LOADING COIL), and CONNECTION COMPONENT (lines, cables).
*   **COMMUNICATION APPEARANCE**: The physical input slot or port allowing connection into the network (a subtype of NETWORK SERVER).
*   **NETWORK ASSEMBLY**: A combination of multiple network components used to deliver telecommunications service.
*   **CIRCUIT**: A logical configuration representing a set of capabilities that use portions of network assemblies to provide communications channels.
*   **DEPLOYMENT**: The instantiation/installation of a product or inventory item at a customer site or facility, tracked over time.
*   **DEPLOYMENT IMPLEMENTATION**: The entity linking a deployed product to the specific CIRCUITs and/or NETWORK ASSEMBLYs that fulfill it.
*   **COMMUNICATION IDENTIFIER**: The inventory of identification strings (phone numbers, IP addresses, pagers) used for communication connections, managed distinctly from standard contact mechanisms.
*   **SERVICE ORDER**: The telecommunications equivalent of a sales order, used for new sales, upgrades, and maintenance to existing deployments.
*   **DEPLOYMENT USAGE**: The entity tracking how a deployment is utilized, subtyped into CALL DETAIL, VOLUME USAGE, and TIME PERIOD USAGE.

@Objectives
*   Strictly separate the marketing/sales definitions of products from the physical implementation (Network Components) and the logical provisioning (Circuits).
*   Maintain accurate tracking of network assets, their geographical locations, and their combinations into functional assemblies.
*   Manage the inventory, assignment, and tracking of Communication Identifiers distinctly from generic party contact methods.
*   Enable complex billing scenarios, including usage-based billing (Call Detail, Volume) and external/third-party Billing Agent arrangements.
*   Provide a robust audit trail from Service Order to Deployment, Deployment Implementation, Deployment Usage, and ultimately Invoicing.

@Guidelines
*   **Party and Role Constraints**:
    *   The AI MUST categorize telecommunications partners and competitors using the TELECOMMUNICATIONS CARRIER role.
    *   The AI MUST support third-party billing scenarios by implementing the BILLING AGENT role and BILLING AGENT ASSIGNMENT relationships.
    *   The AI MUST distinguish customer demographics by explicitly subtyping customers into RESIDENTIAL CUSTOMER and ORGANIZATION CUSTOMER.
*   **Product Catalog Rules**:
    *   The AI MUST subtype telecommunications products into SERVICES (Connectivity Service, Connectivity Feature, Listing Offering, Channel Subscription, Installation/Repair, Service Agreement) and GOODS (Telecommunications System, Device, Accessory).
    *   The AI MUST define product features using AVAILABILITY FEATURE, BILLING FEATURE, and PERFORMANCE CHARACTERISTIC.
    *   The AI MUST map FEATURE INTERACTION INCOMPATIBILITY and FEATURE INTERACTION DEPENDENCY to prevent invalid product configurations.
    *   The AI MUST allow Product Associations (complements, substitutes) to be optionally constrained by specific NETWORK COMPONENT TYPES (e.g., a feature is only available if a specific switch type is used).
*   **Network Infrastructure Architecture**:
    *   The AI MUST model the physical network using NETWORK COMPONENT, subtyped into Support Structure, Server (Switch/Router/Appearance), Device, and Connection Component.
    *   The AI MUST track the location of network components using GEOGRAPHIC LOCATION, classifying the location as a PATHWAY (lines/cables), GEOGRAPHIC POINT (servers/devices), or GEOGRAPHIC BOUNDARY.
    *   The AI MUST allow NETWORK COMPONENTs to be grouped into NETWORK ASSEMBLYs via a many-to-many intersection entity.
*   **Circuit and Provisioning Rules**:
    *   The AI MUST represent the logical functionality of the network using the CIRCUIT entity.
    *   The AI MUST link CIRCUIT to NETWORK ASSEMBLY via the CIRCUIT PRESENCE entity.
    *   The AI MUST define capabilities (bandwidth, speed) via a CAPABILITY TYPE entity linked to NETWORK ASSEMBLY TYPE, CIRCUIT TYPE, and PRODUCT.
*   **Identifier Management Rules**:
    *   The AI MUST NOT embed telephone numbers or IP addresses solely as contact mechanisms if they represent the telecommunication provider's inventory.
    *   The AI MUST use COMMUNICATION IDENTIFIER for network routing numbers and explicitly link them to the physical COMMUNICATION APPEARANCE (port) via COMMUNICATION ID ASSIGNMENT.
*   **Service Order and Deployment Rules**:
    *   The AI MUST name order constructs as SERVICE ORDER and SERVICE ORDER ITEM.
    *   The AI MUST link the fulfillment of a SERVICE ORDER ITEM directly to a DEPLOYMENT entity.
    *   The AI MUST link the DEPLOYMENT to the physical/logical network using the DEPLOYMENT IMPLEMENTATION entity.
*   **Usage Tracking and Invoicing Rules**:
    *   The AI MUST NOT use standard "Shipment" models for service delivery. Delivery MUST be tracked via DEPLOYMENT USAGE.
    *   The AI MUST subtype DEPLOYMENT USAGE into CALL DETAIL (transactional), VOLUME USAGE (e.g., bandwidth used), and TIME PERIOD USAGE (subscription active time).
    *   The AI MUST generate INVOICE ITEMs from DEPLOYMENT USAGE records, utilizing a DEPLOYMENT USAGE BILLING intersection entity to allow a single usage to be billed multiple times (e.g., corrections) or multiple usages to be aggregated into one invoice item.

@Workflow
1.  **Define Parties and Roles**: Establish the internal organizations, residential/organization customers, telecommunications carriers, and billing agents. Set up the Telecommunications Carrier Relationship and Billing Agent Relationship.
2.  **Construct the Product Catalog**: Define Goods and Services. Attach Performance Characteristics and Availability Features. Map out Feature Interactions (dependencies and incompatibilities).
3.  **Model the Physical Network**: Instantiate Network Components (Switches, Routers, Ports, Lines). Assign them to Geographic Locations (Points, Pathways). Group physical components into Network Assemblies.
4.  **Define Logical Circuits and Capabilities**: Create Circuits representing logical paths. Map Circuits to Network Assemblies. Attach Capability Types (e.g., 1.544 Mbps bandwidth) to Circuits, Assemblies, and Products.
5.  **Manage Communication Identifiers**: Create the pool of Communication Identifiers (phone numbers). Assign them to Communication Appearances (physical ports) using Communication ID Assignments.
6.  **Process Service Orders**: Create Service Orders for Products/Features. Verify product availability by checking Circuit Capabilities, Network Assembly constraints, and Product Feature Incompatibilities.
7.  **Instantiate Deployments**: Upon Service Order confirmation, create a Deployment. Link the Deployment to a Facility (Central Office or Customer Location) and to the network via Deployment Implementation.
8.  **Track Deployment Usage**: As the customer utilizes the network, generate Deployment Usage records (Call Details, Volume Usage, or Time Period Usage).
9.  **Generate Invoices**: Aggregate Deployment Usage records. Apply pricing rules. Generate Invoices and assign them to the appropriate Billing Agent if third-party billing is required.
10. **Implement Analytics (Star Schema)**: Create a `DEPLOYMENT_USAGE_FACT` table with measures (quantity, billing amount) linked to dimensions (`CUSTOMERS`, `DEPLOYMENT_USAGE_TYPES`, `UNIT_OF_MEASURES`, `PRODUCTS`, `FACILITIES`, `TIME_BY_HOUR`).

@Examples (Do's and Don'ts)

*   **Network vs. Product Modeling**
    *   [DO]: Create a `PRODUCT` called "Dedicated Business Line" and a separate `CIRCUIT TYPE` called "DS 3 Line". Link the Deployment of the Product to the Circuit via `DEPLOYMENT IMPLEMENTATION`.
    *   [DON'T]: Add physical network attributes (like switch port or cable type) directly to the `PRODUCT` or `ORDER` table.

*   **Communication Identifier Management**
    *   [DO]: Create a `COMMUNICATION IDENTIFIER` table to hold all phone numbers owned by the telco. Link it to `COMMUNICATION APPEARANCE` to show which port the number is wired to. Allow an optional 1:1 link to `CONTACT MECHANISM` if the number is used by a party as their contact info.
    *   [DON'T]: Store assigned customer phone numbers only in the `CONTACT MECHANISM` table, losing the telco's ability to track unassigned numbers or port assignments.

*   **Tracking Telecommunications Delivery**
    *   [DO]: Record delivery of services using the `DEPLOYMENT USAGE` table, subtyped into `CALL DETAIL` (tracking start/end time and from/to numbers) or `VOLUME USAGE`.
    *   [DON'T]: Use generic `SHIPMENT` or `SHIPMENT ITEM` tables to track phone calls or internet bandwidth consumption.

*   **Billing and Invoicing**
    *   [DO]: Create an intersection entity `DEPLOYMENT USAGE BILLING` linking `DEPLOYMENT USAGE` to `INVOICE ITEM` to allow recalculations or aggregated billing. Include `BILLING AGENT ASSIGNMENT` to route the invoice to a third-party carrier if necessary.
    *   [DON'T]: Link an `INVOICE` directly to a `SERVICE ORDER` for ongoing usage-based services without intermediate usage tracking.