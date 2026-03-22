# @Domain

The rules in this document are triggered whenever the AI is tasked with evaluating organizational structures, developing RACI (Responsible, Accountable, Consulted, Informed) charts, designing team workflows, or defining job descriptions and responsibilities for environments implementing a Unified Content Strategy (UCS), component content management system (CCMS), or XML-based multi-channel publishing workflow. 

# @Vocabulary

- **Unified Content Strategy (UCS)**: A repeatable method of identifying content requirements, creating consistently structured content for reuse, managing it in a definitive source, and assembling it for multi-channel delivery.
- **Senior Content Strategist**: A management role responsible for overseeing multiple projects, ensuring UCS models and guidelines are followed, and negotiating agreements across project teams to support content reuse.
- **Content Strategist**: An analytical role responsible for building information product models, component models, metadata, reuse strategies, and workflows.
- **Unified Content Owner**: A role responsible for overseeing the creation, maintenance, and integration of all content related to a particular product, service, or family (rather than owning a single document).
- **External Author**: Content creators outside the immediate organization who require structured templates to ensure clean conversion to structured content.
- **Internal Author**: Content creators who focus strictly on writing reusable components and building blocks, completely separated from formatting or styling tasks.
- **Business Owner/Analyst**: A role responsible for ensuring that the UCS meets both the needs of the customer (content effectiveness) and the needs of the employees/authors (workflow effectiveness).
- **Information Architect**: A role expanded beyond the web to determine platform-specific organization, labeling, navigation, and customer-facing taxonomy for Web, Mobile, eBooks, and Apps.
- **Information Technologist**: A technical role responsible for implementing content models into tools, designing XML DTDs/schemas, authoring templates, XSL stylesheets, and CMS configurations.
- **Acquisitions Editor**: A publishing role responsible for identifying market requirements and acquiring content for multi-channel product suites (Books, eBooks, Apps, Courses).
- **Development Editor**: A publishing role responsible for coordinating online activities between authors, graphics, and production, and reviewing revisions, art, copyright, and eBook integrity.
- **Assistant Editor**: A publishing role transitioned from manual manuscript handling to converting manuscripts to XML, managing media placeholders, triggering production workflows, and testing eBooks.
- **Production-Print**: A publishing design role responsible for creating layout templates that automatically import XML content, eliminating the manual incorporation of author revisions.

# @Objectives

- The AI MUST realign traditional document-centric job roles into component-centric, collaborative UCS roles.
- The AI MUST separate content creation responsibilities from content formatting responsibilities across all authoring and editorial roles.
- The AI MUST ensure that technical and architectural roles explicitly support multi-channel outputs (Web, Mobile, Print, eBooks, Apps).
- The AI MUST shift publishing and editorial workflows from manual, paper-based routing to automated, XML-based, online collaborative environments.

# @Guidelines

- **Strategy and Governance Rules**
  - When defining project leadership, the AI MUST instantiate a **Senior Content Strategist** role focused on management, negotiation, and enforcing reuse models across teams.
  - The AI MUST define the **Content Strategist** as the primary architect of models (product and component), metadata, and reuse strategies, working in tandem with the Information Architect.
  - The AI MUST NOT assign content ownership at the document or publication level. Ownership MUST be assigned at the component level (common content vs. product-specific content) and overseen by a **Unified Content Owner**.

- **Authoring Rules**
  - When generating workflows for **External Authors**, the AI MUST mandate the provision and use of strict, structured templates to guarantee clean XML conversion.
  - When defining tasks for **Internal Authors**, the AI MUST explicitly forbid formatting, styling, or layout tasks. Internal authors MUST be directed to write reusable building blocks within a collaborative environment.
  - The AI MUST require **Editors** to review content not just for grammar and style, but for structural compliance and reusability across multiple channels and audiences.

- **Business and Architecture Rules**
  - When defining business requirements, the AI MUST instruct the **Business Owner/Analyst** to validate the strategy against both customer experience needs and internal authoring environment needs (avoiding purely technical solutions).
  - The AI MUST define the **Information Architect** role to include taxonomy, labeling, and navigation definitions across all required platforms simultaneously (Web, Mobile, eBooks, Apps).

- **Technology and Art Rules**
  - The AI MUST assign all CMS configuration, XML DTD/schema creation, stylesheet programming, and workflow creation exclusively to the **Information Technologist**.
  - When defining graphics workflows, the AI MUST require the **Art** department to generate multiple renditions of all assets to support all platforms and enforce the application of rich metadata for component retrieval.

