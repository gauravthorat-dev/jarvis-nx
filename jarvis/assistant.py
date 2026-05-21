from __future__ import annotations

import asyncio
import os
import random
import signal
import webbrowser
from pathlib import Path

from responses import responses

from jarvis.api.health_server import HealthServer
from jarvis.app.container import ServiceContainer, build_container
from jarvis.commands.default_handlers import register_default_commands
from jarvis.commands.registry import CommandRegistry
from jarvis.config import settings
from jarvis.contracts.events import EventType, WsEvent
from jarvis.core.validators import sanitize_text
from jarvis.plugins.base import CommandContext
from jarvis.plugins.loader import load_plugins
from jarvis.services.system_service import system_snapshot


class JarvisAssistant:
    def __init__(self, container: ServiceContainer | None = None) -> None:
        self.c = container or build_container()
        self.plugins = load_plugins()
        self.registry = CommandRegistry()
        register_default_commands(self.registry, self)
        self.c.hub.on_user_text(self.on_user_text)
        self.health = HealthServer(
            host=settings.health_host,
            port=settings.health_port,
            snapshot_provider=lambda: self.c.state.snapshot().__dict__,
        )
        self._stop_event = asyncio.Event()

    async def emit(self, event: WsEvent) -> None:
        await self.c.bus.publish(event.type.value, event.payload)
        await self.c.hub.broadcast(event.as_dict())

    async def emit_security_scan(self, text: str) -> None:
        await self.emit(WsEvent(EventType.SECURITY_SCAN_RESULT, {'text': text}))

    async def speak(self, text: str) -> None:
        text = sanitize_text(text, 2000)
        if not text:
            return
        self.c.state.update(mode='speak')
        await self.emit(WsEvent(EventType.STATE, {'state': 'speak'}))
        await self.emit(WsEvent(EventType.JARVIS, {'text': text}))
        await asyncio.to_thread(self.c.tts.speak, text)
        self.c.state.update(mode='standby')
        await self.emit(WsEvent(EventType.STATE, {'state': 'standby'}))

    async def on_user_text(self, text: str) -> None:
        await self.handle_query(text, source='ui')

    async def _broadcast_telemetry(self) -> None:
        sys_snap = await asyncio.to_thread(system_snapshot)
        net_snap = await asyncio.to_thread(self.c.network.snapshot)
        await self.emit(WsEvent(EventType.TELEMETRY, {'system': sys_snap, 'network': net_snap}))
        await asyncio.sleep(settings.telemetry_interval_sec)

    async def _broadcast_security(self) -> None:
        sec_snap = await asyncio.to_thread(self.c.security.snapshot)
        await self.emit(WsEvent(EventType.SECURITY, {'data': sec_snap}))
        await asyncio.sleep(settings.security_interval_sec)

    async def _handle_plugins(self, query: str) -> str | None:
        ctx = CommandContext(query=query)
        for plugin in self.plugins:
            if await plugin.can_handle(ctx):
                return await plugin.handle(ctx)
        return None

    async def _fallback_llm(self, query: str) -> str:
        tag = self.c.intent.predict(query)
        if tag and tag in responses:
            return random.choice(responses[tag])

        context = '\n'.join([f'User: {u}\nJarvis: {a}' for u, a in self.c.memory.recent(8)])
        prompt = (
            'You are Jarvis, an AI networking and system assistant. '
            'Be concise, accurate, and practical.\n'
            f'Conversation memory:\n{context}\n'
            f'User: {query}\nJarvis:'
        )
        return await asyncio.to_thread(self.c.llm.ask, prompt)

    async def _handle_single_command(self, query: str, source: str) -> str | None:
        query = sanitize_text(query)
        if not query:
            return None

        self.c.state.update(last_user_query=query, query_count=self.c.state.snapshot().query_count + 1)
        await self.emit(WsEvent(EventType.USER, {'text': query}))

        if source == 'voice' and settings.require_wake_word and settings.wake_word.lower() not in query.lower():
            await self.emit(WsEvent(EventType.HINT, {'text': f'Wake word required. Say "{settings.wake_word} <command>".'}))
            return None

        q = query.lower().replace(settings.wake_word.lower(), '').strip(' ,')

        if any(w in q for w in ['exit', 'bye', 'quit', 'shutdown']):
            goodbye = random.choice(responses['goodbye'])
            await self.speak(goodbye)
            return 'exit'

        plugin_response = await self._handle_plugins(q)
        if plugin_response:
            self.c.memory.add(query, plugin_response)
            await self.speak(plugin_response)
            return None

        cmd_response = await self.registry.dispatch(q)
        if cmd_response is not None:
            self.c.memory.add(query, cmd_response)
            await self.speak(cmd_response)
            return None

        llm_response = await self._fallback_llm(query)
        self.c.memory.add(query, llm_response)
        await self.speak(llm_response)
        return None

    async def handle_query(self, query: str, source: str = 'voice') -> str | None:
        self.c.state.update(mode='think')
        await self.emit(WsEvent(EventType.STATE, {'state': 'think'}))
        parts = [p.strip() for p in query.split(' and ') if p.strip()]
        for command in parts:
            result = await self._handle_single_command(command, source)
            if result == 'exit':
                return result
        return None

    async def voice_loop(self) -> None:
        while not self._stop_event.is_set():
            self.c.state.update(mode='listen')
            await self.emit(WsEvent(EventType.STATE, {'state': 'listen'}))
            query = await asyncio.to_thread(self.c.speech.listen)
            if not query:
                if self.c.speech.last_error:
                    await self.emit(WsEvent(EventType.VOICE_ERROR, {'text': self.c.speech.last_error}))
                await asyncio.sleep(0.1)
                continue
            result = await self.handle_query(query, source='voice')
            if result == 'exit':
                self._stop_event.set()
                break

    async def shutdown(self) -> None:
        self._stop_event.set()
        await self.health.stop()
        await self.c.tasks.shutdown()

    async def run(self) -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self._stop_event.set)
            except NotImplementedError:
                pass

        ui_path = Path(settings.ui_file).resolve()
        if ui_path.exists():
            webbrowser.open(f'file:///{ui_path.as_posix()}')

        ws_task = self.c.tasks.spawn(self.c.hub.serve(), 'ws-server')
        await self.health.start()
        self.c.tasks.schedule_loop(self._broadcast_telemetry, 'telemetry-loop')
        self.c.tasks.schedule_loop(self._broadcast_security, 'security-loop')
        self.c.tasks.spawn(self.voice_loop(), 'voice-loop')

        await asyncio.sleep(0.2)
        await self.speak('System online. Jarvis networking and security dashboard is active.')

        await self._stop_event.wait()
        await self.shutdown()

        if not ws_task.done():
            ws_task.cancel()
