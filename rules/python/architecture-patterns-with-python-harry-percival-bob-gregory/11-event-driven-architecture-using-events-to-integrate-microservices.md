# @Domain
These rules MUST activate when the AI is tasked with architecting inter-service communication, integrating microservices, designing distributed systems, implementing asynchronous message passing, or building adapters for message brokers (e.g., Redis pub/sub, Kafka, RabbitMQ, Event Store).

# @Vocabulary
- **Distributed Ball of Mud**: An anti-pattern created by splitting a system into noun-based microservices (e.g., "Batches", "Orders") that communicate via synchronous HTTP APIs. This results in tangled dependency graphs and brittle architectures.
- **Connascence of Execution**: A strong, undesirable form of coupling where multiple components must know the exact correct order of operations for a process to be successful.
- **Connascence of Timing (Temporal Coupling)**: A strong, undesirable form of coupling where multiple distributed components must be operational simultaneously for an operation to succeed. A failure in one system cascades to the others.
- **Connascence of Name**: A weak, highly desirable form of coupling where distributed components only need to agree on the name of an event and the names of the fields it carries.
- **Message Broker**: External infrastructure (e.g., Redis Pub/Sub channels) used to take messages from publishers and deliver them to subscribers, enabling temporal decoupling.
- **Event Consumer (Inbound Adapter)**: A thin infrastructure adapter that listens to an external message broker, deserializes messages, translates them into internal `Commands`, and feeds them to the internal message bus.
- **Event Publisher (Outbound Adapter)**: A thin infrastructure adapter that acts as an internal event handler, translating internal domain `Events` into serialized payloads and publishing them to an external message broker.
- **Eventual Consistency**: The architectural acceptance that separated services will synchronize over time via asynchronous events, eliminating the need for distributed transactions or synchronous blocking calls.

# @Objectives
- Transform the application into an external message processor, mirroring its internal event-driven architecture.
- Eliminate temporal coupling and synchronous failure cascades between microservices.
- Design microservice boundaries around "verbs" (business processes) rather than "nouns" (database tables or entities).
- Ensure graceful degradation: a service MUST be able to fulfill its primary local operations (e.g., accepting orders) even if upstream/downstream services are experiencing downtime.
- Enforce independent failure domains by accepting eventual consistency across service boundaries.

# @Guidelines
- **Avoid Noun-Based Services**: The AI MUST NOT split systems into microservices based on static entities or database tables (e.g., creating a "Warehouse" service with a CRUD API that directly calls a "Batches" service).
- **Ban Synchronous Workflows Across Services**: The AI MUST NOT use synchronous HTTP REST or RPC calls to orchestrate workflows between microservices.
- **Implement Asynchronous Messaging**: The AI MUST integrate microservices using asynchronous message passing via a Message Broker to achieve Connascence of Name.
- **Translate External Events to Internal Commands**: When an Event Consumer receives a message from an external broker, the AI MUST deserialize the payload and translate it into an internal `Command` (which captures intent) before passing it to the internal message bus. It MUST NOT pass external events directly into the internal domain as events.
- **Publish Internal Events to External Channels**: To communicate with downstream systems, the AI MUST capture internal `Event` objects (facts) raised by the domain model and route them through an Event Publisher adapter to the external message broker.
- **Maintain Thin Adapters**: The AI MUST implement Event Consumers and Event Publishers strictly as thin adapters. They MUST NOT contain business logic. Their sole responsibilities are serialization, deserialization, and message bus interaction.
- **Differentiate Internal vs. External Events**: The AI MUST explicitly decide which internal events are promoted to external events. Not all internal domain events should be published globally. The AI MUST apply validation to outbound external events to protect the contract with downstream consumers.

