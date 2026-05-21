from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any


EventHandler = Callable[[dict[str, Any]], Awaitable[None]]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        self._handlers[topic].append(handler)

    async def publish(self, topic: str, payload: dict[str, Any]) -> None:
        handlers = self._handlers.get(topic, [])
        if not handlers:
            return
        await asyncio.gather(*(h(payload) for h in handlers), return_exceptions=True)
