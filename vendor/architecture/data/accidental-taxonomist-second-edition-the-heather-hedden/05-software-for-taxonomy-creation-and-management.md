@Domain
These rules MUST trigger when the user requests assistance with selecting, configuring, migrating, or structuring data for taxonomy, thesaurus, or ontology management software. This includes formatting import/export files (such as CSV, XML, or SKOS), evaluating taxonomy management tools, writing scripts for taxonomy validation, or designing taxonomy structures for implementation within Content Management Systems (CMS) like Microsoft SharePoint.

@Vocabulary
- **ANSI/NISO Z39.19 / ISO 25964**: The primary international standards for thesaurus creation. Software compliant with these enforces strict relationship rules.
- **SKOS (Simple Knowledge Organization System)**: A W3C standard based on RDF for knowledge organization systems, often permitting more flexible relationships than strict thesaurus standards.
- **OWL (Web Ontology Language)**: A semantic markup language for publishing and sharing ontologies.
- **SaaS (Software-as-a-Service)**: Cloud-hosted software deployment, a major trend in taxonomy management systems.
- **Node**: A concept or term location within a taxonomy management system interface.
- **Polyhierarchy**: A structure where a term has more than one broader term; varying taxonomy software handles this differently.
- **Orphan Term**: A term lacking any hierarchical or associative relationships; good taxonomy software provides quality checks to flag these.
- **Circular Relationship**: An illegal taxonomy structure where a term's broader term is also a narrower term to one of its own narrower terms.
- **CSV (Comma-Separated Values)**: A flat-file format frequently used for taxonomy import/export, requiring specific column structuring to represent hierarchies.
- **TBX (TermBase eXchange / ISO 30042)**: A standard for terminological data interchange (supported by tools like Coreon).
- **Term Store**: Microsoft SharePoint's Managed Metadata Service interface for taxonomy management.
- **Wordmap Nomenclature**: Specific terminology used by the Wordmap software: *Wordset* (concept/node), *Lead word* (preferred term), *Members* (nonpreferred terms), *Physical relationships* (hierarchical), *Nonphysical relationships* (associative).
- **Ontology Nomenclature**: Terms utilized by ontology-centric software (like SAS Ontology Management or Protégé): *Classes*, *Slots*, *Instances/Individuals*.

@Objectives
- Format and structure taxonomy data accurately for import/export across different software platforms, specifically handling the limitations of spreadsheet-based CSV imports.
- Programmatically enforce strict taxonomy standards (ANSI/NISO, ISO) when the target software platform lacks native rule enforcement.
- Provide accurate architectural recommendations based on the specific capabilities, standard compliance, and limitations of varying taxonomy, thesaurus, and ontology software tools.
- Adapt taxonomy data models to the specific nomenclature and constraints of the target system (e.g., SharePoint Term Store, SKOS models, or Wordmap).

@Guidelines

**Data Formatting for Spreadsheet/CSV Import**
- When structuring hierarchical taxonomy data in Excel/CSV for import into taxonomy software, the AI MUST repeat the broader terms in every row for a given branch.
- The AI MUST NOT leave blank cells to the left of a filled-in cell in a CSV import file. Each row must represent a unique path from the top-level term to the narrowest term.
- When placing multiple nonpreferred terms in a spreadsheet column, the AI MUST separate them using a designated delimiter (e.g., a semicolon or pipe) within a single cell.

**Programmatic Rule Enforcement & Quality Control**
- Because not all software (e.g., SharePoint, early versions of TemaTres) natively enforces taxonomy rules, the AI MUST implement or prompt for programmatic validation checks that prohibit:
  1. Terms relating to themselves.
  2. Pairs of terms having more than one kind of relationship between them (e.g., a term cannot be both a Broader Term and a Related Term to the same concept).
  3. Circular relationships (e.g., Term A > BT Term B > BT Term C > BT Term A).
  4. Duplicate term names representing different concepts within the same taxonomy (unless explicitly handled via polyhierarchy mechanisms).
- The AI MUST provide scripts or queries to flag "orphan terms" (terms with no relationships) for human review.

**Software-Specific Architectural Constraints**
- **Microsoft SharePoint (Term Store)**: When designing for SharePoint, the AI MUST account for its limitations: it does not enforce standard taxonomy rules (allows circular relationships and duplicates), it does not support associative (Related Term) relationships natively, and polyhierarchy requires the explicit "Reuse Terms" function (often limited to crossing different facets).
- **Protégé**: When targeting this ontology editor, the AI MUST warn the user that it lacks a standard equivalence relationship (nonpreferred terms) by default, requiring workarounds or SKOS plug-ins.
- **TemaTres**: When dealing with this open-source tool, the AI MUST account for the fact that duplicates can be easily created and are only detected via retrospective quality reports.
- **MultiTes**: When preparing displays or reports for MultiTes, the AI MUST note that the software relies on alphabetical views and pop-ups, lacking an interactive hierarchical tree interface.
- **ThManager**: The AI MUST account for the interface flaw where broader/narrower links display term IDs instead of labels.

