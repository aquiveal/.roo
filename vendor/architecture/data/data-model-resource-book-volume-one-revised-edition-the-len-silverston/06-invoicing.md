@Domain
Trigger these rules when the user requests database design, data modeling, schema creation, software architecture, or SQL generation related to billing, invoicing, payments, financial account transactions, accounts receivable/payable, or tracking the financial resolution of orders, shipments, and work efforts.

@Vocabulary
*   **INVOICE**: A transaction record representing a request for payment, containing header information (date, message, description).
*   **INVOICE ITEM**: The granular line items making up an invoice. Represents products, features, work efforts, time entries, or adjustments (taxes, fees) that are being charged.
*   **INVOICE ITEM TYPE**: A classification for an invoice item (e.g., invoice adjustment, product item, feature item).
*   **BILLING ACCOUNT**: A mechanism for grouping different types of items on different invoices for a single party (e.g., separate accounts for telephone vs. dedicated lines).
*   **INVOICE ROLE**: The specific involvement of a party in an invoice (e.g., billed to, billed from, entered by, sender).
*   **INVOICE STATUS**: The state of an invoice at a specific point in time (e.g., sent, void, approved).
*   **INVOICE TERM**: Conditions of business associated with an invoice or a specific invoice item (e.g., net 30, non-refundable).
*   **SHIPMENT ITEM BILLING / ORDER ITEM BILLING / WORK EFFORT BILLING**: Associative entities resolving the many-to-many relationships between the source transaction and the resulting invoice items.
*   **PAYMENT**: A transfer of money, subtyped as RECEIPT (incoming) or DISBURSEMENT (outgoing).
*   **PAYMENT APPLICATION**: The allocation of a PAYMENT to a specific INVOICE, INVOICE ITEM, or BILLING ACCOUNT.
*   **FINANCIAL ACCOUNT TRANSACTION**: A transaction (DEPOSIT or WITHDRAWAL) that affects a FINANCIAL ACCOUNT (Bank Account, Investment Account) and groups individual receipts or disbursements.

@Objectives
*   Establish a highly flexible, normalized invoicing data architecture that integrates seamlessly with orders, shipments, and human resources/work efforts.
*   Ensure absolute financial auditability by strictly prohibiting the overwriting of historical data (e.g., using recursive adjusting invoice items instead of modifying original quantities).
*   Eliminate redundant or derived data at the schema level (e.g., calculating extended prices or inferring "Paid" status dynamically rather than storing them as static fields).
*   Decouple billing structures from rigid party definitions to support complex multi-organization routing, third-party payers, and flexible contact mechanisms.

@Guidelines
*   **Core Invoice Structure**: The AI MUST separate invoicing into `INVOICE` (header) and `INVOICE ITEM` (detail) entities. 
*   **Invoice Adjustments**: The AI MUST NOT create separate adjustment entities parallel to invoice items. Adjustments (sales tax, shipping and handling, discounts, fees) MUST be modeled as `INVOICE ITEM` instances with an `INVOICE ITEM TYPE` of "adjustment".
*   **Derived Data Prohibition**: The AI MUST NOT include an `extended_price` or `total_amount` attribute in the `INVOICE ITEM` schema. The AI MUST derive this value programmatically via `quantity * amount`.
*   **Invoice Correction Protocol**: The AI MUST NOT modify or overwrite the `quantity` or `amount` of an existing `INVOICE ITEM` if a mistake was made. The AI MUST implement a recursive relationship on `INVOICE ITEM` allowing a new `INVOICE ITEM` (with a negative quantity/amount) to adjust the original item.
*   **Product Features**: When a product feature incurs a charge, the AI MUST model the feature as its own `INVOICE ITEM` recursively linked to the primary product's `INVOICE ITEM` (a "sold with" relationship), rather than squashing feature data into the product line item.
*   **Paid Status Prohibition**: The AI MUST NOT include "Paid" as a valid `INVOICE STATUS TYPE`. The AI MUST derive the "Paid" state dynamically by summing `PAYMENT APPLICATION` amounts against the invoice total. Valid statuses are limited to workflow states (e.g., generated, approved, sent, void).
*   **Invoice Roles & Routing**: The AI MUST link invoices to `CONTACT MECHANISM` entities (e.g., Postal Address, Electronic Address, Telecom Number) for both "billed to" and "billed from" routing. The AI MUST NOT hardcode address strings directly onto the invoice table.
*   **Billing Accounts**: If the enterprise groups charges, the AI MUST implement a `BILLING ACCOUNT` entity. An `INVOICE` MUST relate to either a `PARTY` (directly) or a `BILLING ACCOUNT` (mutually exclusive arc).
*   **Source Transaction Mapping**:
    *   **Shipments**: The AI MUST use a many-to-many associative entity (`SHIPMENT ITEM BILLING`) between `SHIPMENT ITEM` and `INVOICE ITEM`. This entity usually does NOT need a quantity attribute unless partial invoicing of shipped items is a strict business requirement.
    *   **Orders**: The AI MUST use `ORDER ITEM BILLING` when billing occurs directly from orders (bypassing shipments/work). This entity MUST include `amount` and `quantity` attributes to track partial billing against an order commitment.
    *   **Work Efforts/Time**: The AI MUST use `WORK EFFORT BILLING` and `TIME ENTRY BILLING` associative entities to link services to invoice items. `WORK EFFORT BILLING` MUST include a `percentage` attribute to support progress payments (e.g., 30% billed on start).
