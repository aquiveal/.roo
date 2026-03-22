# @Domain
These rules MUST trigger when the AI is tasked with designing or modifying microservice boundaries, configuring repository ownership (e.g., `CODEOWNERS`), generating organizational documentation (e.g., `CONTRIBUTING.md`, Team APIs), establishing continuous integration/code review workflows, scaffolding platform or enablement tools, or evaluating system architectures for scaling development teams.

# @Vocabulary
- **Conway's Law**: The principle that organizations design systems that mirror their own communication structures.
- **Stream-Aligned Team**: A team aligned to a single, valuable stream of work with end-to-end responsibility for delivering user-facing functionality.
- **Enabling Team**: A cross-cutting group of specialists acting as an internal consultancy to help stream-aligned teams upskill and overcome obstacles.
- **Community of Practice (CoP)**: A cross-cutting group fostering shared learning and experiential knowledge across peers from different teams.
- **Strong Ownership**: A model where a specific team owns, controls, and dictates changes to a microservice.
- **Collective Ownership**: A model where any developer from any team can change any microservice (suitable only for small organizations; an anti-pattern at scale).
- **Full Life-Cycle Ownership**: A mature form of strong ownership where a team designs, develops, deploys, operates, and eventually decommissions a microservice.
- **Paved Road**: A set of common tools and platforms provided to make doing the "right thing" easy, without rigidly mandating their use.
- **Team API**: The explicit definition of how other teams interact with a specific team, including code, working practices, communication, and pull request responsiveness.
- **Internal Open Source**: A contribution model where a core team owns a microservice, but "untrusted" developers from other teams can submit pull requests that are vetted by the core team.
- **Orphaned Service**: A mature, stable microservice that rarely changes but still requires an explicit organizational owner.
- **Ensemble (Mob) Programming**: A practice where a whole team works together on a change, requiring awareness of neurodiversity and power dynamics to ensure inclusive participation.

