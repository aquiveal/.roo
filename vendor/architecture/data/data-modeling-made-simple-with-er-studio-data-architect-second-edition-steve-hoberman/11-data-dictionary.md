@Domain
These rules MUST trigger when the AI is tasked with interacting with, configuring, or answering questions about ER/Studio Data Architect's Data Dictionary, metadata reusability, enterprise consistency configurations, metadata imports, or the specific management of Domains, User-Defined Datatypes (UDTs), Reference Values, and Attachments.

@Vocabulary
- **Data Dictionary**: An ER/Studio feature that allows the sharing and reuse of objects (domains, defaults, rules, reference values, and attachments) across models to save time and ensure enterprise consistency.
- **Repository**: A central server-side model management system. If not used, Data Dictionary objects are managed locally within a `.dm1` file and can be imported from other `.dm1` files.
- **Domain**: A set of validation criteria (format, nullability, default values, rules) applied to multiple attributes/columns to standardize characteristics. Serves as a reusable attribute "template."
- **Domain Folder**: A mechanism to organize domains into unique groups (e.g., measures, names, IDs). Deleting a folder deletes all domains and subfolders within it.
- **User-Defined Datatype (UDT)**: A reusable combination of a base datatype, format, and length (width, precision, scale) bound with rules and defaults.
- **Reference Value**: An attribute defining allowed data, specified either as a continuous range of values or an itemized list of specific codes/values.
- **Attachment Type**: An organizational grouping for attachments that defines the scope and object classes to which an attachment can be bound (e.g., organized by object type, subject area, or function).
- **Attachment**: An external piece of information (e.g., Microsoft Word document, PDF, date, list) physically associated with ER/Studio diagram objects via an Attachment Type.
- **Override Controls**: Settings on a Domain that dictate what properties (datatypes, defaults, names, attachments) can or cannot be overridden by the specific attributes bound to that Domain.

@Objectives
- Maximize metadata reuse and enterprise consistency by enforcing the use of Data Dictionary objects instead of manual, object-by-object configurations.
- Ensure accurate resolution of naming conflicts when merging external Data Dictionaries.
- Strictly adhere to ER/Studio's two-tiered attachment system (Attachment Types > Attachments).
- Accurately configure Domain overrides, synchronizations, and bindings.

@Guidelines
- **Data Dictionary Imports**:
  - When importing a Data Dictionary, the AI MUST explicitly declare the resolution strategy for duplicate object names: `Rename imported objects with '_1'`, `Update existing objects with imported data`, or `Skip import of duplicate object`.
- **Domains Management**:
  - The AI MUST configure Domains by specifying a Domain Name, Attribute Name, and Column Name.
  - The AI MUST define whether the Domain requires the `Receive Parent Modifications` flag (to inherit changes from a parent domain).
  - The AI MUST specify if `Synchronize Domain and Attribute/Column Names` should be active (forcing all three names to remain identical).
  - The AI MUST configure `Override Controls` when defining a Domain to dictate whether attributes can override datatypes/defaults, and whether Name Synchronization or Attachment Synchronization is enforced between the Domain and bound attributes.
- **User-Defined Datatypes (UDTs)**:
  - The AI MUST construct UDTs for commonly referenced database attributes (e.g., Phone Number, Postal Code) by specifying the base datatype, width, precision, scale, and nullability.
  - The AI MUST attach default values and rules directly to the UDT to enforce domain integrity automatically.
- **Reference Values**:
  - The AI MUST classify Reference Values as either `By Range` (requiring a minimum and maximum value) or `By List` (requiring a defined list of values and descriptions).
- **Attachments**:
  - The AI MUST NEVER attempt to create an Attachment without first establishing or referencing an `Attachment Type`.
  - The AI MUST bind Attachments to specific object classes (e.g., entities, relationships, attributes) through the `Binding Information` tab.

@Workflow
**Algorithm for Data Dictionary Imports**
1. Identify the source `.dm1` file containing the target Data Dictionary (e.g., the standard `Northwind` data model).
2. Select the specific Data Dictionary from the source file.
3. Define the `Resolve Imported Objects with Duplicate Names` setting based on the user's overwrite preferences.
4. Execute the import and verify the new objects under the Data Dictionary tab in the Model Explorer.

**Algorithm for Creating Reusable Domains**
1. Right-click Domains (or a Domain folder) and initiate a New Domain.
2. Set Domain Name, Attribute Name, and Column Name. Determine if `Synchronize Domain and Attribute/Column Names` is required.
3. Define Datatype, Length, and Nullability (`Allow Nulls` = Yes/No).
4. Bind Declarative Defaults, Rules/Constraints, and Reference Values to the Domain.
5. Define `Override Controls` to lock or allow specific deviations at the attribute level.

**Algorithm for Creating User-Defined Datatypes (UDTs)**
1. Define the Datatype Name.
2. Select the base format, width, precision, and scale.
3. Apply nullability constraints (e.g., `Apply nullability to all bound columns`).
4. Bind any relevant defaults or rules.

**Algorithm for Creating Attachments**
1. Create a `New Attachment Type` in the Attachments folder. Define its Name and `Attachment Type Usage` (the allowed object classes).
2. Right-click the newly created Attachment Type to create a `New Attachment`.
3. Define the Name and Value type (e.g., Text List, External File Path).
4. Apply the attachment to diagram objects via the `Binding Information` controls.

@Examples (Do's and Don'ts)

**Importing Data Dictionaries**
- [DO]: Establish a conflict resolution rule before importing: "To merge the Northwind dictionary, I will use 'Skip import of duplicate object' to preserve your existing 'City' domain while importing the rest."
- [DON'T]: Blindly import external metadata without addressing how name duplications will be handled, which can overwrite critical local configurations.

**Attribute Standardization**
- [DO]: Create a Domain named `BusinessDate` with a 'Date' datatype, bound to a 'Monday' default, and apply this single Domain to `Order Entry Date` and `Employee Hire Date`.
- [DON'T]: Manually edit `Order Entry Date` and `Employee Hire Date` individually to set their datatypes and rules.

**Handling Attachments**
- [DO]: Create an Attachment Type named "Requirements Documents" scoped to Entities, then create an Attachment pointing to "C:\docs\specs.pdf" nested under that type.
- [DON'T]: Attempt to bind a PDF directly to a data model Entity without first defining the Attachment Type organizational grouping.

**Domain Naming**
- [DO]: Check `Synchronize Domain and Attribute/Column Names` if you want a change to the domain name to automatically rename the logical attribute and physical column templates identically.
- [DON'T]: Use `Name Synchronization` under `Override Controls` if you want the attribute name to be entirely detached and independent from the Domain name.