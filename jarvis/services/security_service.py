from __future__ import annotations

import os
import platform
import socket
import subprocess
from typing import Any

import psutil


class SecurityService:
    """Educational and safe local cybersecurity checks."""

    EDUCATIONAL_WARNING = (
        'For authorized educational use only. Scan only localhost or approved local devices.'
    )

    @staticmethod
    def firewall_status() -> str:
        try:
            if platform.system().lower().startswith('win'):
                out = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], capture_output=True, text=True, timeout=12).stdout
                if 'State ON' in out:
                    return 'enabled'
                if 'State OFF' in out:
                    return 'disabled'
            return 'unknown'
        except Exception:
            return 'unknown'

    @staticmethod
    def local_open_ports(max_ports: int = 30) -> list[int]:
        ports = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == psutil.CONN_LISTEN and conn.laddr:
                ports.append(conn.laddr.port)
        return sorted(set(ports))[:max_ports]

    @staticmethod
    def suspicious_processes() -> list[str]:
        alerts = []
        suspect_keywords = ['keylogger', 'miner', 'mimikatz', 'nc.exe', 'netcat']
        for p in psutil.process_iter(['name', 'exe', 'cpu_percent']):
            name = (p.info.get('name') or '').lower()
            exe = (p.info.get('exe') or '').lower()
            if any(k in name or k in exe for k in suspect_keywords):
                alerts.append(f"{p.info.get('name', 'unknown')} ({p.info.get('cpu_percent', 0)}% CPU)")
        return alerts

    @staticmethod
    def password_strength(password: str) -> dict[str, Any]:
        score = 0
        if len(password) >= 12:
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(not c.isalnum() for c in password):
            score += 1
        level = 'weak' if score < 3 else 'moderate' if score < 5 else 'strong'
        return {'score': score, 'level': level, 'max_score': 5}

    @staticmethod
    def security_tips() -> list[str]:
        return [
            'Keep OS and browser updated weekly.',
            'Use unique passwords and enable MFA.',
            'Avoid running unknown executables as administrator.',
            'Review open ports and disable unnecessary services.',
            'Backup critical files regularly.',
        ]

    @staticmethod
    def localhost_nmap_scan() -> str:
        try:
            cmd = ['nmap', '-Pn', '127.0.0.1']
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if out.returncode == 0 and out.stdout:
                return out.stdout[:4000]
            return 'Nmap completed with no readable output.'
        except FileNotFoundError:
            return 'Nmap is not installed. Install Nmap to enable this feature.'
        except Exception:
            return 'Nmap scan failed.'

    def snapshot(self) -> dict[str, Any]:
        return {
            'warning': self.EDUCATIONAL_WARNING,
            'firewall': self.firewall_status(),
            'open_ports': self.local_open_ports(),
            'suspicious_processes': self.suspicious_processes(),
            'tips': self.security_tips(),
        }
