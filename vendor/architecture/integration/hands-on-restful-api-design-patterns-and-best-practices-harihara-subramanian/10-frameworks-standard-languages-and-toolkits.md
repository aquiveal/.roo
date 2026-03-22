@Domain
Trigger these rules when the user requests assistance with selecting, designing, scaffolding, or implementing RESTful APIs and microservices in Java, Go (Golang), or Python. Activation occurs specifically when dealing with framework selection, boilerplate generation, routing setups, database integrations, or applying framework-specific idioms for Spring Boot, Light 4j, Spark, Dropwizard, Gin-gonic, Revel, Django REST Framework (DRF), or Flask-RESTful.

@Vocabulary
- **Opinionated Framework:** A framework that dictates a specific, standard way of doing things, challenging defaults only when explicitly customized (e.g., Spring Boot).
- **Boilerplate:** Reusable code libraries or structural code incorporated with little or no alteration. Frameworks aim to minimize this.
- **Scaffolding:** The automated generation of a project's foundational structure and boilerplate code (e.g., using `light-code-gen`).
- **Profile:** A Spring Boot mechanism to segregate parts of an application's configuration and make it available only to specific environments.
- **Auto-configuration:** Framework modules (like in Spring) available in the classpath that eliminate the need to define specific beans manually.
- **Light-code-gen:** A command-line scaffolding tool used in Light 4j, relying on OpenAPI 3.0 or GraphQL IDL specifications.
- **Lambda Philosophy:** The design principle used in Spark (Java) leveraging Java 8 lambda expressions to create REST APIs with minimal verbosity.
- **HttpRouter / Mux:** A lightweight, high-performance HTTP request router/multiplexer used in Gin-gonic, utilizing a compressing radix tree structure.
- **Interceptors:** Functions in the Revel framework invoked BEFORE or AFTER a specific event (Function, Method, or Controller interceptors).
- **Filters (Revel):** Composable middleware in Revel used to implement horizontal concerns like request logging or authorization.
- **Web-browsable API:** A Django REST Framework (DRF) feature that returns self-describing APIs capable of rendering JSON or HTML representations directly in a web browser.
- **Serializer:** A DRF class that converts complex data (querysets, model instances) into native Python datatypes for rendering into JSON/XML, and vice versa (deserialization).
- **Resourceful Routing:** A Flask-RESTful concept utilizing pluggable views (Resource classes) to define and map HTTP methods directly to class methods.
- **ReqParse:** A Flask-RESTful interface modeled after `argparse` for uniform access and validation of variables in the request object.

@Objectives
- Accurately assess the user's architectural needs (e.g., scale, footprint, language preference) to recommend the exact framework prescribed by the chapter.
- Enforce the native idioms and architectural constraints of the selected framework (e.g., using lambdas for Spark, embedded servers for Dropwizard).
- Ensure horizontal concerns (NFRs) like logging, metrics, security, and health checks are implemented using the framework's native, out-of-the-box libraries.
- Prevent the AI from mixing paradigms (e.g., introducing standard Go `net/http` mux into a Gin project, or external Tomcat configurations into Dropwizard).

@Guidelines

Framework Selection Rules:
- When the user requires a Java framework for rapid, enterprise-ready development with built-in SQL/NoSQL support and messaging, the AI MUST use **Spring Boot**.
- When the user requires a Java SE-based, cloud-native microservice with the lowest latency, smallest footprint, and security-first design (OAuth2 integration), the AI MUST use **Light 4j**.
- When the user requires a Java API built with minimal verbosity (<10 lines) for rapid prototyping, the AI MUST use **Spark Framework**.
- When the user requires a mature, ops-friendly Java framework with robust production metrics and reliable reused libraries (Jetty, Jersey, Jackson), the AI MUST use **Dropwizard**.
- When the user requires a Go framework optimizing for smashing performance, zero-allocation routing, and Http2 server push, the AI MUST use **Gin-gonic**.
- When the user requires a fully-featured, full-stack Go web framework with customizable middleware, hot-code reload, and interceptors, the AI MUST use **Revel**.
- When the user requires a Python API with powerful serialization, out-of-the-box authentication policies, and web-browsable interfaces, the AI MUST use **Django REST Framework (DRF)**.
- When the user requires a Python microframework with minimal setup, resourceful routing, and lightweight abstraction, the AI MUST use **Flask-RESTful**.

Spring Boot Implementation Rules:
- The AI MUST use `spring-boot-starter` packages for dependency management.
- The AI MUST configure environment-specific settings using YAML (`application.yml`) and utilize Spring Profiles.
- For data access, the AI MUST utilize `JdbcTemplate` or Spring Data Repositories for SQL, and Spring Data for NoSQL.
- The AI MUST use `JmsTemplate`, AMQP, or Apache Kafka integrations for messaging.
- For testing, the AI MUST implement `spring-boot-starter-test` utilizing JUnit, AssertJ, Hamcrest, and Mockito.

Light 4j Implementation Rules:
- The AI MUST enforce a design-driven approach by requiring an OpenAPI 3.0 specification or GraphQL IDL before generating code.
- The AI MUST use the `light-code-gen` command-line tool (or its Docker/Maven equivalent) to scaffold the project.
- The AI MUST configure built-in handlers for cross-cutting concerns (auditing, load-balancing, authentication) to keep business logic isolated.

