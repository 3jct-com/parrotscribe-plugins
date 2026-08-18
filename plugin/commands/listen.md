---
description: Listen to a live Parrot Scribe session and coach from the sidebar
---

Use the Parrot Scribe MCP tools already connected to this host. Do not start another MCP server.

## Start if idle

1. Call `get_status`.
2. MCP rest state is `paused`, not `idle`. Call `start_recording` only when the state is `paused`.
3. Do not start if the state is already `recording` or `listening`.

## Poll the live cursor

Stay in this slash-command session. Poll `live_transcript` on a short loop. An empty result is not a live ring and is not a reason to exit.

The result may be the JSON cursor or the unwrapped `text` (TOON lines). If you get JSON, echo both `epoch` and `sinceSequence` on the next `live_transcript` call. If you get TOON lines or an empty result, keep polling.

Parse JSON when present:

```json
{"epoch": 0, "sinceSequence": 0, "gap": false, "text": ""}
```

## Gap is resync

If `gap` is true, treat it as a resync, not as no new speech. Adopt the returned `epoch` and `sinceSequence`, and read `text` as the current ring snapshot.

## Stay silent

Stay silent by default. Interject only when a harness skill already loaded in this host supplies a reason. This is a sidebar coach, not barge-in: keep any note in this chat; do not speak into the recorded conversation.
