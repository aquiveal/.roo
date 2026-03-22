# @Domain
This rule file MUST trigger when the user requests assistance with facilitating, organizing, or simulating an EventStorming workshop; analyzing business processes or workflows through collaborative modeling; recovering lost domain knowledge for a legacy/brownfield system; identifying bounded contexts or aggregates from raw business requirements; or structuring domain events, commands, and policies for a software system.

# @Vocabulary
- **EventStorming**: A low-tech, collaborative workshop used to brainstorm and rapidly model a business process, aligning the mental models of diverse stakeholders.
- **Domain Event**: A record of something interesting that has already happened in the business. Modeled on an **Orange sticky note**. Formulated in the past tense.
- **Pain Point**: A bottleneck, manual step requiring automation, or area of missing domain knowledge. Modeled on a **Rotated (Diamond) Pink sticky note**.
- **Pivotal Event**: A significant domain event indicating a change in context or phase. Modeled using a **Vertical Bar**.
- **Command**: An operation or decision that triggers a domain event. Modeled on a **Light Blue sticky note**. Formulated in the imperative tense.
- **Actor**: A specific user persona or role that executes a command. Modeled on a **Small Yellow sticky note** attached to a Command.
- **Policy**: An automation rule where a specific domain event automatically triggers a command. Modeled on a **Purple sticky note**.
- **Read Model**: The view of data within the domain that an Actor uses to make a decision to execute a Command. Modeled on a **Green sticky note**.
- **External System**: Any system outside the explored domain that executes commands (input) or is notified about events (output). Modeled on a **Standard Pink sticky note**.
- **Aggregate**: An organizational boundary grouping related commands and the events they produce. Modeled on a **Large Yellow sticky note**.
- **Bounded Context**: A system boundary grouping related aggregates (either by functionality or coupling through policies).

# @Objectives
- Systematically guide the user through the 10-step EventStorming process without skipping steps or mixing modeling concepts.
- Ensure strict adherence to the linguistic rules of EventStorming (e.g., past tense for events, imperative for commands).
- Translate discovered business process elements into concrete software architecture boundaries (Aggregates and Bounded Contexts).
- Facilitate the creation of a Ubiquitous Language shared across all stakeholders.
- Prevent the application of EventStorming to trivial, non-complex, or purely technical (CRUD) processes.

# @Guidelines
- **Participant Constraints**: For simulated or planned in-person sessions, the AI MUST advise limiting the group to a maximum of 10 participants to ensure active contribution. For remote/online sessions, the AI MUST advise limiting the group to 5 participants. If more are needed, advise running multiple sessions and merging the models.
- **Scope Qualification**: The AI MUST verify the complexity of the business process. Do NOT use EventStorming for simple, sequential CRUD operations or obvious workflows lacking complex business logic.
- **Color/Shape Discipline**: When generating digital representations, documentation, or mermaid charts of EventStorming sessions, the AI MUST explicitly note the correct sticky note color and shape for every element (e.g., "[Orange] LeadInitialized").
- **Linguistic Discipline**: The AI MUST aggressively correct the user if a Domain Event is not in the past tense, or if a Command is not in the imperative tense.
- **Timeline Organization**: The AI MUST enforce mapping the "happy path" first before detailing alternative paths, error scenarios, or edge cases.
- **Big Picture Variant**: When exploring a massive, enterprise-wide domain, the AI MAY suggest running only Steps 1 through 4 (up to Pivotal Events) to identify high-level Bounded Contexts before doing deep-dive sessions on specific processes.
- **Physical Environment Rules**: When advising on physical setup, the AI MUST mandate a large modeling space (e.g., butcher paper on a wall), abundant markers/stickies, and explicitly advise *against* having chairs in the room to encourage active participation.

# @Workflow
When facilitating an EventStorming process, the AI MUST enforce this rigid, step-by-step algorithmic progression:

1.  **Step 1: Unstructured Exploration**
    *   *Action*: Brainstorm all possible Domain Events.
    *   *Rule*: Use Orange stickies. Enforce past tense. Do not worry about chronological order or redundancy at this stage. Stop when the rate of new events slows down.
