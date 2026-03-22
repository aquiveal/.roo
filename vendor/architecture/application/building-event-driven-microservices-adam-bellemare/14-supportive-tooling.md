# @Domain
These rules MUST be activated when the AI is executing tasks related to DevOps, infrastructure, configuration, scaffolding, monitoring, or security for Event-Driven Microservices (EDMs). This includes creating event streams, configuring event brokers (e.g., Kafka, Pulsar), defining schema registries, writing Container Management System (CMS) configurations (e.g., Kubernetes, Helm), configuring CI/CD pipelines, establishing access control lists (ACLs), setting up monitoring/autoscaling metrics, and writing infrastructure-as-code (IaC) for cluster creation.

# @Vocabulary
- **Microservice-to-Team Assignment System**: A centralized registry tracking the strict ownership of microservices and event streams to specific business teams to manage fine-grained DevOps permissions.
- **Single Writer Principle**: An architectural rule dictating that an event stream has one, and only one, producing microservice.
- **Metadata Tagging**: Key-value pairs attached to event streams to designate properties such as Stream owner, PII (Personally Identifiable Information), Financial information, Namespace, and Deprecation.
- **Quotas**: Event broker limits (e.g., CPU processing time, network I/O) applied to producers and consumers to prevent cluster saturation and accidental Denial of Service (DoS).
- **Schema Registry**: A centralized service that stores event schemas, issuing a unique ID for each schema so payloads only transport the ID, saving bandwidth and enabling data discovery.
- **Offset Management**: The controlled, manual adjustment of a consumer's position in an immutable log (Application reset to beginning, advance to latest, or recover to a specific point in time).
- **ACLs (Access Control Lists)**: Strict permission boundaries (READ, WRITE, CREATE, DELETE, MODIFY, DESCRIBE) enforced at the event broker level to guarantee bounded contexts and identify orphaned streams.
- **Consumer Offset Lag**: The difference in event count between the most recent event in a stream and the last event processed by a consumer group.
- **Hysteresis**: A tolerance threshold or delay loop used in autoscaling logic to prevent a system from endlessly scaling up and down due to fluctuating lag.
- **Programmatic Bringup**: The use of Infrastructure-as-Code to automatically provision event brokers, compute resources, tooling, and cross-cluster replication for isolated testing or scaling.
- **Topology Visualization**: The process of mapping microservice dependencies and interconnectedness by evaluating event stream ACLs rather than relying on self-reporting.

# @Objectives
- The AI MUST enforce absolute ownership and isolation for every microservice and event stream generated, utilizing metadata tags and ACLs.
- The AI MUST automate and standardize the scaffolding of new microservices, ensuring all foundational tools (CI/CD, permissions, logging, schemas) are configured out-of-the-box.
- The AI MUST configure infrastructure to prevent cascading failures using broker quotas, lag monitoring, and autoscaling hysteresis.
- The AI MUST implement state management utilities that allow self-serve, atomic resets of application state, offsets, and internal streams without jeopardizing neighboring systems.
- The AI MUST decouple schema definitions from event payloads by integrating a schema registry pattern.
- The AI MUST establish traceable data lineages and topology graphs strictly derived from infrastructural permissions (ACLs).

# @Guidelines

## Ownership and Metadata
- The AI MUST explicitly assign an owner to every microservice and event stream it configures.
- The AI MUST apply the following metadata tags to all event stream configurations:
  - `owner`: The specific service/team responsible.
  - `pii`: Boolean indicating Personally Identifiable Information.
  - `financial`: Boolean indicating billing/revenue data.
  - `namespace`: The bounded context the stream belongs to.
  - `status`: Active or `deprecated`.
- When an event stream requires breaking changes, the AI MUST tag the legacy stream as `deprecated` and verify that a mechanism exists to notify downstream consumers.

## Stream Configuration and Quotas
- When defining an event stream, the AI MUST explicitly declare `partition count`, `retention policy`, and `replication factor` based on the data's volume and business criticality.
- The AI MUST configure event broker quotas for every producer and consumer to prevent cluster resource saturation.
- The AI MUST disable or vastly increase quotas for producers ingesting data from third-party or external synchronous APIs to prevent external data dropping during ingestion surges.

