# @Domain
These rules MUST be triggered whenever the AI is tasked with evaluating, proposing, documenting, or updating a technology choice, architectural structure, system design, coding standard, or any decision that impacts the non-functional characteristics of a system. They specifically activate when the user requests the creation, review, or modification of an Architecture Decision Record (ADR), or when the AI identifies a technical choice as "architecturally significant".

# @Vocabulary
- **Architecturally Significant**: Any decision that affects the structure, nonfunctional characteristics ("-ilities"), dependencies, interfaces, or construction techniques of a system.
- **Architecture Decision Record (ADR)**: A short text file (usually one to two pages long) acting as the single system of record for a specific architecture decision.
- **Covering Your Assets Anti-Pattern**: The behavioral anti-pattern where an architect avoids or defers making a decision out of fear of making the wrong choice.
- **Groundhog Day Anti-Pattern**: The behavioral anti-pattern where a decision is repeatedly debated because the original business and technical justifications (*why* it was made) were not documented.
- **Email-Driven Architecture Anti-Pattern**: The behavioral anti-pattern where decisions are lost in communication streams (like emails or chat logs) rather than captured in a centralized system of record.
- **Last Responsible Moment**: The optimal time to make an architecture decision—waiting until enough information is gathered to justify the decision, but not waiting so long that it causes "Analysis Paralysis" or delays development.
- **RFC (Request for Comments)**: A specific ADR status used for draft decisions to solicit stakeholder feedback before a hard deadline.
- **Fitness Function**: An automated test or manual check designed to continuously measure and govern compliance with a specific architecture decision.

# @Objectives
- **Establish a Single Source of Truth**: The AI must prevent the "Email-Driven Architecture" anti-pattern by ensuring all architecturally significant decisions are captured in formal ADRs rather than conversational text.
- **Prioritize the 'Why' over the 'How'**: The AI must ensure that every architecture decision explicitly documents the underlying business and technical justifications, preventing the "Groundhog Day" anti-pattern.
- **Enforce Decisiveness**: The AI must prevent the "Covering Your Assets" anti-pattern by proposing firm decisions at the last responsible moment using an affirmative, commanding voice.
- **Ensure Measurability**: The AI must guarantee that every architecture decision includes a concrete method for compliance checking, preferably through automated fitness functions.
- **Justify Standards**: The AI must treat coding and architectural standards as architecture decisions, justifying their existence rather than arbitrarily dictating rules.

