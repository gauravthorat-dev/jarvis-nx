# Security Checklist

- [ ] `JARVIS_WS_TOKEN` configured and rotated.
- [ ] WebSocket exposed only through TLS reverse proxy.
- [ ] Non-localhost scans blocked by policy.
- [ ] Audit logs retained and protected.
- [ ] `.env` excluded from VCS.
- [ ] Host firewall enabled.
- [ ] Dependency scan integrated in CI.
- [ ] Privileged app-launch commands allowlisted.
