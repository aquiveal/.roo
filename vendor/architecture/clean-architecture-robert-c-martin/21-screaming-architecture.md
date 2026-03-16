@Domain
Triggers when the AI is tasked with generating project scaffolds, defining system directory structures, designing core business logic (Entities and Use Cases), integrating third-party frameworks, handling web/UI delivery mechanisms, or writing unit tests for business rules. 

@Vocabulary
- **Screaming Architecture**: An architectural structure whose top-level directories, packages, and files clearly and loudly declare the business intent and domain of the application (e.g., "Health Care System") rather than the frameworks being used (e.g., "Rails" or "Spring").
- **Use Case**: A specific business operation that orchestrates the behavior of Entity objects. It represents the core intent of the application and must remain completely isolated from databases, web servers, and frameworks.
- **Entity Object**: A "plain old object" containing business rules and state. It has absolutely no dependencies on frameworks, databases, or delivery mechanisms.
- **Delivery Mechanism**: An IO device or interface, such as the Web, a console, or a thick client. It is a peripheral detail that must not influence or leak into the system's core architecture.
- **Framework**: A third-party tool, library, or environment used to support the application. Frameworks are treated with skepticism, kept at arm's length, and strictly prevented from invading the core architecture.
- **In Situ Testing**: The ability to execute unit tests on all use cases and entities in complete isolation, without requiring a web server, database connection, or framework context to be running.
- **Peripheral Concerns**: Details such as databases, web servers, routing, and UI rendering that must be deferred, delayed, and decoupled from the business core.

@Objectives
- Ensure the application's highest-level structural organization explicitly reveals its business domain and use cases to any reader.
- Decouple all core business logic (Entities and Use Cases) entirely from frameworks, databases, and delivery mechanisms.
- Treat the Web strictly as an interchangeable IO device, preventing HTTP or web-specific concepts from dictating system design.
- Treat all frameworks as useful but dangerous tools; establish hard boundaries to prevent framework base classes and annotations from polluting business objects.
- Guarantee that the entirety of the business rules can be unit-tested seamlessly without loading external environments or framework dependencies.
- Enable the deferral of decisions regarding databases, web servers, and frameworks to the latest possible moment in the development lifecycle.

@Guidelines
- **Directory and Package Structuring**: The AI MUST name top-level project directories according to business use cases or domain aggregates (e.g., `PatientBilling/`, `AppointmentScheduling/`). The AI MUST NOT use framework-dictated top-level directories (e.g., `Controllers/`, `Views/`, `Models/`).
- **Framework Isolation**: The AI MUST NOT allow core business Entities or Use Case classes to inherit from framework base classes. Frameworks must wrap the core, not the other way around.
- **Web Ignorance**: The AI MUST NOT pass web-specific objects (e.g., `HttpServletRequest`, `JSON` payloads, `HTTP Response` objects) into Use Cases or Entities. The UI layer must translate these into plain data structures before passing them to the business core.
- **Delivery Independence**: The AI MUST architect the core system so that the delivery mechanism (Web, Console, API) can be swapped without modifying a single line of code in the Use Cases or Entities.
- **Database Independence**: The AI MUST abstract database access through interfaces defined by the business core. Entities MUST NOT contain database mapping annotations (e.g., `@Table`, `has_many`, `@Column`).
- **Skeptical Framework Integration**: The AI MUST act under the assumption that frameworks are a liability. When using a framework, the AI MUST generate boundary interfaces or adapters to protect the core application from being heavily coupled to the framework's API.
- **Testability First**: The AI MUST design Use Cases and Entities so they can be instantiated and tested in standard unit test frameworks using standard memory allocation, without any startup of web servers, database connections, or application contexts.

