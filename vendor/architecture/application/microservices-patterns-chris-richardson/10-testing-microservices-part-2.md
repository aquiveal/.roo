# @Domain
Triggered when the user requests the creation, modification, or review of tests in a microservices architecture, specifically focusing on integration tests, component tests, end-to-end (E2E) tests, consumer-driven contract testing, API testing, or persistent layer testing. 

# @Vocabulary
- **Integration Test**: A test that verifies a service can properly interact with infrastructure services (e.g., databases) and other application services, testing individual adapter classes rather than launching the whole service.
- **Component Test**: A business-facing acceptance test that verifies the behavior of a single service in isolation by replacing its application service dependencies with stubs.
- **End-to-End (E2E) Test**: A business-facing test that runs the entire application (multiple services) to verify high-level system behavior.
- **Consumer-Driven Contract Test**: An integration test for a provider that verifies its API matches the exact expectations of a consumer, utilizing predefined contracts.
- **Contract**: A concrete example of an interaction between a pair of services (e.g., an HTTP request/response pair or a specific domain event message).
- **Consumer**: A service that invokes another service's API (e.g., API Gateway calling Order Service, or a service subscribing to domain events).
- **Provider**: A service that exposes an API or publishes an event consumed by another service.
- **Spring Cloud Contract**: A framework used to write contracts and automatically generate provider-side tests and configure consumer-side stubs.
- **WireMock**: A tool used to stub HTTP servers in consumer-side integration tests.
- **Gherkin**: A domain-specific language (DSL) for writing executable specifications using `Given-When-Then` syntax.
- **Cucumber**: An automated testing framework that executes Gherkin specifications by mapping steps to Java methods.
- **In-process Component Test**: A test that runs the service in the same JVM as the test (e.g., `@SpringBootTest`) using in-memory stubs and mocks.
- **Out-of-process Component Test**: A test that runs the service as a separate process (e.g., a Docker container) using real infrastructure but stubbed application dependencies.
- **User Journey Test**: An end-to-end test strategy that combines multiple operations (e.g., create, revise, cancel) into a single, comprehensive scenario to minimize the number of slow E2E tests.

# @Objectives
- Validate inter-service communication quickly and reliably without standing up the entire microservice ecosystem.
- Ensure that provider APIs and consumer expectations remain strictly synchronized using consumer-driven contract testing.
- Verify individual service behavior in isolation using component tests driven by business-readable Gherkin specifications.
- Minimize the number, execution time, and brittleness of end-to-end tests by consolidating operations into User Journey tests.
- Maintain a strict testing pyramid: maximize unit tests, utilize targeted integration tests for adapters, restrict component tests to isolated boundaries, and strictly limit end-to-end tests.

# @Guidelines
- **Integration Testing Constraints:**
  - The AI MUST NOT write integration tests that launch the entire application or multiple services simultaneously. 
  - The AI MUST scope integration tests strictly to the individual adapter classes (e.g., JPA repositories, REST controllers, event publishers) along with their supporting classes.
- **Persistence Integration Testing:**
  - The AI MUST structure persistence integration tests using four phases: Setup, Execute, Verify, and Teardown.
  - The AI MUST use Docker (e.g., via Docker Compose plugins in Gradle/Maven) to provision real infrastructure services (like MySQL or DynamoDB) during test execution rather than relying solely on in-memory replacements.
  - The AI MUST NOT use transaction rollbacks for teardown if the test relies on the ORM to create the database schema, as this can cause in-memory caching discrepancies.
- **Consumer-Driven Contract Testing (REST):**
  - The AI MUST define contracts for REST interactions containing specific HTTP methods, URLs, status codes, headers, and bodies.
  - For Consumer-side REST tests, the AI MUST use Spring Cloud Contract's `@AutoConfigureStubRunner` to mock the provider using WireMock.
  - For Provider-side REST tests, the AI MUST use Rest Assured Mock MVC in a generated test superclass to mock the service's internal business logic and test the controller in isolation.
- **Consumer-Driven Contract Testing (Messaging & Events):**
  - The AI MUST define messaging contracts specifying the channel, body, headers, a `label` for triggering, and a `triggeredBy` method.
  - For Consumer-side event tests, the AI MUST use Spring Cloud Contract stub triggers to publish the contract event and verify the local event handler updates the mocked persistence layer.
  - For Provider-side event tests, the AI MUST configure the base test class to invoke the event publisher using in-memory messaging stubs, catching and validating the emitted event against the contract.
- **Component Testing Rules:**
  - The AI MUST write component tests using Gherkin (`.feature` files) and Cucumber step definition classes.
  - The AI MUST configure step definitions to use `@ContextConfiguration` for Spring integration.
  - When writing Out-of-process component tests, the AI MUST stub application dependencies internally within the test setup (e.g., using WireMock or a custom `SagaParticipantStubManager`) rather than relying on Spring Cloud Contract, which is too heavyweight for this tier.
  - The AI MUST run the service under test and its infrastructure dependencies as Docker containers using a build tool plugin (e.g., Gradle Docker Compose).
