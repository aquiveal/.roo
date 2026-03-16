# @Domain
This rule file is activated whenever the AI is tasked with high-level system design, defining directory structures, separating modules, refactoring legacy code for better decoupling, choosing or implementing technology stacks (databases, web frameworks, delivery mechanisms), or designing deployment and team-collaboration topologies.

# @Vocabulary
- **Architecture Shape**: The foundational structure of the system consisting of the division of the system into components, the arrangement of those components, and the ways in which those components communicate with each other.
- **Policy**: The business rules and procedures; the most essential elements of the system containing its true value.
- **Detail**: Peripheral mechanisms necessary to enable humans, other systems, and programmers to communicate with the policy (e.g., IO devices, databases, web systems, servers, frameworks, communication protocols).
- **Spelunking**: The costly and time-consuming process of digging through existing software to determine the best place and strategy to add a new feature or repair a defect.
- **Cost of Risk**: The likelihood of creating inadvertent defects when modifying poorly architected code.
- **Immediate Deployment**: The ability to deploy the entire software system with a single action, without requiring manual directory creation, property file tweaks, or complex sequencing.
- **Device Independence**: The decoupling of core system policy from specific hardware, IO devices, or physical storage constraints via abstraction.

# @Objectives
- Minimize the human resources and lifetime cost required to build and maintain the required system.
- Maximize programmer productivity through the entire system lifecycle (Development, Deployment, Operation, Maintenance).
- Leave as many technological options open as possible, for as long as possible.
- Maximize the number of decisions *not* made early in the project.
- Expose and elevate the intent and use cases of the system so the architecture reveals its operation at a glance.

# @Guidelines
- **Maintain Programmer Perspective**: The AI MUST NEVER abstract itself away from the code. Architectural designs MUST be grounded in practical programming reality. The AI MUST evaluate the code-level impact and friction of every architectural decision it recommends.
- **Defer Details**: The AI MUST explicitly defer decisions regarding databases, web servers, frameworks, and dependency injection early in the design phase. The AI MUST structure the system so that it is agnostic to these details.
- **Pretend Decisions Are Unmade**: If a specific framework or database is forced by user constraints, the AI MUST pretend the decision has not been made and shape the architecture so that the forced detail can still be changed or deferred as long as possible.
- **Tailor to Team Size (Development)**: The AI MUST consider team structure when partitioning components. For small teams, monolithic structures without heavy superstructure may be recommended to avoid impediments. For large or multiple teams, the AI MUST design well-defined components with reliably stable interfaces.
- **Design for Immediate Deployment (Deployment)**: The AI MUST explicitly evaluate deployment complexity. The AI MUST avoid recommending premature "micro-service architectures" if the configuration and timing of interconnections will compromise the ability to deploy the system with a single action.
- **Scream the Intent (Operation)**: The AI MUST design the architecture to reveal the system's operation. Use cases, features, and required behaviors MUST be elevated to first-class entities with highly visible names (e.g., folder or class names).
- **Mitigate Spelunking (Maintenance)**: The AI MUST separate the system into components and isolate them through stable interfaces to clearly illuminate the pathways for future features and eliminate the risk of inadvertent breakage.
- **Enforce Device Independence**: The AI MUST NOT bind code directly to IO mechanisms, specific physical data formats, or hardware addressing schemes. The AI MUST use abstract unit-record concepts or relative addressing to completely decouple policy from the physical structure of the storage or IO.
- **Treat the Web as a Detail**: The AI MUST NOT let the web delivery mechanism dominate the system structure. The high-level policy MUST remain entirely ignorant of HTML, AJAX, JSP, or REST protocols.

# @Workflow
1. **Identify the Policy**: Extract and list the core business rules and use cases required by the user, entirely ignoring how the data is inputted, stored, or delivered over the web.
2. **Expose Operation**: Define the top-level structure (directories, namespaces, or core classes) using names that explicitly state the use cases (e.g., `OrderProcessor`, `LoanEstimator`). Do not use top-level names that describe frameworks or infrastructure.
3. **Isolate the Details**: Identify all databases, web servers, IO devices, and frameworks. Design boundary interfaces that the Policy will use to communicate with these Details indirectly. 
4. **Draft the Deferral Strategy**: Explicitly document how the architecture allows the database and delivery mechanisms to be deferred, swapped, or experimented with without altering the Policy.
5. **Validate the Four Pillars**:
   - *Development Validation*: Assess if the component boundaries allow parallel teams to work without interference.
   - *Deployment Validation*: Verify that the architecture enables "Immediate Deployment" via a single action. Remove excessive services if they unnecessarily complicate deployment.
   - *Operation Validation*: Ensure the use cases are immediately visible to a new developer looking at the system.
   - *Maintenance Validation*: Confirm that adding a new feature will not require "spelunking" through unrelated code or risk breaking stable code.
6. **Implement with Abstraction**: Write the code ensuring the Policy operates strictly on abstract data representations, leaving physical data mapping, physical addressing, and IO mechanics entirely in the isolated Detail plugins.

# @Examples (Do's and Don'ts)

## Principle: Elevating Use Cases (Operation)
- **[DO]**: Structure the core architecture to reveal what the system does.
  ```text
  /src
    /CalculateInterest
    /ApproveLoan
    /EstimatePayments
  ```
- **[DON'T]**: Structure the architecture to reveal the framework or delivery mechanism.
  ```text
  /src
    /Controllers
    /Views
    /Models
  ```

## Principle: Deferring Details & Keeping Options Open
- **[DO]**: Define business logic to depend on a generic interface, allowing the database decision to be deferred or changed.
  ```python
  class ProcessOrderUseCase:
      def __init__(self, data_repository: OrderRepositoryInterface):
          self.db = data_repository
          
      def execute(self, order_request):
          # Core policy execution unaware of SQL, Mongo, or flat files
          self.db.save(order_request)
  ```
- **[DON'T]**: Bind the business logic directly to a specific database technology or framework.
  ```python
  import sqlite3

  class ProcessOrderUseCase:
      def execute(self, order_request):
          # Core policy polluted by database details
          conn = sqlite3.connect('orders.db')
          cursor = conn.cursor()
          cursor.execute("INSERT INTO orders...")
  ```

## Principle: Physical Addressing and Device Independence
- **[DO]**: Use relative addressing or abstract structures in the application logic, allowing a low-level utility to map it to physical storage.
  ```javascript
  // Application logic uses relative, agnostic IDs
  function retrieveCustomerRecord(customerId) {
      return storageInterface.getRecord(customerId);
  }
  ```
- **[DON'T]**: Hardwire physical disk structures, specific database schemas, or specific IO device instructions into the business logic.
  ```javascript
  // Application logic coupled to physical hardware/storage details
  function retrieveCustomerRecord(customerId) {
      const track = calculateTrack(customerId);
      const sector = calculateSector(customerId);
      return diskController.read(track, sector);
  }
  ```

## Principle: Single-Action Deployment vs. Premature Micro-services
- **[DO]**: Start with a well-partitioned monolith for a small team that can be deployed with a single command (`npm start` or `docker-compose up`), leaving the option to separate into micro-services open for later.
- **[DON'T]**: Immediately adopt a complex micro-service architecture for a small team, resulting in dozens of services that require intricate timing, message queues, and complex configuration scripts just to deploy the initial version.