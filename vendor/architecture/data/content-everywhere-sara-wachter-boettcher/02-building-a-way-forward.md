@Domain
Trigger the application of these rules when the user requests tasks involving content modeling, content management system (CMS) architecture, information architecture (IA) design, multichannel publishing, API-driven content delivery, or the development of digital content strategies.

@Vocabulary
*   **Content Strategy**: The discipline dedicated to understanding audience needs, developing sustainable publishing plans, reducing redundant publishing efforts, aligning cross-channel communication, and preventing project delays by managing the effort required to produce great content.
*   **Technical Communications**: The systematic practice of structuring content, separating its structure from its presentation, and marking it up for transport between systems.
*   **DITA (Darwin Information Type Architecture)**: An XML-based language and methodology for authoring and publishing information in discrete modules categorized according to topic, enabling high reusability.
*   **Information Architecture (IA)**: The structural design of shared information environments focused on spatial relationships, hierarchies, taxonomies, vocabularies, and schemas.
*   **Content Models**: "Micro" information architectures made up of small chunks of interconnected data. 
*   **Author Experience**: The specialized application of User Experience (UX) focused on the creators, writers, and editors using a CMS; aims to make content entry efficient, intuitive, and error-free.
*   **WYSIWYG**: What-You-See-Is-What-You-Get; a presentation-focused interface in legacy CMSs that encourages the blending of structure and visual design (an anti-pattern for future-ready content).
*   **COPE (Create Once, Publish Everywhere)**: A publishing model where a single set of structured content is entered into a CMS and distributed via API to multiple platforms, products, and affiliates.

@Objectives
*   Unify principles from Content Strategy, Technical Communications, Information Architecture, and Content Management to build a foundational framework for future-ready content.
*   Decouple content structure from visual presentation to ensure content can travel fluidly across multiple channels and devices.
*   Transition information systems from strictly hierarchical and linear models to flexible, modular, relational, and semantic architectures.
*   Design CMS environments that prioritize the Author Experience, ensuring content creators correctly and willingly populate structured metadata.
*   Implement COPE methodologies to eliminate redundant content creation and enforce systemic editorial consistency.

@Guidelines
*   **Incorporate Content Strategy Foundations**: You MUST ensure that any proposed content architecture cuts costs by reducing redundant publishing efforts and aligns communication goals across all targeted channels.
*   **Separate Structure from Presentation**: Drawing from Technical Communications, you MUST NEVER embed visual formatting (e.g., HTML font colors, static layout tags) into core content models. Treat content as raw, modular chunks designed for pure data transport (e.g., via XML or JSON APIs).
*   **Design Micro-Architectures**: You MUST build Content Models that act as micro-information architectures. Content must be modeled as small, interconnected chunks rather than monolithic pages.
*   **Avoid Strict Hierarchies**: You MUST architect systems that rely on modular, relational, and semantic connections rather than purely linear or strict top-down hierarchical sitemaps.
*   **Prioritize Author Experience**: When designing CMS schemas or input requirements, you MUST optimize for the author's workflow. Avoid designing complex, frustrating interfaces (like endless dropdowns) that incentivize users to leave metadata fields blank or enter inaccurate data.
*   **Abolish WYSIWYG Reliance**: You MUST actively discourage the use of WYSIWYG editors for structural layout. Prevent authors from turning good text into "pink, bolded nightmares."
*   **Enforce the COPE Model**: You MUST architect content so that it is created once as a structured entity, entered into a centralized CMS, and delivered via API to all dependent endpoints (websites, mobile apps, affiliate stations).
*   **Progress over Perfection**: You MUST adopt an iterative mindset. If a fully automated API-driven COPE ecosystem is not immediately feasible, you MUST take the first step by breaking existing content down into meaningful micro-components.

@Workflow
1.  **Assess the Foundation**: Evaluate the current system against the four foundational lineages: Content Strategy, Technical Communications, Information Architecture, and Content Management. Identify bottlenecks in each.
2.  **Define the COPE Strategy**: Determine the core "kernel" or "story" of the content being requested. Identify all potential endpoints (mobile, desktop, affiliate platforms) that will consume this content.
3.  **Model the Micro-Architecture**: Break the content down into a Content Model. Define the semantic chunks (e.g., headline, teaser blurb, long description, date stamp) rather than visual areas (e.g., sidebar, main column).
4.  **Architect the Author Experience**: Design the CMS input schema for this model. Ensure the fields are explicitly labeled, intuitive, and map directly to the semantic chunks. Ensure the workflow respects the creator's time and prevents frustration.
5.  **Design the Distribution Interface**: Specify how the structured CMS data will be packaged (e.g., via API) to cleanly deliver the content to the predefined endpoints without carrying presentational baggage.

@Examples (Do's and Don'ts)

*   **DO**: Structure a news article using discrete, semantically named fields intended for API distribution.
    ```json
    {
      "article": {
        "headline": "New API Launched",
        "teaser_blurb": "The organization releases a COPE-driven API.",
        "body_text": "Full story goes here...",
        "date_stamp": "2023-10-12"
      }
    }
    ```

*   **DON'T**: Store an article as a single unstructured block of HTML relying on a WYSIWYG editor for visual formatting.
    ```html
    <div class="article-blob">
      <font size="6"><b>New API Launched</b></font><br><br>
      <i>The organization releases a COPE-driven API.</i><br><br>
      Full story goes here...
    </div>
    ```

*   **DO**: Design a CMS data-entry workflow that uses clear, task-oriented forms (Author Experience), ensuring content strategists and writers can easily populate the correct modular chunks.

*   **DON'T**: Implement a complex database schema into the CMS UI without considering the author, forcing non-technical writers to navigate confusing relational tables or write raw markup, which leads to abandoned fields and inaccurate metadata.