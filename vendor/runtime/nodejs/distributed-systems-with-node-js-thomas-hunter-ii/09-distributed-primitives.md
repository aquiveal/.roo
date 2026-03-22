@Domain
These rules MUST trigger when the AI is tasked with designing distributed system architectures, implementing caching, managing state across multiple Node.js instances, creating distributed primitives (counters, locks, queues, rate limiters, ID generators), or writing integrations with Redis (specifically using the `ioredis` package).

@Vocabulary
- **Distributed Primitive**: A core data structure (counter, list, lock, map) that maintains consistency and serves as a source of truth across multiple ephemeral instances of a distributed application.
- **Data Clobbering**: A race condition where multiple distributed instances read the same initial state, modify it locally, and write it back concurrently, overwriting each other's changes.
- **Spinlock**: A naive locking mechanism where an application continuously loops while waiting for a lock to be released. Avoided in distributed Node.js apps due to deadlock risks.
- **Deadlock**: A scenario where two or more distributed instances are stuck waiting indefinitely for each other to release resource locks.
- **Sharding**: Distributing data across a Redis cluster. Keys are hashed to determine their node location.
- **Hash Tag**: A mechanism using curly braces `{}` within a Redis key name (e.g., `user{123}:friends`) to force multiple keys to hash to the exact same cluster shard.
- **Pipelining**: Combining multiple Redis commands in a single TCP message separated by newlines to reduce network round trips.
- **Compound Command**: A native Redis command (e.g., `INCR`, `SETNX`, `RPOPLPUSH`) that performs a multi-step operation atomically.
- **Transaction (`MULTI`/`EXEC`)**: A mechanism that queues multiple commands to execute sequentially and atomically on the Redis server without interruption from other clients.
- **Lua Scripting**: Executing custom, procedural logic natively within the Redis server to ensure absolute atomicity for operations requiring conditional logic based on intermediate reads.

@Objectives
- Ensure state mutation across distributed Node.js instances remains strictly atomic to prevent race conditions and data clobbering.
- Offload state management from Node.js process memory to external distributed data stores (Redis).
- Select the most memory-efficient and performant Redis data structure for the specific business requirement.
- Strictly adhere to cluster-safe coding practices when writing Redis transactions and Lua scripts.
- Minimize blocking on the single-threaded Redis server by avoiding overly complex or slow Lua scripts.

@Guidelines
- **State Offloading**: You MUST NEVER use local Node.js primitives (like `new Map()`, `new Set()`, or arrays) to track state that must be consistent across multiple distributed service instances.
- **Redis Key Design**: 
  - Use ASCII strings for keys to avoid multi-byte string comparison issues.
  - Construct keys using compound naming conventions separated by colons (e.g., `entity:id:attribute`).
  - You MUST use Hash Tags (wrapping a shared routing identifier in `{}`) when performing cross-key operations (Transactions or Lua Scripts) to guarantee all keys reside on the same Redis cluster instance.
- **Atomicity (Read-Modify-Write)**: 
  - You MUST NEVER read a value from Redis, modify it in Node.js memory, and write it back if there is any chance another instance might modify it simultaneously.
  - ALWAYS use Compound Commands (e.g., `INCR`, `HINCRBY`) for atomic numeric updates.
  - Use `SETNX` to implement safe creation locks.
- **Choosing Data Structures**:
  - **Strings**: Use for basic values, binary payloads, and atomic counters (`INCR`, `INCRBYFLOAT`).
  - **Lists**: Use for ordered linked lists and queues. Use `RPOPLPUSH` for atomic queue processing to prevent data loss on crashes. Remember that popping the last item deletes the key.
  - **Sets**: Use for unordered, unique collections (`SADD`, `SMEMBERS`, `SCARD`).
  - **Hashes**: Use when storing objects where individual fields update independently. You MUST favor Hashes over stringified JSON if you need to atomically update a single property (to avoid parsing/stringifying overhead and race conditions). Do NOT store all application entities in one massive hash; use one hash key per entity.
  - **Sorted Sets**: Use for leaderboards, rankings, or querying items by numeric ranges (`ZADD`, `ZRANGE ... WITHSCORES`).
- **Transactions (`MULTI`/`EXEC`)**:
  - Use when executing multiple independent write commands atomically.
  - You MUST NOT use Transactions if the output of the first command determines the input of the second command (use Lua scripting instead).
- **Lua Scripting Constraints**:
  - Use Lua scripting when you need conditional logic or when a command's output feeds into the next command atomically.
  - You MUST pass ALL dynamic keys via the `KEYS` array (and specify `numberOfKeys`).
  - You MUST NEVER hardcode, concatenate, or dynamically generate key names inside the Lua script itself. Failing to pass keys explicitly breaks Redis clustering/sharding.
  - Be aware that Lua uses 1-based array indexing, whereas JavaScript uses 0-based indexing.
  - Use `ioredis`'s `defineCommand` method to automatically handle the efficient `SCRIPT LOAD` and `EVALSHA` fallback flow, preventing the overhead of sending the entire script string on every execution.
  - Keep Lua scripts extremely short and fast to avoid blocking the single-threaded Redis server.
