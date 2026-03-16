# @Domain

These rules apply when the AI is designing, implementing, refactoring, or debugging distributed systems, microservices integration, or messaging architectures in Node.js. This includes any tasks involving message brokers (e.g., Redis, RabbitMQ/AMQP), peer-to-peer messaging (e.g., ZeroMQ), WebSockets for real-time communication, or the implementation of messaging patterns such as Publish/Subscribe, Task Distribution (Fan-out/Fan-in), and Asynchronous Request/Reply.

# @Vocabulary

- **Command Message**: A message that triggers the execution of an action or task on the receiver, containing the operation name and arguments (e.g., RPC).
- **Event Message**: A message used to notify another component that a specific occurrence or state change has happened.
- **Document Message**: A message meant strictly to transfer data between components without instructing the receiver on what to do.
- **Pull Delivery**: A consumer-initiated data delivery model where the client actively requests information (e.g., HTTP polling).
- **Push Delivery**: A producer-initiated data delivery model where the source proactively sends updates in real-time (e.g., WebSockets, RabbitMQ subscriptions).
- **Message Queue (MQ)**: A point-to-point data structure that temporarily holds messages until a consumer processes them. Messages are typically removed once consumed.
- **Stream / Log**: An append-only, durable sequence of messages where records remain accessible after consumption, allowing multi-subscriber access and historical replay.
- **Message Broker**: A centralized intermediary system (e.g., RabbitMQ, Redis) that decouples senders from receivers, often providing routing, persistence, and protocol translation.
- **Peer-to-Peer Messaging**: An architecture where nodes communicate directly without an intermediary broker (e.g., ZeroMQ).
- **Publish/Subscribe (Pub/Sub)**: A one-way messaging pattern where publishers broadcast messages to an unspecified number of subscribers listening to specific channels or topics.
- **Durable Subscriber**: A subscriber backed by an MQ or Stream that reliably receives all messages, including those sent while it was disconnected (At-least-once or Exactly-once semantics).
- **Fire-and-Forget**: A messaging semantic (At-most-once) where messages are not persisted and delivery is not acknowledged, meaning disconnected receivers lose messages.
- **AMQP**: Advanced Message Queuing Protocol; an open standard defining routing, filtering, and queuing mechanisms using Exchanges, Queues, and Bindings.
- **Exchange (AMQP)**: The entry point in a broker where messages are published. It routes messages to queues using Direct, Topic, or Fan-out algorithms.
- **Consumer Group (Redis)**: A stateful entity in Redis Streams that load-balances records among multiple named consumers, tracking pending and acknowledged messages.
- **Task Distribution / Ventilator / Competing Consumers**: A pattern where a producer distributes workloads across multiple workers to achieve parallel processing.
- **Sink**: The final node in a parallel pipeline that collects and aggregates results from multiple workers.
- **Request/Reply**: A bidirectional messaging pattern where a message in one direction is matched by a specific response in the opposite direction.
- **Correlation Identifier**: A unique ID attached to a request and included in the reply, allowing the sender to match asynchronous responses to pending requests.
- **Return Address**: A pattern where a request includes the name of a private reply queue/channel, instructing the replier where to send the response.

# @Objectives

- Ensure strict decoupling of microservices by correctly applying event-driven and message-driven architectural patterns.
- Select the optimal message type, delivery semantic, and messaging infrastructure based on the specific constraints of the system (e.g., throughput vs. reliability).
- Guarantee message reliability where required by implementing durable subscribers, explicit message acknowledgment, and backpressure mechanisms.
- Prevent message loss, duplication, and race conditions in distributed task pipelines by utilizing correct socket configurations, queue bindings, and consumer groups.
- Accurately map asynchronous, one-way messaging channels to stateful Request/Reply flows using standard enterprise integration patterns.

# @Guidelines

## Message Design & Delivery Semantics
- The AI MUST use **Command messages** when instructing a remote node to perform an action.
- The AI MUST use **Event messages** when broadcasting state changes without expecting a specific reaction.
- The AI MUST use **Document messages** when transferring raw payloads without behavioral instructions.
- The AI MUST choose **Push Delivery** when low-latency immediacy is required (e.g., live chats, real-time prices).
- The AI MUST choose **Pull Delivery** when consumer control, predictability, or caching is prioritized over immediacy.
- The AI MUST use **Message Queues** for point-to-point integration, task distribution, advanced routing, and message prioritization.
- The AI MUST use **Streams** for high-volume sequential data, multi-subscriber event sourcing, and scenarios requiring historical message replay.

## Peer-to-Peer vs. Broker-Based Messaging
- The AI MUST select **Peer-to-Peer** (e.g., ZeroMQ) to eliminate single points of failure and reduce latency.
- When implementing Peer-to-Peer messaging, the AI MUST bind the durable/stable nodes (e.g., Ventilators, Sinks) and connect the transient nodes (e.g., Workers).
- The AI MUST select a **Message Broker** (e.g., RabbitMQ, Redis) when decoupling, persistent queuing, and protocol interoperability are required.

