@Domain
Data modeling, database design, software architecture, and data warehousing specifically tailored for the Financial Services industry. This includes banks, credit unions, lending organizations, brokerage services, securities firms, and insurance companies handling financial assets. These rules are activated when requested to design, refactor, or analyze schemas, systems, or queries related to account management, financial product definition, risk analysis, lending, investments, or financial transaction tracking.

@Vocabulary
- **Financial Institution**: An organization providing financial services, functioning as an internal or external party role.
- **Controlling Syndicator**: The lead financial institution in a syndicated loan that manages the primary relationship and distributes risk.
- **Participating Syndicator**: A partnering financial institution that assumes a portion of the risk in a syndicated loan.
- **Worker**: A supertype role encompassing both Employees and Contractors.
- **Plan**: A financial course of action mapped to a customer's specific needs and objectives, fulfilling them via targeted financial products.
- **Financial Product**: A highly customizable, intangible service offering (not a manufactured good) defined by its features and settings.
- **Product Category**: Broad classifications of financial products including Investment Vehicle, Deposit Product, Loan Product, and Lease.
- **Functional Setting**: The driver or parameter that controls how a Financial Product or Product Feature operates (e.g., "Apply fee when account balance goes below zero").
- **Financial Regulation**: Rules imposed either externally (Government Regulation) or internally (Organization Regulation) that govern product behavior and availability.
- **Financial Agreement**: The formalized commitment between the customer and institution. Subtypes include Loan Agreement, Investment Agreement, and Leasing Agreement.
- **Asset Role / Agreement Asset Usage**: The mechanism linking a party's tangible or intangible asset (e.g., home equity) as collateral or security to a financial agreement.
- **Account**: The delivery mechanism that monitors and tracks all activity/transactions resulting from the use of a financial product.
- **Party Account Media**: The physical or digital medium used to access an account (e.g., ATM card, paper checks, software login).
- **Account Transaction**: Actions against an account, divided into Financial Transactions (monetary) and Account Request Transactions (non-monetary inquiries/changes).
- **Account Transaction Task**: Automated tasks (Post, Authorize, Pre-determined) that generate transactions on a scheduled or requested basis.
- **Account Notification**: Work efforts designated to communicate with the customer, categorized into Invoicing, Statement, Marketing, and Alert tasks.
- **Risk Analysis**: A specific analytical work effort evaluating potential loss within a credit or investment exposure, resulting in an Analysis Outcome (score).
- **Market Segment**: A group of selected accounts or parties with similar demographic or behavioral characteristics used for targeted analysis or marketing.

@Objectives
- Model highly flexible and fluid financial services products that can be customized dynamically via features and functional settings.
- Accurately map customer needs and long-term objectives to financial plans and specific investment or lending products.
- Design robust, relationship-driven Account and Account Transaction structures capable of tracking complex multi-account interactions (e.g., sweeps, overdrafts, reversals).
- Ensure strict compliance representation by mapping Financial Regulations and Product Rules directly to product features.
- Support comprehensive risk assessment workflows, securely tracking analysis parameters, actuarial scoring, and credit worthiness.
- Establish dimensional data warehouse star schemas that aggregate account profitability and transaction volume across facilities, organizations, and market segments.

@Guidelines
- **Party and Role Architecture**:
  - Differentiate Customer roles explicitly into INVESTOR or LOAN CUSTOMER based on whether they provide capital or borrow capital.
  - Implement a WORKER supertype to aggregate EMPLOYEE and CONTRACTOR roles.
  - Always track REGULATORY AGENCY roles to govern compliance.
  - For large risk distributions, model CONTROLLING SYNDICATOR and PARTICIPATING SYNDICATOR relationships.
- **Objectives, Needs, and Plans**:
  - Do not link products directly to abstract needs. Route PARTY NEED and PARTY OBJECTIVE (Investment/Lending) to a formal PLAN entity.
  - Link the PLAN to the FINANCIAL PRODUCT(s) chosen to satisfy the customer's scored objectives.
- **Financial Product Configuration**:
  - Separate PRODUCT CATEGORY (Deposit, Loan, Investment, Lease) from the specific FINANCIAL PRODUCT.
  - Connect FINANCIAL PRODUCT to PRODUCT FEATURE.
  - MUST map a FUNCTIONAL SETTING to either the PRODUCT FEATURE or the FINANCIAL PRODUCT to define operational behavior (e.g., renewal terms, fee application conditions).
- **Regulation and Compliance**:
  - Model FINANCIAL REGULATION with subtypes GOVERNMENT REGULATION and ORGANIZATION REGULATION.
  - Apply REGULATION REQUIREMENT instances as FINANCIAL PRODUCT RULEs that restrict or enforce combinations of products, features, and settings.
- **Financial Agreements and Assets**:
  - Use specific FINANCIAL AGREEMENT subtypes: LOAN AGREEMENT, INVESTMENT AGREEMENT, LEASING AGREEMENT.
  - Bind an ASSET (Fixed or Intangible) to the agreement using AGREEMENT ASSET USAGE (e.g., indicating its use as collateral).
  - Define ASSET ROLEs to ensure the party has the legal authority and sufficient equity to pledge the asset.
