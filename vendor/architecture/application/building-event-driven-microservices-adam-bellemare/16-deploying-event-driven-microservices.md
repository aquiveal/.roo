@Domain
These rules are triggered when the AI is tasked with creating, modifying, or reviewing deployment scripts, CI/CD pipelines, container management system (CMS) configurations, schema migration strategies, or infrastructure-as-code for event-driven microservices.

@Vocabulary
- **Deployment Autonomy**: The principle that teams must have full control over deploying their microservices independently of other teams' deployment schedules.
- **Microservice Tax**: The requisite investment in standardized systems (CI/CD, CMS) necessary to deploy and manage microservices at scale.
- **Continuous Integration (CI)**: The automated process of validating, building, and testing code merged into a repository.
- **Continuous Delivery**: Maintaining a deployable codebase where deployment requires manual intervention by the service owner.
- **Continuous Deployment**: The fully automated progression of code from commit directly into the production environment.
- **CMS (Container Management System)**: Systems like Kubernetes that manage the deployment, resource allocation, and scaling of containerized microservices.
- **Basic Full-Stop Deployment**: A deployment pattern where all existing instances of a microservice are stopped, state is potentially cleaned up, and then new instances are started.
- **Rolling Update**: A zero-downtime deployment pattern where instances are stopped, updated, and restarted one at a time.
- **Breaking Schema Change**: A change to a data contract that is incompatible with downstream consumers, requiring migration strategies.
- **Eventual Migration**: A breaking schema migration strategy where the producer writes to both old and new event streams simultaneously until all consumers have migrated.
- **Synchronized Migration**: A high-risk breaking schema migration strategy where a producer switches entirely to a new schema, forcing all consumers to update simultaneously.
- **Blue-Green Deployment**: A zero-downtime deployment pattern where a completely parallel infrastructure ("blue") is brought up alongside the existing ("green"), traffic is shifted, and then the old infrastructure is idled.

@Objectives
- Guarantee that all microservice deployments are completely independent, avoiding synchronous deployments across multiple bounded contexts.
- Prevent data corruption, duplicate event generation, and state store inconsistencies by rigidly applying the correct deployment pattern based on the service's I/O behavior.
- Ensure that CI/CD pipelines include rigorous pre-deployment and post-deployment validation steps, particularly regarding schema compatibility and event stream accessibility.
- Protect downstream consumers from unexpected SLA violations, unannounced breaking schema changes, or massive event reprocessing surges.

@Guidelines

**Architectural & Pipeline Constraints**
- The AI MUST ensure deployment configurations grant teams deployment autonomy; do not couple deployment scripts across different microservices.
- The AI MUST configure CI/CD pipelines to output a ready-to-deploy container or virtual machine that integrates directly with the CMS.
- The AI MUST structure CI/CD pipelines with the following explicit stages: Code Commit -> Automated Unit/Integration Tests -> Pre-deployment Validation -> Deployment -> Post-deployment Validation.

**Validation Rules**
- The AI MUST enforce transient, isolated environments for integration tests within the CI pipeline to avoid multitenancy test pollution.
- Pre-deployment validation MUST include explicit checks to verify that required input/output event streams exist and the microservice has the proper read/write ACL permissions.
- Pre-deployment validation MUST include schema evolution validation; the AI MUST script comparisons between the new codebase schemas and the schema registry.
- Post-deployment validation MUST include automated checks for consumer lag normalization, logging errors, and endpoint health.

**Deployment Pattern Selection & Constraints**
- **Basic Full-Stop Pattern**:
  - The AI MUST use this as the default deployment pattern when state stores must be rebuilt, internal topologies change, or schema evolution rules are broken.
  - The AI MUST script the following sequence for Full-Stop: 1) Stop instances, 2) Clean up (reset consumer groups, purge state stores, delete internal streams), 3) Deploy new instances.
