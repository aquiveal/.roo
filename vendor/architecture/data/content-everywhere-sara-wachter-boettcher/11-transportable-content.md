@Domain
Front-end development, content modeling, markup generation, API schema design, and UI/UX layout creation for text, articles, products, and multimedia content intended for consumption, syndication, or reading environments. Triggered whenever creating readable web pages, defining content data structures, or generating HTML for digital publishing.

@Vocabulary
- **Content Shifting:** The process of a user taking content from one context (e.g., a specific website) and shifting it to another location or service (e.g., Instapaper, Pocket, Pinterest) for reading, saving, or collecting.
- **Portable Content / Orbital Content:** Content models where individual users are the gravitational center and content floats in orbit around them, completely decoupled from its original host website.
- **Read-Later Apps:** Services (like Safari Reader, Instapaper, Readability) that extract core text and media from a webpage, stripping away the surrounding UI and advertising, to provide a clean reading interface.
- **Presentational Markup:** The anti-pattern of using font sizes, bolding, or CSS classes (e.g., `<div class="big-text">`) to denote content hierarchy instead of machine-readable semantic HTML.
- **Parsing:** The act of third-party services programmatically reading, extracting, and re-assembling a site's content.
- **Attribution:** Metadata that maintains the provenance, authorship, and source of a piece of content once it has been shifted away from its original website.
- **Fair Use:** A legal concept regarding the reproduction of copyrighted material for personal use, which complicates how shifted content is monetized and protected.

@Objectives
- **Maximize Universal Parsability:** Ensure all generated content can be flawlessly extracted, understood, and reconstructed by third-party content-shifting services without losing its intended hierarchy, meaning, or narrative flow.
- **Preserve Provenance Through Metadata:** Automatically embed attribution, authorship, and canonical source data directly into portable content modules to survive extraction.
- **Eliminate Presentational Dependency:** Ensure content structure relies exclusively on semantic meaning, completely decoupling the content's integrity from the host site's CSS.
- **Optimize the Native Reading Experience:** Design distraction-free, content-first native layouts that respect the reader, reducing the user's urgent need to shift content to a read-later app just to escape UI noise.
- **Design Standalone Content:** Structure content so that its core message, brand voice, and usefulness remain completely intact even when viewed in a vacuum outside the original application.

@Guidelines
- **Mandatory Semantic Wrappers:** The AI MUST isolate core content from supplementary website noise (navigation, sidebars, ads) using strict semantic HTML5 wrappers (e.g., `<article>`, `<main>`). 
- **Strict Prohibition of Presentational Structure:** The AI MUST NOT use CSS classes, inline styles, `<b>`, `<i>`, or generic `<div>` tags to imply structural meaning (e.g., using a large bold font for a copy deck). The AI MUST use appropriate semantic tags (e.g., `<h1>`-`<h6>`, `<p class="lead">`, `<blockquote>`, `<figure>`).
- **Granular Semantic Chunking:** When formatting complex content (e.g., an article with a Q&A section, video, and body text), the AI MUST enclose each distinct element within its own semantic container so external parsers do not accidentally discard multi-part content (as happens with poorly structured Q&As).
- **Embedded Attribution Data:** The AI MUST embed authorship and provenance directly within the targeted parsing block (inside the `<article>`). Use `<address rel="author">`, `<time datetime="...">`, and canonical links so that when content is shifted, the attribution travels with it.
- **Universal Agnosticism:** The AI MUST NOT optimize markup exclusively for a single third-party parser (e.g., relying solely on Instapaper's specific proprietary tags). The AI MUST build universally semantic content models that gracefully map to any parser.
- **Aggressive Clutter Reduction:** When generating UI/UX layouts for reading experiences, the AI MUST prioritize the content. The AI MUST restrict ads, related links, and intrusive calls-to-action to the extreme periphery (or eliminate them), ensuring they do not interrupt the core content flow.

@Workflow
1. **Identify the Core Content Payload:** Determine the exact boundaries of the primary content (the article, the recipe, the product description) that a user would realistically want to save or shift.
2. **Isolate and Wrap:** Enclose this specific payload in an `<article>` or `<main>` tag. Exclude all site navigation, generic sidebars, and advertising from this container.
3. **Apply Granular Semantics:** Review the payload's internal chunks. Assign semantic HTML to headers, copy decks/teasers, author bylines, publication dates, and pull quotes.
4. **Embed Portable Provenance:** Inject metadata (author name, canonical URL, publication date) directly inside the payload container using HTML5 semantic tags and/or JSON-LD/Microdata, ensuring it is physically bound to the transportable text.
5. **Strip Visual Interference:** Review the surrounding UI layout. Remove or heavily visually demote intrusive banners, pop-ups, and aggressive CTAs that degrade the native reading experience.
6. **Validate Parsability:** Verify that if all CSS and JS were stripped, the raw HTML output within the `<article>` tag still reads sequentially, logically, and retains all contextual meaning and attribution.

@Examples (Do's and Don'ts)

**Semantic Structuring for Parsers**
[DO]
```html
<main>
  <article>
    <header>
      <h1 itemprop="headline">The Future of Orbital Content</h1>
      <p class="copy-deck" itemprop="description">As users take control of their reading experiences, publishers must adapt by building universally parsable structures.</p>
      <address itemprop="author" itemscope itemtype="http://schema.org/Person">
        By <span itemprop="name">Jane Doe</span>
      </address>
      <time datetime="2023-10-24" itemprop="datePublished">October 24, 2023</time>
      <link itemprop="url" href="https://example.com/future-orbital-content" />
    </header>
    
    <section itemprop="articleBody">
      <p>The great content shift is upon us. Users are pocketing and pinning our work...</p>
      <!-- Complex content explicitly wrapped to prevent parser dropping -->
      <figure>
        <video src="interview.mp4" controls></video>
        <figcaption>Author interview regarding content portability.</figcaption>
      </figure>
      <h2>Q&A Session</h2>
      <p><strong>Q: Why do users shift content?</strong></p>
      <p>A: To avoid distracting website layouts.</p>
    </section>
  </article>
</main>
<aside>
  <!-- Non-essential ads and related links placed STRICTLY OUTSIDE the article tag -->
</aside>
```

[DON'T]
```html
<!-- Anti-Pattern: Presentational formatting, no semantic boundaries, attribution lost in generic divs -->
<div id="wrapper">
  <div class="sidebar">Ads and Clutter</div>
  <div class="content-area">
    <div style="font-size: 32px; font-weight: bold;">The Future of Orbital Content</div>
    <div style="font-size: 20px; color: gray;">As users take control of their reading experiences, publishers must adapt by building universally parsable structures.</div>
    
    <!-- Attribution separated from the content body, likely to be stripped by read-later apps -->
    <div class="top-nav-author-box">Jane Doe - Oct 24</div>
    
    <div class="body-text">
      The great content shift is upon us. Users are pocketing and pinning our work...
      
      <!-- Video dropped inline without figure/caption, likely to be ignored or cause parser errors -->
      <video src="interview.mp4"></video>
      <div style="font-size: 24px;">Q&A Session</div>
      Q: Why do users shift content?<br>
      A: To avoid distracting website layouts.
    </div>
  </div>
</div>
```

**Designing the Native Reading Experience**
[DO] Provide a single-column, typography-focused layout where the text spans a comfortable reading width (e.g., 65ch). Place supplementary content at the very bottom of the article to prevent reading interruption.
[DON'T] Interleave ad banners, "retargeted" product widgets, and social sharing overlays every two paragraphs, forcing the user to install a read-later extension just to consume the text.