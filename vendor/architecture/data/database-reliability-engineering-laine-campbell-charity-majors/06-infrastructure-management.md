# @Domain
These rules MUST be triggered whenever the AI is tasked with creating, modifying, or reviewing Infrastructure as Code (IaC), configuration management scripts, database provisioning processes, CI/CD pipelines for infrastructure, server images, orchestration definitions, or service discovery mechanisms. 

# @Vocabulary
- **Configuration Management**: Applications utilizing Domain-Specific Languages (DSLs) or scripts to define server configuration (e.g., Chef, Puppet, Ansible, SaltStack).
- **Idempotency**: An operation that evaluates a desired state and performs whatever is necessary to bring the component to that state regardless of its current state, without duplicating actions or causing errors upon repeated runs.
- **Frying**: The process of dynamic configuration at host deployment time (provision hardware/OS, then run configuration tools).
- **Baking**: The process of taking a base image and configuring it at build time to create a "golden image" artifact (e.g., AMI, VM image) for deployment. 
- **Configuration Drift**: The divergence of a server's state from its defined configuration due to manual tweaks, experiments, or unrecorded mutations.
- **Immutable Infrastructure**: Infrastructure that is strictly forbidden to mutate post-deployment. All changes require modifying the version-controlled definition and redeploying the service.
- **Monolithic Infrastructure Definition**: An anti-pattern where all applications, tiers, and databases for an organization are defined in a single orchestration file or stack.
- **Vertical Separation**: Breaking infrastructure definitions apart by functional service (e.g., separating the signup service from the ordering service).
- **Horizontal Separation (Separated Tiers)**: Breaking service infrastructure definitions apart by architectural tier (e.g., web server stack, application server stack, database stack).
- **Service Catalog / Service Discovery**: An abstraction layer mapping dynamic component designations (IPs, ports) to semantic names (e.g., `mysql-replicas`) acting as the source of truth for current infrastructure state (e.g., Consul, Zookeeper, Etcd).

# @Objectives
- Eliminate manual, repetitive operational toil through programmatic automation.
- Ensure 100% reproducibility of database infrastructures across all environments.
- Prevent configuration drift by enforcing immutable infrastructure or rigorous configuration synchronization.
- Minimize infrastructure failure domains by strictly modularizing orchestration definitions vertically and horizontally.
- Treat infrastructure components as testable software by implementing Test-Driven Development (TDD) for infrastructure and compliance.

# @Guidelines

## Version Control System (VCS) Rules
- The AI MUST treat the VCS as the single source of truth for the entire infrastructure.
- The AI MUST ensure the following are managed via VCS: source code, scripts, library dependencies, configuration files, OS/database image versions.
- The AI MUST explicitly mask or encrypt all passwords and sensitive secrets before storing them in the VCS.

## Configuration Definition Rules
- The AI MUST write configuration definitions that are highly parameterized to support multiple environments (dev, test, production) from the same codebase.
- The AI MUST ensure EVERY configuration action is idempotent. Never assume a state; always check existence before appending, mutating, or deleting.
- The AI MUST include pre- and post-tests for all configuration modules to validate that the expected state was achieved.
- The AI MUST integrate configuration definitions with monitoring and logging platforms for error management.

## Building and Maintaining Infrastructure Rules
- The AI MUST explicitly choose between a "Baking" strategy (using tools like Packer to create golden images) or a "Frying" strategy (using tools like Chef/Ansible on boot) based on the project's immutability requirements.
- The AI MUST design systems to enforce configuration state. If mutations occur, the AI MUST recommend automated Configuration Synchronization (overwriting changes to match baseline) or Component Redeploys (destroying and replacing the drifted host).
- The AI MUST NOT allow manual ssh/root modifications to database environments. 

## Infrastructure Definition and Orchestration Rules
- The AI MUST explicitly reject and refactor Monolithic Infrastructure Definitions. 
- The AI MUST modularize orchestration code (e.g., Terraform, CloudFormation). 
- If multiple applications share a database tier, the AI MUST create at least three distinct definitions: the shared database definition, and separate definitions for each application.
- The AI MUST isolate tiers horizontally to reduce failure domains (e.g., changing DB configuration must not risk breaking the web server build).