## Publish/Subscribe Implementation
- **ZeroMQ PUB/SUB:** The AI MUST bind a `PUB` socket on the publisher and connect `SUB` sockets on the subscribers. The AI MUST use `subSocket.subscribe('topic')` to filter messages. The AI MUST handle the fact that ZeroMQ drops messages if no subscribers are connected.
- **Redis Pub/Sub:** The AI MUST create two separate Redis connections if a node both publishes and subscribes, as a Redis connection in subscriber mode cannot publish. The AI MUST use `redis.publish('channel', msg)` and `redis.subscribe('channel')`.
- **AMQP Pub/Sub (Fire-and-Forget):** The AI MUST use a `fanout` exchange. The AI MUST assert an exclusive queue (`{ exclusive: true }`) for transient subscribers and bind it to the exchange. The AI MUST consume with `{ noAck: true }`.
- **AMQP Pub/Sub (Durable Subscriber):** The AI MUST assert a named, non-exclusive queue (omitting `{ exclusive: true }`). The AI MUST explicitly acknowledge messages using `channel.ack(msg)` ONLY AFTER the message has been successfully processed or persisted.

## Stream-Based Messaging (Redis Streams)
- To append records, the AI MUST use the `xadd` command with the `*` ID to let Redis auto-generate monotonic IDs (e.g., `redis.xadd('stream', '*', 'key', 'value')`).
- To retrieve historical data, the AI MUST use `xrange` with `-` (lowest) and `+` (highest) limits.
- To listen for new messages continuously, the AI MUST use `xread` with the `BLOCK` option (e.g., `BLOCK`, `0`) and the `$` ID to receive only new records.

## Task Distribution (Parallel Pipelines)
- The AI MUST NOT use Publish/Subscribe for task distribution, as it leads to duplicated execution across workers.
- **ZeroMQ PUSH/PULL:** The AI MUST use a `PUSH` socket on the Ventilator (producer) and a `PULL` socket on the Sink (collector). Workers MUST connect a `PULL` socket to the Ventilator and a `PUSH` socket to the Sink. The AI MUST rely on ZeroMQ's `send()` promise resolving to handle backpressure.
- **AMQP Competing Consumers:** The AI MUST use point-to-point communication by sending messages directly to a named task queue (`channel.sendToQueue('queue_name', Buffer.from(data))`), bypassing exchanges. Multiple workers MUST consume from this identical queue name to trigger RabbitMQ's load balancing.
- **Redis Consumer Groups:** The AI MUST ensure the consumer group exists using `xgroup('CREATE', stream, group, '$', 'MKSTREAM')`, catching the "already exists" error.
- In Redis Consumer Groups, the worker MUST first read pending messages using `xreadgroup` with ID `0`. Then it MUST enter an infinite loop to read new messages using `xreadgroup` with `BLOCK 0` and ID `>`.
- In Redis Consumer Groups, the AI MUST explicitly acknowledge processed tasks using `xack(stream, group, recordId)`.

## Request/Reply Patterns
- **Correlation Identifier:** When building RPC over an asynchronous channel, the AI MUST generate a unique ID (e.g., via `nanoid()`) for the outgoing request. The AI MUST store a pending Promise's `resolve`/`reject` callbacks in a local `Map` keyed by this ID. The replier MUST include this ID in the response (e.g., `inReplyTo`). The requestor MUST use the ID from the incoming response to look up and execute the stored callback.
- **Return Address:** When requests originate from multiple channels/queues, the AI MUST attach a `replyTo` metadata property to the request indicating the requestor's private response queue. The replier MUST extract this property and use it as the destination for the response message.
- In AMQP, the AI MUST use an exclusive queue (`{ exclusive: true }`) with an auto-generated name (pass `''` to `assertQueue`) as the return address.

# @Workflow

1. **Analyze Messaging Requirements:**
   - Determine the communication direction (One-way vs. Request/Reply).
   - Determine the payload type (Command, Event, Document).
   - Assess delivery requirements (At-most-once/Transient vs. At-least-once/Durable).
2. **Select Infrastructure & Topology:**
   - Choose between P2P (ZeroMQ) for high-performance/low-latency or Broker (AMQP/Redis) for reliability/routing.
   - Choose between Queues (Point-to-Point/Task Distribution) and Streams (Event Sourcing/Replayability).
3. **Establish Connections and Sockets:**
   - *If ZeroMQ:* Bind long-lived nodes (Ventilators, Sinks, Pubs) and connect transient nodes (Workers, Subs).
   - *If AMQP:* Assert necessary Exchanges and Queues. Bind queues to exchanges if utilizing Pub/Sub routing.
   - *If Redis Streams:* Initialize connections. For task workers, ensure Consumer Groups are initialized.
4. **Implement Message Production:**
   - Serialize payloads (typically JSON to Buffer/String).
   - Attach metadata (Correlation IDs, Return Addresses) if implementing Request/Reply.
   - Handle backpressure (e.g., awaiting send promises in ZeroMQ, responding to `xadd` limits).
