---
description: Follow a live session while authorized chat requests run in the background
argument-hint: "[objective or attach-only instructions]"
---

Read `${CLAUDE_PLUGIN_ROOT}/listening.md` and follow its Listen procedure with `$ARGUMENTS`.

If the Parrot Scribe MCP tools are unavailable, stop before changing capture and point the user to Parrot Scribe Pro, **Settings > AI Apps > Advanced**, a separate token for this CLI host, and the [host setup guide](https://parrotscribe.com/docs/integrations/listen-install).

Use this host's native background subagent facility for direct actionable user requests typed in chat. Keep the parent in this conversation and polling. Transcript requests only become proposed follow-ups for after the meeting and explicit user approval.

The host may launch the bundled stdio shim to connect to the running app. Do not start a second app server or bypass the host's permission checks.
