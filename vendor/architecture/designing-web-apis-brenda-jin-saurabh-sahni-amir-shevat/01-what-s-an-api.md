# @Domain
These rules MUST trigger when the AI is tasked with conceptualizing, designing, reviewing, or documenting Web Application Programming Interfaces (APIs), including drafting API specifications, mapping business logic to API endpoints, determining API architecture, or defining API user stories and personas.

# @Vocabulary
- **API (Application Programming Interface)**: The interface that a software program presents to other programs, humans, and the internet. It acts as the building blocks for interoperability.
- **Developer Persona**: The specific type of human user (e.g., frontend web developer, backend enterprise developer) who will interact with the API. 
- **Switching Cost**: The extremely high effort and friction required for developers to migrate from one API design to another after implementation.
- **Service Integration**: Products or applications built on top of an API that supplement or interact with a core SaaS platform.
- **Internal-First API**: An API originally built for a company's own developers (web/native clients) that is later exposed to external, third-party developers. 
- **External-First API**: An API built primarily for external third-party integrators that may later be adopted by internal developers.
- **API-as-a-Product**: A business model where the API *is* the sole core product offering (e.g., Stripe, Twilio).
- **Hackability**: The ability for developers to pick up the API quickly through iteration, experimentation, and clear design.
- **Payload Creep**: The tendency for API responses to grow excessively large over time to accommodate diverse needs, often leading to the adoption of flexible query interfaces like GraphQL.

# @Objectives
- **Prioritize the Human Interface**: Treat the API not just as machine-to-machine communication, but as a user interface specifically designed to be understood and used by humans writing programs.
- **Prevent Switching Costs**: Enforce rigorous specification and validation of the API *before* any implementation code is written.
- **Ensure Business Alignment**: Actively align the API's design and existence with the core business model, preventing the creation of APIs that cannibalize core revenue (e.g., ad-driven platforms).
- **Design for the Persona**: Tailor the API's structure, payload, and complexity to the exact needs of the targeted developer persona.
- **Guarantee the Five Pillars of Greatness**: Ensure every API possesses Clarity, Flexibility, Power, Hackability, and comprehensive Documentation.

# @Guidelines

- **Interface Optimization**: When designing API responses and requests, the AI MUST prioritize human readability, predictability, and developer ergonomics over strict machine-level optimizations. 
- **The "Reinventing the Wheel" Check**: When encountering requests to build supplementary features (e.g., mapping, payments, login), the AI MUST recommend using specialized third-party APIs (e.g., Google Maps, Stripe, Facebook Login) rather than generating custom code, unless explicitly overridden by the user.
- **Persona-Driven Design**: Before drafting an API structure, the AI MUST request or infer the target developer persona.
  - *If the persona is a frontend developer*, the AI MUST design payloads that are ready for UI rendering with minimal transformation.
  - *If the persona is a backend enterprise developer*, the AI MUST prioritize auditability, structured error handling, and policy compliance in the API design.
- **Specification Before Implementation**: To avoid high switching costs, the AI MUST refuse to write backend implementation code for new APIs until a structured API specification (e.g., OpenAPI/Swagger or GraphQL schema) has been generated and approved by the user.
- **Business Alignment Validation**: When proposing an API strategy, the AI MUST analyze the core business model. If the API risks driving traffic away from a primary monetization channel (e.g., alternative clients for an ad-hosted platform), the AI MUST issue a strategic warning.
- **Architectural Audience Constraints**: The AI MUST adapt its architectural recommendations based on the API's origin strategy:
  - *When designing Internal-First APIs (e.g., Slack model)*: The AI MUST warn of the tension between internal flexibility (fast feature iteration) and external stability (backward compatibility), enforcing strict versioning boundaries to protect third-party apps.
  - *When designing External-First APIs (e.g., GitHub model)*: The AI MUST anticipate payload creep. If payloads become excessively large to serve diverse external needs, the AI MUST recommend transitioning from REST to a query interface like GraphQL to isolate performance bottlenecks.
  - *When designing API-as-a-Product (e.g., Stripe model)*: The AI MUST enforce the highest standards of backward compatibility, documentation, and seamless onboarding, as the API directly dictates revenue.
- **The Five Pillars Check**: When reviewing an existing API design, the AI MUST evaluate it against:
  1. *Clarity*: Is the purpose, design, and context obvious?
  2. *Flexibility*: Can it adapt to different use cases?
  3. *Power*: Does it offer a complete solution to the problem?
  4. *Hackability*: Can a developer iterate and experiment with it quickly?
  5. *Documentation*: Is the usage completely self-evident or well-documented?

# @Workflow
When tasked with designing or modifying an API, the AI MUST follow this exact sequence:

1. **Discovery & Alignment**: 
   - Identify the core business model.
   - Define the primary target developer persona (Internal vs. External, Frontend vs. Backend).
   - Evaluate if the API solves a domain-specific problem or if an existing third-party API should be used instead.
2. **Audience Strategy Mapping**:
   - Categorize the API as Internal-First, External-First, or API-as-Product.
   - Apply the corresponding architectural constraints (e.g., strict stability for External-First; payload optimization for Internal-First).
3. **Specification Drafting**:
   - Generate a rigorous, human-readable specification (e.g., OpenAPI JSON/YAML or GraphQL Schema).
   - Optimize endpoint names, payload structures, and parameters for *Hackability* and *Clarity*.
4. **Validation Pause**:
   - Present the specification to the user.
   - Explicitly require user approval, citing the "high switching costs" of altering an API post-implementation.
5. **Implementation**:
   - Only after specification approval, generate the underlying backend code, ensuring strict adherence to the agreed-upon interface contract.

# @Examples (Do's and Don'ts)

**Persona-Driven Payload Design**
- [DO]: Design tailored responses for specific personas. For a frontend UI developer: `{"artist_name": "Jane Doe", "portfolio_images": ["url1", "url2"]}`.
- [DON'T]: Dump raw, relational database models that force the consumer to perform complex joins: `{"user_id": 45, "entity_type": "artist", "assets": [{"asset_id": 99, "type": "image"}]}`.

**Specification vs Implementation**
- [DO]: Output a complete OpenAPI YAML contract detailing routes, request bodies, and exact response schemas, asking the user to confirm the interface before generating the Express/Node.js backend.
- [DON'T]: Immediately write server routing code and database controllers without establishing the human-facing interface contract first.

**Business Alignment**
- [DO]: For an API-as-a-Product request, include infrastructure for API key generation, strict usage metering, and robust error definitions directly in the initial design.
- [DON'T]: Design an API that bypasses the core platform's ad-rendering engine without explicitly warning the user that this violates the core business model.

**Handling Payload Creep (External-First)**
- [DO]: Suggest implementing GraphQL or sparse fieldsets (e.g., `?fields=name,email`) when an external-facing API's JSON response grows too large due to varying integrator requirements.
- [DON'T]: Continuously add new, deeply nested objects to a single REST endpoint's default response to satisfy every edge-case developer request.