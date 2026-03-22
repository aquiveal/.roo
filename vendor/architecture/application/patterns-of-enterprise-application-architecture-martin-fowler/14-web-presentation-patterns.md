@Domain
These rules MUST trigger when the AI is tasked with designing, refactoring, or implementing Web user interfaces, HTTP request handlers, view rendering logic, or application navigation/screen flow within an enterprise application.

@Vocabulary
- **Model View Controller (MVC)**: An architectural pattern splitting UI interaction into three distinct roles: Model (domain information/behavior), View (display), and Controller (input handling and model manipulation).
- **Page Controller**: An input controller object that handles a request for one specific logical page or action on a Web site.
- **Front Controller**: A single handler object that consolidates and channels all requests for a Web site, usually delegating to a command hierarchy.
- **Template View**: A view pattern that renders information into HTML by embedding markers or tags in a static HTML page.
- **Scriptlet**: Arbitrary programming logic embedded directly into a server page (e.g., ASP, JSP, PHP). Strongly discouraged.
- **Helper Object**: A regular object used alongside a Template View or Page Controller to hold programming logic, keeping the server page strictly display-oriented.
- **Transform View**: A view pattern (often XSLT) that processes domain data element by element, transforming it into HTML based on the input's structure rather than the output's structure.
- **Two Step View**: A view pattern that turns domain data into HTML in two stages: first assembling a presentation-oriented logical screen, then rendering that logical screen into HTML.
- **Logical Screen**: An intermediate data structure used in Two Step View that defines widgets and data without specifying HTML appearance.
- **Application Controller**: A centralized point for handling screen navigation, flow, and state-based view dispatching.
- **Web Handler**: The component of a Front Controller that receives the HTTP request, pulls routing info, and dispatches to a Command.
- **Command (in Front Controller)**: An object that carries out the specific action for a request routed by the Front Controller.
- **Intercepting Filter**: A decorator wrapping the Web Handler in a Front Controller to process common tasks like authentication, logging, or internationalization.

@Objectives
- Enforce an absolute separation of presentation concerns from domain model concerns.
- Ensure controllers are appropriately chosen based on the routing complexity of the application (Page Controller for simple routing, Front Controller for complex/centralized routing).
- Ensure view rendering avoids the mingling of programming logic and display formatting (strictly avoiding scriptlets).
- Isolate complex navigation and screen flow state logic into Application Controllers without leaking domain logic into them.
- Facilitate the ability to substitute different views (or multiple appearances) without modifying domain models or controller actions.

@Guidelines

*Model View Controller (MVC) Strict Separation*
- The AI MUST strictly separate the presentation from the model.
- The AI MUST enforce a unidirectional dependency: the presentation layer depends on the model, but the model MUST NEVER depend on the presentation layer.
- The AI MUST ensure that developers programming in the model are entirely unaware of what presentation is being used.
- If multiple presentations of the same model exist and must stay in sync, the AI MUST use the Observer pattern (events/listeners) to communicate changes from the model to the presentation.
- The AI MUST NOT separate the view and controller unless specifically required to support editable vs. non-editable behaviors using strategy patterns.

*Page Controller*
- The AI MUST map one Page Controller module to one logical page or action on the site.
- The AI MUST perform three basic responsibilities in a Page Controller: (1) Decode the URL/form data, (2) Create and invoke model objects, passing necessary data, (3) Determine the view and forward the model information to it.
- If using a server page (e.g., JSP, PHP) as a Page Controller, the AI MUST delegate all complex logic to a Helper Object to avoid scriptlets.
- The AI MAY use a common superclass for Page Controllers to handle duplicated tasks like forwarding to views or validating mandatory parameters.

*Front Controller*
- The AI MUST use a Front Controller when the site requires complex, centralized request handling (e.g., security, internationalization).
- The AI MUST split the Front Controller into two parts: a Web Handler (to parse the URL/request) and a Command hierarchy (to execute the action).
- The AI MUST NOT put view rendering logic in the Web Handler. The Command object MUST choose which view to use for the response.
- The AI MAY configure the Web Handler to map URLs to Commands either statically (using conditional logic) or dynamically (using reflection/string instantiation based on a properties file or URL parsing).
- The AI SHOULD use Intercepting Filters (decorators) around the Web Handler to dynamically apply common behaviors like authentication or character encoding at runtime.

*Template View*
- The AI MUST NOT embed raw programming logic (scriptlets) into Template Views.
- The AI MUST use a Helper Object to prepare all data and handle all logic required by the Template View.
- The AI MUST replace conditional programming constructs in the view with either: (A) A method on the Helper Object that returns an empty string when the condition is false, or (B) Highly focused, declarative custom tags (e.g., `<highlight condition="isHighSelling">`).
- The AI MUST ensure that any conditional tag relies on a single Boolean property of the Helper Object, rather than evaluating complex expressions in the view.
- For iterating over collections in a Template View, the AI MUST use custom iteration tags rather than programming language loops (`for`, `while`).