**System Selection & Recommendation**
- When the user requires software for Semantic Web integration or Linked Open Data, the AI MUST recommend SKOS/OWL-compliant systems (e.g., PoolParty, TopBraid EVN, Mondeca ITM, VocBench).
- When the user requires strict thesaurus standard enforcement (ISO 25964 / ANSI/NISO Z39.19), the AI MUST recommend dedicated thesaurus systems (e.g., Data Harmony Thesaurus Master, Synaptica, Semaphore).
- When the user requires multilingual taxonomy support with terminological translation standards, the AI MUST recommend systems with native multilingual concept support (e.g., Coreon [TBX support], VocBench, MultiTes).
- When the user requires a lightweight taxonomy for localized intranet CMS tagging without complex associative relationships, the AI MUST suggest SharePoint Managed Metadata or native CMS taxonomy components.

**Nomenclature Translation**
- The AI MUST translate standard taxonomy concepts into the specific nomenclature of the target software.
  - *If Wordmap:* Concept -> Wordset; Preferred Term -> Lead word; Nonpreferred Term -> Members; Hierarchical -> Physical; Associative -> Nonphysical.
  - *If SAS Ontology Management / Protégé:* Term -> Instance/Individual; Category -> Class; Attribute -> Slot.
  - *If SKOS-based (PoolParty, TopBraid):* Term -> Concept; Preferred Term -> prefLabel; Nonpreferred Term -> altLabel.

@Workflow
1. **Analyze Target System**: Identify the specific software or standard the user is targeting (e.g., SharePoint, SKOS XML, Excel CSV, Data Harmony).
2. **Apply System Nomenclature**: Map standard taxonomy terms (BT, NT, RT, UF, Concept) to the target system's vocabulary (e.g., prefLabel, Wordset, Class).
3. **Format the Data Structure**:
   - If CSV: Ensure dense rows with repeating parent terms and no empty left-side cells.
   - If XML/SKOS/OWL: Ensure proper nesting, namespace declarations, and URI assignments.
4. **Execute Constraint Validation**: Run internal logic checks on the provided data to ensure no circular references, duplicate concepts, or conflicting relationships exist, explicitly compensating for systems (like SharePoint) that lack native validation.
5. **Output Delivery & Warnings**: Provide the requested data, script, or analysis. Explicitly list any software-specific limitations the user will encounter (e.g., "Note: SharePoint will not support the associative relationships mapped in this data").

@Examples

**[DO] Format CSV for Taxonomy Import**
```csv
Level 1,Level 2,Level 3,Nonpreferred Terms
Vehicles,Automobiles,Sedans,Cars; Autos
Vehicles,Automobiles,SUVs,
Vehicles,Trucks,,Pickups
```
*(Notice how "Vehicles" and "Automobiles" are repeated to ensure no blank cells to the left of a filled-in cell, establishing a clear hierarchical path for the import parser).*

**[DON'T] Format CSV for Taxonomy Import with Blank Cells**
```csv
Level 1,Level 2,Level 3,Nonpreferred Terms
Vehicles,Automobiles,Sedans,Cars; Autos
,,SUVs,
,Trucks,,Pickups
```
*(This "staircase" visual format is useful for human review but violates taxonomy software import requirements because of the blank cells to the left).*

**[DO] Validate Relationships Programmatically**
```python
# AI enforces taxonomy rules by checking for conflicting relationships
def validate_relationships(taxonomy_data):
    for term, relations in taxonomy_data.items():
        # A term cannot be both a Broader Term and a Related Term to the same target
        overlap = set(relations['BT']).intersection(set(relations['RT']))
        if overlap:
            raise ValueError(f"Rule Violation: {term} shares BT and RT relationships with {overlap}")
```

**[DON'T] Rely on CMS Native Capabilities for Complex Thesauri**
User: "Can I just put this 5,000-term thesaurus with BT, NT, RT, and UF relationships directly into SharePoint?"
AI Response (Incorrect): "Yes, just import it into the SharePoint Term Store."
AI Response (Correct): "You can import the hierarchical (BT/NT) and equivalence (UF) relationships into the SharePoint Term Store using a CSV. However, SharePoint does not natively support associative (RT) relationships. Furthermore, SharePoint will not warn you if you create circular relationships. For a complex thesaurus, it is recommended to manage the taxonomy in a dedicated tool (like Synaptica or PoolParty) and use a connector to push the hierarchical subset to SharePoint."