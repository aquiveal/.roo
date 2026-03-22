# @Domain
These rules MUST be triggered whenever the AI is tasked with designing or implementing content management systems (CMS), front-end layout architectures, responsive web designs, headless CMS data models, API content delivery payloads, or programmatic UI components that handle dynamic content display. 

# @Vocabulary
*   **Art Direction via Metadata**: The practice of using a content element's structural attributes and metadata to programmatically determine its visual presentation and layout, rather than manually designing individual pages.
*   **Rules (Conditions)**: Logical *if-then* statements that dictate how, when, and where a specific content module will occur or be displayed based on context, viewport, or user state.
*   **Content System**: An interconnected ecosystem of content types governed by standardized rules, shared attributes, and logical relationships, rather than manual curation.
*   **Freeform Tags**: An anti-pattern of metadata consisting of unstructured, user-generated keywords (often visualized as tag clouds). Unreliable for rule-building due to inconsistency.
*   **Semantic Elements / Intrinsic Attributes**: Meaningful, inherent chunks of a content model (e.g., *publication date*, *author*, *location*, *price*, *tasting notes*) used as the reliable foundation for business rules.
*   **Taxonomy**: A fixed, controlled vocabulary used to classify content, providing a stable foundation for programmatic logic.
*   **Rule-Making Framework**: A tri-fold evaluation process for every content element consisting of:
    1.  **Meaning**: What the element contributes to the whole and what is lost if it is removed.
    2.  **Priority**: The element's relative importance to business goals and user tasks.
    3.  **Relationships**: How the element interacts with others (Hierarchical, Interdependent, or Complementary).
*   **Hierarchical Relationship**: A parent-child connection between content elements.
*   **Interdependent Relationship**: Content elements that cannot be logically split (e.g., an image and its specific caption).
*   **Complementary Relationship**: Elements that act as "friends" or sidebars; related but capable of existing independently.

# @Objectives
*   Transition architectural focus from designing fixed, manual page layouts to designing dynamic, rule-based content systems.
*   Ensure all responsive design reflows are dictated by content priority and relationships, never by arbitrary DOM structure or blanket layout rules (e.g., dropping sidebars to the bottom).
*   Establish deeply rooted, ontological relationships between disparate content types using shared semantic attributes to automate related-content discovery.
*   Guarantee that all layout containers and content chunks are labeled semantically based on their meaning, never by their visual position on a screen.

# @Guidelines
*   **Semantic Naming Stricture**: The AI MUST NEVER use positional or visual names for content containers, classes, or data models (e.g., `right-sidebar`, `bottom-banner`, `top-nav`). The AI MUST use semantic, purpose-driven names (e.g., `quick-facts`, `author-timeline`, `product-tasting-notes`).
*   **Taxonomy over Freeform**: The AI MUST NOT use or implement freeform text tagging systems for content logic or related-content algorithms. The AI MUST enforce controlled taxonomies or use intrinsic semantic attributes (e.g., `city_id`, `category_id`) to build programmatic relationships.
*   **Responsive Priority Over Stacking**: When designing responsive layouts, the AI MUST NOT apply blanket CSS rules that simply stack columns (e.g., shifting a sidebar to the bottom of the DOM on mobile). The AI MUST assess the priority of the content within the sidebar (e.g., a "Buy" button or critical feature list) and intermix/insert it near the top of the mobile layout if it holds high priority.
*   **Interdependent Locking**: The AI MUST NOT allow interdependent content elements (e.g., a product title and its user rating, or an image and its caption) to be separated by CSS media queries or DOM reflowing. They MUST remain visually and structurally coupled across all viewports.
*   **Shared Attribute Linking**: To generate "Related Content" modules, the AI MUST NOT rely on manual curation or broad keyword matching. The AI MUST query relationships based on shared structured attributes (e.g., linking a `Feature_Article` and a `Hotel_Listing` because both share the exact attribute `city: "Sedona"`).
*   **Contextual Slicing**: When delivering content to different platforms (e.g., desktop web vs. mobile app vs. API endpoint), the AI MUST use rules to deliver specific combinations of content elements tailored to the platform's constraints, rather than truncating a single large text blob.
*   **No Assumption of Mobile Minimalism**: The AI MUST NOT assume mobile users want less content. Do not hide critical content on small viewports just to save space. Evaluate the *Meaning* and *Priority* of the content; if it is critical, it MUST be displayed, potentially using UX patterns like layering (collapsible accordions) rather than deletion.

# @Workflow
Whenever the AI is generating layouts, CMS schemas, or content presentation logic, it MUST execute the following algorithmic process:

