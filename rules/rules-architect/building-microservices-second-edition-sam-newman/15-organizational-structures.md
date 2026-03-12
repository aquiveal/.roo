@Domain
This rule file MUST trigger whenever the user requests assistance with system architecture design, team topology, organizational structuring, code ownership models, platform engineering, repository setup, code review workflows, or the migration of shared/legacy codebases to microservices. 

@Vocabulary
- **Conway's Law**: The principle that organizations design systems that mirror their own communication structures.
- **Stream-Aligned Team**: A small, autonomous team with end-to-end responsibility for delivering a specific slice of user-facing business functionality.
- **Enabling Team**: A cross-cutting group of specialists (e.g., security, architecture) whose primary purpose is to support and upskill stream-aligned teams, acting as internal consultants.
- **Community of Practice (CoP)**: An informal, cross-cutting group that fosters social learning, sharing, and best practices among peers without enforcing strict governance.
- **Strong Ownership**: A code ownership model where a specific microservice is exclusively owned by a single team that dictates its design, technology, and deployment.
- **Collective Ownership**: A code ownership model where any developer from any team can modify any part of the system.
- **Full Life-Cycle Ownership**: The practice where the team that builds a microservice is also responsible for its design, testing, deployment, production support, and eventual decommissioning.
- **Team API**: The defined boundaries, working practices, communication protocols, and code interaction methods (e.g., pull requests) a team exposes to the rest of the organization.
- **The Paved Road**: An approach to platform engineering where the platform team provides a set of tools that make the "right way" the easiest way, while keeping platform usage strictly optional.
- **Internal Open Source**: A governance model for shared codebases where a core team acts as trusted gatekeepers, reviewing and merging pull requests submitted by untrusted external teams.
- **Ensemble Programming (Mob Programming)**: A synchronous code review and development practice where an entire team works collaboratively on a single change simultaneously.
- **Orphaned Service**: A mature microservice that rarely changes but must still retain a designated owning team based on its bounded context.

