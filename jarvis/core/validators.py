from __future__ import annotations

import re

SAFE_HOST_PATTERN = re.compile(r'^[a-zA-Z0-9.-]{1,253}$')
ANSI_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def sanitize_text(text: str, max_len: int = 500) -> str:
    cleaned = ANSI_RE.sub('', text or '')
    return ' '.join(cleaned.strip().split())[:max_len]


def is_safe_host(host: str) -> bool:
    return bool(SAFE_HOST_PATTERN.match(host))
