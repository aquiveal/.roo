# @Domain
These rules MUST trigger whenever the AI is tasked with designing data structures, planning cross-channel user experiences (web, mobile, IoT), organizing application content, defining navigation systems, restructuring legacy software, or establishing the foundational architecture for any interactive, information-dense product or ecosystem.

# @Vocabulary
- **Dematerialization:** The decoupling of information from its physical or specific digital container, allowing it to exist and be interacted with across multiple channels simultaneously.
- **Information Overload:** A state characterized by a diminished signal-to-noise ratio due to excessive information availability, requiring architectural intervention to restore findability.
- **Contextual Proliferation:** The rapid expansion of contexts, physical environments, and devices (desktop, smartphone, wearable, ambient IoT) through which users access information.
- **Places Made of Information:** The psychological framework wherein users perceive digital experiences as physical places, constructed entirely out of language, labels, menus, and visual semantics.
- **Pervasive Information Architecture:** An architectural approach that maintains internal consistency (serving specific contexts) and external consistency (preserving logic across different media, environments, and uses).
- **Semantic Structure:** The underlying, abstract organization and taxonomy of information that remains invariant and consistent, regardless of the specific UI or channel instantiation.
- **Systems Thinking:** A design philosophy that prioritizes the relationships, flows, and interactions between components ("arrows") over the isolated components themselves ("boxes").
- **Structural Coherence:** The high-level invariant logic that ties an entire ecosystem together.
- **Suppleness:** The low-level flexibility that allows invariant structures to adapt gracefully to specific device constraints.
- **Cathedral vs. Garage Fallacy:** The architectural error of failing to align the system's complexity with its actual purpose (e.g., over-engineering a simple utility tool, or under-engineering a massive media ecosystem).

# @Objectives
- The AI MUST make all information within the system highly findable and deeply understandable, regardless of the user's entry point or device.
- The AI MUST design systems that mitigate information overload by structuring data conceptually before applying interface-level treatments.
- The AI MUST establish internal and external consistency across all interaction channels (omni-channel coherence).
- The AI MUST elevate its design approach from building isolated artifacts ("boxes") to defining interconnected ecosystems ("arrows").

# @Guidelines

- **Dematerialization Rule:** When defining data models or content schemas, the AI MUST strictly decouple the information payload from its presentation layer or delivery container. Data MUST be structured abstractly so it can flow seamlessly into a web browser, a mobile app, or an ambient voice interface without requiring restructuring.
- **Contextual Adaptation Constraint:** When designing multi-device experiences, the AI MUST NOT dictate identical user interfaces across devices. Instead, the AI MUST dictate identical *Semantic Structures* while adapting the physical interaction paradigm to the specific device's constraints (e.g., adapting a desktop mega-menu into a mobile sequential drill-down while retaining identical category labels and hierarchy).
- **Ecosystem Coherence (Anti-iTunes) Rule:** When expanding a simple feature into a broader ecosystem, the AI MUST explicitly define unified categorization schemes and business rules. The AI MUST strictly avoid mixing disparate data types (e.g., songs, apps, university lectures) in a single unified view without clear semantic framing and distinct, non-competing filtering mechanisms.
- **Information Placemaking:** When generating UI text, navigation menus, or system terminology, the AI MUST select language that deliberately frames the user's environment. The AI MUST use consistent, context-setting nouns and verbs that allow the user to immediately identify the "place" they are in (e.g., a banking environment vs. a medical environment).
- **Systems Thinking Mandate:** When architecting a new feature, the AI MUST explicitly declare how that feature influences and interacts with existing systems. The AI MUST define the "arrows" (data flows, user journeys, contextual links) before defining the "boxes" (the specific screens or databases).
- **The Scale Verification Check:** Before proposing an architectural solution, the AI MUST ask and answer the Cathedral vs. Garage question: "Is this task building a simple, discrete tool (Garage), or a multi-faceted, evolving ecosystem (Cathedral)?" The AI MUST restrict its structural complexity to match the answer.

