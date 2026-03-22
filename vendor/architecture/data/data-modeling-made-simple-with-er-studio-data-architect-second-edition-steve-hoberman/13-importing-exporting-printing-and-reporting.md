@Domain
Data model importing, exporting, printing, and reporting operations within ER/Studio. These rules MUST trigger whenever the user requests to bring external models into ER/Studio, export data models to external formats (such as XML, ERwin, or images), print data model diagrams, or generate HTML/RTF documentation and reports.

@Vocabulary
- **External Metadata**: Metadata formats from other data modeling tools (e.g., CA ERwin Data Modeler, SAP Sybase PowerDesigner) that can be imported/exported.
- **ERX File**: A legacy file format used by CA ERwin Data Modeler version 3.x and tools like Silwood Technology's Safyr.
- **XSD (XML Schema Definition)**: An XML export format that formally describes elements in an XML document. Used for e-commerce, strict data control, and strong data typing.
- **DTD (Document Type Definition)**: An XML export format that defines element types and structures, used primarily in traditional text document publishing applications.
- **XML Schema Generation**: A wizard-based XML export option that customizes the schema structure and transforms relational entities and attributes into complex types.
- **Quick Launch**: A feature in ER/Studio wizards that allows saving and loading previously configured settings to streamline repetitive operations.
- **RTF (Rich Text Format)**: A report export format suited for viewing and editing in word processors like Microsoft Word.
- **HTML Enhanced Version**: An HTML report generation setting that produces a smaller file size for quicker browser opening and navigation.
- **Page Boundaries**: A display setting that shows diagram lines indicating how the model will be partitioned for printing.
- **Crop Marks**: A multipage printing setting that prints marks on pages to easily align and tape them together for large models.

@Objectives
- Execute seamless data model imports from external modeling tools by utilizing the correct file conversion prerequisites and wizards.
- Generate precise exports tailored to the target system's requirements (e.g., choosing the correct XML standard: XSD vs. DTD).
- Produce optimal image exports for reviewers who do not have ER/Studio installed.
- Configure data model print settings optimally based on model size (fit-to-page vs. multipage with crop marks).
- Generate professional, customized reports (HTML or RTF) based on the target audience's viewing and editing requirements.

@Guidelines
- **Importing ERwin Models**: The AI MUST advise the user to convert CA ERwin Data Modeler files (specifically version 7.x or later) to an XML Repository format *before* initiating the "Import External Metadata" process.
- **Importing ERX Files**: The AI MUST restrict the use of the "Import from ERX File" feature exclusively to legacy CA ERwin version 3.x files or specific tools like Safyr. Newer ERwin models MUST use the External Metadata wizard.
- **Reviewing Import Logs**: The AI MUST instruct the user to review the import status/error codes: Green/Blue circles denote status/information; Orange/Red triangles or Red circles denote warnings/errors that MUST be addressed.
- **Selecting XML Export Types**: 
  - Choose **XSD** if the user requires strict character data content validation, database-style applications, or configuration file validation.
  - Choose **DTD** if the user requires traditional text document publishing validation.
  - Choose **XML Schema Generation Wizard** if the user needs to manually map relational entities/attributes to complex XML types and elements.
- **Exporting Images**: When a user needs to share a model visually with a non-ER/Studio user, the AI MUST use `File > Export Image` (`ALT + F`, then `E`), select a format (EMF, JPEG, GIF, BMP, PNG), and specify the image quality (higher quality results in larger file sizes).
- **Printing Setup**: Before printing, the AI MUST ensure `Page Boundaries` are turned on via `Tools > Options > Display` to visually optimize object placement.
- **Scaling Prints**: For small data models, the AI MUST select `Fit Page`. For large data models, the AI MUST select `Multipage Printing` and enable `Page numbers` and `Crop marks`.
- **Selecting Report Formats**: 
  - Generate **HTML** reports for Intranet/Internet sharing. The AI MUST select "Use enhanced version" to keep file sizes small and fast.
  - Generate **RTF** reports if the user needs to edit the output in Microsoft Word or requires native Word features like a table of contents or page breaks.

@Workflow
1. **Importing External Metadata**:
   - Verify the source format. If ERwin, ensure it is saved as XML.
   - Navigate to `File > Import File` or `File > New... > Import Model From`.
   - Select the source format and file.
   - Configure duplicate name resolution (Rename with '_1', Update existing, or Skip).
   - Review and save/print the status log before completing.
2. **Exporting to XML**:
   - Navigate to `File > Export File` (`ALT + F`, then `F`).
   - Select the appropriate XML format (XSD, DTD, or XML Schema Generation).
   - If using the Schema Generation Wizard, apply namespaces, select target objects, and save Quick Launch settings for future reuse.
3. **Printing a Data Model**:
   - Turn on Page Boundaries (`Tools > Options > Display > Page Boundaries`).
   - Reposition entities to avoid page breaks cutting through them.
   - Navigate to `File > Print...` (`CTRL + P`).
   - Configure Page Scale (Fit Page or manual scaling), Border & Background (Color/Grayscale, grids), Name and Date Label (auditing info), and Multipage settings (Crop marks).
   - Save settings and print.
4. **Generating a Report**:
   - Navigate to `Tools > Generate Reports...` (`ALT + T`, then `R`).
   - Select HTML (check "Use enhanced version") or RTF.
   - Select the target directory.
   - Choose the models and specific objects to include.
   - Apply formatting (add custom logos, author, copyright info).
   - Save Quick Launch settings and generate.

@Examples (Do's and Don'ts)

- **[DO]** Prepare an ERwin file for import by saving it as an XML Repository format in ERwin first, then using the `Import External Metadata` option.
- **[DON'T]** Attempt to use the `Import from ERX File` option for modern ERwin (version 7.x+) data models.

- **[DO]** Select `XSD` when exporting XML for a service-oriented architecture (SOA) application that requires strict data typing and validation.
- **[DON'T]** Use `DTD` for modern database-style applications requiring strong data typing; DTD is for traditional text document publishing.

- **[DO]** Enable `Page Boundaries` before printing and use `Crop marks` and `Page numbers` when printing a large enterprise data model across multiple sheets of paper.
- **[DON'T]** Use `Fit Page` for a massive, 200-entity logical data model, as the printed text will be illegible.

- **[DO]** Check the "Use enhanced version" box when generating an HTML report to ensure the resulting web files are optimized for fast browser rendering.
- **[DON'T]** Generate an HTML report if the user explicitly states they need to add custom paragraphs or edit the text extensively after generation; use RTF instead.