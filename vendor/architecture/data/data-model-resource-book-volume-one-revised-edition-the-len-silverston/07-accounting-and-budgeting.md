@Domain
These rules are activated whenever the AI is tasked with designing, analyzing, refactoring, or generating database schemas, data models, or code related to Accounting, Budgeting, General Ledgers, Financial Transactions, Chart of Accounts, Invoicing impact on accounting, or Financial Resource allocations.

@Vocabulary
- **Chart of Accounts**: The structured list of categories (buckets) an enterprise uses to track its business activity for accounting purposes.
- **GENERAL LEDGER ACCOUNT**: A type of financial reporting bucket to which transactions are posted (e.g., "cash", "supplies expense").
- **GENERAL LEDGER ACCOUNT TYPE**: The classification of a GL account (e.g., Asset, Liability, Owners Equity, Revenue, Expense).
- **ORGANIZATION GL ACCOUNT**: The specific instance of a GL account tied to a specific Internal Organization over a specific time period.
- **ACCOUNTING PERIOD**: The time period (e.g., fiscal year, calendar month) used for financial reporting, marked by `from date` and `thru date`.
- **ACCOUNTING TRANSACTION**: A journal entry representing an event that affects the financial statements. May be Internal (depreciation, amortization) or External (obligations, payments).
- **TRANSACTION DETAIL**: A journal entry line item; represents the specific debit or credit to an Organization GL Account.
- **INTERNAL ACCTG TRANS**: Adjustment transactions affecting only the books of the specific internal organization (e.g., Capitalization, Depreciation).
- **EXTERNAL ACCTG TRANS**: Transactions involving an external party (e.g., Obligation, Payment).
- **OBLIGATION ACCTG TRANS**: An external transaction where a party recognizes it owes money (e.g., Note, Credit Memo, Tax Due, Sales Acctg Trans).
- **PAYMENT ACCTG TRANS**: Collections of moneys received (Receipt) or payments sent (Disbursement).
- **SUBSIDIARY LEDGER**: An account tracking the status of specific parties/products (e.g., Accounts Receivable per customer), modeled as a recursive `ORGANIZATION GL ACCOUNT` mapping.
- **BUDGET**: A mechanism for planning the spending of moneys (Operating Budget or Capital Budget).
- **BUDGET ITEM**: The granular level of a budget detailing exactly what is being budgeted and its amount.
- **BUDGET REVISION IMPACT**: An associative entity resolving the many-to-many relationship between Budget Items and Budget Revisions to track precise changes over time.
- **BUDGET SCENARIO**: Variables (e.g., "best case", "worst case") that apply percentage or amount changes to budget items based on conditional logic.

@Objectives
- Establish robust, historically accurate, and highly flexible accounting and budgeting data structures.
- Ensure strict separation between business transactions (operational) and accounting transactions (financial).
- Enforce standard double-entry accounting principles at the database level.
- Prevent data corruption and system fragility caused by meaningful/intelligent primary keys or poorly structured date periods.
- Accurately track the entire lifecycle of a budget, including granular revisions, multi-party reviews, situational scenarios, and precise payment-to-order allocations.

@Guidelines

**1. Chart of Accounts & General Ledger Rules**
- The AI MUST use non-meaningful, system-generated unique integers for the primary key of `GENERAL LEDGER ACCOUNT`.
- The AI MUST NOT use meaningful or mnemonic keys (e.g., `ABC100-200-A-101`) for GL accounts, as organizational restructuring will break referential integrity.
- The AI MUST map `GENERAL LEDGER ACCOUNT` to `INTERNAL ORGANIZATION` via a many-to-many associative entity (`ORGANIZATION GL ACCOUNT`) that includes a `from date` and `thru date` to track historical chart of accounts changes.
- The AI MUST model `ACCOUNTING PERIOD` using full date domains (`from date` and `thru date`). The AI MUST NOT use partial text-based dates (like `from day` = "Mar 1") to avoid leap year calculation and index conversion errors.
- The AI MUST support subsidiary ledgers by modeling a recursive `comprised of` relationship on `ORGANIZATION GL ACCOUNT` to relate parent accounts (e.g., Accounts Payable) to specific subsidiary accounts (e.g., AP for Supplier X).

