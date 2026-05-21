from __future__ import annotations

import asyncio

from jarvis.core.event_bus import EventBus


def test_event_bus_publish_subscribe() -> None:
    async def _run() -> None:
        bus = EventBus()
        seen = {'count': 0}

        async def handler(payload):
            if payload.get('ok'):
                seen['count'] += 1

        bus.subscribe('telemetry', handler)
        await bus.publish('telemetry', {'ok': True})

        assert seen['count'] == 1

    asyncio.run(_run())
