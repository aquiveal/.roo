@Domain
This rule file is triggered when the AI is tasked with designing, analyzing, refactoring, or generating database schemas, entity-relationship diagrams (ERDs), Object-Relational Mapping (ORM) classes, or software architectures related to product catalogs, goods and services, inventory management, product pricing, product costing, product categorization, product features/options, or product-to-product associations (e.g., Bills of Materials, kitting, substitutes).

@Vocabulary
- **PRODUCT**: Something of significance (good or service) that was, is, or will be sold by the enterprise. A marketing offering.
- **GOOD**: A tangible product subtype that is physical in nature.
- **SERVICE**: An intangible product subtype involving the use of parties' time and expertise.
- **PRODUCT CATEGORY**: A grouping mechanism for products used for catalog organization, sales analysis, or listings.
- **PRODUCT CATEGORY ROLLUP**: A recursive entity allowing product categories to be made up of other product categories (hierarchy).
- **MARKET INTEREST**: An intersection entity linking `PARTY TYPE` and `PRODUCT CATEGORY` to track target demographics for marketing.
- **GOOD IDENTIFICATION**: An entity storing standard identification codes (e.g., SKU, UPCA, UPCE, ISBN, Manufacturer ID) rather than storing them as attributes on the good.
- **PRODUCT FEATURE**: A characteristic, option, variation, or modifier of a product (e.g., color, size, quality, software feature).
- **PRODUCT FEATURE APPLICABILITY**: An entity maintaining which products are available with which product features.
- **PRODUCT FEATURE INTERACTION**: An entity defining dependencies or incompatibilities between selected product features.
- **UNIT OF MEASURE CONVERSION**: An associative entity providing a `conversion_factor` to convert different units of measure into a common unit for inventory assessment.
- **SUPPLIER PRODUCT**: An entity showing which products are offered by which organizations (suppliers or manufacturers), including `available_from_date` and `lead_time`.
- **REORDER GUIDELINE**: An entity defining the `reorder_level` and `reorder_quantity` for a good, specific to a geographic boundary or facility.
- **INVENTORY ITEM**: The physical occurrence or stock of a good at a specific location, separate from the catalog definition of the good.
- **SERIALIZED INVENTORY ITEM / NON-SERIALIZED INVENTORY ITEM**: Subtypes of Inventory Item tracking items by specific serial number or by quantity-on-hand, respectively.
- **LOT**: A grouping of inventory items of the same type, generally used to track production runs or shipments for recall purposes.
- **ITEM VARIANCE**: An entity maintaining the history of inventory shrinkage or overages discovered during physical inspections.
- **PRICE COMPONENT**: An abstracted entity handling all pricing aspects (base price, discounts, surcharges), capable of being tied to geographic boundaries, party types, quantity breaks, order values, or sale types.
- **ESTIMATED PRODUCT COST**: An entity tracking the predicted future trends of product costs (materials, labor, manufacturing, overhead) rather than relying solely on historical actuals.
- **PRODUCT ASSOCIATION**: Entities linking products to other products, including `PRODUCT COMPONENT` (BOMs/kits), `PRODUCT SUBSTITUTE`, `PRODUCT OBSOLESCENCE` (superseding), and `PRODUCT COMPLEMENT` (cross-selling).
- **PART**: The actual physical item (Raw Material, Subassembly, Finished Good) used to produce one or more Products (the marketing offering).

@Objectives
- To maintain a holistic, redundancy-free data architecture for product management that accommodates the enterprise's products, suppliers' products, and competitors' products within a unified structure.
- To separate the marketing/catalog definition of a product from its physical inventory occurrences.
- To abstract pricing, product features, and categorizations into independent, date-tracked entities to support high variability without requiring schema modifications.
- To handle complex product relationships, including dynamic kitting, feature incompatibilities, and bill-of-materials, using standardized associative entities.

@Guidelines

**1. Product Definition & Subtyping**
- The AI MUST model an overarching `PRODUCT` entity with `name`, `introduction_date`, `sales_discontinuation_date`, and `support_discontinuation_date`.
- The AI MUST subtype `PRODUCT` into `GOOD` (tangible) and `SERVICE` (intangible).
- The AI MUST NOT treat raw materials, subassemblies, and finished goods as purely marketing `PRODUCT`s if the enterprise manages manufacturing. Instead, use a `PART` entity subtyped into `RAW MATERIAL`, `SUBASSEMBLY`, and `FINISHED GOOD`, and link `FINISHED GOOD` to the marketing `PRODUCT`.

**2. Product Categorization**
- The AI MUST resolve many-to-many relationships between `PRODUCT` and `PRODUCT CATEGORY` via a `PRODUCT CATEGORY CLASSIFICATION` entity utilizing `from_date` and `thru_date`.
- The AI MUST include a `primary_flag` in the classification entity to designate the primary category and avoid duplicate counting in sales analysis queries.
- The AI MUST implement hierarchical categories using a recursive `PRODUCT CATEGORY ROLLUP` entity.

**3. Product Identification Codes**
- The AI MUST NOT add attributes like `sku`, `isbn`, or `upc` directly to the `GOOD` entity.
- The AI MUST abstract these into a `GOOD IDENTIFICATION` entity related to `GOOD`, containing an `id_value` attribute and subtyped by ID type (e.g., SKU, UPCA, ISBN).

**4. Product Features & Variations**
- The AI MUST NOT create separate product records for every possible variation (e.g., a red shirt and a blue shirt).
- The AI MUST define a `PRODUCT FEATURE` entity subtyped into `STANDARD FEATURE`, `REQUIRED FEATURE`, `SELECTABLE FEATURE`, and `OPTIONAL FEATURE`.
- The AI MUST link features to products via `PRODUCT FEATURE APPLICABILITY`.
- The AI MUST enforce feature logic using a `PRODUCT FEATURE INTERACTION` entity subtyped into `SELECTION INTERACTION INCOMPATIBILITY` and `FEATURE INTERACTION DEPENDENCY`.

