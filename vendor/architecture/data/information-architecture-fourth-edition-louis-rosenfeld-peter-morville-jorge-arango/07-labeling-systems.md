@Domain
Trigger these rules when tasked with designing user interfaces, creating navigation menus, defining routing structures, writing hypertext links, generating sitemaps, establishing metadata tags, constructing taxonomies, or writing any user-facing text that categorizes, represents, or describes chunks of information within a digital product, website, or application.

@Vocabulary
- **Label**: A textual or iconic shortcut used to represent a larger chunk of information, conveying meaning efficiently without taking up excessive physical or cognitive space.
- **Contextual Link**: A hyperlink within the body of a document or prose that relies on surrounding text to establish its meaning and context.
- **Heading**: A label used to establish hierarchy and describe the specific chunk of information that follows it.
- **Navigation System Choice**: A highly prominent, frequently repeated label representing options in a navigation menu.
- **Index Term**: A keyword, tag, descriptive metadata, or controlled vocabulary term used invisibly or visibly to represent content for searching or browsing.
- **Iconic Label**: A visual/graphical label used in space-constrained environments (like mobile interfaces) to represent information.
- **Granularity**: The relative specificity or broadness of a term (e.g., "Restaurants" vs. "Chinese Restaurants").
- **Comprehensiveness**: The extent to which a labeling system covers all necessary options without noticeable gaps.
- **Free-listing**: A research method where users brainstorm terms to describe a specific item.
- **Card Sorting**: A research method (open or closed) used to discover how users tacitly group, sort, and label tasks and content.
- **Search Analytics / Log Analysis**: The study of user search queries to understand the exact terminology users employ when seeking information.

@Objectives
- Communicate information efficiently, acting as a cognitive shortcut to larger content chunks.
- Speak the exact same language as the target audience while accurately reflecting the underlying content.
- Ensure strict predictability and consistency across all labeling systems to eliminate user confusion and cognitive friction.
- Differentiate options clearly so users never have to guess the difference between two labels.
- Educate users about new concepts while helping them quickly identify familiar ones.

@Guidelines

**General Labeling Constraints**
- The AI MUST NOT use organizational jargon or internal company terminology; labels MUST be user-centric.
- The AI MUST narrow the scope of labeling systems. If an environment serves radically different audiences, the AI MUST create modular, separate labeling systems for each rather than a single compromised system.
- The AI MUST ensure labels are mutually exclusive. Users must never be forced to guess the difference between labels (e.g., "Coffee", "Coffeehouse", and "Shop" in the same menu).
- The AI MUST NOT use the same label to represent two different kinds of information within the same system.

**Consistency Rules**
- **Syntax**: The AI MUST strictly unify the grammatical syntax of labels within a single system (e.g., all nouns, all verbs, or all questions). DO NOT mix verb-based and noun-based labels in the same list.
- **Granularity**: The AI MUST group labels of roughly equal specificity. Do not mix broad categories with hyper-specific items in the same menu level.
- **Comprehensiveness**: The AI MUST ensure there are no noticeable gaps in a categorical list (e.g., listing pants, shoes, and accessories, but omitting shirts).
- **Style & Presentation**: The AI MUST enforce consistent capitalization, punctuation, font sizes, and grouping mechanisms across the labeling system.

**Contextual Links**
- The AI MUST design link text to accurately represent the destination content. Ask: "What kind of information will the person expect to be taken to?"
- The AI MUST leverage the surrounding prose to provide context.

**Headings**
- The AI MUST use headings to visually establish hierarchy (using numbering, typography, and whitespace).
- When labeling steps in a sequential process, the AI MUST use numbers to convey progression and verbs to convey the required action for each step.

**Navigation System Choices**
- The AI MUST rely on established, standard conventions for common navigation items (e.g., Home, Search, About Us, Contact Us) to build familiarity.
- If navigation labels are potentially ambiguous, the AI MUST include brief descriptive text beneath or alongside them, space permitting.

**Index Terms & Metadata**
- The AI MUST embed index terms in invisible metadata (like HTML `<meta>` tags or database records) to capture synonyms and user-specific vocabulary that may not appear in the visible text.

**Iconic Labels**
- The AI MUST NOT place form over function. If an icon's meaning is ambiguous, the AI MUST accompany it with a textual label unless the audience is highly trained or the option set is severely limited.

@Workflow
1. **Scope and Audience Definition**: Identify the target audience and the specific context of the system. Define the boundaries of the labeling system (global navigation vs. local sub-menu).
2. **Sourcing Candidates**: Gather candidate labels by:
   - Extracting terms from the content itself (Content Analysis).
   - Reviewing comparable/competitor systems to identify industry typologies.
   - Referencing established controlled vocabularies/thesauri if the domain is specialized.
   - Analyzing user data (search logs, free-listing, or card sorting results) to capture the user's exact vocabulary.
3. **Selection and Refinement**: Filter the candidate labels. Eliminate duplicates and resolve synonyms. 
4. **Consistency Enforcement**: Review the selected labels as a complete system. Normalize the syntax (e.g., convert all to gerunds or all to nouns). Equalize the granularity. Fix any gaps in comprehensiveness. Apply consistent casing and style.
5. **Contextual Validation**: Map the labels onto the UI structure (wireframe or sitemap). Ensure visual hierarchy supports the labels. For contextual links, verify that the surrounding text clarifies the destination.
6. **Future-Proofing**: Evaluate the system for scalability. Ensure that phantom/future content can fit into the defined labeling conventions without breaking the logic.

@Examples (Do's and Don'ts)

**Syntax Consistency**
- [DO]: "Grooming Your Dog", "Feeding Your Dog", "Training Your Dog" (Consistent gerund phrasing).
- [DON'T]: "Grooming Your Dog", "Dog Diets", "How to Train Your Dog" (Mixed syntax causes cognitive friction).

**Granularity in Navigation**
- [DO]: "Restaurants", "Grocery Stores", "Cafes" (Equal specificity).
- [DON'T]: "Restaurants", "Chinese Restaurants", "Burger King" (Mixed granularity confuses the taxonomy).

**Sequential Headings**
- [DO]: "1. Create Account", "2. Enter Billing Information", "3. Confirm Purchase" (Numbered, verb-led, clear sequence).
- [DON'T]: "Account", "Billing", "Finish" (Lacks clear action and sequential progression).

**Navigation System Conventions**
- [DO]: "About Us", "Contact Us", "FAQ".
- [DON'T]: "Who We Are", "Reach Out", "Inquiries and Mysteries" (Do not reinvent standard navigational conventions without a highly specific brand justification).

**Label Differentiation**
- [DO]: "Buy Coffee Beans", "Find a Cafe", "Merchandise" (Clear, mutually exclusive intent).
- [DON'T]: "Coffee", "Coffeehouse", "Shop" (Ambiguous, overlapping meanings that force the user to guess the destination).