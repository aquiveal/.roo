@Domain
Trigger these rules when executing JavaScript/TypeScript software engineering tasks, specifically during system architecture design, type definition, code documentation (JSDoc), linting/formatting configuration, pull request generation, and code review processes.

@Vocabulary
- **Static Analysis**: The process of analyzing code without executing it, typically performed by type checkers (e.g., TypeScript) and linters (e.g., ESLint) to prove program properties or catch dangerous constructs.
- **Unrepresentable State**: A system state that is logically impossible to reach because the type system strictly forbids the inputs or combinations of inputs that would cause it.
- **Bike-shedding**: Wasting disproportionate amounts of time discussing trivial, subjective, and easy-to-grasp aspects of a project (like code formatting) instead of focusing on complex, critical tasks.
- **Formatter**: A tool (e.g., Prettier) strictly dedicated to fixing stylistic issues (spacing, quotes) to produce visually consistent code, eliminating subjective formatting debates.
- **Linter**: A tool (e.g., ESLint) that analyzes code to flag bad practices, unreachable statements, or syntactic constructs likely to cause bugs.
- **Monitoring**: Systems observing software in production to detect anomalies, find performance bottlenecks, and validate assumptions about runtime behavior.
- **Alerting**: Automated notifications triggered by monitoring systems when an application's business value is negatively affected.
- **JSDoc**: A markup language used to document JavaScript/TypeScript code directly within the source files via comment blocks.

@Objectives
- Complement and amplify automated testing by utilizing strict type systems to prove program properties and make invalid states unrepresentable.
- Offload repetitive and subjective quality checks to machines via linters and automated formatters to completely eliminate bike-shedding.
- Elevate code reviews to focus exclusively on semantics, logical correctness, and human intent, treating them as collaborative conversations.
- Embed runtime visibility into systems by establishing foundations for monitoring and alerting based on actual business value.
- Ensure all codebase knowledge is explicitly defined through intent-focused, in-code documentation written prior to implementation.

@Guidelines

**Type Systems & State Management**
- The AI MUST use strict type systems (e.g., TypeScript) to enforce logical rules and constrain program state.
- The AI MUST define types that make invalid states unrepresentable. Do not rely on runtime `if/throw` checks for invalid inputs if a strict type definition can catch the error at compile-time via static analysis.
- The AI MUST utilize literal types, union types, and intersection types to strictly narrow the universe of possible inputs (e.g., `status: "in progress" | "done"` instead of `status: string`).
- The AI MUST NOT write automated tests for edge cases that the compiler inherently prevents due to strict typing.

**Code Reviews & Pull Requests**
- When generating a Pull Request (PR) description, the AI MUST include:
  1. A quick summary of the change's intent and related tickets.
  2. An in-depth explanation of the problem addressed and nuances of the implementation.
  3. A detailed description of the written/updated code, emphasizing design choices.
  4. A brief guide on how the changes were validated.
- When performing a code review, the AI MUST NOT read or review code linearly (alphabetically by file). The AI MUST follow the dependency graph and the author's logical train of thought, tracking the execution path from the entry point.
- When suggesting changes during a code review, the AI MUST clearly explain *why* the code needs changing by highlighting the specific advantages of the suggested approach.
- The AI MUST clearly distinguish between blocking requests (required for approval) and non-blocking suggestions.
- The AI MUST treat code reviews as conversations, including highlighting and complimenting elegant design choices.

**Linting & Formatting**
- The AI MUST delegate all stylistic choices to an opinionated formatter (e.g., Prettier). The AI MUST NOT initiate, encourage, or participate in "bike-shedding" regarding tabs, spaces, or quote types.
- The AI MUST resolve all linter (e.g., ESLint) warnings/errors immediately, treating issues like unused variables or unreachable code as logic defects.
- The AI MUST NEVER leave linting or formatting feedback in a code review; assume machines handle this step.

**Monitoring & Performance**
- The AI MUST adhere to Rob Pike's rule: "Don't tune for speed until you've measured." The AI MUST NOT proactively apply speed hacks or premature optimizations without baseline monitoring metrics proving a bottleneck exists.
- The AI MUST instrument critical paths that impact business value with logging and monitoring hooks to facilitate future alerting.

