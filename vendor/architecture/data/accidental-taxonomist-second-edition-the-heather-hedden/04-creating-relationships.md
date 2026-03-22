@Domain
Triggers when the AI is asked to design, review, modify, audit, or generate a taxonomy, thesaurus, controlled vocabulary, ontology, or metadata schema. Activates when dealing with terms, concepts, tags, knowledge organization systems (KOS), semantic relationships, information architecture hierarchies, or document indexing classifications.

@Vocabulary
- **Concept**: A thing, idea, or shared understanding that is represented by a set of synonymous terms (preferred and nonpreferred). 
- **Reciprocal Relationship**: A bidirectional connection between a pair of terms (e.g., Term A points to Term B, and Term B points to Term A).
- **Asymmetrical Relationship**: A reciprocal relationship that is not identical in both directions (e.g., Broader/Narrower, Use/Used For).
- **Symmetrical Relationship**: A reciprocal relationship that is identical in both directions (e.g., Related Term / Related Term).
- **Equivalence Relationship (USE/UF)**: An asymmetrical relationship between a preferred term and a nonpreferred term. (USE = "use preferred term"; UF = "used for nonpreferred term").
- **Nonpreferred Term (NPT)**: A variant term, synonym, or alias that redirects the user or indexer to the accepted preferred term. Also known as entry terms, lead-in terms, or alternate labels.
- **Upward Posting (Generic Posting)**: The practice of designating a narrower concept as a nonpreferred term that points to a broader preferred term, used when there is insufficient content to justify a distinct narrower term.
- **Hierarchical Relationship (BT/NT)**: An asymmetrical relationship denoting subordination (BT = Broader Term; NT = Narrower Term).
- **Generic-Specific (BTG/NTG)**: A hierarchical relationship indicating a category and its members ("is a" relationship).
- **Instance (BTI/NTI)**: A hierarchical relationship between a generic class and a unique named entity (proper noun).
- **Whole-Part (BTP/NTP)**: A hierarchical relationship where a narrower term is a constituent part of a broader system, organization, or geographic place.
- **Polyhierarchy / Multiple Broader Terms (MBT)**: A structure in which a single term has more than one broader term (parent).
- **Associative Relationship (RT)**: A symmetrical relationship linking terms that are conceptually related but not hierarchically subordinate (RT = Related Term).
- **Sibling Terms**: Terms that share the exact same broader term.
- **Semantic Relationships**: Customized, domain-specific relationships possessing richer meaning than standard BT/NT/RT labels (e.g., "Produces the product" / "Is manufactured by").
- **Orphan Term**: A term in a taxonomy lacking any relationships to other terms (generally prohibited).

@Objectives
- Accurately map concepts using strictly reciprocal relationships to build a cohesive knowledge organization system.
- Enforce the "All/Some Rule" flawlessly across all hierarchical structures.
- Eradicate ambiguity by strategically employing equivalence relationships, scope notes, and structural disambiguation.
- Design taxonomy structures that perfectly balance indexing efficiency with end-user search and discovery behaviors.
- Ensure strict compliance with ANSI/NISO Z39.19 / ISO 25964 thesaurus relationship standards.

@Guidelines

**1. Equivalence Relationships (USE/UF)**
- MUST define a single preferred term for each concept and map all relevant variants as nonpreferred terms pointing to it.
- MUST use asymmetrical syntax: Nonpreferred term `USE` Preferred term; Preferred term `UF` Nonpreferred term.
- MUST map multiple nonpreferred terms to a single preferred term where applicable.
- MAY use 1-to-many equivalence (USE AND / USE PLUS) ONLY for precoordinated concepts where a nonpreferred term explicitly requires two combined preferred terms to convey the concept (e.g., `folk drama USE drama AND folk culture`).
- MUST evaluate the necessity of nonpreferred terms based on the search interface: If the taxonomy relies heavily on a user search box (versus browsing) or automated text matching, dramatically increase the volume of nonpreferred terms.
- ACCEPTABLE types of nonpreferred terms: Synonyms, Near-Synonyms (if scope does not require distinction), Variant Spellings, Lexical Variants (e.g., hair loss / baldness), Foreign Language Terms, Acronyms (ONLY if unambiguous in context), Phrase Inversions (useful for alphabetical indexer browsing, e.g., `buses, school USE school buses`), and Antonyms (for characteristic attributes, e.g., `illiteracy USE literacy`).
- CAUTION with Upward Posting: Use narrower concepts as nonpreferred terms ONLY if user search behavior warrants it and if it will not dilute keyword search accuracy. If an end-user searches the narrow term, they must be made aware they are retrieving broader results.

**2. Hierarchical Relationships (BT/NT)**
- MUST apply the "All/Some Rule" to EVERY hierarchical pairing: All members of the narrower term MUST be contained within the broader term. Only some members of the broader term constitute the members of the narrower term. 
- MUST validate hierarchical relationships using one of four phrase tests:
  1. Narrower terms are a (kind of) broader term.
  2. Narrower term is a specific instance of broader term.
  3. Narrower terms are a constituent part of (the) broader term.
  4. Narrower term is within (the) broader term.
- Polyhierarchies (MBT) are PERMITTED, but the narrower term MUST pass the All/Some rule for EVERY broader term it is assigned to.
- PROHIBITED: A term CANNOT be designated as a narrower term to both a parent term and a grandparent term within the same direct lineage (no direct circular references or skipping levels).

