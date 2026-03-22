@Domain
Triggers when the AI is tasked with generating, reviewing, or structuring developer resources, API documentation, developer portals, code samples, API tutorials, SDK/framework designs, API testing environments, or API community engagement materials.

@Vocabulary
- **Time to Hello World (TTHW):** The metric defining the easiest and fastest set of steps a developer must take to achieve initial success (e.g., making a first API request) using the "Getting Started" guide.
- **Getting Started Guide:** A primer document designed to walk a developer from unfamiliarity to initial success (minimizing TTHW) strictly following the "happy path."
- **Code Sample:** A comprehensive, highly readable, heavily commented block of code providing a reference example of how to use the API for a specific use case or integration, including necessary imports and declarations.
- **Reference App:** A specific type of code sample that tackles a full business use case rather than just demonstrating API functionality.
- **Snippet:** A short (single-digit lines of code), contextual code example embedded within tutorials or FAQs. It omits variable declarations and imports, appearing as if cut-and-pasted from a larger file.
- **SDK (Software Development Kit):** A thin abstraction layer over the API that provides developers with a code library in their native programming language, baking in best practices and security.
- **Framework:** An opinionated abstraction layer built over an API that encapsulates complex functionality and wraps business use cases (e.g., conversational bot interfaces) into an easy-to-use library.
- **Sandbox:** A safe, isolated environment (often using mocked data) where developers can test API calls without altering production data.
- **API Tester:** A UI tool (often built into documentation) allowing developers to execute API requests without writing code by inputting valid parameters.
- **Changelog:** A dedicated page or RSS feed notifying developers of API updates, breaking changes, and security/service notifications.

@Objectives
- Minimize the "Time to Hello World" (TTHW) by designing frictionless, happy-path onboarding experiences.
- Produce comprehensive, standalone API reference documentation that repeats shared contexts (like error codes) to eliminate cross-referencing friction.
- Abstract API complexity by generating native, language-specific SDKs and opinionated frameworks that enforce best practices by default.
- Enhance developer productivity by providing segmented learning materials: tutorials for step-by-step guidance, snippets for context, and reference apps for business logic.
- Ensure all resources (docs, code samples, SDKs) are treated as tightly coupled dependencies that MUST be updated synchronously whenever the API changes.

@Guidelines

**API Documentation & Landing Pages**
- The AI MUST structure the Developer Landing Page to include exactly three core elements: 1) A short explanation of the API's value proposition and use cases; 2) A clear call-to-action (e.g., "Get Started"); 3) Links to key resources, tools, and samples.
- The AI MUST design SEO-optimized structures so documentation is highly discoverable via search engines.
- The AI MUST dedicate a single, independent page for each API method in the Reference Documentation to improve discoverability.
- The AI MUST repeat common information (e.g., generic error codes) across multiple API method pages. Developers do not read docs in sequence; every page must be standalone.
- The AI MUST structure the FAQ by generalizing and anonymizing real-world support inquiries. Format strictly with the question in bold (or prefixed with "Q:") and the answer directly below (or prefixed with "A:").
- The AI MUST include a Changelog with an RSS feed option for all API version updates, breaking changes, and security notices.

**Getting Started Guides**
- The AI MUST NEVER assume prior knowledge. Every technical term must be explained or linked to a prerequisite document.
- The AI MUST strictly adhere to the "happy path." Do not clutter the primary steps with edge cases. Instead, provide a distinct link to troubleshooting documentation for errors.
- The AI MUST show concrete examples of both inputs (e.g., command-line execution) and expected outputs (e.g., JSON response payloads or screenshots).
- The AI MUST end every Getting Started guide with a call-to-action directing the user to the next logical learning resource.

**Code Samples & Snippets**
- The AI MUST differentiate between Snippets and Code Samples. 
- When generating Snippets: Restrict to single-digit lines of code. Omit imports and variable declarations. Provide variations using an interactive language switcher.
- When generating Code Samples: Provide complete, runnable code in the developer's preferred language. Include thorough, step-by-step explanatory comments.
- When generating Reference Apps: Ensure the app is not *too* tightly optimized for the specific use case, allowing developers to easily extrapolate the logic for their own needs.

