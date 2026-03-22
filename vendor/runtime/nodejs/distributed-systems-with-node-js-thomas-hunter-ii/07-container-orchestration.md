# @Domain
Container Orchestration, specifically defining, managing, scaling, and deploying stateless Node.js applications using Kubernetes (K8s), Minikube, Kubectl, and declarative YAML configuration files.

# @Vocabulary
- **Container**: An isolated environment that encapsulates and runs an application.
- **Volume**: A mechanism to mount a filesystem in a semipermanent way outside of a container.
- **Pod**: The smallest interactive unit in the Kubernetes API. Represents an application instance, contains one or more containers, and shares a single IP address.
- **Node**: A worker machine (physical or virtual) in the cluster running a container daemon, Kubelet, and Kube Proxy.
- **Master**: A set of services on a master node that exposes the API and delegates commands to Kubelets.
- **Cluster**: The overall collection of the master and its associated nodes.
- **Scheduling**: The process (`kube-scheduler`) by which Kubernetes determines the best node to assign newly created pods to, based on CPU and memory requirements.
- **Namespaces**: A mechanism for logically dividing a cluster into smaller, semi-isolated collections (e.g., `default`, `kube-system`, `kubernetes-dashboard`).
- **Labels**: Key/value pairs assigned to resources (e.g., `app: web-api`) for identification and grouping.
- **Selectors**: Declarations of a pod's requirements, used by controllers to figure out which pods to manage.
- **Stateful Sets**: Controllers intended to make managing stateful services convenient (not used for stateless Node.js apps).
- **Replica Sets**: A controller that maintains a list of pods, creating or deleting them until the desired number of replicas is met.
- **Deployments**: A controller that manages a Replica Set. Used to deploy new versions, scale instances, or roll back to previous versions.
- **Controllers**: Mechanisms that tell Kubernetes how to change from one state to another.
- **Service**: A resource that exposes a set of pods to the network, acting essentially as a reverse proxy using a selector to target pods.
- **Ingress**: A resource that manages external network access to a service within a Kubernetes cluster.
- **Probe (Liveness Probe)**: A health check used by Kubernetes to determine if a pod is healthy and ready to receive traffic.
- **Minikube**: A simplified tool for running a single-node Kubernetes cluster locally for development.
- **Kubectl**: The command-line interface used to communicate with the Kubernetes Master API.
- **Service Discovery**: The mechanism by which applications find and communicate with other services using the Service name as the hostname.

# @Objectives
- Automate the deployment, scaling, and management of containerized Node.js applications.
- Ensure high availability and self-healing systems by strictly enforcing Kubernetes Deployments, Replica Sets, and Liveness Probes.
- Facilitate zero-downtime rolling updates and reliable rollbacks using declarative YAML configuration files.
- Enable robust inter-service communication and external ingress routing utilizing Kubernetes Services and Ingress controllers.

# @Guidelines
- **Minikube Docker Daemon**: The AI MUST execute `eval $(minikube -p minikube docker-env)` before building Docker images locally. This ensures the images are built inside Minikube's isolated Docker daemon and are accessible to the Kubernetes cluster.
- **Declarative over Imperative**: The AI MUST prefer creating and applying declarative YAML configuration files (`kubectl apply -f <filename.yml>`) rather than using imperative Kubectl subcommands (`kubectl create`, `kubectl expose`).
- **Use Deployments for Stateless Apps**: The AI MUST NEVER create bare Pods. All Node.js stateless applications MUST be managed via a `Deployment` resource.
- **Mandatory Health Checks**: Every container defined in a Deployment MUST include a `livenessProbe` (e.g., an `httpGet` check) to enable Kubernetes to automatically restart unhealthy or crashed applications.
- **Consistent Labeling**: The AI MUST consistently apply `labels` (e.g., `app: <service-name>`) to Pod templates and correctly map them using `selector.matchLabels` in Deployments and `selector` in Services.
- **Service Discovery**: When configuring a Node.js app to communicate with another service in the cluster, the AI MUST configure the target hostname using the exact name of the destination Kubernetes `Service` (e.g., `http://recipe-api-service:80`). Hardcoding IP addresses is strictly FORBIDDEN.
- **Ingress for External Traffic**: To expose services externally, the AI MUST define an `Ingress` resource rather than relying solely on `NodePort` or direct pod access.
- **YAML Concatenation**: The AI MAY concatenate related Kubernetes resources (e.g., a Service and an Ingress) in a single YAML file by separating them with three hyphens (`---`).
- **Tracking Rollouts**: When applying a deployment that may need to be rolled back, the AI MUST use the `--record=true` flag (`kubectl apply -f <file> --record=true`) to log the command in the deployment history.
- **Graceful Shutdown**: Node.js applications MUST be prepared to receive a `SIGTERM` signal from Kubernetes, stop accepting new connections, finish ongoing work, and exit before the 30-second timeout, otherwise Kubernetes will forcefully issue a `SIGKILL`.