**5. Inventory & Storage**
- The AI MUST differentiate between a `GOOD` (the catalog item) and an `INVENTORY ITEM` (the physical occurrence of the good at a location).
- The AI MUST subtype `INVENTORY ITEM` into `SERIALIZED INVENTORY ITEM` (tracking a single item via `serial_num`) and `NON-SERIALIZED INVENTORY ITEM` (tracking a group of items via `quantity_on_hand`).
- The AI MUST link `INVENTORY ITEM` to a `FACILITY` or `CONTAINER` using an exclusive arc (it must be located at one or the other, but not both).
- The AI MUST use an `ITEM VARIANCE` entity, linked to a `REASON` look-up, to track historical shrinkage/overages, rather than blindly overwriting the `quantity_on_hand`.

**6. Product Pricing**
- The AI MUST NOT model pricing as a simple `price` attribute on the `PRODUCT` entity.
- The AI MUST use a `PRICE COMPONENT` entity, utilizing `from_date` and `thru_date`.
- The AI MUST subtype `PRICE COMPONENT` into `BASE PRICE`, `DISCOUNT COMPONENT`, `SURCHARGE COMPONENT`, and `MANUFACTURER SUGGESTED PRICE`.
- The AI MUST further subtype `PRICE COMPONENT` to distinguish between `ONE TIME CHARGE`, `RECURRING CHARGE`, and `UTILIZATION CHARGE`.
- The AI MUST allow `PRICE COMPONENT` to be dynamically linked (via optional relationships) to pricing factors: `GEOGRAPHIC BOUNDARY`, `PARTY TYPE`, `PRODUCT CATEGORY`, `QUANTITY BREAK`, `ORDER VALUE`, and `SALE TYPE`.

**7. Product Costing**
- The AI MUST NOT use highly volatile historical actuals to determine standard product costs.
- The AI MUST model an `ESTIMATED PRODUCT COST` entity linked to `COST COMPONENT TYPE` (e.g., Labor, Materials, Overhead).
- The AI MUST allow estimated costs to vary by `GEOGRAPHIC BOUNDARY` and `ORGANIZATION`.

**8. Product Associations & BOMs**
- The AI MUST model product groupings and kits using a `PRODUCT COMPONENT` (or `MARKETING PACKAGE`) associative entity with a `quantity_used` attribute and `from_date`/`thru_date`.
- The AI MUST handle other associations using dedicated entities: `PRODUCT SUBSTITUTE` (with a substitution `quantity`), `PRODUCT OBSOLESCENCE` (superseding products), `PRODUCT COMPLEMENT` (accessories), and `PRODUCT INCOMPATIBILITY`.

@Workflow
1. **Analyze Subject Nature**: Determine if the system handles tangible goods, intangible services, or both. Define the `PRODUCT` supertype accordingly.
2. **Abstract Identifiers**: Extract hardcoded SKUs or UPCs into a `GOOD IDENTIFICATION` structure to support multiple standard codes per product.
3. **Structure Features**: If products have variations (colors, sizes, grades), establish the `PRODUCT FEATURE` and `PRODUCT FEATURE APPLICABILITY` architecture. Include interaction logic if feature combinations are constrained.
4. **Decouple Inventory**: Ensure the physical tracking of goods (`INVENTORY ITEM`, `LOT`, `ITEM VARIANCE`) is entirely separated from the marketing definition (`PRODUCT`).
5. **Architect Pricing**: Implement the `PRICE COMPONENT` pattern. Verify that the system can apply a discount or base price depending on geographic region, quantity break, or party type without altering the database schema.
6. **Define Associations**: Implement recursive or associative entities to handle Bills of Materials, substitutes, and cross-selling capabilities.

@Examples (Do's and Don'ts)

**Principle: Product Pricing Abstraction**
- [DO] Create a `PRICE_COMPONENT` table with columns: `price_component_id`, `product_id`, `price`, `percent`, `from_date`, `thru_date`, `geographic_boundary_id`, `quantity_break_id`, `party_type_id`.
- [DON'T] Add `base_price`, `discount_percentage`, or `hawaii_surcharge_amount` directly as columns to the `PRODUCT` table.

**Principle: Physical Inventory vs. Product Definition**
- [DO] Create a `PRODUCT` table for "10-pound Printer Paper" and a separate `INVENTORY_ITEM` table containing `inventory_item_id`, `product_id`, `facility_id`, `quantity_on_hand`, and `lot_id`.
- [DON'T] Add `quantity_on_hand`, `warehouse_location`, or `lot_number` directly to the `PRODUCT` table.

**Principle: Product Identification**
- [DO] Create a `GOOD_IDENTIFICATION` table with columns `good_id`, `id_type` (e.g., 'ISBN', 'UPCA', 'SKU'), and `id_value`.
- [DON'T] Alter the `PRODUCT` table to include columns like `sku_number`, `isbn_number`, and `upc_code`.

**Principle: Product Categorization**
- [DO] Use a `PRODUCT_CATEGORY_CLASSIFICATION` intersection table with `product_id`, `category_id`, `from_date`, `thru_date`, and `primary_flag`.
- [DON'T] Add `category_1` and `category_2` columns to the `PRODUCT` table.

**Principle: Inventory Shrinkage Tracking**
- [DO] Create an `ITEM_VARIANCE` table logging `inventory_item_id`, `physical_inventory_date`, `quantity_difference`, and `reason_id` to adjust the calculated stock.
- [DON'T] Manually overwrite the `quantity_on_hand` in the database without an audit trail of the discrepancy.