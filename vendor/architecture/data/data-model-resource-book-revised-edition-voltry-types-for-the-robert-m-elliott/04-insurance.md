@Domain
Trigger these rules when tasked with designing, analyzing, or implementing data models, database schemas, or data warehouse designs (star schemas) for insurance enterprises. This includes domains such as insurance providers (underwriters), insurance agencies, brokerages, third-party administrators, underwriting systems, premium rating and scheduling systems, and claims processing and settlement systems.

@Vocabulary
- **INSURANCE PROVIDER**: The organization that underwrites the insurance products and assumes the risk.
- **INSURANCE AGENCY / BROKER**: Distribution channels that sell and service insurance products. Agencies typically represent one provider; brokers represent multiple.
- **INSURED PARTY**: The person or organization covered by the insurance policy (subtyped into INSURED ORGANIZATION and INSURED INDIVIDUAL, which includes INSURED CONTRACT HOLDER and INSURED DEPENDENT).
- **BENEFICIARY**: The recipient of the claims settlement amounts in the event of the insured party's loss of life or health.
- **FINANCIALLY RESPONSIBLE PARTY**: The party responsible for the financial obligations (premiums, fees) of the insurance policy.
- **INSURANCE ADMINISTRATOR**: A third party that handles administrative functions for the underwriting company.
- **INSURANCE PRODUCT**: A service offered to protect against a loss. It is defined by combinations of COVERAGE TYPEs, COVERAGE LEVELs, and PRODUCT FEATUREs.
- **COVERAGE TYPE**: The specific risk protected by the product (e.g., bodily injury, collision, major medical, dental).
- **COVERAGE LEVEL**: The degree of protection offered, subtyped into COVERAGE AMOUNT, COVERAGE RANGE, DEDUCTIBILITY, COPAY, and COINSURANCE.
- **PRODUCT RULE**: Business or regulatory conditions that govern how products, coverage types, or features operate.
- **COMMUNITY-BASED RATING**: Rating applied to a wide group of insured parties with similar risks using standardized INSURANCE RATE tables.
- **EXPERIENCE-BASED RATING**: Specialized premium rating calculated on a case-by-case basis using RISK ANALYSIS and ACTUARIAL ANALYSIS.
- **INSURANCE APPLICATION / QUOTE**: The pre-agreement stages gathering risk factors to estimate or request premium costs.
- **INSURANCE POLICY**: A subtype of AGREEMENT representing the finalized contract of coverages, features, and costs.
- **POLICY ITEM**: An individual aspect of coverage within an INSURANCE POLICY (e.g., Property, Casualty, Life, Health, Disability).
- **PREMIUM SCHEDULE**: The billing cycle determining when premiums are due, broken down into POLICY ITEM PREMIUMs.
- **INCIDENT**: An event (e.g., car accident, property theft) causing damage or loss that may or may not result in a claim.
- **CLAIM**: A formal request for reimbursement for a loss submitted under an INSURANCE POLICY, composed of CLAIM ITEMs.
- **CLAIM SETTLEMENT**: The process of applying ADJUDICATION RULEs to a CLAIM ITEM to determine the CLAIM PAYMENT AMOUNT, DEDUCTIBLE AMOUNT, and DISALLOWED AMOUNT.

@Objectives
- Architect highly flexible insurance product models capable of defining services via granular coverage types, levels, and features rather than rigid physical goods.
- Separate the modeling of community-based rating (actuarial rate tables) from experience-based rating (custom risk analysis).
- Establish a seamless, traceable data flow from pre-agreement (Application and Quote) to contract (Insurance Policy/Agreement) to billing (Premium Schedule) to loss events (Incidents and Claims).
- Construct precise data warehouse star schemas that allow the enterprise to analyze claims payouts against risk models to ensure profitability and adequate claim reserves.

@Guidelines
- **Party and Role Modeling**:
  - You MUST utilize specific insurance party roles: DEPENDENT, CLAIMS ADJUSTER, INSURANCE AGENT, INSURANCE PROVIDER, DISTRIBUTION CHANNEL, REGULATORY AGENCY, TRUSTEE, BENEFICIARY, INSURED PARTY, and INSURANCE ADMINISTRATOR.
  - You MUST create specific PARTY RELATIONSHIPs: INSURED PARTY TO AGENT, INSURANCE AGENT TO PROVIDER, INSURED PARTY TO INS PROV, and DISTRIBUTION CHANNEL RELATIONSHIP.
