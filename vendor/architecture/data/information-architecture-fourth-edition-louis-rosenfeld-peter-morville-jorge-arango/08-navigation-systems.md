@Domain
Trigger these rules when executing UI/UX design tasks, planning website or application structures, configuring routing, generating frontend navigation components (e.g., headers, footers, sidebars), or conducting usability audits on existing navigation systems.

@Vocabulary
*   **Placemaking**: The use of navigational cues to create a sense of place, allowing users to understand where they are and what they can do within the information environment.
*   **Navigation Stress Test**: An evaluation method where the user drops into the middle of a site, bypassing the home page, to determine if the navigation provides sufficient contextual clues about location and next steps.
*   **Lateral Navigation**: Movement across different branches of a hierarchy.
*   **Vertical Navigation**: Movement up or down within the same branch of a hierarchy.
*   **Embedded Navigation Systems**: Navigation mechanisms integrated directly within the page layout, including global, local, and contextual navigation.
*   **Global Navigation**: A site-wide navigation system present on every page, providing direct access to key areas (e.g., top-level navigation bars, mega-menus, fat footers).
*   **Local Navigation**: A navigation system enabling users to explore the immediate area, subsite, or specific category they are currently viewing.
*   **Contextual Navigation**: "See also" or related links specific to a particular page, document, or object, supporting associative learning.
*   **Supplemental Navigation Systems**: Navigation tools existing outside the primary content-bearing pages (e.g., sitemaps, indexes, guides) designed to back up the primary taxonomy.
*   **Sitemaps**: A visual or textual representation of the top few levels of the information hierarchy, offering a bird's-eye view of the system.
*   **Indexes**: Flat, alphabetical listings of keywords or phrases allowing direct access to content, bypassing the hierarchy.
*   **Term Rotation (Permutation)**: An indexing technique where the words in a phrase are rotated so the user can find the phrase under multiple alphabetical entries (e.g., "Abuse, Elder" and "Elder Maltreatment").
*   **Guides**: Guided tours, tutorials, and walkthroughs featuring linear navigation to introduce new users to content and functionality.
*   **Configurators**: Wizards that help users navigate complex decision trees (e.g., product customization).
*   **Personalization**: System-driven adaptation of navigation or content based on a model of the user's behavior, needs, or past purchases.
*   **Customization**: User-driven adaptation where the user explicitly controls presentation, navigation, or content options.
*   **Social Navigation**: Dynamic navigation systems driven by the actions, voting, or social graphs of other users.

@Objectives
*   Prevent users from getting lost by continuously providing clear location and context ("You Are Here").
*   Balance the freedom of hypertextual navigation (flexibility) with the danger of overwhelming the user (clutter).
*   Ensure navigation paradigms adapt appropriately to device constraints (desktop vs. mobile/touch).
*   Implement overlapping safety nets by backing up embedded navigation with supplemental navigation systems.
*   Support associative learning by connecting related content chunks laterally without breaking the primary hierarchical structure.

@Guidelines

**Placemaking and Context Rules**
*   The AI MUST ensure every page design includes a clear "You Are Here" indicator (e.g., active states on menus, breadcrumbs, contextual headings).
*   The AI MUST include the organization's name, logo, and graphic identity on all pages to orient users who bypass the home page via direct links or search engines.
*   The AI MUST validate any navigation structure using the "Navigation Stress Test." The AI MUST simulate dropping into a deep child page and verify that the UI clearly answers: Where am I? What is the major section? What is the parent page? Where can I go next?

**Embedded Navigation Architecture**
*   The AI MUST implement Global Navigation on every page. For desktop, the AI MUST use text-based labels, mega-menus, or fat footers. For mobile, the AI MUST utilize space-saving patterns (e.g., off-canvas menus, bottom tab bars with iconic representation).
*   The AI MUST implement Local Navigation to complement Global Navigation when a specific section (subsite) requires unique exploration paths. The AI MUST visually distinguish Local Navigation from Global Navigation.
*   The AI MUST incorporate Contextual Navigation (e.g., "Related Products," "Similar Articles") to support lateral movement. The AI MUST use moderation; inline text links MUST NOT distract from core content reading, and external "related" link blocks MUST be separated from primary content.
*   The AI MUST NOT mix Global, Local, and Contextual links into a single, undifferentiated UI cluster. They MUST occupy distinct conceptual and visual zones on the page.

**Device and Interaction Adaptation**
*   The AI MUST align with standard OS and browser navigation features (e.g., Back/Forward, standard menu bar layouts). The AI MUST NOT hijack or break native browser back-button functionality.
*   The AI MUST evaluate screen real estate. The AI MUST use text labels where space permits, and reserve iconic labels for constrained environments (e.g., mobile tab bars), ensuring icons are universally recognizable or paired with text.