**2. Accounting Transactions & Double-Entry Principles**
- The AI MUST model business transactions (e.g., `INVOICE`, `PAYMENT`) and their corresponding accounting transactions (e.g., `SALES ACCTG TRANS`, `PAYMENT ACCTG TRANS`) as completely separate entities connected by a 1-to-1 or 1-to-many relationship. The AI MUST NOT model business transactions as subtypes of accounting transactions due to timing differences (e.g., unposted status).
- The AI MUST break down every `ACCOUNTING TRANSACTION` into one or more `TRANSACTION DETAIL` entities.
- The AI MUST include a `debit/credit flag` and an `amount` attribute in the `TRANSACTION DETAIL` entity. In physical database implementations, the AI MAY implement this as a positive/negative signed amount to facilitate aggregate arithmetic.
- The AI MUST relate every `TRANSACTION DETAIL` to exactly one `ORGANIZATION GL ACCOUNT`.
- The AI MUST include a recursive relationship on `TRANSACTION DETAIL` (e.g., `Associated Transaction ID`) to track which payments paid off which specific invoices, or which credit memos apply to which obligations.

**3. Account Balances (Logical vs. Physical)**
- When designing *Logical Data Models*, the AI MUST NOT model "Account Balance" as an entity or attribute, as it is derived data resulting from summing `TRANSACTION DETAIL` records.
- When designing *Physical Database Designs*, the AI MUST inject an `ORGANIZATION GL ACCOUNT BALANCE` table situated between `TRANSACTION DETAIL` and `ORGANIZATION GL ACCOUNT` to optimize performance for financial reporting.

**4. Budgets and Budget Revisions**
- The AI MUST map `BUDGET` to an `INTERNAL ORGANIZATION` (or party) and a `STANDARD TIME PERIOD`.
- The AI MUST break down budgets into `BUDGET ITEM` records, utilizing a recursive relationship to allow multi-level hierarchical rollups.
- To track budget revisions without duplicating entire budgets, the AI MUST create a `BUDGET REVISION` entity and an associative `BUDGET REVISION IMPACT` entity.
- The `BUDGET REVISION IMPACT` entity MUST contain the `revised amount`, an `add delete flag`, and a `revision reason`, mapping many-to-many between `BUDGET ITEM` and `BUDGET REVISION`.
- The AI MUST relate the `BUDGET REVIEW` (approvals/rejections) directly to the parent `BUDGET` entity, not individually to revisions.

**5. Budget Scenarios & Allocations**
- The AI MUST support `BUDGET SCENARIO` by linking a `BUDGET SCENARIO APPLICATION` to either the `BUDGET` (globally) or `BUDGET ITEM` (locally). This application entity MUST contain either a `percentage change` or an `amount change`.
- The AI MUST map commitments to budgets by relating `ORDER ITEM` directly to `BUDGET ITEM`.
- The AI MUST NOT map disbursements (`PAYMENT`) directly to `BUDGET ITEM` if an order exists. To determine expenditures against commitments, the AI MUST trace the payment through the `INVOICE ITEM` and `SHIPMENT ITEM` back to the `ORDER ITEM`.
- The AI MUST use a `PAYMENT BUDGET ALLOCATION` entity to link payments directly to budgets ONLY when a payment is made without a preceding order (e.g., employee purchasing supplies out-of-pocket).
- The AI MUST map budget classifications to GL accounts using a many-to-many associative entity (`GL BUDGET XREF`) linking `BUDGET ITEM TYPE` to `GENERAL LEDGER ACCOUNT`, including `from date` and `thru date` attributes.

