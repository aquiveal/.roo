@Domain
Data modeling, database design, system architecture, and application logic generation for Human Resources (HR) systems, including personnel management, organizational structures, position tracking, compensation, benefits, payroll, and recruitment.

@Vocabulary
*   **EMP DEPT Model**: A simplistic, inadequate standard HR data model showing employees directly reporting to employees and belonging directly to departments. The AI MUST NOT use this model.
*   **EMPLOYMENT**: A specific subtype of `PARTY RELATIONSHIP` representing the relationship between the `EMPLOYEE` (a `PARTY ROLE`) and an `INTERNAL ORGANIZATION`.
*   **POSITION**: A specific job slot or Full-Time Equivalent (FTE) within an enterprise that exists independently of the person filling it.
*   **POSITION TYPE**: A classification of common characteristics, standard titles, and descriptions shared by multiple specific positions (e.g., "Business Analyst").
*   **POSITION FULFILLMENT**: An associative entity resolving the many-to-many relationship between a `PERSON` and a `POSITION`, supporting historical tracking and job-sharing.
*   **POSITION REPORTING STRUCTURE**: A recursive entity linking a `POSITION` to another `POSITION` to establish organizational hierarchy, rather than linking people to people.
*   **POSITION TYPE CLASS**: An intersection entity between `POSITION TYPE` and `POSITION CLASSIFICATION TYPE` used to categorize positions (e.g., exempt, non-exempt, salaried, hourly).
*   **PAY GRADE & SALARY STEP**: Highly structured pay schedules where grades are tied to position types, and steps define specific salary amounts.
*   **PAY HISTORY**: An entity tracking the actual salary or pay rate of an individual over time, strictly related to the `EMPLOYMENT` relationship, NOT the position or person.
*   **PARTY BENEFIT**: An entity tracking benefits (e.g., insurance, vacation) associated with a specific `EMPLOYMENT` relationship.
*   **PAYROLL PREFERENCE**: Rules defining how an employee's pay is distributed (e.g., split between checking/savings via electronic deposit) and standard ongoing deductions.
*   **PAYCHECK**: A subtype of `DISBURSEMENT` representing the actual gross payment transaction before deductions.
*   **DEDUCTION**: Specific amounts subtracted from a `PAYCHECK` to calculate net pay, categorized by a `DEDUCTION TYPE`.
*   **TERMINATION TYPE / REASON**: Classifications detailing the end of an `EMPLOYMENT` relationship (e.g., resignation, firing) and the specific cause.

@Objectives
*   Design fully integrated HR data models that eliminate the inflexibility of simplistic EMP-DEPT structures.
*   Maintain a strict conceptual separation between the Person (who they are), the Position (the job slot/FTE), and the Employment (the legal/business relationship).
*   Preserve exhaustive historical accuracy using `from_date` and `thru_date` attributes on all assignments, reporting structures, and compensation records.
*   Support complex organizational realities such as job-sharing (multiple people in one position), matrix reporting (one position reporting to multiple positions), and varying compensation for people in the exact same position type.

@Guidelines

*   **Replacing the EMP DEPT Model**: 
    *   The AI MUST NEVER model a direct recursive "reports-to" relationship between `EMPLOYEE` and `MANAGER` entities. 
    *   The AI MUST NEVER model a direct assignment of an `EMPLOYEE` to a `DEPARTMENT`.

*   **Employment Relationship**:
    *   The AI MUST model `EMPLOYMENT` as a subtype of `PARTY RELATIONSHIP`.
    *   `EMPLOYMENT` MUST link the `PARTY ROLE` of `EMPLOYEE` to the `PARTY ROLE` of `INTERNAL ORGANIZATION`.
    *   All employment statuses (e.g., active, inactive, terminated) MUST be maintained on the `EMPLOYMENT` relationship via `PARTY RELATIONSHIP STATUS TYPE`, not on the `PERSON` entity.

