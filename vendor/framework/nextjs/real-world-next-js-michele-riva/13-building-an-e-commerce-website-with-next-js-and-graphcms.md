# @Domain
These rules MUST be triggered when the AI is tasked with building, modifying, or architecting an e-commerce website or storefront using Next.js, explicitly when integrating with a headless CMS (specifically GraphCMS/Hygraph), implementing global shopping cart state via React Context, querying via GraphQL, or processing payments via Stripe Checkout.

# @Vocabulary
- **Headless CMS**: A backend-only content management system built as a content repository that makes content accessible via a REST or GraphQL API for display on any device.
- **GraphCMS**: An API-first headless CMS used to manage product inventory, categories, and content via GraphQL.
- **GraphQLClient**: A lightweight library (`graphql-request`) used to establish a connection with the GraphCMS endpoint using authorization headers.
- **Incremental Static Regeneration (ISR)**: A Next.js rendering strategy using `getStaticProps` with a `revalidate` property to update static pages in the background without rebuilding the entire site.
- **NEXT_PUBLIC_ Prefix**: A mandatory prefix for environment variables in Next.js that must be exposed to the browser (client-side).
- **Stripe Checkout Session**: A server-side generated session object required by Stripe to securely redirect users to a hosted payment page.
- **Line Items (`line_items`)**: The strict array format required by Stripe representing the products, quantities, and prices for a checkout session.
- **Cart Context**: A React Context dedicated to holding the state of the user's shopping basket (mapping product IDs to quantities).

# @Objectives
- Build highly scalable, SEO-friendly, and performant e-commerce storefronts using Next.js hybrid rendering strategies.
- Decouple the frontend from the backend by consuming product data from a Headless CMS (GraphCMS) using GraphQL.
- Manage shopping cart state locally using React Context to prevent unnecessary server loads during product selection.
- Process payments securely by delegating checkout flows to Stripe via server-side API routes.
- Prevent sensitive API keys from leaking to the client by strictly adhering to Next.js environment variable naming conventions.

# @Guidelines

## Project Setup & UI Integration
- The AI MUST integrate Chakra UI for the storefront's styling by installing `@chakra-ui/react`, `@emotion/react`, `@emotion/styled`, and `framer-motion`.
- The AI MUST wrap the application in a `<ChakraProvider>` inside `pages/_app.js`.
- The AI MUST establish a global layout wrapper (e.g., `Flex` and `Box` containers from Chakra UI) inside `_app.js` to ensure consistent UI across all pages.
- The AI MUST install and use `react-icons` (e.g., `react-icons/md`) for UI iconography like shopping carts.

## GraphQL & GraphCMS Configuration
- The AI MUST use `graphql-request` and `graphql` packages instead of heavier clients like Apollo when simple data fetching is sufficient.
- The AI MUST store all GraphQL queries in a dedicated directory: `lib/graphql/queries/`.
- The AI MUST instantiate the `GraphQLClient` centrally in `lib/graphql/index.js`, utilizing environment variables for the endpoint and authorization headers.
- When retrieving products on the client-side (e.g., looking up product details in the cart), the AI MUST ensure the GraphCMS endpoint environment variable is prefixed with `NEXT_PUBLIC_` (i.e., `NEXT_PUBLIC_GRAPHCMS_ENDPOINT`) to prevent polyfill errors in the browser.
- The AI MUST NEVER prefix the GraphCMS mutation/private token with `NEXT_PUBLIC_`. It must remain a server-side secret (e.g., `GRAPHCMS_API_KEY`).

## Rendering Strategies for E-Commerce
- **Home/Storefront Page**: The AI MUST use `getStaticProps` combined with Incremental Static Regeneration (ISR). The returned object MUST include a `revalidate` property (e.g., `revalidate: 60`) so new products appear on the homepage without a full redeploy.
- **Product Detail Pages (`pages/product/[slug].js`)**: The AI MUST use `getStaticPaths` with `fallback: false` (or `true`/`'blocking'` if scaling to thousands of pages) to generate dynamic URLs based on product slugs. The AI MUST use `getStaticProps` to fetch the individual product data.

## Shopping Cart & State Management
- The AI MUST use React Context (`lib/context/Cart/index.js`) to manage the cart state.
- The cart state MUST be structured as an object where keys are product IDs and values are integer quantities: `{ [product_id]: quantity }`.
- The AI MUST wrap the application in the `CartContext.Provider` inside `pages/_app.js`, ensuring it is nested inside the `ChakraProvider`.
- On the Cart page, the AI MUST fetch full product details client-side using a `useEffect` hook that triggers a GraphQL query (`getProductsById`) passing the keys of the cart context object (`Object.keys(items)`).

## Currency and Price Formatting
- **CRITICAL**: The AI MUST handle prices as integer values representing the smallest currency unit (e.g., cents). A price of €4.99 MUST be stored in the CMS and passed to Stripe as `499`.
- When displaying prices on the frontend UI, the AI MUST divide the integer value by 100 (e.g., `price / 100`).

