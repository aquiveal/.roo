# @Domain
These rules MUST be activated when the AI is tasked with creating, modifying, or reviewing deployment artifacts, infrastructure-as-code (IaC), containerization setups, Dockerfiles, Kubernetes manifests (YAML), service meshes (Istio), serverless configurations (AWS Lambda, Serverless Framework), or when handling user requests related to deploying, releasing, or scaling microservices.

# @Vocabulary
- **Production Environment**: The environment providing service management, runtime management, monitoring, and request routing for microservices.
- **Language-specific package**: A deployment artifact tailored to a specific runtime (e.g., an executable JAR, WAR, or NodeJS directory).
- **Service as a virtual machine**: A pattern where a service is packaged as a VM image (e.g., an EC2 AMI) containing the service and its dependencies, providing complete isolation.
- **Service as a container**: A pattern where a service is packaged as a container image (e.g., Docker) and runs in an isolated, OS-level sandbox. 
- **Kubernetes (K8s)**: A Docker orchestration framework that treats a cluster of machines as a single pool of resources, managing scheduling and service instances.
- **Pod**: The basic unit of deployment in Kubernetes, consisting of one or more containers sharing an IP address and storage volumes.
- **Deployment (K8s)**: A declarative specification in Kubernetes that manages the desired number of Pod replicas and handles rolling upgrades/rollbacks.
- **Service (K8s)**: An object providing a stable DNS name and IP address, load-balancing traffic across a set of Pods (Types: ClusterIP, NodePort, LoadBalancer).
- **ConfigMap/Secret (K8s)**: Objects used to supply externalized configuration and sensitive data (credentials) to containers as environment variables or files.
- **Readiness Probe**: A health check mechanism used to determine if a container is ready to accept network traffic.
- **Liveness Probe**: A health check mechanism used to determine if a container has failed and must be terminated/restarted.
- **Service Mesh**: A networking infrastructure layer (e.g., Istio) that mediates communication between services, handling routing, circuit breaking, and separating deployment from release.
- **Sidecar**: A process or container (e.g., Istio Envoy proxy) that runs alongside the service instance to implement cross-cutting concerns.
- **VirtualService (Istio)**: Defines how to route requests for one or more hostnames to specific subsets of a service.
- **DestinationRule (Istio)**: Defines one or more subsets of pods for a service (e.g., versioned subsets) and associated traffic policies.
- **Serverless deployment**: A pattern (e.g., AWS Lambda) where the cloud provider manages infrastructure provisioning, scaling, and execution, charging only for request processing time.
- **Cold start / Long-tail latency**: The delay experienced in serverless deployments when the infrastructure must dynamically provision and initialize a new instance of an application (especially impactful for Java).

# @Objectives
- The AI MUST select the most lightweight deployment pattern that supports the service's requirements, evaluating options in strict order: Serverless -> Containers -> Virtual Machines -> Language-specific packages.
- The AI MUST encapsulate the technology stack within the deployment artifact (VM image or Container image) to eliminate undifferentiated heavy lifting and configuration errors by operations.
- The AI MUST enforce resource constraints and isolation between service instances to prevent misbehaving instances from impacting others.
- The AI MUST guarantee zero-downtime deployments by defining robust health checks (liveness and readiness probes) in orchestration configurations.
- The AI MUST facilitate the separation of deployment (running code in production) from release (routing end-user traffic to the code) using Service Mesh routing rules.

# @Guidelines
- **Deployment Pattern Selection**: 
  - Evaluate serverless deployment first. If the service is event/request-based and not highly sensitive to long-tail latency, use AWS Lambda.
  - If serverless is unsuitable (e.g., requires long-running processes or has strict latency constraints), default to the Service as a Container pattern using Kubernetes.
  - Only use Virtual Machines if utilizing a highly automated IaaS (like AWS Elastic Beanstalk) for a simple application where Kubernetes is overkill.
  - AVOID Language-specific packages natively installed on shared machines due to lack of isolation and resource constraints.
- **Containerization (Docker)**:
  - Dockerfiles MUST use lightweight base images (e.g., `openjdk:8u171-jre-alpine`).
  - Dockerfiles MUST declare a `HEALTHCHECK` instruction to actively probe the service's health endpoint (e.g., `/actuator/health`).
  - Dockerfiles MUST inject externalized configurations dynamically via environment variables rather than hardcoding.
- **Kubernetes Orchestration**:
  - Every deployable service MUST be defined using a `Deployment` object, NEVER as a bare `Pod`.
  - Every `Deployment` MUST define both `livenessProbe` and `readinessProbe` targeting the service's health check API to ensure safe rolling upgrades.
  - Every `Deployment` MUST externalize configuration by mapping environment variables from `ConfigMap` or `Secret` objects.
  - Every `Deployment` MUST be accompanied by a `Service` object that uses label selectors to dynamically load-balance traffic to the pods.
- **Service Mesh (Istio)**:
  - When configuring Istio, Kubernetes `Service` ports MUST use Istio's naming convention: `<protocol>[-<suffix>]` (e.g., `http-api`).
  - K8s `Deployment` metadata MUST include `app` and `version` labels to support distributed tracing and versioned routing.
  - The AI MUST separate deployment from release by generating a `DestinationRule` defining versioned subsets (e.g., `v1`, `v2`) and a `VirtualService` to initially route 100% of traffic to the stable version, or route based on custom headers (e.g., `testuser`) for testing.
