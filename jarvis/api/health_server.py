from __future__ import annotations

import asyncio
import json
from contextlib import suppress


class HealthServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8080, snapshot_provider=None) -> None:
        self.host = host
        self.port = port
        self.snapshot_provider = snapshot_provider
        self._server = None

    async def _handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        with suppress(Exception):
            await reader.read(1024)
        body = json.dumps({'status': 'ok', 'state': self.snapshot_provider() if self.snapshot_provider else {}})
        response = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: application/json\r\n'
            f'Content-Length: {len(body)}\r\n'
            'Connection: close\r\n\r\n'
            f'{body}'
        )
        writer.write(response.encode('utf-8'))
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def start(self) -> None:
        self._server = await asyncio.start_server(self._handler, self.host, self.port)

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
