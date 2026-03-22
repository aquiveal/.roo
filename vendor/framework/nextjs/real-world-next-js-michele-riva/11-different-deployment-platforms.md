# @Domain
These rules trigger when the AI is asked to architect, configure, suggest, or implement deployment strategies, CI/CD pipelines, cloud hosting configurations, containerization (Docker), or custom server setups for Next.js applications.

# @Vocabulary
*   **PaaS (Platform as a Service):** Managed cloud platforms like Vercel, Netlify, and Heroku that standardize and simplify the deployment workflow.
*   **Serverless Functions:** A managed infrastructure execution model where a single function runs on-demand. Billed per execution (duration and memory usage) rather than a fixed hourly server rate. Used by Vercel to support Next.js SSR and API routes.
*   **CDN (Content Delivery Network):** A geographically distributed network of data centers. Essential for serving Next.js statically generated (SSG) pages and static assets to minimize client-to-server request latency.
*   **`serverless-next.js`:** An open-source Serverless component used to deploy hybrid Next.js apps to AWS (maps SSR/APIs to AWS Lambda, and static assets to S3/CloudFront).
*   **Process Manager (PM2):** A tool used on custom servers to monitor and automatically restart Node.js processes if they crash, mitigating Node.js's single-threaded architecture limitations.
*   **Reverse Proxy:** A server (e.g., NGINX, Caddy, Envoy) placed in front of a Node.js application on a custom server to add an extra layer of security and routing capabilities.

# @Objectives
*   Evaluate project architecture (SSG vs. SSR vs. Custom Server) and team constraints to recommend the optimal deployment platform.
*   Prevent architectural mismatches, such as attempting to deploy custom Express.js/Fastify servers to Vercel.
*   Ensure custom server deployments are highly available, secure, and resilient by enforcing the use of process managers and reverse proxies.
*   Standardize Docker containerization for Next.js applications using lightweight images and proper working directories.

# @Guidelines
*   **When targeting Vercel or Netlify:** The AI MUST NOT implement or suggest deploying a custom Node.js server (e.g., Express.js or Fastify). The AI MUST rely on Vercel's automatic Serverless Functions for SSR and API routes.
*   **When deploying a fully Static Site (SSG):** The AI MUST recommend deploying to a CDN (Cloudflare Pages, AWS S3 + CloudFront, or Microsoft Azure Static Web Apps) to achieve the best possible performance and geographic distribution.
*   **When an AWS-centric hybrid deployment (SSG + SSR) is requested:** The AI MUST suggest the `serverless-next.js` architecture, mapping SSR and API routes to AWS Lambda, and static/public files to AWS S3 served via CloudFront.
*   **When configuring a bare-metal or custom Virtual Private Server (VPS / EC2 / DigitalOcean):** 
    *   The AI MUST configure a Node.js runtime environment.
    *   The AI MUST implement a process manager (explicitly PM2) to ensure the application restarts upon crashing.
    *   The AI MUST configure a reverse proxy (NGINX, Caddy, or Envoy) to handle incoming traffic.
    *   The AI MUST explicitly instruct the user to configure firewall rules to accept incoming HTTP/HTTPS traffic on ports 80 and 443.
*   **When writing a Dockerfile for Next.js:**
    *   The AI MUST use a lightweight Alpine Linux base image (e.g., `FROM node:16-alpine`).
    *   The AI MUST create and set a dedicated working directory (`RUN mkdir -p /app` and `WORKDIR /app`).
    *   The AI MUST copy the project files, install dependencies (`npm install`), and build the project (`npm run build`) inside the Dockerfile.
    *   The AI MUST expose the correct port (e.g., `EXPOSE 3000`) and set the start command (`CMD npm run start`).
*   **When configuring Docker for Next.js:** The AI MUST ALWAYS generate a corresponding `.dockerignore` file. This file MUST include `.next` and `node_modules` to prevent copying local builds and dependencies into the container.
*   **When advising on platform choice:** The AI MUST factor in team size and existing infrastructure. (e.g., Recommend Vercel/Netlify/Cloudflare for small teams or solo developers; recommend AWS/Azure/GCP if the company already has a dedicated DevOps team and existing infrastructure on those platforms).

# @Workflow
1.  **Analyze the Application Rendering Strategy:** Determine if the Next.js app relies on SSR, SSG, CSR, API routes, or a Custom Server (Express/Fastify).
2.  **Evaluate Context & Constraints:** Ask or infer the team size, budget, and existing cloud provider ecosystem.
3.  **Select the Deployment Strategy:**
    *   *Vercel/Netlify:* For standard Next.js apps (SSG/SSR) prioritizing developer experience and zero-configuration setups.
    *   *CDN (Cloudflare Pages / AWS S3 / Azure):* For purely static Next.js exports.
    *   *Serverless Framework (`serverless-next.js`):* For AWS-specific hybrid Next.js deployments.
    *   *Docker / Custom Server:* For apps requiring a custom Node.js server or integration into complex existing infrastructures (Kubernetes, AWS ECS).
4.  **Generate Configuration:**
    *   If Docker: Output `Dockerfile` and `.dockerignore`.
    *   If Custom Server: Output PM2 ecosystem files and NGINX reverse proxy configurations.
    *   If Vercel: Provide Vercel CLI commands (`vercel` for preview, `vercel --prod` for production).
5.  **Verify Constraints:** Ensure no custom server logic is being pushed to Vercel, and ensure `.dockerignore` prevents bloated container builds.

# @Examples (Do's and Don'ts)

**[DO] Generate a strict, optimized Dockerfile and `.dockerignore` for Next.js**
```dockerfile
# Dockerfile
FROM node:16-alpine
RUN mkdir -p /app
WORKDIR /app
COPY . /app/
RUN npm install
RUN npm run build
EXPOSE 3000
CMD npm run start
```
```ignore
# .dockerignore
.next
node_modules
```

**[DON'T] Write a Dockerfile without a dedicated working directory or use a bloated base image**
```dockerfile
# Anti-pattern: Uses heavy base image, lacks WORKDIR, lacks .dockerignore context
FROM node:16
COPY . .
RUN npm install
RUN npm run build
CMD npm run start
```

**[DO] Recommend a robust stack for a custom VPS deployment**
"To deploy this Next.js application on your DigitalOcean droplet, we must set up the Node.js runtime, use PM2 as a process manager to ensure the app restarts if the single thread crashes, and place NGINX in front as a reverse proxy. Finally, ensure your firewall is open on ports 80 and 443."

**[DON'T] Suggest deploying a custom server to Vercel**
"Since you have written a custom Express.js server in `server.js` to handle your Next.js routing, let's deploy this directly to Vercel using the `vercel --prod` command." *(Anti-pattern: Vercel does not support custom Node.js servers. The AI must warn the user to either drop the custom server or switch to Docker/VPS deployment).*