@Workflow
1. **Identify the Scope**: Determine if the request requires modeling the Chart of Accounts, Transaction Logging, or Budgeting/Allocations.
2. **Setup the Chart of Accounts**: Define `INTERNAL ORGANIZATION`, `GENERAL LEDGER ACCOUNT`, and intersect them with `ORGANIZATION GL ACCOUNT`. Enforce non-meaningful IDs and robust `ACCOUNTING PERIOD` definitions.
3. **Model the Transactions**: Define the business transaction, then link it to the `ACCOUNTING TRANSACTION` supertype. Break the accounting transaction into `TRANSACTION DETAIL` records ensuring debit/credit compliance and recursive linking.
4. **Determine Logical vs. Physical**: If producing a physical schema, denormalize by adding `ORGANIZATION GL ACCOUNT BALANCE`. If producing a logical model, omit it.
5. **Setup Budgets**: Create the `BUDGET` and `BUDGET ITEM` hierarchy.
6. **Implement Budget Revisions/Scenarios**: Add `BUDGET REVISION IMPACT` to track granular add/delete/modify changes to budget items. Add `BUDGET SCENARIO APPLICATION` to handle what-if percentage/amount shifts.
7. **Trace Financial Allocations**: Connect `ORDER ITEM` to `BUDGET ITEM` for commitments. Ensure payments trace through invoices to orders, prohibiting direct payment-to-budget mapping unless it's a direct expense.

@Examples

**[DO] - Separating Business and Accounting Transactions**
```sql
CREATE TABLE INVOICE (
    invoice_id INT PRIMARY KEY,
    invoice_date DATE,
    description VARCHAR(255)
);

CREATE TABLE ACCOUNTING_TRANSACTION (
    transaction_id INT PRIMARY KEY,
    transaction_date DATE,
    invoice_id INT NULL, -- Link to business transaction
    transaction_type VARCHAR(50) -- e.g., 'SALES_ACCTG_TRANS'
);
```

**[DON'T] - Merging Business and Accounting Transactions**
```sql
-- ANTI-PATTERN: Modeling the business transaction directly as an accounting subtype
CREATE TABLE INVOICE_ACCOUNTING_TRANS (
    invoice_id INT PRIMARY KEY,
    invoice_status VARCHAR(50),
    debit_account VARCHAR(50),
    credit_account VARCHAR(50)
);
```

**[DO] - Meaningless Keys & Proper Time Periods for GL Accounts**
```sql
CREATE TABLE GENERAL_LEDGER_ACCOUNT (
    gl_account_id INT PRIMARY KEY, -- System generated, meaningless
    account_name VARCHAR(100),
    account_type VARCHAR(50) -- e.g., 'Asset'
);

CREATE TABLE ACCOUNTING_PERIOD (
    period_id INT PRIMARY KEY,
    from_date DATE,
    thru_date DATE
);
```

**[DON'T] - Meaningful Keys & String Dates**
```sql
-- ANTI-PATTERN: Smart keys break when organizations restructure. String periods fail leap years.
CREATE TABLE GENERAL_LEDGER_ACCOUNT (
    gl_account_id VARCHAR(50) PRIMARY KEY, -- e.g., 'ABC100-200-A-101'
    from_day VARCHAR(10), -- e.g., 'Mar 1'
    thru_day VARCHAR(10)  -- e.g., 'Feb 28'
);
```

**[DO] - Tracking Budget Revisions via Impact Entity**
```sql
CREATE TABLE BUDGET_REVISION_IMPACT (
    budget_item_id INT,
    budget_revision_id INT,
    revised_amount DECIMAL(18,2),
    add_delete_flag CHAR(1),
    revision_reason VARCHAR(255),
    PRIMARY KEY (budget_item_id, budget_revision_id)
);
```

**[DON'T] - Duplicating Whole Budgets for Minor Revisions**
```sql
-- ANTI-PATTERN: Cloning the entire budget structure every time one item changes.
CREATE TABLE BUDGET_REVISION (
    budget_revision_id INT PRIMARY KEY,
    parent_budget_id INT,
    full_budget_blob TEXT -- Loss of historical tracking at the item level
);
```