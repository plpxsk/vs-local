"""Tests for cli.ollama module."""

from unittest.mock import patch, MagicMock

from cli.ollama import is_installed, is_running, install_instructions, list_local_models


def test_is_installed_when_present():
    with patch("shutil.which", return_value="/usr/local/bin/ollama"):
        assert is_installed() is True


def test_is_installed_when_missing():
    with patch("shutil.which", return_value=None):
        assert is_installed() is False


def test_is_running_when_up():
    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)

    with patch("urllib.request.urlopen", return_value=mock_resp):
        assert is_running() is True


def test_is_running_when_down():
    with patch("urllib.request.urlopen", side_effect=Exception("connection refused")):
        assert is_running() is False


def test_install_instructions_macos():
    instructions = install_instructions("macos")
    assert "brew install ollama" in instructions


def test_install_instructions_linux():
    instructions = install_instructions("linux")
    assert "curl" in instructions


def test_install_instructions_windows():
    instructions = install_instructions("windows")
    assert "Download" in instructions


def test_list_local_models_when_server_down():
    with patch("urllib.request.urlopen", side_effect=Exception("down")):
        with patch("subprocess.run", side_effect=Exception("no ollama")):
            models = list_local_models()
            assert models == []
