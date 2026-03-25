# User Guide

## Basic Workflow

1. Upload one or more `.ipynb` files.
2. Configure export options in the sidebar.
3. Click **Process Files**.
4. Preview the extracted content (code, outputs, markdown, images) in separate tabs.
5. Download the ZIP package.

## Configuration Options


| Option                | Description                        | Default |
| --------------------- | ---------------------------------- | ------- |
| Include outputs       | Export cell execution outputs      | Yes     |
| Include images        | Extract images from outputs        | Yes     |
| Include markdown      | Generate documentation file        | Yes     |
| Remove magic commands | Strip IPython `%` and `!` commands | No      |
| Add cell numbers      | Add `# --- Cell N ---` comments    | No      |
| Custom ZIP name       | Customize output filename          | Auto    |
| Encoding              | Output file encoding               | UTF-8   |


## Notes

- All files are processed in-memory — nothing is stored on the server.
- IPython magic commands can be optionally removed for cleaner scripts.
- HTML and JavaScript outputs are not processed.
- Large notebooks may take longer to process.

