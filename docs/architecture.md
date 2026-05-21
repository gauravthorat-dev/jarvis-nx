# Architecture Deep Dive

## Core Flow
1. Voice/UI input received.
2. Sanitization + safety checks.
3. Intent and deterministic command routing.
4. Fallback to Ollama with memory context.
5. UI and voice output synchronized via WebSocket state events.

## Event-Driven Background Loops
- Telemetry loop publishes `telemetry` events every configured interval.
- Security loop publishes `security` events every configured interval.

## Safety Controls
- Optional WebSocket token authentication.
- Per-client rate limiting.
- Message size constraints.
- Safe host validation for network commands.

## Extensibility
- Plugin protocol (`jarvis.plugins.base`).
- Auto-loader scans `jarvis.plugins.modules`.
- Service-oriented boundaries simplify testing and replacement.
