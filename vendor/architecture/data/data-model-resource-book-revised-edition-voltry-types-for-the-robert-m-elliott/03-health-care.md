# @Domain
Database design, data modeling, and information architecture specifically tailored for Health Care enterprises. This includes hospitals, institutions, medical offices, ambulatory surgery facilities, alternative medicine providers, vision specialists, dentists, and any other enterprise providing treatment for illnesses or injuries. Activate these rules when a user requests data models, database schemas, or system architectures related to patient tracking, clinical workflows, health care billing, claims processing, or clinical outcome analysis.

# @Vocabulary
*   **Individual Health Care Practitioner:** A person who delivers health care treatment (e.g., physicians, chiropractors, nurses, physical therapists).
*   **Patient:** A person scheduled for or receiving health care treatments.
*   **Health Care Provider Organization:** Any organization providing health care, subtyped into Institution (hospitals), Health Care Practice (doctor's offices), or Other.
*   **Network:** A collection of Health Care Provider Organizations linked together to provide services under guidelines usually established by an insurance company.
*   **Group:** A collection of individuals classified within an organization (usually an Employer) to receive insurance coverage.
*   **Third Party Administrator (TPA):** An organization hired to handle the administration of a health care policy, enrollments, and claims (often for self-insured employers).
*   **Insurance Provider:** The organization taking the risk of the health care insurance.
*   **Payor:** The organization that actually pays the claims (could be the Insurance Provider or a TPA).
*   **Health Care Association:** An organization supporting or providing guidelines within the industry (e.g., AMA).
*   **Insured Contract Holder:** The principal person covered under an insurance policy.
*   **Insured Dependent:** A person covered for a policy in addition to the contract holder (spouse, child).
*   **Practice Affiliation:** A relationship identifying which Individual Health Care Practitioners are associated with which Health Care Provider Organizations.
*   **Health Care Offering:** Services or items a provider delivers to patients. Subtyped into Health Care Service Offering (procedures, general services) and Health Care Good Offering (tangible items).
*   **Procedure Offering:** Types of standard health care treatments practitioners offer.
*   **Durable Medical Equipment (DME) Offering:** A subtype of Health Care Good Offering for medical equipment.
*   **Incident:** A specific event (e.g., car accident, epidemic) that may require health care.
*   **Health Care Episode:** A specific health care injury, disease, or ailment tracked over time. One Incident can lead to multiple Episodes.
*   **Health Care Visit:** An appointment or encounter scheduled for a Visit Reason (which may be tied to a Symptom or an Episode).
*   **Health Care Delivery:** Specific treatments or actions performed during a visit (Examination, Procedure Delivery, Drug Administration, Supply Administration, DME Delivery).
*   **Certification Requirement:** Mandatory approvals (e.g., from an insurance company) required before a specific Health Care Delivery can be administered.
*   **Claim:** A request for reimbursement for health care deliveries, subtyped into Institutional, Medical, Dental, and Home Care claims.
*   **Claim Service Code:** Industry-standard codes applied to Claim Items (e.g., CPT, HCPCS, REV).
*   **Diagnosis Type:** Standard codes classifying patient conditions (e.g., ICD9, ICD10).
*   **DRG (Diagnostic Related Groups):** A classification of procedures and diagnoses to facilitate payments.
*   **Claim Settlement Amount:** The breakdown of how a claim was settled, including Deductible Amount, Usual and Customary Amount, Disallowed Amount, and Claim Payment Amount.

# @Objectives
*   Design holistic, integrated health care systems that eliminate redundant data entry and maintain accurate patient, practitioner, and facility profiles.
*   Structure clinical data hierarchically to accurately track the cause and lifecycle of patient care: Incident -> Episode -> Visit -> Delivery.
*   Distinguish clearly between billable Health Care Offerings (procedures, goods) and medical Diagnoses (which justify the procedures but are not directly charged).
*   Model health care claims as an extension of standard invoicing, incorporating industry-specific requirements like Service Codes, Diagnosis Codes, and Coordination of Benefits (many-to-many relationships between deliveries and claim items).
*   Support clinical quality tracking by modeling Health Care Delivery Outcomes and Episode Outcomes independently from financial metrics.

# @Guidelines
*   **Party and Role Modeling:** The AI MUST categorize parties using specific health care roles. People must be modeled as Patients, Individual Health Care Practitioners, Employees, etc. Organizations must be modeled as Health Care Provider Organizations, Networks, Employers, TPAs, Insurance Providers, or Payors.
*   **Patient Demographics and Health Info:** The AI MUST model Medical Conditions and Physical Characteristics as entities associated directly with the Patient to ensure practitioners have the necessary context for treatment.
*   **Facility Hierarchy:** The AI MUST model health care facilities with hierarchical capabilities, allowing scheduling and tracking at granular levels (e.g., Building -> Floor -> Room -> Bed).
*   **Health Care Offerings vs. Diagnoses:** The AI MUST explicitly separate Health Care Offerings (services and goods that are billed) from Diagnoses (medical opinions justifying the service). Diagnoses MUST NOT be modeled as subtypes of Health Care Offerings.
*   **Agreements and Orders:** The AI MUST model "Orders" in a health care context as Appointments, Patient Provider Agreements, Provider Network Agreements, and Insurance Policies.
*   **Clinical Workflow Structure:** The AI MUST enforce the clinical tracking hierarchy:
    1.  `Incident` (Optional: e.g., a car crash).
    2.  `Health Care Episode` (The resulting conditions: e.g., a broken leg and a concussion).
    3.  `Health Care Visit` (The encounter to address the episode).
    4.  `Health Care Delivery` (The specific procedures, drugs, or equipment administered during the visit).
*   **Claims Modeling:** The AI MUST model Claims identically in function to Invoices but utilizing health-specific entities.
    *   A `Claim Item` MUST have a many-to-many relationship with `Health Care Delivery` (to handle combined deliveries on one claim or resubmissions for the same delivery).
    *   `Claim Item` MUST link to `Claim Service Code` (CPT/HCPCS) and `Claim Item Diagnosis Code` (ICD9/ICD10).
*   **Payment and Settlement Modeling:** The AI MUST break down payments using `Claim Settlement Amount` to capture the nuances of health care billing, explicitly modeling `Deductible Amount`, `Usual and Customary Amount`, `Disallowed Amount`, and `Claim Payment Amount`.
*   **Referral Tracking:** The AI MUST distinguish between a `Practitioner Referring Relationship` (a standard, ongoing recommendation rule between doctors) and a `Health Care Referral` (an actual, timestamped event referring a specific patient for a specific episode/diagnosis).
*   **Analytical Star Schemas:** The AI MUST provide Data Mart/Star Schema designs focused on `Episode Outcome Analysis` (measuring the clinical success of treatments) rather than purely financial analysis.

# @Workflow
1.  **Party and Provider Setup:** Define the data structures for Patients, Individual Health Care Practitioners, and Health Care Provider Organizations. Establish the associative entities linking them (e.g., Practice Affiliation, Patient Practitioner Relationship).
2.  **Facility and Contact Definition:** Set up the physical location hierarchies (Hospitals, Clinics, Rooms) and relate them to the Provider Organizations.
3.  **Offerings Catalog Creation:** Define the Health Care Offerings, explicitly categorizing them into Service Offerings (Procedures) and Good Offerings (Pharmaceuticals, DME). Link these to standard pricing components.
4.  **Clinical Encounter Modeling:** Create the tables/entities for Incidents, Episodes, Visits, and Symptoms.
5.  **Care Delivery and Diagnosis:** Model the Health Care Delivery entity. Link Deliveries to the specific Health Care Offerings provided. Establish the Diagnosis entity and link the Deliveries administered to treat that specific Diagnosis. Track Delivery and Episode Outcomes.
6.  **Agreements and Policies:** Define the structural agreements, specifically Insurance Policies (Group vs. Individual), Enrollments, and Enrollment Elections mapping to Coverage Types and Levels.
7.  **Claims Generation Pipeline:** Design the Claims submission schema. Map Health Care Deliveries to Claim Items. Attach required Claim Service Codes and Diagnosis Types to the Claim Items. Ensure Certification Requirements are verified.
8.  **Settlement and Payment:** Model the Claim Settlement process. Break down the settled amounts into deductibles, disallowed amounts, and actual payments, associating them with an Explanation of Benefit Type.
9.  **Reporting/Analysis Layer:** Construct a Star Schema centering on a `Health Care Episode Fact` table, surrounded by dimensions like `Outcome Types`, `Episode Types`, `Diagnosis Types`, `Practitioners`, and `Patient Types`.

# @Examples (Do's and Don'ts)

*   **Clinical Hierarchy**
    *   [DO]: Map a "Car Accident" as an `Incident` that generates two `Health Care Episodes` ("Fractured Arm" and "Concussion"). Create a `Health Care Visit` linked to the "Fractured Arm" episode, containing `Health Care Deliveries` like "X-Ray" (Procedure) and "Cast" (Supply).
    *   [DON'T]: Merge Incidents and Episodes into a single "Medical Event" table that loses the causality and long-term tracking of the individual injuries.

*   **Offerings vs. Diagnoses**
    *   [DO]: Define "Emergency Room Exam" as a `Procedure Offering` and "Simple fracture of the fibula" as a `Diagnosis` linked to the exam delivery.
    *   [DON'T]: Add "Simple fracture of the fibula" into the `Health Care Offering` or `Product` table as a billable item.

*   **Claims to Delivery Mapping**
    *   [DO]: Establish a many-to-many relationship (`Health Care Delivery Claim Submission`) between `Health Care Delivery` and `Claim Item`. This allows a single drug administration to be billed across primary and secondary insurance policies, or resubmitted if denied.
    *   [DON'T]: Use a strict one-to-one relationship making the `Claim Item ID` a foreign key directly on the `Health Care Delivery` row.

*   **Referrals**
    *   [DO]: Create a `Practitioner Referring Relationship` to record that Dr. A generally refers heart patients to Dr. B. Create a separate `Health Care Referral` entity to record that Dr. A referred Patient X to Dr. B on October 12th for a specific episode.
    *   [DON'T]: Overload a single "Referrals" table to handle both the business rules/preferences of doctors and the actual transactional patient referrals.

*   **Payment Settlement**
    *   [DO]: Break a $500 claim item settlement into a $50 `Deductible Amount`, $50 `Disallowed Amount`, and $400 `Claim Payment Amount`, linking an `Explanation of Benefit Type` to the disallowed amount.
    *   [DON'T]: Just record "$400 Paid" without capturing the structured financial breakdown of why the remaining $100 was not covered by the Payor.