## Stripe Payment Integration
- The AI MUST use `@stripe/stripe-js` on the client-side to load Stripe as a singleton promise (`loadStripe`) in `lib/stripe/index.js` using `NEXT_PUBLIC_STRIPE_SHARABLE_KEY`.
- The AI MUST handle checkout session creation EXCLUSIVELY on the server side using the `stripe` package inside an API route (e.g., `pages/api/checkout/index.js`) using `STRIPE_SECRET_KEY`.
- Inside the checkout API route, the AI MUST fetch the product details from GraphCMS securely to prevent users from tampering with prices on the frontend.
- The AI MUST format the `line_items` array exactly to Stripe's specifications:
  - `adjustable_quantity`: `{ enabled: true, minimum: 1 }`
  - `price_data`: `{ currency: 'EUR', product_data: { name, images }, unit_amount: price }`
  - `quantity`: the amount selected by the user.
- The AI MUST define `shipping_address_collection` (e.g., `allowed_countries: ['US', 'IT']`) and `shipping_options` mapping fixed amounts and delivery estimates within the checkout session payload.
- The API route MUST return the generated session ID to the client, which the client then passes to `stripe.redirectToCheckout({ sessionId: session.id })`.

# @Workflow
1. **Initialize Project**: Install Next.js, Chakra UI, GraphQL Request, Stripe SDK, and React Icons.
2. **Environment Setup**: Define `.env.local` containing `NEXT_PUBLIC_GRAPHCMS_ENDPOINT`, `GRAPHCMS_API_KEY`, `NEXT_PUBLIC_STRIPE_SHARABLE_KEY`, `STRIPE_SECRET_KEY`, and `URL`.
3. **GraphQL Setup**: Create `lib/graphql/index.js` exporting the configured `GraphQLClient`. Write and export `.js` files for required GraphQL queries in `lib/graphql/queries/`.
4. **App Shell**: Create `CartContext`, set up `ChakraProvider` and `CartContext.Provider` in `pages/_app.js`. Create and include a global `NavBar` component.
5. **Storefront Generation**: Build `pages/index.js` using `getStaticProps` with `revalidate` to fetch and map all products to `ProductCard` components.
6. **Product Pages**: Build `pages/product/[slug].js` using `getStaticPaths` and `getStaticProps`. Include a quantity selector and an "Add to Cart" button that updates the `CartContext`.
7. **Cart Page**: Build `pages/cart.js`. Read cart items from Context, fetch their full details via GraphQL `useEffect`, calculate the total price, and render a "Pay Now" button.
8. **Stripe Backend Flow**: Create `pages/api/checkout/index.js`. Receive cart IDs/quantities, fetch trusted product data from GraphCMS, construct `line_items` and shipping objects, create a Stripe session, and return it.
9. **Stripe Frontend Flow**: Attach `handlePayment` to the "Pay Now" button. Fetch the session from the API and execute `redirectToCheckout`.

# @Examples (Do's and Don'ts)

## Environment Variables Configuration
- **[DO]** Prefix variables accessed on the client-side with `NEXT_PUBLIC_`.
```javascript
import { GraphQLClient } from 'graphql-request';

const GRAPHCMS_ENDPOINT = process.env.NEXT_PUBLIC_GRAPHCMS_ENDPOINT;
const GRAPHCMS_API_KEY = process.env.GRAPHCMS_API_KEY; // Server only
const authorization = `Bearer ${GRAPHCMS_API_KEY}`;

export default new GraphQLClient(GRAPHCMS_ENDPOINT, {
  headers: {
    ...(GRAPHCMS_API_KEY && { authorization }),
  },
});
```
- **[DON'T]** Use `process.env` without prefixes for client-side variables, which will result in polyfill/undefined errors in the browser.
```javascript
// INCORRECT: This will fail in the browser because GRAPHCMS_ENDPOINT lacks NEXT_PUBLIC_
const GRAPHCMS_ENDPOINT = process.env.GRAPHCMS_ENDPOINT;
```

## Price Formatting for Display and Stripe
- **[DO]** Send integers to Stripe, but divide by 100 for frontend display.
```javascript
// Display in React Component
<Text>€{(product.price / 100).toFixed(2)}</Text>

// Server-side Stripe session creation
const line_items = products.map((product) => ({
  price_data: {
    currency: 'EUR',
    product_data: { name: product.name },
    unit_amount: product.price, // Sent as integer (e.g., 499)
  },
  quantity: items[product.id],
}));
```
- **[DON'T]** Send floats/decimals to Stripe or display raw integer values as currency.
```javascript
// INCORRECT: Stripe API will throw an error if sent a float
unit_amount: product.price / 100, 
```

## Cart Context Updates
- **[DO]** Update the cart using the product ID as the key and the quantity as the value.
```javascript
const { items, setItems } = useContext(CartContext);
function addToCart() {
  setItems({
    ...items,
    [product.id]: quantity,
  });
}
```
- **[DON'T]** Store entire product objects in the cart state, which causes bloat and stale data.
```javascript
// INCORRECT: Do not store the whole object in local state. Fetch it fresh via ID.
setItems([...items, product])
```

## Stripe API Security
- **[DO]** Fetch product details from the backend CMS inside the Checkout API route to guarantee price integrity.
```javascript
export default async function handler(req, res) {
  const { items } = req.body; // Items only contains IDs and quantities
  const { products } = await graphql.request(getProductsDetailsById, { ids: Object.keys(items) });
  // Map line items based on trusted 'products' data
}
```
- **[DON'T]** Trust price data sent directly from the client.
```javascript
// INCORRECT: A malicious user can alter the request payload to change prices
export default async function handler(req, res) {
  const { line_items } = req.body; 
  const session = await stripe.checkout.sessions.create({ line_items });
}
```