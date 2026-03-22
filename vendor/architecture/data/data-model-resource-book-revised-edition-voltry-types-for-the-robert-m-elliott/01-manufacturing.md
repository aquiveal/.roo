@Domain
Trigger these rules when the AI is tasked with designing, refactoring, querying, or analyzing database schemas, data models, or software architectures for manufacturing enterprises, Enterprise Resource Planning (ERP) systems, Materials Requirements Planning (MRP) systems, Product Lifecycle Management (PLM) applications, or shop-floor control systems.

@Vocabulary
*   **Discrete Manufacturing:** The assembly of tangible parts into components (e.g., computers, appliances, machines).
*   **Process Manufacturing:** The mixing of liquids or formulas to create products (e.g., chemicals, paints).
*   **PART:** The type of physical item used or produced in the manufacturing process (distinct from PRODUCT).
*   **PRODUCT:** The marketing offering or the type of thing that is marketed/offered for sale to a customer.
*   **FINISHED GOOD:** A subtype of PART that is ready to be shipped. It maps to one or more PRODUCTs.
*   **RAW MATERIAL:** A subtype of PART representing the lowest-level component purchased from a supplier, with no work performed by the enterprise.
*   **SUBASSEMBLY:** A subtype of PART representing a state of partial completion.
*   **PART SPECIFICATION:** The technical design dimensions, performance characteristics, and tolerances applicable to a PART.
*   **ENGINEERING CHANGE (EC):** A process managing modifications to parts/BOMs, passing through statuses: Request, Notice, and Release.
*   **PART BOM (Bill of Materials):** The hierarchical breakdown of the components comprising a PART.
*   **ENGINEERING BOM:** A PART BOM view defining components and subcomponents from an engineering view with precise specifications.
*   **MANUFACTURING BOM:** A PART BOM view defining the exact parts selected for use in the actual manufacturing process based on cost and quality.
*   **MARKETING PACKAGE:** A product-level hierarchy (not part-level) grouping together products for promotional sales.
*   **PART SUBSTITUTE:** Parts that can replace other parts independent of the BOM context.
*   **PART BOM SUBSTITUTE:** Parts that can replace other parts *only* within a specific bill of materials context.
*   **INVENTORY ITEM CONFIGURATION:** The exact, physical configuration of a specific serialized item (actual vs. standard BOM), subtyped into MANUFACTURING CONFIGURATION and SERVICE CONFIGURATION.
*   **DEPLOYMENT:** The installation event and ongoing location of an INVENTORY ITEM at a customer site.
*   **DEPLOYMENT USAGE:** Tracking of how a deployed product is utilized, categorized into ACTIVITY USAGE, VOLUME USAGE, and TIME PERIOD USAGE.
*   **PROCESS PLAN:** The standard steps, skill standards, and fixed asset standards required to manufacture a product (WORK EFFORT TYPE).
*   **PRODUCTION RUN:** The actual instance of shop-floor work executed to produce products (WORK EFFORT).
*   **MRP (Materials Requirements Planning):** The algorithms and data used to forecast and order the precise amount of resources just in time for production.

@Objectives
*   Ensure absolute separation between physical items managed by the supply chain (PARTs) and the offerings sold by marketing/sales (PRODUCTs).
*   Provide robust, multi-perspective hierarchical data structures that support distinct Engineering, Manufacturing, and Marketing views of assemblies.
*   Preserve the strict traceability of engineering specifications, version changes, and part substitutability context.
*   Track the lifecycle of physical items from raw materials through standard assemblies to specific, real-world fielded configurations (deployments).
*   Capture the granular differences between standard process blueprints (Process Plans) and actual executed shop-floor work (Production Runs).

