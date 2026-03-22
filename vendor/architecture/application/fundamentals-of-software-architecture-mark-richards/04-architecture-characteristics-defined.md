**@Domain**
These rules MUST be triggered whenever the AI is tasked with analyzing system requirements, designing software architecture, evaluating structural or operational design choices, documenting system constraints, or performing trade-off analysis for a software project.

**@Vocabulary**
- **Architecture Characteristic**: The preferred term for a system feature that specifies a nondomain design consideration, influences some structural aspect of the design, and is critical or important to application success. 
- **Nonfunctional Requirement (NFR) / Quality Attribute**: Deprecated terms. The AI MUST NOT use these terms due to their negative or after-the-fact connotations.
- **Explicit Characteristic**: An architecture characteristic that is specifically mandated in the requirements documents or user prompts (e.g., "must handle 10,000 concurrent users" = Scalability).
- **Implicit Characteristic**: An architecture characteristic that is rarely specified in requirements but is absolutely necessary for project success based on the problem domain (e.g., baseline Security, Availability, or Reliability).
- **Operational Characteristic**: A category of characteristics concerning how the system runs (e.g., Availability, Continuity, Performance, Recoverability, Reliability/Safety, Robustness, Scalability).
- **Structural Characteristic**: A category of characteristics concerning code quality and architecture structure (e.g., Configurability, Extensibility, Installability, Leverageability/reuse, Localization, Maintainability, Portability, Supportability, Upgradeability).
- **Cross-Cutting Characteristic**: A category of characteristics that spans the entire system but falls outside pure operational or structural bounds (e.g., Accessibility, Archivability, Authentication, Authorization, Legal, Privacy, Security, Usability).
- **Ubiquitous Language**: A shared, organization-wide vocabulary defining exactly what a characteristic means (e.g., distinguishing "interoperability" from "compatibility") to prevent misunderstandings.
- **Custom Characteristic**: A composite or highly specific characteristic unique to a specific domain context (e.g., "Italy-ility" representing a unique combination of availability, recoverability, and resilience).
- **Least Worst Architecture**: The pragmatic goal of software architecture. It represents a system design that successfully balances competing trade-offs rather than attempting the impossible goal of maximizing every characteristic perfectly.

**@Objectives**
- The AI MUST accurately separate pure domain functionality from nondomain architecture characteristics.
- The AI MUST uncover and document both explicit and implicit characteristics required for a given domain.
- The AI MUST rigorously filter identified characteristics to ensure they require structural design support and are genuinely critical to success.
- The AI MUST prevent over-engineering by keeping the list of supported characteristics as small as possible.
- The AI MUST execute and document trade-off analyses, treating the balancing of characteristics like flying a helicopter (changing one control affects all others).

**@Guidelines**
- **Terminology Constraint**: The AI MUST strictly use the term "Architecture Characteristic" (or characteristics). It MUST NEVER use the terms "Nonfunctional Requirements" (NFRs) or "Quality Attributes".
- **The Three-Part Filter**: Before the AI recommends or accepts an architecture characteristic, it MUST verify that the characteristic meets these three exact criteria:
  1. It specifies a nondomain design consideration.
  2. It influences some structural aspect of the design.
  3. It is critical or important to application success.
- **Functional Separation**: The AI MUST explicitly exclude functional suitability, functional completeness, and functional correctness from lists of architecture characteristics. These are domain requirements, not architecture characteristics.
- **Implicit Discovery Constraint**: The AI MUST NOT rely solely on user-provided requirements. It MUST proactively analyze the problem domain to suggest implicit characteristics (e.g., a banking app implicitly requires rigorous security and data integrity; a high-frequency trading app implicitly requires low-latency performance).
- **Minimization Principle**: The AI MUST actively advise against trying to support too many characteristics. It MUST explicitly warn the user that each supported characteristic adds complexity to the overall design.
- **Trade-Off Declaration**: Whenever the AI proposes an architecture characteristic, it MUST instantly identify at least one inverse characteristic that will be negatively impacted (e.g., "If we prioritize high Security via on-the-fly encryption, it will negatively impact Performance").
- **Custom Definitions**: When standard characteristics (like Learnability or Interoperability) are ambiguous, the AI MUST explicitly define the context or ask the user to establish a Ubiquitous Language definition for the project.

**@Workflow**
1. **Domain Extraction**: Parse the user's prompt or requirements. Separate what the application should do (domain/functional requirements) from how it should do it (architecture characteristics).
2. **Explicit Mapping**: Map the stated technical constraints and performance goals to standardized Operational, Structural, or Cross-Cutting characteristics.
3. **Implicit Discovery**: Analyze the business domain to identify critical undocumented requirements (e.g., Security, Recoverability) and add them to the characteristic list.
4. **Structural Verification**: Run the combined list through the Three-Part Filter. Discard any characteristic that does not specifically require architectural/structural consideration (e.g., discard generic security hygiene if it doesn't require a dedicated structural module/service).
5. **Culling and Prioritization**: Identify the absolute minimum set of characteristics critical for application success. Recommend culling non-critical ones to avoid generic, overly complex designs.
6. **Trade-Off Analysis**: For the finalized list, pair the characteristics against each other to highlight architectural friction (e.g., Scalability vs. Consistency, Security vs. Performance) and propose the "least worst" architectural approach.

**@Examples (Do's and Don'ts)**

- **[DO]** Use modern, precise terminology.
  *Example*: "Based on the requirements, we need to define the **architecture characteristics** for this system. I have identified Scalability as an explicit characteristic, and Security as an implicit characteristic."
- **[DON'T]** Use legacy or self-denigrating terminology.
  *Example*: "Here is the list of nonfunctional requirements and quality attributes you requested."

- **[DO]** Filter characteristics based on structural impact.
  *Example*: "While third-party payment integration requires standard security hygiene, it does not mandate a dedicated structural architecture change. Therefore, we will not elevate it to a primary architecture characteristic. However, our in-house payment processing engine will dictate structural isolation, making Security a primary architecture characteristic here."
- **[DON'T]** Treat functional requirements as architecture characteristics.
  *Example*: "The architecture characteristics for this system include Functional Completeness, Functional Correctness, and Performance."

- **[DO]** Explicitly state trade-offs when prioritizing characteristics.
  *Example*: "To support the requested **Elasticity** for burst traffic, we must trade off some **Performance** overhead for dynamic scaling mechanisms, and we will increase the overall structural complexity."
- **[DON'T]** Promise to maximize all characteristics simultaneously.
  *Example*: "I will design an architecture that maximizes extreme performance, perfect security, infinite scalability, and total availability simultaneously."

- **[DO]** Minimize the list of characteristics.
  *Example*: "You have requested 15 different architecture characteristics. Supporting all of these will lead to a highly complex, unwieldy design. Let's isolate the top 3-4 that are strictly critical to the application's success."
- **[DON'T]** Accept an infinitely growing list of system constraints.
  *Example*: "I have added all 15 architecture characteristics to the design criteria and will ensure the system supports every single one."