**Supplemental Navigation Implementation**
*   The AI MUST generate Sitemaps only for the top few levels of the hierarchy. The AI MUST NOT attempt to list every single destination page in a sitemap, to avoid overwhelming the user.
*   The AI MUST construct Indexes as flat, A-to-Z lists for known-item searching. The AI MUST apply Term Rotation/Permutation selectively to accommodate varied user phrasing, but MUST NOT over-permute to the point of clutter.
*   The AI MUST design Guides and Configurators with clear linear navigation. The AI MUST include explicit "Previous," "Next," and "Home/Exit" controls, allowing the user to abandon the guide at any point.

**Advanced Navigation Constraints**
*   The AI MUST NOT rely on Personalization or Customization as a replacement for a solid foundational taxonomy. The AI MUST treat these as advanced enhancements only.
*   When implementing Social Navigation (e.g., popular lists, user-voted feeds), the AI MUST retain standard Global Navigation to ensure placemaking is preserved and users do not become trapped in algorithmic "echo chambers."

@Workflow
1.  **Context & Device Assessment**: Determine the platform (desktop, mobile web, native app). Select appropriate navigation design patterns (e.g., mega-menus vs. bottom tab bars).
2.  **Placemaking Injection**: Establish the global header, logo placement, and "You Are Here" mechanisms (active link states, breadcrumb trails).
3.  **Hierarchy Translation**: Convert the top-down information architecture into a Global Navigation system. Ensure primary categories are mutually exclusive and clearly labeled.
4.  **Local Navigation Definition**: Identify if the current page belongs to a subsite or deep category. If yes, generate Local Navigation elements (e.g., sidebars or secondary sub-nav bars).
5.  **Contextual Link Mapping**: Analyze the page's content for associative learning opportunities. Generate a constrained list of "See Also" or related items, placing them inline or in a dedicated layout block.
6.  **Supplemental Integration**: Assess the complexity of the site. If the site is large, generate structural logic for a Sitemap and a flat A-to-Z Index.
7.  **Stress Testing**: Execute the Navigation Stress Test on the deepest, most obscure route in the generated architecture to verify context, parent-child relationships, and exit paths. Refine the UI if the test fails.

@Examples

**[DO] Placemaking & "You Are Here" Indicators**
```html
<nav aria-label="Global" class="global-nav">
  <div class="logo">Acme Corp</div>
  <ul class="nav-links">
    <li><a href="/products">Products</a></li>
    <!-- Active state clearly indicates location -->
    <li><a href="/services" aria-current="page" class="active">Services</a></li>
    <li><a href="/support">Support</a></li>
  </ul>
</nav>
<nav aria-label="Breadcrumb" class="breadcrumbs">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/services">Services</a></li>
    <li><span aria-current="page">Cloud Hosting</span></li>
  </ol>
</nav>
```

**[DON'T] Failing the Navigation Stress Test**
```html
<!-- Anti-pattern: Dropping a user into a page with no global context, no logo, and no way to determine the parent category. -->
<div class="page-content">
  <h1>Cloud Hosting Features</h1>
  <p>Our hosting is top notch...</p>
  <a href="/buy">Buy Now</a>
  <!-- User has no idea what site they are on, how to see other services, or how to get to the homepage -->
</div>
```

**[DO] Selective Term Permutation in an Index**
```html
<div class="site-index">
  <h3>A</h3>
  <ul>
    <li><a href="/abuse-elder">Abuse, Elder</a></li>
    <li><a href="/annual-reports">Annual Reports</a></li>
  </ul>
  <h3>E</h3>
  <ul>
    <li><a href="/abuse-elder">Elder Maltreatment</a></li> <!-- Rotated term pointing to the same destination -->
  </ul>
</div>
```

**[DON'T] Overwhelming Sitemaps**
```html
<!-- Anti-pattern: Listing every single deep article in the sitemap instead of the top-level hierarchy -->
<div class="sitemap">
  <ul>
    <li>Technology
      <ul>
        <li>Software
          <ul>
            <li>Update v1.0.1 Release Notes</li>
            <li>Update v1.0.2 Release Notes</li>
            <li>Update v1.0.3 Release Notes</li>
            <!-- 500 more items, burying the user in clutter -->
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>
```

**[DO] Guide/Configurator Navigation**
```html
<div class="configurator-wizard">
  <div class="progress-bar">Step 2 of 4: Select Color</div>
  <div class="configurator-content">...</div>
  <div class="wizard-controls">
    <button class="btn-prev">Previous</button>
    <button class="btn-next">Next</button>
    <a href="/products" class="btn-exit">Save and Exit</a> <!-- Escape hatch -->
  </div>
</div>
```