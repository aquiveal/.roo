@Domain
Trigger these rules when the user requests data modeling, database design, software architecture, or code generation related to purchasing, sales orders, product requirements, requests for quotes/proposals (RFI/RFP/RFQ), bidding, quotes, contracts, agreements, or order adjustments.

@Vocabulary
*   **Order**: A supertype entity representing a commitment between parties to purchase or sell products.
*   **Sales Order / Purchase Order**: Subtypes of the Order supertype, representing the transaction from the seller's or buyer's perspective.
*   **Order Item**: The specific goods, services, or product features requested within an Order. Subtyped into Sales Order Item and Purchase Order Item.
*   **Order Role**: The specific capacity in which a Party participates in an Order (e.g., Bill-To Customer, Placing Party, Internal Organization).
*   **Order Contact Mechanism**: The specific physical or electronic address/number used for a designated purpose on an Order (e.g., Ship-To address, Billing address).
*   **Order Adjustment**: Modifications to the cost of an Order or Order Item, such as discounts, surcharges, taxes, or shipping/handling fees. Never modeled as an Order Item.
*   **Order Status**: An entity tracking the history and current state of an Order or Order Item (e.g., received, approved) using a status datetime.
*   **Order Term**: The legal, financial, or performance conditions governing an Order or specific Order Item.
*   **Order Item Association**: An entity resolving the many-to-many relationship between Sales Order Items and Purchase Order Items (e.g., back-to-back ordering or backorders).
*   **Requirement**: An enterprise's or customer's established need for a product or work effort. Subtyped into Customer Requirement and Internal Requirement.
*   **Order Requirement Commitment**: An associative entity resolving the many-to-many relationship between Requirements and Order Items.
*   **Request**: A solicitation for bids or solutions (RFI, RFP, RFQ). Composed of Request Items.
*   **Quote**: A response to a Request detailing pricing and terms (Bid, Proposal). Composed of Quote Items.
*   **Agreement**: A formal contract between parties establishing long-term rules, terms, and pricing programs that govern future Orders. Composed of Agreement Items.
*   **Addendum**: An entity that tracks historical modifications to an Agreement or Agreement Item.

@Objectives
*   Eradicate the "I" perspective (where the enterprise is assumed and hardcoded) by explicitly modeling both internal and external organizations participating in orders.
*   Eliminate redundant data structures by unifying Sales Orders and Purchase Orders under a single universal Order model.
*   Ensure item-level granularity for shipping, terms, and adjustments so that individual items within an order can be handled independently.
*   Decouple contact mechanisms from parties within the context of an order, recognizing that an order may utilize a contact mechanism distinct from a party's standard profile.
*   Establish a seamless, fully traceable supply chain progression from Requirements -> Requests -> Quotes -> Agreements -> Orders.

@Guidelines
*   **Order Supertype Implementation**: The AI MUST model `ORDER` as a base entity with `SALES ORDER` and `PURCHASE ORDER` as subtypes. The AI MUST NOT create separate, isolated schemas for sales and purchases.
*   **Item-Level Shipping**: The AI MUST relate "Ship-To" parties and "Ship-To" contact mechanisms to the `ORDER ITEM`, NOT the `ORDER` header. This accommodates orders where different items are shipped to different destinations.
*   **Order Item Features**: When an ordered product includes specific configurable features (e.g., color, size), the AI MUST model this via a recursive relationship between `ORDER ITEM` instances (an Order Item for the feature is "ordered with" an Order Item for the product).
*   **Order Adjustments**: The AI MUST model discounts, taxes, surcharges, and fees as an `ORDER ADJUSTMENT` entity related to either the `ORDER` or `ORDER ITEM`. The AI MUST NOT model adjustments as subtypes of `ORDER ITEM` (adjustments are not ordered products).
*   **Party and Contact Mechanism Decoupling**: The AI MUST model the Party (who) and the Contact Mechanism (where) as independent relationships to the Order or Order Item. Do not assume knowing the party means knowing the order's specific contact mechanism, or vice versa.
*   **Flexible vs. Specific Roles**: 
    *   If the business rules are rigid and unchanging, the AI MUST explicitly model specific relationships (e.g., `ORDER` related to `BILL TO CUSTOMER`).
    *   If the business environment is dynamic, the AI MUST use a generic `ORDER ROLE` associative entity linking the `ORDER` to a `PARTY` and an `ORDER ROLE TYPE`.
