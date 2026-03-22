# @Domain
These rules MUST trigger whenever the AI is tasked with designing, analyzing, refactoring, or generating data models, databases, software architectures, or data warehouse schemas for Professional Services enterprises. Activation conditions include domains involving temporary placement firms, accounting firms, law firms, management consultants, administrative assistance contracting firms, computer consulting firms, office cleaning services, or any enterprise whose primary revenue model is billing for time, specialized services, or predetermined deliverables.

# @Vocabulary
To ensure exact architectural alignment, the AI MUST strictly adopt and use the following mental model and terminology:
- **Professional**: A person who has the capability of offering services to clients (e.g., lawyers, accountants, consultants).
- **Client**: A person or organization that has engaged or is currently engaging the enterprise. Subtyped into **Bill To Client** (responsible for payment) and **Delivery Client** (receives the services).
- **Professional Services Provider**: The organization providing the services, which can be an internal organization, a subcontractor, or a competitor.
- **Deliverable Based Service**: A predefined work product produced for a client as a result of an engagement.
- **Time and Materials Service**: A standard service offering billed based on tracked time and materials used.
- **Product Delivery Skill Requirement**: The specific competencies or skills required to deliver a professional service product.
- **Requirement**: A captured need, subtyped into **Resource Requirement** (need for a professional/placement), **Project Requirement** (deliverables-based need), and **Product Requirement** (need for a predefined standard offering).
- **Requirement Communication / Activity**: Tracking mechanisms for the back-and-forth interactions (e.g., resume submission, interview) resolving a requirement.
- **Statement of Work**: A specialized quote item that describes what will be delivered, how, and the governing terms, acting to confirm a mutual understanding.
- **Engagement**: The equivalent of an "Order" in professional services. A commitment to contract professional services.
- **Engagement Item**: A specific contracted service line, subtyped into **Professional Placement**, **Custom Engagement Item**, **Product Order Item** (Standard Service, Deliverable, or Good), and **Other Engagement Item**.
- **Engagement Rate**: The billing rate and associated costs of professionals that may change over time (e.g., standard, overtime).
- **Professional Services Agreement**: A long-term governing contract, subtyped into **Client Agreement** and **Subcontractor Agreement**, which dictates the pricing and terms for subsequent Engagements.
- **Service Entry**: The primary delivery mechanism for professional services, subtyped into **Time Entry**, **Expense Entry**, **Materials Usage**, and **Deliverable Turnover**.
- **Service Entry Header**: The submission vehicle (historically a "timesheet") grouping multiple Service Entries submitted by a Professional.

# @Objectives
When applying these rules, the AI MUST achieve the following systemic goals:
- Accurately map the intangible nature of professional services (time, expertise, deliverables) into concrete data tracking structures.
- Support deep visibility into profitability, resource utilization, and project tracking to help the enterprise deliver projects on time and within budget.
- Facilitate the complete lifecycle from initial Request/Requirement, to Quote/Statement of Work, to Engagement, to Delivery (Service Entries), and finally to Invoicing.
- Bridge the gap between contract-oriented firms (temporary placements) and deliverable-oriented firms (project-based consulting) using a unified, flexible architecture.

# @Guidelines
The AI MUST enforce the following granular constraints and architectural rules:

## Party and Role Modeling
- The AI MUST subtype `PARTY ROLE` to include `PROFESSIONAL`, `CLIENT`, and `PROFESSIONAL SERVICES PROVIDER`.
- The AI MUST further subtype `CLIENT` into `BILL TO CLIENT` and `DELIVERY CLIENT` to separate financial responsibility from service receipt.
- The AI MUST track `SUBCONTRACTOR RELATIONSHIP` within `PARTY RELATIONSHIP` to manage external firms acting as Professional Services Providers.

## Product and Service Modeling
- The AI MUST categorize `PRODUCT` into `SERVICE` or `GOOD`.
- The AI MUST subtype `SERVICE` into `DELIVERABLE BASED SERVICE` and `TIME AND MATERIALS SERVICE`.
- The AI MUST map `SKILL TYPE` to `PRODUCT` using an associative entity `PRODUCT DELIVERY SKILL REQUIREMENT`.
- The AI MUST use `MARKETING PACKAGE` to bundle services (e.g., a strategic plan encompassing models and reports).
- The AI MUST allow `PRODUCT COMPLEMENT` and `PRODUCT OBSOLESCENCE`.
- **ANTI-PATTERN**: The AI MUST NOT use `PRODUCT SUBSTITUTE` or `PRODUCT INCOMPATIBILITY` for services, as substituting one specialized service for another without architectural context is invalid in professional services.

