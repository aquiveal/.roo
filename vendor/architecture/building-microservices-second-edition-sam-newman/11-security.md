# @Domain
Trigger these rules when tasked with designing, implementing, configuring, or reviewing the security architecture of microservices. This includes tasks involving authentication, authorization, secrets management, network security, data encryption (at rest and in transit), continuous integration/delivery security, identity providers (IdP), and inter-service communication protocols.

# @Vocabulary
- **Principle of Least Privilege**: Granting the minimum access a party needs to carry out required functionality, strictly limited to the necessary time period.
- **Defense in Depth**: Implementing multiple layers of security protections (preventative, detective, responsive) rather than relying on a single perimeter.
- **Zero Trust**: An architectural mindset assuming the local network is already compromised; all internal interactions must be explicitly authenticated and authorized.
- **Implicit Trust**: An anti-pattern assuming any call from inside the network perimeter is inherently safe and trusted.
- **NIST Five Functions**: A holistic cybersecurity model comprising Identify, Protect, Detect, Respond, and Recover.
- **Threat Modeling**: The process of analyzing a system from an attacker's perspective to identify valuable assets and vulnerabilities.
- **Datensparsamkeit**: The principle of data frugality; storing only the absolute minimum amount of personally identifiable information (PII) required for business operations.
- **Confused Deputy Problem**: A vulnerability where an upstream party tricks an intermediate, highly-privileged party into performing unauthorized actions on downstream services.
- **Mutual TLS (mTLS)**: A protocol where both the client and the server authenticate each other's identities using certificates.
- **HMAC (Hash-based Message Authentication Code)**: A cryptographic hash used to sign data in transit to ensure it cannot be manipulated, even if sent in the open.
- **JWT (JSON Web Token)**: A standardized, signed (and optionally encrypted) JSON structure used to securely transmit claims (such as identity and roles) between microservices.
- **SSO Gateway**: A centralized proxy that handles redirection to and handshaking with an Identity Provider, passing authentication context to downstream services.
- **Schrödinger Backup**: A backup that has never been tested via restoration, rendering its validity unknown.

# @Objectives
- Build highly secure microservices by shifting from perimeter-based security to Zero Trust environments.
- Protect data rigorously at rest and in transit while practicing extreme data frugality (Datensparsamkeit).
- Decentralize authorization decisions to the individual microservices rather than relying entirely on centralized gateways.
- Automate security practices throughout the delivery lifecycle, including credential rotation, patching, and system rebuilds.
- Prevent cascading security failures by ensuring that compromised microservices yield minimal exploit value.

# @Guidelines

## Core Security Posture
- The AI MUST apply the Principle of Least Privilege to all generated credentials, IAM roles, database access, and network policies. 
- The AI MUST design defenses in depth, combining Preventative (e.g., encryption), Detective (e.g., intrusion detection, logging), and Responsive (e.g., automated rebuilds) controls.
- The AI MUST default to a Zero Trust architecture for all inter-service communication unless specifically instructed that a non-sensitive data zone explicitly permits Implicit Trust.

## Delivery and Automation
- The AI MUST integrate security checks (e.g., static analysis, dependency scanning for known vulnerabilities) into CI/CD pipeline definitions.
- The AI MUST automate infrastructure configurations (Infrastructure as Code) to ensure compromised services can be instantaneously wiped and rebuilt from a clean, version-controlled state.
- The AI MUST specify automated backup processes and MUST enforce mechanisms to regularly test the restoration of these backups to avoid Schrödinger Backups.

## Credentials and Secrets Management
- The AI MUST NOT hardcode secrets, passwords, or API keys in source code.
- The AI MUST utilize dedicated secrets management tools (e.g., HashiCorp Vault, AWS Secrets Manager) for secret distribution and storage.
- The AI MUST scope credentials per microservice instance where possible, avoiding shared global credentials across multiple distinct instances.
- The AI MUST define time-limited credentials and automated rotation policies to minimize the window of opportunity for compromised keys.
- The AI MUST include configuration for scanning source code repositories (e.g., git-secrets, gitleaks) to prevent accidental key commits.

## Securing Data in Transit
- The AI MUST enforce TLS/HTTPS for all external and internal API traffic to prevent visibility by intermediate parties.
- The AI MUST use Mutual TLS (mTLS) to cryptographically verify both client and server identities for service-to-service communication.
- The AI MUST apply HMAC or equivalent cryptographic signatures to payloads if data must be sent without transport-level encryption, ensuring data manipulation is detectable.

