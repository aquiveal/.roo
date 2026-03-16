@Domain
Trigger these rules when the AI is tasked with integrating third-party libraries, open-source packages, standard language boundary interfaces (like generic collections), subsystems from other teams, or APIs that are not yet fully defined or implemented. 

@Vocabulary
- **Boundary**: The integration point or seam where application-controlled code interacts with foreign, uncontrolled code.
- **Foreign Code / Third-Party Code**: Any code not strictly controlled by the immediate development team, including external libraries, frameworks, or code from other internal departments.
- **Boundary Interface**: A broad, generic interface provided by a language or framework (e.g., `java.util.Map`) that exposes more capabilities than the specific application requires.
- **Learning Test**: A controlled experiment written as a unit test to explore, understand, and verify the expected behavior of a third-party API.
- **Adapter**: A structural design pattern used to bridge the gap between a custom, application-specific interface and a third-party API.
- **Outbound Tests**: A suite of boundary tests that exercise the third-party interface exactly as the production code does, serving as an early-warning system for breaking changes in new versions.

@Objectives
- Cleanly integrate foreign code without polluting the application's internal architecture.
- Protect the application from volatile or breaking changes in third-party dependencies.
- Minimize coupling by constraining the scope and visibility of boundary interfaces.
- Prevent external API limitations or poor design from dictating the application's internal design.
- Continue development even when external dependencies are undefined or unavailable.

@Guidelines
- **Encapsulate Boundary Interfaces**: The AI MUST NOT pass boundary interfaces (e.g., standard Maps, Lists, or raw JSON objects representing domain concepts) loosely around the system. They MUST be hidden inside a specific class or close family of classes.
- **Protect Public APIs**: The AI MUST NOT return boundary interfaces from public APIs or accept them as arguments in public APIs.
- **Constrain Capabilities**: When wrapping a boundary interface, the AI MUST tailor the encapsulating class to expose ONLY the methods necessary for the application, enforcing specific design and business rules.
- **Isolate Learning**: The AI MUST NOT experiment with new third-party APIs directly within production code. 
- **Write Learning Tests**: The AI MUST write Learning Tests to interact with and explore third-party APIs. These tests must focus strictly on what the application needs the API to do.
- **Establish Upgrade Safety Nets**: The AI MUST preserve Learning Tests as Outbound Tests. These tests MUST be run whenever the third-party package is updated to instantly detect incompatible behavioral changes.
- **Define the "Perfect" Interface**: When interacting with code that does not yet exist or is currently undefined, the AI MUST NOT block development. The AI MUST define a custom interface representing the behavior the application *wishes* it had.
- **Bridge with Adapters**: Once an undefined third-party API becomes available, the AI MUST implement an Adapter to translate the "perfect" custom interface to the newly provided API.
- **Use Test Doubles**: For undefined or external interfaces, the AI MUST create Fake or Mock implementations of the custom interface to allow client code to be tested independently of the external system.
- **Control the Dependency**: The AI MUST depend on interfaces it controls rather than interfaces it does not control, preventing external code from dictating application architecture.
- **Centralize Third-Party References**: The AI MUST ensure that references to third-party particulars are concentrated in as few places in the codebase as possible.

@Workflow
1. **Dependency Identification**: When tasked with adding a new external dependency or dealing with an undefined subsystem, halt direct implementation in the core business logic.
2. **Knowledge Acquisition (Learning Tests)**: Write unit tests targeting the external API to verify how it operates, handling edge cases, configuration needs, and expected outputs.
3. **Interface Definition**: Define a highly focused, application-specific interface that abstracts the external dependency. This interface must use domain terminology, not the terminology of the third-party provider.
4. **Encapsulation/Adaptation**: 
    - If wrapping a known generic type (like `Map`), create a custom class that holds the generic type as a private instance variable.
    - If integrating an external library or future API, write an Adapter class that implements your application-specific interface and internally calls the external library.
5. **Client Implementation**: Update the core application to depend exclusively on the custom interface or wrapper, completely ignorant of the underlying third-party implementation.
6. **Testing Integration**: Implement Fakes/Mocks of the custom interface to test the core application logic. Preserve the Learning Tests to run against the real third-party API during future library upgrades.

@Examples (Do's and Don'ts)

**Principle: Encapsulating Boundary Interfaces**

[DON'T] Pass a broad boundary interface around the system, forcing clients to handle type casting and exposing dangerous methods (e.g., `clear()`).
```java
// Anti-pattern: Exposing Map directly
Map<String, Sensor> sensors = new HashMap<String, Sensor>();
// Client code must know how to interact with the Map directly
Sensor s = sensors.get(sensorId);
sensors.clear(); // Dangerous exposed behavior
```

[DO] Encapsulate the boundary interface, hiding its implementation and exposing only the exact methods required by the domain.
```java
// Correct: Encapsulating the Map inside a domain concept
public class Sensors {
    private Map<String, Sensor> sensors = new HashMap<String, Sensor>();

    public Sensor getById(String id) {
        return sensors.get(id);
    }
    // clear() is intentionally not exposed
}
```

**Principle: Using Code That Does Not Yet Exist (Isolating Unknowns)**

[DON'T] Wait for an external team to finish their API before writing your code, or leak their eventual implementation details into your business logic.
```java
// Anti-pattern: Waiting for or directly coupling to an unstable/undefined external Transmitter API
public class CommunicationsController {
    public void sendData(ExternalTransmitter api, double frequency, Stream data) {
        // Tied directly to an API we don't control
        api.initializeFrequency(frequency);
        api.streamAnalogRepresentation(data);
    }
}
```

[DO] Define the interface you wish you had, code your business logic against it, and use an Adapter later.
```java
// Correct: Define the "perfect" interface controlled by the application
public interface Transmitter {
    void transmit(double frequency, Stream data);
}

// Client code depends ONLY on the interface it controls
public class CommunicationsController {
    private Transmitter transmitter;

    public CommunicationsController(Transmitter transmitter) {
        this.transmitter = transmitter;
    }

    public void sendData(double frequency, Stream data) {
        transmitter.transmit(frequency, data);
    }
}

// Once the third-party API is ready, bridge the gap with an Adapter
public class TransmitterAdapter implements Transmitter {
    private ExternalTransmitter api;

    public TransmitterAdapter(ExternalTransmitter api) {
        this.api = api;
    }

    @Override
    public void transmit(double frequency, Stream data) {
        api.initializeFrequency(frequency);
        api.streamAnalogRepresentation(data);
    }
}
```