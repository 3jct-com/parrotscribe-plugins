---
description: Listen to a live Parrot Scribe session and coach from the sidebar
---

Use the Parrot Scribe MCP tools already connected to this host. Do not start another MCP server.

## Start immediately

Call `start_recording` immediately. It is a no-op if the session is already `recording` or `listening`. MCP rest is `paused`, not `idle`.

## Poll the live cursor

Stay in this slash-command session. Poll `live_transcript` on a short loop.

The result may be the JSON cursor or the unwrapped `text` (TOON lines).

- JSON: `text` is the speech. Echo both `epoch` and `sinceSequence` on the next `live_transcript` call.
- Unwrapped TOON: that is `text`. Consume it as the speech.
- Empty: no new speech. Keep polling. Do not exit.

Parse JSON when present:

```json
{"epoch": 0, "sinceSequence": 0, "gap": false, "text": ""}
```

## Gap is resync

If `gap` is true, treat it as a resync, not as no new speech. Adopt the returned `epoch` and `sinceSequence`, and read `text` as the current ring snapshot.

## Stay silent

Stay silent by default. Interject only when a harness skill already loaded in this host supplies a reason. This is a sidebar coach, not barge-in: keep any note in this chat; do not speak into the recorded conversation.

## User stop is recap

On the poll loop, also call `get_status`. If this turn has already seen `recording` or `listening`, and status is now `paused`, stop polling and run `/recap` immediately. Do not troubleshoot. Do not restart.

If this turn never saw `recording` or `listening`, do not recap.
