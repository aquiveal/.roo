@Domain
This rule file MUST be activated when the AI is tasked with integrating microservices, designing inter-service communication, implementing asynchronous messaging architectures, defining message brokers (e.g., Redis Pub/Sub, Kafka, RabbitMQ), writing event consumers/publishers, or refactoring synchronous HTTP/RPC calls between services into event-driven workflows.

@Vocabulary
- **Distributed Ball of Mud**: An anti-pattern occurring when a system is split into microservices based on *nouns* (e.g., Batches, Orders) and integrated using synchronous HTTP/RPC calls, resulting in a tangled dependency graph.
- **Temporal Coupling / Connascence of Timing**: A brittle state where multiple distributed components must be available and function simultaneously for an operation to succeed.
- **Connascence of Execution**: A state where multiple components must execute work in a strictly coordinated order to be successful.
- **Connascence of Name**: A weak, highly desirable form of coupling where distributed components only need to agree on the name of an event and its data fields.
- **Message Broker**: A piece of infrastructure (e.g., Redis, Event Store, Kafka) that routes asynchronous messages from publishers to subscribers.
- **Event Consumer**: A primary (driving) adapter that listens to external messages from the Message Broker, deserializes them, and translates them into internal `Command` objects.
- **Event Publisher**: A secondary (driven) adapter that takes outgoing internal `Event` objects, serializes them, and pushes them to the Message Broker.
- **Internal vs. External Events**: The distinction between events meant strictly for intra-service orchestration (Domain Events) and events intended to be broadcast to other microservices (Integration/Public Events).
- **Eventual Consistency**: The accepted state in a distributed system where different microservices will eventually synchronize their state via asynchronous events, rather than immediately via locked synchronous transactions.

@Objectives
- Transform the application into an external message processor that receives inputs via an external message broker and outputs results via the same broker.
- Decouple microservices temporally by replacing synchronous API/RPC integrations with asynchronous event-driven messaging.
- Prevent failure cascades by relying on Eventual Consistency and independent service failure modes.
- Architect microservice boundaries around *verbs* (business processes) rather than *nouns* (data entities).
- Restrict cross-service coupling strictly to Connascence of Name.

@Guidelines

### 1. Architectural Design & Coupling
- The AI MUST NOT integrate microservices using synchronous HTTP or RPC calls to trigger state changes in downstream systems.
- The AI MUST separate services by business processes (*verbs*) rather than data entities (*nouns*).
- The AI MUST enforce Eventual Consistency between services. If one service fails, upstream services MUST still be able to complete their local transactions and publish events.
- The AI MUST replace Connascence of Execution and Timing with Connascence of Name by integrating services strictly via asynchronous messaging.

### 2. Message Consumption (Inbound)
- The AI MUST implement an Event Consumer as a primary adapter (e.g., `redis_eventconsumer.py`).
- The Event Consumer MUST listen to a specific channel/queue on the Message Broker.
- Upon receiving an external message, the Event Consumer MUST deserialize the payload (e.g., JSON), translate it into a specific internal `Command` dataclass, and pass that Command to the internal `messagebus.handle()`.
- The Event Consumer MUST inject the Unit of Work (UoW) when passing the Command to the internal message bus.

### 3. Message Publishing (Outbound)
- The AI MUST NOT allow the internal domain model or internal handlers to interact directly with the external Message Broker.
- The AI MUST implement an Event Publisher as a secondary adapter (e.g., `redis_eventpublisher.py`).
- The Event Publisher MUST expose a simple function/method (e.g., `publish(channel, event)`) that serializes an internal `Event` dataclass to JSON and pushes it to the Message Broker.
- The AI MUST map outgoing events to the Event Publisher adapter within the internal message bus `HANDLERS` dictionary.
- The AI MUST distinctly separate Internal Events from External Events. Only events meant for external consumption should be routed to the Event Publisher.
- The AI MUST apply strict validation to outbound events before they are published to the external Message Broker.

### 4. Testing Event-Driven Integrations
- The AI MUST test external asynchronous integrations using End-to-End (E2E) tests.
- E2E tests MUST interact with the actual Message Broker infrastructure (e.g., a real/Dockerized Redis instance).
- E2E tests MUST trigger workflows by publishing messages to the inbound broker channel or via an API that triggers the workflow.
- E2E tests MUST assert outcomes by subscribing to the outbound broker channel and waiting for the expected event.
- Because asynchronous messaging is temporally decoupled, the AI MUST wrap E2E assertions in a retry loop (e.g., using the `tenacity` library) to wait for messages to arrive over the network.

