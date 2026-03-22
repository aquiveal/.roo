@Domain
These rules are activated when the AI is requested to design, develop, deploy, test, or troubleshoot microservices using Heavyweight Stream-Processing Frameworks. Applicable technologies include Apache Spark, Apache Flink, Apache Storm, Apache Heron, and Apache Beam. Triggers include requests related to big-data stream processing, MapReduce-style topologies, complex windowing/aggregations, cluster-based stream processing, and container-management system (CMS) integration for heavyweight jobs.

@Vocabulary
- **Heavyweight Framework**: A stream-processing framework that requires an independent cluster of processing resources (master/worker nodes) and manages its own internal failures, scaling, and state, separate from the Container Management System (CMS) and Event Broker.
- **Master Node**: The cluster component responsible for prioritizing, assigning, and managing executors and tasks.
- **Worker Node (Executor)**: The cluster component that completes the assigned streaming tasks utilizing local processing power, memory, and disk.
- **Zookeeper**: A centralized service used for distributed coordination, high-availability support, and leader elections among Master Nodes.
- **Job**: A complete stream-processing topology submitted to the heavyweight cluster.
- **Task**: A subdivision of a Job, assigned to a specific Worker Node for execution.
- **Task Manager**: A high-availability component that monitors tasks and restarts them on available executors if failures occur.
- **Driver Mode**: An application submission mode where a local, standalone application coordinates cluster execution. Terminating the driver automatically terminates the application.
- **Cluster Mode**: An application submission mode where the entire application is submitted to the cluster, returning a unique ID. Requires explicit API commands to manage or halt.
- **Checkpoint**: A snapshot of the application's internal state persisted to durable external storage (e.g., HDFS) for recovery and scaling.
- **Operator State**: The mapping of `<partitionId, offset>` saved within a checkpoint.
- **Key State**: The mapping of `<key, state>` (the actual business data) saved within a checkpoint.
- **External Shuffle Service (ESS)**: An isolation layer that receives shuffled events from upstream tasks and stores them for downstream consumption, enabling dynamic scaling of running applications.
- **Namespacing**: Dividing a single heavyweight cluster into logical segments with specific resource allocations to prevent multitenancy resource starvation.

@Objectives
- Design highly scalable, fault-tolerant event-driven microservices utilizing heavyweight cluster resources.
- Ensure strict data locality through proper key-based event shuffling (`keyBy`, `groupByKey`).
- Guarantee deterministic state recovery by synchronizing Operator State and Key State via Checkpoints.
- Align heavyweight framework deployments with microservice operational standards via Driver Mode and CMS (Kubernetes) integrations where supported.
- Prevent multitenancy resource starvation through strict namespacing and resource quotas.

@Guidelines

**Architecture & Cluster Management**
- The AI MUST configure applications to run on a dedicated heavyweight cluster consisting of Master Nodes and Worker Nodes.
- The AI MUST implement distributed coordination (e.g., Apache Zookeeper) to manage high-availability and leader election for Master Nodes.
- When integrating with a CMS (e.g., Kubernetes), the AI MUST enforce static assignment for Master Nodes to prevent the CMS from needlessly shuffling them and triggering false failure alerts.
- For modern microservice alignment, the AI MUST prioritize deploying jobs via CMS resource acquisition (e.g., Spark/Flink on Kubernetes) to isolate worker resources per application, rather than sharing a single monolithic legacy cluster.

**Application Submission & Lifecycle**
- The AI MUST utilize **Driver Mode** when deploying heavyweight frameworks as standard microservices, ensuring that the CI/CD pipeline and CMS can stop the job simply by terminating the standalone driver container.
- If **Cluster Mode** is strictly required, the AI MUST implement tooling or scripts to capture the returned unique application ID and use the cluster's API to manage the application lifecycle (halting, updating).

**State Management & Checkpointing**
- The AI MUST default to using internal state (in-memory spilled to local SSDs) for high-performance operations, rather than external state stores.
- The AI MUST configure persistent **Checkpoints** to durable external storage (e.g., HDFS, S3).
- The AI MUST ensure that Checkpointing logic synchronously captures both the **Operator State** (partition offsets) and the **Key State** (business aggregations) to prevent duplicate processing or data loss upon task recovery.

