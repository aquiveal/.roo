# @Domain
Trigger these rules when the user requests the creation, restructuring, or evaluation of an application's layout, navigation scheme, routing logic, semantic HTML, or overall digital environment structure. These rules also activate when defining user roles, designing content feeds, or establishing the domain-specific nomenclature of a digital product.

# @Vocabulary
*   **Information Environment**: A digital context perceived by users as a distinct "place" (e.g., a bank, a hospital, a social network) where specific interactions and norms apply.
*   **Placemaking**: The deliberate use of semantic cues (labels, layouts, typography, menus) to signal the purpose, function, and behavioral expectations of a digital environment.
*   **Typology**: A standardized, culturally evolved structural pattern specific to a domain (e.g., the standard architectural layout of an e-commerce site or an airline booking system).
*   **Portico**: A structural or semantic element (such as top-level navigation) that serves as a clear, prioritized entrance to the most important parts of an information environment.
*   **Rhythm**: The structural pattern and pacing of information presentation (e.g., the density of search results, the continuous beat of a social media feed) that dictates how a user consumes data.
*   **Shearing Layers (Pace Layering)**: The concept that different parts of a system change at different rates. In digital architecture, the semantic structure (Structure) is slow-changing and stable, while the visual UI (Skin/Stuff) is fast-changing and ephemeral.
*   **Semantic Cues**: Linguistic and visual signs (headings, keywords, link labels) that frame information and orient the user.

# @Objectives
*   Ensure the AI generates environments where users immediately understand "where they are" and "what they can do" through the use of precise semantic cues.
*   Enforce the use of established domain typologies to aid user comprehension, preventing the reinvention of core navigational paradigms.
*   Architect systems using pace layering, decoupling highly volatile UI components from stable, underlying semantic routing and structural hierarchies.
*   Align the digital architecture strictly with the user's channel-specific intent, rather than blindly mirroring physical-world structures.
*   Define rigid, thematic nomenclature for user roles and actions to establish a coherent sense of place.

# @Guidelines
*   **Implement Placemaking via Semantic Cues**: The AI MUST design interfaces that use language (labels, headers) and structure to clearly define the "place." A banking app MUST use language that feels structurally distinct from a social media app.
*   **Adopt Domain Typologies**: When building an application for a recognized industry (e.g., airline, university, hospital), the AI MUST use the standard structural typology for that industry. Brand differentiation MUST be achieved through tone, visual styling, and micro-copy, not by altering the fundamental navigational schema.
*   **Design Structural Porticos**: The AI MUST highlight primary entry points using top-level hierarchical elements. Navigation menus MUST clearly elevate primary actions over secondary links, acting as the "portico" to the application.
*   **Establish Data Rhythm**: When designing feeds, lists, or search results, the AI MUST define a structural rhythm. The AI MUST adjust data density based on the environment (e.g., sparse, highly visual rhythms for media consumption; dense, data-rich rhythms for analytics dashboards).
*   **Apply Shearing Layers (Modularity)**: The AI MUST separate concerns based on their rate of change. Core routing and semantic HTML (Structure) MUST be decoupled from CSS/styling (Skin/Stuff). If a system requires sub-environments with different update cycles, the AI MUST architect them as modular, isolated components (e.g., separate subdomains or micro-frontends).
*   **Enforce Thematic Nomenclature**: The AI MUST establish and strictly adhere to specific nouns for user roles and behaviors that match the environment's theme (e.g., "Buyer/Seller" for marketplaces, "Guest/Host" for hospitality). Generic terms like "User" SHOULD be avoided in user-facing architecture.
*   **Adapt Architecture to Channel Intent**: The AI MUST NOT mirror physical geography in digital space if it conflicts with the user's digital intent. For example, a theme park's website MUST use a "travel and hospitality" typology (booking, hours, tickets) rather than organizing the website solely by the physical map of the park.

# @Workflow
1.  **Typology Identification**: Identify the industry or domain of the requested application. Retrieve and apply the standard structural typology (expected navigation headers, standard user flows) for that domain.
2.  **Nomenclature Definition**: Define the specific language and roles that will create the "Sense of Place." Map generic terms (user, item, post) to thematic terms (e.g., bidder, auction, listing).
3.  **Portico Establishment**: Define the top-level semantic structures (Main Navigation, Hero sections) that will serve as the primary entrances for the user's most critical tasks.
4.  **Layer Decoupling**: Architect the codebase to separate the slow-changing semantic structure (routing, content hierarchy, HTML semantics) from the fast-changing aesthetic layers (CSS, animations, ephemeral UI components).
5.  **Rhythm Calibration**: For any list, grid, feed, or search result view, define the component repetition strategy to establish a consistent interaction rhythm.
6.  **Contextual Validation**: Audit the proposed structure against the specific channel (e.g., mobile web vs. desktop). Adjust the hierarchy to match what the user specifically needs *in that specific digital context*.

# @Examples (Do's and Don'ts)

**Principle: Domain Typologies**
*   [DO]: Structure a university website with top-level navigation labels like "Admissions", "Academics", "Student Life", and "Alumni".
*   [DON'T]: Invent novel, ambiguous top-level navigation for a university such as "Knowledge Hub", "Onboarding", or "Life Journeys" which break the expected typology and confuse users.

**Principle: Adapting Architecture to Channel Intent**
*   [DO]: Architect a retail store's e-commerce website using a product-catalog typology (Browse by Category, Search, Cart, Checkout). 
*   [DON'T]: Architect the e-commerce website to mimic the physical layout of the brick-and-mortar store (e.g., "Aisle 1", "Aisle 2", "Checkout Register") because it ignores the digital user's intent to find items efficiently.

**Principle: Thematic Nomenclature**
*   [DO]: Use specific role labels in an auction application's routing and UI, such as `/bidders/dashboard` and `/sellers/listings`.
*   [DON'T]: Use generic, place-less nomenclature like `/users/dashboard` and `/users/items` which fails to reinforce the context of the environment.

**Principle: Shearing Layers (Modularity)**
*   [DO]: Define the primary navigation and semantic page structure in stable HTML/Routing files, utilizing a separate, easily swappable CSS/Theming system for visual design.
*   [DON'T]: Hardcode volatile visual design properties (like ephemeral promotional banners or highly specific seasonal colors) directly into the core application routing logic or primary architectural hierarchy.

**Principle: Establishing Rhythm**
*   [DO]: Design a news aggregation feed using a consistent, repeating card component structure that users can quickly scroll through, establishing a predictable "beat" of information consumption.
*   [DON'T]: Mix wildly disparate layout patterns (a massive hero image, followed by a tiny text link, followed by a horizontal carousel, followed by a dense data table) in a single linear feed without establishing a clear structural order.