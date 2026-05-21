# Jarvis NX - Production-Minded AI Network & Security Assistant

Jarvis NX is a modular local-first assistant that combines voice + chat AI orchestration with realtime network telemetry and ethical cybersecurity monitoring.

## What Was Upgraded
- Command Handler Registry pattern (`jarvis/commands/*`)
- Event Bus architecture (`jarvis/core/event_bus.py`)
- Service Container / DI (`jarvis/app/container.py`)
- Centralized runtime state (`jarvis/core/state_store.py`)
- Background Task Manager with graceful cancellation (`jarvis/core/task_manager.py`)
- Typed WebSocket message contracts (`jarvis/contracts/events.py`)
- Health endpoint (`jarvis/api/health_server.py` on :8080)
- Docker + Compose support
- CI pipeline (ruff + mypy + pytest)
- Expanded tests (validators, security, event bus, registry)

## Architecture
See:
- `docs/engineering-upgrade.md`
- `docs/architecture.md`
- `docs/api/websocket-events.md`

## Core Features
- Async websocket assistant backend
- Ollama local LLM orchestration with fallback routing
- Voice recognition + TTS
- SQLite memory persistence
- Realtime network telemetry dashboard
- Security monitoring dashboard (educational/local-safe)
- App launch automation via allowlist

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run_jarvis.py
```

Health check:
- `http://127.0.0.1:8080`

## Tests
```bash
pytest -q
```

## Docker
```bash
docker compose up --build
```

## Tech Stack

- Python
- AsyncIO
- WebSockets
- Ollama
- SQLite
- Docker
- Pytest
- Ruff
- Mypy
- HTML/CSS/JavaScript
- GitHub Actions

## Recruiter Demo Flow (5 Minutes)
1. Start Jarvis and open dashboard.
2. Show live telemetry cards updating.
3. Run voice/text command: `system status and wifi status`.
4. Show cybersecurity panel + `scan localhost ports`.
5. Show AI fallback query + context continuity.
6. Mention architecture patterns: DI, event bus, command registry.

## Project Maturity
- Strong Fresher -> Junior-track architecture depth
- Production-minded guardrails, not overengineered complexity
- Clear path to industry-level with RAG + stricter auth + integration testing
