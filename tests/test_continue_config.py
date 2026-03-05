"""Tests for cli.continue_config module."""

import json
import tempfile
from pathlib import Path

from cli.continue_config import generate_config, write_config


def test_generate_config_ollama():
    config = generate_config("qwen2.5-coder:7b", provider="ollama")
    assert config["models"][0]["provider"] == "ollama"
    assert config["models"][0]["model"] == "qwen2.5-coder:7b"
    assert config["models"][0]["apiBase"] == "http://localhost:11434"
    assert config["tabAutocompleteModel"]["provider"] == "ollama"
    assert config["allowAnonymousTelemetry"] is False


def test_generate_config_lmstudio():
    config = generate_config("ignored", provider="lmstudio")
    assert config["models"][0]["provider"] == "lmstudio"
    assert config["models"][0]["model"] == "AUTODETECT"
    assert config["tabAutocompleteModel"]["provider"] == "lmstudio"
    assert config["tabAutocompleteModel"]["model"] == "AUTODETECT"
    assert config["allowAnonymousTelemetry"] is False


def test_generate_config_custom_api_base():
    config = generate_config("test-model", api_base="http://localhost:9999")
    assert config["models"][0]["apiBase"] == "http://localhost:9999"


def test_generate_config_localhost_only():
    """Verify ollama API base points to localhost."""
    config = generate_config("test-model", provider="ollama")
    for model in config["models"]:
        assert "localhost" in model["apiBase"]
    assert "localhost" in config["tabAutocompleteModel"]["apiBase"]


def test_write_config():
    config = generate_config("qwen2.5-coder:7b")
    with tempfile.TemporaryDirectory() as tmpdir:
        path = write_config(config, output_dir=tmpdir)
        assert path.exists()
        loaded = json.loads(path.read_text())
        assert loaded == config
