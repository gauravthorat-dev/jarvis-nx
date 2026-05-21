from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class CommandContext:
    query: str


class Plugin(Protocol):
    name: str

    async def can_handle(self, ctx: CommandContext) -> bool:
        ...

    async def handle(self, ctx: CommandContext) -> str | None:
        ...
