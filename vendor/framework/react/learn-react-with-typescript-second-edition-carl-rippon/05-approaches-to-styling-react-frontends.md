@Domain
React frontend styling tasks, including the creation, refactoring, and maintenance of UI components using Plain CSS, CSS Modules, CSS-in-JS (Emotion), Tailwind CSS, and SVGs within a React/TypeScript codebase.

@Vocabulary
- BEM (Block, Element, Modifier): A CSS naming convention used to manually scope CSS class names and prevent clashes when using plain globally-scoped CSS.
- CSS Modules: An approach where CSS files are named with a `.module.css` extension, allowing Webpack to automatically generate unique, scoped class names at build time.
- CSS-in-JS: A styling approach (e.g., using Emotion) where CSS is written directly within JavaScript/TypeScript files, often allowing for dynamic styling based on component state/props at runtime.
- Tagged Template Literal: A special JavaScript string syntax (e.g., `` css`...` ``) used by CSS-in-JS libraries to parse and apply CSS styles.
- Utility-first CSS: A methodology (used by Tailwind CSS) utilizing low-level, highly reusable, prebuilt CSS classes (e.g., `bg-white`, `px-4`) directly within markup.
- PostCSS: A tool that transforms CSS using JavaScript; Tailwind runs as a plugin within it to generate only the utility classes actually used in the application.
- SVG (Scalable Vector Graphics): A vector image format based on mathematical formulas that scales without distortion.
- ReactComponent: A named import feature in Webpack/Create React App that allows an SVG file to be imported and rendered directly as a React component.

@Objectives
- Eliminate CSS class name clashes globally by applying the correct scoping methodology (BEM, CSS Modules, or CSS-in-JS).
- Optimize Tailwind CSS usage by ensuring utility classes are statically analyzable at build time to prevent aggressive purging.
- Seamlessly inject dynamic and conditional styles based on component state/props using the appropriate syntax for the chosen styling approach.
- Render SVG assets perfectly and without distortion by applying the correct import strategy (image path vs. inline React component).

@Guidelines
- Plain CSS Constraints:
  - When utilizing plain CSS (`.css` files), the AI MUST anticipate global scope clashes (e.g., two components using `.container`).
  - To mitigate clashes in plain CSS, the AI MUST enforce the BEM (Block, Element, Modifier) naming convention (e.g., `Alert__container`).
  - The AI MUST recognize that Webpack bundles all plain CSS without pruning redundant unused classes.
- CSS Modules Constraints:
  - The AI MUST name files using the `.module.css` extension.
  - The AI MUST use camelCase for class names inside the CSS file (e.g., `.headerIcon` instead of `.header-icon`) to allow safe and clean dot-notation property access in JavaScript (`styles.headerIcon`).
  - The AI MUST import the module as an object: `import styles from './Component.module.css';`.
  - The AI MUST apply multiple scoped classes or conditional classes using template literals (e.g., `` className={`${styles.container} ${styles[type]}`} ``).
- CSS-in-JS (Emotion) Constraints:
  - The AI MUST inject the specific pragma `/** @jsxImportSource @emotion/react */` at the absolute top of the file to instruct the transpiler to use Emotion's JSX function.
  - The AI MUST import the `css` function: `import { css } from '@emotion/react';`.
  - The AI MUST apply styles using the `css` prop and tagged template literals instead of `className`.
  - The AI MUST embed conditional logic directly inside the tagged template literal using JavaScript string interpolation (e.g., `color: ${type === 'warning' ? 'red' : 'blue'};`).
- Tailwind CSS Constraints:
  - The AI MUST apply styles exclusively via utility classes within the `className` attribute.
  - The AI MUST use Tailwind's spacing scale (e.g., `px-4` for 1rem/16px padding) and built-in color palettes.
  - The AI MUST NEVER dynamically construct Tailwind class names using partial string concatenation (e.g., `bg-${color}-500`). Tailwind determines used classes statically at build time; dynamic concatenation will result in the class being purged and the style breaking.
  - For conditional Tailwind styling, the AI MUST use full class names in ternary operators (e.g., `type === 'warning' ? 'bg-amber-50' : 'bg-teal-50'`).