2.  **Step 2: Timelines**
    *   *Action*: Organize the Domain Events chronologically.
    *   *Rule*: Map the "happy path" first. Then add branching flows and alternative/error scenarios. Remove duplicates and fix terminology.
3.  **Step 3: Pain Points**
    *   *Action*: Identify process bottlenecks, missing documentation, or missing knowledge.
    *   *Rule*: Mark with Rotated (Diamond) Pink stickies. Track these continuously throughout the rest of the session.
4.  **Step 4: Pivotal Events**
    *   *Action*: Identify major state transitions or phase changes in the timeline.
    *   *Rule*: Draw vertical bars between these events. Use these as early indicators for potential Bounded Context boundaries.
5.  **Step 5: Commands & Actors**
    *   *Action*: Identify the operations that caused the events.
    *   *Rule*: Place Light Blue stickies (imperative tense) immediately before the events they trigger. If a human triggers the command, attach a Small Yellow sticky naming the Actor.
6.  **Step 6: Policies**
    *   *Action*: Identify automated triggers where an event automatically causes a command.
    *   *Rule*: Use Purple stickies to connect the triggering Event to the resulting Command. Include explicit decision criteria on the sticky if applicable.
7.  **Step 7: Read Models**
    *   *Action*: Define the data views required for Actors to make decisions.
    *   *Rule*: Place Green stickies immediately before the Commands, describing the information source the Actor looks at.
8.  **Step 8: External Systems**
    *   *Action*: Map third-party or external systems interacting with the process.
    *   *Rule*: Place standard Pink stickies. Map them to the Commands they trigger (input) or the Events they listen to (output). Ensure ALL Commands are now triggered by an Actor, a Policy, or an External System.
9.  **Step 9: Aggregates**
    *   *Action*: Group related Commands and the Events they produce into cohesive transactional boundaries.
    *   *Rule*: Place them on Large Yellow stickies. Commands go on the left, Events on the right.
10. **Step 10: Bounded Contexts**
    *   *Action*: Group related Aggregates that share a linguistic model, close functionality, or tight coupling via Policies.
    *   *Rule*: Draw boundaries around these groups. Output the final system architecture map based on these boundaries.

# @Examples (Do's and Don'ts)

## Domain Events
- **[DO]**: `[Orange Sticky] OrderSubmitted`, `[Orange Sticky] PaymentFailed`, `[Orange Sticky] CampaignPublished`.
- **[DON'T]**: `[Orange Sticky] SubmitOrder` (Imperative/Command tense), `[Orange Sticky] Order` (Noun).

## Commands
- **[DO]**: `[Light Blue Sticky] EscalateTicket`, `[Light Blue Sticky] CalculateShippingCost`.
- **[DON'T]**: `[Light Blue Sticky] TicketEscalated` (Past tense/Event), `[Light Blue Sticky] Automatic Escalation` (Vague noun).

## Policies
- **[DO]**: `[Purple Sticky] "When ShipmentApproved -> ShipOrder"`, `[Purple Sticky] "When ComplaintReceived AND User is VIP -> EscalateTicket"`.
- **[DON'T]**: `[Purple Sticky] "User clicks escalate"` (This is an Actor triggering a Command, not a Policy reacting to an Event).

## Pain Points vs External Systems
- **[DO]**: Use a `[Diamond Pink Sticky]` to note "We don't know how the airfare pricing algorithm works here."
- **[DO]**: Use a `[Standard Pink Sticky]` to map "Salesforce CRM" as a system receiving the `ShipmentApproved` event.
- **[DON'T]**: Mix the two up by using a standard pink sticky for a missing piece of domain knowledge.

## Session Application
- **[DO]**: Use EventStorming to untangle a complex, undocumented legacy lead-generation workflow spanning marketing and sales teams.
- **[DON'T]**: Use EventStorming to design a simple administrative CRUD screen where users just update their profile pictures and email addresses.