- **Client Configuration**: Use the `ioredis` package. Be aware that `ioredis` automatically queues commands until the connection is established; you do not need to wrap early commands in connection event listeners.

@Workflow
1. **Identify the Primitive**: Determine the distributed requirement (e.g., global counter, unique set, queue, object property update).
2. **Select the Data Structure**: Map the requirement to the exact Redis data structure (String, List, Set, Hash, Sorted Set).
3. **Determine the Atomicity Strategy**:
   - Level 1: Can this be solved with a single Compound Command? (e.g., `INCR`, `HSET`, `SADD`). If yes, use it.
   - Level 2: Does it require multiple distinct writes that don't depend on each other? Use `MULTI` / `EXEC`.
   - Level 3: Does it require reading a value, making a conditional decision, and writing back atomically? Write a Lua script.
4. **Design the Keys**: Establish the key naming convention. If using Transactions or Lua across multiple keys, apply `{hash_tags}` to ensure cluster compatibility.
5. **Implement in Node.js**: Use `ioredis`. If using Lua, abstract the script behind `redis.defineCommand()`.

@Examples (Do's and Don'ts)

**Principle: Atomic Counters and Updates**
- [DO] Use Redis compound commands to handle numeric increments atomically.
```javascript
// DO: Atomically increment a counter in Redis
const Redis = require('ioredis');
const redis = new Redis();

async function incrementVisits(urlId) {
  return await redis.incr(`url:${urlId}:visits`);
}
```
- [DON'T] Read, modify in Node.js, and write back (creates a data-clobbering race condition).
```javascript
// DON'T: Vulnerable to race conditions across multiple processes
async function incrementVisits(urlId) {
  const current = Number(await redis.get(`url:${urlId}:visits`)) || 0;
  const next = current + 1; // Another process might do this exact math simultaneously
  await redis.set(`url:${urlId}:visits`, next);
  return next;
}
```

**Principle: Updating Object Properties**
- [DO] Use Redis Hashes to atomically update a specific property of an entity.
```javascript
// DO: Use Hashes for targeted, atomic field updates
async function giveRaise(employeeId, amount) {
  // Atomically increments just the wage field
  await redis.hincrby(`employee:${employeeId}`, 'wage', amount);
}
```
- [DON'T] Store large entities as JSON strings if you frequently mutate individual fields.
```javascript
// DON'T: Inefficient and vulnerable to race conditions
async function giveRaise(employeeId, amount) {
  const json = await redis.get(`employee:${employeeId}`);
  const employee = JSON.parse(json);
  employee.wage += amount; // If wage was updated elsewhere, that data is now lost
  await redis.set(`employee:${employeeId}`, JSON.stringify(employee));
}
```

**Principle: Lua Script Key Management**
- [DO] Pass all keys explicitly to the `KEYS` array to support Redis clustering, and use `defineCommand` to optimize script delivery via `EVALSHA`.
```javascript
// DO: Define command and pass keys correctly
const fs = require('fs');
redis.defineCommand('joinLobby', {
  numberOfKeys: 2,
  lua: `
    local lobbyKey = KEYS[1]
    local gameKey = KEYS[2]
    local userId = ARGV[1]
    
    redis.call('SADD', lobbyKey, userId)
    if redis.call('SCARD', lobbyKey) == 4 then
      local members = table.concat(redis.call('SMEMBERS', lobbyKey), ",")
      redis.call('DEL', lobbyKey)
      local gameId = redis.sha1hex(members)
      redis.call('HSET', gameKey, gameId, members)
      return {gameId, members}
    end
    return nil
  `
});

// Notice the `{pvp}` hash tag ensuring both keys live on the same cluster node
const [gameId, players] = await redis.joinLobby('lobby{pvp}', 'games{pvp}', 'player123');
```
- [DON'T] Dynamically construct or hardcode key names inside the Lua script.
```javascript
// DON'T: Hardcoding keys inside Lua breaks clustering and sharding
redis.defineCommand('badJoinLobby', {
  numberOfKeys: 0,
  lua: `
    local userId = ARGV[1]
    -- TERRIBLE: Redis doesn't know these keys are being accessed before execution
    redis.call('SADD', 'global_lobby', userId) 
    -- ...
  `
});
```

**Principle: Transactions**
- [DO] Use `MULTI` and `EXEC` for executing independent, multi-key modifications atomically.
```javascript
// DO: Atomic transaction for cross-entity cleanup
async function removeEmployee(employeeId) {
  await redis.multi()
    .srem('employees:active', employeeId)
    .hdel(`employee:${employeeId}`, 'company-id')
    .exec();
}
```
- [DON'T] Attempt to use the result of a command inside the same transaction block.
```javascript
// DON'T: Transactions do not return values until .exec() is called
async function popAndPush() {
  const multi = redis.multi();
  const item = await multi.rpop('queue:pending'); // `item` is not the value, it's the transaction state!
  multi.lpush('queue:processing', item); // Fails
  await multi.exec();
}
// Note: Use the native RPOPLPUSH compound command for this specific scenario.
```