"""LM Studio alternative runtime support."""

import json
import urllib.request
import urllib.error

LMSTUDIO_BASE = "http://localhost:1234/v1"


def is_running() -> bool:
    """Check if LM Studio server is responding."""
    try:
        req = urllib.request.Request(f"{LMSTUDIO_BASE}/models")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


def install_instructions() -> str:
    """Return LM Studio installation instructions."""
    return (
        "Install LM Studio:\n"
        "  1. Download from https://lmstudio.ai/\n"
        "  2. Install and open LM Studio\n"
        "  3. Download a coding model (search for 'qwen2.5-coder')\n"
        "  4. Go to Local Server tab and click 'Start Server'\n"
        "  5. Server runs at http://localhost:1234/v1"
    )


def list_models() -> list[str]:
    """List models loaded in LM Studio."""
    try:
        req = urllib.request.Request(f"{LMSTUDIO_BASE}/models")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return [m["id"] for m in data.get("data", [])]
    except Exception:
        return []


def test_inference(model_name: str | None = None) -> str | None:
    """Run a test inference against LM Studio."""
    try:
        models = list_models()
        if not models:
            return None
        model = model_name or models[0]

        payload = json.dumps(
            {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Write a Python function that returns 'hello world'.",
                    }
                ],
                "max_tokens": 200,
            }
        ).encode()
        req = urllib.request.Request(
            f"{LMSTUDIO_BASE}/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except Exception:
        return None
