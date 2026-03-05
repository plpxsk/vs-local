"""Tests for cli.detect module."""

from cli.detect import get_os, get_ram_gb, recommend_tier


def test_get_os_returns_known_value():
    os_name = get_os()
    assert os_name in ("macos", "linux", "windows")


def test_get_ram_gb_returns_positive():
    ram = get_ram_gb()
    assert ram > 0


def test_recommend_tier_small():
    assert recommend_tier(3.0) == "small"
    assert recommend_tier(4.0) == "small"


def test_recommend_tier_medium():
    assert recommend_tier(8.0) == "medium"
    assert recommend_tier(12.0) == "medium"


def test_recommend_tier_large():
    assert recommend_tier(16.0) == "large"
    assert recommend_tier(32.0) == "large"
