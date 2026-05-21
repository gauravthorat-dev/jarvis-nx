from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv('JARVIS_APP_NAME', 'Jarvis')
    ws_host: str = os.getenv('JARVIS_WS_HOST', '127.0.0.1')
    ws_port: int = int(os.getenv('JARVIS_WS_PORT', '8765'))
    ws_token: str = os.getenv('JARVIS_WS_TOKEN', '')
    ws_max_message_size: int = int(os.getenv('JARVIS_WS_MAX_MESSAGE_SIZE', '8192'))
    ws_rate_limit_per_minute: int = int(os.getenv('JARVIS_WS_RATE_LIMIT_PER_MINUTE', '120'))
    health_host: str = os.getenv('JARVIS_HEALTH_HOST', '127.0.0.1')
    health_port: int = int(os.getenv('JARVIS_HEALTH_PORT', '8080'))
    ui_file: str = os.getenv('JARVIS_UI_FILE', str(BASE_DIR / 'frontend' / 'index.html'))
    llm_model: str = os.getenv('JARVIS_LLM_MODEL', 'llama3')
    wake_word: str = os.getenv('JARVIS_WAKE_WORD', 'jarvis')
    require_wake_word: bool = os.getenv('JARVIS_REQUIRE_WAKE_WORD', 'false').lower() == 'true'
    telemetry_interval_sec: float = float(os.getenv('JARVIS_TELEMETRY_INTERVAL_SEC', '2.0'))
    security_interval_sec: float = float(os.getenv('JARVIS_SECURITY_INTERVAL_SEC', '5.0'))
    log_level: str = os.getenv('JARVIS_LOG_LEVEL', 'INFO')
    logs_dir: Path = BASE_DIR / 'logs'
    memory_db: Path = BASE_DIR / 'data' / 'memory.db'
    interaction_log_file: Path = BASE_DIR / 'interaction_log.json'
    news_cache_file: Path = BASE_DIR / 'data' / 'news_cache.json'


settings = Settings()
