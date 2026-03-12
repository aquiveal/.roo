# @Domain
Trigger these rules when tasked with designing, implementing, evaluating, or refactoring the security architecture of distributed systems and microservices. This includes tasks involving authentication and authorization, secret management, data encryption (at rest and in transit), threat modeling, identity provisioning, CI/CD security automation, API gateway security, and vulnerability remediation.

# @Vocabulary
- **Principle of Least Privilege**: Granting the absolute minimum access required for a party (human or service) to carry out its function, strictly limited to the necessary time period.
- **Defense in Depth**: Utilizing multiple, overlapping layers of security controls (Preventative, Detective, Responsive) so that if one fails, others remain.
- **NIST Five Functions**: Identify, Protect, Detect, Respond, Recover. A holistic model for cybersecurity.
- **Threat Modeling**: The process of analyzing a system from an attacker's perspective to identify vulnerabilities, high-value assets, and appropriate security controls.
- **Schrödinger Backup**: A backup whose validity and restorability are completely unknown until restoration is actively attempted.
- **Implicit Trust**: Assuming all network traffic inside a defined perimeter is inherently safe. (A high-risk anti-pattern in modern microservices).
- **Zero Trust (Perimeterless Computing)**: Operating under the assumption that the network is already compromised; verifying and authenticating every single call, regardless of origin.
- **Datensparsamkeit (Data Frugality)**: The principle of capturing, processing, and storing only the absolute minimum amount of personal data required to fulfill a business operation. 
- **mTLS (Mutual TLS)**: A protocol where both the client and the server authenticate each other's identities using cryptographic certificates.
- **HMAC (Hash-based Message Authentication Code)**: A mechanism used to sign data being sent in the open to guarantee it has not been manipulated.
- **Salted Password Hashing**: Cryptographically hashing passwords with a unique random string (salt) before storage to prevent dictionary and rainbow table attacks.
- **Principal**: An entity (human user, external system, or internal microservice) requesting authentication and authorization.
- **Confused Deputy Problem**: A vulnerability where an upstream party tricks an intermediate service (the deputy) into executing unauthorized actions on a downstream service using the deputy's elevated privileges.
- **JSON Web Token (JWT)**: A standard for creating a signed (and optionally encrypted) JSON data structure used to transmit verified claims about an authenticated principal across distributed services.
- **SSPL / Licensing Context**: An awareness that licensing of underlying monitoring/security tools (like Elasticsearch) may impact architectural choices and vendor lock-in.

# @Objectives
- Enforce the Principle of Least Privilege across all human, infrastructure, and microservice interactions.
- Architect multiple layers of defense (Defense in Depth) so no single point of failure compromises the system.
- Eliminate implicit trust networks by designing Zero Trust communication architectures for sensitive data zones.
- Guarantee the integrity, confidentiality, and authenticity of data both in transit and at rest.
- Decentralize fine-grained authorization logic, pushing it down to the owning microservice to maintain independent deployability.
- Automate all aspects of security operations, including secret rotation, vulnerability scanning, and infrastructure rebuilding.

# @Guidelines

## Core Security Posture
- The AI MUST apply the NIST Five Functions (Identify, Protect, Detect, Respond, Recover) to all architectural security evaluations.
- The AI MUST enforce threat modeling from an external attacker's perspective before recommending preventative controls.
- The AI MUST categorize proposed security controls into Preventative, Detective, and Responsive buckets to ensure balanced defense in depth.
- The AI MUST prioritize automation for security tasks, specifically for credential rotation, patching, and environment rebuilding.

## Secrets and Credential Management
- The AI MUST strongly advocate against hardcoding secrets, passwords, SSH keys, or API keys in source code or plain-text configuration files.
- The AI MUST recommend integrating pre-commit secret scanning tools (e.g., git-secrets, gitleaks) into the CI/CD pipeline.
- The AI MUST ensure credentials are given the tightest possible scope. Each microservice instance MUST have its own unique, isolated credentials (e.g., separate DB users per service instance).
- The AI MUST recommend the use of dedicated, centralized secret management tools (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault).
- The AI MUST design secret distribution so that credentials are short-lived, auto-rotating, and immediately revocable without requiring code redeployments (e.g., leveraging dynamic configuration reloading or `consul-template`).
- The AI MUST mandate Multi-Factor Authentication (MFA) for human access to critical systems, source control, and infrastructure environments.

## Infrastructure and Delivery Pipeline
- The AI MUST embed security checks into the continuous integration pipeline, explicitly requiring SAST (e.g., Brakeman), DAST (e.g., OWASP ZAP), and dependency vulnerability scanning (e.g., Snyk, GitHub code scanning).
- The AI MUST ensure that infrastructure is immutable and reproducible via Infrastructure as Code (IaC). In the event of a breach (e.g., a rootkit), the recovery strategy MUST be to completely wipe and automatically rebuild the environment from source.
- The AI MUST enforce regular, automated restoration testing of backups to prevent "Schrödinger Backups". Backups MUST be stored in isolated environments (e.g., separate cloud accounts) and MUST be encrypted.

## Network and Trust Architecture
- The AI MUST reject Implicit Trust network models for systems handling Private or Secret data.
- The AI MUST recommend a Zero Trust architecture where every inter-microservice request is authenticated and authorized.
- The AI MUST segment microservices into security zones based on the highest data sensitivity classification they handle (e.g., Public, Private, Secret). Lower-security zones MUST NOT have direct access to higher-security zones.

