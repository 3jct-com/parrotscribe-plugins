# Parrot Scribe for your agent

Follow a live conversation using the context, skills, and tools your agent already has. Parrot Scribe captures and transcribes locally. Your agent supplies interpretation and authorized task execution.

## Choose your desktop app

Parrot Scribe 1.0.2 connects ChatGPT, Claude, and Cursor from **Settings > AI Apps**. Open the selected desktop AI app first and leave it running, then choose **Connect** on its row. This catalog does not install those rows.

Connect approves the AI app's current running session. After that app restarts, choose **Manage… > Connect** on its row to approve the new session. This reuses its existing credential and profile. Reopening the AI app alone does not renew approval.

| Desktop app | Connection and instructions |
| --- | --- |
| ChatGPT | The app opens a local plugin with the connection and the listening skill. Start a new local task and select **listening**. |
| Claude | The app installs a local extension, then **Add listening skill…** opens Claude. Claude can still show its red unreviewed-extension warning. |
| Cursor | The app installs `~/.cursor/plugins/local/parrot` and opens Cursor's connection handoff. It does not add the older Cursor commands. Start a new chat. |

The catalog is a custom marketplace for Claude Code and the Codex CLI, not a listing in each provider's public directory. Local connections do not make your Mac available to a web or mobile client.

## Install in Claude Code

Install from the [plugin marketplace](https://github.com/3jct-com/parrotscribe-plugins):

```text
/plugin marketplace add 3jct-com/parrotscribe-plugins
/plugin install parrot@parrotscribe-plugins
```

Plugin 0.4.0 bundles the connection to `/Applications/Parrot Scribe.app/Contents/MacOS/parrotscribe-mcp-shim`. Install the app at that path, keep it running, and turn on **Allow AI apps** in **Settings > AI Apps**. MCP access requires Parrot Scribe Pro. Create this client's token under **Advanced**. Update older plugin installations to 0.4.0 to add this bundled connection.

Create a token for this Claude Code client in Parrot Scribe, then enter it in the plugin's **Parrot Scribe client token** prompt. Claude Code's [sensitive plugin configuration](https://code.claude.com/docs/en/plugins-reference#user-configuration) stores it in the platform credential store and passes it to the shim as `PARROTSCRIBE_MCP_TOKEN`. The package contains only the reference, never your token. Use a current Claude Code version with `userConfig` support.

If this host already has a manual `parrotscribe` MCP connection, use its MCP controls to keep only one connection enabled. Preserve the existing configuration while switching; do not add a second tool set or share this client's token with another host. See the [host setup guide](https://parrotscribe.com/docs/integrations/listen-install) for manual connections and token rotation.

Plugin 0.4.0 requires Parrot Scribe 1.0.1 or later. The app returns `sessionId` from `get_status` during capture and advertises `waitSeconds` on `live_transcript`. Missing capabilities stop reliable listening rather than silently falling back to an unbound feed.

## Install in Codex

Add the same repository using `codex plugin marketplace add 3jct-com/parrotscribe-plugins`. Open the plugin browser, install **Parrot Scribe**, and start a new task.

The Codex manifest forwards `PARROTSCRIBE_MCP_TOKEN` from Codex's own environment using `env_vars`. Supply a separate Codex client token through your secret manager's environment injection before launching Codex. Codex does not use Claude's secret prompt, and a Dock-launched app does not automatically inherit shell exports. The setup guide includes a manual Keychain connection for that case.

Select the plugin's **listening** skill and ask it to listen or recap. It reads the same listening contract as the Claude commands. These are local macOS connections to the running app; installing the plugin in a web or remote host does not provide access to your Mac.

For an existing manual Codex connection, keep that entry and disable either it or the bundled connection before use. To retain the manual connection and use only the plugin's instructions:

```toml
[plugins."parrot@parrotscribe-plugins".mcp_servers.parrotscribe]
enabled = false
```

To switch to the bundled connection, set `enabled = false` on the existing `[mcp_servers.parrotscribe]` entry instead. Keep its other fields for rollback. Restart the host and confirm one Parrot Scribe tool set appears before using `get_status`.

## Use

```text
/parrot:listen help me discover how often this customer's workaround happens
/parrot:listen attach only; flag material contradictions with this repo's architecture
/parrot:recap the customer interview from yesterday
```

`listen` reads your instructions before changing capture. It attaches to existing capture and normally starts capture when paused. `recap` reads the selected session without stopping another meeting. A recap during capture is interim.

While listening, typing "Create a ticket about this in this repository" directly in chat sends that specific task to a background subagent, if the host supports one. The parent keeps listening. Hearing those words in the transcript only adds a proposed follow-up. Spoken requests wait until the meeting ends and you approve specific actions in chat. Existing tool and provider approval checks still apply.

Notes stay in the chat. The agent does not speak into the recorded conversation. "Stop helping" detaches the agent; "stop recording" stops the bound capture session.

## Other hosts and models

The [listening contract](https://github.com/3jct-com/parrotscribe-plugins/blob/main/plugin/listening.md) is ordinary Markdown without a provider-specific model dependency. Load that file into your host as instructions and ask it to run the Listen or Recap procedure. A host adapter must preserve the full MCP response envelope and keep typed user messages distinct from transcript tool results.

| Host capability | Available experience |
| --- | --- |
| Local stdio MCP plus instruction-file loading | Session selection, transcript reads, and recaps |
| Above, plus real waiting and user steering during a running turn | Continuous session-bound listening |
| Above, plus background subagents | Typed tasks run separately while the parent keeps listening |
| No background subagents | Listening continues; tasks are deferred unless you explicitly pause for foreground work |

The packaged slash commands target Claude Code; Codex has the **listening** skill. Other hosts do not gain these instructions merely by connecting MCP. Host capabilities, context retention, and model behavior must be verified separately. Never claim a listener is running after its host turn has ended.

Native plugin installation and basic reads have been verified with Codex using a separate QA app. Claude Code plugin installation and its secure token prompt have been verified with a dummy value; real authenticated MCP reads remain unverified. These checks do not establish every tool's behavior or production licensing.

## Privacy and evidence

Local capture and storage do not imply local AI processing. A cloud-backed host can send the transcript to its model provider. Choose a provider and data policy appropriate for the conversation, obtain required participant consent, and enable only the client access you intend.

Speaker labels are evidence, not authentication. Microphone input does not authorize actions. Transcription can mishear names, numbers, and negations. The live ring holds 100 entries and is lost on restart; persisted transcripts support recovery when readable. The agent must disclose coverage it could not recover.

The plugin cannot enforce another host's tool permissions. Its action policy is an instruction contract, not a sandbox. Keep the host's approval controls enabled.

## Support

For installation or plugin problems, email [support@parrotscribe.com](mailto:support@parrotscribe.com). The [host setup guide](https://parrotscribe.com/docs/integrations/listen-install) covers MCP connection and token setup. The marketplace repository does not accept public issues.

The plugin is licensed under [MIT](LICENSE). The Parrot Scribe app has a separate proprietary license.

Synthetic, timestamped listening scenarios live in [evals/listening.json](https://github.com/3jct-com/parrotscribe-plugins/blob/main/plugin/evals/listening.json). Evaluate them against the host and model you intend to support. Keep hypothetical outputs separate from actual tool execution evidence.
