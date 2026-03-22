@Domain
Trigger these rules when tasked with designing, migrating, structuring, or managing enterprise content architectures. Activate specifically when user requests involve multichannel publishing, content management system (CMS) setups, content modeling, transitioning legacy content (e.g., print or PDF) to digital formats (eBooks, Web, mobile apps), or defining content workflows across disparate organizational departments.

@Vocabulary
- **Content Strategy:** The planning for the creation, delivery, and governance of content. It shifts website and content creation from an ad-hoc art to a rigorous methodology.
- **Handcrafting / Artisanal Production:** An anti-pattern where content is manually tailored and rewritten for specific channels (e.g., tweaking a PDF, rewriting a mobile site).
- **Responsive Web Design:** A visual technique that scales design down for small screens and up for large screens. Critically, it is *insufficient* on its own because it resizes visuals but does not adapt the actual content to the user's context.
- **Adaptive Content:** Format-free, structured, modular, and reusable content not tied to any device. It automatically adjusts to environments/capabilities, filters/layers detail, reorders dynamically, responds to interactions, changes by location, and integrates external sources.
- **Page Container / Print Designer Trap:** The erroneous mindset of designing content restricted to a specific platform, screen resolution, or physical page size.
- **Manufacturing Model:** A paradigm for content creation mirroring industrial assembly (e.g., Swatch watches) where well-designed, reusable components are used to efficiently build diverse information products.
- **Lean Content Production:** A concept borrowed from lean manufacturing focusing exclusively on value; eliminating valueless work, content errors, and rework.
- **Agile Content Production:** A concept borrowed from agile manufacturing focusing on speed, automation, and the elimination of bottlenecks in content generation.
- **Unified Content Strategy:** An approach that treats each content component not only as an individual piece of information but as an interconnected part of multiple potential information products across the enterprise.

@Objectives
- Eradicate the "content silo trap" by forcing content to be engineered for multichannel delivery from inception.
- Shift the system's output from "responsive design" (resizing visuals) to "adaptive content" (re-architecting content based on context, device, and location).
- Implement a "Manufacturing Model" for content, treating all text, data, and media as reusable, format-agnostic components.
- Ensure all content architectures natively support Web, mobile, eBooks, and API-driven applications (e.g., EPOS apps) without requiring manual duplication or platform-specific hardcoding.

@Guidelines
- **Platform Agnosticism:** The AI MUST NOT tie content to a specific platform, screen resolution, or page size. Content must be completely decoupled from its presentation layer.
- **Adaptive Structuring:** The AI MUST structure content so that it can be filtered and layered for greater or lesser depth of detail depending on the target device (e.g., providing a summary for mobile and deep detail for desktop).
- **Componentization:** The AI MUST treat all content generation as the creation of interconnected, reusable components. Never generate monolithic, un-parseable blocks of text.
- **Format-Free Storage:** The AI MUST utilize open, modular markup (e.g., XML) as the base storage format for content to allow easy reuse and sharing among disparate software systems.
- **Metadata Integration:** The AI MUST define and apply robust metadata schemas to all content components to power content personalization and automated assembly.
- **Avoid Tool-Centric Solutions:** The AI MUST recognize that purchasing/using a CMS tool is insufficient without a clear understanding of content requirements and design. Focus on the content model first, not the software tool.
- **API Readiness:** Content schemas MUST be designed with rich APIs in mind, allowing content to be exported and consumed by third-party systems or native applications (e.g., iOS/Android apps).
- **Reject "Responsive-Only" Fixes:** When asked to optimize content for mobile, the AI MUST NOT default to simply applying CSS media queries. The AI MUST evaluate and restructure the content itself to be modular and contextually appropriate.

@Workflow
1. **Content Inventory & Requirements Gathering:** Analyze the existing content corpus. Identify the high-value information and the specific contexts/diagnoses/needs of the end-user.
2. **Metadata Schema Development:** Develop a metadata schema with sufficient granularity to support accurate personalization and contextual delivery, without overwhelming content contributors.
3. **Componentization & XML Conversion:** Break down monolithic documents (e.g., Word, PDF) into discrete, semantic components. Store these components in a format-agnostic, structured language (like XML).
4. **Adaptive Rule Definition:** Define rules for how the content components should behave dynamically. Determine how content should be filtered, layered, reordered, or triggered based on device type, user interaction, or location.
5. **Presentation Layer Decoupling:** Create independent presentation layers (stylesheets, application logic) for each channel (eBook, Web, iOS app) that pull from the centralized, format-free component repository.
6. **API and Delivery Implementation:** Establish the delivery mechanisms (e.g., RESTful APIs) to push the modular content to external applications, electronic point of sale (EPOS) systems, or mobile apps.

@Examples (Do's and Don'ts)

**Principle: Adaptive vs. Responsive Content**

[DO]
```xml
<!-- Format-free, adaptive XML component with metadata for layering -->
<article id="breast-cancer-diagnosis-001" category="medical-info" target-audience="patient">
    <summary audience-device="mobile">
        A biopsy is the only definitive way to diagnose breast cancer.
    </summary>
    <detailed-explanation audience-device="desktop, tablet">
        A biopsy involves removing a small sample of tissue for examination under a microscope. 
        There are several types of biopsies, including fine-needle aspiration, core needle biopsy, and surgical biopsy.
    </detailed-explanation>
    <interactive-element type="user-record" context="doctor-office">
        <prompt>Enter your biopsy results here for your personal record.</prompt>
        <data-field type="text" id="user-biopsy-result" />
    </interactive-element>
</article>
```

[DON'T]
```html
<!-- Monolithic HTML relying purely on responsive CSS to hide things, trapping content in format -->
<div class="diagnosis-page" style="width: 100%; max-width: 960px;">
    <h1>Biopsy Information</h1>
    <p class="desktop-only" style="font-size: 14px; line-height: 1.5;">
        A biopsy involves removing a small sample of tissue... 
        (500 words of dense text that is merely hidden via CSS media queries on mobile, wasting bandwidth and ignoring user context)
    </p>
    <br><br>
</div>
```

**Principle: The Manufacturing Model (Component Reusability)**

[DO]
```json
// Content structured as an API payload ready to be assembled into various products
{
  "component_id": "val-prop-01",
  "metadata": {
    "type": "value_proposition",
    "tags": ["sales", "marketing", "core_product"]
  },
  "content": {
    "headline": "Empower your mobile workforce.",
    "short_description": "Deliver critical data to any device, anywhere.",
    "features": [
      "Offline sync",
      "Cross-platform support",
      "Enterprise-grade security"
    ]
  }
}
// This JSON/XML can be assembled into a web page, a printed brochure, or an app screen.
```

[DON'T]
```html
<!-- Handcrafted, artisanal content locked into a single specific deliverable -->
<html>
  <head><title>Product Brochure Page 3</title></head>
  <body>
    <div id="brochure-callout-box" style="border: 1px solid black; padding: 10px;">
        <h2>Empower your mobile workforce.</h2>
        <p>Deliver critical data to any device, anywhere. Offline sync, Cross-platform support...</p>
    </div>
  </body>
</html>
<!-- If this needs to go into a mobile app, it must be manually rewritten and extracted. -->
```