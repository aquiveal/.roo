# @Domain
Security implementation, system architecture, code generation, configuration management, and dependency auditing for web applications, APIs, and distributed systems. These rules activate whenever the AI is tasked with generating data access layers, handling user input, managing authentication/sessions, designing API endpoints, configuring servers/containers, or managing application secrets.

# @Vocabulary
- **Injection**: An attack on a parser or interpreter that relies on executing user-supplied input (e.g., SQL Injection, XML External Entity/XXE Injection).
- **Session Hijacking/Fixation**: Attacks where an adversary steals or forces a specific session ID to gain unauthorized access to a user's authenticated session.
- **PRNG (Pseudorandom Number Generator)**: A cryptographic algorithm used to generate highly entropic, unguessable session IDs.
- **XSS (Cross-Site Scripting)**: An attack where a service renders user input directly into HTML without input escaping, allowing malicious scripts to execute in a victim's browser.
- **Direct Object Access**: A vulnerability where internal database IDs are exposed in URLs, allowing attackers to probe sequentially for unauthorized data.
- **Directory Traversal**: An attack using `../` or `..\` strings in input to navigate outside the intended directory and access/overwrite unauthorized files.
- **HSTS (HTTP Strict Transport Security)**: A protocol feature that prevents clients from negotiating their way to insecure (non-HTTPS) protocols.
- **KMS (Key Management Service) / Vault**: Secure infrastructure for generating, storing, and issuing encryption keys and secrets dynamically.
- **CSRF (Cross-Site Request Forgery)**: An attack that tricks a victim's browser into executing unwanted state-changing actions on a trusted site.
- **SameSite Cookie**: A cookie attribute that prevents the browser from sending the cookie if the document's origin differs from the target's origin.
- **Pie Crust Defense**: A flawed security model that strictly guards the external perimeter but implicitly trusts all internal service-to-service communication.
- **Core Dump**: A memory dump of an application that can inadvertently leak plaintext passwords and encryption keys to the filesystem.

# @Objectives
- Bake security intrinsically into all code and infrastructure configurations, treating it as a foundational architecture requirement rather than an afterthought.
- Eliminate OWASP Top 10 vulnerabilities by default in all generated code and configurations.
- Ensure data confidentiality and integrity by protecting sensitive data both in transit and at rest.
- Restrict systemic attack surfaces through the Principle of Least Privilege and isolation of network traffic.
- Design cynical, defensive APIs that inherently distrust all caller input, even from internal sources.

# @Guidelines

### 1. Injection Prevention
- When generating database queries, the AI MUST strictly use parameterized queries or prepared statements with placeholders. The AI MUST NEVER concatenate strings to build queries.
- When configuring or instantiating XML parsers, the AI MUST explicitly disable inline Document Type Declarations (DTDs) and External Entities to prevent XXE injection attacks.
- When handling data retrieved from a database, the AI MUST treat it as untrusted user input, as it may have originated from a compromised or malicious source.

### 2. Authentication & Session Management
- When generating URLs or routing configurations, the AI MUST NOT include session identifiers in query parameters or URL paths.
- When managing sessions, the AI MUST generate long, highly entropic session IDs using a cryptographic PRNG.
- When generating authentication flows, the AI MUST explicitly generate a fresh session ID immediately upon successful login to prevent session fixation.
- When storing passwords, the AI MUST apply a strong, modern cryptographic hash algorithm with a unique salt. The AI MUST NOT store passwords in plaintext or use outdated algorithms like SHA-1.
- When generating "forgotten password" flows, the AI MUST NOT email the user's password. It MUST use secure, time-limited reset tokens.
- When configuring account lockout policies, the AI MUST NOT lock out users after a small number of rapid failures (e.g., 3 attempts), to account for automated retries from multiple user devices.
- When communicating between internal services, the AI MUST implement TLS and authenticate the caller. The AI MUST NOT rely on IP addresses for trust or use a "pie crust" defense.

### 3. Cross-Site Scripting (XSS) Prevention
- When rendering user input into a UI, the AI MUST aggressively scrub input on arrival and escape output on rendering.
- When building HTML, the AI MUST use HTML generation libraries/templating engines that escape variables by default. The AI MUST NOT concatenate strings to build HTML.
- When building administrative GUIs or log viewers, the AI MUST apply the exact same strict XSS escaping rules as user-facing applications.

### 4. Access Control & Authorization
- When designing API routes for specific resources, the AI MUST avoid sequential database IDs in URLs. The AI MUST use session-sensitive URLs (e.g., `/users/me`), randomly generated UUIDs, or session-scoped mapping tables.
- When a caller requests a resource they are not authorized to access, the AI MUST return a `404 Not Found` rather than a `403 Forbidden` to prevent leaking the existence of the resource (unless the system explicitly requires distinguishing unauthenticated vs. unauthorized states for known public resources).
- When handling file uploads, the AI MUST treat the client-provided filename as an arbitrary, untrusted string. The AI MUST generate a unique, random key to be used as the actual filesystem name, mapping the original name only in the database.
- When reading or writing files based on user input, the AI MUST sanitize the input to completely strip directory traversal characters (`../`, `..\`).

### 5. Security Misconfiguration
- When generating setup scripts or configurations, the AI MUST NOT include or rely upon default admin credentials (e.g., admin/admin).
- When writing configurations for third-party servers (e.g., MongoDB, Redis, ZooKeeper), the AI MUST explicitly configure authentication mechanisms and disable anonymous access.
- When defining network architectures or Docker compose files, the AI MUST bind administrative and internal-only traffic to separate, isolated Network Interface Cards (NICs) or virtual networks, strictly separated from public-facing traffic.
- When generating deployment bundles, the AI MUST explicitly exclude any default sample applications provided by frameworks or servers.
- When configuring admin accounts, the AI MUST mandate distinct personal accounts and MUST NOT use shared/group accounts.

### 6. Sensitive Data Exposure
- When generating web server configurations, the AI MUST enforce HTTP Strict Transport Security (HSTS) to prevent protocol downgrades.
- When handling decryption of data, the AI MUST authorize the decryption action based on the user's privileges, not the server's overarching privileges.
- When integrating with AWS or HashiCorp environments, the AI MUST utilize KMS or Vault for secrets. The AI MUST explicitly zero-out or expunge decryption keys and plaintext passwords from application memory immediately after use.

### 7. Attack Protection & CSRF
- When creating public APIs, the AI MUST configure rate limiting, request throttling, and API key validation (via API Gateways) to limit data compromise speed.
- When logging bad requests, the AI MUST log the requests grouped by source principal to allow pattern analysis of attacks.
- When designing state-changing web endpoints (POST, PUT, DELETE, PATCH), the AI MUST enforce the use of anti-CSRF tokens.
- When configuring session cookies, the AI MUST utilize the `SameSite=strict` attribute for state-changing operations, optionally separating read (non-strict) and write (strict) cookies.

### 8. Dependency Auditing
- When creating CI/CD pipeline configurations, the AI MUST integrate automated dependency auditing tools (e.g., OWASP Dependency Check) configured to break the build if CVEs are detected in libraries or build plugins.

### 9. API Security
- When writing API validation logic, the AI MUST NOT assume that possession of an unguessable URL grants authorization. The API MUST re-authorize the incoming request against the caller's identity.
- When generating data parsers (JSON, XML, YAML), the AI MUST implement strict bounds and type checking to defend against malicious fuzzing and buffer/memory exhaustion.

### 10. Principle of Least Privilege & Configured Passwords
- When creating Dockerfiles or systemd service files, the AI MUST execute the application as a strictly unprivileged, application-specific user. The AI MUST NEVER run the application as `root` or `Administrator`.
- When configuring production systems, the AI MUST disable core dumps to prevent memory dumps from leaking plaintext secrets to the filesystem.
- When generating application configurations, the AI MUST separate database passwords into an isolated configuration file. The AI MUST configure the OS permissions of this file so it is readable ONLY by the application-specific user.

# @Workflow
1. **Input & Parser Hardening**: 
   - Define strict validation rules for all incoming data.
   - Configure XML/JSON parsers to reject external entities and enforce size limits.
2. **Authentication & Session Bootstrapping**: 
   - Establish secure, PRNG-backed session generation.
   - Enforce HTTPS/HSTS.
   - Configure `SameSite=strict` and `Secure` flags on cookies.
3. **Authorization & Object Access**:
   - Implement strict permission checks on all resource access.
   - Replace sequential IDs in URLs with UUIDs or contextual endpoints (`/me`).
   - Obfuscate unauthorized access responses by returning `404 Not Found`.
4. **Data Privacy & Cryptography Configuration**:
   - Implement modern hashing (salt + strong hash) for passwords.
   - Integrate Key Management Services (KMS/Vault) to fetch secrets dynamically.
   - Ensure memory is wiped of keys immediately post-use.
5. **Infrastructure Isolation & Least Privilege**:
   - Strip root privileges from runtime configurations (Dockerfiles/Systemd).
   - Disable OS-level core dumps.
   - Partition admin/internal APIs onto isolated networks/ports.
   - Add automated CVE scanning to the CI/CD pipeline definition.

# @Examples (Do's and Don'ts)

### SQL Injection
- **[DO]**:
  ```java
  String query = "SELECT * FROM STUDENT WHERE NAME = ?";
  PreparedStatement stmt = connection.prepareStatement(query);
  stmt.setString(1, name);
  ResultSet results = stmt.executeQuery();
  ```
- **[DON'T]**:
  ```java
  // Anti-pattern explicitly warned against: String concatenation
  String query = "SELECT * FROM STUDENT WHERE NAME = '" + name + "';";
  ```

### File Uploads & Directory Traversal
- **[DO]**:
  ```python
  # Treat client filename as arbitrary string, generate random UUID for filesystem
  file_extension = extract_extension(request.files['upload'].filename)
  safe_internal_name = f"{uuid.uuid4()}{file_extension}"
  save_to_disk(request.files['upload'], safe_internal_name)
  save_to_database(original_name=request.files['upload'].filename, internal_name=safe_internal_name)
  ```
- **[DON'T]**:
  ```python
  # Anti-pattern: Trusting client filename, leading to directory traversal/overwrite
  save_to_disk(request.files['upload'], f"/var/www/uploads/{request.files['upload'].filename}")
  ```

### Unauthorized Resource Access (Information Leakage)
- **[DO]**:
  ```javascript
  if (!user.isAuthorizedToView(resourceId)) {
      // Obscure existence of the resource
      return res.status(404).send("Not Found");
  }
  ```
- **[DON'T]**:
  ```javascript
  if (!user.isAuthorizedToView(resourceId)) {
      // Anti-pattern: Leaks that the resource actually exists
      return res.status(403).send("Forbidden");
  }
  ```

### Session ID Management
- **[DO]**:
  ```http
  Set-Cookie: SID=31d4d96e407aad42; Secure; HttpOnly; SameSite=strict
  ```
- **[DON'T]**:
  ```html
  <!-- Anti-pattern: Session ID in URL allows hijacking via copy/paste or referer headers -->
  <a href="http://www.example.com/checkout?session_id=31d4d96e407aad42">Checkout</a>
  ```

### XML Parsing (XXE Prevention)
- **[DO]**:
  ```java
  DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
  // Explicitly disable DTDs and external entities
  dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
  dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
  ```
- **[DON'T]**:
  ```java
  // Anti-pattern: Default factory is vulnerable to XXE
  DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
  Document doc = dbf.newDocumentBuilder().parse(inputStream);
  ```