*   **Payment Application**: The AI MUST resolve payments using a `PAYMENT APPLICATION` entity. The AI MUST map `PAYMENT APPLICATION` either to an `INVOICE` (for standard B2B/B2C billing) or directly to an `INVOICE ITEM` (for highly granular financial domains like banking/loans where payments apply to fees vs. interest vs. principal). Payments applied without an invoice MUST map to a `BILLING ACCOUNT` ("on account" payments).
*   **Financial Account Linking**: The AI MUST group `RECEIPT`s (incoming payments) into a `DEPOSIT` transaction, and map `DISBURSEMENT`s (outgoing payments) to a `WITHDRAWAL` transaction. Both must link to a `FINANCIAL ACCOUNT`.

@Workflow
1.  **Define Core Invoice and Items**: Scaffold the `INVOICE` and `INVOICE ITEM` tables. Add a self-referencing foreign key on `INVOICE ITEM` to support feature bundling and post-issuance adjustments.
2.  **Establish Billing Targets**: Implement mutually exclusive foreign keys on `INVOICE` linking to either `PARTY` (or specific roles like `BILL TO CUSTOMER`) or `BILLING ACCOUNT`. 
3.  **Map Contact Mechanisms**: Add foreign keys on `INVOICE` for `sent_from_contact_mechanism_id` and `addressed_to_contact_mechanism_id`.
4.  **Define Status and Terms**: Create `INVOICE STATUS` (linked to lookup types) and `INVOICE TERM` tables mapping to `INVOICE` and `INVOICE ITEM`.
5.  **Connect Source Transactions**: Generate associative entities (`SHIPMENT ITEM BILLING`, `ORDER ITEM BILLING`, `WORK EFFORT BILLING`, `TIME ENTRY BILLING`) linking operational domains to `INVOICE ITEM`.
6.  **Build Payment Architecture**: Create `PAYMENT` (with subclasses Receipt/Disbursement) and `PAYMENT APPLICATION` to map payments to `INVOICE`s or `BILLING ACCOUNT`s.
7.  **Map to Financial Ledgers**: Connect `PAYMENT` to `FINANCIAL ACCOUNT TRANSACTION` (Deposit/Withdrawal), terminating at `FINANCIAL ACCOUNT`.

@Examples (Do's and Don'ts)

**Principle: Invoice Item Corrections**
*   [DON'T] Create an `UPDATE` statement that changes the `quantity` of an already issued invoice item because the customer returned a damaged good.
    ```sql
    -- ANTI-PATTERN: Overwriting historical financial data
    UPDATE invoice_item SET quantity = 8 WHERE invoice_item_id = 101; 
    ```
*   [DO] Create a new adjustment `INVOICE ITEM` with a negative quantity, linked to the original item via a recursive relationship.
    ```sql
    -- CORRECT: Audit-safe financial adjustment
    INSERT INTO invoice_item (invoice_id, invoice_item_type, quantity, amount, adjusted_invoice_item_id)
    VALUES (500, 'item_adjustment', -2, 50.00, 101);
    ```

**Principle: Adjustments as Items**
*   [DON'T] Add structural columns to the `INVOICE` table for standard adjustments.
    ```sql
    -- ANTI-PATTERN: Hardcoded adjustment columns
    CREATE TABLE invoice (
        id INT PRIMARY KEY,
        tax_amount DECIMAL,
        shipping_amount DECIMAL,
        discount_amount DECIMAL
    );
    ```
*   [DO] Treat all adjustments as `INVOICE ITEM` records categorized by type.
    ```sql
    -- CORRECT: Flexible item-based adjustments
    INSERT INTO invoice_item (invoice_id, invoice_item_type, amount) 
    VALUES (500, 'sales_tax', 14.50);
    INSERT INTO invoice_item (invoice_id, invoice_item_type, amount) 
    VALUES (500, 'shipping_and_handling', 25.00);
    ```

**Principle: Determining "Paid" Status**
*   [DON'T] Include 'Paid' as a selectable status in the `INVOICE STATUS` table.
    ```sql
    -- ANTI-PATTERN: Storing derived state
    INSERT INTO invoice_status (invoice_id, status_type) VALUES (500, 'PAID');
    ```
*   [DO] Calculate paid status dynamically by comparing the invoice total against the sum of `PAYMENT APPLICATION` records.
    ```sql
    -- CORRECT: Derived payment status
    SELECT i.invoice_id,
      SUM(ii.quantity * ii.amount) as total_billed,
      COALESCE(SUM(pa.amount_applied), 0) as total_paid,
      CASE WHEN COALESCE(SUM(pa.amount_applied), 0) >= SUM(ii.quantity * ii.amount) 
           THEN 'Paid' ELSE 'Open' END as calculated_status
    FROM invoice i
    JOIN invoice_item ii ON i.invoice_id = ii.invoice_id
    LEFT JOIN payment_application pa ON i.invoice_id = pa.invoice_id
    GROUP BY i.invoice_id;
    ```

**Principle: Billing Order Items (Progress/Partial Billing)**
*   [DON'T] Link `ORDER ITEM` to `INVOICE ITEM` without tracking the specific amount billed in that instance.
    ```sql
    -- ANTI-PATTERN: Missing allocation amount in associative entity
    CREATE TABLE order_item_billing (
        order_item_id INT,
        invoice_item_id INT
    );
    ```
*   [DO] Include `amount` and `quantity` in the associative entity to track how much of the order commitment has been invoiced.
    ```sql
    -- CORRECT: Tracking partial order fulfillment billing
    CREATE TABLE order_item_billing (
        order_item_id INT,
        invoice_item_id INT,
        amount DECIMAL,
        quantity DECIMAL,
        PRIMARY KEY (order_item_id, invoice_item_id)
    );
    ```