**3. Associative Relationships (RT)**
- MUST use symmetrical syntax: Term A `RT` Term B; Term B `RT` Term A.
- MUST create associative relationships between terms in *different* hierarchies that share strong conceptual links (e.g., Process/Agent, Action/Product, Cause/Effect, Discipline/Practitioner).
- MUST create associative relationships between sibling terms (sharing the same BT) ONLY IF they have overlapping meanings (e.g., `local taxes RT property taxes`).
- PROHIBITED: Do NOT create associative relationships between sibling terms that are mutually exclusive (e.g., `radios` and `TV sets`).
- PROHIBITED: Do NOT create associative relationships between a term and its own broader or narrower terms.
- PROHIBITED: Do NOT recursively map all related terms of a related term to each other unless the direct conceptual link specifically warrants it.

**4. Resolving Hierarchical/Associative Ambiguities**
- Companies vs. Industries: Companies are NOT narrower terms (instances) of industries unless the industry term is explicitly named as a class of companies (e.g., `automobile manufacturers`). Otherwise, use an associative (RT) relationship.
- Members vs. Organizations: Members (individuals or countries) are NOT narrower terms (whole-part) of the organizations they belong to because membership can change. Use associative (RT) relationships. (Exception: if the broader term is phrased as `[Organization] Members`).
- Manufactured Systems: Parts capable of being removed from a whole (e.g., `automobile engines` and `automobiles`) MUST be treated as associative (RT) unless the specific context is a closed system manual (e.g., an auto repair manual).

**5. Semantic Variations for Relationships (Ontologies/Custom Taxonomies)**
- MUST base any customized semantic relationship strictly on one of the three foundational types (Equivalence, Hierarchical, Associative).
- MUST assign distinct, asymmetrical names and codes for both directions of a custom relationship, even if based on an associative relationship (e.g., `Produces the product (PRD)` / `Is manufactured by the company (COM)`).
- MAY utilize Semantic Equivalence to separate displayable vs. administrative nonpreferred terms (e.g., `COR` [Correct term] vs. `CORF` [Correct for] for misspellings that should not display to the user; `USE-I` / `UF-I` for terms visible only to indexers).

@Workflow
1. **Concept Identification & Equivalence Mapping**: Identify the core concept. Select the most accurate Preferred Term. Generate all necessary Nonpreferred Terms (Synonyms, Acronyms, Lexical Variants, Phrase Inversions). Establish `USE/UF` links.
2. **Hierarchical Structuring (BT/NT)**: Assign Broader Terms and Narrower Terms. 
   - Apply the "All/Some" test. 
   - Apply the phrasing test ("is a", "is instance of", "is constituent part of"). 
   - If a term fits under multiple parents, establish a Polyhierarchy, ensuring no parent-to-grandparent bypasses exist.
3. **Associative Linking (RT)**: Scan the taxonomy for related concepts in different hierarchies (e.g., linking a raw material to a manufactured product). Evaluate sibling terms under the same parent; add `RT` links ONLY if their meanings overlap.
4. **Ambiguity Resolution**: Audit Company/Industry, Member/Organization, and Part/Whole relationships. Convert invalid hierarchical links into associative links.
5. **Semantic Customization (If applicable)**: If the system supports ontologies or rich semantics, replace generic BT/NT/RT labels with specific asymmetrical semantic tags (e.g., `TRE` [For treating] / `DRUG` [Can be treated with the drug]).

@Examples (Do's and Don'ts)

**Equivalence Relationships (USE/UF)**
- [DO]: `school buses UF buses, school` (Using a phrase inversion as a nonpreferred term to aid alphabetical indexer browsing).
- [DON'T]: `automobiles UF cars` AND `autos UF cars`. (A single nonpreferred term should not point to multiple preferred terms unless utilizing a strict precoordinated `USE AND` rule).
- [DON'T]: `performers UF players`. (Do not use dictionary synonyms if they do not mean the exact same thing in all contexts. A player is not always a performer).

**Hierarchical Relationships (BT/NT)**
- [DO]: `fruits NT apples` (All apples are fruits, some fruits are apples. Passes the All/Some rule).
- [DON'T]: `breakfast dishes NT egg dishes` (Fails the All/Some rule. Egg dishes are not *always* for breakfast).
- [DON'T]: `technology NT biotechnology`, AND `biotechnology NT genetic engineering`, AND `technology NT genetic engineering`. (Prohibited grandparent bypass. Genetic engineering should only have biotechnology as its BT).
- [DON'T]: `OPEC NT Saudi Arabia`. (Fails whole-part test because membership can change. Use RT instead, or change BT to `OPEC countries`).

**Associative Relationships (RT)**
- [DO]: `taxes NT local taxes`, `taxes NT property taxes`. `local taxes RT property taxes`. (Siblings with overlapping meanings require an RT link).
- [DON'T]: `appliances NT radios`, `appliances NT TV sets`. `radios RT TV sets`. (Siblings that are mutually exclusive DO NOT get an RT link).
- [DO]: `engineering RT engineers`. (Cross-hierarchy link between discipline and practitioner).
- [DON'T]: If `computers RT computer peripherals`, and `computer peripherals NT keyboards`. DO NOT create `computers RT keyboards`. (Do not create associative relationships to the narrower terms of a related term).

**Semantic Variations**
- [DO]: Define asymmetrical semantic associative rules: `Apple Inc. PRD iPod`; `iPod COM Apple Inc.`
- [DON'T]: Use symmetrical labels for custom semantic relationships (e.g., `Apple Inc. MAKER iPod`; `iPod MAKER Apple Inc.` is invalid).