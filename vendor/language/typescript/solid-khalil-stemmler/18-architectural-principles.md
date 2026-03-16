@Domain
These rules MUST trigger whenever the AI is tasked with creating new modules, refactoring project structure, managing imports and dependencies, designing package boundaries, or making architectural decisions regarding file and class grouping.

@Vocabulary
- **Architecture**: The process of making smart decisions about relationships and dependencies to put the codebase in a good position for future changes.
- **Coupling**: The degree to which components rely on one another.
- **Cohesion**: The degree to which elements inside a component belong together.
- **Reuse-Release Equivalence Principle (REP)**: The rule stating that "The granule of reuse is the granule of release." Items grouped for reuse must be versioned and released together.
- **Common Closure Principle (CCP)**: The component-level equivalent of the Single Responsibility Principle. "Gather into components those classes that change for the same reasons and at the same times. Separate into different components those classes that change at different times and for different reasons."
- **Common Reuse Principle (CRP)**: The component-level equivalent of the Interface Segregation Principle. "Don’t force users of a component to depend on things they don’t need."
- **Stable Components**: Components that are hard to change (often because many other components depend on them) and contain high-level policy.
- **Volatile Components**: Components that change frequently and contain low-level implementation details.
- **Policy**: High-level business rules that dictate the core behavior of the application.
- **Conway’s Law**: The principle that software boundaries should mirror the communication structures of the organization/domain.
- **The Dependency Rule**: The rule dictating the strict direction of source code dependencies (always pointing toward higher-level, stable policy).
- **Boundaries**: Logical and physical separations between different parts of the system to isolate changes and enforce the Dependency Rule.

@Objectives
- Make smart, calculated decisions regarding component relationships and dependencies.
- Enforce strict architectural boundaries to prevent ripple effects during code modifications.
- Group classes and files based on their change vectors (CCP) and usage patterns (CRP).
- Protect high-level policy from low-level volatile implementation details.

@Guidelines
- **Dependency Management**: The AI MUST explicitly analyze the dependency graph of any code it writes or modifies. Dependencies MUST flow from Volatile Components towards Stable Components.
- **Enforce the Dependency Rule**: The AI MUST NEVER allow high-level Policy components to import or depend on low-level detail components (e.g., UI, Database, Frameworks).
- **Enforce the Common Closure Principle (CCP)**: When grouping classes into a folder, package, or component, the AI MUST group items that require modification at the same time for the same business reason. If changing feature X requires modifying Class A and Class B, they belong in the same component.
- **Enforce the Common Reuse Principle (CRP)**: The AI MUST NOT create bloated components (e.g., "shared-utils") that force dependent modules to import code they do not use. Extract unrelated functionality into discrete, highly focused components.
- **Enforce the Reuse-Release Equivalence Principle (REP)**: When generating reusable packages or libraries, the AI MUST ensure all code within that package is cohesive enough to be versioned, tracked, and released as a single unit.
- **Establish Boundaries**: The AI MUST use interfaces, abstract classes, or explicit module exports to create Boundaries between domains. Do not allow implicit or hidden dependencies across boundaries.
- **Respect Conway's Law**: When structuring the architecture, the AI MUST group components according to the real-world actors, roles, and subdomains they serve, minimizing cross-boundary coupling.
- **Isolate Volatility**: The AI MUST identify code that is likely to change frequently (Volatile Components) and isolate it behind boundaries so that its changes do not force recompilation or modification of Stable Components.

@Workflow
1. **Analyze Dependencies**: Before creating or moving a class, identify what it depends on and what depends on it. Determine if it is a Stable Component (Policy) or a Volatile Component (Detail).
2. **Apply CCP (Grouping for Change)**: Ask: "If a business requirement changes, which files will I need to touch?" Group those files together into a single component or module.
3. **Apply CRP (Grouping for Reuse)**: Ask: "If a consumer imports this component, are they forced to depend on classes or libraries they don't need?" If yes, split the component into smaller, tightly focused modules.
4. **Enforce the Dependency Rule**: Review all `import` statements. Ensure no Stable Component imports a Volatile Component. If a violation is found, use Dependency Inversion (e.g., an interface) to reverse the source code dependency.
5. **Establish Boundaries**: Ensure the component explicitly exports only what is necessary for release and reuse (REP). Hide all other internals.

@Examples (Do's and Don'ts)

**Principle: Common Closure Principle (CCP)**

[DO]
Group classes that change for the same business reason together in the same feature module.
```typescript
// src/modules/billing/
// These classes change together whenever the billing policy changes.
export class InvoiceGenerator { ... }
export class TaxCalculator { ... }
export class BillingPolicy { ... }
```

[DON'T]
Scatter classes that change for the same reason across infrastructure-based folders, requiring modifications across the entire codebase for a single business requirement change.
```typescript
// src/controllers/BillingController.ts
// src/services/TaxService.ts
// src/models/Invoice.ts
```

**Principle: Common Reuse Principle (CRP)**

[DO]
Create highly focused modules so consumers only depend on what they actually use.
```typescript
// src/packages/string-utils/
export function capitalize() { ... }
export function camelCase() { ... }

// src/packages/date-utils/
export function formatDate() { ... }
```

[DON'T]
Create a bloated "common" or "utils" component that forces users to depend on unrelated modules and third-party libraries they don't need.
```typescript
// src/utils/index.ts
export * from './stringUtils';
export * from './dateUtils';
export * from './databaseConnectionUtils'; // Forces string-utils users to depend on DB libraries!
export * from './htmlParserUtils';
```

**Principle: The Dependency Rule & Stable/Volatile Components**

[DO]
Have Volatile Components (like HTTP controllers) depend on Stable Components (like Domain Interfaces).
```typescript
// src/domain/PaymentProcessor.ts (Stable)
export interface IPaymentProcessor {
  process(amount: number): void;
}

// src/infrastructure/StripeAdapter.ts (Volatile)
import { IPaymentProcessor } from '../domain/PaymentProcessor';

export class StripeAdapter implements IPaymentProcessor {
  process(amount: number): void { /* ... */ }
}
```

[DON'T]
Have Stable Components (Policy) depend on Volatile Components (Details), breaking the Dependency Rule.
```typescript
// src/domain/BillingPolicy.ts (Stable)
// DON'T import concrete implementation details into high-level policy!
import { StripeAdapter } from '../infrastructure/StripeAdapter'; 

export class BillingPolicy {
  execute() {
    const stripe = new StripeAdapter();
    stripe.process(100);
  }
}
```