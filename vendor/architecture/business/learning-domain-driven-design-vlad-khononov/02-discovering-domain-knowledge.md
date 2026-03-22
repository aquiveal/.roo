# @Domain

These rules MUST trigger when the AI is performing tasks related to:
- Analyzing or gathering software requirements from user prompts.
- Designing or refactoring domain models, entities, or business logic.
- Naming classes, methods, variables, or database tables representing business concepts.
- Writing behavioral tests (e.g., BDD, Gherkin) or domain documentation.
- Resolving terminology conflicts, mapping business workflows, or interacting with a brownfield/legacy codebase where business logic must be modernized.

# @Vocabulary

- **Business Problem**: A challenge associated with optimizing workflows, minimizing manual labor, managing resources, or supporting decisions within a business, rather than a purely mathematical or technical riddle.
- **Domain Expert**: A subject matter expert who understands the intricacies of the business being modeled. The origin of all business knowledge.
- **Mental Model**: The domain expert's thought process regarding how the business works, including entities, behaviors, cause/effect relationships, and invariants.
- **Ubiquitous Language (UL)**: A single, precise language used consistently by all project stakeholders (experts, engineers, AI) to describe the business domain. It consists ONLY of business terms, completely devoid of technical jargon.
- **Analysis Model (Anti-Pattern)**: An engineer-friendly translation of domain knowledge that acts as a mediator between business and code, leading to lost or distorted information.
- **Model**: A simplified representation of a real-world thing or phenomenon that intentionally emphasizes certain aspects while ignoring others to solve a specific problem. An abstraction with a specific use in mind.
- **Ambiguous Term**: A single vocabulary word that has multiple, distinct meanings depending on context (e.g., "Policy" meaning a regulatory rule or an insurance contract).
- **Synonymous Term**: Multiple distinct vocabulary words used interchangeably to describe the same concept or role (e.g., "User," "Visitor," "Account"), which obscures distinct behaviors.
- **Tacit Knowledge**: Crucial business knowledge that is not documented or codified, residing only in the minds of domain experts, requiring proactive inquiry to uncover.
- **White Spot**: Missing, unconsidered, or implicitly conflicting edge cases in the business logic or the "happy path" requirements.

# @Objectives

- **Eliminate Translation Layers**: The AI MUST directly translate the domain experts' mental models into source code and documentation using the Ubiquitous Language, avoiding intermediate "technical translation" phases (The Telephone Game).
- **Cultivate Shared Understanding**: The AI MUST enforce the use of a unified business vocabulary across all artifacts (code, tests, documentation, diagrams).
- **Enforce Absolute Consistency**: The AI MUST detect and resolve ambiguities, synonymous terms, and overloaded words in the provided requirements.
- **Abstract for Purpose**: The AI MUST design models that contain *only* the details necessary to solve the specific business problem, ignoring irrelevant real-world attributes.
- **Extract Tacit Knowledge**: The AI MUST proactively interrogate the user to uncover edge cases, hidden invariants, and undocumented rules rather than making assumptions.

# @Guidelines

### Language & Terminology Restrictions
- The AI MUST formulate all class names, method names, variables, and documentation strictly in the Language of the Business.
- The AI MUST NEVER use technical jargon (e.g., "Singleton", "Factory", "Table", "HTML", "IFrame") when discussing or modeling business rules. 
- The AI MUST explicitly flag and reject ambiguous terms. If a term has multiple meanings, the AI MUST prompt the user to define distinct terms for each concept.
- The AI MUST NOT use synonymous terms interchangeably. The AI MUST assign one strict definition per term and enforce its isolated usage.
- If the target business domain operates in a non-English language, the AI MUST use English translations for the nouns/entities in the codebase to align with programming conventions, while maintaining exact conceptual parity.

### Modeling Constraints
- The AI MUST NOT attempt to create a 1:1 copy of the real world. Models MUST intentionally omit extraneous details that do not serve the specific software problem being solved.
- The AI MUST represent behavior (rules, assumptions, invariants) as explicitly as data (nouns). Nouns alone are insufficient.
- The AI MUST treat model generation as a mutual learning process. If the user provides a "happy path," the AI MUST explicitly ask about contradictory edge cases to expose "white spots" in the logic.

