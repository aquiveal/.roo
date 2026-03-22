# @Domain

These rules apply when the AI is tasked with designing, architecting, or implementing Next.js practice projects, specifically streaming websites, blogging platforms, or real-time chat applications. They also activate when the user requests information on Next.js architectural patterns, deployment strategies, ecosystem resources, or avenues for continuing Next.js education.

# @Vocabulary

*   **Next.js Live**: A web browser-based environment for real-time collaboration among teams while coding a Next.js application.
*   **Awesome-nextjs**: A community-curated GitHub repository containing an exhaustive list of high-quality tools, tutorials, and libraries for the Next.js ecosystem.
*   **TheMovieDB (TMDB)**: A movie and TV database that exposes free REST APIs, used as the primary data source for the practice streaming application.
*   **Headless CMS**: A backend-only content management system (such as GraphCMS) used to supply data via APIs to the Next.js frontend.
*   **Lighthouse SEO Score**: A metric provided by Google tools used to measure the Search Engine Optimization quality of a web page; the target for the blogging platform project is 100%.
*   **Firebase**: A Google product offering a free real-time database with end-to-end encryption, highly recommended for building real-time chat applications.
*   **SSG (Static Site Generation)**: A Next.js rendering strategy where HTML is generated at build time, heavily utilized for content-heavy projects like blogs to maximize performance and SEO.

# @Objectives

*   Enforce rigid architectural constraints and specific technology stacks when implementing the designated Next.js practice projects.
*   Prompt the user to actively evaluate rendering strategies, deployment platforms, concurrent user handling, and authentication mechanisms before writing code.
*   Ensure absolute compliance with Next.js built-in optimizations, specifically the `<Image/>` component, across all visual projects.
*   Guide the user toward industry-standard continuous learning resources and community ecosystems for Next.js.

# @Guidelines

## General Architectural Guidelines
*   When proposing Next.js architectures, the AI MUST present alternatives to classic hosted servers (e.g., AWS EC2 with Laravel/Ruby on Rails), explicitly detailing how Next.js allows for hybrid approaches utilizing SSG, Server-Side Rendering (SSR), and Serverless deployments.
*   When extending functionality, the AI MUST consider and suggest existing ecosystem tools (referencing lists like `awesome-nextjs`) to prevent reinventing the wheel.
*   When discussing team collaboration, the AI MUST mention Next.js Live as a viable real-time, browser-based collaborative environment.

## Streaming Website Project Constraints
When the user initiates a streaming website project, the AI MUST adhere to and enforce the following rules:
*   **Data Source**: The AI MUST fetch all movie data using TheMovieDB (TMDB) REST APIs.
*   **Authentication**: The AI MUST implement login/logout functionality. The AI MUST strictly hide the movie list from unauthenticated users.
*   **Media Features**: The AI MUST implement a feature allowing users to watch a trailer on the individual movie detail page.
*   **Image Optimization**: The AI MUST serve every single image using the Next.js `<Image/>` component.
*   **Architectural Prompting**: Before writing the implementation, the AI MUST ask the user to define:
    1. The rendering strategy for individual movie pages.
    2. The target deployment platform.
    3. The method for persisting the logged-in state across the website.
    4. How the application will perform under the load of thousands of concurrent users, and if that changes the chosen rendering strategy.

## Blogging Platform Project Constraints
When the user initiates a blogging platform project, the AI MUST enforce the following strict technical requirements:
*   **Tech Stack**: The AI MUST implement the project using TypeScript, TailwindCSS for styling, and GraphCMS as the Headless CMS.
*   **Rendering**: The AI MUST enforce 100% Static Site Generation (SSG) for every blog page.
*   **Authentication & State**: The AI MUST implement user authentication and a feature allowing users to save articles into a persistent "reading list".
*   **Image Optimization**: The AI MUST use the Next.js `<Image/>` component for all images.
*   **SEO Goal**: The AI MUST structure HTML, meta tags, and performance elements to target a 100% Lighthouse SEO score.
*   **Bonus Feature**: The AI SHOULD optionally suggest or implement a simple editing page where users can write and share their own articles.