Spark Framework (Java) Implementation Rules:
- The AI MUST strictly adhere to the Java 8 lambda philosophy for routing.
- The AI MUST define routes using static imports (`import static spark.Spark.*;`).
- The AI MUST NOT introduce heavy container configurations; rely on Spark's lightweight embedded server.

Dropwizard Implementation Rules:
- The AI MUST bundle and configure applications to run as a simple Unix process via a `main` method utilizing the embedded Jetty server.
- The AI MUST use Jersey for RESTful web services, mapping HTTP requests to plain Java objects.
- The AI MUST use Jackson for all JSON object mapping.
- The AI MUST implement the Metrics library (along with Logback/slf4j) to measure component behavior.
- The AI MUST use Liquibase for database schema revision management.

Gin-gonic Implementation Rules:
- The AI MUST use `HttpRouter` (custom multiplexer) for path matching and variable binding.
- The AI MUST use `multipart.write` to handle file uploads, caching them before server delivery.
- The AI MUST group routes and utilize custom middleware for request handling.

Revel Implementation Rules:
- The AI MUST define URLs and routes in the explicit format: `[METHOD] [URL Pattern] [Controller.Method]`.
- The AI MUST isolate horizontal concerns (logging, cookie policies, auth) using Filters (middleware).
- The AI MUST implement Interceptors for logic that must run BEFORE or AFTER specific events.
- The AI MUST utilize Revel's built-in testing modules for functional test cases.

Django REST Framework (DRF) Implementation Rules:
- The AI MUST implement class-based views or Generic views to map database models to API endpoints.
- The AI MUST define `Serializer` or `ModelSerializer` classes to control JSON/XML rendering and input validation (deserialization).
- The AI MUST configure an authentication scheme (Basic, Token, Session, or OAuth) that runs at the very start of the view.
- The AI MUST utilize DRF Routers to wire view logic to URLs automatically.

Flask-RESTful Implementation Rules:
- The AI MUST implement API endpoints inside classes that inherit from `flask_restful.Resource`.
- The AI MUST use `reqparse.RequestParser()` to validate and parse incoming HTTP request arguments.
- The AI MUST utilize output fields (e.g., `marshal_with`) to format and filter response objects securely, preventing the exposure of internal data structures.

@Workflow
1. **Assessment:** Analyze the user's request to identify the target language (Java, Go, Python), project scale (micro-service, monolith, prototype), and primary operational requirements (performance, metrics, browsability).
2. **Selection:** Select the exact framework from the chapter's roster that best matches the assessment criteria. Output a brief justification based on the framework's core features.
3. **Scaffolding:** Generate the minimal boilerplate required to spin up the chosen framework.
   - *If Light 4j:* Request or generate an OpenAPI spec, then output the `light-code-gen` command.
   - *If Spring/Dropwizard:* Output the Maven/Gradle dependency block and the main application class.
4. **Implementation:** Draft the requested API endpoints adhering strictly to the selected framework's routing conventions (e.g., Resource classes in Flask, Lambdas in Spark, Controllers in Revel).
5. **NFR Integration:** Inject required non-functional requirements using the framework's native tools (e.g., Dropwizard Metrics, Revel Filters, DRF Serializers).
6. **Validation:** Review the generated code to ensure no anti-patterns or competing libraries have been introduced.

@Examples (Do's and Don'ts)

**Spark Framework (Java)**
- [DO]:
  ```java
  import static spark.Spark.*;
  public class MyHelloWorld {
      public static void main(String[] args) {
          get("/sayhello", (request, response) -> "Hello Reader");
      }
  }
  ```
- [DON'T]: Provide a heavy Servlet-based class or use verbose anonymous inner classes instead of lambdas.

**Dropwizard (Java)**
- [DO]: Run the application from a main method spinning up an embedded Jetty server.
  ```java
  public static void main(String[] args) throws Exception {
      new MyDropwizardApplication().run(args);
  }
  ```
- [DON'T]: Generate `web.xml` files or provide instructions for deploying to external Tomcat/JBoss servers.

**Flask-RESTful (Python)**
- [DO]:
  ```python
  from flask_restful import Resource, reqparse

  parser = reqparse.RequestParser()
  parser.add_argument('task')

  class Todo(Resource):
      def get(self, todo_id):
          return {todo_id: 'task details'}
      def put(self, todo_id):
          args = parser.parse_args()
          return {'task': args['task']}
  ```
- [DON'T]: Mix standard Flask `@app.route` decorators for REST endpoints when Flask-RESTful `Resource` classes are requested.

**Revel (Go)**
- [DO]: Define routes in the Revel `routes` file explicitly.
  ```text
  GET     /user/:id     User.Details
  ```
- [DON'T]: Define routes inside the Go main file using `http.HandleFunc`.

**Django REST Framework (Python)**
- [DO]: Use `ModelSerializer` to handle complex datatype conversion securely.
  ```python
  from rest_framework import serializers
  from .models import Investor

  class InvestorSerializer(serializers.ModelSerializer):
      class Meta:
          model = Investor
          fields = ['id', 'name', 'portfolio']
  ```
- [DON'T]: Manually parse JSON from the `request.body` and construct Python dictionaries in the view without using a Serializer.