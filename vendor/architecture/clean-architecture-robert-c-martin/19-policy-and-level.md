# @Domain
This rule set activates whenever the AI is tasked with architectural design, component structuring, module organization, dependency management, refactoring of data flows, or defining the relationships between business logic and input/output (I/O) mechanisms. It strictly governs how the AI must manage source code dependencies, imports (`import`, `using`, `require`), and component boundaries.

# @Vocabulary
- **Policy**: A detailed description of the rules by which inputs are transformed into outputs. All computer programs are aggregates of policy statements.
- **Level**: The strict measurement of a policy's distance from the inputs and outputs of the system. The farther a policy is from both inputs and outputs, the higher its level.
- **Low-Level Policy**: Policies that manage or exist close to the inputs and outputs. These change frequently, with urgency, but for less substantively important reasons.
- **High-Level Policy**: Policies that are furthest from inputs and outputs. These change less frequently and for more substantively important reasons.
- **Source Code / Compile-Time Dependency**: The static dependencies required for the compiler to function (e.g., `import`, `using`, `require` statements).
- **Directed Acyclic Graph (DAG)**: The required structural formation of components, where nodes are components containing policies at the same level, and directed edges are the dependencies connecting components at different levels without forming loops.
- **Plugin Architecture**: A structural pattern where lower-level components are designed to plug into higher-level components, rendering the higher-level components entirely ignorant of the lower-level implementations.

# @Objectives
- Treat all software behaviors as statements of policy and categorize them by their reasons and rates of change.
- Decouple source code dependencies from the direction of data flow.
- Ensure that all source code dependencies point strictly in the direction of higher-level policies.
- Protect high-level policies from the frequent and urgent changes associated with low-level I/O details.
- Maximize the reusability of high-level policies across different contexts by ensuring they carry no dependencies on specific I/O devices or low-level mechanisms.

# @Guidelines
- **Calculate Level by I/O Distance**: The AI MUST determine the "Level" of any component strictly by measuring its conceptual distance from the system's inputs and outputs.
- **Enforce Upward Dependency**: The AI MUST ensure that low-level components (closer to I/O) always depend on high-level components (farther from I/O). High-level components MUST NEVER depend on low-level components.
- **Decouple Dependency from Data Flow**: If data flows from a high-level component to a low-level component, the AI MUST NOT allow a source code dependency to follow that data flow. The AI MUST invert the dependency using polymorphic interfaces.
- **Group by Change (SRP/CCP)**: The AI MUST group policies that change for the same reasons and at the same times into the same component.
- **Separate by Change**: The AI MUST separate policies that change for different reasons or at different times into different components at different levels.
- **Treat Low-Level Components as Plugins**: The AI MUST design I/O devices, formatting logic, and input validation as low-level plugins that implement interfaces defined by the high-level policy.
- **Mitigate Change Impact**: The AI MUST construct the architecture such that trivial but urgent changes at the lowest levels of the system have zero impact on the higher, more important levels.
- **Apply Component Principles**: The AI MUST integrate the Single Responsibility Principle, Open-Closed Principle, Common Closure Principle, Dependency Inversion Principle, Stable Dependencies Principle, and Stable Abstractions Principle when defining policy components and their relationships.

# @Workflow
1. **Policy Identification**: When analyzing a system or feature, identify all distinct statements of policy (e.g., business rules, report formatting, input validation, I/O handling).
2. **Level Assignment**: For each identified policy, map its distance from the physical or abstract inputs and outputs. Assign a "Level" designation (Highest = furthest from I/O).
3. **Volatility Categorization**: Determine the expected frequency, urgency, and underlying reason for change for each policy.
4. **Component Regrouping**: Group policies into components based on matching levels and matching change volatility.
5. **Dependency Mapping**: Draw or define the source code dependencies (imports/requires) between the components.
6. **Dependency Direction Check**: Verify that every dependency points from a lower-level component to a higher-level component.
7. **Dependency Inversion**: If step 6 fails (e.g., a high-level policy directly calls a low-level I/O write function), introduce a boundary interface declared within the high-level component and implemented by the low-level component.
8. **DAG Verification**: Ensure the resulting component dependency map forms a Directed Acyclic Graph.

# @Examples (Do's and Don'ts)

**[DON'T]**
Couple source code dependency directly to data flow, forcing a high-level policy to depend on a low-level I/O policy.

```javascript
// Anti-pattern: High-level encryption policy depends on low-level I/O.
import { readChar } from './ConsoleReader';
import { writeChar } from './ConsoleWriter';

export function encrypt() {
  while (true) {
    const char = readChar(); // High-level depends on low-level input
    const translated = translate(char);
    writeChar(translated); // High-level depends on low-level output
  }
}
```

**[DO]**
Decouple source code dependency from data flow by defining interfaces at the high level, forcing the low-level I/O mechanisms to act as plugins. All dependencies point inward toward the high-level policy.

```javascript
// High-Level Component (Encryption Policy)
// Contains the interfaces, isolating it from I/O details.
export interface CharReader {
  readChar(): string;
}

export interface CharWriter {
  writeChar(c: string): void;
}

export class Encryptor {
  private reader: CharReader;
  private writer: CharWriter;

  constructor(reader: CharReader, writer: CharWriter) {
    this.reader = reader;
    this.writer = writer;
  }

  public encrypt(): void {
    while (true) {
      const char = this.reader.readChar();
      const translated = this.translate(char);
      this.writer.writeChar(translated);
    }
  }

  private translate(c: string): string {
    // Encryption business rule logic
    return c; 
  }
}

// Low-Level Component (I/O Policy)
// Depends ON the High-Level Component's interfaces.
import { CharReader, CharWriter } from './Encryptor';

export class ConsoleReader implements CharReader {
  public readChar(): string {
    // low-level console read logic
  }
}

export class ConsoleWriter implements CharWriter {
  public writeChar(c: string): void {
    // low-level console write logic
  }
}
```