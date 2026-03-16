# @Domain
These rules apply when the AI is engaged in architectural design, component modeling, defining module interfaces, structuring monoliths, extracting micro-services, configuring inter-process communications (IPC), or establishing any boundary interactions between separated software elements. 

# @Vocabulary
- **Boundary Crossing**: A runtime event where a function on one side of a boundary calls a function on the other side and passes data.
- **Monolith**: A software architecture utilizing a single processor and single address space, usually deployed as a single executable file (e.g., statically linked C/C++, executable JAR, or .EXE).
- **Deployment Component**: A dynamically linked library (e.g., .Net DLL, Java JAR, Ruby Gem, UNIX shared library) that requires no compilation during deployment, only gathering.
- **Local Process**: A strong physical boundary where components run in the same processor (or multicore) but in separate memory address spaces, communicating via OS facilities (sockets, mailboxes, message queues).
- **Service**: The strongest architectural boundary, consisting of processes that assume all communication takes place over a network, independent of physical location.
- **Dynamic Polymorphism**: The mechanism used to invert dependencies against the flow of control, enabling high-level components to call low-level components without source code dependencies pointing to the low-level component.
- **Chattiness**: High-frequency, back-and-forth communication between components.

# @Objectives
- Actively manage and restrict source code dependencies across boundaries to build firewalls against cascading changes, recompilations, and redeployments.
- Ensure that source code dependencies strictly point toward higher-level components, regardless of the direction of the runtime flow of control.
- Tailor the communication frequency (chattiness) and data marshaling strictly according to the physical boundary type (Monolith vs. Process vs. Service).
- Enforce the rule that lower-level processes and services must always act as interchangeable plugins to higher-level processes and services.

# @Guidelines
- **Boundary Crossing Independence**: The AI MUST manage source code dependencies for every boundary crossing. When separating components, you MUST prevent changes in one source code module from forcing recompilation or redeployment of another.
- **Monoliths and Deployment Components**: 
  - The AI MUST enforce disciplined segregation of functions and data even when components are deployed in a single executable or dynamically linked library.
  - The AI MAY design chatty, fine-grained communication across these boundaries, as function calls are fast and inexpensive here.
- **Dependency Direction and Polymorphism**:
  - When a lower-level client calls a higher-level service, both runtime flow and compile-time dependencies MUST point toward the higher-level component.
  - When a higher-level client needs to invoke a lower-level service, the AI MUST use dynamic polymorphism (interfaces/abstract classes) to invert the dependency. 
  - The source code dependency MUST point toward the higher-level component, opposing the flow of control.
  - The definition of the data structure passed across the boundary MUST reside on the calling side of the boundary.
- **Thread Management**: The AI MUST NOT treat threads as architectural boundaries or deployment units. Threads MUST be used exclusively as a mechanism to organize the schedule and order of execution.
- **Local Process Constraints**:
  - The AI MUST route communication between local processes using OS facilities (sockets, mailboxes, message queues).
  - The AI MUST limit chattiness across local processes due to the moderate expense of OS calls, data marshaling, decoding, and context switches.
  - High-level local processes MUST NOT contain the names, physical addresses, or registry lookup keys of lower-level local processes.
- **Service Constraints**:
  - The AI MUST assume all communication across service boundaries implies network-level latency (tens of milliseconds to seconds).
  - The AI MUST strictly avoid chatty communication across service boundaries.
  - High-level services MUST NOT contain specific physical knowledge (e.g., hardcoded URIs) of any lower-level service.

# @Workflow
1. **Identify Boundary Type**: Determine if the interaction crosses a Monolith/Deployment Component boundary, a Local Process boundary, or a Service boundary.
2. **Establish Dependency Direction**: Identify which component represents the higher-level policy and which represents the lower-level detail. Ensure all source-code dependencies (imports, requires, includes) point toward the higher-level component.
3. **Apply Interface and Data Abstraction**: If the flow of control goes from high-level to low-level, define an interface inside the high-level component. Define the data structures required for the communication inside the high-level component as well.
4. **Enforce Communication Rules**:
   - If the boundary is a Monolith/Deployment Component, standard function calls and chatty interactions are permitted.
   - If the boundary is a Local Process or Service, bundle data into coarse-grained structures to minimize network/marshaling overhead.
5. **Sanitize Physical Knowledge**: Scan the high-level component to ensure absolutely no URIs, physical addresses, or registry keys related to the lower-level components are hardcoded into the source code.

# @Examples (Do's and Don'ts)

**Principle: Dependency Inversion across Boundaries**
- [DO]: Define an interface and the required data structure in the high-level business logic component. Have the low-level database or delivery component implement that interface.
- [DON'T]: Allow the high-level business logic to import a class or data structure defined in the low-level database component.

**Principle: Local Process and Service Decoupling**
- [DO]: Pass a generic configuration interface or utilize a service discovery mechanism (injected at startup) so the high-level service interacts with the low-level service without knowing its physical location.
- [DON'T]: Hardcode `const lowerLevelServiceUri = "http://10.0.0.5:8080/api"` inside the high-level service's source code.

**Principle: Managing Chattiness based on Boundary Anatomy**
- [DO]: Design coarse-grained DTOs (Data Transfer Objects) to send a complete batch of necessary data across a Service or Local Process boundary in a single network/OS call.
- [DON'T]: Design a Service boundary that requires the client to make 50 separate, sequential HTTP calls to retrieve individual properties of an entity. 

**Principle: Thread Anatomy**
- [DO]: Use threads inside a single deployment component to manage concurrent task execution while maintaining the component's strict architectural boundary.
- [DON'T]: Rely on threads to serve as an architectural boundary separating high-level policy from low-level details.