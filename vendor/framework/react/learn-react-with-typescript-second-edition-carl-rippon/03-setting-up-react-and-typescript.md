@Domain
These rules MUST be triggered whenever the AI is tasked with initializing a React and TypeScript project, configuring Webpack or Babel for a React/TypeScript ecosystem, setting up linting (ESLint) and formatting (Prettier) in a React project, or strongly typing React component props and states.

@Vocabulary
- **Webpack**: A module bundler that aggregates JavaScript source code files, CSS, and images into a single bundle. It can run tools like Babel during the bundling process.
- **Babel**: A transpilation tool used to convert JSX and TypeScript into browser-compatible JavaScript.
- **package.json**: The project configuration file defining the project name, description, npm scripts, and dependent npm modules.
- **tsconfig.json**: The configuration file for the TypeScript compiler.
- **Type Assertion**: The `as` keyword in TypeScript used to explicitly inform the compiler of a specific type (e.g., `document.getElementById('root') as HTMLElement`).
- **createRoot**: A React DOM client function that takes a DOM element and returns a variable to display a React component tree.
- **babel-loader**: A Webpack plugin that allows Babel to transpile React and TypeScript code during the Webpack build process.
- **html-webpack-plugin**: A Webpack plugin used to generate an `index.html` file or use a template to automatically inject the React app's JavaScript bundle.
- **Create React App (CRA)**: A scaffolding tool for rapidly creating React projects with a pre-configured build pipeline.
- **npx**: A Node.js tool that allows npm packages (like `create-react-app`) to be installed temporarily and executed.
- **ESLint**: A linting tool configured to check React and TypeScript code for potential problems.
- **Prettier**: An automatic code formatting tool that ensures consistent code readability.
- **Props**: An object parameter passed into a React component. In TypeScript, this is strongly typed using a `type` alias or `interface`.
- **React.ReactNode**: A specialized TypeScript type provided by React used to type the `children` prop, allowing it to accept strings, null, and JSX elements.
- **Generic Argument**: A type parameter passed to a generic function (e.g., `useState<boolean>()`) to explicitly define the type when it cannot be accurately inferred.
- **React DevTools**: A browser extension used to inspect the React component tree, track state/props, highlight re-renders, and profile component performance.

@Objectives
- Safely and accurately scaffold a React and TypeScript project using either a manual Webpack/Babel configuration or Create React App.
- Strictly separate source code from configuration files.
- Ensure the TypeScript compiler, Babel, and Webpack are perfectly synchronized to handle `.ts` and `.tsx` files without compilation conflicts.
- Automate code quality by integrating Prettier with ESLint to manage formatting rules without clashing.
- Guarantee robust type safety in React components by strictly typing `props` and explicitly typing state variables where inference falls short.

@Guidelines
- **Folder Structure**: The AI MUST place all application source code inside a `src` folder. Project configuration files (`package.json`, `tsconfig.json`, `.babelrc.json`, Webpack configs, etc.) MUST be placed at the root of the project.
- **TypeScript Configuration**: 
  - If using Babel for transpilation, the AI MUST set `"noEmit": true` in `tsconfig.json` to prevent the TypeScript compiler from producing JavaScript files.
  - The AI MUST set `"allowSyntheticDefaultImports": true` and `"esModuleInterop": true` in `tsconfig.json` to enable default imports for React (e.g., `import React from 'react'`).
  - The AI MUST set `"jsx": "react"` in `tsconfig.json`.
- **React Entry Point**: 
  - The entry file MUST be named `index.tsx` so Babel and TypeScript recognize it as containing JSX.
  - The AI MUST use `createRoot` and apply a type assertion (`as HTMLElement`) when selecting the root DOM element to prevent `HTMLElement | null` inference errors.
- **Babel Configuration**:
  - The AI MUST configure `.babelrc.json` with the following presets: `@babel/preset-env`, `@babel/preset-react`, and `@babel/preset-typescript`.
  - The AI MUST include `@babel/plugin-transform-runtime` with `"regenerator": true` to support async/await syntax.
