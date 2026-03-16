# @Domain
These rules are triggered whenever the AI is tasked with designing, architecting, reviewing, or writing code for data storage systems, event logs, analytics pipelines, machine learning feature engineering, or user-tracking mechanisms. This includes tasks involving data collection schemas, database migrations, data retention policies, algorithmic decision-making systems, and integration with payment or external vendor systems.

# @Vocabulary
- **Datensparsamkeit (Data Minimization)**: The principle of collecting and storing only the absolute minimum amount of personal data required for a specified, explicit purpose, and retaining it no longer than necessary. Runs counter to the speculative "big data" philosophy.
- **Right to be Forgotten (Right to Erasure)**: A legal right (e.g., under GDPR) granting individuals the ability to have their personal data completely erased from a system upon request.
- **Immutable Constructs**: Data storage mechanisms, such as append-only logs or event streams, designed to never be modified or deleted. These pose inherent engineering challenges for data erasure requirements.
- **Derived Datasets**: Data representations created by transforming or processing source data, such as machine learning training data, materialized views, or analytical cubes.
- **Compelled Disclosure**: The risk of governments or police forces forcing companies to hand over stored data, potentially endangering users (e.g., revealing criminalized behaviors or locations).
- **Automated Harm**: Profound negative consequences for individuals resulting from automated decision-making systems (e.g., loan approvals, insurance coverage, job interview selection, or criminal suspicion).
- **GDPR / CCPA / EU AI Act**: Major regulatory frameworks governing data protection, privacy, and artificial intelligence safety that must fundamentally influence system architecture.
- **PCI (Payment Card Industry) Standards**: Strict adherence guidelines for payment processing requiring frequent evaluations from independent auditors.
- **SOC Type 2**: Service Organization Control standards requiring third-party audits to verify software vendor adherence to security and privacy practices.

# @Objectives
- Treat data privacy, ethics, and legal compliance as foundational architectural constraints, equal in importance to scalability, reliability, and maintainability.
- Balance the business value of data collection against the societal impact, human rights, and safety of the individuals whose data is being processed.
- Systematically mitigate the risks of data leaks, adversarial compromise, and hostile compelled disclosure by refusing to store unnecessary, sensitive, or speculative data.
- Engineer proactive solutions for the paradox of data erasure within immutable data structures and derived datasets (including ML models).

# @Guidelines

### 1. Enforce Datensparsamkeit (Data Minimization)
- **Reject Speculative Storage**: The AI MUST categorically reject the "Big Data" philosophy of storing vast amounts of data speculatively "just in case it turns out to be useful in the future."
- **Explicit Purpose Binding**: Every field in a schema designed to capture personal data MUST be justified by a specific, currently active feature or business requirement. 
- **Time-to-Live (TTL)**: The AI MUST define explicit retention periods and automatic deletion mechanisms for all personal data. Data must not be kept longer than necessary for its original purpose.

### 2. Architect for the Right to be Forgotten
- **Erasure in Immutable Logs**: When implementing append-only logs, event sourcing, or stream processing, the AI MUST engineer a mechanism to comply with erasure requests. (e.g., Utilizing crypto-shredding, tombstone records, or rewriting/compacting logs to purge personal data).
- **Derived Dataset Propagation**: The AI MUST account for the deletion of user data that has already propagated into derived datasets, analytics warehouses, and training data for machine learning models. The system must support recomputing or purging derived data to eliminate traces of erased users.

### 3. Mitigate Compelled Disclosure and Adversarial Leaks
- **Threat Modeling for Vulnerable Populations**: The AI MUST evaluate data schemas for attributes that could reveal criminalized or highly sensitive behaviors (e.g., location data revealing travel to abortion clinics, data inferring sexual orientation like homosexuality in hostile jurisdictions).
- **IP and Location Scrubbing**: The AI MUST NOT design systems that indefinitely log raw IP addresses or granular geographic location data over time unless absolutely critical to the core application loop. If required, the AI must implement immediate aggregation, anonymization, or truncation.
- **Cost-Benefit of Liability**: The AI MUST evaluate and document the storage cost not just in terms of cloud infrastructure (e.g., Amazon S3 billing), but in terms of legal liability, fines, and reputational damage if the data is compromised.

### 4. Prevent Automated Harm and Bias
- **High-Stakes Decision Safeguards**: If the AI is designing systems that impact profound individual consequences (loans, insurance, job interviews, crime detection, or news feed ranking), it MUST enforce architectural safety nets, logging for bias auditing, and human-in-the-loop review capabilities.

