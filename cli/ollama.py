"""Ollama installation, health check, and model management."""

import shutil
import subprocess
import json
import urllib.request
import urllib.error

OLLAMA_BASE = "http://localhost:11434"


def is_installed() -> bool:
    """Check if Ollama is installed."""
    return shutil.which("ollama") is not None


def is_running() -> bool:
    """Check if Ollama server is responding."""
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


def install_instructions(os_name: str) -> str:
    """Return installation instructions for the given OS."""
    if os_name == "macos":
        return (
            "Install Ollama:\n"
            "  brew install ollama\n"
            "  OR download from https://ollama.com/download/mac"
        )
    if os_name == "linux":
        return (
            "Install Ollama:\n"
            "  curl -fsSL https://ollama.com/install.sh | sh"
        )
    if os_name == "windows":
        return (
            "Install Ollama:\n"
            "  Download from https://ollama.com/download/windows"
        )
    return "Visit https://ollama.com/download for installation instructions."


def start_server() -> subprocess.Popen | None:
    """Start Ollama server in the background. Returns the process or None."""
    try:
        proc = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Wait briefly for startup
        import time

        for _ in range(10):
            time.sleep(1)
            if is_running():
                return proc
        return proc
    except Exception:
        return None


def pull_model(model_name: str) -> bool:
    """Pull a model. Returns True on success."""
    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            check=True,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def list_local_models() -> list[str]:
    """List locally available models."""
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        # Fallback to CLI
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                check=True,
            )
            models = []
            for line in result.stdout.strip().splitlines()[1:]:
                parts = line.split()
                if parts:
                    models.append(parts[0])
            return models
        except Exception:
            return []


def test_inference(model_name: str) -> str | None:
    """Run a quick test inference. Returns the response text or None on failure."""
    try:
        payload = json.dumps(
            {
                "model": model_name,
                "prompt": "Write a Python function that returns 'hello world'.",
                "stream": False,
            }
        ).encode()
        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data.get("response")
    except Exception as e:
        return None
