from __future__ import annotations

import asyncio
import datetime
import random
import re

import wikipedia
from ddgs import DDGS
from core.news import get_latest_info
from core.youtube_controls import next_video, pause_video, resume_video, skip_ad, toggle_mute
from core.youtube_helper import open_youtube, play_youtube
from responses import responses

from jarvis.commands.base import Command
from jarvis.commands.registry import CommandRegistry
from jarvis.core.validators import is_safe_host
from jarvis.services.system_service import local_ip_info, open_application, ping_host, system_snapshot, top_processes, wifi_status


def register_default_commands(registry: CommandRegistry, assistant) -> None:
    async def cmd_time(_: str) -> str:
        return datetime.datetime.now().strftime('The time is %I:%M %p.')

    async def cmd_date(_: str) -> str:
        return datetime.datetime.now().strftime('Today is %A, %d %B %Y.')

    def extract_query_topic(query: str) -> str:
        text = query.lower()
        patterns = [
            r'latest info about',
            r'latest info on',
            r'latest info',
            r'information about',
            r'information on',
            r'info about',
            r'info on',
            r'any info about',
            r'any info on',
            r'news about',
            r'updates on',
            r'update on'
        ]
        for pattern in patterns:
            if pattern in text:
                topic = re.sub(pattern, '', text).strip()
                topic = re.sub(r'\b(on google|on the web|on any platform|google|please|latest|correct|service|platform|site)\b', '', topic).strip()
                return topic or text
        return text

    def search_web_summary(topic: str) -> str | None:
        if not topic:
            return None
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(topic, max_results=1))
            if results:
                return results[0].get('body') or results[0].get('title')
        except Exception:
            return None
        return None

    async def cmd_news(q: str) -> str:
        topic = extract_query_topic(q)
        headlines = get_latest_info(topic)

        if headlines and not any(str(h).startswith('No recent news found') for h in headlines):
            return 'Here are top headlines: ' + ' | '.join(headlines[:5])

        if topic and topic != 'news':
            await assistant.speak(f'Searching the web for {topic}.')
            summary = await asyncio.to_thread(search_web_summary, topic)
            if summary:
                return summary
            try:
                summary = wikipedia.summary(topic, sentences=2)
                return summary
            except Exception:
                pass

        return 'Unable to fetch news right now.'

    async def cmd_open_youtube(_: str) -> str:
        await asyncio.to_thread(open_youtube)
        return 'YouTube opened. Tell me what to play.'

    async def cmd_play(q: str) -> str | None:
        await asyncio.to_thread(play_youtube, q.replace('play', '', 1).strip())
        return None

    async def cmd_app_open(q: str) -> str:
        app_name = q.replace('open ', '', 1).strip()
        return await asyncio.to_thread(open_application, app_name)

    async def cmd_system(_: str) -> str:
        snap = system_snapshot()
        return f"CPU {snap['cpu_percent']} percent, RAM {snap['memory_percent']} percent, Disk {snap['disk_percent']} percent."

    async def cmd_network(_: str) -> str:
        info = local_ip_info()
        net = assistant.network.snapshot()
        return f"Hostname {info['hostname']}, private IP {info['ip_address']}, public IP {net['public_ip']}."

    async def cmd_ping(q: str) -> str:
        target = q.split(maxsplit=1)[1] if len(q.split()) > 1 else '8.8.8.8'
        target = target.strip()
        if not is_safe_host(target):
            return 'Invalid ping target. Please provide a valid host.'
        return await asyncio.to_thread(ping_host, target)

    async def cmd_wifi(_: str) -> str:
        return wifi_status()

    async def cmd_top_proc(_: str) -> str:
        return 'Top CPU processes: ' + '; '.join(top_processes())

    async def cmd_speed(_: str) -> str:
        result = await asyncio.to_thread(assistant.network.speed_test)
        return f"Estimated download speed is {result.get('download_mbps_estimate')} Mbps. {result.get('note')}"

    async def cmd_discover(_: str) -> str:
        devices = await asyncio.to_thread(assistant.network.discover_local_devices)
        return 'Detected local devices: ' + (', '.join(devices) if devices else 'none found')

    async def cmd_security(_: str) -> str:
        sec = await asyncio.to_thread(assistant.security.snapshot)
        return f"Firewall is {sec['firewall']}. Open ports count: {len(sec['open_ports'])}."

    async def cmd_check_password(q: str) -> str:
        pwd = q[len('check password '):]
        result = assistant.security.password_strength(pwd)
        return f"Password strength is {result['level']} with score {result['score']} out of {result['max_score']}."

    async def cmd_nmap(_: str) -> str:
        await assistant.speak('Educational scan starting. Only localhost will be scanned.')
        result = await asyncio.to_thread(assistant.security.localhost_nmap_scan)
        await assistant.emit_security_scan(result)
        return 'Scan completed. Summary sent to dashboard logs.'

    async def cmd_pause(_: str) -> str | None:
        await asyncio.to_thread(pause_video)
        return None

    async def cmd_resume(_: str) -> str | None:
        await asyncio.to_thread(resume_video)
        return None

    async def cmd_skip(_: str) -> str | None:
        await asyncio.to_thread(skip_ad)
        return None

    async def cmd_next(_: str) -> str | None:
        await asyncio.to_thread(next_video)
        return None

    async def cmd_mute(q: str) -> str | None:
        await asyncio.to_thread(toggle_mute, q)
        return None

    async def cmd_exit(_: str) -> str:
        return random.choice(responses['goodbye'])

    registry.register(Command('exit', lambda q: any(w in q for w in ['exit', 'bye', 'quit', 'shutdown']), cmd_exit))
    registry.register(Command('time', lambda q: 'time' in q, cmd_time))
    registry.register(Command('date', lambda q: 'date' in q, cmd_date))
    registry.register(Command('news', lambda q: 'latest news' in q or q == 'news' or 'headlines' in q or 'latest info' in q or 'info about' in q or 'information about' in q or 'info on' in q or 'information on' in q or 'any info' in q, cmd_news))
    registry.register(Command('open_youtube', lambda q: 'open youtube' in q, cmd_open_youtube))
    registry.register(Command('play', lambda q: q.startswith('play '), cmd_play))
    registry.register(Command('pause', lambda q: 'pause' in q, cmd_pause))
    registry.register(Command('resume', lambda q: 'resume' in q, cmd_resume))
    registry.register(Command('skip', lambda q: 'skip ad' in q, cmd_skip))
    registry.register(Command('next', lambda q: 'next video' in q or q == 'next', cmd_next))
    registry.register(Command('mute', lambda q: 'mute' in q, cmd_mute))
    registry.register(Command('open_app', lambda q: q.startswith('open '), cmd_app_open))
    registry.register(Command('system', lambda q: 'system status' in q or 'cpu' in q or 'ram' in q, cmd_system))
    registry.register(Command('network', lambda q: 'ip address' in q or 'network info' in q, cmd_network))
    registry.register(Command('ping', lambda q: q.startswith('ping'), cmd_ping))
    registry.register(Command('wifi', lambda q: 'wifi status' in q, cmd_wifi))
    registry.register(Command('top_process', lambda q: 'top process' in q or 'running process' in q, cmd_top_proc))
    registry.register(Command('speed_test', lambda q: 'speed test' in q or 'internet speed' in q, cmd_speed))
    registry.register(Command('discover', lambda q: 'discover devices' in q or 'local devices' in q, cmd_discover))
    registry.register(Command('security', lambda q: 'security status' in q, cmd_security))
    registry.register(Command('password', lambda q: q.startswith('check password '), cmd_check_password))
    registry.register(Command('nmap', lambda q: 'scan localhost ports' in q or 'nmap localhost' in q, cmd_nmap))
