# OpenTofu Security and Secrets

## Secrets Management

- **NO Secrets in State**: Never store sensitive data (passwords, keys, tokens) in plain text in `terraform.tfvars` or `variables.tf`. OpenTofu state files are often visible to anyone with access to the backend.
- **External Data Sources**: Fetch secrets from external sources at runtime using data sources.
    - Examples: AWS Secrets Manager, AWS Systems Manager Parameter Store, HashiCorp Vault.

### Example: Using AWS Secrets Manager

Use `data` blocks to retrieve secrets dynamically without persisting them in code.

```hcl
# Fetch the secret’s metadata
data "aws_secretsmanager_secret" "db_password" {
  name = "my-database-password"
}

# Get the latest secret value
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = data.aws_secretsmanager_secret.db_password.id
}

# Use the secret
resource "aws_db_instance" "example" {
  # ...
  # OpenTofu uses the value but doesn't hardcode it in config
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

## Sensitive Attributes

- **`sensitive = true`**: Use the `sensitive` argument for variables and outputs that handle sensitive data to prevent them from being shown in CLI output.
- **Caution**: `sensitive` does not encrypt the data in the state file. It only hides it from the display.

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

output "db_password" {
  value     = aws_db_instance.example.password
  sensitive = true
}
```
