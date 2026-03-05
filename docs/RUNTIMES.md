# Runtimes: Ollama, LM Studio, and MLX

## Architecture

```
User → VS Code + Continue.dev → [Ollama | LM Studio | MLX] → Local Model
```

Everything runs on your machine. No cloud APIs, no telemetry, no external network calls.

## Which Should You Use?

| Scenario | Recommendation |
|---|---|
| Windows machine | **Ollama** — MLX not available |
| Mac, want simplest setup | **LM Studio** (uses MLX under the hood, zero config) |
| Mac, want best performance | **MLX** via `mlx_lm.server` |
| Cross-platform team (Mac + Windows) | **Ollama** on both — consistent config |
| On-device fine-tuning / LoRA | **MLX** — first-class support |

## Comparison

| | **Ollama** | **LM Studio** | **MLX** |
|---|---|---|---|
| Platform | Windows / Mac / Linux | Windows / Mac | Mac (Apple Silicon) only |
| Setup | One installer + CLI | Download app | Python + server wrapper |
| Continue.dev | Native, 1-click | OpenAI-compatible | OpenAI-compatible |
| Speed on Apple Silicon | Good | Good (uses MLX) | Fastest |
| Speed on Windows/NVIDIA | Excellent | Good | — |
| Model format | GGUF | GGUF | MLX format (HuggingFace) |
| GUI | No | Yes | No |
| On-device LoRA fine-tuning | Limited | No | Built-in |

---

## Ollama (Default)

Runs models via a REST API at `http://localhost:11434`. Cross-platform and plug-and-play.

```bash
# Install
brew install ollama        # macOS
# or download from https://ollama.com

# Run
ollama serve
ollama pull qwen2.5-coder:7b
```

CLI setup uses Ollama by default:

```bash
python -m cli setup
python -m cli verify
```

---

## LM Studio

GUI-based model management with an OpenAI-compatible API at `http://localhost:1234/v1`.

1. Download from https://lmstudio.ai/
2. Search and download a coding model (recommended: `qwen2.5-coder`)
3. Go to **Local Server** tab → load model → **Start Server**

CLI setup with LM Studio:

```bash
python -m cli setup --lmstudio
python -m cli verify --lmstudio
```

Manual `~/.continue/config.json`:

```json
{
  "models": [{
    "title": "Local Coder (LM Studio)",
    "provider": "openai",
    "model": "your-model-name",
    "apiBase": "http://localhost:1234/v1",
    "apiKey": "lm-studio"
  }],
  "allowAnonymousTelemetry": false
}
```

The `apiKey` field is required by the OpenAI provider but ignored by LM Studio.

---

## MLX (Apple Silicon)

Apple's native ML framework. Uses unified memory — CPU and GPU share the same RAM pool with no memory copying. Noticeably faster than Ollama on M-series chips. The M5 is 19–27% faster than M4 (153 GB/s vs 120 GB/s memory bandwidth).

```bash
pip install mlx-lm
mlx_lm.server --model mlx-community/Qwen2.5-Coder-7B-Instruct-4bit
# → http://localhost:8080
```

Point Continue.dev at `http://localhost:8080/v1` by setting `apiBase` in `~/.continue/config.json`. 1,000+ models available via `mlx-community` on HuggingFace.

Or use **LM Studio**, which handles MLX automatically with no extra config.

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Default runtime | Ollama | Cross-platform, easy CLI, active community |
| VS Code extension | Continue.dev | Open-source, native Ollama support |
| Default model | qwen2.5-coder:7b | Best quality/size ratio for coding |
| Security | 3-layer defense | Defense in depth for air-gap guarantee |
