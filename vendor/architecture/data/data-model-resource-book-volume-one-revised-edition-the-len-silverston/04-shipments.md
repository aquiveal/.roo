@Domain
Activation conditions: The AI MUST activate these rules when the user requests database design, schema creation, logical data modeling, data warehouse design, or ORM configuration specifically related to logistics, shipping, transportation, receiving, inventory issuance (picklists), delivery tracking, and routing. This applies to files such as SQL schemas, ERD documentation, and logistics application source code.

@Vocabulary
- **SHIPMENT**: An overarching entity tracking the movement of goods. Includes estimated dates, costs, and handling instructions.
- **OUTGOING SHIPMENT**: A shipment from an internal organization to an external organization. Subtypes include CUSTOMER SHIPMENT and PURCHASE RETURN.
- **CUSTOMER SHIPMENT**: Products sent out to customers.
- **PURCHASE RETURN**: Products returned to a supplier.
- **INCOMING SHIPMENT**: A shipment from an external organization to an internal organization. Subtypes include PURCHASE SHIPMENT and CUSTOMER RETURN.
- **PURCHASE SHIPMENT**: Incoming purchased items from a supplier.
- **CUSTOMER RETURN**: Incoming shipments of products returned by a customer.
- **TRANSFER**: A shipment from one internal organization to another internal organization.
- **DROP SHIPMENT**: A shipment moving directly from an external organization (supplier) to another external organization (customer).
- **SHIPMENT ITEM**: The detailed line item of a shipment indicating the quantity of a specific GOOD or a `shipment contents description` for non-standard items.
- **SHIPMENT STATUS**: A historical tracking entity recording the state of the shipment (e.g., scheduled, shipped, delivered) at a specific point in time (`status date`).
- **ORDER SHIPMENT**: An associative entity resolving the many-to-many relationship between ORDER ITEM and SHIPMENT ITEM to handle partial, combined, or substituted shipments.
- **SHIPMENT ITEM FEATURE**: An associative entity recording the exact product features shipped (which may differ from features ordered).
- **SHIPMENT PACKAGE**: The physical carton, box, or container containing shipment items.
- **PACKAGING CONTENT**: An associative entity linking SHIPMENT PACKAGE and SHIPMENT ITEM, including a `quantity` attribute to denote how many of an item are in a specific package.
- **SHIPMENT RECEIPT**: An entity tracking the actual receipt of a SHIPMENT PACKAGE, including `datetime received`, `quantity accepted`, `quantity rejected`, and `REJECTION REASON`.
- **SHIPMENT RECEIPT ROLE**: The role a party played in receiving (e.g., inspector, receiving manager).
- **PICKLIST / PICKLIST ITEM**: Entities identifying the plan for pulling items from inventory to fulfill outgoing shipments.
- **ITEM ISSUANCE**: An entity linking a SHIPMENT ITEM to the actual INVENTORY ITEM from which it was extracted.
- **SHIPMENT DOCUMENT**: Documentation accompanying a shipment (e.g., BILL OF LADING, PACKAGING SLIP, EXPORT DOCUMENT, MANIFEST, PORT CHARGES DOCUMENT, TAX AND TARIFF DOCUMENT, HAZARDOUS MATERIALS DOCUMENT).
- **SHIPMENT ROUTE SEGMENT**: An entity representing a single leg of a shipment's journey.
- **SHIPMENT METHOD TYPE**: The mode of transportation (e.g., ground, rail, air, cargo ship).
- **CARRIER**: The organization responsible for transporting the shipment route segment.
- **VEHICLE**: A subtype of FIXED ASSET used to transport shipments, tracking metrics like start/end mileage and fuel used.

@Objectives
- Accurately model the complete shipment lifecycle, separating planning/estimated data from historical status data.
- Establish highly flexible data structures that divorce shipments from orders via many-to-many item-level relationships, accommodating partial fulfillments, consolidated deliveries, and product substitutions.
- Track the physical reality of incoming goods by receiving *packages* rather than raw items, explicitly capturing acceptance, rejection, and discrepancy logic.
- Model the outgoing logistics pipeline rigorously by linking shipment items to inventory extractions via picklists and item issuances.
- Capture the geographical and chronological journey of shipments through granular routing segments, carriers, and vehicle metrics.