- **Serverless (AWS Lambda)**:
  - Java Lambda functions MUST implement the AWS `RequestHandler<I, O>` interface.
  - To mitigate cold starts in Spring Boot Serverless applications, the AI MUST generate an abstract handler class that lazily initializes and caches the Spring `ApplicationContext` using a `ReentrantReadWriteLock`.
  - Lambda deployments MUST use the `Serverless` framework (`serverless.yml`) to define functions, HTTP endpoints (API Gateway integration), and environment variables, rather than manual AWS console configuration.
  - Unhandled exceptions in Lambda HTTP handlers MUST be explicitly caught and converted into structured HTTP 500 responses.

# @Workflow
When tasked with generating or updating a deployment configuration for a microservice, the AI MUST follow this exact algorithm:
1. **Requirement Assessment**: Analyze the service characteristics (latency sensitivity, protocol, statefulness, language).
2. **Pattern Selection**: Determine the target deployment pattern (Serverless -> Container -> VM) based on the assessment.
3. **Artifact Generation**:
   - *If Serverless*: Generate the Java `RequestHandler` implementation with cached ApplicationContext, Gradle `Zip` task, and `serverless.yml`.
   - *If Container*: Generate the `Dockerfile` with base image, copy instructions, entrypoint, and `HEALTHCHECK`.
4. **Orchestration Configuration** (If Container):
   - Generate a Kubernetes `Deployment.yml` including `replicas`, `labels` (`app`, `version`), environment variables (referencing Secrets/ConfigMaps), `readinessProbe`, and `livenessProbe`.
   - Generate a Kubernetes `Service.yml` exposing the necessary named ports.
5. **Release Strategy Configuration** (If Service Mesh is requested):
   - Generate Istio `DestinationRule.yml` defining subsets for the existing and new versions.
   - Generate Istio `VirtualService.yml` routing traffic via weights (canary release) or HTTP headers (dark launch/testing).
6. **Validation**: Ensure no hardcoded credentials exist and that all health checks accurately map to the service's diagnostic endpoints.

# @Examples (Do's and Don'ts)

## Dockerfile Design
- **[DO]** Include a `HEALTHCHECK` and use environment variables.
```dockerfile
FROM openjdk:8u171-jre-alpine
RUN apk --no-cache add curl
CMD java ${JAVA_OPTS} -jar ftgo-restaurant-service.jar
HEALTHCHECK --start-period=30s --interval=5s CMD curl -f http://localhost:8080/actuator/health || exit 1
COPY build/libs/ftgo-restaurant-service.jar .
```
- **[DON'T]** Use a heavy base image and omit health checks.
```dockerfile
FROM ubuntu:latest
# Missing HEALTHCHECK
COPY my-service.jar /app.jar
CMD ["java", "-jar", "/app.jar"]
```

## Kubernetes Deployment
- **[DO]** Define liveness and readiness probes, and use Secrets for sensitive data.
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: ftgo-restaurant-service
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: ftgo-restaurant-service
        version: v1
    spec:
      containers:
      - name: ftgo-restaurant-service
        image: msapatterns/ftgo-restaurant-service:latest
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: SPRING_DATASOURCE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: ftgo-db-secret
              key: password
        livenessProbe:
          httpGet:
            path: /actuator/health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /actuator/health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 20
```
- **[DON'T]** Deploy a bare Pod without a Deployment controller, probes, or hardcode passwords in the YAML.

## Istio Service Mesh Routing
- **[DO]** Define a `VirtualService` that separates deployment from release using header-based routing and traffic weighting.
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ftgo-consumer-service
spec:
  hosts:
  - ftgo-consumer-service
  http:
  - match:
    - headers:
        testuser:
          regex: "^.+$"
    route:
    - destination:
        host: ftgo-consumer-service
        subset: v2
  - route:
    - destination:
        host: ftgo-consumer-service
        subset: v1
      weight: 95
    - destination:
        host: ftgo-consumer-service
        subset: v2
      weight: 5
```
- **[DON'T]** Rely on default Kubernetes Service load balancing across all versions without a `VirtualService` and `DestinationRule` when rolling out new versions.

## AWS Lambda Java Implementation
- **[DO]** Cache the Spring Application Context to mitigate cold starts.
```java
public abstract class AbstractAutowiringHttpRequestHandler extends AbstractHttpHandler {
    private static ConfigurableApplicationContext ctx;
    private ReentrantReadWriteLock ctxLock = new ReentrantReadWriteLock();
    private boolean autowired = false;

    protected synchronized ApplicationContext getAppCtx() {
        ctxLock.writeLock().lock();
        try {
            if (ctx == null) {
                ctx = SpringApplication.run(getApplicationContextClass());
            }
            return ctx;
        } finally {
            ctxLock.writeLock().unlock();
        }
    }

    @Override
    protected void beforeHandling(APIGatewayProxyRequestEvent request, Context context) {
        super.beforeHandling(request, context);
        if (!autowired) {
            getAppCtx().getAutowireCapableBeanFactory().autowireBean(this);
            autowired = true;
        }
    }

    protected abstract Class<?> getApplicationContextClass();
}
```
- **[DON'T]** Reinitialize heavy frameworks (like Spring Boot) inside the `handleRequest` method on every invocation.