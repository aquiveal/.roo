# @Domain
These rules MUST be activated when the AI is tasked with generating, modifying, or reviewing tests for a microservices-based application, specifically focusing on unit testing, implementing automated testing strategies, defining test suites, configuring Continuous Integration (CI) test pipelines, or testing specific architectural components (Entities, Value Objects, Sagas, Domain Services, Controllers, Event/Message Handlers).

# @Vocabulary
- **SUT (System Under Test)**: The specific software element being tested, ranging from a single class to an entire application.
- **Test Fixture**: Everything required to run a test, including the SUT and its dependencies in a specific state.
- **Test Double**: An object that simulates the behavior of a dependency to enable testing the SUT in isolation.
- **Stub**: A test double that returns predefined values to the SUT.
- **Mock**: A test double used to verify that the SUT correctly invokes a dependency.
- **Four-Phase Test**: The standard structure of an automated test, consisting of Setup, Exercise, Verify, and Teardown.
- **Compile-Time Tests**: Fast-running tests (primarily unit tests) that provide immediate feedback and execute in seconds during the code-edit-test loop.
- **Test Quadrant**: A categorization matrix for tests defined by two dimensions: business-facing vs. technology-facing, and supporting programming vs. critiquing the application.
- **Test Pyramid**: A guiding model dictating the relative proportions of test types: a massive base of fast, reliable unit tests, a middle layer of integration/component tests, and a tiny peak of slow, brittle end-to-end tests.
- **Solitary Unit Test**: A unit test that tests a class in complete isolation by mocking or stubbing its dependencies.
- **Sociable Unit Test**: A unit test that tests a class alongside its real dependencies.
- **Consumer-Driven Contract Test**: An integration testing strategy where a provider service's API is verified against the specific expectations (contracts/examples) of its consumer services, avoiding the need for end-to-end test environments.
- **Deployment Pipeline**: The automated process of getting code from commit to production, passing through stages: Pre-commit, Commit, Integration, Component, and Deploy.

# @Objectives
- The AI MUST prioritize the creation of fast, reliable, automated unit tests (the base of the Test Pyramid) to replace slow, manual, or brittle end-to-end testing.
- The AI MUST meticulously decouple the SUT from its environment using Test Doubles (Mocks and Stubs) where appropriate, based on the architectural role of the class.
- The AI MUST strictly apply the Four-Phase Test structure to every generated test.
- The AI MUST select the correct unit testing strategy (Solitary vs. Sociable) dictated by the specific type of microservice component being tested.
- The AI MUST facilitate Consumer-Driven Contract testing concepts when designing tests for Inter-Process Communication (IPC) boundaries (REST, messaging).

# @Guidelines

### Test Structure and Organization
- The AI MUST format every generated test into four distinct phases: 
  1. **Setup**: Initialize the test fixture, instantiate the SUT, and configure test doubles.
  2. **Exercise**: Invoke the SUT.
  3. **Verify**: Make assertions about the outcome, return values, and mock invocations.
  4. **Teardown**: Clean up the test fixture (if applicable, typically used in database tests).
- The AI MUST prioritize unit tests over component and end-to-end tests, referencing the Test Pyramid.

### Handling Dependencies
- When the SUT has dependencies that are complex, slow, or communicate over the network, the AI MUST replace them with Test Doubles.
- The AI MUST use Stubs when the test simply requires the dependency to return data to the SUT.
- The AI MUST use Mocks when the test needs to assert that the SUT invoked the dependency with specific arguments.

### Component-Specific Unit Testing Rules
- **Entities**: The AI MUST generate Sociable Unit Tests for DDD Entities. Setup the entity, invoke its state-changing methods, and verify the resulting state and emitted domain events. Do not mock internal state logic.
- **Value Objects**: The AI MUST generate Sociable Unit Tests for Value Objects. Because they are immutable and have no side effects, the AI MUST invoke methods and assert the return values directly.
- **Sagas**: The AI MUST generate Sociable Unit Tests for Sagas. The AI MUST mock the database and messaging infrastructure using a dedicated testing DSL (e.g., Eventuate Tram Saga testing framework) to verify that the Saga sends the correct sequence of command messages and handles participant replies (both success and failure/compensating transactions).
- **Domain Services**: The AI MUST generate Solitary Unit Tests for Domain Services. The AI MUST mock repositories, messaging classes, and other service dependencies. The AI MUST use mock verification (e.g., `verify()`) to assert that the Domain Service saved objects and published events correctly.
- **Controllers (REST APIs)**: The AI MUST generate Solitary Unit Tests for Controllers. The AI MUST NOT start a real web server. Instead, the AI MUST use a Mock MVC framework (e.g., Spring Mock Mvc or Rest Assured Mock MVC) to test HTTP request routing, parameter extraction, and JSON serialization/deserialization, while mocking the underlying Domain Service.
- **Event and Message Handlers**: The AI MUST generate Solitary Unit Tests for inbound message adapters. The AI MUST use a mock messaging framework to simulate receiving a message/event and verify that the adapter correctly parses the payload and invokes the mocked Domain Service.

### Integration and Pipeline Strategy
- When discussing or configuring CI/CD, the AI MUST organize tests into a Deployment Pipeline consisting of: Pre-commit (fast unit tests), Commit (compile, unit tests, static analysis), Integration, Component, and Deploy.
- When generating tests for API interactions (REST or messaging) between services, the AI MUST advocate for and structure Consumer-Driven Contract Tests using example-based contracts, entirely avoiding the instantiation of the entire microservice ecosystem.

