@Domain
Trigger these rules when a user requests to style a Next.js application, add UI components, integrate styling libraries, or explicitly mentions integrating Chakra UI, TailwindCSS, or Headless UI into a React/Next.js codebase.

@Vocabulary
- **UI Library/Framework**: A collection of pre-built, reusable code, components, and accessibility rules used to abstract common UI patterns and improve developer productivity.
- **Themeable**: The capability of a UI library to allow customization of its default design language, including color schemes, spacing, and fonts.
- **Chakra UI**: An open-source, modular, accessible, and themeable React component library with built-in TypeScript support.
- **ColorModeScript**: A Chakra UI component injected into the HTML document to apply the user's color mode preference (light/dark) before the page renders, preventing flashing.
- **TailwindCSS**: A utility-first CSS framework that provides low-level utility classes to build custom designs directly in HTML without writing custom CSS.
- **Purge**: The process of automatically removing unused CSS classes from the final production bundle to maintain highly optimized performance (used in TailwindCSS).
- **Headless UI**: Completely unstyled, fully accessible UI components designed to be styled with external tools like TailwindCSS, separating logic and accessibility from visual presentation.
- **classnames (cx)**: A JavaScript utility library for conditionally joining CSS class names together.

@Objectives
- Abstract common UI patterns by utilizing reliable, accessible, and themeable UI libraries rather than building from scratch.
- Ensure proper configuration of light and dark modes according to the specific mechanisms of the chosen UI library.
- Maximize Next.js performance and SEO by purging unused CSS and using built-in Next.js optimizations (e.g., the `Image` component).
- Guarantee accessibility (a11y) across components, particularly concerning routing and interactive UI elements.
- Implement responsive design correctly according to the chosen library's specific paradigms (e.g., mobile-first utility classes or array-based responsive props).

@Guidelines

**General UI & Next.js Guidelines**
- The AI MUST NOT use standard HTML `<img>` tags. The AI MUST ALWAYS use the Next.js built-in `<Image />` component to ensure automatic image optimization, better SEO scores, and to prevent Cumulative Layout Shift (CLS).
- When wrapping UI library components (like Buttons or Boxes) inside a Next.js `<Link>`, the AI MUST ALWAYS use the `passHref` prop on the `<Link>` component and set the child component to render as an anchor tag (e.g., `as="a"`) to ensure accessible routing.

**Chakra UI Specifics**
- When setting up Chakra UI, the AI MUST wrap the application component in `<ChakraProvider>` inside the `pages/_app.js` file.
- To customize the theme, the AI MUST use the `extendTheme` function and pass the result to the `theme` prop of `<ChakraProvider>`.
- To support dark/light mode, the AI MUST inject the `<ColorModeScript>` component inside the `<body>` tag of a custom `pages/_document.js` file, passing the `initialColorMode` config.
- The AI MUST use the `useColorMode` hook to conditionally render text or trigger the `toggleColorMode` function.
- For dynamic color values based on the current theme, the AI MUST use the `useColorModeValue('lightValue', 'darkValue')` hook.
- To implement responsive design in Chakra UI, the AI MUST use array syntax for props (e.g., `width={['100%', '50%', '25%']}`), mapping to mobile, tablet, and desktop breakpoints.