*Transform View*
- The AI MUST use a Transform View (typically XSLT or functional transformations) when converting domain-oriented XML data directly into HTML.
- The AI MUST organize the Transform View around separate transform rules for each kind of input element, not by the desired output structure.
- The AI MUST ensure that the domain logic returns XML (or a serializeable Data Transfer Object) to be fed into the Transform View engine.

*Two Step View*
- The AI MUST use a Two Step View for multi-appearance applications (multiple skins/devices) or to enforce strict global layout consistency.
- Stage 1: The AI MUST extract domain data and transform it into a "Logical Screen" structure (e.g., fields, headers, tables) containing absolutely no HTML.
- Stage 2: The AI MUST take the Logical Screen structure and render it into HTML.
- The AI MUST ensure that changing the HTML layout of the entire application only requires modifying the Stage 2 renderer.

*Application Controller*
- The AI MUST introduce an Application Controller ONLY when the application has complex navigation logic, wizard-like flows, or screen choices dependent on object states.
- The AI MUST design the Application Controller to hold structured collections of class references: one for domain commands and one for views.
- The AI MUST NOT put domain logic or presentation-specific UI machinery (like direct HTTP session manipulation) into the Application Controller. It must act strictly as an intermediate flow-director.
- The AI MUST represent control flow in the Application Controller using state machine logic or metadata/configuration files.

@Workflow
1. **Analyze the Request**: Determine if the task involves handling a Web request, defining screen flow, or generating an HTML response.
2. **Determine Controller Architecture**:
   - If the application is simple and URL-to-page mappings are straightforward, implement a **Page Controller**.
   - If the application requires centralized security, routing, or pre-processing, implement a **Front Controller** with a Web Handler and Command objects.
3. **Extract and Process Input**: Have the chosen Controller extract data from the HTTP request and immediately pass it to the Domain Model. Ensure the Domain Model receives no HTTP-specific objects.
4. **Evaluate Screen Flow (Optional)**: If the next screen depends on complex domain state or wizard steps, invoke an **Application Controller** to determine the appropriate Domain Command and View.
5. **Determine View Architecture**:
   - If non-programmers will edit the layout, implement a **Template View** backed by a Helper Object (no scriptlets).
   - If the input is primarily XML or hierarchical data, implement a **Transform View**.
   - If the site requires multiple themes, skins, or device outputs, implement a **Two Step View** (Domain -> Logical Screen -> HTML).
6. **Render**: The Controller (or Command) forwards the prepared model data (or Helper Object) to the chosen View for rendering.

@Examples (Do's and Don'ts)

*MVC Separation*
- [DO] Pass raw data to a domain object: `artist.findNamed(request.getParameter("name"));`
- [DON'T] Pass the HTTP Request directly to a domain object: `artist.findNamed(request);` // Violates Model independence.

*Template View Logic*
- [DO] Use a Helper Object and simple tags for conditions:
  ```jsp
  <helper:highlight condition="isHighSelling" style="bold">
      <jsp:getProperty name="helper" property="price"/>
  </helper:highlight>
  ```
- [DON'T] Use scriptlets for UI logic:
  ```jsp
  <% if (helper.getSales() > 1000) { %>
      <B><%= helper.getPrice() %></B>
  <% } else { %>
      <%= helper.getPrice() %>
  <% } %>
  ```

*Page Controller*
- [DO] Extract parameters, call the domain, and forward to a view:
  ```java
  public void doGet(HttpServletRequest request, HttpServletResponse response) {
      Artist artist = Artist.findNamed(request.getParameter("name"));
      request.setAttribute("helper", new ArtistHelper(artist));
      forward("/artist.jsp", request, response);
  }
  ```
- [DON'T] Mix domain logic and HTML generation inside the Page Controller servlet.

*Front Controller*
- [DO] Create a single Web Handler that instantiates Commands based on parameters:
  ```java
  public void doGet(HttpServletRequest request, HttpServletResponse response) {
      FrontCommand command = getCommand(request); // e.g., parses "?command=Artist"
      command.init(context, request, response);
      command.process(); // Command handles domain invocation and view forwarding
  }
  ```
- [DON'T] Put routing conditional logic (`if command == "A" do X, else if command == "B" do Y`) directly into the Web Handler if it can be dynamically dispatched to Command objects.

*Application Controller*
- [DO] Map events and domain states to specific views and commands:
  ```java
  appController.addResponse("return", AssetStatus.ON_LEASE, GatherReturnDetailsCommand.class, "returnView");
  appController.addResponse("return", AssetStatus.IN_INVENTORY, NullAssetCommand.class, "illegalActionView");
  ```
- [DON'T] Hardcode state-based navigation logic inside the UI buttons or individual Page Controllers.