**SDKs & Frameworks**
- The AI MUST ensure SDK interfaces are highly readable and documented, even if the underlying internal implementation is obfuscated, minified, or complex.
- The AI MUST bake security best practices, rate-limiting handlers, and pagination handlers directly into the SDK/Framework boilerplate.
- The AI MUST prescribe updating SDKs synchronously alongside any API changes to prevent version drift.
- The AI MUST recommend tracking/instrumenting SDK usage independently from direct API calls to measure SDK adoption.

**Developer Tools & Rich Media**
- The AI MUST recommend or mock up interactive API Testers within the documentation that allow parameter input without requiring the user to write code.
- The AI MUST ensure video scripts or outlines are kept short (under 2 minutes) to prevent viewership drop-off.
- The AI MUST integrate troubleshooting and debugging tools (e.g., API log viewers) directly into the developer portal architecture.

**Terms of Service (ToS)**
- The AI MUST draft ToS sections that are short, simple, and readable.
- The ToS MUST cover: Rate limits, data retention policies, privacy policies (PII handling), non-allowed use cases (e.g., commercial, adult), API licensing, and application requirements (e.g., privacy acknowledgments).

**Community Contribution**
- The AI MUST include sections in the documentation architecture for community-contributed content (tutorials, SDK patches).
- The AI MUST ensure contributors receive explicit credit for their submissions.
- The AI MUST add version-compatibility tags to all community-contributed content.

@Workflow
1. **Analyze Developer Context & Onboarding:** Identify the target developer segment, their primary language, and the core use cases. Define the shortest path to a successful "Hello World" (TTHW).
2. **Generate Landing Page & ToS:** Draft a welcoming landing page with a clear value proposition, a "Get Started" CTA, and a short, legally sound Terms of Service defining usage boundaries.
3. **Draft the Getting Started Guide:** Write a strictly "happy path" tutorial. Provide exact input/output examples, explain all terminology, and link to external troubleshooting.
4. **Compile Reference Documentation:** Generate standalone pages for every API method. Inject interactive API testers or mockups. Repeat shared context (like errors) on every applicable page.
5. **Create Code Resources:**
   - Write short, contextual *Snippets* for inline documentation (no imports).
   - Write comprehensive *Code Samples* and *Reference Apps* (fully runnable, heavily commented).
6. **Abstract via SDKs/Frameworks:** Design native libraries that wrap complex workflows, rate limiting, and security best practices into simple functions.
7. **Establish Maintenance & Community Loops:** Generate a Changelog structure, establish an FAQ ingestion format (from support tickets), and create templates for community contributions with attribution guidelines.

@Examples (Do's and Don'ts)

**Getting Started Guides**
- [DO]: "Step 1: Execute this command to fetch your user profile. We assume your API key is valid. If you receive an error, please see our [Troubleshooting Guide](#). \n `curl -H 'Authorization: Bearer YOUR_KEY' https://api.example.com/me` \n Expected Output: `{ "id": "123", "name": "Jane" }`"
- [DON'T]: "Step 1: Execute the curl command. Note that if your key is expired, you will get a 401. If your user is deleted, you will get a 404. If you are rate limited, you will get a 429. Here is how to handle all of those..." (Violates the happy path rule).

**Snippets vs Code Samples**
- [DO] (Snippet in a tutorial): 
  ```javascript
  // Fetch user profile
  apiClient.getUser(userId).then(user => console.log(user.name));
  ```
- [DON'T] (Snippet in a tutorial): 
  ```javascript
  const ApiClient = require('api-client');
  const apiClient = new ApiClient('YOUR_API_KEY');
  let userId = '12345';
  apiClient.getUser(userId).then(user => console.log(user.name));
  ```
  *(Anti-pattern: Snippets should be single-digit lines omitting boilerplate declarations/imports. Leave boilerplate for full Code Samples).*

**Reference Documentation Structure**
- [DO]: Create `/docs/methods/get-user` and `/docs/methods/create-user`. On BOTH pages, explicitly list the definition for `401 Unauthorized` and `429 Too Many Requests`.
- [DON'T]: Create `/docs/methods/get-user` and write "For error codes, please click here to go to the global errors page." (Violates the standalone page rule).

**FAQ Formatting**
- [DO]: 
  **Q: How do I refresh my access token?**
  A: You can refresh your token by calling the `/oauth/refresh` endpoint with your `refresh_token` payload.
- [DON'T]: 
  "John from ACME Corp asked us how to refresh his token yesterday. To do this, you just hit the refresh endpoint." (Violates the rule to generalize and anonymize FAQs).