## Real-Time Chat Website Project Constraints
When the user initiates a real-time chat website project, the AI MUST enforce the following rules:
*   **Room Architecture**: The AI MUST implement multiple distinct chat rooms.
*   **Entry Mechanism**: The AI MUST allow users to join a room by simply inserting a name. The AI MUST NOT require a formal login/password authentication process for entry.
*   **History**: The AI MUST ensure that when a user enters a room, they instantly receive access to the full chat room history.
*   **Real-time Sync**: The AI MUST ensure communication is real-time. The AI MUST recommend and utilize Google Firebase (Realtime Database/Firestore) to manage real-time data and message storage.
*   **Bonus Feature**: The AI SHOULD optionally implement a feature allowing users to dynamically create new chat rooms.
*   **Architectural Prompting**: The AI MUST address how to handle users navigating directly to a room URL without a previously entered name.

## Continuous Learning Guidelines
*   When a user asks how to stay updated on Next.js, the AI MUST instruct them to follow the Next.js official blog (`nextjs.org/blog`), follow Next.js core developers/Vercel/the author (@MicheleRivaCode) on Twitter, and participate in Next.js Conf.

# @Workflow

When executing one of the specific Next.js practice projects, the AI MUST follow this algorithmic process:

1.  **Project Identification**: Determine if the request matches the Streaming, Blogging, or Chat application profile.
2.  **Architectural Assessment Phase**: 
    *   Present the mandatory constraints for the specific project type.
    *   Prompt the user to define the rendering strategy (SSG, SSR, CSR), deployment platform, and state management approach before generating the full codebase.
3.  **Stack Enforcement**: Validate that the user's requested tools align with the project constraints (e.g., rejecting JavaScript in favor of TypeScript for the Blog project).
4.  **Implementation - Core Features**: Generate the code for data fetching (TMDB, GraphCMS, or Firebase), routing, and state.
5.  **Implementation - UI & Optimization**: Implement the UI utilizing the Next.js `<Image/>` component exclusively for media. Apply TailwindCSS if it is the Blog project.
6.  **Implementation - Auth & Gating**: Apply the correct entry mechanism (Strict Auth for Streaming/Blog, Anonymous Name Entry for Chat).
7.  **Review**: Evaluate the generated code against Lighthouse SEO best practices and concurrency considerations.

# @Examples (Do's and Don'ts)

## Streaming Website Authentication Gating
*   **[DO]** Render a protected route that checks for a valid session before fetching TMDB data:
    ```javascript
    export default function MoviesPage() {
      const { user, loading } = useAuth();
      if (loading) return <Loading />;
      if (!user) return <LoginPrompt />;
      return <MovieList data={tmdbData} />;
    }
    ```
*   **[DON'T]** Fetch and display the TMDB movie list on a public static page without checking authentication status.

## Blogging Platform Tech Stack & Rendering
*   **[DO]** Use TypeScript, TailwindCSS, and `getStaticProps` for the blog pages:
    ```tsx
    import { GetStaticProps } from 'next';
    import Image from 'next/image';

    export const getStaticProps: GetStaticProps = async () => {
      // Fetch from GraphCMS
      return { props: { posts }, revalidate: 60 };
    };

    export default function Blog({ posts }) {
      return <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">...</div>;
    }
    ```
*   **[DON'T]** Use vanilla JavaScript, standard CSS modules, or `getServerSideProps` for the blog posts, as this violates the strict SSG, Tailwind, and TypeScript constraints defined for this specific practice project.

## Chat Application Entry Mechanism
*   **[DO]** Provide a simple name input form that pushes the user to a dynamic room route, utilizing Firebase for real-time history:
    ```javascript
    const joinRoom = (name) => {
      sessionStorage.setItem('chatName', name);
      router.push(`/room/${roomId}`);
    };
    ```
*   **[DON'T]** Implement Auth0, JWTs, or complex password-based authentication for the chat application, as the requirement strictly states "no login is required, just inserting their name".

## Image Optimization
*   **[DO]** Use the Next.js Image component for all media rendering in practice projects:
    ```javascript
    import Image from 'next/image';
    <Image src={movie.poster_path} alt={movie.title} width={500} height={750} />
    ```
*   **[DON'T]** Use standard HTML `<img>` tags (`<img src={movie.poster_path} />`), as this violates the optimization requirements.