# @Workflow
1. **Scale and Intent Definition:** The AI MUST begin by explicitly declaring whether the project is a "Garage" (simple, single-purpose tool) or a "Cathedral" (complex, multi-channel ecosystem).
2. **Ecosystem Mapping:** The AI MUST map the complete ecosystem, identifying all distinct content types, user contexts, and channels of interaction (e.g., web, iOS, smartwatch, voice).
3. **Semantic Abstraction:** The AI MUST define the high-level invariant Semantic Structure (taxonomies, hierarchies, core labels) completely independent of any specific UI or device screen.
4. **Channel Instantiation:** For each identified channel, the AI MUST translate the abstract Semantic Structure into a device-specific execution, prioritizing "Suppleness" (low-level flexibility) while ensuring "Structural Coherence" (high-level invariance).
5. **Placemaking Audit:** The AI MUST review all generated labels, categories, and menus to ensure they project a unified, unambiguous digital "place" that guides user understanding.
6. **Cross-Pollination Check:** The AI MUST draw arrows between the distinct system components to define how context and state carry over when a user transitions from one channel or feature to another.

# @Examples (Do's and Don'ts)

### Principle: Dematerialization and Semantic Abstraction
**[DO]**
Define data structures abstractly, separating the core information from the device-specific presentation wrapper.
```json
// Semantic Structure (Device Agnostic)
{
  "entity": "media_item",
  "id": "10485",
  "semantics": {
    "title": "Sgt. Pepper's Lonely Hearts Club Band",
    "creator": "The Beatles",
    "classification": ["Music", "Rock", "Classic"]
  },
  "presentations": {
    "desktop_web": {"layout": "grid_view", "interaction": "hover_play"},
    "mobile_app": {"layout": "list_row", "interaction": "swipe_menu"},
    "voice_ui": {"spoken_prompt": "Playing Sgt. Pepper by The Beatles"}
  }
}
```

**[DON'T]**
Hardcode device-specific containers directly into the foundational data model, preventing cross-channel coherence.
```json
// Anti-pattern: Tied directly to the container
{
  "web_page_div_id": "album_box_10485",
  "html_title_string": "<b>Sgt. Pepper</b>",
  "onclick_route": "/play/10485"
}
```

### Principle: Cathedral vs. Garage (Preventing the iTunes Anti-Pattern)
**[DO]**
When a system outgrows its original problem set, intentionally define separate, contextually appropriate spaces (Information Places) for disparate tasks, maintaining strict semantic boundaries.
*Architecture:*
- Sub-system A (Music): Organized by Artist, Album, Genre. Primary action: "Play".
- Sub-system B (Software Apps): Organized by Platform, Productivity, Games. Primary action: "Install".
- *Cross-system connection:* A unified user profile, but strictly separated semantic environments to prevent search result pollution.

**[DON'T]**
Graft fundamentally different concepts onto a simple tool without systemic restructuring.
*Anti-pattern:* Dumping "Movies", "Podcasts", "PDF Lectures", and "Software Applications" into a single list view originally designed for 40-minute audio albums, resulting in broken business rules and a confused user mental model.

### Principle: Coherence Across Channels
**[DO]**
Adapt the interaction while maintaining the exact same Information Architecture structure.
*Web:* A horizontal top navigation bar with labels: `[ Checking ] [ Savings ] [ Mortgages ] [ Wealth ]`
*Smartwatch:* A vertical, swipeable stack of cards containing the exact same labels: `[ Checking ] -> [ Savings ] -> [ Mortgages ] -> [ Wealth ]`

**[DON'T]**
Change the semantic categorization simply because the screen size changed.
*Anti-pattern:*
*Web:* `[ Checking ] [ Savings ] [ Mortgages ]`
*Smartwatch:* `[ My Money ] [ House Stuff ]` (Breaks external consistency; user must relearn the system's language).