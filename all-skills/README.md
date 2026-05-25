# All Skills Package

Generated at: 2026-05-25 17:15:15 +0800

Packaged snapshot of all AgentSkills visible in the OpenClaw runtime used for this export.

## Layout

- `skills/openclaw-core/` — built-in OpenClaw skills
- `skills/plugin/` — plugin-provided skills
- `skills/user/` — user-installed skills
- `skills/session-selected/` — injected/selected session skill definitions

Total `SKILL.md` files: 56

## Inventory

- `skills/openclaw-core/1password` — Set up and use 1Password CLI for sign-in, desktop integration, and reading or injecting secrets.
- `skills/openclaw-core/apple-notes` — Create, view, edit, delete, search, move, or export Apple Notes via the memo CLI on macOS.
- `skills/openclaw-core/apple-reminders` — List, add, edit, complete, or delete Apple Reminders and reminder lists via remindctl.
- `skills/openclaw-core/bear-notes` — Create, search, and manage Bear notes via grizzly CLI.
- `skills/openclaw-core/blogwatcher` — Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI.
- `skills/openclaw-core/blucli` — BluOS CLI (blu) for discovery, playback, grouping, and volume.
- `skills/openclaw-core/bluebubbles` — Send and manage iMessages via BlueBubbles, including attachments, tapbacks, edits, replies, and groups.
- `skills/openclaw-core/camsnap` — Capture frames or clips from RTSP/ONVIF cameras.
- `skills/openclaw-core/canvas`
- `skills/openclaw-core/clawhub` — Search, install, update, sync, or publish agent skills with the ClawHub CLI and registry.
- `skills/openclaw-core/coding-agent` — 'Delegate coding tasks to Codex, Claude Code, OpenCode, or Pi agents via immediate background processes. Use when: (1) building or creating features/apps, (2) reviewing PRs in a temp clone/worktree, (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-line fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (use sessions_spawn with runtime:"acp"), or any work in ~/clawd workspace (never spawn agents here). All coding-agent runs start with background:true immediately. Claude Code: use --print --permission-mode bypassPermissions (no PTY). Codex/Pi/OpenCode: pty:true required. Completion notification must use openclaw message send, not system event/heartbeat.'
- `skills/openclaw-core/discord` — "Discord ops via the message tool (channel=discord)."
- `skills/openclaw-core/eightctl` — Control Eight Sleep pods (status, temperature, alarms, schedules).
- `skills/openclaw-core/gemini` — Gemini CLI for one-shot Q&A, summaries, and generation.
- `skills/openclaw-core/gh-issues` — "Fetch GitHub issues, delegate fixes to subagents, open PRs, watch reviews, or run /gh-issues workflows."
- `skills/openclaw-core/gifgrep` — Search GIF providers with CLI/TUI, download results, and extract stills/sheets.
- `skills/openclaw-core/github` — "Use gh for GitHub issues, PR status, CI/logs, comments, reviews, releases, and API queries."
- `skills/openclaw-core/gog` — Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.
- `skills/openclaw-core/goplaces` — Query Google Places for text search, place details, resolve, reviews, or scriptable JSON via goplaces.
- `skills/openclaw-core/healthcheck` — Audit and harden hosts running OpenClaw for SSH, firewall, updates, exposure, cron checks, and risk posture.
- `skills/openclaw-core/himalaya` — "Use himalaya to list, read, search, compose, reply, forward, and organize IMAP/SMTP email."
- `skills/openclaw-core/imsg` — iMessage/SMS CLI for listing chats, history, and sending messages via Messages.app.
- `skills/openclaw-core/mcporter` — List, configure, authenticate, call, and inspect MCP servers/tools with mcporter over HTTP or stdio.
- `skills/openclaw-core/model-usage` — Summarize CodexBar local cost logs by model for Codex or Claude, including current or full breakdowns.
- `skills/openclaw-core/nano-pdf` — Edit PDFs with natural-language instructions using the nano-pdf CLI.
- `skills/openclaw-core/node-connect` — Diagnose OpenClaw Android, iOS, or macOS node pairing, QR/setup code, route, auth, and connection failures.
- `skills/openclaw-core/notion` — Notion API for creating and managing pages, databases, and blocks.
- `skills/openclaw-core/obsidian` — Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.
- `skills/openclaw-core/openai-whisper` — Local speech-to-text with the Whisper CLI (no API key).
- `skills/openclaw-core/openai-whisper-api` — Transcribe audio via OpenAI Audio Transcriptions API (Whisper).
- `skills/openclaw-core/openhue` — Control Philips Hue lights and scenes via the OpenHue CLI.
- `skills/openclaw-core/oracle` — Use oracle CLI to bundle prompts and files for second-model debugging, refactor, design, or review checks.
- `skills/openclaw-core/ordercli` — Foodora-only CLI for checking past orders and active order status (Deliveroo WIP).
- `skills/openclaw-core/peekaboo` — Capture and automate macOS UI with the Peekaboo CLI.
- `skills/openclaw-core/sag` — ElevenLabs text-to-speech with mac-style say UX.
- `skills/openclaw-core/session-logs` — Search and analyze your own session logs (older/parent conversations) using jq.
- `skills/openclaw-core/sherpa-onnx-tts` — Local text-to-speech via sherpa-onnx (offline, no cloud)
- `skills/openclaw-core/skill-creator` — Create, edit, improve, tidy, review, audit, or restructure AgentSkills and SKILL.md files.
- `skills/openclaw-core/slack` — Use the Slack tool to react, pin/unpin, send, edit, delete messages, or fetch Slack member info.
- `skills/openclaw-core/songsee` — Generate spectrograms and feature-panel visualizations from audio with the songsee CLI.
- `skills/openclaw-core/sonoscli` — Control Sonos speakers (discover/status/play/volume/group).
- `skills/openclaw-core/spotify-player` — Terminal Spotify playback/search via spogo (preferred) or spotify_player.
- `skills/openclaw-core/summarize` — Summarize or transcribe URLs, YouTube/videos, podcasts, articles, transcripts, PDFs, and local files.
- `skills/openclaw-core/taskflow` — Coordinate multi-step detached tasks as one durable TaskFlow job with owner context, state, waits, and child tasks.
- `skills/openclaw-core/taskflow-inbox-triage` — Example TaskFlow pattern for inbox triage, intent routing, waiting on replies, and later summaries.
- `skills/openclaw-core/things-mac` — Add, update, list, search, or inspect Things 3 todos, inbox, today, projects, areas, and tags on macOS.
- `skills/openclaw-core/tmux` — Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.
- `skills/openclaw-core/trello` — Manage Trello boards, lists, and cards via the Trello REST API.
- `skills/openclaw-core/video-frames` — Extract frames or short clips from videos using ffmpeg.
- `skills/openclaw-core/voice-call` — Start voice calls via the OpenClaw voice-call plugin.
- `skills/openclaw-core/wacli` — Send third-party WhatsApp messages or sync/search WhatsApp history via wacli, not normal active chats.
- `skills/openclaw-core/weather` — "Get current weather, rain, temperature, and forecasts for locations or travel planning."
- `skills/openclaw-core/xurl` — Use xurl for authenticated X API posts, replies, search, DMs, media upload, followers, or raw v2 calls.
- `skills/plugin/browser-automation` — Use when controlling web pages with the OpenClaw browser tool, especially multi-step flows, login checks, tab management, or recovery from stale refs/timeouts.
- `skills/session-selected/sector-overview` — Create comprehensive industry and sector landscape reports covering market dynamics, competitive positioning, key players, and thematic trends. Use for client requests, sector initiations, thematic research pieces, or internal knowledge building. Triggers on "sector overview", "industry report", "market landscape", "sector analysis", "industry deep dive", or "thematic research".
- `skills/user/wind-mcp-skill` — >-
