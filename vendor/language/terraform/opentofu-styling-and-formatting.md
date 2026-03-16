# OpenTofu Styling and Formatting

## Formatting Tools

- **`tofu fmt`**: Always run `tofu fmt` to enforce canonical style.
    - Use in CI pipelines: `tofu fmt -check`.
    - Use pre-commit hooks.
- **`.editorconfig`**: Use an `.editorconfig` file to maintain consistent whitespace and indentation.

### Example `.editorconfig`

```editorconfig
[*]
indent_style = space
indent_size = 2
trim_trailing_whitespace = true

[*.{tf,tfvars}]
indent_style = space
indent_size = 2

[Makefile]
indent_style = tab
```

## Comments

- **Symbol**: Use `#` for comments. Avoid `//` or block comments (`/* ... */`).
- **Section Headers**: Delimit section headers with `# -----` or `######` for clarity.

### Example

```hcl
# --------------------------------------------------
# AWS EC2 Instance Configuration
# --------------------------------------------------

resource "aws_instance" "this" {
  # This is a comment explaining the resource
  ami = "ami-12345678"
}
```

## Documentation

- **Tools**: Use `terraform-docs` to automatically generate documentation from your OpenTofu modules.
- **Integration**: Use pre-commit hooks to update documentation automatically.
