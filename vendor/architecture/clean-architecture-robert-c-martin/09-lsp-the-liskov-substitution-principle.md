# @Domain
This rule file is activated when the AI is engaged in designing class hierarchies, implementing interfaces, creating polymorphic methods, establishing REST API contracts across multiple services, or refactoring conditional logic that relies on type checking, service provider names, or hardcoded API route variations.

# @Vocabulary
- **LSP (Liskov Substitution Principle)**: The principle stating that if for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2, then S is a subtype of T.
- **Substitutability**: The ability of a system to use any implementation of an interface, base class, or service contract interchangeably without the caller possessing or requiring any knowledge of the specific concrete implementation.
- **Architectural Pollution**: The accumulation of complex mechanisms, `if` statements, or configuration databases required to insulate a system from inconsistent interfaces or violations of substitutability.
- **Contract Violation**: When a subtype alters the fundamental behavior or mutability expectations established by the base type (e.g., tying two independently mutable variables together).

# @Objectives
- Guarantee that all derived classes, interface implementations, and service endpoints are strictly substitutable for their base abstractions.
- Prevent the pollution of system architecture with extra mechanisms, special cases, or conditional type checks.
- Extend LSP thinking beyond object-oriented class inheritance to system-level architecture, encompassing REST APIs, micro-services, and broader system boundaries.
- Eliminate defensive logic in calling modules that checks for specific subtypes or service providers.

# @Guidelines
- The AI MUST ensure that the behavior of a calling program is completely unchanged when substituting a base type with any of its subtypes.
- The AI MUST NOT allow a derived class to restrict, couple, or violate the mutability contracts of its base class. If a base class allows independent mutation of properties, the subclass MUST NOT enforce coupled mutation.
- The AI MUST NOT write defensive mechanisms (such as `if` statements, `instanceof` checks, `typeof` checks, or `switch` cases on class types) in the consuming code to handle subtype-specific behaviors.
- When designing REST APIs or service boundaries, the AI MUST ensure that all providers sharing an interface treat input fields, URIs, and data formats identically.
- The AI MUST NOT hardcode special cases for specific service providers (e.g., checking if a URI belongs to a specific company) within core business logic or dispatch modules.
- If inconsistent external interfaces are completely unavoidable (e.g., third-party APIs out of the developer's control), the AI MUST prevent architectural pollution by isolating the translation via configuration data or a discrete mapping layer, rather than using inline conditional statements in the core logic.

# @Workflow
1. **Analyze the Abstraction Contract**: Review the base class, interface, or REST API definition to establish the exact behavioral, structural, and mutability expectations expected by the calling program.
2. **Verify Independent Mutability**: When generating a subclass, explicitly check the base class for independent mutability. Ensure that no subclass enforces coupled mutations on properties that are independently mutable in the base class. If it does, abort the inheritance relationship.
3. **Check Caller Agnosticism**: Inspect the caller (user) code. Confirm that it relies entirely on the abstraction and invokes operations blindly, without querying the concrete type or the origin of the object/service.
4. **Identify Interface Inconsistencies**: When integrating multiple third-party services or implementing APIs, evaluate the routes and payload structures. Reject or flag slight variations in parameter naming (e.g., `destination` vs `dest`).
5. **Eradicate Type-Based Conditionals**: Scan the codebase for any `if`, `switch`, or type-checking logic that routes execution based on a specific subtype or service provider name. Refactor this logic by pushing the specific behavior down into the polymorphic implementations.
6. **Apply Architectural Isolation**: If dealing with an external LSP violation that cannot be fixed at the source provider, extract the compensation logic into a data-driven configuration dictionary or map. Do not pollute the dispatch or core logic modules with the names of the external providers.

# @Examples (Do's and Don'ts)

## Class Inheritance and Substitutability
**[DO]**
```java
// The caller (Billing) operates on the License abstraction blindly.
// Both PersonalLicense and BusinessLicense are perfectly substitutable.
public abstract class License {
    public abstract Money calcFee();
}

public class PersonalLicense extends License {
    public Money calcFee() {
        return new Money(50);
    }
}

public class BusinessLicense extends License {
    public Money calcFee() {
        return new Money(500);
    }
}

public class Billing {
    public void processLicenses(List<License> licenses) {
        for (License license : licenses) {
            Money fee = license.calcFee(); // No type checking required
            charge(fee);
        }
    }
}
```

**[DON'T]**
```java
// The caller's expectations of independent mutability are violated by the subtype.
// A Square is NOT a substitutable subtype of Rectangle.
public class Rectangle {
    private int width;
    private int height;
    public void setW(int w) { this.width = w; }
    public void setH(int h) { this.height = h; }
    public int area() { return width * height; }
}

public class Square extends Rectangle {
    public void setW(int w) { 
        super.setW(w); 
        super.setH(w); // Violates independent mutability
    }
    public void setH(int h) { 
        super.setH(h); 
        super.setW(h); // Violates independent mutability
    }
}

public class User {
    public void testArea(Rectangle r) {
        r.setW(5);
        r.setH(2);
        assert(r.area() == 10); // Fails if r is a Square!
    }
}
```

## Architectural LSP (Services and REST APIs)
**[DO]**
```javascript
// All service providers conform to the exact same REST interface.
// The aggregator can substitute providers transparently.
function dispatchTaxi(driver) {
    const uri = driver.getDispatchUri();
    const payload = {
        pickupAddress: "24 Maple St.",
        pickupTime: "153",
        destination: "ORD"
    };
    
    // Caller blindly executes the dispatch request
    httpClient.put(uri, payload); 
}
```

**[DON'T]**
```javascript
// The architecture is polluted with a violation of substitutability.
// The caller is forced to know about the concrete provider ("acme.com") 
// to handle its non-conforming interface.
function dispatchTaxi(driver) {
    const uri = driver.getDispatchUri();
    let payload;
    
    if (uri.startsWith("acme.com")) {
        // Acme violates the contract by abbreviating 'destination' to 'dest'
        payload = {
            pickupAddress: "24 Maple St.",
            pickupTime: "153",
            dest: "ORD" 
        };
    } else {
        payload = {
            pickupAddress: "24 Maple St.",
            pickupTime: "153",
            destination: "ORD"
        };
    }
    
    httpClient.put(uri, payload); 
}
```