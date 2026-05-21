# Jarvis NX - Production-Minded AI Network & Security Assistant

Jarvis NX is a modular, local-first AI assistant platform that combines voice + chat AI orchestration with realtime networking telemetry, system monitoring, and ethical cybersecurity awareness features.

Designed with production-minded architecture patterns, Jarvis NX focuses on realtime async communication, scalable modular engineering, AI orchestration, and practical diagnostics tooling.

---

# Features

| Feature                  | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| AI Assistant             | Local-first Ollama-powered conversational assistant           |
| Async Architecture       | Event-driven realtime backend using AsyncIO                   |
| WebSocket Communication  | Live frontend/backend synchronization                         |
| Voice Interaction        | Speech recognition + text-to-speech support                   |
| Networking Telemetry     | Realtime IP, Wi-Fi, DNS, gateway, and connectivity monitoring |
| Cybersecurity Monitoring | Local-safe security checks and localhost port scanning        |
| SQLite Memory            | Persistent contextual conversation memory                     |
| System Monitoring        | CPU, memory, and system telemetry support                     |
| Docker Support           | Containerized deployment with Docker Compose                  |
| CI/CD Pipeline           | Ruff, Mypy, and Pytest integrated workflow                    |
| Modular Architecture     | DI container, command registry, event bus, plugin scaffolding |

---

# Architecture Highlights

Jarvis NX was upgraded using modern engineering architecture patterns:

* Command Handler Registry pattern (`jarvis/commands/*`)
* Event Bus architecture (`jarvis/core/event_bus.py`)
* Dependency Injection / Service Container (`jarvis/app/container.py`)
* Centralized runtime state (`jarvis/core/state_store.py`)
* Background Task Manager with graceful cancellation (`jarvis/core/task_manager.py`)
* Typed WebSocket event contracts (`jarvis/contracts/events.py`)
* Health endpoint service (`jarvis/api/health_server.py`)
* Plugin lifecycle scaffolding
* Async orchestration runtime
* Realtime telemetry pipeline

---

# Core Capabilities

## AI & Assistant Features

* Ollama local LLM orchestration
* Intent routing and fallback handling
* Voice recognition + TTS
* Context-aware memory persistence
* Async conversational pipeline

## Networking Features

* Public/private IP detection
* DNS and gateway diagnostics
* Wi-Fi information monitoring
* Connectivity checks
* Ping-based telemetry
* Realtime network dashboard

## Cybersecurity Features

* Educational localhost-safe port scanning
* Firewall awareness checks
* Suspicious process monitoring
* Password strength analysis
* Security telemetry dashboard

## System Features

* Runtime health monitoring
* Async task scheduling
* Application automation via allowlist
* Structured logging pipeline

---

# Project Structure

```text
jarvis-nx/
│
├── jarvis/
│   ├── api/
│   ├── app/
│   ├── commands/
│   ├── contracts/
│   ├── core/
│   ├── plugins/
│   ├── services/
│
├── frontend/
├── docs/
├── tests/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run_jarvis.py
```

---

# Tech Stack

* Python
* AsyncIO
* WebSockets
* Ollama
* SQLite
* Docker
* Pytest
* Ruff
* Mypy
* HTML/CSS/JavaScript
* GitHub Actions

---

# Screenshots

*Add dashboard and telemetry screenshots here.*

Example:

* Main AI Dashboard
* Network Telemetry Panel
* Security Monitoring Dashboard
* Voice Assistant Interface

---

# Architecture Documentation

See:

* `docs/engineering-upgrade.md`
* `docs/architecture.md`
* `docs/api/websocket-events.md`
* `docs/deployment.md`
* `docs/security-checklist.md`

---

# Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env

python run_jarvis.py
```

---

# Health Check

```text
http://127.0.0.1:8080
```

---

# Run Tests

```bash
pytest -q
```

---

# Docker Deployment

```bash
docker compose up --build
```

---

# Recruiter Demo Flow (5 Minutes)

1. Start Jarvis NX and open dashboard
2. Show realtime telemetry cards updating
3. Run commands:

   * `system status`
   * `wifi status`
4. Demonstrate localhost-safe port scan
5. Show AI fallback + memory continuity
6. Explain:

   * Event Bus
   * Dependency Injection
   * Command Registry
   * Async orchestration
   * WebSocket communication

---

# Engineering Focus

Jarvis NX emphasizes:

* Production-minded engineering
* Realtime async architecture
* Local-first AI systems
* Ethical cybersecurity awareness
* Networking telemetry
* Maintainable modular design

---

# Project Maturity

* Strong Fresher → Junior-track architecture depth
* Production-minded guardrails without unnecessary complexity
* Demonstrates async systems, AI orchestration, networking, and modular engineering concepts
* Clear path toward industry-level architecture with:

  * RAG pipelines
  * stricter authorization
  * integration testing
  * streaming AI responses

---

# Future Roadmap

* Local RAG document assistant
* Streaming token rendering
* Whisper offline STT
* Advanced integration tests
* Historical telemetry visualization
* Secure authorization policies
* Realtime telemetry graphs
* Plugin marketplace system

---

# Disclaimer

This project is designed for:

* educational purposes
* ethical experimentation
* local-first AI workflows
* safe networking/security demonstrations

Cybersecurity-related functionality is intentionally restricted to safe local use cases.

---

## Why This Project?

Jarvis NX was built to explore production-minded AI system engineering using realtime async architecture, networking telemetry, ethical cybersecurity concepts, and modular scalable backend design.

---

# License

MIT License
