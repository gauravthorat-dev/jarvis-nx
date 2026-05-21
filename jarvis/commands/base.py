from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable


@dataclass(slots=True)
class Command:
    name: str
    matcher: Callable[[str], bool]
    handler: Callable[[str], Awaitable[str | None]]
