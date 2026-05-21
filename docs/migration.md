# Migration Guide

## From Previous Upgraded Version
1. Replace existing `jarvis/assistant.py`, `jarvis/api/websocket_server.py`, and `frontend/index.html`.
2. Add new files under `jarvis/services/` (`network_service.py`, `security_service.py`) and `jarvis/core/` (`scheduler.py`, `validators.py`).
3. Update `.env` keys with new rate-limit and interval settings.
4. Reinstall dependencies (`pip install -r requirements.txt`).
5. Run smoke test: `python run_jarvis.py`.
