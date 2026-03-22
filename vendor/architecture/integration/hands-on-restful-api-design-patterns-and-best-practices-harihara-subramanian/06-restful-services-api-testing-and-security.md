@Domain
These rules MUST trigger when the AI is tasked with designing, developing, testing, or reviewing RESTful APIs. This includes writing test automation (unit, functional, load, runtime, security), configuring API security measures, implementing authentication/authorization (including OAuth2), mitigating web vulnerabilities (XSS, CSRF, IDOR, Injections, MITM), or architecting data access layers using the CQRS pattern.

@Vocabulary
- **Verification**: The process of checking software for consistency and alignment with documented requirements.
- **Validation**: The process of checking the accuracy of the system against actual end-user needs and expected outcomes.
- **Runtime Error Detection Tests**: Negative tests targeting race conditions, handler failures, network communication failures, and resource leaks (memory, timeouts).
- **OAuth2 Implicit Flow**: Authorization scheme for Single-Page Applications (SPAs).
- **OAuth2 Client-Credentials Flow**: Authorization scheme for machine-to-machine, non-interactive programs.
- **OAuth2 Authorization Code Flow**: Authorization scheme for less trusted third-party apps requesting access.
- **OAuth2 Resource Owner Password Credentials Flow**: Authorization scheme for highly trusted, first-party apps.
- **Reflected XSS**: Non-persistent injection of malicious code executed via a single HTTP response.
- **Stored XSS**: Persistent malicious script injected as input and viewed later by another user or admin.
- **DOM XSS**: Client-side code execution using insecure references to DOM objects unmanaged by the server.
- **CSRF (Cross-site Request Forgery)**: Forcing an authenticated user to execute unwanted actions via forged links/pages.
- **IDOR (Insecure Direct Object Reference)**: Exposing direct access to internal objects (e.g., file IDs, DB keys) without validating user access rights.
- **CRLF Injection**: Injecting End-of-Line/Carriage Return characters to split HTTP headers and facilitate arbitrary content injection.
- **Host Header Injection**: Abusing the HTTP Host Header to manipulate caching or deliver malicious password reset links.
- **MITM (Man-in-the-Middle)**: Interception of network traffic via sniffing, packet injection, SSL stripping, or session hijacking.
- **Replay Attack**: Maliciously repeating a valid data transmission; countered by TTL, timestamps, and OTPs.
- **White-Box Pen Testing**: Security testing with full access to schema, source code, and models to find logic/design flaws and hardcoded secrets.
- **Fuzz Testing (Mutation-based)**: Creating test noise by altering valid data samples (e.g., bit flipping, appending random strings).
- **Fuzz Testing (Generation-based)**: Intelligent fuzzing that builds random test data from scratch based on protocol specifications and data models.
- **CQRS (Command Query Responsibility Segregation)**: Architectural pattern segregating read operations (Queries) from write/update operations (Commands) into separate interfaces or data stores.

@Objectives
- Achieve comprehensive test coverage focusing strictly on the Business layer, bypassing UI layers for API tests.
- Prevent all OWASP-style vulnerabilities within RESTful APIs through strict input validation, encoding, and correct protocol usage.
- Ensure API test cases are entirely self-contained, repeatable, and completely free from test chaining (reusing data from previous tests).
- Architect high-performance, high-contention endpoints using CQRS to independently scale read and write workloads.
- Enforce the principle of least privilege across all endpoints using robust, scheme-appropriate OAuth2 implementations and explicit object-level ownership checks.

@Guidelines
- **Test Strategy & Design:**
  - The AI MUST define the scope, input parameters, bounds (boundary analysis/equivalence classes), and expected results before generating test code.
  - The AI MUST group API test cases strictly by category (Unit, Functional, Security, Runtime).
  - The AI MUST write tests that are self-contained. Test chaining is STRICTLY FORBIDDEN. Each test MUST setup and teardown its own data.
  - The AI MUST explicitly declare the involved/called APIs at the top of each test case file or block.
  - The AI MUST construct specific test sequences for multi-threaded applications or multi-step business transactions.
  - The AI MUST write execution error tests that explicitly assert expected failures (e.g., asserting a 404 for an invalid ID, asserting 401 for bad credentials).
- **Data Protection & Encryption:**
  - The AI MUST classify data. Sensitive data MUST NOT be stored unless absolutely necessary.
  - The AI MUST use tokenization, truncation, and encryption for sensitive data at rest and in transit.
  - The AI MUST explicitly disable caching (e.g., `Cache-Control: no-store`) for all endpoints handling sensitive data.
  - The AI MUST use salted, adaptive hashing (configurable iterations) for password storage.
- **Authentication & Authorization:**
  - The AI MUST select the correct OAuth2 flow based on the client type (Implicit for SPAs, Client-Credentials for M2M, Auth Code for 3rd-party, Resource Owner Password for 1st-party).
  - The AI MUST ensure stateful cookie-based authorization is avoided for multi-domain APIs, preferring stateless token-based authorization (e.g., JWT).
  - The AI MUST implement function-level access control, ensuring administrative or privileged URLs return 403 Forbidden to unauthorized roles.
  - The AI MUST validate object ownership on EVERY request to prevent IDOR. A valid session token is insufficient; the AI MUST verify the authenticated user owns the specific `{id}` requested.
