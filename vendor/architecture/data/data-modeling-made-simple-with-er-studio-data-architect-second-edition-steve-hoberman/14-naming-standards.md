@Domain
Trigger these rules when the user requests assistance with establishing, configuring, applying, migrating, or managing naming standards within a data model or database design, particularly when utilizing ER/Studio Data Architect, or when transforming logical data models into physical data models where naming consistency, abbreviation mapping, and structural naming rules must be rigorously enforced.

@Vocabulary
- **Naming Standards Template (NST)**: A configurable framework used to define organizational naming conventions, including abbreviation lists, text case, name lengths, and prefixes/suffixes. 
- **Internal Template**: A naming standards template bound solely to the current data model and saved within the model's local data dictionary.
- **External Template**: A universally accessible naming standards template saved as an independent XML file (with a `.nst` extension) in a shared directory, intended for use across multiple models.
- **Prime Word**: The primary subject or focal point of an attribute name (e.g., *Customer* in "Customer Last Name").
- **Qualifier (Modifier)**: The term used to further describe or restrict the prime word (e.g., *Last* in "Customer Last Name").
- **Class (Classword)**: The final term in a name that classifies the type of data the attribute holds (e.g., *Name* in "Customer Last Name", or *Amount*, *Code*, *Date*).
- **Naming Standards Utility**: The execution tool used to batch-apply a Naming Standards Template to an entire data model or a specific subset of objects within a model.
- **Freeze Names**: An operational state assigned to specific objects preventing the Naming Standards Utility from altering their names (vital for legacy database structures).
- **Automatic Naming Translation**: A background service enabled via model options that synchronizes and translates logical names to physical names in real-time during the editing process.
- **Complete Synchronization**: A setting within Automatic Naming Translation that automatically updates corresponding physical columns whenever a logical attribute name is changed.
- **Unification**: The process of changing the role names of foreign attributes to match the names of other attributes within the identical entity.
- **ISO-11179**: The international standard for representing metadata in an organization, heavily relied upon for naming standard best practices and definition writing.

@Objectives
- Establish strict enterprise-level naming consistency across all logical and physical data model artifacts.
- Automate the translation of verbose logical business names into compliant, abbreviated physical database column/table names.
- Enforce a structured, formulaic approach to naming construction using Prime words, Qualifiers, and Class words.
- Protect legacy or external system objects from unintended renaming via "Freeze" configurations.
- Ensure that parent-entity naming standards seamlessly cascade to child entities to maintain relationship clarity.

@Guidelines
- **Template Scoping**: When configuring a new standard, the AI MUST first determine the scope. If the standard is specific to one project, the AI MUST instruct the creation of an Internal Template. If the standard is an organizational baseline, the AI MUST instruct the creation of an External Template (`.nst` XML file).
- **Logical vs. Physical Rules**: The AI MUST enforce separate rules for Logical and Physical models. Logical names MUST prioritize business readability (e.g., standard casing, longer max lengths), whereas Physical names MUST adhere to RDBMS constraints (e.g., strict maximum lengths, specific uppercase/lowercase requirements, mandatory prefixes/suffixes).
- **Structural Name Construction**: The AI MUST enforce name construction utilizing the prime-qualifier-class pattern. The AI MUST ensure every attribute name can be parsed into a Prime word, an optional Qualifier, and a mandatory Class word.
- **Abbreviation Mappings**: When translating logical to physical models, the AI MUST utilize a defined abbreviation list. If a physical abbreviation maps to multiple logical words, the AI MUST enforce priority settings (Primary vs. Secondary) to resolve duplicate abbreviations.
- **Character and Separator Handling**: The AI MUST dictate the specific separator conventions (e.g., spaces for logical, underscores for physical) and actively specify rules for stripping or replacing illegal characters (e.g., `$`, `#`) during physical generation.
- **Legacy Protection (Freeze Names)**: When applying the Naming Standards Utility to a model that contains preexisting or legacy database objects, the AI MUST utilize the "Freeze Names" property to explicitly lock legacy attributes/tables from being overwritten by new templates.
- **Inheritance via Automatic Translation**: When configuring Automatic Naming Translation, the AI MUST enable the "Use entity/table NST for children" option to guarantee that child entities appropriately inherit the naming standards assigned to their parent entities.
- **Continuous Synchronization**: The AI MUST recommend enabling "Complete Synchronization" when the design workflow requires physical columns to instantly reflect renaming changes made to their logical attribute counterparts.
- **Fallback Standard**: If the user lacks an established organizational naming convention, the AI MUST default to proposing standards derived from ISO-11179.