## Securing Data at Rest
- The AI MUST utilize well-known, peer-reviewed, standard encryption algorithms and libraries. The AI MUST NOT implement custom cryptographic algorithms.
- The AI MUST use salted password hashing when storing user passwords. Passwords MUST NEVER be stored in plain text or encrypted with reversible cryptographic algorithms.
- The AI MUST enforce Datensparsamkeit by dropping, anonymizing, or masking PII and sensitive data as early as possible.
- The AI MUST physically separate encryption keys from the encrypted data stores.

## Authentication and Authorization
- The AI MUST implement Multi-Factor Authentication (MFA) logic for administrative access or access to highly sensitive systems.
- The AI MUST favor OpenID Connect (OIDC) / OAuth 2.0 over older specifications like SAML.
- The AI MUST NOT put fine-grained authorization logic (e.g., `CAN_REFUND_50_DOLLARS`) in centralized directory services or SSO Gateways. Central directories MUST only provide coarse-grained roles/groups.
- The AI MUST decentralize fine-grained authorization decisions down to the target microservice owning the business functionality.
- The AI MUST prevent the Confused Deputy Problem by ensuring intermediate services (like BFFs or gateways) pass the original user's identity context to downstream microservices using JWTs.
- The AI MUST validate JWT signatures, verify public claims (such as the `exp` expiration field), and retrieve public keys from trusted, secure sources out-of-band.

# @Workflow
1. **Identify**: Begin by establishing the threat model. Identify the data sensitivity levels (e.g., Public, Private, Secret) required for the target microservice and define the required isolation zones.
2. **Configure Identity & Trust**: Set up the environment for Zero Trust. Define mTLS for inter-service communication and configure the SSO Gateway for external requests to extract user identity into a JWT.
3. **Decentralize Authorization**: Implement local authorization checks within the microservice codebase. Ensure the microservice validates the JWT signature and `exp` claim, extracts the user role/ID, and performs context-specific access control.
4. **Secure the Data**: Define targeted encryption at rest for sensitive database columns. Ensure keys are stored in a dedicated Vault. Apply Datensparsamkeit by trimming logging pipelines of PII.
5. **Manage Secrets**: Write Infrastructure as Code to provision least-privilege, time-limited, per-instance database credentials via the secrets manager.
6. **Automate Defense**: Add pre-commit hook configurations for secret scanning, and append dependency vulnerability scanning steps into the CI/CD pipeline code. Ensure automated backup generation and automated restore tests are included in the infrastructure definitions.

# @Examples (Do's and Don'ts)

## Microservice Database Credentials
- **[DO]**: Use a secrets manager to generate a unique, time-limited database credential for *each specific instance* of a microservice dynamically on startup.
- **[DON'T]**: Create a single `db_admin` user and hardcode the username and password into a shared configuration file deployed to all microservice instances.

## Authorization Logic
- **[DO]**: Authenticate the user at the API Gateway to generate a JWT containing `role: customer_support`. Pass the JWT to the `Refund` microservice, which locally executes logic to check if `customer_support` is allowed to issue the requested refund amount.
- **[DON'T]**: Configure the API Gateway to map the user to a role called `ALLOWED_TO_REFUND_100_DOLLARS` and have the gateway blindly approve the request before forwarding it to an implicitly trusting `Refund` microservice.

## JWT Handling
- **[DO]**: Verify the JWT signature using a securely retrieved public key, check the `exp` field to ensure the token is still valid, and limit the JWT payload to necessary identity claims to keep the header size small.
- **[DON'T]**: Accept a JWT without validating the cryptographic signature, ignore the `exp` claim, or pack 10,000 granular permissions into the JWT payload causing HTTP header size limits to be breached.

## Data Frugality (Datensparsamkeit)
- **[DO]**: Log the fact that a user transaction occurred by logging a generated Correlation ID and a masked user identifier (e.g., `User: ***-789`).
- **[DON'T]**: Write the user's full name, physical address, and plain-text IP address to the centralized log aggregation system for long-term storage.

## Inter-Service Communication
- **[DO]**: Require the `Shipping` microservice to authenticate requests coming from the `WebShop` microservice using mTLS, even though both reside inside the same corporate VPC.
- **[DON'T]**: Allow the `Shipping` microservice to accept plain-text HTTP requests from any IP address located within the internal `10.0.0.0/8` corporate subnet.

## Cryptography
- **[DO]**: Use industry-standard algorithms (e.g., AES-GCM) provided by mature, actively maintained libraries (like libsodium or Tink), and store the encryption keys in a dedicated hardware security module (HSM) or Key Management Service (KMS).
- **[DON'T]**: Write a custom bit-shifting encryption loop and store the symmetric encryption key in a hidden table within the same database as the encrypted data.