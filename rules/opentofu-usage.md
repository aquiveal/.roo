# OpenTofu Usage Policy

## Tooling Mandate

- **Exclusively use `tofu`**: You must use the OpenTofu CLI (`tofu`) for all infrastructure operations.
- **Do Not Use `terraform`**: Never invoke the `terraform` command. If you see instructions to use `terraform`, implicitly translate them to `tofu`.

## Commands

- **Init**: `tofu init`
- **Plan**: `tofu plan`
- **Apply**: `tofu apply`
- **Format**: `tofu fmt`
- **Validate**: `tofu validate`

## Terminology

- Refer to the infrastructure-as-code tool as "OpenTofu".
- Refer to configuration files (`.tf`) as "OpenTofu configuration".
