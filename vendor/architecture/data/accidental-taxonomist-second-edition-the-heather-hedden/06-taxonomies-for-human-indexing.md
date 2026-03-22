@Domain
These rules MUST be triggered whenever the AI is tasked with designing, building, reviewing, or modifying taxonomies, controlled vocabularies, thesauri, or user interfaces intended specifically for manual use by Human Indexers (including catalogers, taggers, or subject matter experts). This applies to open indexing, database indexing, enterprise tagging structures, folksonomy management, and the creation of indexing editorial policies.

@Vocabulary
- **Tagging / Keywording:** The assignment of terms to content, which may or may not use a controlled vocabulary, often performed by non-indexers (authors/editors).
- **Cataloging:** The organization and description of library materials, archive documents, or museum collections, encompassing both descriptive metadata, physical classification, and subject indexing.
- **Classification:** The assignment of an item to a single, unique class or physical/virtual location (e.g., a call number).
- **Indexing:** The creation of pointers (terms) to content to facilitate retrieval.
- **Open Indexing (Database Indexing):** Continuous, document-level indexing of accumulating content over time, requiring a controlled taxonomy to maintain consistency across multiple indexers.
- **Closed Indexing:** Fixed-scope indexing, such as back-of-the-book indexing, which is highly granular (paragraph/sentence level) and rarely uses a formal taxonomy.
- **Weighting:** The designation of an assigned index term as primary (major) or secondary (minor) to influence search result relevance sorting.
- **Inverted Terms:** Phrase inversions used as nonpreferred terms to aid alphabetical lookup (e.g., "libraries, public").
- **Shortcuts:** Acronyms, abbreviations, or codes used as nonpreferred terms to save indexers keystrokes (e.g., "ACQ" for "acquisitions").
- **USE-I / UF-I:** Equivalence relationships (Use / Used For) designated exclusively for the indexing interface, hidden from end-user search interfaces.
- **Indexer Notes:** Instructions specific to human indexers explaining when or how to apply a term, distinct from general scope notes.
- **Structured Indexing (Second-Level Indexing):** A form of precoordination using a main heading term followed by a subdivision term (e.g., "Alzheimer's Disease—Diagnosis").
- **Candidate Terms (Unapproved Terms):** New terms proposed by indexers during the indexing process that await taxonomist review.
- **Folksonomy (Social Tagging / Collaborative Tagging):** Uncontrolled, bottom-up, user-generated keyword tags assigned to content.
- **ROT:** Redundant, obsolete, or trivial content or tags.

@Objectives
- Optimize the taxonomy structure and term formats to maximize the speed, accuracy, and consistency of human indexers.
- Differentiate taxonomy features intended for human indexers from those intended for end-user searchers or automated systems.
- Establish strict editorial policies, quality control loops, and feedback mechanisms between indexers and taxonomists.
- Leverage distinct vocabularies and facets to enforce indexing rules.
- Effectively harvest and govern folksonomies/social tags to inform formal taxonomy growth without compromising authority control.

@Guidelines

**1. Indexing Paradigm Identification**
- The AI MUST distinguish between the type of human indexing required:
  - If assigning single locations, apply **Classification** rules.
  - If handling physical/digital archive items with descriptive metadata, apply **Cataloging** rules.
  - If assigning multiple terms to ongoing content, apply **Open Indexing** rules.
  - If creating a book index, apply **Closed Indexing** rules.

**2. Term Creation for Human Indexers**
- **Inverted Terms:** The AI MUST generate phrase-inverted nonpreferred terms (e.g., `Pants, dress USE Dress pants`) to facilitate alphabetical browsing for indexers.
- **Shortcuts:** The AI MUST create logical, short alphanumeric codes as nonpreferred terms for highly used categories (e.g., `FRE USE Financial results & earnings`) to save keystrokes.
- **Indexing-Only Synonyms:** If a nonpreferred term is useful for an indexer but would confuse an end-user search (e.g., upward posting a very specific concept to a broader term), the AI MUST designate the relationship as `USE-I` / `UF-I` (Indexing Only).

