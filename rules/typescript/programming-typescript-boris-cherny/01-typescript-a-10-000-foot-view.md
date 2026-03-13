# @Domain
This rule file is activated whenever the AI is requested to initialize, configure, architect, or write foundational TypeScript projects, specifically focusing on compiler configuration (`tsconfig.json`), linting setup (`tslint.json`), project scaffolding, and fundamental type system interactions (type inference vs. explicit annotation).

# @Vocabulary
- **Compiler**: A program that parses text into an Abstract Syntax Tree (AST) and transforms it into a lower-level representation (bytecode or, in TypeScript's case, JavaScript).
- **Typechecker**: A special program executing between the AST generation and code emission phases that verifies code type safety.
- **Type System**: A set of rules a typechecker uses to assign types to a program.
- **Annotations**: Explicit syntax used to signal a type to the typechecker, taking the form `value: type`.
- **Inferred Types**: Types automatically deduced by the typechecker without explicit annotations.
- **Dynamically Bound**: Types are determined at runtime (JavaScript behavior).
- **Statically Bound**: Types are determined at compile time (TypeScript behavior).
- **Gradual Typing**: A type system that performs best when all types are known at compile time, but does not strictly require every type to be known to compile (though 100% coverage is the mandated target).
- **Weakly Typed / Implicit Conversion**: Language behavior where invalid operations automatically trigger type conversions to force execution (JavaScript behavior).
- **Self-hosting Compiler**: A compiler that compiles itself (e.g., the TypeScript Compiler, TSC).

# @Objectives
- Enforce a strict separation between type-level validation and value-level runtime execution, recognizing that types never affect the generated JavaScript output.
- Achieve 100% type coverage across the codebase to ensure the typechecker can statically analyze all paths before runtime.
- Minimize explicit type annotations by maximizing reliance on TypeScript's powerful type inference engine.
- Eliminate implicit type conversions entirely; mandate explicit, intentional type casting or conversion methods.
- Standardize project scaffolding strictly according to the defined directory structures, `tsconfig.json`, and `tslint.json` configurations.

# @Guidelines
- **Type Emission Constraint**: The AI MUST recognize that TypeScript types are erased during compilation and NEVER affect the generated JavaScript output. Use types strictly for compile-time safety.
- **Inference Over Annotation**: The AI MUST let TypeScript infer as many types as possible. Explicit type annotations (`: type`) MUST ONLY be used when inference falls short or when explicitly requested.
- **Total Type Coverage**: The AI MUST aim for 100% type coverage in all non-legacy code. Gradual typing is ONLY permitted when actively migrating legacy untyped JavaScript to TypeScript.
- **No Implicit Conversions**: The AI MUST NEVER rely on implicit type conversions (e.g., attempting to add a number and an array). If type conversion is necessary, the AI MUST explicitly convert the types (e.g., using `.toString()`).
- **Strict Mode Mandate**: The AI MUST ALWAYS enable `strict: true` in `tsconfig.json` to enforce maximum type safety.
- **Project Configuration Enforcement**: 
  - The AI MUST configure `tsconfig.json` with the following baseline fields: `include`, `lib`, `module`, `outDir`, `sourceMap`, `strict`, and `target`.
  - The AI MUST configure `tslint.json` with `"defaultSeverity": "error"`, extend `"tslint:recommended"`, and enforce the specific stylistic choices: `"semicolon": false` and `"trailing-comma": false`.
- **Directory Structure Enforcement**: The AI MUST organize project files by placing TypeScript source code entirely within a `src/` directory and directing compiler output to a `dist/` directory.

# @Workflow
When tasked with setting up or modifying a new TypeScript project, the AI MUST follow this rigid algorithmic process:
1. **Initialize Dependencies**: Initialize an NPM project and install `typescript`, `tslint`, and `@types/node` as development dependencies (`--save-dev`).
2. **Configure Compiler**: Create a `tsconfig.json` file in the root directory. Populate it with `compilerOptions` containing `"lib": ["es2015"]`, `"module": "commonjs"`, `"outDir": "dist"`, `"sourceMap": true`, `"strict": true`, and `"target": "es2015"`. Set the `"include"` array to `["src"]`.
3. **Configure Linter**: Create a `tslint.json` file in the root directory. Extend `"tslint:recommended"`, set `"defaultSeverity": "error"`, and define `"rules"` to explicitly disable semicolons (`"semicolon": false`) and trailing commas (`"trailing-comma": false`).
4. **Scaffold Directories**: Create a `src/` directory. Create the primary entry point file at `src/index.ts`.
5. **Write Implementation**: Write modern TypeScript inside `src/` using `esnext` features. Rely entirely on type inference for variable declarations; omit explicit annotations unless TypeScript cannot infer the type.
6. **Explicit Conversions**: Scan the implementation for any cross-type operations (e.g., concatenating strings and numbers). Replace any reliance on JavaScript's implicit conversion with explicit method calls (e.g., `.toString()`).
7. **Compile and Execute**: Verify the compilation process by simulating or providing instructions to run `./node_modules/.bin/tsc`, followed by executing the output with `node ./dist/index.js` (or utilizing `ts-node` / `typescript-node-starter` as allowed shortcuts).

# @Examples (Do's and Don'ts)

### Type Inference
- **[DO]** Let TypeScript infer the type automatically from the assigned value:
  ```typescript
  let a = 1
  let b = 'hello'
  let c = [true, false]
  ```
- **[DON'T]** Clutter the code with redundant explicit type annotations:
  ```typescript
  let a: number = 1
  let b: string = 'hello'
  let c: boolean[] = [true, false]
  ```

### Type Conversion
- **[DO]** Convert types explicitly before attempting operations across differing types:
  ```typescript
  let result = (3).toString() + [1].toString()
  ```
- **[DON'T]** Rely on JavaScript's weakly-typed implicit conversion, which TypeScript statically rejects:
  ```typescript
  let result = 3 + [1] // Error TS2365: Operator '+' cannot be applied to types '3' and 'number[]'.
  ```

### Compiler Configuration (`tsconfig.json`)
- **[DO]** Structure the `tsconfig.json` to enforce strictness and explicit input/output directories:
  ```json
  {
    "compilerOptions": {
      "lib": ["es2015"],
      "module": "commonjs",
      "outDir": "dist",
      "sourceMap": true,
      "strict": true,
      "target": "es2015"
    },
    "include": [
      "src"
    ]
  }
  ```
- **[DON'T]** Omit the `strict` flag or mix input/output directories:
  ```json
  {
    "compilerOptions": {
      "target": "es5"
    }
  }
  ```

### Linter Configuration (`tslint.json`)
- **[DO]** Enforce the specific style guidelines derived from the text (no semicolons, no trailing commas):
  ```json
  {
    "defaultSeverity": "error",
    "extends": [
      "tslint:recommended"
    ],
    "rules": {
      "semicolon": false,
      "trailing-comma": false
    }
  }
  ```
- **[DON'T]** Leave formatting open to interpretation or default to allowing semicolons when explicitly forbidden by the project style.