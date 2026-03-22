# @Domain
Trigger these rules when the user requests assistance with designing, architecting, developing, or documenting Content APIs, headless CMS systems, cross-channel publishing architectures, content distribution networks, or any system intended to syndicate content to multiple devices (e.g., websites, mobile apps, smart devices, partner portals).

# @Vocabulary
- **Content API:** An application programming interface specifically designed to store, manage, and transport structured content (which is often inherently ambiguous and narrative-driven) to multiple services, devices, and platforms.
- **Mash-up:** The integration of data or content from multiple external sources and APIs to create a cohesive, enriched user experience or application.
- **Public API:** An open interface allowing external, third-party developers to access and use an organization's content (often subject to strict filtering and editorial limitations).
- **Private API:** A closed interface limited to internal organizational use or a strictly defined network of partners (e.g., used to power an organization's own suite of apps and websites).
- **Read API:** An API designed solely to publish and distribute content outward to consuming applications.
- **Write API:** An API designed to accept incoming content and data from external sources, enabling the aggregation and enrichment of the organization's own content ecosystem.
- **RSS (Real Simple Syndication):** A legacy, limited, one-way feed of content. Distinct from a Content API, which is a two-way "conversation" allowing applications to search, slice, and request specific combinations of content elements.
- **Metadata Filtering:** The programmatic use of structural and descriptive tags to determine which content elements are exposed to which API consumers based on legal, editorial, or access-level constraints.

# @Objectives
- The AI MUST treat content as ambiguous data that requires strict structural context, human-friendly metadata, and clean architecture before it can be successfully distributed via an API.
- The AI MUST design content API architectures that support "create once, publish everywhere" (COPE) methodologies across an infinite number of form factors (websites, mobile apps, IoT devices, print catalogs).
- The AI MUST prioritize the separation of content meaning/structure from its final visual presentation layer.
- The AI MUST ensure that editorial intent, key messaging, storytelling structures, and legal rights are preserved and enforceable within the API payload.

# @Guidelines
- **Structure Before Syndication:** The AI MUST ensure that content is broken down into clean, self-descriptive, modular chunks (e.g., headline, teaser, body, location, author) before designing the API endpoint. An API cannot fix unstructured "blob" content.
- **Differentiate Content from Standard Data:** When designing payloads, the AI MUST account for the narrative and conceptual ambiguity of human content by enforcing rich metadata tagging. Do not treat a news article or product description the same way as simple latitude/longitude data.
- **Tiered Access Levels:** The AI MUST design routing or filtering logic that accounts for Public vs. Private API consumption. Do not assume all content chunks should be available to all endpoints.
- **Enforce Editorial and Legal Rules:** The AI MUST implement metadata fields that allow the API to filter content based on editorial constraints (e.g., "Do not syndicate this specific article text publicly") and legal constraints (e.g., "Photo usage rights limited to internal apps only").
- **Design for Conversation, Not Feeds:** The AI MUST NOT design Content APIs as static, flat feeds (like RSS). The API MUST allow consuming applications to query, search, slice, and request specific combinations of content elements (e.g., requesting only the title, teaser, and audio file for a mobile widget).
- **Enable Personalization:** The AI MUST structure APIs to support dynamic querying, allowing end-users or frequent visitors to create personalized dashboards or customized collections of content (e.g., the my.FCC.gov model).
- **Incorporate Write Capabilities:** When architecting the data flow, the AI MUST evaluate and recommend "Write API" capabilities to ingest third-party or user-generated content, thereby enriching the core content repository.
- **Platform-Agnostic Payloads:** The AI MUST aggressively strip all presentational HTML, inline styling, or device-specific layout instructions from the API response. The API payload MUST convey only meaning and structure.

# @Workflow
1. **Identify Destinations:** Define all known and potential destinations for the content (e.g., desktop site, mobile apps, third-party aggregators, smart devices).
2. **Audit Content Structure:** Review the underlying data model. Ensure the content is structured into modular chunks and enriched with descriptive metadata prior to API exposure.
3. **Define API Tiers:** Establish access levels (Private/Internal, Partner/Affiliate, Public/Third-Party). 
4. **Map Metadata Filters:** Apply rules defining exactly which content elements and metadata tags are exposed to each API tier (e.g., full text for Private, title/teaser only for Public).
5. **Establish Query Capabilities:** Design endpoints that allow consumers to request specific slices of content (conversational API), enabling personalized dashboards and dynamic layouts.
6. **Evaluate Bidirectional Flow:** Determine if the API requires a "Write" layer to accept external content for mash-ups or enrichment.
7. **Validate Agnosticism:** Review the final API response payloads to guarantee absolute separation of content from presentation.

# @Examples (Do's and Don'ts)

## Payload Structure and Presentation Agnosticism
- **[DO]** Design API responses that return discrete, semantic content chunks:
  ```json
  {
    "article_id": "84729",
    "headline": "The Future of Content",
    "teaser": "How APIs are changing the digital landscape.",
    "body_text": "Imagine this: your organization is coming out with a new product...",
    "metadata": {
      "author": "Jane Doe",
      "publish_date": "2023-10-12T08:00:00Z",
      "topic_tags": ["Technology", "Strategy"]
    }
  }
  ```
- **[DON'T]** Design API responses that bundle content into a single presentation-heavy blob:
  ```json
  {
    "article_id": "84729",
    "page_content": "<div class='mobile-sidebar'><h1 style='color:red;'>The Future of Content</h1><p><strong>By Jane Doe</strong></p><p>Imagine this...</p></div>"
  }
  ```

## Access Tiering and Metadata Filtering
- **[DO]** Implement logic that filters the payload based on the consumer's access tier, withholding restricted elements from public endpoints:
  ```javascript
  // Pseudocode for API routing
  if (request.tier === 'PUBLIC') {
      return {
          title: content.title,
          teaser: content.teaser,
          link: content.canonical_url
      };
  } else if (request.tier === 'PRIVATE') {
      return content.full_payload; // Includes full body, high-res images, and internal metadata
  }
  ```
- **[DON'T]** Serve the exact same comprehensive payload to all consumers and rely on the third-party application to "hide" proprietary or legally restricted data.

## API Interaction Model
- **[DO]** Create RESTful or GraphQL endpoints that allow clients to request specific slices of data for personalization: `GET /api/v1/content?topics=accessibility&fields=headline,date,audio_url`
- **[DON'T]** Build a static endpoint that functions like a glorified RSS feed, forcing the consuming application to download the entire daily content dump just to extract one specific element: `GET /api/v1/feed/all_daily_content`