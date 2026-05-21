from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class EventType(StrEnum):
    STATE = 'state'
    USER = 'user'
    JARVIS = 'jarvis'
    JARVIS_STREAM = 'jarvis_stream'
    JARVIS_STREAM_END = 'jarvis_stream_end'
    TELEMETRY = 'telemetry'
    SECURITY = 'security'
    SECURITY_SCAN_RESULT = 'security_scan_result'
    ERROR = 'error'
    HINT = 'hint'
    VOICE_ERROR = 'voice_error'
    SYSTEM_EVENT = 'system_event'


@dataclass(slots=True)
class WsEvent:
    type: EventType
    payload: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {'type': self.type.value, **self.payload}
