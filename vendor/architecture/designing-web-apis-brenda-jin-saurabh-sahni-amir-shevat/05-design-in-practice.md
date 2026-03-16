@Domain
Triggers when the user requests assistance with designing, architecting, or specifying a new web API, when defining use cases or user stories for an API, or when generating an API specification document or proposal.

@Vocabulary
- **Problem Statement**: A succinct definition stated at the top of a specification that outlines the problem being solved, explicitly mentioning how it affects the business, the customers, and the developers building third-party integrations.
- **Impact Statement**: A definition of what success looks like for the API, illustrating the desired behaviors the business wants to see from developers using the API.
- **User Story**: A requirement definition focused on the developer's needs, strictly following the format: "As a [user type], I want [action] so that [outcome]."
- **Technology Architecture**: The selected API transport paradigm (REST, RPC, GraphQL, WebHooks, WebSockets, HTTP Streaming) and authentication mechanism (e.g., OAuth 2.0).
- **API Specification (Spec)**: A structured artifact and contract used to communicate design decisions, solicit feedback, and enable parallel implementation. 
- **Mock Data**: A set of fixed API responses served through a lightweight application (e.g., Node.js) to enable interactive user testing and parallel frontend development before backend implementation is complete.
- **Beta Testing Program**: A feedback mechanism allowing selected developer partners early access to a new API to test and validate usability before official public release.

@Objectives
- Anchor all API design decisions in specific, real-life use cases and user needs, explicitly avoiding designs based on internal application architecture or infrastructure.
- Ensure all stakeholders are aligned by clearly defining the business problem and the desired impact before technical implementation begins.
- Select the most appropriate API paradigm and authentication mechanics by evaluating the pros and cons against the specific user stories.
- Produce standardized, comprehensive API Specification documents that act as a source of truth and a contract for parallel development.
- Maximize early feedback through stakeholder reviews, interactive mock data testing, and beta programs to prevent costly rewrites.

@Guidelines
- The AI MUST design APIs for the experience of the outside developer (the user), NEVER simply exposing internal infrastructure or implementation details.
- The AI MUST define a clear Problem Statement and Impact Statement before writing any API endpoints or code. 
- The Problem Statement MUST explicitly involve three parties (if applicable): the business, the direct customers, and the developers building third-party integrations.
- The AI MUST use the exact User Story template provided: `As a [user type], I want [action] so that [outcome].`
- When selecting an API paradigm, the AI MUST explicitly compare the Pros and Cons of potential options (REST, RPC, GraphQL for request-response; WebHooks, WebSockets, HTTP Streaming for event-driven) against the stated user stories.
- When defining API security, the AI MUST map out the specific resources/objects, the allowed operations (Create, Read, Update, Delete), and the corresponding OAuth scopes.
- The AI MUST evaluate the risk of operations (e.g., DELETE) and proactively suggest omitting high-risk operations from the initial API launch unless strictly necessary.
- The AI MUST structure the API Specification with the following exact sections: Title, Authors, Problem, Solution, Implementation, Authentication, Other things we considered, and Detail Tables.
- The AI MUST format endpoint detail tables with the following columns: URI (including HTTP method), Inputs (Required/Optional with types and default values), Outputs (Status code, payload schema), and Scope.
- The AI MUST format event-driven detail tables with the following columns: Event (event name), Payload (JSON schema), and OAuth Scope.
- The AI MUST include a global error table in the specification outlining: Status Code, Description, and Error Response Body (standardized JSON).
- The AI MUST explicitly recommend a feedback validation loop in the design process, including stakeholder reviews, using mock data for interactive testing, and establishing a beta tester program.

@Workflow
1. **Define Business Objectives**: Generate the Problem Statement and Impact Statement. Ensure both are focused on user needs, business goals, and the developer experience.
2. **Outline Key User Stories**: Generate specific use cases for the target developer using the strict user story template.
3. **Select Technology Architecture**: 
   - Generate a Pro/Con evaluation matrix for the API paradigm (e.g., REST vs. RPC vs. GraphQL or WebHooks vs. WebSockets).
   - Select the paradigm that best fits the User Stories.
   - Define the authentication mechanism (e.g., OAuth 2.0).
   - Generate a table mapping Resources -> Operations -> Scopes.
4. **Write the API Specification**: Generate the full specification document containing:
   - High-level summary (Title, Authors, Problem, Solution, Implementation, Authentication, Other things we considered).
   - Endpoint/Event detail tables.
   - Global HTTP status codes and standard error payload table.
   - Open Questions section.
5. **Validate Decisions (Feedback Plan)**: Output a prescriptive plan for the user to validate the design via stakeholder review, interactive mock data development, and beta testing.

@Examples (Do's and Don'ts)

[DO] Define user stories using the strict template:
As a developer, I want to request a list of files so that I can see what a user has uploaded.
As a developer, I want to edit files on behalf of a user so that users don't need to leave my app to add a file to MyFiles.

[DON'T] Define user stories vaguely without outcomes:
The API needs a way to fetch files.
Developers need to be able to edit files.

[DO] Structure API Specification endpoint tables comprehensively:
| URI | Inputs | Outputs | Scope |
|---|---|---|---|
| `GET /files/:id` | Required: None | 200 OK, `$file` object | `read` |
| `POST /files/:id` | Required: `name` (string), Optional: `notes` (string) | 201 Created, `$file` object | `write` |

[DON'T] Write unstructured or incomplete endpoint specifications:
`GET /files/:id` returns a file object. Requires read scope.

[DO] Map operations and scopes explicitly while mitigating risk:
| Resource | Operation | Scope |
|---|---|---|
| Files | Create | `write` |
| Files | Read | `read` |
| Files | Update | `write` |
*(Note: Delete operation omitted for initial launch due to high risk).*

[DON'T] Assign blanket scopes without evaluating operation risks:
Give developers full read/write/delete access to the `files` scope for all endpoints.

[DO] Define a standardized error response body:
| Status Code | Description | Error Response Body |
|---|---|---|
| 400 Bad Request | The request cannot be accepted due to missing parameters. | `{ "error": "missing_parameter", "message": "The following parameters are missing: <param>" }` |

[DON'T] Define generic or empty errors:
| Status Code | Description |
|---|---|
| 400 | Bad Request |