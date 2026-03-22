@Domain
Trigger these rules when the user requests architectural design, analysis, refactoring, or code generation for systems requiring extreme scalability, high elasticity, high performance, and the ability to handle variable or unpredictable concurrent user volumes. Activation is strictly required when the terms "Space-Based Architecture", "SBA", "tuple space", or "in-memory data grid" are mentioned.

@Vocabulary
- **Tuple Space:** The foundational concept of multiple parallel processors communicating through shared memory, which gives Space-Based Architecture its name.
- **Processing Unit:** The component containing application logic (web and/or backend) and an in-memory data grid/replicated cache. 
- **Virtualized Middleware:** The infrastructure layer responsible for managing and coordinating the processing units. Comprises the Messaging Grid, Data Grid, Processing Grid, and Deployment Manager.
- **Messaging Grid:** The virtualized middleware component that manages input requests, session state, and routes requests to available processing units (e.g., HA Proxy, Nginx).
- **Data Grid:** The replicated cache mechanism interacting synchronously within processing units to keep data state synchronized across instances (e.g., Hazelcast, Apache Ignite, Oracle Coherence).
- **Processing Grid:** An optional middleware component that mediates and orchestrates requests requiring coordination between multiple distinct processing unit types.
- **Deployment Manager:** The component that dynamically starts up and shuts down processing unit instances based on current load conditions to achieve variable scalability (elasticity).
- **Data Pump:** An asynchronous messaging component (persistent queue) that sends updated data from a Processing Unit to a Data Writer to eventually update the database.
- **Data Writer:** A component (service, application, or data hub) that accepts messages from a Data Pump and executes the database update logic (e.g., SQL).
- **Data Reader:** A component invoked only during startup, recovery, or archive retrieval that reads database data and sends it to Processing Units via a reverse data pump.
- **Data Abstraction Layer:** A decoupling model formed by Data Readers and Writers ensuring Processing Units are agnostic to underlying database table schemas, allowing for incremental DB changes.
- **Data Collision:** A state inconsistency occurring when the same cached data is updated concurrently in different Processing Units before replication completes.
- **Replicated Caching:** An active/active caching model where every Processing Unit holds a copy of the cache, synchronized across all instances. High performance, high fault tolerance, but limited by memory capacity.
- **Distributed Caching:** A centralized caching model using external cache servers. Slower performance and lower fault tolerance, but provides high data consistency and supports massive datasets.
- **Near-Cache:** A hybrid caching model using a full backing distributed cache and localized front caches (MRU/MFU/Random Replacement). Explicitly discouraged in SBA due to inconsistent performance.

@Objectives
- Eliminate the database as a synchronous bottleneck in the application's transactional processing path.
- Maximize Elasticity, Scalability, and Performance (achieving 5-star ratings for these characteristics).
- Guarantee eventual consistency between the in-memory data grids and the physical database using reliable asynchronous messaging.
- Decouple the application's processing capacity from the database's scaling limitations (avoiding the "triangle-shaped topology" trap).
- Provide architectural mechanisms to automatically scale up and scale down based on unpredictable user loads.

@Guidelines
- **Synchronous Database Constraint:** The AI MUST NOT design or implement direct, synchronous read/write database connections within the Processing Units. All database updates MUST occur asynchronously via Data Pumps.
- **Processing Unit Design:** The AI MUST encapsulate application code and an in-memory data grid within independently deployable Processing Units.
- **Middleware Implementation:** The AI MUST route all incoming requests through a Messaging Grid, orchestrate complex requests via a Processing Grid, and dynamically scale instances using a Deployment Manager.
- **Data Pump Mechanics:** The AI MUST implement Data Pumps using asynchronous, persistent message queues with FIFO ordering, guaranteed delivery, and client acknowledge modes to prevent data loss.
- **Data Abstraction:** The AI MUST enforce a Data Abstraction Layer. Processing Units must not contain SQL or DB schema definitions; these belong exclusively to Data Writers and Data Readers.
- **Cache Population:** The AI MUST design Data Readers to be invoked ONLY during total cache loss, system startup/redeployment, or when requesting archived data. Temporary cache ownership locks MUST be used to prevent concurrent read floods during startup.
- **Data Collision Calculations:** When recommending Replicated Caching, the AI MUST calculate and evaluate the probability of Data Collisions using the formula: `Collision Rate = N * (UR^2 / S) * RL` (where `N` = number of instances, `UR` = update rate, `S` = cache size in rows, and `RL` = replication latency). 
- **Caching Strategy Selection:**
  - The AI MUST recommend **Replicated Caching** for small datasets (<100 MB), relatively static data, low update frequencies, and requirements demanding high fault tolerance and extreme performance.
  - The AI MUST recommend **Distributed Caching** for large datasets (>500 MB), highly dynamic data, high update rates, and strict consistency requirements.
