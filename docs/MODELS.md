# Model Guide

## Recommended Tiers

| Tier | Model | Download Size | RAM Required | Best For |
|------|-------|--------------|-------------|----------|
| small | `qwen2.5-coder:1.5b` | ~1 GB | 4 GB | Fast completions, low-end hardware |
| medium | `qwen2.5-coder:7b` | ~4.5 GB | 8 GB | **Recommended default** |
| large | `deepseek-coder-v2:16b` | ~9 GB | 16 GB | Highest quality |

The `setup` command auto-detects your RAM and recommends a tier. Override with `--tier`:

```bash
python -m cli setup --tier small
```

## Chat vs Autocomplete

The default config uses two models:
- **Chat model** (`qwen2.5-coder:7b`) — For chat, inline edits, code review
- **Autocomplete model** (`qwen2.5-coder:1.5b`) — For fast tab completions

## Managing Models

```bash
python -m cli models                           # List tiers and local models
python -m cli models --pull qwen2.5-coder:7b   # Pull a model
ollama list                                    # List local models
ollama rm qwen2.5-coder:1.5b                   # Remove a model
```

After pulling a new model, update your config:

```bash
python -m cli config --model <model-name>
```

Or edit `~/.continue/config.json` directly.

---

## Hardware Quick-Reference

| Model | RAM Needed | Best For |
|---|---|---|
| Llama 3.2 3B | ~3 GB | Ultra-light, fast autocomplete |
| Qwen2.5-Coder 7B | ~6 GB | Best coding/RAM ratio |
| Mistral NeMo 12B | ~8 GB | Balanced everyday coding, 128k context |
| StarCoder2 15B | ~10 GB | Code-only, fine-tuning |
| Mistral Small 3 24B | ~14 GB | High quality, single GPU |
| Codestral 22B | ~14 GB | Code specialist, long context |
| Qwen3-Coder 30B MoE | ~20 GB | Repo-level, agentic tasks |
| Qwen2.5-Coder 32B | ~22 GB | Near-GPT-4 quality local |

> **Recommended starting point:** Qwen2.5-Coder 7B for most machines.

---

## Top Coding Models

### Qwen2.5-Coder (7B / 14B / 32B)
The current gold standard for on-device coding. The 7B runs comfortably on 8 GB RAM. The 32B rivals closed-source leaders (91.0% HumanEval, matching GPT-4o).

```bash
ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-coder:32b  # if you have the RAM
```

### Qwen3-Coder (30B A3B — MoE)
Mixture-of-Experts: 30B total params, only 3B active per token. Excels at multi-file reasoning and agentic workflows.

```bash
ollama pull qwen3-coder:30b
```

### Codestral 22B
Mistral's dedicated code model — fast, long context (32K), permissive license.

```bash
ollama pull codestral
```

### DeepSeek-Coder-V2 (Lite / 16B)
Multilingual, strong at repo-level tasks with a large community.

```bash
ollama pull deepseek-coder-v2
```

### Mistral NeMo (12B)
128k context window, Apache 2.0, good for long-context and hardware-constrained setups.

```bash
ollama pull mistral-nemo
```

### GPT-OSS 20B (OpenAI open weights)
Apache 2.0, strong reasoning, works on Ollama / LM Studio / Apple Metal.

```bash
ollama pull gpt-oss:20b
```

### Google Gemma 3 (4B / 12B)
Good instruction following and coding on Apple Silicon, well-maintained by Google.

```bash
ollama pull gemma3:12b
```

---

## Hardware Tips

- **Apple Silicon (M1–M5):** GPU acceleration is automatic. For best speed, use MLX — see [RUNTIMES.md](RUNTIMES.md).
- **NVIDIA GPU:** Ollama uses CUDA automatically. 16B models are feasible with 8 GB+ VRAM.
- **CPU only:** Stick with the small tier. Slower but functional.
