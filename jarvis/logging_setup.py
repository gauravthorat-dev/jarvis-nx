from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from jarvis.config import settings


def configure_logging() -> None:
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    if root.handlers:
        return

    root.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

    file_handler = RotatingFileHandler(settings.logs_dir / 'jarvis.log', maxBytes=2_000_000, backupCount=5, encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root.addHandler(file_handler)
    root.addHandler(console_handler)
