@Domain
Trigger these rules when executing architecture analysis, gathering system requirements, translating business/domain problems into technical constraints, conducting system design planning, evaluating architectural trade-offs, or extracting architectural characteristics ("-ilities") from user stories and project documentation.

@Vocabulary
- **Architecture Characteristics ("-ilities"):** Nondomain design considerations that influence the structural aspect of the system and are critical to application success (e.g., scalability, availability, maintainability).
- **Explicit Characteristics:** Characteristics explicitly derived from statements in requirement documents or user stories (e.g., "Must support 10,000 concurrent users" -> Scalability).
- **Implicit Characteristics:** Characteristics rarely specified in requirements but absolutely necessary for project success, inferred from the inherent knowledge of the problem domain (e.g., college registration systems inherently require Elasticity due to last-minute bursts, even if not stated).
- **Generic Architecture Anti-Pattern:** A destructive architectural anti-pattern where an architect attempts to design a system that supports *all* or too many architecture characteristics, resulting in massive complexity and ultimate project failure (e.g., the Vasa warship).
- **Ivory Tower Architect Anti-Pattern:** Designing architecture in total isolation from the development, operations, and business teams.
- **Scalability:** The ability of a system to handle a large number of sustained, concurrent users without serious performance degradation.
- **Elasticity:** The ability of a system to handle sudden, unpredictable bursts or spikes of traffic (e.g., auction end times, ticket sales).
- **Architecture Katas:** Specific, time-boxed training exercises containing a Description, Users, Requirements, and Additional Context, used to practice identifying architecture characteristics.
- **Domain/Architecture Isomorphism:** The degree to which the shape of the architecture maps to a particular problem domain.

@Objectives
- Extract and translate vague business domain language into precise engineering architecture characteristics.
- Uncover both explicit requirements and implicit domain-driven characteristics.
- Ruthlessly constrain the number of architecture characteristics to minimize system complexity and prevent the Generic Architecture anti-pattern.
- Differentiate between requirements that mandate structural architectural changes versus requirements that can be handled through localized software design patterns.
- Ensure all architectural recommendations are treated as a "least worst" collection of trade-offs rather than "perfect" solutions.

@Guidelines
- **Translation Mapping:** The AI MUST translate business stakeholder concerns into architecture characteristics using the following strict mappings:
  - *Mergers and acquisitions* -> Interoperability, Scalability, Adaptability, Extensibility.
  - *Time to market* -> Agility, Testability, Deployability. (CRITICAL: Agility alone does not equal time to market; it requires testability and deployability).
  - *User satisfaction* -> Performance, Availability, Fault Tolerance, Testability, Deployability, Agility, Security.
  - *Competitive advantage* -> Agility, Testability, Deployability, Scalability, Availability, Fault Tolerance.
  - *Time and budget* -> Simplicity, Feasibility.
- **The Top-Three Constraint:** The AI MUST NOT attempt to prioritize an exhaustive list of architecture characteristics. Instead, the AI MUST constrain the final recommendation to the top three most important characteristics to drive the architecture.
- **Avoid the Generic Architecture Anti-Pattern:** The AI MUST actively discourage designing for too many "-ilities." Every added characteristic complicates the overall system design. 
- **The Elimination Test:** Once a list of characteristics is identified, the AI MUST explicitly identify the *least* important characteristic and recommend eliminating it to simplify the design.
- **Scalability vs. Elasticity:** The AI MUST accurately distinguish between these two characteristics based on user behavior. If user traffic is consistent but high, specify Scalability. If traffic is bursty (e.g., mealtimes, auctions, ticket sales), specify Elasticity.
- **Architecture vs. Design Boundaries:** The AI MUST evaluate if a characteristic requires structural support (Architecture) or can be handled inside the application code (Design).
  - *Example:* Standard data protection is a Design concern (security hygiene). An in-application payment processing isolation module is an Architecture concern.
- **Over-Specification Avoidance:** The AI MUST NOT build unnecessary brittleness into the architecture. If an external third-party service is required (e.g., map routing), the AI should recommend graceful degradation rather than enforcing strict system-wide reliability constraints that fail the whole app if the third party goes down.
- **No Wrong Answers, Only Expensive Ones:** The AI MUST frame architectural decisions as trade-offs. The AI MUST state the negative trade-off (e.g., cost, complexity, coupling) for every recommended architecture characteristic.

@Workflow
1. **Analyze Domain Concerns:** Parse the provided business context and translate stakeholder goals (e.g., "budget constraints", "fast time to market") into the corresponding architectural "-ilities" using the Translation Mapping.
2. **Extract Explicit Characteristics:** Review the stated requirements (e.g., expected user counts, integrations) and map them directly to structural architecture characteristics.
3. **Extract Implicit Characteristics:** Analyze the fundamental nature of the domain. Infer missing characteristics (e.g., unstated bursty traffic, implicit security requirements, expected availability needs).
4. **Filter Architecture vs. Design:** Review the combined list of characteristics. Relegate items to "Application Design" if they do not require systemic structural decisions (e.g., handling customizability via the Template Method pattern instead of a structural Microkernel architecture, or using standard coding hygiene for implicit security).
5. **Trade-off and Elimination:** Review the remaining structural characteristics. Identify the least critical characteristic and eliminate it. 
6. **Final Selection:** Output the final Top Three architecture characteristics. Provide the trade-offs and structural implications for each of the selected characteristics.

@Examples (Do's and Don'ts)

**Translation of Business Drivers**
- [DO]: "To address the business goal of 'Time to Market', the architecture must support Agility, Testability, and Deployability. Just focusing on agility without automated testing and deployment will fail to improve time to market."
- [DON'T]: "The business wants a fast time to market, so the primary architecture characteristic is Performance."

**Prioritization and Constraining**
- [DO]: "From the gathered requirements, we identified 8 potential characteristics. To avoid the Generic Architecture anti-pattern, we must restrict our focus. The top three most critical characteristics for this domain are Elasticity, Availability, and Customizability."
- [DON'T]: "Here is the prioritized list of the 12 architecture characteristics this system must support: 1. Scalability, 2. Availability, 3. Security, 4. Performance, 5. Interoperability..."

**Architecture vs. Design (Security Example)**
- [DO]: "While security is an implicit characteristic of this e-commerce app, standard security hygiene (e.g., not storing plaintext credit cards) is sufficient. Since payment is handled by a third-party processor, security does not require a specialized structural architecture style. We will handle this in Application Design."
- [DON'T]: "Because this application accepts payments, Security is our number one architectural characteristic and we must build a highly secure, isolated, custom architectural structure."

**Scalability vs. Elasticity**
- [DO]: "Because this is a concert ticketing system, users will flood the system the minute tickets go on sale. Therefore, Elasticity (the ability to handle sudden bursts of traffic) is a critical characteristic, rather than just baseline Scalability."
- [DON'T]: "The ticketing system will have 50,000 users at once when sales open, so it needs High Scalability."

**The Elimination Test**
- [DO]: "We have identified Scalability, Availability, Customizability, and Performance. To ensure the 'least worst' architecture and keep the design simple, we must eliminate one. In this sandwich shop domain, Performance is the least critical compared to keeping the system available and handling customizations. We will drop Performance as a primary architectural driver."
- [DON'T]: "We need Scalability, Availability, Customizability, and Performance. We will design a system that maximizes all of them perfectly."