- **Product Modeling**:
  - You MUST NOT model insurance products as simple inventory items. You MUST model an INSURANCE PRODUCT as a collection of COVERAGE AVAILABILITY records.
  - You MUST define COVERAGE AVAILABILITY as the intersection of COVERAGE TYPEs and COVERAGE LEVELs.
  - You MUST categorize COVERAGE LEVELs into DEDUCTIBILITY, COPAY, COINSURANCE, COVERAGE AMOUNT, or COVERAGE RANGE.
  - You MUST apply FUNCTIONAL SETTINGs and PRODUCT FEATUREs to product categories or individual products to handle variations (e.g., "Exclude flood damage").
  - You MUST implement FINANCIAL REGULATIONs and PRODUCT RULEs that dictate what features or coverages can legally or operationally be combined.
- **Rating and Underwriting Modeling**:
  - You MUST initiate rating via a RISK ANALYSIS work effort, which generates one or more ACTUARIAL ANALYSIS records based on ANALYSIS PARAMETERs.
  - For community-based rating, you MUST map ACTUARIAL ANALYSIS to INSURANCE RATE tables (filtered by GEOGRAPHIC BOUNDARY, RISK LEVEL TYPE, etc.).
  - For experience-based rating, you MUST map ACTUARIAL ANALYSIS directly to a POLICY ITEM PREMIUM.
- **Orders (Policies and Agreements) Modeling**:
  - You MUST model the purchasing of insurance as an INSURANCE POLICY, which is a subtype of AGREEMENT (NOT a standard Sales Order).
  - You MUST structure the pre-policy phases using INSURANCE APPLICATION and QUOTE entities. QUOTE ITEMs MUST link to estimated COVERAGE TYPEs, COVERAGE LEVELs, and INSURED ASSETs.
  - You MUST subtype INSURANCE POLICY into specific lines: HEALTH CARE POLICY, LIFE INSURANCE POLICY, CASUALTY INSURANCE POLICY, PROPERTY INSURANCE POLICY, and DISABILITY INSURANCE POLICY.
  - For Property and Casualty, you MUST link the POLICY ITEM to an INSURED ASSET.
  - For Life Insurance, you MUST specify a BENEFICIARY using an AGREEMENT ROLE.
  - For Health Insurance, you MUST model GROUP INSURANCE POLICYs containing ENROLLMENTs, which in turn contain ENROLLMENT ELECTIONs and COVERED INDIVIDUALs.
- **Premium Scheduling and Invoicing Modeling**:
  - You MUST generate a PREMIUM SCHEDULE from the INSURANCE POLICY.
  - The PREMIUM SCHEDULE MUST consist of POLICY ITEM PREMIUMs (the specific cost for each coverage aspect).
  - You MUST link POLICY ITEM PREMIUMs to INVOICE ITEMs via a POLICY ITEM PREMIUM BILLING associative entity to track actual amounts billed versus scheduled amounts.
- **Incidents and Claims Modeling**:
  - You MUST record loss events as an INCIDENT (e.g., MOTOR VEHICLE ACCIDENT, PROPERTY LOSS).
  - You MUST allow an INCIDENT to exist *without* a corresponding CLAIM (e.g., an incident reported by police but not claimed by the insured).
  - You MUST model CLAIMs with CLAIM ITEMs. CLAIM ITEMs MUST link to the INCIDENT and the INSURED ASSET (or HEALTH CARE DELIVERY for health claims).
  - You MUST settle claims using a CLAIM SETTLEMENT entity governed by ADJUDICATION RULEs (Eligibility, Audit, Pricing).
  - The CLAIM SETTLEMENT AMOUNT MUST be broken down into CLAIM PAYMENT AMOUNT, DEDUCTIBLE AMOUNT, USUAL AND CUSTOMARY AMOUNT, and DISALLOWED AMOUNT.
  - You MUST generate a REMITTANCE NOTICE and an EXPLANATION OF BENEFIT TYPE upon payment.
- **Star Schema Design (Claims Analysis)**:
  - You MUST use a CLAIM FACT table containing the measures: `claim_item_requested_amount`, `claim_payment_amount`, and `estimated_cost`.
  - You MUST link the CLAIM FACT table to the following dimensions: `TIME_BY_DAY`, `PARTY_TYPES` (insured party types), `GEOGRAPHIC_BOUNDARYS`, `RISK_LEVEL_TYPES`, `INSURED_ASSET_TYPES`, `INSURANCE_PRODUCTS`, and `COVERAGE_TYPES` (with a hierarchy up to `COVERAGE_LEVELS`).

