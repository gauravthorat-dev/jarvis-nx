# WebSocket Event API

## Client -> Server
- `{"type":"user_text","text":"..."}`: submit user query.

## Server -> Client
- `state`: assistant state (`listen`, `think`, `speak`, `standby`).
- `user`: rendered user text.
- `jarvis`: finalized assistant response.
- `jarvis_stream`: streaming text chunk.
- `jarvis_stream_end`: streaming completed.
- `telemetry`: realtime system + network payload.
- `security`: realtime security payload.
- `security_scan_result`: full localhost nmap output (if requested).
- `error`: validation/rate-limit/auth feedback.

## Security
- Optional token query parameter: `ws://host:port?token=...`
- Rate limit and payload size are server-enforced.