# @Guidelines
- **Identification of Significance**: The AI MUST treat any choice impacting system structure, architecture characteristics (performance, scalability, etc.), dependencies, interfaces, or platform construction tools as an "architecturally significant" decision requiring an ADR.
- **Required ADR Structure**: The AI MUST format all ADRs using exactly these seven sections: Title, Status, Context, Decision, Consequences, Compliance, and Notes. (An "Alternatives" section MAY be added if alternative analysis is too lengthy for the Context section).
- **Title Constraints**: The AI MUST format the ADR title sequentially with a short, unambiguous phrase describing the decision (e.g., "ADR 42. Use of Asynchronous Messaging Between Order and Payment Services").
- **Status Constraints**: The AI MUST use only the following statuses: 
  - *Proposed*: Awaiting approval based on predefined criteria (e.g., cost, cross-team impact, security).
  - *Accepted*: Approved and ready for implementation.
  - *Superseded by [ADR #]*: Replaced by a newer decision.
  - *RFC, Deadline [Date]*: Request for comments to avoid analysis paralysis.
- **Context Constraints**: The AI MUST clearly specify the forces at play forcing the decision and concisely elaborate on the available alternatives.
- **Decision Constraints**: The AI MUST write the decision using an affirmative, commanding voice. It MUST NOT use passive voice or state opinions (e.g., use "We will use...", never "I think we should use...").
- **Justification Constraints**: The AI MUST provide BOTH technical AND business justifications (e.g., cost, time to market, user satisfaction, strategic positioning) within the Decision section.
- **Consequences Constraints**: The AI MUST document both the positive benefits and the negative impacts (trade-offs) of the decision.
- **Compliance Constraints**: The AI MUST define how the decision will be governed. It MUST write or specify an automated fitness function (e.g., using ArchUnit, NetArchTest) or clearly define a manual compliance checklist.
- **Metadata Constraints**: The AI MUST populate the Notes section with metadata: Original author, Approval date, Approved by, Superseded date, Last modified date, Modified by, and Last modification details.
- **Storage/Organization Constraints**: When saving ADRs to a filesystem, the AI MUST organize them logically by scope, using directories such as `/Application/[AppName]/`, `/Integration/`, or `/Enterprise/`.

# @Workflow
When tasked with evaluating a technical choice or creating an Architecture Decision Record, the AI MUST follow this rigid algorithm:

1. **Significance Check**: Evaluate the choice against Michael Nygard's criteria (Structure, Nonfunctional characteristics, Dependencies, Interfaces, Construction techniques). If it matches any, proceed to ADR generation.
2. **Context Gathering**: Define the specific forces, business problems, and technical limitations forcing the decision. Identify all viable alternative solutions.
3. **Drafting the Title & Status**: Assign a sequential number, a concise descriptive title, and an initial Status (e.g., *Proposed* or *RFC*).
4. **Formulating the Decision**: 
   - State the chosen solution using an affirmative, commanding voice.
   - Write the technical justification (how it solves the technical problem).
   - Write the business justification (how it impacts cost, time, or user satisfaction).
5. **Trade-off Analysis (Consequences)**: Identify and document what negative impacts, complexities, or technical debts are introduced by this decision.
6. **Defining Compliance**: Determine if the rule can be automated. If yes, write the exact ArchUnit/NetArchTest code or CI/CD pipeline step needed. If no, write the manual review criteria.
7. **Document Assembly**: Output the final decision strictly using the 7-part ADR template. Ask the user for any missing metadata (Author, Approver) to populate the Notes section.
8. **File Storage**: Suggest saving the document to the appropriate contextual directory (e.g., `/docs/adrs/application/`).

# @Examples (Do's and Don'ts)

## Decision Phrasing (Voice)
- **[DO]**: "We will use asynchronous publish-and-subscribe messaging between the Bid Capture and Bid Tracker services."
- **[DON'T]**: "I think asynchronous messaging between the services would be the best choice." (Violates affirmative voice rule; states an opinion).

## Justifications
- **[DO]**: "We will break apart the monolithic application into separate services. *Technical Justification*: This decouples functional aspects, allowing each part to use fewer virtual machine resources. *Business Justification*: This allows us to deliver new business functionality faster, improving our time to market and reducing release costs."
- **[DON'T]**: "We will break apart the monolith because smaller codebases are easier to read and deploy." (Missing the business justification; risks the Groundhog Day anti-pattern).

## Status Management (Superseding)
- **[DO]**: 
  "Status: Superseded by ADR 68." (On the old ADR)
  "Status: Accepted, supersedes ADR 42." (On the new ADR)
- **[DON'T]**: "Status: Changed." or simply deleting the old ADR file. (Fails to maintain the historical system of record).

## Defining Standards
- **[DO]**: Use an ADR to define a standard. 
  *Context*: "Shared utility classes are becoming duplicated across layers." 
  *Decision*: "All shared objects used by business objects will reside in the shared services layer to isolate shared functionality." 
  *Compliance*: `@Test public void shared_services_should_reside_in_services_layer() { ... }`
- **[DON'T]**: Create a Wiki page titled "Coding Standards" with a bulleted list of rules ("You must put shared objects in the services layer") without documenting the *why* or the consequences.

## Handling Uncertainty
- **[DO]**: "Status: Request For Comments, Deadline 09 JAN 2024".
- **[DON'T]**: Avoid generating the ADR entirely because the user hasn't finalized the database choice yet. (Violates the Covering Your Assets anti-pattern rules).