- **Rolling Update Pattern**:
  - The AI MUST NOT use Rolling Updates if the deployment introduces: breaking changes to state stores, breaking changes to the internal microservice topology (specifically lightweight frameworks), or breaking changes to internal event schemas.
  - The AI MUST use Rolling Updates for zero-downtime deployments when changing external business logic, adding new input streams, or fixing bugs that do not require state reprocessing.
- **Blue-Green Deployment Pattern**:
  - The AI MUST AVOID Blue-Green deployments if the microservice produces events to an output stream (this causes duplicate events or overwritten entities).
  - The AI MUST strictly limit Blue-Green deployments to consumer-only services or synchronous request-response services.
  - When configuring Blue-Green deployments, the AI MUST provision fully isolated external data stores, distinct consumer groups, and independent IP addresses for the "Blue" environment before traffic routing.
- **Breaking Schema Change Pattern**:
  - For non-entity events, the AI SHOULD implement breaking changes by adding a new event stream and modifying the consumer to handle both old and new streams until old events expire.
  - For entity events, the AI MUST configure the producer to reprocess source data to generate new entities under the new schema.
  - The AI MUST default to **Eventual Migration**: configure the producer to emit to *both* the old (deprecated) and new event streams, dropping the old stream only when all consumers have migrated.
  - The AI MUST AVOID **Synchronized Migration** (single stream cutover) unless explicitly instructed, as it requires high-risk coordinated consumer deployments. If forced to use Synchronized Migration, the AI MUST require full integration testing of the producer and all consumers simultaneously.

@Workflow
When tasked with creating or modifying a deployment script or CI/CD pipeline for an event-driven microservice, the AI MUST follow this exact sequence:
1. **Analyze Microservice State & I/O**: Determine if the service produces to output streams, if it maintains internal/external state, and if the code changes alter the internal topology or schemas.
2. **Select the Deployment Pattern**:
   - If producing to output streams -> Discard Blue-Green.
   - If topology/state store/schema changes -> Discard Rolling Update; Select Full-Stop Deployment or Breaking Schema Migration.
   - If breaking schema change -> Select Eventual Migration (Dual-Write).
   - Otherwise -> Select Rolling Update.
3. **Generate CI/CD Pipeline Definition**:
   - Write the Test execution stage (using transient environments).
   - Write the Pre-Deployment Validation stage (Stream ACL checks, Schema compatibility checks).
4. **Generate CMS Deployment Script**:
   - Write the execution script for the selected pattern (e.g., scale down 1-by-1 for Rolling, or Purge-then-Start for Full-Stop).
5. **Generate Post-Deployment Validation**:
   - Write the health and lag monitoring hooks.

@Examples (Do's and Don'ts)

**Pipeline Validation**
- [DO]: Implement a pre-deployment step that queries the Schema Registry to validate that the new Avro/Protobuf schema is forward-compatible.
- [DON'T]: Deploy the container directly after unit tests pass without verifying if the target Kafka topics exist.

**Deployment Pattern Application**
- [DO]: Use a Basic Full-Stop deployment script that purges the local RocksDB state store and resets the Kafka consumer group offset before starting the new container, when altering a map-reduce grouping key.
- [DON'T]: Use a Rolling Update when modifying a `groupByKey()` operation in the stream topology, as this will cause old and new instances to corrupt the internal shuffle streams.

**Blue-Green Deployment**
- [DO]: Implement Blue-Green deployment for a microservice that consumes a user-profile event stream and exclusively serves that data via a REST API.
- [DON'T]: Implement Blue-Green deployment for a microservice that consumes a payment stream, calculates taxes, and outputs to a `tax-calculated` event stream. (Both Blue and Green instances will simultaneously publish to the output stream, causing duplicates).

**Breaking Schema Changes**
- [DO]: Implement an "Eventual Migration" by writing a producer that serializes data into `User-v1` and `User-v2` streams simultaneously, tagging `User-v1` as deprecated.
- [DON'T]: Drop a required column from a producer's schema and force all downstream consumer teams to deploy their updates at the exact same minute to prevent crashing.