# Terraform Variable and Output Guidelines

## Variables

### Definition Rules
1.  **Description**: Always include a `description` argument, even if obvious. Use upstream documentation wording where applicable.
2.  **Order**: Define arguments in this order: `description`, `type`, `default`, `validation`.
3.  **Types**:
    *   Prefer simple types (`number`, `string`, `list(...)`, `map(...)`).
    *   Use specific types (e.g., `map(map(string))`) over `any` unless strict flexibility is needed.
    *   Use `any` only to disable type validation for deeply nested or variable structures.
4.  **Nullable**: Set `nullable = false` if the variable should never be null.

### Validation
Use `validation` blocks to enforce constraints.

```hcl
variable "environment" {
  description = "Environment name for resource tagging"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}
```

### Optional Attributes (Terraform 1.3+)
Use `optional()` in object types for optional fields with defaults.

```hcl
variable "database_settings" {
  type = object({
    name             = string
    backup_retention = optional(number, 7)
  })
}
```

## Outputs

### Definition Rules
1.  **Description**: Always include a `description`.
2.  **Naming**: Follow `{name}_{type}_{attribute}` convention.
3.  **Value**:
    *   Use `try()` to handle values that might be missing due to conditional creation.
    *   Avoid `element(concat(...))` (legacy).

### Example

```hcl
output "security_group_id" {
  description = "The ID of the security group"
  value       = try(aws_security_group.this[0].id, "")
}
```
