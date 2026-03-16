# @Domain
These rules MUST be triggered whenever the AI is tasked with designing, architecting, or implementing Web application user interfaces, HTTP request handling, server-side rendering, routing logic, navigation flows, or resolving architectural separations between presentation layers and domain (business) logic layers.

# @Vocabulary
- **Model View Controller (MVC)**: The foundational architectural pattern splitting UI interaction into three distinct roles: Model, View, and Input Controller.
- **Model**: A nonvisual object (or group of objects) representing information about the domain, containing all data and behavior independent of the UI.
- **View**: An object or file responsible exclusively for the display of information provided by the Model in the UI.
- **Input Controller**: An object that receives user requests, pulls information from the request, forwards business logic to the Model, and determines which View to use for the response.
- **Application Controller**: An optional, centralized intermediary layer handling application flow, screen navigation, and wizard-like logic dictating which screens appear in which order.
- **Page Controller**: An Input Controller pattern where one module (script or server page) handles the request for a specific logical page or action on a Web site.
- **Front Controller**: An Input Controller pattern that consolidates all request handling through a single handler object, which then dispatches to specific Command objects.
- **Template View**: A View pattern that renders information into HTML by embedding markers (tags) into an otherwise static HTML page.
- **Helper Object**: A standard programming object used in conjunction with a Template View to house all programming logic, keeping the view file clean of scriptlets.
- **Scriptlet**: Arbitrary programming logic embedded directly into a server page (e.g., `<% code %>`). Highly discouraged.
- **Transform View**: A View pattern that processes domain data element by element and transforms it into HTML (e.g., using XSLT).
- **Two Step View**: A View pattern that turns domain data into HTML in two stages: Stage 1 forms a presentation-oriented logical screen structure; Stage 2 renders that logical screen into actual HTML.

# @Objectives
- Achieve absolute separation between the presentation layer and the domain logic layer.
- Ensure the Model is entirely agnostic of the Presentation; the Model MUST NOT depend on or call Presentation code.
- Prevent the leaking of application flow and routing logic into View files.
- Eradicate complex scriptlets and conditional programming logic from HTML/Server pages by extracting them into Helper Objects or Transform Views.
- Standardize and centralize UI flow handling based on the complexity of the application (Page Controller for simple navigation, Front Controller/Application Controller for complex navigation).

# @Guidelines

## General MVC Architecture
- The AI MUST separate UI interactions into Model, View, and Input Controller.
- The AI MUST NEVER create a dependency from the Model to the View or the Controller. Domain objects must be completely unaware of the Web presentation.
- If the AI must support multiple presentations (e.g., Web, rich client, command-line), it MUST reuse the exact same Model code without modification.

## Input Controller Selection & Implementation
- The AI MUST evaluate the navigational complexity of the application before generating routing code:
  - If the application has simple logic and a straightforward 1-to-1 mapping of URLs to actions, the AI MUST use **Page Controller**.
  - If the application requires centralized security, internationalization, or dynamic routing across many requests, the AI MUST use **Front Controller**.
- When implementing a **Page Controller**:
  - The AI MAY use a server page or a script as the controller.
  - If using a server page as a Page Controller, the AI MUST immediately delegate logic to a Helper Object to avoid scriptlet code.
- When implementing a **Front Controller**:
  - The AI MUST separate the pattern into two parts: a Web Handler (to parse the URL/request) and a Command hierarchy (to execute the specific action).
  - The AI MUST instantiate a new Command object for each request to avoid multi-threading issues, ensuring Commands do not share state except via the Model.
  - The AI SHOULD use Intercepting Filters (decorators) for cross-cutting concerns like authentication or encoding.

## Application Controller & Screen Flow
- The AI MUST use an **Application Controller** ONLY if the machine (application) dictates the flow of screens (e.g., wizards, conditional step-by-step flows).
- If the user is in control of navigation (can visit any screen at any time), the AI MUST NOT use an Application Controller.
- An Application Controller MUST maintain no dependencies on the UI machinery (e.g., direct HTTP session data) to allow independent testing and reuse.

## View Selection & Implementation
- The AI MUST evaluate the team environment and application theme requirements before generating View code:
  - If WYSIWYG editing or non-programmer design is prioritized, the AI MUST use **Template View**.
  - If strict separation of HTML rendering from domain XML is prioritized, the AI MUST use **Transform View**.
  - If the application requires multiple uniform themes/appearances or global layout changes, the AI MUST use **Two Step View**.
- When implementing a **Template View**:
  - The AI MUST NEVER embed complex programming logic, loops, or raw conditional blocks (scriptlets) directly into the page.
  - The AI MUST create a separate **Helper Object** to contain all programmatic logic. The Template View MUST only call properties/methods of the Helper Object or use focused custom tags.
  - The AI MUST avoid general-purpose `<IF>` conditional tags. Instead, move the conditional logic into the Helper Object or use focused, domain-specific tags.
- When implementing a **Transform View**:
  - The AI MUST organize the view around separate transforms for each kind of input element (e.g., matching XML nodes and outputting HTML fragments).
