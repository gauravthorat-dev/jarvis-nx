# Jarvis NX - Elite Engineering Upgrade

## Architecture Diagram

```text
+-------------------+      ws events      +----------------------+
| Frontend Dashboard| <------------------> | WebSocketHub (API)   |
+-------------------+                      +----------+-----------+
                                                      |
                                                      v
                                           +----------+-----------+
                                           | JarvisAssistant      |
                                           | (orchestrator)       |
                                           +----+-----------+-----+
                                                |           |
                                      commands  |           | events
                                                v           v
                                     +----------+--+   +---+----------------+
                                     | CommandRegistry| | EventBus           |
                                     +----------+--+   +--------------------+
                                                |
                                        +-------+-----------------------------------------+
                                        | Handlers: system, network, security, media, ai |
                                        +-------+-----------------------------------------+
                                                |
                +-------------------------------+----------------------------------+
                |                               |                                  |
                v                               v                                  v
      +---------+---------+            +--------+---------+               +--------+--------+
      | ServiceContainer  |            | TaskManager      |               | StateStore      |
      | (DI)              |            | bg loops         |               | central runtime |
      +---------+---------+            +--------+---------+               +--------+--------+
                |                               |                                  |
                +---------------------+---------+------------------+---------------+
                                      |                            |
                                      v                            v
                        +-------------+-----------+     +----------+-----------+
                        | Telemetry Loop (2s)     |     | Security Loop (5s)  |
                        +-------------------------+     +----------------------+
```

## Request Data Flow

```text
User Voice/Text
  -> sanitize_text
  -> split multi-command (' and ')
  -> plugin pre-check
  -> command registry dispatch
       -> deterministic handler if matched
       -> else intent classifier
       -> else LLM fallback with memory context
  -> response persistence (SQLite)
  -> WebSocket broadcast + TTS
```

## Typed Event Contract
- Implemented in `jarvis/contracts/events.py`
- Event types: `state`, `user`, `jarvis`, `telemetry`, `security`, `error`, `hint`, `voice_error`, etc.

## Production Hardening Added
- Command registry pattern
- Event bus abstraction
- Service container (DI)
- Central state store
- Task manager with graceful cancellation
- Health endpoint (`http://127.0.0.1:8080`)
- Docker + Compose
- CI workflow (lint/type/test)
- Expanded unit tests

## Remaining to reach true 10/10
1. Semantic memory + vector RAG with citations.
2. AuthN/AuthZ policy for privileged commands.
3. TLS reverse proxy + secure session handling.
4. End-to-end websocket + voice integration tests.
5. Performance load test and telemetry history storage.
