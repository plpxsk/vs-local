# Security Guide

This project guarantees **zero external network calls**. All AI inference runs locally.

## Three Security Layers

### Layer 1: Application Configuration

All config files lock API endpoints to localhost:
- Ollama: `http://localhost:11434`
- LM Studio: `http://localhost:1234/v1`

Telemetry is disabled:
- Continue.dev: `"allowAnonymousTelemetry": false`
- VS Code: `"telemetry.telemetryLevel": "off"`
- VS Code: `"http.proxySupport": "off"`

These are set automatically by `python -m cli setup`.

### Layer 2: Network Verification

Run the audit:
```bash
python -m cli verify
```

This checks:
1. **Runtime health** - Ollama/LM Studio is running on localhost
2. **Model availability** - Expected model is loaded
3. **Inference test** - Model produces output
4. **DNS audit** - Known telemetry endpoints are not reachable
5. **Connection audit** - LLM processes only have localhost connections

Standalone network audit:
```bash
python security/verify_no_network.py
```

### Layer 3: OS Firewall Rules

For maximum security, apply OS firewall rules that block outbound traffic for LLM processes.

**These are not auto-applied.** Review and apply manually:

```bash
# Show instructions for your OS
python -m cli firewall
```

#### macOS (pf)
```bash
sudo cp security/pf_rules.conf /etc/pf.anchors/on-device
# Add anchor to /etc/pf.conf, then:
sudo pfctl -f /etc/pf.conf
sudo pfctl -e
```

#### Linux (iptables)
```bash
sudo bash security/iptables_rules.sh
```

#### Windows (PowerShell as Admin)
```powershell
.\security\windows_firewall.ps1
```

## What Gets Blocked

The firewall rules block all outbound traffic for Ollama and LM Studio processes except connections to `127.0.0.1`. This prevents:

- Model telemetry
- Update checks
- Any accidental external API calls
- Data exfiltration

## Verification Checklist

1. Run `python -m cli verify` - all checks should pass
2. Run `python security/verify_no_network.py` - standalone audit
3. Apply firewall rules for your OS
4. Confirm VS Code telemetry is off (check `.vscode/settings.json`)
5. Confirm Continue.dev telemetry is off (check `config/continue/config.json`)