## Schema Management
- The AI MUST NOT embed full schemas within event payload generation code. It MUST configure the producer to register/fetch the schema from a Schema Registry, obtain the schema ID, and append only the ID to the serialized event.
- The AI MUST configure automated notification hooks (via CI/CD or registry webhooks) that trigger alerts to downstream consumer teams when an upstream schema is modified.

## Offset and State Management
- The AI MUST provide scripts or configurations for three distinct offset management scenarios when building DevOps tooling:
  1. Reset to earliest (for full reprocessing).
  2. Advance to latest (to skip stale data).
  3. Reset to a specific timestamp (for point-in-time recovery).
- When writing procedures to reset a stateful microservice, the AI MUST sequence the operations to:
  1. Delete the microservice's internal and changelog streams.
  2. Purge external state store materializations (e.g., DynamoDB, Bigtable).
  3. Reset consumer group offsets to the beginning for input streams.
- State reset capabilities MUST be constrained by RBAC/IAM targeting the specific microservice owner.

## Security and Access Control Lists (ACLs)
- The AI MUST adhere to the Single Writer Principle: Only ONE microservice can be granted `WRITE` or `CREATE` permissions for a specific output event stream.
- The AI MUST assign `CREATE`, `WRITE`, and `READ` permissions for internal and changelog event streams ONLY to the owning microservice. No external service may be granted `READ` access to these streams.
- The AI MUST utilize ACL configurations as the source of truth to programmatically discover orphaned streams (streams with no consumers) or orphaned microservices (services producing to streams with no consumers).

## Monitoring and Container Management
- The AI MUST configure Consumer Offset Lag monitoring to trigger autoscaling.
- The AI MUST explicitly include a hysteresis loop (a tolerance threshold/cooldown period) in autoscaling rules to prevent thrashing (endless scale up/down cycles).
- For high-volume streams, the AI MUST configure lag monitoring to evaluate the *historical deviation* of offset lag, rather than relying solely on absolute instantaneous lag thresholds.
- The AI MUST expose the following CMS controls to the microservice team via configuration files (e.g., Helm `values.yaml`): Environment variables, cluster deployment target, CPU/memory/disk limits, manual instance counts, and autoscaling thresholds.

## Scaffolding and Cluster Bringup
- When creating a new microservice, the AI MUST generate a standardized pipeline encompassing: Repository creation, CI integration, webhooks, team ownership assignment, input stream ACL requests, output stream creation, and templated skeletal code.
- The AI MUST use Infrastructure-as-Code to enable the programmatic bringup of isolated event brokers and compute resources for testing, ensuring cross-cluster event data replication is configured if disaster recovery or staging population is required.

## Topology and Dependencies
- The AI MUST NOT rely on self-reporting or tribal knowledge for dependency tracking. The AI MUST write scripts/tools that parse event broker ACLs to automatically generate topology visualizations and data lineage graphs.
- The AI MUST evaluate the generated topology to minimize cross-team boundary connections, reassigning microservice boundaries if a service creates excessive external coupling.

# @Workflow
When tasked with configuring infrastructure, scaffolding, or DevOps tooling for an Event-Driven Microservice, the AI MUST follow this algorithmic process:

1. **Scaffolding & Identity Initialization**:
   - Generate the microservice skeleton.
   - Inject the `Microservice-to-Team Assignment` configuration.
   - Expose container management controls (CPU/Mem/Disk/Scaling) via a centralized config file.

2. **Stream & ACL Provisioning**:
   - Define all Input, Output, Internal, and Changelog event streams.
   - Apply mandatory metadata tags (`owner`, `pii`, `financial`, `namespace`, `status`) to all streams.
   - Configure ACLs: Grant `READ` for inputs. Grant exclusively `WRITE`/`CREATE` for outputs. Grant exclusively `READ`/`WRITE`/`CREATE` for internal/changelogs.

3. **Quota & Performance Configuration**:
   - Define broker-level quotas (I/O and CPU limits) for the service.
   - Bypass or elevate quotas for external-facing ingestion producers.

4. **Schema Registry Integration**:
   - Configure the producer/consumer to connect to the Schema Registry.
   - Ensure serialization logic requests schema IDs and strips raw schemas from the transport payload.
   - Create a webhook/CI step to notify dependent ACL `READ` owners of schema mutations.

