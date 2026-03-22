@Domain
Any system architecture, application design, code refactoring, or structural scaffolding task that involves organizing modules, classes, directories, or files into layers, specifically in the context of enterprise application development.

@Vocabulary
- **Layering**: A structural technique where principal subsystems are arranged in a hierarchy. Each layer uses the services of the lower layer and hides those lower layers from the layers above it.
- **Layer**: A logical separation of software components (e.g., packages, namespaces, or modules within the same codebase).
- **Tier**: A physical separation of deployment nodes (e.g., a desktop client machine vs. a database server).
- **Presentation Layer**: The logical component responsible for handling the interaction between the user (or external client/service) and the software, displaying information, and interpreting commands.
- **Domain Layer (Business Logic)**: The logical component responsible for domain-specific work, including calculations based on inputs and stored data, validations, and deciding which data source logic to dispatch.
- **Data Source Layer**: The logical component responsible for communicating with external infrastructure, transaction monitors, messaging systems, and databases.
- **Cascading Change**: A systemic downside of layering where adding a single feature (e.g., a new UI field) requires updating the UI, the Domain, and the Data Source layers simultaneously.
- **Complexity Boosters**: Architectural choices—such as physical distribution, explicit multithreading, and paradigm chasms—that carry a massive cost in development and maintenance and should be avoided unless strictly necessary.
- **Alternate UI Test**: A mental heuristic used to identify leaked domain logic by imagining the addition of a radically different presentation layer (e.g., adding a CLI to a Web App).

@Objectives
- Decompose enterprise applications into three principal logical layers: Presentation, Domain, and Data Source.
- Enforce a strict, unidirectional dependency graph where Domain and Data Source layers remain completely ignorant of the Presentation layer.
- Maximize logical separation (Layers) while minimizing physical distribution boundaries (Tiers) to avoid network latency and remote-call complexity.
- Extract all business rules, validations, and arbitrary conditions out of UI components and firmly root them in the Domain layer.

@Guidelines
- **Strict Dependency Rule**: The AI MUST ensure that the Domain and Data Source layers NEVER depend on the Presentation layer. There MUST BE NO imports, method calls, or references from Domain/Data Source code to Presentation code.
- **The Alternate UI Test**: When writing or reviewing Presentation code, the AI MUST ask: "If I were to replace this Web UI with a Command Line Interface, would I have to duplicate this logic?" If the answer is yes, the AI MUST extract that logic into the Domain layer.
- **Boolean UI Triggers**: The AI MUST NOT evaluate raw business data rules inside presentation formatting logic. Instead, the Domain layer MUST expose a Boolean method (e.g., `isEligibleForHighlight()`), which the Presentation layer calls to determine formatting.
- **Data Source Encapsulation**: The AI MUST place all database queries, file writing, or external system communications inside the Data Source layer. The Domain layer MUST NOT contain raw SQL or direct infrastructure API calls.
- **Opaque vs. Transparent Layering**: The AI SHOULD generally make layers opaque (Presentation calls Domain, Domain calls Data Source). However, if the Presentation layer needs to display simple tabular data, the AI MAY allow the Presentation to access the Data Source directly to retrieve data, letting the Domain logic manipulate it afterward.
- **Process Colocation**: The AI MUST keep all layers intended for a single deployment node running within a single process. The AI MUST NOT separate layers into discrete inter-communicating processes (e.g., splitting Domain and Presentation into microservices over HTTP) unless explicitly mandated by the user.
- **Handling Split Domain Logic**: If domain logic MUST be executed on both a client (for UI responsiveness/disconnected operation) and a server, the AI MUST isolate that shared domain logic in a self-contained module completely independent of both the client and server application structures.
- **Avoid Complexity Boosters**: The AI MUST default to architectures that avoid distribution and explicit multithreading unless extreme performance or scalability requirements dictate otherwise.

@Workflow
1. **Context Analysis**: Analyze the user's request to identify the specific features, data models, and user interactions required.
2. **Layer Deconstruction**: Break the required features down into Presentation responsibilities, Domain responsibilities, and Data Source responsibilities.
3. **Domain First**: Implement the Domain layer first. Define the core business rules, algorithms, and validation states independent of any UI framework or Database ORM.
4. **Data Source Integration**: Implement the Data Source layer. Write the persistence mechanisms (Gateways, Repositories) that the Domain layer requires, ensuring the Domain remains decoupled from specific database technologies.
5. **Presentation Implementation**: Implement the Presentation layer. Create controllers and views that interpret user input, call the Domain layer, and format the resulting Domain data.
6. **Dependency Audit**: Scan all generated code to verify the Dependency Rule. Ensure no UI imports exist in the Domain or Data Source files.
7. **Refactor Leaks**: Apply the "Alternate UI Test" to the Presentation layer. Extract any calculation or business comparison found in the views/controllers back into the Domain layer.

@Examples (Do's and Don'ts)

**Principle: Isolating Domain Logic from Presentation (The Highlight Rule)**
- [DON'T] Evaluate business data rules in the UI layer.
  ```javascript
  // Presentation Layer Anti-pattern
  function renderProduct(product, previousMonthSales) {
      // Leaked Domain Logic!
      const isHighlighted = product.sales > (previousMonthSales * 1.10);
      return `<div class="${isHighlighted ? 'text-red' : 'text-black'}">${product.name}</div>`;
  }
  ```
- [DO] Evaluate business rules in the Domain layer and format in the UI layer.
  ```javascript
  // Domain Layer
  class Product {
      hasImprovingSales(previousMonthSales) {
          return this.sales > (previousMonthSales * 1.10);
      }
  }

  // Presentation Layer
  function renderProduct(product, previousMonthSales) {
      const isHighlighted = product.hasImprovingSales(previousMonthSales);
      return `<div class="${isHighlighted ? 'text-red' : 'text-black'}">${product.name}</div>`;
  }
  ```

**Principle: Strict Dependency Rule**
- [DON'T] Pass HTTP request objects or UI-specific context into the Domain layer.
  ```java
  // Domain Layer Anti-pattern
  public class OrderProcessor {
      public void process(HttpServletRequest request) {
          // Domain depends on Presentation (HTTP)!
          String amount = request.getParameter("amount");
          // ...
      }
  }
  ```
- [DO] Parse UI context in the Presentation layer and pass plain data to the Domain layer.
  ```java
  // Presentation Layer
  public void handleRequest(HttpServletRequest request) {
      BigDecimal amount = new BigDecimal(request.getParameter("amount"));
      orderProcessor.process(amount);
  }

  // Domain Layer
  public class OrderProcessor {
      public void process(BigDecimal amount) {
          // Domain is purely business logic, unaware of HTTP
      }
  }
  ```

**Principle: Process Colocation (Avoiding Complexity Boosters)**
- [DON'T] Separate logical layers into distributed network services unnecessarily.
  ```python
  # Anti-pattern: Network call between Presentation and Domain for a standard Web App
  class WebController:
      def execute(self):
          # Incurs high cost of serialization, remote calls, and latency
          response = requests.post("http://domain-service/api/calculate")
          return render(response.json())
  ```
- [DO] Run logical layers in the same process to maximize performance, using standard method calls.
  ```python
  # Correct Layering within the same process
  from myapp.domain import BusinessCalculator

  class WebController:
      def execute(self):
          # Fast, in-process method call
          calculator = BusinessCalculator()
          result = calculator.calculate()
          return render(result)
  ```