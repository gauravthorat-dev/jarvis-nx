from __future__ import annotations

import logging
import re
import subprocess
import time
from collections.abc import Callable

logger = logging.getLogger(__name__)
ANSI_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


class OllamaService:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def ask(self, prompt: str, timeout: int = 120, retries: int = 1) -> str:
        for attempt in range(retries + 1):
            try:
                proc = subprocess.run(
                    ['ollama', 'run', self.model_name, prompt],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    timeout=timeout,
                )
                output = (proc.stdout or '').strip()
                if output:
                    return self._clean_output(output)
                if attempt < retries:
                    time.sleep(1.0)
            except FileNotFoundError:
                return 'Ollama not found. Please install and run Ollama locally.'
            except subprocess.TimeoutExpired:
                if attempt < retries:
                    continue
                return 'Model timeout: response took too long.'
            except Exception as exc:
                logger.exception('Ollama call failed: %s', exc)
                if attempt < retries:
                    time.sleep(1.0)
        return 'I could not generate a response right now.'

    def ask_stream(self, prompt: str, on_chunk: Callable[[str], None], timeout: int = 120) -> str:
        """Streams Ollama output chunks when possible and returns full response."""
        try:
            proc = subprocess.Popen(
                ['ollama', 'run', self.model_name, prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore',
            )
            chunks: list[str] = []
            start = time.time()
            while True:
                if time.time() - start > timeout:
                    proc.kill()
                    return 'Model timeout: response took too long.'
                if proc.stdout is None:
                    break
                char = proc.stdout.read(1)
                if char:
                    chunks.append(char)
                    if len(chunks) % 20 == 0:
                        on_chunk(''.join(chunks[-20:]))
                elif proc.poll() is not None:
                    break
            output = self._clean_output(''.join(chunks))
            return output or 'I could not generate a streamed response right now.'
        except FileNotFoundError:
            return 'Ollama not found. Please install and run Ollama locally.'
        except Exception as exc:
            logger.exception('Ollama stream failed: %s', exc)
            return 'Streaming response failed.'

    @staticmethod
    def _clean_output(text: str) -> str:
        cleaned = ANSI_RE.sub('', text or '')
        cleaned = cleaned.replace('*', '').replace('`', '')
        return ' '.join(cleaned.split()).strip()
