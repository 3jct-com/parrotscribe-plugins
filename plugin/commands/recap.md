---
description: Stop if needed and recap the Parrot Scribe session
---

Use the Parrot Scribe MCP tools already connected to this host. Do not start another MCP server.

1. Call `get_status`. If the state is `recording` or `listening`, call `stop_recording`. `paused` is already stopped.
2. Call `list_sessions`. Recap the newest session (first row).
3. Call `read_transcript` for that session.

Write a summary plus follow-ups. Take the shape from harness skills already loaded in this host. Do not bake in a methodology.
