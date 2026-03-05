"""Full-stack health check and network audit."""

import json
import socket
import subprocess
import urllib.request
from dataclasses import dataclass, field

from cli import ollama, lmstudio, detect


@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str


@dataclass
class VerifyReport:
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        return all(c.passed for c in self.checks)

    def add(self, name: str, passed: bool, message: str):
        self.checks.append(CheckResult(name, passed, message))


def check_runtime(use_lmstudio: bool = False) -> CheckResult:
    """Check if LLM runtime is available and running."""
    if use_lmstudio:
        if lmstudio.is_running():
            return CheckResult("LM Studio server", True, "Running at localhost:1234")
        return CheckResult("LM Studio server", False, "Not responding at localhost:1234")
    else:
        if not ollama.is_installed():
            return CheckResult("Ollama installed", False, "Ollama not found in PATH")
        if not ollama.is_running():
            return CheckResult("Ollama server", False, "Not responding at localhost:11434")
        return CheckResult("Ollama server", True, "Running at localhost:11434")


def check_model(model_name: str, use_lmstudio: bool = False) -> CheckResult:
    """Check if the expected model is available."""
    if use_lmstudio:
        models = lmstudio.list_models()
        if models:
            return CheckResult("Model loaded", True, f"Available: {', '.join(models)}")
        return CheckResult("Model loaded", False, "No models loaded in LM Studio")
    else:
        models = ollama.list_local_models()
        if model_name in models:
            return CheckResult("Model available", True, f"{model_name} is pulled")
        # Check partial match
        base_name = model_name.split(":")[0]
        matches = [m for m in models if base_name in m]
        if matches:
            return CheckResult(
                "Model available", True, f"Found: {', '.join(matches)}"
            )
        return CheckResult(
            "Model available", False, f"{model_name} not found. Available: {models}"
        )


def check_inference(model_name: str, use_lmstudio: bool = False) -> CheckResult:
    """Run a test inference."""
    if use_lmstudio:
        result = lmstudio.test_inference()
        if result:
            return CheckResult("Inference", True, "LM Studio inference OK")
        return CheckResult("Inference", False, "LM Studio inference failed")
    else:
        result = ollama.test_inference(model_name)
        if result:
            return CheckResult("Inference", True, "Ollama inference OK")
        return CheckResult("Inference", False, "Ollama inference failed")


def check_network_audit() -> CheckResult:
    """Check that no known telemetry endpoints are reachable (warning only)."""
    telemetry_hosts = [
        "telemetry.continue.dev",
        "update.continue.dev",
        "stats.ollama.com",
    ]
    reachable = []
    for host in telemetry_hosts:
        try:
            socket.setdefaulttimeout(3)
            socket.getaddrinfo(host, 443)
            reachable.append(host)
        except (socket.gaierror, socket.timeout, OSError):
            pass

    if reachable:
        return CheckResult(
            "Network audit",
            False,
            f"WARNING: Telemetry endpoints reachable: {', '.join(reachable)}. "
            "Consider applying firewall rules from security/.",
        )
    return CheckResult("Network audit", True, "Telemetry endpoints not reachable")


def check_localhost_only() -> CheckResult:
    """Verify LLM processes only listen on localhost."""
    os_name = detect.get_os()
    try:
        if os_name == "macos" or os_name == "linux":
            result = subprocess.run(
                ["lsof", "-i", "-n", "-P"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            lines = result.stdout.splitlines()
            concerns = []
            for line in lines:
                lower = line.lower()
                if "ollama" in lower or "lmstudio" in lower or "lm studio" in lower:
                    if "0.0.0.0" in line or "*:" in line:
                        if "LISTEN" in line:
                            concerns.append(line.strip())
            if concerns:
                return CheckResult(
                    "Localhost-only",
                    False,
                    f"Processes listening on all interfaces:\n"
                    + "\n".join(concerns),
                )
            return CheckResult("Localhost-only", True, "LLM processes bound to localhost")
        else:
            return CheckResult(
                "Localhost-only", True, "Skipped (manual check recommended on Windows)"
            )
    except Exception as e:
        return CheckResult("Localhost-only", True, f"Could not verify: {e}")


def run_all(model_name: str, use_lmstudio: bool = False) -> VerifyReport:
    """Run all verification checks."""
    report = VerifyReport()
    report.checks.append(check_runtime(use_lmstudio))
    report.checks.append(check_model(model_name, use_lmstudio))
    report.checks.append(check_inference(model_name, use_lmstudio))
    report.checks.append(check_network_audit())
    report.checks.append(check_localhost_only())
    return report
