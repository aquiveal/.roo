# @Domain
This set of rules is activated whenever the AI is tasked with software architecture design, specifically when grouping classes, functions, or modules into larger components, packages, or deployable units. It applies during system refactoring, package creation, dependency management, and release cycle planning.

# @Vocabulary
- **Component**: The units of deployment. The smallest entities that can be deployed as part of a system (e.g., jar files, DLLs, Gem files).
- **Component Cohesion**: The logical and physical forces that dictate which classes and modules belong together inside the same component.
- **REP (Reuse/Release Equivalence Principle)**: "The granule of reuse is the granule of release." The principle stating that components must be releasable units with tracking, versioning, and documentation, sharing an overarching theme.
- **CCP (Common Closure Principle)**: "Gather into components those classes that change for the same reasons and at the same times. Separate into different components those classes that change at different times and for different reasons." The component-level equivalent of the Single Responsibility Principle (SRP).
- **CRP (Common Reuse Principle)**: "Don't force users of a component to depend on things they don't need." The component-level equivalent of the Interface Segregation Principle (ISP).
- **Tension Diagram for Component Cohesion**: The conceptual framework representing the opposing forces of REP/CCP (inclusive principles that make components larger) and CRP (an exclusive principle that makes components smaller).

# @Objectives
- Group classes into deployable components based on clear, justifiable architectural principles rather than ad-hoc context.
- Isolate the impact of changes to minimize the number of components that must be recompiled, revalidated, and redeployed.
- Prevent consumers of a component from being forced to depend on classes and modules they do not use.
- Dynamically balance the architectural tension between "develop-ability" (maintainability) and "reusability" based on the current maturity stage of the project.

# @Guidelines
- The AI MUST enforce the **REP** by ensuring all classes within a component share an overarching theme, purpose, and make sense to be released together under a single version number with shared release documentation.
- The AI MUST NOT create components consisting of a random hodgepodge of unrelated classes or modules.
- The AI MUST enforce the **CCP** by co-locating classes that are closed to the same types of expected changes. If two classes are so tightly bound that they always change together, they MUST be in the same component.
- The AI MUST prioritize maintainability over reusability during the early stages of a project's lifecycle by heavily favoring the CCP to minimize the blast radius of changes.
- The AI MUST enforce the **CRP** by ensuring that classes grouped together are inseparable in their reuse. If a consuming component only uses one class from a target component, the dependency is still rigid; therefore, unused classes MUST be moved to separate components.
- The AI MUST NOT force a system to depend on components containing unused classes, as this triggers unnecessary recompilation, revalidation, and redeployment.
- The AI MUST act as the resolver of the **Tension Triangle**: 
  - Do not focus solely on REP and CRP, or too many components will be impacted during simple changes.
  - Do not focus solely on CCP and REP, or too many unneeded releases will be generated for consumers.
- The AI MUST continually re-evaluate the component structure. As a project matures and begins to be consumed by other projects, the AI MUST shift the architectural focus from develop-ability (CCP) toward reusability (REP and CRP), allowing the component composition to jitter and evolve over time.

# @Workflow
1. **Analyze Class Relationships**: Before grouping classes into a component, evaluate their behavior, change frequency, and reuse patterns.
2. **Apply the Common Closure Principle (CCP)**: Identify axes of change. Group classes that change for the same business reasons or at the same times into a single component candidate.
3. **Apply the Common Reuse Principle (CRP)**: Evaluate the component candidate's internal classes. Ask: "Are these classes always reused together?" (e.g., a Container and its Iterator). If certain classes are used independently of the rest, extract them into a separate component.
4. **Apply the Reuse/Release Equivalence Principle (REP)**: Validate the resulting component. Ensure it has a single, cohesive theme that can be logically documented, versioned, and tracked through a formal release process.
5. **Evaluate Project Maturity**: 
   - If the project is in early development, explicitly bias the grouping toward **CCP** to maximize develop-ability and keep the number of deployed components small.
   - If the project is mature and highly consumed, explicitly bias the grouping toward **REP** and **CRP** to protect consumers from unnecessary updates.
6. **Iterate and Refactor**: Treat component boundaries as fluid. If changes repeatedly span multiple components, merge them (CCP). If consumers complain about massive dependency updates for minor features, split them (CRP).

# @Examples (Do's and Don'ts)

## Reuse/Release Equivalence Principle (REP)
- **[DO]**: Group a `SecureSocket`, `PacketFormatter`, and `ConnectionManager` into a `NetworkCommunications` component, tagging it with a release version (e.g., v1.2.0) and a changelog, because they form a cohesive, thematic module.
- **[DON'T]**: Group a `DatabaseQueryBuilder` and a `ScreenPixelRenderer` into a `CoreUtils` component just because they were written by the same developer. This violates REP as they lack an overarching theme and logical release equivalence.

## Common Closure Principle (CCP)
- **[DO]**: Place `OrderValidator`, `OrderCalculator`, and `OrderRepository` into a single `OrderProcessing` component. When the business rules for processing an order change, only this single component needs to be recompiled, revalidated, and redeployed.
- **[DON'T]**: Place `OrderValidator` in an `API` component and `OrderCalculator` in a `Math` component. When order rules change, multiple independent components will require simultaneous changes and synchronized releases, causing deployment friction.

## Common Reuse Principle (CRP)
- **[DO]**: Separate a heavy `ImageProcessing` library from a lightweight `StringUtilities` library. A module that needs to capitalize a string should depend only on `StringUtilities` and remain completely isolated from the `ImageProcessing` component.
- **[DON'T]**: Place `StringUtilities` and `ImageProcessing` into a single `CommonTools` component. If a developer updates an image filter, every module using `StringUtilities` will be forced to recompile, revalidate, and redeploy despite not caring about the image filter change.