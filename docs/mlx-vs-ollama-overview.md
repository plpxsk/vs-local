# MLX vs Ollama: Quick Reference

## Which Should You Use?

| Scenario | Recommendation |
|---|---|
| Windows machine | **Ollama** — MLX not available |
| Mac, want simplest setup | **LM Studio** (uses MLX under the hood, zero config) |
| Mac, want best performance | **MLX** via `mlx_lm.server` or `mlx-openai-server` |
| Cross-platform team (Mac + Windows) | **Ollama** on both — consistent config |
| On-device fine-tuning / LoRA | **MLX** — first-class support |

---

## Key Difference

Ollama runs on **GGUF** via llama.cpp — cross-platform, plug-and-play. MLX is Apple's native ML framework that exploits **unified memory** on Apple Silicon, where CPU and GPU share the same RAM pool. No memory copying = faster inference. A Mac with 96GB unified memory can run models that would otherwise need an expensive NVIDIA GPU.

On M-series chips, MLX is noticeably faster than Ollama for the same model. The M5 provides a 19–27% boost over M4 due to higher memory bandwidth (153 GB/s vs 120 GB/s).

---

## Comparison Table

| | **Ollama** | **MLX** |
|---|---|---|
| Platform | Windows / Mac / Linux | Mac (Apple Silicon) only |
| Setup | One installer | Python + server wrapper |
| Continue.dev | Native, 1-click | Via OpenAI-compatible server |
| Speed on Apple Silicon | Good | Faster |
| Speed on Windows/NVIDIA | Excellent | ❌ |
| Model library | Very large | 1,000+ via `mlx-community` on HuggingFace |
| On-device LoRA fine-tuning | Limited | ✅ Built-in |
| MLflow compatibility | ✅ | ✅ |

---

## Connecting MLX to Continue.dev

MLX needs a server wrapper to expose an OpenAI-compatible API:

```bash
pip install mlx-lm
mlx_lm.server --model mlx-community/Qwen2.5-Coder-7B-Instruct-4bit
# → http://localhost:8080
```

Then in Continue.dev `config.json` point `apiBase` at `http://localhost:8080/v1`. For more features (multi-model, speculative decoding), use `mlx-openai-server` instead. Or just use **LM Studio**, which handles all of this automatically.

---

## MLflow

Works identically regardless of backend — MLflow only cares about your experiment logging code, not what's serving the model.

> See also: `local-llm-models-summary.md` for model tiers, VRAM requirements, and pull commands.
