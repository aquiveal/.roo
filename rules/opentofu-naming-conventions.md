# OpenTofu Naming Conventions

## General Rules

### Delimiters and Case
- Use **underscores** (`_`) instead of dashes (`-`) in all names (resources, data sources, variables, outputs).
- Prefer **lowercase** letters and numbers.

### Resource Names
- **Do not repeat resource type** in the resource name.
    ```hcl
    # Good
    resource "aws_route_table" "public" {}

    # Bad
    resource "aws_route_table" "public_route_table" {}
    resource "aws_route_table" "public_aws_route_table" {}
    ```
- **Generic Name (`this`)**: Use `this` if the resource module creates a single resource of this type.
    ```hcl
    resource "aws_nat_gateway" "this" { ... }
    ```
- **Singular Nouns**: Always use singular nouns for names.

## Resource Argument Ordering

1. **Meta-arguments**: `count` / `for_each` must be the **first** argument.
2. **Attributes**: Resource specific arguments.
3. **Tags**: `tags` should be the **last** real argument.
4. **Lifecycle/Depends On**: Follow `tags` with `depends_on` and `lifecycle`.

### Example

```hcl
resource "aws_nat_gateway" "this" {
  count = 2

  allocation_id = "..."
  subnet_id     = "..."

  tags = {
    Name = "..."
  }

  depends_on = [aws_internet_gateway.this]

  lifecycle {
    create_before_destroy = true
  }
}
```

## Variables

- **Pluralization**: Use plural names for variables of type `list(...)` or `map(...)` (e.g., `public_subnets` instead of `public_subnet`).
- **Booleans**: Use positive variable names (e.g., `encryption_enabled` instead of `encryption_disabled`).

## Outputs

- **Structure**: `{name}_{type}_{attribute}`
    - `{name}`: Resource name (e.g., `private`).
    - `{type}`: Resource type without provider prefix (e.g., `subnet`).
    - `{attribute}`: The attribute returned (e.g., `id`).
- **Generic Outputs**: Omit `this` prefix if the output is returning a value from a primary resource.
    - *Example*: `security_group_id` instead of `this_security_group_id`.
- **Lists**: Use plural names if the return value is a list.

### Example

```hcl
# Return at most one ID of security group
output "security_group_id" {
  description = "The ID of the security group"
  value       = try(aws_security_group.this[0].id, aws_security_group.name_prefix[0].id, "")
}

# Plural name for list output
output "rds_cluster_instance_endpoints" {
  description = "A list of all cluster instance endpoints"
  value       = aws_rds_cluster_instance.this.*.endpoint
}
```
