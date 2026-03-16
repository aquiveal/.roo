@Domain
These rules MUST trigger when the AI is requested to design system architecture, create remote APIs, implement Web Services, establish network or process boundaries, refactor distributed object models, or write code that communicates across physical tiers (e.g., Client/Server, Web Server/Application Server, Application Server/Database).

@Vocabulary
- **First Law of Distributed Object Design**: "Don't distribute your objects!" The foundational principle that objects should reside in a single process rather than being distributed across network nodes by class or component.
- **Clustering**: The deployment strategy of placing all classes into a single process and running multiple identical copies of that process across various processing nodes to achieve scalability and load balancing.
- **Transparency**: A middleware illusion that allows objects to call each other without knowing if the callee is in the same process or a different one. (Considered a dangerous concept regarding performance).
- **Fine-Grained Interface**: An interface utilizing lots of small methods (e.g., `getCity()`, `getState()`). Ideal for in-process OO design but catastrophic for remote performance.
- **Coarse-Grained Interface**: An interface designed to minimize calls by bundling operations and data (e.g., `updateAddressDetails()`). Mandatory for inter-process/remote communication.
- **Remote Facade**: A coarse-grained object placed at the distribution boundary whose sole role is to translate coarse-grained remote methods into calls on underlying fine-grained local objects. It contains NO domain logic.
- **Data Transfer Object (DTO)**: An object used to bundle and carry data across a network connection in a single call. It must be easily serializable and contain NO references to internal domain objects.
- **Web Service / XML-HTTP Interface**: A cross-platform remote interface. Verbose and slow; to be used only for integration across different platforms, not for internal application distribution.

@Objectives
- The AI MUST aggressively minimize the number of inter-process and remote procedure calls in any system design.
- The AI MUST advocate for clustering over distributed object topologies.
- The AI MUST enforce a strict separation between in-process communication (fine-grained) and out-of-process communication (coarse-grained).
- The AI MUST ensure that distribution boundaries are explicit and never hidden behind "transparent" middleware abstractions.
- The AI MUST prevent domain logic from leaking into distribution boundaries (Facades and DTOs).

@Guidelines

**1. System Topologies and Distribution**
- When requested to scale a system or distribute objects by class (e.g., placing `Customer` objects on Node A and `Order` objects on Node B), the AI MUST reject this approach and instead implement **Clustering**.
- When evaluating architectural boundaries, the AI MUST allow distribution ONLY in the following unavoidable scenarios:
  - Client/Server divides (desktop/browser to shared data repository).
  - Application Server to Database (optimizing SQL, which is inherently a remote interface).
  - Web Server to Application Server (only when strictly necessary; otherwise, run in a single process).
  - Integration with third-party software packages or vendor systems.
  - Unavoidable, genuine physical splits in application server software.

**2. Interface Granularity**
- When generating code for intra-process (local) object collaboration, the AI MUST use **Fine-Grained Interfaces** to promote flexibility, extendibility, and standard Object-Oriented principles.
- When generating code that crosses a process or network boundary, the AI MUST use **Coarse-Grained Interfaces** to minimize network latency and roundtrips.
- When evaluating middleware that claims "Transparency" between local and remote calls, the AI MUST explicitly warn the user that transparency is a fallacy regarding performance, and that interface design MUST change at process boundaries.

**3. Implementing the Distribution Boundary**
- When creating a distribution boundary, the AI MUST implement a **Remote Facade**.
- When generating a Remote Facade, the AI MUST ensure it is a thin skin that delegates entirely to local fine-grained objects. The AI MUST NOT place any domain logic, validations, or workflow rules inside the Remote Facade.
- When exposing operations remotely, the AI MUST make the distribution policy explicit so developers are aware they are invoking an expensive remote call.

**4. Data Transfer**
- When data must cross a Remote Facade, the AI MUST generate a **Data Transfer Object (DTO)** to bundle the data.
- When designing a DTO, the AI MUST ensure it references ONLY other DTOs and fundamental primitive/string types. It MUST NOT contain references to local domain objects or webs of fine-grained local inter-object references.
- When returning data remotely, the AI MUST err on the side of sending *too much* data in a single DTO rather than requiring the client to make multiple remote calls to fetch missing data.

