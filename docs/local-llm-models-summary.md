# Local LLM Models for On-Device Dev (Ollama + Continue.dev + MLflow)

## 🏆 Top Coding Models

### 1. Qwen2.5-Coder (7B / 14B / 32B)
The current gold standard for on-device coding. The 32B model rivals closed-source leaders with 91.0% on HumanEval (matching GPT-4o) and 73.7% on Aider code repair. The 7B version runs comfortably on 8GB VRAM and is still very capable for everyday dev work.

```bash
ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-coder:32b  # if you have the VRAM
```

**Best for:** Everyday coding assistance, autocomplete, multi-language support.

---

### 2. Qwen3-Coder (30B A3B — MoE)
A Mixture-of-Experts model with 30 billion total parameters but only 3 billion active per token, delivering coding performance competitive with much larger dense models. Excels at multi-step code reasoning, multi-file program analysis, and tool-augmented development workflows.

```bash
ollama pull qwen3-coder:30b
```

**Best for:** Repo-level tasks, agentic coding, complex refactors.

---

### 3. Codestral 22B
A sweet spot for quality + latency + context (32K). Mistral's dedicated code model — faster than general-purpose models of the same size for coding tasks, permissive license for local use.

```bash
ollama pull codestral
```

**Best for:** Code generation, long context, speed-sensitive workflows.

---

### 4. DeepSeek-Coder-V2 (Lite / 16B)
A multilingual code model family built for repo-level tasks with strong open tooling and a large community. The Lite variant runs well on modest hardware.

```bash
ollama pull deepseek-coder-v2
```

**Best for:** Multi-language projects, repo-level understanding.

---

## 🇪🇺 Mistral Picks

### Mistral NeMo (12B)
Built in collaboration with NVIDIA, offering a context window of up to 128k tokens with state-of-the-art reasoning and coding accuracy in its size class. Apache 2.0 licensed (fully open), trained with quantization awareness for FP8 inference without performance loss.

```bash
ollama pull mistral-nemo
```

**VRAM:** ~8GB at Q4 | **Context:** 128k tokens | **License:** Apache 2.0

**Best for:** Balanced everyday coding, long context, hardware-constrained setups.

---

### Mistral Small 3 (24B)
Sets a new benchmark in the sub-70B category — "knowledge-dense," fitting in a single RTX 4090 or a 32GB RAM MacBook once quantized. Competitive with models 3x its size on code, math, and instruction following.

```bash
ollama pull mistral-small
```

**VRAM:** ~14–16GB at Q4 | **License:** Apache 2.0

**Best for:** High-quality output when you have the GPU headroom.

---

## 🔓 Other Notable Open Source

### Meta Llama 3.2 (1B / 3B) — Ultra Lightweight
The 1B model requires only ~2GB of memory; the 3B requires ~6GB. Well within reach of modern laptops without a dedicated GPU. Not coding-specialized but great for fast autocomplete on minimal hardware.

```bash
ollama pull llama3.2:3b
```

---

### StarCoder2 (3B / 7B / 15B)
Open, well-documented, and popular for fine-tuning and IDE tooling. Built specifically for code with a strong community and direct Continue.dev integration.

```bash
ollama pull starcoder2:7b
```

---

### GPT-OSS 20B (OpenAI open weights)
OpenAI's open-weight reasoning and coding model released under Apache 2.0. Strong reasoning for the size, works across Ollama, LM Studio, and Apple Metal.

```bash
ollama pull gpt-oss:20b
```

---

### Google Gemma 3 (4B / 12B)
Strong on instruction following and coding, runs well on Apple Silicon. Well-resourced backing from Google with frequent updates.

```bash
ollama pull gemma3:12b
```

---

## 📊 Hardware Quick-Reference

| Model | VRAM Needed | Best For |
|---|---|---|
| Llama 3.2 3B | ~3 GB | Ultra-light, fast autocomplete |
| Qwen2.5-Coder 7B | ~6 GB | Best coding/VRAM ratio |
| Mistral NeMo 12B | ~8 GB | Balanced everyday coding, 128k context |
| StarCoder2 15B | ~10 GB | Code-only, fine-tuning |
| Mistral Small 3 24B | ~14 GB | High quality, single GPU |
| Codestral 22B | ~14 GB | Code specialist, long context |
| Qwen3-Coder 30B MoE | ~20 GB | Repo-level, agentic tasks |
| Qwen2.5-Coder 32B | ~22 GB | Near-GPT-4 quality local |

> **Recommended starting point:** Qwen2.5-Coder 7B or 14B for most machines.
> Mistral NeMo is a strong runner-up with broader capability and a massive 128k context window.

---

## 🔧 Stack Context

These models are evaluated in the context of:
- **Ollama** — local model runner (Windows / Mac plug-and-play)
- **Continue.dev** — VS Code extension (disable telemetry on first launch)
- **MLflow** — local experiment tracking (`mlflow server --host 127.0.0.1`)

All models run fully on-device with zero external calls once downloaded.
