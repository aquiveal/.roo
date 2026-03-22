@Domain
Trigger these rules when designing, modifying, analyzing, or reviewing data models that involve conditional logic, constraints, directives, 'if/then/while' scenarios, pricing algorithms, prioritization, routing logic, formatting guidelines, or any metadata that governs business behavior. These rules apply whenever variable data is influenced by specific conditions or when business rules must be databased rather than hidden in application code.

@Vocabulary
- **Business Rule:** A directive intended to influence or guide business behavior, or a constraint on data beyond the constraints implied by the standard data model.
- **Subject:** The entity or entities that are affected by a rule (e.g., `PRODUCT`, `ORDER`, `EVENT TYPE`).
- **Factor:** A condition, circumstance, or element contributing to a particular result or outcome of a rule.
- **Attribute Factor:** A factor maintained as a simple attribute within the rule entity itself (e.g., `effective from date`, `effective thru date`).
- **Specific Factor:** A factor that relates to a specific, existing entity in the data model (e.g., `GEOGRAPHIC BOUNDARY`, `ROLE TYPE`).
- **Generalized Factor:** A factor not directly tied to an existing entity, captured via flexible associative entities (`RULE FACTOR TYPE` and `ENTITY RULE FACTOR`).
- **Outcome:** The result or action that is supposed to happen when the conditions (factors) of a business rule are met.
- **Attribute Outcome:** An outcome maintained as a simple attribute of the rule entity (e.g., `price amount`, `discount percentage`).
- **Specific Outcome:** An outcome that relates directly to an existing entity in the data model (e.g., triggering a specific `WORK EFFORT TYPE`).
- **Generalized Outcome:** An outcome modeled flexibly using generic rule outcome entities (`RULE OUTCOME TYPE` and `ENTITY RULE OUTCOME`).
- **Rule Manager:** The party responsible for the upkeep of the business rule data.
- **Authorized Rule User:** A party with the rights to use the rule.
- **Rule Specifier:** A party with relevant knowledge who directly specifies the rule.
- **Rule Source:** The definitive originator or supplier of the rule.

@Objectives
- Transform implicit application logic, procedural code, and process models into explicit, data-driven business rule structures.
- Integrate metadata (rules) seamlessly with business data (subjects, specific factors, specific outcomes) to form a unified data model.
- Enable dynamic business environments where changes to pricing, workflows, and constraints can be made by changing data instances rather than modifying application code or database schema.
- Enforce rigorous governance and traceability of business rules by explicitly modeling the parties responsible for sourcing, specifying, and managing them.

@Guidelines

**1. Identification of Business Rules**
- The AI MUST treat the requirement as a Business Rule if it includes conditional statements ('if, then', 'while', 'in case'), pricing variations, prioritization/ranking criteria, supply routing choices, follow-up triggers, or inventory replenishment limits.
- The AI MUST model rules as data (metadata) linked directly to the business data entities they govern.

**2. Core Components of a Rule Pattern**
- Every business rule implementation MUST capture three fundamental components: 
  1. Core Rule Data (Rule statement, name, classification).
  2. Factors (The conditions affecting the rule).
  3. Outcomes (The results of the rule).

**3. Level 2 Business Rules Pattern (Domain-Specific)**
- Use this pattern when modeling rules for a specific situation, problem area, or business subject area (e.g., `PRICE COMPONENT RULE`, `EVENT TYPE RULE`).
- The AI MUST create an `[ENTITY] RULE` entity (e.g., `PRICE COMPONENT RULE`).
- The AI MUST link the `[ENTITY] RULE` to its Subject(s) via a 1:M relationship (e.g., a `PRODUCT` may be priced by one or more `PRICE COMPONENT RULE`s).
- The AI MUST classify the rule using an `[ENTITY] RULE TYPE` entity with a recursive relationship to allow rule type rollups.
- The AI MUST map Specific Factors using optional foreign keys to existing entities (e.g., linking `PRICE COMPONENT RULE` to `GEOGRAPHIC BOUNDARY`).
- The AI MUST map Generalized Factors using `[ENTITY] RULE FACTOR`, `RULE FACTOR TYPE`, `RULE FACTOR VALUE`, and `FACTOR VALUE TYPE`.
- The AI MUST map Specific Outcomes by linking the rule entity to the target outcome entity.
- The AI MUST map Generalized Outcomes using `[ENTITY] RULE OUTCOME`, `RULE OUTCOME TYPE`, `RULE OUTCOME VALUE`, and `OUTCOME VALUE TYPE`.

**4. Level 3 Business Rules Pattern (Enterprise-Wide Generalized)**
- Use this pattern when an enterprise requires a unified, highly flexible data model to capture many types of business rules across domains.
- The AI MUST create a generalized `BUSINESS RULE` supertype entity to hold common attributes (`rule name`, `rule statement`).
- The AI MUST create specific subtypes of `BUSINESS RULE` (e.g., `PRICE COMPONENT RULE`, `EVENT TYPE RULE`) to hold links to specific Subjects, Specific Factors, and Specific Outcomes.
- The AI MUST link the `BUSINESS RULE` supertype to `BUSINESS RULE FACTOR` (for generalized factors) and `BUSINESS RULE OUTCOME` (for generalized outcomes).
- The AI MUST use the Level 3 Classification Pattern (`BUSINESS RULE CATEGORY CLASSIFICATION`, `BUSINESS RULE CATEGORY`, `BUSINESS RULE CATEGORY TYPE`) to allow rules to be classified in multiple, intersecting ways.

