from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)


class BackgroundScheduler:
    def __init__(self) -> None:
        self._tasks: list[asyncio.Task] = []

    def schedule(self, coro_factory: Callable[[], Awaitable[None]], name: str) -> None:
        async def runner() -> None:
            while True:
                try:
                    await coro_factory()
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    logger.exception('Background task %s failed: %s', name, exc)
                    await asyncio.sleep(1)

        self._tasks.append(asyncio.create_task(runner(), name=name))

    async def stop(self) -> None:
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