@Workflow
1. **Identify the Business Domain**: Analyze the requested system to determine the core business domain and primary use cases.
2. **Scaffold by Intent**: Generate a directory structure where the top-level folders represent the identified use cases and business concepts.
3. **Define Plain Entities**: Implement the core business objects (Entities) as plain, standalone classes without any framework imports, base classes, or data-persistence annotations.
4. **Implement Isolated Use Cases**: Write the Use Case objects that coordinate the Entities. Ensure these classes take simple data structures as inputs and return simple data structures as outputs.
5. **Establish Framework Boundaries**: Create adapter classes/interfaces at the periphery of the system to handle database operations and web routing. Connect these to the core using Dependency Inversion.
6. **Write In Situ Tests**: Generate unit tests that instantiate the Entities and Use Cases directly, mocking any external interfaces, proving the business logic works without external environments.
7. **Integrate the Delivery Mechanism**: Implement the Web/UI layer solely as an IO device that translates user actions into the plain data structures expected by the Use Cases.

@Examples (Do's and Don'ts)

**Principle: Screaming Architecture (Project Structure)**
- [DO]
  ```text
  src/
  ├── PatientRegistration/
  │   ├── RegisterPatientUseCase.ts
  │   └── PatientEntity.ts
  ├── AppointmentScheduling/
  │   ├── ScheduleAppointmentUseCase.ts
  │   └── AppointmentEntity.ts
  └── Infrastructure/
      ├── WebControllers/
      └── DatabaseAdapters/
  ```
- [DON'T]
  ```text
  src/
  ├── Controllers/
  │   ├── PatientController.ts
  │   └── AppointmentController.ts
  ├── Models/
  │   ├── Patient.ts
  │   └── Appointment.ts
  └── Views/
      └── PatientView.ts
  ```

**Principle: Entities as Plain Old Objects (Framework Isolation)**
- [DO]
  ```typescript
  export class Video {
      constructor(public id: string, public title: string, public price: number) {}

      calculateDiscount(percentage: number): number {
          return this.price - (this.price * (percentage / 100));
      }
  }
  ```
- [DON'T]
  ```typescript
  import { Entity, Column, BaseEntity } from 'typeorm';

  @Entity()
  export class Video extends BaseEntity {
      @Column()
      public id: string;

      @Column()
      public title: string;

      @Column()
      public price: number;
  }
  ```

**Principle: The Web is a Detail (Delivery Independence)**
- [DO]
  ```typescript
  // Web Controller (Outer Layer) translates HTTP to plain data
  handleRequest(req: HttpRequest, res: HttpResponse) {
      const requestData = new PurchaseVideoRequest(req.body.videoId, req.body.userId);
      const useCase = new PurchaseVideoUseCase();
      const result = useCase.execute(requestData);
      res.send(result);
  }

  // Use Case (Inner Layer) knows nothing of HTTP
  class PurchaseVideoUseCase {
      execute(request: PurchaseVideoRequest): PurchaseVideoResponse {
          // business logic
      }
  }
  ```
- [DON'T]
  ```typescript
  // Use Case knows about the Web / HTTP
  class PurchaseVideoUseCase {
      execute(req: HttpRequest, res: HttpResponse) {
          const videoId = req.body.videoId;
          // business logic
          res.send({ status: "success" });
      }
  }
  ```

**Principle: Testable Architectures (In Situ Testing)**
- [DO]
  ```typescript
  test('It should apply volume discount', () => {
      // Test executes purely in memory, instantly, without Spring/Rails/Express
      const video = new Video("123", "Clean Code", 100);
      const useCase = new PurchaseVideoUseCase(new MockDatabaseGateway());
      const response = useCase.execute(new PurchaseRequest("123", "user1"));
      expect(response.total).toBe(90);
  });
  ```
- [DON'T]
  ```typescript
  test('It should apply volume discount', async () => {
      // Test requires booting a database and web server to test a business rule
      await Database.connect();
      await App.start();
      const response = await httpClient.post('/buy', { videoId: "123", userId: "user1" });
      expect(response.body.total).toBe(90);
  });
  ```