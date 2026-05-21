from __future__ import annotations

from dataclasses import dataclass

from jarvis.api.websocket_server import WebSocketHub
from jarvis.config import settings
from jarvis.core.event_bus import EventBus
from jarvis.core.state_store import StateStore
from jarvis.core.task_manager import TaskManager
from jarvis.services.intent_service import IntentClassifier
from jarvis.services.llm_service import OllamaService
from jarvis.services.memory_service import MemoryStore
from jarvis.services.network_service import NetworkService
from jarvis.services.security_service import SecurityService
from jarvis.services.speech_service import SpeechService
from jarvis.services.tts_service import TTSService


@dataclass(slots=True)
class ServiceContainer:
    tts: TTSService
    speech: SpeechService
    llm: OllamaService
    memory: MemoryStore
    intent: IntentClassifier
    network: NetworkService
    security: SecurityService
    hub: WebSocketHub
    bus: EventBus
    tasks: TaskManager
    state: StateStore


def build_container() -> ServiceContainer:
    return ServiceContainer(
        tts=TTSService(),
        speech=SpeechService(),
        llm=OllamaService(settings.llm_model),
        memory=MemoryStore(settings.memory_db),
        intent=IntentClassifier('data/jarvis_model.pkl', 'data/jarvis_vectorizer.pkl'),
        network=NetworkService(),
        security=SecurityService(),
        hub=WebSocketHub(
            settings.ws_host,
            settings.ws_port,
            settings.ws_max_message_size,
            settings.ws_token,
            settings.ws_rate_limit_per_minute,
        ),
        bus=EventBus(),
        tasks=TaskManager(),
        state=StateStore(),
    )