@Guidelines
- **Shipment Subtyping**: When creating a shipment entity, the AI MUST implement inheritance or subtyping for the shipment directions: OUTGOING SHIPMENT, INCOMING SHIPMENT, TRANSFER, and DROP SHIPMENT.
- **Date Separation**: The AI MUST place estimated/planning dates (`estimated ship date`, `estimated ready date`, `estimated arrival date`) directly on the SHIPMENT entity. Actual occurrence dates MUST be modeled inside a separate SHIPMENT STATUS history table.
- **Address & Party Linking**: A SHIPMENT MUST have explicit relationships to both a `shipped from` and a `shipped to` POSTAL ADDRESS and PARTY.
- **Auxiliary Contact Mechanisms**: The AI MUST model independent relationships between SHIPMENT and CONTACT MECHANISM for specific logistical purposes (e.g., a `receiving contact number` to call the receiver, and a `used to inquire about` contact to reach the sender).
- **Item Level Granularity**: What is being shipped MUST be modeled in a SHIPMENT ITEM entity. This entity MUST relate to a standard GOOD entity or utilize a `shipment contents description` attribute for non-standard, one-time goods.
- **Recursive Shipment Items**: The AI MUST implement a recursive relationship on SHIPMENT ITEM to handle items that are sent back in response to a previous shipment item (e.g., defect returns).
- **Order-to-Shipment Mapping**: The AI MUST NEVER create a direct 1-to-many relationship from ORDER to SHIPMENT. The AI MUST create an associative entity (ORDER SHIPMENT) between ORDER ITEM and SHIPMENT ITEM to handle many-to-many fulfillments (e.g., partial shipments, multiple orders in one shipment).
- **Feature Tracking**: Because the features of an item shipped may intentionally or accidentally differ from the item ordered, the AI MUST link PRODUCT FEATURE to SHIPMENT ITEM via a SHIPMENT ITEM FEATURE associative entity.
- **Inbound Receipts**: The AI MUST model receipts against the physical container (SHIPMENT PACKAGE), NOT the SHIPMENT ITEM directly. The hierarchy MUST be: SHIPMENT ITEM <- PACKAGING CONTENT -> SHIPMENT PACKAGE <- SHIPMENT RECEIPT.
- **Receipt Metrics**: The SHIPMENT RECEIPT entity MUST include `quantity accepted`, `quantity rejected`, and a relationship to REJECTION REASON.
- **Outbound Issuances**: Outgoing shipments MUST be modeled using a PICKLIST generated from SHIPMENT ITEMs. The actual extraction MUST be modeled using an ITEM ISSUANCE entity that links the SHIPMENT ITEM to the specific INVENTORY ITEM.
- **Shipment Documentation**: The AI MUST allow SHIPMENT DOCUMENT records to attach at three different levels of granularity depending on document type: to the SHIPMENT (e.g., Manifest), the SHIPMENT PACKAGE (e.g., Packing Slip), or the SHIPMENT ITEM (e.g., Hazardous Materials Document).
- **Route Segments**: The AI MUST model the path of a shipment using SHIPMENT ROUTE SEGMENTs. Each segment MUST link to exactly one SHIPMENT METHOD TYPE and exactly one CARRIER, and optionally a VEHICLE and from/to FACILITY entities.
- **Vehicle Metrics**: When tracking owned vehicles, the AI MUST model VEHICLE as a subtype of FIXED ASSET and include attributes for `start mileage`, `end mileage`, and `fuel used` on the relationship between VEHICLE and SHIPMENT ROUTE SEGMENT.