### Documentation & Testing Rules
- The AI MUST capture "nouns" (entities, roles, processes) in a continuously updated project glossary. 
- The AI MUST capture "behaviors" (business logic, invariants, rules) using automated tests written in the Gherkin language (Given/When/Then).
- The AI MUST ensure the Gherkin tests are readable by a non-technical domain expert, strictly utilizing the Ubiquitous Language.
- The AI MUST recommend or apply static code analysis rules (like NDepend configurations) to mechanically verify that the codebase strictly adheres to the Ubiquitous Language terms if applicable to the environment.

### Brownfield / Legacy Projects
- When working in an existing system with an incorrect or highly technical formed language, the AI MUST exercise patience. The AI MUST enforce the correct Ubiquitous Language in new documentation and new source code boundaries without immediately breaking existing external architectural dependencies.

# @Workflow

When executing a task within the target domain, the AI MUST adhere to the following algorithmic sequence:

1. **Knowledge Discovery & Extraction:**
   - Scan the user's prompt for business requirements.
   - Identify all nouns, verbs, rules, and edge cases.
   - *Action:* If the requirements only cover the "happy path" or omit invariants, HALT and prompt the user with targeted questions to extract tacit knowledge and expose white spots.

2. **Ubiquitous Language Cultivation:**
   - Filter the extracted terms.
   - Identify any technical jargon used to describe business logic. *Action:* Translate to business terms.
   - Identify ambiguous terms (one word, multiple meanings). *Action:* Split into distinct terms.
   - Identify synonyms (multiple words, one meaning). *Action:* Consolidate to a single, authoritative term.

3. **Model Definition:**
   - Define the specific problem the model is intended to solve.
   - Strip away all real-world attributes of the entities that do not directly contribute to solving this specific problem (purposeful abstraction).

4. **Artifact Generation:**
   - **Glossary Update:** Output a markdown glossary defining the validated nouns, roles, and processes.
   - **Behavior Specification:** Output Gherkin (Given/When/Then) scenarios mapping the exact business rules, state changes, and invariants using ONLY the Ubiquitous Language.

5. **Code Translation:**
   - Generate source code where classes, properties, and methods map 1:1 with the Ubiquitous Language and Gherkin specifications.
   - Ensure absolutely no intermediate "analysis model" translations exist in the logic.

# @Examples (Do's and Don'ts)

### Principle: Language of the Business vs. Technical Jargon
- **[DO]**
  ```csharp
  public class AdvertisingCampaign {
      public void Publish() {
          if (!HasActivePlacements()) {
              throw new InvalidDomainStateException("A campaign can be published only if at least one of its placements is active.");
          }
      }
  }
  ```
- **[DON'T]**
  ```csharp
  public class CampaignManager {
      public void UpdateRecord() {
          // Anti-pattern: Using DB jargon to describe business rules
          if (db.ActivePlacementsTable.Count == 0) {
              throw new Exception("Cannot update campaign because active-placements table has no correlated records.");
          }
      }
  }
  ```

### Principle: Eliminating Ambiguous Terms
- **[DO]**
  ```markdown
  // Glossary Definition
  - RegulatoryRule: A legal constraint imposed by the government.
  - InsuranceContract: The binding agreement between the company and the customer.
  ```
- **[DON'T]**
  ```markdown
  // Anti-pattern: Using "Policy" for both concepts, requiring the AI or Engineer to guess the context.
  - Policy: Can be a government rule or the user's contract.
  ```

### Principle: Eliminating Synonymous Terms
- **[DO]**
  ```csharp
  // Differentiating based on explicit roles and behaviors
  public class UnregisteredVisitor { /* Used solely for web analytics tracking */ }
  public class RegisteredAccount { /* Has access to system functionality and billing */ }
  ```
- **[DON'T]**
  ```csharp
  // Anti-pattern: Using User, Visitor, and Account interchangeably throughout the code for the exact same entity.
  public class User { ... }
  public void ProcessVisitor(User account) { ... }
  ```

### Principle: Capturing Behavior via Gherkin (Ubiquitous Language)
- **[DO]**
  ```gherkin
  Scenario: Notify the agent about a new support case
    Given Vincent Jules submits a new support case saying "I need help configuring AWS Infinidash"
    When the ticket is assigned to Mr. Wolf
    Then the agent receives a notification about the new ticket
  ```
- **[DON'T]**
  ```gherkin
  # Anti-pattern: Using UI/Technical details in behavior specs
  Scenario: User clicks submit
    Given the user fills the HTML form input "messageBox" with "Help"
    When the user clicks the "btn-submit" button to POST to the database
    Then the system inserts a record into the AgentTickets table
  ```