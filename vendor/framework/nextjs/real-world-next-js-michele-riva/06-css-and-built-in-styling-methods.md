# @Domain

These rules apply to any task involving UI styling, CSS architecture, component styling, or configuration of styling preprocessors/compilers (PostCSS, SASS) within a Next.js application. Trigger these behaviors when asked to style React components, create stylesheets, configure CSS modules, or implement styling mechanisms.

# @Vocabulary

*   **Styled JSX**: A CSS-in-JS library built into Next.js that allows writing component-scoped CSS rules using JavaScript. Rules are injected at runtime.
*   **CSS Modules**: A styling method where plain CSS classes are imported into React components as JavaScript objects. It generates unique, locally scoped class names at build time, offering zero runtime cost.
*   **React Hydration Cost**: The performance penalty incurred by CSS-in-JS libraries (like Styled JSX) when CSS rules must be re-generated and injected into the DOM on the client side after the initial HTML load.
*   **PostCSS**: A tool used by Next.js under the hood to compile CSS at build time. Default configurations handle vendor prefixes (Autoprefixer), flexbox bug fixes, and older browser compatibility.
*   **Autoprefixer**: A PostCSS plugin that automatically adds vendor prefixes to CSS rules based on values from "Can I Use".
*   **SASS/SCSS**: CSS preprocessors supported natively by Next.js (upon installation of the `sass` package). **SCSS** (Sassy CSS) extends CSS syntax using brackets/semicolons, whereas **SASS** uses indentation. SCSS is preferred for compatibility.
*   **Selector Composition (`composes`)**: A CSS Modules feature allowing a class to inherit/extend properties from another class (e.g., `composes: button-default;`).
*   **Selector Nesting / `@extend`**: SASS/SCSS features allowing nested rule declarations (using `&`) and class inheritance (`@extend .base-class;`).

# @Objectives

*   Prevent CSS naming collisions by enforcing component-scoped styling (CSS Modules or Styled JSX).
*   Prioritize zero-runtime-cost styling methodologies (CSS Modules, SASS) to maximize performance and allow browser caching of CSS rules.
*   Maintain predictable, scalable CSS architectures by properly segregating global styles from component-local styles.
*   Preserve Next.js default polyfills and vendor-prefixing when customizing PostCSS configurations.
*   Ensure SASS/SCSS integrations are correctly configured and optimized within the Next.js build lifecycle.

# @Guidelines

### 1. General Styling Strategy
*   **Prioritize CSS Modules / SASS over Styled JSX**: The AI MUST favor CSS Modules (with or without SASS) over Styled JSX for production applications. Styled JSX incurs a runtime cost during React hydration and prevents the browser from caching CSS rules.
*   **Global Styles Restriction**: Global CSS files (e.g., `globals.css`) MUST ONLY be imported inside the `pages/_app.js` file. The AI MUST NEVER import standard `.css` files into individual components or other pages.

### 2. Implementing CSS Modules
*   **File Naming**: The AI MUST append `.module.css` or `.module.scss` to the filename to opt-in to CSS Modules (e.g., `Button.module.css`).
*   **Usage**: The AI MUST import the module as a default object and apply classes using object notation (e.g., `import styles from './Button.module.css';` and `className={styles.button}`).
*   **Composition**: The AI SHOULD utilize the `composes` property to share styles between classes within a CSS Module instead of duplicating properties.
*   **Local Globals**: If a specific selector within a CSS Module needs to act globally, the AI MUST wrap it using the `:global` keyword (e.g., `.wrapper :global(.target) { ... }`).

### 3. Implementing SASS/SCSS
*   **Dependency Requirement**: Before attempting to compile `.scss` or `.sass` files, the AI MUST ensure the `sass` npm package is installed.
*   **Syntax Preference**: The AI MUST prefer `.scss` (SCSS) syntax over `.sass` for maximum compatibility with standard CSS.
*   **Advanced Features**: The AI SHOULD utilize SASS features like selector nesting (using `&`) and `@extend` for composing styles, but MUST AVOID excessively deep nesting that produces bloated, unpredictable compiled CSS.
*   **Configuration**: Any custom SASS compiler options (e.g., `outputStyle: 'compressed'`) MUST be placed inside `next.config.js` under the `sassOptions` property.

