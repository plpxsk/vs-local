"""Model tier definitions."""

from dataclasses import dataclass


@dataclass
class ModelInfo:
    name: str
    size_gb: float
    min_ram_gb: int
    description: str


TIERS: dict[str, ModelInfo] = {
    "small": ModelInfo(
        name="qwen2.5-coder:1.5b",
        size_gb=1.0,
        min_ram_gb=4,
        description="Fast completions, low-end hardware",
    ),
    "medium": ModelInfo(
        name="qwen2.5-coder:7b",
        size_gb=4.5,
        min_ram_gb=8,
        description="Recommended default",
    ),
    "large": ModelInfo(
        name="deepseek-coder-v2:16b",
        size_gb=9.0,
        min_ram_gb=16,
        description="Highest quality",
    ),
}

AUTOCOMPLETE_MODEL = "qwen2.5-coder:1.5b"

DEFAULT_TIER = "medium"


def get_model(tier: str) -> ModelInfo:
    """Get model info for a tier."""
    return TIERS[tier]


def get_all_models() -> dict[str, ModelInfo]:
    """Return all model tiers."""
    return TIERS
