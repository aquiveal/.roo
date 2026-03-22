@Domain
These rules MUST trigger when the AI is requested to design, review, or generate database schemas, data models, or queries related to work management, project management, manufacturing/production runs, maintenance tracking, time tracking, asset assignment, professional services, or human resource task allocation.

@Vocabulary
- **Work Requirement:** A distinct entity representing an internal or customer need to perform work (e.g., a need for a production run, an asset repair, or an internal project).
- **Requirement Type:** Categorization of the work requirement (e.g., "project," "maintenance," "production run").
- **Anticipated Demand:** A specific requirement type representing forecasted demand; applicable ONLY to goods/inventory, NEVER to services.
- **Work Order Item:** An entity representing a formal commitment to perform work, distinct from a requirement.
- **Work Effort:** The actual execution or fulfillment of a Work Requirement or Work Order Item.
- **Work Effort Type:** The hierarchical classification of an effort (e.g., "Program," "Project," "Phase," "Activity," "Task").
- **Work Effort Purpose Type:** The functional categorization of an effort (e.g., "Maintenance," "Production Run," "Work Flow," "Research").
- **Work Effort Association:** A recursive relationship mapping work efforts to other work efforts to represent hierarchical breakdowns.
- **Work Effort Dependency:** A recursive relationship mapping the execution order of work efforts (e.g., Precedency, Concurrency).
- **Work Effort Party Assignment:** The allocation of a `PARTY` (person or organization) to a `WORK_EFFORT` for a specific `WORK_EFFORT_ROLE_TYPE` over a defined time period.
- **Party Skill / Skill Type:** Entities used to define the qualifications of a party to assist in work effort scheduling.
- **Time Entry:** A record of time spent, explicitly linked to a `TIMESHEET` (belonging to a worker) and a `WORK_EFFORT`.
- **Rate Type:** A classification of financial cost/billing (e.g., "billing rate," "regular pay," "overtime rate") applied to parties, positions, or specific assignments.
- **Fixed Asset:** Property, vehicles, or equipment required to complete a work effort.
- **Work Effort Standards:** Baseline planning metrics attached to a `WORK_EFFORT_TYPE` that estimate required skills, goods, and fixed assets.

@Objectives
- Ensure strict architectural separation between the *need* for work (`WORK_REQUIREMENT`), the *commitment* to do work (`WORK_ORDER_ITEM`), and the *execution* of work (`WORK_EFFORT`).
- Enforce recursive, dynamic hierarchical structures for breaking down work efforts, strictly prohibiting flat or separate task entities.
- Implement highly normalized resource tracking (labor, inventory, equipment) with robust historical tracking using date ranges (`from_date`, `thru_date`).
- Establish a flexible, multi-tiered rate and costing structure capable of calculating billing and payroll independently based on Party, Position, or specific Assignment.
- Differentiate between standard planning estimates (Standards) and actual execution (Assignments and Results).