1.  **Element Deconstruction & Semantic Labeling**:
    *   Identify all micro-elements within the content type.
    *   Assign strict semantic names to each element (e.g., `teaser-copy`, `dietary-warnings`, `purchase-action`). Reject any positional names.
2.  **Attribute & Taxonomy Standardization**:
    *   Identify which elements are intrinsic attributes (e.g., Location, Date) or map to a fixed taxonomy.
    *   Define relationships to other content types based *only* on these standardized attributes.
3.  **Framework Evaluation (Meaning, Priority, Relationships)**:
    *   *Analyze Meaning*: Determine if the element is essential or optional.
    *   *Analyze Priority*: Rank the element against others for business goals (e.g., "Buy now" = High, "Publisher info" = Low).
    *   *Analyze Relationships*: Group elements that are Interdependent.
4.  **Rule Generation (If-Then Logic)**:
    *   Write explicit presentation rules based on Step 3. (e.g., "IF viewport is < 480px, THEN inject `purchase-action` immediately below `teaser-copy`, DO NOT push to bottom").
    *   Write related-content rules. (e.g., "IF page is `city`, THEN fetch `articles` where `article.city_id == city.id`).
5.  **Implementation**:
    *   Generate the code (HTML/CSS/JS/GraphQL) reflecting these rules, utilizing CSS Grid/Flexbox order properties or component-based conditional rendering to achieve semantic reflow.

# @Examples (Do's and Don''ts)

### 1. Naming Content Modules
*   **[DO]**: Use semantic names that describe the content's purpose.
    ```css
    .product-tasting-notes { ... }
    .author-bio { ... }
    .related-landmarks { ... }
    ```
*   **[DON'T]**: Use positional names that break when layouts shift across devices.
    ```css
    .right-sidebar { ... }
    .bottom-widget { ... }
    .left-column { ... }
    ```

### 2. Responsive Content Priority
*   **[DO]**: Use CSS `order` or component logic to intermix high-priority sidebar content (like a "Buy" button or ratings) directly under the title/teaser on mobile screens.
    ```jsx
    // React Example
    <article className="product-layout">
      <header className="product-title">{title}</header>
      <div className="product-teaser">{teaser}</div>
      {/* High priority element injected high up in the mobile flow via CSS order or DOM placement */}
      <aside className="purchase-action buy-button">{buyButton}</aside>
      <div className="product-description">{longDescription}</div>
    </article>
    ```
*   **[DON'T]**: Apply a blanket rule that forces all sidebar content to the very bottom of a long mobile page, hiding critical conversion metrics.
    ```html
    <!-- Anti-pattern: The Buy Button is buried under 10 paragraphs of mobile text -->
    <div class="main-content">
      <h1>Title</h1>
      <p>...10 paragraphs of text...</p>
    </div>
    <div class="sidebar-drops-to-bottom-on-mobile">
      <button>Buy Coffee</button>
    </div>
    ```

### 3. Generating Related Content
*   **[DO]**: Build ontological relationships by querying shared fixed attributes (Taxonomy/Metadata).
    ```javascript
    // Fetching related landmarks and articles based on a shared intrinsic attribute
    const currentCity = "Sedona";
    const relatedLandmarks = database.landmarks.filter(l => l.city === currentCity);
    const relatedArticles = database.articles.filter(a => a.city === currentCity);
    ```
*   **[DON'T]**: Rely on unstructured, freeform user tags to generate contextual relationships, which leads to disconnected or irrelevant content.
    ```javascript
    // Anti-pattern: Relying on inconsistent freeform tags
    const currentTags = ["red rocks", "vacation", "arizona", "fun"];
    const relatedContent = database.search(currentTags); // Yields inconsistent, non-ontological garbage
    ```

### 4. Interdependent Relationships in Layouts
*   **[DO]**: Ensure elements whose meaning relies on each other (e.g., Recipe Title and its Star Rating) are locked together in the component hierarchy so they never split across breakpoints.
    ```html
    <div class="recipe-header-group">
      <h1 class="recipe-title">Goat Cheese Pizza</h1>
      <span class="recipe-rating">★★★★★</span>
    </div>
    ```
*   **[DON'T]**: Place interdependent elements in separate structural containers that flow apart on mobile viewports.
    ```html
    <!-- Anti-pattern: Rating drops to the bottom of the page on mobile, severing its meaning from the title -->
    <div class="column-left">
      <h1 class="recipe-title">Goat Cheese Pizza</h1>
    </div>
    <div class="column-right (drops to bottom on mobile)">
      <span class="recipe-rating">★★★★★</span>
    </div>
    ```