**5. Protocols and Web Services**
- When selecting a transport mechanism between two systems built on the *same* software platform, the AI MUST favor native binary Remote Procedure Call (RPC) mechanisms over XML/HTTP or SOAP due to performance overhead.
- When integrating systems built on *different* platforms, the AI MUST implement XML/HTTP (Web Services/SOAP/REST).
- When exposing an OO API as a Web Service, the AI MUST layer the HTTP interface over the existing OO interface, transforming HTTP requests into standard OO calls.
- When designing new distributed interactions, the AI MUST favor or suggest asynchronous, message-based communication over synchronous RPC wherever the business use case permits.

@Workflow
When tasked with designing, implementing, or reviewing a distributed system architecture, the AI MUST adhere to the following rigid algorithmic process:

1. **Challenge Distribution**: Analyze the request to see if distribution is genuinely required. If the user is trying to distribute business objects across servers for "load balancing", forcefully recommend **Clustering** instead.
2. **Identify Boundaries**: If distribution is unavoidable (e.g., UI client to server, or platform to vendor package), explicitly map out the exact line where the inter-process communication occurs.
3. **Isolate Domain Logic**: Ensure all complex business logic is contained within standard, Fine-Grained local domain objects.
4. **Construct Remote Facades**: Create Coarse-Grained facade classes at the boundary line. Map bulk operations (e.g., `getOrderDetails`) to the underlying Fine-Grained domain methods.
5. **Construct DTOs**: Create serializable Data Transfer Objects for all inputs and outputs of the Remote Facade. Strip all domain object references from these DTOs.
6. **Optimize Transport**: Select the transport protocol. Default to native binary RPC for identical platforms, and XML/HTTP Web Services only for cross-platform integration.
7. **Review for Asynchrony**: Evaluate if the remote call can be handled via asynchronous messaging and advise the user accordingly.

@Examples (Do's and Don'ts)

**Principle: System Distribution Topologies**
- [DO]: Deploy the entire application logic (Customer, Order, Product) into a single unified process, and deploy copies of this exact same process across Server A, Server B, and Server C (Clustering).
- [DON'T]: Deploy the `Customer` component on Server A, the `Order` component on Server B, and the `Product` component on Server C, causing them to communicate over the network.

**Principle: Interface Granularity at Boundaries**
- [DO]: Create a coarse-grained method on a remote service: `public CustomerProfileDTO getCustomerProfile(String customerId);`
- [DON'T]: Expose fine-grained methods on a remote service: `public String getCustomerCity(String customerId); public String getCustomerState(String customerId);`

**Principle: Remote Facade Implementation**
- [DO]: 
```java
// Remote Facade
public void updateCustomerAddress(String id, AddressDTO dto) {
    Customer customer = customerRepository.findById(id);
    Address address = new Address(dto.getStreet(), dto.getCity(), dto.getZip());
    customer.updateAddress(address); // Domain logic stays in the domain object
}
```
- [DON'T]: 
```java
// Remote Facade
public void updateCustomerAddress(String id, AddressDTO dto) {
    Customer customer = customerRepository.findById(id);
    // Anti-pattern: Domain logic leaking into Facade
    if (dto.getZip() == null || dto.getZip().length() < 5) {
        throw new ValidationException("Invalid Zip"); 
    }
    customer.setStreet(dto.getStreet());
    customer.setCity(dto.getCity());
    customer.setZip(dto.getZip());
}
```

**Principle: Data Transfer Objects (DTOs)**
- [DO]:
```java
public class OrderDTO implements Serializable {
    public String orderId;
    public String customerName;
    public List<String> itemNames; // Uses fundamental types
}
```
- [DON'T]:
```java
public class OrderDTO implements Serializable {
    public String orderId;
    public CustomerDomainEntity customer; // Anti-pattern: References local domain objects!
}
```