**Scaling & Shuffling**
- When designing topologies that require stateful aggregations, the AI MUST enforce data locality by introducing a shuffle phase (e.g., `keyBy`, `groupByKey`) before the windowing or aggregation function.
- If dynamic scaling (scaling while the application is running) is required, the AI MUST configure an **External Shuffle Service (ESS)** to decouple upstream shuffle generators from downstream consumers. *Exception: If utilizing Apache Spark 3.0+, the AI MAY configure native dynamic resource allocation without an ESS by leveraging prolonged executor lifespans.*
- If dynamic scaling is not supported, the AI MUST execute scaling via the restart method: Pause consumption -> Trigger Checkpoint -> Stop application -> Reinitialize with new parallelism settings -> Reload state from Checkpoint.

**Multitenancy & Resource Allocation**
- The AI MUST NOT deploy applications to a shared cluster without defining resource boundaries.
- The AI MUST mitigate multitenancy starvation by either provisioning discrete smaller clusters per team OR enforcing strict **Namespacing** with predefined maximum resource allocations.

**Languages & APIs**
- The AI MUST default to JVM-based languages (Java, Scala) or Python when writing heavyweight microservices, as these frameworks natively support them.
- The AI MUST utilize MapReduce-style functional chains or framework-specific SQL implementations to define the processing topology.

@Workflow
When tasked with generating or modifying a Heavyweight Framework Microservice, the AI MUST follow this exact sequence:

1. **Deployment Architecture Selection**: Determine if the target environment is a Hosted Service, a self-managed CMS/Kubernetes integration, or a standalone cluster. Select CMS integration if available.
2. **Submission Mode Definition**: Configure the deployment pipeline to use Driver Mode (preferred for microservices) or Cluster Mode.
3. **Topology Construction**: 
   - Define input event streams.
   - Apply union/merge operations if consuming from multiple related streams.
   - Enforce a shuffle operation (e.g., `.keyBy(<key selector>)`) to ensure data locality based on the primary entity key.
   - Apply time-based bounds using Windowing functions (e.g., Tumbling, Sliding, Session windows).
   - Apply the aggregation or reduce function.
   - Define the sink to the output event broker.
4. **Checkpoint Configuration**: Implement state snapshotting ensuring that partition offsets and keyed state are synchronously flushed to durable storage.
5. **Scaling Strategy Implementation**: Define the autoscaling policy (CPU, memory, consumer lag) and establish whether scaling will be dynamic (requires ESS/Spark 3.0+) or require a pause-and-restart script.
6. **Multitenancy Configuration**: Assign the job to a specific namespace or isolated worker pool to prevent resource hoarding.

@Examples (Do's and Don'ts)

**DO**: Construct a highly-available, localized topology using MapReduce APIs with proper shuffling and windowing.
```java
// [DO] Example using Apache Flink for a Session Window topology
DataStream<Action> clickStream = env.addSource(clickSource);
DataStream<Action> viewStream = env.addSource(viewSource);

clickStream
    .union(viewStream)
    // CRITICAL: Shuffle data to ensure locality before aggregation
    .keyBy(action -> action.getUserId())
    // Apply time-sensitive logic
    .window(EventTimeSessionWindows.withGap(Time.minutes(30)))
    .aggregate(new UserSessionAggregator())
    .addSink(outputSink);
```

**DON'T**: Attempt to deploy a heavyweight topology without configuring durable checkpoints, leading to desynchronized operator and key states upon worker failure.
```java
// [DON'T] Failing to configure checkpoints in a stateful application
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
// MISSING: env.enableCheckpointing(10000);
// MISSING: env.setStateBackend(new FsStateBackend("hdfs://namenode:40010/flink/checkpoints"));

DataStream<Event> stream = env.addSource(mySource);
stream.keyBy(event -> event.getKey())
      .map(new StatefulMapper()) // If this task fails, state is lost permanently!
      .addSink(mySink);
```

**DO**: Deploy the application using Driver Mode in a container managed by a CMS (like Kubernetes), so the microservice deployment pipeline can cleanly tear down the application by killing the driver pod.
```yaml
# [DO] Kubernetes Deployment targeting a Spark Driver
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-streaming-driver
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: spark-driver
        image: my-spark-app:v1
        command: ["spark-submit", "--deploy-mode", "client", "--master", "k8s://https://k8s-apiserver:443", "my_app.jar"]
```

**DON'T**: Submit a long-running streaming job to a shared global cluster without a namespace or resource cap, allowing it to starve all other applications of executors when processing a backlog.
```bash
# [DON'T] Submitting without resource caps or namespaces
spark-submit --deploy-mode cluster --master spark://global-master:7077 my_app.jar
# This can consume all available worker memory/CPU on the cluster!
```