- **Vulnerability Mitigation:**
  - **XSS**: The AI MUST encode/escape all user inputs before persistence and before rendering in responses.
  - **CSRF**: The AI MUST implement Synchronizer Token Patterns, Double Submit Cookies, or SameSite cookie attributes for stateful mutations (PUT, POST, DELETE).
  - **DoS/DDoS**: The AI MUST implement rate limiting, pagination, and payload size restrictions to prevent flood and buffer overflow attacks.
  - **Injections (SQL, LDAP, XPath, Command)**: The AI MUST use parameterized queries or prepared statements. Direct string concatenation of user input into queries is STRICTLY FORBIDDEN.
  - **CRLF & Host Header**: The AI MUST sanitize carriage returns (`\r\n`) from user input and MUST NOT dynamically generate links/responses relying solely on the incoming Host header.
  - **Replay Attacks**: The AI MUST enforce countermeasures for state-mutating requests, including timestamps, Time-to-Live (TTL) parameters, and Client-side MACs or One-Time Passwords (OTPs).
  - **MITM**: The AI MUST enforce HTTPS, configure HSTS (HTTP Strict Transport Security), and ensure session tokens are transmitted securely.
- **Security Testing (Penetration & Fuzzing):**
  - The AI MUST simulate White-Box penetration testing by statically analyzing the code for syntax errors, logic flow mismatches, and hardcoded credentials.
  - The AI MUST generate fuzz tests that mutate valid inputs via bit-flipping and random string appendage.
  - The AI MUST generate intelligent fuzz tests based on the API schema/data model to probe for buffer overflows and unhandled exceptions.
- **CQRS Architecture:**
  - The AI MUST implement CQRS when the application experiences significantly differing read vs. write loads, or when business domain logic dictates complex command validations.
  - The AI MUST physically or logically separate Command (write) models/DTOs from Query (read) models/DTOs.
  - The AI MUST handle eventual consistency gracefully when utilizing separate physical data stores for reads and writes.

@Workflow
1. **Scope and Context Definition**: 
   - Identify the specific API endpoint(s), HTTP verbs, request/response schemas, and data classifications.
   - Determine if the task is testing, securing, or architecting (e.g., CQRS).
2. **Security & Vulnerability Hardening** (If writing/reviewing implementation):
   - Apply access control checks (IDOR, Function-level).
   - Apply input sanitization and parameterization (SQLi, XSS, CRLF).
   - Apply protocol constraints (HSTS, CSRF tokens, anti-replay timestamps).
3. **Architecture Mapping** (If CQRS is required):
   - Scaffold the Command interface (asynchronous, transactional storage, returns HTTP 202).
   - Scaffold the Query interface (synchronous, de-normalized view, eventually consistent, returns HTTP 200).
4. **Test Suite Generation**:
   - Step 4a: Create Unit Tests validating single operations with mocked dependencies.
   - Step 4b: Create Functional Tests asserting business rules and complex input combinations.
   - Step 4c: Create Runtime Tests passing invalid configurations, forcing timeouts, and checking error handler gracefulness.
   - Step 4d: Create Security Tests asserting 401/403 on IDOR attempts and invalid token usage.
   - Step 4e: Create Fuzz Tests generating boundary-breaking noise.
5. **Review against Anti-Patterns**:
   - Ensure no test chaining exists.
   - Ensure no sensitive data is cached.
   - Ensure no direct object reference is made without an ownership validation.

@Examples (Do's and Don'ts)

**Principle: Test Independence (No Chaining)**
- [DO]:
  ```python
  def test_delete_user():
      # Setup: Create an isolated user specifically for this test
      user_id = api.post("/users", json={"name": "Test User"}).json()["id"]
      
      # Execute
      response = api.delete(f"/users/{user_id}")
      
      # Assert
      assert response.status_code == 204
  ```
- [DON'T]:
  ```python
  def test_delete_user():
      # Relies on the user created in `test_create_user()` running right before this.
      # Anti-pattern: Test Chaining
      response = api.delete(f"/users/{global_user_id}")
      assert response.status_code == 204
  ```

**Principle: Insecure Direct Object Reference (IDOR) Prevention**
- [DO]:
  ```java
  @GetMapping("/documents/{docId}")
  public ResponseEntity<Document> getDocument(@PathVariable String docId, Principal principal) {
      Document doc = documentService.findById(docId);
      // Validate ownership BEFORE returning the object
      if (!doc.getOwnerId().equals(principal.getName()) && !principal.hasRole("ADMIN")) {
          return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
      }
      return ResponseEntity.ok(doc);
  }
  ```
- [DON'T]:
  ```java
  @GetMapping("/documents/{docId}")
  public ResponseEntity<Document> getDocument(@PathVariable String docId) {
      // Anti-pattern: Blindly trusting the user to only request their own document ID
      Document doc = documentService.findById(docId);
      return ResponseEntity.ok(doc);
  }
  ```

**Principle: OAuth2 Flow Selection**
- [DO]: Use the `client_credentials` grant type for a background cron job synchronizing data between two internal microservices.
- [DON'T]: Use the `implicit` grant type for a highly-trusted backend server interacting with an API, exposing tokens in URLs unnecessarily.

**Principle: Command Query Responsibility Segregation (CQRS)**
- [DO]: Create a `CreateOrderCommand` handled by an `OrderCommandHandler` that writes to an event store, and a separate `GetOrderSummaryQuery` handled by an `OrderQueryHandler` that reads from a fast, flattened NoSQL read-replica.
- [DON'T]: Create a single massive `Order` entity with a generic `updateOrder()` method that locks the database table for writes, causing read timeouts for thousands of users trying to view their order status concurrently.

**Principle: Replay Attack Mitigation**
- [DO]: Require a cryptographic nonce and a `timestamp` in the payload for a high-value financial transaction API, rejecting any request where the timestamp is older than 60 seconds or the nonce has been seen before.
- [DON'T]: Accept an identical POST payload to `/api/transfer-funds` multiple times simply because the static API key in the header is valid.