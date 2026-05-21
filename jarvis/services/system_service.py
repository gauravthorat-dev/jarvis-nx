from __future__ import annotations

import datetime
import os
import platform
import socket
import subprocess
from typing import Any

import psutil


def system_snapshot() -> dict[str, Any]:
    vm = psutil.virtual_memory()
    return {
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'platform': platform.platform(),
        'cpu_percent': psutil.cpu_percent(interval=0.2),
        'memory_percent': vm.percent,
        'memory_used_gb': round(vm.used / (1024**3), 2),
        'memory_total_gb': round(vm.total / (1024**3), 2),
        'disk_percent': psutil.disk_usage('/').percent,
        'battery_percent': getattr(psutil.sensors_battery(), 'percent', None),
    }


def local_ip_info() -> dict[str, str]:
    hostname = socket.gethostname()
    return {'hostname': hostname, 'ip_address': socket.gethostbyname(hostname)}


def ping_host(host: str = '8.8.8.8') -> str:
    flag = '-n' if platform.system().lower().startswith('win') else '-c'
    result = subprocess.run(['ping', flag, '2', host], capture_output=True, text=True, timeout=15)
    return result.stdout.splitlines()[-1] if result.stdout else 'Ping completed.'


def wifi_status() -> str:
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True, timeout=10)
        lines = [line.strip() for line in result.stdout.splitlines() if 'SSID' in line or 'Signal' in line or 'State' in line]
        return '; '.join(lines) if lines else 'Wi-Fi details unavailable.'
    except Exception:
        return 'Wi-Fi details unavailable.'


def top_processes(limit: int = 5) -> list[str]:
    procs = []
    for p in psutil.process_iter(['name', 'cpu_percent']):
        info = p.info
        procs.append((info.get('name', 'unknown'), info.get('cpu_percent', 0.0) or 0.0))
    procs.sort(key=lambda x: x[1], reverse=True)
    return [f'{name}: {cpu:.1f}%' for name, cpu in procs[:limit]]


def open_application(app_name: str) -> str:
    """Open a common desktop application safely by alias."""
    app = (app_name or '').strip().lower()
    if not app:
        return 'Please tell me which app to open.'

    alias_map = {
        'notepad': ['notepad.exe'],
        'calculator': ['calc.exe'],
        'paint': ['mspaint.exe'],
        'cmd': ['cmd.exe'],
        'powershell': ['powershell.exe'],
        'chrome': ['chrome.exe'],
        'google chrome': ['chrome.exe'],
        'edge': ['msedge.exe'],
        'microsoft edge': ['msedge.exe'],
        'firefox': ['firefox.exe'],
        'vscode': ['code.cmd'],
        'vs code': ['code.cmd'],
        'visual studio code': ['code.cmd'],
        'whatsapp': ['start', 'whatsapp:'],
        'settings': ['start', 'ms-settings:'],
        'file explorer': ['explorer.exe'],
        'explorer': ['explorer.exe'],
    }

    cmd = alias_map.get(app)
    if not cmd:
        return f"I don't have a safe launcher configured for {app_name}."

    try:
        if cmd[0] == 'start':
            os.startfile(cmd[1])  # type: ignore[attr-defined]
        else:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f'Opening {app_name}.'
    except Exception:
        return f"I couldn't open {app_name} on this system."