*   **Status History**: The AI MUST track the life cycle of orders by utilizing an `ORDER STATUS` entity that includes a `status datetime` attribute to maintain a historical log, rather than just a single status attribute on the order.
*   **Derivable Statuses**: The AI MUST NOT include "shipped", "invoiced", or "backordered" as static Order Status values if they can be dynamically derived from physical shipment, invoice, or order item association records.
*   **Sales Tax**: The AI MUST use a `SALES TAX LOOKUP` entity resolving the intersection of `GEOGRAPHIC BOUNDARY` and `PRODUCT CATEGORY` to derive tax adjustments.
*   **Order Item Associations**: When a purchase order is generated to fulfill a sales order (e.g., a backorder), the AI MUST link them using a many-to-many `ORDER ITEM ASSOCIATION` entity.
*   **Requirement to Order Mapping**: The AI MUST relate `REQUIREMENT` and `ORDER ITEM` via a many-to-many `ORDER REQUIREMENT COMMITMENT` entity (including a `quantity` attribute) to allow partial fulfillments or grouped orders.
*   **Request and Quote Constraints**: The AI MUST relate a `QUOTE ITEM` to one and only one `REQUEST ITEM`. A request item can have many quote items (from multiple bidders), but a quote item specifically answers exactly one request item.
*   **Agreement to Order Rule**: When processing an order, the AI MUST validate pricing and terms against any active `AGREEMENT` covering the parties involved. An order may override an agreement, but the agreement acts as the baseline pricing program.

@Workflow
1.  **Establish the Core Order Hierarchy**: Define the `ORDER` supertype (attributes: order ID, order date, entry date) and its subtypes (`SALES ORDER`, `PURCHASE ORDER`). 
2.  **Define Order Items**: Define `ORDER ITEM` related to `PRODUCT`. Implement a recursive relationship on `ORDER ITEM` to handle optional/selectable product features.
3.  **Assign Roles and Contact Mechanisms**: 
    *   Link the `ORDER` header to Placing/Taking/Billing parties and mechanisms.
    *   Link the `ORDER ITEM` to Ship-To/Installation parties and mechanisms.
4.  **Implement Adjustments and Terms**: Create `ORDER ADJUSTMENT` (discounts, fees, taxes) and `ORDER TERM` entities. Relate both to either the `ORDER` (header level) or `ORDER ITEM` (line level).
5.  **Build the Requirement/Request/Quote Pre-Order Chain** (If requested by user):
    *   Model `REQUIREMENT` (recursive, subtyped into Product/Work).
    *   Model `REQUEST` (RFI, RFP, RFQ) and `REQUEST ITEM`.
    *   Link `REQUIREMENT` to `REQUEST ITEM` via `REQUIREMENT REQUEST`.
    *   Model `QUOTE` and `QUOTE ITEM`. Link `QUOTE ITEM` strictly to one `REQUEST ITEM`.
6.  **Establish Long-term Agreements** (If requested by user):
    *   Model `AGREEMENT` and `AGREEMENT ITEM`.
    *   Attach `AGREEMENT PRICING PROGRAM` (linked to `PRICE COMPONENT`) and `AGREEMENT TERM`s to dictate standard rules between parties.
7.  **Connect Chain to Order**: Map `REQUIREMENT`s, `QUOTE ITEM`s, and `AGREEMENT`s to `ORDER ITEM`s to complete the business cycle.

@Examples (Do's and Don'ts)

*   [DO] Unify Sales and Purchase Orders.
```sql
CREATE TABLE Order (
    order_id INT PRIMARY KEY,
    order_type VARCHAR(50), -- 'SALES' or 'PURCHASE'
    order_date DATE,
    entry_date DATE
);
```

*   [DON'T] Create redundant tables for Sales and Purchase Orders.
```sql
-- ANTI-PATTERN
CREATE TABLE Sales_Order (...);
CREATE TABLE Purchase_Order (...);
```

*   [DO] Place the shipping destination at the Item level to support split shipments.
```sql
CREATE TABLE Order_Item (
    order_item_seq_id INT,
    order_id INT,
    product_id INT,
    ship_to_party_id INT,
    ship_to_contact_mech_id INT,
    PRIMARY KEY (order_item_seq_id, order_id)
);
```

*   [DON'T] Place the shipping destination strictly at the Order header level.
```sql
-- ANTI-PATTERN: Prevents items in the same order from going to different locations.
CREATE TABLE Order (
    order_id INT PRIMARY KEY,
    ship_to_address_id INT 
);
```

*   [DO] Separate Order Adjustments from Order Items.
```sql
CREATE TABLE Order_Adjustment (
    order_adjustment_id INT PRIMARY KEY,
    order_id INT,
    order_item_seq_id INT NULL,
    adjustment_type VARCHAR(50), -- 'DISCOUNT', 'TAX', 'FEE'
    amount DECIMAL
);
```

*   [DON'T] Subtype Adjustments under Order Items.
```sql
-- ANTI-PATTERN: Adjustments are not ordered products.
CREATE TABLE Order_Item (
    item_type VARCHAR(50) -- 'PRODUCT', 'DISCOUNT_ADJUSTMENT'
);
```

*   [DO] Track order status historically.
```sql
CREATE TABLE Order_Status (
    order_id INT,
    status_type_id INT,
    status_datetime DATETIME,
    PRIMARY KEY (order_id, status_type_id, status_datetime)
);
```

*   [DON'T] Use a single overwritable status column.
```sql
-- ANTI-PATTERN: Destroys historical lifecycle data.
CREATE TABLE Order (
    order_id INT PRIMARY KEY,
    current_status VARCHAR(50)
);
```