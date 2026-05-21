from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any


@dataclass
class AssistantState:
    mode: str = 'standby'
    connected_clients: int = 0
    query_count: int = 0
    last_user_query: str = ''
    counters: dict[str, int] = field(default_factory=dict)


class StateStore:
    def __init__(self) -> None:
        self._state = AssistantState()
        self._lock = Lock()

    def snapshot(self) -> AssistantState:
        with self._lock:
            return AssistantState(**self._state.__dict__)

    def update(self, **kwargs: Any) -> None:
        with self._lock:
            for k, v in kwargs.items():
                setattr(self._state, k, v)

    def increment(self, key: str, amount: int = 1) -> None:
        with self._lock:
            self._state.counters[key] = self._state.counters.get(key, 0) + amount