*   **Position Definition**:
    *   The AI MUST model `POSITION` to represent a single Full-Time Equivalent (FTE) job slot.
    *   `POSITION` MUST include attributes for planning and status: `estimated_from_date`, `estimated_thru_date`, `actual_from_date`, `actual_thru_date`, `salary_flag`, `exempt_flag`, `full_time_flag`, and `temporary_flag`.
    *   Positions MUST be authorized or funded via an optional relationship to `BUDGET ITEM`.
    *   `POSITION` MUST be related to a `POSITION TYPE` to inherit standard titles, descriptions, and benefit percentages.
    *   `POSITION` MUST be related to the `ORGANIZATION` acting as the hiring company.

*   **Responsibilities**:
    *   The AI MUST model `VALID RESPONSIBILITY` tied to `POSITION TYPE` (what a type of job *can* do) and `POSITION RESPONSIBILITY` tied to `POSITION` (what a specific job slot *actually* does).
    *   Both responsibility entities MUST include `from_date` and `thru_date`.

*   **Position Fulfillment & Job Sharing**:
    *   The AI MUST map people to positions using the `POSITION FULFILLMENT` associative entity.
    *   The primary key of `POSITION FULFILLMENT` MUST be a compound key consisting of `position_id`, `party_id` (from `PERSON`), and `from_date`. This specific key structure explicitly permits job-sharing (multiple people occupying the same position simultaneously).

*   **Position Reporting Structure**:
    *   The AI MUST model organizational hierarchy using the `POSITION REPORTING STRUCTURE` entity linking `POSITION` to `POSITION`.
    *   This entity MUST include `from_date`, `thru_date`, and a `primary_flag`. The `primary_flag` MUST be used to support matrix reporting (indicating the primary supervisor when a position reports to multiple positions).

*   **Salary and Compensation**:
    *   *Standard Rates*: The AI MUST model acceptable salary ranges via `POSITION TYPE RATE` linked to `POSITION TYPE`, optionally using `PAY GRADE` and `SALARY STEP` for structured government/union scales.
    *   *Actual Pay*: The AI MUST model actual employee compensation using `PAY HISTORY`.
    *   `PAY HISTORY` MUST be related to the `EMPLOYMENT` relationship, NEVER to the `POSITION` (since job-sharers may earn different amounts) and NEVER directly to `PERSON` (since a person may have multiple employments).

*   **Benefits**:
    *   The AI MUST model benefits using `PARTY BENEFIT` linked to `EMPLOYMENT`, NOT to `PERSON` (to handle multi-company benefits without duplication/coordination errors).
    *   `PARTY BENEFIT` MUST include `from_date`, `thru_date`, `actual_employer_paid_percent`, `available_time` (for leave balances), and actual `cost`.

*   **Payroll**:
    *   The AI MUST model payroll disbursements using the `PAYCHECK` subtype of `PAYMENT`.
    *   The AI MUST use `PAYROLL PREFERENCE` (linked to `EMPLOYEE` and `INTERNAL ORGANIZATION`) to define how net pay is distributed (e.g., `PAYMENT METHOD TYPE`, percentages/flat amounts, routing numbers, account numbers).
    *   The AI MUST model subtractions from gross pay using `DEDUCTION` (linked to `PAYCHECK` and `DEDUCTION TYPE`). Net pay is a derived calculation: `PAYCHECK.amount` minus sum of `DEDUCTION.amount`.

*   **Recruitment/Applications**:
    *   The AI MUST model `EMPLOYMENT APPLICATION` originating from a `PERSON` (candidate) and optionally from a referring `PERSON`.
    *   `EMPLOYMENT APPLICATION` MUST optionally relate to a specific `POSITION` and include an `EMPLOYMENT APPLICATION STATUS TYPE` and `EMPLOYMENT APPLICATION SOURCE TYPE`.

*   **Skills, Qualifications, and Performance**:
    *   The AI MUST link `PARTY SKILL`, `PARTY QUALIFICATION`, and `RESUME` to `PARTY` (since organizations can also have skills/qualifications).
    *   The AI MUST link `PERSON TRAINING` specifically to `PERSON`.
    *   The AI MUST model `EMPLOYEE PERFORMANCE REVIEW` linking the receiving `EMPLOYEE` to the reviewing `MANAGER`, containing `PERFORMANCE REVIEW ITEM`s with ratings and comments.

