force_cli_reload.py

Summary
- Small custom exception class `ForceCLIReload` used to signal the CLI loop to reload and re-render the prompt.

Usage
- Raised inside code that needs the prompt to refresh; caught by the CLI loop (`functions.cli_pt`) to trigger a reload.