- When implementing a **Two Step View**:
  - The AI MUST separate the transformation into exactly two stages.
  - Stage 1 MUST generate a logical screen structure (e.g., fields, tables, headers) completely devoid of HTML styling.
  - Stage 2 MUST translate the logical screen structure into final HTML.

# @Workflow
When tasked with creating or refactoring a Web Presentation feature, the AI MUST adhere to the following algorithmic process:

1. **Layer Separation Check**: 
   - Identify the domain logic (calculations, rules) vs. presentation logic (formatting, request parsing). 
   - Ensure domain logic is placed in a Domain Model or Transaction Script completely isolated from HTTP requests.
2. **Determine Controller Architecture**:
   - Assess routing complexity. If simple, implement **Page Controller**. If complex/needs centralized preprocessing, implement **Front Controller**.
   - Assess navigation control. If the application dictates screen sequence based on state, implement an **Application Controller** to hold the flow logic map.
3. **Determine View Architecture**:
   - Select **Template View**, **Transform View**, or **Two Step View** based on layout consistency requirements and data format (e.g., XML vs. Objects).
4. **Implement the Input Controller**:
   - Extract form data from the HTTP request.
   - Instantiate or locate the appropriate Model object(s).
   - Invoke Model behavior.
   - Pass the resulting data/Model to the View (or to a Helper Object attached to the View).
5. **Implement the View**:
   - If using Template View, build a Helper Object. Route all data extraction and iteration through the Helper Object. Write the HTML utilizing only simple markers or custom tags referencing the Helper.
   - If using Transform View, map the domain data to an intermediate format (like XML) and write the transformation rules to output HTML.

# @Examples (Do's and Don'ts)

## Controller Logic in Views
- **[DON'T]** Mix controller logic, domain logic, and HTML in a single server page using scriptlets:
  ```jsp
  <% 
    String id = request.getParameter("id");
    Album album = Album.find(id);
    if (album == null) { 
      response.sendRedirect("error.jsp"); 
    } else { 
  %>
  <h1><%= album.getTitle() %></h1>
  <% } %>
  ```
- **[DO]** Use a Controller to handle the request, invoke the model, and forward to a clean View:
  ```java
  // Controller Class
  public void doGet(HttpServletRequest request, HttpServletResponse response) {
      Album album = Album.find(request.getParameter("id"));
      if (album == null) {
          forward("/error.jsp", request, response);
      } else {
          request.setAttribute("helper", new AlbumHelper(album));
          forward("/album.jsp", request, response);
      }
  }
  ```

## Template View Iteration & Conditionals
- **[DON'T]** Use raw programming loops and complex conditionals inside the HTML template:
  ```jsp
  <ul>
  <% for (Iterator it = helper.getAlbums().iterator(); it.hasNext();) {
      Album album = (Album) it.next(); 
      if (album.isHighSelling()) { %>
        <li><b><%= album.getTitle() %></b></li>
      <% } else { %>
        <li><%= album.getTitle() %></li>
  <%  }
     } %>
  </ul>
  ```
- **[DO]** Use a Helper Object or focused custom tags to keep the Template View declarative:
  ```jsp
  <ul>
    <tag:forEach host="helper" collection="albums" id="each">
      <li>
        <tag:highlight condition="isHighSelling" style="bold">
          <jsp:getProperty name="each" property="title"/>
        </tag:highlight>
      </li>
    </tag:forEach>
  </ul>
  ```

## Front Controller Implementation
- **[DON'T]** Duplicate request parsing and security checks across dozens of individual Page Controllers.
- **[DO]** Centralize request handling in a Front Controller that dispatches to stateless Commands:
  ```java
  // Front Controller Web Handler
  public void doGet(HttpServletRequest request, HttpServletResponse response) {
      FrontCommand command = getCommand(request); // dynamically load command
      command.init(getServletContext(), request, response);
      command.process();
  }
  
  // Specific Command Object
  class ArtistCommand extends FrontCommand {
      public void process() {
          Artist artist = Artist.findNamed(request.getParameter("name"));
          request.setAttribute("helper", new ArtistHelper(artist));
          forward("/artist.jsp");
      }
  }
  ```

## Two Step View
- **[DON'T]** Hardcode specific HTML tables and styling directly into every individual page's XSLT or Template when building a multi-appearance site.
- **[DO]** Transform data into a logical structure (Stage 1), then transform the logical structure into HTML (Stage 2):
  ```xml
  <!-- Stage 1 Output (Logical Screen) -->
  <screen>
    <title>Zero Hour</title>
    <field label="Artist">Astor Piazzola</field>
    <table>
      <row><cell>Tanguedia III</cell><cell>4:39</cell></row>
    </table>
  </screen>
  ```
  ```xslt
  <!-- Stage 2 Transform (Global HTML styling) -->
  <xsl:template match="table">
    <table class="global-theme-table"><xsl:apply-templates/></table>
  </xsl:template>
  <xsl:template match="table/row/cell">
    <td class="global-theme-cell"><xsl:apply-templates/></td>
  </xsl:template>
  ```