### 5. Enforce Compliance and Auditability
- **PCI and SOC 2 Readiness**: When integrating with payment processors or building B2B SaaS platforms, the AI MUST design data flows that support strict separation of concerns, continuous compliance, and readiness for third-party independent audits.

# @Workflow
When tasked with designing a new data system, schema, or analytics pipeline, the AI MUST execute the following algorithm:

1. **Data Purpose & Minimization Review**:
   - Audit the requested data fields.
   - Strip out any fields intended for "future speculative analytics."
   - Assign a TTL (Time-to-Live) to all remaining personal data fields.

2. **Erasure Strategy Formulation**:
   - Identify if the target storage utilizes immutable constructs (e.g., Kafka logs, EventStore).
   - Define the exact technical mechanism for how a "Right to be Forgotten" request will be executed across both the primary system of record AND all downstream derived datasets/ML models.

3. **Threat & Compelled Access Modeling**:
   - Analyze the schema for high-risk data (IP histories, location tracking, behavioral inferences).
   - Apply anonymization or aggregation to this data before it is written to persistent storage.
   - Document the liability risk if the data were subpoenaed or stolen.

4. **Algorithmic Impact Assessment**:
   - If the data feeds an automated decision engine, flag the system design with warnings regarding potential bias.
   - Insert architectural hooks for auditing the decision-making process.

5. **Audit & Compliance Mapping**:
   - Verify if the system touches payment data (apply PCI constraints) or serves enterprise vendors (apply SOC 2 audit logging constraints).

# @Examples (Do's and Don'ts)

### Data Minimization (Datensparsamkeit)
- **[DO]**: Design schemas that collect only what is needed for the transaction, and automatically drop it afterward.
  ```sql
  -- DO: Minimal, purpose-driven schema with TTL strategy
  CREATE TABLE user_sessions (
      session_id UUID PRIMARY KEY,
      user_id UUID REFERENCES users(id),
      login_time TIMESTAMP NOT NULL,
      -- IP address is truncated/anonymized at the application layer before insertion
      anonymized_ip VARCHAR(45),
      expires_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP + INTERVAL '30 days'
  );
  ```
- **[DON'T]**: Implement speculative "store everything" tables.
  ```sql
  -- DON'T: Speculative Big Data collection
  CREATE TABLE user_tracking_events (
      event_id UUID PRIMARY KEY,
      user_id UUID,
      raw_ip_address VARCHAR(45),
      exact_gps_location POINT,
      every_click_xy_coordinate JSONB,
      -- Retained forever "just in case data scientists need it later"
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

### Handling Erasure in Immutable Constructs
- **[DO]**: Implement crypto-shredding for append-only event logs so that discarding the encryption key renders the personal data permanently inaccessible without modifying the immutable log.
  ```json
  // DO: Event sourcing payload using Crypto-Shredding
  {
    "eventType": "UserRegistered",
    "timestamp": "2025-10-12T08:00:00Z",
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "encryptedPersonalInfo": "U2FsdGVkX1+...[Encrypted with User-Specific Key]...",
    "keyId": "key-123e4567"
  }
  ```
- **[DON'T]**: Store plaintext personal data in an immutable Kafka topic or EventStore where it cannot be selectively deleted to comply with GDPR.
  ```json
  // DON'T: Plaintext PII in an immutable log
  {
    "eventType": "UserRegistered",
    "timestamp": "2025-10-12T08:00:00Z",
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "email": "jane.doe@example.com",
    "homeAddress": "123 Main St..."
  }
  ```

### Compelled Disclosure & Vulnerable Populations
- **[DO]**: Aggregate location data so that individual visits to sensitive locations (e.g., clinics) cannot be reconstructed by adversaries or law enforcement.
  ```python
  # DO: Truncate location to zip code or broad region before storing
  def process_location_data(raw_lat, raw_lon):
      region_polygon = get_broad_region(raw_lat, raw_lon)
      store_to_analytics_db(region_polygon)
      # Raw coordinates are dropped from memory
  ```
- **[DON'T]**: Build systems that indefinitely track and store raw IP addresses and granular GPS coordinates of user movements.
  ```python
  # DON'T: Store granular, identifiable tracking data
  def process_location_data(user_id, raw_ip, raw_lat, raw_lon):
      db.execute(
          "INSERT INTO user_movement_history (user_id, ip, lat, lon, time) VALUES (?, ?, ?, ?, ?)",
          (user_id, raw_ip, raw_lat, raw_lon, current_time())
      )
  ```