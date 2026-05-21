# Deployment Guide

## Local
1. `python -m venv .venv`
2. `.venv\\Scripts\\activate`
3. `pip install -r requirements.txt`
4. `copy .env.example .env`
5. `python run_jarvis.py`
6. Health check: `http://127.0.0.1:8080`

## Docker
1. `docker build -t jarvis-nx .`
2. `docker run -p 8765:8765 -p 8080:8080 --env-file .env jarvis-nx`

## Docker Compose
- `docker compose up --build`

## Production Checklist
- Set `JARVIS_WS_TOKEN`.
- Keep `JARVIS_WS_HOST=127.0.0.1` unless reverse-proxied.
- Put TLS termination in nginx/caddy.
- Restrict privileged commands.
- Enable CI gate on PRs.