- **Account Delivery Modeling**:
  - Create the ACCOUNT entity as the primary delivery mechanism of the product.
  - Relate ACCOUNT to FINANCIAL PRODUCT via an ACCOUNT PRODUCT intersection entity that includes `from_date` and `thru_date` to support product migration over time without losing account history.
  - Map PARTY to ACCOUNT ROLE using strict roles (Owner, Joint Owner, Approved User, Guarantor).
  - Define PARTY ACCOUNT MEDIA to track access mechanisms and track the MEDIA STATUS (Active, Inactive, Lost).
- **Transaction Processing**:
  - Differentiate ACCOUNT TRANSACTION into FINANCIAL TRANSACTION (Deposit, Withdrawal, Interest, Dividend) and ACCOUNT REQUEST TRANSACTION (Inquiry, Change Request).
  - Mandate ACCOUNT TRANSACTION STATUS tracking (e.g., Posted, Completed, Hold, Reversed).
  - Utilize ACCOUNT TRANSACTION RELATIONSHIP to link dependent transactions (e.g., an overdraft withdrawal linked to a credit card advance, or a deposit linked to a swept account).
  - Model ACCOUNT TRANSACTION TASK to handle scheduled automation (Pre-determined frequency sweeps).
- **Work Efforts and Notifications**:
  - Categorize ACCOUNT NOTIFICATION into INVOICING TASK, STATEMENT TASK, MARKETING TASK, and ALERT TASK (fraud/error warnings).
- **Risk Analysis Architecture**:
  - Map the RISK ANALYSIS work effort to an ANALYSIS OUTCOME using weighted ANALYSIS PARAMETERs.
  - Point the outcome to a PARTY TARGET (behavior/credit score), ACCOUNT TARGET (account performance score), or MARKET SEGMENT (group score).
- **Data Warehousing (Star Schemas)**:
  - *Account Star Schema*: Track `number_of_accounts`, `average_balance`, `average_return`, and `number_of_transactions`. Map dimensions to FACILITYS, INTERNAL_ORGANIZATIONS, FINANCIAL_PRODUCTS, OWNERS, ACCOUNT_MANAGERS, MARKET_SEGMENTS, and TIME_BY_WEEK.
  - *Transaction Star Schema*: Track `number_of_transactions` and `total_transaction_amount`. Map dimensions to ACCOUNT_TRANSACTION_TYPES and TIME_BY_DAY for granular behavioral analysis.

@Workflow
1. **Party Identification**: Model the involved Parties, Roles, and Relationships. Distinctly classify Investors, Loan Customers, Syndicators, and Regulatory Agencies.
2. **Needs Assessment**: Map the Party Needs and Objectives (scored by priority) to Financial Plans.
3. **Product Definition**: Define the Financial Products by associating them with Product Categories, Product Features, and controlling Functional Settings.
4. **Regulatory Constraints**: Apply internal and external Financial Regulations and Product Rules to restrict or enforce allowable product configurations.
5. **Agreement Formalization**: Model the Financial Agreements. Specify ASSET bindings (collateral/equity usage) and assign specific Agreement Roles (Owner, Co-signer).
6. **Account Instantiation**: Construct the Account Delivery structures. Link the Account to the Agreement, the applicable Financial Product(s) (with effective dates), and provision the Party Account Media (cards/checks).
7. **Transaction Mapping**: Detail the Account Transaction structures. Categorize monetary vs. non-monetary types, configure automated Transaction Tasks, establish strict statuses, and map Transaction Relationships (e.g., reversals, sweeps).
8. **Work Effort & Risk Management**: Define associated Work Efforts encompassing routine Account Notifications (statements, invoices, fraud alerts) and formal Risk Analysis tasks (credit scoring, market segmentation).
9. **Analytics Schema Generation**: Design the Data Warehouse Star Schemas to aggregate Account profitability and trace Transaction-level behavioral volumes.

@Examples (Do's and Don'ts)
- **Party Modeling**
  - [DO]: Sub-type the CUSTOMER role into INVESTOR and LOAN CUSTOMER to explicitly define their capital relationship with the institution.
  - [DON'T]: Use a generic CUSTOMER role without differentiating whether the party is borrowing money or providing investment capital.

- **Product Rules and Configuration**
  - [DO]: Define operational behaviors using a FUNCTIONAL SETTING linked to a PRODUCT FEATURE (e.g., Feature: "Overdraft Fee", Setting: "Apply fee when balance < $0").
  - [DON'T]: Hardcode behavioral conditions or fee structures directly into a flat product table.

- **Agreements and Collateral**
  - [DO]: Link a specific ASSET (e.g., "2000 Mustang GT") to a LOAN AGREEMENT using the AGREEMENT ASSET USAGE entity to clearly define it as collateral.
  - [DON'T]: Attach collateral data directly to the customer profile outside the strict boundaries of an active Financial Agreement.

- **Transaction Tracking**
  - [DO]: Link an overdraft deposit to the triggering withdrawal using an ACCOUNT TRANSACTION RELATIONSHIP to maintain a precise audit trail.
  - [DON'T]: Record standalone, orphaned deposits or reversals without tracing them back to the specific transaction that generated them.

- **Risk Assessment**
  - [DO]: Generate an ANALYSIS OUTCOME from a formal RISK ANALYSIS work effort, targeting a specific PARTY TARGET with a calculated behavior/credit score.
  - [DON'T]: Manually overwrite a user's credit rating directly on their Party profile without an auditable, timestamped Analysis Task linking the parameters evaluated.