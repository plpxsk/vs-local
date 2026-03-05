#!/usr/bin/env python3
"""Standalone network audit script. Run independently to verify no external calls."""

import socket
import subprocess
import sys
import platform


TELEMETRY_HOSTS = [
    "telemetry.continue.dev",
    "update.continue.dev",
    "stats.ollama.com",
    "registry.ollama.com",
    "api.openai.com",
    "api.anthropic.com",
]

LLM_PROCESS_NAMES = ["ollama", "lmstudio", "lm studio", "lm-studio"]


def check_dns_telemetry() -> list[str]:
    """Check which telemetry endpoints resolve."""
    reachable = []
    for host in TELEMETRY_HOSTS:
        try:
            socket.setdefaulttimeout(3)
            socket.getaddrinfo(host, 443)
            reachable.append(host)
        except (socket.gaierror, socket.timeout, OSError):
            pass
    return reachable


def check_outbound_connections() -> list[str]:
    """Check for non-localhost outbound connections from LLM processes."""
    system = platform.system().lower()
    concerns = []

    try:
        if system in ("darwin", "linux"):
            result = subprocess.run(
                ["lsof", "-i", "-n", "-P"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            for line in result.stdout.splitlines():
                lower = line.lower()
                if any(name in lower for name in LLM_PROCESS_NAMES):
                    # Flag non-localhost connections
                    if "ESTABLISHED" in line or "LISTEN" in line:
                        if "127.0.0.1" not in line and "localhost" not in lower and "[::1]" not in line:
                            concerns.append(line.strip())
        elif system == "windows":
            result = subprocess.run(
                ["netstat", "-b", "-n"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            lines = result.stdout.splitlines()
            for i, line in enumerate(lines):
                lower = line.lower()
                if any(name in lower for name in LLM_PROCESS_NAMES):
                    if i > 0 and "127.0.0.1" not in lines[i - 1]:
                        concerns.append(lines[i - 1].strip() + " " + line.strip())
    except Exception as e:
        concerns.append(f"Could not check connections: {e}")

    return concerns


def main():
    print("=" * 60)
    print("  Network Audit: On-Device LLM")
    print("=" * 60)
    all_ok = True

    # DNS check
    print("\n[1] Checking telemetry DNS resolution...")
    reachable = check_dns_telemetry()
    if reachable:
        all_ok = False
        print(f"  WARNING: These telemetry hosts are reachable:")
        for h in reachable:
            print(f"    - {h}")
        print("  Consider applying firewall rules from security/")
    else:
        print("  OK: No telemetry hosts reachable")

    # Outbound connections
    print("\n[2] Checking outbound connections from LLM processes...")
    concerns = check_outbound_connections()
    if concerns:
        all_ok = False
        print(f"  WARNING: Non-localhost connections detected:")
        for c in concerns:
            print(f"    {c}")
    else:
        print("  OK: No external connections detected")

    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("  RESULT: All checks passed. No external network calls detected.")
    else:
        print("  RESULT: Warnings found. Review above and apply firewall rules.")
    print("=" * 60)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
