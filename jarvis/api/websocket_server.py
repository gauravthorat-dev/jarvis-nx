from __future__ import annotations

import asyncio
import json
import logging
import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from urllib.parse import parse_qs, urlparse

import websockets

logger = logging.getLogger(__name__)


class WebSocketHub:
    def __init__(
        self,
        host: str,
        port: int,
        max_message_size: int = 8192,
        token: str = '',
        rate_limit_per_minute: int = 120,
    ) -> None:
        self.host = host
        self.port = port
        self.max_message_size = max_message_size
        self.token = token
        self.rate_limit_per_minute = rate_limit_per_minute
        self.clients: set = set()
        self._on_user_text: Callable[[str], Awaitable[None]] | None = None
        self._client_hits: dict[str, deque[float]] = defaultdict(deque)

    def on_user_text(self, handler: Callable[[str], Awaitable[None]]) -> None:
        self._on_user_text = handler

    def _is_authorized(self, websocket) -> bool:
        if not self.token:
            return True
        parsed = urlparse(getattr(websocket, 'path', '') or '')
        token = parse_qs(parsed.query).get('token', [''])[0]
        return token == self.token

    def _rate_limited(self, websocket) -> bool:
        remote = str(getattr(websocket, 'remote_address', 'unknown'))
        bucket = self._client_hits[remote]
        now = time.time()
        while bucket and now - bucket[0] > 60:
            bucket.popleft()
        if len(bucket) >= self.rate_limit_per_minute:
            return True
        bucket.append(now)
        return False

    async def _handler(self, websocket) -> None:
        if not self._is_authorized(websocket):
            await websocket.close(code=1008, reason='Unauthorized token')
            return

        self.clients.add(websocket)
        try:
            async for raw in websocket:
                if len(raw) > self.max_message_size:
                    continue
                if self._rate_limited(websocket):
                    await websocket.send(json.dumps({'type': 'error', 'text': 'Rate limit exceeded'}))
                    continue
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if payload.get('type') == 'user_text' and self._on_user_text:
                    text = str(payload.get('text', '')).strip()
                    if text:
                        await self._on_user_text(text)
        finally:
            self.clients.discard(websocket)

    async def broadcast(self, payload: dict) -> None:
        if not self.clients:
            return
        data = json.dumps(payload)
        await asyncio.gather(*(client.send(data) for client in list(self.clients)), return_exceptions=True)

    async def serve(self) -> None:
        async with websockets.serve(self._handler, self.host, self.port, max_size=self.max_message_size):
            logger.info('WebSocket server running on ws://%s:%s', self.host, self.port)
            await asyncio.Future()