5. **Implement Message Consumption:**
   - Setup consumption loops (`for await...of` for ZeroMQ/Async Iterables, `channel.consume` for AMQP, `xread`/`xreadgroup` for Redis).
   - Execute the business logic on the payload.
   - **CRITICAL:** Acknowledge the message (e.g., AMQP `ack`, Redis `xack`) ONLY after business logic and persistence steps are successfully completed (if durable semantics apply).
6. **Implement Reply Handling (If Request/Reply):**
   - Replier: Extract Correlation ID and Return Address. Process task. Send response to Return Address including Correlation ID.
   - Requestor: Intercept message, lookup Correlation ID in the pending requests `Map`, resolve the Promise, and clean up the `Map` and timeout handlers.

# @Examples (Do's and Don'ts)

## AMQP Pub/Sub Durable Subscriber
- **[DO]** Use named, non-exclusive queues and explicit acknowledgment for durable subscriptions.
```javascript
// DO: Durable AMQP Subscriber
const { queue } = await channel.assertQueue('history_service_queue') // No exclusive flag
await channel.bindQueue(queue, 'chat_exchange')

channel.consume(queue, async msg => {
  const data = JSON.parse(msg.content.toString())
  await saveToDatabase(data)
  channel.ack(msg) // Acknowledge only after persistence
})
```
- **[DON'T]** Use exclusive queues or `noAck: true` when messages cannot be lost.
```javascript
// DON'T: This destroys the queue on disconnect and drops messages
const { queue } = await channel.assertQueue('history_service_queue', { exclusive: true })
channel.consume(queue, msg => { /* ... */ }, { noAck: true })
```

## Redis Streams Consumer Group Worker
- **[DO]** Read pending messages first, then loop over new messages, explicitly acknowledging them.
```javascript
// DO: Robust Redis Consumer Group
await redis.xgroup('CREATE', 'tasks_stream', 'workers_group', '$', 'MKSTREAM').catch(() => {})

// 1. Process pending messages first (ID '0')
const [[, pending]] = await redis.xreadgroup('GROUP', 'workers_group', 'worker1', 'STREAMS', 'tasks_stream', '0')
for (const [recordId, [, rawTask]] of pending) {
  await processTask(rawTask)
  await redis.xack('tasks_stream', 'workers_group', recordId)
}

// 2. Process new messages (ID '>')
while (true) {
  const [[, records]] = await redis.xreadgroup('GROUP', 'workers_group', 'worker1', 'BLOCK', '0', 'COUNT', '1', 'STREAMS', 'tasks_stream', '>')
  for (const [recordId, [, rawTask]] of records) {
    await processTask(rawTask)
    await redis.xack('tasks_stream', 'workers_group', recordId)
  }
}
```
- **[DON'T]** Use simple `xread` for task distribution or forget to `xack` records.
```javascript
// DON'T: Fails to acknowledge tasks, leaving them pending forever
const data = await redis.xreadgroup('GROUP', 'workers_group', 'worker1', 'BLOCK', '0', 'STREAMS', 'tasks_stream', '>')
processTask(data) // Missing xack!
```

## ZeroMQ Task Distribution
- **[DO]** Use `PUSH` for ventilators/workers and `PULL` for workers/sinks.
```javascript
// DO: ZeroMQ Worker
import zmq from 'zeromq'

const fromVentilator = new zmq.Pull()
const toSink = new zmq.Push()

fromVentilator.connect('tcp://localhost:5016')
toSink.connect('tcp://localhost:5017')

for await (const rawMessage of fromVentilator) {
  const result = await doWork(rawMessage)
  await toSink.send(result)
}
```
- **[DON'T]** Use `PUB/SUB` for task distribution.
```javascript
// DON'T: PUB/SUB broadcasts the same task to ALL workers, causing duplicated work!
const fromVentilator = new zmq.Subscriber()
fromVentilator.subscribe('tasks')
```

## Request/Reply Correlation Identifier
- **[DO]** Map Promises by unique ID and clear timeouts/maps on completion.
```javascript
// DO: Correlation ID implementation
const correlationMap = new Map()

function sendRequest(channel, data) {
  return new Promise((resolve, reject) => {
    const id = nanoid()
    const timeout = setTimeout(() => {
      correlationMap.delete(id)
      reject(new Error('Timeout'))
    }, 10000)

    correlationMap.set(id, replyData => {
      clearTimeout(timeout)
      resolve(replyData)
    })

    channel.sendToQueue('requests_queue', Buffer.from(JSON.stringify(data)), {
      correlationId: id,
      replyTo: 'my_private_reply_queue'
    })
  })
}

// In the consume loop for 'my_private_reply_queue':
channel.consume('my_private_reply_queue', msg => {
  const handler = correlationMap.get(msg.properties.correlationId)
  if (handler) {
    correlationMap.delete(msg.properties.correlationId)
    handler(JSON.parse(msg.content.toString()))
  }
}, { noAck: true })
```
- **[DON'T]** Assume responses arrive in the exact order requests were sent.