## Securing Data (In Transit and At Rest)
- The AI MUST require TLS (HTTPS) for all data in transit to ensure server identity and data confidentiality.
- The AI MUST enforce Mutual TLS (mTLS) for verifying client identity in inter-microservice communication.
- If data must be sent over unencrypted channels, the AI MUST require HMAC to prevent data manipulation.
- The AI MUST strictly prohibit the invention of custom cryptographic algorithms. Only industry-standard, well-known cryptographic libraries MUST be recommended.
- The AI MUST enforce *Datensparsamkeit* (Data Frugality): recommend stripping or masking Personally Identifiable Information (PII) as early as possible and deleting it when no longer strictly necessary.
- The AI MUST ensure cryptographic keys for data at rest are stored securely and externally from the database where the encrypted data resides.

## Authentication and Authorization
- The AI MUST differentiate between coarse-grained and fine-grained authorization. Coarse-grained checks (e.g., "Is this user a STAFF member?") MAY occur at the API Gateway. Fine-grained checks (e.g., "Is this STAFF member allowed to issue a $500 refund?") MUST be executed locally by the specific microservice owning that domain.
- The AI MUST NOT leak fine-grained, microservice-specific roles into central directory services.
- The AI MUST prevent the Confused Deputy Problem by passing the original user's identity and claims down to the target microservice, rather than having downstream services implicitly trust the intermediate caller.
- The AI MUST utilize JSON Web Tokens (JWTs) for decentralized authorization.
- The AI MUST ensure JWTs are generated per-request at the gateway and signed securely. 
- The AI MUST ensure downstream microservices validate the JWT signature (via securely distributed public keys) and check standard public claims (e.g., `exp` for expiration).
- The AI MUST flag long-lived JWTs in asynchronous workflows as a security risk and require architectural mitigations.

# @Workflow
When tasked with securing a microservice architecture or evaluating an existing design, the AI MUST execute the following algorithmic process:

1. **Identify & Threat Model:** 
   - Analyze the system boundary, the types of data stored (Public, Private, PII, Secret), and potential external/internal attackers.
   - Categorize microservices into isolated security zones based on data sensitivity.
2. **Design Data Protection:** 
   - Apply *Datensparsamkeit*; eliminate unnecessary data collection.
   - Specify encryption algorithms for data at rest and define isolated key storage (e.g., Vault).
   - Enforce TLS/mTLS for all data in transit.
3. **Configure Authentication & Authorization:**
   - Define the human MFA and SSO strategy (e.g., OpenID Connect).
   - Map coarse-grained roles to the API Gateway.
   - Design the JWT generation, signing, and transmission flow to downstream services.
   - Push fine-grained permission logic directly into the specific target microservices.
4. **Implement Secret & Credential Management:**
   - Define unique, tightly-scoped credentials for every individual microservice.
   - Establish automated rotation schedules and dynamic revocation paths.
5. **Automate Security Operations (CI/CD):**
   - Inject dependency scanning, secret scanning (gitleaks), and DAST/SAST into the build pipeline.
   - Define immutable infrastructure rebuild processes for incident recovery.
   - Schedule automated backup encryption and restoration validation.
6. **Validate Defense in Depth:**
   - Review the architecture to ensure Preventative, Detective, and Responsive controls exist independently of one another.

# @Examples (Do's and Don'ts)

## Microservice Database Credentials
- **[DO]** Provision unique, auto-rotating database credentials for each specific microservice instance via a central secret manager. Inject these dynamically using a tool like `consul-template`.
- **[DON'T]** Hardcode a single, shared database username and password across multiple instances of a microservice, or across different microservices. 

## Decentralized Authorization (Preventing Confused Deputy)
- **[DO]** Have the API Gateway authenticate the user via OpenID Connect, generate a short-lived JWT containing the user's ID and coarse roles, and pass it in the `Authorization` header. The downstream `OrderService` validates the JWT signature and verifies that the `sub` (user ID) in the token matches the requested Order ID.
- **[DON'T]** Have the `WebShop` BFF authenticate the user and then make an unauthenticated internal network call to the `OrderService` requesting user data, relying on the `OrderService` implicitly trusting the `WebShop`'s IP address.

## Managing Application Secrets
- **[DO]** Use HashiCorp Vault to issue a time-limited AWS IAM role specifically scoped for the `ImageProcessor` service to access exactly one S3 bucket for exactly 15 minutes.
- **[DON'T]** Commit an AWS Access Key ID and Secret Access Key into the `ImageProcessor` GitHub repository, even if the repository is private.

## Security Zones and Data Privacy (Datensparsamkeit)
- **[DO]** Strip PII from analytics events at the edge. Run the `MedicalRecords` microservice in a strictly isolated "Secret" network zone requiring mTLS and specific JWT claims to accept inbound traffic.
- **[DON'T]** Store full user profiles including ages, genders, and names in the `RecommendationEngine` database when only an anonymized ID and a list of previously purchased genres are needed to generate a recommendation.

## Backups and Recovery
- **[DO]** Automate nightly, encrypted database backups sent to an isolated, separate cloud provider account. Include an automated CI/CD stage that provisions a temporary database, restores the backup, and runs data integrity checks before tearing it down.
- **[DON'T]** Save database dumps to the local filesystem of the database server and assume they are valid without ever testing the restoration process.