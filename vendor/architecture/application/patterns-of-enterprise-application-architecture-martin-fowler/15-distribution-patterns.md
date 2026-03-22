# @Domain

These rules MUST be triggered whenever the AI is tasked with designing, implementing, refactoring, or reviewing architectures involving network boundaries, remote APIs, web services (REST/SOAP/RPC), inter-process communication (IPC), client-server data exchange, or distributed systems. This includes any requests involving `Remote Facade`, `Data Transfer Object (DTO)`, `Assembler`/`Mapper` classes for external APIs, or decisions regarding system scalability and node distribution.

# @Vocabulary

*   **Distribution Boundary**: The physical or process separation between different parts of a system (e.g., client vs. server, web server vs. application server). Crossing this boundary requires an expensive remote call.
*   **First Law of Distributed Object Design**: "Don't distribute your objects!" The principle that distributing an application by putting different interconnected components on different physical nodes cripples performance and increases complexity.
*   **Clustering**: The preferred alternative to distributing objects, where all classes are placed into a single process, and multiple identical copies of that process are run across various physical nodes to scale the system.
*   **Local Interface**: A fine-grained interface used within a single process. Favors small methods and small objects to maximize extendibility and maintainability.
*   **Remote Interface**: A coarse-grained interface used across a distribution boundary. Designed specifically to minimize the number of network calls (roundtrips) required to perform an action.
*   **Remote Facade**: A coarse-grained facade object placed explicitly at a distribution boundary. It wraps a web of fine-grained local objects, providing a remote interface without containing any domain logic itself.
*   **Data Transfer Object (DTO)**: A serializable object that aggregates and carries multiple pieces of data across a process or network boundary in a single method call. Contains no domain logic.
*   **Assembler (or DTO Mapper)**: A specialized object responsible for transferring data between the internal Domain Model objects and external Data Transfer Objects, ensuring neither knows about the other.
*   **Bulk Accessor**: A single getter or setter method on a Remote Facade that retrieves or updates a large block of data (usually via a DTO) to avoid multiple fine-grained remote calls.

# @Objectives

*   **Minimize Remote Calls**: The AI MUST optimize all distributed interactions to use the absolute minimum number of network roundtrips. 
*   **Isolate Domain Logic**: The AI MUST completely isolate domain/business logic from the mechanics of distribution, remote communication, and API formatting.
*   **Maintain Granularity Separation**: The AI MUST maintain fine-grained interfaces for in-process object collaboration while strictly enforcing coarse-grained interfaces for cross-process communication.
*   **Decouple Data Representations**: The AI MUST ensure that the internal Domain Model structure is never leaked directly across a network boundary, nor is it strictly coupled to the DTO structure.

# @Guidelines

### 1. Architecture & Distribution Strategies
*   **Obey the First Law**: The AI MUST NEVER proactively suggest separating a cohesive object model or domain layer across different physical processes or servers simply for "performance."
*   **Default to Clustering**: When horizontal scalability is required, the AI MUST suggest scaling via Clustering (running identical full-stack processes on multiple nodes) rather than distributing discrete components across nodes.
*   **Acknowledge Hard Boundaries**: The AI MUST apply distribution patterns ONLY at unavoidable boundaries (e.g., client to server, application server to database, integration with external vendor packages).
*   **Restrict Web Services**: The AI MUST NOT use Web Services (XML/HTTP/SOAP/REST) for intra-application communication. Web Services MUST only be used for application integration across disparate platforms or as the outermost presentation layer.