# @Objectives
- The AI MUST align system architecture with the communication structures and boundaries of the organization (Conway's Law).
- The AI MUST optimize system design to minimize cross-team communication, coordination, and lockstep deployments.
- The AI MUST enforce and structure "Strong Ownership" by mapping every microservice to a single owning team.
- The AI MUST treat developer experience, team autonomy, and the cognitive load of human operators as first-class architectural constraints.
- The AI MUST replace rigid architectural governance with "Paved Road" platforms and peer-review workflows.

# @Guidelines
- **Organizational Alignment (Conway's Law)**: When proposing a microservice extraction or merge, the AI MUST explicitly ask or define which team will own the resulting service(s). The AI MUST NOT propose a service boundary that requires constant synchronous coordination between two different teams.
- **Team Size & Autonomy**: The AI MUST design systems under the assumption that optimum team size is 5 to 10 people (the "two-pizza" rule). If a service requires more than 10 people to maintain, the AI MUST recommend functionally decomposing the service.
- **Ownership Protocols**: The AI MUST enforce Strong Ownership. The AI MUST NOT recommend Collective Ownership for organizations with more than ~20 developers. Every service, even static "Orphaned Services", MUST have an explicit owner.
- **Cross-Team Contributions (Internal Open Source)**: When configuring repositories where cross-team collaboration is required to avoid delivery bottlenecks, the AI MUST generate strict PR templates, contribution guidelines, and CI/CD validation to assist the core "trusted" committers in reviewing code from "untrusted" external committers.
- **Handling Shared Microservices**: If the AI detects a shared microservice acting as a delivery bottleneck (receiving high volumes of PRs from multiple teams), the AI MUST suggest one of three remediations:
  1. Reassigning ownership to the team most affected.
  2. Splitting the microservice.
  3. Implementing a pluggable framework where the core team maintains the skeleton, and external teams contribute independent libraries or run local variations.
- **Platform as a Paved Road**: When generating platform-level code or infrastructure templates (e.g., scaffolding, CI pipelines), the AI MUST configure them to be easily consumable ("Paved Road") but MUST NOT bake in artificial restrictions that prevent teams from bypassing the platform if their specific context requires it.
- **Change Reviews**: The AI MUST configure review processes to favor fast, synchronous peer reviews within the team. The AI MUST NOT introduce external architectural approval gates for routine code changes, as this degrades delivery performance.
- **Geographical Distribution**: The AI MUST limit synchronous communication dependencies (and thus tight architectural coupling) between teams operating in wildly different time zones.
- **Team APIs**: The AI MUST document repository interactions by generating `README.md` and `CONTRIBUTING.md` files that explicitly define the "Team API" (how to contact the owning team, SLA for PR reviews, issue logging procedures).

# @Workflow
When configuring a repository, generating an architecture proposal, or setting up deployment pipelines, the AI MUST execute the following algorithm:

1. **Assess Organizational Boundaries**: Identify the teams involved. Map the proposed or existing microservices to these teams. Verify that the mapping is 1:1 (one service is owned by one team, though one team may own multiple services).
2. **Establish Explicit Ownership**: Generate or update `CODEOWNERS` files, `README` badges, and infrastructure metadata tags (e.g., AWS tags, Kubernetes labels) to definitively state which stream-aligned team owns the microservice.
3. **Define the Team API**: Scaffold repository documentation that answers: 
   - Who owns this?
   - How do external teams submit changes (Internal Open Source)?
   - What is the expected turnaround for PR reviews?
4. **Configure Peer-Review Pipelines**: Generate CI/CD configuration (e.g., GitHub Actions, GitLab CI) that enforces automated quality checks and requires internal peer reviews, explicitly avoiding external architectural approval gates.
5. **Evaluate the Paved Road**: If generating platform tools or shared templates, ensure the generated code encapsulates complex cross-cutting concerns (e.g., authentication, logging) but remains opt-in and configurable for the consuming stream-aligned teams.
6. **Remediate Bottlenecks**: If instructed to resolve a highly-contended codebase, analyze the PR/commit history to determine if the service should be decomposed (functional decomposition), modularized (plugin architecture), or reassigned.

# @Examples (Do's and Don'ts)

## [DO] Explicitly Define Strong Ownership
**Scenario**: Generating a `CODEOWNERS` file and metadata for a new microservice.
```text
# CODEOWNERS
# Strong ownership: The checkout-squad owns the entirety of this microservice
* @acme-inc/checkout-squad

# Infrastructure as Code tags (e.g., Terraform)
tags = {
  Service     = "shopping-cart"
  Owner       = "checkout-squad"
  Support     = "slack://#checkout-squad-alerts"
  Lifecycle   = "full-ownership"
}
```

## [DON'T] Implement Centralized Approval Gates
**Scenario**: Configuring branch protection rules or CI/CD pipelines.
```yaml
# ANTI-PATTERN: Forcing external architecture boards to approve standard changes
branches:
  main:
    required_pull_request_reviews:
      required_approving_review_count: 2
      # BAD: Requiring an external siloed team to approve stream-aligned team code
      require_code_owner_reviews: true
      required_reviewers:
        - @acme-inc/enterprise-architecture-board 
```

## [DO] Define a Team API for Internal Open Source
**Scenario**: Generating a `CONTRIBUTING.md` for a shared service to reduce coordination costs.
```markdown
# Interacting with the Catalog Service (Team API)

**Owner**: @acme-inc/catalog-squad
**Primary Contact**: #catalog-squad-help on Slack

## Submitting Changes (Internal Open Source)
We welcome PRs from other teams to prevent delivery bottlenecks! To ensure your PR is merged quickly:
1. Discuss the change in #catalog-squad-help before writing code.
2. Ensure all automated tests pass.
3. We review external PRs synchronously every day at 14:00 UTC. Feel free to join our Zoom room for an inline review.
```

## [DON'T] Create Tightly Coupled Cross-Team Processes
**Scenario**: Proposing an architectural workflow for a cross-cutting business requirement.
**AI Output Anti-pattern**: "To implement the new multi-user account feature, the frontend team should create a shared branch, make their UI changes, and then hand off the branch to the backend team to add the database changes, followed by a joint deployment on Friday."
**Reasoning**: This violates independent deployability and creates massive coordination costs. The AI MUST instead suggest stream-aligned teams owning vertical slices, or decoupling the deployment via API contracts (CDCs) and feature toggles.