@Workflow
When tasked with designing a logistics or shipping database schema, the AI MUST follow this exact sequence:
1.  **Define Core Shipment**: Create the `SHIPMENT` table/entity with estimated date attributes, ship costs, and handling instructions. Subtype it into Incoming, Outgoing, Transfer, and Drop Shipment categories.
2.  **Assign Logistics Nodes**: Create foreign keys or relationships for `shipped_from_party`, `shipped_to_party`, `shipped_from_address`, and `shipped_to_address`. Add optional links for inquiry and receiving contact mechanisms.
3.  **Detail the Shipment Contents**: Create `SHIPMENT_ITEM`. Link it to the `GOOD` catalog. Add a recursive self-referencing relationship to handle returns of specific items. 
4.  **Map to Commitments (Orders)**: Create the `ORDER_SHIPMENT` many-to-many resolution table between `ORDER_ITEM` and `SHIPMENT_ITEM`. 
5.  **Handle Shipped Features**: Create the `SHIPMENT_ITEM_FEATURE` table to independently record the product features actually placed in the shipment.
6.  **Implement Status Tracking**: Create the `SHIPMENT_STATUS` table linking to `SHIPMENT` and `SHIPMENT_STATUS_TYPE` to record timestamped state changes.
7.  **Model Inbound Receiving**: Create `SHIPMENT_PACKAGE` and link to items via `PACKAGING_CONTENT`. Create `SHIPMENT_RECEIPT` linking to the package, equipped with acceptance/rejection quantity attributes.
8.  **Model Outbound Issuance**: Create `PICKLIST` and `PICKLIST_ITEM`. Create `ITEM_ISSUANCE` to bridge the `SHIPMENT_ITEM` and the specific `INVENTORY_ITEM` taken from the warehouse.
9.  **Map the Journey**: Create `SHIPMENT_ROUTE_SEGMENT`. Link it to `CARRIER`, `SHIPMENT_METHOD_TYPE`, and `VEHICLE` (treated as a fixed asset with mileage/fuel tracking).
10. **Attach Documentation**: Create `SHIPMENT_DOCUMENT` with polymorphic or optional relationships to `SHIPMENT`, `SHIPMENT_PACKAGE`, and `SHIPMENT_ITEM`.

@Examples (Do's and Don'ts)

- **Order-to-Shipment Resolution**
  - [DO]: 
    ```sql
    CREATE TABLE order_shipment (
      order_id INT,
      order_item_seq_id INT,
      shipment_id INT,
      shipment_item_seq_id INT,
      quantity DECIMAL(18,2),
      PRIMARY KEY (order_id, order_item_seq_id, shipment_id, shipment_item_seq_id)
    );
    ```
  - [DON'T]: 
    ```sql
    ALTER TABLE shipment ADD COLUMN order_id INT; -- Fails to handle partial or combined shipments at the item level.
    ```

- **Receipt Tracking Granularity**
  - [DO]:
    ```sql
    CREATE TABLE shipment_receipt (
      receipt_id INT PRIMARY KEY,
      shipment_package_id INT NOT NULL, -- Receipts happen against the physical package
      datetime_received DATETIME,
      quantity_accepted DECIMAL(18,2),
      quantity_rejected DECIMAL(18,2),
      rejection_reason_id INT
    );
    ```
  - [DON'T]:
    ```sql
    CREATE TABLE shipment_receipt (
      receipt_id INT PRIMARY KEY,
      shipment_item_id INT NOT NULL -- Ignores the physical reality of how goods arrive in boxes/cartons.
    );
    ```

- **Date and Status Tracking**
  - [DO]: Store `estimated_ship_date` on the `SHIPMENT` table, and store `status_date` alongside a `status_id` in a separate `SHIPMENT_STATUS` history table.
  - [DON'T]: Store `actual_ship_date` or `actual_arrival_date` directly on the `SHIPMENT` table without a corresponding history tracking table for state transitions.

- **Vehicle Tracking**
  - [DO]: Treat `VEHICLE` as a related entity to `SHIPMENT_ROUTE_SEGMENT` and track segment-specific metrics like `start_mileage`, `end_mileage`, and `fuel_used` on a vehicle-segment intersection (or directly on the segment if strictly one vehicle per segment).
  - [DON'T]: Treat `VEHICLE` merely as a string attribute on the shipment itself.