### 2. Remote Facade Constraints
*   **Enforce Coarse-Grained Interfaces**: Any object intended for remote use MUST have a coarse-grained interface (bulk accessors/mutators). The AI MUST NEVER expose a fine-grained object (like an individual `Address` with `setCity`, `setState`) over a remote interface.
*   **Zero Domain Logic**: The AI MUST NEVER place any domain logic, validation, or business workflow rules inside a Remote Facade. The facade's ONLY job is to unpack the request, delegate to fine-grained domain objects, and pack the response.
*   **Centralize Transactions & Security**: The AI MUST utilize the methods of the Remote Facade as the primary boundaries for initiating/committing transactions and performing security/access-control checks. A transaction MUST NOT be left open when control returns to the client.
*   **Consolidate Facades**: The AI MUST favor a smaller number of Remote Facades with many cohesive methods (e.g., `CustomerService` covering multiple customer-related use cases) over dozens of tiny, single-method facades.
*   **State Management**: If a Remote Facade must maintain session state, the AI MUST explicitly design a state management strategy (Client Session State, Server Session State, or Database Session State) and be aware of pooling implications. Stateless Remote Facades are preferred for pooling efficiency.

### 3. Data Transfer Object (DTO) Constraints
*   **Bundle Data**: The AI MUST aggregate data from multiple domain objects into a single DTO if the client needs that data simultaneously. Err on the side of sending too much data rather than requiring the client to make a second remote call.
*   **No Domain Objects**: The AI MUST NEVER include Domain Model objects inside a DTO. A DTO MUST ONLY contain primitives, strings, simple data types (dates), or other DTOs.
*   **Graph Simplification**: The AI MUST flatten or simplify the complex graph of a Domain Model into a simple hierarchical graph suitable for straightforward serialization.
*   **Client-Driven Design**: The AI MUST design the DTO structure around the needs of the client (e.g., a specific UI screen or API consumer) rather than blindly mirroring the database or Domain Model.
*   **Serialization Tolerance**: When implementing serialization, the AI MUST consider versioning. If binary serialization is used, the AI MUST warn that client and server must be perfectly synced. Prefer tolerant serialization (e.g., Map-based, XML, or JSON with unknown-property-ignore features) if clients might be outdated.

### 4. Assembler Constraints
*   **Strict Decoupling**: The AI MUST NOT allow the Domain Object to instantiate or populate a DTO. The AI MUST NOT allow a DTO to instantiate or populate a Domain Object.
*   **Use Assemblers**: The AI MUST create a dedicated Assembler (or Mapper) class to read from the Domain Model and write to the DTO, and vice versa. 
*   **Handling Updates**: When an Assembler processes an incoming DTO to update the Domain Model, the AI MUST carefully apply business rules (e.g., deciding whether to update an existing object, destroy and replace it, or throw an error if an expected related object is missing).

# @Workflow

When tasked with creating or modifying a distributed boundary, a remote API, or a web service, the AI MUST execute the following algorithmic process:

1.  **Distribution Assessment**: Verify that a physical network/process boundary is actually required. If the request attempts to artificially distribute a single application without justification, advise Clustering instead.
2.  **Domain Model Verification**: Ensure the underlying Domain Model is designed with fine-grained, cohesive objects, ignoring any remote access requirements.
3.  **Client Needs Analysis**: Identify the specific data payload the remote client needs to display a screen or complete a process.
4.  **DTO Construction**: Design a `DataTransferObject` (or hierarchy of DTOs) that encapsulates the exact payload required by the client in step 3. Ensure the DTO uses only primitives and easily serializable types.
5.  **Assembler Implementation**: Create an `Assembler` class. Implement a method `writeDTO(DomainObject)` to map outward, and `updateDomain(DTO)` to map inward.
6.  **Remote Facade Implementation**: Create the `RemoteFacade`. 
    *   Add a coarse-grained method for the client operation.
    *   Implement transaction boundaries (begin/commit) around the method logic.
    *   Implement security checks.
    *   Instantiate the Assembler, invoke the fine-grained Domain Model, and return the resulting DTO.

# @Examples (Do's and Don'ts)

### [DO] Remote Facade and Assembler implementation isolating Domain Logic
**Explanation:** The Remote Facade handles the transaction and uses an Assembler to convert the Domain Object into a DTO. The Domain Object remains completely ignorant of the DTO and the Facade.

