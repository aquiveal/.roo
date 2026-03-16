@Domain
These rules MUST be triggered when the AI is tasked with designing, analyzing, or refactoring data processing workflows, ETL (Extract, Transform, Load) pipelines, EDI (Electronic Data Interchange) systems, task orchestrators/mediators (e.g., Apache Camel), or any architecture explicitly referred to as "Pipeline Architecture" or "Pipes and Filters" style.

@Vocabulary
- **Pipeline Architecture (Pipes and Filters)**: A fundamental, technically partitioned architecture style consisting of discrete processing components (filters) connected by communication channels (pipes).
- **Pipe**: A unidirectional, point-to-point communication channel between two filters.
- **Filter**: A self-contained, independent, and generally stateless component that performs exactly one task.
- **Producer (Source)**: The starting point of a pipeline process. It is outbound-only.
- **Transformer (Map)**: A filter that accepts input, performs a transformation on some or all of the data, and forwards it to the outbound pipe.
- **Tester (Reduce)**: A filter that accepts input, tests one or more criteria, and optionally produces output based on that test (serving as a conditional gateway or router).
- **Consumer (Sink)**: The termination point for the pipeline flow, which typically persists the final result to a database or displays it on a user interface.
- **Architectural Quantum**: A measure of independent deployability and synchronous connascence. For Pipeline Architecture, the quantum is ALWAYS ONE (1) because it is deployed as a monolithic application.
- **Compositional Reuse**: The ability to dynamically chain small, discrete filters together to solve complex problems (akin to Unix shell scripting).

@Objectives
- The AI MUST design pipelines as a sequence of highly decoupled, single-responsibility components.
- The AI MUST ensure all data flow is strictly unidirectional and point-to-point.
- The AI MUST enforce the statelessness of all intermediate processing filters to allow safe data processing.
- The AI MUST maximize compositional reuse by preventing composite (multi-task) filters.
- The AI MUST accurately communicate the architectural trade-offs of this style, specifically highlighting its low scalability, low elasticity, and low fault tolerance inherent to monolithic deployments.

@Guidelines
- **Filter Constraints**:
  - The AI MUST restrict every filter to performing ONE task only. If a task is composite, the AI MUST break it down into a sequence of multiple discrete filters.
  - The AI MUST design filters to be entirely stateless and independent of other filters.
  - The AI MUST explicitly categorize every generated filter as a Producer, Transformer, Tester, or Consumer. No ambiguous filter types are allowed.
- **Pipe Constraints**:
  - The AI MUST ensure pipes are strictly unidirectional. Data MUST NOT flow backward.
  - The AI MUST ensure pipes are point-to-point. Broadcasting (sending the exact same data payload to multiple disparate endpoints simultaneously from a single pipe) is strictly forbidden in the core pipe definition.
  - The AI MUST optimize the payload carried on the pipes. Data packets MUST be kept as small as possible to ensure high performance.
- **Architectural and Topological Rules**:
  - The AI MUST treat the pipeline architecture as a technically partitioned monolith (Architectural Quantum = 1).
  - The AI MUST NOT design the pipeline to rely on distributed transactions or independent scaling of individual filters, as the entire pipeline scales as a single monolithic deployment unit.
  - The AI MUST utilize the Tester filter to conditionally route data (e.g., dropping irrelevant data or routing specific metric types to specific Transformers) to ensure the pipeline is highly extensible.
- **Trade-off Management**:
  - When recommending this architecture, the AI MUST state its primary strengths: Low Cost, Simplicity, and Modularity.
  - The AI MUST warn the user about its primary weaknesses: Low Elasticity, Low Scalability, and Low Fault Tolerance (e.g., an out-of-memory error in one filter will crash the entire pipeline monolith).
  - The AI MUST assess deployability and testability as "average/medium" because, while filters are modular and easily testable in isolation, the deployment remains a monolithic unit carrying inherent deployment ceremony and risk.

@Workflow
1. **Source Identification**: Begin by identifying the data source. Design the `Producer` filter to interface with this source (e.g., subscribing to a Kafka topic, reading a file) and emit outbound data.
2. **Task Decomposition**: Analyze the business requirement and break the required processing down into the smallest possible, atomic tasks.
3. **Filter Assignment**:
   - For any task requiring data validation, filtering, or conditional logic, create a `Tester` filter.
   - For any task requiring data mutation, calculation, or format changes, create a `Transformer` filter.
4. **Pipeline Chaining**: Connect the filters sequentially using unidirectional `Pipes`. Ensure the output of one filter exactly matches the expected input schema of the subsequent filter. Keep payloads minimal.
5. **Sink Assignment**: Design the `Consumer` filter at the end of the chain to persist the final data (e.g., saving to a MongoDB database) or pass it to a UI.
6. **Extensibility Check**: Review the pipeline to ensure that a new filter (e.g., a new Tester) could be inserted between any two existing pipes without breaking the existing filters.
7. **Statelessness Validation**: Audit all Transformers and Testers to guarantee no internal state is maintained between pipe executions.

@Examples (Do's and Don'ts)

[DO]
```python
# Example of a well-architected Pipeline using discrete, single-purpose filters

class KafkaProducer:
    # Producer Filter
    def fetch_data(self):
        # Fetches raw telemetry data
        return {"type": "duration", "value": 150, "service": "auth"}

class DurationTester:
    # Tester Filter
    def process(self, data):
        # Only forwards data if it is of type 'duration'
        if data.get("type") == "duration":
            return data
        return None

class DurationTransformer:
    # Transformer Filter
    def process(self, data):
        # Converts milliseconds to seconds
        data["value_seconds"] = data["value"] / 1000.0
        return data

class MongoDBConsumer:
    # Consumer Filter
    def save(self, data):
        # Persists data to the database
        db.insert("telemetry", data)

# Pipeline Execution (Pipes)
def run_pipeline():
    producer = KafkaProducer()
    tester = DurationTester()
    transformer = DurationTransformer()
    consumer = MongoDBConsumer()

    raw_data = producer.fetch_data()
    tested_data = tester.process(raw_data)
    if tested_data:
        transformed_data = transformer.process(tested_data)
        consumer.save(transformed_data)
```

[DON'T]
```python
# Anti-pattern: Composite "God Filter" that violates the Pipeline Architecture style

class TelemetryProcessor:
    # VIOLATION: Combines Producer, Tester, Transformer, and Consumer into one component.
    # VIOLATION: Maintains internal state.
    def __init__(self):
        self.processed_count = 0 # Stateful

    def process_everything(self):
        # Producer
        data = {"type": "duration", "value": 150, "service": "auth"}
        
        # Tester & Transformer mixed together
        if data["type"] == "duration":
            data["value_seconds"] = data["value"] / 1000.0
            self.processed_count += 1
            
            # Consumer mixed in
            db.insert("telemetry", data)
            
            # VIOLATION: Bidirectional flow / cyclic dependency
            self.report_back_to_source(self.processed_count)
```