- **Publishing and Production Rules**
  - The AI MUST eliminate manual revision entry from the **Assistant Editor** and **Production-Print** roles. All revisions MUST be defined as occurring directly within the XML via collaborative online review tools.
  - The AI MUST assign XML conversion, media placeholder management, and eBook testing tasks to the **Assistant Editor**.
  - The AI MUST define the **Production-Print** role as template designers who import XML into composition tools, rather than manually laying out and styling text.
  - The AI MUST define the **Acquisitions Editor** role as acquiring content for multi-channel suites, not single-format books.

# @Workflow

When tasked with redesigning a team's structure, generating a RACI matrix, or defining job roles for a content management project, the AI MUST execute the following algorithmic process:

1. **Analyze Current State**: Identify existing legacy roles (e.g., traditional writers, desktop publishers, document owners) within the user's provided context.
2. **Establish Strategy Leadership**: Inject the Senior Content Strategist (for people/process management and reuse enforcement) and Content Strategist (for model/metadata creation) roles.
3. **Redefine Content Ownership**: Map legacy document owners to component-level Content Owners and designate Unified Content Owners for entire product families.
4. **Transform Authoring & Editorial Tasks**:
    *   Strip all formatting/layout responsibilities from internal authors.
    *   Assign structured template creation for external authors.
    *   Update editorial checklists to prioritize multi-channel reusability.
5. **Expand Architecture & Technical Scopes**:
    *   Expand the Information Architect's deliverables to include Web, Mobile, eBook, and App navigation.
    *   Assign XML framework, stylesheet, and template creation to Information Technologists.
    *   Mandate multi-rendition asset creation and rich metadata tagging for the Art department.
6. **Modernize Publishing Workflows** (If applicable to the domain):
    *   Shift Acquisitions to suite-based procurement.
    *   Shift Development Editors to online coordination and eBook integrity checks.
    *   Shift Assistant Editors to XML conversion and placeholder management.
    *   Shift Copy Editors to collaborative online review tools.
    *   Shift Production to XML-import template design.
7. **Generate Output**: Output the finalized role definitions, explicitly noting the transition from legacy duties to UCS duties.

# @Examples (Do's and Don'ts)

### Defining Author Responsibilities
- **[DO]**: "The Internal Author is responsible for writing structured content components, focusing entirely on the core message and identifying opportunities for reuse across the product family. Formatting is handled automatically by the CMS."
- **[DON'T]**: "The Internal Author is responsible for writing the document, applying the correct font styles, and ensuring the layout looks good for the final PDF." *(Anti-pattern: Internal authors in a UCS must not perform formatting or layout tasks).*

### Defining Content Ownership
- **[DO]**: "The Unified Content Owner will oversee the creation and integration of both common safety warnings and specific operational procedures across the entire Model X product family."
- **[DON'T]**: "John is the owner of the Model X User Manual and will write and maintain the entire document from start to finish." *(Anti-pattern: Document-level ownership creates silos. Ownership must be component-based and collaborative).*

### Defining Publishing Production
- **[DO]**: "The Production-Print team will design InDesign templates structured to automatically import XML components. Author revisions will be made in the XML source, and the Production team will simply re-import the updated XML."
- **[DON'T]**: "The Production-Print team will receive marked-up PDFs from the Assistant Editor and manually type the author's revisions into the page layout files." *(Anti-pattern: Manual revision entry by production is obsolete in a UCS; revisions must happen in the XML).*

### Defining the Assistant Editor Role
- **[DO]**: "The Assistant Editor will convert the external author's manuscript to XML, insert image placeholders, verify the XML index, and test the resulting eBook output."
- **[DON'T]**: "The Assistant Editor will print out copies of the manuscript for the author and manually type in the author's handwritten edits." *(Anti-pattern: Assistant editors must transition to XML management and online workflows).*

### Defining the Business Analyst Role
- **[DO]**: "The Business Analyst will gather requirements to ensure the new content models meet the end-customers' multi-channel needs while also providing a usable, efficient workflow for the internal authors."
- **[DON'T]**: "The Business Analyst will gather system requirements to select the best XML authoring software for the IT department." *(Anti-pattern: Business analysts must advocate for both customer needs and the authors' working environment, not just technical solutions).*