**Documentation**
- The AI MUST write documentation *before* writing the implementation code, using the writing process to structure thoughts and clarify the module's interface ("Writing is thinking").
- The AI MUST focus documentation on the *intent* (Why) of the code, NOT the *inner workings* (How).
- The AI MUST co-locate documentation with the code using JSDoc comment blocks rather than creating disparate, easily-outdated external Markdown wikis.
- The AI MUST explicitly document processes and contribution policies (e.g., adding a JSDoc note that a specific module requires 100% test coverage for all new PRs).

@Workflow
When tasked with implementing a new feature or module, the AI MUST strictly adhere to the following sequence:
1. **Document Intent (JSDoc)**: Write the JSDoc block defining the interface, constraints, and the *why* behind the module before writing any executable code.
2. **Define Strict Types**: Construct TypeScript types/interfaces that strictly constrain the input/output universe, ensuring invalid states are unrepresentable at compile time.
3. **Implement Logic**: Write the code to satisfy the types and documentation, ensuring formatters and linters are adhered to flawlessly. Do not prematurely optimize.
4. **Instrument Monitoring**: Add necessary logging or monitoring hooks to observe business-critical behaviors.
5. **Generate PR Description**: If creating a PR, generate a highly detailed description including summary, nuances, changed code breakdown, and validation steps.

When tasked with reviewing code, the AI MUST follow this sequence:
1. **Trace the Execution Path**: Open files according to the dependency graph, starting at the entry point of the change, ignoring alphabetical file order.
2. **Review Semantics, Not Syntax**: Ignore formatting and stylistic choices. Assume the linter/formatter has run.
3. **Provide Contextual Feedback**: For every requested change, explain the *why* and the benefits. Compliment good code.
4. **Categorize Severity**: Clearly mark which items block approval and which are optional suggestions.

@Examples (Do's and Don'ts)

**Type Systems**
- [DO] Define exact constraints using literal and intersection types.
```typescript
export type OrderItems = { 0: string } & Array<string>;
export type DoneOrder = { status: "done", items: OrderItems };
export const addToDeliveryQueue = (order: DoneOrder) => {
  state.deliveries.push(order);
};
```
- [DON'T] Rely on generic types and runtime checks for invalid states.
```typescript
export const addToDeliveryQueue = (order: any) => {
  if (order.status !== "done") throw new Error("Unfinished order");
  if (!order.items || order.items.length === 0) throw new Error("No items");
  state.deliveries.push(order);
};
```

**Documentation**
- [DO] Document the *intent* using JSDoc before writing code.
```typescript
/**
 * Calculates final pricing for a user's cart to guarantee accurate billing.
 * Ensures promotional rules are applied exclusively to eligible accounts,
 * prioritizing customer retention metrics.
 */
export const applyDiscount = (cart: Cart, user: User): number => { ... }
```
- [DON'T] Document the *mechanics* inside a detached wiki file.
```typescript
// Iterates over the cart array, sums the price property, checks if the user is VIP, then multiplies by 0.8.
export const applyDiscount = (cart: any[], user: any) => { ... }
```

**Code Reviews**
- [DO] Follow logic flow, compliment design, and explain the *why*.
```text
(Reviewing `paymentGateway.ts` first because it's the entry point)
"Great use of the strategy pattern here to handle multiple payment providers! 
**Blocking Change**: However, in `calculateFees`, we are subject to floating-point math errors. Let's switch to using an integer-based library (like `dinero.js`) to prevent rounding errors that could impact revenue."
```
- [DON'T] Review alphabetically and bike-shed over styling.
```text
(Reviewing `apiUtils.ts` first simply because it starts with 'A')
"Please change these double quotes to single quotes. Also, you have an extra blank line here."
```

**Optimization**
- [DO] Rely on monitoring to guide optimization.
```typescript
// Standard, readable array reduction. Optimization deferred until monitoring proves a bottleneck.
const total = items.reduce((sum, item) => sum + item.price, 0);
```
- [DON'T] Apply unmeasured speed hacks.
```typescript
// Premature optimization using bitwise operators and reverse while-loops without metric justification.
let total = 0;
let i = items.length;
while (i--) { total += items[i].price | 0; }
```