@Workflow
When tasked with integrating an external event or notifying an external service, the AI MUST follow this exact sequence:

1. **Define the Domain Event/Command**: Create a `Command` dataclass for the inbound message or an `Event` dataclass for the outbound message in `domain/events.py` or `domain/commands.py`.
2. **Update the Domain Model (If Outbound)**: Modify the aggregate (e.g., `Product.allocate`) to append the new outbound `Event` to its `.events` list upon successful state mutation.
3. **Implement the Publisher Adapter (If Outbound)**: Create a secondary adapter (e.g., `adapters/redis_eventpublisher.py`) with a `publish` function that serializes the `Event` to JSON and sends it to the Message Broker.
4. **Register the Publisher (If Outbound)**: Add a handler in the service layer that calls the publisher adapter, and register it in `messagebus.py` under the corresponding `Event`.
5. **Implement the Consumer Adapter (If Inbound)**: Create a primary adapter (e.g., `entrypoints/redis_eventconsumer.py`) that subscribes to the Message Broker, parses the incoming JSON, instantiates the `Command`, and routes it to `messagebus.handle()`.
6. **Write the E2E Test**: Write an E2E test that mimics the external system. Publish an inbound message (or hit an API endpoint), then subscribe to the outbound channel. Use a `tenacity` retry loop to listen for and assert against the final JSON payload.

@Examples (Do's and Don'ts)

### External Service Integration
[DON'T] Make synchronous HTTP calls to downstream microservices from within a service layer or web controller.
```python
# ANTI-PATTERN: Distributed Ball of Mud / Temporal Coupling
def allocate_endpoint():
    # ... local allocation logic ...
    
    # Synchronously coupling to the warehouse service
    response = requests.post('http://warehouse-api/dispatch', json=dispatch_data)
    if response.status_code != 200:
        raise Exception("Warehouse down, failing local transaction")
```

[DO] Raise an internal event, handle it by converting it to a public event, and publish it asynchronously via a Message Broker.
```python
# DO: Event Publisher Adapter
import json
import redis
from allocation.domain import events

r = redis.Redis(host='redis', port=6379)

def publish(channel: str, event: events.Event):
    # Serializes the event and decouples temporally from downstream services
    r.publish(channel, json.dumps(dataclasses.asdict(event)))

# In messagebus.py HANDLERS:
# { events.Allocated: [handlers.publish_allocated_event] }
```

### Inbound Message Consumption
[DON'T] Mix infrastructure parsing and domain logic when consuming messages.
```python
# ANTI-PATTERN: Business logic leaking into the infrastructure adapter
def handle_redis_message(m):
    data = json.loads(m['data'])
    # Directly manipulating DB sessions and domain models
    batch = session.query(Batch).filter_by(ref=data['batchref']).first()
    batch.qty = data['qty']
    session.commit()
```

[DO] Parse the message, translate it into a Command, and route it to the internal Message Bus.
```python
# DO: Thin Event Consumer Adapter
def handle_change_batch_quantity(m):
    data = json.loads(m['data'])
    # Translate external JSON to internal Command
    cmd = commands.ChangeBatchQuantity(ref=data['batchref'], qty=data['qty'])
    
    # Route to internal message processor
    messagebus.handle(cmd, uow=unit_of_work.SqlAlchemyUnitOfWork())
```

### Testing Asynchronous Workflows
[DON'T] Expect asynchronous messages to arrive immediately in tests, resulting in flaky tests.
```python
# ANTI-PATTERN: No retry loop for async message retrieval
redis_client.publish_message('change_batch_quantity', data)
message = subscription.get_message()
# This will likely fail because the message hasn't been processed yet
assert json.loads(message['data'])['batchref'] == expected
```

[DO] Use a retry loop (e.g., `tenacity`) to poll for the expected message.
```python
# DO: Retry loop for Eventual Consistency
from tenacity import Retrying, stop_after_delay

redis_client.publish_message('change_batch_quantity', data)

messages = []
for attempt in Retrying(stop=stop_after_delay(3), reraise=True):
    with attempt:
        message = subscription.get_message(timeout=1)
        if message:
            messages.append(message)
        
        data = json.loads(messages[-1]['data'])
        assert data['batchref'] == expected_batchref
```