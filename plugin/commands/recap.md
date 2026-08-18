---
description: Stop if needed and recap the Parrot Scribe session
---

Use the Parrot Scribe MCP tools already connected to this host. Do not start another MCP server.

1. Call `stop_recording` immediately. It is a no-op if the session is already `paused`. Live states are `recording` and `listening`.
2. Call `list_sessions`. Recap the newest session (first row).
3. Call `read_transcript` for that session.

Write a summary. Add follow-ups only when the session has real actions. A video or other passive watch with nothing to do gets no follow-ups. Do not invent any. Take the shape from harness skills already loaded in this host. Do not bake in a methodology.