@Workflow
1. **Define the Parties and Roles**: Instantiate the insurance providers, agents, regulatory agencies, and insured parties using the specialized insurance role subtypes. Set up their relationships (e.g., Agent to Provider).
2. **Construct the Insurance Product**: Define the base INSURANCE PRODUCT. Attach available COVERAGE TYPEs (e.g., collision, major medical) and COVERAGE LEVELs (e.g., $500 deductible, 80% coinsurance). Apply PRODUCT FEATUREs and constrain them using PRODUCT RULEs.
3. **Establish Pricing/Rating Rules**: Design the RISK ANALYSIS process. For standardized products, generate the INSURANCE RATE tables mapping risk factors (age, geographic boundary) to base premiums. For custom risks, set up the direct experience-based ACTUARIAL ANALYSIS paths.
4. **Model the Lifecycle of the Policy**: 
    - Create the INSURANCE APPLICATION.
    - Generate a QUOTE mapping risk parameters to proposed premiums.
    - Finalize the AGREEMENT as an INSURANCE POLICY, breaking it down into specific POLICY ITEMs (Property, Life, Health, etc.). Link required assets or beneficiaries.
5. **Schedule and Bill Premiums**: Create the PREMIUM SCHEDULE for the policy. Generate POLICY ITEM PREMIUMs and map them to INVOICE ITEMs for monthly/quarterly billing.
6. **Process Loss Events (Incidents & Claims)**: 
    - Record INCIDENTs independently.
    - If a claim is filed, create a CLAIM with CLAIM ITEMs linked to the INCIDENT and the INSURED ASSET.
    - Execute CLAIM SETTLEMENT applying ADJUDICATION RULEs to calculate payouts, deductibles, and disallowed amounts. Issue REMITTANCE NOTICEs.
7. **Design Analytics**: Create the Claim Star Schema to feed settlement data back into the underwriting process, measuring payouts against the assigned `RISK_LEVEL_TYPES`.

@Examples (Do's and Don'ts)

- [DO] Model insurance products as a matrix of coverages.
  ```sql
  CREATE TABLE INSURANCE_PRODUCT (product_id INT PRIMARY KEY, name VARCHAR);
  CREATE TABLE COVERAGE_TYPE (coverage_type_id INT PRIMARY KEY, description VARCHAR);
  CREATE TABLE COVERAGE_LEVEL (coverage_level_id INT PRIMARY KEY, amount DECIMAL, level_type VARCHAR);
  CREATE TABLE COVERAGE_AVAILABILITY (
      product_id INT,
      coverage_type_id INT,
      coverage_level_id INT,
      availability_type VARCHAR, -- e.g., 'Required', 'Optional', 'Standard'
      PRIMARY KEY (product_id, coverage_type_id, coverage_level_id)
  );
  ```

- [DON'T] Model an insurance policy as a standard sales order selling an inventory item.
  ```sql
  -- INCORRECT: Treats a policy like a shipped physical good
  CREATE TABLE SALES_ORDER (order_id INT, item_id INT, qty INT, shipping_date DATE);
  ```

- [DO] Separate Incidents from Claims to track risk factors accurately.
  ```sql
  CREATE TABLE INCIDENT (incident_id INT PRIMARY KEY, incident_type VARCHAR, date DATE);
  CREATE TABLE CLAIM (claim_id INT PRIMARY KEY, policy_id INT);
  CREATE TABLE CLAIM_ITEM (
      claim_item_id INT PRIMARY KEY, 
      claim_id INT, 
      incident_id INT, -- Maps the claim to the real-world event
      requested_amount DECIMAL
  );
  ```

- [DON'T] Lump all claim amounts into a single payout field without tracking adjudication.
  ```sql
  -- INCORRECT: Fails to track why amounts were paid or denied
  CREATE TABLE CLAIM (claim_id INT, total_paid DECIMAL);
  ```

- [DO] Break down claim settlements using Adjudication Rules.
  ```sql
  CREATE TABLE CLAIM_SETTLEMENT (settlement_id INT PRIMARY KEY, claim_item_id INT);
  CREATE TABLE CLAIM_SETTLEMENT_AMOUNT (
      amount_id INT PRIMARY KEY,
      settlement_id INT,
      amount DECIMAL,
      amount_type VARCHAR, -- e.g., 'Deductible', 'Disallowed', 'Payment'
      explanation_of_benefit_type VARCHAR
  );
  ```

- [DO] Model the Claims Star Schema with specific insurance dimensions.
  ```sql
  CREATE TABLE CLAIM_FACT (
      time_id INT,
      geographic_boundary_id INT,
      risk_level_type_id INT,
      insured_asset_type_id INT,
      insurance_product_id INT,
      coverage_type_id INT,
      claim_item_requested_amount DECIMAL,
      claim_payment_amount DECIMAL,
      estimated_cost DECIMAL
  );
  ```