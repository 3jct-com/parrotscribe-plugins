---
description: Stop if needed and recap the Parrot Scribe session
---

Use the Parrot Scribe MCP tools already connected to this host. Do not start another MCP server.

1. Call `get_status`. If recording is still live, call `stop_recording`.
2. Resolve the session with `list_sessions`.
3. Call `read_transcript` for that session.

Write a summary plus follow-ups. Take the shape from harness skills already loaded in this host. Do not bake in a methodology.
