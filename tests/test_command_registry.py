from __future__ import annotations

import asyncio

from jarvis.commands.base import Command
from jarvis.commands.registry import CommandRegistry


def test_command_registry_dispatches_first_match() -> None:
    async def _run() -> None:
        reg = CommandRegistry()

        async def h1(_: str) -> str:
            return 'first'

        async def h2(_: str) -> str:
            return 'second'

        reg.register(Command('c1', lambda q: 'open' in q, h1))
        reg.register(Command('c2', lambda q: True, h2))

        out = await reg.dispatch('open notepad')
        assert out == 'first'

    asyncio.run(_run())


def test_command_registry_none_when_no_match() -> None:
    async def _run() -> None:
        reg = CommandRegistry()

        async def h(_: str) -> str:
            return 'x'

        reg.register(Command('only', lambda q: q == 'abc', h))
        out = await reg.dispatch('zzz')
        assert out is None

    asyncio.run(_run())
