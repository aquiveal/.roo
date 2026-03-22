# @Domain
React UI development involving overlays, popups, modal dialogs, tooltips, dropdowns, and any elements requiring `position: absolute`, `position: fixed`, `z-index` manipulation, or escaping content clipping.

# @Vocabulary
- **Stacking Context:** A three-dimensional Z-axis (depth) concept in CSS that defines what sits on top of what. It is an isolated bubble; elements inside cannot break out to overlap elements in a higher parent stacking context, regardless of their own `z-index`.
- **Containing Block:** The element to which a positioned element is relative. For `position: fixed`, it is usually the viewport, unless a parent has a property like `transform`, which creates a new Containing Block.
- **Content Clipping:** The visual truncation of absolutely positioned elements when rendered inside a parent with `overflow: hidden` and `position: relative`.
- **React Portal (`createPortal`):** An API provided by `react-dom` that renders a React Element into a physically different DOM node outside of the current component's DOM hierarchy, while maintaining its place within the React component tree.
- **React Synthetic Events:** React's cross-browser wrapper around native events. These bubble up the *React component tree*, not the physical DOM tree.
- **Native DOM Events:** Standard browser events (e.g., triggered via `addEventListener` or native `<form onSubmit>`). These bubble up the *physical DOM tree*.

# @Objectives
- The AI MUST perfectly position UI overlays (modals, tooltips) so they are never hidden, clipped, or trapped underneath other UI elements.
- The AI MUST correctly diagnose and resolve CSS Stacking Context and overflow traps without resorting to arbitrary `z-index: 9999` hacks.
- The AI MUST utilize React Portals to break elements out of Stacking Context traps.
- The AI MUST preserve the functional integrity of portalled components, ensuring proper Context access, event propagation, form submission, and CSS styling.

# @Guidelines

## CSS Positioning Rules
- When using `position: absolute`, the AI MUST account for the fact that it is positioned relative to the closest positioned parent (not necessarily the screen).
- The AI MUST NOT place `position: absolute` overlays inside containers with `overflow: hidden` and `position: relative`, as this will cause Content Clipping.
- When using `position: fixed` to escape overflow clipping, the AI MUST check parent elements for properties like `transform` (often used in animations). If a parent has `transform`, it forms a new Containing Block, breaking viewport-relative fixed positioning.
- The AI MUST recognize that neither `position: absolute` nor `position: fixed` can escape a Stacking Context trap.

## Stacking Context Diagnostics
- When a user reports that a modal or overlay is rendering underneath another element (e.g., under a sticky header), the AI MUST investigate the parents for Stacking Context triggers.
- The AI MUST treat the following CSS rules as Stacking Context triggers:
  - `position: relative` or `position: absolute` combined with `z-index` (other than `auto`).
  - `position: sticky` or `position: fixed`.
  - `transform` (e.g., `translate`).
  - `z-index` on Flex or Grid children.
- If a Stacking Context trap is identified, the AI MUST NOT attempt to fix it by merely increasing the `z-index` of the trapped child element. It MUST recommend React Portals.

## React Portal Implementation Constraints
- When rendering modals, dialogs, or global tooltips deeply nested in the component tree, the AI MUST use `createPortal(reactElement, domNode)` from the `react-dom` package.
- **React Lifecycle & State Context:** The AI MUST treat the portalled component as part of the original React tree. It will re-render when the parent re-renders, unmount when the parent unmounts, and retain access to React Context providers wrapping the parent.
- **Synthetic Event Bubbling:** The AI MUST rely on React's `onClick` (or other Synthetic Events) on the parent component to intercept events from the portalled child, as React events bubble through the React tree, bypassing the physical DOM structure.
- **Native Event Isolation:** The AI MUST NOT use native DOM event listeners (e.g., `element.addEventListener('click')`) on the parent container to catch events from the portalled child.
- **DOM Traversal Isolation:** The AI MUST NOT use `.parentElement` or similar DOM traversal properties to find the React parent of a portalled component.
- **CSS Isolation:** The AI MUST NOT use CSS descendant selectors (e.g., `.parent-class .modal-class`) to style a portalled component, because the modal no longer physically resides inside `.parent-class` in the DOM.
- **Form Submission Isolation:** The AI MUST NOT wrap a portalled trigger in a `<form>` tag expecting the submit button inside the portal to trigger an `onSubmit` event on that form. Native form submission relies on the DOM tree. If a form is needed in a portal, the `<form>` tag MUST be placed *inside* the portalled component itself.

