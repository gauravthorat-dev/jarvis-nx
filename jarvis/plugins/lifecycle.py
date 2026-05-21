from __future__ import annotations

from typing import Protocol


class LifecyclePlugin(Protocol):
    name: str

    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...


class PluginLifecycleManager:
    def __init__(self, plugins: list[LifecyclePlugin]) -> None:
        self.plugins = plugins

    async def start_all(self) -> None:
        for plugin in self.plugins:
            await plugin.start()

    async def stop_all(self) -> None:
        for plugin in reversed(self.plugins):
            await plugin.stop()
