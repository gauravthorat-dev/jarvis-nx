from __future__ import annotations

from jarvis.commands.base import Command


class CommandRegistry:
    def __init__(self) -> None:
        self._commands: list[Command] = []

    def register(self, command: Command) -> None:
        self._commands.append(command)

    async def dispatch(self, query: str) -> str | None:
        for command in self._commands:
            if command.matcher(query):
                return await command.handler(query)
        return None