```java
// 1. The DTO (Pure data, serializable, no domain logic)
public class AlbumDTO implements Serializable {
    public String title;
    public String artistName;
    public String[] trackTitles;
}

// 2. The Assembler (Decouples Domain from DTO)
public class AlbumAssembler {
    public AlbumDTO writeDTO(Album album) {
        AlbumDTO dto = new AlbumDTO();
        dto.title = album.getTitle();
        dto.artistName = album.getArtist().getName();
        
        List<String> tracks = new ArrayList<>();
        for (Track track : album.getTracks()) {
            tracks.add(track.getTitle());
        }
        dto.trackTitles = tracks.toArray(new String[0]);
        return dto;
    }
}

// 3. The Remote Facade (Coarse-grained, handles transaction, delegates logic)
public class AlbumServiceFacade {
    
    public AlbumDTO getAlbumDetails(String albumId) throws RemoteException {
        TransactionManager.beginTransaction();
        try {
            // Security check
            SecurityManager.checkPermission("READ_ALBUM");
            
            // Fetch fine-grained domain object
            Album album = Registry.findAlbum(albumId);
            if (album == null) throw new ObjectNotFoundException();
            
            // Assemble and return DTO
            AlbumAssembler assembler = new AlbumAssembler();
            AlbumDTO result = assembler.writeDTO(album);
            
            TransactionManager.commitTransaction();
            return result;
        } catch (Exception e) {
            TransactionManager.rollbackTransaction();
            throw new RemoteException("Failed to fetch album", e);
        }
    }
}
```

### [DON'T] Remote Facade containing Domain Logic and exposing Fine-Grained interfaces
**Explanation:** This anti-pattern exposes fine-grained methods (`setArtist`, `setTitle`) over a network, causing severe latency due to multiple roundtrips. It also places domain logic inside the distributed boundary, and leaks internal domain models to the client.

```java
// ANTI-PATTERN: DO NOT DO THIS
public class RemoteAlbumService {
    
    // BAD: Fine-grained remote methods require multiple network roundtrips
    public void setAlbumTitle(String albumId, String title) throws RemoteException {
        Album album = Database.getAlbum(albumId);
        album.setTitle(title);
        Database.save(album);
    }

    public void setAlbumArtist(String albumId, String artistId) throws RemoteException {
        Album album = Database.getAlbum(albumId);
        Artist artist = Database.getArtist(artistId);
        album.setArtist(artist);
        Database.save(album);
    }

    // BAD: Returns a complex Domain Object directly over the wire, 
    // which may fail serialization or cause Lazy Load exceptions on the client.
    public Album getAlbum(String albumId) throws RemoteException {
        return Database.getAlbum(albumId);
    }

    // BAD: Domain logic inside the Remote Facade
    public void calculateRevenue(String albumId) throws RemoteException {
        Album album = Database.getAlbum(albumId);
        // Domain logic leaking into distribution layer
        double revenue = album.getSales() * 0.15; 
        if (revenue > 1000) {
            album.markAsProfitable();
        }
        Database.save(album);
    }
}
```

### [DO] DTO aggregating multiple Domain Objects
**Explanation:** The DTO combines data from `Order`, `Customer`, and `LineItem` objects so the client receives everything in a single remote call.

```java
public class OrderSummaryDTO {
    public String orderId;
    public String customerName;
    public String customerShippingAddress;
    public double totalAmount;
    public String[] itemNames;
}
```

### [DON'T] Domain Object serializing itself into a DTO
**Explanation:** A Domain Object should not depend on the DTO or API layer.

```java
// ANTI-PATTERN: DO NOT DO THIS
public class Order extends DomainObject {
    private Customer customer;
    private List<LineItem> items;

    // BAD: Domain object knows about external DTO representations
    public OrderSummaryDTO toDTO() {
        OrderSummaryDTO dto = new OrderSummaryDTO();
        dto.orderId = this.getId();
        dto.customerName = this.customer.getName();
        return dto;
    }
}
```