- **Near-Cache Anti-Pattern:** The AI MUST explicitly reject and avoid implementing Near-Cache topologies (front caches with a full backing cache) to prevent inconsistent responsiveness between processing units.
- **Hybrid Cloud Deployments:** When security and extreme elasticity are both required, the AI MUST propose deploying Processing Units and Virtualized Middleware in elastic cloud environments while keeping Data Writers, Data Readers, and physical databases in secure on-premises environments.
- **Testing Constraints:** The AI MUST acknowledge the 1-star testability rating of SBA and design automated deployment scripts and production-like staging environments to safely simulate extreme load testing.

@Workflow
1. **Topology Definition:** Establish the Processing Units required for the domain. Group application logic and assign the appropriate in-memory data grids (Hazelcast, Ignite, etc.) to these units.
2. **Middleware Configuration:** Define the Messaging Grid for load balancing and the Deployment Manager with metrics-based scaling thresholds to handle unpredictable bursts.
3. **Caching Strategy Assessment:** Analyze data volume, update frequency, and consistency needs to assign either Replicated Caching or Distributed Caching to each data domain. Calculate data collision risks if Replicated Caching is selected.
4. **Data Pump & Writer Design:** Create asynchronous messaging queues (Data Pumps) mapped to specific data domains. Design corresponding Data Writers to consume these messages and execute DB schemas/SQL.
5. **Data Reader Design:** Formulate the reverse data pump and caching lock mechanism required to hydrate the in-memory grids upon cold startup or system crash.
6. **Data Loss Prevention:** Verify that the messaging infrastructure implements synchronous send, persistent queues, client acknowledge modes, and ACID commits in the Data Writers with Last Participant Support (LPS).

@Examples (Do's and Don'ts)

- **[DO]** Asynchronous Database Updates via Data Pumps
  ```java
  // Inside the Processing Unit:
  public void updateCustomerProfile(CustomerProfile profile) {
      // 1. Update the replicated in-memory data grid
      profileCache.put(profile.getId(), profile);
      // 2. Asynchronously send update to Data Pump (Message Queue)
      messageQueue.send(new DataPumpMessage("UPDATE", profile));
      // Return immediately to user
  }

  // Inside the Data Writer (Separate Component):
  public void processDataPumpMessage(DataPumpMessage msg) {
      // Execute SQL update using ACID transaction
      database.update("UPDATE customer SET ... WHERE id = ?", msg.getProfile());
      messageQueue.acknowledge(msg);
  }
  ```

- **[DON'T]** Synchronous Database Calls within Processing Units
  ```java
  // ANTI-PATTERN: Direct database connection inside Processing Unit
  public void updateCustomerProfile(CustomerProfile profile) {
      profileCache.put(profile.getId(), profile);
      // Blocks the thread, creating a massive bottleneck under load
      database.update("UPDATE customer SET ...", profile); 
  }
  ```

- **[DO]** Safe Data Hydration via Data Readers
  ```java
  public void onStartup() {
      if (cache.tryLock("HydrationLock")) {
          try {
              // Send request to Data Reader via reverse data pump
              dataReaderQueue.send(new CacheHydrationRequest("CustomerProfile"));
              // Listen for reverse data pump response and populate
              populateCacheFromResponse();
          } finally {
              cache.unlock("HydrationLock");
          }
      } else {
          // Wait for the lock-holder to finish hydrating the replicated cache
          waitForCacheHydration();
      }
  }
  ```

- **[DON'T]** Near-Cache Implementation
  ```xml
  <!-- ANTI-PATTERN: Configuring Near-Cache in Space-Based Architecture -->
  <near-cache name="CustomerProfile">
      <eviction max-size="1000" eviction-policy="LRU"/>
      <!-- This causes unpredictable latency between instances and MUST BE REJECTED -->
  </near-cache>
  ```