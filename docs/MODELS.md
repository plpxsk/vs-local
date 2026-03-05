# Model Guide

## Recommended Tiers

| Tier | Model | Download Size | RAM Required | Speed | Quality |
|------|-------|--------------|-------------|-------|---------|
| small | `qwen2.5-coder:1.5b` | ~1 GB | 4 GB | Fast | Good for completions |
| medium | `qwen2.5-coder:7b` | ~4.5 GB | 8 GB | Moderate | **Recommended** |
| large | `deepseek-coder-v2:16b` | ~9 GB | 16 GB | Slower | Best quality |

## Auto-Detection

The `setup` command automatically detects your RAM and recommends a tier:

- **16 GB+** -> large tier
- **8-16 GB** -> medium tier (default)
- **< 8 GB** -> small tier

Override with `--tier`:
```bash
python -m cli setup --tier small
```

## Chat vs Autocomplete

The default config uses two models:
- **Chat model** (`qwen2.5-coder:7b`) - For chat, inline edits, code review
- **Autocomplete model** (`qwen2.5-coder:1.5b`) - For fast tab completions

The smaller autocomplete model provides faster responses for the frequent, short completions during typing.

## Managing Models

```bash
# List available tiers and local models
python -m cli models

# Pull a specific model
python -m cli models --pull qwen2.5-coder:7b

# Pull directly with Ollama
ollama pull qwen2.5-coder:7b

# List all local models
ollama list

# Remove a model
ollama rm qwen2.5-coder:1.5b
```

## Using Different Models

After pulling a model, update your config:
```bash
python -m cli config --model <model-name>
```

Or edit `~/.continue/config.json` directly.

## Hardware Tips

- **Apple Silicon (M1/M2/M3/M4)**: Models run on the GPU automatically. 7B models work well.
- **NVIDIA GPU**: Ollama uses CUDA automatically if available. 16B models feasible with 8 GB+ VRAM.
- **CPU only**: Stick with the small tier (1.5B). Inference will be slower but functional.
- **RAM**: The model must fit in memory. 7B models need ~4.5 GB, so 8 GB system RAM is the practical minimum.
