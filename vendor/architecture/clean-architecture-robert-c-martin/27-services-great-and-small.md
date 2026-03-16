# @Domain
Trigger these rules when evaluating, refactoring, designing, or implementing Service-Oriented Architectures (SOA), micro-services, distributed execution units, or when tasked with adding cross-cutting features to a system composed of multiple services.

# @Vocabulary
*   **Service**: A process or execution unit that communicates across process and/or platform boundaries. Services are essentially expensive function calls and are not, by default, architecturally significant elements.
*   **Architecture**: Defined by the boundaries drawn within a system and by the dependencies that cross those boundaries, separating high-level policy from low-level detail according to the Dependency Rule. It is not defined by physical communication mechanisms (like services).
*   **Decoupling Fallacy**: The incorrect assumption that services are strictly decoupled. Services are strongly coupled by the data records they share and the behaviors they must mutually agree upon.
*   **Independent Deployment Fallacy**: The incorrect assumption that services can always be developed and deployed entirely independently. Data and behavior coupling often require coordinated deployments.
*   **Cross-Cutting Concern (The Kitty Problem)**: A feature or requirement that cuts across multiple functional behaviors or services, making functional service decomposition vulnerable to cascading changes.
*   **Component-Based Service**: A service designed internally using SOLID principles and components, allowing new features to be added as separate, dynamically loadable modules (e.g., JAR files, DLLs, Gems) that extend abstract base classes without modifying existing code.
*   **Dependency Rule**: Source code dependencies must always point inward toward high-level policies.

# @Objectives
*   Prevent the architectural fallacy of equating physical service separation with true architectural decoupling.
*   Protect systems from the cascading modifications caused by cross-cutting concerns.
*   Ensure that architectural boundaries run *through* services, not just *between* them.
*   Structure services internally as extensible, component-based architectures adhering to the Open-Closed Principle and the Dependency Rule.

# @Guidelines
*   The AI MUST NOT assume that extracting functionality into a separate network service establishes an architectural boundary.
*   The AI MUST recognize that if a new field is added to a data record passed between services, every service operating on that field is strongly coupled.
*   When evaluating a new feature that affects multiple functional steps (e.g., UI, Finder, Selector, Dispatcher), the AI MUST explicitly identify this as a cross-cutting concern.
*   The AI MUST NOT implement cross-cutting features by modifying the source code of every existing functional service in the pipeline.
*   The AI MUST apply SOLID design principles within the internal structure of services.
*   The AI MUST use polymorphism, specifically patterns like `Template Method` or `Strategy`, to handle new features without modifying existing service components.
*   The AI MUST structure services as a set of abstract base classes inside core components, allowing new features to be developed as derivative classes residing in entirely separate components.
*   The AI MUST ensure that new feature components follow the Dependency Rule, pointing dependencies toward the abstract base classes of the original components.
*   The AI MUST design services so that adding a new feature involves adding a new deployable unit (e.g., JAR, Gem, DLL) to the service's load path, rather than recompiling and redeploying the existing service monolith.

# @Workflow
1.  **Analyze Service Coupling**: Review the data records passed between the existing services. Identify any shared data structures that create implicit behavioral coupling.
2.  **Evaluate Feature Impact**: When tasked with adding a feature, map out which functional areas (UI, selection, dispatching, etc.) the feature touches. If it touches multiple areas, flag it as a cross-cutting concern.
3.  **Define Abstract Foundations**: Within the existing services, extract the core functional logic into abstract base classes or interfaces, removing specific feature logic.
4.  **Implement Polymorphic Extensions**: Create a new, isolated component for the requested feature. Implement the feature by creating classes that extend the abstract base classes or implement the `Strategy`/`Template Method` interfaces defined in step 3.
5.  **Enforce the Dependency Rule**: Verify that the newly created feature component depends strictly on the core abstract components. The core components MUST NOT have any source code dependencies on the new feature component.
6.  **Configure Dynamic Loading**: Delegate the instantiation of the new feature classes to a factory controlled by the UI or configuration, ensuring the feature can be delivered as an independent deployable unit added to the runtime environment.

# @Examples (Do's and Don'ts)

**Principle: Handling Cross-Cutting Concerns (The Kitty Problem)**

*   **[DON'T]** Modify a chain of functional services to accommodate a new domain concept.
    ```java
    // Anti-pattern: Modifying all existing services for the new "Kitten" feature
    public class TaxiFinderService {
        public List<Candidate> findCandidates(Request req) {
            if (req.isKittenDelivery()) {
                // new kitten specific logic
            } else {
                // standard taxi logic
            }
        }
    }
    public class TaxiSelectorService {
        public Selection select(List<Candidate> candidates, Request req) {
            if (req.isKittenDelivery() && driver.hasCatAllergies()) {
                // new kitten specific logic
            }
        }
    }
    ```

*   **[DO]** Extract the specific domain feature into a separate component that implements strategies defined by the core service abstractions.
    ```java
    // Core Service Component (Abstract)
    public abstract class RideCandidateStrategy {
        public abstract List<Candidate> findCandidates(Request req);
        public abstract boolean isEligible(Candidate candidate, Request req);
    }

    // New Independently Deployable Component (Kittens.jar)
    public class KittenDeliveryStrategy extends RideCandidateStrategy {
        @Override
        public List<Candidate> findCandidates(Request req) {
            return KittenCollectionPointDB.findNearby();
        }

        @Override
        public boolean isEligible(Candidate candidate, Request req) {
            return !candidate.getDriver().hasCatAllergies() &&
                   !candidate.getVehicle().hadKittensInLast(3, TimeUnit.DAYS);
        }
    }
    ```

**Principle: Service Monoliths vs. Component-Based Services**

*   **[DON'T]** Treat a service as a single, tightly coupled monolithic deployment unit where boundaries stop at the network interface.
    ```text
    Service Architecture (Anti-pattern):
    [TaxiFinderService.jar] -> depends on -> shared database
    (To add a feature, we must edit, recompile, and redeploy TaxiFinderService.jar)
    ```

*   **[DO]** Draw architectural boundaries *through* the service, separating it into core abstractions and feature-specific plugin components.
    ```text
    Component-Based Service Architecture:
    [CoreFinderService.jar] (Contains abstract base classes and interfaces)
             ^
             | (Dependency Rule: Plugins depend on Core)
             |
    [StandardRidesPlugin.jar] (Dynamically loaded feature)
    [KittenDeliveryPlugin.jar] (Dynamically loaded feature)
    ```