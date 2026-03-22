# @Domain
Trigger this rule file when the user request involves system architecture, project planning, requirements gathering, ontology creation, terminology standardization, structural mapping, or moving a project from the conceptual phase ("why") to the definition phase ("what").

# @Vocabulary
- **Object**: A specific, material thing.
- **Interface**: A point where a user affects an object or location.
- **Location**: A particular place or position.
- **Journey**: The steps taken within or between locations.
- **Structure**: A configuration of objects and locations.
- **System**: A set of structures working together.
- **Ecosystem**: A collection of related systems.
- **Place**: A space deliberately designated and arranged for a specific purpose (Placemaking).
- **Space**: An open, free, or unoccupied area between places where users dictate their own actions.
- **Placemaking**: The act of choreographing a sequence of steps and encoding intent through clues so users know what to do in a specific area.
- **Linguistic Insecurity**: The anxiety or frustration caused by misunderstood language, jargon, or fear that language will not conform to a context.
- **Ontology**: The explicit declaration of what a word or concept means within a specific project context.
- **Controlled Vocabulary**: An organized, documented list of terms to use ("Words We Say") and terms explicitly banned ("Words We Don't Say").
- **Requirement**: A concrete statement formed strictly by combining Nouns (objects/actors) and Verbs (actions) that describes a desired result without outlining the mechanism to achieve it.
- **Noun**: Represents the objects, people, and places involved in a mess.
- **Verb**: Represents the actions that can be taken (which cannot exist without nouns).

# @Objectives
- Move the project incrementally from understanding *why* change is needed to explicitly defining *what* will be built.
- Eliminate linguistic insecurity by forcing absolute clarity, establishing a shared ontology, and aggressively untangling acronyms, jargon, and homographs.
- Formulate requirements strictly as implementation-agnostic noun-verb relationships.
- Guarantee that any architectural decision explicitly defines the scale it operates on (from Object to Ecosystem) and accounts for cascading effects on adjacent levels.

# @Guidelines
- **Prevent Paralysis:** The AI MUST prioritize choosing a single, incremental direction over presenting an overwhelming list of choices. Progress outweighs perfection.
- **Enforce Structural Levels:** The AI MUST explicitly declare which structural level it is working at (Object, Interface, Location, Journey, Structure, System, or Ecosystem).
- **Analyze Cascading Impacts:** When a decision is made at one level, the AI MUST analyze and document its ripple effects on the levels above and below it. 
- **Define Places vs. Spaces:** The AI MUST differentiate between "Places" (areas with prescribed, choreographed tasks) and "Spaces" (open, flexible areas). The AI MUST NOT over-constrain Spaces.
- **Eradicate Accidental Synonyms:** The AI MUST group terms with similar meanings and force the selection of a single, definitive term to be used across the project.
- **Construct the "Words We Say" List:** The AI MUST document approved terms, including acceptable synonyms, variant spellings, tone, and specific acronym rules.
- **Construct the "Words We Don't Say" List:** The AI MUST document forbidden terms that misalign with intent, conflict with user mental models, carry historical/cultural baggage, or introduce homographic ambiguity.
- **Execute Nested Definitions (The Outsider Rule):** When defining a term, the AI MUST write the simplest definition possible, identify/extract any complex or domain-specific words *within* that definition, and recursively define those extracted words.
- **Capture Term Context:** For every core term, the AI MUST document its "History" (how it changed over time), "Myths" (how it is commonly misunderstood), and "Alternatives" (accidental synonyms).
- **Enforce Noun-Verb Requirements:** The AI MUST construct system requirements ONLY by identifying the project's core Nouns (actors/objects) and mapping them to appropriate Verbs (actions). 
- **Strip Options and Opinions from Requirements:** The AI MUST formulate "Strong Requirements." Strong requirements define the result without dictating the *how* (options/mechanisms, e.g., "button", "click") and without introducing subjective measurements (opinions/adverbs, e.g., "easily", "quickly", "seamlessly").
- **Acknowledge Reality:** The AI MUST filter plans through the realistic constraints of time and resources. The AI MUST NOT fall in love with unbuildable ideal plans.

# @Workflow
When tasked with defining a project's direction, terminology, or requirements, the AI MUST follow this rigid, step-by-step algorithmic process:

1. **Level Assessment:** 
   - Identify and explicitly state the structural level of the target entity (Object, Interface, Location, Journey, Structure, System, or Ecosystem).
   - List the immediate upward (macro) and downward (micro) levels that will be impacted by changes.
2. **Terminology Extraction:** 
   - Extract all nouns (objects, people, places) and verbs (actions) from the user's prompt.
   - Group similar terms. Flag all acronyms, jargon, and potential homographs.
3. **Ontology & Vocabulary Generation:**
   - Output a `[Controlled Vocabulary]` section.
   - Define a "Words We Say" list with strict definitions using the "Nested Definitions" rule (defining complex words used within the definition).
   - Document the History, Myths, and Alternatives for the top 3 core nouns.
   - Define a "Words We Don't Say" list, explicitly banning problematic terms and explaining why.
4. **Requirement Synthesis:**
   - Map approved Nouns to approved Verbs.
   - Output a `[Requirements]` section consisting strictly of Strong Requirements (Subject + Action + Object).
   - Strip all UI-specific mechanisms (buttons, screens, clicks) and subjective adverbs (easily, beautifully) from the requirements.
5. **Cascading Impact Review:**
   - Output a `[Reality Check]` section detailing how the new requirements will practically affect the adjacent structural levels, noting resource or time constraints that might impede progress.

# @Examples (Do's and Don'ts)

**Principle: Formulating Strong Requirements**
- **[DO]:** "An author can publish an article." / "A user can read a post." / "A customer can request a refund."
- **[DON'T]:** "A user is able to easily publish an article with one click of a button." (Violates rules by including an opinion ["easily"] and dictating the interface/option ["one click of a button"]).

**Principle: Nested Definitions (The Outsider Rule)**
- **[DO]:** 
  - *Tree*: A plant that grows from the ground.
    - *Plant*: A living organism that absorbs water and inorganic substances.
    - *Grow*: To undergo natural development by increasing in size.
    - *Ground*: The solid surface of the earth.
- **[DON'T]:** 
  - *Tree*: A perennial woody plant with a trunk and branches. (Fails to define "perennial", "woody", "trunk", and "branches").

**Principle: Cascading Impacts across Structural Levels**
- **[DO]:** "Change: Eliminate paper napkins to be environmentally friendly. Level: Object. Impact on Ecosystem/System: We must define a new process for where dirty cloth napkins go, how they are collected, cleaning frequency, required inventory, and emergency protocols for dining room spills."
- **[DON'T]:** "Let's swap paper napkins for cloth napkins at the tables." (Fails to consider the cascading workflow, maintenance, and system impacts of the object-level change).

**Principle: Controlled Vocabulary (Words We Don't Say)**
- **[DO]:** 
  - *Words We Say*: Customer, Subscribe, Post.
  - *Words We Don't Say*: "User" (too generic for our business context), "Hit" (carries violent or ambiguous baggage), "Asset" (defined differently across three internal teams; too ambiguous).
- **[DON'T]:** 
  - "We will use the terms Customer, User, and Client interchangeably." (Creates linguistic insecurity and accidental synonyms).