**3. Relationships and Term Notes**
- **Associative Relationships (RT):** The AI MUST extensively map associative relationships across different hierarchies (e.g., mapping a product to an action, or a discipline to an object) to help indexers discover more accurate terms during manual lookup.
- **Hierarchical Relationships (BT/NT):** The AI MUST map strict hierarchies to allow indexers to drill down to the most specific applicable term.
- **Indexer Notes:** The AI MUST generate specific `Indexer Notes` for broad, ambiguous, or highly technical terms. These notes MUST dictate usage rules (e.g., "Use a more specific term if possible" or "Use this term primarily for articles related to X. For Y, use Z").

**4. Taxonomy Structure and Indexing UI Features**
- **Distinct Vocabularies:** The AI MUST separate taxonomies into distinct authority files or facets (e.g., Topics, People, Organizations, Locations). This separation MUST be used to enforce UI-level indexing limits (e.g., "Max 4 locations, Min 2 topics").
- **Structured Indexing:** If highly precise retrieval is required (e.g., academic/medical), the AI MUST implement a secondary controlled vocabulary of standard subdivisions (e.g., Treatment, History, Diagnosis) to be appended to main headings.
- **UI Design Requirements:** When specifying UI requirements for indexing tools, the AI MUST require:
  - Truncated/start-of-word alphabetical search (with a toggle for nonpreferred terms).
  - Hierarchical tree browsing.
  - Hyperlinked cross-references from nonpreferred to preferred terms.
  - Dedicated panes/windows for term records (BT, NT, RT, Notes).
  - Keyboard shortcuts for rapid term entry and validation.

**5. Vocabulary Management Levels**
- When establishing the indexing workflow, the AI MUST define and enforce one of the following term-creation permission levels:
  1. **Strict Control:** Indexers use only existing terms. Candidate terms must be approved by a taxonomist before use (content goes on hold).
  2. **Unapproved Allowed (Entities Only):** Indexers may create and immediately use candidate terms for Named Entities (people, companies), but subject/topic terms require taxonomist approval.
  3. **Unapproved Allowed (All):** Indexers may create and immediately use candidate terms for any concept, subject to retroactive taxonomist review/cleanup.
  4. **Mixed (Taxonomy + Keywords):** Indexers use a controlled taxonomy for core facets, but assign uncontrolled keywords for supplemental metadata.

**6. Indexing Editorial Policy**
- The AI MUST generate a comprehensive Indexing Editorial Policy that defines:
  - Criteria for subject relevance (when a passing mention is NOT indexed).
  - Granularity and level of detail.
  - Sibling Thresholds (e.g., "If 3 or more narrower sibling terms apply, index with the broader parent term instead").
  - Term combination rules.
  - Weighting criteria (when to mark a term as Primary vs. Secondary).

**7. Folksonomy and Social Tagging Management**
- The AI MUST treat folksonomies (social tags) as supplemental to, not replacements for, formal taxonomies.
- The AI MUST establish a governance cycle for folksonomies: periodically harvest user-generated tags, analyze for frequency, merge synonymous/variant tags into a single preferred tag, and promote highly stable, high-value tags into the formal controlled taxonomy.

**8. Taxonomy Quality Control and Improvement**
- The AI MUST use indexer behavior to refine the taxonomy:
  - Underused terms -> The AI MUST generate additional nonpreferred terms/synonyms.
  - Overused terms -> The AI MUST split the concept into multiple narrower terms.
  - Frequently combined terms -> The AI MUST create a single precoordinated term.
  - Misused terms -> The AI MUST write clarifying Indexer Notes.