*   **Termination**:
    *   The AI MUST model termination as an event updating the `thru_date` and `PARTY RELATIONSHIP STATUS TYPE` of the `EMPLOYMENT` entity.
    *   The AI MUST relate `TERMINATION TYPE` and `TERMINATION REASON` to the ended `EMPLOYMENT`.
    *   The AI MUST track post-employment claims via an `UNEMPLOYMENT CLAIM` entity related to the terminated `EMPLOYMENT`.

@Workflow
1.  **Define Structural Context**: Establish `PERSON` and `INTERNAL ORGANIZATION` parties.
2.  **Define the Hierarchy Blueprint**: Create `POSITION TYPE` records, associate them with `VALID RESPONSIBILITY` records, and link them to `POSITION TYPE CLASS` categorizations.
3.  **Create Job Slots**: Instantiate `POSITION` records (the FTEs), linked to an authorizing `BUDGET ITEM` and the hiring `ORGANIZATION`.
4.  **Establish Reporting Lines**: Link `POSITION` records to other `POSITION` records using `POSITION REPORTING STRUCTURE`, applying `from_date` and `primary_flag`.
5.  **Create Employment Relationships**: Instantiate `EMPLOYMENT` (subtype of `PARTY RELATIONSHIP`) linking an `EMPLOYEE` role to an `INTERNAL ORGANIZATION` role.
6.  **Fulfill Positions**: Assign the `PERSON` to the `POSITION` via `POSITION FULFILLMENT`, specifying `from_date` to maintain history.
7.  **Define Compensation & Benefits**: Attach `PAY HISTORY` and `PARTY BENEFIT` records to the `EMPLOYMENT` relationship.
8.  **Setup Payroll**: Establish `PAYROLL PREFERENCE` rules for the `EMPLOYEE`, enabling the future generation of `PAYCHECK` and `DEDUCTION` records.
9.  **Manage Lifecycles**: Process `EMPLOYMENT APPLICATION`s, execute `EMPLOYEE PERFORMANCE REVIEW`s, and when necessary, update the `EMPLOYMENT` relationship with `TERMINATION TYPE` and `TERMINATION REASON`.

@Examples (Do's and Don'ts)

*   **Reporting Structures**
    *   [DO]: Relate a `POSITION` to another `POSITION` via `POSITION REPORTING STRUCTURE`. (e.g., "Programmer/Analyst Position #101" reports to "IS Development Manager Position #50" from 2021-01-01 to blank).
    *   [DON'T]: Relate an `EMPLOYEE` directly to a `MANAGER` via a recursive foreign key on an employee table. (This destroys history when the manager gets promoted).

*   **Position Fulfillment & Job Sharing**
    *   [DO]: Use a `POSITION FULFILLMENT` intersection table with a compound primary key (`position_id`, `party_id`, `from_date`) to map people to job slots.
    *   [DON'T]: Add a `person_id` or `employee_id` directly as a foreign key on the `POSITION` table. (This prevents job-sharing and historical tracking).

*   **Actual Salary Tracking**
    *   [DO]: Link the `PAY HISTORY` entity directly to the `EMPLOYMENT` (Party Relationship) entity.
    *   [DON'T]: Link actual salary to the `POSITION` entity (two people sharing a job might earn different rates) or the `PERSON` entity (a person might have multiple concurrent jobs).

*   **Termination**
    *   [DO]: Terminate the employment by setting a `thru_date` on the `EMPLOYMENT` relationship, changing the `PARTY RELATIONSHIP STATUS TYPE` to "terminated", and appending a `TERMINATION REASON`.
    *   [DON'T]: Add an `is_terminated` flag or a `status` of "resigned" directly on the `PERSON` or `EMPLOYEE` entity. (The person hasn't terminated; the legal relationship of employment has).