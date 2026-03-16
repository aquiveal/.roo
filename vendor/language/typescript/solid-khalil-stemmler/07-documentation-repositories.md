@Domain
This rule set is triggered whenever the AI is tasked with creating, reviewing, updating, or structuring repository documentation (e.g., `README.md`, `CONTRIBUTING.md`), initializing a new project repository, or defining the onboarding, testing, and debugging instructions for a codebase.

@Vocabulary
- **High-Leverage Repository**: A well-designed codebase entry point that anticipates and automatically answers the most common developer questions, creating leverage by reducing the need for future maintainers to contact the original authors.
- **The Midfielder Metaphor**: The strategic mindset required for repository design. Just as a soccer midfielder surveys surroundings, predicts needs, and sets up plays, repository documentation must think ahead and strategically place information to make future developers useful immediately.
- **Push Complexity Downwards**: The architectural principle of structuring information from the most declarative, highest layer of abstraction down to the lowest. The required hierarchy is: Repository -> Feature folders -> Tests -> Implementation boundary -> Implementation internals.
- **Tests as Documentation**: The practice of using test suites (which demonstrate use cases and functionality) as the primary form of documentation for enterprise software, explicitly replacing traditional, manually written API documentation.
- **Affordances (in Documentation)**: Clear explanations of what a repository is used for, allowing developers to immediately understand what problems the codebase solves and how they can utilize it.

@Objectives
- Create high-leverage repositories that act as the ultimate jumping-off point for learning a codebase.
- Anticipate the needs of future maintainers by providing immediate, copy-and-pasteable solutions to top-level developer goals.
- Enforce the "Push Complexity Downwards" hierarchy so that readers are never overwhelmed by implementation details at the repository root.
- Establish the test suite as the single source of truth for system capabilities, omitting heavy API documentation unless building public developer tooling.

@Guidelines
- **The 6 Mandatory Questions**: The AI MUST ensure the repository root documentation (e.g., `README.md`) explicitly answers the following six questions:
  1. *What is this?*
  2. *What is it for?*
  3. *How do I get started?*
  4. *How do I run the tests?*
  5. *How do I debug it?*
  6. *Where are the features?*
- **Title and Description Constraint**: The AI MUST provide a clear Title and exactly a ONE-sentence description stating whether the repo is a frontend application, backend service, or other specific service.
- **Affordance Creation**: Under "What is it for?", the AI MUST explain the repository's purpose so developers can quickly build mental affordances (e.g., "Ah, I can use this to solve X").
- **Frictionless Setup**: Under "How do I get started?", the AI MUST provide explicit, copy-and-pasteable terminal commands. 
- **Single-Command Testing**: Under "How do I run the tests?", the AI MUST provide a single command to run the test suite. If the testing setup requires an involved process (e.g., installing heavy dependencies or setting up databases), the AI MUST abstract those details into a separate file (e.g., `TESTING_SETUP.md`) and link to it.
- **Explicit Debugging State**: Under "How do I debug it?", the AI MUST document any special flags, environment variables, or specific commands required to run the application in debug mode.
- **Feature Discoverability**: Under "Where are the features?", the AI MUST provide direct links or clear file-path directions to the feature-driven folders where the actual work happens.
- **Push Complexity Downwards**: The AI MUST NOT explain implementation details (how the code works) in the root repository documentation. The AI MUST guide the user through the established hierarchy: point them to the feature folders, which point to the tests, which point to the implementation boundaries (controllers/pages), which finally reveal the implementation internals.
- **Tests Over API Docs Rule**: When documenting enterprise applications, the AI MUST point developers to the test suite to learn the system's use cases and API capabilities. The AI MUST NOT generate comprehensive written API documentation. 
- **The Public Tooling Exception**: The ONLY exception to the "Tests Over API Docs Rule" is if the AI determines the project is a public SDK, developer tool, library, or framework (e.g., like Apollo or Stripe). In this specific context, the AI MUST generate thorough, written API documentation.

@Workflow
1. **Context Analysis**: Identify the repository's core domain, purpose, and whether it is an internal enterprise application or a public developer tool.
2. **Initialize Root Documentation**: Create or update the `README.md` file to act as the "Midfielder" of the project.
3. **Define Identity**: Write the Title and a strict one-sentence description answering "What is this?".
4. **Establish Affordances**: Write the "What is it for?" section, explaining the business problem the repository solves.
5. **Document Onboarding**: Write the "How do I get started?" section using direct, copy-and-pasteable terminal commands.
6. **Document Testing**: Write the "How do I run the tests?" section. Provide the single command needed. Extract complex setup steps into a separate linked guide if necessary.
7. **Document Debugging**: Write the "How do I debug it?" section, detailing specific debug flags or IDE configurations.
8. **Map the Features**: Write the "Where are the features?" section. Provide navigation directly to the feature folders to push complexity downwards.
9. **Delegate Documentation to Tests**: Add a section explicitly instructing developers to read the test files within the feature folders to understand the system's use cases and functionality. (Bypass this step and generate API docs ONLY if the project is a public SDK/tool).

@Examples (Do's and Don'ts)

[DO]
```markdown
# DDDForum Backend

A Node.js backend service powering the DDDForum web application.

## What is it for?
This repository handles all core domain logic, user authentication, and forum operations (posts, comments, voting) for the DDDForum enterprise.

## How do I get started?
```bash
npm install
npm run start:dev
```

## How do I run the tests?
```bash
npm run test
```
*(If you need to set up the local testing database first, please see our [Test Setup Guide](./docs/TESTING.md))*

## How do I debug it?
To run the server with the Node debugger attached:
```bash
npm run start:debug
```

## Where are the features?
We use a feature-driven folder structure. You can find all use cases located in `src/modules/`. 

## Documentation
To understand how a feature works, what it does, and what its capabilities are, **read the tests** located inside each specific feature folder (e.g., `src/modules/forum/useCases/upvotePost/upvotePost.spec.ts`). Our tests act as our primary documentation.
```

[DON'T]
```markdown
# Backend
This is the backend. 

## API Documentation
### POST /users
Creates a user. 
Parameters:
- email (string)
- password (string)
Implementation details: This route hits the `UserController`, which calls the `CreateUserUseCase`, which uses the `SequelizeUserRepo` to save to a MySQL database using the `UserModel`.

### GET /posts
Gets posts.

(No instructions on how to install, run tests, or run in debug mode. Fails to push complexity downwards by exposing implementation details in the README. Fails to rely on tests as documentation for an enterprise app).
```