@Workflow
1. **Analyze Indexing Context:** Determine if the project requires Open Indexing, Cataloging, or Classification. Assess the volume of content and the subject matter expertise of the human indexers.
2. **Determine Vocabulary Management Level:** Select the appropriate permission level (Strict, Unapproved Entities, Unapproved All, or Mixed) based on content turnaround speed requirements and available taxonomist resources.
3. **Structure Distinct Vocabularies:** Segment the taxonomy into logical facets (Topics, Organizations, Places) to enforce indexing limits and UI simplicity.
4. **Generate Terms & Shortcuts:** Populate preferred terms, then generate standard synonyms, inverted terms (for alphabetical lookup), and shortcut codes (for rapid entry).
5. **Establish Relationships:** Map comprehensive hierarchical (BT/NT) and associative (RT) relationships specifically to guide human indexers to the most precise terms.
6. **Draft Indexer Notes:** Write instructional notes for terms prone to misuse or over-generalization.
7. **Write the Editorial Policy:** Document the rules for relevance, weighting, minimum/maximum term limits, and sibling thresholds.
8. **Establish the Feedback Loop:** Define the UI/workflow mechanism for indexers to suggest candidate terms and report missing concepts to the taxonomist.
9. **Folksonomy Integration (If Applicable):** Define the schedule and rules for cleaning up user-generated tags and promoting them to the formal taxonomy.

@Examples

**[DO]**
```markdown
**Preferred Term:** Public libraries
**UF (Used For):** 
- Community libraries
- Libraries, public (Inverted term for A-Z browse)
- PLIB (Shortcut code for rapid data entry)
**BT:** Libraries
**RT:** Public librarians
**Indexer Note:** Use this term strictly for the institution or organization. For the physical buildings, assign this term AND "Library buildings". Do not assign if the document only briefly mentions a public library in passing.
```

**[DON'T]**
```markdown
**Preferred Term:** Public libraries
**Synonyms:** Community libraries, Libraries, public, PLIB
**Note:** A library that is accessible by the general public.
*(Explanation: Fails to use standard UF/BT/RT tagging. Mixes inverted terms and shortcuts as generic synonyms without UI designation. The note is a generic dictionary definition (Scope Note) rather than an actionable Indexer Note.)*
```

**[DO]**
```markdown
**Editorial Policy: Sibling Threshold Rule**
When indexing a document that discusses multiple specific concepts under a single category:
- If the document covers 1 or 2 specific narrower terms (e.g., Apples, Bananas), assign those specific terms.
- If the document covers 3 or more narrower sibling terms (e.g., Apples, Bananas, Oranges), DO NOT assign the specific terms. Instead, assign the immediate Broader Term (BT): "Fruit".
```

**[DON'T]**
```markdown
**Editorial Policy: Sibling Threshold Rule**
Index every fruit mentioned in the document so the search engine can find it. If the text mentions apples, bananas, and oranges, tag all three plus the word fruit just to be safe.
*(Explanation: Encourages over-indexing and violates standard human indexing policies regarding sibling thresholds and upward posting, which degrades precision.)*
```

**[DO]**
```markdown
**Folksonomy Governance Procedure:**
1. Monthly, export top 100 uncontrolled tags generated by users/authors.
2. Identify ROT (Redundant, Obsolete, Trivial) tags and deprecate.
3. Consolidate lexical variants (e.g., "UX", "user experience", "User exp") by mapping them as nonpreferred terms to a newly designated preferred tag.
4. If a consolidated tag sustains high volume for 2 consecutive quarters, formally promote it into the enterprise taxonomy with full BT/NT/RT relationships.
```

**[DON'T]**
```markdown
**Folksonomy Governance Procedure:**
Allow users to tag content with whatever keywords they want. The search engine will index these keywords automatically, so the taxonomy will naturally build itself over time without taxonomist intervention.
*(Explanation: Treats folksonomy as a replacement for taxonomy, ignoring the inherent flaws of social tagging (inconsistency, low precision/recall, bias) explicitly warned against in the text.)*
```