@Objectives
- Ensure that the proposed software architecture perfectly aligns with the organizational communication structure to minimize cross-team coordination (Conway's Law).
- Optimize for team autonomy by advocating for small, self-sufficient, stream-aligned teams over siloed, functional groups.
- Enforce "Strong Ownership" models for microservices, explicitly rejecting "Collective Ownership" as organizational scale increases.
- Position platform engineering and architecture as enabling functions rather than authoritarian governance gates.
- Architect deployment and review workflows to prioritize synchronous feedback, isolated testing, and independent deployability.

@Guidelines

**Team Size and Autonomy**
- When recommending team sizes, the AI MUST constrain teams to 5-10 individuals. The AI MUST warn that adding people to late projects increases coordination overhead and delays delivery (Brooks's Law).
- The AI MUST advocate for "Stream-Aligned Teams" with "Full Life-Cycle Ownership" over their microservices. 
- The AI MUST ensure teams explicitly define a "Team API" documenting how external groups should interact with their code and processes.

**Code Ownership Models**
- The AI MUST default to proposing a "Strong Ownership" model (one team explicitly owns a microservice). 
- If the user proposes "Collective Ownership" for an organization with more than 20 developers, the AI MUST warn that this model requires high global consistency, reduces technology options, and causes tight architectural coupling.
- When generating repository configurations (e.g., `CODEOWNERS`), the AI MUST map specific microservices to single, distinct team aliases.
- When dealing with an "Orphaned Service," the AI MUST assign its ownership to the team that manages the encompassing bounded context, even if the service requires no immediate changes.

**Platform and Governance**
- When designing platforms or infrastructure tooling, the AI MUST apply the "Paved Road" principle: the platform MUST be highly usable but STRICTLY OPTIONAL. The AI MUST NOT generate policies that mandate platform usage.
- The AI MUST define the platform team's primary metric as developer adoption driven by usability, not enforced compliance.
- The AI MUST treat architects as members of an "Enabling Team." The AI MUST NOT generate architectures where architects act as isolated external reviewers or command-and-control gatekeepers.

**Managing Shared Microservices and Bottlenecks**
- If a microservice becomes a delivery bottleneck because multiple teams need to change it, the AI MUST propose one of three solutions:
  1. Reassign ownership to the team making the most changes.
  2. Implement an "Internal Open Source" model where the owning team acts as core committers vetting pull requests.
  3. Refactor the service into a "Pluggable/Modular" framework where teams inject domain-specific libraries, BUT the AI MUST warn that this forces lockstep deployments of the core framework.
- The AI MUST warn that high volumes of inbound pull requests to a single team are a critical anti-pattern indicating an improperly bounded microservice.

**Change Reviews and Feedback Loops**
- When defining code review workflows, the AI MUST prioritize synchronous, peer-based reviews (e.g., Pair Programming, Ensemble Programming) over asynchronous or external reviews.
- The AI MUST NOT generate workflows that require external architectural approval boards for standard deployments, as this decreases software delivery performance.

**Geographical Distribution**
- If the user specifies a geographically distributed organization, the AI MUST map software boundaries to geographical boundaries. A single microservice MUST NOT be co-owned by teams in entirely different time zones to avoid asynchronous communication delays.

@Workflow
1. **Analyze Org Structure**: When prompted with an architectural task, first request or infer the size, distribution, and structure of the organization building the software.
2. **Evaluate Conway's Law**: Cross-reference the proposed system boundaries with the team boundaries. Identify any microservice that requires commits from multiple distinct teams.
3. **Resolve Bottlenecks**: If cross-team coordination is required to deploy a feature, re-draw the service boundaries or propose a transfer of service ownership to a single stream-aligned team.
4. **Apply Ownership**: Generate documentation, repository structures, and deployment pipelines that enforce "Strong Ownership" (e.g., dedicated CI/CD pipelines per team, specific `CODEOWNERS`).
5. **Define Enabling Support**: Introduce "Paved Road" platform tools and "Enabling Teams" to handle cross-cutting concerns (security, deployment) without blocking the stream-aligned teams.
6. **Establish Review Loops**: Generate synchronous local code review processes, ensuring changes are approved by peers within the same team rather than external bodies.

@Examples (Do's and Don'ts)

[DO] Implement Strong Ownership via Repository Configuration
```yaml
# DO: Clearly define strong ownership using CODEOWNERS where one team owns the domain
/services/recommendations/ @musiccorp/customer-engagement-team
/services/shopping-cart/   @musiccorp/purchase-flow-team
/services/inventory/       @musiccorp/warehouse-operations-team
```

[DON'T] Implement Collective Ownership via Repository Configuration
```yaml
# DON'T: Allow any team to collectively own and merge code across all domains
/services/recommendations/ @musiccorp/all-engineers
/services/shopping-cart/   @musiccorp/all-engineers
/services/inventory/       @musiccorp/all-engineers
```

[DO] Design Paved Road Platform Policies
```markdown
# DO: Make platform adoption driven by usability
## Deployment Policy
Teams are highly encouraged to use the `musiccorp-k8s-deployer` CLI for zero-downtime deployments. It handles mutual TLS, logging, and metrics automatically. However, if a stream-aligned team has specific requirements (e.g., deploying a serverless AWS Lambda), they are fully empowered to build their own pipeline provided they meet the baseline organizational SLOs.
```

[DON'T] Design Mandatory Command-and-Control Platform Policies
```markdown
# DON'T: Govern via strict platform mandates
## Deployment Policy
ALL microservices MUST be deployed using the central platform team's Jenkins pipeline. No team is permitted to use alternative deployment targets or tools. Any deviations require a 4-week review cycle and sign-off by the central Enterprise Architecture Board.
```

[DO] Resolve Shared Microservice Bottlenecks
```markdown
# DO: Use Internal Open Source for unavoidable shared code
## Core Payment Framework (Owned by @finance-team)
To add a country-specific payment gateway, please submit a PR to the `/integrations` folder. The `@finance-team` (Core Committers) will synchronously review the PR within 24 hours to ensure idiomatic consistency before merging.
```

[DON'T] Create Cross-Team Code Review Bottlenecks
```markdown
# DON'T: Rely on asynchronous external reviews
## Pull Request Requirements
Once the stream-aligned team finishes a feature, assign the PR to the external `@architecture-review-board`. They meet bi-weekly to review all cross-domain PRs.
```