# @Workflow
1. **Identify the Process**: Analyze the cross-service integration requirement. Model it as a verb or business process (e.g., "allocating") rather than a data manipulation on a noun.
2. **Define Inbound Contract**: Define the JSON schema for the incoming external message. Create a corresponding internal `Command` dataclass representing the intent of the external message.
3. **Build the Event Consumer**: 
   - Instantiate a connection to the Message Broker.
   - Subscribe to the relevant external channel.
   - For each received message, parse the JSON, instantiate the internal `Command`, and execute `messagebus.handle(cmd, uow)`.
4. **Update the Domain Model**: Implement the business logic for the command within the aggregate. Upon successful execution, append an internal `Event` to the aggregate's `.events` list.
5. **Define Outgoing Contract**: Create an `Event` dataclass that captures all necessary information downstream services will need.
6. **Build the Event Publisher**:
   - Create a function (the Outbound Adapter) that accepts the outgoing `Event`.
   - Serialize the `Event` to JSON.
   - Publish the JSON payload to the corresponding Message Broker channel.
7. **Wire the Publisher**: Register the Event Publisher adapter in the internal message bus `EVENT_HANDLERS` dictionary so it triggers when the domain raises the event.
8. **Write an Async End-to-End Test**:
   - Inject the trigger message (via HTTP API or by publishing a message directly to the broker test client).
   - Subscribe a test client to the outbound Message Broker channel.
   - Use a retry loop (e.g., `tenacity.Retrying`) with a timeout to wait for the asynchronous outbound message to arrive.
   - Assert against the contents of the received JSON message.

# @Examples (Do's and Don'ts)

### [DO] Implement thin Event Consumer adapters that map external messages to internal Commands
```python
import json
import redis
from allocation.domain import commands
from allocation.service_layer import messagebus, unit_of_work

r = redis.Redis(host='localhost', port=6379)

def main():
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('change_batch_quantity')
    
    for m in pubsub.listen():
        handle_change_batch_quantity(m)

def handle_change_batch_quantity(m):
    data = json.loads(m['data'])
    # Translate external event payload into an internal Command
    cmd = commands.ChangeBatchQuantity(ref=data['batchref'], qty=data['qty'])
    # Dispatch to the internal message bus
    messagebus.handle(cmd, uow=unit_of_work.SqlAlchemyUnitOfWork())
```

### [DO] Implement thin Event Publisher adapters for outbound integration
```python
import json
import redis
from dataclasses import asdict
from allocation.domain import events

r = redis.Redis(host='localhost', port=6379)

def publish(channel: str, event: events.Event):
    # Serialize domain event to JSON and push to external message broker
    r.publish(channel, json.dumps(asdict(event)))
```

### [DO] Test asynchronous event-driven flows using retry loops
```python
import json
from tenacity import Retrying, stop_after_delay

def test_change_batch_quantity_leading_to_reallocation():
    # 1. Setup initial state via API
    api_client.post_to_add_batch('batch1', 'SKU-1', qty=10)
    api_client.post_to_allocate('order1', 'SKU-1', 10)
    
    # 2. Subscribe to outbound channel
    subscription = redis_client.subscribe_to('line_allocated')
    
    # 3. Inject inbound message
    redis_client.publish_message('change_batch_quantity', {
        'batchref': 'batch1',
        'qty': 5
    })
    
    # 4. Await asynchronous output with a retry loop
    messages = []
    for attempt in Retrying(stop=stop_after_delay(3), reraise=True):
        with attempt:
            message = subscription.get_message(timeout=1)
            if message:
                messages.append(message)
            data = json.loads(messages[-1]['data'])
            assert data['orderid'] == 'order1'
```

### [DON'T] Create Distributed Balls of Mud via Synchronous HTTP APIs
```python
# ANTI-PATTERN: Synchronous temporal coupling between microservices
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    # ... logic ...
    
    # DON'T do this: If the warehouse service is down, the allocation service fails.
    # This is Connascence of Timing and Connascence of Execution.
    response = requests.post(
        "http://warehouse-service/api/dispatch", 
        json={"sku": sku, "qty": qty}
    )
    if response.status_code != 200:
        return "Failed to dispatch", 500
        
    return "Allocated", 201
```