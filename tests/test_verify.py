"""Tests for cli.verify module."""

from unittest.mock import patch, MagicMock
import socket

from cli.verify import (
    check_runtime,
    check_model,
    check_network_audit,
    run_all,
    VerifyReport,
    CheckResult,
)


def test_check_runtime_ollama_running():
    with patch("cli.ollama.is_installed", return_value=True):
        with patch("cli.ollama.is_running", return_value=True):
            result = check_runtime(use_lmstudio=False)
            assert result.passed is True


def test_check_runtime_ollama_not_installed():
    with patch("cli.ollama.is_installed", return_value=False):
        result = check_runtime(use_lmstudio=False)
        assert result.passed is False


def test_check_runtime_lmstudio_running():
    with patch("cli.lmstudio.is_running", return_value=True):
        result = check_runtime(use_lmstudio=True)
        assert result.passed is True


def test_check_runtime_lmstudio_not_running():
    with patch("cli.lmstudio.is_running", return_value=False):
        result = check_runtime(use_lmstudio=True)
        assert result.passed is False


def test_check_model_found():
    with patch("cli.ollama.list_local_models", return_value=["qwen2.5-coder:7b"]):
        result = check_model("qwen2.5-coder:7b")
        assert result.passed is True


def test_check_model_not_found():
    with patch("cli.ollama.list_local_models", return_value=[]):
        result = check_model("qwen2.5-coder:7b")
        assert result.passed is False


def test_check_network_audit_clean():
    with patch("socket.getaddrinfo", side_effect=socket.gaierror("not found")):
        result = check_network_audit()
        assert result.passed is True


def test_check_network_audit_telemetry_reachable():
    with patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("1.2.3.4", 443))]):
        result = check_network_audit()
        assert result.passed is False
        assert "reachable" in result.message


def test_verify_report_all_passed():
    report = VerifyReport()
    report.add("test1", True, "ok")
    report.add("test2", True, "ok")
    assert report.all_passed is True


def test_verify_report_some_failed():
    report = VerifyReport()
    report.add("test1", True, "ok")
    report.add("test2", False, "fail")
    assert report.all_passed is False
