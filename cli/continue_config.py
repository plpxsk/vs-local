"""Generate Continue.dev configuration locked to localhost."""

import json
from pathlib import Path

from cli.models import AUTOCOMPLETE_MODEL


def generate_config(
    model_name: str,
    provider: str = "ollama",
    api_base: str | None = None,
) -> dict:
    """Generate a Continue.dev config dict."""
    if provider == "ollama":
        base = api_base or "http://localhost:11434"
        return {
            "models": [
                {
                    "title": "Local Coder",
                    "provider": "ollama",
                    "model": model_name,
                    "apiBase": base,
                }
            ],
            "tabAutocompleteModel": {
                "title": "Local Autocomplete",
                "provider": "ollama",
                "model": AUTOCOMPLETE_MODEL,
                "apiBase": base,
            },
            "allowAnonymousTelemetry": False,
        }
    else:
        # Use Continue.dev's native lmstudio provider — it queries /v1/models at
        # runtime to detect whichever model is currently loaded in LM Studio.
        return {
            "models": [
                {
                    "title": "Local Coder (LM Studio)",
                    "provider": "lmstudio",
                    "model": "AUTODETECT",
                }
            ],
            "tabAutocompleteModel": {
                "title": "Local Autocomplete (LM Studio)",
                "provider": "lmstudio",
                "model": "AUTODETECT",
            },
            "allowAnonymousTelemetry": False,
        }


def write_config(config: dict, output_dir: str | None = None) -> Path:
    """Write config to the repo's config/continue/ directory."""
    if output_dir:
        config_dir = Path(output_dir)
    else:
        config_dir = Path(__file__).parent.parent / "config" / "continue"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    return config_path


def install_to_home(config: dict, overwrite: bool = False) -> Path | None:
    """Install config to the user's Continue.dev config directory.

    If overwrite is False and ~/.continue/config.json already exists, does nothing
    and returns None (caller should prompt and pass overwrite=True to replace).
    When overwriting, the existing file is backed up to config.json.backup.
    """
    home = Path.home()
    continue_dir = home / ".continue"
    continue_dir.mkdir(parents=True, exist_ok=True)
    config_path = continue_dir / "config.json"

    if config_path.exists() and not overwrite:
        return None

    # Back up existing config before overwriting
    if config_path.exists():
        backup = continue_dir / "config.json.backup"
        config_path.rename(backup)

    config_path.write_text(json.dumps(config, indent=2) + "\n")
    return config_path
