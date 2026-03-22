@Domain
Triggers when the user requests to synchronize data models, identify architectural drift between models and databases, reconcile differences between logical and physical designs, compare submodels, generate comparison reports, or explicitly invoke the ER/Studio "Compare/Merge Utility".

@Vocabulary
- **Compare and Merge Utility**: The ER/Studio feature used to reconcile differences, synchronize, and report on discrepancies between models in the same file, across different files, or between a model and a database/SQL file.
- **Source Model**: The currently open model (or submodel) from which the Compare and Merge Utility is initiated.
- **Target Model**: The model, submodel, database, or SQL file being compared against the Source Model.
- **Quick Launch**: A saved configuration of comparison settings that can be loaded to streamline repetitive Compare and Merge operations.
- **Resolution Values**: Actionable choices applied to identified differences during comparison, specifically: "Ignore", "Delete from current (source) model", or "Merge into target model".
- **Save Matches**: A defined mapping between two objects that prevents ER/Studio from flagging them as a difference in future comparisons.
- **Universal Mapping**: A saved match mapping defined between objects across *different* ER/Studio files.
- **User-Defined Mapping**: A saved match mapping defined between objects within the *same* ER/Studio file.
- **Submodel Comparison**: A strict comparison scope limited exclusively to comparing a submodel to another submodel within the *same* data model file.

@Objectives
- Reconcile differences and maintain synchronization between conceptual/logical models, physical models, and actual databases.
- Prevent and resolve architectural drift caused by independent modifications (e.g., a data modeler altering a model while a DBA alters a database table).
- Enforce strict compatibility rules when selecting Source and Target comparison artifacts.
- Guide the user systematically through the 5-page Compare and Merge Wizard to ensure comprehensive metadata and object selection.
- Generate actionable discrepancy reports (RTF or HTML) to facilitate team reviews before committing structural changes.

@Guidelines
- **Target Validation - Logical Data Models**: When the Source is a Logical Data Model, the AI MUST strictly permit comparisons ONLY to:
  1. A physical data model in the same `.dm1` file.
  2. A logical data model of another ER/Studio data model.
  3. A physical data model of another ER/Studio data model.
- **Target Validation - Physical Data Models**: When the Source is a Physical Data Model, the AI MUST strictly permit comparisons ONLY to:
  1. The logical data model of the same data model file.
  2. Another physical data model of the same data model file, PROVIDED it shares the exact same DBMS platform and version.
  3. A logical data model of another ER/Studio data model.
  4. A physical data model of another ER/Studio data model, PROVIDED it shares the exact same DBMS platform and version.
  5. A database (including NoSQL databases like MongoDB) or a SQL file.
- **Target Validation - Submodels**: When the Source is a Submodel, the AI MUST strictly permit comparisons ONLY to another submodel within the *same* data model.
- **Invocation Methods**: The AI MUST utilize or instruct the user to utilize one of the following exact command paths to invoke the utility:
  - Menu: `Model > Compare and Merge Utility...`
  - Application Toolbar: Click the corresponding icon.
  - Explorer: Right-click on source model (or submodel) > `Compare and Merge Utility...`
  - Shortcut Key: `<ALT + M>, then <M>`
  - Shortcut Menu: Right-click on white space > `Compare and Merge Utility...`
- **Resolution Handling**: When differences are found, the AI MUST require the user to explicitly define a resolution (Ignore, Delete from current, Merge into target) rather than assuming an automatic overwrite.
- **Mapping Preservation**: If objects are conceptually identical but named differently (e.g., `Customer` in Model A and `Client` in Model B), the AI MUST instruct the user to define a Universal Mapping (cross-file) or User-Defined Mapping (same-file) via the "Save Matches" feature to optimize future comparisons.

@Workflow
1. **Initiation and Validation**: Identify the Source Model type (Logical, Physical, or Submodel). Validate the intended Target Model against the strict compatibility rules defined in `@Guidelines`.
2. **Invocation**: Invoke the Compare and Merge Utility using the standard command paths (`<ALT + M>, then <M>`).
3. **Wizard Page 1 - Target Selection**: Select the specific comparison target (e.g., another ER/Studio model, a database). Optionally, load a predefined `Quick Launch` settings file.
4. **Wizard Page 2 - Subset Selection**: Refine the scope of the target file. Select the specific logical model, physical model, or submodel within the target to compare against.
5. **Wizard Page 3 - Metadata Selection**: Select the specific types of metadata to compare (defaults to all). Adjust General Options if necessary (e.g., check "ignore case" when comparing names, or "exclude definitions" when dealing with new physical structures).
6. **Wizard Page 4 - Object Selection**: Select the specific object classes to include in the comparison (Entities, Views, Users, Roles, Shapes). Optionally, save the current configuration as a `Quick Launch` file for future use.
7. **Wizard Page 5 - Resolution and Reporting**: 
   - Apply filters using the `Filter Results` drop-down to isolate specific subsets of differences.
   - For each discrepancy, select a `Resolution Value`: Ignore, Delete from current model, or Merge into target model.
   - Define `Save Matches` (Universal or User-Defined Mappings) for equivalent objects with differing names.
   - Click `<Report>` to generate an RTF or HTML document detailing the discrepancies for stakeholder review.
8. **Finalization**: Click `<Finish>` to execute the selected merge resolutions. Prompt the user to save the newly synchronized models.

@Examples (Do's and Don'ts)

[DO]
**Scenario**: Identifying unmodeled database changes made by a DBA.
**Action**: The AI guides the user to open the Logical Data Model as the Source. The AI validates that a database is a valid target. The AI instructs the user to invoke `<ALT + M>, then <M>`, select the live database on Wizard Page 1, proceed to Wizard Page 5, click `<Report>` to generate an HTML discrepancy report, and review the changes before selecting "Merge into target model" (updating the model to reflect the database) or "Delete from current model" (if the model should dictate the database state).

[DON'T]
**Scenario**: Comparing two physical models with different platforms.
**Action**: The AI attempts to compare a Physical Data Model built for Oracle 11g with a Physical Data Model built for Teradata.
**Correction**: The AI MUST block this action, citing the guideline: "Physical to Physical comparisons require the models to share the same DBMS platform and version."

[DO]
**Scenario**: Comparing subsets of a large enterprise model.
**Action**: The AI instructs the user to right-click a specific submodel in the Data Model Explorer, select `Compare and Merge Utility...`, and choose another submodel strictly within the *same* `.dm1` file to execute a focused Submodel-to-Submodel comparison.

[DON'T]
**Scenario**: Resolving repetitive false-positive naming differences.
**Action**: The AI manually clicks "Ignore" every time `Client` is compared to `Customer` in a cross-file comparison.
**Correction**: The AI MUST instruct the user to click `<...>` next to `Save Matches` on Wizard Page 5 and define a Universal Mapping between `Client` and `Customer` so ER/Studio automatically registers them as a match in all future comparisons.