@Workflow
1. **Evaluate Scope and Instantiate Template**:
   - Determine if the naming standard applies locally or globally.
   - For local: Guide the user to Data Dictionary -> Naming Standards Template -> New Naming Standards Template (Internal).
   - For global: Output instructions to save the template externally as an XML `.nst` file for reuse.
2. **Configure Object Lengths and Casings**:
   - Access the Logical tab: Set maximum lengths, standard case formatting, and logical prefixes.
   - Access the Physical tab: Set RDBMS-specific maximum lengths, physical casing (e.g., all uppercase), and physical prefixes/suffixes.
3. **Define Mapping and Construction Logic**:
   - Access the Mapping tab -> Abbreviations: Define Prime words, Qualifiers, and Class words. Populate logical-to-physical abbreviation pairs.
   - Access the Mapping tab -> Order: Establish the sequence of terms (e.g., Prime + Qualifier + Class).
   - Access the Mapping tab -> General: Set separator characters (e.g., space to underscore) and define illegal character replacement logic.
4. **Establish Protection Boundaries**:
   - Identify any existing database structures within the model that cannot be altered.
   - Apply the "Freeze Names" attribute to these specific entities, tables, or columns.
5. **Apply the Standards**:
   - **Batch Mode**: Instruct the use of `Model > Naming Standards Utility`. Select the target template on the Options tab, select the target objects on the Output tab, and execute the translation.
   - **Continuous Mode**: Instruct the user to navigate to `Tools > Options > Naming Handling`. Enable Automatic Naming Translation, check "Use entity/table NST for children", and configure Complete Synchronization.

@Examples (Do's and Don'ts)

- **Template Scoping**
  - [DO]: Instruct the creation of an External `.nst` Template if the user mentions defining standards for the "Enterprise Data Warehouse Program" containing multiple subject-area data models.
  - [DON'T]: Recommend an Internal Template bound to the local Data Dictionary for enterprise-wide guidelines, as it prevents other `.dm1` files from sharing the standard.

- **Name Construction (Prime, Qualifier, Class)**
  - [DO]: Enforce logical naming as `[Prime] [Qualifier] [Class]`. For example: "Customer" (Prime) + "Last" (Qualifier) + "Name" (Class).
  - [DON'T]: Accept monolithic or unclassified names such as "CustLName" in the logical model without ensuring it parses into distinct Prime, Qualifier, and Class terms.

- **Protecting Legacy Objects**
  - [DO]: Direct the user to check the "Freeze Names" option in the Naming Standards tab for an entity named `TBL_OLD_CUST_SYS` to prevent the utility from renaming it to the new `CUSTOMER` standard.
  - [DON'T]: Blindly run the Naming Standards Utility across the entire model without analyzing whether existing physical structures rely on strict legacy names.

- **Abbreviation Conflict Resolution**
  - [DO]: Use the Priority column in the Mapping tab to resolve conflicts. If "ACCT" maps to both "Account" and "Accounting", set "Account" as *Primary* and "Accounting" as *Secondary*.
  - [DON'T]: Leave duplicate physical abbreviations unresolved, which causes translation failures or incorrect logical names during reverse translation.

- **Handling Child Entities**
  - [DO]: Enable the "Use entity/table NST for children" setting under Options so that when a parent entity applies a specific template, the resulting associative entities or subtype children automatically inherit the exact same Prime word and abbreviation rules.
  - [DON'T]: Manually apply standard templates to every individual child table if an automated parent-child inheritance option is available in the Naming Handling settings.