@Guidelines
- **Separation of Requirement, Order, and Effort:** The AI MUST model `WORK_REQUIREMENT`, `WORK_ORDER_ITEM`, and `WORK_EFFORT` as distinct entities. The AI MUST link them using associative entities (e.g., `WORK_REQUIREMENT_FULFILLMENT` or `WORK_ORDER_ITEM_FULFILLMENT`).
- **Anticipated Demand Constraints:** When modeling anticipated or forecasted demand, the AI MUST restrict this logic to tangible inventory items. The AI MUST NOT generate structures that pre-fabricate services based on anticipated demand.
- **Work Effort Hierarchies:** The AI MUST use a recursive relationship (many-to-many associative entity `WORK_EFFORT_ASSOCIATION`) to break down projects into phases, activities, and tasks. The AI MUST NOT create separate entities like `PROJECT`, `PHASE`, or `TASK`.
- **Work Effort Dependencies:** The AI MUST use a recursive `WORK_EFFORT_DEPENDENCY` entity to handle task sequencing (Precedency/Concurrency).
- **Party Assignments:** The AI MUST link resources to work efforts using `WORK_EFFORT_PARTY_ASSIGNMENT`. This entity MUST include a composite key containing `work_effort_id`, `party_id`, `role_type_id`, and `from_date` to support job sharing and role changes over time.
- **Facility and Location Assignment:** The AI MUST allow a `WORK_EFFORT_PARTY_ASSIGNMENT` to optionally link to a `FACILITY` to explicitly support remote work and telecommuting, distinct from the primary `FACILITY` of the `WORK_EFFORT`.
- **Time Tracking Architecture:** The AI MUST relate `TIME_ENTRY` to a `TIMESHEET` (which defines the worker and period) and to a `WORK_EFFORT`. The AI MUST NOT relate `TIME_ENTRY` directly to `WORK_EFFORT_PARTY_ASSIGNMENT` to avoid redundant storage of the Party ID.
- **Multi-tiered Rates:** The AI MUST support rate resolution by modeling rates at three levels: `PARTY_RATE` (individual's base rate), `POSITION_TYPE_RATE` (standard rate for a job title), and `WORK_EFFORT_ASSIGNMENT_RATE` (rate negotiated for a specific task). All rate entities MUST include a `RATE_TYPE` (e.g., billing vs. pay).
- **Inventory and Asset Assignments:** The AI MUST track physical resource consumption and usage through `WORK_EFFORT_INVENTORY_ASSIGNMENT` (for consumed goods/raw materials) and `WORK_EFFORT_FIXED_ASSET_ASSIGNMENT` (for equipment/vehicles used temporarily).
- **Standards vs. Actuals:** The AI MUST attach estimated resource requirements (`WORK_EFFORT_SKILL_STANDARD`, `WORK_EFFORT_GOOD_STANDARD`, `WORK_EFFORT_FIXED_ASSET_STANDARD`) exclusively to the `WORK_EFFORT_TYPE` entity for planning purposes. Actual usage MUST be tied to the specific `WORK_EFFORT` instance.
- **Results Tracking:** The AI MUST model the output of a work effort explicitly using outcome entities such as `WORK_EFFORT_DELIVERABLE_PRODUCED`, `WORK_EFFORT_INVENTORY_PRODUCED`, or relationships to a repaired `FIXED_ASSET`.

@Workflow
When tasked with designing a work effort or project management schema, the AI MUST adhere to the following algorithmic sequence:
1. **Define the Need:** Instantiate `WORK_REQUIREMENT` with subtypes mapped to `REQUIREMENT_TYPE` (Project, Maintenance, Production Run). If applicable, map to a `WORK_ORDER_ITEM` for contractual commitments.
2. **Instantiate the Execution:** Create the `WORK_EFFORT` entity. Ensure it contains attributes for scheduled vs. actual dates, and estimated vs. actual hours.
3. **Classify and Structure:** Assign `WORK_EFFORT_TYPE` and `WORK_EFFORT_PURPOSE_TYPE`. Generate the recursive `WORK_EFFORT_ASSOCIATION` for WBS (Work Breakdown Structure) and `WORK_EFFORT_DEPENDENCY` for execution sequencing.
4. **Establish Planning Standards:** Model standard resource requirements by linking `WORK_EFFORT_TYPE` to Skill Standards, Good Standards, and Fixed Asset Standards.
5. **Model Resource Assignments:** Generate associative entities connecting `WORK_EFFORT` to actual `PARTY` (via Party Assignment), `INVENTORY_ITEM` (via Inventory Assignment), and `FIXED_ASSET` (via Asset Assignment). Include status and date ranges on all assignments.
6. **Implement Time and Costing:** Build the `TIMESHEET` and `TIME_ENTRY` structures. Implement the three-tiered rate architecture (`PARTY_RATE`, `POSITION_TYPE_RATE`, `WORK_EFFORT_ASSIGNMENT_RATE`) linked via `RATE_TYPE`.
7. **Define Deliverables:** Conclude the lifecycle by modeling the output generated by the effort via explicit Results/Produced entities.

@Examples (Do's and Don'ts)

- **Work Breakdown Structure:**
  - [DO]: Model tasks and projects as instances of `WORK_EFFORT` linked via a `WORK_EFFORT_ASSOCIATION` table to handle parent-child hierarchies.
  - [DON'T]: Create separate physical tables for `PROGRAM`, `PROJECT`, `PHASE`, and `TASK`.

- **Time Tracking:**
  - [DO]: Relate `TIME_ENTRY` to a `TIMESHEET` (which links to the `WORKER`/`PARTY`) and independently to the `WORK_EFFORT` being billed.
  - [DON'T]: Add `party_id` directly to `TIME_ENTRY` or link `TIME_ENTRY` directly to `WORK_EFFORT_PARTY_ASSIGNMENT`, which creates data redundancy and referential anomalies.

- **Rate Management:**
  - [DO]: Use a `RATE_TYPE` lookup table (e.g., "overtime pay," "standard billing") and allow rates to be defined dynamically in `WORK_EFFORT_ASSIGNMENT_RATE` with `from_date` and `thru_date`.
  - [DON'T]: Hardcode `billing_rate` or `pay_rate` as static columns on the `EMPLOYEE` or `PARTY` table.

- **Requirements vs. Efforts:**
  - [DO]: Maintain a strict boundary by generating a `WORK_REQUIREMENT` table to capture the request/budget, and a `WORK_EFFORT` table to capture the execution, joined by a many-to-many `WORK_REQUIREMENT_FULFILLMENT` table.
  - [DON'T]: Merge the work request (the "why" and "budget") into the same table as the work task (the "who", "when", and "how").