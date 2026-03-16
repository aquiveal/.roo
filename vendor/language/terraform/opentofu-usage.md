# OpenTofu Usage Policy

## Tooling Mandate

- **General Rule**: Use the OpenTofu CLI (`tofu`) for infrastructure operations.
- **Coder Templates Exception**: When working with Coder templates, you **must use `terraform`** instead of `tofu`.
- **Do Not Use `terraform` outside of Coder**: Unless working with Coder templates, never invoke the `terraform` command. If you see instructions to use `terraform` in other contexts, implicitly translate them to `tofu`.

## Commands

For general usage:
- **Init**: `tofu init`
- **Plan**: `tofu plan`
- **Apply**: `tofu apply`
- **Format**: `tofu fmt`
- **Validate**: `tofu validate`

For Coder templates:
- **Init**: `terraform init`
- **Plan**: `terraform plan`
- **Apply**: `terraform apply`
- **Format**: `terraform fmt`
- **Validate**: `terraform validate`

## Terminology

- Refer to the infrastructure-as-code tool as "OpenTofu" (or "Terraform" when working specifically with Coder templates).
- Refer to configuration files (`.tf`) as "OpenTofu configuration" (or "Terraform configuration" for Coder).