**5. Factor Modeling Rules**
- The AI MUST NOT duplicate existing business data to create a factor. If a factor is an existing concept (like Customer Size or Geographic Boundary), it MUST be modeled as a Specific Factor relationship.
- The AI MUST use Attribute Factors only for single, atomic data points standard to rule execution (e.g., `effective from date`, `effective thru date`).
- The AI MUST use Generalized Factors for derived data, ranges, or parameters not stored elsewhere in the core data model (e.g., "Number of years as a customer", "Average payment history range").

**6. Outcome Modeling Rules**
- The AI MUST use Attribute Outcomes for atomic, non-repeating results intrinsic to the rule subtype (e.g., `price amount`, `discount percentage`).
- The AI MUST use Specific Outcomes if the result is triggering an existing system concept (e.g., initiating an `Audit project` inside `WORK EFFORT TYPE`).
- The AI MUST use Generalized Outcomes to allow flexible, multi-value results (e.g., Rule Outcome = "Gift", Outcome Value = "2", Outcome Value Type = "Pen Sets").

**7. Business Rule Governance (Party Roles)**
- The AI MUST support rule traceability using the Contextual Roles Pattern.
- Create a `BUSINESS RULE ROLE` associative entity linking `BUSINESS RULE`, `PARTY`, and `ROLE TYPE`.
- Ensure standard `ROLE TYPE` instances are supported: "Rule manager", "Authorized rule user", "Rule specifier", and "Rule source".
- Allow rules to have multiple sources or historical sources by maintaining this as a M:M associative relationship.

**8. Supplementary Rule Attributes**
- The AI SHOULD include optional attributes in the Rule entity for rigorous documentation: `rule note` (explanatory comments), `rule reference` (quoted authority), `rule source`, `rule specified by`, `rule managed by`, and `external reference id` (link to external rules engine).

@Workflow
1. **Identify the Rule Trigger:** Detect language in the requirements indicating constraints, conditional execution ('if X then Y'), prioritization, or variable pricing.
2. **Define the Subject(s):** Determine which core business entity or entities are affected by this rule (e.g., `ORDER`, `PRODUCT`, `CUSTOMER`).
3. **Analyze and Categorize Factors:**
   - Check if the condition relies on existing data entities -> Model as a *Specific Factor* relationship.
   - Check if the condition is a basic validity span -> Model as an *Attribute Factor* (e.g., `effective thru date`).
   - Check if the condition is derived or external -> Model as a *Generalized Factor* (`RULE FACTOR TYPE`).
4. **Analyze and Categorize Outcomes:**
   - Check if the result is a simple, non-repeating value -> Model as an *Attribute Outcome* (e.g., `surcharge amount`).
   - Check if the result triggers a known entity state -> Model as a *Specific Outcome*.
   - Check if the result is variable/complex -> Model as a *Generalized Outcome* (`RULE OUTCOME TYPE`).
5. **Select Pattern Level:**
   - Apply Level 2 if modeling a specific, localized application domain (e.g., only modeling pricing).
   - Apply Level 3 if designing an enterprise architecture, MDM, or rules-engine schema requiring a unified `BUSINESS RULE` supertype.
6. **Apply the Pattern:** Draft the entities, attributes, and relationships. Ensure associative entities are used where a rule involves M:M specific factors or outcomes (e.g., a rule applying to multiple `ROLE TYPE`s).
7. **Incorporate Governance:** Add the `BUSINESS RULE ROLE` intersection to link `PARTY` entities to the rules for sourcing, management, and specification.

@Examples (Do's and Don'ts)

**Pricing Logic Modeling**
- [DO] Model pricing via a `PRICE COMPONENT RULE` entity that links to a `PRODUCT` (Subject), `GEOGRAPHIC BOUNDARY` (Specific Factor), and has a `discount percentage` (Attribute Outcome).
- [DON'T] Add `US_Price`, `UK_Price`, and `Partner_Discount` as static attributes directly on the `PRODUCT` entity. 

**Factor Categorization**
- [DO] Use existing entities. If a rule condition depends on the communication method, link the rule directly to `COMMUNICATION EVENT TYPE` as a Specific Factor.
- [DON'T] Create a new generalized `RULE FACTOR TYPE` with a value of "Phone Call" if a `COMMUNICATION EVENT TYPE` entity already exists in the enterprise data model.

**Rule Centralization (Level 3)**
- [DO] Create a `BUSINESS RULE` supertype with subtypes `EVENT TYPE RULE` and `PRICE COMPONENT RULE`. Link `BUSINESS RULE FACTOR` to the supertype so generalized factors are consistently handled across all rule types.
- [DON'T] Create separate `EVENT TYPE RULE FACTOR` and `PRICE COMPONENT RULE FACTOR` entities if the goal is an enterprise-wide Level 3 integration.

**Rule Governance**
- [DO] Use a `BUSINESS RULE ROLE` associative entity to link the Supreme Court (Party) as the "Rule manager" (Role Type) to a specific Constitutional Law (Business Rule).
- [DON'T] Use basic text attributes like `managed_by_name` on the rule entity, as it prevents tracking the party robustly across the enterprise model.

**Outcome Multiplicity**
- [DO] Use Generalized Outcomes (`BUSINESS RULE OUTCOME`, `RULE OUTCOME VALUE`) when a single rule can result in multiple actions (e.g., Outcome 1: "Apology", Outcome 2: "Coupon", Value: "$50").
- [DON'T] Hardcode `apology_indicator` and `coupon_amount` as attributes on an `EVENT TYPE RULE` if outcome types are expected to expand or change over time.