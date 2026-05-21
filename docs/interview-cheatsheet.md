# Interview Cheat Sheet

## 90-Second Architecture Pitch
Jarvis NX is a local-first, event-driven assistant platform. I separated orchestration from capabilities using a DI container and command registry, then connected everything with typed websocket contracts and an event bus. Deterministic handlers execute system/network/security commands, while unresolved queries route to Ollama with SQLite-backed context memory. Background task loops stream telemetry and security snapshots to a realtime dashboard. I added production-minded scaffolding: health endpoint, Docker/Compose, CI checks, rate limiting, input sanitization, and unit tests.

## Tough Questions + Strong Answers
1. Why command registry over giant if/else?
- Better separation of concerns, easier extension, focused testability, lower merge conflict risk.

2. How do you prevent websocket abuse?
- Max payload size, per-client rate limits, optional token auth, sanitization, and TLS-ready deployment guidance.

3. How is AI reliability improved?
- Deterministic command routing first, intent fallback second, LLM fallback last; reduces hallucination for operational actions.

4. How would you scale?
- Move heavy actions to worker queue, persist telemetry in TSDB, shard websocket gateways, add auth service and observability.

5. Security boundaries?
- Local-safe scanning policy, fixed subprocess vectors, host validation, and ethical-only messaging. Next step: policy/RBAC layer.