**TailwindCSS Specifics**
- When configuring TailwindCSS, the AI MUST edit `tailwind.config.js` and populate the `purge` array with all paths containing Next.js pages and components (e.g., `['./pages/**/*.{js,jsx}', './components/**/*.{js,jsx}']`) to eliminate unused CSS.
- To support dark mode, the AI MUST set `darkMode: 'class'` in `tailwind.config.js`.
- The AI MUST use the `next-themes` library's `<ThemeProvider attribute="class">` to wrap the application in `pages/_app.js` to manage the dark/light mode class on the HTML tag.
- When creating a theme switcher component using `next-themes` (`useTheme` hook), the AI MUST ensure the component only renders on the client side by returning `null` if `typeof window === 'undefined'`. This prevents server/client hydration mismatches since the theme is stored in `localStorage`.
- The AI MUST write TailwindCSS classes following a mobile-first approach, applying base classes for mobile and using prefixes (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`) for larger screens.

**Headless UI Specifics**
- The AI MUST use Headless UI components to add dynamic, accessible behavior (like Modals, Menus, Dropdowns) to a TailwindCSS project without adding predefined visual styles.
- The AI MUST use the `classnames` library to dynamically construct TailwindCSS class strings based on Headless UI state variables (e.g., using the `{({ active }) => ...}` render prop pattern).
- The AI MUST wrap interactive Headless UI items (like dropdown menus) in the Headless UI `<Transition>` component, utilizing TailwindCSS transition utility classes to control enter and leave animations smoothly.

@Workflow

**Setting up Chakra UI**
1. Install dependencies: `yarn add @chakra-ui/react @emotion/react@^11 @emotion/styled@^11 framer-motion@^4 @chakra-ui/icons`.
2. Create or update `pages/_app.js` to wrap `<Component {...pageProps} />` with `<ChakraProvider>`.
3. Create custom themes using `extendTheme` if required.
4. Create or update `pages/_document.js` to inject `<ColorModeScript>` for persistent dark/light mode.

**Setting up TailwindCSS**
1. Install dependencies: `yarn add -D autoprefixer postcss tailwindcss` and `yarn add next-themes`.
2. Initialize Tailwind: Run `npx tailwindcss init -p` to create configuration files.
3. Configure `tailwind.config.js`: Add paths to the `purge` array and set `darkMode: 'class'`.
4. Update `pages/_app.js`: Import `'tailwindcss/tailwind.css'` and wrap the application with `<ThemeProvider attribute="class">`.
5. Implement responsive and dark mode utility classes across components (e.g., `dark:bg-gray-900`, `sm:w-9/12`).

**Setting up Headless UI**
1. Install dependencies: `yarn add @headlessui/react classnames`.
2. Import required headless components (e.g., `Menu`, `Transition`).
3. Build the structure using Headless UI elements.
4. Pass dynamic states (like `active` or `disabled`) to children.
5. Use `classnames` to combine conditional Tailwind classes.

@Examples (Do's and Don'ts)

**Routing and Links in UI Frameworks**
- [DO] Pass the `href` correctly to Chakra UI components for accessibility.
```jsx
import Link from 'next/link';
import { Button } from '@chakra-ui/react';

export default function Nav() {
  return (
    <Link href="/about" passHref>
      <Button as="a" colorScheme="teal">
        About Us
      </Button>
    </Link>
  );
}
```
- [DON'T] Wrap UI components in a Next.js Link without `passHref` and `as="a"`, breaking a11y and SEO.
```jsx
import Link from 'next/link';
import { Button } from '@chakra-ui/react';

export default function Nav() {
  return (
    <Link href="/about">
      <Button colorScheme="teal">
        About Us
      </Button>
    </Link>
  );
}
```

**Image Optimization**
- [DO] Use Next.js `<Image />` for optimized loading and SEO.
```jsx
import Image from 'next/image';

export default function UserCard({ user }) {
  return (
    <div className="relative">
      <Image 
        src={user.cover_image} 
        alt={user.username} 
        layout="fill"
        objectFit="cover"
      />
    </div>
  );
}
```
- [DON'T] Use native `<img>` tags which cause layout shifts and poor performance.
```jsx
export default function UserCard({ user }) {
  return (
    <div className="relative">
      <img src={user.cover_image} alt={user.username} className="w-full h-96 object-cover" />
    </div>
  );
}
```

**TailwindCSS Client-Side Theme Switcher**
- [DO] Prevent hydration mismatch by checking for the window object.
```jsx
import { useTheme } from 'next-themes';

export default function ThemeSwitch() {
  const { theme, setTheme } = useTheme();

  if (typeof window === 'undefined') return null;

  return (
    <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
      Toggle theme
    </button>
  );
}
```
- [DON'T] Render the theme switcher without verifying the client environment, causing React hydration errors.
```jsx
import { useTheme } from 'next-themes';

export default function ThemeSwitch() {
  const { theme, setTheme } = useTheme();

  return (
    <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
      Toggle theme
    </button>
  );
}
```

**Chakra UI Responsive Design**
- [DO] Use Chakra UI's array syntax for clean, mobile-first responsive design.
```jsx
import { Grid } from '@chakra-ui/react';

export default function Layout() {
  return (
    <Grid gridTemplateColumns={['1fr', 'repeat(2, 1fr)', 'repeat(3, 1fr)']}>
      {/* Content */}
    </Grid>
  );
}
```
- [DON'T] Use hardcoded inline media queries or separate CSS files for basic component responsiveness in Chakra UI.
```jsx
import { Grid } from '@chakra-ui/react';

export default function Layout() {
  return (
    <Grid className="custom-responsive-grid">
      {/* Content */}
    </Grid>
  );
}
```