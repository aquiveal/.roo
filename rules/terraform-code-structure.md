# Terraform Code Structure

## File Organization

Split your Terraform configurations into logical files:

- **`main.tf`**: Call modules, locals, and data sources to create all resources.
- **`variables.tf`**: Contains declarations of variables used in `main.tf`.
- **`outputs.tf`**: Contains outputs from the resources created in `main.tf`.
- **`versions.tf`**: Contains version requirements for Terraform and providers.

### Restrictions
- **`terraform.tfvars`**: Do **not** use `terraform.tfvars` inside resource modules. It should only be used in composition (root modules).

## Module Structure

- **Keep Resource Modules Plain**: Resource modules should be as simple as possible, focusing on a specific resource type or closely related group of resources.
- **Data Sources as Glue**: Use data sources and `terraform_remote_state` to connect infrastructure modules within a composition.

## Remote State

- **Mandatory**: Start your project using remote state.
- **Reasoning**:
    - "Your laptop is no place for your infrastructure source of truth."
    - Managing `tfstate` in git is risky.
    - Enables collaboration and locking.

## Example Directory Layout

```text
composition/
  ├── main.tf
  ├── variables.tf
  ├── outputs.tf
  ├── versions.tf
  └── terraform.tfvars
modules/
  └── my-module/
      ├── main.tf
      ├── variables.tf
      ├── outputs.tf
      └── versions.tf
```
