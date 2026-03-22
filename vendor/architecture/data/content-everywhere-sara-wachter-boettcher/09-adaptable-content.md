# @Domain
These rules are activated when the AI is engaged in tasks involving responsive web design, adaptive web design, front-end architecture, mobile optimization, CSS layout restructuring, viewport-based UI refactoring, or content strategy implementation across multiple devices.

# @Vocabulary
*   **Adaptive Design:** An approach extending progressive enhancement where an interface adapts to a user's device utilizing markup, JavaScript, and assistive technology support, often using distinct templates or conditional loading based on device capabilities.
*   **Responsive Design:** An approach utilizing fluid grids, flexible images, and CSS3 media queries to allow a single layout to resize and reflow dynamically across various viewport widths.
*   **Flexbox (Flexible Box Layout Module):** A CSS specification used to create and nest flexible content boxes, critical for providing source-order independence (changing the visual order of items without changing HTML structure).
*   **Grid Layouts:** A CSS specification that divides space into columns and rows, allowing elements to be rearranged predictably across different display sizes.
*   **Interdigitation (Intermixing):** The practice of folding or weaving secondary content modules (like sidebars or related links) into the logical narrative breaks of main content on smaller screens, rather than simply stacking them at the bottom of the page.
*   **AppendAround:** A JavaScript pattern/technique (pioneered by Filament Group) that creates multiple containers for a single piece of content and uses CSS media queries to determine which container the content is injected into at different breakpoints.
*   **Content Layering:** A UI strategy for small screens where dense content (like long reviews or deep navigation) is visually minimized but kept accessible behind a tap (e.g., accordions, expand/collapse toggles, or sub-pages) to aid scannability.
*   **AJAX Include Pattern:** A conditional loading technique where mandatory core content loads quickly without JavaScript, and secondary/layered content is fetched asynchronously only when requested or when device capabilities allow.
*   **Lazy Loading:** Conditionally loading heavy assets or non-critical content only when needed, to optimize initial page weight.
*   **Platform-Agnostic Content:** The principle that all core content must be equally accessible to all users regardless of the device they are using.
*   **Platform-Aware Experience:** Enhancing the presentation of platform-agnostic content by utilizing device-specific hardware capabilities (e.g., GPS, touch screens, accelerometers).

# @Objectives
*   Achieve true content parity across all devices; never artificially restrict or remove content based on assumptions about mobile user intent.
*   Preserve the narrative flow, hierarchy, and persuasive structure of content at every breakpoint through semantic reflowing and interdigitation.
*   Optimize performance and page weight for mobile contexts without sacrificing content availability, utilizing conditional loading and layering.
*   Transition from rigid, page-based layout thinking to flexible, systematic, component-based content architecture.

# @Guidelines
*   **Content Parity is Mandatory:** The AI MUST NOT remove, hide (via `display: none`), or strip out content for mobile viewports based on assumptions (e.g., "mobile users are on the go and want less info"). Mobile users MUST receive the complete content experience.
*   **Avoid Mindless Stacking:** When adapting multi-column desktop layouts for single-column mobile viewports, the AI MUST NOT default to simply pushing sidebars and asides to the absolute bottom of the DOM. 
*   **Implement Interdigitation:** The AI MUST map secondary content chunks (calls to action, quick facts, related items) and weave them intelligently *between* paragraphs or sections of the primary content flow using CSS or JS patterns.
*   **Utilize Source-Order Independence:** The AI MUST utilize CSS Flexbox (specifically the `order` property) or CSS Grid Layouts to change the visual prioritization of content elements at different breakpoints while maintaining a logical, accessible HTML source order.
*   **Apply Content Layering:** To prevent infinitely long mobile pages, the AI MUST layer dense or secondary content (e.g., lengthy product reviews, exhaustive navigation) behind tap-based UI patterns (collapsible panels, tabs, or deep-links), keeping the content accessible but not visually overwhelming.
*   **Use Conditional and Lazy Loading:** The AI MUST implement AJAX include patterns or lazy loading for heavy media (large images, embedded videos) and deeply layered content. Core text content must load immediately; heavy assets should load conditionally.
*   **Eliminate Non-Communicative Cruft:** The AI MUST evaluate the communicative value of visual elements. Purely decorative, bandwidth-heavy assets (e.g., generic 1MB stock photos that add no meaning) MUST be aggressively flagged for removal or replaced with lightweight alternatives to respect user bandwidth.
*   **Leverage Platform-Aware Enhancements:** While content remains agnostic, the AI MUST suggest or implement device-specific UX enhancements (e.g., swapping a static map for a location-aware GPS routing feature on mobile) when appropriate.
*   **Design for Dynamic Containers:** The AI MUST write CSS and JS that allows content chunks to adapt to the size of their parent container (using relative units, fluid typography, and max-widths) rather than relying on fixed-pixel dimensions.

# @Workflow
1.  **Content Chunking & Audit:** Break down the existing page into discrete, semantic content modules (e.g., Headline, Body Text, Pull Quote, Call to Action, Sidebar/Related Links).
2.  **Priority & Narrative Mapping:** Determine the relative importance of each module. Identify exactly where secondary modules (like a "Buy Now" button or "Quick Facts") logically belong within the narrative flow of the main content.
3.  **Mobile-First Core Assembly:** Construct the mobile layout first. Ensure 100% of the content is present in the HTML.
4.  **Layering Strategy:** Identify dense chunks (e.g., long lists of user reviews). Wrap these in expand/collapse UI components (like `<details>`/`<summary>`) to preserve vertical screen space.
5.  **Interdigitation Execution:** Apply CSS Flexbox/Grid or the JavaScript `AppendAround` pattern to shift the physical rendering of secondary chunks so they appear intertwined with the main content at specific breakpoints.
6.  **Performance Optimization:** Implement lazy loading for images. Use AJAX include patterns to defer the loading of hidden, layered content until the user interacts with the expand trigger.
7.  **Platform Enhancement:** Assess if HTML elements can be augmented with device APIs (e.g., adding `tel:` links to phone numbers, hooking into geolocation for addresses).

# @Examples (Do's and Don'ts)

*   **Content Parity vs. Assumption-Based Removal:**
    *   [DON'T] Use `@media (max-width: 768px) { .product-specs { display: none; } }` to hide detailed technical specifications from mobile users.
    *   [DO] Use a collapsible accordion: `<details><summary>Technical Specifications</summary><div class="product-specs">...</div></details>` so the mobile user can choose to view the content.

*   **Mindless Stacking vs. Interdigitation:**
    *   [DON'T] Allow a critical sidebar containing a "Purchase Options" block to naturally fall to the very bottom of the page, underneath 3,000 words of article text, simply because the screen narrowed.
    *   [DO] Use CSS Flexbox (`order: -1`) or a DOM-moving JavaScript pattern to inject the "Purchase Options" block immediately after the first introductory paragraph on mobile screens.

*   **Heavy Assets vs. Lightweighting:**
    *   [DON'T] Force a mobile browser on a 3G connection to download a 2MB decorative banner image of a generic landscape.
    *   [DO] Use responsive `<picture>` elements, `srcset`, or media queries to load a tiny, optimized image, or omit the purely decorative image entirely if it serves no communicative purpose.

*   **Static vs. Platform-Aware:**
    *   [DON'T] Serve a static JPG map of a campus to a smartphone user without providing an interactive alternative.
    *   [DO] Provide the static map as a fallback, but detect mobile capabilities and offer a button that launches the native mapping application using geolocation for turn-by-turn directions.