### 4. Customizing PostCSS
*   **File Creation**: To customize PostCSS, the AI MUST create a `postcss.config.json` file in the project root.
*   **Preserving Defaults**: When overriding PostCSS, the AI MUST include Next.js's required base configuration to prevent breaking Autoprefixer and flexbox bug fixes.
*   **Required Base Configuration**:
    ```json
    {
      "plugins": [
        "postcss-flexbugs-fixes",
        [
          "postcss-preset-env",
          {
            "autoprefixer": { "flexbox": "no-2009" },
            "stage": 3,
            "features": { "custom-properties": false }
          }
        ]
      ]
    }
    ```
    *Note: `custom-properties: false` is required because PostCSS cannot safely compile CSS variables for IE11. If older browser support for variables is needed, the AI MUST recommend SASS variables instead.*

### 5. Implementing Styled JSX (If explicitly requested)
*   **Scoping**: The AI MUST wrap CSS rules within `<style jsx>{` \`...\` `}</style>` directly inside the component's JSX return statement.
*   **Global Overrides Risk**: The AI MUST AVOID using `<style jsx global>` unless absolutely necessary to modify global HTML tags (like `body` or `html`) from within a specific component layout. Warn the user that this can leak styles across the application.

# @Workflow

When requested to style a component or configure styling in Next.js, follow this algorithmic process:

1.  **Determine Styling Methodology**:
    *   If the user does not specify, default to **CSS Modules** (`.module.css`).
    *   If SASS features are requested, check for `sass` package in `package.json`, install if missing, and use `.module.scss`.
    *   If JS-interop is specifically requested and performance is not the primary constraint, use **Styled JSX**.
2.  **Global vs. Local Assessment**:
    *   If styles apply to the whole app (resets, fonts, body margins), place them in `styles/globals.css` and import into `pages/_app.js`.
    *   If styles apply to a component, create a locally scoped file (e.g., `ComponentName.module.css`).
3.  **File Generation**: Generate the CSS/SCSS file with appropriately named, modular classes. Use `composes` or `@extend` to reduce duplication.
4.  **Component Integration**:
    *   Import the `styles` object into the React component.
    *   Map the object keys to the `className` attributes of the JSX elements.
5.  **Build/Config Adjustments**:
    *   If requested to modify browser targets or CSS transpilation, generate `postcss.config.json` ensuring Next.js defaults are retained.
    *   If SASS options are needed, modify `next.config.js` -> `sassOptions`.

# @Examples (Do's and Don'ts)

### CSS Modules

**[DO] Use CSS modules and apply classes via the styles object:**
```javascript
// styles/Button.module.css
.buttonDefault {
  padding: 10px;
  border-radius: 5px;
}
.buttonSuccess {
  composes: buttonDefault;
  background-color: green;
}

// components/Button.js
import styles from '../styles/Button.module.css';

export default function Button({ children }) {
  return <button className={styles.buttonSuccess}>{children}</button>;
}
```

**[DON'T] Use standard CSS imports in components:**
```javascript
// components/Button.js
import '../styles/button.css'; // ANTI-PATTERN: Breaks Next.js build and causes global scope leaks

export default function Button({ children }) {
  return <button className="button-success">{children}</button>;
}
```

### Global Styles

**[DO] Import global CSS only in `pages/_app.js`:**
```javascript
// pages/_app.js
import '../styles/globals.css';

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}
```

**[DON'T] Import global CSS into individual pages or components:**
```javascript
// pages/index.js
import '../styles/globals.css'; // ANTI-PATTERN: Global CSS cannot be imported outside _app.js

export default function Home() { ... }
```

### Styled JSX

**[DO] Use standard `<style jsx>` for component-scoped styles:**
```javascript
export default function Highlight({ text }) {
  return (
    <>
      <span className="highlight">{text}</span>
      <style jsx>{`
        .highlight {
          background: yellow;
          font-weight: bold;
        }
      `}</style>
    </>
  );
}
```

**[DON'T] Use global Styled JSX casually without understanding side effects:**
```javascript
export default function Highlight({ text }) {
  return (
    <>
      <span>{text}</span>
      <style jsx global>{`
        span {
          background: yellow; /* ANTI-PATTERN: This will turn EVERY span on the entire website yellow */
        }
      `}</style>
    </>
  );
}
```

### SASS/SCSS Integration

**[DO] Use SCSS nesting to structure modular rules cleanly:**
```scss
// styles/Alert.module.scss
.alert {
  padding: 15px;
  border-radius: 5px;

  &.success {
    background-color: #d4edda;
    color: #155724;
  }
}
```

**[DON'T] Create deeply nested SCSS that compiles to bloated CSS output:**
```scss
// styles/Bad.module.scss
// ANTI-PATTERN: Causes unpredictable output and massive file sizes
.container {
  div {
    ul {
      li {
        a {
          span {
            color: red;
          }
        }
      }
    }
  }
}
```