# @Workflow
When tasked with writing a test for a microservice component, the AI MUST execute the following algorithmic process:
1. **Identify the Component Type**: Analyze the SUT to determine if it is an Entity, Value Object, Saga, Domain Service, Controller, or Event/Message Handler.
2. **Determine the Test Strategy**: 
   - If Entity, Value Object, or Saga -> Select *Sociable Unit Test*.
   - If Domain Service, Controller, or Handler -> Select *Solitary Unit Test*.
3. **Identify and Isolate Dependencies**: List all dependencies of the SUT. For Solitary tests, explicitly create Mocks or Stubs for these dependencies.
4. **Construct the Setup Phase**: Write the code to instantiate the mocks, configure stub return values (e.g., `when(...).thenReturn(...)`), and instantiate the SUT injecting the test doubles.
5. **Construct the Exercise Phase**: Write the exact trigger invoking the target behavior (e.g., making a Mock MVC HTTP request, or calling the business method).
6. **Construct the Verify Phase**: Write the assertions to validate return values, JSON payloads, HTTP status codes, or use `verify(...)` to ensure mocks were called with the exact expected parameters.
7. **Construct the Teardown Phase**: Write cleanup logic if the framework or environment requires resetting shared state.

# @Examples (Do's and Don'ts)

### 1. Testing Domain Services (Solitary)
[DO]
```java
public class OrderServiceTest {
    private OrderService orderService;
    private OrderRepository orderRepository;
    private DomainEventPublisher eventPublisher;

    @Before
    public void setup() {
        // 1. Setup: Configure mocks
        orderRepository = mock(OrderRepository.class);
        eventPublisher = mock(DomainEventPublisher.class);
        orderService = new OrderService(orderRepository, eventPublisher);
    }

    @Test
    public void shouldCreateOrder() {
        // 1. Setup: Stub behavior
        when(orderRepository.save(any(Order.class))).then(invocation -> {
            Order order = (Order) invocation.getArguments()[0];
            order.setId(101L);
            return order;
        });

        // 2. Exercise
        Order order = orderService.createOrder(1L, 2L, MENU_ITEMS);

        // 3. Verify
        verify(orderRepository).save(same(order));
        verify(eventPublisher).publish(eq(Order.class), eq(101L), anyList());
    }
}
```

[DON'T]
```java
// Anti-pattern: Using a real database repository in a Domain Service unit test (makes it slow and brittle).
public class OrderServiceTest {
    @Autowired
    private OrderRepository realRepository; // DON'T DO THIS
    
    @Test
    public void shouldCreateOrder() {
        OrderService service = new OrderService(realRepository);
        service.createOrder(1L, 2L, MENU_ITEMS);
        assertNotNull(realRepository.findById(1L)); // End-to-end integration bleed
    }
}
```

### 2. Testing Controllers (Solitary)
[DO]
```java
public class OrderControllerTest {
    private OrderService orderService;
    
    @Before
    public void setup() {
        // 1. Setup
        orderService = mock(OrderService.class);
    }

    @Test
    public void shouldFindOrder() {
        // 1. Setup
        when(orderService.findById(1L)).thenReturn(Optional.of(TEST_ORDER));
        
        // 2. Exercise & 3. Verify (using Rest Assured Mock MVC)
        given().
            standaloneSetup(new OrderController(orderService)).
        when().
            get("/orders/1").
        then().
            statusCode(200).
            body("orderId", equalTo(1)).
            body("state", equalTo("APPROVAL_PENDING"));
    }
}
```

[DON'T]
```java
// Anti-pattern: Starting the full Spring Boot application context and real web server to test a single controller method.
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class OrderControllerTest {
    @Test
    public void shouldFindOrder() {
        // DON'T run the entire app just to test HTTP routing and JSON mapping.
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response = restTemplate.getForEntity("http://localhost:8080/orders/1", String.class);
        assertEquals(200, response.getStatusCodeValue());
    }
}
```

### 3. Testing Value Objects (Sociable)
[DO]
```java
public class MoneyTest {
    // 1. Setup
    private Money m1 = new Money(10);
    private Money m2 = new Money(15);

    @Test
    public void shouldAdd() {
        // 2. Exercise & 3. Verify
        assertEquals(new Money(25), m1.add(m2));
    }
}
```

[DON'T]
```java
// Anti-pattern: Mocking an immutable value object.
public class MoneyTest {
    @Test
    public void shouldAdd() {
        Money m1 = mock(Money.class); // DON'T DO THIS
        when(m1.add(any())).thenReturn(new Money(25));
    }
}
```

### 4. Testing Sagas (Sociable with Mocked Infrastructure)
[DO]
```java
public class CreateOrderSagaTest {
    @Test
    public void shouldRejectOrderDueToConsumerVerificationFailed() {
        // 1. Setup, 2. Exercise, 3. Verify using Saga DSL
        given()
            .saga(new CreateOrderSaga(kitchenProxy), new CreateOrderSagaState(ORDER_ID, DETAILS))
        .expect()
            .command(new ValidateOrderByConsumer(CONSUMER_ID, ORDER_ID, TOTAL))
            .to("consumerServiceChannel")
        .andGiven()
            .failureReply() // Simulate consumer service rejecting
        .expect()
            .command(new RejectOrderCommand(ORDER_ID))
            .to("orderServiceChannel");
    }
}
```

[DON'T]
```java
// Anti-pattern: Testing sagas by deploying RabbitMQ/Kafka and microservices.
public class CreateOrderSagaTest {
    @Test
    public void testSaga() {
        // DON'T stand up infrastructure and poll databases to test Saga orchestration logic.
        rabbitTemplate.convertAndSend("consumerChannel", new ValidateCommand());
        Thread.sleep(5000); 
        // ...
    }
}
```