# @Workflow
When tasked with containerizing and orchestrating a Node.js application locally, the AI MUST adhere to this exact sequence:

1. **Initialize Cluster**: Start Minikube (`minikube start`).
2. **Enable Add-ons**: If external ingress is required, enable the ingress controller (`minikube addons enable ingress`).
3. **Configure Docker Environment**: Point the local Docker CLI to Minikube's daemon: `eval $(minikube -p minikube docker-env)`.
4. **Build Image**: Build the application's Docker image using the configured daemon (`docker build -t <app-name>:<version> .`).
5. **Create Deployment YAML**: Write a `<app-name>-deployment.yml` defining the `Deployment`, `replicas`, `matchLabels`, container `image`, `ports`, environment variables (`env`), and `livenessProbe`.
6. **Create Network YAML**: Write a `<app-name>-network.yml` defining the `Service` (mapping `port` to `targetPort`) and, if external access is needed, an `Ingress` routing to the Service.
7. **Apply Configurations**: Execute `kubectl apply -f <app-name>-deployment.yml --record=true` followed by `kubectl apply -f <app-name>-network.yml`.
8. **Verify State**: Monitor the rollout using `kubectl get pods -w -l app=<app-name>` until the pods show a status of `Running` and `READY 1/1`.
9. **Scaling**: To scale, modify the `replicas` count in the Deployment YAML and re-run `kubectl apply -f <app-name>-deployment.yml`.
10. **Updating**: To update the application version, build a new image tag, update the `image` field in the Deployment YAML, and re-run `kubectl apply -f <app-name>-deployment.yml --record=true`.
11. **Rolling Back**: If a deployment fails or crashes, identify the previous revision using `kubectl rollout history deployment.apps/<app-name>`, then revert using `kubectl rollout undo deployment.apps/<app-name> --to-revision=<revision-number>`.

# @Examples (Do's and Don'ts)

### [DO] Define a robust Deployment with replicas, labels, and liveness probes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: recipe-api
  labels:
    app: recipe-api
spec:
  replicas: 5
  selector:
    matchLabels:
      app: recipe-api
  template:
    metadata:
      labels:
        app: recipe-api
    spec:
      containers:
        - name: recipe-api
          image: recipe-api:v1
          ports:
            - containerPort: 1337
          livenessProbe:
            httpGet:
              path: /health
              port: 1337
            initialDelaySeconds: 3
            periodSeconds: 10
```

### [DON'T] Deploy bare pods or omit health checks
```yaml
# INCORRECT: Creating a raw Pod instead of a Deployment, lacking self-healing and replication.
# INCORRECT: Missing a livenessProbe, meaning Kubernetes won't know if the Node.js event loop blocks.
apiVersion: v1
kind: Pod
metadata:
  name: recipe-api
spec:
  containers:
    - name: recipe-api
      image: recipe-api:v1
      ports:
        - containerPort: 1337
```

### [DO] Use Service Names for Inter-Service Communication (Service Discovery)
```yaml
# In the Deployment YAML for the consuming service
        env:
          - name: TARGET
            value: "recipe-api-service" # K8s DNS will resolve this to the upstream service IP
```
```javascript
// In the Node.js Application code
const TARGET = process.env.TARGET || 'localhost:4000';
// Makes request to http://recipe-api-service/recipes/42
const req = await fetch(`http://${TARGET}/recipes/42`); 
```

### [DON'T] Hardcode IP addresses or Pod-specific details for network calls
```yaml
# INCORRECT: Hardcoding a minikube IP or specific Pod IP. Pods are ephemeral and IPs change constantly.
        env:
          - name: TARGET
            value: "172.17.0.3:31710"
```

### [DO] Combine Service and Ingress in a declarative network YAML
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-api-service
spec:
  type: NodePort
  selector:
    app: web-api
  ports:
    - port: 1337
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: web-api-ingress
spec:
  rules:
    - host: example.org
      http:
        paths:
          - path: /
            backend:
              serviceName: web-api-service
              servicePort: 1337
```