"""Firewall rule information and generation."""

from pathlib import Path

from cli.detect import get_os

SECURITY_DIR = Path(__file__).parent.parent / "security"


def get_firewall_info() -> str:
    """Return firewall setup instructions for the current OS."""
    os_name = get_os()
    if os_name == "macos":
        rules_file = SECURITY_DIR / "pf_rules.conf"
        return (
            f"macOS pf firewall rules are available at:\n"
            f"  {rules_file}\n\n"
            f"To apply:\n"
            f"  sudo cp {rules_file} /etc/pf.anchors/on-device\n"
            f"  sudo pfctl -f /etc/pf.conf\n"
            f"  sudo pfctl -e\n\n"
            f"This blocks all outbound traffic for Ollama/LM Studio except localhost."
        )
    elif os_name == "linux":
        rules_file = SECURITY_DIR / "iptables_rules.sh"
        return (
            f"Linux iptables rules are available at:\n"
            f"  {rules_file}\n\n"
            f"To apply:\n"
            f"  sudo bash {rules_file}\n\n"
            f"This blocks all outbound traffic for Ollama/LM Studio except localhost."
        )
    elif os_name == "windows":
        rules_file = SECURITY_DIR / "windows_firewall.ps1"
        return (
            f"Windows Firewall rules are available at:\n"
            f"  {rules_file}\n\n"
            f"To apply (PowerShell as Administrator):\n"
            f"  .\\{rules_file}\n\n"
            f"This blocks all outbound traffic for Ollama/LM Studio except localhost."
        )
    return "No firewall template available for this OS."
