---
description: Stop if needed and recap a Parrot Scribe session
argument-hint: "[session]"
---

Use the Parrot Scribe MCP tools already connected to this host. Do not start another MCP server.

The free text after `/recap` is `$ARGUMENTS`.

1. Call `stop_recording` immediately. It is a no-op if the session is already `paused`. Live states are `recording` and `listening`.
2. Resolve the session:
   - If `$ARGUMENTS` is empty, recap the newest session (first `list_sessions` row).
   - If `$ARGUMENTS` has text, use `search_sessions` and `list_sessions` to find the match. Ask a clarifying question when more than one session could match. Do not guess.
3. Call `read_transcript` for that session.

Write a summary. Add follow-ups only when the session has real actions. A video or other passive watch with nothing to do gets no follow-ups. Do not invent any. Take the shape from harness skills already loaded in this host. Do not bake in a methodology.