- **End-to-End Testing Rules:**
  - The AI MUST write E2E tests using Gherkin/Cucumber.
  - The AI MUST design E2E tests strictly as "User Journey Tests" that chain together multiple actions (e.g., Place Order -> Revise Order -> Cancel Order) in a single test scenario to reduce test setup overhead and execution time.

# @Workflow
When tasked with writing tests for a microservice, the AI MUST execute the following algorithm:
1. **Determine Test Tier:** Analyze the request to determine if it requires an Integration Test, Component Test, or End-to-End Test.
2. **For Integration Tests (REST or Messaging):**
   1. Generate the Groovy Contract specifying the exact input (request/message) and output (response/event).
   2. Write the Provider-side abstract base class defining the setup (e.g., Mockito mocks injected into controllers/publishers) and hook methods (`triggeredBy`).
   3. Write the Consumer-side integration test using `@AutoConfigureStubRunner` to retrieve the contract and validate the consumer proxy/handler.
3. **For Persistence Integration Tests:**
   1. Write the test targeting the specific Repository/DAO class.
   2. Wrap the execution and verification phases in explicit transactional blocks if required to accurately simulate database commit behavior.
4. **For Component Tests:**
   1. Write the high-level Gherkin `.feature` file defining the business scenario using `Given/When/Then` steps.
   2. Implement the Java Step Definitions class mapping the Gherkin steps to REST API calls or stub configurations.
   3. Define the infrastructure requirements (e.g., Docker Compose configurations) needed to spin up the isolated service and its DB/Broker.
5. **For End-to-End Tests:**
   1. Consolidate required assertions into a single User Journey Gherkin scenario.
   2. Write step definitions that interact with the system entirely through the external API Gateway or frontend interfaces, verifying global state changes.

# @Examples (Do's and Don'ts)

## Integration Testing: Provider-Side REST
- **[DO]** Use Rest Assured Mock MVC in a base class to isolate the controller during contract tests.
```java
public abstract class HttpBase {
    @Before
    public void setup() {
        OrderService orderService = mock(OrderService.class);
        OrderRepository orderRepository = mock(OrderRepository.class);
        OrderController orderController = new OrderController(orderService, orderRepository);
        
        when(orderRepository.findById(1223232L))
            .thenReturn(Optional.of(OrderDetailsMother.CHICKEN_VINDALOO_ORDER));
            
        RestAssuredMockMvc.standaloneSetup(orderController);
    }
}
```
- **[DON'T]** Boot up the entire Spring Context with real databases for a REST provider contract test.

## Integration Testing: Consumer-Side REST
- **[DO]** Use Spring Cloud Contract stub runners to mock the provider.
```java
@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment= SpringBootTest.WebEnvironment.NONE)
@AutoConfigureStubRunner(ids = {"net.chrisrichardson.ftgo.contracts:ftgo-order-service-contracts"}, workOffline = false)
public class OrderServiceProxyIntegrationTest {
    @Value("${stubrunner.runningstubs.ftgo-order-service-contracts.port}")
    private int port;
    
    // Configure WebClient to hit localhost:port
}
```
- **[DON'T]** Hardcode HTTP mock responses manually using standard Mockito on the `WebClient`; always use the contract-generated stubs.

## Component Testing
- **[DO]** Write acceptance tests in Gherkin and map them to Cucumber step definitions.
```gherkin
Feature: Place Order
  Scenario: Order authorized
    Given a valid consumer
    And using a valid credit card
    When I place an order for Chicken Vindaloo
    Then the order should be APPROVED
```
```java
@ContextConfiguration(classes = TestConfiguration.class)
public class OrderServiceComponentTestStepDefinitions {
    @Given("using a (.*) credit card")
    public void useCreditCard(String creditCard) {
        if (creditCard.equals("valid")) {
            sagaParticipantStubManager.forChannel("accountingService")
                .when(AuthorizeCommand.class).replyWithSuccess();
        }
    }
}
```
- **[DON'T]** Write component tests in pure Java without a DSL, or use Spring Cloud Contract for stubbing out-of-process component test dependencies.

## End-to-End Testing
- **[DO]** Combine operations into a single User Journey.
```gherkin
Scenario: Order created, revised, and cancelled
    Given a valid consumer
    When I place an order
    Then the order should be APPROVED
    And when I revise the order by adding 2 samosas
    Then the order total should be 20.97
    And when I cancel the order
    Then the order should be CANCELLED
```
- **[DON'T]** Write three separate E2E scenarios for create, revise, and cancel, as this triggers the massive setup/teardown overhead of E2E tests three times.