#!/bin/bash
# Linux iptables rules for on-device LLM
# Block all outbound traffic for Ollama/LM Studio except localhost
#
# Usage: sudo bash iptables_rules.sh

set -e

echo "Applying on-device LLM firewall rules..."

# Allow localhost traffic for Ollama
iptables -A OUTPUT -o lo -p tcp --dport 11434 -j ACCEPT
iptables -A OUTPUT -o lo -p tcp --dport 1234 -j ACCEPT

# Get Ollama user ID (if running as dedicated user)
OLLAMA_UID=$(id -u ollama 2>/dev/null || echo "")

if [ -n "$OLLAMA_UID" ]; then
    # Block all other outbound for Ollama user
    iptables -A OUTPUT -m owner --uid-owner "$OLLAMA_UID" -j DROP
    echo "Blocked outbound for ollama user (UID: $OLLAMA_UID)"
else
    echo "Note: Ollama user not found. If Ollama runs as your user,"
    echo "consider creating a dedicated 'ollama' user or using the"
    echo "process-based rules below."
fi

# Alternative: block by process name using cgroups (requires cgroupsv2)
# If using systemd, you can restrict in the service file:
#   [Service]
#   IPAddressAllow=localhost
#   IPAddressDeny=any

echo "Firewall rules applied."
echo "To persist: run 'iptables-save > /etc/iptables/rules.v4'"