- SVG Integration Constraints:
  - When rendering an SVG inside an `img` tag, the AI MUST import the default path: `import logo from './logo.svg';` and use it as `src={logo}`.
  - When rendering an SVG inline (to allow CSS manipulation like fill/stroke), the AI MUST import it as a React component using the named export: `import { ReactComponent as Icon } from './icon.svg';` and render it as `<Icon />`.

@Workflow
1. Identify the chosen styling approach dictated by the user, the existing file extension, or the project setup (`.css`, `.module.css`, Emotion, Tailwind).
2. For Plain CSS: Create the file, define classes using BEM, import it normally, and apply strings to `className`.
3. For CSS Modules: Create `.module.css`, define camelCase classes, import as `styles`, and apply via `className={styles.className}`.
4. For CSS-in-JS (Emotion): Add the `@jsxImportSource` pragma, import `css`, and write tagged template literals directly into the `css` prop on the target elements, utilizing string interpolation for dynamic states.
5. For Tailwind CSS: Construct the `className` string using full, statically analyzable utility classes. Use ternaries providing complete class name strings for conditional styling.
6. For SVGs: Determine if the SVG needs styling control (use `ReactComponent` import) or acts as a static image (use default path import), and implement accordingly.

@Examples (Do's and Don'ts)

Plain CSS (Global Scope Mitigation)
[DO]
```tsx
import './Alert.css';
export function Alert() {
  return <div className="Alert__container">Hello</div>;
}
```
[DON'T] (Avoid generic class names that will clash globally)
```tsx
import './Alert.css';
export function Alert() {
  return <div className="container">Hello</div>;
}
```

CSS Modules (Naming Convention)
[DO]
```css
/* Alert.module.css */
.headerIcon { width: 30px; }
```
```tsx
import styles from './Alert.module.css';
<span className={styles.headerIcon}>⚠</span>
```
[DON'T] (Using kebab-case forces ugly bracket notation)
```css
/* Alert.module.css */
.header-icon { width: 30px; }
```
```tsx
import styles from './Alert.module.css';
<span className={styles['header-icon']}>⚠</span>
```

CSS-in-JS (Emotion setup and conditionals)
[DO]
```tsx
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';

export function Button({ isPrimary }) {
  return (
    <button
      css={css`
        border-radius: 4px;
        background-color: ${isPrimary ? 'blue' : 'gray'};
      `}
    >
      Click Me
    </button>
  );
}
```
[DON'T] (Missing pragma, causing `css` prop to be ignored by standard React)
```tsx
import { css } from '@emotion/react';

export function Button({ isPrimary }) {
  return <button css={css`border-radius: 4px;`}>Click</button>; // Will not work
}
```

Tailwind CSS (Conditional/Dynamic Classes)
[DO]
```tsx
export function Badge({ color }) {
  return (
    <span className={`px-2 py-1 ${color === 'red' ? 'bg-red-500' : 'bg-blue-500'}`}>
      Badge
    </span>
  );
}
```
[DON'T] (String concatenation hides the class from the PurgeCSS compiler)
```tsx
export function Badge({ color }) {
  // Tailwind will not bundle 'bg-red-500' because the literal string isn't found
  return (
    <span className={`px-2 py-1 bg-${color}-500`}>
      Badge
    </span>
  );
}
```

SVG Imports
[DO] (Component import for inline rendering)
```tsx
import { ReactComponent as WarningIcon } from './warning.svg';

export function Alert() {
  return <WarningIcon className="w-5 h-5 fill-amber-900" />;
}
```
[DON'T] (Trying to render a path string as a component)
```tsx
import WarningIcon from './warning.svg'; // Imports a string path

export function Alert() {
  return <WarningIcon />; // React will throw an error
}
```