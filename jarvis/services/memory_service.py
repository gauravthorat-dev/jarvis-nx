from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterable


class MemoryStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL,
                    user_text TEXT NOT NULL,
                    assistant_text TEXT NOT NULL
                )
                '''
            )
            conn.commit()

    def add(self, user_text: str, assistant_text: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT INTO interactions(ts, user_text, assistant_text) VALUES (?, ?, ?)',
                (datetime.now().isoformat(timespec='seconds'), user_text, assistant_text),
            )
            conn.commit()

    def recent(self, limit: int = 8) -> Iterable[tuple[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                'SELECT user_text, assistant_text FROM interactions ORDER BY id DESC LIMIT ?', (limit,)
            ).fetchall()
        return list(reversed(rows))

    def clear(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM interactions')
            conn.commit()