# @Workflow
When tasked with creating an overlay, modal, or tooltip, or fixing a z-index/clipping bug, the AI MUST follow this exact sequence:

1. **Analyze the UI Requirement:** Determine if the element is an overlay (modal, tooltip, dropdown) that must visually break out of its container.
2. **Evaluate CSS Traps:** Inspect the parent hierarchy for `overflow: hidden`, `position: sticky/fixed`, `transform`, or `z-index` values. 
3. **Select Implementation Strategy:**
   - If no Stacking Context traps exist and it's a simple relative tooltip, use `position: absolute`.
   - If it must position relative to the viewport and no `transform` parents exist, consider `position: fixed`.
   - If trapped by a Stacking Context, or if building a global Modal Dialog, default to React Portals.
4. **Implement Portal (if selected):**
   - Import `createPortal` from `react-dom`.
   - Identify or create a target DOM node (e.g., `document.getElementById('root')` or `document.body`).
   - Wrap the overlay JSX in `createPortal(<Overlay />, targetNode)`.
5. **Verify Teleportation Rules:**
   - Ensure no CSS cascades are broken due to the DOM shift.
   - Ensure any `<form>` tags fully encapsulate their inputs and submit buttons *within* the portalled JSX.
   - Validate that React Contexts and state variables used within the portal are sourced correctly from the React parent.

# @Examples (Do's and Don'ts)

## Applying Portals for Modals
- **[DON'T]** Render a modal deep inside a main content area that has transitions or positioned elements, as it will get trapped by Stacking Contexts.
```jsx
// Incorrect: Trapped in Stacking Context caused by "transform"
const App = () => (
  <div className="main" style={{ transform: 'translate(0, 0)' }}>
    <button onClick={open}>Show Modal</button>
    {isOpen && <div className="modal" style={{ position: 'fixed', zIndex: 9999 }}>Trapped!</div>}
  </div>
);
```
- **[DO]** Use `createPortal` to teleport the modal to the root of the document, escaping the Stacking Context trap.
```jsx
// Correct: Escapes Stacking Context using a Portal
import { createPortal } from 'react-dom';

const App = () => (
  <div className="main" style={{ transform: 'translate(0, 0)' }}>
    <button onClick={open}>Show Modal</button>
    {isOpen && createPortal(
      <div className="modal">Safe!</div>,
      document.body // or document.getElementById('root')
    )}
  </div>
);
```

## Styling Portalled Components
- **[DON'T]** Rely on the parent container's CSS class to style the portalled child.
```css
/* Incorrect: Will fail because .modal is teleported outside of .main */
.main .modal {
  background: red;
}
```
- **[DO]** Apply standalone classes to the portalled component, or pass a unified theme class directly to the portalled element.
```css
/* Correct: Styles the modal independently of its React parent */
.modal {
  background: red;
}
```

## Handling Form Submissions in Portals
- **[DON'T]** Wrap the React parent in a `<form>` if the submit buttons are inside the portal. The native `submit` event will not bubble across the DOM gap.
```jsx
// Incorrect: Form submission will fail
const App = () => (
  <form onSubmit={handleSubmit}>
    <input name="field1" />
    {isOpen && createPortal(
      <Modal>
        <button type="submit">Submit Form</button> {/* Will NOT trigger handleSubmit! */}
      </Modal>,
      document.body
    )}
  </form>
);
```
- **[DO]** Place the `<form>` tag completely inside the portalled component.
```jsx
// Correct: Form submission works via DOM tree
const App = () => (
  <div className="app">
    {isOpen && createPortal(
      <Modal>
        <form onSubmit={handleSubmit}>
          <input name="field1" />
          <button type="submit">Submit Form</button>
        </form>
      </Modal>,
      document.body
    )}
  </div>
);
```