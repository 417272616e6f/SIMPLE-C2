cli_pt.py

Summary
- Prompt-toolkit based interactive CLI that is session-aware.
- Provides session-scoped history, safe printing, and built-in colon commands for session management and history inspection.

Key functions / behavior
- `run_cli()` : main blocking loop. Waits for an active session, then opens a `PromptSession` using that session's `InMemoryHistory`.
- Supports colon commands:
  - `:sessions` / `:ss` list sessions and mark active
  - `:session <id>` / `:s <id>` switch active session and print recent output
  - `:history` / `:h` show recent history
- Uses `ForceCLIReload` exception to trigger a CLI reload when needed.

Notes
- Uses `prompt_toolkit.patch_stdout.patch_stdout` to allow background prints while prompting.
- Blocks until EOF/KeyboardInterrupt; runs in a daemon thread when launched by `index.py`.
