from __future__ import annotations

import ipaddress
import platform
import re
import socket
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import psutil
import requests


class NetworkService:
    """Collects local networking telemetry for dashboard and commands."""

    @staticmethod
    def private_ip() -> str:
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def public_ip() -> str:
        try:
            return requests.get('https://api.ipify.org', timeout=4).text.strip()
        except Exception:
            return 'Unavailable'

    @staticmethod
    def gateway_info() -> str:
        try:
            if platform.system().lower().startswith('win'):
                out = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=10).stdout
                for line in out.splitlines():
                    if 'Default Gateway' in line and ':' in line:
                        val = line.split(':', 1)[1].strip()
                        if val:
                            return val
            return 'Unavailable'
        except Exception:
            return 'Unavailable'

    @staticmethod
    def dns_info() -> list[str]:
        servers: list[str] = []
        try:
            if platform.system().lower().startswith('win'):
                out = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, timeout=10).stdout
                capture = False
                for line in out.splitlines():
                    if 'DNS Servers' in line:
                        capture = True
                        servers.append(line.split(':', 1)[1].strip())
                        continue
                    if capture:
                        if line.startswith(' ' * 10):
                            item = line.strip()
                            if item:
                                servers.append(item)
                        else:
                            capture = False
            return [s for s in servers if s] or ['Unavailable']
        except Exception:
            return ['Unavailable']

    @staticmethod
    def wifi_info() -> dict[str, str]:
        result = {'state': 'unknown', 'ssid': 'n/a', 'signal': 'n/a'}
        try:
            out = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True, timeout=10).stdout
            for line in out.splitlines():
                if 'State' in line:
                    result['state'] = line.split(':', 1)[1].strip()
                elif re.match(r'\s*SSID\s*:', line):
                    result['ssid'] = line.split(':', 1)[1].strip()
                elif 'Signal' in line:
                    result['signal'] = line.split(':', 1)[1].strip()
            return result
        except Exception:
            return result

    @staticmethod
    def ping_latency(host: str = '8.8.8.8') -> float | None:
        try:
            t0 = time.perf_counter()
            socket.create_connection((host, 53), timeout=2).close()
            return round((time.perf_counter() - t0) * 1000, 2)
        except Exception:
            return None

    @staticmethod
    def connectivity() -> bool:
        try:
            requests.get('https://www.google.com', timeout=3)
            return True
        except Exception:
            return False

    @staticmethod
    def active_adapters() -> list[str]:
        adapters = []
        for name, stats in psutil.net_if_stats().items():
            if stats.isup:
                adapters.append(name)
        return adapters

    @staticmethod
    def connection_quality(latency_ms: float | None, connected: bool) -> str:
        if not connected:
            return 'offline'
        if latency_ms is None:
            return 'degraded'
        if latency_ms < 80:
            return 'excellent'
        if latency_ms < 180:
            return 'good'
        return 'poor'

    @staticmethod
    def network_usage() -> dict[str, float]:
        io = psutil.net_io_counters()
        return {
            'bytes_sent_mb': round(io.bytes_sent / (1024 * 1024), 2),
            'bytes_recv_mb': round(io.bytes_recv / (1024 * 1024), 2),
        }

    @staticmethod
    def speed_test() -> dict[str, Any]:
        """Lightweight fallback speed test; avoids aggressive traffic if library unavailable."""
        started = time.perf_counter()
        try:
            resp = requests.get('https://speed.hetzner.de/1MB.bin', timeout=8)
            size_bytes = len(resp.content)
            sec = max(0.01, time.perf_counter() - started)
            mbps = round((size_bytes * 8) / (sec * 1_000_000), 2)
            return {'download_mbps_estimate': mbps, 'note': 'Approximate quick test'}
        except Exception:
            return {'download_mbps_estimate': None, 'note': 'Unavailable'}

    @staticmethod
    def discover_local_devices(limit: int = 20) -> list[str]:
        """Safe local discovery using ARP table only (no intrusive scan)."""
        devices: list[str] = []
        try:
            out = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=10).stdout
            for line in out.splitlines():
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+', line)
                if match:
                    ip = match.group(1)
                    try:
                        if ipaddress.ip_address(ip).is_private:
                            devices.append(ip)
                    except ValueError:
                        continue
            uniq = sorted(set(devices))
            return uniq[:limit]
        except Exception:
            return []

    def snapshot(self) -> dict[str, Any]:
        connected = self.connectivity()
        latency = self.ping_latency()
        return {
            'private_ip': self.private_ip(),
            'public_ip': self.public_ip(),
            'gateway': self.gateway_info(),
            'dns': self.dns_info(),
            'wifi': self.wifi_info(),
            'adapters': self.active_adapters(),
            'latency_ms': latency,
            'connected': connected,
            'quality': self.connection_quality(latency, connected),
            'usage': self.network_usage(),
        }