## Requirements, Requests, and Quotes Modeling
- The AI MUST model `REQUIREMENT` to track both `CLIENT REQUIREMENT` and `INTERNAL REQUIREMENT` (e.g., subcontracting needs).
- The AI MUST subtype `REQUIREMENT` into `RESOURCE REQUIREMENT` (linking to `NEEDED SKILL`), `PROJECT REQUIREMENT` (linking to `NEEDED DELIVERABLE`), and `PRODUCT REQUIREMENT` (linking to `DESIRED FEATURE`).
- The AI MUST model back-and-forth interactions using `REQUIREMENT COMMUNICATION` and `REQUIREMENT ACTIVITY`.
- The AI MUST model `REQUEST` as RFI, RFP, or RFQ, consisting of `REQUEST ITEM`s that map back to `REQUIREMENT`, `NEEDED DELIVERABLE`, `NEEDED SKILL`, `DESIRED FEATURE`, or `PRODUCT`.
- The AI MUST subtype `QUOTE ITEM` to include `STATEMENT OF WORK` to confirm written understanding of delivery and terms.

## Engagement (Order) Modeling
- The AI MUST replace standard "Order" nomenclature with `ENGAGEMENT`.
- The AI MUST subtype `ENGAGEMENT ITEM` into `PROFESSIONAL PLACEMENT`, `CUSTOM ENGAGEMENT ITEM`, `PRODUCT ORDER ITEM` (subtyped into `STANDARD SERVICE ORDER ITEM`, `DELIVERABLE ORDER ITEM`, `GOOD ORDER ITEM`), and `OTHER ENGAGEMENT ITEM`.
- The AI MUST model billing rates using `ENGAGEMENT RATE` associated with the `ENGAGEMENT ITEM`, tracking changing rates over time via `from date` and `thru date`, and applying `RATE TYPE` (e.g., regular, overtime).
- The AI MUST map `ENGAGEMENT ITEM` to `WORK EFFORT` via `ENGAGEMENT WORK FULFILLMENT` to support breaking down a single commitment into multiple manageable projects.

## Agreement Modeling
- The AI MUST subtype `AGREEMENT` into `PROFESSIONAL SERVICES AGREEMENT`.
- The AI MUST further subtype `PROFESSIONAL SERVICES AGREEMENT` into `CLIENT AGREEMENT` and `SUBCONTRACTOR AGREEMENT`.
- The AI MUST establish that a `PROFESSIONAL SERVICES AGREEMENT` governs multiple `ENGAGEMENT`s, dictating overarching terms, conditions, and base pricing.

## Delivery and Service Entry Modeling
- The AI MUST NOT use traditional Shipment models for time/services (only for tangible goods like CD-ROMs or documents).
- The AI MUST model delivery via `SERVICE ENTRY`, subtyped into `TIME ENTRY`, `EXPENSE ENTRY`, `MATERIALS USAGE`, and `DELIVERABLE TURNOVER`.
- The AI MUST group `SERVICE ENTRY`s under a `SERVICE ENTRY HEADER` submitted by a `PROFESSIONAL`.
- The AI MUST map `PROFESSIONAL` to `ENGAGEMENT ITEM` via `PROFESSIONAL ASSIGNMENT` (for placement firms) or to `WORK EFFORT` (for deliverable-oriented firms).
- Within `TIME ENTRY`, the AI MUST track both the billing rate (charged to client) and the cost (paid to the professional) to calculate gross margin.

## Invoicing Modeling
- The AI MUST construct `INVOICE ITEM`s to bill for `PRODUCT`s, `PRODUCT FEATURE`s, `SERVICE ENTRY`s, and/or `WORK EFFORT`s.
- The AI MUST include a `percentage` attribute when billing for `WORK EFFORT`s to allow for partial billing (e.g., phase completion).
- The AI MUST allow the consolidation of several `SERVICE ENTRY`s into a single `INVOICE ITEM`.

