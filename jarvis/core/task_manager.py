from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self) -> None:
        self._tasks: list[asyncio.Task] = []

    def spawn(self, coro: Awaitable[None], name: str) -> asyncio.Task:
        task = asyncio.create_task(coro, name=name)
        self._tasks.append(task)
        return task

    def schedule_loop(self, loop_coro_factory: Callable[[], Awaitable[None]], name: str) -> None:
        async def runner() -> None:
            while True:
                try:
                    await loop_coro_factory()
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    logger.exception('Background task %s failed: %s', name, exc)
                    await asyncio.sleep(0.5)

        self.spawn(runner(), name)

    async def shutdown(self) -> None:
        for task in self._tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
