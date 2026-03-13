# General OpenTofu Best Practices

## Explicit Dependencies
Use `locals` to calculate logic and explicit dependency hints, especially when conditional logic is complex.

```hcl
locals {
  create_vpc = var.vpc_id == ""
}

resource "aws_vpc" "this" {
  count = local.create_vpc ? 1 : 0
  # ...
}
```

## Versioning
- **Pin Versions**: Always pin OpenTofu and provider versions in `versions.tf` to avoid breaking changes.
- **Lock File**: Commit `.terraform.lock.hcl` to version control.

```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}
```

## State Management
- **Small Blast Radius**: Keep state files small. Easier to manage, faster to plan/apply, and safer (less impact if corrupted).
- **Isolation**: Insulate unrelated resources by placing them in separate states.

## CI/CD
- **Automation**: Use CI/CD for applying changes.
- **Pre-commit**: Use `pre-commit-opentofu` to lint, format, and document code before it reaches the repo.