- **Webpack Configuration**:
  - The AI MUST use `ts-node` to write Webpack configuration in TypeScript (`webpack.dev.config.ts`).
  - The AI MUST intersect Webpack's `Configuration` type with the `webpack-dev-server` `Configuration` type to achieve proper typing for the config object.
  - The AI MUST configure `babel-loader` to process `/\.(ts|js)x?$/i` file extensions.
  - The AI MUST configure `resolve.extensions` to include `['.tsx', '.ts', '.js']`.
  - The AI MUST configure the development server (`devServer`) with `historyApiFallback: true` to support deep linking and client-side routing.
- **Prettier & ESLint Integration**:
  - The AI MUST install `prettier`, `eslint-config-prettier`, and `eslint-plugin-prettier` as development dependencies.
  - The AI MUST update the `eslintConfig` section in `package.json` to extend `plugin:prettier/recommended` to allow Prettier to override conflicting ESLint rules.
  - The AI MUST create a `.prettierrc.json` defining exact stylistic rules (e.g., `printWidth`, `singleQuote`, `semi`, `tabWidth`, `trailingComma`, `endOfLine`).
- **Typing Component Props**:
  - The AI MUST define a custom type (typically named `Props`) using a `type` alias (or `interface`) directly above the component definition.
  - The AI MUST explicitly type the `children` prop using `React.ReactNode`.
  - The AI MUST destructure the props in the component signature and apply the defined type (e.g., `({ heading, children }: Props)`).
- **Typing Component State**:
  - The AI MUST rely on TypeScript's type inference when initializing state with a defined default value (e.g., `useState(true)` infers `boolean`).
  - The AI MUST explicitly define the state type using a generic argument on the `useState` hook when no default value is provided or when the initial value is `null`/`undefined` (e.g., `useState<boolean>()`).

@Workflow
1. **Project Scaffold**: Determine if the project is manual (Webpack) or automatic (CRA).
   - *Manual*: Generate `src/index.html` with a `<div id="root"></div>`. Generate `package.json`. Install TypeScript, React, ReactDOM, Babel, Webpack, and their respective types/loaders. Generate `tsconfig.json`, `.babelrc.json`, and `webpack.dev.config.ts`.
   - *Automatic*: Use `npx create-react-app <name> --template typescript`.
2. **Linting and Formatting Configuration**:
   - Install Prettier and ESLint integration packages (`eslint-config-prettier`, `eslint-plugin-prettier`).
   - Create `.prettierrc.json` with strict formatting parameters.
   - Modify the `eslintConfig` in `package.json` to append the Prettier plugin.
3. **Component Creation**:
   - Create the component file with a `.tsx` extension.
   - Define a `Props` type alias mapping all expected properties and optional properties (using `?`).
   - Write the function component, destructuring props and applying the `: Props` annotation.
4. **State Implementation**:
   - Analyze required states. Implement `useState`.
   - Validate if the initial value adequately infers the type. If it evaluates to `undefined` or `any`, inject a generic type argument (`useState<Type>()`).

@Examples (Do's and Don'ts)

[DO] Use type assertion for the React root element to satisfy TypeScript's strict null checks.
```tsx
import { createRoot } from 'react-dom/client';

const root = createRoot(
  document.getElementById('root') as HTMLElement
);
```

[DON'T] Leave the root element un-asserted, causing potential `null` type errors.
```tsx
const root = createRoot(document.getElementById('root')); // Error: Argument of type 'HTMLElement | null' is not assignable
```

[DO] Explicitly define a `Props` type alias and type the destructured parameters.
```tsx
type Props = {
  heading: string;
  closable?: boolean;
  children: React.ReactNode;
};

export function Alert({ heading, closable, children }: Props) {
  return (
    <div>
      <h1>{heading}</h1>
      {children}
    </div>
  );
}
```

[DON'T] Leave props untyped, falling back to the `any` type.
```tsx
export function Alert({ heading, closable, children }) { // Error: implicit 'any'
  // ...
}
```

[DO] Use generic arguments for `useState` when the initial value is omitted or `null`.
```tsx
const [visible, setVisible] = useState<boolean>();
const [email, setEmail] = useState<string | null>(null);
```

[DON'T] Omit the generic argument when no initial value is provided, causing it to infer `undefined`.
```tsx
const [visible, setVisible] = useState(); // Infers undefined, preventing you from safely storing a boolean.
```

[DO] Configure ESLint to defer formatting to Prettier in `package.json`.
```json
"eslintConfig": {
  "extends": [
    "react-app",
    "react-app/jest",
    "plugin:prettier/recommended"
  ]
}
```