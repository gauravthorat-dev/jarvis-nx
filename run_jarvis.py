from __future__ import annotations

import asyncio

from jarvis.assistant import JarvisAssistant
from jarvis.logging_setup import configure_logging


def main() -> None:
    configure_logging()
    assistant = JarvisAssistant()
    asyncio.run(assistant.run())


if __name__ == '__main__':
    main()