5. **Monitoring & Autoscaling Setup**:
   - Implement consumer offset lag metric collection.
   - Configure autoscaling policies based on lag history, explicitly embedding a hysteresis cooldown.

6. **State & Offset Management Utilities**:
   - Generate an "Application Reset" runbook/script that automates: (a) Internal/changelog topic deletion, (b) External store truncation, and (c) Consumer offset reset.
   - Generate offset mutation scripts supporting `earliest`, `latest`, and `timestamp` targets.

7. **Topology Registration**:
   - Output an infrastructure graph derived strictly from the applied ACLs to validate bounded contexts and team interconnectedness.

# @Examples (Do's and Don'ts)

## Stream Configuration and Metadata
**[DO]**
```yaml
# Correct Stream Configuration with explicit tags, ACLs, and Quotas
topics:
  - name: "user-profile-updates"
    partitions: 12
    replication_factor: 3
    retention_ms: -1 # Infinite retention for entity streams
    tags:
      owner: "identity-team"
      pii: "true"
      financial: "false"
      namespace: "user-management"
      status: "active"
    acls:
      - principal: "User:identity-ms"
        operations: ["WRITE", "CREATE"]
      - principal: "User:*"
        operations: ["READ"]
    quotas:
      producer_byte_rate: 10485760
```

**[DON'T]**
```yaml
# Incorrect Stream Configuration missing tags, single writer enforcement, and quotas
topics:
  - name: "user-profile-updates"
    partitions: 1
    # Missing replication and retention
    # Missing metadata tags (owner, PII, etc.)
    acls:
      - principal: "User:*"
        operations: ["WRITE", "READ"] # Violates Single Writer Principle
```

## Schema Registry Implementation
**[DO]**
```java
// Correct: Payload only contains Schema ID fetched from Registry
byte[] serializeEvent(UserProfile event) {
    int schemaId = schemaRegistryClient.register(SUBJECT, event.getSchema());
    ByteBuffer buffer = ByteBuffer.allocate(4 + event.toByteArray().length);
    buffer.putInt(schemaId);
    buffer.put(event.toByteArray());
    return buffer.array();
}
```

**[DON'T]**
```java
// Incorrect: Payload transmits the entire raw schema in every message
byte[] serializeEvent(UserProfile event) {
    String rawPayload = "{ \"schema\": \"" + event.getSchema().toString() + "\", \"data\": " + event.toJson() + "}";
    return rawPayload.getBytes();
}
```

## Autoscaling and Lag Monitoring
**[DO]**
```yaml
# Correct: Autoscaling on lag includes hysteresis/cooldown
autoscaling:
  metrics:
    - type: External
      external:
        metric:
          name: kafka_consumer_lag
        target:
          type: AverageValue
          value: 500
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300 # Hysteresis: wait 5 minutes before scaling down
      policies:
        - type: Pods
          value: 1
          periodSeconds: 60
```

**[DON'T]**
```yaml
# Incorrect: Autoscaling on instantaneous lag without stabilization (will cause thrashing)
autoscaling:
  metrics:
    - type: External
      external:
        metric:
          name: kafka_consumer_lag
        target:
          type: AverageValue
          value: 5
  # Missing hysteresis / stabilizationWindowSeconds
```

## Application Reset Scripting
**[DO]**
```bash
#!/bin/bash
# Correct Application Reset sequence
echo "1. Deleting internal and changelog streams..."
kafka-topics.sh --delete --topic "my-app-KSTREAM-AGGREGATE-STATE-STORE-changelog" --bootstrap-server $BROKER
echo "2. Purging external materialized state..."
aws dynamodb delete-table --table-name "my-app-materialized-view"
echo "3. Resetting input offsets to earliest..."
kafka-consumer-groups.sh --bootstrap-server $BROKER --group "my-app-group" --reset-offsets --to-earliest --execute --topic "input-stream"
```

**[DON'T]**
```bash
#!/bin/bash
# Incorrect: Only resetting offsets, leaving corrupted state and old changelogs intact
kafka-consumer-groups.sh --bootstrap-server $BROKER --group "my-app-group" --reset-offsets --to-earliest --execute --topic "input-stream"
# Fails to delete internal topics and external state stores, resulting in non-deterministic behavior.
```