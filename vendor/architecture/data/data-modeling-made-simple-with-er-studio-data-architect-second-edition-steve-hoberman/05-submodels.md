# @Domain
These rules MUST trigger when the user requests to segment, organize, or display a large ER/Studio data model into smaller, manageable pieces, or when the user explicitly requests to create, edit, move, customize, or delete "Submodels" within an ER/Studio data model. 

# @Vocabulary
*   **Submodel**: A display of a specific part or subset of a data model used to make large, complex data models easier to understand and communicate to specific audiences.
*   **Main Model**: The default, root holding area created automatically when a data model is created. It contains every object created within the entire model.
*   **Nested Submodel**: A submodel created within another submodel, acting similarly to a subfolder in a file directory system.
*   **Submodel Aesthetics**: Properties specific only to the submodel display, such as background color, font, resizing an entity, and model layout. 
*   **Submodel Content**: Data modeling objects and their fundamental properties, such as entity names and attributes. Changing these in a submodel changes them globally across the entire data model.
*   **Related Objects Level**: A setting determining the depth of relationships brought into a submodel (e.g., Level 1 brings in direct parents/children; Level 2 brings in grandparents/grandchildren).
*   **Title Block**: An object inserted into a submodel that provides important identification information for printouts and display, including project name, file name, submodel name, version, modification date, and copyright.

# @Objectives
*   The AI MUST segment large, complex data models into highly readable, audience-specific submodels.
*   The AI MUST strictly safeguard global model integrity by distinguishing between local submodel aesthetic changes and global data model content changes.
*   The AI MUST properly configure inheritance, relationship inclusions, and related object depths when generating submodels.
*   The AI MUST ensure every submodel is properly documented with definitions, necessary attribute bindings, and a Title Block.

# @Guidelines
*   **Aesthetic vs. Content Mutability Rules:**
    *   When the user requests to change model aesthetics (e.g., changing submodel background color, resizing an entity, rearranging entities, changing entity background color without "Apply to all submodels" checked), the AI MUST apply these changes *only* to the active submodel.
    *   When the user requests to change model content (e.g., changing an entity's name, creating an entity), the AI MUST apply these changes globally, acknowledging that the change will reflect in the Main Model and all other submodels containing that object.
*   **Deletion Constraints:**
    *   When the user deletes an entity or relationship from a submodel, the AI MUST explicitly clarify whether to delete the object from the *entire data model* or just remove it from the *submodel display*. Removing it from the submodel display leaves it intact in the Main Model.
*   **Submodel Creation Configuration:**
    *   The AI MUST evaluate if related entities should be automatically included. The AI MUST keep `Automatically Include Relationships` checked by default.
    *   The AI MUST set the `Select Related Objects...` level based on context: Level 1 for direct relationships, Level 2 for including extended lineage (grandparents) to show boundary connections.
    *   The AI MUST determine placement behavior: check `Place New Objects Near Existing Objects` to cluster new entities near existing ones/center, or leave unchecked to retain their original source positions.
*   **Nested Submodel Inheritance:**
    *   When creating nested submodels, the AI MUST ask or determine if `Inherit Objects Added to Nested Submodels` should be checked. If checked, any entity added to the child submodel MUST automatically display in the parent submodel.
*   **Attribute Display Optimization:**
    *   If an entity within a submodel contains an extremely high number of attributes, the AI MUST use the `Attributes` tab to deselect non-essential attributes for readability. The AI MUST note that ER/Studio will display an ellipsis (...) to indicate hidden attributes.
*   **Submodel Documentation:**
    *   The AI MUST ensure the `Definition` tab is populated for the submodel.
    *   The AI MUST ensure a Title Block is inserted (`Insert > Title Block`) into every submodel to prevent printouts from getting mixed up.
    *   If external documentation (e.g., requirements, user stories) exists, the AI MUST bind them to the submodel using the `Attribute Bindings` tab via the Data Dictionary.

# @Workflow
When tasked with creating or managing an ER/Studio submodel, the AI MUST follow this algorithmic process:

1.  **Define Scope and Audience**:
    *   Determine the specific subset of entities/relationships required for the target audience.
    *   Determine if this submodel should be nested within an existing submodel.
2.  **Initialize Submodel**:
    *   Invoke the creation command (`Model > Create Submodel…` or `<ALT + M>, then <C>`).
    *   Highlight and assign the target entities in the left pane of the Create Submodel screen.
3.  **Configure Submodel Settings**:
    *   Set `Inherit Objects Added to Nested Submodels` based on parent-child relationship needs.
    *   Set `Show all available items` (keep checked to see all possible objects).
    *   Configure `Select Related Objects...` (Level 1 for standard, Level 2+ for expanded boundaries).
    *   Ensure `Automatically Include Relationships` is checked.
4.  **Optimize Readability**:
    *   Filter visible attributes via the `Attributes` tab if entities are too large.
    *   Adjust aesthetics (background colors, entity arrangements) noting that these changes are local to the submodel.
5.  **Document the Submodel**:
    *   Enter a definition in the `Definition` tab.
    *   Insert a Title Block into the submodel workspace.
    *   Bind any relevant external files via the `Attribute Bindings` tab.

# @Examples (Do's and Don'ts)

*   **Aesthetic vs Content Changes**
    *   [DO]: When the user asks to "Make the Customer entity red in the Sales submodel and rename it to Client", the AI MUST state: "I will change the entity color to red locally in the Sales submodel. However, renaming it to 'Client' is a content change and will rename it everywhere, including the Main Model. Proceed?"
    *   [DON'T]: Treat entity renaming, creating, or full deletion as local submodel actions without warning the user of global impacts.

*   **Deleting Objects**
    *   [DO]: When asked to remove an entity from a submodel to clean up the view, use the "remove from submodel" function to simply hide it from the current view while retaining it in the Main Model.
    *   [DON'T]: Use the global `Delete Entity` command when the user merely wants to hide the entity from a specific submodel display.

*   **Handling Large Entities in Submodels**
    *   [DO]: Deselect irrelevant attributes from the `Attributes` tab when displaying a massive entity in a high-level conceptual submodel, allowing the ellipsis (...) to indicate hidden data.
    *   [DON'T]: Force the display of 100+ attributes in a submodel intended for high-level business review.

*   **Documentation**
    *   [DO]: Create a Title Block (`Insert > Title Block`) immediately after creating a new submodel so that all subsequent printouts or image exports contain project metadata.
    *   [DON'T]: Create a submodel and leave it without a Title Block or Definition.