## Testing and Compliance Rules
- The AI MUST use descriptive testing frameworks (e.g., ServerSpec, Inspec) to perform static and dynamic compliance and acceptance testing on all built infrastructure.
- The AI MUST design local Development/Sandbox environments using tools like Vagrant and Packer to exactly mirror production software and configuration.

## Service Catalog Integration Rules
- The AI MUST utilize a Service Catalog for cross-stack communication. Hardcoded IPs are strictly forbidden.
- The AI MUST register new datastore instances into a Service Catalog namespace (e.g., under a specific `shard_id`) upon creation.
- The AI MUST use Service Catalogs to trigger load balancer template rebuilds during database failovers, to share writable shard information, and to advertise seed nodes for clustering.

# @Workflow
When tasked with creating or updating database infrastructure, the AI MUST execute the following algorithmic process:

1. **Parameterize the Definition**: Define the configuration code (Ansible/Chef/Puppet) using variables that allow the code to scale across Dev, Test, and Prod without duplication.
2. **Implement Idempotent Logic**: For every step (file creation, package install, config edit), write conditions that check the current state and only apply the change if the state diverges from the target.
3. **Select Build Strategy**: Define whether the infrastructure will be Baked (Packer template outputting an AMI) or Fried (Terraform provisioning an instance and passing cloud-init scripts). 
4. **Architect the Stack**: Break the orchestration definition (Terraform/CloudFormation) into separate modules for the specific service (Vertical) and specific tier (Horizontal).
5. **Integrate Service Discovery**: Embed scripts/commands in the provisioning step to dynamically query the Service Catalog (Consul/Zookeeper) for dependencies and register the newly built node's IP/Role into the catalog.
6. **Write Acceptance Tests**: Generate ServerSpec/Inspec code to validate the applied configuration (e.g., checking if the database port is listening, checking file permissions).
7. **Mirror to Local Dev**: Ensure a Vagrantfile or Docker Compose configuration is generated that utilizes the exact same provisioning code for local sandbox testing.

# @Examples (Do's and Don'ts)

## Configuration Idempotency
- **[DO]**:
```bash
if ! grep -q "^innodb_buffer_pool_size" /etc/mysql/my.cnf; then
  echo "innodb_buffer_pool_size=1G" >> /etc/mysql/my.cnf
else
  sed -i 's/^innodb_buffer_pool_size.*/innodb_buffer_pool_size=1G/' /etc/mysql/my.cnf
fi
```
- **[DON'T]**:
```bash
# Anti-pattern: Blindly appending will duplicate entries on repeated runs
echo "innodb_buffer_pool_size=1G" >> /etc/mysql/my.cnf
```

## Infrastructure Orchestration Structure
- **[DO]**: 
Structuring Terraform into horizontally and vertically separated modules:
```text
infrastructure/
├── signup_service/
│   ├── web_tier/
│   │   └── main.tf
│   └── app_tier/
│       └── main.tf
└── shared_databases/
    └── user_db_cluster/
        └── main.tf
```
- **[DON'T]**: 
Lumping the entire organization into a single monolithic definition:
```text
infrastructure/
└── everything_production.tf
```

## Service Discovery over Static IPs
- **[DO]**: 
Configuring an application to query a Service Catalog for the database leader:
```hcl
data "consul_service" "mysql_primary" {
  name = "user-db-primary"
}
# Outputting the dynamic IP to the app config
```
- **[DON'T]**: 
Hardcoding IP addresses between horizontally separated stacks:
```hcl
variable "database_ip" {
  default = "10.0.5.50" # Anti-pattern: Will break upon automated failover or redeploy
}
```

## Maintaining Configuration (Immutability)
- **[DO]**: To update a database parameter, modify the Chef cookbook, commit to VCS, trigger the CI/CD pipeline to bake a new AMI, and perform a rolling redeployment of the database cluster.
- **[DON'T]**: SSH into the production database server, manually edit `my.cnf`, and run `systemctl restart mysql`.