@Guidelines
*   **Party and Organization Modeling:**
    *   The AI MUST differentiate between a `DISTRIBUTION_CHANNEL` (the method/organization used to get products to market), a `DISTRIBUTOR` (buys and sells the manufacturer's products), and a `CUSTOMER` (the end purchaser/user).
    *   The AI MUST subtype the `CUSTOMER` role into `BILL_TO_CUSTOMER`, `SHIP_TO_CUSTOMER`, and `END_USER_CUSTOMER` to resolve complex corporate purchasing scenarios.
*   **Part vs. Product Separation:**
    *   The AI MUST NOT model `PART` and `PRODUCT` as the same entity.
    *   The AI MUST define a one-to-many relationship from `FINISHED_GOOD` (a `PART` subtype) to `PRODUCT`, acknowledging that a single physical item can be sold under multiple marketing identities.
*   **Design Engineering & Specifications:**
    *   The AI MUST attach design specifications (Performance, Constraints, Tolerances) to the `PART` entity, NEVER to the `PRODUCT` entity.
    *   The AI MUST implement an `ENGINEERING_CHANGE` entity with a many-to-many relationship to both `PART_SPECIFICATION` and `PART_BOM` to accurately track the impact of design changes.
*   **Bill of Materials (BOM) Implementation:**
    *   The AI MUST use a recursive relationship on the `PART` entity to represent the `PART_BOM`.
    *   The AI MUST include a `BOM_TYPE` or sub-typing mechanism to separate the `ENGINEERING_BOM` (ideal blueprint) from the `MANUFACTURING_BOM` (actual factory parts list).
    *   The AI MUST manage marketing bundles via a recursive relationship on the `PRODUCT` entity (e.g., `MARKETING_PACKAGE`), keeping it strictly separate from `PART_BOM`.
*   **Substitutability Rules:**
    *   The AI MUST support two distinct substitution matrices: `PART_SUBSTITUTE` (global replacement, anytime) and `PART_BOM_SUBSTITUTE` (replacement valid only within a specific parent assembly).
*   **Inventory Item Configurations:**
    *   To track field maintenance, the AI MUST implement a recursive `INVENTORY_ITEM_CONFIGURATION` entity between specific `INVENTORY_ITEM` instances (tracking serial numbers).
    *   The AI MUST differentiate between a `MANUFACTURING_CONFIGURATION` (how it left the factory) and a `SERVICE_CONFIGURATION` (how it looks now after field repairs).
*   **Order and MRP Modeling:**
    *   The AI MUST constrain `PURCHASE_ORDER_ITEM`s to reference `PART`s (or occasionally `PRODUCT`s from external suppliers).
    *   The AI MUST constrain `SALES_ORDER_ITEM`s to reference ONLY `PRODUCT`s.
    *   For distribution agreements, the AI MUST support "releases" (orders) applied against an overarching `DISTRIBUTION_AGREEMENT` until the quota is met.
*   **Product Deployment and Usage:**
    *   For field-tracked assets, the AI MUST model `DEPLOYMENT` linking an `INVENTORY_ITEM` to a `FACILITY` and a `PRODUCT`.
    *   If billing or liability is usage-based, the AI MUST track `DEPLOYMENT_USAGE` with appropriate unit-of-measure lookups (Activity, Volume, or Time Period).
    *   The AI MUST explicitly model inventory ownership (e.g., consignment scenarios where the manufacturer stores parts owned by a supplier).
*   **Work Effort (Shop Floor Control):**
    *   The AI MUST model `PROCESS_PLAN` as a hierarchy of `WORK_EFFORT_TYPE`s (standard templates) encompassing `WORK_EFFORT_SKILL_STANDARD`, `PART_STANDARD`, and `FIXED_ASSET_STANDARD`.
    *   The AI MUST model actual shop-floor execution as a hierarchy of `WORK_EFFORT`s (the `PRODUCTION_RUN` subtype), linking to actual `PARTY` assignments, `INVENTORY_ITEM` assignments, and actual `FIXED_ASSET` assignments.
*   **Analytics & Star Schema:**
    *   When designing reporting tables, the AI MUST create a `PRODUCTION_RUN_FACT` table holding measures for standard vs. actual performance (e.g., `cost`, `cost_variance_from_standard`, `duration`, `duration_variance_from_standard`, `quantity_produced`, `quantity_rejected`).

@Workflow
1.  **Party Definition:** Establish the manufacturing roles (`SUPPLIER`, `DISTRIBUTOR`, `END_USER_CUSTOMER`) and structure the organization hierarchies.
2.  **Part & Product Cataloging:** Define the `PART` taxonomy (`RAW_MATERIAL`, `SUBASSEMBLY`, `FINISHED_GOOD`) and map `FINISHED_GOOD`s to their corresponding marketed `PRODUCT`s.
3.  **Engineering Rule Definition:** Define `PART_SPECIFICATION`s and the `ENGINEERING_CHANGE` control process impacting those parts.
4.  **BOM Construction:** Implement recursive relationships for the `ENGINEERING_BOM`, `MANUFACTURING_BOM`, and global/contextual `PART_SUBSTITUTE` matrices. Implement `MARKETING_PACKAGE`s on the Product side.
5.  **MRP & Order Routing:** Architect `PURCHASE_ORDER`s to ingest `PART`s and `SALES_ORDER`s to output `PRODUCT`s.
6.  **Shop Floor Planning & Execution:** Design `PROCESS_PLAN` (standards) and map them to `PRODUCTION_RUN` (actuals), capturing precise labor, materials, and machine usage.
7.  **Field Deployment:** Map the conversion of sold products to field `DEPLOYMENT`s, supporting recursive `INVENTORY_ITEM_CONFIGURATION`s for field service tracking.
8.  **Analytical Schema Generation:** Build Star Schemas targeting production efficiency, comparing standard process plan metrics against actual production run metrics.

@Examples (Do's and Don'ts)

*   **Part vs. Product Separation:**
    *   [DO] Create an entity `PART` (e.g., Part #Extreme_5_PC) and a related entity `PRODUCT` (e.g., Product "Super Extreme 5 PC" for consumers, Product "Business Classic 5" for enterprises).
    *   [DON'T] Add pricing, marketing descriptions, or target demographic attributes to the physical `PART` table.

*   **Bill of Materials (BOM) Modeling:**
    *   [DO] Use a composite primary key for `PART_BOM` that includes `parent_part_id`, `child_part_id`, and `bom_view_type` (Engineering vs. Manufacturing) to allow the same components to be structured differently depending on the department.
    *   [DON'T] Mix a promotional bundle (e.g., PC + Free T-Shirt) into the `PART_BOM`. That must be modeled as a `PRODUCT_ASSOCIATION` subtype `MARKETING_PACKAGE`.

*   **Part Substitution:**
    *   [DO] Create an entity `PART_BOM_SUBSTITUTE` that links a specific `PART_BOM` record to an alternative `PART_BOM` record (e.g., "Memory Stick A can replace Memory Stick B *only* when building Motherboard X").
    *   [DON'T] Rely solely on a global `PART_SUBSTITUTE` table if manufacturing rules dictate that substitutions are strictly context-dependent.

*   **Shop Floor Tracking (Process vs. Actual):**
    *   [DO] Model `WORK_EFFORT_TYPE` to store the *estimated* hours and materials for a routing step, and model `WORK_EFFORT` (Production Run) to store the *actual* start/stop times and actual materials consumed.
    *   [DON'T] Hardcode production steps into the actual production run table; they must reference a master `PROCESS_PLAN` definition.

*   **Inventory Configuration (As-Maintained):**
    *   [DO] Track field repairs by creating a recursive relationship between `INVENTORY_ITEM` instances (e.g., associating specific Serial Number Hard Drive to specific Serial Number PC chassis) with `from_date` and `thru_date` to maintain a history of swapped parts.
    *   [DON'T] Overwrite the original shipping configuration record when a field technician swaps a subassembly; preserve the `MANUFACTURING_CONFIGURATION` and log the update as a new `SERVICE_CONFIGURATION`.