## Star Schema (Data Warehousing) Requirements
- The AI MUST generate a `TIME_ENTRY_FACT` table when designing analytic structures.
- Measures in `TIME_ENTRY_FACT` MUST include `dollars_billed` (billing rate * time), `hours_billed` (normalized using Unit of Measure conversions), `cost` (amount paid to professional), and `gross_margin` (cost / dollars_billed).
- Dimensions MUST include `PROFESSIONALS`, `CLIENTS`, `PROJECTS`, `RATE_TYPES`, `TIME_BY_DAY`, and `ENGAGEMENT_ITEM_TYPES`.

# @Workflow
When tasked with modeling a Professional Services system, the AI MUST follow this rigid algorithm:
1.  **Define the Parties**: Initialize `PARTY`, `PARTY ROLE`, and `PARTY RELATIONSHIP`. Instantiate specific roles: `PROFESSIONAL`, `CLIENT` (Bill To/Delivery), and `PROFESSIONAL SERVICES PROVIDER`.
2.  **Establish the Service Catalog**: Define `PRODUCT` as `SERVICE` (Deliverable Based vs. Time and Materials). Link required skills using `PRODUCT DELIVERY SKILL REQUIREMENT`. Bundle offerings using `MARKETING PACKAGE`.
3.  **Map Pre-Sales Activities**: Design `REQUIREMENT` structures (Resource, Project, Product). Link to `REQUEST` (RFI/RFP/RFQ) and establish `QUOTE ITEM`s including `STATEMENT OF WORK`.
4.  **Formalize Agreements and Engagements**: Create the `PROFESSIONAL SERVICES AGREEMENT` (Client/Subcontractor) as the governing contract. Define the `ENGAGEMENT` and break it into `ENGAGEMENT ITEM`s (Placements, Custom Engagements, Deliverables). Apply `ENGAGEMENT RATE`s.
5.  **Model Delivery and Work Efforts**: Assign Professionals to Engagements or Work Efforts. Create the `SERVICE ENTRY HEADER` and underlying `SERVICE ENTRY` structures (Time, Expense, Materials, Deliverable Turnover). Ensure cost and billing rate are captured at the Time Entry level.
6.  **Construct Invoicing**: Map `SERVICE ENTRY`s and `WORK EFFORT`s to `INVOICE ITEM`s. Include partial billing capabilities via percentage flags on Work Efforts.
7.  **Design Analytics**: Build the `TIME_ENTRY_FACT` star schema connecting to Professionals, Clients, Projects, Rate Types, Time, and Engagement Item Types.

# @Examples (Do's and Don'ts)

## Product Association Rules
- **[DO]**: Use `MARKETING PACKAGE` to bundle a "Strategic IT Assessment" service with a "Database Design" deliverable and a "Software License" good.
- **[DON'T]**: Use `PRODUCT SUBSTITUTE` to suggest that an "Accounting Audit" can automatically be substituted by a "Tax Return Filing" in the system architecture.

## Engagement vs. Order Terminology
- **[DO]**: Create an `ENGAGEMENT` entity containing an `ENGAGEMENT ITEM` subtyped as `PROFESSIONAL PLACEMENT` when a client hires a contract data modeler.
- **[DON'T]**: Create a generic `SALES ORDER` with a `SALES ORDER ITEM` for placing a human resource.

## Delivery Tracking
- **[DO]**: Use a `SERVICE ENTRY HEADER` to group `TIME ENTRY` (hours worked), `EXPENSE ENTRY` (travel costs), and `DELIVERABLE TURNOVER` (completed architectural document) submitted by a consultant on Friday afternoon.
- **[DON'T]**: Attempt to log consultant hours worked using a `SHIPMENT` or `SHIPMENT ITEM` table.

## Professional Assignment
- **[DO]**: Link a `PROFESSIONAL` directly to a `WORK EFFORT` (Project/Activity/Task) for a deliverables-based consulting firm, or directly to an `ENGAGEMENT ITEM` for a temporary placement/staffing firm.
- **[DON'T]**: Force temporary contract workers (placements) into a rigid `WORK EFFORT` structure if the firm only bills based on the `ENGAGEMENT ITEM` contract.