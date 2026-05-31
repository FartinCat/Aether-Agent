---
category: core
---
# Instinct: Privacy Sanitization

## The Pattern
Public-facing documentation must never contain real user paths, machine names, or directory structures that reveal the author's personal environment.

## When It Fires
- Writing or updating README.md, deployment guides, or example commands.
- Generating code snippets or CLI examples that reference filesystem paths.
- Producing any output that will be committed to a public repository.

## Correct Behavior
- Use generic, neutral example paths:
  - **Windows**: `C:\Dev\aether-agent\`, `C:\Dev\my-project\`
  - **Linux/macOS**: `~/dev/aether-agent/`, `/home/user/my-project/`
  - **WSL**: `/mnt/c/dev/aether-agent/`
- Use `you` or `user` as placeholder usernames, never real OS usernames.
- Use `your-org` or `AetherAgent` for GitHub org references.
- Treat any path containing a real username, `Git_Work`, `Documents`, or home directory structure as a **privacy leak**.

## Patterns to Flag
- `/home/<real-username>/` or `/Users/<real-username>/`
- `C:\Users\<real-username>\`
- `D:\Git_Work\` or similar personal workspace roots
- `/mnt/d/Git_Work/` (WSL equivalents of the above)

## Failure Mode
- Real path `D:\Git_Work\Aether Agent\` appears in README.md example commands.
- Git username or machine hostname embedded in documentation.
- Session-specific paths from AETHER.md §18 copied into public docs.

## Override Protocol
User explicitly says "use exact paths" or "this is a private doc".
