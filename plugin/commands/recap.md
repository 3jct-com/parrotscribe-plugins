---
description: Recap a selected session without stopping unrelated capture
argument-hint: "[session ID or historical description]"
---

Read `${CLAUDE_PLUGIN_ROOT}/listening.md` and follow its Recap procedure with `$ARGUMENTS`.

If the Parrot Scribe MCP tools are unavailable, stop and point the user to Parrot Scribe Pro, **Settings > MCP**, and the [host setup guide](https://parrotscribe.com/docs/integrations/listen-install).

Use the listening turn's bound session unless the user selects another. Recap is read-only; do not stop capture just to summarize. Spoken action requests remain proposals until the meeting ends and the user explicitly approves them in chat.

The host may launch the bundled stdio shim to connect to the running app. Do not start a second app server or bypass the host's permission checks.
