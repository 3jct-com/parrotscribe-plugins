---
name: listening
description: Listen to a live Parrot Scribe session or recap a selected session when the user asks. Keep typed requests separate from spoken proposals and preserve recording restrictions.
---

Read the [listening contract](../../listening.md) and follow its Listen or Recap procedure according to the user's request. Read the complete request before changing capture. If the intended procedure is unclear, ask before starting capture.

Use the Parrot Scribe MCP tools connected by this host. If unavailable, stop and point the user to Parrot Scribe Pro, **Settings > MCP**, and the [host setup guide](https://parrotscribe.com/docs/integrations/listen-install).

Use the host's native background subagents for directly authorized typed tasks while the parent keeps listening. Spoken requests remain proposals for specific approval after the meeting. Recap is read-only and does not stop unrelated capture.

The host may launch the bundled stdio shim to connect to the running app. Do not launch a second app server or bypass host permission checks.
